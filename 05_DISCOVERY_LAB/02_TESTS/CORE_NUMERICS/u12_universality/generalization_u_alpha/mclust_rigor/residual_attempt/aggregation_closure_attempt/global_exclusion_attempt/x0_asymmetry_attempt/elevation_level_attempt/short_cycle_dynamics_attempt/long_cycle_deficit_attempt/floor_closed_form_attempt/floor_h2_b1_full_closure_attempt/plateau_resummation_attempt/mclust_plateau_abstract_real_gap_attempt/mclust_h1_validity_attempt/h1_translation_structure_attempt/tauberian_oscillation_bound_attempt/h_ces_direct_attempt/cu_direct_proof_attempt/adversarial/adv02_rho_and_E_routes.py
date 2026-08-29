#!/usr/bin/env python3
"""
adv02_rho_and_E_routes.py -- hostile referee, wave 29 front (a)
CU-DIRECT-PROOF-ATTEMPT.

Item (b): independently re-derive rho(h',z) = int_0^inf f'(x+h'+u)*Q_u(z)du
(via IBP on the ORIGINAL rho definition, fresh, not importing the target's
s03), and examine whether the target's "TWO independent bounding routes"
for |E(h',z)| are genuinely independent derivations, or just look that way.

Route A (target's s03 Part 3, "bound_route_A"): |E| <= (L2/2)*R''(z),
  bounded further via G3 to L2/(z(1+z^2)).
Route B (target's s03 Part 2, actually derived in the script): |E| <=
  (L2/z)*sigma(z), bounded via G2 to the SAME L2/(z(1+z^2)).

FINDING: Route A's core claim -- that int_0^inf u*Q_u(z) du = R''(z)/2
EXACTLY -- is TRUE (confirmed below via an independent double-integral-swap
derivation and to machine precision numerically), and is a genuinely
DIFFERENT technique from Route B's pointwise majorization R(u+z)<=1/z. So
the two routes ARE mathematically independent. However: this exact
identity (int u*Q_u(z)du = R''(z)/2) is NEVER derived anywhere in the
target's own committed scripts (s01, s02, s03) -- Route A's bound is
simply asserted via a bare prose comment in s03 Part 3, sourced from
ATTEMPT.md's own prose (Sec 3.3) with no derivation shown. The underlying
math is correct (verified here), but the "two independent bounding
routes, cross-checked" claim is under-supported by the actual committed
artifact trail -- only Route B is genuinely derived in code.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40

print("=" * 78)
print("PART 1 -- re-derive rho(h',z) = int_0^inf f'(x+h'+u)*Q_u(z) du via IBP")
print("=" * 78)
u, s, zz_sym, hp, x = sp.symbols('u s z hp x', positive=True)
print("rho(h',z) := int_0^inf e^{-u^2/2-uz} [f(x+h'+u)-f(x+h')] du")
print("For f absolutely continuous: f(x+h'+u)-f(x+h') = int_0^u f'(x+h'+s) ds")
print("(Lebesgue FTC, valid for f Lipschitz -- hyp (C')). Substituting and")
print("swapping order of integration (Fubini, f' bounded, kernel abs. integrable):")
print()
print("  rho(h',z) = int_0^inf f'(x+h'+u) [int_u^inf e^{-w^2/2-wz} dw] du")
print()
w_expr = u + s
target_exp = sp.expand(-w_expr**2/2 - w_expr*zz_sym)
alt_exp = sp.expand(-u**2/2 - u*zz_sym - s**2/2 - s*(u+zz_sym))
diff = sp.simplify(target_exp - alt_exp)
print("Exponent identity -(u+s)^2/2-(u+s)z - [-u^2/2-uz-s^2/2-s(u+z)] =", diff)
assert diff == 0
print("CONFIRMED: int_u^inf e^{-w^2/2-wz} dw = e^{-u^2/2-uz}*R(u+z) =: Q_u(z)")
print("=> rho(h',z) = int_0^inf f'(x+h'+u) * Q_u(z) du.   [matches target Sec 3.3]")
print()

print("=" * 78)
print("PART 2 -- is int_0^inf u*Q_u(z) du EXACTLY R''(z)/2 (Route A's basis)?")
print("=" * 78)
print("Independent derivation via double-integral swap (fresh, not in any")
print("target script): Q_u(z) = int_u^inf e^{-w^2/2-wz} dw, so")
print("  int_0^inf u*Q_u(z) du = int_0^inf u*[int_u^inf e^{-w^2/2-wz}dw] du")
print("    = int_0^inf e^{-w^2/2-wz} [int_0^w u du] dw   (swap: u in [0,w] for fixed w)")
print("    = int_0^inf e^{-w^2/2-wz} * (w^2/2) dw")
print("    = (1/2) * int_0^inf w^2 e^{-w^2/2-wz} dw")
print("    = R''(z)/2       [since R''(z) = int_0^inf u^2 e^{-u^2/2-uz} du,")
print("      confirmed by direct double differentiation under the integral]")
print()
print("This is an EXACT algebraic identity, not a bound -- verified numerically")
print("to full mpmath precision below (NOT shown or derived anywhere in the")
print("target's own s01/s02/s03):")
print()

def R_mp(zz):
    zz = mp.mpf(zz)
    return mp.sqrt(mp.pi/2)*mp.erfc(zz/mp.sqrt(2))*mp.exp(zz**2/2)
def Rpp_mp(zz):
    zz = mp.mpf(zz)
    f = lambda uu: uu**2 * mp.e**(-uu**2/2 - uu*zz)
    return mp.quad(f, [0, mp.inf])
def Q_u(uu, zz):
    uu = mp.mpf(uu); zz = mp.mpf(zz)
    return mp.e**(-uu**2/2 - uu*zz) * R_mp(uu+zz)
def first_moment_Q(zz):
    zz = mp.mpf(zz)
    f = lambda uu: uu * Q_u(uu, zz)
    return mp.quad(f, [0, 4, 12, 30, 60, mp.inf])
def sigma_mp(zz):
    zz = mp.mpf(zz)
    return 1 - zz*R_mp(zz)

rpp_label = "R''(z)/2"
print(f"{'z':>6} {'int u*Q_u du':>20} {rpp_label:>20} {'reldiff':>10}")
all_ok = True
for zz in [1, 2, 5, 10, 50, 100]:
    a = first_moment_Q(zz)
    b = Rpp_mp(zz)/2
    reldiff = abs(a-b)/abs(b)
    all_ok &= reldiff < mp.mpf('1e-30')
    print(f"{zz:6} {float(a):20.14e} {float(b):20.14e} {float(reldiff):10.2e}")
assert all_ok
print("CONFIRMED EXACT: int u*Q_u(z) du = R''(z)/2, to full precision. Route A's")
print("core claim is mathematically TRUE (an exact identity, not merely a bound).")
print()

print("=" * 78)
print("PART 3 -- Route B (genuinely derived in target's s03 Part 2): a")
print("DIFFERENT, cruder pointwise majorization")
print("=" * 78)
print("Route B bounds the SAME exact quantity int u*Q_u(z)du via R(u+z)<=1/z")
print("(pointwise, u>=0 => u+z>=z), giving int u*Q_u(z)du <= (1/z)*sigma(z)")
print("-- a genuine UPPER BOUND (not exact), via a DIFFERENT technique (pointwise")
print("majorization of R, not a double-integral swap identity for R''):")
print()
print(f"{'z':>6} {'exact: int u*Q_u du':>22} {'Route B bound (1/z)sigma(z)':>30} {'A<=B?':>8}")
for zz in [1,2,5,10,50,100]:
    a = first_moment_Q(zz)
    b = sigma_mp(zz)/mp.mpf(zz)
    print(f"{zz:6} {float(a):22.10e} {float(b):30.10e} {str(a<=b):>8}")
print()
print("Both G2 (used by Route B: R(z)>=z/(1+z^2) => sigma<=1/(1+z^2)) and G3")
print("(used by Route A: R(z)<=1/z => R''(z)<=2/(z(1+z^2))) use OPPOSITE")
print("directions of the G1 bracket, yet both final bounds collapse to the")
print("SAME formula L2/(z(1+z^2)) -- not a coincidence: R''(z) and sigma(z)")
print("are algebraically linked (R''(z) = [1-sigma(z)(1+z^2)]/z, verified below),")
print("but they are genuinely DIFFERENT quantities, and Route A computes an")
print("EXACT value for one (R''(z)/2) while Route B only bounds a RELATED")
print("but distinct quantity via a cruder pointwise argument.")
Rpp_alg = sp.symbols('Rpp')
z_s, sigma_s = sp.symbols('z sigma', positive=True)
lhs_check = sp.simplify((1 - sigma_s*(1+z_s**2))/z_s)
print()
print("Algebraic link R''(z) = [1-sigma(z)(1+z^2)]/z re-derived (from")
print("R''=(1+z^2)*w1(z), w1=R-z/(1+z^2), R=(1-sigma)/z -- elementary algebra):")
w1_expr = (1-sigma_s)/z_s - z_s/(1+z_s**2)
Rpp_expr = sp.simplify((1+z_s**2)*w1_expr)
match = sp.simplify(Rpp_expr - lhs_check) == 0
print("  R''(z) via w1 =", sp.simplify(Rpp_expr), " -- matches [1-sigma(1+z^2)]/z ?", match)
assert match
print()
print("VERDICT on item (b): the 'two independent bounding routes' ARE genuinely")
print("mathematically independent (different techniques, opposite G1")
print("directions), and Route A's underlying claim is TRUE and exact -- but")
print("Route A's derivation (the double-integral swap giving R''(z)/2 exactly)")
print("is NEVER shown in the target's own s01/s02/s03 scripts; it is only")
print("asserted via prose. This is a genuine, LOW-severity documentation gap")
print("(the substantive claim survives independent re-derivation here), not a")
print("mathematical error.")
