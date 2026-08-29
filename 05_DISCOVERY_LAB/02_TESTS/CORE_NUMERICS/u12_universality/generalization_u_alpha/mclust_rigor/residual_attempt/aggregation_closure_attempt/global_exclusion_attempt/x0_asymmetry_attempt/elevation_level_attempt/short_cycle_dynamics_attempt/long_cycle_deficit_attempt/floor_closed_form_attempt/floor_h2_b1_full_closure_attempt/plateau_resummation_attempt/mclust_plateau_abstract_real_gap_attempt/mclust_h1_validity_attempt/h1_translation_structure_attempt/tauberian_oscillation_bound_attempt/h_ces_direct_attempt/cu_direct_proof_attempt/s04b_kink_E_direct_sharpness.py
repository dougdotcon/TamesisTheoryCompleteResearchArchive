#!/usr/bin/env python3
"""
s04b_kink_E_direct_sharpness.py -- wave 29 front (a), CU-DIRECT-PROOF-ATTEMPT

A CHEAPER, more DIRECT sharpness test than s04's full double-integral
raw-kernel evaluation (which timed out before reaching large z -- see
Self-caught issues in ATTEMPT.md): this script computes ONLY the residual
E(h',z) := rho(h',z) - f'(x+h')*sigma(z) directly via a SINGLE integral
(not nested inside the outer h'-integral of the full kernel), for a kinked
(Lipschitz-only, NOT C^{1,1}) test function, and checks whether the
RIGOROUS-under-(C'') rate |E(h',z)|=O(1/z^3) (s03) survives or degrades
to the CRUDE-under-(C')-only rate O(1/z^2) (s02 Part 2's fallback bound)
-- i.e. whether s03's C^{1,1} hypothesis is a genuine mathematical
necessity or just this front's own proof-technique artifact.

f_kink(a) := 1/(1+a) + 0.3*|a-3|     (Lipschitz, kink in f' at a=3)
Evaluated at h'=1 (so the kink sits at u=2 inside the u-integration --
an interior point, f'(x+h')=f'(1) well-defined, away from the kink
itself), x=0.
"""
import mpmath as mp

mp.mp.dps = 30


def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.exp(z**2/2)


def sigma_mp(z):
    z = mp.mpf(z)
    return 1 - z * R_mp(z)


def f_smooth(a):
    return mp.sin(a) / (3 + a**2)


def fprime_smooth(a, h=mp.mpf('1e-15')):
    return (f_smooth(a + h) - f_smooth(a - h)) / (2*h)


def f_kink(a):
    return 1/(1+a) + mp.mpf('0.3') * abs(a - 3)


def fprime_kink_onesided(a, side, h=mp.mpf('1e-15')):
    # one-sided derivative, valid away from the kink at a=3
    if side == 'right':
        return (f_kink(a + h) - f_kink(a)) / h
    return (f_kink(a) - f_kink(a - h)) / h


def rho_direct(f, x, hp, z, kink_u=None):
    x = mp.mpf(x); hp = mp.mpf(hp); z = mp.mpf(z)
    base = f(x + hp)

    def integrand(u):
        return mp.e**(-u**2/2 - u*z) * (f(x + hp + u) - base)

    pts = [0]
    if kink_u is not None and kink_u > 0:
        pts.append(kink_u)
    pts += [2, 6, 15, 35, 70, 150, mp.inf]
    pts = sorted(set([mp.mpf(p) for p in pts]))
    return mp.quad(integrand, pts)


x0 = mp.mpf(0)
hp0 = mp.mpf(1)
kink_a = mp.mpf(3)
kink_u = kink_a - (x0 + hp0)   # = 2

fp_smooth_val = fprime_smooth(x0 + hp0)
# f_kink is smooth (derivative = -1/(1+a)^2 +/- 0.3) at a=x0+hp0=1, away
# from the kink at a=3 -- well-defined two-sided derivative there:
fp_kink_val = fprime_kink_onesided(x0 + hp0, 'right')
fp_kink_val_L = fprime_kink_onesided(x0 + hp0, 'left')
print(f"f_kink'(1) [right-diff] = {float(fp_kink_val):.10f}, "
      f"[left-diff] = {float(fp_kink_val_L):.10f}  (should agree: away from kink)")
assert abs(fp_kink_val - fp_kink_val_L) < mp.mpf('1e-8')

print()
print(f"{'z':>7} {'|E| smooth':>16} {'z^2|E|s':>10} {'z^3|E|s':>10}   "
      f"{'|E| kink':>16} {'z^2|E|k':>10} {'z^3|E|k':>10}")

zs = [mp.mpf(v) for v in [10, 30, 100, 300, 1000, 3000, 10000, 30000]]
z2Es, z3Es, z2Ek, z3Ek = [], [], [], []
for z in zs:
    rho_s = rho_direct(f_smooth, x0, hp0, z)
    E_s = rho_s - fp_smooth_val * sigma_mp(z)
    rho_k = rho_direct(f_kink, x0, hp0, z, kink_u=kink_u)
    E_k = rho_k - fp_kink_val * sigma_mp(z)
    z2Es.append(z**2*abs(E_s)); z3Es.append(z**3*abs(E_s))
    z2Ek.append(z**2*abs(E_k)); z3Ek.append(z**3*abs(E_k))
    print(f"{float(z):7.0f} {float(abs(E_s)):16.6e} {float(z**2*abs(E_s)):10.4f} "
          f"{float(z**3*abs(E_s)):10.4f}   {float(abs(E_k)):16.6e} {float(z**2*abs(E_k)):10.4f} "
          f"{float(z**3*abs(E_k)):10.4f}")

print()
print("z^3*|E| trend, smooth f (should CONVERGE to a constant, per s03's rigorous O(1/z^3)):")
print(" ", [round(float(v), 5) for v in z3Es])
print("z^3*|E| trend, kink f   (per s02's crude fallback, expect this to GROW,")
print(" not converge, if (C') alone genuinely fails to deliver O(1/z^3)):")
print(" ", [round(float(v), 5) for v in z3Ek])
print()
print("z^2*|E| trend, kink f (should CONVERGE to a nonzero constant if the true")
print(" rate for the kink case is exactly O(1/z^2), confirming s02's crude")
print(" bound is SHARP, not merely a loose unproven upper bound):")
print(" ", [round(float(v), 6) for v in z2Ek])
