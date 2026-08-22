#!/usr/bin/env python3
"""
Case-level brute-force check for the NEW from-scratch psi_n^{(2),R}
derivation (derive_psiR_from_scratch.py): classify each pi by (m, k) where
m = length of source-0's OWN pi-cycle D, k = position of source-1 on D
(None if source-1 is off D), and check the empirical conditional success
probability P(0 is cyclic | pi) against:
   source1 off D:            m(3n-m+1)/(2n^2)     [= P_b(ell=m, d=0)]
   source1 on D at position k: (m-k)(n+k)/n^2       [= P_c(ell=m, p=0, q=k)]
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


def classify(pi, n, src0=0, src1=1):
    """D = pi-cycle containing src0. m=|D|. k = position of src1 on D
    (1-indexed from src0), or None if src1 not on D."""
    D = []
    cur = src0
    while True:
        D.append(cur)
        cur = pi[cur]
        if cur == src0:
            break
    m = len(D)
    k = D.index(src1) if src1 in D else None
    return m, k


def Pb0(m, n):
    return F(m * (3 * n - m + 1), 2 * n * n)


def Pc0k(m, k, n):
    return F((m - k) * (n + k), n * n)


def run(n):
    assert n >= 2
    counts = {}
    for pi in permutations(range(n)):
        m, k = classify(list(pi), n)
        for U0, U1 in product(range(n), repeat=2):
            f = [0] * n
            f[0] = U0
            f[1] = U1
            for i in range(2, n):
                f[i] = pi[i]
            cyc = cyclic_flags(f, n)
            key = (m, k)
            rec = counts.setdefault(key, [0, 0])
            rec[1] += 1
            if cyc[0]:
                rec[0] += 1

    print(f"n={n}: {len(counts)} distinct (m,k) configurations")
    mism = 0
    for key in sorted(counts, key=lambda t: (t[0], -1 if t[1] is None else t[1])):
        m, k = key
        hits, tot = counts[key]
        emp = F(hits, tot)
        pred = Pb0(m, n) if k is None else Pc0k(m, k, n)
        ok = emp == pred
        if not ok:
            mism += 1
            print(f"  MISMATCH m={m} k={k}: empirical={emp} ({hits}/{tot}) predicted={pred}")
    print(f"  {len(counts)} configs checked, {mism} mismatches")
    return mism


if __name__ == "__main__":
    n_lo, n_hi = int(sys.argv[1]), int(sys.argv[2])
    tot = 0
    for n in range(n_lo, n_hi + 1):
        tot += run(n)
    print(f"\nTOTAL MISMATCHES: {tot}")
