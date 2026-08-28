"""
Large-n Monte Carlo triangulation, general K, direct simulation of
Definition 4's actual model (own random permutations and iid uniform
targets -- NOT the reduced/arc model, an independent simulation path).
Reserved seed range for this front: 20260904000-20260904999.

Bonus only, not a substitute for the exact symbolic/brute-force results.
"""
import numpy as np
from fractions import Fraction
import sys


def simulate(n, K, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    q1, q2 = n - 2, n - 1
    both_cyclic = 0
    same_cycle = 0
    for _ in range(trials):
        perm = rng.permutation(n)
        f = perm.copy()
        U = rng.integers(0, n, size=K)
        f[:K] = U

        def is_cyclic(start):
            cur = start
            for _ in range(n + 1):
                cur = f[cur]
                if cur == start:
                    return True
            return False

        c1 = is_cyclic(q1)
        c2 = is_cyclic(q2)
        if c1 and c2:
            both_cyclic += 1
            # same final cycle? walk forward from q1 until revisits q1;
            # check whether q2 appears in that orbit.
            cur = q1
            members = set()
            for _ in range(n + 1):
                members.add(cur)
                cur = f[cur]
                if cur == q1:
                    break
            if q2 in members:
                same_cycle += 1
    return both_cyclic, same_cycle, trials


if __name__ == '__main__':
    configs = [
        (4, 200, 200_000, 20260904001),
        (4, 2000, 30_000, 20260904002),
        (4, 5000, 10_000, 20260904003),
        (5, 200, 200_000, 20260904004),
        (5, 2000, 30_000, 20260904005),
        (6, 200, 200_000, 20260904006),
    ]
    print("K | n | trials | P(both cyc) hat | se | z vs 1/(K+1) | "
          "P(same) hat | se | z vs 1/(2(K+1))")
    for K, n, trials, seed in configs:
        bc, sc, T = simulate(n, K, trials, seed)
        p_bc = bc / T
        se_bc = (p_bc * (1 - p_bc) / T) ** 0.5
        target_bc = 1 / (K + 1)
        z_bc = (p_bc - target_bc) / se_bc if se_bc > 0 else float('nan')

        p_sc = sc / T
        se_sc = (p_sc * (1 - p_sc) / T) ** 0.5
        target_sc = 1 / (2 * (K + 1))
        z_sc = (p_sc - target_sc) / se_sc if se_sc > 0 else float('nan')

        print(f"K={K} n={n} trials={T}: P(both)={p_bc:.5f} se={se_bc:.5f} "
              f"z={z_bc:+.2f} (target {target_bc:.5f}) | "
              f"P(same)={p_sc:.5f} se={se_sc:.5f} z={z_sc:+.2f} "
              f"(target {target_sc:.5f})")
