"""
Symbolic derivation of the SECOND MOMENT that Conjecture 2 predicts for
M(c), directly from the conjectured law M(c) =d min(1, sqrt(E/c)),
E~Exp(1). This is a NEW closed form (not previously stated anywhere in
THEOREM.md, which only records the mean phi_infty(c)) that gives a
concrete numerical target for the "moment method" route attempted in
ATTEMPT.md Section 3. Pure elementary calculus -- fully symbolic, no
floating point.

Also cross-checks against the SERIES form (mixing the Conjecture-1
second moment E[M_K^2] over K~Poisson(c)), confirming the two routes
to "what Conjecture 2 predicts for E[M(c)^2]" agree -- i.e. that the
K-mixture definition and the min(1,sqrt(E/c)) representation are the
SAME conjectured object, exactly as THEOREM.md Section 8 states.
"""
import sympy as sp

c, x, e, K = sp.symbols('c x e K', positive=True)

print("=" * 70)
print("Route A: E[M(c)^2] directly from M(c) = min(1, sqrt(E/c)), E~Exp(1)")
print("=" * 70)

# M(c)^2 = min(1, E/c).  E[min(1, E/c)] = int_0^c (e/c) exp(-e) de + int_c^oo exp(-e) de
term1 = sp.integrate((e / c) * sp.exp(-e), (e, 0, c))
term2 = sp.integrate(sp.exp(-e), (e, c, sp.oo))
second_moment_A = sp.simplify(term1 + term2)
print("term1 = int_0^c (e/c)e^-e de =", sp.simplify(term1))
print("term2 = int_c^oo e^-e de     =", sp.simplify(term2))
print("E[M(c)^2] (route A)          =", second_moment_A)

target = (1 - sp.exp(-c)) / c
diff_A = sp.simplify(second_moment_A - target)
print("Candidate closed form (1-e^-c)/c matches route A exactly:", diff_A == 0, " (diff =", diff_A, ")")

print()
print("=" * 70)
print("Route B: E[M(c)^2] via the K-mixture definition of Conjecture 2")
print("  (M(c) := M_K, K~Poisson(c) independent; use Conjecture 1's")
print("   f_{M_K}(x) = 2Kx(1-x^2)^{K-1} -- CONJECTURED for K>=2, PROVED")
print("   K=1,2,3 -- to get E[M_K^2] for each K, then Poisson-mix.)")
print("=" * 70)

Kint = sp.symbols('Kint', positive=True, integer=True)
fMK = 2 * Kint * x * (1 - x**2)**(Kint - 1)
EM2_K = sp.integrate(x**2 * fMK, (x, 0, 1))
EM2_K = sp.simplify(EM2_K)
print("E[M_K^2] (from Conjecture 1's density, symbolic in K) =", EM2_K)

# Sanity: K=0 special-cased (M_0 = 1 a.s., since no reroutes -> whole space cyclic)
print("K=0 special case: M_0 = 1 a.s. => E[M_0^2] = 1 (not covered by the K>=1 formula above)")

# Poisson-mix E[M_K^2] over K ~ Poisson(c), split K=0 term explicitly
n = sp.symbols('n', positive=True, integer=True)
# For K>=1: E[M_K^2] = (K)/(K+2) -- let's see what sympy gives after simplify with explicit small K,
# then attempt the general term and sum from K=1 to oo, plus the K=0 term e^{-c}*1.
EM2_K_general = sp.simplify(EM2_K)
print("Simplified E[M_K^2] as function of K:", EM2_K_general)

pmf = sp.exp(-c) * c**Kint / sp.factorial(Kint)
mix_term_general = pmf * EM2_K_general  # valid for K>=1
series_sum = sp.exp(-c) * 1 + sp.Sum(mix_term_general, (Kint, 1, sp.oo))  # K=0 term handled separately
series_sum_closed = sp.simplify(series_sum.doit())
print("Poisson-mixture sum (route B), closed form:", series_sum_closed)

diff_B = sp.simplify(series_sum_closed - target)
print("Matches (1-e^-c)/c exactly:", diff_B == 0, " (diff =", sp.nsimplify(diff_B), ")")

print()
print("=" * 70)
print("Numeric cross-check at a few c values (both routes vs target, floats)")
print("=" * 70)
for cval in [sp.Rational(1, 2), 1, 2, 5, 10]:
    a = float(second_moment_A.subs(c, cval))
    b = float(series_sum_closed.subs(c, cval))
    t = float(target.subs(c, cval))
    print(f"c={float(cval):6.2f}  routeA={a:.10f}  routeB={b:.10f}  target=(1-e^-c)/c={t:.10f}")
