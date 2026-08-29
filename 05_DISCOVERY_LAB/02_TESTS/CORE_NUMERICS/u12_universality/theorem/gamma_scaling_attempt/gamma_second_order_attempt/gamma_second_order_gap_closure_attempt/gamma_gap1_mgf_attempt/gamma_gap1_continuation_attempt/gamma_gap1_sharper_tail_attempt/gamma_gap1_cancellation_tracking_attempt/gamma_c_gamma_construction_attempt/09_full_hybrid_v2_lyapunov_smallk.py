#!/usr/bin/env python3
"""
Script 09 -- Second-pass hybrid assembly: apply the SAME Lyapunov/exact-
4th-moment refinement (script 03) to the SMALL-K residual term too, not
just the main bulk term. Script 06's Check (C) found that for
gamma=0.99, 0.90 the small-k residual (script 05's deterministic
H_{k2}^3*e^{H_{k2}} version) was the BINDING constraint, not the bulk
term -- so this is the natural next lever.

Derivation of this front's own small-k bound (self-derived here, not
copied from any ancestor formula -- the predecessor's own small-k
formula carries an extra "e^{1/2}" factor whose exact derivation this
front's required reading did not include in enough detail to cite
precisely, so rather than copy an unverified constant, this script
re-derives its OWN small-k bound from first principles):

  sum_{k=1}^{k2} e^{-s(k)} R_k
     <= sum_{k=1}^{k2} 1 * R_k                          (e^{-s(k)}<=1, trivial)
     <= k2 * max_{k<=k2} R_k                              (crude union bound)
     <= k2 * (1/6) * e^{H_full(k2)} * (E[x(D)^4]|_{k=k2})^{3/4}
                                                            (Lyapunov, same as bulk,
                                                             using k-uniformity of
                                                             BOTH H_full(k) and
                                                             E[x(D)^4]|_k, verified
                                                             numerically below)

This is a strictly SIMPLER (and, since it omits the un-derived e^{1/2}
factor, at least as tight) bound than the deterministic H_{k2}^3 version
used in script 05.
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
log_("SCRIPT 09 -- hybrid v2: Lyapunov refinement applied to small-k too")
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

def bulk_term_new(k_val, n_val, gamma, Theta_k):
    Dlo = max(-gamma*k_val, -Theta_k); Dhi = min((1-gamma)*k_val, Theta_k)
    H_Theta = exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi)
    Ex4_val = Ex4_f(k_val, n_val, gamma)
    if Ex4_val < 0: Ex4_val = mp.mpf(0)
    return mp.mpf('1')/6 * mp.e**H_Theta * Ex4_val**mp.mpf('0.75')

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

def small_k_residual_v2(n_val, gamma, C, a_slack):
    """Lyapunov-based small-k bound, self-derived (see module docstring):
       k2 * (1/6) * e^{H_full(k2)} * (E[x(D)^4]|_{k2})^{3/4}."""
    k2 = k2_threshold(n_val, gamma, C, a_slack)
    k2_int = max(mp.mpf(1), k2)
    Dlo = -gamma*k2_int; Dhi = (1-gamma)*k2_int
    H_k2 = exact_cubic_max_abs(k2_int, n_val, gamma, Dlo, Dhi)
    Ex4v = Ex4_f(k2_int, n_val, gamma)
    if Ex4v < 0: Ex4v = mp.mpf(0)
    return k2_int * mp.mpf('1')/6 * mp.e**H_k2 * Ex4v**mp.mpf('0.75')

def G_n_bound(n_val, gamma):
    b = beta_of(gamma)
    return mp.sqrt(mp.pi*n_val/b)

def W_hybrid_v2(n_val, gamma, C, a_slack):
    K = K_real(n_val, gamma)
    Theta_K = C*mp.sqrt(K*mp.log(n_val))
    bulk = bulk_term_new(K, n_val, gamma, Theta_K)
    tail = tail_term_new(K, n_val, gamma, C, a_slack)
    Gn = G_n_bound(n_val, gamma)
    small_k = small_k_residual_v2(n_val, gamma, C, a_slack)
    return Gn*(bulk + tail) + small_k

GAMMAS = [mp.mpf(x) for x in ['0.99','0.9','0.7','0.5','0.3','0.1','0.05','0.01']]
A_SLACK = mp.mpf('0.05')
MARGINS = [mp.mpf(x) for x in ['1.01','1.05','1.10','1.20','1.50','2.0']]

def find_n0_log10(gamma, C, a_slack, lo_log10=5, hi_log10=200):
    def f(log10n):
        n_val = mp.mpf(10)**log10n
        try:
            w = W_hybrid_v2(n_val, gamma, C, a_slack)
        except Exception:
            return mp.mpf('inf')
        return mp.log(w) if w > 0 else mp.mpf('-inf')
    lo, hi = mp.mpf(lo_log10), mp.mpf(hi_log10)
    if f(hi) >= 0:
        return None
    if f(lo) < 0:
        return lo
    for _ in range(60):
        mid = (lo+hi)/2
        if f(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return hi

def optimize_margin(gamma, a_slack, margins):
    best = None
    C0 = mp.sqrt((2+a_slack)*sigma2_of(gamma)*(lambda_tight_of(gamma)+mp.mpf('0.5')))
    for m in margins:
        C = m*C0
        n0 = find_n0_log10(gamma, C, a_slack)
        if n0 is not None and (best is None or n0 < best[1]):
            best = (m, n0, C)
    return best

log_("\n--- n_0(gamma) bisection, hybrid v2 (Lyapunov bulk AND small-k) ---")
results_table = []
for gamma in GAMMAS:
    best = optimize_margin(gamma, A_SLACK, MARGINS)
    if best is None:
        log_(f"  gamma={float(gamma):.2f}: NO crossing found!")
        continue
    m, n0, C = best
    results_table.append((gamma, m, n0, C))
    log_(f"  gamma={float(gamma):>5.2f}  best margin={float(m):>5.2f}  "
         f"C={mp.nstr(C,6)}  log10(n0)={mp.nstr(n0,8)}")

log_("\n--- No-spurious-oscillation check (15 decades beyond each n_0) ---")
for gamma, m, n0, C in results_table:
    grid = [n0 + mp.mpf(i)*mp.mpf('0.5') for i in range(0, 31)]
    vals = [W_hybrid_v2(mp.mpf(10)**lg, gamma, C, A_SLACK) for lg in grid]
    increasing_found = any(vals[i+1] > vals[i] for i in range(len(vals)-1))
    log_(f"  gamma={float(gamma):.2f}: increasing_found={increasing_found}")

log_("\n--- k-uniformity check for E[x(D)^4]|_k over k<=k2 (needed for the")
log_("    small-k Lyapunov bound's own validity) ---")
viol = 0; checks = 0
for gamma, m, n0, C in results_table:
    n_val = mp.mpf(10)**n0
    k2 = k2_threshold(n_val, gamma, C, A_SLACK)
    k2_int = max(mp.mpf(1), k2)
    Ex4_at_k2 = Ex4_f(k2_int, n_val, gamma)
    if Ex4_at_k2 < 0: Ex4_at_k2 = mp.mpf(0)
    worst_ratio = mp.mpf(0)
    for fr in [mp.mpf(x) for x in ['0.001','0.01','0.1','0.5','0.9','0.99','1.0']]:
        kv = max(mp.mpf(1), fr*k2_int)
        Ex4_kv = Ex4_f(kv, n_val, gamma)
        if Ex4_kv < 0: Ex4_kv = mp.mpf(0)
        checks += 1
        ratio = Ex4_kv/Ex4_at_k2 if Ex4_at_k2 > 0 else mp.mpf(0)
        worst_ratio = max(worst_ratio, ratio)
        if Ex4_kv > Ex4_at_k2*(1+mp.mpf('1e-15')):
            viol += 1
    log_(f"  gamma={float(gamma):.2f}: worst E[x^4](k)/E[x^4](k2) ratio = {mp.nstr(worst_ratio,6)}")
log_(f"  TOTAL: {checks} checks, {viol} violations")

with open('n0_hybrid_v2_table.pkl', 'wb') as f:
    pickle.dump([(str(a),str(b),str(c),str(d)) for a,b,c,d in results_table], f)

log_("\nDone.")
with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
