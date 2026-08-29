"""
02_inner_expansion_derivation.py

GAMMA-CROSSOVER-MATCHED-ASYMPTOTICS-ATTEMPT (wave 34), DISC-DEC-151.

THE CENTRAL NEW DERIVATION OF THIS FRONT: the INNER-REGION asymptotic of
term_m(n,gamma) for m FIXED (O(1)) as n -> infinity -- a genuinely
different, and (as this script shows) considerably easier, limit than the
MESOSCALE limit m = lambda*sqrt(n), lambda fixed, that Estagios 56-59 all
work in.

Route: second-order Watson's-lemma expansion of the inner t-integral,
I(n,m,gamma) := Integral_0^1 t^m (1-t)^m (1-gamma*t)^(n-m) dt,
substituting t = s/n and expanding the integrand in powers of 1/n with m
held as a SYMBOLIC FIXED PARAMETER (not scaled with n) -- together with the
exact polynomial-in-n expansion of the binomial prefactor
C(n+m+1,2m+1)/B(m+1,m+1). This is entirely different machinery from the
inner-t-saddle-point Laplace method used throughout Estagios 56-58 (which
is valid for m -> infinity), because at fixed m the integral's peak does
NOT sharpen -- there is no saddle point to speak of; ordinary Watson's
lemma (expand integrand, integrate term by term) applies directly and
gives a clean POWER series in 1/n.

Result derived here:

    term_m(n,gamma) = 1/gamma + A_m(gamma)/n + O(1/n^2),   m = O(1) fixed,

    A_m(gamma) = m(m+3)/(2*gamma) - m(m+1)/gamma^2.

Two INDEPENDENT, non-circular sanity checks of this new formula, both
performed symbolically below:
  (i) A_0(gamma) = 0 exactly -- consistent with the cited EXACT fact
      term_0(n,gamma) = (1-(1-gamma)^(n+1))/gamma, whose distance from
      1/gamma is EXPONENTIALLY small in n, not O(1/n) -- so the O(1/n)
      coefficient at m=0 had better vanish identically, and it does.
  (ii) -gamma*A_1(gamma) = c(gamma) = 2(1-gamma)/gamma EXACTLY -- i.e.
      this front's fresh, independently-derived A_m(gamma) formula
      reproduces the ALREADY-PROVED (Estagio 52, re-verified script 01
      Part D of this front) local rate c(gamma) at m=1, via a completely
      different derivation route (direct fixed-m Watson expansion here,
      vs. a direct term_1/term_0 ratio limit there). This is a genuine,
      non-circular validation of the new formula.

No .py file of any ancestor/predecessor/referee front was read, imported,
or consulted. This derivation is written entirely fresh from the
mathematical definitions cited (and re-verified) in script 01.
"""
import sympy as sp
from sympy import symbols, Rational, factorial, simplify, series, oo, exp, sqrt, Function, O

print("=" * 78)
print("STEP 1: exact expansion of the Watson's-lemma integrand at fixed m,")
print("        substituting t = s/n, to O(1/n) beyond leading order")
print("=" * 78)

s, n, m, gamma, eps = symbols('s n m gamma epsilon', positive=True)

# (n-m)*ln(1-gamma*s/n), expanded to O(1/n) (eps := 1/n)
# ln(1-gamma*s*eps) = -gamma*s*eps - (gamma*s*eps)**2/2 - O(eps^3)
ln_term = sp.series(sp.log(1 - gamma * s * eps), eps, 0, 3).removeO()
exponent_expr = (1 / eps - m) * ln_term  # (n-m) = 1/eps - m
exponent_series = sp.series(exponent_expr, eps, 0, 2).removeO()
exponent_series = sp.expand(exponent_series)
print("(n-m)*ln(1-gamma*t), t=s/n, expanded in eps=1/n (kept to O(eps)):")
print(f"  {exponent_series}")
# expect: -gamma*s + eps*(gamma*m*s - gamma**2*s**2/2) + O(eps^2)

coeff_eps0 = exponent_series.coeff(eps, 0)
coeff_eps1 = exponent_series.coeff(eps, 1)
print(f"  O(eps^0) piece: {coeff_eps0}   (expect -gamma*s)")
print(f"  O(eps^1) piece: {coeff_eps1}   (expect gamma*m*s - gamma**2*s**2/2)")
assert simplify(coeff_eps0 - (-gamma * s)) == 0
assert simplify(coeff_eps1 - (gamma * m * s - gamma ** 2 * s ** 2 / 2)) == 0

