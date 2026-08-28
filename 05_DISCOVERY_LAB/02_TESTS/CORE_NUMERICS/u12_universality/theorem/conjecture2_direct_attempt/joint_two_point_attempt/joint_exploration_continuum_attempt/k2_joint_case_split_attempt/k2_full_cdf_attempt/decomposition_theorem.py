"""
The K=2 Full Cycle-Count Decomposition Theorem: derivation and
independent verification, entirely from scratch (no .py file from any
other front read or imported).

Setup (THEOREM.md Definition 4, K=2; notation matches
k2_joint_case_split_attempt/ATTEMPT.md's prose, re-derived not copied):
  - pi uniform random permutation of [n], sources fixed WLOG at {0,1}.
  - U_0, U_1 i.i.d. Uniform([n]).
  - f(i) := U_i for i in {0,1}, f(i) := pi(i) otherwise.
  - By the Marked-Point Gap Structure fact (m=2 case, re-derived below
    only as a citation of its conclusion, not re-proved -- it is a
    general-m combinatorial fact about uniform permutations, independent
    of anything K=2-specific), the two "arcs" ARC(0) (points ending at
    source 0, forward along pi) and ARC(1) (points ending at source 1)
    have lengths (L_0, L_1) uniform over all pairs with L_0,L_1>=1,
    L_0+L_1<=n (n-choose-2 such pairs, each w.p. 1/C(n,2)), and O :=
    n-L_0-L_1 points lie entirely outside both arcs (in pi-cycles
    touching neither source) and are AUTOMATICALLY cyclic under f.

This script:
  (1) States and verifies Proposition S (law of S, the set of cyclic
      sources) by exact 9-case enumeration over destinations.
  (2) States and verifies the Full Decomposition Theorem
      T = O + sum_{s in S} V_s (V_s indep unif given S) against a
      from-scratch "position-level reduced model" (arcs as explicit
      small graphs, U_0/U_1 landing uniformly among n slots).
  (3) Cross-checks the reduced model's *unconditional* (in L) T-law
      against the true brute-force ground truth already computed in
      true_bruteforce_full_cdf_k2.py's logs, for several n.
"""
import sys
from fractions import Fraction
from itertools import product
from collections import Counter

import sympy as sp


# ---------------------------------------------------------------------
# Part 1: Proposition S -- symbolic 9-case verification
# ---------------------------------------------------------------------

def prop_S_symbolic():
    p0, p1, pD = sp.symbols('p0 p1 pD', positive=True)
    # 9 destination combos: dest(0), dest(1) each in {0,1,'D'}
    # weight of combo = p_{dest(0)} * p_{dest(1)}
    weight = {0: p0, 1: p1, 'D': pD}

    def cyclic_set(dest):
        # dest: dict {0: d0, 1: d1}, d in {0,1,'D'}
        S = set()
        for s in (0, 1):
            x = s
            seen = set()
            cyclic = False
            for _ in range(3):  # at most 2 sources, +1 safety
                if x == 'D':
                    break
                if x in seen:
                    if x == s:
                        cyclic = True
                    break
                seen.add(x)
                x = dest[x]
            if x == s and x != 'D':
                cyclic = True
            if cyclic:
                S.add(s)
        return frozenset(S)

    totals = {frozenset(): 0, frozenset({0}): 0, frozenset({1}): 0,
              frozenset({0, 1}): 0}
    for d0, d1 in product((0, 1, 'D'), repeat=2):
        dest = {0: d0, 1: d1}
        S = cyclic_set(dest)
        totals[S] += weight[d0] * weight[d1]

    totals = {k: sp.expand(v) for k, v in totals.items()}

    claimed = {
        frozenset(): pD,
        frozenset({0}): sp.expand(p0 * (p0 + pD)),
        frozenset({1}): sp.expand(p1 * (p1 + pD)),
        frozenset({0, 1}): sp.expand(2 * p0 * p1),
    }

    print("Proposition S: 9-case symbolic derivation vs claimed formulas")
    ok = True
    for key in totals:
        # substitute pD = 1 - p0 - p1 to compare under the constraint
        diff = sp.simplify(
            (totals[key] - claimed[key]).subs(pD, 1 - p0 - p1)
        )
        status = "OK" if diff == 0 else f"MISMATCH (diff={diff})"
        if diff != 0:
            ok = False
        print(f"  S={sorted(key) if key else '{}'}: derived={totals[key]}  "
              f"claimed={claimed[key]}  diff(after pD=1-p0-p1)={diff}  {status}")

    total_sum = sp.simplify(sum(totals.values()).subs(pD, 1 - p0 - p1))
    print(f"  sum of all P(S=.) (after pD=1-p0-p1) = {total_sum} "
          f"({'OK, =1' if total_sum == 1 else 'MISMATCH'})")
    ok = ok and (total_sum == 1)
    return ok


