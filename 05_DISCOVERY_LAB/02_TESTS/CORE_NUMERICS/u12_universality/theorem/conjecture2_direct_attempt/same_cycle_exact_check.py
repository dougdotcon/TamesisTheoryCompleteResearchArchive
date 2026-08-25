"""
Exact brute-force check of the classical fact used in ATTEMPT.md Section
3.3 (block-structure reduction): for a uniform random permutation of
[n], two distinct fixed labels i != j lie in the SAME cycle with
probability EXACTLY 1/2, for every n >= 2 -- not just asymptotically.

This is the discrete-n analogue of the continuum fact this document
derives fresh (P(x1, x2 in the same PD(1) block) = 1/2, via
E[L] = integral_0^1 ell dell = 1/2 using Fact A, L~Unif(0,1)), and
serves as an independent cross-check that the continuum derivation's
answer is the "n->infinity limit" of a genuine, exactly verifiable
finite-n fact (not merely plausible-sounding).

Exact rational arithmetic via itertools.permutations (feasible for
n<=8 or so) -- no floating point, no sampling.
"""
import itertools
from fractions import Fraction


def same_cycle(perm, i, j, n):
    # perm: tuple, perm[k-1] = pi(k), 1-indexed labels 1..n
    y = i
    while True:
        y = perm[y - 1]
        if y == i:
            return False  # closed back to i without hitting j
        if y == j:
            return True


results = {}
for n in range(2, 8):
    count_same = 0
    total = 0
    for perm in itertools.permutations(range(1, n + 1)):
        total += 1
        if same_cycle(perm, 1, 2, n):
            count_same += 1
    frac = Fraction(count_same, total)
    results[n] = frac
    print(f"n={n}: P(1,2 same cycle) = {count_same}/{total} = {frac}  (== 1/2: {frac == Fraction(1,2)})")

assert all(v == Fraction(1, 2) for v in results.values()), "classical fact FAILED at some n"
print()
print("CONFIRMED: P(1,2 same cycle) = 1/2 EXACTLY for every n=2..7 (classical fact).")
print("This matches, exactly, the continuum fact derived in ATTEMPT.md Section 3.3:")
print("P(two independent uniform points share a PD(1) block) = E[L] = 1/2, L~Unif(0,1).")
