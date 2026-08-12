#!/usr/bin/env python3
"""
Independent adversarial reproduction of DISC-COSMOLOGY-MOND-SPARC-002.

Written FROM SCRATCH, without reading run_preregistered_analysis.py or
result_primary.json, using only PREREGISTRATION.md and PROVENANCE.md as
the spec. Uses ONLY the 120 discovery_galaxies; never reads holdout_galaxies.

Model:  g_obs = g_bar / (1 - exp(-sqrt(g_bar/g_dagger)))
V_bar^2 = 0.50*Vdisk*|Vdisk| + 0.7*Vbul*|Vbul| + Vgas*|Vgas|   (sign-preserving)
"""
import json
import numpy as np
from scipy.optimize import curve_fit

KPC_TO_M = 3.0856775814913673e19
KMS_TO_MS = 1000.0

UPS_DISK = 0.50
UPS_BUL = 0.7

BASE = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS"
SPLIT_PATH = f"{BASE}/COSMOLOGY_A0_DERIVATION/data/discovery_holdout_split.json"
ROTMOD_DIR = f"{BASE}/COSMOLOGY_MOND_SPARC/data/Rotmod_LTG"

SEED = 42  # bootstrap seed (declared, arbitrary)
N_BOOT = 1000


def sgn_sq(v):
    """sign-preserving quadrature term: v*|v|"""
    return v * np.abs(v)


def load_galaxy(name):
    path = f"{ROTMOD_DIR}/{name}_rotmod.dat"
    data = np.loadtxt(path, comments="#")
    # columns: Rad[kpc], Vobs[km/s], errV, Vgas[km/s], Vdisk[km/s], Vbul[km/s], SBdisk, SBbul
    rad = data[:, 0]
    vobs = data[:, 1]
    vgas = data[:, 3]
    vdisk = data[:, 4]
    vbul = data[:, 5]

    vbar2 = UPS_DISK * sgn_sq(vdisk) + UPS_BUL * sgn_sq(vbul) + sgn_sq(vgas)  # (km/s)^2

    mask = vbar2 > 0
    n_excluded = int((~mask).sum())

    r_m = rad[mask] * KPC_TO_M
    vbar2_si = vbar2[mask] * (KMS_TO_MS ** 2)
    vobs_si = vobs[mask] * KMS_TO_MS

    g_bar = vbar2_si / r_m
    g_obs = (vobs_si ** 2) / r_m

    return g_bar, g_obs, n_excluded


def rar_model(g_bar, g_dagger):
    return g_bar / (1.0 - np.exp(-np.sqrt(g_bar / g_dagger)))


def fit_g_dagger_scaled(g_bar, g_obs, p0_scaled=1.0):
    """
    Fit in rescaled units (g / 1e-10) to avoid the finite-difference Jacobian
    underflow that occurs when fitting raw SI values (~1e-10) with default
    curve_fit step sizes. Returns g_dagger in SI units, plus convergence info.
    """
    SCALE = 1e-10
    gb = g_bar / SCALE
    go = g_obs / SCALE

    def model_scaled(gb_, gd_scaled):
        return gb_ / (1.0 - np.exp(-np.sqrt(gb_ / gd_scaled)))

    popt, pcov = curve_fit(model_scaled, gb, go, p0=[p0_scaled], maxfev=20000)
    gd_scaled = popt[0]
    gd_si = gd_scaled * SCALE

    # residuals check
    pred = model_scaled(gb, gd_scaled)
    rel_resid = np.abs(pred - go) / np.abs(go)
    median_rel_resid = np.median(rel_resid)

    return gd_si, median_rel_resid


