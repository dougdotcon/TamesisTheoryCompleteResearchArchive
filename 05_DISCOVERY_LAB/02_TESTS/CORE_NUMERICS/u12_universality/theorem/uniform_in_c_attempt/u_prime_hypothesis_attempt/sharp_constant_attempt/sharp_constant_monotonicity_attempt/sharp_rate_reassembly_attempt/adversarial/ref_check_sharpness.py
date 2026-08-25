# ref_check_sharpness.py -- referee check R5: par.6 honesty + T5 table.
# R5a: constants arithmetic: a/a*, 4(sqrt2-1), decimal roundings.
# R5b: replicate the T5 excerpt rows (n=256 and the 3000/3000 cell).
# R5c: tightness trajectory along c=n: ratio n|Delta_n(n)|/(a*sqrt n+kappa_B)
#      at n=100,1000,3000,10000,30000  -- tests BOTH the asymptotic claim
#      (ratio -> 1 from below) AND the target's "max LHS/RHS = 0.9700 at
#      (3000,3000)" claim against its own T4c cells at n=5000..30000.
# R5d: n Delta_n(n) - (a* sqrt n - 1/3) -> 0 (the par.6 asymptotic law).
import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import (Q_exact, Q_bracket_truncated, sqrt_bracket,
                        phi_inf_bracket, ASTAR_LO, ASTAR_HI,
                        A_OLD_LO, A_OLD_HI, SQRT_PI_LO, SQRT_PI_HI,
                        SQRT2_LO, SQRT2_HI, phi_nK_table, phi_mix)
import mpmath as mp
mp.mp.dps = 40

t0 = time.time()
fails = 0
checks = 0
def rec(ok, msg):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("  ** FAIL:", msg)

KAPPA = mp.mpf('0.280480169024586')   # display value, confirmed in R3
astar = mp.sqrt(mp.pi) * (1 / mp.sqrt(2) - mp.mpf(1) / 2)
aold = 1 + mp.sqrt(mp.pi / 2)

print("== R5a: constants ==")
print(f"  a* = {mp.nstr(astar, 12)}  (target 0.3670872119...)")
rec(abs(astar - mp.mpf('0.3670872119')) < 1e-9, "a* value")
rec(float(ASTAR_LO) < float(astar) < float(ASTAR_HI)
    and ASTAR_HI < F(3670873, 10**7),
    "a* < 0.3670873 (decimal form)")
print(f"  a*_hi = {float(ASTAR_HI):.10f} < 0.3670873 :",
      ASTAR_HI < F(3670873, 10**7))
r = aold / astar
print(f"  a/a* = {mp.nstr(r, 8)}  (target 6.1384)")
rec(abs(r - mp.mpf('6.1384')) < 5e-4, "a/a* = 6.1384")
ov = astar / (mp.sqrt(mp.pi) / 8)
print(f"  a*/(sqrt(pi)/8) = {mp.nstr(ov, 8)}; 4(sqrt2-1) = "
      f"{mp.nstr(4*(mp.sqrt(2)-1), 8)}  (target 1.6569)")
rec(abs(ov - 4 * (mp.sqrt(2) - 1)) < 1e-25, "overshoot factor identity")
# improvement factors quoted: 3.47 at c=0.5, -> a/a* = 6.1384 as c->inf
f05 = (aold * mp.sqrt(0.5) + KAPPA) / (astar * mp.sqrt(0.5) + KAPPA)
print(f"  full-bound old/sharp at c=0.5: {mp.nstr(f05, 5)} (target 3.47)")
rec(abs(f05 - mp.mpf('3.47')) < 5e-3, "3.47 factor")

print("== R5b: T5 excerpt rows (exact-driven) ==")
targets = {1: ('0.036106', '0.647567', '2.533794'),
           10: ('0.219808', '1.441312', '7.406085'),
           100: ('2.181324', '3.951352', '22.813622'),
           256: ('5.546475', '6.153876', '36.333506')}
