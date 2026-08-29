#!/usr/bin/env python3
"""
Script 02 -- Exact Binomial central-moment machinery for D:=M-gamma*k,
M~Bin(k,gamma), built fresh from the exact cumulant generating function
(NOT imported from any ancestor script), and a fresh re-derivation of
x(D)'s exact cubic coefficients (cited/cross-checked against the
referee-corrected closed forms quoted in the predecessor's ATTEMPT.md
Sec.2 / gamma_gap1_mgf_attempt/ATTEMPT.md Sec.2, but independently
re-derived here, not copied).

Route: cumulants are ADDITIVE over the k i.i.d. Bernoulli(gamma) summands
of M, so kappa_j(D) = k * kappa_tilde_j(gamma) for j>=2 (kappa_1(D)=0
since D is centered), where kappa_tilde_j(gamma) is the j-th cumulant of
a SINGLE Bernoulli(gamma) trial -- k-independent, cheap to compute via
one sympy.series call. Central moments of D are then recovered via the
standard moment<->cumulant recursion (verified below against the two
classical Binomial central-moment formulas already cited elsewhere in
this lineage, mu_3 and mu_4).

This machinery feeds script 03's exact-moment (Cauchy-Schwarz-based)
refinement of the Bulk/Tail Lemma's BULK term.
"""
import time
import pickle
import sympy as sp
from sympy import symbols, Rational, log, exp, series, Poly, binomial, factorial, simplify, expand

LOG = []
def log_(*args):
    s = " ".join(str(a) for a in args)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 02 -- exact Binomial central moments of D via cumulants")
log_("="*78)

t = symbols('t')
g, k, n = symbols('gamma k n', positive=True)

MAXORD = 18   # need up to D^18 for E[x(D)^6], x cubic in D

# ---------------------------------------------------------------------
# Part A. Single-Bernoulli(gamma) cumulants (k-independent), fresh
# ---------------------------------------------------------------------
log_("\n--- Part A: single-Bernoulli(gamma) cumulants (fresh series expansion) ---")
t0 = time.time()
cgf1 = log(1 - g + g*exp(t))
ser = series(cgf1, t, 0, MAXORD+1).removeO()
poly = Poly(ser, t)
kappa_tilde = {0: sp.Integer(0)}
for j in range(1, MAXORD+1):
    c = poly.coeff_monomial(t**j)
    kappa_tilde[j] = expand(factorial(j)*c)
log_(f"  computed in {time.time()-t0:.2f}s")
log_(f"  kappa_tilde_1 = {kappa_tilde[1]}   (must be gamma, the mean)")
log_(f"  kappa_tilde_2 = {kappa_tilde[2]}   (must be gamma(1-gamma), the variance)")
assert simplify(kappa_tilde[1] - g) == 0
assert simplify(kappa_tilde[2] - g*(1-g)) == 0

# ---------------------------------------------------------------------
# Part B. Cumulants of D:=M-gamma*k (additive scaling by k), then
# moment<->cumulant recursion for raw (=central, since mean 0) moments.
# ---------------------------------------------------------------------
log_("\n--- Part B: cumulants and central moments of D=M-gamma*k ---")
kappa_D = {0: sp.Integer(0), 1: sp.Integer(0)}
for j in range(2, MAXORD+1):
    kappa_D[j] = k*kappa_tilde[j]

t0 = time.time()
mu = {0: sp.Integer(1)}
for nn in range(1, MAXORD+1):
    s = sp.Integer(0)
    for m in range(1, nn+1):
        s += binomial(nn-1, m-1) * kappa_D[m] * mu[nn-m]
    mu[nn] = expand(s)
log_(f"  moment recursion computed in {time.time()-t0:.2f}s, orders 0..{MAXORD}")

log_(f"\n  mu_2 = E[D^2] = {mu[2]}")
log_(f"  mu_3 = E[D^3] = {mu[3]}")
log_(f"  mu_4 = E[D^4] = {mu[4]}")

# Cross-check against the two CLASSICAL closed forms already cited
# elsewhere in this lineage (gamma_second_order_attempt/ATTEMPT.md Sec5,
# Gap1 statement): mu_3=k*gamma*(1-gamma)*(1-2*gamma),
# mu_4=k*gamma*(1-gamma)*[1+3*(k-2)*gamma*(1-gamma)].
cited_mu3 = k*g*(1-g)*(1-2*g)
cited_mu4 = k*g*(1-g)*(1+3*(k-2)*g*(1-g))
d3 = simplify(mu[3] - cited_mu3)
d4 = simplify(mu[4] - cited_mu4)
log_(f"\n  Cross-check vs cited classical mu_3: difference = {d3}")
log_(f"  Cross-check vs cited classical mu_4: difference = {d4}")
assert d3 == 0
assert d4 == 0
log_("  BOTH cross-checks PASSED (exact zero symbolic difference).")

# ---------------------------------------------------------------------
# Part C. Brute-force numeric spot-check of the moment machinery
# against literal Binomial pmf summation, for small k -- an independent
# sanity anchor before trusting the recursion for anything downstream.
# ---------------------------------------------------------------------
log_("\n--- Part C: brute-force pmf cross-check (small k, exact Fraction) ---")
from fractions import Fraction
from math import comb

def brute_force_moment(k_val, g_val: Fraction, order):
    total = Fraction(0)
    for m in range(0, k_val+1):
        p = Fraction(comb(k_val, m)) * g_val**m * (1-g_val)**(k_val-m)
        d = Fraction(m) - g_val*k_val
        total += p * d**order
    return total

