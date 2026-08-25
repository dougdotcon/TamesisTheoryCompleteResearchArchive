#!/usr/bin/env python3
"""
03_highprec_spotcheck.py -- wave 17 front (e), DISC-DEC-072, GAMMA-SCALING-LAW-ATTEMPT

Independent high-precision (mpmath, 40 digits) cross-checks of the float64
pipeline of 02, and two-way checks of the load-bearing asymptotic ingredients:

  (H1) Full-sum mpmath evaluation of phi(n, gamma*n) via Lemma 1 at
       (n=4096, gamma in {0.3, 0.7}) vs the float64 evaluator (same formula,
       independent arithmetic path).
  (H2) phi_inf(c) two ways: (a) (sqrt(pi)/2) c^{-1/2} erf(sqrt(c)) [Theorem 1
       closed form]; (b) direct numerical quadrature of int_0^1 e^{-c t^2} dt
       [Theorem 1 integral]; and check |phi_inf(c) - (sqrt(pi)/2)c^{-1/2}|
       against the PROVED envelope e^{-c}/(2c) (Corollary 4.2, THEOREM.md).
  (H3) Gaussian-sum lemma check: |sum_{k>=1} e^{-beta k^2/n} - (1/2)sqrt(pi n/beta)|
       <= 1 for the (n,beta) used in the proof, several (gamma, n).
  (H4) gamma=1 anchor: R(n,1) = (Q(n)/n)/phi_inf(n) -> sqrt(2), with Q(n) from
       the rising-product recursion (exact rational -> mpmath), n up to 2*10^5.

No randomness anywhere.
"""
import time
from mpmath import mp, mpf, exp as mexp, sqrt as msqrt, erf as merf, pi as mpi, quad, log as mlog

mp.dps = 40
LOG = []
def logp(s):
    print(s, flush=True)
    LOG.append(s)

def phi_mp(n, gamma):
    """Full Lemma-1 sum in mpmath: phi(n, gamma*n)."""
    g = mpf(gamma)
    one = mpf(1)
    tot = mpf(0)
    for k in range(1, n + 1):
        # binomial pmf recursion in m, exact in mp arithmetic
        pmf = (one - g) ** k  # m=0
        P = one
        A = pmf
        for m in range(1, k + 1):
            pmf = pmf * (k - m + 1) / m * g / (one - g) if gamma < 1 else pmf
            P = P * (n - k + m) / n
            A += pmf * P
        tot += A
    return tot / n

def phi_mp_trunc(n, gamma, kmax):
    g = mpf(gamma)
    one = mpf(1)
    tot = mpf(0)
    for k in range(1, kmax + 1):
        pmf = (one - g) ** k
        P = one
        A = pmf
        for m in range(1, k + 1):
            pmf = pmf * (k - m + 1) / m * g / (one - g)
            P = P * (n - k + m) / n
            A += pmf * P
        tot += A
    return tot / n

def main():
    t0 = time.time()
    logp("=== 03_highprec_spotcheck.py ===  (mpmath dps=40; no randomness)")

    # ---------- H1 ----------
    logp("\n[H1] mpmath full sum vs float64 pipeline at n=4096")
    import numpy as np
    from scipy.special import gammaln
    from math import log, log1p

    def phi_float(n, gamma):
        tot = 0.0
        lg, l1g = log(gamma), log1p(-gamma)
        for k in range(1, n + 1):
            m = np.arange(0, k + 1)
            logpmf = (gammaln(k + 1) - gammaln(m + 1) - gammaln(k - m + 1)
                      + m * lg + (k - m) * l1g)
            i = np.arange(1, k + 1)
            logfac = np.concatenate(([0.0], np.cumsum(np.log1p(-(k - i) / n))))
            tot += np.exp(logpmf + logfac).sum()
        return tot / n

    n = 4096
    for gamma in (0.3, 0.7):
        t = time.time()
        hi = phi_mp_trunc(n, gamma, n)   # full k range (kmax=n)
        fl = phi_float(n, gamma)
        rel = abs(fl - float(hi)) / float(hi)
        logp(f"  n={n}, gamma={gamma}: mp={mp.nstr(hi, 18)}  float64={fl:.15e}  "
             f"rel.diff={rel:.2e}  ({time.time()-t:.0f}s)")
        assert rel < 1e-12

    # ---------- H2 ----------
    logp("\n[H2] phi_inf(c) two ways + Corollary 4.2 envelope")
    for gamma, n in [(0.1, 262144), (0.5, 65536), (0.9, 262144)]:
        c = mpf(gamma) * n
        a = msqrt(mpi) / 2 / msqrt(c) * merf(msqrt(c))
        b = quad(lambda t: mexp(-c * t * t), [0, 1])
        lead = msqrt(mpi) / 2 / msqrt(c)
        env = mexp(-c) / (2 * c)
        logp(f"  c={float(c):.1f}: closed-form={mp.nstr(a,16)} quad={mp.nstr(b,16)} "
             f"|diff|={mp.nstr(abs(a-b),3)};  |phi_inf - lead|={mp.nstr(abs(a-lead),3)} "
             f"<= e^-c/(2c)={mp.nstr(env,3)}: {abs(a-lead) <= env}")

    # ---------- H3 ----------
    logp("\n[H3] Gaussian-sum vs integral: |sum - (1/2)sqrt(pi n/beta)| <= 1")
    for gamma in (0.1, 0.5, 0.9, 1.0):
        for n in (256, 65536):
            beta = mpf(gamma) * (2 - mpf(gamma)) / 2
            s = mpf(0)
            k = 1
            while True:
                t_ = mexp(-beta * k * k / n)
                s += t_
                if t_ < mpf(10) ** (-50):
                    break
                k += 1
            I = msqrt(mpi * n / beta) / 2
            logp(f"  gamma={gamma}, n={n}: sum={mp.nstr(s,12)} integral={mp.nstr(I,12)} "
                 f"diff={mp.nstr(s-I,4)} (|.|<=1: {abs(s-I)<=1})")

    # ---------- H4 ----------
    logp("\n[H4] gamma=1 anchor: R(n,1)=(Q(n)/n)/phi_inf(n) -> sqrt(2)")
    tgt = msqrt(2)
    for n in (10**3, 10**4, 10**5, 2 * 10**5):
        term = mpf(1)
        Q = mpf(0)
        for k in range(1, n + 1):
            term *= mpf(n - k + 1) / n
            Q += term
            if term < mpf(10) ** (-45):
                break
        phin = Q / n
        c = mpf(n)
        pinf = msqrt(mpi) / 2 / msqrt(c) * merf(msqrt(c))
        R = phin / pinf
        logp(f"  n={n}: R={mp.nstr(R,12)}  R-sqrt2={mp.nstr(R-tgt,4)}  "
             f"sqrt(n)*(R-sqrt2)={mp.nstr(msqrt(n)*(R-tgt),6)}")

    logp(f"\nTotal time: {time.time()-t0:.1f}s")
    with open(__file__.replace(".py", ".log"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
