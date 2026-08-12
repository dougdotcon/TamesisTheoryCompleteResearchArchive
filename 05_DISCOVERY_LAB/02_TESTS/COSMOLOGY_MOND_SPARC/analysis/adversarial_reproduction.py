#!/usr/bin/env python3
"""
Independent adversarial re-implementation of the pre-registered EFE/SPARC test.

Written from scratch, WITHOUT reading run_preregistered_analysis.py or
result_primary.json first, based solely on:
  - PREREGISTRATION.md (locked hypothesis / null model / test statistic /
    falsification criterion)
  - data/PROVENANCE.md (data file description)
  - direct inspection of the raw data files' actual format

Purpose: try to REFUTE the primary result by independently reproducing (or
failing to reproduce) it, hunting for implementation bugs, and running
robustness/sensitivity checks not covered by the locked pre-registration.

This script does not modify any file under 02_TESTS/COSMOLOGY_MOND_SPARC/
other than writing its own output files (this script itself, and
result_adversarial.json).
"""

import json
import math
import os
import numpy as np
from scipy import stats

BASE = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_MOND_SPARC"
MRT_PATH = os.path.join(BASE, "data", "SPARC_Lelli2016c.mrt")
ROTMOD_DIR = os.path.join(BASE, "data", "Rotmod_LTG")

F_D_CLUSTER_CODE = 4  # "4 = Ursa Major Cluster of Galaxies" per .mrt header note (2)


def parse_mrt(path):
    """Parse SPARC_Lelli2016c.mrt: header lines 1-98 (1-indexed), data from line 99.
    Whitespace-separated columns:
    Galaxy T D e_D f_D Inc e_Inc L e_L Reff SBeff Rdisk SBdisk MHI RHI Vflat e_Vflat Q Ref
    f_D is column index 4 (0-indexed).
    """
    galaxies = []
    with open(path, "r") as f:
        lines = f.readlines()

    # Lines 1-98 (1-indexed) == lines[0:98] (0-indexed) are header/notes.
    # Data starts at line 99 (1-indexed) == lines[98] (0-indexed).
    data_lines = lines[98:]

    for lineno, raw in enumerate(data_lines, start=99):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        # Stop if we hit a trailing separator/footer line (defensive; not expected)
        if line.strip().startswith("---") or line.strip().startswith("==="):
            continue
        parts = line.split()
        if len(parts) < 5:
            raise ValueError(f"Unexpected short line {lineno}: {line!r}")
        galaxy_name = parts[0]
        f_d_raw = parts[4]
        try:
            f_d = int(f_d_raw)
        except ValueError:
            raise ValueError(f"Non-integer f_D {f_d_raw!r} at line {lineno} for {galaxy_name}")
        galaxies.append({"name": galaxy_name, "f_D": f_d, "lineno": lineno})

    return galaxies


def load_rotmod(galaxy_name):
    """Load Rotmod_LTG/<Galaxy>_rotmod.dat -> (r, v) arrays, radius-sorted as-is in file.
    Columns: Rad Vobs errV Vgas Vdisk Vbul SBdisk SBbul
    Lines starting with # are comments/header.
    """
    path = os.path.join(ROTMOD_DIR, f"{galaxy_name}_rotmod.dat")
    if not os.path.exists(path):
        return None, None, path
    r_list = []
    v_list = []
    with open(path, "r") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts = s.split()
            if len(parts) < 2:
                continue
            r_list.append(float(parts[0]))
            v_list.append(float(parts[1]))
    return np.array(r_list, dtype=float), np.array(v_list, dtype=float), path


