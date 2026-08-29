#!/usr/bin/env python3
"""
s02_Rpp_bound_numeric.py -- BOUNDARY-LAYER-SELFHEAL-ATTEMPT

Fresh, from-scratch mpmath numerical confirmation of:
  (i)   R''(z) = (1+z^2)*R(z) - z   (Part 1 of s01, closed form)
  (ii)  R''(z) <= 2/z^3 for z>0     (Part 5 of s01, elementary bound)
  (iii) int_0^inf u*Q_u(z) du = R''(z)/2, where
        Q_u(z) := int_u^inf e^{-w^2/2-wz} dw
        (Parts 2-3 of s01, the swap identity this front's Step 5 needs)

All via DIRECT numerical quadrature of the raw definitions (R(z) via its
own defining integral AND via the erfcx closed form, cross-checked; R''(z)
via direct numerical differentiation of R AND via the closed-form
(1+z^2)R(z)-z, cross-checked; Q_u(z) via its own tail-integral definition;
int u*Q_u(z)du via direct outer quadrature).
"""
import mpmath as mp

mp.mp.dps = 40


def R_direct(z):
    """R(z) := int_0^inf e^{-u^2/2-uz} du, via its OWN raw definition."""
    z = mp.mpf(z)
    return mp.quad(lambda u: mp.e**(-u**2 / 2 - u * z), [0, mp.inf])


def R_erfcx(z):
    """R(z) = sqrt(pi/2)*erfcx(z/sqrt2), the closed-form route."""
    z = mp.mpf(z)
    return mp.sqrt(mp.pi / 2) * mp.erfc(z / mp.sqrt(2)) * mp.e**(z**2 / 2)


print("=" * 78)
print("Check 0: R_direct(z) vs R_erfcx(z) -- two independent routes to R")
print("=" * 78)
zs_check = [mp.mpf(v) for v in ['0.5', '1', '3', '10', '50', '300']]
for z in zs_check:
    a = R_direct(z)
    b = R_erfcx(z)
    print(f"  z={float(z):8.2f}  R_direct={a}  R_erfcx={b}  reldiff={float(abs(a-b)/b):.3e}")
    assert abs(a - b) / b < mp.mpf('1e-25'), "R_direct vs R_erfcx mismatch"
print("PASS: R_direct and R_erfcx agree to > 25 digits at all test points.")

print()
print("=" * 78)
print("Check (i): R''(z) via direct numerical differentiation of R_erfcx")
print("           vs the closed form (1+z^2)*R(z) - z")
print("=" * 78)
zs = [mp.mpf(v) for v in ['0.3', '1', '2', '5', '10', '30', '100', '1000', '10000']]
for z in zs:
    Rpp_numdiff = mp.diff(R_erfcx, z, n=2)
    Rpp_closed = (1 + z**2) * R_erfcx(z) - z
    reldiff = abs(Rpp_numdiff - Rpp_closed) / abs(Rpp_closed)
    print(f"  z={float(z):10.2f}  R''_numdiff={float(Rpp_numdiff): .10e}  "
          f"R''_closed={float(Rpp_closed): .10e}  reldiff={float(reldiff):.3e}")
    assert reldiff < mp.mpf('1e-15'), f"R'' mismatch at z={z}"
print("PASS: numerical d^2/dz^2 R(z) matches (1+z^2)*R(z)-z at every z tested.")

print()
print("=" * 78)
print("Check (ii): R''(z) <= 2/z^3 for all tested z>0 (elementary bound,")
print("            s01 Part 5), plus the ASYMPTOTIC TIGHTNESS z^3*R''(z)->2")
print("=" * 78)
for z in zs:
    Rpp = (1 + z**2) * R_erfcx(z) - z
    bound = 2 / z**3
    ratio = Rpp / bound
    z3Rpp = z**3 * Rpp
    print(f"  z={float(z):10.2f}  R''={float(Rpp):.6e}  2/z^3={float(bound):.6e}  "
          f"R''/(2/z^3)={float(ratio):.6f}  z^3*R''={float(z3Rpp):.6f}")
    assert Rpp <= bound, f"R'' EXCEEDS the claimed bound 2/z^3 at z={z}"
print("PASS: R''(z) <= 2/z^3 holds at every tested z (ratio always <=1);")
print("      z^3*R''(z) -> 2 as z->infinity (bound is asymptotically TIGHT,")
print("      not merely a loose over-estimate).")

print()
print("=" * 78)
print("Check (iii): int_0^inf u*Q_u(z) du = R''(z)/2, Q_u(z):=int_u^inf")
print("             e^{-w^2/2-wz}dw  -- via DIRECT double quadrature,")
print("             independent of the closed-form route above")
print("=" * 78)


def Q_direct(u, z):
    u = mp.mpf(u)
    z = mp.mpf(z)
    return mp.quad(lambda w: mp.e**(-w**2 / 2 - w * z), [u, mp.inf])


zs3 = [mp.mpf(v) for v in ['1', '3', '10', '50']]
for z in zs3:
    lhs = mp.quad(lambda u: u * Q_direct(u, z), [0, mp.inf])
    rhs = ((1 + z**2) * R_erfcx(z) - z) / 2
    reldiff = abs(lhs - rhs) / abs(rhs)
    print(f"  z={float(z):8.2f}  int(u*Q_u)du={float(lhs):.10e}  "
          f"R''(z)/2={float(rhs):.10e}  reldiff={float(reldiff):.3e}")
    assert reldiff < mp.mpf('1e-10'), f"int(u*Q_u)du mismatch at z={z}"
print("PASS: int_0^inf u*Q_u(z)du = R''(z)/2 confirmed by DIRECT quadrature")
print("      (a genuinely independent numerical route from the symbolic")
print("      Fubini-swap derivation of s01 Parts 2-3).")

print()
print("=" * 78)
print("ALL CHECKS PASSED.")
print("=" * 78)
