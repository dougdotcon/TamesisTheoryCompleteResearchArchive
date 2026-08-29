#!/usr/bin/env python3
"""
Script 06 -- Hard sanity checks on script 05's hybrid bound, BEFORE
trusting its striking n_0(gamma) reduction:

  (A) R_k^bound (this front's Lyapunov-based bulk formula, pointwise,
      i.e. (1/6)(E[x(D)^4])^{3/4} without the e^{H_Theta}/bulk-vs-tail
      split) vs R_k^exact := (1/6) E_M[|x(D)|^3 e^{|x(D)|}], computed by
      DIRECT summation over the true Binomial pmf (mpmath, no shortcuts)
      -- must have R_k^exact <= R_k^bound at every tested point, or the
      whole construction is unsound.

  (B) Term-by-term breakdown of W_hybrid at script 05's own found n_0(
      gamma) for a representative subset of gamma, to see which term
      (bulk/tail/small-k) is binding and confirm no term is a spurious
      near-zero (a classic sign of a silent bug elsewhere cancelling
      it out).

  (C) Direct re-verification that bulk_term_new(K,n,gamma,Theta_K) is
      indeed an upper bound on E[|x(D)|^3 e^{|x(D)|} * 1_{|D|<=Theta_K}],
      via brute-force exact pmf summation restricted to the bulk event,
      at moderate (k,n) where this is computationally feasible.
"""
import pickle
import time
import mpmath as mp
import sympy as sp
from sympy import symbols, Poly, expand
from math import comb

mp.mp.dps = 80

LOG = []
def log_(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 06 -- hard sanity checks on the hybrid bound")
log_("="*78)

with open('moment_data.pkl', 'rb') as f:
    data = pickle.load(f)

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')
c0 = sp.sympify(data['c0']); c1 = sp.sympify(data['c1'])
c2 = sp.sympify(data['c2']); c3 = sp.sympify(data['c3'])
mu = {int(kk): sp.sympify(v) for kk, v in data['mu'].items()}
x_D = c0 + c1*D + c2*D**2 + c3*D**3
x4 = expand(x_D**4)
x4_poly = Poly(x4, D)
Ex4 = sp.Integer(0)
for j in range(0, 13):
    coeff = x4_poly.coeff_monomial(D**j) if j > 0 else x4_poly.coeff_monomial(1)
    Ex4 += coeff * mu[j]
Ex4 = expand(Ex4)

Ex4_f = sp.lambdify((k, n, g), Ex4, modules='mpmath')
c0_f = sp.lambdify((k, n, g), c0, modules='mpmath')
c1_f = sp.lambdify((k, n, g), c1, modules='mpmath')
c2_f = sp.lambdify((k, n, g), c2, modules='mpmath')
c3_f = sp.lambdify((k, n, g), c3, modules='mpmath')

def beta_of(gamma): return gamma*(2-gamma)/2
def sigma2_of(gamma): return gamma*(1-gamma)
def lambda_tight_of(gamma):
    return max(mp.mpf(4), 4*(1-gamma)**2/(gamma*(2-gamma)))
def K_real(n_val, gamma):
    b = beta_of(gamma)
    return mp.sqrt(4*n_val*mp.log(n_val)/b) + 1

def exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi):
    c0v = c0_f(k_val, n_val, gamma); c1v = c1_f(k_val, n_val, gamma)
    c2v = c2_f(k_val, n_val, gamma); c3v = c3_f(k_val, n_val, gamma)
    def xval(Dv): return c0v + c1v*Dv + c2v*Dv**2 + c3v*Dv**3
    candidates = [Dlo, Dhi]
    a_, b_, c_ = 3*c3v, 2*c2v, c1v
    if abs(a_) > mp.mpf('1e-90'):
        disc = b_**2 - 4*a_*c_
        if disc >= 0:
            sq = mp.sqrt(disc)
            for root in [(-b_+sq)/(2*a_), (-b_-sq)/(2*a_)]:
                if Dlo <= root <= Dhi:
                    candidates.append(root)
    return max(abs(xval(Dv)) for Dv in candidates)

def x_val_mp(k_val, n_val, gamma, Dv):
    return (c0_f(k_val,n_val,gamma) + c1_f(k_val,n_val,gamma)*Dv
            + c2_f(k_val,n_val,gamma)*Dv**2 + c3_f(k_val,n_val,gamma)*Dv**3)

