"""Quick empirical probe: what (K,dps) is needed for the direct-summation
plateau at c=1000, s=0, to stabilize to ~20-25 digits via the two-t0
convergence check (c*t0 = 230 vs 260)? Determines sizing for the main
experiment; not itself a claimed result."""
import time
from mpmath import mp, mpf
from u02_family_series import build_family, fam_eval, erfcx

c_val = mpf(1000)


def Phi_sum(alist, s, t0, Eval, K_use):
    total = mpf(0)
    t0p = mpf(1)
    for k in range(K_use + 1):
        total += fam_eval(alist[k], s, Eval) * t0p
        t0p *= t0
    return total


for K, dps in [(150, 90), (250, 150), (400, 250)]:
    t0start = time.time()
    a, b, cv, sc = build_family(c_val, K, dps=dps)
    mp.dps = dps
    s = mpf(0)
    Eval = erfcx(s)
    lo = Phi_sum(a, s, mpf(60) / c_val, Eval, K)
    hi = Phi_sum(a, s, mpf(80) / c_val, Eval, K)
    diff = abs(lo - hi)
    reldiff = diff / abs(hi) if hi != 0 else diff
    dt = time.time() - t0start
    print(f"K={K:5d} dps={dps:4d}  time={dt:6.1f}s  "
          f"Phi_hi={hi}  reldiff(lo,hi)={reldiff}")
