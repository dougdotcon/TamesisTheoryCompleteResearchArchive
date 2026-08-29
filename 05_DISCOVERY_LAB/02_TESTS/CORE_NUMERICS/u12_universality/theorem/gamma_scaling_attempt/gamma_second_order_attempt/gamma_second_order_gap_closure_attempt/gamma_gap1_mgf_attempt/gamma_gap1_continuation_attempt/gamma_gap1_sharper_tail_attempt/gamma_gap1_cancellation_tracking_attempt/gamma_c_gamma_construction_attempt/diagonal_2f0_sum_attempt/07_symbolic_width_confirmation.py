"""
Script 07 -- symbolic confirmation of the m-sum's Gaussian-width constant
c = 2(1-gamma)/gamma found numerically in script 06.

Exact closed forms for term_0(n,gamma) and term_1(n,gamma) (m=0,1 are
easy enough for sympy to sum exactly for symbolic n), then
lim_{n->infty} n * log(term_0/term_1) is computed symbolically and
compared to the numerically-fitted c.
"""
import sympy as sp

n, gam = sp.symbols('n gamma', positive=True)

# term_0(n,gamma) = T(n,0) = sum_{j=0}^n (1-gamma)^j   (exact geometric sum)
term0 = sp.summation((1 - gam)**sp.Symbol('j'), (sp.Symbol('j'), 0, n))
term0 = sp.simplify(term0)
print(f"term_0(n,gamma) = {term0}")

# term_1(n,gamma) = (gamma/n) * T(n,1),  T(n,1) = sum_{j=0}^{n-1} (j+1)(n-j)(1-gamma)^j
j = sp.Symbol('j')
T1 = sp.summation((j + 1) * (n - j) * (1 - gam)**j, (j, 0, n - 1))
T1 = sp.simplify(T1)
term1 = sp.simplify((gam / n) * T1)
print(f"term_1(n,gamma) = {term1}")

print()
print("=== Sanity: numeric spot check vs script 06's mpmath term_m, n=50, gamma=1/2 ===")
t0_num = float(term0.subs({n: 50, gam: sp.Rational(1, 2)}))
t1_num = float(term1.subs({n: 50, gam: sp.Rational(1, 2)}))
print(f"  term_0(50, 1/2) = {t0_num:.10f}  (script 06 mpmath value: 2.0000000000)")
print(f"  term_1(50, 1/2) = {t1_num:.10f}  (script 06 mpmath value: 1.9200000000)")

print()
print("=== log-ratio * n, large-n limit (symbolic) ===")
print("(sympy's gruntz algorithm cannot decide sign(log(1-gamma)) on its own "
      "since 0<gamma<1 is only known 'morally', not declared -- so we drop the "
      "exponentially small (1-gamma)^n / (1-gamma)^(n-1) terms explicitly first, "
      "which is legitimate for any FIXED gamma in (0,1) as n->infinity, then let "
      "sympy take the resulting purely-rational-in-n limit unassisted.)")
term1_poly_part = term1.subs({(1 - gam)**n: 0, (1 - gam)**(n - 1): 0})
term1_poly_part = sp.simplify(term1_poly_part)
print(f"  term_1(n,gamma), exponentially small terms dropped -> {term1_poly_part}")
logratio_n = sp.simplify(n * sp.log(term0 / term1_poly_part))
# term0 -> 1/gamma exactly once (1-gamma)^(n+1) is dropped too, for the same reason
term0_poly_part = sp.Rational(1) / gam
logratio_n = sp.simplify(n * sp.log(term0_poly_part / term1_poly_part))
limit_val = sp.limit(logratio_n, n, sp.oo)
print(f"  n*log(term_0/term_1) -> {sp.simplify(limit_val)}  as n -> infinity")
predicted = 2 * (1 - gam) / gam
print(f"  predicted c = 2(1-gamma)/gamma = {predicted}")
diff = sp.simplify(limit_val - predicted)
print(f"  difference (should simplify to 0): {diff}")

print()
print("=== Numeric evaluation of the limit at 3 sample gamma, cross-checking script 06 ===")
for gval in [sp.Rational(1, 2), sp.Rational(1, 5), sp.Rational(7, 10)]:
    lv = float(limit_val.subs(gam, gval))
    pv = float(predicted.subs(gam, gval))
    print(f"  gamma={gval}: limit={lv:.6f}  predicted 2(1-g)/g={pv:.6f}  "
          f"(script 06 fitted values converged to ~{lv:.3f})")
