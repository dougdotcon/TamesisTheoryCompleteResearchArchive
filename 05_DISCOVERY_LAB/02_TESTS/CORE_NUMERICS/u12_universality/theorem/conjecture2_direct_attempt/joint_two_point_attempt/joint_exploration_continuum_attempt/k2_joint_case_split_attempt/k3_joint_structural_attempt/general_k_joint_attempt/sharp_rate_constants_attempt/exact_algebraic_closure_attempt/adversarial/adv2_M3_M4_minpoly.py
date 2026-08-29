"""
Independent computation of M_3, M_4 (max of g_3, g_4 on [0,1]) and their
exact minimal polynomials, using Poly(...).real_roots() (NOT sp.solve),
per this archive's own established bug precedent (Estagio 46 self-caught bug).
Then factor g_3'(x), g_4'(x) to check the "irreducible quartic factor" claim.
"""
import sympy as sp

x, t = sp.symbols('x t')

g3 = 3*x**6 - 3*x**5 - 3*x**2 + 3*x
g4 = -6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x

print("="*70)
print("K=3: g3'(x), real roots in (0,1), M_3")
print("="*70)
g3p = sp.expand(sp.diff(g3, x))
print("g3'(x) =", g3p)
g3p_factored = sp.factor(g3p)
print("factor(g3'(x)) =", g3p_factored)

g3p_poly = sp.Poly(g3p, x)
roots3 = g3p_poly.real_roots()
print("\nreal_roots of g3':", roots3)
interior3 = [r for r in roots3 if 0 < r < 1]
print("interior (0,1) roots:", interior3)
assert len(interior3) == 1, "expected unique interior critical point for g3"
x3star = interior3[0]
M3 = sp.simplify(g3.subs(x, x3star))
M3_n = sp.N(M3, 30)
x3star_n = sp.N(x3star, 30)
print("x3* =", x3star_n)
print("M3 = g3(x3*) =", M3_n)

print("\n" + "="*70)
print("K=4: g4'(x), real roots in (0,1), M_4")
print("="*70)
g4p = sp.expand(sp.diff(g4, x))
print("g4'(x) =", g4p)
g4p_factored = sp.factor(g4p)
print("factor(g4'(x)) =", g4p_factored)

g4p_poly = sp.Poly(g4p, x)
roots4 = g4p_poly.real_roots()
print("\nreal_roots of g4':", roots4)
interior4 = [r for r in roots4 if 0 < r < 1]
print("interior (0,1) roots:", interior4)
assert len(interior4) == 1, "expected unique interior critical point for g4"
x4star = interior4[0]
M4 = sp.simplify(g4.subs(x, x4star))
M4_n = sp.N(M4, 30)
x4star_n = sp.N(x4star, 30)
print("x4* =", x4star_n)
print("M4 = g4(x4*) =", M4_n)

print("\n" + "="*70)
print("Compare against claimed numeric values")
print("="*70)
M3_claimed = sp.Float("0.71207155813802780842", 30)
M4_claimed = sp.Float("0.70871839340932161418", 30)
print("M3 computed  :", M3_n)
print("M3 claimed   :", M3_claimed)
print("diff         :", sp.N(M3_n - M3_claimed, 10))
print()
print("M4 computed  :", M4_n)
print("M4 claimed   :", M4_claimed)
print("diff         :", sp.N(M4_n - M4_claimed, 10))

print("\n" + "="*70)
print("Now: verify claimed minimal polynomials for M_3, M_4")
print("="*70)

# Claimed minimal polys (from task statement):
minpoly_M3_claimed = 15552*t**4 - 3355*t**3 - 42192*t**2 + 181440*t - 110592
minpoly_M4_claimed = 35831808*t**4 - 49852544*t**3 - 220711113*t**2 + 556322688*t - 274710528

print("\nminpoly_M3_claimed =", minpoly_M3_claimed)
val = minpoly_M3_claimed.subs(t, M3)
val_simplified = sp.nsimplify(val, rational=False)
val_num = sp.N(val, 30)
print("Evaluated at exact M3 (algebraic, via real_roots root object):", val_num)
print("Exact simplify (radsimp/simplify) of substitution:", sp.simplify(val))

print("\nminpoly_M4_claimed =", minpoly_M4_claimed)
val4 = minpoly_M4_claimed.subs(t, M4)
val4_num = sp.N(val4, 30)
print("Evaluated at exact M4:", val4_num)
print("Exact simplify of substitution:", sp.simplify(val4))

print("\n" + "="*70)
print("Irreducibility of claimed minimal polynomials over Q")
print("="*70)
p3 = sp.Poly(minpoly_M3_claimed, t, domain='QQ')
print("minpoly_M3_claimed factor_list:", sp.factor_list(minpoly_M3_claimed, t))
print("is irreducible (QQ):", p3.is_irreducible)

p4 = sp.Poly(minpoly_M4_claimed, t, domain='QQ')
print("minpoly_M4_claimed factor_list:", sp.factor_list(minpoly_M4_claimed, t))
print("is irreducible (QQ):", p4.is_irreducible)

print("\n" + "="*70)
print("Cross-check: independently compute minimal_polynomial(M3), (M4) via sympy")
print("="*70)
try:
    mp3 = sp.minimal_polynomial(M3, t)
    print("sp.minimal_polynomial(M3, t) =", mp3)
except Exception as e:
    print("minimal_polynomial(M3) failed:", e)

try:
    mp4 = sp.minimal_polynomial(M4, t)
    print("sp.minimal_polynomial(M4, t) =", mp4)
except Exception as e:
    print("minimal_polynomial(M4) failed:", e)

print("\nDONE.")
