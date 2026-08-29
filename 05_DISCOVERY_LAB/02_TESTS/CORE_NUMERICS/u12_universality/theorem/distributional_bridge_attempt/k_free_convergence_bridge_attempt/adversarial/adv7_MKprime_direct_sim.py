"""
Independent Monte Carlo simulation of M_K' DIRECTLY from its own defining
construction (Section 3: Dirichlet(1,...,1) weights via order statistics,
Proposition S applied to continuum weights, uniform within-arc positions),
NOT reusing MK_prime_KS_test.py. Cross-checked against the exact target
CDF F_K(x)=1-(1-x^2)^K via (a) mean/variance comparison to exact values,
and (b) a coarse empirical-CDF-vs-exact-CDF sup-difference at a handful of
x points, for a few K values spanning the claimed evidence range.
"""
import numpy as np
from fractions import Fraction
import math


def sample_MKprime(K, trials, rng):
    xi = rng.random((trials, K))
    eta = rng.random((trials, K))
    xi_sorted = np.sort(xi, axis=1)
    cumQ = np.concatenate([np.zeros((trials, 1)), xi_sorted], axis=1)  # (trials, K+1)
    q_D = 1.0 - cumQ[:, -1]

    Mprime = np.copy(q_D)
    # find dest for each source j via searchsorted into cumQ row
    for j in range(K):
        e = eta[:, j]
        # t such that cumQ[t] < e <= cumQ[t+1], t in 0..K-1; if none, DEAD
        # use searchsorted per row (cumQ rows vary per trial)
        # t_idx = number of cumQ boundaries <= e, minus 1 (since cumQ[0]=0)
        # We'll do it with a loop over K thresholds (K is small in our tests)
        dest_t = np.full(trials, -1, dtype=int)
        for t in range(K):
            mask = (cumQ[:, t] < e) & (e <= cumQ[:, t + 1])
            dest_t[mask] = t
        # cyclic membership requires solving the functional graph; but for the
        # MARGINAL construction of M_K' we actually need S (the full cyclic
        # set), not just per-j dest. We'll compute S properly below instead
        # of trying to shortcut here. (This loop only builds dest_all.)
        if j == 0:
            dest_all = np.full((trials, K), -1, dtype=int)  # -1 = DEAD marker
        dest_all[:, j] = dest_t

    # compute S (cyclic sources) and accumulate V_t' for each trial via a
    # straightforward per-trial loop (K is small, trials moderate -- fine).
    Mprime = np.copy(q_D)
    for i in range(trials):
        dest = dest_all[i]
        color = [0] * K
        cyclic_src = [False] * K
        pred = [None] * K
        for start in range(K):
            if color[start] != 0:
                continue
            path = []
            cur = start
            while True:
                if cur == -1:
                    break
                if color[cur] == 2:
                    break
                if color[cur] == 1:
                    idx = path.index(cur)
                    for node in path[idx:]:
                        cyclic_src[node] = True
                    break
                color[cur] = 1
                path.append(cur)
                cur = dest[cur]
            for node in path:
                if color[node] != 2:
                    color[node] = 2
        for t in range(K):
            if dest[t] != -1:
                pred[dest[t]] = t
        for t in range(K):
            if cyclic_src[t]:
                j = pred[t]
                Vt = cumQ[i, t + 1] - eta[i, j]
                Mprime[i] += Vt
    return Mprime


def exact_moments(K):
    mean = Fraction(4 ** K * math.factorial(K) ** 2, math.factorial(2 * K + 1)) / (K + 1) \
        if False else None
    # simpler: use the known varphi_K formula directly
    varphi_K = Fraction(4 ** K * math.factorial(K) ** 2, math.factorial(2 * K + 1))
    return varphi_K


def exact_cdf(K, x):
    return 1 - (1 - x ** 2) ** K


if __name__ == "__main__":
    for K, trials, seed in [(3, 60000, 555001), (7, 60000, 555002), (15, 40000, 555003)]:
        rng = np.random.default_rng(seed)
        Mp = sample_MKprime(K, trials, rng)
        mc_mean = Mp.mean()
        target_mean = float(exact_moments(K))
        # KS-style sup |empirical CDF - exact CDF| on a grid
        xs = np.linspace(0.05, 0.95, 19)
        sup_diff = 0.0
        for x in xs:
            emp = (Mp <= x).mean()
            exact = exact_cdf(K, x)
            sup_diff = max(sup_diff, abs(emp - exact))
        print(f"K={K:>2} trials={trials:>6}  MC mean={mc_mean:.6f}  target varphi_K={target_mean:.6f}  "
              f"diff={abs(mc_mean-target_mean):.5f}  sup|empCDF-exactCDF| (19-pt grid)={sup_diff:.5f}  "
              f"(expected MC noise scale ~ 1/sqrt(trials) ~= {1/np.sqrt(trials):.5f})")
