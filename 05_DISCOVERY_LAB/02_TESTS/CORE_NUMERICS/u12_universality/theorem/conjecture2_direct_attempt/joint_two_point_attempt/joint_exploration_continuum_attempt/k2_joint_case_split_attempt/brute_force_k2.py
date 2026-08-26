"""
Fresh, independent, from-scratch exact brute-force enumeration of
Definition 4's finite conditional-K model (THEOREM.md Sec 7.2) at K=2,
computing P_nn(n,2) := P(q1, q2 both cyclic) for two fixed non-rerouted
query points, and the marginal ψ_n^{(2)} = P(generic point cyclic) as a
cross-check against THEOREM.md's already-proved closed form
ψ_n^{(2)} = 8/15 + 4/(15n) + 1/(15n^2).

Model: points labeled 0..n-1. Rerouted sources fixed at {0,1} (K=2).
Query points fixed at {n-2, n-1} (the two "last" labels, generic,
non-rerouted, distinct from sources as long as n>=4).
pi ranges over all n! permutations of [n]; U0, U1 range independently
over all n targets each (Definition 1's reroute targets).
f(i) = U_i for i in {0,1}, f(i) = pi(i) otherwise.

Exact rational arithmetic (Fraction) throughout; no floating point, no
sampling. This script does NOT import or read any code from any other
front in this lineage -- it is written fresh from Definition 4's prose
description alone.
"""
from fractions import Fraction
from itertools import permutations
import sys


def cyclic_points(f, n):
    """Return the set of points x in [n] with f^k(x) = x for some k>=1."""
    cyclic = set()
    color = [0] * n  # 0 = unvisited, 1 = in-progress, 2 = done
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:
            # x is the entrance of a fresh cycle just found in this path
            idx = path.index(x)
            for y in path[idx:]:
                cyclic.add(y)
        for y in path:
            color[y] = 2
    return cyclic


def run(n):
    assert n >= 4
    q1, q2 = n - 2, n - 1
    total = 0
    both_cyclic = 0
    generic_cyclic = 0  # marginal check: point q1 alone
    for pi in permutations(range(n)):
        for u0 in range(n):
            for u1 in range(n):
                f = list(pi)
                f[0] = u0
                f[1] = u1
                cyc = cyclic_points(f, n)
                total += 1
                if q1 in cyc and q2 in cyc:
                    both_cyclic += 1
                if q1 in cyc:
                    generic_cyclic += 1
    return Fraction(both_cyclic, total), Fraction(generic_cyclic, total), total


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [4, 5, 6]
    for n in ns:
        pnn, psi, total = run(n)
        # cross-check against THEOREM.md's already-proved psi_n^{(2)}
        psi_theorem = Fraction(8, 15) + Fraction(4, 15 * n) + Fraction(1, 15 * n * n)
        match = "OK" if psi == psi_theorem else "MISMATCH!!"
        print(f"n={n}: total_configs={total} "
              f"P_nn(n,2)={pnn} ({float(pnn):.6f})  "
              f"psi_n^(2)={psi} ({float(psi):.6f}) vs THEOREM.md {psi_theorem} [{match}]")
