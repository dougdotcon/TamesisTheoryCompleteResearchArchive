"""
02_lambda_divergence_and_monotonicity.py

Consequence of script 01's Part B: with the EXACT kappa_0(gamma) = 8/(gamma(2-gamma))
pinned down (not the illustrative gamma-independent kappa_0=2.25 the Gap-1 front used
for concreteness), re-examine the Gap-1 front's own §3.3 formula

    lambda(gamma) := kappa_0(gamma) * (3/2 - gamma)

which controls the required Hoeffding split constant via C^2 > 1/4 + lambda/2
(Section 3.3 of gamma_gap1_mgf_attempt/ATTEMPT.md).

The Gap-1 front's §5 item 2 explicitly claimed:
  "The formula lambda(gamma)=kappa_0(3/2-gamma) is manifestly continuous and
   bounded on (0,1) ... between kappa_0 at gamma=1 and (3/2)kappa_0 at gamma=0,
   which strongly suggests uniformity holds with a single gamma-independent C."

This claim implicitly treated kappa_0 as a gamma-independent constant. This
script checks whether it survives once kappa_0(gamma) is substituted correctly.
"""
import sympy as sp

gamma = sp.symbols('gamma', positive=True)
beta = gamma * (2 - gamma) / 2
kappa0 = sp.simplify(4 / beta)

lam = sp.simplify(kappa0 * (sp.Rational(3, 2) - gamma))
print("lambda(gamma) = kappa_0(gamma) * (3/2 - gamma), fully substituted:")
sp.pprint(lam)
lam_simpl = sp.together(lam)
print("\nCombined single fraction:")
sp.pprint(lam_simpl)

print(f"\nlambda(gamma=1)    = {lam.subs(gamma,1)}   "
      f"(Gap-1 front's own asserted lower endpoint 'kappa_0 at gamma=1' -- "
      f"NOTE: with the correct kappa_0(1)=8, this endpoint value is 4, "
      f"not the front's illustrative kappa_0=2.25.)")
for g in [sp.Rational(9,10), sp.Rational(1,2), sp.Rational(3,10),
          sp.Rational(1,10), sp.Rational(1,100), sp.Rational(1,1000)]:
    print(f"lambda(gamma={float(g):<7g}) = {float(lam.subs(gamma,g)):.4f}")

limit_at_0 = sp.limit(lam, gamma, 0, dir='+')
print(f"\nlim_{{gamma->0+}} lambda(gamma) = {limit_at_0}")

print("\n" + "=" * 78)
print("VERDICT on Gap-1 front's Section 5 item 2 claim of boundedness on (0,1):")
print("=" * 78)
print("REFUTED. lambda(gamma) is continuous and finite at every fixed gamma in")
print("(0,1) (it is a ratio of polynomials with no pole inside the open interval,")
print("only at the boundary gamma=0), but it is UNBOUNDED as gamma -> 0+: the")
print("claimed upper bound '(3/2)*kappa_0' silently assumed kappa_0 constant.")
print("The actual sup over (0,1) is +infinity, attained only in the gamma->0 limit.")

print("\n" + "-" * 78)
print("Monotonicity of lambda(gamma) on (0,1) (needed for compact-uniformity):")
print("-" * 78)
lam_prime = sp.simplify(sp.diff(lam, gamma))
print("\nd(lambda)/d(gamma), simplified:")
sp.pprint(lam_prime)

# Determine sign of the derivative on (0,1): write as ratio, examine numerator sign
num, den = sp.fraction(sp.together(lam_prime))
num = sp.expand(num)
den = sp.expand(den)
print(f"\nNumerator of lambda'(gamma) (expanded): {num}")
print(f"Denominator of lambda'(gamma) (expanded): {den}")

# denominator is (gamma*(2-gamma))^2 or similar -- always positive on (0,1)
den_positive_on_01 = all(den.subs(gamma, sp.Rational(p, 100)) > 0 for p in range(1, 100))
print(f"\nDenominator strictly positive for gamma in (0,1) (sampled at 99 points, "
      f"p/100 for p=1..99): {den_positive_on_01}")

num_negative_on_01 = all(num.subs(gamma, sp.Rational(p, 100)) < 0 for p in range(1, 100))
print(f"Numerator strictly negative for gamma in (0,1) (sampled at 99 points): "
      f"{num_negative_on_01}")

# Rigorous symbolic check: is num < 0 for all gamma in (0,1)?
# num should be a polynomial; find its roots and confirm none lie in (0,1)
roots = sp.solve(sp.Eq(num, 0), gamma)
print(f"\nRoots of the numerator (exact, via sympy.solve): {roots}")
roots_in_01 = [r for r in roots if r.is_real and 0 < r < 1]
print(f"Roots of the numerator lying strictly inside (0,1): {roots_in_01}")

if not roots_in_01:
    # numerator has constant sign on (0,1); check sign at one interior point
    sign_at_half = num.subs(gamma, sp.Rational(1, 2))
    print(f"\nSince the numerator has no root in (0,1), it has constant sign there.")
    print(f"Numerator at gamma=1/2: {sign_at_half} (negative => numerator < 0 throughout (0,1))")
    assert sign_at_half < 0
    print("\n=> lambda'(gamma) < 0 for ALL gamma in (0,1): lambda is strictly")
    print("   DECREASING on (0,1) -- a fully rigorous, exact-algebra fact (not a")
    print("   numerical sample check), confirming the earlier numeric evidence.")
else:
    print("UNEXPECTED: numerator has a root in (0,1) -- monotonicity claim needs revision.")

print("\n" + "=" * 78)
print("CONSEQUENCE for 'uniformity in gamma as a continuum' (mandate item 2):")
print("=" * 78)
print("""
Since lambda(gamma) is exact-algebra-PROVED strictly decreasing on (0,1) with
lambda(1)=4 and lambda(gamma)->infinity as gamma->0+:

  * NO single gamma-independent split constant C works for ALL gamma in the
    open interval (0,1) simultaneously, because the Bulk/Tail Lemma's tail
    piece requires (script 04/05 below) C^2 > 1/4 + (explicit multiple of)
    lambda(gamma)/2, and the right-hand side is unbounded as gamma->0.
    This refutes the Gap-1 front's own suggested resolution of mandate item 2.

  * On any COMPACT sub-interval [gamma_0, 1) subset (0,1), gamma_0 > 0 fixed,
    lambda is bounded above by its value at the left endpoint, lambda(gamma_0)
    (by the monotonicity just proved), so a SINGLE C = C(gamma_0) DOES work
    uniformly for all gamma in [gamma_0, 1) -- this is provable and is exactly
    the same "uniform on compacts of (0,1]" pattern already established
    elsewhere in this lineage for the first-order law (wave-17 Corollary 1).

This is a precise, rigorous diagnosis (not a numerical guess): the mandate's
"uniformity over gamma in (0,1) as a continuum" is TRUE in the compact-subset
sense standard in this lineage, and FALSE in the literal single-constant-for-
the-whole-open-interval sense the predecessor's phrasing suggested.
""")
