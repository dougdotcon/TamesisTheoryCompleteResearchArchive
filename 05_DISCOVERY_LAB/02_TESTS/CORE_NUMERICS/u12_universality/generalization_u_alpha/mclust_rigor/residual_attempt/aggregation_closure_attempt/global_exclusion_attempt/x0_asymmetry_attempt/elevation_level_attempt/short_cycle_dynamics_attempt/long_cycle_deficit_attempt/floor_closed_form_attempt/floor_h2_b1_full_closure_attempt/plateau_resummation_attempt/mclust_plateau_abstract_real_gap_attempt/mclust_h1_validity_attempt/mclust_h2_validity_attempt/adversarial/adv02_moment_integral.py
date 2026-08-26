"""
Adversarial independent verification of the moment-integral normalization
claim underlying ATTEMPT.md Section 3.1 / S2:

  (1/eps) * int_0^inf e^{-v/eps} v^m / m! dv = eps^m    EXACTLY, no leftover 1/m!.

This is the crux the front says it self-caught as a near-miss (an early
draft wrote Phi ~ sum_m eps^m/m! (d/dx-d/dy)^m W, i.e. carried an extra
1/m! that should NOT be there once the moment integral's own m! is folded
in). We independently re-derive this from scratch:
  (1/eps) int_0^inf e^{-v/eps} v^m dv  = m! * eps^m   [standard Gamma-function moment]
  => (1/eps) int_0^inf e^{-v/eps} v^m/m! dv = eps^m   (dividing by m!, no leftover).

Verify symbolically for m=0..8 (exact rational/symbolic eps), and via the
general Gamma-function argument for symbolic m.
"""
import sympy as sp

v, eps, m = sp.symbols('v eps m', positive=True)

print("="*70)
print("Symbolic check, m = 0..8, exact integration")
print("="*70)
all_pass = True
for mm in range(0, 9):
    integrand = sp.exp(-v/eps) * v**mm / sp.factorial(mm)
    val = sp.integrate(integrand, (v, 0, sp.oo))
    val = sp.simplify(val / eps)  # multiply by (1/eps) prefactor... wait need (1/eps)*integral
    # integral itself, then multiply the WHOLE thing by (1/eps)
    result = sp.simplify(val)
    expected = eps**mm
    ok = sp.simplify(result - expected) == 0
    all_pass &= ok
    print(f"m={mm}: (1/eps)*int_0^inf e^(-v/eps) v^m/m! dv = {result}   [expected eps^{mm}]   {'PASS' if ok else 'FAIL'}")

assert all_pass
print("\nAll m=0..8 cases PASS: coefficient is exactly eps^m, no leftover 1/m!.\n")

print("="*70)
print("General symbolic m via the Gamma-function moment formula")
print("="*70)
# int_0^inf e^{-v/eps} v^m dv = eps^{m+1} * Gamma(m+1) = eps^{m+1} * m!
# This is the standard substitution v = eps*u:
#   int_0^inf e^{-u} (eps u)^m * eps du = eps^{m+1} int_0^inf e^{-u} u^m du = eps^{m+1} * Gamma(m+1)
u = sp.Symbol('u', positive=True)
raw_moment_via_sub = sp.integrate(sp.exp(-u) * (eps*u)**m * eps, (u, 0, sp.oo))
print("int_0^inf e^{-v/eps} v^m dv  [via v=eps*u substitution] =", raw_moment_via_sub)
expected_raw = eps**(m+1) * sp.gamma(m+1)
diff = sp.simplify(raw_moment_via_sub - expected_raw)
print("difference from eps^(m+1)*Gamma(m+1):", diff)
assert diff == 0
print("PASS: raw moment = eps^(m+1) * m! (Gamma(m+1)), general m.\n")

print("Dividing by m! (Taylor coefficient) and by eps (the (1/eps) kernel prefactor):")
final_general = sp.simplify(raw_moment_via_sub / sp.gamma(m+1) / eps)
print("(1/eps) * int_0^inf e^{-v/eps} v^m/m! dv =", final_general)
assert sp.simplify(final_general - eps**m) == 0
print("PASS: general-m symbolic derivation confirms coefficient EXACTLY eps^m; no 1/m! survives.\n")

print("="*70)
print("Cross-check against the WRONG (self-caught, early-draft) claim")
print("="*70)
print("Early draft: Phi ~ sum_m eps^m/m! (d/dx-d/dy)^m W  -- i.e. would need")
print("  (1/eps) int_0^inf e^{-v/eps} v^m dv = eps^m  (NO 1/m! in the moment)")
wrong_claim = sp.simplify(raw_moment_via_sub / eps)
print("Actual value of (1/eps)*int_0^inf e^{-v/eps} v^m dv =", wrong_claim, " = m! * eps^m")
print("This is m!*eps^m, NOT eps^m -- confirms the early draft's un-divided moment")
print("integral is off by a factor of m!, exactly matching what the front's S2")
print("says it caught (an extra/missing 1/m! mismatch). If the Taylor 1/m! is")
print("correctly included in the SOURCE term (v^m/m!, i.e. the m-th Taylor term")
print("of W(x+v,y-v) in v), the two m!'s cancel and coefficient 1 survives.")
print("This is exactly the correct account: PASS.\n")

print("ALL MOMENT-INTEGRAL NORMALIZATION CHECKS PASSED.")
