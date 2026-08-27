"""
REFEREE script 03 -- THE MOST IMPORTANT CHECK. Independent re-derivation
and verification of the target document's flagship finding (its section 4):

    C0_Bernstein(gamma,a)^2 := (2+a) * sigma^2(gamma) * (lambda_hat(gamma) + 1/2)

is claimed to be strictly decreasing and BOUNDED on the entire open interval
(0,1) for every fixed a>0, with

    sup_{gamma in (0,1)} C0_Bernstein(gamma,a)^2 = lim_{gamma->0+} = 28a + 56.

Definitions used (cited from the predecessor's own ATTEMPT.md, read in full
by the referee -- these are exactly the predecessor's own definitions, not
altered):
    sigma^2(gamma) := gamma*(1-gamma)                       [Bernoulli variance]
    beta(gamma)    := gamma*(2-gamma)/2                     [wave-17 truncation const.]
    lambda_hat(gamma) := 16*(7/4 - gamma) / beta(gamma)     [growth rate of the
                          predecessor's own EXPLICIT crude Ghat(n,gamma) bound
                          -- NOT the tighter idealized asymptotic lambda(gamma)
                          from Estagio 36. This distinction is itself checked
                          below (task item: "verify this distinction is real").]

Also independently re-derived for contrast:
    lambda(gamma) := 4*(3-2*gamma) / (gamma*(2-gamma))      [Estagio 36's own
                          "tight" asymptotic quantity -- proved unbounded on
                          (0,1) by the predecessor]
    kappa_0(gamma) := 8 / (gamma*(2-gamma))                  [wave-17 truncation
                          constant, K^2 = kappa_0 * n * ln n]

All symbolic work done via sympy, with OWN variable names, built entirely
from the mathematical prose of the required-reading documents -- no .py file
of this front or its lineage was opened.

Checks:
  1. sigma^2(gamma)*lambda_hat(gamma) -> 28 as gamma->0+  (the "why this is
     not a coincidence" mechanism claim, task item 4).
  2. C0_Bernstein(gamma,a)^2 is exact-algebra proved strictly DECREASING on
     (0,1) for representative a>0, via sign analysis of the derivative's
     numerator (a polynomial in gamma), checked for real roots in (0,1).
  3. lim_{gamma->0+} C0_Bernstein(gamma,a)^2 = 28a+56 (symbolic limit).
  4. lim_{gamma->1-} C0_Bernstein(gamma,a)^2 = 0 (symbolic limit).
  5. Cross-check numerically (independent dense scan, not relying on the
     symbolic derivative) that the function is monotone decreasing and its
     sup over a fine grid matches 28a+56 to high precision, for several a.
  6. Contrast: C0_Hoeffding(gamma)^2 := 1/4 + lambda_hat(gamma)/2 (the
     Hoeffding-route quantity, built with lambda_hat as the target document
     specifies -- since Hoeffding's construction is the SAME assembly but
     with the tail factor 2n^{-2C^2} instead of Bernstein's, i.e. no sigma^2
     weighting) is shown unbounded as gamma->0+, matching Estagio 36 /
     predecessor's finding for the analogous quantity built from lambda_hat.
  7. Sanity: at a=0.05, sup C0_Bernstein^2 = 28*0.05+56 = 57.4 (claimed);
     verified against dense numeric scan.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

g = sp.symbols('gamma', positive=True)
a = sp.symbols('a', positive=True)

sigma2 = g * (1 - g)
beta = g * (2 - g) / 2
lambda_hat = 16 * (sp.Rational(7, 4) - g) / beta          # predecessor's Ghat growth rate
lambda_tight = 4 * (3 - 2 * g) / (g * (2 - g))             # Estagio 36's own lambda(gamma)
kappa0 = 8 / (g * (2 - g))

print("=== Setup: definitions re-derived from prose, sanity-printed ===")
print("sigma^2(gamma) =", sp.simplify(sigma2))
print("beta(gamma)    =", sp.simplify(beta))
print("lambda_hat(gamma) simplified =", sp.simplify(lambda_hat))
print("lambda_tight(gamma) simplified =", sp.simplify(lambda_tight))
print("kappa0(gamma) =", sp.simplify(kappa0))
print()

# sanity: lambda_hat should equal 8*(7-4*gamma)/(gamma*(2-gamma)) per the
# target document's own alternate form; confirm symbolically.
alt_form = 8 * (7 - 4 * g) / (g * (2 - g))
diff_alt = sp.simplify(lambda_hat - alt_form)
print(f"Check lambda_hat(gamma) == 8*(7-4*gamma)/(gamma*(2-gamma))? diff = {diff_alt}")
assert diff_alt == 0, "MISMATCH in lambda_hat alternate form"
print()

# ---------------------------------------------------------------------
# Check 1: sigma^2 * lambda_hat -> 28 as gamma -> 0+ (mechanism claim)
# ---------------------------------------------------------------------
print("=== Check 1: sigma^2(gamma)*lambda_hat(gamma) -> ? as gamma->0+ ===")
product = sp.simplify(sigma2 * lambda_hat)
print("sigma^2(gamma)*lambda_hat(gamma) simplified =", product)
limit_product_0 = sp.limit(product, g, 0, dir='+')
print(f"lim_{{gamma->0+}} sigma^2*lambda_hat = {limit_product_0}")
assert limit_product_0 == 28, f"MECHANISM CLAIM FAILS: got {limit_product_0}, expected 28"
print("CONFIRMED: sigma^2(gamma)*lambda_hat(gamma) -> 28 as gamma->0+.")
print()

# For contrast, check sigma^2 * lambda_tight (should ALSO be finite, since
# lambda_tight ~ 4/gamma too -- let's see what it goes to, as an extra
# independent sanity probe, not claimed by the document but worth checking.
product_tight = sp.simplify(sigma2 * lambda_tight)
limit_tight_0 = sp.limit(product_tight, g, 0, dir='+')
print(f"[extra probe, not itself a document claim] sigma^2*lambda_tight -> {limit_tight_0} as gamma->0+")
print()

# ---------------------------------------------------------------------
# Check 2-5: C0_Bernstein(gamma,a)^2 monotonicity and limits
# ---------------------------------------------------------------------
print("=== Checks 2-4: C0_Bernstein(gamma,a)^2 -- strict monotone decrease, limits ===")
C0_bernstein_sq = (2 + a) * sigma2 * (lambda_hat + sp.Rational(1, 2))
C0_bernstein_sq = sp.simplify(C0_bernstein_sq)
print("C0_Bernstein(gamma,a)^2 =", C0_bernstein_sq)
print()

# derivative w.r.t. gamma, for a FIXED symbolic a (independent re-derivation,
# not copying the target's own derivative)
dC0_dg = sp.diff(C0_bernstein_sq, g)
dC0_dg_simplified = sp.simplify(dC0_dg)
print("d/dgamma C0_Bernstein^2 (simplified) =", dC0_dg_simplified)

# isolate numerator over common denominator, get a polynomial in gamma (a stays symbolic)
num, den = sp.fraction(sp.together(dC0_dg_simplified))
num_poly = sp.expand(num)
den_poly = sp.expand(den)
print()
print("Numerator of the derivative (as polynomial in gamma, a symbolic):")
print(" ", num_poly)
print("Denominator (as polynomial in gamma):")
print(" ", den_poly)

# Denominator sign on (0,1): should be manifestly positive (a square /
# positive quantity) -- check by substitution at several points and by
# sympy's own positivity check where possible.
print()
print("Denominator positivity check on (0,1) [sample points]:")
den_positive_everywhere = True
for gv in [sp.Rational(1, 100), sp.Rational(1, 10), sp.Rational(1, 2),
           sp.Rational(9, 10), sp.Rational(99, 100)]:
    val = den_poly.subs(g, gv)
    print(f"  gamma={float(gv):.4f}: den = {val}  (positive: {val > 0})")
    if val <= 0:
        den_positive_everywhere = False
print(f"Denominator positive at all sample points: {den_positive_everywhere}")
print()

# Now determine roots of the numerator in gamma, for FIXED representative
# values of a (since the numerator is a polynomial jointly in gamma and a,
# checking "no root in (0,1) for EVERY a>0" requires treating a as a free
# positive parameter -- do this two ways: (i) symbolic in a via sympy
# real_roots/solve treating a as parameter and requiring no solution for any
# a>0 by inspecting the numerator's structure; (ii) concretely for many
# representative a values.)
print("=== Numerator root analysis (own independent method) ===")
gamma_poly = sp.Poly(num_poly, g)
print("Numerator as a polynomial in gamma (coefficients may involve a):")
for i, c in enumerate(reversed(gamma_poly.all_coeffs())):
    print(f"  gamma^{i} coeff: {sp.simplify(c)}")
print()

representative_as = [sp.Rational(1, 100), sp.Rational(1, 20), sp.Rational(1, 10),
                     sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1),
                     sp.Integer(2), sp.Integer(5), sp.Integer(10), sp.Integer(100)]

all_pass = True
for a_val in representative_as:
    num_at_a = sp.expand(num_poly.subs(a, a_val))
    poly_a = sp.Poly(num_at_a, g)
    roots = sp.real_roots(poly_a)
    roots_in_01 = [r for r in roots if sp.N(r) > 0 and sp.N(r) < 1]
    # sign at midpoint
    mid_val = num_at_a.subs(g, sp.Rational(1, 2))
    sign_ok = mid_val < 0
    status = "OK (no root in (0,1), negative at midpoint)" if (not roots_in_01 and sign_ok) else "FAIL"
    if roots_in_01 or not sign_ok:
        all_pass = False
    print(f"  a={float(a_val):8.4f}: real roots={[sp.N(r,6) for r in roots]}, "
          f"roots in (0,1)={roots_in_01}, numerator(1/2)={float(mid_val):.4f} -> {status}")

print()
print(f"Strict monotone-decrease check across representative a values: {'PASS' if all_pass else 'FAIL'}")
print()

# Also: is the numerator's sign structure such that it's negative for EVERY
# a>0, not just the tested values? Do this by treating the numerator as a
# polynomial in gamma with coefficients LINEAR in a (since the construction
# only ever multiplies lambda_hat/sigma2 pieces by (2+a) linearly), and
# checking sign for a->0+ and a->infinity as the two extremes, plus at a
# generic symbolic point -- the family of coefficients is affine in a, so if
# it's negative at a=0+ and stays negative in the same functional form as a
# grows (since (2+a) is a positive overall multiplicative prefactor that
# does not change sign structure across gamma), monotonicity should persist.
print("=== Extra check: is (2+a) merely an overall positive prefactor? ===")
# C0_bernstein_sq = (2+a) * sigma2 * (lambda_hat + 1/2). The (2+a) factor is
# gamma-independent, so d/dgamma[(2+a)*f(gamma)] = (2+a)*f'(gamma), meaning
# the SIGN of the derivative in gamma is entirely determined by the sign of
# f'(gamma) = d/dgamma[sigma2*(lambda_hat+1/2)], independent of a (since
# 2+a>0 for all a>0)! This is a strong structural simplification worth
# confirming directly.
f_gamma = sp.simplify(sigma2 * (lambda_hat + sp.Rational(1, 2)))
df_dgamma = sp.simplify(sp.diff(f_gamma, g))
print("f(gamma) := sigma^2*(lambda_hat+1/2) =", f_gamma)
print("f'(gamma) =", df_dgamma)
num_f, den_f = sp.fraction(sp.together(df_dgamma))
num_f_poly = sp.Poly(sp.expand(num_f), g)
roots_f = sp.real_roots(num_f_poly)
roots_f_in_01 = [r for r in roots_f if sp.N(r) > 0 and sp.N(r) < 1]
mid_f = sp.expand(num_f).subs(g, sp.Rational(1, 2))
print(f"f'(gamma) numerator real roots: {[sp.N(r,6) for r in roots_f]}")
print(f"roots in (0,1): {roots_f_in_01}")
print(f"f'(gamma) numerator at gamma=1/2: {mid_f} (negative => f decreasing there)")
structural_confirmed = (not roots_f_in_01) and (mid_f < 0)
print(f"STRUCTURAL CONFIRMATION -- since C0_Bernstein^2=(2+a)*f(gamma) and (2+a)>0 for")
print(f"  every a>0, monotonicity of C0_Bernstein^2 in gamma is EQUIVALENT, for every")
print(f"  a>0 simultaneously, to monotonicity of f(gamma) alone (a-independent question).")
print(f"  f(gamma) is exact-algebra strictly decreasing on (0,1): {'PASS' if structural_confirmed else 'FAIL'}")
print(f"  ==> this proves the 'for every a>0' universal claim in ONE shot, not just at")
print(f"      10 sample a-values -- a strictly stronger check than the target's own a-by-a table.")
print()

# limits
print("=== Checks 3-4: limits as gamma->0+ and gamma->1- ===")
lim0 = sp.limit(C0_bernstein_sq, g, 0, dir='+')
lim1 = sp.limit(C0_bernstein_sq, g, 1, dir='-')
print(f"lim_{{gamma->0+}} C0_Bernstein(gamma,a)^2 = {sp.simplify(lim0)}")
print(f"lim_{{gamma->1-}} C0_Bernstein(gamma,a)^2 = {sp.simplify(lim1)}")
claimed_lim0 = 28 * a + 56
diff0 = sp.simplify(lim0 - claimed_lim0)
print(f"Difference from claimed 28a+56: {diff0}")
assert diff0 == 0, f"LIMIT AT 0 MISMATCH: got {lim0}, claimed {claimed_lim0}"
assert lim1 == 0, f"LIMIT AT 1 MISMATCH: got {lim1}, claimed 0"
print("CONFIRMED: lim_{gamma->0+} = 28a+56 EXACTLY; lim_{gamma->1-} = 0 EXACTLY.")
print()

# ---------------------------------------------------------------------
# Check 5: independent dense numeric scan (not relying on symbolic work)
# ---------------------------------------------------------------------
print("=== Check 5: independent dense numeric scan (mpmath, not sympy) ===")


def C0_bernstein_numeric(gamma, a_val):
    gamma = mp.mpf(gamma)
    a_val = mp.mpf(a_val)
    sigma2_n = gamma * (1 - gamma)
    beta_n = gamma * (2 - gamma) / 2
    lam_hat_n = 16 * (mp.mpf('1.75') - gamma) / beta_n
    return (2 + a_val) * sigma2_n * (lam_hat_n + mp.mpf('0.5'))


test_as = [mp.mpf('0.05'), mp.mpf('0.5'), mp.mpf(1), mp.mpf(5)]
n_grid = 50000
overall_ok = True
for a_val in test_as:
    prev = None
    monotone_ok = True
    max_val = mp.mpf(0)
    max_at = None
    for i in range(1, n_grid):
        gamma_i = mp.mpf(i) / n_grid  # (0,1)
        val = C0_bernstein_numeric(gamma_i, a_val)
        if val > max_val:
            max_val = val
            max_at = gamma_i
        if prev is not None and val > prev:
            monotone_ok = False
        prev = val
    claimed_sup = 28 * a_val + 56
    rel_err = abs(max_val - claimed_sup) / claimed_sup
    print(f"  a={float(a_val):.4f}: numeric max over {n_grid-1} pts = {float(max_val):.6f} "
          f"at gamma={float(max_at):.6f}, claimed sup(=lim gamma->0)={float(claimed_sup):.6f}, "
          f"rel.err={float(rel_err):.3e}, monotone-decreasing over scan: {monotone_ok}")
    if rel_err > 1e-3 or not monotone_ok:
        overall_ok = False
print(f"Dense numeric scan overall: {'PASS' if overall_ok else 'FAIL'}")
print()

# ---------------------------------------------------------------------
# Check 6: contrast with Hoeffding-route quantity built from lambda_hat
# ---------------------------------------------------------------------
print("=== Check 6: contrast -- C0_Hoeffding(gamma)^2 := 1/4 + lambda_hat(gamma)/2 ===")
C0_hoeffding_sq = sp.Rational(1, 4) + lambda_hat / 2
lim_hoeff_0 = sp.limit(C0_hoeffding_sq, g, 0, dir='+')
print(f"lim_{{gamma->0+}} C0_Hoeffding(gamma)^2 = {lim_hoeff_0}")
assert lim_hoeff_0 == sp.oo, "Hoeffding quantity should diverge, but didn't!"
print("CONFIRMED: C0_Hoeffding(gamma)^2 diverges (+infinity) as gamma->0+, consistent")
print("  with Estagio 36 / predecessor's finding that the analogous Hoeffding-route")
print("  quantity is UNBOUNDED on (0,1). Bernstein's variance-weighting is what")
print("  converts this divergence into the finite limit 28a+56 confirmed above.")
print()

# also check lambda_tight itself (Estagio 36's literal quantity) diverges,
# as an independent re-confirmation of the predecessor's own claim (not
# taking it on faith)
lim_tight_0 = sp.limit(lambda_tight, g, 0, dir='+')
print(f"[independent re-confirmation, own derivation] lim_{{gamma->0+}} lambda(gamma) (Estagio 36's "
      f"own tight quantity) = {lim_tight_0}")
assert lim_tight_0 == sp.oo

print()
print("=== Check 7: a=0.05 sup value spot check ===")
claimed_sup_005 = 28 * sp.Rational(5, 100) + 56
print(f"28*0.05+56 = {float(claimed_sup_005)}")
assert abs(float(claimed_sup_005) - 57.4) < 1e-9

print()
print("=== FINAL SUMMARY ===")
print("1. sigma^2*lambda_hat -> 28 as gamma->0+ : CONFIRMED (exact symbolic limit)")
print("2. C0_Bernstein^2 strictly decreasing on (0,1) for EVERY a>0 simultaneously:")
print(f"   CONFIRMED via structural factorization (2+a)*f(gamma), f(gamma) proved")
print(f"   strictly decreasing by exact-algebra root analysis: {'PASS' if structural_confirmed else 'FAIL'}")
print(f"   (also independently spot-checked at 10 representative a values: {'PASS' if all_pass else 'FAIL'})")
print("3. lim_{gamma->0+} C0_Bernstein^2 = 28a+56 : CONFIRMED (exact symbolic limit)")
print("4. lim_{gamma->1-} C0_Bernstein^2 = 0 : CONFIRMED (exact symbolic limit)")
print(f"5. Dense independent numeric scan (50000 pts, 4 values of a): {'PASS' if overall_ok else 'FAIL'}")
print("6. Hoeffding-route contrast (built from lambda_hat) diverges as gamma->0+: CONFIRMED")
print("7. sup at a=0.05 is 57.4: CONFIRMED")
