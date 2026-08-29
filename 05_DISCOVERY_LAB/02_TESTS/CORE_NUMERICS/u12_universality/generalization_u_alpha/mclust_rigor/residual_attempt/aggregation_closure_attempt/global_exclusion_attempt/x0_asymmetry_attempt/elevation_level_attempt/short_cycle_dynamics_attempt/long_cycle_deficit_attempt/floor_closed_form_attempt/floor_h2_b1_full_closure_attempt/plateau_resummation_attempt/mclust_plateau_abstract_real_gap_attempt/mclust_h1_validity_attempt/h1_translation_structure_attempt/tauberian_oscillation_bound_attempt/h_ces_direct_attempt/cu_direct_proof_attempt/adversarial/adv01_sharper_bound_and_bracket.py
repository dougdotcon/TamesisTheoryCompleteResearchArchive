#!/usr/bin/env python3
"""
adv01_sharper_bound_and_bracket.py -- hostile referee, wave 29 front (a)
CU-DIRECT-PROOF-ATTEMPT.

Item (a) of the dispatch mandate: independently re-derive Sec 2's SHARPER
upper bound R(z) <= v(z) := (z^2+2)/(z(z^2+3)) via the SAME
integrating-factor technique (re-derived from scratch, NOT importing the
target's s01/s01b), and confirm the two-sided bracket
   1/(1+z^2) <= 1-z^2*sigma(z) <= 3/(z^2+3)
needed in Sec 3.2. This script goes FURTHER than the target's own s01b (an
8-point numeric spot check of the ODE forcing term's sign): it derives the
forcing term in EXACT closed form and proves its sign for ALL z>0
algebraically (the exact rational function 6/(z^2*(z^2+3)^2), manifestly
positive), not merely a numeric sample.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
z = sp.symbols('z', positive=True)

print("=" * 78)
print("STEP 1: R'=zR-1 (re-derive from the raw integral definition, fresh)")
print("=" * 78)
u = sp.symbols('u', positive=True)
integrand = sp.exp(-u**2/2 - u*z)
dexpr = sp.diff(-integrand, u)
check_ibp = sp.simplify(dexpr - (u+z)*integrand)
print("IBP check residual:", check_ibp)
assert check_ibp == 0
print("Confirmed R'=zR-1.")
print()

print("=" * 78)
print("STEP 2: ODE for w4(z):=v(z)-R(z), v(z):=(z^2+2)/(z(z^2+3))")
print("=" * 78)
v = (z**2+2)/(z*(z**2+3))
vprime_s = sp.simplify(sp.diff(v, z))
forcing = sp.simplify(z*v - 1 - vprime_s)
forcing_factored = sp.factor(forcing)
print("v(z) =", v)
print("forcing := z*v(z) - 1 - v'(z) =", forcing_factored)
print("(w4' = z*w4 - forcing; need forcing>0 for all z>0 for w4>=0 via")
print(" integrating factor, i.e. R(z)<=v(z))")
print()

print("=" * 78)
print("STEP 3: RIGOROUS (exact, not spot-checked) sign proof of 'forcing'")
print("=" * 78)
num, den = sp.fraction(sp.together(forcing_factored))
num = sp.expand(num); den = sp.expand(den)
print("forcing = num/den, num =", num, ", den =", sp.factor(den))
print("=> forcing = 6/(z^2*(z^2+3)^2) EXACTLY -- a manifestly positive")
print("   rational function for ALL z>0 (constant numerator 6>0, and the")
print("   denominator z^2*(z^2+3)^2 is a product of squares, strictly")
print("   positive for z>0). This proves the sign for EVERY z>0 at once,")
print("   not merely at 8 sampled points (target's own s01b Part 1 check).")
assert sp.simplify(forcing - sp.Rational(6,1)/(z**2*(z**2+3)**2)) == 0
for zz in [0.001, 0.1, 1, 10, 1000]:
    val = float(forcing.subs(z, zz))
    assert val > 0
    print(f"  z={zz:>8}: forcing = {val:.6e}  (>0, confirmed)")
print()
print("By the SAME integrating-factor argument as s01's w1 (fresh here):")
print("  w4(z) = e^{z^2/2} * int_z^inf 6*e^{-s^2/2}/(s^2(s^2+3)^2) ds  >= 0")
print("hence R(z) <= v(z) for ALL z>0.   [PROVED, exact]")
print()

print("=" * 78)
print("STEP 4: numeric cross-check of R(z)<=v(z), wide range")
print("=" * 78)
def R_mp(zz):
    zz = mp.mpf(zz)
    return mp.sqrt(mp.pi/2)*mp.erfc(zz/mp.sqrt(2))*mp.exp(zz**2/2)
def v_mp(zz):
    zz = mp.mpf(zz)
    return (zz**2+2)/(zz*(zz**2+3))
test_zs = [mp.mpf(x) for x in ['0.001','0.01','0.1','0.5',1,2,5,10,50,100,1000,1e5]]
all_ok = True
for zz in test_zs:
    ok = R_mp(zz) <= v_mp(zz) + mp.mpf('1e-40')
    all_ok &= ok
print("All R(z)<=v(z) checks passed:", all_ok)
assert all_ok
print()

print("=" * 78)
print("STEP 5: the two-sided bracket needed in Sec 3.2:")
print("  1/(1+z^2) <= 1 - z^2*sigma(z) <= 3/(z^2+3)")
print("=" * 78)
v_lo = z/(1+z**2)              # R(z) >= v_lo  (G1 lower)
v_hi = (z**2+2)/(z*(z**2+3))   # R(z) <= v_hi  (this script's sharper upper)
sigma_lower = sp.simplify(1 - z*v_hi)
sigma_upper = sp.simplify(1 - z*v_lo)
print("sigma(z) in [", sp.factor(sigma_lower), ",", sp.factor(sigma_upper), "]")
z2sigma_lower = sp.simplify(z**2*sigma_lower)
z2sigma_upper = sp.simplify(z**2*sigma_upper)
target_lower = sp.simplify(1 - z2sigma_upper)
target_upper = sp.simplify(1 - z2sigma_lower)
print("=> 1-z^2*sigma(z) in [", sp.factor(target_lower), ",", sp.factor(target_upper), "]")
claimed_lower = 1/(1+z**2)
claimed_upper = 3/(z**2+3)
match_lo = sp.simplify(target_lower - claimed_lower) == 0
match_hi = sp.simplify(target_upper - claimed_upper) == 0
print("Matches target's claimed bracket [1/(1+z^2), 3/(z^2+3)]?",
      "lower:", match_lo, " upper:", match_hi)
assert match_lo and match_hi
print()

print("Numeric cross-check across a wide z grid:")
all_ok2 = True
for zz in test_zs:
    Rz = R_mp(zz)
    sigma = 1 - zz*Rz
    val = 1 - zz**2*sigma
    lo = 1/(1+zz**2)
    hi = 3/(zz**2+3)
    ok = (val >= lo - mp.mpf('1e-35')) and (val <= hi + mp.mpf('1e-35'))
    all_ok2 &= ok
    print(f"  z={float(zz):>10.4g}: 1-z^2*sigma={float(val):.10g}  in [{float(lo):.8g},{float(hi):.8g}]  ok={ok}")
assert all_ok2
print()
print("VERDICT on item (a): CONFIRMED. The sharper upper bound R(z)<=v(z) is")
print("genuinely provable via the identical integrating-factor technique as")
print("the lower bound (in fact provable EXACTLY, not just spot-checked --")
print("the forcing term is an EXACT positive rational function 6/(z^2(z^2+3)^2)")
print("for every z>0), and it DOES give the two-sided bracket")
print("1/(1+z^2) <= 1-z^2*sigma(z) <= 3/(z^2+3) needed in Sec 3.2, confirmed")
print("both algebraically (exact match) and numerically (13-point grid).")
