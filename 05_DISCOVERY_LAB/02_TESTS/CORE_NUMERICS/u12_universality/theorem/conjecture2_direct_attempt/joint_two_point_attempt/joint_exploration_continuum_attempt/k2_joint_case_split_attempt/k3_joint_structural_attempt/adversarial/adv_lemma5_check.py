"""
Independent, from-scratch re-derivation and verification of Lemma 5's
closed-form single-point and cross-arc formulas.

Method:
 (A) Symbolic (sympy) re-derivation via explicit case enumeration on the
     3-node cyclic-structure graph, done independently (own case analysis,
     not copied from ATTEMPT.md's proof sketch).
 (B) Cross-check against exact enumeration: for concrete small (n, L0,
     L1, L2), enumerate ALL n^3 choices of (U0,U1,U2) as concrete SLOT
     indices among the n abstract points (L0 slots for arc0 [1..L0],
     L1 for arc1, L2 for arc2, remainder outside), build the full
     position-level functional graph directly (same style as
     adv_lemma4_position_level.py, independently reconstructed here),
     determine cyclicity of every position by direct forward traversal,
     and average with exact Fraction arithmetic. Compare to Lemma 5's
     claimed closed forms AND to the sympy re-derivation.

No .py file from any front in the lineage was read.
"""
from fractions import Fraction
import itertools
import sympy as sp

# ---------- Part A: symbolic re-derivation ----------

n, L0, L1, L2, i, ip = sp.symbols('n L0 L1 L2 i ip', positive=True)

# Single-point formula for ARC(0), position i, independently re-derived
# by summing the 5 cyclic-structure cases that put 0 on a cycle:
#   home (0->0): i/n
#   2-cycle via 1 (0->1->0): (L1/n)*(i/n)
#   2-cycle via 2 (0->2->0): (L2/n)*(i/n)
#   3-cycle 0->1->2->0: (L1/n)*(L2/n)*(i/n)
#   3-cycle 0->2->1->0: (L2/n)*(L1/n)*(i/n)
P_single_derived = (i/n) + (L1/n)*(i/n) + (L2/n)*(i/n) + (L1/n)*(L2/n)*(i/n) + (L2/n)*(L1/n)*(i/n)
P_single_derived = sp.simplify(P_single_derived)
P_single_claimed = i*(2*L1*L2 + L1*n + L2*n + n**2) / n**3

diff_single = sp.simplify(P_single_derived - P_single_claimed)

# Cross-arc formula for ARC(0) pos i and ARC(1) pos i', independently
# re-derived by summing the 6 cyclic-structure cases that put BOTH 0 and 1
# on cycles (see derivation notes in REFEREE_REPORT.md):
#   (i)   0 fixed, 1 fixed (separate):                  (i/n)(i'/n)
#   (ii)  0 fixed, {1,2} 2-cycle:                        (i/n)(L2/n)(i'/n)
#   (iii) 1 fixed, {0,2} 2-cycle:                        (L2/n)(i/n)(i'/n)
#   (iv)  {0,1} 2-cycle:                                 (i/n)(i'/n)
#   (v)   3-cycle 0->1->2->0:                            (i'/n)(L2/n)(i/n)
#   (vi)  3-cycle 0->2->1->0:                             (L2/n)(i/n)(i'/n)
P_cross_derived = (
    (i/n)*(ip/n)
    + (i/n)*(L2/n)*(ip/n)
    + (L2/n)*(i/n)*(ip/n)
    + (i/n)*(ip/n)
    + (ip/n)*(L2/n)*(i/n)
    + (L2/n)*(i/n)*(ip/n)
)
P_cross_derived = sp.simplify(P_cross_derived)
P_cross_claimed = 2*i*ip*(2*L2 + n) / n**3
diff_cross = sp.simplify(P_cross_derived - P_cross_claimed)

print("=== Part A: symbolic re-derivation ===")
print("P_single derived :", P_single_derived)
print("P_single claimed :", sp.simplify(P_single_claimed))
print("difference (should be 0):", diff_single)
print()
print("P_cross derived  :", P_cross_derived)
print("P_cross claimed  :", sp.simplify(P_cross_claimed))
print("difference (should be 0):", diff_cross)
print()
ok_symbolic = (diff_single == 0) and (diff_cross == 0)
print(f"SYMBOLIC_REDERIVATION_MATCHES_CLAIM: {ok_symbolic}")
print()

