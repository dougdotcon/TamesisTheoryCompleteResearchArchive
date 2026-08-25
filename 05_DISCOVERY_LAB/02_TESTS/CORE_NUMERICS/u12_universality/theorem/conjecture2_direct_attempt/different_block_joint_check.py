"""
Exact brute-force check of the third elementary classical fact used in
ATTEMPT.md Section 3.3: for a uniform random permutation of [n],
conditional on labels 1,2 lying in DIFFERENT cycles, of lengths
(ell1, ell2) respectively, the joint counting measure of (ell1,ell2)
is UNIFORM over {(ell1,ell2): ell1,ell2>=1, ell1+ell2<=n} -- i.e. every
lattice point in that discrete triangle is equally likely. This is the
discrete-n analogue of the continuum claim that, given x1,x2 are in
different PD(1) blocks, the joint density of (block-length-1,
block-length-2) is uniform (density 1, i.e. constant) on the simplex
{m1,m2>0, m1+m2<1} -- used in ATTEMPT.md Section 3.3.
"""
import itertools
from collections import Counter

def cycle_lengths_1_2(perm, n):
    # length of cycle containing 1
    y = 1
    l1 = 0
    while True:
        y = perm[y - 1]
        l1 += 1
        if y == 1:
            break
    same = False
    y = perm[0]
    z = 1
    while z != 1 or l1 == 0:
        pass
    # simpler: check membership by re-walking
    seen1 = set()
    y = 1
    for _ in range(l1):
        seen1.add(y)
        y = perm[y - 1]
    if 2 in seen1:
        return l1, None  # same cycle
    y = 2
    l2 = 0
    while True:
        y = perm[y - 1]
        l2 += 1
        if y == 2:
            break
    return l1, l2

for n in range(3, 8):
    counts = Counter()
    total = 0
    for perm in itertools.permutations(range(1, n + 1)):
        total += 1
        l1, l2 = cycle_lengths_1_2(perm, n)
        if l2 is not None:
            counts[(l1, l2)] += 1
    vals = sorted(set(counts.values()))
    expected_pairs = [(a, b) for a in range(1, n) for b in range(1, n) if a + b <= n]
    missing = [p for p in expected_pairs if p not in counts]
    print(f"n={n}: distinct count-values over all (ell1,ell2) pairs = {vals}  "
          f"(uniform iff single value)  missing_pairs={missing}")
