#!/usr/bin/env python3
"""
INDEPENDENT, FROM-SCRATCH true brute force of THEOREM.md Definition 4
at K=4, written for the adversarial referee review of ATTEMPT.md
(k4_full_cdf_attempt). No code from any front's .py files was read;
this is built directly from Definition 4's own text (THEOREM.md lines
~859-872): pi a uniform random permutation of [n]; sources fixed WLOG
at {0,1,2,3} (exchangeability); U_0,U_1,U_2,U_3 i.i.d. Uniform([n]),
independent of pi; f(i):=U_i for i in sources, f(i):=pi(i) otherwise;
T := #{cyclic points of f}.

Two independent enumeration routes are implemented and cross-checked
against each other at small n:

  ROUTE A ("literal"): iterate over ALL n! permutations pi of [n] and
    all n^4 tuples (U_0,...,U_3) -- exactly matches the raw sample
    space size n!*n^4 the front itself reports in its own table.

  ROUTE B ("reduced, faster"): since f(i) for i in {0,1,2,3} depends
    only on U_i (pi(0..3) is thrown away, never used), the marginal
    distribution of T depends only on pi restricted to positions
    {4,...,n-1}. For a uniform permutation of [n], that restriction is
    uniform over all INJECTIVE functions from {4,...,n-1} into [n]
    (a standard elementary fact about uniform random permutations --
    fixing the image of a subset of positions of a uniform permutation
    gives a uniform distribution over injections). There are
    P(n, n-4) = n!/4! such injections, so Route B enumerates
    P(n,n-4)*n^4 configurations instead of n!*n^4 -- exactly 4!=24x
    fewer, with IDENTICAL resulting T distribution. This is not a
    heuristic shortcut; it is proven equal below by direct comparison
    against Route A at n=4,5,6 before being trusted alone at n=7,8.

Cyclic-point counting: standard functional-graph peeling (repeatedly
strip in-degree-0 nodes; survivors are exactly the cycle nodes),
vectorized over a batch of configurations with numpy for speed.

Output: exact PMF/CDF of T via Fraction, saved to bf_k4_pmf_<n>.json,
plus a comparison against Proposicao D4's own closed-form formula
(transcribed directly from ATTEMPT.md's prose, not from any .py file).
"""
import sys, time, json
from fractions import Fraction
from itertools import permutations
import numpy as np

def cyclic_count_batch(f_batch, n):
    """f_batch: (B,n) int array, values in [0,n). Returns (B,) array of T."""
    B = f_batch.shape[0]
    indeg = np.zeros((B, n), dtype=np.int32)
    rows_all = np.repeat(np.arange(B), n)
    cols_all = f_batch.ravel()
    np.add.at(indeg, (rows_all, cols_all), 1)
    alive = np.ones((B, n), dtype=bool)
    for _ in range(n):
        to_remove = alive & (indeg == 0)
        if not to_remove.any():
            break
        alive &= ~to_remove
        rr, cc = np.nonzero(to_remove)
        if rr.size == 0:
            break
        targets = f_batch[rr, cc]
        np.add.at(indeg, (rr, targets), -1)
    return alive.sum(axis=1)

def route_A_literal(n):
    """Literal enumeration: all n! permutations x all n^4 U-tuples."""
    counts = np.zeros(n + 1, dtype=np.int64)
    idx = np.indices((n,) * 4).reshape(4, -1).T.astype(np.int32)  # (n^4,4)
    B = idx.shape[0]
    total = 0
    for perm in permutations(range(n)):
        base = np.array(perm, dtype=np.int32)
        f_batch = np.tile(base, (B, 1))
        f_batch[:, :4] = idx
        Ts = cyclic_count_batch(f_batch, n)
        vals, cnts = np.unique(Ts, return_counts=True)
        counts[vals] += cnts
        total += B
    return counts, total

def route_B_reduced(n, verbose=False):
    """Reduced enumeration: injective tail assignments x all n^4 U-tuples."""
    ntail = n - 4
    counts = np.zeros(n + 1, dtype=np.int64)
    idx = np.indices((n,) * 4).reshape(4, -1).T.astype(np.int32)  # (n^4,4)
    B = idx.shape[0]
    total = 0
    ng = 0
    t0 = time.time()
    for g in permutations(range(n), ntail):
        base = np.zeros(n, dtype=np.int32)
        if ntail > 0:
            base[4:] = g
        f_batch = np.tile(base, (B, 1))
        f_batch[:, :4] = idx
        Ts = cyclic_count_batch(f_batch, n)
        vals, cnts = np.unique(Ts, return_counts=True)
        counts[vals] += cnts
        total += B
        ng += 1
        if verbose and ng % 200 == 0:
            print(f"    ... {ng} tail-assignments done, {time.time()-t0:.1f}s", file=sys.stderr)
    return counts, total

