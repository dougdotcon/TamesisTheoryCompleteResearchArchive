#!/usr/bin/env python3
"""
Independent Monte Carlo triangulation of Proposicao D4, large n, using
the mandate's reserved seed sub-range 20260926500-20260926799 (grep-
confirmed unused elsewhere in 05_DISCOVERY_LAB/ before use -- see
referee report). Direct simulation of Definition 4 itself (own
np.random.Generator permutation + own i.i.d. targets), NOT the
decomposition/reduced model -- independent of every other script here.
"""
import numpy as np
from fractions import Fraction

def Q_D4(n, k):
    return (-k**6 + 9*k**5 + (4*n**2 - 18*n - 31)*k**4
            + (-16*n**2 + 80*n + 51)*k**3
            + (-6*n**4 + 42*n**3 - 55*n**2 - 120*n - 40)*k**2
            + (6*n**4 - 50*n**3 + 97*n**2 + 70*n + 12)*k
            + 4*n**6 - 30*n**5 + 74*n**4 - 52*n**3 - 30*n**2 - 12*n)

def D4_cdf(n, k):
    if k >= n:
        return Fraction(1)
    if k < 0:
        return Fraction(0)
    num = k * (k + 1) * Q_D4(n, k)
    den = n**5 * (n - 1) * (n - 2) * (n - 3)
    return Fraction(num, den)

def cyclic_count(f, n):
    color = np.zeros(n, dtype=np.int8)
    oncycle = np.zeros(n, dtype=bool)
    order_idx = np.full(n, -1, dtype=np.int64)
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            order_idx[x] = len(path)
            path.append(x)
            x = f[x]
        if color[x] == 1:
            cstart = order_idx[x]
            for y in path[cstart:]:
                oncycle[y] = True
        for y in path:
            color[y] = 2
    return int(oncycle.sum())

def simulate(n, trials, seed):
    rng = np.random.default_rng(seed)
    Ts = np.empty(trials, dtype=np.int64)
    for i in range(trials):
        pi = rng.permutation(n)
        U = rng.integers(0, n, size=4)
        f = pi.copy()
        f[0], f[1], f[2], f[3] = U
        Ts[i] = cyclic_count(f, n)
    return Ts

cells = [
    (100, 200000, 20260926501, 25),
    (100, 200000, 20260926502, 50),
    (100, 200000, 20260926503, 75),
    (500, 30000, 20260926504, 125),
    (500, 30000, 20260926505, 250),
    (500, 30000, 20260926506, 375),
]

print(f"{'n':>5}{'trials':>10}{'k':>7}{'D4 pred':>12}{'MC est':>12}{'s.e.':>10}{'z':>8}")
worst_z = 0
for n, trials, seed, k in cells:
    Ts = simulate(n, trials, seed)
    mc_est = float(np.mean(Ts <= k))
    se = (mc_est * (1 - mc_est) / trials) ** 0.5
    pred = float(D4_cdf(n, k))
    z = (mc_est - pred) / se if se > 0 else 0.0
    worst_z = max(worst_z, abs(z))
    print(f"{n:>5}{trials:>10}{k:>7}{pred:>12.6f}{mc_est:>12.6f}{se:>10.5f}{z:>8.2f}")

print(f"\nworst |z| across all cells: {worst_z:.2f} "
      f"({'consistent, all within ~3 sigma' if worst_z < 3.5 else 'INVESTIGATE'})")
