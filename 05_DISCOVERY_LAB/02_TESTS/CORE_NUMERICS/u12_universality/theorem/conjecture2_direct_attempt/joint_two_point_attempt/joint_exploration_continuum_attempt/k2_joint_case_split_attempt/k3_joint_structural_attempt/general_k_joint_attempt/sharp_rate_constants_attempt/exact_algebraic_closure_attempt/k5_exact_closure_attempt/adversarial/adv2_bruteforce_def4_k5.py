"""
INDEPENDENT REFEREE brute-force enumeration of THEOREM.md Definition 4,
K=5, written completely fresh (no code read from the target's own
bruteforce_definition4_k5.py, which was not opened for its code -- only
its PROSE/claims in ATTEMPT.md were read).

Definition 4 (THEOREM.md lines 859-872), restated:
  - pi a uniform random permutation of [n].
  - K indices (WLOG {0,...,K-1} by exchangeability) are "reroute sources";
    each source i gets an independent uniform random target U_i in [n]
    (Definition 1's reroute mechanism), replacing pi(i).
  - f(i) := U_i for i<K, f(i) := pi(i) otherwise.
  - T := #{cyclic points of f} := #{i : the forward f-orbit of i returns
    to i}.
  - M_n^{(K)} := T/n.  F_n^{(K)}(x) := P(M_n^{(K)} <= x).

This script enumerates ALL n! permutations pi and ALL n^K reroute-target
tuples U EXHAUSTIVELY (no decomposition, no shortcut, no importing of
any "arc"/"cycle-count-decomposition" theory) and computes the exact
distribution of T, hence the exact CDF, as a Fraction.

Implementation deliberately DIFFERENT in style from a naive re-walk-based
cycle detector: uses functional-graph "rho" cycle detection via visited
timestamps (Floyd/Brent-free direct method), coded independently.
"""
import sys
import time
from fractions import Fraction
from itertools import permutations, product
from math import factorial


def cyclic_point_count(f):
    """f: tuple/list, f[i] in range(len(f)). Returns number of i on a
    cycle of the functional graph i -> f[i]."""
    n = len(f)
    state = [0] * n     # 0 = unvisited, 1 = on current DFS stack (with a
                          # step index in `stamp`), 2 = fully resolved
    stamp = [0] * n
    on_cycle = [False] * n
    for start in range(n):
        if state[start] != 0:
            continue
        path = []
        v = start
        while state[v] == 0:
            state[v] = 1
            stamp[v] = len(path)
            path.append(v)
            v = f[v]
        if state[v] == 1:
            # found a back-edge into the CURRENT path -> genuine cycle
            for u in path[stamp[v]:]:
                on_cycle[u] = True
        for u in path:
            if state[u] == 1:
                state[u] = 2
    return sum(on_cycle)


def exact_cdf_K5(n):
    K = 5
    assert n >= K
    counts = [0] * (n + 1)
    total_configs = 0
    for pi in permutations(range(n)):
        pi = list(pi)
        for U in product(range(n), repeat=K):
            f = pi[:]  # copy
            for i in range(K):
                f[i] = U[i]
            T = cyclic_point_count(f)
            counts[T] += 1
            total_configs += 1
    expected = factorial(n) * n ** K
    assert total_configs == expected, (total_configs, expected)
    cum = 0
    cdf = []
    for k in range(n + 1):
        cum += counts[k]
        cdf.append(Fraction(cum, total_configs))
    return counts, cdf, total_configs


if __name__ == "__main__":
    for n in (5, 6):
        t0 = time.time()
        counts, cdf, total = exact_cdf_K5(n)
        elapsed = time.time() - t0
        print(f"n={n} K=5  total configs={total}  elapsed={elapsed:.1f}s")
        print(f"  T-distribution counts (T=0..{n}): {counts}")
        for k in range(n + 1):
            print(f"    k={k}: P(T<=k) = {cdf[k]} = {float(cdf[k]):.12f}")
        sys.stdout.flush()
    print("DONE (independent referee brute force, K=5, n=5,6).")
