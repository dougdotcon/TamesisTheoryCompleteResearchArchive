"""
General-K closed-form single-point / cross-arc formulas (the general-K
analogue of Lemma 5 of the K=3 predecessor front), derived fresh from the
cycle-predecessor structure (Lemma 4, verified general-K in
lemma4_general_k.py) and the uniform-landing-position fact.

Derivation summary (see ATTEMPT.md for the full written proof):

Let x_s := L_s/n for s=0..K-1 (x_D := O/n = 1 - sum x_s).

P0(s) := P(node s is cyclic in the K-node destination graph)
       = x_s * sum_{S subset of Others(s)} |S|! * prod_{u in S} x_u
  where Others(s) = {0,...,K-1} \ {s}.

P(position i in ARC(s) is cyclic) = (i / L_s) * P0(s)      [i = 1..L_s]

For s != s', P_{s,s'} := P(s AND s' both cyclic)
  = P_same(s,s') + P_disjoint(s,s'), where, with M := Others(s,s') :=
  {0,...,K-1} \ {s,s'}  (size K-2):

  P_same(s,s')     = x_s * x_s' * sum_{S subset M} (|S|+1)! * prod_{u in S} x_u
  P_disjoint(s,s') = x_s * x_s' * sum_{S1,S2 subset M, S1 cap S2 = empty}
                          |S1|! * prod_{u in S1} x_u * |S2|! * prod_{u in S2} x_u

P(pos i in ARC(s), pos i' in ARC(s') both cyclic) = (i/L_s)*(i'/L_s') * P_{s,s'}

This script:
  (1) implements these formulas symbolically (sympy.Rational arithmetic,
      L_0..L_{K-1}, n as symbols) for a given concrete K,
  (2) cross-checks them against a DIRECT, independent, brute-force
      enumeration of the full (K+1)^K destination table (own implementation,
      no shortcut, exact Fraction arithmetic) at concrete numeric (n, L)
      values, for K = 1,...,6.
"""
from itertools import product, combinations
from fractions import Fraction
import sympy as sp


def P0_formula(s, K, x):
    """x: list of K sympy symbols/exprs x_0..x_{K-1}."""
    others = [u for u in range(K) if u != s]
    total = sp.Integer(0)
    for r in range(0, len(others) + 1):
        for S in combinations(others, r):
            prod = sp.Integer(1)
            for u in S:
                prod *= x[u]
            total += sp.factorial(r) * prod
    return x[s] * total


def P_same_formula(s, sp_, K, x):
    M = [u for u in range(K) if u != s and u != sp_]
    total = sp.Integer(0)
    for r in range(0, len(M) + 1):
        for S in combinations(M, r):
            prod = sp.Integer(1)
            for u in S:
                prod *= x[u]
            total += sp.factorial(r + 1) * prod
    return x[s] * x[sp_] * total


def P_disjoint_formula(s, sp_, K, x):
    M = [u for u in range(K) if u != s and u != sp_]
    total = sp.Integer(0)
    m = len(M)
    for mask1 in range(3 ** m):
        # base-3 digit d in {0,1,2}: 0=in S1, 1=in S2, 2=neither
        S1 = []
        S2 = []
        code = mask1
        ok = True
        for j in range(m):
            d = code % 3
            code //= 3
            if d == 0:
                S1.append(M[j])
            elif d == 1:
                S2.append(M[j])
        prod1 = sp.Integer(1)
        for u in S1:
            prod1 *= x[u]
        prod2 = sp.Integer(1)
        for u in S2:
            prod2 *= x[u]
        total += sp.factorial(len(S1)) * prod1 * sp.factorial(len(S2)) * prod2
    return x[s] * x[sp_] * total


def P_pair_formula(s, sp_, K, x):
    return sp.expand(P_same_formula(s, sp_, K, x) + P_disjoint_formula(s, sp_, K, x))


# ---------------------------------------------------------------------
# Independent ground truth: brute-force enumeration of the (K+1)^K
# destination table, exact Fraction arithmetic, no reference whatsoever
# to the formulas above.
# ---------------------------------------------------------------------