def outer_slope(r, v):
    """Outer log-log slope per PREREGISTRATION.md Section 4:
    r_outer = r[n//2:], v_outer = v[n//2:] (points as-ordered in file, already
    radius-sorted); slope = polyfit(log(r_outer), log(v_outer), 1)[0].
    Returns (slope, n_total, n_outer, note) where note flags any anomaly
    (e.g. non-positive value fed to log).
    """
    n = len(r)
    r_outer = r[n // 2:]
    v_outer = v[n // 2:]
    n_outer = len(r_outer)
    note = None
    if n_outer < 2:
        return None, n, n_outer, "excluded: <2 outer points"
    if np.any(r_outer <= 0) or np.any(v_outer <= 0):
        note = "WARNING: non-positive value in outer r or v -> log(non-positive)"
        # Do not silently mask -- let it produce nan/-inf/warning naturally like
        # a naive implementation would, so we can detect the bug if present.
    with np.errstate(all="raise"):
        try:
            logr = np.log(r_outer)
            logv = np.log(v_outer)
        except FloatingPointError as e:
            return None, n, n_outer, f"excluded: log() error ({e})"
    if np.any(~np.isfinite(logr)) or np.any(~np.isfinite(logv)):
        return None, n, n_outer, "excluded: non-finite value after log()"
    slope = np.polyfit(logr, logv, 1)[0]
    return slope, n, n_outer, note


def main():
    galaxies = parse_mrt(MRT_PATH)
    assert len(galaxies) == 175, f"Expected 175 galaxies, got {len(galaxies)}"

    n_cluster_catalog = sum(1 for g in galaxies if g["f_D"] == F_D_CLUSTER_CODE)
    n_field_catalog = sum(1 for g in galaxies if g["f_D"] != F_D_CLUSTER_CODE)
    print(f"Catalog: {len(galaxies)} galaxies total; "
          f"f_D==4 (cluster) = {n_cluster_catalog}; f_D!=4 (field) = {n_field_catalog}")

    cluster_slopes = []
    field_slopes = []
    excluded = []
    missing_files = []
    per_galaxy_records = []

    total_points_by_group = {"cluster": [], "field": []}

    for g in galaxies:
        name = g["name"]
        is_cluster = (g["f_D"] == F_D_CLUSTER_CODE)
        group = "cluster" if is_cluster else "field"

        r, v, path = load_rotmod(name)
        if r is None:
            missing_files.append(name)
            continue

        n_total = len(r)
        slope, n_tot_check, n_outer, note = outer_slope(r, v)
        total_points_by_group[group].append(n_total)

        rec = {
            "galaxy": name,
            "f_D": g["f_D"],
            "group": group,
            "n_total_points": n_total,
            "n_outer_points": n_outer,
            "slope": slope,
            "note": note,
        }
        per_galaxy_records.append(rec)

        if slope is None:
            excluded.append(rec)
            continue

        if is_cluster:
            cluster_slopes.append(slope)
        else:
            field_slopes.append(slope)

    cluster_slopes = np.array(cluster_slopes, dtype=float)
    field_slopes = np.array(field_slopes, dtype=float)

    n_cluster = len(cluster_slopes)
    n_field = len(field_slopes)

    mean_cluster = float(np.mean(cluster_slopes))
    mean_field = float(np.mean(field_slopes))
    std_cluster_ddof1 = float(np.std(cluster_slopes, ddof=1))
    std_field_ddof1 = float(np.std(field_slopes, ddof=1))
    std_cluster_ddof0 = float(np.std(cluster_slopes, ddof=0))
    std_field_ddof0 = float(np.std(field_slopes, ddof=0))

    # Welch's t-test (equal_var=False), two-sided p-value from scipy.
    t_stat, p_two_sided = stats.ttest_ind(cluster_slopes, field_slopes, equal_var=False)
    t_stat = float(t_stat)
    p_two_sided = float(p_two_sided)

    # One-sided p-value in EFE-predicted direction: cluster_mean < field_mean.
    # scipy's two-sided p is P(|T| >= |t_obs|) under the null. If t_obs < 0
    # (cluster mean < field mean, i.e. in the predicted direction), the
    # correct one-sided p in that direction is p_two_sided / 2.
    # If t_obs >= 0 (wrong direction), the one-sided p in the predicted
    # direction is > 0.5 (specifically 1 - p_two_sided/2), i.e. NOT supportive.
    if t_stat < 0:
        p_one_sided_efe_direction = p_two_sided / 2.0
    else:
        p_one_sided_efe_direction = 1.0 - p_two_sided / 2.0

    verdict_supports_efe = (mean_cluster < mean_field) and (p_one_sided_efe_direction < 0.05)

    print()
    print(f"N_cluster (with valid slope) = {n_cluster}")
    print(f"N_field   (with valid slope) = {n_field}")
    print(f"mean cluster slope = {mean_cluster:.6f}  (std ddof=1: {std_cluster_ddof1:.6f}, ddof=0: {std_cluster_ddof0:.6f})")
    print(f"mean field   slope = {mean_field:.6f}  (std ddof=1: {std_field_ddof1:.6f}, ddof=0: {std_field_ddof0:.6f})")
    print(f"t-statistic (Welch) = {t_stat:.6f}")
    print(f"two-sided p-value   = {p_two_sided:.6f}")
    print(f"one-sided p-value (EFE direction: cluster<field) = {p_one_sided_efe_direction:.6f}")
    print(f"Verdict: {'SUPPORTS EFE' if verdict_supports_efe else 'DOES NOT SUPPORT EFE'} "
          f"(criterion: cluster_mean<field_mean AND one-sided p<0.05)")
    print()
    print(f"Excluded galaxies (< 2 outer points or log() problem): {len(excluded)}")
    for e in excluded:
        print(f"  {e['galaxy']} (f_D={e['f_D']}, group={e['group']}, "
              f"n_total={e['n_total_points']}, n_outer={e['n_outer_points']}, note={e['note']})")
    print(f"Missing rotmod files: {len(missing_files)} {missing_files}")

    # --- Robustness / sensitivity checks (Section C of adversarial task) ---

    # (1) ddof sanity check already computed above (ddof=0 vs ddof=1 std; does
    # not affect scipy's internal Welch t-test computation, which always uses
    # its own variance estimator regardless of what we separately report).

    # (2) Sanity-check one-sided derivation against an independent one-sided
    # Welch t-test computed via scipy's `alternative` parameter (available in
    # modern scipy), comparing cluster vs field with alternative='less'
    # (i.e. testing cluster_mean < field_mean directly).
    try:
        t_stat_alt, p_one_sided_scipy_native = stats.ttest_ind(
            cluster_slopes, field_slopes, equal_var=False, alternative="less"
        )
        p_one_sided_scipy_native = float(p_one_sided_scipy_native)
        t_stat_alt = float(t_stat_alt)
    except TypeError:
        # Older scipy without `alternative` kwarg.
        t_stat_alt, p_one_sided_scipy_native = None, None

    # (3) Thin-data galaxies: total points < 4 (per group), and result if
    # those galaxies are excluded from BOTH groups. This is a robustness
    # note only -- NOT a new pre-registered result.
    thin_cluster = [r for r in per_galaxy_records
                    if r["group"] == "cluster" and r["n_total_points"] < 4]
    thin_field = [r for r in per_galaxy_records
                  if r["group"] == "field" and r["n_total_points"] < 4]

    thin_names = set(r["galaxy"] for r in thin_cluster + thin_field)
    cluster_slopes_no_thin = np.array(
        [r["slope"] for r in per_galaxy_records
         if r["group"] == "cluster" and r["galaxy"] not in thin_names and r["slope"] is not None],
        dtype=float,
    )
    field_slopes_no_thin = np.array(
        [r["slope"] for r in per_galaxy_records
         if r["group"] == "field" and r["galaxy"] not in thin_names and r["slope"] is not None],
        dtype=float,
    )
    n_cluster_no_thin = len(cluster_slopes_no_thin)
    n_field_no_thin = len(field_slopes_no_thin)
    if n_cluster_no_thin >= 2 and n_field_no_thin >= 2:
        mean_cluster_no_thin = float(np.mean(cluster_slopes_no_thin))
        mean_field_no_thin = float(np.mean(field_slopes_no_thin))
        t_stat_no_thin, p_two_sided_no_thin = stats.ttest_ind(
            cluster_slopes_no_thin, field_slopes_no_thin, equal_var=False
        )
        t_stat_no_thin = float(t_stat_no_thin)
        p_two_sided_no_thin = float(p_two_sided_no_thin)
        if t_stat_no_thin < 0:
            p_one_sided_no_thin = p_two_sided_no_thin / 2.0
        else:
            p_one_sided_no_thin = 1.0 - p_two_sided_no_thin / 2.0
        verdict_no_thin = (mean_cluster_no_thin < mean_field_no_thin) and (p_one_sided_no_thin < 0.05)
    else:
        mean_cluster_no_thin = mean_field_no_thin = None
        t_stat_no_thin = p_two_sided_no_thin = p_one_sided_no_thin = None
        verdict_no_thin = None

    print()
    print("--- Robustness checks ---")
    print(f"(2) scipy native one-sided (alternative='less') t={t_stat_alt}, p={p_one_sided_scipy_native}")
    print(f"    Manual halving p={p_one_sided_efe_direction:.6f} -- "
          f"{'MATCHES' if (p_one_sided_scipy_native is not None and abs(p_one_sided_scipy_native - p_one_sided_efe_direction) < 1e-9) else 'CHECK'}")
    print(f"(3a) Galaxies with <4 TOTAL rotmod points (literal reading of the task): "
          f"cluster={len(thin_cluster)} field={len(thin_field)}")
    for r in thin_cluster + thin_field:
        print(f"    {r['galaxy']} group={r['group']} n_total={r['n_total_points']} n_outer={r['n_outer_points']} slope={r['slope']}")
    print(f"    Excluding thin-data galaxies (<4 total pts): N_cluster={n_cluster_no_thin}, N_field={n_field_no_thin}")
    print(f"    mean_cluster={mean_cluster_no_thin}, mean_field={mean_field_no_thin}")
    print(f"    t={t_stat_no_thin}, one-sided p={p_one_sided_no_thin}, verdict_supports_efe={verdict_no_thin}")

    # (3b) Extended check: this dataset happens to have NO galaxy with <4 total
    # points, but it DOES have galaxies sitting exactly at the pre-registered
    # minimum (n_outer == 2, the smallest outer-half size the pre-registration
    # allows before exclusion). A 2-point log-log "fit" is not a fit at all --
    # it is a line drawn exactly through 2 points, zero residual, maximal
    # leverage on the group mean/variance. Check sensitivity to these.
    boundary_records = [r for r in per_galaxy_records
                         if r["n_outer_points"] == 2 and r["slope"] is not None]
    boundary_names = set(r["galaxy"] for r in boundary_records)
    cluster_slopes_no_boundary = np.array(
        [r["slope"] for r in per_galaxy_records
         if r["group"] == "cluster" and r["galaxy"] not in boundary_names and r["slope"] is not None],
        dtype=float,
    )
    field_slopes_no_boundary = np.array(
        [r["slope"] for r in per_galaxy_records
         if r["group"] == "field" and r["galaxy"] not in boundary_names and r["slope"] is not None],
        dtype=float,
    )
    n_cluster_nb = len(cluster_slopes_no_boundary)
    n_field_nb = len(field_slopes_no_boundary)
    mean_cluster_nb = float(np.mean(cluster_slopes_no_boundary))
    mean_field_nb = float(np.mean(field_slopes_no_boundary))
    t_stat_nb, p_two_sided_nb = stats.ttest_ind(
        cluster_slopes_no_boundary, field_slopes_no_boundary, equal_var=False
    )
    t_stat_nb = float(t_stat_nb)
    p_two_sided_nb = float(p_two_sided_nb)
    p_one_sided_nb = p_two_sided_nb / 2.0 if t_stat_nb < 0 else 1.0 - p_two_sided_nb / 2.0
    verdict_nb = (mean_cluster_nb < mean_field_nb) and (p_one_sided_nb < 0.05)

    print(f"(3b) Galaxies at the pre-registration's minimum allowed outer-half size "
          f"(n_outer==2, i.e. a 2-point 'fit'): {len(boundary_records)}")
    for r in boundary_records:
        print(f"    {r['galaxy']} group={r['group']} n_total={r['n_total_points']} slope={r['slope']}")
    print(f"    Excluding these {len(boundary_records)} boundary galaxies: "
          f"N_cluster={n_cluster_nb}, N_field={n_field_nb}")
    print(f"    mean_cluster={mean_cluster_nb:.6f}, mean_field={mean_field_nb:.6f}")
    print(f"    t={t_stat_nb:.6f}, one-sided p={p_one_sided_nb:.6f}, verdict_supports_efe={verdict_nb}")

    result = {
        "script": "adversarial_reproduction.py",
        "independent_from": "run_preregistered_analysis.py (not read before writing this script)",
        "catalog": {
            "n_galaxies_total": len(galaxies),
            "n_cluster_f_D_eq_4_catalog": n_cluster_catalog,
            "n_field_f_D_ne_4_catalog": n_field_catalog,
        },
        "primary_test": {
            "n_cluster": n_cluster,
            "n_field": n_field,
            "mean_cluster_slope": mean_cluster,
            "mean_field_slope": mean_field,
            "std_cluster_slope_ddof1": std_cluster_ddof1,
            "std_field_slope_ddof1": std_field_ddof1,
            "std_cluster_slope_ddof0": std_cluster_ddof0,
            "std_field_slope_ddof0": std_field_ddof0,
            "t_statistic_welch": t_stat,
            "p_two_sided": p_two_sided,
            "p_one_sided_efe_direction": p_one_sided_efe_direction,
            "verdict_supports_efe_per_preregistration": verdict_supports_efe,
        },
        "excluded_galaxies": [
            {"galaxy": e["galaxy"], "group": e["group"], "f_D": e["f_D"],
             "n_total_points": e["n_total_points"], "n_outer_points": e["n_outer_points"],
             "note": e["note"]}
            for e in excluded
        ],
        "missing_rotmod_files": missing_files,
        "robustness_checks": {
            "scipy_native_one_sided_alternative_less": {
                "t_statistic": t_stat_alt,
                "p_value": p_one_sided_scipy_native,
                "matches_manual_halving": (
                    p_one_sided_scipy_native is not None
                    and abs(p_one_sided_scipy_native - p_one_sided_efe_direction) < 1e-9
                ),
            },
            "thin_data_galaxies_lt_4_total_points": {
                "n_cluster_thin": len(thin_cluster),
                "n_field_thin": len(thin_field),
                "thin_galaxies": [
                    {"galaxy": r["galaxy"], "group": r["group"],
                     "n_total_points": r["n_total_points"], "n_outer_points": r["n_outer_points"],
                     "slope": r["slope"]}
                    for r in (thin_cluster + thin_field)
                ],
                "result_excluding_thin_galaxies": {
                    "n_cluster": n_cluster_no_thin,
                    "n_field": n_field_no_thin,
                    "mean_cluster_slope": mean_cluster_no_thin,
                    "mean_field_slope": mean_field_no_thin,
                    "t_statistic_welch": t_stat_no_thin,
                    "p_one_sided_efe_direction": p_one_sided_no_thin,
                    "verdict_supports_efe_per_preregistration": verdict_no_thin,
                },
                "note": "Informational robustness note only, per adversarial review instructions. "
                        "This is NOT a new pre-registered result and must not be presented as "
                        "confirming or refuting the hypothesis on its own.",
            },
            "boundary_two_point_fit_galaxies": {
                "description": "Galaxies at the pre-registration's own minimum allowed "
                                "outer-half size (n_outer==2): a 2-point log-log 'fit' has "
                                "zero residual and maximal leverage. All 4 such galaxies in "
                                "this dataset happen to fall in the field group.",
                "n_boundary_galaxies": len(boundary_records),
                "boundary_galaxies": [
                    {"galaxy": r["galaxy"], "group": r["group"],
                     "n_total_points": r["n_total_points"], "slope": r["slope"]}
                    for r in boundary_records
                ],
                "result_excluding_boundary_galaxies": {
                    "n_cluster": n_cluster_nb,
                    "n_field": n_field_nb,
                    "mean_cluster_slope": mean_cluster_nb,
                    "mean_field_slope": mean_field_nb,
                    "t_statistic_welch": t_stat_nb,
                    "p_one_sided_efe_direction": p_one_sided_nb,
                    "verdict_supports_efe_per_preregistration": verdict_nb,
                },
                "note": "Informational robustness note only, per adversarial review "
                        "instructions. NOT a new pre-registered result. Flags that the "
                        "primary p=0.0494 result is sensitive to exactly 4 field galaxies "
                        "with only 2 outer-half points each.",
            },
        },
        "per_galaxy_records": per_galaxy_records,
    }

    out_path = os.path.join(BASE, "analysis", "result_adversarial.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=lambda o: None)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
