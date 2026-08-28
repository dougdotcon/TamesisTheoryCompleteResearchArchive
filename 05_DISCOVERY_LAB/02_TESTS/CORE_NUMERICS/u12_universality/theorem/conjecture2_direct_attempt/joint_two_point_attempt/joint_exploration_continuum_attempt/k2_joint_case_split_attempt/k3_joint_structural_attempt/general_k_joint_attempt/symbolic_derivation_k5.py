"""
Attempt at full symbolic (sympy, exact Rational) closed-form derivation of
P_nn(n,5), generalizing symbolic_derivation_k4.py (quintuple sum).
"""
import sympy as sp
from itertools import combinations
import time

K = 5
n = sp.Symbol('n', positive=True)
L = sp.symbols('L0 L1 L2 L3 L4', positive=True)


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
    print("Building T(L0..L4) symbolically...", flush=True)
    T = build_T()
    print(f"  done in {time.time()-t0:.1f}s, ops={sp.count_ops(T)}", flush=True)

    expr = T
    bounds = [
        (L[4], 1, n - L[0] - L[1] - L[2] - L[3]),
        (L[3], 1, n - L[0] - L[1] - L[2] - 1),
        (L[2], 1, n - L[0] - L[1] - 2),
        (L[1], 1, n - L[0] - 3),
        (L[0], 1, n - 4),
    ]
    for var, lo, hi in bounds:
        t1 = time.time()
        expr = sp.summation(expr, (var, lo, hi))
        expr = sp.together(sp.expand(expr))
        print(f"summed {var} in {time.time()-t1:.1f}s, ops={sp.count_ops(expr)}", flush=True)

    binom_n5 = sp.factorial(n) / (sp.factorial(5) * sp.factorial(n - 5))
    denom = binom_n5 * (n - 5) * (n - 6)
    P_nn_5 = sp.simplify(expr / denom)
    P_nn_5 = sp.factor(sp.together(P_nn_5))
    print("FINAL Proposition NN5 (symbolic):", flush=True)
    print(P_nn_5, flush=True)
    print("Total elapsed:", time.time() - t0, "s", flush=True)
