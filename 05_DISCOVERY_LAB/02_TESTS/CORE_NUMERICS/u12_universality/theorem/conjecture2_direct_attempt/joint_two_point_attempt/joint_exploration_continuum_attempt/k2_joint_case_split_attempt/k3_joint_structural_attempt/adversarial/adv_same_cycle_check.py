"""
Independent, from-scratch raw brute-force check that, within Definition
4's K=3 model, P(both cyclic AND same final cycle) is EXACTLY half of
P(both cyclic) -- i.e. a direct numeric confirmation of Theorem J's
Corollary (cited from Estagio 25) applied at K=3, rather than blind trust
in the citation. Also checks Corollary NN3.2's arithmetic
(P_nn-same(n,3) -> 1/8) against the raw data.

No .py file from any front in the lineage was read.
"""
import itertools
import sys
import time
from fractions import Fraction


def cycle_of(f, x, n):
    """Returns the set of points in x's forward orbit if x is cyclic,
    else None."""
    cur = f[x]
    path = [x]
    for _ in range(n):
        if cur == x:
            return set(path)
        path.append(cur)
        cur = f[cur]
    return None


def compute(n):
    q1, q2 = n - 2, n - 1
    total = 0
    both_cyclic = 0
    both_same_cycle = 0

    rng = range(n)
    for pi in itertools.permutations(rng):
        f = list(pi)
        for U0 in rng:
            f[0] = U0
            for U1 in rng:
                f[1] = U1
                for U2 in rng:
                    f[2] = U2
                    total += 1
                    c1 = cycle_of(f, q1, n)
                    if c1 is None:
                        continue
                    c2 = cycle_of(f, q2, n)
                    if c2 is None:
                        continue
                    both_cyclic += 1
                    if q2 in c1:
                        both_same_cycle += 1
    return total, both_cyclic, both_same_cycle


if __name__ == '__main__':
    ns = [int(x) for x in sys.argv[1:]] or [6, 7]
    for n in ns:
        t0 = time.time()
        total, both, same = compute(n)
        elapsed = time.time() - t0
        p_both = Fraction(both, total)
        p_same = Fraction(same, total)
        ratio = Fraction(same, both) if both else None
        print(f"n={n}: P(both cyclic)={p_both}  P(both, same cycle)={p_same}  "
              f"ratio same/both={ratio}  (elapsed {elapsed:.2f}s)")
