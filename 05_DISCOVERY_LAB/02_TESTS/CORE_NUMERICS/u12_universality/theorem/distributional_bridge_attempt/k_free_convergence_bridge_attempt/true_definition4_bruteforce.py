"""
Fresh, independent, exact (exhaustive) brute-force implementation of
THEOREM.md Definition 4 (K reroutes fixed at positions 0,...,K-1 of [n]),
for small (n,K). No code from any other front in this archive is used --
written from scratch from Definition 4's own description.

Points are labelled 0,...,n-1. Sources 0,...,K-1 are rerouted to targets
U_0,...,U_{K-1} in {0,...,n-1}; the remaining n-K points follow a uniform
random permutation pi (restricted to those points as a bijection of the
WHOLE point set composed with the identity on sources -- i.e. pi is a
uniform random permutation of {0,...,n-1}, and f(i):=U_i for i<K,
f(i):=pi(i) otherwise). T := #{i : i is cyclic under f} (i lies on a cycle
of the functional graph of f). Every permutation (n!) and every target
tuple (n^K) is enumerated exactly; the exact pmf of T is returned as a
dict {T-value: exact count}. No randomness.
"""
import itertools
import math
from fractions import Fraction as Fr


def exact_T_distribution(n, K):
    assert 0 <= K < n
    counts = {}
    total = 0
    all_points = list(range(n))
    for U in itertools.product(range(n), repeat=K):
        for perm in itertools.permutations(range(n)):
            f = list(perm)
            for i in range(K):
                f[i] = U[i]
            # find cyclic points: i is cyclic iff following f from i returns to i
            # compute via functional-graph cycle detection (standard: a point is
            # cyclic iff it lies on a cycle of the functional graph)
            T = 0
            # find all points on cycles via the "colors" method: white/gray/black
            color = [0] * n  # 0=unvisited,1=in progress,2=done
            on_cycle = [False] * n
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
                    # found a new cycle starting at x within path
                    idx = path.index(x)
                    for p in path[idx:]:
                        on_cycle[p] = True
                for p in path:
                    color[p] = 2
            T = sum(on_cycle)
            counts[T] = counts.get(T, 0) + 1
            total += 1
    assert total == math.factorial(n) * n ** K
    return counts, total


def exact_cdf_from_counts(n, counts, total):
    """Return {k/n: exact Fraction P(T<=k)} for k=0,...,n."""
    cdf = {}
    cum = 0
    for k in range(0, n + 1):
        cum += counts.get(k, 0)
        cdf[k] = Fr(cum, total)
    return cdf


if __name__ == "__main__":
    for (n, K) in [(4, 1), (5, 1), (4, 2), (5, 2), (6, 2), (5, 3), (6, 3)]:
        counts, total = exact_T_distribution(n, K)
        cdf = exact_cdf_from_counts(n, counts, total)
        mean = sum(Fr(k, 1) * Fr(c, total) for k, c in counts.items())
        print(f"n={n} K={K}: total={total} E[T]={mean} E[T]/n={mean/n}")
        print(f"   pmf(T): {dict(sorted(counts.items()))}")