# (1-t)^m = (1 - s*eps)^m, expanded to O(eps): 1 - m*s*eps + O(eps^2)
one_minus_t_m = sp.series((1 - s * eps) ** m, eps, 0, 2).removeO()
print(f"\n(1-t)^m expanded in eps: {one_minus_t_m}   (expect 1 - m*s*eps)")

# exp(exponent_series) expanded to O(eps): exp(-gamma*s)*(1 + eps*(coeff_eps1))
exp_leading = sp.exp(-gamma * s)
exp_correction_factor = 1 + eps * coeff_eps1  # (1+x)*e^x0 approx e^{x0}(1+x1*eps)
print(f"\n(1-gamma*t)^(n-m) ~ exp(-gamma*s) * [1 + eps*({coeff_eps1})]")

# full integrand-over-eps^{m+1} bracket (excluding s^m and e^{-gamma s} prefactors):
bracket = sp.expand((1 - eps * m * s) * (1 + eps * coeff_eps1))
bracket_to_O_eps = sp.series(bracket, eps, 0, 2).removeO()
print(f"\nCombined [ (1-t)^m ] x [ correction factor ], to O(eps):")
print(f"  {bracket_to_O_eps}")
coeff1 = sp.expand(bracket_to_O_eps.coeff(eps, 1))
print(f"  O(eps) coefficient (multiplies s^m * exp(-gamma*s)): {coeff1}")
# expect: m*(gamma-1)*s - gamma**2*s**2/2
expect_coeff1 = m * (gamma - 1) * s - gamma ** 2 * s ** 2 / 2
assert simplify(coeff1 - expect_coeff1) == 0
print("  MATCHES hand-derivation exactly: m*(gamma-1)*s - gamma^2*s^2/2")

print()
print("=" * 78)
print("STEP 2: integrate term-by-term (exact Gamma-function moments),")
print("        I(n,m,gamma) ~ eps^(m+1) * [ m!/gamma^(m+1)")
print("                          + eps*( ... ) ]")
print("=" * 78)

k = symbols('k', integer=True, positive=True)
# int_0^oo s^p exp(-gamma s) ds = p! / gamma^(p+1)


def moment(p):
    return factorial(p) / gamma ** (p + 1)


I_leading = moment(m)
I_correction = m * (gamma - 1) * moment(m + 1) - (gamma ** 2 / 2) * moment(m + 2)
I_correction = simplify(I_correction)
print(f"Leading moment integral (coefficient of eps^(m+1)):      {I_leading}")
print(f"O(eps) correction integral (coefficient of eps^(m+2)):   {I_correction}")

# Factor I_correction / I_leading =: B1(m,gamma)
B1 = simplify(I_correction / I_leading)
B1 = sp.expand(B1)
print(f"\nB1(m,gamma) := I_correction / I_leading = {B1}")
expect_B1 = m * (gamma - 1) * (m + 1) / gamma - (m + 1) * (m + 2) / 2
print(f"Hand-derivation predicts:                 {sp.expand(expect_B1)}")
assert simplify(B1 - expect_B1) == 0
print("MATCHES.")

print()
print("=" * 78)
print("STEP 3: exact expansion of the binomial/factorial prefactor")
print("        C(n+m+1,2m+1)/B(m+1,m+1), fixed m, n -> infinity")
print("=" * 78)

# (n+m+1)!/(n-m)! = product_{k=-m+1}^{m+1} (n+k) = n^(2m+1) * prod(1+k/n)
# Sum_{k=-m+1}^{m+1} k = 2m+1  (arithmetic series, proved below symbolically
# for concrete small m, and by the general arithmetic-series formula).
m_val_check = symbols('m_check')
for mm in range(0, 6):
    ks = list(range(-mm + 1, mm + 2))
    s_k = sum(ks)
    assert s_k == 2 * mm + 1, (mm, s_k)
print("Sum_{k=-m+1}^{m+1} k = 2m+1, confirmed for m=0..5 (general arithmetic-series fact).")

