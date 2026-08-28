"""
Fresh, from-scratch, fully-exhaustive ground truth for the K=2 full CDF.

Directly implements THEOREM.md Definition 4 at K=2, literally: enumerate
EVERY permutation pi of [n] and EVERY pair (U_0,U_1) in [n]^2, build the
mapping f, count cyclic points T, and tabulate the exact (Fraction) law
of T. No shortcuts, no reduced model, no code read from any other front.

This is the ground truth against which every closed-form claim in
ATTEMPT.md is checked.
"""
import sys
from fractions import Fraction
from itertools import permutations
from collections import Counter


def cyclic_count(f, n):
    """f: list of length n, f[i] in [0,n). Count points i with i on a
    directed cycle of the functional graph i -> f[i]."""
    # standard functional-graph cyclic-point detection: iterate each node
    # forward; a node is cyclic iff its forward orbit returns to itself.
    # O(n) approach: find all nodes with in-degree reachable... simplest
    # robust way for these small n: for each i, walk forward at most n+1
    # steps recording visited; if we return to i, cyclic. This is O(n^2)
    # worst case, fine for the n we brute-force here.
    cyclic = [False] * n
    color = [0] * n  # 0 unvisited, 1 in progress, 2 done
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
            # found a new cycle starting at x within `path`
            idx = path.index(x)
            for y in path[idx:]:
                cyclic[y] = True
        for y in path:
            color[y] = 2
    return sum(cyclic)


def brute_force_T_distribution(n):
    """Exact distribution of T for Definition 4's K=2 model at fixed n.
    Sources fixed at {0,1} (Definition 4's own exchangeability argument,
    used only to cut the enumeration cost -- NOT assumed correct without
    this being exactly Definition 4's construction restricted to a
    specific K-subset, which by definition has the same law as a random
    K-subset by exchangeability of pi and independence of pi, U's)."""
    assert n >= 2
    counts = Counter()
    total = 0
    idx = list(range(n))
    for perm in permutations(idx):
        # perm[i] = pi(i)
        for U0 in range(n):
            for U1 in range(n):
                f = list(perm)
                f[0] = U0
                f[1] = U1
                T = cyclic_count(f, n)
                counts[T] += 1
                total += 1
    return counts, total


def cdf_from_counts(counts, total, n):
    """Return dict k -> Fraction P(T<=k), k=0..n."""
    cum = 0
    out = {}
    for k in range(0, n + 1):
        cum += counts.get(k, 0)
        out[k] = Fraction(cum, total)
    return out


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [2, 3, 4, 5, 6, 7]
    for n in ns:
        counts, total = brute_force_T_distribution(n)
        cdf = cdf_from_counts(counts, total, n)
        print(f"n={n} total_configs={total}")
        for k in range(0, n + 1):
            print(f"  k={k}  P(T<=k) = {cdf[k]}  (={float(cdf[k]):.6f})")
        print(f"  pmf: {dict(sorted(counts.items()))}")
        sys.stdout.flush()
