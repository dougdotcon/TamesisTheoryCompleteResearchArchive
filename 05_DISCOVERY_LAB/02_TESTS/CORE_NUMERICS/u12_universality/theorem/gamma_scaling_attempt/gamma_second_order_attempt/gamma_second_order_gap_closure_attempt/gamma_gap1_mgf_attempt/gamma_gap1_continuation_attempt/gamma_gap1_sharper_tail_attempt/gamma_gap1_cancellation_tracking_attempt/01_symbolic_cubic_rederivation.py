"""
01_symbolic_cubic_rederivation.py

Fresh, from-scratch symbolic (sympy) re-derivation of:
  tau(m)      := sum_{i=1}^m ((k-i)/n)^2      [closed form, cubic in m]
  delta(D)    := D(2k(1-gamma)-D-1)/(2n)       [cited exact identity, wave-17]
  x(D)        := delta(D) + tau(gamma*k+D)/2   [Gap 1's combined object]
as an exact cubic polynomial in D, with closed-form coefficients c0..c3.

No .py file from any ancestor/sibling front was read or imported. Every
derivation below is redone from the mathematical prose of THEOREM.md and
the three ancestor ATTEMPT.md files (which are read-only source material,
never code).

Cross-checks c0..c3 against the grandparent's (gamma_gap1_mgf_attempt)
ADVERSARIALLY-CORRECTED closed forms:
  c0 = (gamma*k/(12*n^2)) * (2*gamma^2*k^2 - 6*gamma*k^2 + 3*gamma*k + 6*k^2 - 6*k + 1)
  c1 = (1/n^2) * [ gamma^2*k^2/2 - gamma*k^2 - gamma*k*n + gamma*k/2 + k^2/2 + k*n - k/2 - n/2 + 1/12 ]
  c2 = (2*gamma*k - 2*k - 2*n + 1) / (4*n^2)
  c3 = 1/(6*n^2)
"""
import sympy as sp

k, n, gamma, m, D, M = sp.symbols('k n gamma m D M', positive=False)

print("=" * 78)
print("PART A -- tau(m) closed form, fresh sympy.summation")
print("=" * 78)

i = sp.Symbol('i', integer=True, positive=True)
tau_sum = sp.summation(((k - i) / n) ** 2, (i, 1, m))
tau_m = sp.expand(tau_sum)
print("tau(m) =", tau_m)

# Sanity: tau(m) must be a cubic polynomial in m (for fixed k,n)
tau_poly_m = sp.Poly(tau_m, m)
print("degree in m:", tau_poly_m.degree())
assert tau_poly_m.degree() == 3, "tau(m) must be exactly cubic in m"

# Direct brute-force check for several small integer (k,m,n) that the
# closed form matches literal summation -- independent of the symbolic
# summation machinery itself.
import random
random.seed(1)  # deterministic small sanity grid, not a "drawn seed" per
                 # this front's discipline (see Seeds section of ATTEMPT.md)
mismatches = 0
for _ in range(40):
    kk = random.randint(5, 60)
    nn = random.randint(kk + 1, 200)
    mm = random.randint(0, kk)
    lhs = sum(sp.Rational((kk - ii), nn) ** 2 for ii in range(1, mm + 1))
    rhs = tau_m.subs({k: kk, n: nn, m: mm})
    if sp.simplify(lhs - rhs) != 0:
        mismatches += 1
        print("MISMATCH", kk, nn, mm, lhs, rhs)
print(f"brute-force tau(m) check: 40 random (k,n,m) triples, {mismatches} mismatches")
assert mismatches == 0

print()
print("=" * 78)
print("PART B -- x(D) := delta(D) + tau(gamma*k+D)/2, exact cubic in D")
print("=" * 78)

delta_D = D * (2 * k * (1 - gamma) - D - 1) / (2 * n)
tau_M = tau_m.subs(m, gamma * k + D)
x_D = sp.expand(delta_D + tau_M / 2)

x_poly = sp.Poly(x_D, D)
print("degree in D:", x_poly.degree())
assert x_poly.degree() == 3, "x(D) must be exactly cubic in D"

c3_route1 = x_poly.coeff_monomial(D ** 3)
c2_route1 = x_poly.coeff_monomial(D ** 2)
c1_route1 = x_poly.coeff_monomial(D)
c0_route1 = x_poly.coeff_monomial(1)

c0_route1 = sp.simplify(c0_route1)
c1_route1 = sp.simplify(c1_route1)
c2_route1 = sp.simplify(c2_route1)
c3_route1 = sp.simplify(c3_route1)

