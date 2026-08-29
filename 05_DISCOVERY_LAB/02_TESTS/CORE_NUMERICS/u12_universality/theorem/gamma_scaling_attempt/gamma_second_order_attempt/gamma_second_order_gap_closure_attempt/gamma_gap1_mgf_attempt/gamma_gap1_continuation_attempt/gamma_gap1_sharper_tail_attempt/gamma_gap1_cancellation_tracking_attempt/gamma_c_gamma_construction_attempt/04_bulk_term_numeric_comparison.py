#!/usr/bin/env python3
"""
Script 04 -- Numeric (mpmath, high precision) comparison of the
predecessor's deterministic-worst-case BULK term H_Theta^3 against this
front's Lyapunov/exact-4th-moment BULK term (E[x(D)^4])^{3/4}, at K=
K_real(n,gamma) (predecessor's own tight truncation, cited, re-derived),
across the SAME 8 sample gamma the whole lineage has used since Estagio
36 for direct comparability.

Everything here is built fresh from script 02/03's exact symbolic
machinery (c0..c3, E[x(D)^4]) -- no ancestor .py file imported.
"""
import pickle
import time
import mpmath as mp
import sympy as sp
from sympy import symbols, Rational, sqrt as spsqrt

mp.mp.dps = 60

LOG = []
def log_(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 04 -- numeric comparison: H_Theta^3 (predecessor) vs")
log_("            (E[x(D)^4])^{3/4} (this front), at K=K_real(n,gamma)")
log_("="*78)

with open('moment_data.pkl', 'rb') as f:
    data = pickle.load(f)

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')
c0 = sp.sympify(data['c0']); c1 = sp.sympify(data['c1'])
c2 = sp.sympify(data['c2']); c3 = sp.sympify(data['c3'])
mu = {int(kk): sp.sympify(v) for kk, v in data['mu'].items()}

x_D = c0 + c1*D + c2*D**2 + c3*D**3

from sympy import Poly, expand
x4 = expand(x_D**4)
x4_poly = Poly(x4, D)
Ex4 = sp.Integer(0)
for j in range(0, 13):
    coeff = x4_poly.coeff_monomial(D**j) if j > 0 else x4_poly.coeff_monomial(1)
    Ex4 += coeff * mu[j]
Ex4 = expand(Ex4)

# lambdify for fast high-precision mpmath evaluation
Ex4_f = sp.lambdify((k, n, g), Ex4, modules='mpmath')
c0_f = sp.lambdify((k, n, g), c0, modules='mpmath')
c1_f = sp.lambdify((k, n, g), c1, modules='mpmath')
c2_f = sp.lambdify((k, n, g), c2, modules='mpmath')
c3_f = sp.lambdify((k, n, g), c3, modules='mpmath')

def beta_of(gamma):
    return gamma*(2-gamma)/2

def K_real(n_val, gamma):
    """Predecessor's own tight truncation (Estagio 49/predecessor Sec.6),
    cited, re-derived independently: K_real(n,gamma):=sqrt(4 n ln n / beta)+1."""
    b = beta_of(gamma)
    return mp.sqrt(4*n_val*mp.log(n_val)/b) + 1

def exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi):
    """Exact max of |x_k(D)| over D in [Dlo,Dhi], via endpoints + any
    interior critical point of x_k'(D)=c1+2c2 D+3c3 D^2=0 (quadratic
    formula, closed form) -- re-implementing the predecessor's own
    exact-cubic-max METHOD fresh (cited technique), not importing code."""
    c0v = c0_f(k_val, n_val, gamma); c1v = c1_f(k_val, n_val, gamma)
    c2v = c2_f(k_val, n_val, gamma); c3v = c3_f(k_val, n_val, gamma)
    def xval(Dv):
        return c0v + c1v*Dv + c2v*Dv**2 + c3v*Dv**3
    candidates = [Dlo, Dhi]
    # critical points: 3*c3*D^2 + 2*c2*D + c1 = 0
    a_, b_, c_ = 3*c3v, 2*c2v, c1v
    if abs(a_) > mp.mpf('1e-80'):
        disc = b_**2 - 4*a_*c_
        if disc >= 0:
            sq = mp.sqrt(disc)
            for root in [(-b_+sq)/(2*a_), (-b_-sq)/(2*a_)]:
                if Dlo <= root <= Dhi:
                    candidates.append(root)
    vals = [abs(xval(Dv)) for Dv in candidates]
    return max(vals)

