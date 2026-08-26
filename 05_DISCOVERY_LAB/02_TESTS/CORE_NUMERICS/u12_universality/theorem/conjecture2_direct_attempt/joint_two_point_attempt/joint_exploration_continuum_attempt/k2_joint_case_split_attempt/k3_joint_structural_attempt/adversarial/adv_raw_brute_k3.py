"""
Independent, from-scratch, TRUE raw brute-force enumeration of
Definition 4's full K=3 model, written purely from the mathematical
description (no .py file from any front in the lineage was read).

Model: pi a uniform random permutation of [n]; K=3 reroute sources fixed
at {0,1,2}; targets U0,U1,U2 iid Uniform([n]); f(i)=U_i for i in {0,1,2},
f(i)=pi(i) otherwise; query points fixed at {n-2,n-1}; "cyclic" means the
forward f-orbit returns to the starting point.

P_nn(n,3) := P(n-2 and n-1 both cyclic for f), computed EXACTLY over
every one of the n! * n^3 (pi, U0,U1,U2) configurations, via integer
counting (Fraction at the end only, to avoid float error).

This literally enumerates every permutation and every (U0,U1,U2) triple
-- no reduced/arc model, no shortcut of any kind.
"""
import itertools
import sys
import time
from fractions import Fraction


def is_cyclic(f, x, n):
    cur = f[x]
    for _ in range(n):
        if cur == x:
            return True
        cur = f[cur]
    return False


def compute_pnn3_raw(n):
    q1, q2 = n - 2, n - 1
    assert q1 not in (0, 1, 2) and q2 not in (0, 1, 2), "sources/queries must be disjoint"
    total = 0
    both_cyclic = 0

    rng = range(n)
    for pi in itertools.permutations(rng):
        f = list(pi)  # f[i] = pi(i) initially; will overwrite f[0],f[1],f[2] per U-triple
        for U0 in rng:
            f[0] = U0
            for U1 in rng:
                f[1] = U1
                for U2 in rng:
                    f[2] = U2
                    total += 1
                    if is_cyclic(f, q1, n) and is_cyclic(f, q2, n):
                        both_cyclic += 1
    return Fraction(both_cyclic, total), total, both_cyclic


if __name__ == '__main__':
    ns = [int(x) for x in sys.argv[1:]] or [6, 7]
    for n in ns:
        t0 = time.time()
        frac, total, cnt = compute_pnn3_raw(n)
        elapsed = time.time() - t0
        print(f"n={n}: P_nn(n,3) = {cnt}/{total} = {frac}  "
              f"(elapsed {elapsed:.2f}s)")
