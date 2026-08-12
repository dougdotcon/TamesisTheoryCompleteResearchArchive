#!/usr/bin/env python3
"""
Independent adversarial reproduction of DISC-RH-ZERO-GAP-RUNS-001.

Written FROM SCRATCH by an independent adversarial reviewer, without
reading run_preregistered_analysis.py or result_primary.json first, per
the pre-registered spec in PREREGISTRATION.md.

Loads zeros1.txt (primary, 100000 real zeta zeros) and zeros3.txt
(secondary, 10000 zeros near zero #10^12, offsets from base
267653395647), computes normalized gaps, and for the pre-registered grid
c in {0.10, 0.20, 0.30} x r in {2, 3} counts runs of r consecutive gaps
all >= c in the real ordered sequence vs. a null of 10000 random
permutations of the same gap multiset. Reports both one-sided p-values
(real > null, and real < null) for full transparency.
"""

import json
import math
import numpy as np

DATA_DIR = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/data"
OUT_PATH = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/analysis/result_adversarial.json"

C_GRID = [0.10, 0.20, 0.30]
R_GRID = [2, 3]
N_PERM = 10000
SEED = 424242  # different from pre-registered seed 20260812, deliberately, for independence
BONFERRONI_THRESHOLD = 0.05 / 6


def load_zeros1(path):
    with open(path, "r") as f:
        vals = [float(tok) for tok in f.read().split()]
    assert len(vals) == 100000, f"expected 100000 zeros in zeros1.txt, got {len(vals)}"
    return np.array(vals, dtype=np.float64)


def load_zeros3(path):
    with open(path, "r") as f:
        lines = f.readlines()
    # Verified by direct inspection: lines 1-9 (1-indexed) are header/prose,
    # numeric data begins at line 10 (1-indexed) i.e. lines[9:] in 0-indexed
    # slicing, and continues to the end of the file (10000 values).
    data_lines = lines[9:]
    assert len(data_lines) == 10000, f"expected 10000 data lines in zeros3.txt, got {len(data_lines)}"
    offsets = np.array([float(x.strip()) for x in data_lines], dtype=np.float64)
    base = 267653395647.0
    heights = base + offsets
    return heights


def normalized_gaps(zeros):
    gammas = zeros[:-1]
    gaps = np.diff(zeros)
    # normalized gap = (gamma_{n+1} - gamma_n) * log(gamma_n / (2*pi)) / (2*pi)
    norm = gaps * np.log(gammas / (2.0 * math.pi)) / (2.0 * math.pi)
    return norm


def count_runs(gaps, c, r):
    """Count positions i (0-indexed, overlapping windows) such that
    gaps[i..i+r-1] are ALL >= c. Vectorized, no off-by-one: valid i range
    is 0 .. len(gaps)-r inclusive, i.e. len(gaps)-r+1 positions."""
    n = len(gaps)
    if r > n:
        return 0
    ge = gaps >= c
    # sliding window sum of booleans == r means all True in window
    csum = np.cumsum(ge, dtype=np.int64)
    csum = np.concatenate(([0], csum))
    window_sums = csum[r:] - csum[:-r]  # length n - r + 1
    return int(np.sum(window_sums == r))


