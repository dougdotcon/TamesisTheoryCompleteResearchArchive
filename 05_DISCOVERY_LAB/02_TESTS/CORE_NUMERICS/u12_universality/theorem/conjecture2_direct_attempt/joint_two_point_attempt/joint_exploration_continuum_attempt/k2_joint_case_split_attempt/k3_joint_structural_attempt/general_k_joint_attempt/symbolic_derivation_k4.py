"""
Attempt at a full symbolic (sympy, exact Rational, no floating point)
closed-form derivation of P_nn(n,4), generalizing the K=3 predecessor's
symbolic_derivation_k3.py approach (quadruple sum instead of triple).

If this completes, it upgrades Proposition NN4 from "exact-interpolation
verified at 20+ independent points, matching true brute force at n=6,7(,8)"
to a fully symbolic, no-floating-point, closed-form derivation exactly in
the archive's PROVED style.
"""
import sympy as sp
from itertools import combinations
import time

K = 4
n = sp.Symbol('n', positive=True)
L = sp.symbols('L0 L1 L2 L3', positive=True)


def P0_sym(s, x):
    others = [u for u in range(K) if u != s]
    total = sp.Integer(0)
    for r in range(0, len(others) + 1):
        for S in combinations(others, r):
            prod = sp.Integer(1)
            for u in S:
                prod *= x[u]
            total += sp.factorial(r) * prod
    return sp.expand(x[s] * total)


def P_pair_sym(s, sp_, x):
    M = [u for u in range(K) if u != s and u != sp_]
    total_same = sp.Integer(0)
    for r in range(0, len(M) + 1):
        for S in combinations(M, r):
            prod = sp.Integer(1)
            for u in S:
                prod *= x[u]
            total_same += sp.factorial(r + 1) * prod
    same = x[s] * x[sp_] * total_same

    total_disj = sp.Integer(0)
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
        p1 = sp.Integer(1)
        for u in S1:
            p1 *= x[u]
        p2 = sp.Integer(1)
        for u in S2:
            p2 *= x[u]
        total_disj += sp.factorial(len(S1)) * p1 * sp.factorial(len(S2)) * p2
    disj = x[s] * x[sp_] * total_disj
    return sp.expand(same + disj)


def build_T():
    x = [L[s] / n for s in range(K)]
    O = n - sum(L)
    P0 = [P0_sym(s, x) for s in range(K)]
    T = O * (O - 1)
    for s in range(K):
        T += 2 * O * P0[s] * (L[s] - 1) / 2
        # same-arc ordered-pair sum: 2 * (P0[s]/L[s]) * sum_{i=1}^{Ls-2} i*(Ls-1-i)
        i = sp.Symbol('i_')
        inner = sp.summation(i * (L[s] - 1 - i), (i, 1, L[s] - 2))
        T += 2 * (P0[s] / L[s]) * inner
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                Ppair = P_pair_sym(s, sp_, x)
                T += Ppair * (L[s] - 1) / 2 * (L[sp_] - 1) / 2
    return sp.together(sp.expand(T))


if __name__ == '__main__':
    t0 = time.time()
    print("Building T(L0,L1,L2,L3) symbolically...")
    T = build_T()
    print(f"  done in {time.time()-t0:.1f}s")
    print("T has", sp.count_ops(T), "ops")

    # sum over L3 = 1 .. n-L0-L1-L2, then L2 = 1..n-L0-L1-1, then L1 = 1..n-L0-2,
    # then L0 = 1..n-3
    t1 = time.time()
    S3 = sp.summation(T, (L[3], 1, n - L[0] - L[1] - L[2]))
    S3 = sp.together(sp.expand(S3))
    print(f"summed L3 in {time.time()-t1:.1f}s, ops={sp.count_ops(S3)}")

    t2 = time.time()
    S2 = sp.summation(S3, (L[2], 1, n - L[0] - L[1] - 1))
    S2 = sp.together(sp.expand(S2))
    print(f"summed L2 in {time.time()-t2:.1f}s, ops={sp.count_ops(S2)}")

    t3 = time.time()
    S1 = sp.summation(S2, (L[1], 1, n - L[0] - 2))
    S1 = sp.together(sp.expand(S1))
    print(f"summed L1 in {time.time()-t3:.1f}s, ops={sp.count_ops(S1)}")

    t4 = time.time()
    S0 = sp.summation(S1, (L[0], 1, n - 3))
    S0 = sp.together(sp.expand(S0))
    print(f"summed L0 in {time.time()-t4:.1f}s, ops={sp.count_ops(S0)}")

    binom_n4 = sp.factorial(n) / (sp.factorial(4) * sp.factorial(n - 4))
    denom = binom_n4 * (n - 4) * (n - 5)
    P_nn_4 = sp.simplify(S0 / denom)
    P_nn_4 = sp.factor(sp.together(P_nn_4))
    print("FINAL Proposition NN4 (symbolic):")
    print(P_nn_4)
    print("Total elapsed:", time.time() - t0, "s")
