#!/usr/bin/env python3
"""
REFEREE, FRESH, NAIVE CROSS-CHECK (deliberately NOT using the
injection+K!-weighting speedup device of def4_exhaustive_check.py, to
validate that device independently). Enumerates literally every
(pi, R, U) triple -- pi ranging over ALL n! permutations of Sym(n)
directly via itertools.permutations, R over all C(n,K) subsets, U over
all n^K destination tuples -- with NO reweighting trick at all. Slower,
but structurally simpler and independent of the main script's main
efficiency device, so a match against def4_exhaustive_check.py's output
is a genuine independent confirmation that the weighting trick used
there introduces no bug.

Only run at small (n,K) where n! * C(n,K) * n^K is small enough to be
naively tractable (a few million at most).
"""
import itertools
import math
from fractions import Fraction


def cyclic_points_and_cycle_ids(f, n):
    UNVISITED, ON_PATH, DONE = 0, 1, 2
    state = [UNVISITED] * n
    cyclic = [False] * n
    cid = {}
    next_cid = 0
    for start in range(n):
        if state[start] != UNVISITED:
            continue
        path = []
        pos_in_path = {}
        v = start
        while state[v] == UNVISITED:
            state[v] = ON_PATH
            pos_in_path[v] = len(path)
            path.append(v)
            v = f[v]
        if state[v] == ON_PATH:
            idx = pos_in_path[v]
            this_cid = next_cid
            next_cid += 1
            for u in path[idx:]:
                cyclic[u] = True
                cid[u] = this_cid
        for u in path:
            state[u] = DONE
    return cyclic, cid


def run_cell_naive(n, K, pair=(0, 1)):
    i0, j0 = pair
    total = 0
    both = 0
    same = 0
    diff = 0
    for pi in itertools.permutations(range(n)):
        for R in itertools.combinations(range(n), K):
            Rset = set(R)
            for U in itertools.product(range(n), repeat=K):
                f = list(pi)
                for k, r in enumerate(R):
                    f[r] = U[k]
                f = tuple(f)
                total += 1
                cyclic, cid = cyclic_points_and_cycle_ids(f, n)
                if cyclic[i0] and cyclic[j0]:
                    both += 1
                    if cid[i0] == cid[j0]:
                        same += 1
                    else:
                        diff += 1
    expected_total = math.factorial(n) * math.comb(n, K) * (n ** K)
    assert total == expected_total, (total, expected_total)
    p_both = Fraction(both, total)
    p_same = Fraction(same, total)
    p_diff = Fraction(diff, total)
    return p_both, p_same, p_diff, total


def main():
    # Small cells only (naive method is O(n! * C(n,K) * n^K), no speedup)
    cells = [
        (3, 0), (3, 1), (3, 2), (3, 3),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        (5, 2), (5, 5),
        (6, 1),
    ]
    print("Naive (no-shortcut) cross-check of def4_exhaustive_check.py's results")
    print(f"{'n':>3} {'K':>3} | {'P_both':>14} {'P_same':>14} {'P_diff':>14} | configs")
    for (n, K) in cells:
        p_both, p_same, p_diff, total = run_cell_naive(n, K)
        ok = (p_same == p_diff) and (p_same * 2 == p_both)
        print(f"{n:>3} {K:>3} | {str(p_both):>14} {str(p_same):>14} {str(p_diff):>14} | {total:>8} | corollary_ok={ok}")


if __name__ == "__main__":
    main()
