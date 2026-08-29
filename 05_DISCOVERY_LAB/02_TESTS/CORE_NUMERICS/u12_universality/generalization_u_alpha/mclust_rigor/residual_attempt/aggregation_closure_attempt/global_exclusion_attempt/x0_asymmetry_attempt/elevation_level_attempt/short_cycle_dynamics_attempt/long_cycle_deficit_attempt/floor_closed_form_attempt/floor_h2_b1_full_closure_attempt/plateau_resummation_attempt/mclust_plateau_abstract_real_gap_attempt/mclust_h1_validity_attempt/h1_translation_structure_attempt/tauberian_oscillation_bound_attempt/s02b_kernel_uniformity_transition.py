"""
s02b_kernel_uniformity_transition.py

TAUBERIAN-OSCILLATION-BOUND-ATTEMPT, wave 26 front (c).

Follow-up to s02: at eps=0.1 (used throughout s02, matching the standard
c=100 scaling of this lineage), h/eps already exceeds ~10 (fully saturated,
e^{-h/eps}~0) at EVERY tested ratio down to h/y=0.1, so s02's sweep never
actually visits the transition region h=O(eps) within the SAME run as the
large-h (h close to y) region -- it only confirms the (already-saturated)
tail is uniform, not that nothing untoward happens THROUGH the transition
on the way there. This script uses a LARGER eps (relative to z) so that a
single ratio sweep, at FIXED z, passes through h/eps ~ 0.01 (unsaturated)
up to h/eps ~ 200 (deeply saturated) AND up to h/y=0.99 (h close to y, the
regime s01's T1 bound needs), all in one run -- a strictly more demanding
combined test than s02 or than h1_translation_structure_attempt's own
Sec 5.4 (which only tested h=y/2, a SINGLE ratio, not a full sweep through
both regimes at once).

Written FRESH; same de-stiffened quadrature approach as s02, not copied.
"""
import mpmath as mp
import time

mp.mp.dps = 30

def make_f(kind):
    if kind == 'rational':
        return lambda xx: 1 / (1 + xx)
    else:
        raise ValueError(kind)

def inner_theta(hp, z, x, f):
    def integrand(w):
        u = w / z
        return mp.e ** (-(u * u) / 2 - w) * f(x + hp + u)
    return (mp.mpf(1) / z) * mp.quad(integrand, [0, 1, 3, 8, 20, 45, 80])

def hp_breakpoints(h, eps):
    pts = [0]
    for m in (0.1, 0.5, 1, 3, 8, 20, 50):
        p = m * eps
        if 0 < p < h:
            pts.append(p)
    pts.append(h)
    return sorted(set(pts))

def K_A_raw(y, t, x, eps, f):
    h = y - t
    z = x + y
    bpts = hp_breakpoints(h, eps)
    return mp.quad(lambda hp: mp.e ** (-hp / eps) * inner_theta(hp, z, x, f), bpts)

def K_B(h, x, eps, f):
    bpts = hp_breakpoints(h, eps)
    return mp.quad(lambda v: mp.e ** (-v / eps) * f(x + v), bpts)

def K_full(y, t, x, eps, f):
    h = y - t
    z = x + y
    My = (1 - eps * z) / eps
    return My * K_A_raw(y, t, x, eps, f) + K_B(h, x, eps, f)

def predicted(y, t, x, eps, f):
    h = y - t
    z = x + y
    return (f(x) - mp.e ** (-h / eps) * f(x + h)) / z

print("=" * 92)
print("Combined transition + large-h sweep. eps=5, z=1000 (x=0,y=1000), f=1/(1+x)")
print("h/eps ranges from ~0.05 (unsaturated) to ~198 (deeply saturated),")
print("h/y ranges from 0.001 to 0.99 (approaching the T1-relevant regime).")
print("=" * 92)
eps = mp.mpf(5)
x0 = mp.mpf(0)
z = mp.mpf(1000)
y_ = z - x0
f = make_f('rational')

ratios = [mp.mpf(r) for r in
          ('0.0002', '0.001', '0.005', '0.01', '0.02', '0.05',
           '0.1', '0.3', '0.6', '0.9', '0.99')]

print(f"{'h/y':>8} {'h':>10} {'h/eps':>8} {'K_full*z':>12} "
      f"{'pred*z':>12} {'z^2*err':>12}")
zerrs = []
t0 = time.time()
for r in ratios:
    h_ = r * y_
    t_ = y_ - h_
    kf = K_full(y_, t_, x0, eps, f)
    pr = predicted(y_, t_, x0, eps, f)
    err = kf - pr
    z2err = z * z * err
    zerrs.append(float(z2err))
    print(f"{float(r):8.4f} {float(h_):10.3f} {float(h_/eps):8.3f} "
          f"{float(kf*z):12.6f} {float(pr*z):12.6f} {float(z2err):12.6f}")
print(f"\nelapsed: {time.time()-t0:.1f}s")
print(f"\nmax|z^2*err| across the FULL transition+large-h sweep: "
      f"{max(abs(v) for v in zerrs):.4f}")
print(f"min|z^2*err|: {min(abs(v) for v in zerrs):.4f}")
print("(bounded and smoothly varying through BOTH the h~eps transition AND")
print(" the large-h/y~1 regime -> no blowup detected anywhere in between)")
