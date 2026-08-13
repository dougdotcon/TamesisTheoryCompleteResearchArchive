#!/usr/bin/env python3
"""
Replication Gate — third-dataset robustness check for
DISC-RH-GAP-EXTREME-VALUE-SCALING-001.

Written from scratch by the third, independent Gate agent, using ONLY
PREREGISTRATION.md (Sections 1 and 4, LOCKED) and data/PROVENANCE.md as
inputs. This script was written before reading run_preregistered_analysis.py
or adversarial_reproduction.py, and does not import or reuse any code from
them.

Dataset: data/zeros5.txt (Odlyzko, zeros near #10^22), fetched fresh by this
agent — see the "Gate de Replicacao, terceiro dataset (zeros5.txt)" section
appended to data/PROVENANCE.md for full provenance (URL, sha256, header
verification).

Numerical-hazard note (flagged in the task and confirmed empirically below):
BASE = 1370919909931995300000 has 22 significant digits and is NOT exactly
representable in float64 (~15-17 significant digits). Representing BASE as a
float64 and rounding to the nearest integer changes it by 65376 (absolute
error), which dwarfs a typical gap (~0.01-0.4 in raw offset units, or
~0.05-2 in normalized units). Therefore:
  - Raw gaps are computed as offset_{n+1} - offset_n directly (BASE cancels
    algebraically and never needs to be formed at full precision).
  - BASE is used ONLY inside the log(gamma_n / (2*pi)) term, formed as
    float64 gamma_n = BASE + offset_n. This term is provably insensitive to
    the ~1e-15 relative rounding error of a float64 sum at this magnitude:
    d/dx log(x) = 1/x, so a relative perturbation eps in x produces an
    absolute change of ~eps in log(x) -- utterly negligible next to the
    scale of the statistic (medians of order 1e-2 to 1, log-log OLS slope
    of order -0.3).
"""

import json
import math
import random
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
ZEROS5_PATH = DATA_DIR / "zeros5.txt"
OUT_PATH = HERE / "result_gate_third_dataset.json"

BASE = 1370919909931995300000  # from zeros5.txt header, "gamma - BASE"
TWO_PI = 2.0 * math.pi

# Locked grid (PREREGISTRATION.md Section 4, step 2) -- do not change.
N_GRID = [500, 1000, 2000, 5000, 10000]
# Locked minimum-blocks quality bar stated in PREREGISTRATION.md Section 4
# step 3 ("contanto que >=8 blocos por N") -- used here only to FLAG which
# grid points meet the bar declared for the primary dataset, not to alter
# the grid itself.
MIN_BLOCKS_BAR = 8

N_BOOTSTRAP = 10000
BOOTSTRAP_SEED = 20260813  # this agent's own seed, reported explicitly


def parse_zeros5(path: Path):
    """Parse zeros5.txt into a list of raw offsets (floats), auto-detecting
    where the prose header ends and the numeric data begins (does not
    assume a fixed line number a priori -- verified against the observed
    structure below)."""
    numeric_line_re = re.compile(r"^\s*\d+\.\d+\s*$")
    offsets = []
    data_started = False
    first_data_line_no = None
    last_data_line_no = None
    with open(path, "r") as f:
        for line_no, line in enumerate(f, start=1):
            if numeric_line_re.match(line):
                if not data_started:
                    data_started = True
                    first_data_line_no = line_no
                offsets.append(float(line.strip()))
                last_data_line_no = line_no
            else:
                if data_started:
                    # a non-numeric line after data started would be
                    # unexpected -- fail loudly rather than silently drop
                    # data.
                    raise ValueError(
                        f"non-numeric line {line_no} found after data "
                        f"section started at line {first_data_line_no}: "
                        f"{line!r}"
                    )
    return offsets, first_data_line_no, last_data_line_no


def compute_normalized_gaps(offsets):
    """Normalized gap formula, PREREGISTRATION.md Section 1 (same formula
    as ../RH_ZETA_ZEROS/PREREGISTRATION.md Section 1):
        g_n = (gamma_{n+1} - gamma_n) * log(gamma_n / (2*pi)) / (2*pi)
    Raw gap (gamma_{n+1} - gamma_n) computed directly from offset
    differences -- NEVER by forming two float64 gamma_n values and
    subtracting them (catastrophic cancellation, see module docstring).
    """
    gaps = []
    for n in range(len(offsets) - 1):
        raw_gap = offsets[n + 1] - offsets[n]  # BASE cancels algebraically
        gamma_n_approx = BASE + offsets[n]  # float64 OK only inside log()
        density_factor = math.log(gamma_n_approx / TWO_PI) / TWO_PI
        gaps.append(raw_gap * density_factor)
    return gaps


