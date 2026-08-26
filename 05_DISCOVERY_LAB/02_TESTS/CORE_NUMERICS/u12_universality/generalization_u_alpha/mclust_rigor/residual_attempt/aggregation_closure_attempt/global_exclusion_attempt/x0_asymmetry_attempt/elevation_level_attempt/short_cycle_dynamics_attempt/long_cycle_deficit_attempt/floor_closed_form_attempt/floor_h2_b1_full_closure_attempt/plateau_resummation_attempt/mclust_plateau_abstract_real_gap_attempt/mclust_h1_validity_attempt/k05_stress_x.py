"""
k05_stress_x.py -- stress test: push x (and thus s=x/sqrt(c)) further,
including into the region s>1 (physically outside the process's natural
domain s in [0,1], where "s" was originally a fraction-of-pool-consumed
variable) at smaller c, to look specifically for a FAILURE of uniformity
-- a genuine attempt to find a counterexample/limitation, not just more
confirmation.
"""
import time, mpmath as mp
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k01_family_series as fam
import k03_profiles as prof

cases = [
    # (c, K, dps, x_list)
    (1000, 300, 60, [0, 2, 4, 6, 8, 10, 12, 15, 20]),
    (4000, 800, 90, [0, 2, 4, 6, 8, 10, 12, 15, 20]),
]

print(f"{'c':>6} {'x':>5} {'s=x/sqrtc':>10} {'F':>16} {'gap1/eps':>12} {'psi3(x)':>12} {'ratio':>8} {'convOK':>7}")
for c, K, DPS, xs in cases:
    t0 = time.time()
    a, b = fam.build_family(c, K, DPS)
    mp.mp.dps = DPS
    sqc = mp.sqrt(mp.mpf(c))
    eps = 1 / sqc
    t0p = mp.mpf(50) / c
    t0c = mp.mpf(60) / c
    for x in xs:
        s0 = mp.mpf(x) / sqc
        F = fam.phi_series_sum(a, s0, t0p, K, c)
        Fc = fam.phi_series_sum(a, s0, t0c, K, c)
        d = abs((F - Fc) / Fc) if Fc != 0 else abs(F - Fc)
        p1 = prof.psi1(x); p2 = prof.psi2(x); p3 = prof.psi3(x)
        rho1 = (F - eps * p1) / eps**2
        gap1 = rho1 - p2
        ratio = gap1 / (eps * p3) if p3 != 0 else mp.mpf('nan')
        print(f"{c:>6} {x:>5} {mp.nstr(s0,4):>10} {mp.nstr(F,10):>16} "
              f"{mp.nstr(gap1/eps,6):>12} {mp.nstr(p3,6):>12} {mp.nstr(ratio,5):>8} "
              f"{'ok' if d<mp.mpf('1e-12') else 'BAD:'+mp.nstr(d,2):>7}")
    print(f"  (build {time.time()-t0:.1f}s)")
