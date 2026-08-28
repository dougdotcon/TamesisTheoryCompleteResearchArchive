"""
Independent, from-scratch assembly check of P_nn(n,K) (ATTEMPT.md Sec 5),
built on TWO already-independently-verified ingredients from this referee's
own scripts 02/03 (exact match against direct brute force at every tested
point, no formula taken on faith from the front):

  (i)  node-level P_0(s), P_pair(s,s') closed forms (script 02)
  (ii) position-level linear-in-i / bilinear-in-(i,i') scaling (script 03)

plus Lemma 1 (Governing-Source Reindexing target): (L_0,...,L_{K-1},O)
uniform over all compositions of n-K into K+1 nonnegative parts (L_s>=1,
O>=0) -- this specific fact is cited, not re-derived here (it was proved
by the k2_joint_case_split predecessor for general m and independently
re-verified by that front's own dedicated referee; re-deriving it again
from Definition 1-4 is redundant with that closed, adversarially-reviewed
result, so this script only re-uses its STATEMENT, which is elementary
stars-and-bars once accepted).

For a CONCRETE (n,K), this script:
  1. enumerates every composition (L_0,...,L_{K-1},O) of n-K into K+1
     nonnegative parts, L_s>=1, exactly (there are C(n,K) of them);
  2. for each, computes T(L) = sum over ALL ordered pairs of the n-K
     non-source "roles" (O outside roles + interior arc positions) of
     the exact probability both are cyclic, using ONLY the already
     brute-force-verified single-point/cross-arc/same-arc formulas
     (own code, re-implemented here, not copy-pasted from script 02/03);
  3. averages: P_nn(n,K) = (1/C(n,K)) * sum_L T(L) / ((n-K)(n-K-1)).

This is compared, exactly (Fraction), against the claimed closed-form
Propositions NN1-NN6 at MANY values of n per K -- enough points to pin
down the degree-K polynomial numerator uniquely (a match at K+2 or more
points is not a coincidence: two distinct degree-K polynomials cannot
agree at more than K points), so a match across a full swept range is a
genuine independent confirmation of the closed forms, not merely of a
handful of cherry-picked points.
"""
import itertools
from fractions import Fraction
from math import comb, factorial
import sys


def P0_formula(K, s, x):
    others = [u for u in range(K) if u != s]
    total = 0
    for r in range(len(others) + 1):
        for S in itertools.combinations(others, r):
            term = 1
            for u in S:
                term = term * x[u]
            total = total + factorial(len(S)) * term
    return x[s] * total


def Ppair_formula(K, s, sp, x):
    M = [u for u in range(K) if u != s and u != sp]
    same = 0
    for r in range(len(M) + 1):
        for S in itertools.combinations(M, r):
            term = 1
            for u in S:
                term = term * x[u]
            same = same + factorial(len(S) + 1) * term
    same = same * x[s] * x[sp]
    disj = 0
    for r1 in range(len(M) + 1):
        for S1 in itertools.combinations(M, r1):
            rest = [u for u in M if u not in S1]
            for r2 in range(len(rest) + 1):
                for S2 in itertools.combinations(rest, r2):
                    t1 = 1
                    for u in S1:
                        t1 = t1 * x[u]
                    t2 = 1
                    for u in S2:
                        t2 = t2 * x[u]
                    disj = disj + factorial(len(S1)) * t1 * factorial(len(S2)) * t2
    disj = disj * x[s] * x[sp]
    return same + disj


def T_of_L(K, n, L, O):
    x = [Fraction(Ls, n) for Ls in L]
    P0 = [P0_formula(K, s, x) for s in range(K)]
    # outside-outside
    T = Fraction(O * (O - 1))
    # outside-arc (both orders): 2 * O * sum_s sum_{i=1}^{L_s-1} (i/L_s)*P0[s]
    for s in range(K):
        m = L[s] - 1
        if m > 0:
            sum_i = Fraction(m * (m + 1), 2) / L[s]  # sum_{i=1}^{m} i / L_s
            T += 2 * O * sum_i * P0[s]
    # same-arc ordered pairs i != i': both cyclic = P(min(i,i') cyclic).
    # sum_{i!=i', 1<=i,i'<=m} min(i,i') = 2*sum_{i=1}^{m-1} i*(m-i)
    # (closed form, elementary; cross-checked against the direct O(m^2)
    # double loop below for small m before being trusted at scale --
    # see 04b_same_arc_sanity.py).
    for s in range(K):
        m = L[s] - 1
        if m >= 2:
            sum_i_times = sum(i * (m - i) for i in range(1, m))
            acc = Fraction(2 * sum_i_times, L[s]) * P0[s]
            T += acc
    # cross-arc ordered pairs (s != s', all i in arc s interior, i' in arc s' interior).
    # Ppair_formula(K,s,sp,x) is symmetric under s<->sp (P_same/P_disjoint both
    # depend on {s,sp} only through x_s*x_sp and M=complement of {s,sp}), so
    # compute each unordered pair once and reuse for both orderings.
    for s in range(K):
        for sp in range(s + 1, K):
            m1 = L[s] - 1
            m2 = L[sp] - 1
            if m1 > 0 and m2 > 0:
                sum_i = Fraction(m1 * (m1 + 1), 2) / L[s]
                sum_ip = Fraction(m2 * (m2 + 1), 2) / L[sp]
                Pss = Ppair_formula(K, s, sp, x)
                T += 2 * sum_i * sum_ip * Pss
    return T


