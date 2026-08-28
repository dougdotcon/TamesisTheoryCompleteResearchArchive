#!/usr/bin/env python3
"""
Supplementary INDEPENDENT check of the Full Cycle-Count Decomposition
Theorem at K=4 (not just Proposicao S's marginal law of S): that,
given S, the (V_s)_{s in S} are mutually independent, each
V_s ~ Uniform{1,...,L_s}, using the SAME from-scratch position-level
construction as propS_position_model.py (predecessor-arc-including-
source convention, resolved there).

For a fixed (n,L) config, V_s (s in S) is computed directly as: the
count of cyclic points lying within source s's own arc (its L_s
predecessor points, s itself included) -- these arcs are disjoint by
construction, so this is an unambiguous, directly-readable quantity
from the realized cyclic-point set.
"""
from fractions import Fraction
from itertools import product
from adv_propS_position_model import build_pi, cyclic_points_of_f

def run(n, L, label):
    print(f"\n--- {label}: n={n}, L(pure-predecessor,excl. source)={L} ---")
    pi, arcs, O = build_pi(n, L)
    true_L = [Li + 1 for Li in L]  # includes source itself
    arc_plus_source = {s: set(arcs[s]) | {s} for s in [0, 1, 2, 3]}

    joint_counts = {}  # S (frozenset) -> {tuple(V_s for s in sorted(S)): count}
    S_counts = {}
    total = 0
    for U in product(range(n), repeat=4):
        f = list(pi)
        f[0], f[1], f[2], f[3] = U
        cyc = cyclic_points_of_f(f, n)
        S = frozenset(s for s in [0, 1, 2, 3] if s in cyc)
        Vs = {}
        for s in S:
            Vs[s] = len(arc_plus_source[s] & cyc)
        key = tuple(Vs[s] for s in sorted(S))
        joint_counts.setdefault(S, {}).setdefault(key, 0)
        joint_counts[S][key] += 1
        S_counts[S] = S_counts.get(S, 0) + 1
        total += 1

    all_ok = True
    for S, keydict in joint_counts.items():
        if not S:
            continue
        nS = S_counts[S]
        s_list = sorted(S)
        # expected: uniform product over {1,...,true_L[s]}
        expected_total_combos = 1
        for s in s_list:
            expected_total_combos *= true_L[s]
        expected_prob_each = Fraction(1, expected_total_combos)
        ok_this_S = True
        seen_combos = set()
        for key, cnt in keydict.items():
            seen_combos.add(key)
            emp = Fraction(cnt, nS)
            if emp != expected_prob_each:
                ok_this_S = False
        # also check every combo in {1,...,L_s}^|S| appears (uniform support, no gaps)
        import itertools as it
        full_support = set(it.product(*[range(1, true_L[s] + 1) for s in s_list]))
        support_ok = (seen_combos == full_support)
        ok_this_S = ok_this_S and support_ok
        all_ok = all_ok and ok_this_S
        tag = "OK" if ok_this_S else "MISMATCH"
        print(f"    S={sorted(S)}: |S| realizations={nS}, "
              f"expected uniform over {expected_total_combos} combos: {tag}")
    print(f"  Overall V_s|S independence+uniformity check: {'PASS' if all_ok else 'FAIL'}")
    return all_ok

if __name__ == "__main__":
    ok = True
    ok &= run(9, (1, 1, 0, 2), "mixed case with a zero-arc source")
    ok &= run(8, (0, 0, 0, 0), "all sources bare (max degeneracy)")
    ok &= run(10, (2, 1, 1, 1), "generic, O=1")
    print("\n" + "=" * 70)
    print("OVERALL Decomposition Theorem (V_s | S) check:",
          "ALL PASSED" if ok else "FAILURES FOUND")
    print("=" * 70)
