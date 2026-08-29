#!/usr/bin/env python3
"""
adv04_sharpness_reproduction.py -- hostile referee, wave 29 front (a)
CU-DIRECT-PROOF-ATTEMPT.

Item (d): independently reproduce the target's own s04c (adversarially-
aligned pointwise E(h',z) degradation) and s04d (aggregate Efull
boundary-layer self-healing) experiments, FRESH CODE, using the target's
own exact parameters (a0=0.1, eps=0.5, x=0) to check the SPECIFIC
published numbers: z^2|E| -> 0.2208 (s04c) and z^3|Efull| -> 0.936 (s04d).
"""
import mpmath as mp
mp.mp.dps = 30

def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2)*mp.erfc(z/mp.sqrt(2))*mp.exp(z**2/2)

def sigma_mp(z):
    z = mp.mpf(z)
    return 1 - z*R_mp(z)

a0 = mp.mpf('0.1')
def f_kink(a):
    return 1/(1+a) + mp.mpf('0.3')*abs(a-a0)

def fprime_at(a, h=mp.mpf('1e-15')):
    return (f_kink(a+h)-f_kink(a))/h

def rho_direct(x, hp, z):
    x = mp.mpf(x); hp = mp.mpf(hp); z = mp.mpf(z)
    base = f_kink(x+hp)
    kink_u = a0 - (x+hp)
    integrand = lambda u: mp.e**(-u**2/2-u*z)*(f_kink(x+hp+u)-base)
    pts = [mp.mpf(0)]
    if kink_u > 0:
        pts.append(kink_u)
    pts += [mp.mpf(v) for v in [1,3,8,20,50,120,300]]
    pts.append(mp.inf)
    pts = sorted(set(pts))
    return mp.quad(integrand, pts)

x0 = mp.mpf(0)

print("=" * 78)
print("EXPERIMENT 1 (reproduce s04c): adversarially-aligned pointwise E, a0=0.1")
print("=" * 78)
zs = [mp.mpf(v) for v in [20,50,150,500,1500,5000,15000]]
print(f"{'z':>8} {'hp':>12} {'|E|':>16} {'z^2|E|':>10} {'z^3|E|':>12}")
z2s, z3s = [], []
for z in zs:
    hp = a0 - 1/z
    if hp <= 0:
        continue
    fp = fprime_at(x0+hp)
    rho = rho_direct(x0, hp, z)
    E = rho - fp*sigma_mp(z)
    z2 = z**2*abs(E); z3 = z**3*abs(E)
    z2s.append(z2); z3s.append(z3)
    print(f"{float(z):8.0f} {float(hp):12.6f} {float(abs(E)):16.6e} {float(z2):10.4f} {float(z3):12.2f}")
print()
print("z^2|E| -> ", float(z2s[-1]), "  (target's own published value: 0.2208)")
print("z^3|E| at z=15000 -> ", float(z3s[-1]), "  (target's own published value: 3312.42)")
assert abs(float(z2s[-1]) - 0.2208) < 0.001
assert abs(float(z3s[-1]) - 3312.42) < 1.0
print("MATCH CONFIRMED to published precision.")
print()

print("=" * 78)
print("EXPERIMENT 2 (reproduce s04d): aggregate Efull, boundary-layer")
print("self-healing, SAME a0=0.1, eps=0.5, x=0")
print("=" * 78)
eps = mp.mpf('0.5')

def fprime_c(a, h=mp.mpf('1e-12')):
    return (f_kink(a+h)-f_kink(a-h))/(2*h)

def E_of_hp(hp, z):
    hp = mp.mpf(hp); z = mp.mpf(z)
    base = f_kink(x0+hp)
    kink_u = a0-(x0+hp)
    fp = fprime_c(x0+hp)
    integrand = lambda u: mp.e**(-u**2/2-u*z)*(f_kink(x0+hp+u)-base)
    pts = [mp.mpf(0)]
    if kink_u > 0:
        pts.append(kink_u)
    pts += [mp.mpf(v) for v in [1,3,8,20,50,120]]
    pts.append(mp.inf)
    pts = sorted(set(pts))
    rho = mp.quad(integrand, pts)
    return rho - fp*sigma_mp(z)

def Efull(z, h):
    z = mp.mpf(z); h = mp.mpf(h)
    bps = set([mp.mpf(0), a0/2, a0, min(2*a0,h), eps, 2*eps, 4*eps])
    bps = sorted(b for b in bps if 0 <= b <= h) + [h]
    bps = sorted(set(bps))
    return mp.quad(lambda hp: mp.e**(-hp/eps)*E_of_hp(hp,z), bps)

print(f"{'z':>7} {'|Efull|':>16} {'z^2|Efull|':>12} {'z^3|Efull|':>12}")
zs2 = [mp.mpf(v) for v in [10,30,80,200,500]]
z3_full = []
for z in zs2:
    h = z
    Ef = Efull(z, h)
    z2 = z**2*abs(Ef); z3 = z**3*abs(Ef)
    z3_full.append(z3)
    print(f"{float(z):7.0f} {float(abs(Ef)):16.6e} {float(z2):12.5f} {float(z3):12.5f}")

print()
print("z^3|Efull| -> ", float(z3_full[-1]), "  (target's own published value: 0.936)")
assert abs(float(z3_full[-1]) - 0.936) < 0.005
print("MATCH CONFIRMED to published precision.")
print()
print("VERDICT on item (d), part 1: the target's SPECIFIC published numbers")
print("for both the pointwise-degradation (s04c) and aggregate-self-healing")
print("(s04d) experiments are independently reproduced here, FRESH CODE, to")
print("full agreement -- these are genuine, correctly-computed findings, not")
print("errors or artifacts of the target's own implementation.")
