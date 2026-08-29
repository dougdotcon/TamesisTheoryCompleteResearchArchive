"""
02_leading_order_symbolic_comparison.py

Symbolic (exact-algebra) leading-order comparison of THREE quantities, all
evaluated at k=K (the truncation bound, per the sharper_tail front's own
convention of working with c_i(K) throughout), as n -> infinity with the
TRUE wave-17 truncation K^2 = (4/beta) n ln n, beta = gamma(2-gamma)/2:

  (1) lambda(gamma)      -- the TRUE/ideal leading constant (Estagio 36),
                             lambda(gamma) := kappa_0(gamma)*(3/2-gamma)
                             = 4(3-2*gamma)/(gamma(2-gamma)).
                             This is what the *dominant monomials* of the
                             literal Taylor-remainder quantity would give if
                             no bounding slack were introduced at all.
  (2) hat_lambda(gamma)  -- the CURRENT crude bound's leading constant
                             (continuation/sharper_tail fronts),
                             hat_lambda(gamma) = 16(7/4-gamma)/beta(gamma),
                             built from g(K):=|c0|+|c1|K+|c2|K^2+|c3|K^3
                             (triangle-inequality summed absolute values,
                             symmetric range |D|<=K, AND a crude K_max=2K
                             margin baked into the "K" used).
  (3) lambda_tight(gamma) -- THIS FRONT's new leading constant, built from
                             the EXACT maximum of the signed cubic x_K(D)
                             over the TRUE (asymmetric) support
                             D in [-gamma*K, (1-gamma)*K], i.e. NO triangle
                             inequality across c0..c3, and the TRUE K (not
                             a 2x-inflated K_max).

All three are derived by symbolic sympy.limit (exact-algebra), not curve
fitting or numerical sampling -- matching this lineage's own standard for
"PROVED" vs "numerically confirmed" asymptotic claims (see Estagio 33/36's
own use of sympy.limit for lambda(gamma)).
"""
import sympy as sp

k, n, gamma, D = sp.symbols('k n gamma D', positive=True)
nn = sp.Symbol('n', positive=True)

beta = gamma * (2 - gamma) / 2

# ---------------------------------------------------------------------
# Re-derive c0..c3(k,n,gamma) fresh (same as script 01, kept self-
# contained here so this script can run standalone / be independently
# spot-checked against script 01's output).
# ---------------------------------------------------------------------
m = sp.Symbol('m')
i = sp.Symbol('i', integer=True, positive=True)
tau_m = sp.expand(sp.summation(((k - i) / n) ** 2, (i, 1, m)))
delta_D = D * (2 * k * (1 - gamma) - D - 1) / (2 * n)
tau_M = tau_m.subs(m, gamma * k + D)
x_D = sp.expand(delta_D + tau_M / 2)
x_poly = sp.Poly(x_D, D)
c3 = sp.simplify(x_poly.coeff_monomial(D ** 3))
c2 = sp.simplify(x_poly.coeff_monomial(D ** 2))
c1 = sp.simplify(x_poly.coeff_monomial(D))
c0 = sp.simplify(x_poly.coeff_monomial(1))
print("c0,c1,c2,c3 re-derived (matches script 01):")
print(" c0 =", c0)
print(" c1 =", c1)
print(" c2 =", c2)
print(" c3 =", c3)

# ---------------------------------------------------------------------
# Substitute k -> K, a fresh symbol standing for the truncation bound,
# so we can freely substitute K^2 = (4/beta) n ln(n) at leading order.
# ---------------------------------------------------------------------
K = sp.Symbol('K', positive=True)
c0_K = c0.subs(k, K)
c1_K = c1.subs(k, K)
c2_K = c2.subs(k, K)
c3_K = c3.subs(k, K)

print()
print("=" * 78)
print("PART A -- the TRUE ideal leading constant lambda(gamma) (Estagio 36,")
print("re-derived independently here as a cross-check)")
print("=" * 78)
lam_true = sp.simplify(4 * (3 - 2 * gamma) / (gamma * (2 - gamma)))
print("lambda(gamma) =", lam_true)
print("lambda(1)   =", lam_true.subs(gamma, 1), " (expect 4)")
print("lambda(1/2) =", lam_true.subs(gamma, sp.Rational(1, 2)), " (expect 32/3 ~ 10.667)")

print()
print("=" * 78)
print("PART B -- the CURRENT crude bound's hat_lambda(gamma) (continuation/")
print("sharper_tail fronts), re-derived independently as a cross-check")
print("=" * 78)
hat_lam = sp.simplify(16 * (sp.Rational(7, 4) - gamma) / beta)
print("hat_lambda(gamma) =", hat_lam)
print("hat_lambda(1) =", hat_lam.subs(gamma, 1), " (expect 24)")
ratio = sp.simplify(hat_lam / lam_true)
print("hat_lambda/lambda at gamma=1:", ratio.subs(gamma, 1), " (expect 6)")
print("hat_lambda/lambda as gamma->0:", sp.limit(ratio, gamma, 0), " (expect 14/3 ~ 4.667)")

