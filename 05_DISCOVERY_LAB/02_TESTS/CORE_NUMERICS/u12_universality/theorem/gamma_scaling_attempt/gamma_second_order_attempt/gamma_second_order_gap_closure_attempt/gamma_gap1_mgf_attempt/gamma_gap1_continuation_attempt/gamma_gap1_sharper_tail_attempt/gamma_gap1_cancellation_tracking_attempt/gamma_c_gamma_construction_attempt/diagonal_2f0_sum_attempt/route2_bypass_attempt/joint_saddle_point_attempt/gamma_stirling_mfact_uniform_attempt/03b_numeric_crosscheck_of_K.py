#!/usr/bin/env python3
"""
Script 03b -- independent mpmath (NO sympy series machinery) numeric
cross-check of script 03's symbolic result:

  K(lambda,gamma) := coefficient of eps=1/sqrt(n) in
                      B(n,m,gamma) := ln F(n,m,gamma) + ln I_leading(n,m,gamma)
                                       - ln T_prof(lambda,gamma)

  symbolic result (script 03): K(lambda,gamma) = -lambda^3/6 + 3*lambda/2
                                                   - 1/(12*lambda) - lambda/gamma

This script computes B(n,m,gamma) DIRECTLY via mpmath high-precision
arithmetic (mpmath loggamma, exact t* formula, exact -g''(t*)) at large
n, m=round(lambda*sqrt(n)), and fits sqrt(n)*B(n,m,gamma) -> K(lambda,gamma)
as n grows, at several (lambda,gamma) points -- exactly the "independent
mpmath cross-check with no series machinery" methodology the predecessor
front used for its own Delta closed form.
"""
import mpmath as mp

mp.mp.dps = 60

def tstar(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    return (gam*n + 2*m - mp.sqrt(gam**2*n**2 + 4*(1-gam)*m**2)) / (2*gam*(m+n))

def g_of(t, n, m, gam):
    return m*mp.log(t) + m*mp.log(1-t) + (n-m)*mp.log(1-gam*t)

def gpp_of(t, n, m, gam):
    # g(t) = m ln t + m ln(1-t) + (n-m) ln(1-gam t)
    # g'(t) = m/t - m/(1-t) - gam(n-m)/(1-gam t)
    # g''(t) = -m/t^2 - m/(1-t)^2 - gam^2 (n-m)/(1-gam t)^2
    return -m/t**2 - m/(1-t)**2 - gam**2*(n-m)/(1-gam*t)**2

def lnF(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    return m*mp.log(gam/n) + mp.loggamma(n+m+2) - mp.loggamma(n-m+1) - mp.loggamma(m+1)

def lnIlead(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    ts = tstar(n, m, gam)
    A = -gpp_of(ts, n, m, gam)
    return g_of(ts, n, m, gam) + mp.mpf('0.5')*mp.log(2*mp.pi) - mp.mpf('0.5')*mp.log(A)

def lnTprof(lam, gam):
    lam, gam = mp.mpf(lam), mp.mpf(gam)
    return -mp.log(gam) - ((2-gam)/(2*gam))*lam**2

def K_predicted(lam, gam):
    lam, gam = mp.mpf(lam), mp.mpf(gam)
    return -lam**3/6 + mp.mpf(3)*lam/2 - 1/(12*lam) - lam/gam

def B_of(n, lam, gam):
    m = int(mp.nint(lam*mp.sqrt(n)))
    n = mp.mpf(n)
    return lnF(n, m, gam) + lnIlead(n, m, gam) - lnTprof(lam, gam), m

print("="*90)
print("Numeric check: sqrt(n) * B(n,m,gamma) -> K(lambda,gamma) as n->infty")
print("="*90)

points = [(0.3, 0.5), (1.0, 0.5), (2.0, 0.5), (0.5, 0.2), (1.5, 0.8), (3.0, 0.3)]
ns = [10**4, 10**6, 10**8, 10**10, 10**12]

overall = []
for lam, gam in points:
    print(f"\n--- lambda={lam}, gamma={gam}  (K_predicted = {float(K_predicted(lam,gam)):.8f}) ---")
    prev = None
    for nn in ns:
        Bval, m = B_of(nn, lam, gam)
        scaled = mp.sqrt(mp.mpf(nn)) * Bval
        print(f"  n={nn:>14,d}  m={m:>10,d}  sqrt(n)*B = {float(scaled): .8f}")
    Kpred = float(K_predicted(lam, gam))
    Kfit = float(scaled)
    rel = abs(Kfit - Kpred) / (abs(Kpred) + 1e-300)
    overall.append(rel)
    print(f"  -> at largest n, sqrt(n)*B = {Kfit:.8f} vs K_predicted = {Kpred:.8f}"
          f"  (rel diff {rel:.3e})")

print()
print("="*90)
print(f"Worst relative discrepancy across all 6 (lambda,gamma) points at n=10^12: "
      f"{max(overall):.3e}")
assert max(overall) < 1e-4, "MISMATCH between symbolic K and numeric fit -- STOP"
print("CONFIRMED (independent mpmath route, no sympy series machinery):")
print("K(lambda,gamma) = -lambda^3/6 + 3*lambda/2 - 1/(12*lambda) - lambda/gamma")
print("matches the direct high-precision numeric evaluation of")
print("B(n,m,gamma) = ln F + ln I_leading - ln T_prof at every point tested.")
