"""
k07_stress_x_corrected.py -- corrected rerun of k05_stress_x.py's x=14,16,20
rows at c=200.

SELF-CAUGHT ISSUE (disclosed, per this lineage's convention): k05's
first pass used K=400 for the c=200 stress grid (sufficient for x<=12,
verified in k04/k05 via the two-t0 approach-rate cross-check), but at
x=14 (s=0.99, near the presumed physical boundary s=1) and beyond, the
two-t0 cross-check itself FAILED (relative disagreement ~0.86-1.0,
i.e. no stable digits at all) -- caught by this front's own diagnostic
BEFORE the resulting numbers were used in any uniformity-ratio table.
This script reruns x=14,16,20 at c=200 with K=800,dps=90 (up from
K=400,dps=60) and re-checks convergence; see ATTEMPT.md Section 5.6 for
the reading of the corrected numbers (uniformity continues to hold, no
breakdown found -- the earlier apparent "ratio blowup" at x=20 in k05's
raw log was purely this numerical non-convergence artifact, not a
finding about H1).
"""
import mpmath as mp
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k01_family_series as fam
import k03_profiles as prof

c, K, DPS = 200, 800, 90
a, b = fam.build_family(c, K, DPS)
mp.mp.dps = DPS
sqc = mp.sqrt(mp.mpf(c))
eps = 1 / sqc
t0p = mp.mpf(50) / c
t0c = mp.mpf(60) / c

print(f"{'x':>4} {'s=x/sqrtc':>10} {'F':>18} {'approach_reldiff':>18} {'ratio1':>10}")
for x in [14, 16, 20]:
    s0 = mp.mpf(x) / sqc
    F = fam.phi_series_sum(a, s0, t0p, K, c)
    Fc = fam.phi_series_sum(a, s0, t0c, K, c)
    d = abs((F - Fc) / Fc)
    p1, p2, p3 = prof.psi1(x), prof.psi2(x), prof.psi3(x)
    rho1 = (F - eps * p1) / eps**2
    gap1 = rho1 - p2
    ratio1 = gap1 / (eps * p3)
    print(f"{x:>4} {mp.nstr(s0,4):>10} {mp.nstr(F,14):>18} {mp.nstr(d,3):>18} {mp.nstr(ratio1,6):>10}")
