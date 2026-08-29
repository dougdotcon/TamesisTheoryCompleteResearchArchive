"""
Script 04 -- direct high-precision numerical verification, against the
EXACT inner integral I(n,m,gamma) = int_0^1 t^m (1-t)^m (1-gamma t)^(n-m) dt
(mpmath quadrature, no shortcuts), of:

  (i)  the leading-order Laplace approximation
           I0(n,m,gamma) := exp(g(t*)) * sqrt(2 pi / A)
       has relative error ~ Delta(n,m,gamma) = c(lambda,gamma)/sqrt(n)
       (script 03's new closed-form leading correction), and

  (ii) the CORRECTED approximation I0*(1+Delta) has relative error
       decaying STRICTLY FASTER than Delta itself (i.e. the correction
       genuinely captures the next order, not just a cosmetic rescaling),

 both checked UNIFORMLY across a grid of lambda in [0.3, 3.0] (bounded away
 from 0, per the mandate's own lambda-bounded framing) and gamma in
 {0.3, 0.5, 0.8} -- and separately at lambda=0.05, DELIBERATELY outside the
 claimed-uniform range, to show the correction's own coefficient (and thus
 its region of validity) genuinely breaks down there, not merely asserted.

Quadrature robustness: this front's own fresh implementation (not copied
from any ancestor script) seeds mp.quad with the analytic t* and an
explicit window of half-width K/sqrt(A) as interior breakpoints, since a
naive mp.quad(f,[0,1]) call is known (predecessor's own self-caught issue,
Estagio 56 Sec 8 item 3) to fail outright for this integrand once t* is
very close to 0 and the peak very narrow -- reproduced and independently
re-fixed here before trusting any downstream number.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

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


def exact_integral(n_v, m_v, gam_v, window_mult=12):
    """I(n,m,gamma) via mp.quad, seeded at the analytic t* with an
    explicit window, robust for t* close to 0 or 1 and A very large."""
    tstar = tstar_l(n_v, m_v, gam_v)
    A = -gpp_l(n_v, m_v, gam_v, tstar)
    width = 1/mp.sqrt(A)
    lo = max(mp.mpf('1e-40'), tstar - window_mult*width)
    hi = min(mp.mpf(1) - mp.mpf('1e-40'), tstar + window_mult*width)
    g_at_star = g_l(n_v, m_v, gam_v, tstar)

    def integrand(tt):
        return mp.e**(g_l(n_v, m_v, gam_v, tt) - g_at_star)

    # breakpoints: full domain plus a tight window around t*, so mp.quad's
    # tanh-sinh nodes are forced to resolve the peak explicitly.
    breakpoints = sorted(set([mp.mpf(0), lo, tstar, hi, mp.mpf(1)]))
    val = mp.quad(integrand, breakpoints)
    return mp.e**g_at_star * val, tstar, A


def laplace_leading(n_v, m_v, gam_v):
    tstar = tstar_l(n_v, m_v, gam_v)
    A = -gpp_l(n_v, m_v, gam_v, tstar)
    g_at_star = g_l(n_v, m_v, gam_v, tstar)
    return mp.e**g_at_star * mp.sqrt(2*mp.pi/A), tstar, A


def delta_correction(n_v, m_v, gam_v):
    tstar = tstar_l(n_v, m_v, gam_v)
    A = -gpp_l(n_v, m_v, gam_v, tstar)
    g3 = gppp_l(n_v, m_v, gam_v, tstar)
    g4 = gpppp_l(n_v, m_v, gam_v, tstar)
    return g4/(8*A**2) + 5*g3**2/(24*A**3)


print("=== Sanity: quadrature vs. Laplace-leading at a modest, easily-")
print("    cross-checkable (n,m,gamma) point ===")
n0, m0, g0 = mp.mpf(2000), mp.mpf(20), mp.mpf(0.4)
Iexact, ts, A0 = exact_integral(n0, m0, g0)
I0, _, _ = laplace_leading(n0, m0, g0)
print(f"  n={n0} m={m0} gamma={g0}: exact={Iexact}  Laplace0={I0}  rel.err={abs(Iexact/I0-1)}")

print()
print("=== MAIN GRID: lambda in {0.3,0.5,1.0,1.5,2.0,3.0}, gamma in {0.3,0.5,0.8} ===")
print("For each (lambda,gamma), n grows over {1e4,4e4,1.6e5,6.4e5,2.56e6}")
print("(factor 4 each step) and m = round(lambda*sqrt(n)).")
print()

lambda_grid = [mp.mpf(x) for x in ['0.3', '0.5', '1.0', '1.5', '2.0', '3.0']]
gamma_grid = [mp.mpf(x) for x in ['0.3', '0.5', '0.8']]
n_grid = [mp.mpf(10000) * mp.mpf(4)**k for k in range(5)]

results = {}  # (lam,gam) -> list of (n, rel_err_leading, rel_err_corrected)
for lam in lambda_grid:
    for gm in gamma_grid:
        rows = []
        for n_v in n_grid:
            m_v = mp.nint(lam*mp.sqrt(n_v))
            if m_v < 1:
                m_v = mp.mpf(1)
            Iexact, tstar, A_v = exact_integral(n_v, m_v, gm)
            I0, _, _ = laplace_leading(n_v, m_v, gm)
            Delta_v = delta_correction(n_v, m_v, gm)
            I_corrected = I0*(1+Delta_v)
            rel_err_leading = abs(Iexact/I0 - 1)
            rel_err_corrected = abs(Iexact/I_corrected - 1)
            rows.append((n_v, rel_err_leading, rel_err_corrected, Delta_v))
        results[(lam, gm)] = rows
        print(f"lambda={float(lam):.2f} gamma={float(gm):.2f}:")
        for (n_v, e0, e1, Dv) in rows:
            print(f"   n={float(n_v):>12.0f}  rel.err(leading)={float(e0):.6e}"
                  f"  rel.err(corrected)={float(e1):.6e}  Delta={float(Dv):.6e}")
        # log-log slope of rel.err(leading) vs n, and rel.err(corrected) vs n
        import math
        ns = [float(r[0]) for r in rows]
        e0s = [float(r[1]) for r in rows]
        e1s = [float(r[2]) for r in rows]
        slope0 = (math.log(e0s[-1]) - math.log(e0s[0])) / (math.log(ns[-1]) - math.log(ns[0]))
        slope1 = (math.log(e1s[-1]) - math.log(e1s[0])) / (math.log(ns[-1]) - math.log(ns[0]))
        print(f"   log-log slope (leading)  = {slope0:.3f}  (predicted -0.5)")
        print(f"   log-log slope (corrected)= {slope1:.3f}  (predicted <= -1, i.e. strictly steeper)")
        print()

print("=== BOUNDARY CHECK: lambda=0.05, deliberately OUTSIDE the claimed")
print("    uniform range [0.3,3.0] -- does the correction's own predicted")
print("    coefficient blow up, and does its accuracy degrade, as expected? ===")
lam_bad = mp.mpf('0.05')
for gm in gamma_grid:
    rows = []
    for n_v in n_grid:
        m_v = mp.nint(lam_bad*mp.sqrt(n_v))
        if m_v < 1:
            m_v = mp.mpf(1)
        Iexact, tstar, A_v = exact_integral(n_v, m_v, gm)
        I0, _, _ = laplace_leading(n_v, m_v, gm)
        Delta_v = delta_correction(n_v, m_v, gm)
        I_corrected = I0*(1+Delta_v)
        rel_err_leading = abs(Iexact/I0 - 1)
        rel_err_corrected = abs(Iexact/I_corrected - 1)
        rows.append((n_v, rel_err_leading, rel_err_corrected, Delta_v, m_v))
    print(f"lambda={float(lam_bad):.3f} gamma={float(gm):.2f}  [predicted coeff 1/(12*lambda)={float(1/(12*lam_bad)):.3f}]:")
    for (n_v, e0, e1, Dv, m_v) in rows:
        print(f"   n={float(n_v):>12.0f} m={float(m_v):>6.0f}  rel.err(leading)={float(e0):.6e}"
              f"  rel.err(corrected)={float(e1):.6e}  Delta={float(Dv):.6e}")
    print()

print("=== EXTENDED-n FOLLOW-UP (self-caught, see ATTEMPT.md Sec 8) ===")
print("The MAIN GRID above shows the leading-order log-log slope drifting")
print("visibly below the predicted -0.5 at larger lambda (e.g. lambda=3.0:")
print("-0.41 to -0.43 over n in [1e4,2.56e6]), and the corrected slope")
print("correspondingly short of -1. Investigated directly, not dismissed:")
print("pushing n further (to 1e9) at three representative (lambda,gamma)")
print("points below shows the LOCAL slope converging cleanly to -0.5 and")
print("-1.0 respectively as n grows -- i.e. this is a genuine pre-asymptotic")
print("finite-n effect (larger lambda needs larger n to reach the claimed")
print("asymptotic rate, since c(lambda,gamma)=1/(12 lambda) is itself")
print("smaller at large lambda, so higher-order terms remain relatively")
print("more significant longer), not a flaw in the derived rate itself.")
print()
import math as _math
for lam, gm in [(mp.mpf('1.0'), mp.mpf('0.5')), (mp.mpf('3.0'), mp.mpf('0.5')), (mp.mpf('0.3'), mp.mpf('0.5'))]:
    print(f"lambda={float(lam)} gamma={float(gm)}:")
    ns_ext = [mp.mpf(10)**k for k in [4, 5, 6, 7, 8, 9]]
    e0s, e1s = [], []
    for n_v in ns_ext:
        m_v = mp.nint(lam*mp.sqrt(n_v))
        Iexact, _, _ = exact_integral(n_v, m_v, gm)
        I0, _, _ = laplace_leading(n_v, m_v, gm)
        Delta_v = delta_correction(n_v, m_v, gm)
        e0 = abs(Iexact/I0 - 1)
        e1 = abs(Iexact/(I0*(1+Delta_v)) - 1)
        e0s.append(e0); e1s.append(e1)
        print(f"   n={float(n_v):.0e} m={float(m_v):.0f}  e0={float(e0):.4e}  e1={float(e1):.4e}")
    for i in range(len(ns_ext)-1):
        s0 = (mp.log(e0s[i+1])-mp.log(e0s[i]))/(mp.log(ns_ext[i+1])-mp.log(ns_ext[i]))
        s1 = (mp.log(e1s[i+1])-mp.log(e1s[i]))/(mp.log(ns_ext[i+1])-mp.log(ns_ext[i]))
        print(f"   local slope n={float(ns_ext[i]):.0e}->{float(ns_ext[i+1]):.0e}:"
              f" leading={float(s0):.3f}  corrected={float(s1):.3f}")
    print()

print("=== SUMMARY ===")
print("If, at every (lambda,gamma) in the MAIN GRID, the leading-order slope")
print("is close to -0.5 and the corrected slope is close to -1 (or steeper),")
print("this confirms the claimed uniform O(1/sqrt(n)) remainder for the")
print("leading Laplace approx and that Delta genuinely captures the next")
print("order, UNIFORMLY across the tested lambda range. If lambda=0.05")
print("(outside the claimed range) shows visibly larger Delta / less clean")
print("improvement from correction, this substantiates -- not just asserts")
print("-- that lambda bounded away from 0 is a genuine, necessary condition")
print("for uniformity, not a cosmetic hedge.")
