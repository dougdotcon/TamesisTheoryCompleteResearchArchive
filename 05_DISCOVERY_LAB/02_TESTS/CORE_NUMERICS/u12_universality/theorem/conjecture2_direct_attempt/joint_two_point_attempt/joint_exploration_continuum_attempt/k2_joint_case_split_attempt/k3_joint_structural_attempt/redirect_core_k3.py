"""
redirect_core_k3.py

The Three-Source Redirect-Structure computation: the K=3 generalization of
the predecessor's Lemma 2 (Two-Source Redirect Structure).

Built entirely from scratch from the mechanics of Definition 4 (THEOREM.md
Sec 7.2) and the K=2 Lemma 1 / Lemma 2 pattern described in the predecessor
ATTEMPT.md's prose (NOT from reading any of its code).

--- Setup (derived fresh in this front's own ATTEMPT.md, Sec 2) ---

Apply the Marked-Point Gap Structure Lemma (Lemma 1 of the predecessor,
cited by name and statement only -- general m, already PROVED there and
re-confirmed independently by this front, see gap_lemma_m3_unittest.py) with
m=3 marks {0,1,2}. This gives: a topology sigma (uniform on S_3, the
"contracted permutation" on the marks) and, independently, arc lengths
(a_0,a_1,a_2,O) [MARK-indexed: a_m = g(m)+1 is the length -- INCLUDING the
tail, which is the next mark sigma(m) -- of the arc starting right after
mark m] uniform over compositions of n-3 into 4 nonnegative parts.

This front's own new reduction (ATTEMPT.md Sec 2.2, PROVED, elementary):
by exchangeability of (a_0,a_1,a_2) [a direct consequence of Lemma 1's own
proof: the uniform-over-compositions law is invariant under permuting the
role labels 0,1,2] and independence of sigma, the GOVERNING-SOURCE-indexed
arc lengths L_s := a_{sigma^{-1}(s)} (the arc whose TAIL is mark s, i.e.
whose continuation is governed by U_s) satisfy: (L_0,L_1,L_2,O) is uniform
over the SAME compositions of n-3 into 4 nonnegative parts, and INDEPENDENT
of sigma. Hence topology sigma can be marginalized out entirely -- it plays
no further role in computing P_nn(n,3).

Each L_s (s=0,1,2) counts ARC(s)'s total length: L_s - 1 interior
(non-source) positions, then position L_s = mark s itself (the tail). Query
points, disjoint from the 3 sources by construction, can only occupy
interior positions 1..L_s-1 of some arc, or be among the O "outside" points
(automatically cyclic, exactly as in the K=1/K=2 case: their forward
f-orbit never meets a reroute source).

--- The redirect structure itself ---

Each source t in {0,1,2} independently sends its target U_t to one of n
equally likely slots, categorized as: HOME (lands within ARC(t) itself, its
own governed arc, L_t slots), OTHER-s for s != t (lands within ARC(s), L_s
slots), or DEAD (lands outside all arcs, O slots). Write dest(t) for this
choice, valued in {0,1,2,'D'} (dest(t)=t means home).

Given a full destination assignment dest: {0,1,2} -> {0,1,2,'D'} (64 raw
combinations, matching THEOREM.md Estagio 31's own "4x4x4=64-cell" naming
of this exact obstruction), a source s (0,1,2) is CYCLIC (meaning: the arc
ARC(s) contributes a nonempty cyclic tail-segment) iff iterating dest from s
returns to s before hitting 'D' -- i.e. s lies on a cycle (fixed point,
2-cycle, or 3-cycle) of the functional graph dest restricted to {0,1,2}.//
If s is cyclic, it has a UNIQUE predecessor pred(s) in that cycle (the
unique t with dest(t)=s AND t itself cyclic -- possibly t=s, the "home"
case); this is a genuinely new fact this front establishes and verifies
(Lemma 4 below), generalizing the K=2 fact that an arc's own eventual
cycle doesn't depend on where OTHER, non-cycle-forming incoming chains
entered it -- multiple sources can target the same arc, but only the one
that is itself part of the returning cycle determines that arc's cyclic
set.

Then: an interior position i in ARC(s) is CYCLIC iff s is cyclic AND the
actual landing position of U_{pred(s)} within ARC(s) is <= i. (For s=t=
pred(s), i.e. home, this is "the actual landing position of U_s within its
own arc is <= i" -- exactly the K=1/K=2 "home" rule.)

This module implements this reduced model exactly (fractions.Fraction
throughout), and separately verifies it against literal enumeration over
concrete integer positions (not just destination buckets) for small
(L0,L1,L2,n) -- an internal cross-check of the "i/n substitution" algebra
used for speed -- before it is used, in redirect_verify_k3.py, against
TRUE brute force over full permutations (brute_force_k3.py) as final ground
truth.
"""

