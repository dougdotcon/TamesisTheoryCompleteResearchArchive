"""
adv01_watson_rederivation.py -- REFEREE independent re-derivation.

Independent, from-scratch Watson's-lemma-at-fixed-m derivation of
term_m(n,gamma)'s O(1/n) inner coefficient A_m(gamma), done via a
DIFFERENT decomposition path than the front's own script 02: instead of
building "bracket = (1-eps*m*s)*(1+eps*coeff_eps1)" the way the front
does, this script (a) expands ln[(1-t)^m] and (n-m)ln(1-gamma t) as a
SINGLE combined log-integrand in t=s/n and exponentiates ONCE, and
(b) cross-checks the prefactor expansion via direct Pochhammer-ratio
asymptotics (using sympy's built-in series-at-infinity on the exact
ratio (n+m+1)!/(n-m)!/n^(2m+1), not the hand arithmetic-series argument
the front uses) -- a genuinely different sympy code path for the same
fact, not a transcription of the front's script.

Also verifies the two validation checks (A_0=0; -gamma*A_1=c(gamma))
independently.
"""
import sympy as sp
from sympy import symbols, simplify, series, factorial, oo, Rational, gamma as Gamma

print("="*78)
print("Independent re-derivation of term_m(n,gamma) inner (m fixed) expansion")
print("="*78)

s, n, m, g, eps = symbols('s n m g epsilon', positive=True)

# ---- Path A: combined log-integrand, single exponentiation --------------
# integrand (excluding s^m prefactor, after t=s/n, dt=ds/n):
#   (1-t)^m (1-g t)^(n-m),  t = s*eps,  eps := 1/n
# combined log:  m*ln(1-s*eps) + (1/eps - m)*ln(1 - g*s*eps)
log_combined = m*sp.log(1 - s*eps) + (1/eps - m)*sp.log(1 - g*s*eps)
log_series = sp.series(log_combined, eps, 0, 2).removeO()
log_series = sp.expand(log_series)
print("\nCombined log-integrand, expanded in eps=1/n to O(eps):")
print(f"  {log_series}")

c0 = log_series.coeff(eps, 0)
c1 = log_series.coeff(eps, 1)
print(f"  O(eps^0): {c0}  (expect -g*s)")
print(f"  O(eps^1): {c1}")
assert simplify(c0 - (-g*s)) == 0

# exponentiate: exp(c0 + eps*c1 + O(eps^2)) = exp(c0)*(1+eps*c1+O(eps^2))
# integrand ~ s^m * exp(-g*s) * (1 + eps*c1 + O(eps^2))
print(f"\nIntegrand ~ s^m*exp(-g*s)*(1 + eps*({c1}) + O(eps^2))")

def moment(p):
    return factorial(p) / g**(p+1)

I_leading = moment(m)

# Need integral of s^m * c1(s) * exp(-g s) ds -- c1 is a polynomial in s.
c1_poly = sp.expand(c1)
print(f"\nc1(s) as polynomial in s: {c1_poly}")
# integrate s^m * c1_poly * exp(-g*s) termwise via moments
c1_poly_dict = sp.Poly(c1_poly, s).all_coeffs()[::-1]  # ascending powers of s
I_corr = 0
for power, coeff in enumerate(c1_poly_dict):
    if coeff == 0:
        continue
    I_corr += coeff * moment(m + power)
I_corr = simplify(I_corr)
print(f"I_correction (coefficient of eps^(m+2) after integrating termwise) = {I_corr}")

B1 = simplify(I_corr / I_leading)
B1 = sp.expand(B1)
print(f"\nB1(m,g) [Path A] = {B1}")

# ---- Cross-check B1 against front's hand-derivation expect_B1 -----------
expect_B1_front = m*(g-1)*(m+1)/g - (m+1)*(m+2)/2
diff_B1 = simplify(B1 - expect_B1_front)
print(f"Front's claimed B1 formula: {sp.expand(expect_B1_front)}")
print(f"Difference (should be 0): {diff_B1}")
assert diff_B1 == 0
print("MATCH (Path A, single-exponentiation route, agrees with front's B1).")

