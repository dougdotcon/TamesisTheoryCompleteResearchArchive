"""
Referee check (item 3): verify irreducibility over Q of the two quartic
factors that g3'(x), g4'(x) reduce to after stripping trivial roots
(x=+-1), i.e. the quartics whose roots are x3*, x4* themselves (NOT the
M3/M4 minimal polynomials in t, which are checked separately in
adv2_M3_M4_minpoly.py). Irreducible quartic => always Ferrari-radical-
solvable (degree <=4 is below the Abel-Ruffini boundary) => confirms
there is no Galois-theoretic obstruction at K=3,4.
"""
import sympy as sp
x = sp.symbols('x')
q3 = 6*x**4 + x**3 + x**2 + x - 1
q4 = 12*x**4 - 2*x**3 + x**2 + 2*x - 1
print("q3 factor_list:", sp.factor_list(q3))
print("q3 irreducible (QQ):", sp.Poly(q3, x, domain='QQ').is_irreducible)
print("q4 factor_list:", sp.factor_list(q4))
print("q4 irreducible (QQ):", sp.Poly(q4, x, domain='QQ').is_irreducible)

print("\nDiscriminant q3:", sp.discriminant(q3, x))
print("Discriminant q4:", sp.discriminant(q4, x))

print("\nq3 real_roots:", sp.Poly(q3, x).real_roots())
print("q4 real_roots:", sp.Poly(q4, x).real_roots())
