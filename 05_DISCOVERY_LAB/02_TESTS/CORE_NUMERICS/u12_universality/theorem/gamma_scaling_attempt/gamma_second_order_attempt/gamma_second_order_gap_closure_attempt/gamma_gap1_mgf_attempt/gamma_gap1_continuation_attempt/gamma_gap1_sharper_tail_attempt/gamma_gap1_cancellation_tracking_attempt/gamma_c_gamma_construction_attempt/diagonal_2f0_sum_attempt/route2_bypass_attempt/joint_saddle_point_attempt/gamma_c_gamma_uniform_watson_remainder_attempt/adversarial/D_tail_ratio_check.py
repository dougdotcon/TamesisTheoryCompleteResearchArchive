"""
Independent check D: does the curvature ratio |g''(t)|/A stay bounded
away from 0 over the WHOLE domain (0,1), or only within the K<=40
window the front actually tested? This probes whether Sec 5 Step 2's
analytic bound (which implicitly needs A_low=f*A for the ENTIRE tail,
not just the tested window) is truly justified, or whether it's an
unverified extrapolation that happens to not matter because Step 3's
direct quadrature measurement doesn't rely on it.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
n, m, gam, t = sp.symbols('n m gamma t', positive=True)
g = m*sp.log(t) + m*sp.log(1-t) + (n-m)*sp.log(1-gam*t)
gpp = sp.diff(g, t, 2)
t_star_expr = (2*m + gam*n - sp.sqrt(gam**2*n**2 + 4*(1-gam)*m**2)) / (2*gam*(m+n))
gpp_l = sp.lambdify((n, m, gam, t), gpp, modules='mpmath')
tstar_l = sp.lambdify((n, m, gam), t_star_expr, modules='mpmath')

grid = [(mp.mpf('0.3'), mp.mpf('0.3')), (mp.mpf('1.0'), mp.mpf('0.5')), (mp.mpf('3.0'), mp.mpf('0.8')),
        (mp.mpf('0.05'), mp.mpf('0.5')), (mp.mpf('0.3'), mp.mpf('0.02')), (mp.mpf('0.3'), mp.mpf('0.98'))]
n_test = mp.mpf(10)**7

for lam, gm in grid:
    m_v = mp.nint(lam*mp.sqrt(n_test))
    tstar = tstar_l(n_test, m_v, gm)
    A = -gpp_l(n_test, m_v, gm, tstar)
    print(f"lambda={float(lam)} gamma={float(gm)} t*={float(tstar):.6e} A={float(A):.4e}")
    # scan |g''(t)|/A across the WHOLE domain (0,1), not just near t*
    worst = None
    for frac in [mp.mpf(x) for x in
                 ['1e-8','1e-6','1e-4','0.001','0.01','0.05','0.1','0.2','0.3','0.4',
                  '0.5','0.6','0.7','0.8','0.9','0.95','0.99','0.999','0.9999','0.999999']]:
        tt = frac  # scan absolute t in (0,1), not relative to t*
        if tt <= 0 or tt >= 1 or (gm*tt >= 1):
            continue
        val = -gpp_l(n_test, m_v, gm, tt)
        ratio = val/A
        if worst is None or ratio < worst[1]:
            worst = (tt, ratio)
    print(f"   worst |g''(t)|/A over WHOLE (0,1) domain scan: t={float(worst[0]):.6f} ratio={float(worst[1]):.6e}")
    # also check specifically as t->1 (only relevant if gamma*t<1 near t=1, i.e. gamma<1)
    for tt in [mp.mpf('0.999999999'), mp.mpf(1)-mp.mpf('1e-15')]:
        if gm*tt < 1:
            val = -gpp_l(n_test, m_v, gm, tt)
            print(f"     t={float(tt):.12f}  |g''(t)|/A = {float(val/A):.6e}")
    print()
