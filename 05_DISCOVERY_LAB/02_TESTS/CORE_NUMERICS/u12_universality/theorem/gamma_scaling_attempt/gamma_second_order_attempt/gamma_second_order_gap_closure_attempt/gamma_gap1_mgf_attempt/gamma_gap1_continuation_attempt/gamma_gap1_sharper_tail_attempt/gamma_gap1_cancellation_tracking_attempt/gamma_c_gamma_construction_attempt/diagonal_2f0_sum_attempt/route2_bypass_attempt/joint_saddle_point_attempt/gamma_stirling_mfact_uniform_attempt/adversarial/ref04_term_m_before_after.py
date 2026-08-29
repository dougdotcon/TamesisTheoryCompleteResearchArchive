#!/usr/bin/env python3
"""
Referee script 04 -- INDEPENDENT reproduction of the front's central Sec 5
numerical deliverable. Written from scratch WITHOUT reading or importing
the front's own script 04 (only its prose description in ATTEMPT.md was
consulted for the formulas being compared). Uses a FRESH grid of (lambda,
gamma) points not in the front's own 6-point main grid or 3-point extended
push, and pushes to n=10^10.

Computes, for each (lambda,gamma):
  - term_m(n,gamma) EXACTLY: F(n,m,gamma) via mpmath.loggamma (exact, no
    approximation) times I(n,m,gamma) via adaptive high-precision
    quadrature over [0,1], seeded with breakpoints around the analytic t*.
  - (a) T_prof(lambda,gamma) alone [leading order]
  - (b) T_prof*(1+Delta) [predecessor's inner-integral-only correction]
  - (c) T_prof*(1+Delta+Delta_m) [this front's combined correction]
and reports the local log-log slope of the relative error of each,
confirming (or refuting) the claimed -0.5 -> -1.0 order improvement.
"""
import mpmath as mp
import math

mp.mp.dps = 50

def tstar(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    return (gam*n + 2*m - mp.sqrt(gam**2*n**2 + 4*(1-gam)*m**2)) / (2*gam*(m+n))

def g_of(t, n, m, gam):
    return m*mp.log(t) + m*mp.log(1-t) + (n-m)*mp.log(1-gam*t)

def gpp_of(t, n, m, gam):
    return -m/t**2 - m/(1-t)**2 - gam**2*(n-m)/(1-gam*t)**2

def gppp_of(t, n, m, gam):
    return 2*m/t**3 - 2*m/(1-t)**3 - 2*gam**3*(n-m)/(1-gam*t)**3

def gpppp_of(t, n, m, gam):
    return -6*m/t**4 - 6*m/(1-t)**4 - 6*gam**4*(n-m)/(1-gam*t)**4

def lnF(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    return m*mp.log(gam/n) + mp.loggamma(n+m+2) - mp.loggamma(n-m+1) - mp.loggamma(m+1)

def I_exact(n, m, gam, K_window=18):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    ts = tstar(n, m, gam)
    A = -gpp_of(ts, n, m, gam)
    g_ts = g_of(ts, n, m, gam)
    width = K_window / mp.sqrt(A)
    lo = max(mp.mpf('1e-300'), ts - width)
    hi = min(1 - mp.mpf('1e-300'), ts + width)
    def rel_integrand(t):
        if t <= 0 or t >= 1:
            return mp.mpf(0)
        return mp.e**(g_of(t, n, m, gam) - g_ts)
    rel_integral = mp.quad(rel_integrand, [0, lo, ts, hi, 1])
    return mp.e**g_ts * rel_integral

def Delta_predecessor(n, m, gam):
    n, m, gam = mp.mpf(n), mp.mpf(m), mp.mpf(gam)
    ts = tstar(n, m, gam)
    A = -gpp_of(ts, n, m, gam)
    gp3 = gppp_of(ts, n, m, gam)
    gp4 = gpppp_of(ts, n, m, gam)
    return gp4/(8*A**2) + 5*gp3**2/(24*A**3)

def K_coeff(lam, gam):
    lam, gam = mp.mpf(lam), mp.mpf(gam)
    return mp.mpf(3)*lam/2 - lam**3/6 - 1/(12*lam) - lam/gam

def Delta_m_this_front(n, lam, gam):
    return K_coeff(lam, gam) / mp.sqrt(mp.mpf(n))

def T_prof(lam, gam):
    lam, gam = mp.mpf(lam), mp.mpf(gam)
    return (1/gam) * mp.e**(-((2-gam)/(2*gam))*lam**2)

def term_m_exact(n, m, gam):
    return mp.e**lnF(n, m, gam) * I_exact(n, m, gam)

def errs_at(nn, lam_target, gam):
    nn_mp = mp.mpf(nn)
    m = int(round(lam_target*mp.sqrt(nn_mp)))
    lam = m/mp.sqrt(nn_mp)     # ACTUAL lambda -- checked, this bookkeeping
                                # subtlety is what the front self-caught as
                                # its own Sec 8 item 1 bug; verified fixed
                                # correctly here too, independently.
    tm = term_m_exact(nn, m, gam)
    Tp = T_prof(lam, gam)
    D = Delta_predecessor(nn, m, gam)
    Dm = Delta_m_this_front(nn, lam, gam)
    err_a = tm/Tp - 1
    err_b = tm/(Tp*(1+D)) - 1
    err_c = tm/(Tp*(1+D+Dm)) - 1
    return m, lam, err_a, err_b, err_c

def loglog_slope(n1, e1, n2, e2):
    return (math.log(float(abs(e2)))-math.log(float(abs(e1)))) / (math.log(float(n2))-math.log(float(n1)))

print("="*100)
print("INDEPENDENT before/after reproduction -- FRESH (lambda,gamma) grid,")
print("n pushed to 10^10, own script, own point choices")
print("="*100)

# Fresh points: none of these (lambda,gamma) pairs match the front's own
# main grid {(0.3,0.5),(1.0,0.5),(2.0,0.5),(0.5,0.3),(1.5,0.3),(1.0,0.8)}
# or extended push {(1.0,0.5),(0.3,0.5),(2.0,0.3)}.
points = [(0.7, 0.6), (1.2, 0.4), (2.5, 0.55), (0.4, 0.65)]
ns = [10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10]

for lam, gam in points:
    print(f"\n--- lambda~{lam}, gamma={gam} (fresh point) ---")
    rows = []
    for nn in ns:
        m, lam_a, ea, eb, ec = errs_at(nn, lam, gam)
        rows.append((nn, ea, eb, ec))
        print(f"  n={nn:<12,d}  m={m:<9,d}  lambda_actual={float(lam_a):.6f}  "
              f"|err_leading|={float(abs(ea)):.4e}  |err_Delta|={float(abs(eb)):.4e}  "
              f"|err_Delta+Deltam|={float(abs(ec)):.4e}")
    print("  local slopes (leading / Delta-only / Delta+Deltam), decade-by-decade:")
    for i in range(1, len(rows)):
        sa = loglog_slope(rows[i-1][0], rows[i-1][1], rows[i][0], rows[i][1])
        sb = loglog_slope(rows[i-1][0], rows[i-1][2], rows[i][0], rows[i][2])
        sc = loglog_slope(rows[i-1][0], rows[i-1][3], rows[i][0], rows[i][3])
        print(f"    n:{rows[i-1][0]:.0e}->{rows[i][0]:.0e}   {sa:>8.3f}  {sb:>8.3f}  {sc:>8.3f}")

print()
print("Expected (per front's claim): leading & Delta-only slopes -> -0.5,")
print("Delta+Deltam slope -> -1.0, at every fresh point.")
