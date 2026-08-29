#!/usr/bin/env python3
"""
s04c_kink_adversarial_alignment.py -- wave 29 front (a),
CU-DIRECT-PROOF-ATTEMPT

s04b tested E(h',z) for a kink FAR from the u~1/z concentration scale
(kink crossed at a FIXED u=2, giving exponentially suppressed effect --
z^3|E| converged nicely even for the kink function). This script tests
the ADVERSARIALLY ALIGNED case: h' chosen, AS A FUNCTION OF z, so the
kink-crossing point u* := a0-h' sits EXACTLY at the kernel's own
concentration scale u*~1/z -- the one regime where a kink could plausibly
defeat the O(1/z^3) rate even in the pointwise-in-h' sense.

f_kink(a) := 1/(1+a) + 0.3*|a-a0|,  a0 := 0.1 (chosen small, comparable
to the eps=0.5 scale governing the OUTER h'-integral's own concentration
-- the most adversarial STATIC placement relative to that integral, per
the honest diagnosis in s04b's own writeup).

Test sequence: h'_z := a0 - 1/z   (so crossing point u*=1/z exactly),
for z large enough that h'_z > 0.
"""
import mpmath as mp

mp.mp.dps = 30


def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.exp(z**2/2)


def sigma_mp(z):
    z = mp.mpf(z)
    return 1 - z * R_mp(z)


a0 = mp.mpf('0.1')


def f_kink(a):
    return 1/(1+a) + mp.mpf('0.3') * abs(a - a0)


def fprime_kink(a, side, h=mp.mpf('1e-16')):
    if side == 'right':
        return (f_kink(a + h) - f_kink(a)) / h
    return (f_kink(a) - f_kink(a - h)) / h


def rho_direct(f, x, hp, z, kink_u=None):
    x = mp.mpf(x); hp = mp.mpf(hp); z = mp.mpf(z)
    base = f(x + hp)

    def integrand(u):
        return mp.e**(-u**2/2 - u*z) * (f(x + hp + u) - base)

    pts = [mp.mpf(0)]
    if kink_u is not None and kink_u > 0:
        pts.append(kink_u)
    pts += [mp.mpf(v) for v in [2, 6, 15, 35, 70, 150]]
    pts.append(mp.inf)
    pts = sorted(set(pts))
    return mp.quad(integrand, pts)


x0 = mp.mpf(0)
print(f"kink location a0={float(a0)}, x={float(x0)}")
print()
print(f"{'z':>8} {'h_prime':>12} {'u*=a0-h_prime':>14} {'|E|':>16} {'z^2|E|':>10} {'z^3|E|':>10}")

zs = [mp.mpf(v) for v in [20, 50, 150, 500, 1500, 5000, 15000]]
z3E_vals = []
z2E_vals = []
for z in zs:
    hp = a0 - 1/z
    if hp <= 0:
        continue
    u_star = a0 - hp
    fp_right = fprime_kink(x0 + hp, 'right')
    rho_k = rho_direct(f_kink, x0, hp, z, kink_u=u_star)
    E_k = rho_k - fp_right * sigma_mp(z)
    z2E = z**2 * abs(E_k)
    z3E = z**3 * abs(E_k)
    z2E_vals.append(z2E)
    z3E_vals.append(z3E)
    print(f"{float(z):8.0f} {float(hp):12.6f} {float(u_star):14.6f} {float(abs(E_k)):16.6e} "
          f"{float(z2E):10.4f} {float(z3E):10.4f}")

print()
print("z^2*|E| trend (adversarially-aligned kink -- if this CONVERGES to a")
print(" nonzero constant, that CONFIRMS the true rate degrades to exactly")
print(" O(1/z^2) at this alignment, i.e. (C') alone genuinely does NOT")
print(" suffice for a uniform-in-h' O(1/z^3) bound -- matching s02's crude")
print(" bound as SHARP, not merely an unproven artifact):")
print(" ", [round(float(v), 6) for v in z2E_vals])
print()
print("z^3*|E| trend (if this DIVERGES/grows without bound, confirms the")
print(" O(1/z^3) rate genuinely fails at this alignment):")
print(" ", [round(float(v), 4) for v in z3E_vals])
