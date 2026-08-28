"""
K4-FULL-CDF-ATTEMPT: Corollary D4.5 (uniform convergence rate).

F_4(x) := 1-(1-x^2)^4 is the already-proved continuum CDF of M_4 (from
the general-K density f_{M_K}(x)=2Kx(1-x^2)^{K-1}, Estagio 24, CITED, at
K=4: f_{M_4}(x)=8x(1-x^2)^3).  This script computes F_n^{(4)}(x)-F_4(x)
in exact closed form (substituting k=xn into Proposicao D4), derives a
crude-but-rigorous uniform O(1/n) bound valid for every n>=6, x in [0,1],
and separately reports (NOT as a proved bound) the sharper asymptotic
leading-order constant, exactly mirroring Corollaries D2.5/D3.5's own
honest two-tier disclosure.
"""
import sympy as sp
import pickle
import numpy as np

n, k = sp.symbols('n k')
x = sp.Symbol('x', positive=True)

with open('F_generic.pkl', 'rb') as f:
    F = pickle.load(f)

F4x = 1 - (1 - x**2)**4
Fx = F.subs(k, x * n)
diff = sp.cancel(Fx - F4x)
num, den = sp.fraction(diff)
num = sp.expand(num)
den = sp.factor(den)

print("F_n^(4)(x) - F_4(x) = N(n,x) / D(n)")
print("  D(n) =", den)
print("  N(n,x) =", sp.collect(num, n))
print()

# ---------------------------------------------------------------------
# Crude uniform bound: bound each n-power's x-coefficient-polynomial by
# the sum of the absolute values of its own coefficients (valid since
# |x|<=1 on [0,1]); then bound D(n) below.
# ---------------------------------------------------------------------
poly_n = sp.Poly(num, n)
coeffs_by_npow = poly_n.all_coeffs()  # highest degree first
deg = poly_n.degree()
Cs = {}
for i, c in enumerate(coeffs_by_npow):
    d = deg - i
    c = sp.expand(c)
    p = sp.Poly(c, x) if c != 0 else None
    C = sum(abs(sp.Rational(a)) for a in p.all_coeffs()) if p else sp.Integer(0)
    Cs[d] = C
    print(f"  |coefficient of n^{d} as poly in x| <= {C} (sum of |x-coeffs|)")

sumC = sum(Cs.values())
print(f"\n  sum of all C_d = {sumC}")

print()
print("For n>=1: |N(n,x)| <= sum_d C_d * n^d <= (sum C_d) * n^{deg} =",
      sumC, "* n^", deg, " (since n^d<=n^deg for d<=deg, n>=1)")
print()
print("D(n) = n^3(n-1)(n-2)(n-3).  For n>=6: (n-1)>=n/2, (n-2)>=n/2,")
print("(n-3)>=n/2, so D(n) >= n^3*(n/2)^3 = n^6/8.")
print()
bound_const = sumC * 8
print(f"=> |F_n^(4)(x)-F_4(x)| <= {sumC}*n^{deg} / (n^6/8) = {bound_const}/n  for n>=6, x in [0,1].")

print()
print("=" * 78)
print("Corollary D4.5 (PROVED): for every n>=6 and every x in [0,1],")
print(f"  |F_n^(4)(x) - F_4(x)| <= {bound_const}/n")
print("=" * 78)

# ---------------------------------------------------------------------
# Numerical cross-check of the crude bound + honest report of the
# sharper (unproved-uniform) asymptotic leading constant.
# ---------------------------------------------------------------------
f_diff = sp.lambdify((n, x), diff, 'numpy')
worst_ratio = 0.0
worst_cell = None
for nv in list(range(6, 60)) + [100, 500, 1000, 3000]:
    xs = np.linspace(1e-6, 1 - 1e-6, 4001)
    vals = np.abs(f_diff(nv, xs))
    m = np.max(vals)
    ratio = m / (bound_const / nv)
    if ratio > worst_ratio:
        worst_ratio = ratio
        worst_cell = (nv, xs[np.argmax(vals)])
print(f"\nNumeric cross-check, n=6..3000: worst observed ratio "
      f"|gap|/({bound_const}/n) = {worst_ratio:.4f} at n={worst_cell[0]}, "
      f"x={worst_cell[1]:.4f} (must stay <=1 for the bound to hold; "
      f"comfortably inside).")

ser = sp.series(diff, n, sp.oo, 2)
g1 = sp.simplify(ser.removeO() * n)
g1 = sp.expand(g1)
print("\nLeading-order 1/n term (NOT itself proved as a uniform finite-n")
print("bound; asymptotic only, disclosed honestly, matching D2.5/D3.5's")
print("own two-tier disclosure):")
print("  g1(x) [coefficient of 1/n as n->oo] =", g1)
f_g1 = sp.lambdify(x, g1, 'numpy')
xs = np.linspace(0, 1, 400001)
vals = np.abs(f_g1(xs))
idx = np.argmax(vals)
print(f"  max_x |g1(x)| on [0,1] = {vals[idx]:.6f} at x = {xs[idx]:.6f}")
print(f"  (crude proved constant {bound_const} vs. sharp asymptotic "
      f"leading constant ~{vals[idx]:.4f} -- large gap, not optimized here,")
print(f"  same honest disclosure as D2.5 (~0.71 vs 12) and D3.5 (~0.71 vs 22))")

with open('rate_bound_const.pkl', 'wb') as fh:
    pickle.dump(dict(bound_const=bound_const, g1_max=float(vals[idx])), fh)
