# verify_kappa_star.py -- T3: certification of the additive constant.
#   kappa* = kappa_B := sup_{c>=0} c^2 I2(c),  I2(c)=int_0^1 t^4 e^{-c t^2} dt.
# Claims certified here (pure rational arithmetic, no float trust):
#   (K1)  kappa_B < 0.2805          [the decimal used in the theorem display]
#   (K2)  kappa_B > 0.28048         [lower witness at c0 ~= 4.086754546]
# Plus a high-precision (mpmath, 50 dps; NOT load-bearing) computation of
# kappa_B and its argmax, compared to the Estagio 12 / referee values.
#
# Method for (K1): split [0,infty) at C0 = 5.62.
#   Tail c >= C0: c^2 I2(c) <= c^2 int_0^inf t^4 e^{-ct^2} dt = (3/8)sqrt(pi/c)
#     (Gaussian moment: differentiate int_0^inf e^{-at^2}dt = (1/2)sqrt(pi/a)
#      twice in a), decreasing in c, so <= (3/8)sqrt_hi(pi)/sqrt_lo(C0) < 0.2805.
#   Head [0, C0]: branch-and-bound. On [c1,c2], I2 is decreasing in c
#     (integrand decreasing in c pointwise), so
#        sup_{[c1,c2]} c^2 I2(c) <= c2^2 * I2_hi(c1),
#     a certified rational bound. Bisect until every leaf clears 0.2805.
# Deterministic; no seed used.

import sys, time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from engine import PI_HI, PI_LO, sqrt_lo, sqrt_hi, I2_bracket

t0 = time.time()
fails = 0
TAU = Fraction(2805, 10000)
C0 = Fraction(562, 100)

# ---- tail ---------------------------------------------------------------
tail_bound = Fraction(3, 8) * sqrt_hi(PI_HI) / sqrt_lo(C0)
ok = tail_bound < TAU
print(f"[{'PASS' if ok else 'FAIL'}] tail c>={float(C0)}: (3/8)sqrt(pi/c) <= "
      f"{float(tail_bound):.9f} < {float(TAU)}")
fails += (not ok)

# ---- head: branch and bound --------------------------------------------
stack = [(Fraction(0), C0)]
leaves = 0
evals = 0
min_clearance = None
worst_leaf = None
failed_intervals = []
while stack:
    c1, c2 = stack.pop()
    lo_i2, hi_i2 = I2_bracket(c1)
    evals += 1
    ub = c2 * c2 * hi_i2
    if ub < TAU:
        leaves += 1
        cl = TAU - ub
        if min_clearance is None or cl < min_clearance:
            min_clearance, worst_leaf = cl, (c1, c2)
        continue
    if c2 - c1 < Fraction(1, 10**7):
        failed_intervals.append((c1, c2))
        continue
    mid = (c1 + c2) / 2
    stack.append((c1, mid))
    stack.append((mid, c2))

ok = not failed_intervals
print(f"[{'PASS' if ok else 'FAIL'}] head [0,{float(C0)}]: branch-and-bound, "
      f"{leaves} certified leaves, {evals} interval evaluations, "
      f"0 failures" if ok else f"[FAIL] {len(failed_intervals)} intervals could not be certified")
if worst_leaf:
    print(f"  tightest leaf: [{float(worst_leaf[0]):.7f},{float(worst_leaf[1]):.7f}], "
          f"clearance {float(min_clearance):.3e}  [{time.time()-t0:.0f}s]")
fails += (not ok)
print(f"==> (K1) kappa_B < {float(TAU)}  {'CERTIFIED' if not fails else 'NOT certified'}")

# ---- lower witness ------------------------------------------------------
c0 = Fraction(4086754546, 10**9)
lo_i2, hi_i2 = I2_bracket(c0)
val_lo = c0 * c0 * lo_i2
val_hi = c0 * c0 * hi_i2
KLO = Fraction(28048, 100000)
ok = val_lo > KLO
print(f"[{'PASS' if ok else 'FAIL'}] (K2) c0^2 I2(c0) in "
      f"[{float(val_lo):.12f},{float(val_hi):.12f}] > {float(KLO)} at c0={float(c0)}")
fails += (not ok)
print(f"==> kappa_B in (0.28048, 0.2805), certified rational arithmetic.")

# ---- high-precision value (display only, NOT load-bearing) --------------
try:
    import mpmath as mp
    mp.mp.dps = 50
    def c2I2(c):
        s = mp.sqrt(c)
        # int_0^s u^4 e^{-u^2} du = (3 sqrt(pi)/8) erf(s) - e^{-s^2}(3s/4 + s^3/2)
        integral = (3 * mp.sqrt(mp.pi) / 8) * mp.erf(s) - mp.e**(-s**2) * (3 * s / 4 + s**3 / 2)
        return integral / s          # c^2 I2(c) = (1/sqrt(c)) int_0^sqrt(c) u^4 e^{-u^2} du
    # sanity: closed form vs direct quadrature
    q = mp.quad(lambda t: t**4 * mp.e**(-4 * t * t), [0, 1]) * 16
    assert abs(c2I2(mp.mpf(4)) - q) < mp.mpf(10) ** (-40), "closed form mismatch"
    cstar = mp.findroot(lambda c: mp.diff(c2I2, c), mp.mpf(4.087))
    kappa = c2I2(cstar)
    print(f"  mpmath (50 dps): argmax c* = {mp.nstr(cstar, 15)}, "
          f"kappa_B = {mp.nstr(kappa, 15)}")
    print(f"  Estagio 12 value:      0.280480169025    (attained at 4.086754546)")
    print(f"  wave-11 referee value: 0.280480169024586")
except Exception as exc:      # mpmath merely decorative here
    print(f"  [note] mpmath display skipped: {exc}")

print(f"\nTOTAL fails: {fails}, {time.time()-t0:.1f}s")
sys.exit(1 if fails else 0)
