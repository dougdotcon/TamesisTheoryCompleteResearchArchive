#!/usr/bin/env python3
"""
Independent adversarial reproduction of DISC-RH-GAP-EXTREME-VALUE-SCALING-001.

Written from scratch, WITHOUT reading run_preregistered_analysis.py or
result_primary.json, following only PREREGISTRATION.md and the task
instructions given to the adversarial reviewer.

Method (per preregistration):
  1. Load zeros1.txt (100,000 real zeta zeros).
  2. Normalized gaps: g_n = (gamma_{n+1} - gamma_n) * log(gamma_n/(2*pi)) / (2*pi)
     for n = 1..99999 (consecutive pairs) -> 99,999 gaps.
  3. Grid N in {500, 1000, 2000, 5000, 10000}.
  4. For each N: partition gap sequence into non-overlapping contiguous blocks
     of size N (drop remainder). Compute min within each block. Take median of
     block minima.
  5. Fit log(median_min_N) = alpha + beta*log(N) via OLS over the 5 grid points.
  6. Bootstrap 95% CI on beta: 10,000 replicates, resample block-minima with
     replacement (same count per N), independently per N, recompute median,
     refit OLS, collect beta.
"""

import json
import math
import numpy as np

DATA_PATH = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/data/zeros1.txt"
OUT_PATH = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_GAP_EXTREME_VALUE_SCALING/analysis/result_adversarial.json"

N_GRID = [500, 1000, 2000, 5000, 10000]
N_BOOT = 10000
SEED = 20260812  # as declared in preregistration; point estimate of beta does not depend on this

TWO_PI = 2.0 * math.pi


def load_zeros(path):
    zeros = np.loadtxt(path, dtype=np.float64)
    assert zeros.ndim == 1
    return zeros


def normalized_gaps(zeros):
    gamma = zeros[:-1]
    gamma_next = zeros[1:]
    raw_gap = gamma_next - gamma
    density = np.log(gamma / TWO_PI) / TWO_PI
    return raw_gap * density


def block_minima(gaps, N):
    n_blocks = len(gaps) // N  # floor division -> drop remainder
    usable = gaps[: n_blocks * N]
    blocks = usable.reshape(n_blocks, N)
    return blocks.min(axis=1)


def ols_fit(x, y):
    # simple closed-form OLS slope/intercept, y = alpha + beta*x
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n = len(x)
    xbar = x.mean()
    ybar = y.mean()
    sxx = np.sum((x - xbar) ** 2)
    sxy = np.sum((x - xbar) * (y - ybar))
    beta = sxy / sxx
    alpha = ybar - beta * xbar
    return alpha, beta


