"""
Independent, from-scratch brute force for Estagio 28's OWN finite-n
convention: query points fixed at {0,1}; the K=2 reroute-source set R is a
uniform random 2-subset of ALL of [n] (allowed to intersect {0,1}), targets
i.i.d. Uniform([n]) for i in R, f(i)=pi(i) otherwise.

This is DIFFERENT from the P_nn convention (brute_k2_ref.py), where the
reroute sources are fixed WLOG at {0,1} and the query points are the
OTHER two indices n-2,n-1 (always disjoint from the sources).

Written entirely from the mathematical description in THEOREM.md Estagio 28
/ joint_exploration_continuum_attempt/ATTEMPT.md's prose (Proposition K1's
setup, section 1). No .py file from any front was read.

We compute P(0,1 both cyclic) exactly via Fraction, iterating over:
  - pi in Sym([n])              (n! permutations)
  - R, an unordered 2-subset of [n]   (C(n,2) subsets)
  - (u_r for r in R), each in [n]    (n^2 assignments)
"""
import sys
import os
import itertools
from fractions import Fraction
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cycle_utils import cyclic_points


def compute_overlap_cell(n, verbose=True):
    assert n >= 2
    total = 0
    count_both = 0

    t0 = time.time()
    subsets = list(itertools.combinations(range(n), 2))
    for pi in itertools.permutations(range(n)):
        f_base = list(pi)
        for (r1, r2) in subsets:
            for u1 in range(n):
                for u2 in range(n):
                    f = list(f_base)
                    f[r1] = u1
                    f[r2] = u2
                    total += 1
                    cyc = cyclic_points(f)
                    if 0 in cyc and 1 in cyc:
                        count_both += 1
    elapsed = time.time() - t0

    P_both = Fraction(count_both, total)
    if verbose:
        print(f"n={n}: total={total} time={elapsed:.2f}s "
              f"P_n^(2)(both) [overlap-allowed] = {P_both} ({float(P_both):.6f})")
    return {"n": n, "total": total, "P_both": P_both, "elapsed": elapsed}


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [4, 5]
    for n in ns:
        compute_overlap_cell(n)
