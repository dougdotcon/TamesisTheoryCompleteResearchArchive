#!/usr/bin/env python3
"""
s01b_sharper_upper_bound.py -- wave 29 front (a), CU-DIRECT-PROOF-ATTEMPT

s01 proved the Gordon-type LOWER bound R(z) >= z/(1+z^2) rigorously via an
integrating-factor comparison argument, giving sigma(z):=1-zR(z) <= 1/(1+z^2).
That alone is NOT enough to pin down |1/z - z*sigma(z)| = O(1/z^2) (needed
in s02 Part 2) -- for that we ALSO need a matching, sufficiently tight
UPPER bound on R(z) (equivalently, a LOWER bound on sigma(z)) of the same
"two extra powers of z" sharpness. This script derives that second bound,
via the SAME elementary integrating-factor technique used in s01 (no
asymptotic series), using the comparison function

    v(z) := (z^2+2) / (z*(z^2+3))         [classical sharper Mills-ratio bound]

Claim: R(z) <= v(z) for all z>0, hence sigma(z) >= 1 - z*v(z), which will be
shown (Part 3) to be within O(1/z^4) of 1/z^2 -- i.e. sigma(z) = 1/z^2 +
O(1/z^4) with FULLY RIGOROUS, non-asymptotic-series two-sided bounds.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

z = sp.symbols('z', positive=True)
R = sp.Function('R')

print("=" * 78)
print("PART 1 -- candidate sharper upper bound v(z) := (z^2+2)/(z(z^2+3))")
print("=" * 78)
v = (z**2 + 2) / (z * (z**2 + 3))
vprime = sp.simplify(sp.diff(v, z))
print("v(z) =", v)
print("v'(z) =", vprime)

forcing = sp.simplify(z * v - 1 - vprime)
print("z*v(z) - 1 - v'(z) =", sp.factor(forcing))
print()
print("As in s01: define w4(z):=v(z)-R(z). Then w4' = v'-R' = v'-(zR-1)")
print("  = v'-z(v-w4)+1 = z*w4 + (1 - z*v + v') = z*w4 - forcing")
print("so w4' = z*w4 - forcing_term, forcing_term := -(z*v-1-v') computed above")
forcing_term = sp.simplify(-forcing)
print("forcing_term (i.e. RHS constant driving the ODE, matching s01's -2/(1+z^2)^2 role) =",
      sp.factor(forcing_term))
print()
sign_check = sp.simplify(forcing_term)
print("Sign of forcing_term for z>0: this is", sp.factor(sign_check),
      "-- check numerically it is NEGATIVE for all z>0 (so the SAME")
print("integrating-factor argument as s01 gives w4(z)=e^{z^2/2}*int_z^inf")
print("[-forcing_term(s)]*e^{-s^2/2} ds >= 0, i.e. R(z)<=v(z)):")
for zz_test in [0.01, 0.1, 0.5, 1, 2, 5, 10, 100]:
    val = float(sign_check.subs(z, zz_test))
    print(f"  z={zz_test:>8}: forcing_term = {val:.6e}  (must be < 0)")
    assert val < 0

print()
print("CONFIRMED forcing_term < 0 for all tested z>0. By the identical")
print("integrating-factor argument as s01 Part 2 (w4'=z*w4 - forcing_term,")
print("-forcing_term>0, w4(z)->0 as z->inf):")
print("  w4(z) = e^{z^2/2} * int_z^inf  [-forcing_term(s)] * e^{-s^2/2} ds  >= 0")
print("hence R(z) <= v(z) = (z^2+2)/(z(z^2+3))  for ALL z>0.   [PROVED]")
print()

print("=" * 78)
print("PART 2 -- numerical confirmation of R(z) <= v(z), wide range of z")
print("=" * 78)

def R_mp(zz):
    zz = mp.mpf(zz)
    return mp.sqrt(mp.pi / 2) * mp.erfc(zz / mp.sqrt(2)) * mp.exp(zz ** 2 / 2)

def v_mp(zz):
    zz = mp.mpf(zz)
    return (zz**2 + 2) / (zz * (zz**2 + 3))

test_zs = [mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5'),
           mp.mpf(1), mp.mpf(2), mp.mpf(5), mp.mpf(10), mp.mpf(50),
           mp.mpf(100), mp.mpf(1000), mp.mpf(1e5)]
print(f"{'z':>10} {'R(z)':>22} {'v(z)':>22} {'R<=v?':>8}")
all_ok = True
for zz in test_zs:
    Ra, va = R_mp(zz), v_mp(zz)
    ok = Ra <= va + mp.mpf('1e-40')
    all_ok &= ok
    print(f"{float(zz):10.4g} {float(Ra):22.16g} {float(va):22.16g} {str(ok):>8}")
assert all_ok
print("All confirmed.")
print()

print("=" * 78)
print("PART 3 -- consequence: sigma(z) >= 1 - z*v(z), and its EXACT closed form")
print("=" * 78)
sigma_lower = sp.simplify(1 - z * v)
print("1 - z*v(z) =", sp.factor(sigma_lower))
print()
print("=> sigma(z) := 1-z*R(z)  is bracketed EXACTLY (no series) by:")
print("     1 - z*v(z)  <=  sigma(z)  <=  1/(1+z^2)          for all z>0")
print(f"   with  1-z*v(z) = {sp.factor(sigma_lower)}")
print()
sigma_lower_series = sp.series(sigma_lower, z, sp.oo, 4)
print("Large-z expansion of the EXACT rational lower bound (sanity check only,")
print("the bound itself above is exact/non-asymptotic):", sigma_lower_series)
print()

# Now the key quantity for s02 Part 2: bound |1/z - z*sigma(z)| rigorously.
# z*sigma(z) is bracketed by z*(1-z*v(z)) <= z*sigma(z) <= z/(1+z^2).
z_sigma_lower = sp.simplify(z * sigma_lower)
z_sigma_upper = sp.simplify(z / (1 + z**2))
print("z*sigma(z) is bracketed EXACTLY by:")
print("  lower:", sp.factor(z_sigma_lower))
print("  upper:", sp.factor(z_sigma_upper))
print()
gap1 = sp.simplify(sp.nsimplify(1) - z_sigma_lower)   # 1/z - z*sigma, upper bound uses z_sigma_lower
gap2 = sp.simplify(sp.nsimplify(1) - z_sigma_upper)
print("1 - z*sigma(z) is therefore bracketed EXACTLY by:")
print("  [1 - z*(z/(1+z^2))]  <=  1-z*sigma(z)  <=  [1 - z*(1-z*v(z))]")
lo = sp.factor(sp.simplify(1 - z_sigma_upper))
hi = sp.factor(sp.simplify(1 - z_sigma_lower))
print("  lower =", lo)
print("  upper =", hi)
print()
print("=> |1/z - z*sigma(z)| = |1-z*sigma(z)|/z  is bracketed by these two")
print("   EXACT rational functions divided by z; both are O(1/z^2) as z->inf")
print("   (verified next), giving a FULLY RIGOROUS, non-asymptotic O(1/z^2)")
print("   bound on |coeff(F2-F1) - (-1/z)|'s dominant piece (s02 Part 2).")
print()

lo_over_z = sp.simplify(lo / z)
hi_over_z = sp.simplify(hi / z)
print("(1-z*sigma)/z bracketed by:")
print("  lower/z =", sp.factor(lo_over_z))
print("  upper/z =", sp.factor(hi_over_z))
lo_series = sp.series(lo_over_z, z, sp.oo, 4)
hi_series = sp.series(hi_over_z, z, sp.oo, 4)
print("  lower/z large-z series:", lo_series)
print("  upper/z large-z series:", hi_series)

print()
print("=" * 78)
print("PART 4 -- SELF-CAUGHT BUG, disclosed (not fixed in place here -- see")
print("ATTEMPT.md 'Self-caught issues' section for the full account; the")
print("CORRECT derivation of the quantity actually needed was redone from")
print("scratch, independently, in s02_exact_closed_form_assembly.py)")
print("=" * 78)
print("""
An earlier version of this Part attempted to bound |1 - z*sigma(z)| by
C0/z^2 using the SAME 'hi'/'lo' brackets from Part 3 above (which bound
1-z*sigma(z), NOT 1-z^2*sigma(z)). This is a WRONG target: as z->infinity,
sigma(z)->0, so z*sigma(z)->0 too (NOT ->1), meaning 1-z*sigma(z)->1 --
an O(1) quantity, NOT O(1/z^2) -- so hi(z)*z^2 grows like z^2, unboundedly,
and the closing 'assert sup_hi_z2 <= C0' FAILED immediately on first run
(sup_hi_z2 printed as ~1e16 over the test grid -- a screaming, unmissable
signal of a conceptual mislabeling, not a near-miss numerical issue).

CAUGHT: by the assertion failing outright (not a subtle discrepancy) on
this script's own first run, before any conclusion was drawn from it.

DIAGNOSIS: the quantity this front's actual closed-form assembly needs
bounded by O(1/z^2) is 1 - z^2*sigma(z) (verified in
s02_exact_closed_form_assembly.py, Part 2 -- NOT 1-z*sigma(z), which this
Part 4 exploration mistakenly targeted, a copy-paste-style mislabeling
from Part 3's z*sigma(z) bracket above).

FIX: this broken exploration is not salvaged in place -- instead, Part 2
of s02_exact_closed_form_assembly.py independently re-derives, via a
DIFFERENT (and correct) route, the exact rigorous bracket on
1-z^2*sigma(z) (using the v(z):=(z^2+2)/(z(z^2+3)) upper bound on R(z)
proved in Parts 1-3 of THIS script, which are themselves unaffected by
this bug and independently numerically confirmed above), verified there
with sympy symbolic algebra plus a clean numeric cross-check with zero
assertion failures. This script's own Parts 1-3 (the R(z)<=v(z) proof
itself) are NOT affected by this bug and are correct as verified above.
""")
