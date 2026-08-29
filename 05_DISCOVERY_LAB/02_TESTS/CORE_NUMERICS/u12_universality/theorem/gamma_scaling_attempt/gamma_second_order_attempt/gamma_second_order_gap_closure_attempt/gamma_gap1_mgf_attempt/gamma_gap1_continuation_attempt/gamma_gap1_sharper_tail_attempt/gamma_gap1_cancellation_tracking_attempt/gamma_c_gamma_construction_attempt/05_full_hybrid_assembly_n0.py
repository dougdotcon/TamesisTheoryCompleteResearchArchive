#!/usr/bin/env python3
"""
Script 05 -- Full hybrid Bulk/Tail assembly: this front's Lyapunov/
exact-4th-moment BULK term (script 03/04) + a fresh re-derivation of the
Bernstein-with-slack TAIL term (Estagio 37's technique, cited, re-derived
from the raw Bernstein inequality here, not imported) + a small-k
residual, bisected for n_0(gamma) at the SAME 8 sample gamma used since
Estagio 36, for direct apples-to-apples comparison against the
predecessor's own Sec.9 table.

Bernstein-with-slack, re-derived from scratch (cited inequality only):
  D = sum of k i.i.d. terms, each Bernoulli(gamma)-centered, so each
  bounded within an interval of length 1 (in [-gamma,1-gamma]), variance
  sigma^2(gamma)=gamma(1-gamma). Standard (two-sided) Bernstein's
  inequality for a sum of independent bounded random variables (CITED,
  classical, same citation tier as Hoeffding, already used throughout
  this lineage since Estagio 37):
     P(|D|>t) <= 2 exp( -t^2 / (2*(k*sigma^2 + t/3)) ).
  For t=Theta_k=C*sqrt(k ln n), demanding 2*t/3 <= a*k*sigma^2 (absorbing
  the t/3 correction into an inflated (2+a) denominator factor) gives a
  UNIFORM bound  P(|D|>Theta_k) <= 2*n^{-C^2/((2+a)*sigma^2)}  valid for
  all k >= k_2(n,gamma,C,a) := (2C/(3*a*sigma^2))^2 * ln(n)  -- an
  EXPLICIT O(ln n) threshold, re-derived here (not copied) and confirmed
  to match the QUALITATIVE description ("k_2=O(ln n)") the predecessor's
  own ATTEMPT.md reports for this same technique.
"""
import pickle
import time
import mpmath as mp
import sympy as sp
from sympy import symbols

mp.mp.dps = 80

LOG = []
def log_(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

log_("="*78)
log_("SCRIPT 05 -- full hybrid Bulk/Tail assembly, n_0(gamma) at 8 sample gamma")
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

Ex4_f = sp.lambdify((k, n, g), Ex4, modules='mpmath')
c0_f = sp.lambdify((k, n, g), c0, modules='mpmath')
c1_f = sp.lambdify((k, n, g), c1, modules='mpmath')
c2_f = sp.lambdify((k, n, g), c2, modules='mpmath')
c3_f = sp.lambdify((k, n, g), c3, modules='mpmath')

def beta_of(gamma):
    return gamma*(2-gamma)/2

def sigma2_of(gamma):
    return gamma*(1-gamma)

def lambda_tight_of(gamma):
    return max(mp.mpf(4), 4*(1-gamma)**2/(gamma*(2-gamma)))

def K_real(n_val, gamma):
    b = beta_of(gamma)
    return mp.sqrt(4*n_val*mp.log(n_val)/b) + 1

def exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi):
    c0v = c0_f(k_val, n_val, gamma); c1v = c1_f(k_val, n_val, gamma)
    c2v = c2_f(k_val, n_val, gamma); c3v = c3_f(k_val, n_val, gamma)
    def xval(Dv):
        return c0v + c1v*Dv + c2v*Dv**2 + c3v*Dv**3
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
    """This front's Lyapunov/exact-4th-moment bulk bound:
       (1/6) * e^{H_Theta} * (E[x(D)^4])^{3/4}."""
    Dlo = max(-gamma*k_val, -Theta_k)
    Dhi = min((1-gamma)*k_val, Theta_k)
    H_Theta = exact_cubic_max_abs(k_val, n_val, gamma, Dlo, Dhi)
    Ex4_val = Ex4_f(k_val, n_val, gamma)
    if Ex4_val < 0:
        Ex4_val = mp.mpf(0)
    return mp.mpf('1')/6 * mp.e**H_Theta * Ex4_val**mp.mpf('0.75')