mismatches = 0
checks = 0
for k_val in [1, 2, 5, 8]:
    for g_num in [1, 3, 7]:
        g_val = Fraction(g_num, 10)
        for order in [2, 3, 4, 6]:
            bf = brute_force_moment(k_val, g_val, order)
            sym_val = mu[order].subs({k: k_val, g: Rational(g_num, 10)})
            sym_val = Fraction(int(sp.fraction(sp.nsimplify(sym_val))[0]),
                                int(sp.fraction(sp.nsimplify(sym_val))[1]))
            checks += 1
            if sym_val != bf:
                mismatches += 1
                log_(f"    MISMATCH k={k_val} gamma={g_val} order={order}: "
                     f"sym={sym_val} bf={bf}")
log_(f"  {checks} brute-force moment checks (k<=8, order in {{2,3,4,6}}), "
     f"{mismatches} mismatches")
assert mismatches == 0

# ---------------------------------------------------------------------
# Part D. Fresh re-derivation of x(D)'s exact cubic coefficients,
# cross-checked against the referee-corrected forms quoted (cited, not
# imported as code) from gamma_gap1_mgf_attempt/ATTEMPT.md Sec.2.
# ---------------------------------------------------------------------
log_("\n--- Part D: fresh re-derivation of x(D) = delta(D) + tau(M)/2 ---")
m_sym = symbols('m', integer=True, nonnegative=True)
i_sym = symbols('i', integer=True, positive=True)

# tau(m) := sum_{i=1}^m ((k-i)/n)^2 -- exact cubic in m, fresh via sympy.summation
tau_m = sp.summation(((k - i_sym)/n)**2, (i_sym, 1, m_sym))
tau_m = sp.expand(tau_m)
log_(f"  tau(m) (fresh, sympy.summation) = {tau_m}")

D_sym = symbols('D')
M_sym = g*k + D_sym
tau_M = expand(tau_m.subs(m_sym, M_sym))

# delta(D) = D*(2*k*(1-gamma)-D-1)/(2n) -- EXACT, cited from the wave-17
# front's own identity sigma_k(m)-sigma_k(x) = (m-x)(2k-m-x-1)/(2n) at
# x=gamma*k (this identity itself is the wave-17 front's PROVED Sec.2
# result, used here as a black box exactly as every descendant front
# has, not re-derived from sigma_k's own definition).
delta_D = D_sym*(2*k*(1-g) - D_sym - 1)/(2*n)

x_D = expand(delta_D + tau_M/2)
x_poly = Poly(x_D, D_sym)
c0 = simplify(x_poly.coeff_monomial(1))
c1 = simplify(x_poly.coeff_monomial(D_sym))
c2 = simplify(x_poly.coeff_monomial(D_sym**2))
c3 = simplify(x_poly.coeff_monomial(D_sym**3))
log_(f"\n  c0 = {c0}")
log_(f"  c1 = {c1}")
log_(f"  c2 = {c2}")
log_(f"  c3 = {c3}")

# Cross-check against the referee-CORRECTED closed forms quoted verbatim
# in gamma_gap1_mgf_attempt/ATTEMPT.md Sec.2 (post-adversarial correction,
# DISC-DEC-089): c3=1/(6n^2); c2=(2*gamma*k-2*k-2*n+1)/(4n^2);
# c1=(1/n^2)*[gamma^2 k^2/2 - gamma k^2 - gamma k n + gamma k/2 + k^2/2
#            + k n - k/2 - n/2 + 1/12];
# c0=(gamma k /(12 n^2))*[2 gamma^2 k^2 - 6 gamma k^2 + 3 gamma k + 6 k^2
#            - 6 k + 1]   (the CORRECTED bracket, no spurious extra gamma).
c3_cited = Rational(1,6)/n**2
c2_cited = (2*g*k - 2*k - 2*n + 1)/(4*n**2)
c1_cited = (1/n**2)*(g**2*k**2/2 - g*k**2 - g*k*n + g*k/2 + k**2/2 + k*n - k/2 - n/2 + Rational(1,12))
c0_cited = (g*k/(12*n**2))*(2*g**2*k**2 - 6*g*k**2 + 3*g*k + 6*k**2 - 6*k + 1)

for name, mine, cited in [('c0', c0, c0_cited), ('c1', c1, c1_cited),
                           ('c2', c2, c2_cited), ('c3', c3, c3_cited)]:
    diff = simplify(mine - cited)
    log_(f"  {name}: fresh - cited(referee-corrected) = {diff}")
    assert diff == 0, f"{name} MISMATCH vs cited referee-corrected form"
log_("  ALL FOUR COEFFICIENTS match the referee-corrected cited forms exactly.")

# ---------------------------------------------------------------------
# Save everything for scripts 03/04.
# ---------------------------------------------------------------------
data = {
    'mu': {str(kk): sp.srepr(v) for kk, v in mu.items()},
    'c0': sp.srepr(c0), 'c1': sp.srepr(c1), 'c2': sp.srepr(c2), 'c3': sp.srepr(c3),
    'tau_m': sp.srepr(tau_m),
}
with open('moment_data.pkl', 'wb') as f:
    pickle.dump(data, f)
log_("\nSaved central moments (order 0..18) and x(D) coefficients to moment_data.pkl")

log_("\nALL CHECKS PASSED.")
with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
