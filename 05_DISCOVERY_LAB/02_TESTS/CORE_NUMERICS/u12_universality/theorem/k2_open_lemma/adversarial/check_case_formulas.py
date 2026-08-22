#!/usr/bin/env python3
"""
Independent, from-scratch, CASE-LEVEL brute-force check (not just the final
summed closed form): for fixed n, enumerate all (pi, U1, U2), classify each
instance by (ell, case, d) or (ell, case, p, q) as defined by ATTEMPT.md
section 4.3 / my own independent re-derivation in the referee report, and
compute empirical exact conditional success probabilities, compared against
P_b(ell,d) = (ell-d)(3n-ell+1)/(2n^2) and P_c(ell,p,q) = (ell-q)(n+q-p)/n^2.

This checks the CASE ANALYSIS ITSELF, not merely its aggregate consequence.
Sources = points {0,1} (0-indexed). Generic reference point = 2 (n>=3).
"""
import sys
from fractions import Fraction as F
from itertools import permutations, product


def cyclic_flags(f, n):
    color = [0] * n
    cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            idx = path.index(cur)
            for j in range(idx, len(path)):
                cyclic[path[j]] = True
        for p in path:
            color[p] = 2
    return cyclic


def classify(pi, n, ref=2, src0=0, src1=1):
    """Return (case, ell, extra) where extra=(d,) for case 'b', (p,q) for
    case 'c', () for case 'a'. Trace pi's cycle containing `ref`."""
    cyc = []
    cur = ref
    while True:
        cyc.append(cur)
        cur = pi[cur]
        if cur == ref:
            break
    ell = len(cyc)
    pos0 = cyc.index(src0) if src0 in cyc else None
    pos1 = cyc.index(src1) if src1 in cyc else None
    if pos0 is None and pos1 is None:
        return ('a', ell, ())
    if pos0 is not None and pos1 is not None:
        p, q = sorted((pos0, pos1))
        return ('c', ell, (p, q))
    d = pos0 if pos0 is not None else pos1
    return ('b', ell, (d,))


def Pb_formula(ell, d, n):
    return F((ell - d) * (3 * n - ell + 1), 2 * n * n)


def Pc_formula(ell, p, q, n):
    return F((ell - q) * (n + q - p), n * n)


def run(n):
    assert n >= 3
    counts = {}  # key -> [hits, total]
    for pi in permutations(range(n)):
        case, ell, extra = classify(list(pi), n)
        for U0, U1 in product(range(n), repeat=2):
            f = [0] * n
            f[0] = U0
            f[1] = U1
            for i in range(2, n):
                f[i] = pi[i]
            cyc = cyclic_flags(f, n)
            key = (case, ell, extra)
            rec = counts.setdefault(key, [0, 0])
            rec[1] += 1
            if cyc[2]:
                rec[0] += 1

    print(f"n={n}: {len(counts)} distinct (case, ell, extra) configurations")
    mismatches = 0
    checked = 0
    for key in sorted(counts):
        case, ell, extra = key
        hits, tot = counts[key]
        emp = F(hits, tot)
        if case == 'a':
            pred = F(1)
        elif case == 'b':
            (d,) = extra
            pred = Pb_formula(ell, d, n)
        else:
            p, q = extra
            pred = Pc_formula(ell, p, q, n)
        checked += 1
        ok = (emp == pred)
        if not ok:
            mismatches += 1
            print(f"  MISMATCH case={case} ell={ell} extra={extra}: "
                  f"empirical={emp} ({hits}/{tot})  predicted={pred}")
    print(f"  checked {checked} configurations, {mismatches} mismatches")
    return mismatches


if __name__ == "__main__":
    n_lo, n_hi = int(sys.argv[1]), int(sys.argv[2])
    total_mismatches = 0
    for n in range(n_lo, n_hi + 1):
        total_mismatches += run(n)
    print(f"\nTOTAL MISMATCHES ACROSS ALL n TESTED: {total_mismatches}")
