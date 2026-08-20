"""
Adversarial reproduction / null-discovery check for the Kilauea
`spectral_gap` finding (p=0.0 in BOTH primary and robust variants),
per AGENTS.md step 7 / this line's mandatory-if-p<0.05 discipline.

Runs, with a REDUCED n_mc=50 (exploratory/adversarial checks, not the
confirmatory primary test -- the locked N_SURROGATES=200 result already
stands in result_kilauea_{primary,robust}.json and is NOT recomputed
here):

  (a) Placebo split-within-PRE: splits the real PRE segment (no genuine
      transition) at its midpoint and runs the SAME pipeline. Tests
      whether ANY arbitrary split of a long real seismic series produces
      a similarly large spectral_gap jump (would indicate a generic
      property of this domain/length, not something specific to the true
      eruption transition).
  (b) M6.9-exclusion: truncates the PRIMARY POST segment to end 6h before
      the M6.9 south-flank earthquake (2018-05-04T22:32:54 UTC), removing
      the mainshock's strong-motion signal directly, and re-runs PRE vs.
      this truncated POST. Tests whether the spectral_gap effect (and its
      LARGE magnitude specifically in the primary variant) depends on the
      mainshock being inside the window.
  (c) Bootstrap corroboration (reduced n_bootstrap=50): moving-block
      bootstrap (Kunsch 1989), pre-authorized fallback significance test,
      run on the ALREADY-COMPUTED real PRE/POST features for both
      variants, to check whether an alternative significance method
      corroborates IAAFT's p=0.0 (mirrors the exact adversarial check
      that broke lempel_ziv_complexity's Daphnet finding in this line).
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dmd_common import run_dmd_analysis, run_block_bootstrap_test_dmd, compute_dmd_features, SEED

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rqa", "analysis")
)
from rqa_common import subsample_segment  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "confound_check_kilauea_results.json")

N_MC_CHECK = 50
FS_HZ = 100.0
SIX_HOURS_SAMPLES = int(6 * 3600 * FS_HZ)


def _to_jsonable(obj):
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}
    if isinstance(obj, np.ndarray):
        return _to_jsonable(obj.tolist())
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def _strip_heavy(result):
    if result is None:
        return None
    keep_keys = [
        "status", "tau", "d", "delta_f_dom", "delta_zeta", "delta_spectral_gap",
        "p_f_dom", "p_zeta", "p_spectral_gap",
        "f_dom_pre", "f_dom_post", "zeta_pre", "zeta_post",
        "spectral_gap_pre", "spectral_gap_post",
        "real_dominant_rate_pre", "real_dominant_rate_post",
        "surrogate_gap_n_valid", "surrogate_gap_n_undefined",
        "diagnostics", "config",
    ]
    out = {}
    for k in keep_keys:
        if k in result:
            out[k] = result[k]
    for side in ("real_pre", "real_post"):
        r = result.get(side)
        if isinstance(r, dict):
            out[side] = {
                "status": r.get("status"), "rank_info": r.get("rank_info"),
                "n_complex_pairs": r.get("n_complex_pairs"), "n_real_modes": r.get("n_real_modes"),
            }
    return out


def check_a_placebo_split_within_pre():
    print("=== (a) Placebo split-within-PRE (no real transition) ===", flush=True)
    pre_full = np.load(os.path.join(DATA_DIR, "kilauea_pre_primary.npy"))
    n = len(pre_full)
    half = n // 2
    placebo_pre = pre_full[:half]
    placebo_post = pre_full[half:]
    print(f"placebo_pre n={len(placebo_pre)} placebo_post n={len(placebo_post)}", flush=True)
    t0 = time.time()
    result = run_dmd_analysis(placebo_pre, placebo_post, seed=SEED, n_mc=N_MC_CHECK)
    elapsed = time.time() - t0
    print(f"[placebo] status={result['status']} elapsed={elapsed:.1f}s", flush=True)
    if result["status"] == "ok":
        print(f"[placebo] spectral_gap: PRE={result['spectral_gap_pre']} POST={result['spectral_gap_post']} "
              f"delta={result['delta_spectral_gap']} p={result['p_spectral_gap']}", flush=True)
    return {"result": _strip_heavy(result), "wall_clock_seconds": elapsed,
            "n_pre": int(len(placebo_pre)), "n_post": int(len(placebo_post))}


def check_b_m69_exclusion():
    print("\n=== (b) M6.9-exclusion (truncate PRIMARY POST 6h before mainshock) ===", flush=True)
    pre = np.load(os.path.join(DATA_DIR, "kilauea_pre_primary.npy"))
    post_full = np.load(os.path.join(DATA_DIR, "kilauea_post_primary.npy"))
    post_truncated = post_full[:-SIX_HOURS_SAMPLES]
    print(f"pre n={len(pre)} post_truncated n={len(post_truncated)} "
          f"(full post was {len(post_full)}, removed last {SIX_HOURS_SAMPLES} samples = 6h)", flush=True)
    t0 = time.time()
    result = run_dmd_analysis(pre, post_truncated, seed=SEED, n_mc=N_MC_CHECK)
    elapsed = time.time() - t0
    print(f"[m69_excl] status={result['status']} elapsed={elapsed:.1f}s", flush=True)
    if result["status"] == "ok":
        print(f"[m69_excl] spectral_gap: PRE={result['spectral_gap_pre']} POST={result['spectral_gap_post']} "
              f"delta={result['delta_spectral_gap']} p={result['p_spectral_gap']}", flush=True)
    return {"result": _strip_heavy(result), "wall_clock_seconds": elapsed,
            "n_pre": int(len(pre)), "n_post": int(len(post_truncated))}


def check_c_bootstrap_corroboration(variant):
    print(f"\n=== (c) Bootstrap corroboration, variant={variant} (n_bootstrap=50) ===", flush=True)
    pre_raw = np.load(os.path.join(DATA_DIR, f"kilauea_pre_{variant}.npy"))
    post_raw = np.load(os.path.join(DATA_DIR, f"kilauea_post_{variant}.npy"))
    pre, _ = subsample_segment(pre_raw, max_n=200000)
    post, _ = subsample_segment(post_raw, max_n=200000)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            f"result_kilauea_{variant}.json")) as f:
        locked_result = json.load(f)
    tau, d = locked_result["tau"], locked_result["d"]
    print(f"reusing LOCKED (tau={tau}, d={d}) from result_kilauea_{variant}.json", flush=True)

    t0 = time.time()
    boot_result = run_block_bootstrap_test_dmd(pre, post, d, tau, n_bootstrap=50, seed=SEED)
    elapsed = time.time() - t0
    print(f"[bootstrap/{variant}] elapsed={elapsed:.1f}s", flush=True)
    print(f"[bootstrap/{variant}] p_bootstrap_gap={boot_result.get('p_bootstrap_gap')} "
          f"delta_gap_boot_mean={boot_result.get('delta_gap_boot_mean')} "
          f"ci95={boot_result.get('delta_gap_boot_ci95')}", flush=True)
    return {"boot_result": _to_jsonable(boot_result), "wall_clock_seconds": elapsed,
            "tau_reused": tau, "d_reused": d}


def main():
    report = {}
    report["a_placebo_split_within_pre"] = check_a_placebo_split_within_pre()
    report["b_m69_exclusion"] = check_b_m69_exclusion()
    report["c_bootstrap_corroboration_primary"] = check_c_bootstrap_corroboration("primary")
    report["c_bootstrap_corroboration_robust"] = check_c_bootstrap_corroboration("robust")

    with open(OUT_PATH, "w") as f:
        json.dump(_to_jsonable(report), f, indent=2)
    print(f"\nWrote {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