# So ln[(n+m+1)!/(n-m)!] = (2m+1)*ln(n) + (2m+1)/n + O(1/n^2)
# => (n+m+1)!/(n-m)! = n^(2m+1) * [1 + (2m+1)/n + O(1/n^2)]
prefactor_correction = 2 * m + 1
print(f"(n+m+1)!/(n-m)! ~ n^(2m+1) * [1 + ({prefactor_correction})/n + O(1/n^2)]")

print()
print("=" * 78)
print("STEP 4: assemble term_m(n,gamma) = (gamma^m/n^m)*m!*T(n,m) to O(1/n)")
print("=" * 78)

# T(n,m) = [(n+m+1)!/(n-m)!] * I(n,m,gamma) / (m!)^2
#        ~ n^(2m+1)[1+(2m+1)/n] * (m!/gamma^(m+1)) * n^(-(m+1)) [1+B1/n] / (m!)^2
#        = [n^m / (m! gamma^(m+1))] * [1 + ((2m+1)+B1)/n + O(1/n^2)]
total_bracket = simplify(prefactor_correction + B1)
total_bracket = sp.expand(total_bracket)
print(f"(2m+1) + B1(m,gamma) = {total_bracket}")

# term_m = (gamma^m/n^m) * m! * T(n,m)
#        = (1/gamma) * [1 + total_bracket/n + O(1/n^2)]
A_m = simplify(total_bracket / gamma)
A_m = sp.expand(A_m)
print(f"\n*** A_m(gamma) := gamma-scaled O(1/n) coefficient of term_m ***")
print(f"    A_m(gamma) = {A_m}")

A_m_factored = sp.factor(A_m)
print(f"    A_m(gamma) factored = {A_m_factored}")

# Cross-check against the target closed form claimed in the ATTEMPT.md prose:
A_m_target = m * (m + 3) / (2 * gamma) - m * (m + 1) / gamma ** 2
diff_Am = simplify(A_m - A_m_target)
print(f"\nClaimed closed form: m(m+3)/(2*gamma) - m(m+1)/gamma^2")
print(f"Difference (should be 0): {diff_Am}")
assert diff_Am == 0
print("EXACT MATCH.")

print()
print("=" * 78)
print("STEP 5: two non-circular validation checks")
print("=" * 78)

A_0 = A_m.subs(m, 0)
print(f"A_0(gamma) = {A_0}   (expect exactly 0, since term_0->1/gamma EXPONENTIALLY, no O(1/n) term)")
assert simplify(A_0) == 0
print("  CONFIRMED: A_0 = 0 exactly.")

A_1 = simplify(A_m.subs(m, 1))
print(f"\nA_1(gamma) = {A_1}")
neg_gamma_A1 = simplify(-gamma * A_1)
c_gamma_cited = 2 * (1 - gamma) / gamma
print(f"-gamma*A_1(gamma) = {neg_gamma_A1}")
print(f"c(gamma) (cited, PROVED, re-verified script 01 Part D) = {c_gamma_cited}")
diff_c = simplify(neg_gamma_A1 - c_gamma_cited)
print(f"Difference (should be 0): {diff_c}")
assert diff_c == 0
print("  CONFIRMED: -gamma*A_1(gamma) = c(gamma) EXACTLY.")
print("  (Reasoning: term_1/term_0 = [1/gamma+A_1/n]/[1/gamma+A_0/n] = 1+gamma*A_1/n+O(1/n^2)")
print("   since A_0=0, so c(n,gamma):=-n*log(term_1/term_0) -> -gamma*A_1(gamma) = c(gamma).)")

print()
print("A_2, A_3, A_4 for reference:")
for mm in range(2, 5):
    print(f"  A_{mm}(gamma) = {sp.factor(A_m.subs(m, mm))}")

print()
print("ALL STEP 1-5 SYMBOLIC DERIVATIONS AND CHECKS PASSED.")
print()
print("NOTE (disclosed): this derivation is a FORMAL asymptotic expansion")
print("(Watson's lemma to next order, extending the integration domain")
print("s in [0,n] to s in [0,infinity) with an error that is standard-")
print("Watson's-lemma exponentially small in n, not derived here with an")
print("explicit rigorous remainder bound) -- matching the level of rigor")
print("this lineage's own T_prof/Delta/Delta_m derivations (Estagios")
print("56-58) were held to. It is checked extensively against exact")
print("high-precision numerics in script 03.")
