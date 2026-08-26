#!/usr/bin/env python3
"""
REFEREE, FRESH FROM SCRATCH (no script from the front's directory was read
or reused). Independently re-verifies the classical fact cited in
ATTEMPT.md Section 3:

    For a uniform random permutation of m >= 2 labeled elements, and any
    two fixed distinct elements i,j: P(i,j same cycle) = 1/2 exactly,
    for EVERY m (not just asymptotically).

Method: exhaustive enumeration of all m! permutations of range(m) via
itertools.permutations, exact cycle decomposition via a from-scratch
"visiting/done" marking algorithm (NOT copied from anywhere), exact
integer counting, Fraction for the final ratio. Deterministic -- no
randomness, no seed needed.

Extends the front's own re-derivation range (m=2..7) to m=2..9.
"""
import itertools
from fractions import Fraction


def cycle_id_of_permutation(p):
    """p: tuple representing a permutation of range(len(p)), p[i] = image of i.
    Returns a list `cid` with cid[i] = an integer label identifying the
    cycle containing i (same label iff same cycle). Fresh, elementary
    algorithm: follow orbits, label as we go.
    """
    m = len(p)
    cid = [-1] * m
    label = 0
    for start in range(m):
        if cid[start] != -1:
            continue
        v = start
        while cid[v] == -1:
            cid[v] = label
            v = p[v]
        label += 1
    return cid


def classical_same_cycle_fraction(m, i=0, j=1):
    """Exhaustively enumerate all m! permutations of range(m); return the
    exact Fraction P(i,j in same cycle)."""
    assert 0 <= i < m and 0 <= j < m and i != j
    total = 0
    same = 0
    for p in itertools.permutations(range(m)):
        total += 1
        cid = cycle_id_of_permutation(p)
        if cid[i] == cid[j]:
            same += 1
    return Fraction(same, total), same, total


def main():
    print("Classical fact re-derivation (fresh, independent of the front's scripts)")
    print("P(i,j same cycle) for a uniform random permutation of m elements")
    print(f"{'m':>3} | {'same':>10} | {'total':>10} | {'fraction':>12} | matches 1/2?")
    all_ok = True
    for m in range(2, 10):
        frac, same, total = classical_same_cycle_fraction(m)
        ok = (frac == Fraction(1, 2))
        all_ok = all_ok and ok
        print(f"{m:>3} | {same:>10} | {total:>10} | {str(frac):>12} | {'YES' if ok else 'NO -- VIOLATION'}")
    print()
    if all_ok:
        print("RESULT: classical fact CONFIRMED exactly (fraction == 1/2) for every m in 2..9.")
    else:
        print("RESULT: VIOLATION FOUND -- see table above.")

    # A second, structurally different cross-check: instead of tracking a
    # fixed pair (0,1), verify the fact holds for EVERY pair (i,j), not
    # just (0,1), at a couple of m values, as an extra independent check
    # of the enumeration/labeling logic itself.
    print()
    print("Extra cross-check: verify P(i,j same cycle)=1/2 for ALL pairs (i,j), not just (0,1)")
    for m in [4, 5, 6]:
        counts_same = {}
        counts_total = {}
        for p in itertools.permutations(range(m)):
            cid = cycle_id_of_permutation(p)
            for i in range(m):
                for j in range(i + 1, m):
                    key = (i, j)
                    counts_total[key] = counts_total.get(key, 0) + 1
                    if cid[i] == cid[j]:
                        counts_same[key] = counts_same.get(key, 0) + 1
        m_ok = True
        for key in counts_total:
            frac = Fraction(counts_same.get(key, 0), counts_total[key])
            if frac != Fraction(1, 2):
                m_ok = False
                print(f"  m={m} pair {key}: VIOLATION, fraction={frac}")
        print(f"  m={m}: all C({m},2)={len(counts_total)} pairs give exactly 1/2: {'YES' if m_ok else 'NO'}")


if __name__ == "__main__":
    main()
