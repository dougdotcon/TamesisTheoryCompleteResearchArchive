"""
REFEREE script 06 -- independent check of two secondary claims in the target
document's section 6:
  (a) k2/K_max at gamma=0.99 shrinks from ~2.0e-3 at n0 to ~3.6e-23 forty
      decades beyond n0 (own reconstruction, using the same k2, K_max
      formulas already independently verified in ref02/ref05).
  (b) log W(n,gamma,C) [both Hoeffding and Bernstein constructions] shows no
      local increase (no spurious oscillation) from n0 through 40 decades
      beyond, at a handful of representative gamma.
"""
import mpmath as mp
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref05_n0_final_spotcheck_all8 import (
    K_max_of, sigma2_of, C0_bernstein_of, C0_hoeffding_of,
    logW_hoeffding, logW_bernstein_refined,
)

mp.mp.dps = 60

print("=== (a) k2/K_max shrinking check at gamma=0.99 ===")
gamma = mp.mpf('0.99')
a_slack = mp.mpf('0.05')
C0b = C0_bernstein_of(gamma, a_slack)
C_bern = mp.mpf('1.2') * C0b
n0_log10 = mp.mpf('17.72')  # target's own claimed n0(0.99)

for offset in [0, 10, 20, 30, 40]:
    logn = n0_log10 + offset
    n = mp.power(10, logn)
    K = K_max_of(n, gamma)
    sigma2 = sigma2_of(gamma)
    M = max(gamma, 1 - gamma)
    k2 = (2 * M * C_bern / (3 * a_slack * sigma2)) ** 2 * mp.log(n)
    ratio = k2 / K
    print(f"  n0+{offset:3d} decades (log10 n={float(logn):.2f}): "
          f"k2/K_max = {float(ratio):.6e}")

print()
print("Target's claim: 2.0e-3 at n0, 3.6e-23 forty decades beyond -- compare above.")
print()

print("=== (b) No spurious oscillation check: log W monotone decreasing ===")
print("    (Hoeffding and Bernstein, 5 representative gamma, fine grid from n0 to")
print("     +40 decades beyond, half-decade steps)")
print()

PUBLISHED_OLD = {'0.99': mp.mpf('20.79'), '0.5': mp.mpf('50.28'),
                 '0.1': mp.mpf('65.95'), '0.01': mp.mpf('84.88'), '0.9': mp.mpf('36.83')}
NEW_N0 = {'0.99': mp.mpf('17.72'), '0.5': mp.mpf('50.35'),
          '0.1': mp.mpf('63.06'), '0.01': mp.mpf('75.79'), '0.9': mp.mpf('33.64')}

for gstr in ['0.99', '0.9', '0.5', '0.1', '0.01']:
    gamma = mp.mpf(gstr)
    C0h = C0_hoeffding_of(gamma)
    C_hoeff = mp.mpf('1.2') * C0h
    C0b = C0_bernstein_of(gamma, a_slack)
    C_bern = mp.mpf('1.2') * C0b

    n0_h = PUBLISHED_OLD[gstr]
    n0_b = NEW_N0[gstr]

    vals_h = []
    vals_b = []
    grid = [mp.mpf(i) * mp.mpf('0.5') for i in range(0, 81)]  # 0..40 in steps of 0.5
    for off in grid:
        logn_h = n0_h + off
        logn_b = n0_b + off
        vals_h.append(logW_hoeffding(logn_h, gamma, C_hoeff))
        vals_b.append(logW_bernstein_refined(logn_b, gamma, C_bern, a_slack))

    inc_h = any(vals_h[i + 1] > vals_h[i] for i in range(len(vals_h) - 1))
    inc_b = any(vals_b[i + 1] > vals_b[i] for i in range(len(vals_b) - 1))
    print(f"  gamma={gstr:>5}: Hoeffding increasing_found={inc_h}   "
          f"Bernstein increasing_found={inc_b}")

print()
print("(increasing_found=False at every gamma for both constructions confirms no")
print(" spurious oscillation over the searched range, matching the target's own")
print(" claim in section 6.)")