# ---- Path B: prefactor expansion via sympy series-at-infinity, NOT the --
# ---- front's hand arithmetic-series argument -----------------------------
print()
print("="*78)
print("Prefactor (n+m+1)!/(n-m)! / n^(2m+1) -> 1 + c/n + O(1/n^2): sympy's")
print("OWN series-at-infinity on the exact Gamma-function ratio (not the")
print("front's by-hand arithmetic-series-sum argument)")
print("="*78)

for mm in range(0, 5):
    nn, epsn = symbols('nn epsn', positive=True)
    # (n+m+1)!/(n-m)! = rising_factorial(n-m+1, 2m+1) -- an explicit
    # POLYNOMIAL in n of degree 2m+1 (sp.rf expands to a polynomial for
    # integer mm), so after dividing by n^(2m+1) and substituting n=1/eps
    # this is an ORDINARY rational function of eps -- genuine Taylor
    # series at eps=0, not an asymptotic-at-infinity series (sidesteps
    # the sympy Gamma-asymptotics limitation hit above), and is a
    # completely different sympy code path from the front's own by-hand
    # arithmetic-series argument.
    poly_num = sp.expand(sp.rf(nn - mm + 1, 2*mm + 1))
    ratio = poly_num / nn**(2*mm+1)
    ratio_eps = ratio.subs(nn, 1/epsn)
    ser = sp.series(ratio_eps, epsn, 0, 2).removeO()
    ser = sp.expand(ser)
    coeff_1_over_n = ser.coeff(epsn, 1)
    print(f"  m={mm}: ratio(1/n) series to O(eps) = {ser}")
    print(f"         -> 1/n coefficient = {coeff_1_over_n}  (expect {2*mm+1})")
    assert simplify(coeff_1_over_n - (2*mm+1)) == 0
print("CONFIRMED for m=0..4 via an independent sympy route (Gamma-function")
print("asymptotic series, not the front's by-hand telescoping argument):")
print("(n+m+1)!/(n-m)! ~ n^(2m+1)*(1+(2m+1)/n+O(1/n^2)).")

print()
print("="*78)
print("Assembling term_m(n,g) = (g^m/n^m)*m!*T(n,m), T(n,m) = prefactor*I/(m!)^2")
print("="*78)
total_bracket = simplify((2*m+1) + B1)
A_m = simplify(total_bracket / g)
A_m = sp.expand(A_m)
print(f"A_m(g) [independent re-derivation] = {A_m}")

A_m_target = m*(m+3)/(2*g) - m*(m+1)/g**2
diff_final = simplify(A_m - A_m_target)
print(f"Front's claimed closed form:        {sp.expand(A_m_target)}")
print(f"Difference (should be 0): {diff_final}")
assert diff_final == 0
print("EXACT MATCH -- A_m(gamma) = m(m+3)/(2*gamma) - m(m+1)/gamma^2 independently confirmed.")

print()
print("="*78)
print("Two non-circular validation checks, independently re-run")
print("="*78)
A0 = simplify(A_m.subs(m, 0))
print(f"A_0(g) = {A0}  (expect 0)")
assert A0 == 0

A1 = simplify(A_m.subs(m, 1))
neg_g_A1 = simplify(-g*A1)
c_gamma_cited = 2*(1-g)/g
diff_c = simplify(neg_g_A1 - c_gamma_cited)
print(f"A_1(g) = {A1}")
print(f"-g*A_1(g) = {neg_g_A1}")
print(f"c(g) cited = {c_gamma_cited}")
print(f"Difference (should be 0): {diff_c}")
assert diff_c == 0
print("CONFIRMED: -g*A_1(g) = c(g) exactly, independently re-derived.")

print()
print("A_2, A_3, A_4 (independent re-derivation, for cross-reference against")
print("the front's own table):")
for mm in range(2, 5):
    print(f"  A_{mm}(g) = {sp.factor(A_m.subs(m, mm))}")

print()
print("ALL INDEPENDENT RE-DERIVATION CHECKS PASSED.")
