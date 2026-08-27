"""
Diagnostic follow-up to ref04: investigate the gamma=0.99 discrepancy between
the referee's own Bernstein n0 reconstruction (19.51) and the target's
claimed value (17.72). Print all the individual pieces (bulk term, tail
term, small-k term, k2 vs K_max) at both the referee's own crossover and the
target's claimed crossover, to see which piece is driving the difference,
and to determine whether this is (a) a known limitation of the referee's
deliberately-approximate small-k reconstruction (disclosed as such in
ref04), or (b) a genuine issue worth flagging in the target document.
"""
import mpmath as mp
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref04a_n0_assembly_reconstruction_initial import (
    K_max_of, sigma2_of, Ghat_of, Ghat_Theta_of, Gn_bound_of, C0_bernstein_of,
    g_bound, lambda_hat_of,
)

mp.mp.dps = 60

gamma = mp.mpf('0.99')
a_slack = mp.mpf('0.05')
C0b = C0_bernstein_of(gamma, a_slack)
C_bern = mp.mpf('1.2') * C0b
print(f"gamma=0.99, a=0.05")
print(f"C0_Bernstein = {float(C0b):.6f}, C = 1.2*C0 = {float(C_bern):.6f}")
print()

for logn_val, label in [(mp.mpf('17.72'), "target's claimed n0"),
                          (mp.mpf('19.51'), "referee's own n0")]:
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

    gk2 = g_bound(k2, K, n, gamma)
    smallk_log = mp.log(k2) + mp.mpf('0.5') - mp.log(6) + 3 * mp.log(gk2) + gk2

    print(f"--- {label}: log10(n)={float(logn_val)} ---")
    print(f"  K_max = {float(K):.6e}")
    print(f"  k2    = {float(k2):.6e}   k2/K_max = {float(k2/K):.6e}")
    print(f"  Ghat(n,gamma) = {float(Gh):.6f}")
    print(f"  Ghat_Theta(n,gamma,C) = {float(GhT):.6f}")
    print(f"  sigma^2(0.99) = {float(sigma2):.6f}  (very small -- close to gamma=1)")
    print(f"  tail_exponent (Bernstein) = -C^2/((2+a)sigma^2) = {float(tail_exponent):.4f}")
    print(f"  log(bulk+tail term) [natural log] = {float(bulk_tail_log):.4f}")
    print(f"  g(k2) [small-k term argument]     = {float(gk2):.6f}")
    print(f"  log(small-k term) [natural log]   = {float(smallk_log):.4f}")
    hi = max(bulk_tail_log, smallk_log)
    lo = min(bulk_tail_log, smallk_log)
    combined = hi + mp.log1p(mp.exp(lo - hi))
    print(f"  combined log(W) = {float(combined):.4f}   (want <=0 for n0)")
    print(f"  DOMINANT term: {'small-k' if smallk_log > bulk_tail_log else 'bulk+tail'}")
    print()

print("=== Comparison with target document's own disclosed numbers (ATTEMPT.md section 8 item 3) ===")
print("Target claims, AT ITS OWN n0(0.99)~10^17.72:")
print("  log(small-k term) ~ -0.04")
print("  log(bulk+tail term) ~ -3.18")
print("  i.e. small-k term is only ~e^3.14 ~ 23x smaller than bulk+tail, non-negligible")
print()
print("Referee's own reconstruction AT THE TARGET'S CLAIMED n0=10^17.72 finds instead:")
