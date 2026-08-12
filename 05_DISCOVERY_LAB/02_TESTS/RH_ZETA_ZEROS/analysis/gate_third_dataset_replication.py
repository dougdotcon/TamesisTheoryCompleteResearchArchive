#!/usr/bin/env python3
"""
Replication Gate — third-agent, third-dataset robustness check for
DISC-RH-ZERO-GAP-RUNS-001.

Written from scratch by the Gate agent, based ONLY on:
  - 05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/PREREGISTRATION.md (Sections 1 and 4)
  - 05_DISCOVERY_LAB/03_REPLICATION_GATE/PROTOCOL.md (fallback clause, Section 3)
  - the freshly downloaded data/zeros4.txt (never touched before this session)

This script does NOT import from, read, or copy any code from
run_preregistered_analysis.py or adversarial_reproduction.py — it was written
before either of those files was opened by this agent.

Locked statistic (PREREGISTRATION.md Section 4), applied unmodified to a new
data source per the Gate's fallback clause (PROTOCOL.md Section 3, since this
test declared no sealed holdout split at pre-registration time):

  Normalized gap formula (Section 1):
      g_n = (gamma_{n+1} - gamma_n) * log(gamma_n / (2*pi)) / (2*pi)

  Grid: c in {0.10, 0.20, 0.30} x r in {2, 3}   (6 cells)

  Observed statistic per cell: count of overlapping windows of r consecutive
  gaps, in the REAL height-ordered sequence, that are ALL >= c.

  Null: 10,000 random permutations of the same multiset of gap values
  (numpy.random.default_rng, seed reported below).

  p_value_real_greater = (1 + #{null >= observed}) / (10001)   -- tests real > null
  p_value_real_lower   = (1 + #{null <= observed}) / (10001)   -- tests real < null (inverse)

  Bonferroni threshold: 0.05 / 6 ~= 0.0083333
"""

import json
import math
import re
import sys
import time

import numpy as np

DATA_PATH = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/data/zeros4.txt"
OUT_PATH = "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/RH_ZETA_ZEROS/analysis/result_gate_third_dataset.json"

SEED = 20260812  # same seed convention documented in PREREGISTRATION.md Section 4
N_PERM = 10_000
GRID_C = [0.10, 0.20, 0.30]
GRID_R = [2, 3]
BONFERRONI_THRESHOLD = 0.05 / 6.0
TWO_PI = 2.0 * math.pi


def parse_zeros4(path):
    """Parse zeros4.txt: extract the header offset base and the list of
    numeric offset values (data lines). Self-verifying: does not assume the
    header line count matches zeros3.txt or any other file — it locates the
    base via regex on the first header line and locates data lines by
    attempting float() parse on every non-blank line, keeping only lines
    that parse cleanly as a bare float (which the prose header lines do not,
    because they contain commas, words, and a trailing 'i * ...' fragment)."""
    with open(path, "r") as f:
        raw_lines = f.readlines()

    if not raw_lines:
        raise ValueError("zeros4.txt is empty")

    first_line = raw_lines[0]
    m = re.search(r"Values of gamma\s*-\s*(\d+)", first_line)
    if not m:
        raise ValueError(
            f"Could not find 'Values of gamma - <BASE>' pattern in header line 1: {first_line!r}"
        )
    base = int(m.group(1))

    offsets = []
    first_data_line_no = None
    last_data_line_no = None
    header_lines_consumed = []
    for i, line in enumerate(raw_lines, start=1):
        s = line.strip()
        if s == "":
            continue
        try:
            v = float(s)
        except ValueError:
            header_lines_consumed.append((i, line.rstrip("\n")))
            continue
        if first_data_line_no is None:
            first_data_line_no = i
        last_data_line_no = i
        offsets.append(v)

    return {
        "base": base,
        "offsets": offsets,
        "n_offsets": len(offsets),
        "first_data_line_no": first_data_line_no,
        "last_data_line_no": last_data_line_no,
        "total_lines_in_file": len(raw_lines),
        "header_lines": header_lines_consumed,
    }


