#!/usr/bin/env python3
"""
s01_gordon_mills_ratio_lemma.py -- wave 29 front (a), CU-DIRECT-PROOF-ATTEMPT

Goal: a fully RIGOROUS (non-asymptotic-series), elementary chain of bounds
on R(z) := int_0^inf e^{-u^2/2 - u z} du  (the Mills-ratio-type function
this whole sub-lineage's closed-form kernel is built from, R'=zR-1,
R(0)=sqrt(pi/2)) that will let us bound the Watson's-lemma remainder
rho(h',z) WITHOUT invoking an asymptotic series (whose remainder was never
rigorously bounded by any ancestor front -- only numerically tested).

This is new content: no ancestor front in this sub-lineage derived or used
an explicit, provably-correct, non-asymptotic double inequality for R(z).
They used R(z)<=1/z (cited) and an asymptotic SERIES R(z)~1/z-1/z^3+...
(formal, no rigorous remainder). Here we derive and PROVE:

  (G1)  z/(1+z^2) <= R(z) <= 1/z                      for all z>0
  (G2)  0 <= sigma(z) := 1 - z*R(z) <= 1/(1+z^2) <= 1/z^2
  (G3)  0 <= R''(z) <= 2*R(z)/(1+z^2) <= 2/(z*(1+z^2)) <= 2/z^3

via an elementary integrating-factor / comparison argument on the linear
ODE R'=zR-1 (and its derivative R''=R+zR'), fully independent of any
asymptotic expansion. This is the technical engine for s02/s03.

Method: sympy for every symbolic step (ODE substitution checks, algebraic
identities); mpmath (dps=50) for independent high-precision numerical
confirmation of positivity/inequality claims across a wide range of z,
including small z where the asymptotic series is not even valid, to make
sure the bounds are genuinely non-asymptotic.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

print("=" * 78)
print("PART 1 -- symbolic setup: R satisfies R'=zR-1, R(0)=sqrt(pi/2)")
print("=" * 78)

z = sp.symbols('z', positive=True)
R = sp.Function('R')

# R is defined as R(z) = int_0^inf e^{-u^2/2-u z} du. Confirm this integral
# satisfies R'=zR-1 by direct symbolic differentiation under the integral
# sign and one integration by parts (re-derived fresh here, independent of
# any ancestor script).
u, eps_sym = sp.symbols('u eps', positive=True)
integrand = sp.exp(-u**2/2 - u*z)
# d/dz of the integrand:
dintegrand_dz = sp.diff(integrand, z)
print("d/dz[e^{-u^2/2-uz}] =", dintegrand_dz, " (= -u * integrand, as expected)")
assert sp.simplify(dintegrand_dz - (-u)*integrand) == 0

# IBP check: d/du[-e^{-u^2/2-uz}] = (u+z) e^{-u^2/2-uz}. Integrate 0..inf:
# int_0^inf (u+z) e^{-u^2/2-uz} du = [-e^{-u^2/2-uz}]_0^inf = 0 - (-1) = 1
# i.e. int u*e(...) du + z*R(z) = 1  =>  R'(z) = -int u*e(...)du = zR(z)-1
dexpr = sp.diff(-integrand, u)
check_ibp = sp.simplify(dexpr - (u + z) * integrand)
print("d/du[-e^{-u^2/2-uz}] - (u+z)e^{-u^2/2-uz} =", check_ibp, " (must be 0)")
assert check_ibp == 0
print("=> int_0^inf u*e^{-u^2/2-uz} du = 1 - z*R(z) = -R'(z)   [EXACT identity, confirmed]")
print()

print("=" * 78)
print("PART 2 -- Gordon-type lower bound: R(z) >= z/(1+z^2) for all z>0")
print("=" * 78)
# Comparison function v(z) := z/(1+z^2). Define w1(z):=R(z)-v(z).
# Claim: w1 satisfies the linear ODE w1' = z*w1 - 2/(1+z^2)^2, and hence
# (via integrating factor e^{-z^2/2}, using w1->0 at z->inf) has the
# EXPLICIT closed form
#   w1(z) = e^{z^2/2} * int_z^inf 2*e^{-s^2/2}/(1+s^2)^2 ds   >= 0.
zsym = z
v = zsym / (1 + zsym**2)
vprime = sp.diff(v, zsym)
print("v(z) := z/(1+z^2);  v'(z) =", sp.simplify(vprime))

# z*v(z) - 1 - v'(z), the RHS forcing term appearing in w1' = z*w1 + (z*v-1-v')
forcing = sp.simplify(zsym*v - 1 - vprime)
print("z*v(z) - 1 - v'(z) =", forcing, " (claimed: -2/(1+z^2)^2)")
assert sp.simplify(forcing - (-2/(1+zsym**2)**2)) == 0
print("CONFIRMED: w1(z):=R(z)-v(z) satisfies w1'(z) = z*w1(z) - 2/(1+z^2)^2")
print("  [since R'=zR-1 and w1'=R'-v'=zR-1-v' = z(w1+v)-1-v' = z*w1 + (zv-1-v')]")
print()

# Verify the integrating-factor closed form solves this ODE (symbolically,
# via Leibniz differentiation under the integral sign -- independent check
# that the CANDIDATE closed form is correct, not merely "solves at one point").
s = sp.symbols('s', positive=True)
# candidate: w1(z) = exp(z^2/2) * Integral(2*exp(-s^2/2)/(1+s^2)^2, (s, z, oo))
Iz = sp.Function('Iz')  # stands for int_z^inf 2e^{-s^2/2}/(1+s^2)^2 ds, dIz/dz = -2e^{-z^2/2}/(1+z^2)^2
candidate = sp.exp(zsym**2/2) * Iz(zsym)
dcandidate = sp.diff(candidate, zsym)
# substitute dIz/dz -> -2*exp(-z^2/2)/(1+z^2)^2
dcandidate_sub = dcandidate.subs(sp.Derivative(Iz(zsym), zsym), -2*sp.exp(-zsym**2/2)/(1+zsym**2)**2)
target_rhs = zsym*candidate - 2/(1+zsym**2)**2
diffcheck = sp.simplify(dcandidate_sub - target_rhs)
print("Candidate w1(z)=e^{z^2/2}*Iz(z) satisfies w1'=z*w1-2/(1+z^2)^2?",
      "residual =", diffcheck, " (must be 0)")
assert diffcheck == 0
print("CONFIRMED: the integrating-factor closed form is an exact solution.")
print("Since e^{z^2/2}*Iz(z) -> 0 as z->inf (both factors controlled; matches")
print("the boundary condition w1(z)->0), and the integrand 2e^{-s^2/2}/(1+s^2)^2")
print("is manifestly POSITIVE for all s, Iz(z)=int_z^inf(...)ds > 0 for every")
print("finite z, hence w1(z) = e^{z^2/2}*Iz(z) > 0 for ALL z > 0 (and =0 only")
print("in the z->inf limit). This is a fully elementary, non-asymptotic proof.")
print()

print("=" * 78)
print("PART 3 -- numerical confirmation of (G1): z/(1+z^2) <= R(z) <= 1/z")
print("=" * 78)

def R_mp(zz):
    zz = mp.mpf(zz)
    # R(z) = sqrt(pi/2) * erfcx(z/sqrt(2))  [cited closed form, record fact]
    return mp.sqrt(mp.pi/2) * mp.erfc(zz/mp.sqrt(2)) * mp.exp(zz**2/2)

def R_mp_direct(zz):
    # independent direct-quadrature route (NOT via erfcx), to cross-check
    zz = mp.mpf(zz)
    f = lambda uu: mp.e**(-uu**2/2 - uu*zz)
    return mp.quad(f, [0, mp.inf])

test_zs = [mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5'),
           mp.mpf(1), mp.mpf(2), mp.mpf(5), mp.mpf(10), mp.mpf(50),
           mp.mpf(100), mp.mpf(1000), mp.mpf(10000), mp.mpf(1e6)]

print(f"{'z':>10} {'R(z) [erfcx]':>22} {'R(z) [direct quad]':>22} {'rel.diff':>12} "
      f"{'lower z/(1+z^2)':>18} {'upper 1/z':>14} {'G1 holds?':>10}")
all_g1_ok = True
for zz in test_zs:
    Ra = R_mp(zz)
    Rb = R_mp_direct(zz)
    reldiff = abs(Ra - Rb) / max(abs(Ra), mp.mpf('1e-30'))
    lower = zz / (1 + zz**2)
    upper = 1 / zz
    ok = (Ra >= lower - mp.mpf('1e-40')) and (Ra <= upper + mp.mpf('1e-40'))
    all_g1_ok &= ok
    print(f"{float(zz):10.4g} {float(Ra):22.16g} {float(Rb):22.16g} {float(reldiff):12.2e} "
          f"{float(lower):18.10g} {float(upper):14.10g} {str(ok):>10}")

print()
print("All G1 checks passed:", all_g1_ok)
assert all_g1_ok
print()

print("=" * 78)
print("PART 4 -- consequence (G2): 0 <= sigma(z) := 1-z*R(z) <= 1/(1+z^2) <= 1/z^2")
print("=" * 78)
# Direct algebraic consequence of G1: z*v(z) = z^2/(1+z^2), so
# 1 - z*R(z) <= 1 - z*v(z) = 1 - z^2/(1+z^2) = 1/(1+z^2).  And z*R(z)<=1 (from
# R<=1/z) gives 1-zR(z) >= 0. Confirm this algebra symbolically:
sigma_upper_check = sp.simplify(1 - zsym*v - 1/(1+zsym**2))
print("1 - z*v(z) - 1/(1+z^2) =", sigma_upper_check, " (must be 0)")
assert sigma_upper_check == 0
print("CONFIRMED (G2) algebraically, given (G1).")
print()

# Numerically re-confirm directly on R (not v) for good measure:
print(f"{'z':>10} {'sigma(z)=1-zR(z)':>20} {'1/(1+z^2)':>14} {'1/z^2':>14} {'G2 holds?':>10}")
all_g2_ok = True
for zz in test_zs:
    Ra = R_mp(zz)
    sigma = 1 - zz*Ra
    bound1 = 1/(1+zz**2)
    bound2 = 1/zz**2
    ok = (sigma >= -mp.mpf('1e-40')) and (sigma <= bound1 + mp.mpf('1e-40'))
    all_g2_ok &= ok
    print(f"{float(zz):10.4g} {float(sigma):20.14g} {float(bound1):14.8g} {float(bound2):14.8g} {str(ok):>10}")
assert all_g2_ok
print()

print("=" * 78)
print("PART 5 -- second-derivative bound (G3): 0<=R''(z)<=2R(z)/(1+z^2)<=2/(z(1+z^2))<=2/z^3")
print("=" * 78)
# R''(z) = R(z) + z*R'(z) = R(z) + z*(z*R(z)-1) = R(z)*(1+z^2) - z = (1+z^2)*w1(z)
Rpp_formula = sp.simplify(R(zsym) + zsym*(zsym*R(zsym) - 1))
print("R''(z) = R(z) + z*R'(z) [via R'=zR-1] =", Rpp_formula)
Rpp_alt = sp.expand(R(zsym)*(1+zsym**2) - zsym)
check = sp.simplify(Rpp_formula - Rpp_alt)
print("R(z)*(1+z^2) - z  matches? residual =", check)
assert check == 0
# So R''(z) = (1+z^2)*w1(z), where w1(z)=R(z)-z/(1+z^2) already proved >=0.
# Upper bound: w1(z) = e^{z^2/2} int_z^inf 2e^{-s^2/2}/(1+s^2)^2 ds
#   <= e^{z^2/2} * [1/(1+z^2)^2] * int_z^inf 2e^{-s^2/2} ds   (since 1/(1+s^2)^2
#      is DECREASING in s, so its sup over s>=z is its value AT s=z)
#   = [1/(1+z^2)^2] * 2*R(z)        [since e^{z^2/2}*int_z^inf e^{-s^2/2}ds = R(z)]
# => R''(z) = (1+z^2)*w1(z) <= (1+z^2)*2*R(z)/(1+z^2)^2 = 2*R(z)/(1+z^2)
decreasing_check = sp.simplify(sp.diff(1/(1+s**2)**2, s))
print("d/ds[1/(1+s^2)^2] =", decreasing_check, " (negative for s>0 => decreasing, confirms sup-at-s=z step)")
print()
print("Algebraic chain: R''(z) = (1+z^2)*w1(z) <= (1+z^2)*2R(z)/(1+z^2)^2 = 2R(z)/(1+z^2)")
print("                        <= 2*(1/z)/(1+z^2) = 2/(z(1+z^2)) <= 2/z^3")
print()

def Rpp_mp(zz):
    zz = mp.mpf(zz)
    Ra = R_mp(zz)
    Rp = zz*Ra - 1
    return Ra + zz*Rp  # = R''(z) via the ODE, evaluated using high-precision R,R'

def Rpp_mp_direct(zz):
    # fully independent route: R''(z) = int_0^inf u^2 e^{-u^2/2-uz} du (direct
    # differentiation twice under the integral sign of the ORIGINAL definition)
    zz = mp.mpf(zz)
    f = lambda uu: uu**2 * mp.e**(-uu**2/2 - uu*zz)
    return mp.quad(f, [0, mp.inf])

hdr1 = "Rpp(z) [ODE]"
hdr2 = "Rpp(z) [direct u^2 quad]"
print(f"{'z':>10} {hdr1:>16} {hdr2:>24} {'reldiff':>10} "
      f"{'2R(z)/(1+z^2)':>16} {'2/(z(1+z^2))':>14} {'2/z^3':>12} {'G3 ok?':>8}")
all_g3_ok = True
for zz in test_zs:
    a = Rpp_mp(zz)
    b = Rpp_mp_direct(zz)
    reldiff = abs(a-b)/max(abs(a), mp.mpf('1e-30'))
    bound1 = 2*R_mp(zz)/(1+zz**2)
    bound2 = 2/(zz*(1+zz**2))
    bound3 = 2/zz**3
    ok = (a >= -mp.mpf('1e-35')) and (a <= bound1 + mp.mpf('1e-35'))
    all_g3_ok &= ok
    print(f"{float(zz):10.4g} {float(a):16.10g} {float(b):24.10g} {float(reldiff):10.2e} "
          f"{float(bound1):16.10g} {float(bound2):14.8g} {float(bound3):12.6g} {str(ok):>8}")
assert all_g3_ok
print()
print("All G3 checks passed:", all_g3_ok)
print()

print("=" * 78)
print("SUMMARY -- fully rigorous, non-asymptotic bounds established:")
print("=" * 78)
print("""
 (G1)  z/(1+z^2) <= R(z) <= 1/z                       for all z>0  [PROVED]
 (G2)  0 <= sigma(z):=1-zR(z) <= 1/(1+z^2) <= 1/z^2                [PROVED]
 (G3)  0 <= R''(z) <= 2R(z)/(1+z^2) <= 2/(z(1+z^2)) <= 2/z^3       [PROVED]

These are ELEMENTARY, EXACT-CONSTANT, non-asymptotic bounds (an
integrating-factor comparison argument on the defining ODE R'=zR-1),
independently re-derived and cross-checked here (both against a symbolic
ODE-substitution route AND an independent direct mpmath quadrature of the
raw definitions of R, R', R''). They do NOT depend on the formal Mills-
ratio asymptotic SERIES (1/z-1/z^3+3/z^5-...) that every ancestor front in
this sub-lineage used only formally/numerically -- these bounds hold for
EVERY z>0, including small z where that series is not even convergent-
useful. This lemma is the technical engine for s02's rigorous bound on the
Watson's-lemma remainder rho(h',z), and hence for a genuine partial PROOF
of hypothesis (U), Sec 2 of ATTEMPT.md.
""")
