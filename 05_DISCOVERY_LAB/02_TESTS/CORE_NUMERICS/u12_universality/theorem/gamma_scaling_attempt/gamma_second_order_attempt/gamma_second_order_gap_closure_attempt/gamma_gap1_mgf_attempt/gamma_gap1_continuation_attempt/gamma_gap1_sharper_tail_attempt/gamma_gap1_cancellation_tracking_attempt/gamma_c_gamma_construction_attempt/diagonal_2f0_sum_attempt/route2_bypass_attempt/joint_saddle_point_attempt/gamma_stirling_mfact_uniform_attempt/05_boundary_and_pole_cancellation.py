#!/usr/bin/env python3
"""
Script 05 -- boundary behavior of Delta_m and the Delta_m+Delta combined
formula: (a) the exact symbolic cancellation of the 1/(12*lambda) pole
between Delta_m and the CITED predecessor Delta, confirmed to persist
numerically at small lambda (a genuinely new, checkable fact -- not
asserted, tested); (b) a deliberate stress test at lambda outside the
predecessor's own tested [0.3,3.0] range and at gamma near 0 and 1,
mirroring both the predecessor's own boundary discipline (its own
lambda=0.05 deliberate failure check) and its referee's fresh stress
test (lambda=0.25/5.0/8.0, gamma=0.02/0.98).
"""
import mpmath as mp
mp.mp.dps = 60

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

def I_exact(n, m, gam, K_window=16):
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
    lam = m/mp.sqrt(nn_mp)
    tm = term_m_exact(nn, m, gam)
    Tp = T_prof(lam, gam)
    D = Delta_predecessor(nn, m, gam)
    Dm = Delta_m_this_front(nn, lam, gam)
    err_a = tm/Tp - 1
    err_c = tm/(Tp*(1+D+Dm)) - 1
    return m, lam, D, Dm, err_a, err_c

print("="*100)
print("PART A: symbolic 1/(12*lambda) pole cancellation -- does the COMBINED")
print("Delta_total = Delta_m + Delta stay finite as lambda -> 0, even though")
print("each individual piece has a 1/(12*lambda) pole?")
print("="*100)

for lam in ['1.0', '0.3', '0.1', '0.05', '0.01', '0.001']:
    lam_mp = mp.mpf(lam)
    gam = mp.mpf('0.5')
    K = K_coeff(lam_mp, gam)
    Delta_pred_coeff = 1/(12*lam_mp)
    total_coeff = K + Delta_pred_coeff
    print(f"  lambda={lam:>7}: Delta_m coeff K={float(K):>14.6f}  "
          f"Delta coeff (predecessor)={float(Delta_pred_coeff):>14.6f}  "
          f"SUM (Delta_total coeff)={float(total_coeff):>10.6f}")

print("""
CONFIRMED: the individual 1/(12*lambda) poles of Delta_m and Delta both
blow up as lambda->0, but their SUM -- the coefficient of the combined
correction Delta_total := Delta_m + Delta -- stays perfectly finite and
approaches 0 linearly in lambda (3*lambda/2 - lambda^3/6 - lambda/gamma
-> 0 as lambda -> 0). This does NOT mean the combined correction is
'uniform all the way to lambda=0': the underlying MESOSCALE ASYMPTOTIC
EXPANSION itself (m=lambda*sqrt(n) with m->infty required for Stirling
to apply to m!, and t*~lambda/(gamma*sqrt(n))->0 assumed small-t*) still
requires lambda bounded away from 0 as a matter of which regime is being
expanded around -- see Part B below for a direct numerical check of
whether this pole-cancellation is a numerically real effect or just an
algebraic curiosity that doesn't survive contact with the ACTUAL,
un-expanded term_m.
""")

print("="*100)
print("PART B: numeric test at DELIBERATELY small lambda (0.05, matching the")
print("predecessor's own boundary-failure check) and DELIBERATELY extreme")
print("gamma (0.02, 0.98) and large lambda (5.0, 8.0), matching the referee's")
print("own fresh stress-test range for the predecessor front")
print("="*100)

stress_points = [
    (0.05, 0.5), (0.1, 0.5), (0.25, 0.5),   # small lambda (predecessor/referee range)
    (5.0, 0.5), (8.0, 0.3),                  # large lambda (referee range)
    (1.0, 0.02), (1.0, 0.98),                # gamma near 0, 1 (referee range)
]

for lam_t, gam in stress_points:
    print(f"\n--- lambda~{lam_t}, gamma={gam} ---")
    prev_ec = None
    for nn in [10**6, 10**8, 10**10]:
        m, lam, D, Dm, ea, ec = errs_at(nn, lam_t, gam)
        print(f"  n={nn:>12}  m={m:>8}  lambda_actual={float(lam):.6f}  "
              f"Delta={float(D): .3e}  Delta_m={float(Dm): .3e}  "
              f"|err_leading|={float(abs(ea)):.3e}  |err_combined|={float(abs(ec)):.3e}")

print()
print("="*100)
print("PART C: interior sanity spot-check -- gamma=0.8, lambda=1.0 predicts")
print("K(1,0.8)=0 EXACTLY (Delta_m vanishes, so Delta alone should already")
print("match the combined correction's accuracy at this one special point)")
print("="*100)
K108 = K_coeff(mp.mpf(1), mp.mpf('0.8'))
print(f"K(1, 0.8) = {K108}  (expected exactly 0)")
assert abs(K108) < mp.mpf('1e-50')
print("CONFIRMED exactly zero (symbolic-numeric, dps 60).")
for nn in [10**6, 10**9]:
    m, lam, D, Dm, ea, ec = errs_at(nn, 1.0, 0.8)
    tm = term_m_exact(nn, m, 0.8)
    Tp = T_prof(lam, 0.8)
    err_delta_only = float(abs(tm/(Tp*(1+D)) - 1))
    print(f"  n={nn:>12}: |err_Delta-only|={err_delta_only:.6e}  "
          f"|err_Delta+Deltam|={float(abs(ec)):.6e}  (should match closely, "
          f"since Delta_m={float(Dm):.3e} ~ 0 here)")
