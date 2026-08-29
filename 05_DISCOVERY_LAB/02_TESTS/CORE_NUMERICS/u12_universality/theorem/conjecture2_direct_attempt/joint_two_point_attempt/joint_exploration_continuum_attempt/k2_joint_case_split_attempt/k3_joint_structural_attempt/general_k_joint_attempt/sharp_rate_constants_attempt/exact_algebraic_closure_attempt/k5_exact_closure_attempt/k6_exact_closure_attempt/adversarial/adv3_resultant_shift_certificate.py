"""
Hostile referee, K6-EXACT-CLOSURE-ATTEMPT. THE central, highest-priority
independent check for this review.

Independently reconstructs, from scratch, g6(x), M6 (+ minimal
polynomial), the boundary threshold, R(n,m):=Res_x(F1,F2), S(n) (upper
target) and S2(n) (lower target), and then independently verifies BOTH
headline shift-certificate claims:

  (a) S(y+8) has uniform-sign coefficients => S(n) has no real root
      exceeding 8 (closes the UPPER bound).
  (b) S2(y+35) has uniform-sign coefficients => S2(n) has no real root
      exceeding 35 (closes the LOWER bound, after the genuine K=4-style
      wrinkle: S2(y+8) is NOT uniform-sign).

D6(n,k) is taken from adv1_D6_derivation.py's own independently-derived
and independently-confirmed result (not re-derived a third time here --
adv1 already proved, via a completely independently-typed pipeline, that
it is symbolically IDENTICAL to the target's own claimed D6). Everything
from g6(x) onward in this script is fresh code, independent of the
target's k6_exact_closure.py (read only per the review's task
instructions, to know which specific numeric claims to check).
"""
import time
import sympy as sp

n, x, k, m, t = sp.symbols('n x k m t', real=True)
K = 6

print("=" * 78)
print("STEP 0: D6(n,k), taken from adv1's own independently-confirmed result")
print("=" * 78)
Bracket6 = (
    -k**10 + 25*k**9 + 6*k**8*n**2 - 45*k**8*n - 270*k**8 - 96*k**7*n**2
    + 760*k**7*n + 1650*k**7 - 15*k**6*n**4 + 195*k**6*n**3 - 9*k**6*n**2
    - 5380*k**6*n - 6273*k**6 + 135*k**5*n**4 - 1875*k**5*n**3
    + 4359*k**5*n**2 + 20734*k**5*n + 15345*k**5 + 20*k**4*n**6
    - 330*k**4*n**5 + 1375*k**4*n**4 + 3600*k**4*n**3 - 22441*k**4*n**2
    - 47215*k**4*n - 24080*k**4 - 80*k**3*n**6 + 1440*k**3*n**5
    - 7975*k**3*n**4 + 4641*k**3*n**3 + 50821*k**3*n**2 + 64330*k**3*n
    + 23300*k**3 - 15*k**2*n**8 + 270*k**2*n**7 - 1730*k**2*n**6
    + 3435*k**2*n**5 + 7610*k**2*n**4 - 20391*k**2*n**3 - 58916*k**2*n**2
    - 50320*k**2*n - 12576*k**2 + 15*k*n**8 - 310*k*n**7 + 2360*k*n**6
    - 7055*k*n**5 + 730*k*n**4 + 20526*k*n**3 + 33716*k*n**2 + 20016*k*n
    + 2880*k + 6*n**10 - 105*n**9 + 720*n**8 - 2375*n**7 + 3384*n**6
    - 10*n**5 - 1860*n**4 - 6696*n**3 - 7440*n**2 - 2880*n
)
Dn6 = n ** 7 * (n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)
D6_formula = k * (k + 1) * Bracket6 / Dn6
print("D6(n,k) loaded (independently confirmed correct by adv1).")

print()
print("=" * 78)
print("STEP 1: g6(x), M6 -- re-derived independently")
print("=" * 78)
F6n = sp.cancel(D6_formula.subs(k, n * x))
F6_cont = sp.expand(1 - (1 - x ** 2) ** K)
Delta6 = sp.cancel(F6n - F6_cont)
Num6 = sp.expand(sp.cancel(Delta6 * Dn6))
h6 = sp.cancel(n * Delta6)

Npoly_n = sp.Poly(Num6, n)
g6 = sp.expand(Npoly_n.coeff_monomial(n ** Npoly_n.degree()))
g6_factored_claim = sp.expand(-3 * x * (x - 1) ** 5 * (x + 1) ** 4 * (5 * x ** 2 - 3 * x + 2))
assert sp.simplify(g6 - g6_factored_claim) == 0
print("g6(x) = -3x(x-1)^5(x+1)^4(5x^2-3x+2) -- CONFIRMED (referee's own re-derivation).")

