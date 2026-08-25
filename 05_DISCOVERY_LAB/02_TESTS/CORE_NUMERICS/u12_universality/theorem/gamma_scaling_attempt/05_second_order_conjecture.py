#!/usr/bin/env python3
"""
05_second_order_conjecture.py -- wave 17 front (e), DISC-DEC-072, GAMMA-SCALING-LAW-ATTEMPT

Tests the CONJECTURED second-order constant (ATTEMPT.md SS7.3, heuristically
derived, NOT proved except at gamma=1):

    sqrt(n) * ( phi(n,gamma n)/phi_inf(gamma n) - sqrt(2/(2-gamma)) )
        --> C(gamma) := -(2/(3 sqrt(pi))) * sqrt(gamma) * (6 - 8 gamma + 3 gamma^2) / (2-gamma)^2.

At gamma=1 this equals -2/(3 sqrt(pi)), which IS provable from
Q(n) = sqrt(pi n/2) - 1/3 + O(n^{-1/2})  (Robbins 1955 + FGKP95 theta(n)->1/3,
both already verified in the archive's Estagio 19 lineage).

Method: compute x_n := sqrt(n)*(R_n - target) at n and 2n (float64 evaluator of 02,
certified truncation), then Richardson-extrapolate assuming x_n = C + b/sqrt(n):
    C_est = x_{2n} + (x_{2n} - x_n)/(sqrt(2) - 1).
Report C_est vs C(gamma) at the largest available pair (n, 2n) = (131072, 262144).

No randomness anywhere.
"""
import numpy as np
from scipy.special import gammaln
from math import log, sqrt, pi, exp, log1p, erf
import time

LOG = []
def logp(s):
    print(s, flush=True)
    LOG.append(s)

def A_k_vec(n, g, kmax):
    out = np.empty(kmax + 1)
    out[0] = 1.0
    lg = log(g) if g > 0 else -np.inf
    l1g = log1p(-g) if g < 1 else -np.inf
    for k in range(1, kmax + 1):
        m = np.arange(0, k + 1)
        if 0.0 < g < 1.0:
            logpmf = (gammaln(k + 1) - gammaln(m + 1) - gammaln(k - m + 1)
                      + m * lg + (k - m) * l1g)
        elif g == 1.0:
            logpmf = np.full(k + 1, -np.inf); logpmf[k] = 0.0
        else:
            logpmf = np.full(k + 1, -np.inf); logpmf[0] = 0.0
        i = np.arange(1, k + 1)
        logfac = np.concatenate(([0.0], np.cumsum(np.log1p(-(k - i) / n))))
        out[k] = np.exp(logpmf + logfac).sum()
    return out

def phi_trunc(n, g):
    a_g = g * (1 - log(2)) / 2.0
    Kc = int(sqrt(max(n, 10)))
    while Kc < n:
        T1 = exp(-a_g * (Kc + 1)) / (1 - exp(-a_g))
        gg = g / (4.0 * n)
        T2 = exp(-gg * Kc * Kc) * (1 + 1 / (2 * gg * Kc))
        if (T1 + T2) / n < 1e-18:
            break
        Kc = int(Kc * 1.15) + 1
    Kc = min(Kc, n)
    A = A_k_vec(n, g, Kc)
    return A[1:].sum() / n

def main():
    t0 = time.time()
    logp("=== 05_second_order_conjecture.py ===  (no randomness)")
    logp("x_n := sqrt(n)(R_n - target);  Richardson: C_est = x_2n + (x_2n - x_n)/(sqrt2 - 1)")
    logp(f"{'gamma':>6} {'x_n(131072)':>12} {'x_n(262144)':>12} {'C_est':>10} "
         f"{'C(gamma)':>10} {'|C_est-C|':>10}")
    n1, n2 = 131072, 262144
    worst = 0.0
    for g in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 1.0):
        target = sqrt(2.0 / (2.0 - g))
        xs = []
        for n in (n1, n2):
            phi = phi_trunc(n, g)
            c = g * n
            pinf = 0.5 * sqrt(pi / c) * erf(sqrt(c))
            xs.append(sqrt(n) * (phi / pinf - target))
        C_est = xs[1] + (xs[1] - xs[0]) / (sqrt(2) - 1)
        C_conj = -(2.0 / (3.0 * sqrt(pi))) * sqrt(g) * (6 - 8 * g + 3 * g * g) / (2 - g) ** 2
        dev = abs(C_est - C_conj)
        worst = max(worst, dev / abs(C_conj))
        logp(f"{g:>6} {xs[0]:>12.6f} {xs[1]:>12.6f} {C_est:>10.6f} "
             f"{C_conj:>10.6f} {dev:>10.2e}")
    logp(f"  worst relative deviation of C_est from conjectured C(gamma): {worst:.2e}")
    logp(f"\nTotal time: {time.time()-t0:.1f}s")
    with open(__file__.replace(".py", ".log"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
