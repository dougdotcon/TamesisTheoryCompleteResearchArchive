"""
General-K symbolic (sympy, exact Rational, no floating point) closed-form
derivation of P_nn(n,K), for any concrete integer K >= 1. This is the
master derivation script of this front: a single parametrized algorithm
that, given K, produces Proposition NN_K -- the exact closed form of
P_nn(n,K) -- by exact symbolic K-fold summation.

Generalizes symbolic_derivation_k3.py (K3-joint-structural-attempt front,
predecessor) beyond K=3, using two new general-K mechanisms proved and
verified in this front's other scripts:

  (1) Governing-Source Reindexing (general K) -- verified in
      gsr_general_k_unittest.py -- lets us work directly with the
      governing-source-indexed arc lengths (L_0,...,L_{K-1}, O), uniform
      over compositions of n into K+1 nonnegative parts (L_s>=1), with
      topology marginalized out entirely.

  (2) The general-K Lemma 5 analogue (single-point / cross-arc closed
      forms), derived from Lemma 4 (Cycle-Predecessor Uniqueness, general
      K, verified in lemma4_general_k_unittest.py) and the uniform-landing-
      position fact, verified in lemma5_general_k_unittest.py (node-level,
      K=1..6) and lemma5_position_level_unittest.py (position-level,
      K=1..5):

        x_s := L_s/n  (s = 0,...,K-1)

        P0(s) := P(node s cyclic in the K-node destination graph)
               = x_s * sum_{S subseteq Others(s)} |S|! * prod_{u in S} x_u

        P(pos i in ARC(s) cyclic) = (i/L_s) * P0(s)

        For s != s', with M := Others(s,s') (size K-2):
        P_same(s,s')     = x_s*x_s' * sum_{S subseteq M} (|S|+1)! * prod_{u in S} x_u
        P_disjoint(s,s') = x_s*x_s' * sum_{S1,S2 subseteq M disjoint}
                                |S1|!*prod_{S1}x * |S2|!*prod_{S2}x
        P_pair(s,s') = P_same(s,s') + P_disjoint(s,s')

        P(pos i in ARC(s), pos i' in ARC(s') both cyclic)
            = (i/L_s)*(i'/L_s') * P_pair(s,s')

  (3) Assembly (direct generalization of the predecessor's K=2/K=3 T(L)
      assembly, THEOREM.md / ATTEMPT.md prose):

        P_nn(n,K) = (1/C(n,K)) * sum_{compositions (L_0,...,L_{K-1})}
                        T(L) / [(n-K)(n-K-1)]

      with T(L) the sum over all ordered pairs of the n-K non-source
      "roles" (O outside points, always cyclic; interior positions
      1..L_s-1 of each arc) of P(both roles cyclic), evaluated exactly via
      the closed forms above and the same-arc monotone fact (cyclic set of
      an arc is a suffix {k,...,L_s}, so for i<i' in the same arc, both
      cyclic iff i cyclic).

Usage: python3 symbolic_derivation_general_k.py K   (K = 1,...,6 tested
       in this front; the algorithm itself places no a priori limit on K,
       only wall-clock time, see ATTEMPT.md Sec 6 for the honest scaling
       diagnosis).
"""
import sys
import time
from itertools import combinations
import sympy as sp


def P0_sym(s, K, x):
    others = [u for u in range(K) if u != s]
    total = sp.Integer(0)
    for r in range(0, len(others) + 1):
        for S in combinations(others, r):
            prod = sp.Integer(1)
            for u in S:
                prod *= x[u]
            total += sp.factorial(r) * prod
    return sp.expand(x[s] * total)


def P_pair_sym(s, sp_, K, x):
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


def build_T(K, n, L):
    x = [L[s] / n for s in range(K)]
    O = n - sum(L)
    P0 = [P0_sym(s, K, x) for s in range(K)]
    T = O * (O - 1)
    i_ = sp.Symbol('i_')
    for s in range(K):
        T += 2 * O * P0[s] * (L[s] - 1) / 2
        inner = sp.summation(i_ * (L[s] - 1 - i_), (i_, 1, L[s] - 2))
        T += 2 * (P0[s] / L[s]) * inner
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                Ppair = P_pair_sym(s, sp_, K, x)
                T += Ppair * (L[s] - 1) / 2 * (L[sp_] - 1) / 2
    return sp.together(sp.expand(T))


def derive_P_nn(K, verbose=True):
    n = sp.Symbol('n', positive=True)
    L = list(sp.symbols(f'L0:{K}', positive=True))

    t0 = time.time()
    if verbose:
        print(f"[K={K}] Building T(L_0,...,L_{K-1}) symbolically...", flush=True)
    T = build_T(K, n, L)
    if verbose:
        print(f"[K={K}]   done in {time.time()-t0:.1f}s, ops={sp.count_ops(T)}",
              flush=True)

    expr = T
    # Sum L_{K-1} first (bound n - L_0 - ... - L_{K-2}, i.e. reserve 0 extra
    # since no other not-yet-summed variable remains below it), then
    # L_{K-2}, ..., down to L_0. When about to sum L_j, the variables
    # L_{j+1},...,L_{K-1} have ALREADY been integrated out (each needed
    # >=1), so summing L_j must reserve (K-1-j) units of room for them:
    # hi = n - sum(L_0..L_{j-1}) - (K-1-j). (Matches the predecessor's own
    # K=3 bounds exactly: j=2 -> n-L0-L1; j=1 -> n-L0-1; j=0 -> n-2.)
    for j in reversed(range(K)):
        lo = 1
        hi = n - sum(L[:j]) - (K - 1 - j)
        t1 = time.time()
        expr = sp.summation(expr, (L[j], lo, hi))
        expr = sp.together(sp.expand(expr))
        if verbose:
            print(f"[K={K}]   summed L{j} in {time.time()-t1:.1f}s, "
                  f"ops={sp.count_ops(expr)}", flush=True)

    binom_nK = sp.factorial(n) / (sp.factorial(K) * sp.factorial(n - K))
    denom = binom_nK * (n - K) * (n - K - 1)
    P_nn_K = sp.simplify(expr / denom)
    P_nn_K = sp.factor(sp.together(P_nn_K))
    if verbose:
        print(f"[K={K}] FINAL Proposition NN{K} (symbolic):", flush=True)
        print(f"  P_nn(n,{K}) = {P_nn_K}", flush=True)
        print(f"[K={K}] Total elapsed: {time.time()-t0:.1f}s", flush=True)
    return P_nn_K


if __name__ == '__main__':
    Ks = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5, 6]
    results = {}
    for K in Ks:
        results[K] = derive_P_nn(K)
        print()
    print("=== Summary ===")
    for K, val in results.items():
        print(f"K={K}: P_nn(n,{K}) = {val}")