g6p = sp.expand(sp.diff(g6, x))
g6p_factored_claim = sp.expand(-6 * (x - 1) ** 4 * (x + 1) ** 3 * (30 * x ** 4 - 14 * x ** 3 + x ** 2 + 4 * x - 1))
assert sp.simplify(g6p - g6p_factored_claim) == 0
print("g6'(x) = -6(x-1)^4(x+1)^3(30x^4-14x^3+x^2+4x-1) -- CONFIRMED.")

quartic_interior = sp.Poly(30 * x ** 4 - 14 * x ** 3 + x ** 2 + 4 * x - 1, x)
assert quartic_interior.is_irreducible
print("Interior quartic 30x^4-14x^3+x^2+4x-1 irreducible over Q -- CONFIRMED "
      "(referee's own sp.Poly(...).is_irreducible call).")

crit = sp.Poly(g6p, x).real_roots()
print(f"g6'(x) real roots (with multiplicity), referee's own count: {len(crit)}")
interior = [c for c in crit if 0 < sp.N(c) < 1]
assert len(interior) == 1
x6star = interior[0]
M6 = sp.simplify(g6.subs(x, x6star))
print("x6* =", sp.N(x6star, 35))
print("M6  =", sp.N(M6, 35))

minpoly_M6 = sp.minimal_polynomial(M6, t)
assert sp.Poly(minpoly_M6, t).is_irreducible
print("minpoly(M6) [referee's own sp.minimal_polynomial call]:")
print(" ", minpoly_M6)

target_minpoly = sp.expand(
    35429400000000000 * t ** 4 + 17921731935293824 * t ** 3
    - 248044660324924125 * t ** 2 + 350950285900800000 * t
    - 137134080000000000
)
diff_minpoly = sp.expand(sp.Poly(minpoly_M6, t).as_expr() - target_minpoly)
# they may differ by an overall constant factor (both are "the" minimal
# polynomial up to scaling/sign, sympy's own normalization may or may not
# match the target's printed form) -- check ratio is a constant.
ratio = sp.simplify(sp.Poly(minpoly_M6, t).as_expr() / target_minpoly)
print("minpoly(M6) [referee] / minpoly(M6) [target, transcribed] =", ratio,
      "(should be a nonzero rational constant if both represent the SAME "
      "minimal polynomial up to normalization)")
assert ratio.is_rational and ratio != 0
print("CONFIRMED: same minimal polynomial (up to constant rational factor).")

print()
print("=" * 78)
print("STEP 2: boundary value h6(n,1), and its crossing with -M6")
print("=" * 78)
h1 = sp.factor(h6.subs(x, 1))
print("h6(n,1) =", h1)
assert sp.simplify(h1 - (-720 / ((n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)))) == 0
print("CONFIRMED: h6(n,1) = -720/[(n-1)(n-2)(n-3)(n-4)(n-5)] (referee's own "
      "independent simplification).")

# Solve h6(n,1) = -M6 exactly via resultant elimination against M6's own
# minimal polynomial (an independently-constructed elimination, not
# copied from the target's own G_bnd/boundary_threshold routine).
# Gb=0 defines m := 720/[(n-1)...(n-5)] = -h6(n,1); we want h6(n,1)=-M6,
# i.e. m=M6 (or an algebraic conjugate) -- so eliminate m against
# minpoly_M6 DIRECTLY (t -> m, not negated).
#
# NOTE (self-caught sign bug, disclosed honestly): a first version of
# this script eliminated against minpoly_M6.subs(t, -m) here by mistake
# (the substitution appropriate for the OTHER, physically-irrelevant
# crossing h6(n,1)=+M6), producing a spurious n0_boundary=6.2609... that
# did NOT match the target's claimed 7.2786.... Caught immediately by
# the mismatch assertion below firing; root-caused by direct numeric
# solving of h6(n,1)=-M6 via mpmath.findroot as an independent tie-
# breaker (see the referee report), which confirmed 7.2786... is the
# genuinely correct crossing and pinpointed the sign error as the
# referee's own bug, not the target's.
Gb = sp.expand(((n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)) * m - 720)
Sb_lower = sp.expand(sp.resultant(sp.Poly(Gb, m), sp.Poly(minpoly_M6.subs(t, m), m)))
roots_b = sp.Poly(Sb_lower, n).real_roots()
roots_b_num = [sp.N(r, 25) for r in roots_b]
n0_boundary = max(r for r in roots_b_num if r > 5)
print("n0_boundary (h6(n,1)=-M6 crossing, referee's own independent "
      "elimination) =", n0_boundary)
assert abs(float(n0_boundary) - 7.278581437127420988290004) < 1e-15
print("MATCHES the target's claimed value 7.278581437127420988290004... "
      "to the digits shown.  CONFIRMED.")

