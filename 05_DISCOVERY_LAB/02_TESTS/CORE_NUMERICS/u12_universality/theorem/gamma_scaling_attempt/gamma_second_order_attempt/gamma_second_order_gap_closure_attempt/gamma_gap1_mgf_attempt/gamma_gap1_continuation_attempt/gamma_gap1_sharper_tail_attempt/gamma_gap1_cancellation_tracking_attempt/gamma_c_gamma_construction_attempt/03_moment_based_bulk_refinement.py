#!/usr/bin/env python3
"""
Script 03 -- A genuinely different refinement of the Bulk/Tail Lemma's
BULK term, via Lyapunov's inequality + the EXACT 4th moment of x(D)
(script 02's machinery), instead of the deterministic worst-case
exact-cubic-max evaluated at the bulk RADIUS Theta_k (predecessor's own
H_Theta, Estagio 33/49's own construction, cited/reused unchanged for
the TAIL piece).

Motivation (this front's own diagnosis, stated precisely): the
predecessor's own Sec.9 explicitly reports that at the naive margin,
"for 5 of 8 tested gamma, the BULK term (not the Bernstein-tail term)
is what is still >1" -- i.e. the bulk piece, not the tail piece, is
now the binding constraint for most gamma. The predecessor's bulk bound
   H_Theta^3 * e^{H_Theta}
evaluates the cubic x_k(D) at the deterministic worst case D=Theta_k
(the FAR EDGE of the bulk region, at radius C*sqrt(k ln n) -- a radius
that is Theta(sqrt(ln n)) STANDARD DEVIATIONS out, since
std(D)=sqrt(k*gamma*(1-gamma)), growing without bound as n->infty).
But E[|x(D)|^3 * 1_{bulk}] is an EXPECTATION, dominated by TYPICAL D
(order sqrt(k), not order sqrt(k ln n)) -- so bounding it by the value
at the extreme edge Theta_k is provably wasteful by a factor that GROWS
with n (not just a fixed constant, unlike every previous front's own
tightenings, which each removed only a bounded multiplicative factor).

This script's fix: bound the bulk piece via
   E[|x(D)|^3 e^{|x(D)|} 1_{bulk}]
      <= e^{H_Theta} * E[|x(D)|^3 * 1_{bulk}]        (det. bound on e^{...} only)
      <= e^{H_Theta} * E[|x(D)|^3]                    (drop indicator, |x|^3>=0)
      <= e^{H_Theta} * (E[x(D)^4])^{3/4}               (Lyapunov's inequality,
                                                          always valid, no new
                                                          citation beyond
                                                          elementary L^p theory)
using the EXACT (not asymptotic) E[x(D)^4], computed via script 02's
exact moment machinery -- no approximation anywhere in this step.

H_Theta itself (needed for the e^{H_Theta} factor, and unchanged for the
tail piece) is RE-DERIVED fresh here via the same exact-cubic-max method
as Estagio 49/predecessor (cited technique, re-implemented independently,
not imported).
"""
import pickle
import time
import sympy as sp
from sympy import symbols, Rational, sqrt, log as splog, exp as spexp, simplify, expand, Poly, solve

LOG = []
def log_(*args):
    s = " ".join(str(a) for a in args)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 03 -- Lyapunov/exact-4th-moment refinement of the BULK term")
log_("="*78)

with open('moment_data.pkl', 'rb') as f:
    data = pickle.load(f)

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')

c0 = sp.sympify(data['c0'])
c1 = sp.sympify(data['c1'])
c2 = sp.sympify(data['c2'])
c3 = sp.sympify(data['c3'])
mu = {int(kk): sp.sympify(v) for kk, v in data['mu'].items()}

x_D = c0 + c1*D + c2*D**2 + c3*D**3

# ---------------------------------------------------------------------
# Part A. Exact E[x(D)^4], via the moment substitution (D^j -> mu[j]).
# ---------------------------------------------------------------------
log_("\n--- Part A: exact E[x(D)^4] via moment substitution ---")
t0 = time.time()
x4 = expand(x_D**4)
x4_poly = Poly(x4, D)
Ex4 = sp.Integer(0)
for j in range(0, 13):
    coeff = x4_poly.coeff_monomial(D**j) if j > 0 else x4_poly.coeff_monomial(1)
    Ex4 += coeff * mu[j]
Ex4 = expand(Ex4)
log_(f"  computed in {time.time()-t0:.2f}s (degree-12-in-D substitution)")
log_(f"  E[x(D)^4] has {len(Ex4.as_ordered_terms())} terms after expansion "
     f"(not printed in full -- huge rational function of k,n,gamma)")

# Sanity: at gamma=1, D=0 a.s. (M=k a.s.), so E[x(D)^4] should reduce to
# c0(gamma=1)^4 exactly (all D-dependent terms vanish since mu[j]->0 for
# j>=1 when the distribution degenerates to a point mass -- but our
# closed-form mu[j] formulas were derived for GENERIC gamma via the
# cumulant route and do NOT trivially vanish at gamma=1 symbolically
# without simplification, since e.g. mu[2]=k*gamma*(1-gamma) does -> 0
# at gamma=1 correctly). Check this holds.
Ex4_at_gamma1 = simplify(Ex4.subs(g, 1))
c0_at_gamma1 = simplify(c0.subs(g, 1))
log_(f"\n  Sanity check gamma=1: E[x(D)^4]|_{{gamma=1}} = {Ex4_at_gamma1}")
log_(f"                          c0|_{{gamma=1}}^4       = {simplify(c0_at_gamma1**4)}")
diff_sanity = simplify(Ex4_at_gamma1 - c0_at_gamma1**4)
log_(f"  difference: {diff_sanity}")
assert diff_sanity == 0, "gamma=1 degenerate-case sanity check FAILED"
log_("  PASSED (degenerate gamma=1 case confirms the moment substitution is correct).")

