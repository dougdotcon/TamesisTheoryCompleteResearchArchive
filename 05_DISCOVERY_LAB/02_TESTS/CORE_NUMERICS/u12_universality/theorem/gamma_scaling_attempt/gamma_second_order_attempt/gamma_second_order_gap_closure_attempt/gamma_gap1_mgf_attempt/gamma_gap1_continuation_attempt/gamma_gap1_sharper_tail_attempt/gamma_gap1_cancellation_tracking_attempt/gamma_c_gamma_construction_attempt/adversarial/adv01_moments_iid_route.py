"""
Independent re-derivation (from scratch, not reading the target's scripts)
of:
 (a) the two classical Binomial central-moment formulas mu_3, mu_4 cited
     in gamma_second_order_attempt/ATTEMPT.md Sec.5, via a DIFFERENT route
     than the target's cumulant-recursion route (direct MGF / raw-moment
     substitution instead of cumulant->moment recursion), to cross-check
     both the target's Part A/B (script 02) and the ancestor's citation.
 (b) x(D):=delta(D)+tau(M)/2's exact cubic coefficients c0..c3, via a
     THIRD independent route (direct polynomial substitution + sympy.expand,
     not Poly.coeff_monomial), cross-checked against target's script 02.
 (c) E[x(D)^4] via DIRECT raw-moment substitution (not via the cumulant
     recursion the target used), to catch any recursion-implementation bug
     that might not show up in a "cross-check against a classical formula"
     since mu_4 is checked but mu up to 12 (needed for E[x^4], degree 12
     in D) are not classically cited anywhere.
"""
import sympy as sp
from sympy import symbols, Rational, exp, log, series, expand, simplify, factorial, binomial as symbinom

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')

print("="*70)
print("Part (a): mu_3, mu_4 via DIRECT MGF/raw-moment route (not cumulants)")
print("="*70)

t = symbols('t')
# MGF of a single Bernoulli(g): M(t) = 1-g+g*e^t
# MGF of D = M - g*k = sum of k iid (Bernoulli(g)-g) terms
# central MGF of a single centered Bernoulli: E[e^{t(X-g)}] = e^{-tg}(1-g+g e^t)
single_centered_mgf = exp(-t*g)*(1-g+g*exp(t))
MAXORD = 8
ser = series(single_centered_mgf, t, 0, MAXORD+1).removeO()
ser = expand(ser)
poly = sp.Poly(ser, t)
# raw moments of the centered single term:
single_moments = {}
for j in range(0, MAXORD+1):
    c = poly.coeff_monomial(t**j) if j > 0 else poly.coeff_monomial(1)
    single_moments[j] = expand(factorial(j)*c)

print("Single centered-Bernoulli raw moments (E[(X-g)^j]):")
for j in range(5):
    print(f"  j={j}: {single_moments[j]}")

# D = sum of k iid such terms -> MGF of D = (single_centered_mgf)^k
# central moments of D via raw-moment extraction from D's MGF series
D_mgf = single_centered_mgf**k
# Can't directly series-expand with symbolic exponent k using sympy.series,
# so instead use: ln(MGF_D) = k * ln(single_centered_mgf), then exponentiate
# the series (this is effectively re-deriving the cumulant approach from a
# different starting point: MGF, not CGF-by-series-of-log). To make this a
# GENUINELY independent check (different implementation path), we instead
# verify mu_3, mu_4 by finite-k brute-force substitution for many small k,
# then also do the symbolic route via binomial-expansion of E[(D)^j] using
# the standard central-moment-of-a-sum-of-iid formula via multinomial only
# for orders 3,4 by hand (Bienayme-type formulas), i.e. genuinely different
# algebra, not the same cumulant machinery.

print("\n--- symbolic mu_3, mu_4 of D (sum of k iid centered Bernoulli) via")
print("    the classical i.i.d.-sum central moment formulas (different algebra")
print("    from cumulant recursion): ---")
# For a sum D = sum_{i=1}^k Y_i of iid centered variables Y_i (E[Y]=0):
#   E[D^3] = k * E[Y^3]                      (cross terms vanish since E[Y]=0)
#   E[D^4] = k * E[Y^4] + 3*k*(k-1)*(E[Y^2])^2
# (standard identities for sums of iid mean-zero variables, elementary
#  multinomial expansion + independence + E[Y]=0 killing all mixed terms
#  except the "all-square-pairs" term for order 4)
EY2 = single_moments[2]
EY3 = single_moments[3]
EY4 = single_moments[4]
mu3_indep_route = expand(k*EY3)
mu4_indep_route = expand(k*EY4 + 3*k*(k-1)*EY2**2)

cited_mu3 = k*g*(1-g)*(1-2*g)
cited_mu4 = k*g*(1-g)*(1+3*(k-2)*g*(1-g))

print(f"  mu_3 (this independent route) = {mu3_indep_route}")
print(f"  mu_3 (cited classical formula) = {expand(cited_mu3)}")
print(f"  difference = {simplify(mu3_indep_route - cited_mu3)}")

print(f"  mu_4 (this independent route) = {mu4_indep_route}")
print(f"  mu_4 (cited classical formula) = {expand(cited_mu4)}")
print(f"  difference = {simplify(mu4_indep_route - cited_mu4)}")

assert simplify(mu3_indep_route - cited_mu3) == 0
assert simplify(mu4_indep_route - cited_mu4) == 0
print("  BOTH MATCH -- independent confirmation of the two classical formulas")
print("  cited in gamma_second_order_attempt/ATTEMPT.md Sec.5, via a route")
print("  DIFFERENT from the target's cumulant-recursion (this uses the")
print("  elementary 'sum of iid mean-zero variables' moment identities).")