def block_minima(gaps, n_block):
    """Non-overlapping contiguous blocks of size n_block; returns the list
    of per-block minima. Returns an empty list if fewer than n_block gaps
    are available (0 complete blocks)."""
    n_complete_blocks = len(gaps) // n_block
    minima = []
    for b in range(n_complete_blocks):
        block = gaps[b * n_block : (b + 1) * n_block]
        minima.append(min(block))
    return minima


def ols_fit(xs, ys):
    """Simple OLS slope/intercept for y = alpha + beta*x."""
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    sxx = sum((x - mean_x) ** 2 for x in xs)
    beta = sxy / sxx
    alpha = mean_y - beta * mean_x
    return alpha, beta


def run_grid_fit(gaps, n_values, min_blocks_required=1):
    """For each N in n_values with >= min_blocks_required complete blocks,
    compute median-of-block-minima. Returns dict N -> (n_blocks, minima,
    median) for the usable points, plus the list of skipped points."""
    results = {}
    skipped = []
    for n_block in n_values:
        minima = block_minima(gaps, n_block)
        if len(minima) < min_blocks_required:
            skipped.append((n_block, len(minima)))
            continue
        median = statistics.median(minima)
        results[n_block] = {
            "n_blocks": len(minima),
            "block_minima": minima,
            "median_min": median,
        }
    return results, skipped


def bootstrap_ci_beta(results, seed, n_bootstrap=N_BOOTSTRAP):
    """Bootstrap 95% CI on beta: resample block minima with replacement
    (same count per N) each replicate, recompute medians, refit OLS on
    log(N) vs log(median), collect beta. Only uses the N values present in
    `results` (i.e. already filtered to usable grid points)."""
    rng = random.Random(seed)
    ns = sorted(results.keys())
    log_ns = [math.log(n) for n in ns]
    betas = []
    for _ in range(n_bootstrap):
        log_medians = []
        for n_block in ns:
            minima = results[n_block]["block_minima"]
            resample = [rng.choice(minima) for _ in range(len(minima))]
            log_medians.append(math.log(statistics.median(resample)))
        _, beta = ols_fit(log_ns, log_medians)
        betas.append(beta)
    betas.sort()
    lo_idx = int(0.025 * n_bootstrap)
    hi_idx = int(0.975 * n_bootstrap) - 1
    hi_idx = min(hi_idx, n_bootstrap - 1)
    return betas[lo_idx], betas[hi_idx], betas


