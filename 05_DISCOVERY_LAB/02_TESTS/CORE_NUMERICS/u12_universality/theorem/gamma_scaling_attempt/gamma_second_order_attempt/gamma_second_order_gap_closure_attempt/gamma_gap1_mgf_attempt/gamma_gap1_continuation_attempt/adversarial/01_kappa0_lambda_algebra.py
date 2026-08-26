"""
Adversarial referee script 01.
Independent re-derivation of kappa_0(gamma) and lambda(gamma), from
scratch, based ONLY on:
  - the wave-17 front's own quoted truncation formula
    K := ceil( sqrt( (4/beta) * n * ln n ) ),  beta := gamma*(2-gamma)/2
    (gamma_scaling_attempt/ATTEMPT.md, Sec.2 line ~173 defines beta,
     Sec.5 line ~307 defines K -- confirmed by direct reading, not by
     trusting the target front's quotation)
  - the predecessor's (gamma_gap1_mgf_attempt) own definition
    K^2 =: kappa_0 * n * ln(n)   (i.e. kappa_0 is the squared-K
    normalization constant), and its own formula
    lambda(gamma) := kappa_0 * (3/2 - gamma)
    (this is the exponent such that e^{g(K)} ~ n^lambda in Sec 3.3 of
     gamma_gap1_mgf_attempt/ATTEMPT.md)

No .py file from any front in this lineage was read. This script derives
everything symbolically with sympy, independently.
"""
import sympy as sp

gamma = sp.symbols('gamma', positive=True)

# --- Step 1: beta, from wave-17 ATTEMPT.md Sec 2 ---
beta = gamma * (2 - gamma) / 2

# --- Step 2: kappa_0 from K^2 = kappa_0 * n * ln(n) ---
# K = sqrt((4/beta) * n * ln(n))  (dropping the ceiling, which only adds
# O(1) and does not affect the leading constant kappa_0)
# => K^2 = (4/beta) * n * ln(n)  => kappa_0 = 4/beta
kappa_0 = sp.simplify(4 / beta)
print("kappa_0(gamma) =", kappa_0)

kappa_0_expected = sp.Rational(8, 1) / (gamma * (2 - gamma))
diff_kappa0 = sp.simplify(kappa_0 - kappa_0_expected)
print("kappa_0 - claimed 8/(gamma*(2-gamma)) simplifies to:", diff_kappa0)
assert diff_kappa0 == 0, "MISMATCH in kappa_0 formula!"

# spot values
for gv in [sp.Integer(1), sp.Rational(1, 2), sp.Rational(1, 10), sp.Rational(1, 100)]:
    val = kappa_0.subs(gamma, gv)
    print(f"  kappa_0({gv}) = {sp.nsimplify(val)} = {float(val):.6f}")

lim0 = sp.limit(kappa_0, gamma, 0, dir='+')
print("lim_{gamma->0+} kappa_0(gamma) =", lim0)
assert lim0 == sp.oo

# --- Step 3: lambda(gamma) := kappa_0(gamma) * (3/2 - gamma) ---
lam = sp.simplify(kappa_0 * (sp.Rational(3, 2) - gamma))
print("\nlambda(gamma) = kappa_0(gamma)*(3/2-gamma) simplifies to:", lam)

lam_expected = 4 * (3 - 2 * gamma) / (gamma * (2 - gamma))
diff_lam = sp.simplify(lam - lam_expected)
print("lambda - claimed 4(3-2*gamma)/(gamma*(2-gamma)) simplifies to:", diff_lam)
assert diff_lam == 0, "MISMATCH in lambda formula!"

lam1 = lam.subs(gamma, 1)
print("\nlambda(1) =", lam1)
assert lam1 == 4

lam_lim0 = sp.limit(lam, gamma, 0, dir='+')
print("lim_{gamma->0+} lambda(gamma) =", lam_lim0)
assert lam_lim0 == sp.oo

for gv in [sp.Rational(9, 10), sp.Rational(1, 2), sp.Rational(1, 10),
           sp.Rational(1, 100), sp.Rational(1, 1000)]:
    val = lam.subs(gamma, gv)
    print(f"  lambda({gv}) = {float(val):.6f}")

# --- Step 4: monotonicity of lambda on (0,1): compute lambda', find its
# sign on the open interval (0,1) independently ---
lam_prime = sp.diff(lam, gamma)
lam_prime_simplified = sp.simplify(lam_prime)
print("\nlambda'(gamma) simplifies to:", lam_prime_simplified)

# put over common denominator, extract numerator
num, den = sp.fraction(sp.together(lam_prime_simplified))
num = sp.expand(num)
den = sp.expand(den)
print("numerator of lambda':", num)
print("denominator of lambda':", den)

# denominator sign on (0,1): gamma^2*(2-gamma)^2 > 0 always (for gamma in (0,1))
# check denominator is manifestly positive
den_test_pts = [sp.Rational(1, 100), sp.Rational(1, 2), sp.Rational(99, 100)]
for gv in den_test_pts:
    dv = den.subs(gamma, gv)
    print(f"  den({gv}) = {float(dv):.6f}  (must be >0)")
    assert dv > 0

# roots of numerator
roots = sp.solve(sp.Eq(num, 0), gamma)
print("roots of numerator of lambda':", roots)
real_roots_in_01 = [r for r in roots if r.is_real and 0 < r < 1]
print("real roots strictly inside (0,1):", real_roots_in_01)
assert len(real_roots_in_01) == 0, "Found a root in (0,1) -- monotonicity claim FALSE!"

# also check numerator has no real root over ALL reals inside (0,1) via
# a fine numeric scan as an independent sanity check (not relying purely
# on sp.solve)
import mpmath as mp
mp.mp.dps = 50
num_f = sp.lambdify(gamma, num, 'mpmath')
signs = set()
bad_pts = []
N = 20000
for i in range(1, N):
    gv = mp.mpf(i) / N
    v = num_f(gv)
    s = 1 if v > 0 else (-1 if v < 0 else 0)
    signs.add(s)
    if s == 0:
        bad_pts.append(gv)
print(f"\nFine scan of numerator sign over {N-1} points in (0,1): signs seen = {signs}")
print("zero-crossings found (should be empty):", bad_pts)
assert signs <= {-1} or signs <= {1}, "Sign changes across scan -- possible root!"

# midpoint value, matches claimed numerator -8*g^2+24*g-24 at g=1/2 -> -14
midpoint_num_claimed = -8 * sp.Rational(1, 2)**2 + 24 * sp.Rational(1, 2) - 24
print("\nClaimed numerator form -8*g^2+24*g-24 at g=1/2:", midpoint_num_claimed)
num_at_half = num.subs(gamma, sp.Rational(1, 2))
print("Our derived numerator at g=1/2:", num_at_half)
# they need not be the identical polynomial (could differ by a positive
# constant factor / different clearing of denominators), only same SIGN
# and same conclusion; check ratio is a positive constant if both nonzero
if num_at_half != 0:
    print("Sign check: our numerator at 1/2 is",
          "negative" if num_at_half < 0 else "positive")
    assert num_at_half < 0, "Sign mismatch vs claimed midpoint value!"

print("\nALL CHECKS PASSED: kappa_0(gamma)=8/(gamma(2-gamma)) confirmed;")
print("lambda(gamma)=4(3-2*gamma)/(gamma(2-gamma)) confirmed continuous,")
print("unbounded as gamma->0+, lambda(1)=4, and strictly DECREASING on (0,1)")
print("(numerator of lambda' has no real root in (0,1) and is negative")
print("throughout, confirmed both by sp.solve and by a 19999-point scan).")
