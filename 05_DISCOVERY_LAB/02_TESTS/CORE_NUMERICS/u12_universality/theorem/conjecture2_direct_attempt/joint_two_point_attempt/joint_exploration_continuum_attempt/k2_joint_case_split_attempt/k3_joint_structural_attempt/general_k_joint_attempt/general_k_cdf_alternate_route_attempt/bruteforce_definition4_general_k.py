"""
Fresh, independent ground-truth brute force for Definition 4 (THEOREM.md
Section 7.2): pi a uniform random permutation of {0,...,n-1}, K fixed
sources {0,...,K-1} (WLOG by exchangeability), each source i has an
independent uniform target U_i in {0,...,n-1}. f(i):=U_i for i a source,
f(i):=pi(i) otherwise. T := #{cyclic points of f} (points lying on a
cycle of the functional graph of f). M_n^{(K)} := T/n.

This script enumerates EVERY permutation pi of [n] and EVERY target tuple
(U_0,...,U_{K-1}) in [n]^K exhaustively (exact counting, Fraction
arithmetic, no shortcut), and reports the exact CDF vector
P(T<=k), k=0,...,n, for each (n,K) requested.

Written completely fresh from the Definition 4 prose in THEOREM.md
Section 7.2 -- no script from any sibling or ancestor front was read or
imported. This is the archive-standard independent ground truth every
front in this lineage cross-checks against.
"""
from fractions import Fraction
from itertools import permutations, product


def cyclic_count(f, n):
    """f: list of length n, f[i] in [0,n). Count points lying on a cycle
    of the functional graph (standard: iterate n steps from a "visited"
    marker via cycle detection -- rho-shaped functional graphs have a
    unique cycle per weakly-connected component, found by tortoise-hare
    or simple forward-marking)."""
    color = [0] * n  # 0 = unvisited, 1 = in progress, 2 = done
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
            # found a new cycle: everything in path from x's first
            # occurrence onward is on the cycle
            idx = path.index(x)
            for p in path[idx:]:
                on_cycle[p] = True
        for p in path:
            color[p] = 2
    return sum(on_cycle)


def bruteforce_cdf(n, K):
    """Returns exact Fraction vector P(T<=k) for k=0..n."""
    assert 0 <= K <= n
    counts = [0] * (n + 1)
    total = 0
    for pi in permutations(range(n)):
        for targets in product(range(n), repeat=K):
            f = list(pi)
            for i in range(K):
                f[i] = targets[i]
            T = cyclic_count(f, n)
            counts[T] += 1
            total += 1
    cdf = []
    running = 0
    for k in range(n + 1):
        running += counts[k]
        cdf.append(Fraction(running, total))
    return cdf, counts, total


if __name__ == "__main__":
    cases = [(4, 1), (4, 2), (5, 2), (5, 3), (6, 3), (6, 4), (7, 3), (7, 4)]
    print("Fresh independent Definition-4 brute force (ground truth).")
    print("=" * 70)
    results = {}
    for (n, K) in cases:
        cdf, counts, total = bruteforce_cdf(n, K)
        results[(n, K)] = cdf
        print(f"n={n} K={K}  total={total}")
        for k in range(n + 1):
            print(f"   P(T<={k}) = {cdf[k]}")
        print("-" * 70)

    # Sanity checks: CDF must be nondecreasing, end at 1, start >= 0.
    all_ok = True
    for (n, K), cdf in results.items():
        ok = (cdf[-1] == 1) and all(cdf[i] <= cdf[i + 1] for i in range(len(cdf) - 1))
        if not ok:
            all_ok = False
            print(f"SANITY FAIL at (n,K)=({n},{K})")
    print(f"All CDF sanity checks (nondecreasing, ends at 1) passed: {all_ok}")

    # Save results for import by other verification scripts in this directory.
    import json
    out = {f"{n}_{K}": [str(x) for x in cdf] for (n, K), cdf in results.items()}
    with open("bruteforce_cdf_cache.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("Saved bruteforce_cdf_cache.json")