def main():
    offsets, first_line, last_line = parse_zeros5(ZEROS5_PATH)
    print(f"Parsed {len(offsets)} offsets from lines {first_line}-{last_line}")
    print(f"First offset: {offsets[0]}, last offset: {offsets[-1]}")

    gaps = compute_normalized_gaps(offsets)
    print(f"Computed {len(gaps)} normalized gaps")
    print(f"min gap: {min(gaps):.6f}, max gap: {max(gaps):.6f}, "
          f"mean gap: {statistics.mean(gaps):.6f}")

    # --- Full locked grid attempt (report exactly what each N yields) ---
    full_results, full_skipped = run_grid_fit(gaps, N_GRID, min_blocks_required=1)
    print("\nPer-N block counts (full locked grid, N=500..10000):")
    quality_flags = {}
    for n_block in N_GRID:
        if n_block in full_results:
            nb = full_results[n_block]["n_blocks"]
            med = full_results[n_block]["median_min"]
            meets_bar = nb >= MIN_BLOCKS_BAR
            quality_flags[n_block] = meets_bar
            print(f"  N={n_block:6d}: {nb:3d} blocks, median_min={med:.6f}, "
                  f"meets >=8-block bar: {meets_bar}")
        else:
            skipped_entry = [s for s in full_skipped if s[0] == n_block][0]
            print(f"  N={n_block:6d}: {skipped_entry[1]} blocks (INSUFFICIENT, "
                  f"skipped -- cannot compute a block minimum at all)")
            quality_flags[n_block] = False

    usable_ns_full = sorted(full_results.keys())
    log_ns_full = [math.log(n) for n in usable_ns_full]
    log_meds_full = [math.log(full_results[n]["median_min"]) for n in usable_ns_full]
    alpha_full, beta_full = ols_fit(log_ns_full, log_meds_full)
    lo_full, hi_full, _ = bootstrap_ci_beta(full_results, BOOTSTRAP_SEED)
    print(f"\n[Full available grid: N={usable_ns_full}]")
    print(f"beta = {beta_full:.6f}, 95% CI = [{lo_full:.6f}, {hi_full:.6f}]")

    # --- Task 2D robustness check: restrict to N points meeting the
    # preregistration's own >=8-block quality bar (this is the
    # statistically defensible subset on this smaller dataset) ---
    strict_ns = [n for n in N_GRID if quality_flags.get(n, False)]
    strict_results, _ = run_grid_fit(gaps, strict_ns, min_blocks_required=MIN_BLOCKS_BAR)
    usable_ns_strict = sorted(strict_results.keys())
    log_ns_strict = [math.log(n) for n in usable_ns_strict]
    log_meds_strict = [math.log(strict_results[n]["median_min"]) for n in usable_ns_strict]
    if len(usable_ns_strict) >= 2:
        alpha_strict, beta_strict = ols_fit(log_ns_strict, log_meds_strict)
        lo_strict, hi_strict, _ = bootstrap_ci_beta(strict_results, BOOTSTRAP_SEED)
        print(f"\n[Strict >=8-block subset: N={usable_ns_strict}]")
        print(f"beta = {beta_strict:.6f}, 95% CI = [{lo_strict:.6f}, {hi_strict:.6f}]")
    else:
        alpha_strict = beta_strict = lo_strict = hi_strict = None
        print(f"\n[Strict >=8-block subset: N={usable_ns_strict} -- fewer than "
              f"2 usable points, cannot fit OLS]")

    # --- Task 2D variant: drop only N=10000 (the point with 0 blocks,
    # which is impossible to compute regardless) and keep everything else
    # that has >=1 block, i.e. N in {500,1000,2000,5000} ---
    drop_10000_ns = [n for n in N_GRID if n != 10000]
    drop_results, _ = run_grid_fit(gaps, drop_10000_ns, min_blocks_required=1)
    usable_drop = sorted(drop_results.keys())
    log_ns_drop = [math.log(n) for n in usable_drop]
    log_meds_drop = [math.log(drop_results[n]["median_min"]) for n in usable_drop]
    alpha_drop, beta_drop = ols_fit(log_ns_drop, log_meds_drop)
    lo_drop, hi_drop, _ = bootstrap_ci_beta(drop_results, BOOTSTRAP_SEED)
    print(f"\n[Drop N=10000 only: N={usable_drop}]")
    print(f"beta = {beta_drop:.6f}, 95% CI = [{lo_drop:.6f}, {hi_drop:.6f}]")

    def verdict_for(beta, lo, hi):
        gue_survives = lo <= (-1.0 / 3.0) <= hi
        poisson_survives = lo <= -1.0 <= hi
        goe_survives = lo <= -0.5 <= hi
        return {
            "beta": beta,
            "ci95": [lo, hi],
            "minus_one_third_in_ci": gue_survives,
            "minus_one_in_ci": poisson_survives,
            "minus_one_half_in_ci": goe_survives,
        }

    out = {
        "test_id": "DISC-RH-GAP-EXTREME-VALUE-SCALING-001",
        "role": "replication_gate_third_dataset_robustness_check",
        "dataset": "zeros5.txt",
        "n_zeros": len(offsets),
        "n_gaps": len(gaps),
        "data_line_range": [first_line, last_line],
        "bootstrap_seed": BOOTSTRAP_SEED,
        "n_bootstrap_replicates": N_BOOTSTRAP,
        "min_blocks_bar_from_preregistration": MIN_BLOCKS_BAR,
        "per_N_block_counts": {
            str(n): (full_results[n]["n_blocks"] if n in full_results else 0)
            for n in N_GRID
        },
        "per_N_median_min": {
            str(n): (full_results[n]["median_min"] if n in full_results else None)
            for n in N_GRID
        },
        "full_available_grid": {
            "N_used": usable_ns_full,
            **verdict_for(beta_full, lo_full, hi_full),
        },
        "strict_ge8_blocks_subset": {
            "N_used": usable_ns_strict,
            **(verdict_for(beta_strict, lo_strict, hi_strict)
               if beta_strict is not None else {"note": "insufficient points for OLS"}),
        },
        "drop_N10000_only": {
            "N_used": usable_drop,
            **verdict_for(beta_drop, lo_drop, hi_drop),
        },
    }

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
