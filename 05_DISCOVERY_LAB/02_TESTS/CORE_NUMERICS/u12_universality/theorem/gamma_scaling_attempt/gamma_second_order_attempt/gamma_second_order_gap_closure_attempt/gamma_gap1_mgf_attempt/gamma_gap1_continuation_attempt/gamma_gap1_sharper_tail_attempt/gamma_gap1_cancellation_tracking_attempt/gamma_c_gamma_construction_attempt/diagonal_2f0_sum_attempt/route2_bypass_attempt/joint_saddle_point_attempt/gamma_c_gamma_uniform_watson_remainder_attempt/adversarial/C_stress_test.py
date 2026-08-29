"""
Independent referee stress test C: fresh (lambda,gamma,n) points NOT in
the front's own grid, including edge cases near/outside the claimed
uniformity boundary [0.3,3.0], gamma close to 0/1, and very large n.

Uses mpmath quadrature (relative-integrand trick: subtract g(t*) before
exponentiating, to avoid the catastrophic-cancellation pitfall flagged in
the dispatch brief) at dps scaled to n so cancellation loss is covered.
"""
import sympy as sp
import mpmath as mp

n, m, gam, t = sp.symbols('n m gamma t', positive=True)
g = m*sp.log(t) + m*sp.log(1-t) + (n-m)*sp.log(1-gam*t)
gpp = sp.diff(g, t, 2)
gppp = sp.diff(g, t, 3)
gpppp = sp.diff(g, t, 4)
t_star_expr = (2*m + gam*n - sp.sqrt(gam**2*n**2 + 4*(1-gam)*m**2)) / (2*gam*(m+n))

g_l = sp.lambdify((n, m, gam, t), g, modules='mpmath')
gpp_l = sp.lambdify((n, m, gam, t), gpp, modules='mpmath')
gppp_l = sp.lambdify((n, m, gam, t), gppp, modules='mpmath')
gpppp_l = sp.lambdify((n, m, gam, t), gpppp, modules='mpmath')
tstar_l = sp.lambdify((n, m, gam), t_star_expr, modules='mpmath')


def exact_integral(n_v, m_v, gam_v, window_mult=14):
    tstar = tstar_l(n_v, m_v, gam_v)
    A = -gpp_l(n_v, m_v, gam_v, tstar)
    width = 1/mp.sqrt(A)
    lo = max(mp.mpf('1e-60'), tstar - window_mult*width)
    hi = min(mp.mpf(1) - mp.mpf('1e-60'), tstar + window_mult*width)
    g_at_star = g_l(n_v, m_v, gam_v, tstar)

    def integrand(tt):
        return mp.e**(g_l(n_v, m_v, gam_v, tt) - g_at_star)

    breakpoints = sorted(set([mp.mpf(0), lo, tstar, hi, mp.mpf(1)]))
    val = mp.quad(integrand, breakpoints)
    return mp.e**g_at_star * val, tstar, A


def laplace_leading(n_v, m_v, gam_v):
    tstar = tstar_l(n_v, m_v, gam_v)
    A = -gpp_l(n_v, m_v, gam_v, tstar)
    g_at_star = g_l(n_v, m_v, gam_v, tstar)
    return mp.e**g_at_star * mp.sqrt(2*mp.pi/A)


def delta_correction(n_v, m_v, gam_v):
    tstar = tstar_l(n_v, m_v, gam_v)
    A = -gpp_l(n_v, m_v, gam_v, tstar)
    g3 = gppp_l(n_v, m_v, gam_v, tstar)
    g4 = gpppp_l(n_v, m_v, gam_v, tstar)
    return g4/(8*A**2) + 5*g3**2/(24*A**3)


tests = [
    # (label, lambda, gamma, n, dps)
    ("just below claimed lower bound lambda=0.25",       mp.mpf('0.25'), mp.mpf('0.5'),  mp.mpf('1e10'), 50),
    ("just above claimed lower bound lambda=0.35",        mp.mpf('0.35'), mp.mpf('0.5'),  mp.mpf('1e10'), 50),
    ("gamma very close to 0 (0.02)",                       mp.mpf('1.0'),  mp.mpf('0.02'), mp.mpf('1e10'), 50),
    ("gamma very close to 1 (0.98)",                       mp.mpf('1.0'),  mp.mpf('0.98'), mp.mpf('1e10'), 60),
    ("lambda beyond claimed upper bound: lambda=5.0",      mp.mpf('5.0'),  mp.mpf('0.5'),  mp.mpf('1e10'), 50),
    ("lambda=8.0, further beyond claimed upper bound",     mp.mpf('8.0'),  mp.mpf('0.5'),  mp.mpf('1e10'), 60),
    ("extreme n=1e12, lambda=1.0",                          mp.mpf('1.0'),  mp.mpf('0.5'),  mp.mpf('1e12'), 60),
    ("extreme n=1e14, lambda=1.0",                          mp.mpf('1.0'),  mp.mpf('0.5'),  mp.mpf('1e14'), 70),
    ("extreme n=1e15, lambda=2.0, gamma=0.7",               mp.mpf('2.0'),  mp.mpf('0.7'),  mp.mpf('1e15'), 80),
    ("lambda=0.3 boundary itself (claimed included), n=1e10", mp.mpf('0.3'), mp.mpf('0.6'), mp.mpf('1e10'), 50),
]

print(f"{'label':55s} {'lambda':>6s} {'gamma':>6s} {'n':>10s} {'Delta':>14s} "
      f"{'rel.err(lead)':>15s} {'rel.err(corr)':>15s} {'sqrtn*Delta':>13s} {'1/(12lam)':>10s}")
for label, lam, gm, n_v, dps in tests:
    mp.mp.dps = dps
    m_v = mp.nint(lam*mp.sqrt(n_v))
    Iexact, tstar, A_v = exact_integral(n_v, m_v, gm)
    I0 = laplace_leading(n_v, m_v, gm)
    Delta_v = delta_correction(n_v, m_v, gm)
    I_corr = I0*(1+Delta_v)
    rel_lead = abs(Iexact/I0 - 1)
    rel_corr = abs(Iexact/I_corr - 1)
    pred_coeff = 1/(12*lam)
    sqrtn_Delta = mp.sqrt(n_v)*Delta_v
    print(f"{label:55s} {float(lam):6.2f} {float(gm):6.2f} {float(n_v):10.1e} "
          f"{float(Delta_v):14.6e} {float(rel_lead):15.6e} {float(rel_corr):15.6e} "
          f"{float(sqrtn_Delta):13.6f} {float(pred_coeff):10.6f}")
