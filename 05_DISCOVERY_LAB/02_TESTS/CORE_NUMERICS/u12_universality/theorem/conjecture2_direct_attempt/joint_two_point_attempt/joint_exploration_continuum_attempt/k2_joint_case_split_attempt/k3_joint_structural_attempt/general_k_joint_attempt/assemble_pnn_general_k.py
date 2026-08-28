"""
General-K assembly of P_nn(n,K), the reduced-model computation, exact
Fraction arithmetic, no floating point. Fresh code, generalizing the
predecessor's own K=2/K=3 T(L) assembly (THEOREM.md / ATTEMPT.md prose)
to general K using the Lemma-5-general-K formulas verified in
lemma5_general_k.py / lemma5_position_level_general_k.py.

  P_nn(n,K) = (1 / C(n,K)) * sum_{compositions (L_0,...,L_{K-1}), L_s>=1,
                                    O=n-sum(L)>=0}
                T(L) / [(n-K)(n-K-1)]

  T(L) = O(O-1)                                         [outside-outside]
       + 2*O* sum_s sum_{i=1}^{L_s-1} P(i in ARC(s) cyc) [outside-arc, both orders]
       + sum_s sum_{i<i'<=L_s-1} 2 * P(i in ARC(s) cyc)  [same-arc, both orders;
                                                            uses monotone fact]
       + sum_{s != s'} sum_{i=1}^{L_s-1} sum_{i'=1}^{L_{s'}-1}
             P(i in ARC(s), i' in ARC(s') both cyc)       [cross-arc]

using the closed forms:
  P(i in ARC(s) cyc)                 = (i/L_s) * P0(s)
  P(i in ARC(s), i' in ARC(s') cyc)  = (i/L_s)*(i'/L_s') * P_pair(s,s')
"""
from fractions import Fraction
from itertools import combinations
import math


def P0_exact(s, K, x):
    others = [u for u in range(K) if u != s]
    total = Fraction(0)
    for r in range(0, len(others) + 1):
        for S in combinations(others, r):
            prod = Fraction(1)
            for u in S:
                prod *= x[u]
            total += math.factorial(r) * prod
    return x[s] * total


def P_pair_exact(s, sp_, K, x):
    M = [u for u in range(K) if u != s and u != sp_]
    total_same = Fraction(0)
    for r in range(0, len(M) + 1):
        for S in combinations(M, r):
            prod = Fraction(1)
            for u in S:
                prod *= x[u]
            total_same += math.factorial(r + 1) * prod
    same = x[s] * x[sp_] * total_same

    total_disj = Fraction(0)
    m = len(M)
    for mask in range(3 ** m):
        S1, S2 = [], []
        code = mask
        for j in range(m):
            d = code % 3
            code //= 3
            if d == 0:
                S1.append(M[j])
            elif d == 1:
                S2.append(M[j])
        p1 = Fraction(1)
        for u in S1:
            p1 *= x[u]
        p2 = Fraction(1)
        for u in S2:
            p2 *= x[u]
        total_disj += math.factorial(len(S1)) * p1 * math.factorial(len(S2)) * p2
    disj = x[s] * x[sp_] * total_disj
    return same + disj


def sum_i_cyc(L_s, P0_s):
    # sum_{i=1}^{L_s-1} (i/L_s)*P0_s = P0_s * (L_s-1)/2
    return P0_s * Fraction(L_s - 1, 2)


def sum_same_arc_ordered(L_s, P0_s):
    # sum over ordered i != i' in 1..L_s-1 of P(min cyclic) = 2*sum_{i<i'} (i/L_s)P0_s
    # = 2*(P0_s/L_s) * sum_{i=1}^{L_s-2} i*(L_s-1-i)
    if L_s - 1 < 2:
        return Fraction(0)
    total = Fraction(0)
    for i in range(1, L_s - 1):
        total += i * (L_s - 1 - i)
    return 2 * Fraction(P0_s, L_s) * total


def sum_cross_arc(L_s, L_sp, Ppair):
    # sum_{i=1}^{L_s-1} sum_{i'=1}^{L_sp-1} (i/L_s)(i'/L_sp)*Ppair
    return Ppair * Fraction(L_s - 1, 2) * Fraction(L_sp - 1, 2)


def T_of_L(L, O, n):
    K = len(L)
    x = [Fraction(L[s], n) for s in range(K)]
    P0 = [P0_exact(s, K, x) for s in range(K)]
    total = Fraction(O * (O - 1))
    for s in range(K):
        total += 2 * O * sum_i_cyc(L[s], P0[s])
        total += sum_same_arc_ordered(L[s], P0[s])
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                Ppair = P_pair_exact(s, sp_, K, x)
                total += sum_cross_arc(L[s], L[sp_], Ppair)
    return total


def compositions(n, K):
    """Yield all (L_0,...,L_{K-1}) with L_s>=1, sum<=n (O=n-sum>=0)."""
    if K == 1:
        for L0 in range(1, n + 1):
            yield (L0,)
        return

    def rec(remaining_n, k):
        if k == 1:
            for L in range(1, remaining_n + 1):
                yield (L,)
            return
        for L in range(1, remaining_n - (k - 1) + 1):
            for rest in rec(remaining_n - L, k - 1):
                yield (L,) + rest

    yield from rec(n, K)


def binom(n, k):
    return math.comb(n, k)


def P_nn(n, K):
    assert n > K
    num = Fraction(0)
    count = 0
    for L in compositions(n, K):
        O = n - sum(L)
        assert O >= 0
        num += T_of_L(L, O, n)
        count += 1
    assert count == binom(n, K)
    denom = binom(n, K) * (n - K) * (n - K - 1)
    return Fraction(num, denom) if isinstance(num, int) else num / denom


if __name__ == '__main__':
    import sys
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n_lo = int(sys.argv[2]) if len(sys.argv) > 2 else K + 2
    n_hi = int(sys.argv[3]) if len(sys.argv) > 3 else K + 12
    print(f"=== P_nn(n,{K}) reduced-model exact computation ===")
    for n in range(n_lo, n_hi + 1):
        val = P_nn(n, K)
        print(f"n={n}: P_nn(n,{K}) = {val} = {float(val):.10f}")
