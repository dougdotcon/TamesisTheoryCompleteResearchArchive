"""
monte_carlo_k3.py

Large-n Monte Carlo triangulation of P_nn(n,3) -> 1/4 and the K=3 same-cycle
continuum transfer -> 1/8, direct simulation of Definition 4 (K=3), NOT
using the reduced model at all (independent check, own random simulation).

Reserved seeds: 20260892000-20260892999 (this front's own range per its
mandate). Uses numpy.random.SeedSequence-derived generators, one per (n)
cell, all within the reserved range.
"""

import sys
import numpy as np


def simulate_cell(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    q1, q2 = n - 2, n - 1
    both = 0
    same_cycle_both = 0  # both cyclic AND same final cycle
    for _ in range(trials):
        pi = rng.permutation(n)
        f = pi.copy()
        U = rng.integers(0, n, size=3)
        f[0], f[1], f[2] = U[0], U[1], U[2]

        def cyclic_and_rep(x):
            # returns (is_cyclic, representative_min_element_of_cycle) if cyclic
            seen = []
            y = x
            for _ in range(n + 1):
                seen.append(y)
                y = f[y]
                if y == x:
                    return True, min(seen)
                if y in seen:
                    return False, None
            return False, None

        c1, r1 = cyclic_and_rep(q1)
        c2, r2 = cyclic_and_rep(q2)
        if c1 and c2:
            both += 1
            if r1 == r2:
                same_cycle_both += 1
    return both, same_cycle_both, trials


if __name__ == "__main__":
    cells = [
        (200, 200_000, 20260892001),
        (2000, 30_000, 20260892002),
        (5000, 10_000, 20260892003),
    ]
    print("n, trials, both_hat, se_both, z_vs_1/4, same_hat, se_same, z_vs_1/8")
    for n, trials, seed in cells:
        both, same, tot = simulate_cell(n, trials, seed)
        p_both = both / tot
        se_both = (p_both * (1 - p_both) / tot) ** 0.5
        z_both = (p_both - 0.25) / se_both if se_both > 0 else float('nan')
        p_same = same / tot
        se_same = (p_same * (1 - p_same) / tot) ** 0.5
        z_same = (p_same - 0.125) / se_same if se_same > 0 else float('nan')
        print(f"{n}, {trials}, {p_both:.5f}, {se_both:.5f}, {z_both:+.2f}, "
              f"{p_same:.5f}, {se_same:.5f}, {z_same:+.2f}")
