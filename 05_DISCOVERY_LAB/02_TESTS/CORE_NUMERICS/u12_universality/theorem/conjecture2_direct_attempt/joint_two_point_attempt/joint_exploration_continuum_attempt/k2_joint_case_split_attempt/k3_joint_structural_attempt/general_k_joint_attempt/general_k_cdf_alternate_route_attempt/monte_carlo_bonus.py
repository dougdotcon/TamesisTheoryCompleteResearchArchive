"""
Bonus large-(n,K) triangulation: direct Monte Carlo simulation of
Definition 4's actual model (its own random-permutation simulation path,
independent of the composition-simplex / Layer-1 / W-collapse machinery
used everywhere else in this front), compared against the exact
reference engine (reference_Sr_double_sum.unconditional_cdf_via_Sr,
itself independently verified against true brute force and against
D1/D2/D3 -- see reference_Sr_double_sum.log).

Reserved seed block for this front (DISC-DEC-118, wave 25 front (b)):
20260930000-20260930999. Grep-confirmed unused before first use (see
ATTEMPT.md Section "Seeds"). Only this script uses randomness anywhere
in this front.
"""
import numpy as np
from fractions import Fraction
import sys
sys.path.insert(0, '.')
from reference_Sr_double_sum import unconditional_cdf_via_Sr


def simulate_once(n, K, rng):
    pi = rng.permutation(n)
    f = pi.copy()
    targets = rng.integers(0, n, size=K)
    f[:K] = targets
    # cycle detection on functional graph f
    color = np.zeros(n, dtype=np.int8)
    on_cycle = np.zeros(n, dtype=bool)
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
            idx = path.index(x)
            for p in path[idx:]:
                on_cycle[p] = True
        for p in path:
            color[p] = 2
    return int(on_cycle.sum())


def mc_estimate(n, K, k, trials, seed):
    rng = np.random.default_rng(seed)
    count_le = 0
    for _ in range(trials):
        T = simulate_once(n, K, rng)
        if T <= k:
            count_le += 1
    p_hat = count_le / trials
    se = (p_hat * (1 - p_hat) / trials) ** 0.5
    return p_hat, se


if __name__ == "__main__":
    configs = [
        (12, 4, 5, 20000, 20260930001),
        (12, 4, 8, 20000, 20260930002),
        (15, 5, 7, 15000, 20260930003),
        (15, 5, 11, 15000, 20260930004),
        (18, 6, 9, 10000, 20260930005),
        (18, 6, 14, 10000, 20260930006),
        (20, 4, 10, 10000, 20260930007),
        (20, 8, 15, 8000, 20260930008),
    ]
    print("Monte Carlo triangulation, reserved seeds 20260930001-20260930008")
    print("=" * 78)
    for (n, K, k, trials, seed) in configs:
        target = unconditional_cdf_via_Sr(n, K, k)
        target_f = float(target)
        p_hat, se = mc_estimate(n, K, k, trials, seed)
        z = (p_hat - target_f) / se if se > 0 else float('nan')
        print(f"n={n:3d} K={K} k={k:3d} trials={trials:6d} seed={seed}  "
              f"target={target_f:.6f}  MC={p_hat:.6f}  se={se:.5f}  z={z:+.2f}")
    print()
    print("All cells within a few standard errors of the exact target expected;")
    print("triangulation only, not itself proof, per lineage convention.")