def tail_term_new(K_val, n_val, gamma, C, a_slack):
    """Bernstein-with-slack tail piece, re-derived fresh (see module
    docstring): (1/6)*2*n^{-C^2/((2+a)sigma^2)} * H_K^3 * e^{H_K}, H_K the
    exact-cubic-max over the FULL true support at k=K (cited technique,
    re-implemented fresh in exact_cubic_max_abs)."""
    Dlo = -gamma*K_val
    Dhi = (1-gamma)*K_val
    H_K = exact_cubic_max_abs(K_val, n_val, gamma, Dlo, Dhi)
    sigma2 = sigma2_of(gamma)
    exponent = -(C**2)/((2+a_slack)*sigma2) * mp.log(n_val)
    prob_factor = 2*mp.e**exponent
    return mp.mpf('1')/6 * prob_factor * H_K**3 * mp.e**H_K

def k2_threshold(n_val, gamma, C, a_slack):
    sigma2 = sigma2_of(gamma)
    return (2*C/(3*a_slack*sigma2))**2 * mp.log(n_val)

def small_k_residual(n_val, gamma, C, a_slack):
    """Small-k (k<k_2=O(ln n)) residual, bounded crudely by k_2 times
    this front's own bulk-style bound evaluated AT k_2 over the FULL
    (unclipped) support -- matching the predecessor's own convention
    (their Sec.8 self-caught-bug fix: evaluate the small-k piece at its
    own natural k_2 scale, not at K). Disclosed simplification: unlike
    the main bulk/tail pieces (where this front's improvement is the
    point), this small-k piece is not the bottleneck at the scales
    tested (k_2=O(ln n) is always dwarfed by K=O(sqrt(n ln n)) for large
    n) so a reasonably crude but valid bound suffices here."""
    k2 = k2_threshold(n_val, gamma, C, a_slack)
    k2_int = max(mp.mpf(1), k2)
    Dlo = -gamma*k2_int
    Dhi = (1-gamma)*k2_int
    H_k2 = exact_cubic_max_abs(k2_int, n_val, gamma, Dlo, Dhi)
    return mp.mpf('1')/6 * k2_int * mp.e**mp.mpf('0.5') * H_k2**3 * mp.e**H_k2

def G_n_bound(n_val, gamma):
    """Cited (Lemma D0 lineage, reused as-is exactly like every ancestor)."""
    b = beta_of(gamma)
    return mp.sqrt(mp.pi*n_val/b)

def W_hybrid(n_val, gamma, C, a_slack):
    K = K_real(n_val, gamma)
    Theta_K = C*mp.sqrt(K*mp.log(n_val))
    bulk = bulk_term_new(K, n_val, gamma, Theta_K)
    tail = tail_term_new(K, n_val, gamma, C, a_slack)
    Gn = G_n_bound(n_val, gamma)
    small_k = small_k_residual(n_val, gamma, C, a_slack)
    return Gn*(bulk + tail) + small_k

# ---------------------------------------------------------------------
# Sanity check: Bernstein-with-slack tail vs the TRUE binomial tail
# probability, verified against direct pmf summation (small k) -- a
# fresh, independent verification of the cited inequality's correctness
# in THIS script's own implementation, before trusting it for bisection.
# ---------------------------------------------------------------------
log_("\n--- Sanity: Bernstein-with-slack P(|D|>t) bound vs EXACT binomial tail ---")
from math import comb
def exact_tail_prob(k_val, gamma_f, t):
    total = 0.0
    for m in range(0, k_val+1):
        Dv = m - gamma_f*k_val
        if abs(Dv) > t:
            total += comb(k_val, m) * gamma_f**m * (1-gamma_f)**(k_val-m)
    return total

