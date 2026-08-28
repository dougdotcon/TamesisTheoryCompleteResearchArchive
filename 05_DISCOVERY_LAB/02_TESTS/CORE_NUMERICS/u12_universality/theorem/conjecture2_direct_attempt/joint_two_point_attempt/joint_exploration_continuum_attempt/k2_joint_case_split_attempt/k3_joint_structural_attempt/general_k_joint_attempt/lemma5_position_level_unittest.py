"""
Position-level (not just node/arc-level) brute-force verification of the
general-K Lemma 5 analogue:

  P(pos i in ARC(s) cyclic)                    = (i/L_s) * P0(s)
  P(pos i in ARC(s), pos i' in ARC(s') cyclic)  = (i/L_s)*(i'/L_s') * P_{s,s'}   (s!=s')
  P(pos i, pos i' both in ARC(s), i<i')         = (i/L_s) * P0(s)

This enumerates ALL n^K exact landing choices (U_0,...,U_{K-1}) each
uniform over the n abstract slots (K arcs of given lengths + O outside
slots), builds the explicit functional graph position-by-position, and
determines cyclicity of every query position by direct graph traversal --
no reference to the destination-table shortcut or the P0/P_pair formulas
except for the final comparison. Fresh, independent implementation.
"""
from itertools import product
from fractions import Fraction


def build_slots(L, O):
    """Returns list of all abstract slot labels, in a fixed order, and a
    dict mapping slot -> its deterministic pi-successor slot (before any
    reroute is applied) for interior positions."""
    slots = []
    succ = {}
    for s, Ls in enumerate(L):
        for i in range(1, Ls + 1):
            slots.append(('arc', s, i))
        for i in range(1, Ls):
            succ[('arc', s, i)] = ('arc', s, i + 1)
        # succ[('arc', s, Ls)] is set by the reroute (U_s), not here
    for j in range(O):
        slots.append(('out', j))
        succ[('out', j)] = ('out', j)  # simplest: each outside slot a fixed pt
    return slots, succ


def is_cyclic(g, p):
    seen = set()
    cur = p
    while True:
        if cur not in g:
            return False
        if cur in seen:
            return cur == p
        seen.add(cur)
        cur = g[cur]


def position_level_probs(K, L, O):
    n = sum(L) + O
    slots, succ = build_slots(L, O)
    sources = [('arc', s, L[s]) for s in range(K)]

    # P(pos i in ARC(s) cyclic) for every s,i ; P(cross pairs); P(same-arc pairs)
    single_counts = {(s, i): Fraction(0) for s in range(K) for i in range(1, L[s] + 1)}
    cross_counts = {}
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                for i in range(1, L[s] + 1):
                    for ip in range(1, L[sp_] + 1):
                        cross_counts[(s, i, sp_, ip)] = Fraction(0)
    same_counts = {}
    for s in range(K):
        for i in range(1, L[s] + 1):
            for ip in range(i + 1, L[s] + 1):
                same_counts[(s, i, ip)] = Fraction(0)

    total = 0
    for U in product(slots, repeat=K):
        # U[t] is the landing slot for source t's reroute
        g = dict(succ)
        for t in range(K):
            g[sources[t]] = U[t]
        total += 1
        prob = Fraction(1, n ** K)  # will sum counts as integer, divide at end

        for s in range(K):
            for i in range(1, L[s] + 1):
                if is_cyclic(g, ('arc', s, i)):
                    single_counts[(s, i)] += 1

        for s in range(K):
            for sp_ in range(K):
                if sp_ != s:
                    for i in range(1, L[s] + 1):
                        ci = is_cyclic(g, ('arc', s, i))
                        if not ci:
                            continue
                        for ip in range(1, L[sp_] + 1):
                            if is_cyclic(g, ('arc', sp_, ip)):
                                cross_counts[(s, i, sp_, ip)] += 1

        for s in range(K):
            for i in range(1, L[s] + 1):
                ci = is_cyclic(g, ('arc', s, i))
                if not ci:
                    continue
                for ip in range(i + 1, L[s] + 1):
                    if is_cyclic(g, ('arc', s, ip)):
                        same_counts[(s, i, ip)] += 1

    denom = n ** K
    single = {k: Fraction(v, denom) for k, v in single_counts.items()}
    cross = {k: Fraction(v, denom) for k, v in cross_counts.items()}
    same = {k: Fraction(v, denom) for k, v in same_counts.items()}
    return single, cross, same, n


