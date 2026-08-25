#!/usr/bin/env python3
"""HOSTILE REFEREE check 4: audits of every numerical inequality used in the
proof chain (Lemmas 2-5), at (n,gamma) pairs the front did NOT use, plus a
high-precision mpmath cross-check of the float64 evaluator.

(A) Lemma 3:  A_k <= e^{-a k} + e^{-g k(k-1)/(4n)}         k=1..K
(B) Lemma 4 upper: A_k <= (1+eps_k) e^{-s(k)},
    eps_k = (k/n) sqrt(k/2) e^{k^3/(4n^2)}
    Lemma 4 lower: A_k >= (1-k^3/n^2) e^{-s(k)}            (k<=n/2)
    s(k) = beta k^2/n - g k/(2n)
(C) Hoeffding scalar:  g e^{l(1-g)} + (1-g) e^{-l g} <= e^{l^2/8}
(D) -ln(1-x) - x <= x^2  on [0, 1/2]
(E) Lemma 5(a) defect: |sum_{k=1}^K e^{-beta k^2/n} - G_n| <= 1
(F) mpmath dps=40 cross-check of the certified float64 evaluator
(G) closed-form constants: (G_n/n)/L_n = sqrt(2/(2-g)) exact;
    Gamma(5/4)/sqrt(2pi); C(gamma) sample values vs ATTEMPT tables
"""
import math
import numpy as np
from ref02_gamma_grid import nphi_certified, lgamma_table

def A_k_array(n, g, K):
    """A_k for k=1..K, float64, windowed binomial (same certified window
    as ref02)."""
    lg = lgamma_table(K+2)
    A = np.zeros(K+1)
    if g >= 1.0:
        for k in range(1, K+1):
            i = np.arange(1, k+1, dtype=np.float64)
            A[k] = math.exp(np.log((n-k+i)/n).sum())
        return A
    lq, l1q = math.log(g), math.log1p(-g)
    for k in range(1, K+1):
        w = int(math.ceil(8.0*math.sqrt(k))) + 1
        mlo = max(0, int(math.floor(g*k)) - w)
        mhi = min(k, int(math.ceil(g*k)) + w)
        m = np.arange(mlo, mhi+1)
        logpmf = lg[k] - lg[m] - lg[k-m] + m*lq + (k-m)*l1q
        i = np.arange(1, mhi+1, dtype=np.float64)
        clog = np.concatenate(([0.0], np.log((n-k+i)/n).cumsum()))
        A[k] = float(np.exp(logpmf + clog[m]).sum())
    return A

