"""
Bonus large-n Monte Carlo triangulation of Proposicao D2 -- NOT a proof
(that is Sections 2-5 of ATTEMPT.md), just a sanity check by directly
simulating Definition 4's K=2 model itself (own random permutations and
reroute targets, not the reduced/decomposition model).

Reserved seeds: 20260923001, 20260923002, 20260923003 (this front's
own range 20260923000-20260923999).
"""
import numpy as np


def simulate_T(n, trials, rng):
    """Direct simulation of Definition 4's K=2 model: uniform random
    permutation of [n], sources fixed at {0,1}, U_0,U_1 i.i.d. Unif([n]),
    count cyclic points of the resulting mapping f."""
    results = np.empty(trials, dtype=np.int64)
    for t in range(trials):
        perm = rng.permutation(n)
        f = perm.copy()
        f[0] = rng.integers(0, n)
        f[1] = rng.integers(0, n)
        # cyclic point count via iterative coloring (O(n), dict lookup
        # instead of list.index to avoid an accidental O(n^2))
        color = np.zeros(n, dtype=np.int8)
        cyclic_count = 0
        for start in range(n):
            if color[start] != 0:
                continue
            path = []
            pos = {}
            x = start
            while color[x] == 0:
                color[x] = 1
                pos[x] = len(path)
                path.append(x)
                x = f[x]
            if color[x] == 1:
                cyclic_count += len(path) - pos[x]
            for y in path:
                color[y] = 2
        results[t] = cyclic_count
    return results


def D2_predict(n, k):
    num = -k * (k + 1) * (k**2 - k - 2 * n**2 + 3 * n)
    den = n**3 * (n - 1)
    return num / den


if __name__ == "__main__":
    seeds = [20260923001, 20260923002, 20260923003]
    cells = [
        (200, 200000, 50), (200, 200000, 100), (200, 200000, 150),
        (2000, 30000, 500), (2000, 30000, 1000), (2000, 30000, 1500),
        (5000, 10000, 1250), (5000, 10000, 2500), (5000, 10000, 3750),
    ]
    print(f"{'n':>6} {'trials':>8} {'k':>6} {'D2 pred':>10} "
          f"{'MC est':>10} {'s.e.':>8} {'z':>7}")
    seed_idx = 0
    for (n, trials, k) in cells:
        seed = seeds[seed_idx % len(seeds)]
        seed_idx += 1
        rng = np.random.default_rng(seed)
        T = simulate_T(n, trials, rng)
        est = np.mean(T <= k)
        se = np.sqrt(est * (1 - est) / trials)
        pred = D2_predict(n, k)
        z = (est - pred) / se if se > 0 else float('nan')
        print(f"{n:6d} {trials:8d} {k:6d} {pred:10.6f} {est:10.6f} "
              f"{se:8.5f} {z:7.2f}")
