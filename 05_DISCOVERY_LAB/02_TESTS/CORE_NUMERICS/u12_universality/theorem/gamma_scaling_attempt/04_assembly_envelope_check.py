#!/usr/bin/env python3
"""
04_assembly_envelope_check.py -- wave 17 front (e), DISC-DEC-072, GAMMA-SCALING-LAW-ATTEMPT

End-to-end numerical certificate of the ASSEMBLED sandwich of ATTEMPT.md SS5
(Theorem 1'), with the exact envelope definitions used there, mirrored here
verbatim:

  beta   = gamma(2-gamma)/2,   a_gam = gamma(1-ln2)/2,  G_n = (1/2) sqrt(pi n / beta)
  K      = ceil( sqrt( (4/beta) n ln n ) )        [requires K <= min(n/2, n^{2/3})]
  delta  = exp(gamma K/(2n)) - 1
  J32    = (Gamma(5/4)/2) (n/beta)^{5/4} + 2 (3n/(4beta))^{3/4} e^{-3/4}
  J3     = n^2/(2 beta^2) + 2 (3n/(2beta))^{3/2} e^{-3/2}
  rho    = e^{-a_gam (K+1)}/(1-e^{-a_gam}) + e^{-gamma K^2/(4n)} (1 + 2n/(gamma K))
  T      = (n/(2 beta K)) e^{-beta K^2 / n}

  U  = (1+delta) [ G_n + (e^{1/4}/(sqrt(2) n)) J32 ] + rho
  Lo = G_n - 1 - T - (1+delta) J3 / n^2

  CLAIM (Theorem 1'):  Lo <= n phi(n, gamma n) <= U   whenever K <= min(n/2, n^{2/3}).

Also checks:
  (S)  the scalar Hoeffding inequality used in Lemma 4:
       gamma e^{lam(1-gamma)} + (1-gamma) e^{-lam gamma} <= e^{lam^2/8}
       on a dense (gamma, lam) grid (classical Hoeffding lemma; independent check).
  (Th) reports Theta_n = max(U/G_n - 1, 1 - Lo/G_n) vs the observed |n phi/G_n - 1|.

No randomness anywhere.
"""
import numpy as np
from scipy.special import gammaln
from math import log, sqrt, pi, exp, log1p, ceil, gamma as Gamma
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

def nphi_certified(n, g):
    """n*phi(n, g*n) as an interval [v, v+tb]: v = truncated sum over k<=Kc,
    tb = certified Lemma-3 tail bound on sum_{k>Kc} A_k (independent of the
    envelope's own K).  Kc chosen so tb is negligible; still reported."""
    a_g = g * (1 - log(2)) / 2.0
    Kc = int(sqrt(max(n, 10)))
    while Kc < n:
        T1 = exp(-a_g * (Kc + 1)) / (1 - exp(-a_g))
        gg = g / (4.0 * n)
        T2 = exp(-gg * Kc * Kc) * (1 + 1 / (2 * gg * Kc))
        if (T1 + T2) < 1e-13:
            break
        Kc = int(Kc * 1.15) + 1
    Kc = min(Kc, n)
    if Kc == n:
        tb = 0.0
    else:
        T1 = exp(-a_g * (Kc + 1)) / (1 - exp(-a_g))
        gg = g / (4.0 * n)
        tb = T1 + exp(-gg * Kc * Kc) * (1 + 1 / (2 * gg * Kc))
    A = A_k_vec(n, g, Kc)
    return A[1:].sum(), tb

def envelope(n, g):
    beta = g * (2 - g) / 2.0
    a_g = g * (1 - log(2)) / 2.0
    G = 0.5 * sqrt(pi * n / beta)
    K = ceil(sqrt((4.0 / beta) * n * log(n)))
    ok = (K <= n / 2) and (K <= n ** (2.0 / 3.0))
    delta = exp(g * K / (2.0 * n)) - 1.0
    J32 = (Gamma(1.25) / 2.0) * (n / beta) ** 1.25 + 2.0 * (3.0 * n / (4 * beta)) ** 0.75 * exp(-0.75)
    J3 = n * n / (2 * beta * beta) + 2.0 * (3.0 * n / (2 * beta)) ** 1.5 * exp(-1.5)
    rho = exp(-a_g * (K + 1)) / (1 - exp(-a_g)) + exp(-g * K * K / (4.0 * n)) * (1 + 2.0 * n / (g * K))
    T = (n / (2 * beta * K)) * exp(-beta * K * K / n)
    U = (1 + delta) * (G + (exp(0.25) / (sqrt(2) * n)) * J32) + rho
    Lo = G - 1 - T - (1 + delta) * J3 / (n * n)
    return G, K, ok, U, Lo

def main():
    t0 = time.time()
    logp("=== 04_assembly_envelope_check.py ===  (no randomness)")

    # ---------- sandwich check ----------
    logp("\n[Sandwich] Lo <= n phi(n,gamma n) <= U  (Theorem 1' envelope, verbatim)")
    logp(f"{'gamma':>6} {'n':>7} {'K':>6} {'cond':>5} {'Lo/G':>9} {'nphi/G':>9} "
         f"{'U/G':>9} {'holds':>6} {'Theta_n':>9} {'|nphi/G-1|':>10} {'tailbnd':>9}")
    all_ok = True
    for g in (0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
        for n in (1024, 4096, 16384, 65536, 262144):
            G, K, ok, U, Lo = envelope(n, g)
            npv, tb = nphi_certified(n, g)
            holds = (Lo <= npv) and (npv + tb <= U)
            Theta = max(U / G - 1, 1 - Lo / G)
            if ok:
                all_ok &= holds
            logp(f"{g:>6} {n:>7} {K:>6} {str(ok):>5} {Lo/G:>9.5f} {npv/G:>9.5f} "
                 f"{U/G:>9.5f} {str(holds):>6} {Theta:>9.5f} {abs(npv/G-1):>10.6f} {tb:>9.1e}")
    logp(f"  All sandwich checks hold (where side condition K<=min(n/2,n^(2/3)) met): {all_ok}")

    # ---------- scalar Hoeffding ----------
    logp("\n[S] scalar Hoeffding: g e^(l(1-g)) + (1-g) e^(-l g) <= e^(l^2/8)")
    gs = np.linspace(0.001, 0.999, 999)
    ls = np.linspace(-30, 30, 6001)
    Gm, Lm = np.meshgrid(gs, ls)
    lhs = Gm * np.exp(Lm * (1 - Gm)) + (1 - Gm) * np.exp(-Lm * Gm)
    rhs = np.exp(Lm * Lm / 8.0)
    viol = int((lhs > rhs * (1 + 1e-12)).sum())
    logp(f"  grid 999 x 6001 = {lhs.size} points, violations: {viol}")

    logp(f"\nTotal time: {time.time()-t0:.1f}s")
    with open(__file__.replace(".py", ".log"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
