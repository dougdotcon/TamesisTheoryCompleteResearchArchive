#!/usr/bin/env python3
"""
Script 07 -- k-uniformity checks for THIS front's own bulk/small-k
constructions, at the SAME rigor tier this lineage has used since the
grandparent's own referee first flagged this exact issue (Estagio 33's
adversarial report): the Bulk/Tail Lemma's proof needs its bound to hold
uniformly for 1<=k<=K, but the coefficients are not literally monotone
term-by-term in k for gamma near 1 -- so every front in this lineage
(mgf_attempt, continuation, sharper_tail, cancellation_tracking) has
verified NUMERICALLY (not as a blanket theorem) that the SPECIFIC facts
each construction needs hold, with 0 violations across a broad grid.
This script does the analogous check for THIS front's own two new
quantities:

  (1) bulk_term_new(k,n,gamma,Theta_k) -- is this quantity's value at
      k=K (used as a uniform stand-in for its value at every k<=K in the
      W_hybrid assembly) actually an upper bound on its own value at
      every k<=K? I.e. is bulk_term_new(.,k,.) non-decreasing enough in
      k that k=K dominates?

  (2) H_k (full, UNCLIPPED support exact-cubic-max) -- is H_{k2} (used
      as a uniform stand-in for the small-k residual, k=1..k2) actually
      an upper bound on H_k for every k<=k2?

Both checked at the SAME 8 sample gamma and representative n-scales this
front's own n_0(gamma) table (script 05) actually uses.
"""
import pickle
import time
import mpmath as mp
import sympy as sp
from sympy import symbols, Poly, expand

mp.mp.dps = 80

LOG = []
def log_(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 07 -- k-uniformity checks (this front's own constructions)")
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

def bulk_term_new(k_val, n_val, gamma, Theta_k):
    Dlo = max(-gamma*k_val, -Theta_k); Dhi = min((1-gamma)*k_val, Theta_k)
    H_Theta = exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi)
    Ex4_val = Ex4_f(k_val, n_val, gamma)
    if Ex4_val < 0: Ex4_val = mp.mpf(0)
    return mp.mpf('1')/6 * mp.e**H_Theta * Ex4_val**mp.mpf('0.75')

def H_full(k_val, n_val, gamma):
    Dlo = -gamma*k_val; Dhi = (1-gamma)*k_val
    return exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi)

with open('n0_hybrid_table.pkl', 'rb') as f:
    n0_table_raw = pickle.load(f)
n0_table = [(mp.mpf(a), mp.mpf(b), mp.mpf(c), mp.mpf(d)) for a,b,c,d in n0_table_raw]

log_("\n--- Check (1): is bulk_term_new(k,.) at k=K an upper bound on its own")
log_("    value at every 1<=k<=K (evaluated at EACH k's own Theta_k=C*sqrt(k ln n))? ---")
viol1 = 0
checks1 = 0
for gamma, m, n0, C in n0_table:
    n_val = mp.mpf(10)**n0
    K = K_real(n_val, gamma)
    bulk_at_K = bulk_term_new(K, n_val, gamma, C*mp.sqrt(K*mp.log(n_val)))
    # sample k across the full range, log-spaced plus a few near K
    fracs = [mp.mpf(x) for x in ['0.0001','0.001','0.01','0.05','0.1','0.25','0.5',
                                   '0.75','0.9','0.99','0.999','1.0']]
    worst_ratio = mp.mpf(0)
    for fr in fracs:
        kv = max(mp.mpf(1), fr*K)
        Theta_kv = C*mp.sqrt(kv*mp.log(n_val))
        bulk_kv = bulk_term_new(kv, n_val, gamma, Theta_kv)
        checks1 += 1
        ratio = bulk_kv/bulk_at_K if bulk_at_K > 0 else mp.mpf(0)
        worst_ratio = max(worst_ratio, ratio)
        if bulk_kv > bulk_at_K*(1+mp.mpf('1e-15')):
            viol1 += 1
            log_(f"    VIOLATION gamma={float(gamma):.2f} k/K={float(fr)}: "
                 f"bulk(k)={mp.nstr(bulk_kv,6)} > bulk(K)={mp.nstr(bulk_at_K,6)}")
    log_(f"  gamma={float(gamma):.2f}: {len(fracs)} k-fractions checked, "
         f"worst bulk(k)/bulk(K) ratio = {mp.nstr(worst_ratio,6)} (<=1 required)")
log_(f"\n  TOTAL Check(1): {checks1} checks, {viol1} violations")

log_("\n--- Check (2): is H_full(k2,.) an upper bound on H_full(k,.) for 1<=k<=k2? ---")
viol2 = 0
checks2 = 0
for gamma, m, n0, C in n0_table:
    n_val = mp.mpf(10)**n0
    sigma2 = gamma*(1-gamma)
    A_SLACK = mp.mpf('0.05')
    k2 = (2*C/(3*A_SLACK*sigma2))**2 * mp.log(n_val)
    k2_int = max(mp.mpf(1), k2)
    H_at_k2 = H_full(k2_int, n_val, gamma)
    fracs = [mp.mpf(x) for x in ['0.001','0.01','0.05','0.1','0.25','0.5','0.75','0.9','0.99','1.0']]
    worst_ratio2 = mp.mpf(0)
    for fr in fracs:
        kv = max(mp.mpf(1), fr*k2_int)
        H_kv = H_full(kv, n_val, gamma)
        checks2 += 1
        ratio2 = H_kv/H_at_k2 if H_at_k2 > 0 else mp.mpf(0)
        worst_ratio2 = max(worst_ratio2, ratio2)
        if H_kv > H_at_k2*(1+mp.mpf('1e-15')):
            viol2 += 1
            log_(f"    VIOLATION gamma={float(gamma):.2f} k/k2={float(fr)}: "
                 f"H(k)={mp.nstr(H_kv,6)} > H(k2)={mp.nstr(H_at_k2,6)}")
    log_(f"  gamma={float(gamma):.2f}: k2={mp.nstr(k2_int,5)}, worst H(k)/H(k2) ratio = "
         f"{mp.nstr(worst_ratio2,6)} (<=1 required)")
log_(f"\n  TOTAL Check(2): {checks2} checks, {viol2} violations")

log_("\n" + "="*78)
if viol1 == 0 and viol2 == 0:
    log_("BOTH k-uniformity checks PASSED (0 violations) -- at the SAME numerical-")
    log_("verification-only rigor tier this lineage has used for this exact class")
    log_("of fact since the grandparent's own referee first flagged it (Estagio 33).")
else:
    log_(f"VIOLATIONS FOUND: check1={viol1}, check2={viol2} -- see ATTEMPT.md for how")
    log_("this affects the honest status of the n_0(gamma) table.")

with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