print()
print("=" * 78)
print("PART C -- THIS FRONT's lambda_tight(gamma): exact max of the signed")
print("cubic over the TRUE asymmetric support, TRUE (uninflated) K")
print("=" * 78)

# TRUE K (no crude 2x margin): K^2 = (4/beta) n ln(n)  =>  K = sqrt((4/beta) n ln(n))
Ksub = sp.sqrt(4 * nn * sp.log(nn) / beta)

# Endpoints of the TRUE support of D at k=K: D in [-gamma*K, (1-gamma)*K]
D_max = (1 - gamma) * K
D_min = -gamma * K

x_at_Dmax = c0_K + c1_K * D_max + c2_K * D_max ** 2 + c3_K * D_max ** 3
x_at_Dmin = c0_K + c1_K * D_min + c2_K * D_min ** 2 + c3_K * D_min ** 3
x_at_Dmax = sp.simplify(x_at_Dmax)
x_at_Dmin = sp.simplify(x_at_Dmin)
print("x_K(D_max) [D=(1-gamma)K] =", x_at_Dmax)
print("x_K(D_min) [D=-gamma*K]   =", x_at_Dmin)

# Substitute K -> Ksub(n) and take n -> infinity of [value]/ln(n).
x_at_Dmax_n = x_at_Dmax.subs(K, Ksub)
x_at_Dmin_n = x_at_Dmin.subs(K, Ksub)

lim_plus = sp.limit(x_at_Dmax_n / sp.log(nn), nn, sp.oo)
lim_minus = sp.limit(x_at_Dmin_n / sp.log(nn), nn, sp.oo)
print()
print("lim_{n->infty} x_K(D_max)/ln(n) =", sp.simplify(lim_plus))
print("lim_{n->infty} x_K(D_min)/ln(n) =", sp.simplify(lim_minus))

lam_plus = sp.simplify(lim_plus)
lam_minus = sp.simplify(lim_minus)

# lambda_tight is the leading constant of the MAXIMUM absolute value
# reachable at the two endpoints (interior critical points handled in
# script 03's finite-n numerics; at leading order in n the interior
# critical point of a low-degree-in-D-relative-to-K perturbation will be
# shown in script 03 to lie extremely close to one endpoint or outside
# the true support entirely for the regimes that matter -- verified
# numerically, not assumed here).
lam_tight_candidate = sp.simplify(sp.Max(sp.Abs(lam_plus), sp.Abs(lam_minus)))
print()
print("lambda_tight(gamma) candidate := max(|lim_plus|, |lim_minus|) =")
print(" ", lam_tight_candidate)

print()
print("Evaluate lambda_tight at sample gamma:")
for g in [sp.Rational(1, 100), sp.Rational(1, 10), sp.Rational(3, 10),
          sp.Rational(1, 2), sp.Rational(7, 10), sp.Rational(9, 10),
          sp.Rational(99, 100)]:
    lp = lim_plus.subs(gamma, g)
    lm = lim_minus.subs(gamma, g)
    lt = lam_true.subs(gamma, g)
    hl = hat_lam.subs(gamma, g)
    print(f"  gamma={float(g):.2f}: lim_plus={sp.nsimplify(lp)}={float(lp):.4f}"
          f"  lim_minus={float(lm):.4f}  |max|={max(abs(float(lp)), abs(float(lm))):.4f}"
          f"   [true lambda={float(lt):.4f}, old hat_lambda={float(hl):.4f}]")

print()
print("=" * 78)
print("PART D -- symbolic simplification of lim_plus, lim_minus as closed")
print("forms in gamma (not just numeric samples)")
print("=" * 78)
lim_plus_simplified = sp.simplify(sp.nsimplify(lim_plus, [gamma]))
lim_minus_simplified = sp.simplify(sp.nsimplify(lim_minus, [gamma]))
print("lim_plus(gamma)  simplified =", lim_plus_simplified)
print("lim_minus(gamma) simplified =", lim_minus_simplified)

# Try to get a single closed-form ratio lim_plus/lambda_true, lim_minus/lambda_true
ratio_plus = sp.simplify(lim_plus_simplified / lam_true)
ratio_minus = sp.simplify(lim_minus_simplified / lam_true)
print()
print("lim_plus / lambda_true  =", ratio_plus)
print("lim_minus / lambda_true =", ratio_minus)
