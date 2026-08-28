"""
True Definition-4 brute force, general K -- built completely fresh from
THEOREM.md's own prose description of Definition 4 (no code from any other
front in this lineage read or reused).

Model (Definition 4): pi a uniform random permutation of [n]. K reroute
sources fixed WLOG at {0,...,K-1}. Targets U_0,...,U_{K-1} i.i.d. Uniform
on [n], independent of pi. f(i):=U_i for i a source, f(i):=pi(i) otherwise.
f is therefore a (generally non-bijective) function [n]->[n] -- a
functional graph. T := #{cyclic points of f} (points lying on a cycle of
this functional graph). M_n^{(K)} := T/n.

This script enumerates, EXACTLY (every pi, every target tuple), the
distribution of T for small (n,K), and reports the exact rational CDF
P(T<=k) for every k, using fractions.Fraction throughout (no floating
point). This is the independent ground truth against which every other
claim in this front is checked.
"""
from fractions import Fraction
from itertools import permutations, product
from math import factorial as fact


def cyclic_points_count(f, n):
    """Number of points of [n] lying on a cycle of the functional graph f.

    Standard functional-graph algorithm: walk from each unvisited node,
    marking nodes 'in progress'; if the walk re-enters an 'in progress'
    node, that closes a genuine cycle -- mark every node on that cycle
    (from the re-entry point onward in the walk) as cyclic.
    """
    color = [0] * n  # 0 = unvisited, 1 = in progress, 2 = done
    on_cycle = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        cur = start
        while color[cur] == 0:
            color[cur] = 1
            path.append(cur)
            cur = f[cur]
        if color[cur] == 1:
            idx = path.index(cur)
            for node in path[idx:]:
                on_cycle[node] = True
        for node in path:
            color[node] = 2
    return sum(on_cycle)


def bruteforce_cdf(n, K):
    """Returns (cdf, total_configs). cdf[k] = Fraction P(T<=k), k=0..n."""
    counts = [0] * (n + 1)
    total = 0
    for pi in permutations(range(n)):
        for targets in product(range(n), repeat=K):
            f = {}
            for s in range(K):
                f[s] = targets[s]
            for i in range(K, n):
                f[i] = pi[i]
            T = cyclic_points_count(f, n)
            counts[T] += 1
            total += 1
    assert total == fact(n) * n ** K
    cdf = {}
    cum = 0
    for k in range(n + 1):
        cum += counts[k]
        cdf[k] = Fraction(cum, total)
    return cdf, total


if __name__ == "__main__":
    print("True Definition-4 brute force, general K -- ground truth.")
    print("=" * 70)
    cases = [(4, 1), (5, 1), (4, 2), (5, 2), (6, 2), (4, 3), (5, 3), (6, 3), (5, 4), (6, 4)]
    for n, K in cases:
        cdf, total = bruteforce_cdf(n, K)
        print(f"n={n} K={K}  (total exact configs = {total})")
        for k in range(n + 1):
            print(f"   P(T<={k}) = {cdf[k]}")
    print("=" * 70)
    print("Ground truth generated for all cells above (own from-scratch")
    print("enumeration, exact Fraction arithmetic, no shortcut of any kind).")