def run_dataset(name, gaps, seed):
    rng = np.random.default_rng(seed)
    n = len(gaps)
    results = {}

    observed = {}
    for c in C_GRID:
        for r in R_GRID:
            observed[(c, r)] = count_runs(gaps, c, r)

    null_counts = {(c, r): np.empty(N_PERM, dtype=np.int64) for c in C_GRID for r in R_GRID}

    for p in range(N_PERM):
        perm = rng.permutation(gaps)
        # sanity: permutation preserves multiset (checked cheaply once)
        for c in C_GRID:
            for r in R_GRID:
                null_counts[(c, r)][p] = count_runs(perm, c, r)

    # multiset preservation check (once, on first permutation regenerated deterministically)
    rng_check = np.random.default_rng(seed)
    perm_check = rng_check.permutation(gaps)
    multiset_ok = bool(np.array_equal(np.sort(perm_check), np.sort(gaps)))

    cells = []
    for c in C_GRID:
        for r in R_GRID:
            obs = observed[(c, r)]
            nulls = null_counts[(c, r)]
            null_mean = float(np.mean(nulls))
            null_std = float(np.std(nulls, ddof=1))
            p_greater = (1 + int(np.sum(nulls >= obs))) / (N_PERM + 1)
            p_lower = (1 + int(np.sum(nulls <= obs))) / (N_PERM + 1)
            supports_H = p_greater < BONFERRONI_THRESHOLD
            inverse_signal = p_lower < BONFERRONI_THRESHOLD
            cells.append({
                "c": c, "r": r,
                "observed": obs,
                "null_mean": null_mean,
                "null_std": null_std,
                "p_value_real_greater": p_greater,
                "p_value_real_lower": p_lower,
                "supports_H": supports_H,
                "inverse_signal": inverse_signal,
            })

    return {
        "dataset": name,
        "n_gaps": n,
        "seed": seed,
        "mean_normalized_gap": float(np.mean(gaps)),
        "std_normalized_gap": float(np.std(gaps)),
        "multiset_preserved_check": multiset_ok,
        "cells": cells,
    }


def drift_check(gaps, label):
    idx = np.arange(len(gaps))
    corr = float(np.corrcoef(idx, gaps)[0, 1])
    # split into 10 deciles by position, report mean normalized gap per decile
    n = len(gaps)
    decile_means = []
    step = n // 10
    for i in range(10):
        lo = i * step
        hi = (i + 1) * step if i < 9 else n
        decile_means.append(float(np.mean(gaps[lo:hi])))
    # linear regression slope
    slope, intercept = np.polyfit(idx, gaps, 1)
    return {
        "label": label,
        "pearson_corr_position_vs_gap": corr,
        "linear_slope": float(slope),
        "linear_intercept": float(intercept),
        "decile_means": decile_means,
    }


def main():
    zeros1 = load_zeros1(f"{DATA_DIR}/zeros1.txt")
    gaps1 = normalized_gaps(zeros1)

    zeros3 = load_zeros3(f"{DATA_DIR}/zeros3.txt")
    gaps3 = normalized_gaps(zeros3)

    print(f"zeros1: n_zeros={len(zeros1)}, n_gaps={len(gaps1)}, mean_norm_gap={np.mean(gaps1):.6f}, std={np.std(gaps1):.6f}")
    print(f"zeros3: n_zeros={len(zeros3)}, n_gaps={len(gaps3)}, mean_norm_gap={np.mean(gaps3):.6f}, std={np.std(gaps3):.6f}")
    print(f"zeros3 first heights: {zeros3[:3]}")
    print(f"zeros1 first gap (unnormalized): {zeros1[1]-zeros1[0]:.6f}, gamma0={zeros1[0]:.6f}")

    result_primary = run_dataset("zeros1.txt (primary)", gaps1, SEED)
    result_secondary = run_dataset("zeros3.txt (secondary)", gaps3, SEED + 1)

    drift_primary = drift_check(gaps1, "zeros1.txt normalized gap vs position index")
    drift_secondary = drift_check(gaps3, "zeros3.txt normalized gap vs position index")

    out = {
        "test_id": "DISC-RH-ZERO-GAP-RUNS-001",
        "role": "independent adversarial reproduction",
        "bonferroni_threshold": BONFERRONI_THRESHOLD,
        "primary": result_primary,
        "secondary": result_secondary,
        "drift_check": {
            "primary": drift_primary,
            "secondary": drift_secondary,
        },
    }

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    print("\n=== PRIMARY (zeros1.txt) ===")
    for cell in result_primary["cells"]:
        print(cell)
    print("\n=== SECONDARY (zeros3.txt) ===")
    for cell in result_secondary["cells"]:
        print(cell)
    print("\n=== DRIFT CHECK ===")
    print("primary:", drift_primary["pearson_corr_position_vs_gap"], drift_primary["linear_slope"])
    print("secondary:", drift_secondary["pearson_corr_position_vs_gap"], drift_secondary["linear_slope"])
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