# ---------- Part B: exact enumeration cross-check ----------

def build_slots(L0v, L1v, L2v, nv):
    """Returns list of n abstract "point ids": arc0 slots 1..L0, arc1
    slots 1..L1, arc2 slots 1..L2, then outside points."""
    points = []
    for s, Lv in ((0, L0v), (1, L1v), (2, L2v)):
        for pos in range(1, Lv + 1):
            points.append((s, pos))
    n_used = L0v + L1v + L2v
    assert n_used <= nv
    for k in range(nv - n_used):
        points.append(('OUT', k))
    assert len(points) == nv
    return points


def cyclic_status_for_config(L, nv, U):
    """U: dict s(0,1,2) -> concrete point (one of the point-id tuples).
    Returns dict (s,i)->bool cyclic for every arc-interior/tail position."""
    def f(node):
        if node[0] == 'OUT':
            return None  # outside points' own f-edge is irrelevant to arc cyclicity here
        s, pos = node
        if pos < L[s]:
            return (s, pos + 1)
        # tail: this IS source s itself; edge is the reroute U[s]
        return U[s]

    cyclic = {}
    for s in (0, 1, 2):
        for pos in range(1, L[s] + 1):
            node = (s, pos)
            cur = f(node)
            seen = {node}
            is_cyc = False
            steps = 0
            while cur is not None:
                if cur == node:
                    is_cyc = True
                    break
                if cur in seen:
                    is_cyc = False
                    break
                seen.add(cur)
                cur = f(cur)
                steps += 1
                if steps > 10000:
                    raise RuntimeError("non-termination")
            cyclic[node] = is_cyc
    return cyclic


def exact_probs(L0v, L1v, L2v, nv):
    """Exact Fraction probabilities, via full enumeration of all nv^3
    (U0,U1,U2) choices (each ranges over ALL nv abstract points)."""
    L = {0: L0v, 1: L1v, 2: L2v}
    points = build_slots(L0v, L1v, L2v, nv)
    total = nv ** 3

    # accumulate: for each interior position pair we care about, count
    single_counts = {s: [0] * (L[s] + 1) for s in (0, 1, 2)}  # index by pos
    cross_counts = {}  # (s,pos,s2,pos2) -> count, s != s2

    for U0, U1, U2 in itertools.product(points, repeat=3):
        U = {0: U0, 1: U1, 2: U2}
        cyc = cyclic_status_for_config(L, nv, U)
        for s in (0, 1, 2):
            for pos in range(1, L[s] + 1):
                if cyc[(s, pos)]:
                    single_counts[s][pos] += 1

    for U0, U1, U2 in itertools.product(points, repeat=3):
        pass  # (single pass reused below combined with cross to save time)

    return single_counts, total, L


def exact_single_and_cross(L0v, L1v, L2v, nv):
    L = {0: L0v, 1: L1v, 2: L2v}
    points = build_slots(L0v, L1v, L2v, nv)
    total = nv ** 3

    single_counts = {s: [0] * (L[s] + 1) for s in (0, 1, 2)}
    cross01_counts = {}  # (pos0,pos1) -> count of both cyclic

    for U0, U1, U2 in itertools.product(points, repeat=3):
        U = {0: U0, 1: U1, 2: U2}
        cyc = cyclic_status_for_config(L, nv, U)
        for s in (0, 1, 2):
            for pos in range(1, L[s] + 1):
                if cyc[(s, pos)]:
                    single_counts[s][pos] += 1
        for pos0 in range(1, L[0] + 1):
            if not cyc[(0, pos0)]:
                continue
            for pos1 in range(1, L[1] + 1):
                if cyc[(1, pos1)]:
                    cross01_counts[(pos0, pos1)] = cross01_counts.get((pos0, pos1), 0) + 1

    return single_counts, cross01_counts, total, L


