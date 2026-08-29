"""Probe: does (K=400,dps=250) also suffice at c=4000,16000,64000 (same
ct0 in [60,80] target)? Truncation should need at MOST as many terms as
c=1000 since t0=ct0/c shrinks as c grows (faster series convergence)."""
from mpmath import mp, mpf
from u02_family_series import build_family, fam_eval, erfcx

K, dps = 400, 250


def Phi_sum(alist, s, t0, Eval, K_use):
    total = mpf(0)
    t0p = mpf(1)
    for k in range(K_use + 1):
        total += fam_eval(alist[k], s, Eval) * t0p
        t0p *= t0
    return total


for c in (4000, 16000, 64000):
    c_val = mpf(c)
    a, b, cv, sc = build_family(c_val, K, dps=dps)
    mp.dps = dps
    s = mpf(0)
    Eval = erfcx(s)
    lo = Phi_sum(a, s, mpf(60) / c_val, Eval, K)
    hi = Phi_sum(a, s, mpf(80) / c_val, Eval, K)
    reldiff = abs(lo - hi) / abs(hi)
    print(f"c={c:6d}  Phi_hi(s=0)={hi}")
    print(f"           reldiff(lo,hi)={reldiff}")
