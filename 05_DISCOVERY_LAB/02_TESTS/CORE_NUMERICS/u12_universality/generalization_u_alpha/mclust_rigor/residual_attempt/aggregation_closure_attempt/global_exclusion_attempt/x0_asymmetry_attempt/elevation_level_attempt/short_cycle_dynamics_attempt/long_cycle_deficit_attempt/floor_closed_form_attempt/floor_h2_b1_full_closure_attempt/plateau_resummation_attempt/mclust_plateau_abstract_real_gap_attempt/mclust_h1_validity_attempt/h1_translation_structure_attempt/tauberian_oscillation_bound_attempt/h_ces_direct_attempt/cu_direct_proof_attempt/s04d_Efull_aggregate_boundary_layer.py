#!/usr/bin/env python3
"""
s04d_Efull_aggregate_boundary_layer.py -- wave 29 front (a),
CU-DIRECT-PROOF-ATTEMPT

s04c showed E(h',z) POINTWISE-in-h' genuinely degrades to O(1/z^2) (not
O(1/z^3)) at an h' adversarially aligned with a kink (mere (C'), no
C^{1,1}). This script checks whether that pointwise degradation SURVIVES
integration against the outer weight e^{-h'/eps} -- i.e. whether the
AGGREGATE quantity Efull(z):=int_0^h e^{-h'/eps}E(h',z)dh' (the quantity
that actually enters the closed-form remainder, s02/s03) is still
O(1/z^3) despite the pointwise degradation (a "boundary-layer" effect:
the bad h'-region has width ~O(1/z), so its O(1/z^2)-sized contribution
integrates to O(1/z^3) in aggregate) -- or whether it too degrades to
O(1/z^2), confirming (C'') is a genuine, not merely pointwise-technical,
necessity for (U).

f_kink(a) := 1/(1+a) + 0.3*|a-a0|, a0=0.1, x=0, eps=0.5 (same as s04c).
"""
import mpmath as mp

mp.mp.dps = 20


def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.exp(z**2/2)


def sigma_mp(z):
    z = mp.mpf(z)
    return 1 - z * R_mp(z)


a0 = mp.mpf('0.1')
eps = mp.mpf('0.5')
x0 = mp.mpf(0)


def f_kink(a):
    return 1/(1+a) + mp.mpf('0.3') * abs(a - a0)


def fprime_kink(a, h=mp.mpf('1e-12')):
    return (f_kink(a + h) - f_kink(a - h)) / (2*h)


def E_of_hp(hp, z):
    hp = mp.mpf(hp); z = mp.mpf(z)
    base = f_kink(x0 + hp)
    fp = fprime_kink(x0 + hp) if abs(hp - a0) > mp.mpf('1e-9') else fprime_kink(x0 + hp + mp.mpf('1e-9'))

    def integrand(u):
        return mp.e**(-u**2/2 - u*z) * (f_kink(x0 + hp + u) - base)

    kink_u = a0 - hp
    pts = [mp.mpf(0)]
    if kink_u > 0:
        pts.append(kink_u)
    pts += [mp.mpf(v) for v in [2, 6, 15, 35, 80]]
    pts.append(mp.inf)
    pts = sorted(set(pts))
    rho = mp.quad(integrand, pts)
    return rho - fp * sigma_mp(z)


def Efull(z, h):
    z = mp.mpf(z); h = mp.mpf(h)
    bps = [mp.mpf(0), a0/2, a0, min(a0*2, h) if a0*2 < h else h]
    bps = [b for b in bps if b <= h]
    bps += [eps, 2*eps, h]
    bps = sorted(set([b for b in bps if b <= h] + [h]))
    return mp.quad(lambda hp: mp.e**(-hp/eps) * E_of_hp(hp, z), bps)


print(f"{'z':>7} {'h':>6} {'|Efull|':>16} {'z^2|Efull|':>12} {'z^3|Efull|':>12}")
zs = [mp.mpf(v) for v in [10, 30, 80, 200, 500]]
z2vals, z3vals = [], []
for z in zs:
    h = z  # y=z (x=0), h up to y; outer integral concentrated near 0 anyway
    Ef = Efull(z, h)
    z2 = z**2*abs(Ef)
    z3 = z**3*abs(Ef)
    z2vals.append(z2); z3vals.append(z3)
    print(f"{float(z):7.0f} {float(h):6.0f} {float(abs(Ef)):16.6e} {float(z2):12.5f} {float(z3):12.5f}")

print()
print("z^2*|Efull| trend (if CONVERGES to nonzero: aggregate degrades to")
print(" O(1/z^2), confirming (C'') genuinely necessary even in aggregate):")
print(" ", [round(float(v), 6) for v in z2vals])
print("z^3*|Efull| trend (if CONVERGES to nonzero/bounded: aggregate STILL")
print(" achieves O(1/z^3) despite pointwise degradation -- boundary-layer")
print(" self-healing, (C') alone may suffice for the AGGREGATE (U) after all):")
print(" ", [round(float(v), 6) for v in z3vals])
