#!/usr/bin/env python3
"""
ADVERSARIAL bonus Monte Carlo triangulation, independent implementation,
direct simulation of THEOREM.md Definition 4's K=3 model itself (own
random permutations and reroute targets, not any reduced model) -- not a
substitute for the exact checks in this directory, just a further
triangulation layer, per this archive's convention.

Uses this referee's own reserved seed range 20260921000-20260921999
(confirmed unused before first use -- see REFEREE_REPORT.md Sec on seeds).
"""

import sys
import numpy as np
from fractions import Fraction


def d3_formula(n, k):
    if k >= n:
        return 1.0
    if k < 0:
        return 0.0
    n_ = Fraction(n)
    k_ = Fraction(k)
    numerator = k_ * (k_ + 1) * (
        k_**4 - 4 * k_**3
        - (3 * n_**2 - 9 * n_ - 5) * k_**2
        + (3 * n_**2 - 11 * n_ - 2) * k_
        + (3 * n_**4 - 12 * n_**3 + 12 * n_**2 + 2 * n_)
    )
    denominator = n_**4 * (n_ - 1) * (n_ - 2)
    return float(numerator / denominator)


def cyclic_count_np(f):
    """f: 1D numpy array, f[i] in [0,n). Returns #cyclic points, O(n)."""
    n = len(f)
    UNVISITED, ON_PATH, DONE = 0, 1, 2
    state = np.zeros(n, dtype=np.int8)
    cyclic = np.zeros(n, dtype=bool)
    for start in range(n):
        if state[start] != UNVISITED:
            continue
        path = []
        x = start
        while state[x] == UNVISITED:
            state[x] = ON_PATH
            path.append(x)
            x = f[x]
        if state[x] == ON_PATH:
            idx = path.index(x)
            for j in range(idx, len(path)):
                cyclic[path[j]] = True
        for p in path:
            state[p] = DONE
    return int(cyclic.sum())


def simulate(n, trials, seed):
    rng = np.random.default_rng(np.random.SeedSequence(seed))
    Ts = np.empty(trials, dtype=np.int64)
    for i in range(trials):
        pi = rng.permutation(n)
        U = rng.integers(0, n, size=3)
        f = pi.copy()
        f[0], f[1], f[2] = U[0], U[1], U[2]
        Ts[i] = cyclic_count_np(f)
    return Ts


def main():
    cells = [
        # (n, trials, k, seed)
        (300, 60000, 75, 20260921001),
        (300, 60000, 150, 20260921002),
        (300, 60000, 225, 20260921003),
        (1000, 20000, 250, 20260921004),
        (1000, 20000, 500, 20260921005),
        (1000, 20000, 750, 20260921006),
    ]
    print(f"{'n':>6} {'trials':>8} {'k':>6} {'D3 pred':>10} {'MC est':>10} "
          f"{'s.e.':>8} {'z':>7}")
    all_within_3sigma = True
    for n, trials, k, seed in cells:
        Ts = simulate(n, trials, seed)
        pred = d3_formula(n, k)
        est = float((Ts <= k).mean())
        se = (pred * (1 - pred) / trials) ** 0.5
        z = (est - pred) / se if se > 0 else float('nan')
        print(f"{n:>6} {trials:>8} {k:>6} {pred:>10.6f} {est:>10.6f} "
              f"{se:>8.5f} {z:>7.2f}")
        if abs(z) > 4:
            all_within_3sigma = False

    print()
    if all_within_3sigma:
        print("All Monte Carlo cells within 4 s.e. of the Proposicao D3 "
              "prediction -- consistent triangulation (own reserved seeds "
              "20260921001-20260921006), not itself proof (the exact "
              "brute-force and reduced-model checks in this directory are "
              "the actual evidence).")
    else:
        print("*** at least one Monte Carlo cell deviates by >4 s.e. -- "
              "investigate. ***")
    return 0 if all_within_3sigma else 1


if __name__ == "__main__":
    sys.exit(main())
