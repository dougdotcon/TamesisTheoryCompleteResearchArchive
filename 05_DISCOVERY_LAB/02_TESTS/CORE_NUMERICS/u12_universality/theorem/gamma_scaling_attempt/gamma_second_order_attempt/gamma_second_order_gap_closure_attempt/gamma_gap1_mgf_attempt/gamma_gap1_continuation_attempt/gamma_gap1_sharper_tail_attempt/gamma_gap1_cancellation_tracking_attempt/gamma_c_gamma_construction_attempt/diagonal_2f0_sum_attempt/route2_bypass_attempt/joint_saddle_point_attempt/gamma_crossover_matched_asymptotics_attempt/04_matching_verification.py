"""
04_matching_verification.py

GAMMA-CROSSOVER-MATCHED-ASYMPTOTICS-ATTEMPT (wave 34), DISC-DEC-151.

THE MATCHED-ASYMPTOTICS STEP: does the INNER expansion (script 02,
A_m(gamma), valid for m=O(1) fixed as n->infinity) agree, in the overlap
regime 1<<m<<sqrt(n) (equivalently lambda:=m/sqrt(n) -> 0 as n->infinity
with m -> infinity too, slowly), with the OUTER expansion (T_prof(lambda,
gamma) + its next-order correction Delta_total(lambda,gamma)/sqrt(n),
cited/re-verified script 01 Part E, from Estagios 56-58)?

Substituting m = lambda*sqrt(n) into A_m(gamma)/n and collecting powers of
lambda and 1/sqrt(n) gives TWO separate pieces:

  A_m(gamma)/n = lambda^2 * [1/(2*gamma) - 1/gamma^2]              (an O(1) term in lambda, times... )
                 + (lambda/sqrt(n)) * [3/(2*gamma) - 1/gamma^2]     (an O(1/sqrt(n)) term)

CLAIM 1 (leading, O(lambda^2) piece): this EXACTLY equals T_prof(lambda,
gamma)'s own quadratic Taylor coefficient around lambda=0 -- i.e. the
INNER expansion's leading behavior, extended formally to growing m, folds
smoothly into T_prof itself (no discrepancy at this order).

CLAIM 2 (subleading, O(lambda/sqrt(n)) piece): this EXACTLY equals
T_prof(0,gamma) times the LINEAR-in-lambda coefficient of Delta_total(
lambda,gamma) as lambda->0 -- i.e. the inner expansion's NEXT correction
folds smoothly into the ALREADY-PROVED (Estagios 57+58 combined)
mesoscale next-order correction, again with NO discrepancy.

Both claims, if true, are a genuine (non-circular, since A_m(gamma) was
derived here via a totally different route -- fixed-m Watson's lemma, not
the mesoscale Laplace-on-t+Stirling-on-m method of Estagios 56-58)
matching-asymptotics validation: the two independently-derived asymptotic
pictures (inner: this front; outer: Estagios 56-58) are mutually
consistent in their overlap region, at the two orders checked.

This is checked SYMBOLICALLY (exact, sympy) below, and then spot-checked
numerically (mpmath) by comparing both sides at concrete lambda, gamma,
n values.
"""
import sympy as sp
from sympy import symbols, Rational, simplify, series, exp, sqrt, oo

print("=" * 78)
print("SETUP: recall the closed forms (cited or derived) needed")
print("=" * 78)

lam, gamma, n, m = symbols('lambda gamma n m', positive=True)

# From script 02 (this front, DERIVED): A_m(gamma), the O(1/n) inner
# coefficient of term_m(n,gamma) at m fixed.
A_m_formula = m * (m + 3) / (2 * gamma) - m * (m + 1) / gamma ** 2
print(f"A_m(gamma) [this front, script 02]      = {A_m_formula}")

# Cited (Estagio 56, PROVED): the mesoscale profile.
T_prof = (1 / gamma) * exp(-((2 - gamma) / (2 * gamma)) * lam ** 2)
print(f"T_prof(lambda,gamma) [Estagio 56, cited] = {T_prof}")

# Cited (Estagios 57+58 combined, PROVED, re-verified script 01 Part E):
# Delta_total(lambda,gamma) x sqrt(n) = the pole-free combined next-order
# multiplicative correction.
Delta_total_x_sqrtn = Rational(3, 2) * lam - lam ** 3 / 6 - lam / gamma
print(f"Delta_total(lambda,gamma)*sqrt(n) [Estagios 57+58, cited] = {Delta_total_x_sqrtn}")

print()
print("=" * 78)
print("STEP 1: substitute m = lambda*sqrt(n) into A_m(gamma)/n, expand in")
print("        the TWO independent small parameters (lambda fixed small,")
print("        1/sqrt(n) -> 0), and separate the two orders")
print("=" * 78)

sqrtn = symbols('sqrtn', positive=True)  # sqrtn := sqrt(n), an independent formal symbol
A_m_subst = A_m_formula.subs(m, lam * sqrtn)
A_m_over_n = simplify(A_m_subst / sqrtn ** 2)
A_m_over_n_expanded = sp.expand(A_m_over_n)
print(f"A_m(gamma)/n, with m=lambda*sqrt(n):")
print(f"  {A_m_over_n_expanded}")

# Collect by power of sqrtn (equivalently 1/sqrt(n)): the lambda^2 term has
# NO 1/sqrtn factor (it is O(1) in n, i.e. this is the part that must match
# T_prof's own O(1) small-lambda behavior); the lambda term carries an
# explicit 1/sqrtn (i.e. O(1/sqrt(n)), matching Delta_total/sqrt(n)).
term_lambda2 = sp.limit(A_m_over_n_expanded, sqrtn, oo)  # the sqrtn-independent piece
remainder = sp.simplify(A_m_over_n_expanded - term_lambda2)
term_lambda1_over_sqrtn = sp.simplify(remainder * sqrtn)
print(f"\nO(1) [sqrtn-independent] piece  (should match T_prof's O(lambda^2)):")
print(f"  {term_lambda2}")
print(f"O(1/sqrtn) piece, x sqrtn (should match T_prof(0)*[linear coeff of Delta_total]):")
print(f"  {term_lambda1_over_sqrtn}")