def compute_normalized_gaps(base, offsets):
    """Compute normalized gaps using PREREGISTRATION.md Section 1's exact
    formula: g_n = (gamma_{n+1}-gamma_n) * log(gamma_n/(2*pi)) / (2*pi).

    Precision note (load-bearing): base ~ 1.44e20 cannot be represented
    exactly in float64 (base has 21 significant digits; float64 carries
    ~15-17). If gamma_n were formed as (base + offset_n) in float64 and then
    *subtracted* to get gaps, the subtraction would be catastrophically
    cancellation-prone: each float64 gamma_n carries an absolute rounding
    error of order base * 2^-52 ~ 3.2e4, which totally swamps the true gap
    magnitude (~0.05-2). So gaps are computed directly from the raw offset
    differences (offset_{n+1} - offset_n), NEVER by subtracting two
    already-summed gamma_n float64 values. The base is only ever used inside
    the log(gamma_n/(2*pi)) term, where a relative float64 rounding error of
    order 2^-52 ~ 2.2e-16 in gamma_n changes log(gamma_n/2pi) by an
    absolute amount of order 2.2e-16 -- utterly negligible for this
    statistic's threshold comparisons (c in {0.10,0.20,0.30}).
    """
    offsets = np.asarray(offsets, dtype=np.float64)
    n = len(offsets)
    raw_gaps = offsets[1:] - offsets[:-1]  # exact-ish, no cancellation issue (small numbers)
    gamma = float(base) + offsets[:-1]  # gamma_n for n=1..N-1, used only inside log()
    norm_factor = np.log(gamma / TWO_PI) / TWO_PI
    normalized_gaps = raw_gaps * norm_factor
    return normalized_gaps


def count_runs(bool_arr, r):
    """Count overlapping windows of length r that are all True."""
    n = len(bool_arr)
    if n < r:
        return 0
    csum = np.cumsum(np.concatenate(([0], bool_arr.astype(np.int64))))
    window_sums = csum[r:] - csum[:-r]
    return int(np.sum(window_sums == r))


