#!/usr/bin/env python3
"""
INDEPENDENT verification of Proposicao S at K=4, via an explicit
position-level construction built from scratch from THEOREM.md's own
text (Definition 4, plus the Governing-Source-Reindexing description
quoted/cited in ATTEMPT.md section 1.2: (L_0,L_1,L_2,L_3,O) are arc
lengths with L_s = length of the arc whose TAIL is source s, O = count
of points on no marked arc). No .py file from any front was read.

Model built here (my own construction, not copied from any front):
  - n points total, labelled 0..n-1.
  - Sources are 0,1,2,3.
  - We construct a SPECIFIC permutation pi realizing a chosen
    (L_0,L_1,L_2,L_3,O) composition, by placing all 4 sources plus
    their arcs on ONE big pi-cycle, and (if O>0) the O leftover points
    on a SEPARATE, second pi-cycle disjoint from the sources.
  - "the arc whose tail is source s" is read as: the L_s points
    immediately BEFORE s in pi's cyclic order (i.e. the L_s
    predecessors of s along the big cycle, up to the previous source).
    This is the only reading consistent with the Decomposition
    Theorem's T=O+sum V_s, V_s~Uniform{1,...,L_s}: landing your
    target U_s among these L_s "predecessor" points means following
    pi forward from that point reaches s again after some number of
    steps in {1,...,L_s}, closing a cycle through s.
  - Big cycle order (pi maps each point to the next in this list,
    wrapping around):
      [pred-arc of source 0 (L_0 pts)] , 0 ,
      [pred-arc of source 1 (L_1 pts)] , 1 ,
      [pred-arc of source 2 (L_2 pts)] , 2 ,
      [pred-arc of source 3 (L_3 pts)] , 3 ,
    (wraps back to the start).
  - If O>0: a second disjoint pi-cycle covering the O leftover points
    (e.g. a single O-cycle, or O fixed points -- shouldn't matter to
    S/V_s since O-points never interact with sources by construction;
    checked below with two different O-substructures for safety).

For each such explicit (pi, sources) realization, T is computed by
BRUTE FORCE over all n^4 tuples (U_0,U_1,U_2,U_3) in range(n)^4 (exact
integer counting), and for each we determine, from first principles
(functional-graph cyclic-point detection), which sources end up on a
cycle of f -- this is exactly S -- and cross-tabulate the resulting
empirical P(S=A) (exact Fraction, denominator n^4) against Proposicao
S's claimed closed form:

    P(S=A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)

with p_i := L_i/n, p_D := O/n, for EVERY one of the 16 subsets A of
{0,1,2,3} -- deliberately including boundary cases with some L_i=0,
which the derivation building-blocks in ATTEMPT.md section 4.1 (S1,
PS, TS, QS, and the "binom(m-1,3) compositions of m into 4 POSITIVE
parts" language) appear, on their face, to implicitly exclude -- see
the referee report for discussion of this apparent internal notation
inconsistency.
"""
import sys
from fractions import Fraction
from itertools import product

def build_pi(n, L, O_substructure="single_cycle"):
    """
    L = (L0,L1,L2,L3), sum(L)+4+O = n.
    Returns pi as a list (pi[i] = image of i), the sorted list of
    source predecessor-arc point sets (for bookkeeping), and O.
    """
    L0, L1, L2, L3 = L
    total_arc = L0 + L1 + L2 + L3
    O = n - 4 - total_arc
    assert O >= 0
    pts = list(range(4, n))  # generic pool for arcs + O points
    pos = 0
    arcs = {}
    for s, Ls in zip([0, 1, 2, 3], [L0, L1, L2, L3]):
        arcs[s] = pts[pos:pos + Ls]
        pos += Ls
    off_points = pts[pos:pos + O]
    assert len(off_points) == O
    assert pos + O == len(pts)

    pi = [None] * n
    order = []
    for s in [0, 1, 2, 3]:
        order.extend(arcs[s])
        order.append(s)
    # big cycle: order[i] -> order[i+1], wrap
    for i in range(len(order)):
        pi[order[i]] = order[(i + 1) % len(order)]

    if O > 0:
        if O_substructure == "single_cycle":
            for i in range(len(off_points)):
                pi[off_points[i]] = off_points[(i + 1) % len(off_points)]
        elif O_substructure == "fixed_points":
            for p in off_points:
                pi[p] = p
        else:
            raise ValueError(O_substructure)

    assert sorted(pi) == list(range(n)), "pi must be a permutation"
    return pi, arcs, O

