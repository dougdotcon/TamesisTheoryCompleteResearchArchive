"""Referee from-scratch exact enumeration of the three discrete finite-n
cross-checks of ATTEMPT.md Section 3.2 (Lemmas B1-B3 analogues), rebuilt
purely from the ATTEMPT.md prose (no front script read or reused).

For every permutation of [n] (itertools.permutations, exact integer counts):

  [D1] (Lemma B1 analogue)  #{pi : 1,2 in the same cycle} == n!/2 exactly,
       for n = 2..8.
  [D2] (Lemma B2 analogue)  given 1,2 in the same cycle of length ell, the
       forward pi-distance d from 1 to 2 is exactly uniform on {1..ell-1}:
       every (ell,d) cell carries the identical count -- and that count is
       (n-2)! (referee-derived closed form: choose the other ell-2 cycle
       mates C(n-2,ell-2), place them (ell-2)!, permute the rest (n-ell)!
       => (n-2)! independent of both ell and d).  n = 3..8.
  [D3] (Lemma B3 analogue)  given 1,2 in different cycles of lengths
       (ell1, ell2), every lattice cell with ell1,ell2>=1, ell1+ell2<=n
       carries the identical count, again (n-2)! (same telescoping:
       C(n-2,ell1-1)(ell1-1)! * C(n-1-ell1,ell2-1)(ell2-1)! * (n-ell1-ell2)!
       == (n-2)!).  n = 3..8.

All counts exact integers; asserts halt loudly on any deviation.
"""
import itertools
import math
from collections import Counter

FAIL = 0


def cycle_info(perm, n):
    """perm: tuple, perm[i] = image of i (0-indexed). Return (same, ell or
    (ell1,ell2), forward distance 0->1 if same)."""
    # cycle of 0
    cyc0 = [0]
    j = perm[0]
    while j != 0:
        cyc0.append(j)
        j = perm[j]
    if 1 in cyc0:
        d = cyc0.index(1)          # forward distance from 0 to 1
        return True, len(cyc0), d
    # cycle of 1
    cyc1 = [1]
    j = perm[1]
    while j != 1:
        cyc1.append(j)
        j = perm[j]
    return False, (len(cyc0), len(cyc1)), None


for n in range(2, 9):
    total = math.factorial(n)
    same_count = 0
    same_cells = Counter()   # (ell, d) -> count
    diff_cells = Counter()   # (ell1, ell2) -> count
    for perm in itertools.permutations(range(n)):
        same, info, d = cycle_info(perm, n)
        if same:
            same_count += 1
            same_cells[(info, d)] += 1
        else:
            diff_cells[info] += 1

    # D1
    ok1 = (2 * same_count == total)
    print(f"n={n}: P(1,2 same cycle) = {same_count}/{total}"
          f"  == 1/2: {ok1}")
    if not ok1:
        FAIL += 1

    if n < 3:
        continue
    ref = math.factorial(n - 2)

    # D2: uniform over d within each ell, and equal to (n-2)!
    ok2 = True
    for ell in range(2, n + 1):
        counts = [same_cells.get((ell, d), 0) for d in range(1, ell)]
        if any(cc != ref for cc in counts):
            ok2 = False
            print(f"  D2 DEVIATION n={n} ell={ell}: {counts} != {ref}")
    # completeness: no unexpected cells
    exp_same = sum(ell - 1 for ell in range(2, n + 1)) * ref
    if exp_same != same_count:
        ok2 = False
        print(f"  D2 CELL-TOTAL MISMATCH n={n}: {exp_same} != {same_count}")
    print(f"  D2 same-cycle: every (ell,d) cell == (n-2)! = {ref}: {ok2}")
    if not ok2:
        FAIL += 1

    # D3: single count value over all valid (ell1, ell2), equal to (n-2)!
    ok3 = True
    for ell1 in range(1, n):
        for ell2 in range(1, n - ell1 + 1):
            cc = diff_cells.get((ell1, ell2), 0)
            if cc != ref:
                ok3 = False
                print(f"  D3 DEVIATION n={n} ({ell1},{ell2}): {cc} != {ref}")
    # no cells outside the simplex
    for (a, b), cc in diff_cells.items():
        if a + b > n:
            ok3 = False
            print(f"  D3 IMPOSSIBLE CELL n={n}: ({a},{b}) count {cc}")
    exp_diff = sum(1 for a in range(1, n) for b in range(1, n - a + 1)) * ref
    if exp_diff != total - same_count:
        ok3 = False
        print(f"  D3 CELL-TOTAL MISMATCH n={n}: {exp_diff} != {total - same_count}")
    print(f"  D3 different-cycle: every (ell1,ell2) cell == (n-2)! = {ref}: {ok3}")
    if not ok3:
        FAIL += 1

print()
print("TOTAL FAILURES:", FAIL)
assert FAIL == 0, "AT LEAST ONE DISCRETE ENUMERATION CHECK FAILED"
print("ALL DISCRETE ENUMERATION CHECKS PASSED (n = 2..8, exact)")
