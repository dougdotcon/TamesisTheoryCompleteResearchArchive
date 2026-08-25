"""
Exact brute-force check of a second elementary classical fact used in
ATTEMPT.md Section 3.3: for a uniform random permutation of [n],
CONDITIONAL on two distinct labels i,j lying in the same cycle (of
whatever length ell results), the forward distance from i to j around
that cycle (number of pi-steps from i until first hitting j) is
UNIFORM on {1,...,ell-1}, where ell is the (also random) shared cycle
length -- i.e. jointly, (ell, forward-distance) has the law: ell take
any value with the count derived below, and given ell, the forward
offset is exactly uniform on {1,...,ell-1}.

This is the discrete analogue of the continuum claim (used, but not
fully exploited due to the identified obstruction, in ATTEMPT.md
Section 3.3): given x1,x2 share a PD(1) block of length ell, the
forward arc-distance from x1 to x2 within it is Unif(0,ell).
"""
import itertools
from fractions import Fraction
from collections import Counter

def forward_offset_and_length(perm, i, j, n):
    y = i
    d = 0
    while True:
        y = perm[y - 1]
        d += 1
        if y == i:
            return None  # closed back to i without hitting j -> not same cycle
        if y == j:
            # need full cycle length: continue from j back to i
            length = d
            z = y
            while z != i:
                z = perm[z - 1]
                length += 1
            return (d, length)

for n in range(3, 8):
    counts = Counter()  # (ell, d) -> count
    total = 0
    for perm in itertools.permutations(range(1, n + 1)):
        total += 1
        r = forward_offset_and_length(perm, 1, 2, n)
        if r is not None:
            counts[r] += 1
    # for each ell, check uniformity of d in {1,...,ell-1}
    by_ell = {}
    for (d, ell), cnt in counts.items():
        by_ell.setdefault(ell, {})[d] = cnt
    ok = True
    for ell, dmap in sorted(by_ell.items()):
        vals = set(dmap.values())
        if len(vals) != 1 or set(dmap.keys()) != set(range(1, ell)):
            ok = False
        print(f"  n={n} ell={ell}: counts over d=1..{ell-1} = {[dmap[d] for d in range(1,ell)]}  uniform: {len(vals)==1}")
    print(f"n={n}: ALL ell uniform in offset: {ok}\n")
