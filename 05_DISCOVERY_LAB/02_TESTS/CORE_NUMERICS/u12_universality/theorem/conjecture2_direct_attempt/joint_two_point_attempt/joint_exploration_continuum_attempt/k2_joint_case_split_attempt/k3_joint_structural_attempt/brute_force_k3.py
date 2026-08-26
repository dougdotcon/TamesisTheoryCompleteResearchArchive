"""
brute_force_k3.py

Ground-truth exhaustive enumeration of Definition 4 (THEOREM.md Sec 7.2),
the finite conditional-K model, at K=3, for small n.

Written entirely from scratch from the prose description of Definition 4 in
THEOREM.md (as read by this front) and the notational conventions of the
predecessor ATTEMPT.md (k2_joint_case_split_attempt), WITHOUT reading or
importing any .py file from any other front, per the hard constraint of this
front's mandate.

Model (Definition 4, K=3 instance): pi a uniform random permutation of
[n] = {0,...,n-1}. Reroute sources fixed WLOG at {0,1,2} (Definition 4's own
exchangeability argument, cited). Targets U0,U1,U2 i.i.d. Uniform([n]),
independent of pi. f(i) := U_i for i in {0,1,2}; f(i) := pi(i) otherwise.
Query points fixed WLOG at {n-3, n-2, n-1} (distinct from the sources,
requiring n >= 6).

P_nn(n,3) := P(n-3, n-2, n-1 ... wait: query set here is TWO points, matching
Lemma P2 / Proposition NN2's own P_nn(n,K) convention: P_nn(n,K) is the
probability that TWO specific query points (not K of them) are both cyclic
for f, with the query points held fixed and disjoint from the K reroute
sources. We use query points {n-2, n-1} (the last two indices), requiring
n >= 5 (3 sources + 2 distinct query points, with the query points allowed to
coincide with index n-3 or not -- we only need n-2, n-1 disjoint from
{0,1,2}, i.e. n >= 5 suffices arithmetically, but n>=6 is used throughout to
keep a safety margin consistent with the predecessor's own n>=4 requirement
at K=2, scaled up for K=3: sources {0,1,2} + queries {n-2,n-1} need
n-2 > 2, i.e. n >= 5; we use n>=6 for the brute-force table to have a little
room and match the predecessor's convention style).

A point x is "cyclic" for f iff iterating f from x returns to x within n
steps (equivalently: x lies on a directed cycle of the functional graph of
f). This exactly matches the definition used throughout THEOREM.md and the
predecessor ATTEMPT.md.

Exact rational arithmetic via fractions.Fraction throughout; no floating
point at any stage. No randomness in this script (fully exhaustive).
"""

import sys
import time
from fractions import Fraction
from itertools import permutations, product


def is_cyclic(f, x, n):
    """Return True iff iterating f from x returns to x (x lies on a cycle
    of the functional graph of f)."""
    y = f[x]
    steps = 1
    while y != x and steps <= n:
        y = f[y]
        steps += 1
    return y == x


def p_nn_k3(n, verbose=False):
    """Exhaustive computation of P_nn(n,3) = P(query points n-2,n-1 both
    cyclic for f), over ALL n! permutations pi and ALL n^3 (U0,U1,U2)
    combinations, each equally likely (total n! * n^3 equally likely
    configurations)."""
    assert n >= 6, "need sources {0,1,2} and queries {n-2,n-1} disjoint, with margin"
    q1, q2 = n - 2, n - 1
    both_count = 0
    total = 0
    t0 = time.time()
    perm_count = 0
    for pi in permutations(range(n)):
        perm_count += 1
        f = list(pi)
        for U0, U1, U2 in product(range(n), repeat=3):
            f[0], f[1], f[2] = U0, U1, U2
            if is_cyclic(f, q1, n) and is_cyclic(f, q2, n):
                both_count += 1
            total += 1
        if verbose and perm_count % 5000 == 0:
            elapsed = time.time() - t0
            print(f"  n={n}: {perm_count}/{__import__('math').factorial(n)} "
                  f"permutations done, {elapsed:.1f}s elapsed", file=sys.stderr)
    p = Fraction(both_count, total)
    return p, both_count, total


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [6, 7]
    print("n, both_count, total, P_nn(n,3) [exact], float, elapsed_s")
    for n in ns:
        t0 = time.time()
        p, both_count, total = p_nn_k3(n, verbose=True)
        elapsed = time.time() - t0
        print(f"{n}, {both_count}, {total}, {p}, {float(p):.10f}, {elapsed:.2f}")