def R_k_exact(k_val, n_val, gamma):
    """(1/6) E_M[|x(D)|^3 e^{|x(D)|}], DIRECT exact pmf summation, no shortcuts."""
    total = mp.mpf(0)
    for m in range(0, k_val+1):
        p = mp.binomial(k_val, m) * mp.mpf(gamma)**m * mp.mpf(1-gamma)**(k_val-m)
        Dv = mp.mpf(m) - gamma*k_val
        xv = x_val_mp(k_val, n_val, gamma, Dv)
        total += p * abs(xv)**3 * mp.e**abs(xv)
    return total/6

def R_k_bulk_exact_restricted(k_val, n_val, gamma, Theta):
    """(1/6) E_M[|x(D)|^3 e^{|x(D)|} * 1_{|D|<=Theta}], DIRECT pmf summation."""
    total = mp.mpf(0)
    for m in range(0, k_val+1):
        Dv = mp.mpf(m) - gamma*k_val
        if abs(Dv) > Theta:
            continue
        p = mp.binomial(k_val, m) * mp.mpf(gamma)**m * mp.mpf(1-gamma)**(k_val-m)
        xv = x_val_mp(k_val, n_val, gamma, Dv)
        total += p * abs(xv)**3 * mp.e**abs(xv)
    return total/6

def bulk_term_new(k_val, n_val, gamma, Theta_k):
    Dlo = max(-gamma*k_val, -Theta_k); Dhi = min((1-gamma)*k_val, Theta_k)
    H_Theta = exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi)
    Ex4_val = Ex4_f(k_val, n_val, gamma)
    if Ex4_val < 0: Ex4_val = mp.mpf(0)
    return mp.mpf('1')/6 * mp.e**H_Theta * Ex4_val**mp.mpf('0.75')

