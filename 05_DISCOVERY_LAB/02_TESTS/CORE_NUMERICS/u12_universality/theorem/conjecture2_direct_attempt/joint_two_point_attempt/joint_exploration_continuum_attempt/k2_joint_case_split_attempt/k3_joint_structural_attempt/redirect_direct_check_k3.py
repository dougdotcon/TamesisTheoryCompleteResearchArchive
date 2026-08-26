"""
redirect_direct_check_k3.py

Independent internal cross-check of redirect_core_k3.py's "64 destination
bucket" reduction, WITHOUT using that reduction: builds the reduced-model
sample space directly at the level of concrete integer positions (not
buckets), i.e. literally enumerates all n^3 (U0,U1,U2) SLOT choices (each of
n slots labeled: ('arc', s, k) for k=1..L[s], or ('out', j) for
j=1..O), constructs the resulting functional graph on those n abstract
slots by hand (arc-interior succession is deterministic; a slot at the tail
of arc s, i.e. ('arc',s,L[s]), succeeds to wherever U_s landed; outside
slots have no further edges tracked here since outside points are
automatically cyclic by construction and never need chasing further for
THIS purpose -- see note below), and directly determines cyclicity of two
query positions by iterating this graph.

This is independent of redirect_core_k3.py's own "which source is the
returning predecessor" combinatorial shortcut -- it re-derives the same
quantity by brute position-level simulation over the *reduced* sample
space, so agreement between the two is a genuine, non-circular check of the
predecessor/64-case reduction's correctness (it does NOT depend on
redirect_core_k3.py's code in any way -- built fully independently, from
the same Definition-4 mechanics).

Note on "outside": an outside slot's own forward edge, within the reduced
arc model, is irrelevant to determining whether ARC positions are cyclic
(an arc chain that reaches 'outside' is dead, full stop, regardless of what
outside points do among themselves -- this is inherited directly from
Definition 4's own combinatorics: the outside points form a closed
permutation of themselves, disjoint from all arcs, so nothing that enters
it ever returns to an arc position). So this script models a landing in
'out' as an absorbing DEAD state, exactly matching redirect_core_k3.py's
own treatment -- but it is DERIVED here again independently, by explicit
graph simulation rather than the case-table shortcut, as the point of the
cross-check.
"""

from fractions import Fraction
from itertools import product


def build_slots(L, O):
    """Return list of all n slots in a fixed order, and a lookup dict
    slot -> index."""
    slots = []
    for s in range(3):
        for k in range(1, L[s] + 1):
            slots.append(('arc', s, k))
    for j in range(1, O + 1):
        slots.append(('out', j))
    return slots


def is_slot_cyclic(pos, succ, n_hops_cap):
    """pos: starting slot. succ: dict slot -> next slot or None (DEAD).
    Returns True iff iterating succ from pos returns to pos before DEAD,
    within n_hops_cap steps."""
    x = succ.get(pos)
    steps = 0
    while x is not None and steps < n_hops_cap:
        if x == pos:
            return True
        x = succ.get(x)
        steps += 1
    return False


def p_joint_cyclic_direct(n, L, query1, query2):
    """query1, query2: each either None ('outside', trivially cyclic) or
    (s, k) an interior position (1 <= k <= L[s]-1). Direct enumeration over
    all n^3 (U0,U1,U2) slot choices."""
    O = n - sum(L)
    slots = build_slots(L, O)
    assert len(slots) == n, (len(slots), n)

    if query1 is None and query2 is None:
        return Fraction(1)

    both_count = 0
    total = 0
    for U0, U1, U2 in product(slots, repeat=3):
        # Build succ: deterministic arc-interior edges, plus the 3 sources'
        # chosen edges. Tail of arc s is slot ('arc',s,L[s]); its own
        # successor is U_s (the s-th source's reroute target).
        succ = {}
        for s in range(3):
            for k in range(1, L[s]):
                succ[('arc', s, k)] = ('arc', s, k + 1)
        Us = [U0, U1, U2]
        for s in range(3):
            tail = ('arc', s, L[s])
            target = Us[s]
            succ[tail] = None if target[0] == 'out' else target
        # outside slots: no outgoing edge tracked (irrelevant, see docstring)

        ok = True
        for q in (query1, query2):
            if q is None:
                continue
            s, k = q
            pos = ('arc', s, k)
            if not is_slot_cyclic(pos, succ, n):
                ok = False
                break
        if ok:
            both_count += 1
        total += 1
    return Fraction(both_count, total)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from redirect_core_k3 import p_joint_cyclic as p_joint_cyclic_reduced

    n = 10
    L = (3, 2, 2)
    cases = [
        (None, None),
        (None, (0, 1)),
        ((0, 1), (0, 2)),
        ((0, 1), (1, 1)),
        ((1, 1), (2, 1)),
        ((0, 2), (2, 1)),
    ]
    print(f"n={n}, L={L}, O={n - sum(L)}")
    all_ok = True
    for q1, q2 in cases:
        direct = p_joint_cyclic_direct(n, L, q1, q2)
        reduced = p_joint_cyclic_reduced(n, L, q1, q2)
        match = (direct == reduced)
        all_ok &= match
        print(f"  query=({q1},{q2}): direct={direct}  reduced={reduced}  match={match}")
    print("ALL MATCH" if all_ok else "MISMATCH FOUND")