GAMMAS = [mp.mpf('0.99'), mp.mpf('0.9'), mp.mpf('0.7'), mp.mpf('0.5'),
          mp.mpf('0.3'), mp.mpf('0.1'), mp.mpf('0.05'), mp.mpf('0.01')]
C_MARGIN = mp.mpf('1.05')   # illustrative split constant, matching predecessor's typical range

N_TEST = [mp.mpf(10)**e for e in [10, 20, 30, 40, 50, 60, 80, 100]]

log_("\n--- H_Theta^3 (predecessor, deterministic worst-case) vs")
log_("    (E[x(D)^4])^{3/4} (this front, Lyapunov/exact-4th-moment), same K_real, C=1.05 ---")
log_(f"{'gamma':>6} {'n':>8} {'H_Theta^3':>16} {'(E[x^4])^(3/4)':>18} {'ratio old/new':>15}")

results = []
for gamma in GAMMAS:
    for n_val in N_TEST:
        beta = beta_of(gamma)
        K = K_real(n_val, gamma)
        Theta_K = C_MARGIN*mp.sqrt(K*mp.log(n_val))
        Dlo = max(-gamma*K, -Theta_K)
        Dhi = min((1-gamma)*K, Theta_K)
        if Dlo >= Dhi:
            continue
        H_Theta = exact_cubic_max_abs(K, n_val, gamma, Dlo, Dhi)
        Ex4_val = Ex4_f(K, n_val, gamma)
        if Ex4_val < 0:
            Ex4_val = mp.mpf(0)
        new_bulk_base = Ex4_val**mp.mpf('0.75')
        old_bulk_base = H_Theta**3
        ratio = old_bulk_base/new_bulk_base if new_bulk_base > 0 else mp.inf
        results.append((gamma, n_val, old_bulk_base, new_bulk_base, ratio))

# print a representative subset (largest n for each gamma, to see asymptotic behavior)
for gamma in GAMMAS:
    rows = [r for r in results if r[0] == gamma]
    row = rows[-1]  # largest n tested
    log_(f"{float(row[0]):>6.2f} {mp.nstr(row[1],4):>8} {mp.nstr(row[2],6):>16} "
         f"{mp.nstr(row[3],6):>18} {mp.nstr(row[4],6):>15}")

log_("\n--- Full table (all n tested), gamma=0.5 (representative) ---")
for r in results:
    if r[0] == mp.mpf('0.5'):
        log_(f"  n=10^{int(mp.log10(r[1]))}: H_Theta^3={mp.nstr(r[2],8)}  "
             f"(E[x^4])^0.75={mp.nstr(r[3],8)}  ratio={mp.nstr(r[4],8)}")

log_("\n--- Does the ratio (old/new) GROW with n, as the analytic estimate")
log_("    predicts (order (ln n)^1.5, unbounded)? Check via fitted exponent")
log_("    of ratio vs ln(ln(n)) [since predicted ratio ~ C^3 (ln n)^1.5]. ---")
for gamma in GAMMAS:
    rows = [r for r in results if r[0] == gamma]
    if len(rows) < 2:
        continue
    n1, r1 = rows[0][1], rows[0][4]
    n2, r2 = rows[-1][1], rows[-1][4]
    # ratio ~ (ln n)^1.5  =>  ln(ratio) ~ 1.5 ln(ln n)
    lr1, lr2 = mp.log(r1), mp.log(r2)
    lnln1, lnln2 = mp.log(mp.log(n1)), mp.log(mp.log(n2))
    if lnln2 != lnln1:
        fitted_exp = (lr2-lr1)/(lnln2-lnln1)
    else:
        fitted_exp = mp.mpf('nan')
    log_(f"  gamma={float(gamma):.2f}: ratio(n={mp.nstr(n1,3)})={mp.nstr(r1,5)}  "
         f"ratio(n={mp.nstr(n2,3)})={mp.nstr(r2,5)}  fitted ln-ln exponent={mp.nstr(fitted_exp,4)} "
         f"[predicted ~1.5]")

with open('bulk_comparison_results.pkl', 'wb') as f:
    pickle.dump([(str(a), str(b), str(c), str(d), str(e)) for a,b,c,d,e in results], f)

log_("\nDone. See log for the full quantitative comparison.")
with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