def analyze_dest(dest, K):
    cyclic = set()
    for s in range(K):
        cur = s
        visited = set()
        ok = False
        while True:
            if cur is None:
                break
            if cur in visited:
                ok = (cur == s)
                break
            visited.add(cur)
            cur = dest[cur]
        if ok:
            cyclic.add(s)
    return cyclic


def brute_force_P0_and_pairs(K, L, n):
    """L: tuple of K positive ints, n: total. O = n - sum(L). Returns
    (P0_dict[s], Ppair_dict[(s,s')]) via exact enumeration over all n^K
    landing choices restricted only through the DEST-arc level (since,
    given dest is fixed, cyclicity of s does not depend on exact landing
    positions -- only 'both cyclic' node-level events matter here)."""
    O = n - sum(L)
    assert O >= 0
    weights = list(L) + [O]  # index K = DEAD
    total_n = n
    P0 = {s: Fraction(0) for s in range(K)}
    Ppair = {}
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                Ppair[(s, sp_)] = Fraction(0)

    # enumerate all K-tuples of dest choices, each choice in {0..K-1, DEAD},
    # weighted by product of weights[choice]/n, exact Fraction.
    choices_per_source = list(range(K)) + [None]
    for dest_tuple in product(choices_per_source, repeat=K):
        dest = {t: dest_tuple[t] for t in range(K)}
        prob = Fraction(1)
        for t in range(K):
            w = weights[dest[t]] if dest[t] is not None else weights[K]
            prob *= Fraction(w, total_n)
        cyclic = analyze_dest(dest, K)
        for s in cyclic:
            P0[s] += prob
        for s in cyclic:
            for sp_ in cyclic:
                if sp_ != s:
                    Ppair[(s, sp_)] += prob
    return P0, Ppair


def check_K(K, n_val, L_val):
    x_syms = sp.symbols(f'x0:{K}')
    n_sym = sp.Symbol('n')
    L_syms = sp.symbols(f'L0:{K}')
    # substitute numeric n, L; x_s = L_s/n
    subs = {n_sym: n_val}
    for i in range(K):
        subs[L_syms[i]] = L_val[i]
    x_num = [sp.Rational(L_val[i], n_val) for i in range(K)]

    P0_pred = {}
    for s in range(K):
        val = P0_formula(s, K, x_num)
        P0_pred[s] = Fraction(int(sp.fraction(sp.nsimplify(val))[0]),
                               int(sp.fraction(sp.nsimplify(val))[1]))

    Ppair_pred = {}
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                val = P_pair_formula(s, sp_, K, x_num)
                num, den = sp.fraction(sp.nsimplify(val))
                Ppair_pred[(s, sp_)] = Fraction(int(num), int(den))

    P0_true, Ppair_true = brute_force_P0_and_pairs(K, L_val, n_val)

    ok_P0 = all(P0_pred[s] == P0_true[s] for s in range(K))
    ok_pair = all(Ppair_pred[k] == Ppair_true[k] for k in Ppair_true)
    print(f"K={K}, n={n_val}, L={L_val}: P0 match={ok_P0}, pair match={ok_pair}")
    if not ok_P0:
        print("  P0_pred:", P0_pred)
        print("  P0_true:", P0_true)
    if not ok_pair:
        for k in Ppair_true:
            if Ppair_pred[k] != Ppair_true[k]:
                print("  mismatch", k, Ppair_pred[k], Ppair_true[k])
    return ok_P0 and ok_pair


if __name__ == '__main__':
    print("=== General-K Lemma 5 analogue: formula vs brute-force destination table ===")
    all_ok = True
    test_cases = [
        (1, 5, (2,)),
        (2, 9, (3, 4)),
        (2, 10, (2, 5)),
        (3, 12, (3, 4, 2)),
        (3, 9, (2, 2, 2)),
        (4, 13, (3, 3, 2, 2)),
        (4, 11, (2, 2, 2, 2)),
        (5, 15, (2, 3, 2, 3, 2)),
        (5, 12, (2, 2, 2, 2, 2)),
        (6, 15, (2, 2, 2, 2, 2, 2)),
    ]
    for K, n_val, L_val in test_cases:
        ok = check_K(K, n_val, L_val)
        all_ok = all_ok and ok
    print()
    print("ALL MATCH" if all_ok else "SOME MISMATCHES FOUND")