def main():
    with open(SPLIT_PATH) as f:
        split = json.load(f)

    discovery = split["discovery_galaxies"]
    assert len(discovery) == 120, f"expected 120 discovery galaxies, got {len(discovery)}"
    # Explicitly do NOT touch split["holdout_galaxies"] anywhere below.

    all_g_bar = []
    all_g_obs = []
    total_excluded = 0
    per_galaxy = {}  # name -> (g_bar array, g_obs array) for bootstrap

    for name in discovery:
        g_bar, g_obs, n_exc = load_galaxy(name)
        total_excluded += n_exc
        all_g_bar.append(g_bar)
        all_g_obs.append(g_obs)
        per_galaxy[name] = (g_bar, g_obs)

    all_g_bar = np.concatenate(all_g_bar)
    all_g_obs = np.concatenate(all_g_obs)
    n_points = len(all_g_bar)

    print(f"N discovery galaxies: {len(discovery)}")
    print(f"N points pooled: {n_points}")
    print(f"N points excluded (g_bar<=0): {total_excluded}")

    # --- Convergence verification: try multiple initial guesses ---
    guesses_scaled = [0.1, 1.0, 5.0, 10.0, 50.0]
    results = []
    for p0 in guesses_scaled:
        gd, med_resid = fit_g_dagger_scaled(all_g_bar, all_g_obs, p0_scaled=p0)
        results.append((p0, gd, med_resid))
        print(f"  p0_scaled={p0:6.2f}  -> g_dagger={gd:.6e}  median_rel_resid={med_resid:.4f}")

    gd_vals = np.array([r[1] for r in results])
    spread = (gd_vals.max() - gd_vals.min()) / np.median(gd_vals)
    print(f"Relative spread across initial guesses: {spread:.6f}")
    assert spread < 1e-3, "FIT DID NOT CONVERGE CONSISTENTLY across initial guesses!"

    g_dagger_point = float(np.median(gd_vals))
    median_rel_resid_point = float(np.median([r[2] for r in results]))
    print(f"g_dagger point estimate (linear-space fit): {g_dagger_point:.6e}")
    print(f"median relative residual: {median_rel_resid_point:.4f}")

    # Sanity: point estimate should be same order of magnitude as literature 1.2e-10
    assert 1e-11 < g_dagger_point < 1e-9, "g_dagger point estimate outside plausible order of magnitude!"

    # --- Log-space fit (robustness check, not pre-registered) ---
    def log_resid(log_gd, g_bar, g_obs):
        gd = np.exp(log_gd)
        pred = rar_model(g_bar, gd)
        return np.log10(pred) - np.log10(g_obs)

    from scipy.optimize import least_squares
    # use scaled units here too for numerical stability
    SCALE = 1e-10
    gb_s = all_g_bar / SCALE
    go_s = all_g_obs / SCALE

    def log_resid_scaled(log_gd_scaled):
        gd_s = np.exp(log_gd_scaled)
        pred = gb_s / (1.0 - np.exp(-np.sqrt(gb_s / gd_s)))
        return np.log10(pred) - np.log10(go_s)

    res_log = least_squares(log_resid_scaled, x0=[np.log(1.0)])
    g_dagger_logspace = float(np.exp(res_log.x[0]) * SCALE)
    log_resid_final = log_resid_scaled(res_log.x)
    log_dex_scatter = float(np.std(log_resid_final))
    print(f"g_dagger (log-space fit): {g_dagger_logspace:.6e}, log10 dex scatter: {log_dex_scatter:.4f}")

    # --- Galaxy-level bootstrap ---
    rng = np.random.default_rng(SEED)
    names_arr = np.array(discovery)
    boot_estimates = []
    n_fail = 0
    for i in range(N_BOOT):
        sample_names = rng.choice(names_arr, size=len(names_arr), replace=True)
        gb_list = []
        go_list = []
        for nm in sample_names:
            gb, go = per_galaxy[nm]
            gb_list.append(gb)
            go_list.append(go)
        gb_boot = np.concatenate(gb_list)
        go_boot = np.concatenate(go_list)
        try:
            gd_boot, _ = fit_g_dagger_scaled(gb_boot, go_boot, p0_scaled=1.0)
            if np.isfinite(gd_boot) and 1e-13 < gd_boot < 1e-7:
                boot_estimates.append(gd_boot)
            else:
                n_fail += 1
        except Exception:
            n_fail += 1

    boot_estimates = np.array(boot_estimates)
    print(f"Bootstrap replicates succeeded: {len(boot_estimates)}/{N_BOOT} (failed: {n_fail})")

    ci_lo, ci_hi = np.percentile(boot_estimates, [2.5, 97.5])
    print(f"95% CI (galaxy-level bootstrap, {N_BOOT} reps, seed={SEED}): [{ci_lo:.6e}, {ci_hi:.6e}]")

    a0_A = 6.62607015e-34 * 0  # placeholder, will overwrite below properly
    c = 2.99792458e8
    H0_SI = 70.0 * 1000.0 / (3.0856775814913673e22)  # 70 km/s/Mpc -> 1/s  (1 Mpc = 3.0857e22 m)
    a0_A = c * H0_SI / (2 * np.pi)
    a0_B = c * H0_SI

    print(f"a0_A (cH0/2pi) = {a0_A:.6e} m/s^2")
    print(f"a0_B (cH0)     = {a0_B:.6e} m/s^2")

    HA_survives = ci_lo <= a0_A <= ci_hi
    HB_survives = ci_lo <= a0_B <= ci_hi

    print(f"H_A survives (a0_A in CI): {HA_survives}")
    print(f"H_B survives (a0_B in CI): {HB_survives}")

    if HA_survives and not HB_survives:
        verdict = "H_A_SURVIVES_H_B_FALSIFIED"
    elif HB_survives and not HA_survives:
        verdict = "H_B_SURVIVES_H_A_FALSIFIED"
    elif HA_survives and HB_survives:
        verdict = "INCONCLUSIVE_BOTH_SURVIVE"
    else:
        verdict = "BOTH_FALSIFIED"

    print(f"VERDICT: {verdict}")

    # --- Robustness check D: drop largest-residual outlier galaxy ---
    # compute per-galaxy median relative residual at point estimate g_dagger
    per_galaxy_resid = {}
    for nm in discovery:
        gb, go = per_galaxy[nm]
        pred = rar_model(gb, g_dagger_point)
        rel = np.median(np.abs(pred - go) / np.abs(go))
        per_galaxy_resid[nm] = rel
    worst_galaxy = max(per_galaxy_resid, key=per_galaxy_resid.get)
    print(f"Worst-residual galaxy: {worst_galaxy} (median rel resid={per_galaxy_resid[worst_galaxy]:.4f})")

    discovery_no_outlier = [n for n in discovery if n != worst_galaxy]
    gb_no = np.concatenate([per_galaxy[n][0] for n in discovery_no_outlier])
    go_no = np.concatenate([per_galaxy[n][1] for n in discovery_no_outlier])
    gd_no_outlier, _ = fit_g_dagger_scaled(gb_no, go_no, p0_scaled=1.0)
    print(f"g_dagger point estimate excluding {worst_galaxy}: {gd_no_outlier:.6e}")

    # bootstrap CI excluding outlier (for robustness note only, fewer reps for speed: still 1000 for rigor)
    names_no = np.array(discovery_no_outlier)
    boot_no = []
    per_galaxy_no = {n: per_galaxy[n] for n in discovery_no_outlier}
    rng2 = np.random.default_rng(SEED)
    for i in range(N_BOOT):
        sample_names = rng2.choice(names_no, size=len(names_no), replace=True)
        gb_list = [per_galaxy_no[nm][0] for nm in sample_names]
        go_list = [per_galaxy_no[nm][1] for nm in sample_names]
        gb_b = np.concatenate(gb_list)
        go_b = np.concatenate(go_list)
        try:
            gd_b, _ = fit_g_dagger_scaled(gb_b, go_b, p0_scaled=1.0)
            if np.isfinite(gd_b) and 1e-13 < gd_b < 1e-7:
                boot_no.append(gd_b)
        except Exception:
            pass
    boot_no = np.array(boot_no)
    ci_no_lo, ci_no_hi = np.percentile(boot_no, [2.5, 97.5])
    print(f"95% CI excluding {worst_galaxy}: [{ci_no_lo:.6e}, {ci_no_hi:.6e}]")
    HA_no = ci_no_lo <= a0_A <= ci_no_hi
    HB_no = ci_no_lo <= a0_B <= ci_no_hi
    print(f"Excluding outlier: H_A survives={HA_no}, H_B survives={HB_no}")

    # --- write result JSON ---
    result = {
        "n_discovery_galaxies": len(discovery),
        "n_points_pooled": int(n_points),
        "n_points_excluded": int(total_excluded),
        "g_dagger_point_estimate_linear_space": g_dagger_point,
        "median_relative_residual_linear_space": median_rel_resid_point,
        "g_dagger_logspace_fit": g_dagger_logspace,
        "log10_dex_scatter": log_dex_scatter,
        "bootstrap": {
            "n_replicates_requested": N_BOOT,
            "n_replicates_succeeded": int(len(boot_estimates)),
            "seed": SEED,
            "ci_95": [float(ci_lo), float(ci_hi)],
        },
        "a0_A": a0_A,
        "a0_B": a0_B,
        "H_A_survives": bool(HA_survives),
        "H_B_survives": bool(HB_survives),
        "verdict": verdict,
        "robustness_outlier_exclusion": {
            "worst_galaxy": worst_galaxy,
            "worst_galaxy_median_rel_resid": per_galaxy_resid[worst_galaxy],
            "g_dagger_point_estimate_excl_outlier": gd_no_outlier,
            "ci_95_excl_outlier": [float(ci_no_lo), float(ci_no_hi)],
            "H_A_survives_excl_outlier": bool(HA_no),
            "H_B_survives_excl_outlier": bool(HB_no),
        },
        "convergence_check": {
            "initial_guesses_scaled": [r[0] for r in results],
            "fitted_g_dagger_per_guess": [r[1] for r in results],
            "relative_spread_across_guesses": float(spread),
        },
        "holdout_touched": False,
    }

    out_path = f"{BASE}/COSMOLOGY_A0_DERIVATION/analysis/result_adversarial.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
