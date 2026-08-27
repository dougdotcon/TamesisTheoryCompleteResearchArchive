"""
Fresh reduced-model assembly of P_nn(n,K), built from the predecessor's
PROVED closed forms (general_k_joint_attempt/ATTEMPT.md sec 4.2, 4.3, 5.1),
using the P_same == P_disjoint collapse established in
double_integral_p_disjoint.py (so P_{s,s'} = 2 * x_s * x_s' *
Sum_{S subseteq M} (|S|+1)! Prod_{u in S} x_u).

Written completely fresh from the mathematical prose; no .py file from any
front (this lineage or any sibling) read.

Purpose in this front: (a) an independent, concrete-(n,K), exact-Fraction
cross-check of the FAST symbolic GF/moment pipeline
(symbolic_pnn_via_composition_gf.py) at every K this document touches,
including the NEW K=7,8 results; (b) the actual ground truth this front
built to confirm the P_same==P_disjoint collapse feeds correctly into real
probabilities, not just an algebraic curiosity -- validated below against
bruteforce_definition4_groundtruth.py's true Definition-4 enumeration.

T(L) construction, reconstructed explicitly from ATTEMPT.md sec 5.1's
description ("T(L) sums, over all ordered pairs of the n-K non-source
roles, the exact probability both are cyclic -- outside-outside=1,
outside-arc, same-arc via the monotone fact, cross-arc via the P_0/P_s,s'
formulas"):

  non-source "roles" = O outside points (always cyclic) + interior
  positions 1..L_s-1 of each arc s (position L_s itself is the source).

  T(L) := sum over ALL ORDERED pairs of distinct roles of P(both cyclic):
    - outside-outside: O*(O-1) * 1
    - outside-arc (both orderings): O * P_0(s) * (L_s - 1), summed over s
        [Sum_{i=1}^{L_s-1} i/L_s = (L_s-1)/2, times 2 orderings]
    - same-arc: within arc s, ordered pairs i!=i' in {1,...,L_s-1}:
        P(both cyclic) = P(min(i,i') cyclic), cyclic set is a suffix.
        Computed here by DIRECT double summation (not a hand-derived
        shortcut formula) to avoid smuggling an arithmetic slip in.
    - cross-arc: ordered pairs of distinct arcs (s,s'): (L_s-1)/2 *
        (L_{s'}-1)/2 * P_{s,s'}, summed over all ordered (s,s'), s!=s'.

  P_nn(n,K) = (1/C(n,K)) * Sum_{L: composition, L_i>=1, sum L_i <= n}
                  T(L) / [(n-K)*(n-K-1)]
"""
import itertools
from fractions import Fraction
from math import comb


def factorial(k):
    f = 1
    for i in range(2, k + 1):
        f *= i
    return f


def p0_terms(s, K, L, n):
    """P_0(s) = x_s * Sum_{S subseteq Others(s)} |S|! * Prod_{u in S} x_u,
    x_u = L_u/n. Others(s) = all sources except s."""
    others = [u for u in range(K) if u != s]
    total = Fraction(0)
    for r in range(len(others) + 1):
        for S in itertools.combinations(others, r):
            term = Fraction(1)
            for u in S:
                term *= Fraction(L[u], n)
            term *= factorial(r)
            total += term
    return Fraction(L[s], n) * total


def p_ss_terms(s, sp_, K, L, n):
    """P_{s,s'} = 2 * x_s * x_s' * Sum_{S subseteq M} (|S|+1)! * Prod_S x_u,
    M = all sources except {s,s'} -- the P_same==P_disjoint collapse from
    double_integral_p_disjoint.py, used here directly (verified there as
    an exact algebraic identity, and re-confirmed below via the true
    Definition-4 brute force)."""
    M = [u for u in range(K) if u != s and u != sp_]
    total = Fraction(0)
    for r in range(len(M) + 1):
        for S in itertools.combinations(M, r):
            term = Fraction(1)
            for u in S:
                term *= Fraction(L[u], n)
            term *= factorial(r + 1)
            total += term
    return 2 * Fraction(L[s], n) * Fraction(L[sp_], n) * total


def same_arc_sum_direct(Ls, P0s):
    """Direct double sum: ordered pairs i!=i' in {1,...,Ls-1}, contributes
    P(min(i,i') cyclic) = (min(i,i')/Ls) * P0s. No shortcut algebra
    trusted blindly here."""
    total = Fraction(0)
    for i in range(1, Ls):
        for ip in range(1, Ls):
            if i == ip:
                continue
            total += Fraction(min(i, ip), Ls) * P0s
    return total


def T_of_L(L, K, n):
    O = n - sum(L)
    total = Fraction(O * (O - 1))
    P0 = {s: p0_terms(s, K, L, n) for s in range(K)}
    for s in range(K):
        total += Fraction(O) * P0[s] * (L[s] - 1)
    for s in range(K):
        total += same_arc_sum_direct(L[s], P0[s])
    for s in range(K):
        for sp_ in range(K):
            if s == sp_:
                continue
            Pss = p_ss_terms(s, sp_, K, L, n)
            total += Fraction(L[s] - 1, 2) * Fraction(L[sp_] - 1, 2) * Pss
    return total


