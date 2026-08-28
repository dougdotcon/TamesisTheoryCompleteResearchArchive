"""
Section 6 (bonus) of ATTEMPT.md: larger-(n,K) Monte Carlo triangulation.

Direct simulation of Definition 4's actual model (own random-permutation
simulation path, independent of every reduced-model script in this
directory), compared against the exact O(C(n,K))-time reference engine
of `proposition_s_and_conditional_cdf.py` (unconditional_cdf_slow),
itself independently verified against true brute force in that script's
own log. Triangulation only, not proof, per this lineage's convention.

Reserved seed range for this front: 20260927000-20260927999
(DISC-DEC-114, wave 24 front (b); grep-confirmed unused before first use
-- see ATTEMPT.md Section "Seeds").
"""
import numpy as np
from proposition_s_and_conditional_cdf import unconditional_cdf_slow


def simulate(n, K, k, trials, seed):
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(trials):
        pi = rng.permutation(n)
        targets = rng.integers(0, n, size=K)
        f = np.empty(n, dtype=np.int64)
        f[:K] = targets
        f[K:] = pi[K:]
        # cyclic point count via functional-graph cycle detection
        color = np.zeros(n, dtype=np.int8)
        on_cycle = np.zeros(n, dtype=bool)
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
        T = int(on_cycle.sum())
        if T <= k:
            hits += 1
    return hits / trials


if __name__ == "__main__":
    print("Monte Carlo bonus: larger (n,K) triangulation vs the exact")
    print("Section-1 reference engine. Reserved seeds 20260927000-20260927999.")
    print("=" * 78)
    cells = [
        (12, 4, 5, 20000, 20260927001),
        (12, 4, 8, 20000, 20260927002),
        (15, 5, 7, 15000, 20260927003),
        (15, 5, 11, 15000, 20260927004),
        (18, 5, 9, 10000, 20260927005),
        (18, 5, 14, 10000, 20260927006),
    ]
    for n, K, k, trials, seed in cells:
        target = float(unconditional_cdf_slow(n, K, k))
        est = simulate(n, K, k, trials, seed)
        se = (est * (1 - est) / trials) ** 0.5
        z = (est - target) / se if se > 0 else float('nan')
        print(f"n={n:4d} K={K} k={k:3d} trials={trials:6d} seed={seed}  "
              f"target={target:.6f}  MC={est:.6f}  se={se:.5f}  z={z:+.2f}")
    print("=" * 78)
    print("All cells expected within a few standard errors of the exact target")
    print("(triangulation only; the exact machinery in Sections 1-3 is the")
    print("actual evidence for those claims).")