# ---------------------------------------------------------------------
# Part 2: position-level reduced model (arcs as explicit small graphs)
# ---------------------------------------------------------------------

def reduced_model_T_distribution(n, L0, L1):
    """Exact distribution of T given (n, L0, L1), by enumerating all n^2
    landing slots of (U_0, U_1) explicitly against the two-arc graph
    structure. O = n - L0 - L1 automatically-cyclic points are added at
    the end. Returns Counter of T -> count (out of n^2)."""
    assert L0 >= 1 and L1 >= 1 and L0 + L1 <= n
    O = n - L0 - L1

    def slot_to_node(slot):
        # slot: 0..n-1 (0-indexed uniform landing position)
        if slot < L0:
            return ('a0', slot + 1)  # position 1..L0 in arc0
        elif slot < L0 + L1:
            return ('a1', slot - L0 + 1)  # position 1..L1 in arc1
        else:
            return 'OUT'

    counts = Counter()
    for u0 in range(n):
        for u1 in range(n):
            dest0 = slot_to_node(u0)
            dest1 = slot_to_node(u1)

            def f(node):
                kind, i = node
                if kind == 'a0':
                    if i < L0:
                        return ('a0', i + 1)
                    else:
                        return dest0
                else:
                    if i < L1:
                        return ('a1', i + 1)
                    else:
                        return dest1

            nodes = [('a0', i) for i in range(1, L0 + 1)] + \
                    [('a1', i) for i in range(1, L1 + 1)]
            cyclic = set()
            color = {}
            for start in nodes:
                if start in color:
                    continue
                path = []
                x = start
                while x != 'OUT' and x not in color:
                    color[x] = 1
                    path.append(x)
                    x = f(x)
                if x != 'OUT' and color.get(x) == 1:
                    idx = path.index(x)
                    for y in path[idx:]:
                        cyclic.add(y)
                for y in path:
                    color[y] = 2
            T = O + len(cyclic)
            counts[T] += 1
    return counts, n * n


def decomposition_formula_T_distribution(n, L0, L1):
    """Predicted distribution of T via the Decomposition Theorem +
    Proposition S, given (n, L0, L1): T = O + sum_{s in S} V_s, V_s
    uniform on {1,...,L_s} given S, independent given S."""
    O = n - L0 - L1
    p0, p1 = Fraction(L0, n), Fraction(L1, n)
    pD = Fraction(O, n)
    PS = {
        frozenset(): pD,
        frozenset({0}): p0 * (p0 + pD),
        frozenset({1}): p1 * (p1 + pD),
        frozenset({0, 1}): 2 * p0 * p1,
    }
    counts = Counter()  # T -> probability (Fraction), scaled later
    # empty
    counts[O] += PS[frozenset()]
    # {0}
    for v in range(1, L0 + 1):
        counts[O + v] += PS[frozenset({0})] * Fraction(1, L0)
    # {1}
    for v in range(1, L1 + 1):
        counts[O + v] += PS[frozenset({1})] * Fraction(1, L1)
    # {0,1}
    for v0 in range(1, L0 + 1):
        for v1 in range(1, L1 + 1):
            counts[O + v0 + v1] += PS[frozenset({0, 1})] * \
                Fraction(1, L0 * L1)
    return counts


