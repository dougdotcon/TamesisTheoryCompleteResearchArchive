#!/usr/bin/env python3
"""
s04_kink_sharpness_stress_test.py -- wave 29 front (a), CU-DIRECT-PROOF-ATTEMPT

DECISIVE numerical sharpness check of the finding from s02/s03: does the
closed-form kernel's remainder genuinely need (C'') [f' Lipschitz, i.e. f
in C^{1,1}], or does mere (C') [f itself merely Lipschitz, e.g. with a
kink in f'] still happen to give the O(1/z^2) rate empirically (in which
case the s02/s03 proof route would just be a non-sharp PROOF TECHNIQUE
limitation, not a genuine mathematical obstruction)?

Method: a FRESH (from-scratch, no ancestor-code import), independently
re-implemented raw-kernel evaluator (K_A^raw via the single-integral
reduction -- an already-established, twice-independently-verified record
fact, reused here as a cited FORMULA per this lineage's own discipline,
not as imported code) computes z^2*[K(y,t)f(x) - (f(x)-e^{-h/eps}f(x+h))/z]
for TWO test functions sharing the same sup-norm and Lipschitz bound:

  f_smooth(a) := 1/(1+a)                              [C^infty, baseline]
  f_kink(a)   := 1/(1+a) + 0.3*|a-3|                   [Lipschitz-only,
                                                         genuine kink in f'
                                                         at a=3, NOT C^1]

across a wide z-sweep, at FIXED h/eps regime (so the kink at a=3 is
genuinely swept through by the h' integration for every z tested). If
(C') alone sufficed, both functions' z^2*err should stay bounded/converge
as z->infinity. If the s02/s03 analysis is right, f_kink's z^2*err should
GROW (unboundedly, or at least not converge) while f_smooth's stays
bounded -- i.e. f_kink's TRUE remainder order is genuinely worse than
O(1/z^2) (consistent with the O(1/z) upper bound s02/s03 derive as the
best available under (C') alone).

Sanity check first (mandatory discipline): reproduce a known cross-check
value from this sub-lineage's own record before trusting anything new.
"""
import mpmath as mp

mp.mp.dps = 40


def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi / 2) * mp.erfc(z / mp.sqrt(2)) * mp.exp(z ** 2 / 2)


def raw_kernel_Kf(f, x, y, t, eps):
    """
    Fresh, from-scratch implementation of K(y,t)f(x) = M_y*K_A^raw(y,t)f(x)
    + K_B(y-t)f(x), using the single-integral reduction of K_A^raw (a
    record fact, re-derived independently by three prior fronts in this
    exact sub-lineage -- reused here as a CITED FORMULA, not imported
    code):
      K_A^raw(y,t)f(x) = int_0^h e^{-h'/eps} Theta_{h'}(z) dh'
      Theta_{h'}(z)    = int_0^inf e^{-u^2/2-uz} f(x+h'+u) du
      K_B(h)f(x)       = int_0^h e^{-v/eps} f(x+v) dv
      M_y              = (1-eps*z)/eps,   z:=x+y,  h:=y-t
    De-stiffened via substitution u=v/z for the inner integral (large z
    makes e^{-uz} decay on scale 1/z; substituting removes the stiffness),
    and geometric breakpoints for the outer h'-integral (concentrated near
    its own exponential decay scale eps) -- following the SAME de-stiffening
    discipline this sub-lineage's own record establishes as necessary
    (re-implemented fresh here, not copied).
    """
    x = mp.mpf(x); y = mp.mpf(y); t = mp.mpf(t); eps = mp.mpf(eps)
    z = x + y
    h = y - t

    def Theta(hp):
        hp = mp.mpf(hp)
        # inner integral via u = v/z substitution: int_0^inf e^{-u^2/2-uz} f(x+hp+u) du
        #   = (1/z) int_0^inf e^{-(v/z)^2/2 - v} f(x+hp+v/z) dv
        def integrand(v):
            u = v / z
            return mp.e**(-u**2/2 - v) * f(x + hp + u)
        return (1/z) * mp.quad(integrand, [0, 2, 8, 20, 50, 100, mp.inf])

    # geometric breakpoints for the outer integral, concentrated near the
    # exponential decay scale eps, capped at a fixed count regardless of h
    bps = [mp.mpf(0)]
    scale = eps / mp.mpf(4)
    while scale < h and len(bps) < 14:
        bps.append(scale)
        scale *= 2
    bps.append(h)
    bps = sorted(set(bps))

    def outer_integrand(hp):
        return mp.e**(-hp/eps) * Theta(hp)

    K_A_raw = mp.quad(outer_integrand, bps)
    M_y = (1 - eps*z) / eps
    K_B = mp.quad(lambda v: mp.e**(-v/eps) * f(x+v), bps)
    return M_y * K_A_raw + K_B


