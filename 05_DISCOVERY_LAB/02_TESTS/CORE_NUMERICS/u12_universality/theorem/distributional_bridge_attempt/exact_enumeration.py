"""
Exact enumeration (exact rational arithmetic where it matters) of the
FULL distribution of the cyclic-point count T = #cyclic(f) under
THEOREM.md Definition 4 (K reroutes fixed WLOG at indices 0..K-1,
0-indexed here; matches the archive's own k1_exact_check.py /
k2_exact_exploration.py convention up to the indexing offset).

This is new relative to the existing archive scripts, which only ever
accumulate the MEAN (phi_n^{(K)} / psi_n^{(K)}). Here we keep the whole
distribution of T (a Counter over t=0..n), plus the exact two-point
quantities P_nn, P_nr, P_rr needed for the second-moment reduction
lemma of ATTEMPT.md Section 4.

No randomness anywhere in this script (exhaustive enumeration only).
"""
import itertools
import json
from fractions import Fraction
from collections import Counter
import sys
import time

def cyclic_set(f, n):
    """Return the set of cyclic points of a mapping f: [n]->[n] given as
    a list f[0..n-1]. O(n) via standard three-color DFS-iterative walk."""
    color = [0] * n  # 0 unvisited, 1 in-progress, 2 done
    cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        i = start
        while color[i] == 0:
            color[i] = 1
            path.append(i)
            i = f[i]
        if color[i] == 1:
            # found a fresh cycle starting at position of i in path
            j = path.index(i)
            for p in path[j:]:
                cyclic[p] = True
        for p in path:
            color[p] = 2
    return cyclic


def enumerate_cell(n, K):
    """Exhaustive enumeration over all n! permutations and n^K reroute
    targets for the K rerouted indices 0..K-1 (0-indexed). Returns:
      - Counter of T = #cyclic points (raw integer counts, not yet
        normalized)
      - total number of (pi,U) configurations
      - raw counts of 'both cyclic' events for three point-type pairs:
          nn: (n-1, n-2) -- both guaranteed non-rerouted iff K <= n-2
          nr: (n-1, 0)   -- one non-rerouted, one rerouted iff K>=1, n-1>=K
          rr: (0, 1)     -- both rerouted iff K>=2
        (each entry is None if the required index configuration is not
        available at this (n,K), e.g. rr needs K>=2)
    """
    assert n >= 1 and 0 <= K <= n
    idx_nn = (n - 1, n - 2) if (K <= n - 2 and n >= 2) else None
    idx_nr = (n - 1, 0) if (K >= 1 and n - 1 >= K) else None
    idx_rr = (0, 1) if K >= 2 else None

    counter = Counter()
    cnt_nn = 0
    cnt_nr = 0
    cnt_rr = 0
    total = 0

    perms = itertools.permutations(range(n))
    targets_space = list(itertools.product(range(n), repeat=K)) if K > 0 else [()]

    for pi in perms:
        for U in targets_space:
            f = list(pi)
            for k in range(K):
                f[k] = U[k]
            cyc = cyclic_set(f, n)
            t = sum(cyc)
            counter[t] += 1
            total += 1
            if idx_nn is not None and cyc[idx_nn[0]] and cyc[idx_nn[1]]:
                cnt_nn += 1
            if idx_nr is not None and cyc[idx_nr[0]] and cyc[idx_nr[1]]:
                cnt_nr += 1
            if idx_rr is not None and cyc[idx_rr[0]] and cyc[idx_rr[1]]:
                cnt_rr += 1

    return counter, total, cnt_nn, cnt_nr, cnt_rr, idx_nn, idx_nr, idx_rr


def summarize(n, K, counter, total, cnt_nn, cnt_nr, cnt_rr):
    total_f = Fraction(total)
    dist = {t: Fraction(c, total) for t, c in sorted(counter.items())}
    mean = sum(Fraction(t) * p for t, p in dist.items()) / n
    # exact CDF at integer thresholds k=0..n : F(k/n) = P(T<=k)
    cdf = {}
    acc = Fraction(0)
    for t in range(n + 1):
        acc += dist.get(t, Fraction(0))
        cdf[t] = acc
    out = {
        "n": n, "K": K, "total_configs": total,
        "mean_M": str(mean), "mean_M_float": float(mean),
        "dist_T": {str(t): str(p) for t, p in dist.items()},
        "cdf_at_k_over_n": {str(k): str(v) for k, v in cdf.items()},
    }
    return out


def main():
    cells = [
        (1, 0), (2, 0),
        (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
        (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
    ]
    results = []
    for (n, K) in cells:
        t0 = time.time()
        counter, total, cnn, cnr, crr, idx_nn, idx_nr, idx_rr = enumerate_cell(n, K)
        elapsed = time.time() - t0
        r = summarize(n, K, counter, total, cnn, cnr, crr)
        r["elapsed_sec"] = round(elapsed, 3)
        r["idx_nn"] = idx_nn
        r["idx_nr"] = idx_nr
        r["idx_rr"] = idx_rr
        if idx_nn is not None:
            r["P_nn"] = str(Fraction(cnn, total))
            r["P_nn_float"] = float(Fraction(cnn, total))
        if idx_nr is not None:
            r["P_nr"] = str(Fraction(cnr, total))
            r["P_nr_float"] = float(Fraction(cnr, total))
        if idx_rr is not None:
            r["P_rr"] = str(Fraction(crr, total))
            r["P_rr_float"] = float(Fraction(crr, total))
        results.append(r)
        print(f"n={n:2d} K={K} total={total:>10d} mean={r['mean_M_float']:.6f} "
              f"P_nn={r.get('P_nn_float')} P_nr={r.get('P_nr_float')} "
              f"P_rr={r.get('P_rr_float')} t={elapsed:.2f}s", flush=True)

    with open("exact_enumeration_results.json", "w") as fh:
        json.dump(results, fh, indent=1)
    print("wrote exact_enumeration_results.json")


if __name__ == "__main__":
    main()