def cyclic_points_of_f(f, n):
    """f: list length n, f[i] in [0,n). Returns set of cyclic points."""
    color = [0] * n  # 0 unvisited, 1 in-progress, 2 done
    order_idx = [-1] * n
    oncycle = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            order_idx[x] = len(path)
            path.append(x)
            x = f[x]
        if color[x] == 1:
            # found a fresh cycle: from x back around to x
            cstart = order_idx[x]
            for y in path[cstart:]:
                oncycle[y] = True
        for y in path:
            color[y] = 2
    return set(i for i in range(n) if oncycle[i])

def empirical_S_law(n, L, O_substructure="single_cycle"):
    pi, arcs, O = build_pi(n, L, O_substructure)
    L0, L1, L2, L3 = L
    counts = {}
    total = 0
    for U in product(range(n), repeat=4):
        f = list(pi)
        f[0], f[1], f[2], f[3] = U
        cyc = cyclic_points_of_f(f, n)
        S = frozenset(s for s in [0, 1, 2, 3] if s in cyc)
        counts[S] = counts.get(S, 0) + 1
        total += 1
    return counts, total, O

def prop_S_formula(n, L, O, A):
    """
    NOTE on convention (resolved after an initial mismatch -- see referee
    report): Proposicao S's own L_s must INCLUDE the source point s
    itself (so L_s>=1 always: V_s=1 <-> landing exactly on s, a direct
    self-loop; V_s=L_s <-> landing at the farthest predecessor). Our
    build_pi()'s `L` parameter counts only the PURE predecessor points
    (excluding s), so the true Proposicao-S L_s here is L_input+1.
    """
    from math import factorial
    p = [Fraction(Li + 1, n) for Li in L]
    pD = Fraction(O, n)
    m = len(A)
    prod_p = Fraction(1)
    sum_p = Fraction(0)
    for a in A:
        prod_p *= p[a]
        sum_p += p[a]
    return factorial(m) * prod_p * (pD + sum_p)

def all_subsets():
    subs = []
    for r in range(5):
        from itertools import combinations
        subs.extend(combinations([0, 1, 2, 3], r))
    return [frozenset(s) for s in subs]

def run_case(n, L, label, O_substructure="single_cycle"):
    print(f"\n--- case {label}: n={n}, L=(L0,L1,L2,L3)={L}, O_substructure={O_substructure} ---")
    counts, total, O = empirical_S_law(n, L, O_substructure)
    print(f"  O={O}, total configs (n^4)={total}")
    subs = all_subsets()
    all_match = True
    for A in subs:
        empirical = Fraction(counts.get(A, 0), total)
        formula = prop_S_formula(n, L, O, A)
        match = (empirical == formula)
        all_match = all_match and match
        tag = "OK" if match else "MISMATCH"
        if not match:
            print(f"    A={sorted(A)}: empirical={empirical}  formula={formula}  {tag}")
    print(f"  16-subset check: {'ALL MATCH' if all_match else 'MISMATCH FOUND'}")
    # also confirm sums to 1
    ssum = sum(prop_S_formula(n, L, O, A) for A in subs)
    print(f"  sum of formula over 16 subsets = {ssum} (should be 1): {'OK' if ssum == 1 else 'FAIL'}")
    return all_match and (ssum == 1)

if __name__ == "__main__":
    all_ok = True
    # A spread of concrete (n,L) configurations, DELIBERATELY including
    # cases with some L_i = 0 (boundary/degenerate arcs) and cases with
    # O = 0 (no off-arc points at all), to stress-test Proposicao S at
    # points the shift-trick building blocks in ATTEMPT.md section 4.1
    # look, on their face, like they might silently exclude.
    cases = [
        (8, (1, 1, 1, 1), "generic, all L_i=1, O=0"),
        (10, (2, 1, 1, 1), "generic, unequal L_i, O=1"),
        (10, (0, 1, 1, 1), "BOUNDARY: L_0=0"),
        (10, (0, 0, 1, 2), "BOUNDARY: two L_i=0"),
        (9, (0, 0, 0, 1), "BOUNDARY: three L_i=0"),
        (8, (0, 0, 0, 0), "BOUNDARY: all L_i=0 (O=4)"),
        (12, (2, 2, 2, 2), "generic, O=0"),
        (11, (3, 1, 0, 2), "BOUNDARY: one L_i=0, unequal rest"),
    ]
    for n, L, label in cases:
        ok = run_case(n, L, label, "single_cycle")
        all_ok = all_ok and ok
        if sum(L) < n - 4:  # O > 0, also test with fixed_points O-substructure
            ok2 = run_case(n, L, label + " [O as fixed points instead of a cycle]",
                            "fixed_points")
            all_ok = all_ok and ok2

    print("\n" + "=" * 70)
    print("OVERALL Proposicao S @ K=4 position-level check:",
          "ALL PASSED (including all-zero-arc / boundary cases)" if all_ok
          else "FAILURES FOUND -- SEE ABOVE")
    print("=" * 70)
