"""
K3-FULL-CDF-ATTEMPT -- fresh, independent, fully-exhaustive ground truth
for the ENTIRE distribution (not just the second moment) of
T = #{cyclic points of f} at K=3, straight from Definition 4's prose
(THEOREM.md Sec.7.2): pi a uniform permutation of [n], K=3 reroute sources
fixed WLOG at {0,1,2}, U_0,U_1,U_2 each independently Uniform([n]),
f(i)=U_i for i in {0,1,2}, f(i)=pi(i) otherwise. A point x is cyclic iff
iterating f from x returns to x.

Enumerates every one of n!*n^3 configurations exactly (Fraction
arithmetic). Used only to validate the closed-form CDF (Proposicao D3) at
small n, n=3..8 -- the smallest possible n (n=3, no interior points at
all, O=0 forced) through n=8 (matching Estagio 35's own verification
range for the second-moment-only quantity P_nn(n,3)).

No code read from any other front (this lineage or ancestor/sibling).
"""
import sys
import time
from fractions import Fraction
from itertools import permutations, product
from collections import Counter


def cdf_at_n(n, K=3):
    counts = Counter()
    total = 0
    for pi in permutations(range(n)):
        for U in product(range(n), repeat=K):
            f = list(pi)
            for i in range(K):
                f[i] = U[i]
            cyc = 0
            for x in range(n):
                cur = x
                visited = set()
                while cur not in visited:
                    visited.add(cur)
                    cur = f[cur]
                if cur == x:
                    cyc += 1
            counts[cyc] += 1
            total += 1
    cdf = {}
    cum = Fraction(0)
    for T in range(0, n + 1):
        cum += Fraction(counts.get(T, 0), total)
        cdf[T] = cum
    return cdf, total


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else [3, 4, 5, 6, 7, 8]
    for n in ns:
        t0 = time.time()
        cdf, total = cdf_at_n(n)
        dt = time.time() - t0
        print(f"n={n}  total_configs={total}  ({dt:.2f}s)")
        for k in range(0, n + 1):
            print(f"   P(T<={k:2d}) = {cdf[k]}")
        print()
