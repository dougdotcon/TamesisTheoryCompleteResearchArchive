"""
s04_x_dependence_check.py

Supplementary check to s03: confirms the K(y,t)=O(1/(x+y)) claim is
governed by z=x+y (not by y alone), by repeating the same measurement at
several FIXED x>0 values, fixed h and eps, sweeping y. Prediction: the
fitted log-log slope of |K(y,t)f(x)| vs y should STILL be close to -1
(since for x fixed and y->infinity, z=x+y~y, same asymptotic regime), and
the ABSOLUTE magnitude of K(y,t)f(x) at matched y should be SMALLER for
larger x (since z=x+y is larger there) -- both checked directly.

No randomness. Deterministic quadrature (mpmath), same method as s03.
"""

import mpmath as mp
import math

mp.mp.dps = 25
U_CUTOFF = mp.mpf(14)


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


f = lambda xx: 1/(1+xx)
epsv = mp.mpf('0.1')
h = mp.mpf('2.0')

print(f"eps={float(epsv)}, h={float(h)}, f=1/(1+x) -- x-dependence of K(y,t)f(x) decay")
print()
for x in [mp.mpf(v) for v in [0, 1, 3, 10]]:
    ys = [h + d for d in [mp.mpf(v) for v in [1, 10, 100, 1000, 3000]]]
    totals = []
    print(f"x={float(x):.1f}:")
    print(f"{'y':>8s} {'z=x+y':>8s} {'K(y,t)f(x)':>16s}")
    for y in ys:
        t = y - h
        MKA = M_y_KA_raw_f(x, y, t, epsv, f)
        KB = KB_f(x, h, epsv, f)
        total = MKA + KB
        totals.append((y, total))
        print(f"{float(y):8.1f} {float(x+y):8.1f} {mp.nstr(total,10):>16s}")
    logy = [math.log(float(v[0])) for v in totals]
    logt = [math.log(abs(float(v[1]))) for v in totals]
    n = len(logy)
    mx, my = sum(logy)/n, sum(logt)/n
    slope = sum((logy[i]-mx)*(logt[i]-my) for i in range(n)) / sum((logy[i]-mx)**2 for i in range(n))
    print(f"  fitted log-log slope vs y (all 5 points): {slope:.4f}  (prediction: -1)")
    print()

print("Cross-x comparison at matched y=1002.0 (t=1000.0): value should shrink as x grows")
print("(since z=x+y grows), consistent with O(1/z) rather than O(1/y) alone.")