print()
print("=" * 78)
print("STEP 3: R(n,m) = Res_x(F1,F2); S(n) upper, S2(n) lower")
print("=" * 78)
F1 = sp.expand(sp.diff(Num6, x))
F2 = sp.expand(m * Dn6 - n * Num6)
t0 = time.time()
R = sp.expand(sp.resultant(F1, F2, x))
Rpoly_check = sp.Poly(R, n, m)
print(f"Res_x(F1,F2) elapsed: {time.time()-t0:.2f}s  "
      f"deg_n={sp.Poly(R,n).degree()}  deg_m={sp.Poly(R,m).degree()}")
assert sp.Poly(R, n).degree() == 264
assert sp.Poly(R, m).degree() == 11
print("Matches target's claimed R(n,m) degrees (264 in n, 11 in m).  CONFIRMED.")

t0 = time.time()
S = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_M6.subs(t, m), m)))
Spoly = sp.Poly(S, n)
print(f"S(n) [upper target] elapsed: {time.time()-t0:.2f}s  degree={Spoly.degree()}")
assert Spoly.degree() == 1052

t0 = time.time()
S2 = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_M6.subs(t, -m), m)))
S2poly = sp.Poly(S2, n)
print(f"S2(n) [lower target] elapsed: {time.time()-t0:.2f}s  degree={S2poly.degree()}")
assert S2poly.degree() == 1056
print("Both degrees (1052, 1056) match the target's claims.  CONFIRMED.")

print()
print("=" * 78)
print("STEP 4: shift-certificate verification (the headline check)")
print("=" * 78)


def shift_certificate(poly, B):
    """Referee's own independent implementation. Uses Poly.shift(B),
    independently sanity-checked (see adv3b_shift_sanity.py/.log) to
    confirm it truly computes P(y+B) with y the SAME generator symbol --
    not merely trusted because the target used it."""
    shifted = poly.shift(B)
    coeffs = shifted.all_coeffs()
    nz = [c for c in coeffs if c != 0]
    signs = set(sp.sign(c) for c in nz)
    return len(signs) <= 1, coeffs


ok8, coeffs_S_at_8 = shift_certificate(Spoly, 8)
print(f"(a) S(y+8) uniform-sign: {ok8}")
assert ok8
signs_S8 = set(sp.sign(c) for c in coeffs_S_at_8 if c != 0)
print(f"    signs present: {signs_S8}  (all coefficients share this sign)")
print("    => rigorously, NO real root of S(n) exceeds 8.  INDEPENDENTLY CONFIRMED.")

ok8_2, coeffs_S2_at_8 = shift_certificate(S2poly, 8)
print(f"\nS2(y+8) uniform-sign: {ok8_2}  (target claims this should be False "
      f"-- the genuine wrinkle)")
assert not ok8_2
print("    CONFIRMED: inconclusive at B=8, exactly as the target reports "
      "(the genuine K=4-style wrinkle is real, not a fabricated pretext "
      "for a weaker method).")

ok35, coeffs_S2_at_35 = shift_certificate(S2poly, 35)
print(f"\n(b) S2(y+35) uniform-sign: {ok35}")
assert ok35
signs_S2_35 = set(sp.sign(c) for c in coeffs_S2_at_35 if c != 0)
print(f"    signs present: {signs_S2_35}")
print("    => rigorously, NO real root of S2(n) exceeds 35.  INDEPENDENTLY CONFIRMED.")

# Also check the immediately-preceding bound (34) is genuinely NOT enough
# -- i.e. B=35 is not an arbitrary overshoot with no content; there really
# is a root strictly between 34 and 35, matching the target's own claim.
ok34, _ = shift_certificate(S2poly, 34)
print(f"\nS2(y+34) uniform-sign: {ok34}  (expect False: 35 is where it first clears)")
assert not ok34

print()
print("=" * 78)
print("STEP 5: direct sign evaluation of S2(n) at integers 28..37")
print("(independent confirmation the sign change is genuine, not a")
print("shift-certificate artifact)")
print("=" * 78)
prev_sign = None
prev_val = None
change_at = None
for nv in range(28, 38):
    val = S2poly.eval(nv)
    sgn = sp.sign(val)
    print(f"  S2({nv}) sign = {sgn}   (referee's own direct sp.Poly.eval)")
    if prev_sign is not None and sgn != prev_sign and change_at is None:
        change_at = (nv - 1, nv)
    prev_sign = sgn
print(f"\nSign change located at: {change_at}")
assert change_at == (34, 35)
print("CONFIRMED: genuine sign change strictly between n=34 and n=35, "
      "independently reproduced by direct polynomial evaluation at "
      "integers (no root-isolation machinery used at all).")

print()
print("=" * 78)
print("ALL STEP-4/5 HEADLINE CLAIMS INDEPENDENTLY CONFIRMED.")
print("=" * 78)
print(f"M6 = {sp.N(M6, 40)}")
print(f"minpoly(M6) [referee] = {minpoly_M6}")
