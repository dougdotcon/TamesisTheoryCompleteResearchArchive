#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH true brute force of THEOREM.md Definition 4 at K=3.

Written entirely independently: no .py file from any front in this lineage
(k3_full_cdf_attempt, k3_joint_structural_attempt, k2_joint_case_split_attempt,
joint_exploration_continuum_attempt, joint_two_point_attempt,
conjecture2_direct_attempt, general_k_joint_attempt,
k3_full_cdf_attempt_ABANDONED_STALLED) was opened, read, or imported to build
this. Only the prose of THEOREM.md Definition 4 (Sec 7.2) was used.

Definition 4 (K=3 fixed-reroute model), transcribed from THEOREM.md:
  pi a uniform random permutation of [n] (0-indexed here: {0,...,n-1}).
  Sources fixed at {0,1,2} WLOG by the exchangeability argument stated in
  Definition 4 itself.
  U_0,U_1,U_2 i.i.d. Uniform([n]) (0-indexed: uniform on {0,...,n-1}),
  independent of pi.
  f(i) := U_i for i in {0,1,2}; f(i) := pi(i) otherwise.
  T := #{cyclic points of f}  (a point x is cyclic iff iterating f from x
  returns to x).
  M_n^{(3)} := T/n.

This script enumerates EVERY (pi, U_0, U_1, U_2) combination exactly
(n! * n^3 configurations), computes T for each via O(n) functional-graph
cycle detection (no shortcuts, no reduced model, no citation of any lemma
from this lineage), and tabulates the exact distribution of T using Python
integer counts (converted to exact fractions.Fraction at the end) -- zero
floating point anywhere.

Output: for each n tested, exact P(T<=k) for every k=0..n, printed and
also dumped as JSON (fractions as [num,den] pairs) for cross-checking by
other adversarial scripts in this directory.
"""

import itertools
import json
import sys
import time
from fractions import Fraction

def cyclic_count(f, n):
    """f: list of length n, f[i] in range(n). Returns #cyclic points.
    Standard O(n) functional-graph 3-coloring cycle detection, written
    from scratch (no library, no citation)."""
    UNVISITED, ON_PATH, DONE = 0, 1, 2
    state = [UNVISITED] * n
    cyclic = [False] * n
    for start in range(n):
        if state[start] != UNVISITED:
            continue
        path = []
        x = start
        while state[x] == UNVISITED:
            state[x] = ON_PATH
            path.append(x)
            x = f[x]
        if state[x] == ON_PATH:
            # x is on the current path -> found a new cycle from x to end of path
            idx = path.index(x)
            for j in range(idx, len(path)):
                cyclic[path[j]] = True
        # mark everyone on path as DONE (cyclic flag already set where applicable)
        for p in path:
            state[p] = DONE
    return sum(cyclic)


def bruteforce_T_distribution(n):
    """Exhaustive enumeration of Definition 4's K=3 model at fixed n.
    Returns dict {T_value: exact_count} and total configuration count."""
    assert n >= 3
    counts = {}
    total = 0
    base_perm_indices = list(range(n))
    for pi in itertools.permutations(base_perm_indices):
        pi = list(pi)
        for U0, U1, U2 in itertools.product(range(n), repeat=3):
            f = list(pi)
            f[0] = U0
            f[1] = U1
            f[2] = U2
            T = cyclic_count(f, n)
            counts[T] = counts.get(T, 0) + 1
            total += 1
    return counts, total


def cdf_from_counts(counts, total, n):
    """Exact P(T<=k) for k=0..n, as Fraction, from the tallied counts."""
    cum = 0
    cdf = {}
    for k in range(0, n + 1):
        cum += counts.get(k, 0)
        cdf[k] = Fraction(cum, total)
    assert cum == total, "sanity: cumulative count must reach total"
    return cdf


def d3_formula(n, k):
    """Proposition D3's claimed closed form, transcribed independently
    from ATTEMPT.md Sec 4.1 (verbatim transcription for comparison
    purposes only -- this function does NOT import any code from the
    front; it is typed fresh from the prose formula in ATTEMPT.md):

    P(M_n^(3) <= k/n) =
        k(k+1) [ k^4 - 4k^3 - (3n^2-9n-5)k^2 + (3n^2-11n-2)k
                 + (3n^4-12n^3+12n^2+2n) ]
        -----------------------------------------------------
                     n^4 (n-1)(n-2)
    for 0<=k<=n-1, and 1 for k>=n.
    """
    if k >= n:
        return Fraction(1, 1)
    if k < 0:
        return Fraction(0, 1)
    n = Fraction(n)
    k = Fraction(k)
    numerator = k * (k + 1) * (
        k**4 - 4 * k**3
        - (3 * n**2 - 9 * n - 5) * k**2
        + (3 * n**2 - 11 * n - 2) * k
        + (3 * n**4 - 12 * n**3 + 12 * n**2 + 2 * n)
    )
    denominator = n**4 * (n - 1) * (n - 2)
    return numerator / denominator


def main():
    ns = [3, 4, 5, 6, 7, 8]
    if len(sys.argv) > 1:
        ns = [int(x) for x in sys.argv[1:]]

    results = {}
    all_ok = True
    for n in ns:
        t0 = time.time()
        counts, total = bruteforce_T_distribution(n)
        elapsed = time.time() - t0
        expected_total = 1
        for i in range(1, n + 1):
            expected_total *= i
        expected_total *= n ** 3
        assert total == expected_total, f"n={n}: total configs {total} != {expected_total}"

        cdf = cdf_from_counts(counts, total, n)
        mismatches = []
        for k in range(0, n):
            bf = cdf[k]
            pred = d3_formula(n, k)
            if bf != pred:
                mismatches.append((k, str(bf), str(pred)))
        ok = (len(mismatches) == 0)
        all_ok = all_ok and ok
        print(f"n={n}  configs={total}  elapsed={elapsed:.2f}s  "
              f"k-range=0..{n-1}  mismatches={len(mismatches)}  "
              f"{'OK' if ok else 'MISMATCH'}")
        if mismatches:
            for m in mismatches:
                print("   MISMATCH:", m)
        results[n] = {
            "total_configs": total,
            "elapsed_s": elapsed,
            "counts": {str(kk): vv for kk, vv in counts.items()},
            "cdf": {str(kk): [vv.numerator, vv.denominator] for kk, vv in cdf.items()},
            "mismatches": mismatches,
        }

    out_path = __file__.replace(".py", "_results.json")
    try:
        with open(out_path) as fh:
            existing = json.load(fh)
    except FileNotFoundError:
        existing = {}
    existing.update({str(k): v for k, v in results.items()})
    with open(out_path, "w") as fh:
        json.dump(existing, fh, indent=1)
    print(f"\nResults dumped to {out_path}")
    print()
    if all_ok:
        print(f"ALL CHECKS PASSED: Proposicao D3 matches TRUE brute force of "
              f"Definition 4 exactly, for n in {ns}, every k.")
    else:
        print("*** AT LEAST ONE MISMATCH FOUND -- Proposicao D3 is WRONG "
              "for at least one (n,k). ***")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
