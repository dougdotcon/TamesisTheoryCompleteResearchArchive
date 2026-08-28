"""
Independent, from-scratch TRUE brute-force ground truth for P_nn(n,K).

Model (as stated in general_k_joint_attempt/ATTEMPT.md Sec 1.2, itself a
direct restatement of THEOREM.md Definition 4 under WLOG source/query
fixing by exchangeability):

  pi: uniform random permutation of [n] (0-indexed here: {0,...,n-1})
  K reroute sources fixed at {0,...,K-1}
  U_0,...,U_{K-1} i.i.d. Uniform([n]) (0-indexed), independent of pi
  f(i) := U_i           for i in {0,...,K-1}
  f(i) := pi(i)         otherwise

Query points fixed at {n-2, n-1} (need n >= K+2 so they are disjoint from
sources).

P_nn(n,K) := P(both n-2 and n-1 are cyclic points of f)

where a point p is "cyclic" for f iff iterating f from p returns to p
(f is a general functional graph on n nodes, out-degree 1 each -- NOT
necessarily a permutation, since sources' images are overridden by
independent uniform targets, so the map is generally not a bijection).

This script enumerates ALL n! permutations times ALL n^K target vectors,
exactly, using Python's Fraction for the final ratio. No shortcuts, no
"arc"/"reduced model" abstraction -- literal simulation of the stated
process from Definition 4. Written without ever reading any .py file in
this front's or any sibling front's directory.
"""
import itertools
from fractions import Fraction
import sys
import time


def is_cyclic(f, p, n):
    # iterate f from p; if we return to p within n steps, cyclic
    cur = f[p]
    for _ in range(n):
        if cur == p:
            return True
        cur = f[cur]
    return False


def brute_force_Pnn(n, K):
    assert n >= K + 2
    q1, q2 = n - 2, n - 1
    total = 0
    both = 0
    for pi in itertools.permutations(range(n)):
        for U in itertools.product(range(n), repeat=K):
            f = list(pi)
            for i in range(K):
                f[i] = U[i]
            total += 1
            if is_cyclic(f, q1, n) and is_cyclic(f, q2, n):
                both += 1
    return Fraction(both, total), total


if __name__ == "__main__":
    cases = [(1, 3), (1, 4), (1, 5), (1, 6),
             (2, 4), (2, 5), (2, 6), (2, 7),
             (3, 5), (3, 6), (3, 7),
             (4, 6), (4, 7)]
    for K, n in cases:
        t0 = time.time()
        val, total = brute_force_Pnn(n, K)
        dt = time.time() - t0
        print(f"K={K} n={n} configs={total:>12,} P_nn={val} = {float(val):.10f}  ({dt:.1f}s)")
        sys.stdout.flush()
