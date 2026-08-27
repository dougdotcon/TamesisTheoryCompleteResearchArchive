"""
Follow-up refinement: retry the small-k residual term using coefficients
evaluated at the RUNNING k (i.e. c_i(k2), not c_i(K_max)) -- the more
natural choice for a deterministic per-k bound, since there is no structural
reason to inflate the small-k coefficients up to the global truncation
bound K_max the way the Bulk/Tail Lemma's k-uniformity trick does. This
tests whether that specific modeling choice explains the gamma=0.99
discrepancy found in ref04b.
"""
import mpmath as mp
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref04a_n0_assembly_reconstruction_initial import (
    K_max_of, sigma2_of, Ghat_of, Ghat_Theta_of, Gn_bound_of, C0_bernstein_of,
    g_bound,
)

mp.mp.dps = 60

gamma = mp.mpf('0.99')
a_slack = mp.mpf('0.05')
C0b = C0_bernstein_of(gamma, a_slack)
C_bern = mp.mpf('1.2') * C0b

for logn_val, label in [(mp.mpf('17.72'), "target's claimed n0"),
                          (mp.mpf('19.51'), "referee's OLD (K-coeff) n0")]:
    n = mp.power(10, logn_val)
    K = K_max_of(n, gamma)
    sigma2 = sigma2_of(gamma)
    M = max(gamma, 1 - gamma)
    k2 = (2 * M * C_bern / (3 * a_slack * sigma2)) ** 2 * mp.log(n)
    Gn = Gn_bound_of(n, gamma)
    Gh = Ghat_of(n, gamma)
    GhT = Ghat_Theta_of(n, gamma, C_bern)
    tail_exponent = -(C_bern * C_bern) / ((2 + a_slack) * sigma2)
    tail_factor = 2 * mp.power(n, tail_exponent)
    bulk_term = mp.power(GhT, 3) * mp.exp(GhT)
    tail_term = tail_factor * mp.power(Gh, 3) * mp.exp(Gh)
    bulk_tail_log = mp.log(Gn) + mp.log(bulk_term + tail_term) - mp.log(6)

    # NEW: small-k term using coefficients at running k=k2 (not K_max)
    gk2_running = g_bound(k2, k2, n, gamma)
    smallk_log_running = mp.log(k2) + mp.mpf('0.5') - mp.log(6) + 3 * mp.log(gk2_running) + gk2_running

    print(f"--- {label}: log10(n)={float(logn_val)} ---")
    print(f"  bulk+tail log = {float(bulk_tail_log):.4f}")
    print(f"  [running-k coeffs] g(k2) = {float(gk2_running):.6f}, "
          f"log(small-k term) = {float(smallk_log_running):.4f}")
    hi = max(bulk_tail_log, smallk_log_running)
    lo = min(bulk_tail_log, smallk_log_running)
    combined = hi + mp.log1p(mp.exp(lo - hi))
    print(f"  combined logW (running-k small-k term) = {float(combined):.4f}")
    print()

print("Target's own disclosed numbers at its published n0(0.99): "
      "log(small-k)~-0.04, log(bulk+tail)~-3.18")
print()

# Now re-bisect n0 for gamma=0.99 using the refined (running-k) small-k term
def logW_bernstein_refined(logn, gamma_, C_, a_):
    n_ = mp.power(10, logn)
    Gn_ = Gn_bound_of(n_, gamma_)
    Gh_ = Ghat_of(n_, gamma_)
    GhT_ = Ghat_Theta_of(n_, gamma_, C_)
    sigma2_ = sigma2_of(gamma_)
    tail_exponent_ = -(C_ * C_) / ((2 + a_) * sigma2_)
    tail_factor_ = 2 * mp.power(n_, tail_exponent_)
    bulk_term_ = mp.power(GhT_, 3) * mp.exp(GhT_)
    tail_term_ = tail_factor_ * mp.power(Gh_, 3) * mp.exp(Gh_)
    bulk_tail_log_ = mp.log(Gn_) + mp.log(bulk_term_ + tail_term_) - mp.log(6)
    M_ = max(gamma_, 1 - gamma_)
    k2_ = (2 * M_ * C_ / (3 * a_ * sigma2_)) ** 2 * mp.log(n_)
    if k2_ < 1:
        k2_ = mp.mpf(1)
    gk2_ = g_bound(k2_, k2_, n_, gamma_)  # running-k coefficients
    smallk_log_ = mp.log(k2_) + mp.mpf('0.5') - mp.log(6) + 3 * mp.log(gk2_) + gk2_
    hi_ = max(bulk_tail_log_, smallk_log_)
    lo_ = min(bulk_tail_log_, smallk_log_)
    return hi_ + mp.log1p(mp.exp(lo_ - hi_))


a_, b_ = mp.mpf(1), mp.mpf(250)
fa = logW_bernstein_refined(a_, gamma, C_bern, a_slack)
fb = logW_bernstein_refined(b_, gamma, C_bern, a_slack)
print(f"Bracket check: logW(1)={float(fa):.3f}, logW(250)={float(fb):.3f}")
for _ in range(200):
    mid = (a_ + b_) / 2
    fm = logW_bernstein_refined(mid, gamma, C_bern, a_slack)
    if fm > 0:
        a_ = mid
    else:
        b_ = mid
    if b_ - a_ < mp.mpf('1e-3'):
        break
n0_refined = (a_ + b_) / 2
print(f"Refined (running-k small-k term) bisected log10(n0) at gamma=0.99: {float(n0_refined):.4f}")
print(f"Target's claimed value: 17.72")
print(f"Referee's original (K-coeff small-k) value: 19.51")