def verify_reduced_vs_formula():
    print("\nDecomposition Theorem given (n,L0,L1): reduced model vs formula")
    cases = [
        (5, 1, 1), (5, 2, 1), (5, 1, 3), (5, 2, 2),
        (7, 3, 2), (7, 1, 1), (7, 4, 1), (7, 2, 4),
        (8, 3, 3), (9, 5, 2),
    ]
    all_ok = True
    for (n, L0, L1) in cases:
        counts, denom = reduced_model_T_distribution(n, L0, L1)
        reduced = {k: Fraction(v, denom) for k, v in counts.items()}
        formula = decomposition_formula_T_distribution(n, L0, L1)
        keys = set(reduced) | set(formula)
        ok = True
        for k in keys:
            a = reduced.get(k, Fraction(0))
            b = formula.get(k, Fraction(0))
            if a != b:
                ok = False
        all_ok = all_ok and ok
        print(f"  n={n} L0={L0} L1={L1}: {'OK' if ok else 'MISMATCH'}")
        if not ok:
            print(f"    reduced={reduced}")
            print(f"    formula={formula}")
    return all_ok


# ---------------------------------------------------------------------
# Part 3: unconditional (averaged over the composition simplex) check
#         against fresh brute force of the FULL Definition-4 model
# ---------------------------------------------------------------------

def unconditional_T_distribution_via_decomposition(n):
    """Average decomposition_formula_T_distribution over all C(n,2)
    (L0,L1) pairs, each equally likely -- this uses ONLY the claimed
    Marked-Point Gap fact (L0,L1 uniform on the simplex) + Proposition S
    + the Decomposition Theorem; it does NOT touch pi or U_0,U_1 directly."""
    from math import comb
    total_pairs = comb(n, 2)
    agg = Counter()
    for L0 in range(1, n):
        for L1 in range(1, n - L0 + 1):
            dist = decomposition_formula_T_distribution(n, L0, L1)
            for k, p in dist.items():
                agg[k] += p
    agg = {k: v / total_pairs for k, v in agg.items()}
    return agg


def verify_against_true_bruteforce(ns):
    """Compare unconditional_T_distribution_via_decomposition(n) (built
    purely from the claimed Decomposition Theorem + Proposition S) to a
    FRESH true brute force of Definition 4 itself (own permutations+U's
    enumeration, imported from true_bruteforce_full_cdf_k2.py -- the
    same fresh, from-scratch script already used for ground truth)."""
    from true_bruteforce_full_cdf_k2 import brute_force_T_distribution
    print("\nUnconditional (whole Definition-4 model) check: "
          "Decomposition Theorem vs fresh true brute force")
    all_ok = True
    for n in ns:
        counts, total = brute_force_T_distribution(n)
        bf = {k: Fraction(v, total) for k, v in counts.items()}
        pred = unconditional_T_distribution_via_decomposition(n)
        keys = set(bf) | set(pred)
        ok = True
        for k in keys:
            a = bf.get(k, Fraction(0))
            b = pred.get(k, Fraction(0))
            if a != b:
                ok = False
        all_ok = all_ok and ok
        print(f"  n={n}: {'OK -- exact match on every k' if ok else 'MISMATCH'}")
        if not ok:
            for k in sorted(keys):
                a = bf.get(k, Fraction(0))
                b = pred.get(k, Fraction(0))
                if a != b:
                    print(f"    k={k}: bf={a} pred={b}")
    return all_ok


if __name__ == "__main__":
    ok1 = prop_S_symbolic()
    ok2 = verify_reduced_vs_formula()
    ok3 = verify_against_true_bruteforce([3, 4, 5, 6, 7])
    print("\n" + "=" * 70)
    if ok1 and ok2 and ok3:
        print("ALL CHECKS PASSED: Proposition S and the K=2 Full "
              "Cycle-Count Decomposition Theorem hold.")
    else:
        print("SOME CHECKS FAILED -- see above.")
        sys.exit(1)
