# ref_check_kappa.py -- referee check R3: kappa_B in (0.28048, 0.2805),
# by the referee's OWN method (independent of the target's script).
#
# kappa_B = sup_{c>=0} f(c),  f(c) = c^2 I2(c),  I2(c)=int_0^1 t^4 e^{-ct^2}dt.
#
# R3a (upper, tail):  f(c) <= c^2 * int_0^inf t^4 e^{-ct^2} dt
#                          = (3/8) sqrt(pi/c)   [Gaussian 4th moment],
#     decreasing in c; certified value at c=5.62 (and 6) < 0.2805.
# R3b (upper, head [0,5.62]): adaptive branch-and-bound with the certified
#     interval bound  sup_{[c1,c2]} f <= c2^2 * I2_hi(c1)
#     (valid because I2 is decreasing in c: e^{-c t^2} decreasing in c).
# R3c (lower): certified witness at c0 = 4.086754546:
#     f(c0) > 0.28048 via exact-series bracket of I2(c0).
# R3d (display, NON-load-bearing): mpmath 50dps argmax + value, to compare
#     with the target's 0.280480169024586 @ 4.08675454645254.
import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import I2_bracket, sqrt_bracket, PI_LO, PI_HI, SQRT_PI_HI

t0 = time.time()
fails = 0
checks = 0
def rec(ok, msg):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("  ** FAIL:", msg)

TARGET = F(2805, 10**4)

print("== R3a: tail bound ==")
# (3/8) sqrt(pi/c) at c=5.62, certified upper value:
for cc in [F(562, 100), F(6)]:
    val_hi = F(3, 8) * sqrt_bracket(PI_HI / cc)[1]
    rec(val_hi < TARGET, f"tail at c={cc}")
    print(f"  (3/8)sqrt(pi/{cc}) <= {float(val_hi):.7f} < 0.2805 :",
          val_hi < TARGET)
# check the target's own printed tail number 0.2803742 at 5.62
v = F(3, 8) * sqrt_bracket(PI_HI / F(562, 100))[1]
print(f"  (target printed 0.2803742; referee gets {float(v):.7f})")

print("== R3b: head [0, 5.62], adaptive branch-and-bound ==")
leaves = 0
evals = 0
worst_clear = (F(1), None)
stack = [(F(0), F(562, 100))]
I2hi_cache = {}
def I2hi(c):
    global evals
    if c not in I2hi_cache:
        I2hi_cache[c] = I2_bracket(c)[1]
        evals += 1
    return I2hi_cache[c]
maxdepth_hit = False
while stack:
    c1, c2 = stack.pop()
    bound = c2 * c2 * I2hi(c1)
    if bound < TARGET:
        leaves += 1
        clear = TARGET - bound
        if clear < worst_clear[0]:
            worst_clear = (clear, (c1, c2))
        continue
    if c2 - c1 < F(1, 10**7):
        maxdepth_hit = True
        break
    mid = (c1 + c2) / 2
    stack.append((c1, mid))
    stack.append((mid, c2))
rec(not maxdepth_hit, "branch-and-bound converged")
print(f"  leaves={leaves}, I2 interval evals={evals}, "
      f"converged={not maxdepth_hit}")
print(f"  tightest leaf clearance {float(worst_clear[0]):.3e} on "
      f"[{float(worst_clear[1][0]):.6f},{float(worst_clear[1][1]):.6f}]")
print(f"  => kappa_B < 0.2805 CERTIFIED (head+tail), "
      f"elapsed {time.time()-t0:.0f}s")

print("== R3c: lower witness ==")
c0 = F(4086754546, 10**9)
lo, hi = I2_bracket(c0)
f_lo = c0 * c0 * lo
f_hi = c0 * c0 * hi
rec(f_lo > F(28048, 10**5), "witness > 0.28048")
print(f"  f({float(c0)}) in ({float(f_lo):.15f}, {float(f_hi):.15f})")
print(f"  > 0.28048 :", f_lo > F(28048, 10**5))
rec(f_hi < TARGET, "witness < 0.2805 (consistency)")

print("== R3d: display value (mpmath 50 dps, NON-load-bearing) ==")
import mpmath as mp
mp.mp.dps = 50
def f_mp(c):
    c = mp.mpf(c)
    # closed form: c^2 I2(c) = c^{-1/2}[ (3 sqrt(pi)/8) erf(sqrt c)
    #                                  - e^{-c}(3 sqrt(c)/4 + c^{3/2}/2) ]
    s = mp.sqrt(c)
    return (mp.mpf(3) / 8 * mp.sqrt(mp.pi) * mp.erf(s)
            - mp.e**(-c) * (3 * s / 4 + c * s / 2)) / s
def f_quad(c):
    return c**2 * mp.quad(lambda t: t**4 * mp.e**(-c * t * t), [0, 1])
# cross-check closed form vs direct quadrature
d = abs(f_mp(mp.mpf(4)) - f_quad(mp.mpf(4)))
rec(d < mp.mpf(10)**(-40), "closed form vs quadrature")
print(f"  |closed-form - quadrature| at c=4: {mp.nstr(d, 3)}")
# maximize: solve f'(c)=0 by golden/ternary refinement
a, b = mp.mpf(3.5), mp.mpf(4.7)
for _ in range(220):
    m1 = a + (b - a) / 3
    m2 = b - (b - a) / 3
    if f_mp(m1) < f_mp(m2):
        a = m1
    else:
        b = m2
cstar = (a + b) / 2
print(f"  argmax c* = {mp.nstr(cstar, 15)}")
print(f"  kappa_B   = {mp.nstr(f_mp(cstar), 15)}")
print(f"  (target: c*=4.08675454645254, kappa_B=0.280480169024586)")
rec(abs(cstar - mp.mpf('4.08675454645254')) < mp.mpf('1e-10'), "c* match")
rec(abs(f_mp(cstar) - mp.mpf('0.280480169024586')) < mp.mpf('1e-14'),
    "kappa_B display match")

print(f"== R3 SUMMARY: {checks} checks, {fails} failures, "
      f"elapsed {time.time()-t0:.0f}s ==")
sys.exit(1 if fails else 0)