# ---------------------------------------------------------------------
# Part B. Brute-force numeric cross-check of E[x(D)^4] against literal
# Binomial pmf summation (independent of the moment-recursion route),
# small (k,n,gamma).
# ---------------------------------------------------------------------
log_("\n--- Part B: brute-force pmf cross-check of E[x(D)^4] ---")
from fractions import Fraction
from math import comb

def brute_force_Ex4(k_val, n_val, g_val: Fraction):
    total = Fraction(0)
    for m in range(0, k_val+1):
        p = Fraction(comb(k_val, m)) * g_val**m * (1-g_val)**(k_val-m)
        Dv = Fraction(m) - g_val*k_val
        c0v = c0.subs({k: k_val, n: n_val, g: sp.Rational(g_val.numerator, g_val.denominator)})
        c1v = c1.subs({k: k_val, n: n_val, g: sp.Rational(g_val.numerator, g_val.denominator)})
        c2v = c2.subs({k: k_val, n: n_val, g: sp.Rational(g_val.numerator, g_val.denominator)})
        c3v = c3.subs({k: k_val, n: n_val, g: sp.Rational(g_val.numerator, g_val.denominator)})
        c0f = Fraction(c0v.p, c0v.q); c1f = Fraction(c1v.p, c1v.q)
        c2f = Fraction(c2v.p, c2v.q); c3f = Fraction(c3v.p, c3v.q)
        xval = c0f + c1f*Dv + c2f*Dv**2 + c3f*Dv**3
        total += p * xval**4
    return total

mismatches_B = 0
checks_B = 0
for (k_val, n_val, g_num) in [(2, 5, 3), (3, 10, 1), (4, 9, 7), (5, 20, 5), (3, 7, 2)]:
    g_val = Fraction(g_num, 10)
    bf = brute_force_Ex4(k_val, n_val, g_val)
    sym_val = Ex4.subs({k: k_val, n: n_val, g: sp.Rational(g_num, 10)})
    sym_val = sp.nsimplify(sym_val)
    sym_frac = Fraction(sp.fraction(sym_val)[0], sp.fraction(sym_val)[1])
    checks_B += 1
    match = (sym_frac == bf)
    log_(f"  k={k_val} n={n_val} gamma={g_val}: brute={bf}  sym={sym_frac}  match={match}")
    if not match:
        mismatches_B += 1
log_(f"  {checks_B} brute-force E[x(D)^4] checks, {mismatches_B} mismatches")
assert mismatches_B == 0

# ---------------------------------------------------------------------
# Part C. Re-derive H_K (exact-cubic-max, cited technique from
# Estagio 49/predecessor, re-implemented fresh) and lambda_tight(gamma),
# for the asymptotic comparison.
# ---------------------------------------------------------------------
log_("\n--- Part C: fresh re-derivation of lambda_tight(gamma) (cited technique) ---")
beta = g*(2-g)/2
K_sym = symbols('K', positive=True)   # K = K_real(n,gamma), substituted later

xK = x_D.subs(D, D).subs(k, K_sym)  # x evaluated with k->K symbolically (still function of D)
xK_expr = c0.subs(k, K_sym) + c1.subs(k, K_sym)*D + c2.subs(k, K_sym)*D**2 + c3.subs(k, K_sym)*D**3

# endpoints of the TRUE support at k=K: D_max=(1-gamma)K, D_min=-gamma*K
D_max_expr = (1-g)*K_sym
D_min_expr = -g*K_sym

# Substitute K^2 = (4/beta) n ln(n) (the wave-17 truncation, cited) to
# get the leading order in ln(n) as n->infty -- same substitution
# Estagio 49 used, re-derived independently here.
lnn = symbols('L', positive=True)  # stands for ln(n)
K_of_n = sqrt((4/beta)*n*lnn)

val_at_Dmax = xK_expr.subs(D, D_max_expr).subs(K_sym, K_of_n)
val_at_Dmin = xK_expr.subs(D, D_min_expr).subs(K_sym, K_of_n)

lim_Dmax = sp.limit(sp.factor(val_at_Dmax)/lnn, n, sp.oo)
lim_Dmin = sp.limit(sp.factor(val_at_Dmin)/lnn, n, sp.oo)
log_(f"  lim x_K(D_max)/ln(n) = {simplify(lim_Dmax)}   [expect 4(1-gamma)^2/(gamma(2-gamma))]")
log_(f"  lim x_K(D_min)/ln(n) = {simplify(lim_Dmin)}   [expect -4, gamma-independent]")

expect_max = 4*(1-g)**2/(g*(2-g))
expect_min = sp.Integer(-4)
d_max = simplify(lim_Dmax - expect_max)
d_min = simplify(lim_Dmin - expect_min)
log_(f"  difference from Estagio-49-cited value (Dmax): {d_max}")
log_(f"  difference from Estagio-49-cited value (Dmin): {d_min}")
assert d_max == 0
assert d_min == 0
log_("  Fresh re-derivation MATCHES Estagio 49's cited lambda_tight(gamma) exactly.")

lambda_tight = sp.Max(4, 4*(1-g)**2/(g*(2-g)))
log_(f"\n  lambda_tight(gamma) = max(4, 4(1-gamma)^2/(gamma(2-gamma)))  [cited, re-confirmed]")

with open('lambda_tight_confirmed.pkl', 'wb') as f:
    pickle.dump({'lambda_tight_piece1': sp.srepr(expect_max), 'checked': True}, f)

log_("\nScript 03 Part A-C: ALL CHECKS PASSED.")
with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written (Part A-C). Continuing to asymptotic comparison in script 04.")
