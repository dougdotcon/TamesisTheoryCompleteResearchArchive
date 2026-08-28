"""
Corollary D2.2 (uniform convergence rate): compares Proposicao D2's
finite-n CDF F_n^(2)(x) (x=k/n) to the already-proved continuum CDF
F_2(x) := 1-(1-x^2)^2 = 2x^2-x^4 (from f_{M_2}(x)=4x(1-x^2), THEOREM.md
Estagio 15, cited, NOT re-derived here), and derives a rigorous uniform
O(1/n) bound on the gap, in the style of k3_full_cdf_attempt's Corollary
D3.5.
"""
import sympy as sp

n, x, k = sp.symbols('n x k', positive=True)

D2_k = -k * (k + 1) * (k**2 - k - 2*n**2 + 3*n) / (n**3 * (n - 1))
D2_x = sp.simplify(D2_k.subs({k: x * n}))

F2 = 1 - (1 - x**2)**2
F2 = sp.expand(F2)

gap = sp.cancel(D2_x - F2)
gap = sp.together(gap)
print("F_n^(2)(x) - F_2(x) [exact, x=k/n substituted directly into D2]:")
print(f"  gap = {gap}")

# Express gap = N(n,x) / D(n), extract N and D
num, den = sp.fraction(sp.together(gap))
num = sp.expand(num)
den = sp.expand(den)
print(f"\n  numerator N(n,x)   = {num}")
print(f"  denominator D(n)   = {den}")

# Leading 1/n term (n->oo expansion at fixed x)
series = sp.series(gap, n, sp.oo, 3).removeO()
print(f"\n  Laurent series in 1/n (fixed x): {sp.nsimplify(series)}")
g1 = sp.simplify(sp.limit(gap * n, n, sp.oo))
print(f"  leading term coefficient g1(x) := lim n*(F_n-F_2) = {g1}")

# max |g1(x)| over x in [0,1]
g1_prime = sp.diff(g1, x)
crit = sp.solve(sp.Eq(g1_prime, 0), x)
print(f"\n  critical points of g1(x) on (0,1): {crit}")
vals = [g1.subs(x, c) for c in crit if c.is_real and 0 < c < 1] if crit else []
vals += [g1.subs(x, 0), g1.subs(x, 1)]
vals_num = [sp.N(v) for v in vals]
print(f"  g1 values at endpoints/critical points: {list(zip(crit if crit else [], vals_num))}")
maxabs = max(abs(v) for v in vals_num)
print(f"  max |g1(x)| on [0,1] ~= {maxabs}")

# Rigorous uniform bound: bound |num| by sum of |coeffs| (as poly in n,
# each coeff itself a poly in x bounded on [0,1] by sum of |coeffs in x|),
# and lower-bound den = n^3(n-1) crudely.
print("\n--- Rigorous finite-n uniform bound ---")
# num as polynomial in n; coefficients are polys in x
num_poly_n = sp.Poly(num, n)
coeffs_in_n = num_poly_n.all_coeffs()  # highest degree first
bound_on_x01 = 0
for c in coeffs_in_n:
    c = sp.expand(c)
    # bound |c(x)| for x in [0,1] by sum of abs of its coefficients
    cp = sp.Poly(c, x) if c != 0 else None
    if cp is None:
        continue
    bound_on_x01 += sum(abs(sp.Rational(a)) for a in cp.all_coeffs())
print(f"  sum over n-degree coefficients of (sum |x-coeffs|) = {bound_on_x01}")