def main():
    zeros = load_zeros(DATA_PATH)
    assert len(zeros) == 100000, f"expected 100000 zeros, got {len(zeros)}"

    gaps = normalized_gaps(zeros)
    n_gaps = len(gaps)
    assert n_gaps == 99999, f"expected 99999 gaps, got {n_gaps}"

    print(f"Loaded {len(zeros)} zeros, {n_gaps} normalized gaps.")
    print(f"gap stats: min={gaps.min():.6f} max={gaps.max():.6f} mean={gaps.mean():.6f}")

    block_min_by_N = {}
    n_blocks_by_N = {}
    median_by_N = {}

    for N in N_GRID:
        bm = block_minima(gaps, N)
        n_blocks = len(bm)
        expected_n_blocks = n_gaps // N
        assert n_blocks == expected_n_blocks
        block_min_by_N[N] = bm
        n_blocks_by_N[N] = n_blocks
        median_by_N[N] = float(np.median(bm))
        print(f"N={N:6d}  n_blocks={n_blocks:4d} (floor({n_gaps}/{N})={n_gaps//N})  "
              f"median_block_min={median_by_N[N]:.8f}")

    # check expected block counts against preregistration text values
    expected_counts_prereg_text = {500: 199, 1000: 99, 2000: 49, 5000: 19, 10000: 9}
    # NOTE: preregistration body text (Section 4 step 3) actually says
    # "99, 99, 49, 19, 9" for N in {500,1000,2000,5000,10000} -- this looks
    # like a typo (500 -> should be 199, matches header text which does say 199).
    # We check against the arithmetically correct values (floor(99999/N)).
    computed_counts = {N: n_blocks_by_N[N] for N in N_GRID}
    print("\nBlock count check (floor(99999/N)):")
    for N in N_GRID:
        exp = n_gaps // N
        print(f"  N={N}: computed={computed_counts[N]}, floor-division-expected={exp}, "
              f"prereg-header-claim={expected_counts_prereg_text[N]}, match={computed_counts[N]==exp}")

    log_N = np.log(np.array(N_GRID, dtype=np.float64))
    log_median = np.log(np.array([median_by_N[N] for N in N_GRID], dtype=np.float64))

    alpha_obs, beta_obs = ols_fit(log_N, log_median)
    print(f"\nOLS fit (5 points): alpha={alpha_obs:.6f}, beta={beta_obs:.6f}")

    # cross-check with numpy.polyfit
    beta_polyfit, alpha_polyfit = np.polyfit(log_N, log_median, 1)
    print(f"Cross-check via np.polyfit: beta={beta_polyfit:.6f}, alpha={alpha_polyfit:.6f}")

    # cross-check with scipy if available
    try:
        from scipy import stats as spstats
        lr = spstats.linregress(log_N, log_median)
        print(f"Cross-check via scipy.stats.linregress: beta={lr.slope:.6f}, "
              f"alpha={lr.intercept:.6f}, r={lr.rvalue:.6f}, stderr={lr.stderr:.6f}")
    except ImportError:
        print("scipy not available, skipping linregress cross-check")

    # ---- Bootstrap CI ----
    rng = np.random.default_rng(SEED)
    boot_betas = np.empty(N_BOOT, dtype=np.float64)

    for b in range(N_BOOT):
        log_median_boot = np.empty(len(N_GRID), dtype=np.float64)
        for i, N in enumerate(N_GRID):
            bm = block_min_by_N[N]
            nb = n_blocks_by_N[N]
            resample_idx = rng.integers(0, nb, size=nb)
            resample = bm[resample_idx]
            log_median_boot[i] = np.log(np.median(resample))
        _, beta_b = ols_fit(log_N, log_median_boot)
        boot_betas[b] = beta_b

    ci_lo, ci_hi = np.percentile(boot_betas, [2.5, 97.5])
    print(f"\nBootstrap ({N_BOOT} reps, seed={SEED}): "
          f"beta 95% CI = [{ci_lo:.6f}, {ci_hi:.6f}]")
    print(f"bootstrap beta mean={boot_betas.mean():.6f}, std={boot_betas.std():.6f}")

    gue_in_ci = ci_lo <= -1.0/3.0 <= ci_hi
    poisson_in_ci = ci_lo <= -1.0 <= ci_hi
    print(f"-1/3 = {-1/3:.6f} in CI: {gue_in_ci}")
    print(f"-1 in CI: {poisson_in_ci}")

    # ---- Robustness check C: drop N=10000 (thinnest, 9 blocks) ----
    N_GRID_no10000 = [N for N in N_GRID if N != 10000]
    log_N_r1 = np.log(np.array(N_GRID_no10000, dtype=np.float64))
    log_median_r1 = np.log(np.array([median_by_N[N] for N in N_GRID_no10000], dtype=np.float64))
    alpha_r1, beta_r1 = ols_fit(log_N_r1, log_median_r1)
    print(f"\n[Robustness] Drop N=10000 (4 points {N_GRID_no10000}): beta={beta_r1:.6f}")

    # bootstrap CI for this 4-point fit too
    boot_betas_r1 = np.empty(N_BOOT, dtype=np.float64)
    rng2 = np.random.default_rng(SEED + 1)
    for b in range(N_BOOT):
        log_median_boot = np.empty(len(N_GRID_no10000), dtype=np.float64)
        for i, N in enumerate(N_GRID_no10000):
            bm = block_min_by_N[N]
            nb = n_blocks_by_N[N]
            resample_idx = rng2.integers(0, nb, size=nb)
            resample = bm[resample_idx]
            log_median_boot[i] = np.log(np.median(resample))
        _, beta_b = ols_fit(log_N_r1, log_median_boot)
        boot_betas_r1[b] = beta_b
    ci_lo_r1, ci_hi_r1 = np.percentile(boot_betas_r1, [2.5, 97.5])
    print(f"[Robustness] Drop N=10000: bootstrap 95% CI = [{ci_lo_r1:.6f}, {ci_hi_r1:.6f}]")

    # ---- Robustness check: only 4 largest-N points (drop N=500) ----
    N_GRID_large4 = [N for N in N_GRID if N != 500]
    log_N_r2 = np.log(np.array(N_GRID_large4, dtype=np.float64))
    log_median_r2 = np.log(np.array([median_by_N[N] for N in N_GRID_large4], dtype=np.float64))
    alpha_r2, beta_r2 = ols_fit(log_N_r2, log_median_r2)
    print(f"\n[Robustness] Drop N=500, use 4 largest-N points {N_GRID_large4}: beta={beta_r2:.6f}")

    boot_betas_r2 = np.empty(N_BOOT, dtype=np.float64)
    rng3 = np.random.default_rng(SEED + 2)
    for b in range(N_BOOT):
        log_median_boot = np.empty(len(N_GRID_large4), dtype=np.float64)
        for i, N in enumerate(N_GRID_large4):
            bm = block_min_by_N[N]
            nb = n_blocks_by_N[N]
            resample_idx = rng3.integers(0, nb, size=nb)
            resample = bm[resample_idx]
            log_median_boot[i] = np.log(np.median(resample))
        _, beta_b = ols_fit(log_N_r2, log_median_boot)
        boot_betas_r2[b] = beta_b
    ci_lo_r2, ci_hi_r2 = np.percentile(boot_betas_r2, [2.5, 97.5])
    print(f"[Robustness] 4 largest-N points: bootstrap 95% CI = [{ci_lo_r2:.6f}, {ci_hi_r2:.6f}]")

    # ---- Check: how much sampling variability is in the N=10000 median-of-9 alone? ----
    bm_10000 = block_min_by_N[10000]
    print(f"\n[Diagnostic] N=10000 block minima (9 values): {sorted(bm_10000.tolist())}")
    # bootstrap just the median of these 9 values, holding other N's fixed at observed median,
    # to see how much this single point's resampling noise contributes to beta variance
    rng4 = np.random.default_rng(SEED + 3)
    only_10000_boot_medians = np.empty(2000)
    for b in range(2000):
        idx = rng4.integers(0, 9, size=9)
        only_10000_boot_medians[b] = np.median(bm_10000[idx])
    print(f"[Diagnostic] median-of-9 resampling distribution: "
          f"mean={only_10000_boot_medians.mean():.6f}, std={only_10000_boot_medians.std():.6f}, "
          f"min={only_10000_boot_medians.min():.6f}, max={only_10000_boot_medians.max():.6f}, "
          f"observed median={median_by_N[10000]:.6f}")
    # how many distinct values can median of 9 resampled-with-replacement take?
    n_unique_boot_medians = len(np.unique(only_10000_boot_medians))
    print(f"[Diagnostic] unique median values across 2000 resamples of the 9-point set: {n_unique_boot_medians}")

    # ---- GEV / Wigner surmise near-zero exponent sanity check (task C, part 3) ----
    # Wigner surmise: p(s) = (32/pi^2) s^2 exp(-4 s^2 / pi)
    # near s=0: p(s) ~ (32/pi^2) s^2 * (1 - 4 s^2/pi + ...) -> leading order C*s^2, beta_gue=2
    s_vals = np.array([1e-4, 1e-3, 1e-2, 1e-1])
    C = 32.0 / (math.pi ** 2)
    p_vals = C * s_vals**2 * np.exp(-4 * s_vals**2 / math.pi)
    # local log-log slope between successive points -> should approach 2 as s->0
    log_s = np.log(s_vals)
    log_p = np.log(p_vals)
    local_slopes = np.diff(log_p) / np.diff(log_s)
    print(f"\n[Wigner check] p(s) at s={s_vals.tolist()}")
    print(f"[Wigner check] local log-log slopes (should -> 2 as s->0): {local_slopes.tolist()}")
    # min ~ N^{-1/(beta+1)}: beta=2 -> exponent -1/3; beta=0 (Poisson, uniform density near 0) -> exponent -1
    print(f"[Wigner check] predicted scaling exponent for beta=2: {-1.0/(2+1):.6f} (GUE)")
    print(f"[Wigner check] predicted scaling exponent for beta=0: {-1.0/(0+1):.6f} (Poisson)")

    result = {
        "test_id": "DISC-RH-GAP-EXTREME-VALUE-SCALING-001",
        "role": "independent adversarial reproduction",
        "script": "adversarial_reproduction.py",
        "n_zeros": int(len(zeros)),
        "n_gaps": int(n_gaps),
        "N_grid": N_GRID,
        "n_blocks_by_N": {str(N): int(n_blocks_by_N[N]) for N in N_GRID},
        "median_block_min_by_N": {str(N): median_by_N[N] for N in N_GRID},
        "ols_fit_primary": {
            "alpha": float(alpha_obs),
            "beta": float(beta_obs),
            "beta_polyfit_crosscheck": float(beta_polyfit),
        },
        "bootstrap_primary": {
            "n_boot": N_BOOT,
            "seed": SEED,
            "ci_95": [float(ci_lo), float(ci_hi)],
            "boot_beta_mean": float(boot_betas.mean()),
            "boot_beta_std": float(boot_betas.std()),
            "gue_in_ci": bool(gue_in_ci),
            "poisson_in_ci": bool(poisson_in_ci),
        },
        "robustness_drop_N10000": {
            "N_grid": N_GRID_no10000,
            "beta": float(beta_r1),
            "ci_95": [float(ci_lo_r1), float(ci_hi_r1)],
        },
        "robustness_drop_N500_largest4": {
            "N_grid": N_GRID_large4,
            "beta": float(beta_r2),
            "ci_95": [float(ci_lo_r2), float(ci_hi_r2)],
        },
        "diagnostic_N10000_median_of_9_resampling": {
            "block_minima": sorted(bm_10000.tolist()),
            "boot_median_mean": float(only_10000_boot_medians.mean()),
            "boot_median_std": float(only_10000_boot_medians.std()),
            "n_unique_boot_median_values_of_2000": int(n_unique_boot_medians),
        },
        "wigner_local_loglog_slopes": local_slopes.tolist(),
        "reported_values_from_result_primary_for_comparison": {
            "beta_observed": -0.3395,
            "ci_95": [-0.3872, -0.2868],
        },
    }

    with open(OUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote results to {OUT_PATH}")


if __name__ == "__main__":
    main()
