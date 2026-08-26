"""
Independent, from-scratch large-n Monte Carlo triangulation of Definition
4's K=3 model, using this referee's own reserved seed range
(20260893000-20260893999), direct simulation (own random permutations
and reroute targets, not the reduced model).

No .py file from any front in the lineage was read.
"""
import sys
import time
import numpy as np


def simulate(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    both_cyclic = 0
    both_same = 0
    q1, q2 = n - 2, n - 1
    for _ in range(trials):
        pi = rng.permutation(n)
        f = pi.copy()
        U = rng.integers(0, n, size=3)
        f[0], f[1], f[2] = U[0], U[1], U[2]

        # trace q1
        cur = f[q1]
        path = [q1]
        cyc1 = False
        for _ in range(n):
            if cur == q1:
                cyc1 = True
                break
            path.append(cur)
            cur = f[cur]
        if not cyc1:
            continue
        cur = f[q2]
        cyc2 = False
        for _ in range(n):
            if cur == q2:
                cyc2 = True
                break
            cur = f[cur]
        if not cyc2:
            continue
        both_cyclic += 1
        if q2 in path:
            both_same += 1
    return both_cyclic, both_same


if __name__ == '__main__':
    configs = [
        (200, 200_000, 20260893001),
        (2000, 30_000, 20260893002),
        (5000, 10_000, 20260893003),
    ]
    for n, trials, seed in configs:
        t0 = time.time()
        both, same = simulate(n, trials, seed)
        elapsed = time.time() - t0
        p_both = both / trials
        p_same = same / trials
        se_both = (p_both * (1 - p_both) / trials) ** 0.5
        se_same = (p_same * (1 - p_same) / trials) ** 0.5
        z_both = (p_both - 0.25) / se_both if se_both > 0 else float('nan')
        z_same = (p_same - 0.125) / se_same if se_same > 0 else float('nan')
        print(f"n={n:5d} trials={trials:7d} seed={seed}  "
              f"P(both)={p_both:.5f} se={se_both:.5f} z_vs_1/4={z_both:+.2f}  "
              f"P(same)={p_same:.5f} se={se_same:.5f} z_vs_1/8={z_same:+.2f}  "
              f"(elapsed {elapsed:.1f}s)")
