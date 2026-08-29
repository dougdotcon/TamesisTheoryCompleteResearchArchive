"""
s02c_kernel_uniformity_xnonzero.py

TAUBERIAN-OSCILLATION-BOUND-ATTEMPT, wave 26 front (c).

Quick supplementary check: does hypothesis (U) [closed-form kernel error
stays O(1/z^2), uniformly across h/y ratio] ALSO hold at a NONZERO x, not
just x=0 (as s02/s02b tested)? This partially supports the x-uniformity
claim (ingredient (ii)(a) in the main document): the analytic bound in s01
is, by construction, automatically non-increasing in x for x>=0 GIVEN (U)
holds at that x -- this script spot-checks (U) itself away from x=0.

Written FRESH, same de-stiffened quadrature approach as s02/s02b.
"""
import mpmath as mp
import time

mp.mp.dps = 30

def f(xx):
    return 1 / (1 + xx)

def inner_theta(hp, z, x, fn):
    def integrand(w):
        u = w / z
        return mp.e ** (-(u * u) / 2 - w) * fn(x + hp + u)
    return (mp.mpf(1) / z) * mp.quad(integrand, [0, 1, 3, 8, 20, 45, 80])

def hp_breakpoints(h, eps):
    pts = [0]
    for m in (0.5, 1, 3, 8, 20, 50):
        p = m * eps
        if 0 < p < h:
            pts.append(p)
    pts.append(h)
    return sorted(set(pts))

def K_full(y, t, x, eps, fn):
    h = y - t
    z = x + y
    My = (1 - eps * z) / eps
    bpts = hp_breakpoints(h, eps)
    KAraw = mp.quad(lambda hp: mp.e ** (-hp / eps) * inner_theta(hp, z, x, fn), bpts)
    KB = mp.quad(lambda v: mp.e ** (-v / eps) * fn(x + v), bpts)
    return My * KAraw + KB

def predicted(y, t, x, eps, fn):
    h = y - t
    z = x + y
    return (fn(x) - mp.e ** (-h / eps) * fn(x + h)) / z

print("=" * 90)
print("x=3 (nonzero), eps=0.1, z:=x+y so y=z-3, f=1/(1+x), ratios h/y=0.1,0.5,0.9")
print("=" * 90)
eps = mp.mpf('0.1')
x0 = mp.mpf(3)
for zz in (200, 1000):
    z = mp.mpf(zz)
    y_ = z - x0
    for r in (mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('0.9')):
        h_ = r * y_
        t_ = y_ - h_
        t0 = time.time()
        kf = K_full(y_, t_, x0, eps, f)
        pr = predicted(y_, t_, x0, eps, f)
        err = kf - pr
        z2err = z * z * err
        print(f"z={zz:5d} ratio={float(r):.2f}  K*z={float(kf*z):.6f}  "
              f"pred*z={float(pr*z):.6f}  z^2*err={float(z2err):.4f}  "
              f"({time.time()-t0:.1f}s)")

print()
print("Compare against x=0 values at the SAME z (from s02/s02b, f=1/(1+x)):")
print("  z=100 (x=0): z^2*err = -0.9004 (all ratios)")
print("  -> here at x=3, z^2*err should be of similar magnitude/sign,")
print("     consistent with (U) holding away from x=0 too (not a proof of")
print("     uniformity for ALL x, but a spot-check against a specific")
print("     alternative failure mode: (U) breaking down as soon as x!=0).")