# =======================================================================
# Check (A): R_k^exact <= R_k^bound (unrestricted pointwise Lyapunov
# bound, i.e. (1/6)*e^{H_full}*(E[x(D)^4])^{3/4} with H_full the exact
# max over the FULL true support -- the "no bulk/tail split" comparison)
# =======================================================================
log_("\n--- Check (A): R_k^exact vs pointwise Lyapunov bound R_k^bound ---")
log_("  (moderate k,n so direct pmf summation is feasible)")
viol_A = 0
checks_A = 0
for k_val in [10, 30, 80]:
    for n_val in [1000, 20000]:
        for gamma_f in [mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.8')]:
            Dlo_full = -gamma_f*k_val; Dhi_full = (1-gamma_f)*k_val
            H_full = exact_cubic_max_abs(k_val, n_val, gamma_f, Dlo_full, Dhi_full)
            Ex4v = Ex4_f(k_val, n_val, gamma_f)
            if Ex4v < 0: Ex4v = mp.mpf(0)
            R_bound = mp.mpf('1')/6 * mp.e**H_full * Ex4v**mp.mpf('0.75')
            R_exact = R_k_exact(k_val, n_val, gamma_f)
            checks_A += 1
            ok = (R_exact <= R_bound*(1+mp.mpf('1e-20')))
            if not ok:
                viol_A += 1
                log_(f"    VIOLATION k={k_val} n={n_val} gamma={float(gamma_f)}: "
                     f"exact={mp.nstr(R_exact,10)} > bound={mp.nstr(R_bound,10)}")
            else:
                log_(f"    OK k={k_val:>3} n={n_val:>6} gamma={float(gamma_f):.1f}: "
                     f"R_exact={mp.nstr(R_exact,6):>14}  R_bound={mp.nstr(R_bound,6):>14}  "
                     f"ratio(bound/exact)={mp.nstr(R_bound/R_exact if R_exact>0 else mp.inf,6)}")
log_(f"  TOTAL: {checks_A} checks, {viol_A} violations")
assert viol_A == 0, "Lyapunov bound VIOLATED against exact pmf -- construction is UNSOUND"

# =======================================================================
# Check (B): the BULK-restricted (|D|<=Theta) exact quantity vs
# bulk_term_new's claimed bound, at moderate scale.
# =======================================================================
log_("\n--- Check (B): bulk-restricted R_k^exact vs bulk_term_new bound ---")
viol_B = 0
checks_B = 0
for k_val in [20, 60]:
    for n_val in [5000, 50000]:
        for gamma_f in [mp.mpf('0.3'), mp.mpf('0.6')]:
            Theta = mp.mpf('1.05')*mp.sqrt(k_val*mp.log(n_val))
            restricted_exact = R_k_bulk_exact_restricted(k_val, n_val, gamma_f, Theta)
            bound = bulk_term_new(k_val, n_val, gamma_f, Theta)
            checks_B += 1
            ok = restricted_exact <= bound*(1+mp.mpf('1e-20'))
            status = "OK" if ok else "VIOLATION"
            if not ok: viol_B += 1
            log_(f"    {status} k={k_val:>3} n={n_val:>6} gamma={float(gamma_f):.1f} "
                 f"Theta={mp.nstr(Theta,5)}: restricted_exact={mp.nstr(restricted_exact,6)} "
                 f"bound={mp.nstr(bound,6)}")
log_(f"  TOTAL: {checks_B} checks, {viol_B} violations")
assert viol_B == 0

# =======================================================================
# Check (C): term-by-term breakdown of W_hybrid at script 05's found
# n_0(gamma), reusing script 05's exact assembly logic (re-implemented
# here, not imported, to keep this script standalone/independently
# runnable -- values will match script 05's own internal numbers).
# =======================================================================
log_("\n--- Check (C): term-by-term breakdown at the found n_0(gamma) ---")

def tail_term_new(K_val, n_val, gamma, C, a_slack):
    Dlo = -gamma*K_val; Dhi = (1-gamma)*K_val
    H_K = exact_cubic_max_abs(K_val, n_val, gamma, Dlo, Dhi)
    sigma2 = sigma2_of(gamma)
    exponent = -(C**2)/((2+a_slack)*sigma2) * mp.log(n_val)
    prob_factor = 2*mp.e**exponent
    return mp.mpf('1')/6 * prob_factor * H_K**3 * mp.e**H_K

def k2_threshold(n_val, gamma, C, a_slack):
    sigma2 = sigma2_of(gamma)
    return (2*C/(3*a_slack*sigma2))**2 * mp.log(n_val)

def small_k_residual(n_val, gamma, C, a_slack):
    k2 = k2_threshold(n_val, gamma, C, a_slack)
    k2_int = max(mp.mpf(1), k2)
    Dlo = -gamma*k2_int; Dhi = (1-gamma)*k2_int
    H_k2 = exact_cubic_max_abs(k2_int, n_val, gamma, Dlo, Dhi)
    return mp.mpf('1')/6 * k2_int * mp.e**mp.mpf('0.5') * H_k2**3 * mp.e**H_k2

def G_n_bound(n_val, gamma):
    b = beta_of(gamma)
    return mp.sqrt(mp.pi*n_val/b)

with open('n0_hybrid_table.pkl', 'rb') as f:
    n0_table_raw = pickle.load(f)
n0_table = [(mp.mpf(a), mp.mpf(b), mp.mpf(c), mp.mpf(d)) for a,b,c,d in n0_table_raw]

A_SLACK = mp.mpf('0.05')
for gamma, m, n0, C in n0_table:
    n_val = mp.mpf(10)**n0
    K = K_real(n_val, gamma)
    Theta_K = C*mp.sqrt(K*mp.log(n_val))
    bulk = bulk_term_new(K, n_val, gamma, Theta_K)
    tail = tail_term_new(K, n_val, gamma, C, A_SLACK)
    Gn = G_n_bound(n_val, gamma)
    smallk = small_k_residual(n_val, gamma, C, A_SLACK)
    total = Gn*(bulk+tail) + smallk
    k2 = k2_threshold(n_val, gamma, C, A_SLACK)
    log_(f"  gamma={float(gamma):.2f}  n0=10^{mp.nstr(n0,6)}  K={mp.nstr(K,4)}  k2={mp.nstr(k2,4)}")
    log_(f"      G_n*bulk={mp.nstr(Gn*bulk,6):>14}  G_n*tail={mp.nstr(Gn*tail,6):>14}  "
         f"small_k={mp.nstr(smallk,6):>14}  TOTAL={mp.nstr(total,6):>10}  "
         f"[binding: {'bulk' if Gn*bulk>=Gn*tail and Gn*bulk>=smallk else ('tail' if Gn*tail>=smallk else 'small_k')}]")

log_("\nAll sanity checks complete.")
with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
