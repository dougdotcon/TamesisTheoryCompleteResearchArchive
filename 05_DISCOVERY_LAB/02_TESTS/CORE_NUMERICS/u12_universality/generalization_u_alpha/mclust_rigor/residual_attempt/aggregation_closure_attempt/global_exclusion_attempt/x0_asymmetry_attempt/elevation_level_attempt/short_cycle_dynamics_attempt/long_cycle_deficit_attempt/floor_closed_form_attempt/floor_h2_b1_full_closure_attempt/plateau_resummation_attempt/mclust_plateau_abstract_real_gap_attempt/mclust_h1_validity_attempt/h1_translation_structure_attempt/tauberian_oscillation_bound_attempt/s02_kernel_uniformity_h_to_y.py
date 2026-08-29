"""
s02_kernel_uniformity_h_to_y.py

TAUBERIAN-OSCILLATION-BOUND-ATTEMPT, wave 26 front (c).

Numerically tests hypothesis (U) named in s01: is the closed-form kernel's
O(1/z^2) remainder uniform in h over the FULL range h in [0,y] -- including
h/y -> 1 (i.e. t -> 0, the "old" part of the Volterra history) -- and not
merely for h growing proportionally at a FIXED ratio h=y/2 as
h1_translation_structure_attempt (DISC-DEC-122) Sec 5.4 tested?

This is essential for the T1 bound in s01: the derivation there integrates
over t in [0,y1], i.e. h1=y1-t ranges over the FULL interval [0,y1],
including h1 close to y1 (t close to 0) -- a regime never tested by any
ancestor front.

Written FRESH: raw kernel definitions (K_A^raw single-integral reduction,
K_B, M_y) re-implemented from the mathematical formulas quoted (as cited,
proved facts of record) in the required reading -- no ancestor .py file
opened or imported. De-stiffening substitution (u=w/z for the inner
integral) used throughout, per this lineage's own established discipline
against naive scipy.integrate.quad failures at large z (confirmed
catastrophic, ~6 orders of magnitude, by h1_translation_structure_attempt's
own referee).
"""
import mpmath as mp
import time

mp.mp.dps = 30

def make_f(kind):
    if kind == 'rational':
        return lambda xx: 1 / (1 + xx)
    elif kind == 'expdecay':
        return lambda xx: mp.e ** (-xx / mp.mpf(3))
    else:
        raise ValueError(kind)

def inner_theta(hp, z, x, f):
    """Theta_{h'}(z) = int_0^inf e^{-u^2/2-uz} f(x+h'+u) du,
    de-stiffened via u = w/z (mass concentrates near u~1/z for large z)."""
    def integrand(w):
        u = w / z
        return mp.e ** (-(u * u) / 2 - w) * f(x + hp + u)
    # breakpoints in w to help adaptive quadrature see the e^{-w} decay
    return (mp.mpf(1) / z) * mp.quad(integrand, [0, 1, 3, 8, 20, 45, 80])

def hp_breakpoints(h, eps):
    """Breakpoints for the outer h'-integral over [0,h], concentrating
    nodes near h'=0 where e^{-h'/eps} has its mass (width ~eps)."""
    pts = [0]
    for m in (0.5, 1, 3, 8, 20, 50):
        p = m * eps
        if p < h:
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

print("=" * 90)
print("SANITY CHECK: cross-validate against h1_translation_structure_attempt's own")
print("published Sec 5.4 value at x=0,eps=0.1,f=1/(1+x),h=y/2,y=10 (quoted verbatim)")
print("published: z*K(y,t)f(0) = 0.9156333394  at y=10 (so t=5, h=5, z=10)")
print("=" * 90)
eps = mp.mpf('0.1')
f1 = make_f('rational')
t0 = time.time()
y, h = mp.mpf(10), mp.mpf(5)
t_ = y - h
val = K_full(y, t_, 0, eps, f1)
z = y
print(f"this front's independent value: z*K(y,t)f(0) = {float(z*val):.10f}   "
      f"(took {time.time()-t0:.1f}s)")
diff = abs(z * val - mp.mpf('0.9156333394'))
print(f"absolute difference from published value: {float(diff):.3e}")
status = "PASS (agrees to published precision)" if diff < mp.mpf('1e-6') else "CHECK"
print(f"-> {status}")
print()

print("=" * 90)
print("MAIN TEST: sweep h/y ratio from 0.1 up to 0.999 (h1 -> y1, i.e. t -> 0)")
print("at several FIXED z=x+y, checking whether z^2*(K_full - predicted) stays")
print("BOUNDED (not blowing up) uniformly across the WHOLE ratio range.")
print("=" * 90)
x0 = mp.mpf(0)
ratios = [mp.mpf(r) for r in ('0.1', '0.3', '0.5', '0.7', '0.9', '0.95', '0.99')]
zs = [mp.mpf(zz) for zz in (100, 500, 2000)]

results = {}
for fname in ('rational', 'expdecay'):
    f = make_f(fname)
    print(f"\n--- test function: {fname} ---")
    print(f"{'z':>6} {'h/y':>6} {'K_full*z':>14} {'predicted*z':>14} "
          f"{'z^2*err':>14} {'rel.err (of K)':>14}")
    for zz in zs:
        y_ = zz - x0
        for r in ratios:
            h_ = r * y_
            t_ = y_ - h_
            kf = K_full(y_, t_, x0, eps, f)
            pr = predicted(y_, t_, x0, eps, f)
            err = kf - pr
            z2err = zz * zz * err
            relerr = err / kf if kf != 0 else mp.nan
            results[(fname, float(zz), float(r))] = (float(kf), float(pr),
                                                       float(z2err), float(relerr))
            print(f"{float(zz):6.0f} {float(r):6.3f} {float(kf*zz):14.6f} "
                  f"{float(pr*zz):14.6f} {float(z2err):14.6f} {float(relerr):14.3e}")

print()
print("=" * 90)
print("ANALYSIS: does z^2*err stay bounded (not diverging) as ratio -> 1, at each z?")
print("=" * 90)
for fname in ('rational', 'expdecay'):
    print(f"\n--- {fname} ---")
    for zz in (100.0, 500.0, 2000.0):
        vals = [results[(fname, zz, float(r))][2] for r in ratios]
        vmax = max(abs(v) for v in vals)
        print(f"  z={zz:7.0f}: z^2*err across ratios = "
              f"[{', '.join(f'{v:8.4f}' for v in vals)}]  "
              f"max|z^2*err|={vmax:.4f}")