def compositions(total, parts_min1, parts_free):
    """Yield tuples (a_0,...,a_{parts_min1-1}, b_0,...,b_{parts_free-1})
    where the first parts_min1 entries are >=1 (arc lengths L_s) and the
    remaining parts_free entries are >=0 (here just O, parts_free=1),
    summing to `total`=n."""
    # here: parts_min1 = K (each >=1), parts_free = 1 (O>=0), sum = n
    K = parts_min1
    # iterate over all L_0..L_{K-1} >=1 with sum <= total, O = total - sum
    def rec(idx, remaining, acc):
        if idx == K:
            yield tuple(acc) + (remaining,)
            return
        # remaining slots after this: need at least 1 for each of the rest, plus O>=0
        max_here = remaining - (K - idx - 1)  # leave >=1 for each remaining L
        for v in range(1, max_here + 1):
            acc.append(v)
            yield from rec(idx + 1, remaining - v, acc)
            acc.pop()
    yield from rec(0, total, [])


def assembled_Pnn(n, K):
    assert n >= K + 2
    total_T = Fraction(0)
    count = 0
    for comp in compositions(n, K, 1):
        L = comp[:K]
        O = comp[K]
        total_T += T_of_L(K, n, L, O)
        count += 1
    assert count == comb(n, K), (count, comb(n, K))
    return total_T / (count * (n - K) * (n - K - 1))


CLAIMED = {
    1: lambda n: Fraction(3 * n + 1, 6 * n),
    2: lambda n: Fraction(10 * n**2 + 7 * n + 2, 30 * n**2),
    3: lambda n: Fraction(35 * n**3 + 38 * n**2 + 23 * n + 6, 140 * n**3),
    4: lambda n: Fraction(126 * n**4 + 187 * n**3 + 177 * n**2 + 98 * n + 24, 630 * n**4),
    5: lambda n: Fraction(462 * n**5 + 874 * n**4 + 1139 * n**3 + 989 * n**2 + 514 * n + 120, 2772 * n**5),
    6: lambda n: Fraction(1716 * n**6 + 3958 * n**5 + 6616 * n**4 + 7933 * n**3 + 6472 * n**2 + 3204 * n + 720, 12012 * n**6),
}

if __name__ == "__main__":
    ranges = {
        1: range(3, 15),
        2: range(4, 15),
        3: range(5, 16),
        4: range(6, 17),
        5: range(7, 18),
        # K=6: a degree-6 rational-function numerator is pinned down
        # uniquely by matching at 7 or more points (it cannot agree with
        # a genuinely different polynomial at more points than its
        # degree). n=8..14 gives exactly 7 independent points, all at
        # the boundary or above; interactively (this referee's session,
        # not reproduced in this default run to keep wall-time bounded)
        # n=8..16 (9 points) were also checked and all matched -- see
        # REFEREE_REPORT.md Sec on Proposition NN6.
        6: range(8, 15),
    }
    overall = True
    for K, ns in ranges.items():
        ok_all = True
        for n in ns:
            got = assembled_Pnn(n, K)
            claimed = CLAIMED[K](n)
            ok = (got == claimed)
            ok_all = ok_all and ok
            if not ok:
                print(f"  MISMATCH K={K} n={n}: assembled={got} claimed={claimed}")
        print(f"K={K}: n in {list(ns)} -> {'ALL MATCH' if ok_all else 'MISMATCH FOUND'}")
        overall = overall and ok_all
        sys.stdout.flush()
    print("=== FINAL:", "ALL OK" if overall else "SOME MISMATCHES", "===")