def main():
    t0 = time.time()

    parsed = parse_zeros4(DATA_PATH)
    base = parsed["base"]
    offsets = parsed["offsets"]
    n_offsets = parsed["n_offsets"]

    print(f"[parse] base = {base}")
    print(f"[parse] n_offsets = {n_offsets}")
    print(f"[parse] first_data_line_no = {parsed['first_data_line_no']}, "
          f"last_data_line_no = {parsed['last_data_line_no']}, "
          f"total_lines_in_file = {parsed['total_lines_in_file']}")
    print(f"[parse] header lines consumed (non-numeric, skipped): {len(parsed['header_lines'])}")
    for ln, txt in parsed["header_lines"]:
        print(f"    line {ln}: {txt!r}")

    if n_offsets != 10000:
        print(f"WARNING: expected 10000 offset values per Odlyzko index description, got {n_offsets}",
              file=sys.stderr)

    # Sanity check: base + first offset should match the header's own stated
    # value for zero # 10^21 + 1 (144,176,897,509,546,973,538.49806962...)
    first_gamma_check = base + offsets[0]
    print(f"[sanity] base + offsets[0] = {first_gamma_check!r} "
          f"(header states 144176897509546973538.49806962...)")

    gaps = compute_normalized_gaps(base, offsets)
    n_gaps = len(gaps)
    print(f"[gaps] n_gaps = {n_gaps}")
    print(f"[gaps] mean = {gaps.mean():.6f}, std = {gaps.std():.6f}, "
          f"min = {gaps.min():.6f}, max = {gaps.max():.6f}")

    # Bonus diagnostic (not part of the locked statistic): lag-1 Pearson
    # correlation and position-vs-gap correlation, for cross-checking against
    # the drift-artifact concern already ruled out on the other two datasets.
    lag1_corr = float(np.corrcoef(gaps[:-1], gaps[1:])[0, 1])
    positions = np.arange(n_gaps, dtype=np.float64)
    position_corr = float(np.corrcoef(positions, gaps)[0, 1])
    print(f"[diagnostic] lag-1 Pearson corr(gap_i, gap_{{i+1}}) = {lag1_corr:.6f}")
    print(f"[diagnostic] position-vs-gap Pearson corr = {position_corr:.6e}")

    rng = np.random.default_rng(SEED)

    results = {}
    cells = []

    for c in GRID_C:
        bool_real_c = gaps >= c
        # Generate N_PERM permutations of the gap multiset, shared across both
        # r values for this c (same underlying shuffles, evaluated at r=2 and
        # r=3 -- a legitimate implementation choice: each individual cell's
        # null distribution is still exactly "10,000 permutations of the same
        # multiset of gap values" as required by Section 4).
        null_counts = {r: np.empty(N_PERM, dtype=np.int64) for r in GRID_R}
        for p in range(N_PERM):
            perm = rng.permutation(gaps)
            bool_perm_c = perm >= c
            for r in GRID_R:
                null_counts[r][p] = count_runs(bool_perm_c, r)

        for r in GRID_R:
            observed = count_runs(bool_real_c, r)
            nulls = null_counts[r]
            null_mean = float(nulls.mean())
            null_std = float(nulls.std())
            p_greater = (1 + int(np.sum(nulls >= observed))) / (N_PERM + 1)
            p_lower = (1 + int(np.sum(nulls <= observed))) / (N_PERM + 1)

            sig_greater = p_greater < BONFERRONI_THRESHOLD
            sig_lower = p_lower < BONFERRONI_THRESHOLD

            if sig_greater:
                verdict = "SUPPORTS_H_HIGH"
            elif sig_lower:
                verdict = "INVERSE_SIGNAL_LOW"
            else:
                verdict = "NOT_SIGNIFICANT"

            cell = {
                "c": c,
                "r": r,
                "observed_count": int(observed),
                "null_mean": null_mean,
                "null_std": null_std,
                "p_value_real_greater": p_greater,
                "p_value_real_lower": p_lower,
                "bonferroni_threshold": BONFERRONI_THRESHOLD,
                "significant_greater": bool(sig_greater),
                "significant_lower": bool(sig_lower),
                "cell_verdict": verdict,
            }
            cells.append(cell)
            print(f"[cell c={c:.2f} r={r}] observed={observed} null_mean={null_mean:.2f} "
                  f"null_std={null_std:.2f} p_greater={p_greater:.5f} p_lower={p_lower:.5f} "
                  f"-> {verdict}")

    n_support_high = sum(1 for c in cells if c["cell_verdict"] == "SUPPORTS_H_HIGH")
    n_inverse = sum(1 for c in cells if c["cell_verdict"] == "INVERSE_SIGNAL_LOW")

    if n_inverse > 0:
        aggregate_verdict = "INVERSE_SIGNAL"
    elif n_support_high >= 5:
        aggregate_verdict = "STRONG_SUPPORT"
    elif 2 <= n_support_high <= 4:
        aggregate_verdict = "PARTIAL_SUPPORT"
    else:
        aggregate_verdict = "NO_SUPPORT"

    elapsed = time.time() - t0

    # Cross-check against the pattern reported for zeros1.txt / zeros3.txt:
    # significant INVERSE signal specifically at c=0.30 (both r=2 and r=3).
    c30_cells = [c for c in cells if c["c"] == 0.30]
    c30_both_inverse = all(c["cell_verdict"] == "INVERSE_SIGNAL_LOW" for c in c30_cells)

    output = {
        "test_id": "DISC-RH-ZERO-GAP-RUNS-001",
        "role": "REPLICATION_GATE_THIRD_DATASET_ROBUSTNESS_CHECK",
        "gate_requirement_satisfied": "PROTOCOL.md Section 3 fallback clause "
            "(no sealed holdout declared at pre-registration time; formal robustness "
            "check against an additional, previously-untouched data source, documented "
            "explicitly as such)",
        "dataset": "zeros4.txt",
        "dataset_description": "Odlyzko zeta_tables/zeros4: zeros #10^21+1 through "
            "10^21+10^4, offsets from base gamma = 144176897509546973000",
        "height_regime_gamma_approx": 1.44176897509546973e20,
        "comparison_regimes": {
            "primary_zeros1": "gamma up to ~75000",
            "secondary_zeros3": "gamma ~ 2.68e11",
            "this_gate_zeros4": "gamma ~ 1.44e20",
        },
        "parse_metadata": {
            "base": base,
            "n_offsets_parsed": n_offsets,
            "first_data_line_no": parsed["first_data_line_no"],
            "last_data_line_no": parsed["last_data_line_no"],
            "total_lines_in_file": parsed["total_lines_in_file"],
            "n_header_lines_skipped": len(parsed["header_lines"]),
        },
        "gap_stats": {
            "n_gaps": n_gaps,
            "mean": float(gaps.mean()),
            "std": float(gaps.std()),
            "min": float(gaps.min()),
            "max": float(gaps.max()),
            "lag1_pearson_corr": lag1_corr,
            "position_vs_gap_pearson_corr": position_corr,
        },
        "rng_seed": SEED,
        "n_permutations_per_cell": N_PERM,
        "grid_c": GRID_C,
        "grid_r": GRID_R,
        "bonferroni_threshold": BONFERRONI_THRESHOLD,
        "cells": cells,
        "n_cells_support_h_high": n_support_high,
        "n_cells_inverse_signal": n_inverse,
        "aggregate_verdict_locked_criteria": aggregate_verdict,
        "c030_both_r_inverse_significant": c30_both_inverse,
        "matches_primary_and_secondary_pattern": c30_both_inverse,
        "elapsed_seconds": elapsed,
    }

    with open(OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n[done] elapsed = {elapsed:.1f}s")
    print(f"[done] aggregate verdict (locked criteria) = {aggregate_verdict}")
    print(f"[done] c=0.30 both r inverse-significant (matches zeros1/zeros3 pattern)? {c30_both_inverse}")
    print(f"[done] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
