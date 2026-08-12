#!/usr/bin/env python3
"""
Replication Gate — independent holdout-only reimplementation.

Written from scratch by a third, independent agent, using ONLY:
  - PREREGISTRATION.md (Section 4, the locked test statistic)
  - data/PROVENANCE.md (data source + g_bar/g_obs formula)
  - 03_REPLICATION_GATE/PROTOCOL.md (2026-08-12 clarification: rerun the
    EXACT SAME Section-4 statistic, holdout-only, never combined with
    discovery, never a new criterion)

This script was written and run BEFORE reading run_preregistered_analysis.py,
adversarial_reproduction.py, result_primary.json, or result_adversarial.json.

Only reads discovery_holdout_split.json's "holdout_galaxies" (55 galaxies) —
the discovery_galaxies list is never touched here.
"""
import json
import math
import os

import numpy as np
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Constants (Section 2 of PREREGISTRATION.md / PROVENANCE.md)
# ---------------------------------------------------------------------------
KPC_TO_M = 3.0856775814913673e19
KMS_TO_MS = 1000.0
UPSILON_DISK = 0.50
UPSILON_BUL = 0.7

A0_A = 1.0824e-10  # Holographic Bridge: c*H0/(2*pi)
A0_B = 6.8009e-10  # MOND Emergence: c*H0

BASE = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS"
SPLIT_PATH = os.path.join(BASE, "COSMOLOGY_A0_DERIVATION/data/discovery_holdout_split.json")
ROTMOD_DIR = os.path.join(BASE, "COSMOLOGY_MOND_SPARC/data/Rotmod_LTG")

SEED = 20260812  # fixed seed for the bootstrap, reported per Gate task instructions
N_BOOTSTRAP = 1000


def load_holdout_names():
    with open(SPLIT_PATH) as f:
        d = json.load(f)
    return d["holdout_galaxies"], d


def read_rotmod(name):
    """Read <name>_rotmod.dat: 3 comment lines then
    Rad[kpc] Vobs[km/s] errV Vgas[km/s] Vdisk[km/s] Vbul[km/s] SBdisk SBbul
    Returns arrays of g_bar, g_obs in SI units (m/s^2), and count excluded.
    """
    path = os.path.join(ROTMOD_DIR, f"{name}_rotmod.dat")
    rows = []
    with open(path) as f:
        lines = f.readlines()
    data_lines = [ln for ln in lines if not ln.strip().startswith("#") and ln.strip()]
    for ln in data_lines:
        parts = ln.split()
        rows.append([float(x) for x in parts[:6]])  # Rad,Vobs,errV,Vgas,Vdisk,Vbul
    rows = np.array(rows)
    r_kpc = rows[:, 0]
    vobs = rows[:, 1]
    vgas = rows[:, 3]
    vdisk = rows[:, 4]
    vbul = rows[:, 5]

    # sign-preserving quadrature, PREREGISTRATION.md Section 2
    vbar2 = (
        UPSILON_DISK * vdisk * np.abs(vdisk)
        + UPSILON_BUL * vbul * np.abs(vbul)
        + vgas * np.abs(vgas)
    )  # (km/s)^2, signed

    n_total = len(vbar2)
    keep = vbar2 > 0
    n_excluded = n_total - int(keep.sum())

    r_m = r_kpc[keep] * KPC_TO_M
    vbar2_si = vbar2[keep] * (KMS_TO_MS ** 2)  # (m/s)^2
    vobs2_si = (vobs[keep] * KMS_TO_MS) ** 2

    g_bar = vbar2_si / r_m
    g_obs = vobs2_si / r_m

    return g_bar, g_obs, n_total, n_excluded


def rar_model_scaled(g_bar_scaled, gdag_scaled):
    """g_obs/1e-10 = (g_bar/1e-10) / (1 - exp(-sqrt( (g_bar/1e-10) / (gdag/1e-10) )))"""
    return g_bar_scaled / (1.0 - np.exp(-np.sqrt(g_bar_scaled / gdag_scaled)))


def fit_gdagger(g_bar, g_obs, p0_scaled):
    """Fit on data pre-scaled by 1e-10 (both g_bar, g_obs, and gdag guess)."""
    SCALE = 1e-10
    gb_s = g_bar / SCALE
    go_s = g_obs / SCALE
    popt, pcov = curve_fit(rar_model_scaled, gb_s, go_s, p0=[p0_scaled], maxfev=20000)
    return popt[0] * SCALE  # back to SI