from fractions import Fraction
from itertools import product


def analyze_dest(dest):
    """dest: tuple (dest[0],dest[1],dest[2]) each in {0,1,2,'D'}.
    Returns (cyclic: dict s->bool, pred: dict s->predecessor or None)."""
    cyclic = {}
    for s in range(3):
        seen = {s}
        x = dest[s]
        steps = 0
        result = False
        while steps < 4:
            if x == 'D':
                result = False
                break
            if x == s:
                result = True
                break
            if x in seen:
                # cycles among OTHER nodes, s is a transient tail -> not cyclic
                result = False
                break
            seen.add(x)
            x = dest[x]
            steps += 1
        cyclic[s] = result
    pred = {}
    for s in range(3):
        if not cyclic[s]:
            pred[s] = None
            continue
        candidates = [t for t in range(3) if dest[t] == s and cyclic[t]]
        assert len(candidates) == 1, (dest, s, candidates)
        pred[s] = candidates[0]
    return cyclic, pred


def all_dest_combos():
    return list(product([0, 1, 2, 'D'], repeat=3))


def p_single_cyclic(n, L, s, i):
    """Exact P(position i in ARC(s) is cyclic), reduced model.
    L = (L0,L1,L2) tuple of ints. i in 1..L[s]-1."""
    total = Fraction(0)
    for dest in all_dest_combos():
        dest_map = {0: dest[0], 1: dest[1], 2: dest[2]}
        cyclic, pred = analyze_dest(dest_map)
        if not cyclic[s]:
            continue
        p = pred[s]
        w = Fraction(1)
        for t in range(3):
            if t == p:
                w *= Fraction(i, n)
            else:
                target = dest_map[t]
                if target == 'D':
                    O = n - sum(L)
                    w *= Fraction(O, n)
                else:
                    w *= Fraction(L[target], n)
        total += w
    return total


def p_joint_cyclic(n, L, query1, query2):
    """Exact P(query1 cyclic AND query2 cyclic), reduced model.
    query1, query2: each either None (meaning 'outside', automatically
    cyclic) or (s, i) meaning interior position i of ARC(s)."""
    O = n - sum(L)
    if query1 is None and query2 is None:
        return Fraction(1)
    if query1 is None:
        s2, i2 = query2
        return p_single_cyclic(n, L, s2, i2)
    if query2 is None:
        s1, i1 = query1
        return p_single_cyclic(n, L, s1, i1)

    s1, i1 = query1
    s2, i2 = query2
    total = Fraction(0)
    for dest in all_dest_combos():
        dest_map = {0: dest[0], 1: dest[1], 2: dest[2]}
        cyclic, pred = analyze_dest(dest_map)
        if not cyclic[s1] or not cyclic[s2]:
            continue
        p1 = pred[s1]
        p2 = pred[s2]
        # Build the set of "constrained" sources -> the bound to use.
        constraint = {}
        if s1 == s2:
            # same arc: single predecessor (p1==p2 necessarily, since the
            # cyclic set of a single arc has one well-defined predecessor)
            assert p1 == p2
            bound = min(i1, i2)
            constraint[p1] = bound
        else:
            # different arcs -- p1, p2 might coincide (e.g. a single source
            # is predecessor of both only if that source's dest equals both
            # s1 and s2 simultaneously, impossible since dest is single
            # valued and s1!=s2) so p1 != p2 always here; two independent
            # constraints.
            assert p1 != p2
            constraint[p1] = i1
            constraint[p2] = i2
        w = Fraction(1)
        for t in range(3):
            if t in constraint:
                w *= Fraction(constraint[t], n)
            else:
                target = dest_map[t]
                if target == 'D':
                    w *= Fraction(O, n)
                else:
                    w *= Fraction(L[target], n)
        total += w
    return total


if __name__ == "__main__":
    # quick smoke test
    n = 10
    L = (3, 2, 2)
    print("O =", n - sum(L))
    print("P(pos1 in arc0 cyclic) =", p_single_cyclic(n, L, 0, 1))
    print("P(pos2 in arc0 cyclic) =", p_single_cyclic(n, L, 0, 2))
    print("P(both pos1,pos2 arc0 cyclic) =",
          p_joint_cyclic(n, L, (0, 1), (0, 2)))
    print("P(pos1 arc0, pos1 arc1 both cyclic) =",
          p_joint_cyclic(n, L, (0, 1), (1, 1)))