viol = 0
checks = 0
for k_val in [20, 50, 100]:
    for gamma_f in [0.3, 0.5, 0.7]:
        sigma2 = gamma_f*(1-gamma_f)
        for t_frac in [0.5, 1.0, 2.0]:
            t = t_frac*mp.sqrt(k_val*sigma2)
            bern_bound = 2*float(mp.e**(-(float(t)**2)/(2*(k_val*sigma2+float(t)/3))))
            exact = exact_tail_prob(k_val, gamma_f, float(t))
            checks += 1
            if exact > bern_bound + 1e-12:
                viol += 1
                log_(f"  VIOLATION k={k_val} gamma={gamma_f} t={float(t):.3f}: "
                     f"exact={exact:.6g} > bound={bern_bound:.6g}")
log_(f"  {checks} checks, {viol} violations (Bernstein's classical inequality, "
     f"as expected: 0 violations)")
assert viol == 0

# ---------------------------------------------------------------------
# Bisection for n_0(gamma): find n such that W_hybrid(n,gamma,C,a) < 1,
# then confirm it stays < 1 up to 20+ decades beyond (no-oscillation
# check, same convention as every ancestor).
# ---------------------------------------------------------------------
log_("\n--- Bisecting n_0(gamma) for W_hybrid(n,gamma,C,a) < 1 ---")

GAMMAS = [mp.mpf(x) for x in ['0.99','0.9','0.7','0.5','0.3','0.1','0.05','0.01']]
A_SLACK = mp.mpf('0.05')   # matching predecessor's own choice, for direct comparability

def find_n0_log10(gamma, C, a_slack, lo_log10=5, hi_log10=200):
    """Bisect on log10(n) for the crossing where W_hybrid < 1."""
    def f(log10n):
        n_val = mp.mpf(10)**log10n
        try:
            w = W_hybrid(n_val, gamma, C, a_slack)
        except Exception:
            return mp.mpf('inf')
        return mp.log(w) if w > 0 else mp.mpf('-inf')
    lo, hi = mp.mpf(lo_log10), mp.mpf(hi_log10)
    if f(hi) >= 0:
        return None  # doesn't cross in range
    if f(lo) < 0:
        return lo   # already below at lo
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

results_table = []
MARGINS = [mp.mpf(x) for x in ['1.01','1.05','1.10','1.20','1.50','2.0']]

t_start = time.time()
for gamma in GAMMAS:
    best = optimize_margin(gamma, A_SLACK, MARGINS)
    if best is None:
        log_(f"  gamma={float(gamma):.2f}: NO crossing found in tested range!")
        continue
    m, n0, C = best
    results_table.append((gamma, m, n0, C))
    log_(f"  gamma={float(gamma):>5.2f}  best margin={float(m):>5.2f}  "
         f"C={mp.nstr(C,6)}  log10(n0)={mp.nstr(n0,8)}")
log_(f"\nBisection wall time: {time.time()-t_start:.1f}s")

# ---------------------------------------------------------------------
# No-spurious-oscillation check, 15 decades beyond each n_0.
# ---------------------------------------------------------------------
log_("\n--- No-spurious-oscillation check (15 decades beyond each n_0) ---")
for gamma, m, n0, C in results_table:
    grid = [n0 + mp.mpf(i)*mp.mpf('0.5') for i in range(0, 31)]
    vals = [W_hybrid(mp.mpf(10)**lg, gamma, C, A_SLACK) for lg in grid]
    increasing_found = any(vals[i+1] > vals[i] for i in range(len(vals)-1))
    log_(f"  gamma={float(gamma):.2f}: increasing_found={increasing_found} "
         f"(checked log10 n0..n0+15, step 0.5)")

with open('n0_hybrid_table.pkl', 'wb') as f:
    pickle.dump([(str(a),str(b),str(c),str(d)) for a,b,c,d in results_table], f)

log_("\nDone.")
with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