def fit_gdagger_galaxies(galaxy_data, p0_scaled):
    """galaxy_data: list of (g_bar, g_obs) arrays per galaxy. Pool and fit."""
    if not galaxy_data:
        return None
    g_bar_all = np.concatenate([gb for gb, go in galaxy_data])
    g_obs_all = np.concatenate([go for gb, go in galaxy_data])
    if len(g_bar_all) < 3:
        return None
    return fit_gdagger(g_bar_all, g_obs_all, p0_scaled)


def main():
    holdout_names, split_meta = load_holdout_names()
    assert len(holdout_names) == 55, f"expected 55 holdout galaxies, got {len(holdout_names)}"

    galaxy_data = {}
    n_points_total = 0
    n_excluded_total = 0
    missing = []
    for name in holdout_names:
        path = os.path.join(ROTMOD_DIR, f"{name}_rotmod.dat")
        if not os.path.exists(path):
            missing.append(name)
            continue
        g_bar, g_obs, n_total, n_excluded = read_rotmod(name)
        galaxy_data[name] = (g_bar, g_obs)
        n_points_total += n_total
        n_excluded_total += n_excluded

    if missing:
        raise RuntimeError(f"Missing rotmod files for holdout galaxies: {missing}")

    n_points_used = n_points_total - n_excluded_total

    # ---- Point estimate: pooled fit across all 55 holdout galaxies ----
    all_data = list(galaxy_data.values())
    g_bar_all = np.concatenate([gb for gb, go in all_data])
    g_obs_all = np.concatenate([go for gb, go in all_data])

    # Convergence check: two different reasonable initial guesses (in units of 1e-10)
    guess1 = 1.2   # literature value
    guess2 = 3.0   # a different, less "obvious" guess
    fit1 = fit_gdagger(g_bar_all, g_obs_all, guess1)
    fit2 = fit_gdagger(g_bar_all, g_obs_all, guess2)
    rel_diff = abs(fit1 - fit2) / fit1
    converged = rel_diff < 1e-3
    if not converged:
        raise RuntimeError(
            f"Fit did NOT converge robustly: p0=1.2e-10 -> {fit1:.6e}, "
            f"p0=3.0e-10 -> {fit2:.6e}, rel_diff={rel_diff:.4%}"
        )
    gdagger_point = fit1

    # A third guess far off, for extra paranoia
    guess3 = 10.0
    fit3 = fit_gdagger(g_bar_all, g_obs_all, guess3)
    rel_diff_3 = abs(fit3 - gdagger_point) / gdagger_point

    # ---- Diagnostic only (NOT part of the decision criterion, Section 4/5
    # of PREREGISTRATION.md is followed literally above): quantify how much
    # of the pooled unweighted sum-of-squares is dominated by a handful of
    # high-g_bar (high-surface-brightness) galaxies. Reported for
    # transparency about WHY the holdout point estimate differs from the
    # discovery-sample point estimate; does not change the verdict logic.
    per_galaxy_max_gbar = {name: gb.max() for name, (gb, go) in galaxy_data.items()}
    top3_names = sorted(per_galaxy_max_gbar, key=per_galaxy_max_gbar.get, reverse=True)[:3]
    sumsq_total = float(np.sum(g_bar_all ** 2))
    sumsq_top3 = float(np.sum(np.concatenate([galaxy_data[n][0] for n in top3_names]) ** 2))
    top3_leverage_share = sumsq_top3 / sumsq_total

    # ---- Bootstrap 95% CI, galaxy-level resampling ----
    rng = np.random.default_rng(SEED)
    names_arr = list(galaxy_data.keys())
    n_gal = len(names_arr)
    boot_estimates = []
    n_boot_failed = 0
    for i in range(N_BOOTSTRAP):
        sample_idx = rng.integers(0, n_gal, size=n_gal)
        sample_names = [names_arr[j] for j in sample_idx]
        sample_data = [galaxy_data[n] for n in sample_names]
        try:
            est = fit_gdagger_galaxies(sample_data, p0_scaled=gdagger_point / 1e-10)
            if est is not None and np.isfinite(est) and est > 0:
                boot_estimates.append(est)
            else:
                n_boot_failed += 1
        except Exception:
            n_boot_failed += 1

    boot_estimates = np.array(boot_estimates)
    ci_lo, ci_hi = np.percentile(boot_estimates, [2.5, 97.5])

    a0_A_in_ci = ci_lo <= A0_A <= ci_hi
    a0_B_in_ci = ci_lo <= A0_B <= ci_hi

    if not a0_A_in_ci and not a0_B_in_ci:
        verdict_pattern = "BOTH_FALSIFIED"
    elif a0_A_in_ci and a0_B_in_ci:
        verdict_pattern = "BOTH_SURVIVE_INCONCLUSIVE"
    elif a0_A_in_ci and not a0_B_in_ci:
        verdict_pattern = "H_A_SURVIVES_H_B_FALSIFIED"
    else:
        verdict_pattern = "H_B_SURVIVES_H_A_FALSIFIED"

    # Compare with discovery-sample verdict (H_A survives, H_B falsified)
    discovery_verdict = "H_A_SURVIVES_H_B_FALSIFIED"
    if verdict_pattern == discovery_verdict:
        gate_verdict = "REPLICATION_PASSED"
    elif verdict_pattern in ("BOTH_SURVIVE_INCONCLUSIVE", "BOTH_FALSIFIED"):
        gate_verdict = "REPLICATION_FAILED_INCONCLUSIVE"
    else:
        gate_verdict = "REPLICATION_FAILED_CONTRADICTS"

    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-002",
        "gate_role": "independent_third_agent_holdout_replication",
        "data_scope": "holdout_galaxies_ONLY (55 galaxies) — discovery_galaxies never read",
        "split_file_seed": split_meta["seed"],
        "n_holdout_galaxies": len(holdout_names),
        "n_points_total_before_exclusion": int(n_points_total),
        "n_points_excluded_vbar2_le_0": int(n_excluded_total),
        "n_points_used_in_fit": int(n_points_used),
        "gdagger_point_estimate_SI": gdagger_point,
        "convergence_check": {
            "p0_1_scaled_1e-10": guess1,
            "fit1_SI": fit1,
            "p0_2_scaled_1e-10": guess2,
            "fit2_SI": fit2,
            "rel_diff_1_2": rel_diff,
            "p0_3_scaled_1e-10": guess3,
            "fit3_SI": fit3,
            "rel_diff_1_3": rel_diff_3,
            "converged": bool(converged),
        },
        "bootstrap": {
            "seed": SEED,
            "n_replicates_requested": N_BOOTSTRAP,
            "n_replicates_succeeded": int(len(boot_estimates)),
            "n_replicates_failed": int(n_boot_failed),
            "resampling_unit": "galaxy (with replacement, n=55 per replicate)",
        },
        "ci_95_SI": [float(ci_lo), float(ci_hi)],
        "a0_A": A0_A,
        "a0_A_label": "Holographic Bridge, c*H0/(2*pi)",
        "a0_A_in_ci_95": bool(a0_A_in_ci),
        "a0_B": A0_B,
        "a0_B_label": "MOND Emergence, c*H0",
        "a0_B_in_ci_95": bool(a0_B_in_ci),
        "verdict_pattern_holdout": verdict_pattern,
        "discovery_sample_verdict_pattern": discovery_verdict,
        "gate_verdict": gate_verdict,
        "sanity_check_literature_gdagger": {
            "literature_value_SI": 1.20e-10,
            "fitted_value_SI": gdagger_point,
            "pct_diff": abs(gdagger_point - 1.20e-10) / 1.20e-10,
        },
        "diagnostic_leverage_concentration_NOT_part_of_decision_criterion": {
            "note": (
                "Informational only. PREREGISTRATION.md Section 4's pooled "
                "unweighted nonlinear least-squares statistic was followed "
                "literally with no modification; this field explains WHY the "
                "holdout point estimate differs from the discovery-sample "
                "point estimate, it does not alter the verdict above."
            ),
            "top3_highest_gbar_galaxies": top3_names,
            "top3_share_of_pooled_sum_of_squares_gbar2": top3_leverage_share,
        },
    }

    out_path = os.path.join(
        BASE, "COSMOLOGY_A0_DERIVATION/analysis/result_gate_holdout.json"
    )
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
