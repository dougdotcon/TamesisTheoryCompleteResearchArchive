"""
Independent referee re-derivation B: mesoscale scaling of A, g'''(t*),
g''''(t*), and the resulting closed form for Delta(n,m,gamma) at
m=lambda*sqrt(n), n->infinity.

Uses sympy.limit of A_expr*eps**p (leading-power extraction), NOT
sympy.series (avoids the front's own disclosed timeout workaround, and
is a genuinely different symbolic route).
"""
import sympy as sp

n, m, gam, t, lam, eps = sp.symbols('n m gamma t lambda epsilon', positive=True)

g = m*sp.log(t) + m*sp.log(1-t) + (n-m)*sp.log(1-gam*t)
gpp = sp.diff(g, t, 2)
gppp = sp.diff(g, t, 3)
gpppp = sp.diff(g, t, 4)

t_star = (2*m + gam*n - sp.sqrt(gam**2*n**2 + 4*(1-gam)*m**2)) / (2*gam*(m+n))

# sanity: t_star solves g'(t)=0
gp = sp.diff(g, t)
check = sp.simplify(gp.subs(t, t_star))
print("g'(t*) simplified (expect 0):", check)

A_expr = sp.simplify(-gpp.subs(t, t_star))
g3_expr = sp.simplify(gppp.subs(t, t_star))
g4_expr = sp.simplify(gpppp.subs(t, t_star))

print("\nA(t*) =", A_expr)
print("g3(t*) =", g3_expr)
print("g4(t*) =", g4_expr)

# substitute m = lambda*sqrt(n), n = 1/eps**2  (eps=1/sqrt(n) -> 0)
subs_meso = {m: lam*sp.sqrt(n)}

A_m = sp.simplify(A_expr.subs(subs_meso))
g3_m = sp.simplify(g3_expr.subs(subs_meso))
g4_m = sp.simplify(g4_expr.subs(subs_meso))

# now substitute n = 1/eps**2 and find leading power of eps as eps->0,
# via sympy.limit of (expr * eps**p) for candidate p, NOT .series
def leading_power_and_coeff(expr_in_n, nsym, target_var_name, p_search_range):
    """Find integer/half-integer p and coeff c such that
    lim_{n->oo} expr/n**p = c (nonzero, finite)."""
    for p in p_search_range:
        val = sp.limit(expr_in_n / nsym**p, nsym, sp.oo)
        if val.is_finite and val != 0:
            return p, sp.nsimplify(val)
    return None, None

from sympy import Rational
search_powers = [Rational(k,2) for k in range(-2, 12)]

pA, cA = leading_power_and_coeff(A_m, n, 'n', search_powers)
print(f"\nA ~ {cA} * n^{pA}   (front claims n^{{3/2}} * gamma^2/lambda)")

pG3, cG3 = leading_power_and_coeff(g3_m, n, 'n', search_powers)
print(f"g3(t*) ~ {cG3} * n^{pG3}   (front claims n^2 * 2 gamma^3/lambda^2)")

pG4, cG4 = leading_power_and_coeff(g4_m, n, 'n', search_powers)
print(f"g4(t*) ~ {cG4} * n^{pG4}   (front claims -n^{{5/2}} * 6 gamma^4/lambda^3)")

# Now build Delta's two terms symbolically from these leading pieces and
# confirm the combined power/coefficient via limit (again, no .series).
# Delta = g4/(8A^2) + 5*g3^2/(24*A^3)
term1 = g4_m/(8*A_m**2)
term2 = 5*g3_m**2/(24*A_m**3)
Delta_m = sp.simplify(term1 + term2)

pD, cD = leading_power_and_coeff(Delta_m, n, 'n', [Rational(k,2) for k in range(-6,2)])
print(f"\nDelta(n,m=lam*sqrt(n),gamma) ~ {cD} * n^{pD}")
print("front claims Delta ~ 1/(12*lambda) * n^(-1/2), gamma-independent")

cD_simpl = sp.simplify(cD)
print("coefficient simplified:", cD_simpl)
print("does it depend on gamma?", cD_simpl.has(gam))
print("compare to 1/(12*lambda):", sp.simplify(cD_simpl - 1/(12*lam)), " (expect 0 if match)")

# also verify the two individual terms separately, matching front's claim
pT1, cT1 = leading_power_and_coeff(term1, n, 'n', [Rational(k,2) for k in range(-6,2)])
pT2, cT2 = leading_power_and_coeff(term2, n, 'n', [Rational(k,2) for k in range(-6,2)])
print(f"\nterm1=g4/(8A^2) ~ {cT1} n^{pT1}")
print(f"term2=5g3^2/(24A^3) ~ {cT2} n^{pT2}")
print("sum of coefficients:", sp.simplify(cT1+cT2), " vs 1/(12*lambda):", sp.simplify(1/(12*lam)))