print("c0 (route 1, direct Poly extraction) =", c0_route1)
print("c1 (route 1) =", c1_route1)
print("c2 (route 1) =", c2_route1)
print("c3 (route 1) =", c3_route1)

print()
print("-" * 78)
print("Route 2: derivative-based hand assembly (tau, tau', tau'' at m=gamma*k)")
print("-" * 78)

tau_p = sp.diff(tau_m, m)
tau_pp = sp.diff(tau_m, m, 2)

c0_route2 = sp.simplify(tau_m.subs(m, gamma * k) / 2)
c1_route2 = sp.simplify(k * (1 - gamma) / n - sp.Rational(1, 2) / n + tau_p.subs(m, gamma * k) / 2)
c2_route2 = sp.simplify(-sp.Rational(1, 2) / n + tau_pp.subs(m, gamma * k) / 4)
c3_route2 = sp.Rational(1, 6) / n ** 2

print("c0 (route 2, derivative-based) =", c0_route2)
print("c1 (route 2) =", c1_route2)
print("c2 (route 2) =", c2_route2)
print("c3 (route 2) =", c3_route2)

print()
print("-" * 78)
print("Cross-check route 1 vs route 2 (must be exactly zero difference)")
print("-" * 78)
d0 = sp.simplify(c0_route1 - c0_route2)
d1 = sp.simplify(c1_route1 - c1_route2)
d2 = sp.simplify(c2_route1 - c2_route2)
d3 = sp.simplify(c3_route1 - c3_route2)
print("diff c0:", d0)
print("diff c1:", d1)
print("diff c2:", d2)
print("diff c3:", d3)
assert d0 == 0 and d1 == 0 and d2 == 0 and d3 == 0, "route1/route2 must match exactly"

print()
print("=" * 78)
print("PART C -- cross-check against grandparent's adversarially-corrected c_i")
print("=" * 78)

c0_grandparent = (gamma * k / (12 * n ** 2)) * (
    2 * gamma ** 2 * k ** 2 - 6 * gamma * k ** 2 + 3 * gamma * k + 6 * k ** 2 - 6 * k + 1
)
c1_grandparent = (sp.Rational(1, 1) / n ** 2) * (
    gamma ** 2 * k ** 2 / 2 - gamma * k ** 2 - gamma * k * n + gamma * k / 2
    + k ** 2 / 2 + k * n - k / 2 - n / 2 + sp.Rational(1, 12)
)
c2_grandparent = (2 * gamma * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
c3_grandparent = sp.Rational(1, 6) / n ** 2

dg0 = sp.simplify(c0_route1 - c0_grandparent)
dg1 = sp.simplify(c1_route1 - c1_grandparent)
dg2 = sp.simplify(c2_route1 - c2_grandparent)
dg3 = sp.simplify(c3_route1 - c3_grandparent)
print("diff vs grandparent c0:", dg0)
print("diff vs grandparent c1:", dg1)
print("diff vs grandparent c2:", dg2)
print("diff vs grandparent c3:", dg3)
assert dg0 == 0 and dg1 == 0 and dg2 == 0 and dg3 == 0, \
    "must match grandparent's adversarially-corrected closed forms exactly"

print()
print("Numeric spot check at the referee's own test point gamma=1/2,k=10,n=100:")
val = c0_route1.subs({gamma: sp.Rational(1, 2), k: 10, n: 100})
print("c0(1/2,10,100) =", val, " (expected 51/4000 =", sp.Rational(51, 4000), ")")
assert val == sp.Rational(51, 4000)

print()
print("ALL CHECKS PASSED. Working c_i (route 1 == route 2 == grandparent's")
print("corrected forms, exact zero symbolic difference in all cases).")

print()
print("=" * 78)
print("PART D -- exact (not crude) support of D = M - gamma*k")
print("=" * 78)
print("M ~ Bin(k,gamma) so M in [0,k] exactly (integer-valued, but the")
print("*range* of the real number D=M-gamma*k is exactly the closed")
print("interval [-gamma*k, (1-gamma)*k] -- attained at M=0 and M=k")
print("respectively. This is EXACT, not a bound -- it is what M's own")
print("definition as a Binomial count directly gives, requiring no")
print("further argument.")
print()
print("Contrast with the Bulk/Tail Lemma's existing crude tail-region use")
print("of |D| <= k (i.e. the symmetric interval [-k,k]), which is a valid")
print("but strictly looser superset whenever gamma != 1/2 -- e.g. gamma=0.01")
print("gives true D in [-0.01k, 0.99k], NOT [-k,k]; gamma=0.99 gives true D")
print("in [-0.99k, 0.01k], NOT [-k,k]. This asymmetry is exploited in script 02.")
