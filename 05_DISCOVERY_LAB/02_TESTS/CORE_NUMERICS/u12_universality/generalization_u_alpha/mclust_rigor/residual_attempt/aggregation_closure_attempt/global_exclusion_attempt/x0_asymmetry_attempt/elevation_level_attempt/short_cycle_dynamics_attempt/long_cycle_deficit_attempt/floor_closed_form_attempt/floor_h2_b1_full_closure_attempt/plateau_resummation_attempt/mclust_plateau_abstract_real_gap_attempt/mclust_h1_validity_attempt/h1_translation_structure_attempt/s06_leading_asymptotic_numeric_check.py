"""
s06_leading_asymptotic_numeric_check.py

H1-TRANSLATION-STRUCTURE-ATTEMPT. Independently verifies the CLOSED-FORM
leading asymptotic derived and symbolically checked in s05:

  K(y,t) f(x)  ~  [ f(x) - e^{-h/eps} f(x+h) ] / z  + O(1/z^2),   z:=x+y, h:=y-t

by computing z * K(y,t) f(x) via DIRECT quadrature of the RAW operator
definitions (same method as s03/s04, independent of s05's symbolic route)
at a sequence of increasing z, and checking convergence to the predicted
closed-form value f(x) - e^{-h/eps} f(x+h) -- not just the 1/z ORDER
(already confirmed in s03/s04), but the exact leading COEFFICIENT.

Also performs Richardson extrapolation (using the now-established O(1/z)
leading + implied O(1/z^2) next-order structure) to sharpen the z->infinity
estimate from finite-z data, and reports the extrapolated value against
the closed-form prediction.

No randomness. Deterministic quadrature (mpmath).
"""

import mpmath as mp

mp.mp.dps = 30
U_CUTOFF = mp.mpf(15)


def M_y_KA_raw_f(x, y, t, epsv, f):
    def outer(w):
        xprime = x + y - w
        def inner(u):
            return mp.e**(-u**2/2 - u*(xprime + w)) * f(xprime + u)
        Tw = mp.quad(inner, [0, U_CUTOFF])
        return mp.e**(-(y - w)/epsv) * Tw
    KAraw = mp.quad(outer, [t, y])
    My_factor = (1 - epsv*(x + y)) / epsv
    return My_factor * KAraw


def KB_f(x, h, epsv, f):
    return mp.quad(lambda v: mp.e**(-v/epsv) * f(x + v), [0, h])


def K_full(x, y, t, epsv, f):
    return M_y_KA_raw_f(x, y, t, epsv, f) + KB_f(x, y - t, epsv, f)


cases = [
    # (x, h, eps, fname, f)
    (0.0, 0.5, 0.1, "f=1/(1+x)", lambda xx: 1/(1+xx)),
    (0.0, 2.0, 0.1, "f=1/(1+x)", lambda xx: 1/(1+xx)),
    (1.0, 2.0, 0.1, "f=1/(1+x)", lambda xx: 1/(1+xx)),
    (0.0, 2.0, 1/mp.sqrt(1000), "f=1/(1+x)", lambda xx: 1/(1+xx)),
    (0.0, 2.0, 0.1, "f=exp(-x/3)", lambda xx: mp.e**(-xx/3)),
    (2.0, 5.0, 0.1, "f=exp(-x/3)", lambda xx: mp.e**(-xx/3)),
]

print(f"{'x':>5s} {'h':>5s} {'eps':>10s} {'f':>12s}  {'z':>8s} {'z*K(y,t)f(x)':>16s}  "
      f"{'predicted limit':>18s} {'rel.err':>10s}")
print("-" * 100)

results_summary = []
for (x, h, epsv, fname, f) in cases:
    x = mp.mpf(x); h = mp.mpf(h); epsv = mp.mpf(epsv)
    predicted = f(x) - mp.e**(-h/epsv) * f(x + h)
    zs = [mp.mpf(v) for v in [10, 30, 100, 300, 1000, 3000, 10000]]
    vals = []
    for z in zs:
        y = z - x
        t = y - h
        if t < 0:
            continue
        Kval = K_full(x, y, t, epsv, f)
        scaled = z * Kval
        vals.append((z, scaled))
        rel = abs(scaled - predicted) / (abs(predicted) if predicted != 0 else 1)
        print(f"{float(x):5.1f} {float(h):5.1f} {float(epsv):10.5f} {fname:>12s}  "
              f"{float(z):8.1f} {mp.nstr(scaled,10):>16s}  "
              f"{mp.nstr(predicted,10):>18s} {mp.nstr(rel,4):>10s}")
    # Richardson extrapolation assuming z*K = predicted + A/z + O(1/z^2):
    # use last two points (z1,v1),(z2,v2): predicted_extrap = (z2*v2 - z1*v1)/(z2-z1)
    if len(vals) >= 2:
        (z1, v1), (z2, v2) = vals[-2], vals[-1]
        extrap = (z2*v2 - z1*v1) / (z2 - z1)
        rel_extrap = abs(extrap - predicted) / (abs(predicted) if predicted != 0 else 1)
        print(f"      Richardson extrapolation (last 2 pts): {mp.nstr(extrap,10)}  "
              f"vs predicted {mp.nstr(predicted,10)}   rel.err={mp.nstr(rel_extrap,4)}")
        results_summary.append((x, h, epsv, fname, predicted, vals[-1][1], extrap, rel_extrap))
    print()

print("=" * 100)
print("SUMMARY")
print("=" * 100)
worst = mp.mpf(0)
for (x, h, epsv, fname, predicted, last_val, extrap, rel_extrap) in results_summary:
    worst = max(worst, rel_extrap)
    print(f"x={float(x):.1f} h={float(h):.1f} eps={float(epsv):.5f} {fname:>12s}: "
          f"Richardson-extrapolated z*K -> {mp.nstr(extrap,8)}, "
          f"predicted {mp.nstr(predicted,8)}, rel.err {mp.nstr(rel_extrap,4)}")
print(f"\nWorst Richardson-extrapolated relative error across {len(results_summary)} cases: "
      f"{mp.nstr(worst,4)}")
print("\nA small (<1%) Richardson-extrapolated relative error at EVERY case confirms")
print("the closed-form formula K(y,t)f(x) ~ [f(x)-e^{-h/eps}f(x+h)]/z, not merely")
print("its 1/z ORDER (already independently confirmed in s03/s04).")