def check_config(L0v, L1v, L2v, nv):
    single_counts, cross01_counts, total, L = exact_single_and_cross(L0v, L1v, L2v, nv)
    mismatches = []

    # check single-point formula for ARC(0)
    for pos in range(1, L[0] + 1):
        actual = Fraction(single_counts[0][pos], total)
        claimed = Fraction(pos * (2*L[1]*L[2] + L[1]*nv + L[2]*nv + nv**2), nv**3)
        if actual != claimed:
            mismatches.append(('single_arc0', pos, actual, claimed))

    # check single-point formula for ARC(1) too (symmetric role, L0<->irrelevant, uses "other two" = L0,L2)
    for pos in range(1, L[1] + 1):
        actual = Fraction(single_counts[1][pos], total)
        claimed = Fraction(pos * (2*L[0]*L[2] + L[0]*nv + L[2]*nv + nv**2), nv**3)
        if actual != claimed:
            mismatches.append(('single_arc1', pos, actual, claimed))

    # check cross-arc formula ARC(0),ARC(1), using L2 as the "third" arc
    for pos0 in range(1, L[0] + 1):
        for pos1 in range(1, L[1] + 1):
            actual = Fraction(cross01_counts.get((pos0, pos1), 0), total)
            claimed = Fraction(2 * pos0 * pos1 * (2*L[2] + nv), nv**3)
            if actual != claimed:
                mismatches.append(('cross01', pos0, pos1, actual, claimed))

    # check same-arc monotone-nesting claim (R3-analogue): for i<i' in arc0,
    # P(both cyclic) == P(pos i cyclic) (the nearer-to-tail one)
    for i1 in range(1, L[0] + 1):
        for i2 in range(i1 + 1, L[0] + 1):
            # both cyclic count: need direct count of (i1 cyclic AND i2 cyclic)
            pass  # computed separately below

    return mismatches, single_counts, cross01_counts, total, L


def check_same_arc_monotone(L0v, L1v, L2v, nv):
    L = {0: L0v, 1: L1v, 2: L2v}
    points = build_slots(L0v, L1v, L2v, nv)
    total = nv ** 3
    both_counts = {}
    single_counts0 = [0] * (L[0] + 1)
    for U0, U1, U2 in itertools.product(points, repeat=3):
        U = {0: U0, 1: U1, 2: U2}
        cyc = cyclic_status_for_config(L, nv, U)
        for pos in range(1, L[0] + 1):
            if cyc[(0, pos)]:
                single_counts0[pos] += 1
        for i1 in range(1, L[0] + 1):
            if not cyc[(0, i1)]:
                continue
            for i2 in range(i1 + 1, L[0] + 1):
                if cyc[(0, i2)]:
                    both_counts[(i1, i2)] = both_counts.get((i1, i2), 0) + 1

    mismatches = []
    for i1 in range(1, L[0] + 1):
        for i2 in range(i1 + 1, L[0] + 1):
            both = Fraction(both_counts.get((i1, i2), 0), total)
            marg = Fraction(single_counts0[i1], total)
            if both != marg:
                mismatches.append((i1, i2, both, marg))
    return mismatches


if __name__ == '__main__':
    configs = [
        (2, 2, 2, 9),
        (3, 2, 1, 10),
        (1, 1, 1, 6),
        (3, 3, 2, 11),
        (2, 3, 4, 12),
    ]
    total_mismatches = 0
    for (L0v, L1v, L2v, nv) in configs:
        print(f"--- config L=({L0v},{L1v},{L2v}), n={nv} ---")
        mism, single_counts, cross01_counts, total, L = check_config(L0v, L1v, L2v, nv)
        print(f"  total configs enumerated: {total}")
        print(f"  mismatches (single/cross vs Lemma5 formulas): {len(mism)}")
        for m in mism[:10]:
            print("   ", m)
        total_mismatches += len(mism)

        mono_mism = check_same_arc_monotone(L0v, L1v, L2v, nv)
        print(f"  same-arc monotone-nesting mismatches: {len(mono_mism)}")
        for m in mono_mism[:10]:
            print("   ", m)
        total_mismatches += len(mono_mism)

    print()
    print(f"LEMMA5_EXACT_CROSSCHECK_OK: {total_mismatches == 0}")