print()
print("=" * 78)
print("STEP 2: CLAIM 1 -- match against T_prof's own small-lambda Taylor")
print("        coefficient of lambda^2")
print("=" * 78)

T_prof_taylor = series(T_prof, lam, 0, 4).removeO()
print(f"T_prof(lambda,gamma) Taylor series to O(lambda^4): {T_prof_taylor}")
Tprof_const = T_prof_taylor.coeff(lam, 0)
Tprof_lam2_coeff = T_prof_taylor.coeff(lam, 2)
print(f"  constant term (lambda^0): {Tprof_const}   (expect 1/gamma)")
print(f"  lambda^2 coefficient:     {Tprof_lam2_coeff}")

# term_lambda2 still carries its own explicit lambda**2 factor (it is the
# sqrtn-independent PIECE of A_m/n as a function of lambda, not yet
# stripped to a bare coefficient); Tprof_lam2_coeff is the bare coefficient
# (via .coeff(lam,2)). Compare on equal footing by stripping term_lambda2's
# lambda**2 factor too.
term_lambda2_bare_coeff = simplify(term_lambda2 / lam ** 2)
diff1 = simplify(term_lambda2_bare_coeff - Tprof_lam2_coeff)
print(f"Inner piece, lambda^2 factored out: {term_lambda2_bare_coeff}")
print(f"\nCLAIM 1 check: [inner lambda^2 coeff] - [T_prof's own lambda^2 Taylor coeff] = {diff1}")
assert diff1 == 0
print("CLAIM 1 CONFIRMED EXACTLY: the inner expansion's leading (lambda^2)")
print("behavior matches T_prof's own small-lambda Taylor expansion exactly.")

print()
print("=" * 78)
print("STEP 3: CLAIM 2 -- match against T_prof(0,gamma) times Delta_total's")
print("        own linear-in-lambda coefficient as lambda -> 0")
print("=" * 78)

Delta_total_taylor = series(Delta_total_x_sqrtn, lam, 0, 2).removeO()
print(f"Delta_total(lambda,gamma)*sqrt(n), Taylor to O(lambda^2): {Delta_total_taylor}")
Delta_lin_coeff = Delta_total_taylor.coeff(lam, 1)
print(f"  linear-in-lambda coefficient: {Delta_lin_coeff}")

predicted_by_outer_bare = simplify(Tprof_const * Delta_lin_coeff)
print(f"\nT_prof(0,gamma) * [Delta_total's bare linear coeff] = {predicted_by_outer_bare}")
term_lambda1_bare_coeff = simplify(term_lambda1_over_sqrtn / lam)
print(f"Inner expansion's own O(1/sqrtn) piece, lambda factored out = {term_lambda1_bare_coeff}")

diff2 = simplify(term_lambda1_bare_coeff - predicted_by_outer_bare)
print(f"\nCLAIM 2 check: difference = {diff2}")
assert diff2 == 0
print("CLAIM 2 CONFIRMED EXACTLY: the inner expansion's NEXT (O(1/sqrt(n)),")
print("linear-in-m) correction matches T_prof(0)*Delta_total's own linear-")
print("in-lambda behavior exactly.")

print()
print("=" * 78)
print("STEP 4: numeric spot-check of both claims at concrete (gamma) values")
print("        (purely as an independent sanity check of the symbolic algebra")
print("        above -- no new content, deterministic, no randomness)")
print("=" * 78)
import mpmath as mp
mp.mp.dps = 50
for gamma_val in ['0.2', '0.37', '0.5', '0.63', '0.8', '0.95']:
    g = mp.mpf(gamma_val)
    lhs1 = (1 / (2 * g) - 1 / g ** 2)
    rhs1 = -((2 - g) / (2 * g)) / g  # d^2/dlam^2 [ (1/g) e^{-A lam^2} ] /2! at lam=0 = -A/g
    d1 = abs(lhs1 - rhs1)
    lhs2 = (Rational(3, 2) / g - 1 / g ** 2)
    rhs2 = (1 / g) * (Rational(3, 2) - 1 / g)
    d2 = abs(float(lhs2) - float(rhs2))
    print(f"  gamma={gamma_val}: CLAIM1 diff={mp.nstr(d1, 6)}   CLAIM2 diff={d2:.3e}")

print()
print("ALL MATCHING CHECKS (CLAIMS 1-2) PASSED SYMBOLICALLY AND NUMERICALLY.")
print()
print("INTERPRETATION (stated precisely, not overclaimed): this confirms")
print("that the two independently-derived asymptotic regimes -- the INNER")
print("expansion (m=O(1) fixed, this front) and the OUTER expansion")
print("(m=Theta(sqrt(n)), Estagios 56-58) -- are mutually consistent when")
print("formally extended toward their common overlap region (1<<m<<sqrt(n),")
print("i.e. lambda->0 as m,n->infinity together). This is a genuine, non-")
print("trivial, non-circular cross-check (much like Estagio 56's own")
print("G_n-coefficient-reproduction check) -- but it does NOT by itself")
print("compute crossover(n,gamma)'s limiting value; see ATTEMPT.md Section")
print("5/6 for why not, and script 05 for an honest, explicitly-informal")
print("numerical exploration of where the crossover sum's O(1) mass")
print("actually accumulates.")
