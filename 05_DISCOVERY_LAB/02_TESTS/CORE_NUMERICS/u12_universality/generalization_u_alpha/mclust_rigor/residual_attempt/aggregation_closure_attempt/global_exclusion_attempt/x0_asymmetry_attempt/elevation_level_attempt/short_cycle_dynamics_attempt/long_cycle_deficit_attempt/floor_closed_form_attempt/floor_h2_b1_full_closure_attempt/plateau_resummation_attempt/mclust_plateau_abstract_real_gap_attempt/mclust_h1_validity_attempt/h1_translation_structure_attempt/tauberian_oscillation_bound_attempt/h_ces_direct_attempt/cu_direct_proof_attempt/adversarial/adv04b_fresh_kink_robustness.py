"""
adv04b_fresh_kink_robustness.py -- hostile referee, wave 29 front (a)
CU-DIRECT-PROOF-ATTEMPT.

Item (d), part 2: reproduce the target's s04c/s04d PHENOMENON (not just its
exact numbers, already confirmed digit-for-digit in adv04) with a FRESH,
differently-shaped kink function and fresh parameters, to test whether the
pointwise-degrades / aggregate-self-heals pattern is a robust, general
phenomenon or an artifact of the one specific test function the target
used.

Fresh kink: g_kink(a) := exp(-a/2)*cos(2a) + 0.6*max(0,a-b0) -- a
ONE-SIDED "ramp" kink (derivative jump 0->0.6), DIFFERENT in shape from
the target's two-sided |a-a0| kink (derivative jump -0.3->+0.3, same
magnitude 0.6, chosen to match for comparability). b0=0.25 (kink
location), eps=0.3, x0=0.05 (small nonzero x, distinct from target's
x=0), hp := b0-x0-1/z (adversarial alignment analogous to s04c's
hp:=a0-1/z).

RESULT (see log): Part A (pointwise E(h',z)) ROBUSTLY reproduces the SAME
phenomenon with this different function -- z^2|E| converges cleanly to a
nonzero constant (~0.2206, close to the target's own 0.2208, plausibly
because the derivative-jump MAGNITUDE was matched at 0.6) as z grows from
20 to 15000, confirming the pointwise degradation is not an artifact of
the one tested function's exact shape. Part B (aggregate Efull) is
NOISIER/slower for this fresh, differently-shaped (one-sided ramp) kink --
z^3|Efull| does not blow up (no divergence, unlike what would indicate a
genuine failure of self-healing) but climbs slowly and had not clearly
plateaued by z=500 (0.0586 -> 0.0511 -> 0.1137 -> 0.1358 -> 0.1444, still
rising but decelerating: ratio 1.19 from z=80->200, 1.06 from z=200->500).
This is CONSISTENT WITH, but a less clean/decisive confirmation of, the
aggregate self-healing phenomenon than the exact reproduction on the
target's OWN function (adv04, which converges cleanly and matches the
published 0.936 to full precision) -- reported honestly as suggestive-but-
not-fully-resolved for this second function, rather than overstated either
way. A longer z-sweep (z>500, not attempted here given time budget) would
be needed to settle whether it plateaus.
"""
import mpmath as mp
mp.mp.dps = 25

def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2)*mp.erfc(z/mp.sqrt(2))*mp.exp(z**2/2)
def sigma_mp(z):
    z = mp.mpf(z)
    return 1 - z*R_mp(z)

b0 = mp.mpf('0.25')
eps = mp.mpf('0.3')
x0 = mp.mpf('0.05')

def g_kink(a):
    a = mp.mpf(a)
    ramp = a - b0 if a > b0 else mp.mpf(0)
    return mp.e**(-a/2)*mp.cos(2*a) + mp.mpf('0.6')*ramp

def gprime_at(a, h=mp.mpf('1e-15')):
    return (g_kink(a+h)-g_kink(a))/h

def rho_direct(hp, z):
    hp = mp.mpf(hp); z = mp.mpf(z)
    base = g_kink(x0+hp)
    kink_u = b0 - (x0+hp)
    integrand = lambda u: mp.e**(-u**2/2-u*z)*(g_kink(x0+hp+u)-base)
    pts = [mp.mpf(0)]
    if kink_u > 0:
        pts.append(kink_u)
    pts += [mp.mpf(v) for v in [1,3,8,20,50,120,300]]
    pts.append(mp.inf)
    pts = sorted(set(pts))
    return mp.quad(integrand, pts)

print("Part A: pointwise E(h',z), adversarially aligned FRESH ramp kink")
print(f"kink b0={float(b0)}, x0={float(x0)}, eps={float(eps)}")
zs = [mp.mpf(v) for v in [20,50,150,500,1500,5000,15000]]
print(f"{'z':>8} {'hp':>12} {'u*':>10} {'|E|':>16} {'z^2|E|':>10} {'z^3|E|':>12}")
z2s=[]
for z in zs:
    hp = b0 - x0 - 1/z
    if hp<=0: continue
    u_star = b0-(x0+hp)
    fp = gprime_at(x0+hp)
    rho = rho_direct(hp, z)
    E = rho - fp*sigma_mp(z)
    z2=z**2*abs(E); z3=z**3*abs(E)
    z2s.append(z2)
    print(f"{float(z):8.0f} {float(hp):12.6f} {float(u_star):10.6f} {float(abs(E)):16.6e} {float(z2):10.4f} {float(z3):12.2f}")
print("z^2|E| trend:", [round(float(v),5) for v in z2s])
print()

def E_of_hp(hp, z):
    hp = mp.mpf(hp); z = mp.mpf(z)
    base = g_kink(x0+hp)
    kink_u = b0-(x0+hp)
    fp = gprime_at(x0+hp)
    integrand = lambda u: mp.e**(-u**2/2-u*z)*(g_kink(x0+hp+u)-base)
    pts=[mp.mpf(0)]
    if kink_u>0: pts.append(kink_u)
    pts += [mp.mpf(v) for v in [1,3,8,20,50,120]]
    pts.append(mp.inf)
    pts = sorted(set(pts))
    rho = mp.quad(integrand, pts)
    return rho - fp*sigma_mp(z)

def Efull(z,h):
    z=mp.mpf(z); h=mp.mpf(h)
    bps=set([mp.mpf(0), b0/2, b0, min(2*b0,h), eps, 2*eps])
    bps=sorted(b for b in bps if 0<=b<=h)+[h]
    bps=sorted(set(bps))
    return mp.quad(lambda hp: mp.e**(-hp/eps)*E_of_hp(hp,z), bps)

print("Part B: aggregate Efull(z), SAME fresh ramp kink/alignment")
zs2=[mp.mpf(v) for v in [10,30,80,200,500]]
print(f"{'z':>7} {'|Efull|':>16} {'z^2|Efull|':>12} {'z^3|Efull|':>12}")
z3s=[]
for z in zs2:
    h=z
    Ef=Efull(z,h)
    z2=z**2*abs(Ef); z3=z**3*abs(Ef)
    z3s.append(z3)
    print(f"{float(z):7.0f} {float(abs(Ef)):16.6e} {float(z2):12.5f} {float(z3):12.5f}")
print("z^3|Efull| trend:", [round(float(v),5) for v in z3s])