# so |N(n,x)| <= bound_on_x01 * (some poly bound in n, since each coeff c_i(x)
# multiplies n^i) -- more directly: bound |N(n,x)| <= sum_i |c_i(x)| * n^i
# <= (sum_i sup|c_i(x)|) * n^{deg} for n>=1. Let's just print the coefficients
# themselves and their sup on [0,1] explicitly, deg by deg, to get an exact,
# checkable bound (not hidden inside one lumped constant).
print("\n  Numerator N(n,x) coefficients by power of n (highest degree first):")
deg = num_poly_n.degree()
total_bound_expr = 0
for i, c in enumerate(coeffs_in_n):
    power = deg - i
    c = sp.expand(c)
    if c == 0:
        continue
    cpoly = sp.Poly(c, x)
    sup_bound = sum(abs(sp.Rational(a)) for a in cpoly.all_coeffs())  # crude sup bound on [0,1] via |sum|coeff||
    print(f"    n^{power}: coeff(x) = {c}   crude sup-bound on [0,1] <= {sup_bound}")
    total_bound_expr += sup_bound * n**power

print(f"\n  => |N(n,x)| <= {total_bound_expr} for all x in [0,1], n>=1 "
      f"(crude bound, each x-coefficient bounded by sum of |coeffs|)")

den_expanded = sp.expand(den)
print(f"  D(n) = {den_expanded} = n(n-1)")

# N(n,x) has degree EXACTLY 1 in n (the n^3(n-1) from D2's own
# denominator cancels three powers of n against the k=xn substitution --
# genuinely simpler than K3's rate corollary, not an error): from the
# printout above, |N(n,x)| <= 4n + 4 for every x in [0,1], n>=1 (each
# n-coefficient of N, as a polynomial in x, is bounded on [0,1] by the
# sum of the absolute values of its own coefficients -- both equal 4
# here). D(n) = n(n-1) >= n^2/2 for n>=2 (since n-1>=n/2 there).
print("\n  Elementary rigorous bound: for n>=2, (n-1)>=n/2, so "
      "D(n)=n(n-1)>=n^2/2.")
print("  Combined with |N(n,x)|<=4n+4 (proved above, coefficient-sum "
      "method), for n>=2:")
print("    |F_n^(2)(x)-F_2(x)| <= (4n+4)/(n^2/2) = 8/n + 8/n^2 <= 12/n")
print("  (using 8/n^2<=4/n for n>=2) -- a genuine, rigorously proved, "
      "uniform O(1/n) bound for every n>=2, x in [0,1].")

import numpy as np
worst_n_times_gap = 0
worst_n = None
for nv in list(range(2, 200)) + [500, 1000, 2000, 5000]:
    xs = np.linspace(0, 1, 401)
    for xv in xs:
        val = float(gap.subs({n: nv, x: xv}))
        if abs(val) * nv > worst_n_times_gap:
            worst_n_times_gap = abs(val) * nv
            worst_n = (nv, xv)
print(f"\n  Numerically observed sup_n,x [n * |F_n^(2)(x)-F_2(x)|] "
      f"~= {worst_n_times_gap:.6f} at (n,x)~={worst_n}")
print(f"  (compare to max|g1(x)|~={float(maxabs):.6f} -- the asymptotic "
      f"leading-order sup)")
print(f"  Proved crude uniform bound is 12/n (i.e. n*gap<=12) -- observed "
      f"worst case {worst_n_times_gap:.4f} is comfortably inside it, and "
      f"consistent with the tight asymptotic constant ~0.7107.")

# Direct check that the proved bound 12/n actually dominates the exact
# gap for a wide range of n (not just the sampled worst case above).
print("\n  Direct check that 12/n bound holds (n=2..3000, dense x grid):")
worst_ratio = 0
for nv in list(range(2, 60)) + list(range(60, 3001, 37)):
    xs = np.linspace(0, 1, 201)
    for xv in xs:
        val = abs(float(gap.subs({n: nv, x: xv})))
        bound = 12.0 / nv
        if val > bound + 1e-12:
            print(f"    BOUND VIOLATED at n={nv} x={xv}: gap={val} > 12/n={bound}")
        ratio = val / bound if bound > 0 else 0
        worst_ratio = max(worst_ratio, ratio)
print(f"  max observed |gap|/(12/n) ratio = {worst_ratio:.4f} (<=1 means bound holds)")