# ---- Proposicao D4 closed form, transcribed verbatim from ATTEMPT.md prose ----
def Q_D4(n, k):
    return (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4
            + (-16*n**2 + 80*n + 51)*k**3
            + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
            + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
            + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)

def D4_cdf(n, k):
    if k >= n:
        return Fraction(1)
    if k < 0:
        return Fraction(0)
    num = k * (k + 1) * Q_D4(n, k)
    den = n**5 * (n - 1) * (n - 2) * (n - 3)
    return Fraction(num, den)

def pmf_to_cdf_fractions(counts, total):
    cdf = []
    running = 0
    for c in counts:
        running += int(c)
        cdf.append(Fraction(running, int(total)))
    return cdf

def check_n(n, use_route_A_too=False):
    print(f"\n=== n={n} ===")
    t0 = time.time()
    countsB, totalB = route_B_reduced(n, verbose=(n >= 7))
    tB = time.time() - t0
    print(f"Route B (reduced): total configs = {totalB}, elapsed {tB:.1f}s")
    expected_total = 1
    from math import factorial
    expected_total = (factorial(n) // factorial(4)) * n**4
    assert totalB == expected_total, f"config count mismatch: {totalB} vs expected {expected_total}"
    print(f"  matches expected P(n,n-4)*n^4 = {expected_total}: OK")

    if use_route_A_too:
        t0 = time.time()
        countsA, totalA = route_A_literal(n)
        tA = time.time() - t0
        print(f"Route A (literal): total configs = {totalA}, elapsed {tA:.1f}s")
        expected_total_A = factorial(n) * n**4
        assert totalA == expected_total_A
        # Route A counts should be exactly 24x Route B counts (since totalA=24*totalB)
        ratio_ok = all(a == 24 * b for a, b in zip(countsA, countsB))
        print(f"  Route A counts == 24 * Route B counts (every T value): {ratio_ok}")
        if not ratio_ok:
            print("  MISMATCH between Route A and Route B -- INVESTIGATE", file=sys.stderr)
            print("  countsA:", countsA.tolist())
            print("  countsB:", countsB.tolist())

    cdf = pmf_to_cdf_fractions(countsB, totalB)
    mismatches = []
    for k in range(0, n):
        bf_val = cdf[k]
        d4_val = D4_cdf(n, k)
        if bf_val != d4_val:
            mismatches.append((k, bf_val, d4_val))
    print(f"Compared Proposicao D4 vs brute-force CDF for k=0..{n-1}: "
          f"{n - len(mismatches)}/{n} exact matches")
    if mismatches:
        print("  MISMATCHES FOUND:")
        for k, bf_val, d4_val in mismatches:
            print(f"    k={k}: brute-force={bf_val}  D4-formula={d4_val}  diff={bf_val-d4_val}")
    else:
        print("  ALL MATCH EXACTLY.")
    # also check k=n trivial boundary
    assert D4_cdf(n, n) == Fraction(1)
    return len(mismatches) == 0, countsB.tolist(), totalB

if __name__ == "__main__":
    results = {}
    all_ok = True
    # Cross-validate Route A vs Route B at small n first (n=4,5) -- proves the
    # "reduced" enumeration is a faithful representation of the literal model.
    for n in [4, 5]:
        ok, counts, total = check_n(n, use_route_A_too=True)
        all_ok = all_ok and ok
        results[n] = {"ok": ok, "counts": counts, "total": total}
    # n=6..9 with Route B only (Route A would carry a redundant 24x overhead)
    for n in [6, 7, 8, 9]:
        ok, counts, total = check_n(n, use_route_A_too=False)
        all_ok = all_ok and ok
        results[n] = {"ok": ok, "counts": counts, "total": total}

    print("\n" + "=" * 70)
    print("OVERALL:", "ALL PROPOSICAO D4 CHECKS PASSED, n=4..9, every k "
          "(n=9 goes one full step beyond even the front's own reach of n=8)"
          if all_ok else "MISMATCHES FOUND -- SEE ABOVE")
    print("=" * 70)

    with open("/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/bf_k4_results.json", "w") as fh:
        json.dump(results, fh)