n = 256
tab = phi_nK_table(n)
for c, (tnd, tsh, told) in targets.items():
    ph = phi_mix(n, F(c), tab)
    lo, hi = phi_inf_bracket(F(c))
    nd_lo = n * min(abs(ph - lo), abs(ph - hi))
    nd_hi = n * max(abs(ph - lo), abs(ph - hi))
    sh = astar * mp.sqrt(c) + KAPPA
    od = aold * mp.sqrt(c) + KAPPA
    okd = abs(float(nd_hi) - float(tnd)) < 2e-6
    oks = abs(float(sh) - float(tsh)) < 2e-6
    oko = abs(float(od) - float(told)) < 2e-6
    rec(okd and oks and oko, f"T5 row c={c}")
    print(f"  c={c}: n|D|={float(nd_hi):.6f} (target {tnd}) "
          f"sharp={mp.nstr(sh,7)} (t {tsh}) old={mp.nstr(od,7)} (t {told})")
print(f"  elapsed {time.time()-t0:.0f}s")

print("== R5c/R5d: tightness along c=n ==")
print("      n     n|Delta_n(n)|      ratio to (a*sqrt n+kB)   "
      "n*Delta - (a*sqrt n - 1/3)")
prev_ratio = 0
ratios = {}
for n in [100, 1000, 3000]:
    Qv = Q_exact(n)
    lo, hi = phi_inf_bracket(F(n))
    nd = float(max(abs(Qv - n * lo), abs(Qv - n * hi)))   # = n|Delta|
    ratio = nd / float(astar * mp.sqrt(n) + KAPPA)
    dev = nd - float(astar * mp.sqrt(n) - mp.mpf(1) / 3)
    ratios[n] = ratio
    print(f"  {n:6d}  {nd:14.6f}      {ratio:.6f}              {dev:+.6f}")
    rec(ratio > prev_ratio, f"ratio increasing at n={n}")
    rec(ratio < 1, f"ratio < 1 at n={n}")
    prev_ratio = ratio
for n in [10000, 30000]:
    Qlo, Qhi = Q_bracket_truncated(n)
    slo, shi = sqrt_bracket(n)
    pil = SQRT_PI_LO / (2 * shi) - F(1, 2 * n * 2**n)
    pih = SQRT_PI_HI / (2 * slo)
    nd = float(max(abs(Qhi - n * pil), abs(Qlo - n * pih)))
    ratio = nd / float(astar * mp.sqrt(n) + KAPPA)
    dev = nd - float(astar * mp.sqrt(n) - mp.mpf(1) / 3)
    ratios[n] = ratio
    print(f"  {n:6d}  {nd:14.6f}      {ratio:.6f}              {dev:+.6f}")
    rec(ratio > prev_ratio, f"ratio increasing at n={n}")
    rec(ratio < 1, f"ratio < 1 at n={n}")
    prev_ratio = ratio
# target's claims: 0.847 at 100, 0.949 at 1000, 0.970 at 3000
rec(abs(ratios[100] - 0.847) < 2e-3, "target 0.847 at n=100")
rec(abs(ratios[1000] - 0.949) < 2e-3, "target 0.949 at n=1000")
rec(abs(ratios[3000] - 0.970) < 2e-3, "target 0.970 at n=3000")
print(f"  target quoted 0.847 / 0.949 / 0.970 at n=100/1000/3000: "
      f"{ratios[100]:.3f} / {ratios[1000]:.3f} / {ratios[3000]:.3f}")
print(f"  NOTE: at the target's own T4c cells n=10000 and n=30000 the ratio "
      f"is {ratios[10000]:.4f} and {ratios[30000]:.4f} > 0.9700 -- see "
      f"REFEREE_REPORT.md finding on the 'max LHS/RHS = 0.970' claim.")

print(f"== R5 SUMMARY: {checks} checks, {fails} failures, "
      f"elapsed {time.time()-t0:.0f}s ==")
sys.exit(1 if fails else 0)