def main():
    out = []
    def log(s):
        print(s, flush=True); out.append(s)
    log("=== ref04: proof-inequality audits (hostile referee) ===")
    pairs = [(32768, 0.2), (65536, 0.6), (16384, 1.0), (131072, 0.4)]
    TOL = 1e-11   # absolute tolerance for float roundoff in audits
    for n, g in pairs:
        beta = g*(2.0-g)/2.0
        a = g*(1.0-math.log(2.0))/2.0
        K = math.ceil(math.sqrt((4.0/beta)*n*math.log(n)))
        K = min(K, n//2)
        A = A_k_array(n, g, K)
        k = np.arange(1, K+1, dtype=np.float64)
        s = beta*k*k/n - g*k/(2.0*n)
        # (A) Lemma 3
        lhs3 = A[1:]
        rhs3 = np.exp(-a*k) + np.exp(-g*k*(k-1)/(4.0*n))
        v3 = int(np.sum(lhs3 > rhs3 + TOL))
        # (B) Lemma 4
        eps = (k/n)*np.sqrt(k/2.0)*np.exp(k**3/(4.0*n*n))
        up = (1.0+eps)*np.exp(-s)
        loB = (1.0-k**3/(n*n))*np.exp(-s)
        vU = int(np.sum(A[1:] > up + TOL))
        vL = int(np.sum(A[1:] < loB - TOL))
        # margins
        mU = float(np.min(up - A[1:]))
        mL = float(np.min(A[1:] - loB))
        log(f"[A/B] (n={n}, g={g}) k=1..{K}: Lemma3 violations={v3}, "
            f"Lemma4-upper violations={vU} (min margin {mU:.2e}), "
            f"Lemma4-lower violations={vL} (min margin {mL:.2e})")
    # (C) Hoeffding scalar on a grid finer than the front's (1999 x 12001)
    gg = np.linspace(0.0005, 0.9995, 1999)[:, None]
    ll = np.linspace(-30.0, 30.0, 12001)[None, :]
    lhs = gg*np.exp(ll*(1.0-gg)) + (1.0-gg)*np.exp(-ll*gg)
    rhs = np.exp(ll*ll/8.0)
    vC = int(np.sum(lhs > rhs*(1+1e-13)))
    log(f"[C] Hoeffding scalar 1999x12001 grid: violations={vC}")
    # (D) -ln(1-x)-x <= x^2 on [0,1/2]
    x = np.linspace(0, 0.5, 2000001)
    lhsD = -np.log1p(-x) - x
    vD = int(np.sum(lhsD > x*x + 1e-14))
    margin_at_half = 0.25 - (-math.log1p(-0.5) - 0.5)
    log(f"[D] -ln(1-x)-x<=x^2 on [0,1/2], 2e6+1 pts: violations={vD}; "
        f"margin at x=1/2: {margin_at_half:.6f} (positive => strict)")
    # (E) Lemma 5(a) defect at 8 pairs
    for (n, g) in [(1024,0.1),(1024,0.9),(4096,0.3),(4096,1.0),
                   (16384,0.5),(65536,0.2),(65536,0.7),(262144,0.6)]:
        beta = g*(2.0-g)/2.0
        K = math.ceil(math.sqrt((4.0/beta)*n*math.log(n)))
        k = np.arange(1, K+1, dtype=np.float64)
        Ssum = float(np.exp(-beta*k*k/n).sum())
        G = 0.5*math.sqrt(math.pi*n/beta)
        # add proved tail bound of the dropped k>K part to be fair
        tail = (n/(2.0*beta*K))*math.exp(-beta*K*K/n)
        log(f"[E] (n={n},g={g}): |sum-G_n| = {abs(Ssum-G):.4f} "
            f"(tail<= {tail:.1e})  <=1: {'OK' if abs(Ssum-G)<=1.0 else 'FAIL'}")
    # (F) mpmath cross-check
    try:
        import mpmath as mp
        mp.mp.dps = 40
        for (n, g) in [(4096, 0.3), (4096, 0.7), (16384, 0.5)]:
            Kf = math.ceil(math.sqrt((4.0/g)*n*(40 + 0.5*math.log(n)+5)))
            # exact-precision truncated sum with FULL m range (no window)
            tot = mp.mpf(0)
            for k in range(1, Kf+1):
                q = mp.mpf(g)
                # binomial pmf via recurrence, full range
                pm = (1-q)**k
                P = mp.mpf(1)
                Ak = pm*P  # m=0
                for m in range(1, k+1):
                    pm = pm*q*(k-m+1)/((1-q)*m)
                    P = P*mp.mpf(n-k+m)/n
                    Ak += pm*P
                tot += Ak
            S, budget, _ = nphi_certified(n, g)
            rel = abs(float((tot - S)/tot))
            log(f"[F] mpmath dps=40 (n={n},g={g}): nphi_mp={mp.nstr(tot,20)} "
                f"float64={S:.15e} rel.diff={rel:.2e} "
                f"(certifies roundoff; budget/nphi={budget/S:.1e})")
    except ImportError:
        log("[F] mpmath NOT AVAILABLE -- roundoff certified only by budget")
    # (G) constants
    import fractions
    for g in (0.1, 0.5, 0.9, 1.0):
        beta = g*(2-g)/2
        lhs = math.sqrt(g/beta)
        rhs = math.sqrt(2/(2-g))
        log(f"[G] g={g}: sqrt(g/beta)={lhs:.15f} sqrt(2/(2-g))={rhs:.15f} "
            f"diff={abs(lhs-rhs):.1e}")
    cst = math.gamma(1.25)/math.sqrt(2*math.pi)
    log(f"[G] Gamma(5/4)/sqrt(2pi) = {cst:.10f}; ATTEMPT prints '0.36158...' "
        f"-> {'MATCHES' if abs(cst-0.36158)<5e-5 else 'CHECK'} "
        f"(true value rounds to 0.36160; see report)")
    for g in (0.1, 0.5, 0.9, 0.99, 1.0):
        C = -(2.0/(3.0*math.sqrt(math.pi)))*math.sqrt(g) \
            * (6.0-8.0*g+3.0*g*g)/((2.0-g)**2)
        log(f"[G] C({g}) closed form = {C:.6f}")
    with open(__file__.replace('.py','.log'), 'w') as fh:
        fh.write('\n'.join(out)+'\n')

if __name__ == '__main__':
    main()