# --- formulas under test (re-derived, imported logic duplicated for full
# independence would be ideal, but to test the ACTUAL claimed formulas we
# reuse the P0/P_pair combinatorial sums exactly as derived in
# lemma5_general_k.py's docstring; re-implemented fresh here, not imported) ---
from itertools import combinations


def P0_exact(s, K, x):
    others = [u for u in range(K) if u != s]
    total = Fraction(0)
    import math
    for r in range(0, len(others) + 1):
        for S in combinations(others, r):
            prod = Fraction(1)
            for u in S:
                prod *= x[u]
            total += math.factorial(r) * prod
    return x[s] * total


def P_pair_exact(s, sp_, K, x):
    import math
    M = [u for u in range(K) if u != s and u != sp_]
    # same-cycle
    total_same = Fraction(0)
    for r in range(0, len(M) + 1):
        for S in combinations(M, r):
            prod = Fraction(1)
            for u in S:
                prod *= x[u]
            total_same += math.factorial(r + 1) * prod
    same = x[s] * x[sp_] * total_same
    # disjoint-cycle
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


def check(K, L, O):
    n = sum(L) + O
    x = [Fraction(L[s], n) for s in range(K)]
    single, cross, same, n_check = position_level_probs(K, L, O)
    assert n_check == n

    P0 = [P0_exact(s, K, x) for s in range(K)]
    ok_single = True
    for s in range(K):
        for i in range(1, L[s] + 1):
            pred = Fraction(i, L[s]) * P0[s]
            actual = single[(s, i)]
            if pred != actual:
                ok_single = False
                print(f"  MISMATCH single s={s} i={i}: pred={pred} actual={actual}")

    ok_cross = True
    Ppair = {}
    for s in range(K):
        for sp_ in range(K):
            if sp_ != s:
                Ppair[(s, sp_)] = P_pair_exact(s, sp_, K, x)
    for s in range(K):
        for sp_ in range(K):
            if sp_ == s:
                continue
            for i in range(1, L[s] + 1):
                for ip in range(1, L[sp_] + 1):
                    pred = Fraction(i, L[s]) * Fraction(ip, L[sp_]) * Ppair[(s, sp_)]
                    actual = cross[(s, i, sp_, ip)]
                    if pred != actual:
                        ok_cross = False
                        print(f"  MISMATCH cross s={s} i={i} sp={sp_} ip={ip}: "
                              f"pred={pred} actual={actual}")

    ok_same = True
    for s in range(K):
        for i in range(1, L[s] + 1):
            for ip in range(i + 1, L[s] + 1):
                pred = Fraction(i, L[s]) * P0[s]
                actual = same[(s, i, ip)]
                if pred != actual:
                    ok_same = False
                    print(f"  MISMATCH same s={s} i={i} ip={ip}: pred={pred} actual={actual}")

    print(f"K={K}, L={L}, O={O}, n={n}: single-point match={ok_single}, "
          f"cross-arc match={ok_cross}, same-arc match={ok_same}")
    return ok_single and ok_cross and ok_same


if __name__ == '__main__':
    print("=== Position-level brute force vs Lemma-5-general-K formulas ===")
    cases = [
        (1, (3,), 2),
        (2, (2, 3), 2),
        (2, (3, 2), 1),
        (3, (2, 2, 2), 2),
        (3, (2, 2, 3), 1),
        (4, (2, 2, 2, 2), 1),
        (4, (2, 2, 1, 2), 1),
        (5, (1, 2, 1, 2, 1), 1),
    ]
    all_ok = True
    for K, L, O in cases:
        all_ok = check(K, L, O) and all_ok
    print()
    print("ALL MATCH" if all_ok else "SOME MISMATCHES")