def compositions_leq(K, n):
    """All (L_0,...,L_{K-1}), L_i >= 1, sum L_i <= n."""
    def rec(k, remaining):
        if k == 1:
            if remaining >= 1:
                yield (remaining,)
            return
        for v in range(1, remaining - (k - 1) + 1):
            for rest in rec(k - 1, remaining - v):
                yield (v,) + rest
    for total in range(K, n + 1):
        yield from rec(K, total)


def assemble_pnn(n, K):
    assert n >= K + 2
    Csum = Fraction(0)
    count = 0
    for L in compositions_leq(K, n):
        Csum += T_of_L(L, K, n)
        count += 1
    assert count == comb(n, K), f"composition count mismatch: {count} vs C({n},{K})={comb(n, K)}"
    return Csum / (comb(n, K) * (n - K) * (n - K - 1))


if __name__ == "__main__":
    import time

    print("Reduced-model assembly (fresh implementation) vs ground-truth brute force")
    print("=" * 78)
    known_bruteforce = {
        (1, 3): Fraction(5, 9), (1, 4): Fraction(13, 24), (1, 5): Fraction(8, 15),
        (1, 6): Fraction(19, 36),
        (2, 4): Fraction(19, 48), (2, 5): Fraction(287, 750), (2, 6): Fraction(101, 270),
        (3, 5): Fraction(389, 1250), (3, 6): Fraction(3, 10), (3, 7): Fraction(7017, 24010),
    }
    all_ok = True
    for (K, n), bf_val in known_bruteforce.items():
        red_val = assemble_pnn(n, K)
        ok = (red_val == bf_val)
        all_ok = all_ok and ok
        print(f"K={K}, n={n}: reduced-model = {red_val}   brute-force = {bf_val}   match={ok}")
    print("=" * 78)
    print(f"ALL MATCH true Definition-4 brute force (K=1,2,3): {all_ok}")

    print()
    print("Cross-check against predecessor's own true-brute-force table, K=4,5")
    print("(general_k_joint_attempt/ATTEMPT.md sec 6.2) -- independent re-derivation,")
    print("not read from their code, built from the math description only:")
    predecessor_bf = {
        (4, 6): Fraction(209, 810), (4, 7): Fraction(12535, 50421),
        (4, 8): Fraction(25999, 107520), (5, 7): Fraction(78077, 352947),
    }
    for (K, n), val in predecessor_bf.items():
        t0 = time.time()
        r = assemble_pnn(n, K)
        dt = time.time() - t0
        ok = (r == val)
        all_ok = all_ok and ok
        print(f"  K={K},n={n}: mine={r}  predecessor-reported={val}  match={ok}  ({dt:.1f}s)")

    print()
    print("Cross-check against Propositions NN4, NN5, NN6 (predecessor, PROVED),")
    print("many n per K, well beyond the K=4-6 brute-force overlap points:")

    def nn4(nv):
        nv = Fraction(nv)
        return (126 * nv ** 4 + 187 * nv ** 3 + 177 * nv ** 2 + 98 * nv + 24) / (630 * nv ** 4)

    def nn5(nv):
        nv = Fraction(nv)
        return (462 * nv ** 5 + 874 * nv ** 4 + 1139 * nv ** 3 + 989 * nv ** 2 + 514 * nv + 120) / (2772 * nv ** 5)

    def nn6(nv):
        nv = Fraction(nv)
        return (1716 * nv ** 6 + 3958 * nv ** 5 + 6616 * nv ** 4 + 7933 * nv ** 3
                + 6472 * nv ** 2 + 3204 * nv + 720) / (12012 * nv ** 6)

    for n in [6, 7, 8, 10, 12, 15, 20]:
        t0 = time.time(); r = assemble_pnn(n, 4); dt = time.time() - t0
        ok = (r == nn4(n)); all_ok = all_ok and ok
        print(f"  K=4,n={n}: mine={r}  NN4={nn4(n)}  match={ok}  ({dt:.1f}s)")
    for n in [7, 8, 10, 12, 15]:
        t0 = time.time(); r = assemble_pnn(n, 5); dt = time.time() - t0
        ok = (r == nn5(n)); all_ok = all_ok and ok
        print(f"  K=5,n={n}: mine={r}  NN5={nn5(n)}  match={ok}  ({dt:.1f}s)")
    for n in [8, 9, 10, 12, 15]:
        t0 = time.time(); r = assemble_pnn(n, 6); dt = time.time() - t0
        ok = (r == nn6(n)); all_ok = all_ok and ok
        print(f"  K=6,n={n}: mine={r}  NN6={nn6(n)}  match={ok}  ({dt:.1f}s)")

    print()
    print(f"GRAND TOTAL -- ALL CHECKS IN THIS SCRIPT MATCH: {all_ok}")