def closed_form_target(f, x, h, z, eps):
    return (f(x) - mp.e**(-h/eps) * f(x + h)) / z


print("=" * 78)
print("SANITY CHECK -- reproduce h1_translation_structure_attempt's published")
print("Sec 5.4 cross-check value: x=0,eps=0.1,f=1/(1+x),h=y/2,y=10")
print("published: z*K(y,t)f(0) = 0.9156333394")
print("=" * 78)
f1 = lambda a: 1/(1+a)
x0, eps0, y0 = mp.mpf(0), mp.mpf('0.1'), mp.mpf(10)
h0 = y0/2
t0 = y0 - h0
Kval = raw_kernel_Kf(f1, x0, y0, t0, eps0)
z0 = x0 + y0
print(f"fresh implementation: z*K(y,t)f(0) = {float(z0*Kval):.10f}")
print(f"published value:                     0.9156333394")
print(f"abs diff: {float(abs(z0*Kval - mp.mpf('0.9156333394'))):.3e}")
assert abs(z0*Kval - mp.mpf('0.9156333394')) < mp.mpf('1e-8')
print("CONFIRMED (matches to the precision the published value was quoted at).")
print()

print("=" * 78)
print("MAIN TEST -- z^2*[K(y,t)f(x) - target] for a SMOOTH vs a KINKED f,")
print("same regime as h_ces_direct_attempt's s03 stress test: x=0,eps=0.5,")
print("h=z/2 (i.e. y=z, t=y-h=z/2), z swept from 20 to 2000")
print("=" * 78)

f_smooth = lambda a: 1/(1+a)
f_kink = lambda a: 1/(1+a) + mp.mpf('0.3')*abs(a - 3)

x, eps = mp.mpf(0), mp.mpf('0.5')
zs = [mp.mpf(v) for v in [20, 50, 100, 200, 400, 800, 1600, 2000]]

print(f"{'z':>7} {'z^2*err smooth':>18} {'z^2*err kink':>18} "
      f"{'z*err smooth':>15} {'z*err kink':>15}")
smooth_z2err = []
kink_z2err = []
smooth_zerr = []
kink_zerr = []
for z in zs:
    y = z
    h = z/2
    t = y - h
    Ks = raw_kernel_Kf(f_smooth, x, y, t, eps)
    Kk = raw_kernel_Kf(f_kink, x, y, t, eps)
    Ts = closed_form_target(f_smooth, x, h, z, eps)
    Tk = closed_form_target(f_kink, x, h, z, eps)
    err_s = Ks - Ts
    err_k = Kk - Tk
    smooth_z2err.append(z**2 * err_s)
    kink_z2err.append(z**2 * err_k)
    smooth_zerr.append(z * err_s)
    kink_zerr.append(z * err_k)
    print(f"{float(z):7.0f} {float(z**2*err_s):18.6f} {float(z**2*err_k):18.6f} "
          f"{float(z*err_s):15.6f} {float(z*err_k):15.6f}")

print()
print("=" * 78)
print("ANALYSIS -- log-log slope of |err| vs z (last 4 points), each function")
print("=" * 78)

def loglog_slope(zs_, errs_):
    import math
    zs_f = [float(v) for v in zs_[-4:]]
    errs_f = [float(abs(v)) for v in errs_[-4:]]
    # crude least-squares slope of log|err| vs log(z)
    n = len(zs_f)
    lx = [math.log(v) for v in zs_f]
    ly = [math.log(v) for v in errs_f]
    mx = sum(lx)/n
    my = sum(ly)/n
    num = sum((lx[i]-mx)*(ly[i]-my) for i in range(n))
    den = sum((lx[i]-mx)**2 for i in range(n))
    return num/den

errs_smooth = [smooth_z2err[i]/zs[i]**2 for i in range(len(zs))]  # = err_s itself
errs_kink = [kink_z2err[i]/zs[i]**2 for i in range(len(zs))]
slope_smooth = loglog_slope(zs, errs_smooth)
slope_kink = loglog_slope(zs, errs_kink)
print(f"log-log slope of |err(z)| for f_smooth (expect ~ -2, i.e. O(1/z^2)): {slope_smooth:.4f}")
print(f"log-log slope of |err(z)| for f_kink   (expect ~ -1 if (C') alone,")
print(f"                                        NOT -2, per s02/s03's analysis): {slope_kink:.4f}")
print()
print("z^2*err trend for smooth f (should CONVERGE to a constant):",
      [float(v) for v in smooth_z2err])
print("z^2*err trend for kink f   (should GROW / not converge, per the analysis):",
      [float(v) for v in kink_z2err])
print()
print("z*err trend for kink f (should CONVERGE to a nonzero constant if the")
print("true rate for f_kink is genuinely O(1/z), matching s02/s03's derived")
print("upper bound being SHARP, not just a loose proof-technique artifact):")
print(" ", [float(v) for v in kink_zerr])
