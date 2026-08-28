"""
Section 1 of ATTEMPT.md: the exact unconditional-CDF setup, general K.

Cites (does NOT re-derive) two already-PROVED, K-free results from
`general_k_decomposition_attempt/ATTEMPT.md` (Estagio 41):

  * The Full Cycle-Count Decomposition Theorem: T = O + sum_{s in S} V_s,
    where S subseteq {0,...,K-1} is the random set of cyclic reroute
    sources and, given S, the (V_s)_{s in S} are MUTUALLY INDEPENDENT,
    V_s ~ Uniform{1,...,L_s}.
  * Proposition S (K-free): for every A subseteq {0,...,K-1}, |A|=:r,
        P(S=A | L) = r! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a),
    p_a := L_a/n, p_D := O/n.

Combining these (exactly as Estagio 40 Section 3 did concretely at K=3,
generalized here to any K -- an elementary generalization, since the
inner "P(O + sum_{s in A} V_s <= k)" term is just an elementary |A|-fold
discrete-uniform lattice count regardless of K):

  P(T<=k | L) = sum_{A subseteq {0,...,K-1}}
                    P(S=A|L) * Count_{|A|}(L_A ; k-O) / prod_{a in A} L_a

  Count_r(L_1,...,L_r ; t) := #{(v_1,...,v_r) in Z^r :
                                    1<=v_i<=L_i for all i, sum v_i <= t}

and P(T<=k) = average of P(T<=k|L) over the uniform composition simplex
of (L_0,...,L_{K-1}, O), L_i>=1, O>=0, sum = n (the Governing-Source
Reindexing corollary, cited).

This script implements both pieces directly from the formulas above (own
code, nothing imported from any other front) and verifies the RESULT
against the true Definition-4 brute force of
`bruteforce_definition4_general_k.py`, for every k, at several (n,K).
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb, factorial

from bruteforce_definition4_general_k import bruteforce_cdf


def count_le(Ls, t):
    """Count_r(Ls; t): #{v in Z^r : 1<=v_i<=Ls[i], sum v_i <= t}.
    Direct enumeration -- fine for the small Ls used in these checks;
    the closed-form treatment of this object is Sections 2-4's subject.
    """
    r = len(Ls)
    if r == 0:
        return 1 if t >= 0 else 0
    if t < r:
        return 0
    cnt = 0
    for v in product(*[range(1, L + 1) for L in Ls]):
        if sum(v) <= t:
            cnt += 1
    return cnt


def P_S_eq_A_given_L(A, L, O, n):
    """Proposition S (cited, general_k_decomposition_attempt Section 2.4)."""
    r = len(A)
    if r == 0:
        return Fraction(O, n)
    prod_p = Fraction(1)
    sum_p = Fraction(0)
    for a in A:
        prod_p *= Fraction(L[a], n)
        sum_p += Fraction(L[a], n)
    pD = Fraction(O, n)
    return factorial(r) * prod_p * (pD + sum_p)


def cond_cdf(L, O, n, k):
    """P(T<=k | L) via Proposition S + the elementary lattice count."""
    K = len(L)
    total = Fraction(0)
    for r in range(0, K + 1):
        for A in combinations(range(K), r):
            pA = P_S_eq_A_given_L(A, L, O, n)
            if r == 0:
                total += pA * (1 if (k - O) >= 0 else 0)
                continue
            Ls = tuple(L[a] for a in A)
            prodL = 1
            for x in Ls:
                prodL *= x
            cnt = count_le(Ls, k - O)
            total += pA * Fraction(cnt, prodL)
    return total


def compositions(n, K):
    """Yields (L, O) with L a K-tuple, L_i>=1, O>=0, sum(L)+O=n."""
    def rec(idx, remaining):
        if idx == K:
            yield (remaining,)
            return
        for v in range(1, remaining + 1):
            for rest in rec(idx + 1, remaining - v):
                yield (v,) + rest
    for tup in rec(0, n):
        L, O = tup[:K], tup[K]
        if O >= 0:
            yield L, O


def unconditional_cdf_slow(n, K, k):
    """O(C(n,K)) exact reference engine: average cond_cdf over the true
    composition simplex. Independent of everything in Sections 2-4;
    this IS "Section 1 of the mandate" made computable."""
    total = Fraction(0)
    cnt = 0
    for L, O in compositions(n, K):
        total += cond_cdf(L, O, n, k)
        cnt += 1
    assert cnt == comb(n, K)
    return total / cnt


if __name__ == "__main__":
    print("Section-1 setup verification: Proposition S + elementary lattice")
    print("count, averaged over the composition simplex, vs true brute force.")
    print("=" * 70)
    cases = [(4, 1), (4, 2), (5, 2), (5, 3), (6, 3)]
    all_ok = True
    for n, K in cases:
        bf_cdf, _ = bruteforce_cdf(n, K)
        print(f"n={n} K={K}:")
        for k in range(n + 1):
            got = unconditional_cdf_slow(n, K, k)
            want = bf_cdf[k]
            ok = (got == want)
            all_ok = all_ok and ok
            print(f"   k={k}: setup={got}  bruteforce={want}  {'OK' if ok else 'MISMATCH!'}")
    print("=" * 70)
    print(f"ALL CHECKS MATCH: {all_ok}")
    if not all_ok:
        raise SystemExit(1)
