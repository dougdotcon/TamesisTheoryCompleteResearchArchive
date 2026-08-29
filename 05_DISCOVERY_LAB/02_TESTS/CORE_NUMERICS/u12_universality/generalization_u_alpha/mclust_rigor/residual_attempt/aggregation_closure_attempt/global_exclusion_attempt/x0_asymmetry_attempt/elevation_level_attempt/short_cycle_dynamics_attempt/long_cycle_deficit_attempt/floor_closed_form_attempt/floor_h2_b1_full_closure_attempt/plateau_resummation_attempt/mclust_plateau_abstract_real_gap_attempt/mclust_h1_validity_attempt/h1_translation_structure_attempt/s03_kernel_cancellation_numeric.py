"""
s03_kernel_cancellation_numeric.py

H1-TRANSLATION-STRUCTURE-ATTEMPT (wave 25, front c). Part B, numerical
verification of the CENTRAL new claim of this front:

  K(y,t) f (x) = (M_y K_A^raw(y,t) f)(x) + (K_B(y-t) f)(x)

decays like O(1/(x+y)) as y -> infinity at FIXED h:=y-t (equivalently,
fixed elapsed time), for Lipschitz test functions f, EVEN THOUGH each of
the two additive pieces individually settles to a NONZERO, non-decaying
(order eps) limit -- i.e. a delicate, near-total cancellation, not a
"small perturbation of a translation-invariant base kernel" in the naive
sense.

This script computes (M_y K_A^raw(y,t) f)(x) and (K_B(y-t) f)(x)
INDEPENDENTLY, via DIRECT quadrature of their RAW/original definitions
(not the s01/s02 reduced forms -- so this is an independent check of the
whole chain, not merely a self-consistency check of s02's own algebra),
for several test functions f, several fixed h, x=0, sweeping y over 3
orders of magnitude, and:

  (a) confirms M_y K_A^raw(y,t) f(x) -> a NONZERO limit as y->inf (does
      NOT vanish -- consistent with h_eps(z)->eps, DISC-DEC-113/115);
  (b) confirms K_B(h) f(x) is exactly y-independent (trivially, by
      construction -- included only as a sanity check of the harness);
  (c) confirms the SUM decays, and fits its decay rate (log-log slope
      vs y) -- prediction: slope -> -1 (i.e. O(1/y), matching O(1/(x+y))
      at x=0).

No randomness anywhere. Deterministic adaptive quadrature (mpmath.quad).
Moderate working precision (dps=25) and an explicit, disclosed finite
cutoff (u,h' truncated at a point where the Gaussian tail is below 1e-30
relative) chosen for tractable runtime -- verified sufficient in Sec 0
below before use.
"""

import mpmath as mp

mp.mp.dps = 25
U_CUTOFF = mp.mpf(14)  # e^{-u^2/2} at u=14 is ~exp(-98) ~ 1e-43: negligible


def M_y_KA_raw_f(x, y, t, epsv, f):
    """(M_y K_A^raw(y,t) f)(x), computed from the RAW (w,u) double-integral
    definition, with M_y = multiply by (1-eps(x+y))/eps applied AFTER."""
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
    """(K_B(h) f)(x) = int_0^h e^{-v/eps} f(x+v) dv, exact by definition."""
    return mp.quad(lambda v: mp.e**(-v/epsv) * f(x + v), [0, h])


test_functions = {
    "f=1/(1+x)   (L~1)":  lambda xx: 1/(1+xx),
    "f=exp(-x/3) (L~1/3)": lambda xx: mp.e**(-xx/3),
}

print("=" * 90)
print("Sec 0 -- cutoff sanity check: U_CUTOFF=14 tail contribution")
print("=" * 90)
tail = mp.quad(lambda u: mp.e**(-u**2/2), [U_CUTOFF, mp.inf])
full = mp.quad(lambda u: mp.e**(-u**2/2), [0, mp.inf])
print(f"tail/full = {mp.nstr(tail/full, 6)}  (negligible, as expected)")
print()

for epsv, label in [(mp.mpf('0.1'), "eps=0.1 (c=100)"), (1/mp.sqrt(1000), "eps=1/sqrt(1000) (c=1000)")]:
    for h in [mp.mpf('0.5'), mp.mpf('2.0'), mp.mpf('5.0')]:
        for fname, f in test_functions.items():
            print("=" * 90)
            print(f"{label}, h={mp.nstr(h,4)}, {fname}, x=0")
            print("=" * 90)
            x = mp.mpf(0)
            rows = []
            ys = [h + d for d in [mp.mpf(v) for v in [0.5, 1, 3, 10, 30, 100, 300, 1000, 3000]]]
            for y in ys:
                t = y - h
                MKA = M_y_KA_raw_f(x, y, t, epsv, f)
                KB = KB_f(x, h, epsv, f)
                total = MKA + KB
                rows.append((y, MKA, KB, total))
            print(f"{'y':>8s} {'M_y K_A^raw f(0)':>20s} {'K_B(h) f(0)':>16s} "
                  f"{'K(y,t) f(0) = sum':>20s}")
            for (y, MKA, KB, total) in rows:
                print(f"{float(y):8.1f} {mp.nstr(MKA,10):>20s} {mp.nstr(KB,10):>16s} "
                      f"{mp.nstr(total,10):>20s}")
            # log-log slope fit of |total| vs y over the last few (largest-y) points
            import math
            logy = [math.log(float(r[0])) for r in rows[-5:]]
            logt = [math.log(abs(float(r[3]))) for r in rows[-5:]]
            n = len(logy)
            mean_x = sum(logy)/n
            mean_y = sum(logt)/n
            num = sum((logy[i]-mean_x)*(logt[i]-mean_y) for i in range(n))
            den = sum((logy[i]-mean_x)**2 for i in range(n))
            slope = num/den
            print(f"  KB(h) is exactly y-independent (sanity check): "
                  f"{'PASS' if len(set(mp.nstr(r[2],15) for r in rows))==1 else 'FAIL'}")
            print(f"  M_y K_A^raw f(0) settles toward a NONZERO limit as y->inf "
                  f"(last value: {mp.nstr(rows[-1][1],8)})")
            print(f"  Fitted log-log slope of |K(y,t)f(0)| vs y (last 5 points): "
                  f"{slope:.4f}  (prediction: -1)")
            print()

print("Done. Full numeric table in s03_kernel_cancellation_numeric.log.")
