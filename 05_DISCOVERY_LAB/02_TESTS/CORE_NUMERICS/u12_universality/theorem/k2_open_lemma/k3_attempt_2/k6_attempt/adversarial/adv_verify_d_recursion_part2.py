"""
PART B, item 2 continued: having independently confirmed (adv_verify_d_recursion.py,
via unbiased sympy series/coefficient extraction on generic indexed coefficient
sequences, cross-checked at k=0..5) that the coefficient-of-t^k recursion is

  (k+1+r+b) d_k^{(r)}(b) =
        -r(k+1) c_k^{(r-1)}(b+1)                                          [k=0 too]
      + r*[ (r-1) c_{k-1}^{(r-2)}(b+2) + d_{k-1}^{(r-1)}(b+1) - (r+b) c_k^{(r-1)}(b+1) ]   (k>=1)
      + r*[ 1 - (r+b) c_0^{(r-1)}(b+1) ]                                                    (k=0)
      + (k+1) c_{k+1}^{(r)}(b) * [(1+r+b)+k/2]

now verify -- for SYMBOLIC r,k,b, with a script written from scratch (own
variable names/structure, not copied from k6_attempt/verify_dk_recursion.py)
-- that ATTEMPT.md's claimed closed form

  d_k^{(r)}(b) = C(k+2,2) * r!/(r-k-1)! / prod_{i=1}^{k+2}(r+b+i)

satisfies this recursion, using the ALREADY-INDEPENDENTLY-PROVED c_k^{(r)}(b)
closed form (adv_verify_c_recursion.py).
"""
import sympy as sp

r, k, b = sp.symbols('r k b', positive=True)


def C(rr, kk, bb):
    """c_kk^{(rr)}(bb), independently proved (adv_verify_c_recursion.py)."""
    return sp.factorial(rr) / sp.factorial(rr - kk) / sp.rf(rr + bb + 1, kk + 1)


def D(rr, kk, bb):
    """conjectured d_kk^{(rr)}(bb)."""
    return sp.binomial(kk + 2, 2) * sp.factorial(rr) / sp.factorial(rr - kk - 1) / sp.rf(rr + bb + 1, kk + 2)


print("=== General k>=1 case, symbolic r,k,b ===")
LHS = (k + 1 + r + b) * D(r, k, b)
RHS = (-r * (k + 1) * C(r - 1, k, b + 1)
       + r * ((r - 1) * C(r - 2, k - 1, b + 2) + D(r - 1, k - 1, b + 1) - (r + b) * C(r - 1, k, b + 1))
       + (k + 1) * C(r, k + 1, b) * ((1 + r + b) + k / sp.Integer(2)))
diff = sp.simplify(LHS - RHS)
print("LHS-RHS simplify =", diff)
assert diff == 0

print()
print("=== k=0 boundary case, symbolic r,b ===")
LHS0 = (1 + r + b) * D(r, 0, b)
RHS0 = (-r * 1 * C(r - 1, 0, b + 1)
        + r * (1 - (r + b) * C(r - 1, 0, b + 1))
        + 1 * C(r, 1, b) * ((1 + r + b) + 0))
diff0 = sp.simplify(LHS0 - RHS0)
print("LHS-RHS simplify =", diff0)
assert diff0 == 0

print()
print("BOTH IDENTITIES CONFIRMED, INDEPENDENTLY, FOR SYMBOLIC r,k,b.")
print()

print("=== Sanity: d_k^{(r)}(b) is 0 for k >= r (sum should terminate at k=r-1) ===")
val_at_kr = sp.simplify(D(r, r, b))  # should reflect a pole in factorial(-1) -> formally undefined;
print("D(r,r,b) [k=r, formally out of range] via factorial ratio:", val_at_kr)
i = sp.Symbol('i')
falling = sp.Product(r - i, (i, 0, r - 1)).doit()  # r(r-1)...(1), = r!  -- NOT zero at k=r-1 boundary
falling_at_k_r = sp.Product(r - i, (i, 0, r)).doit()  # extra factor (r-r)=0 at k=r (one too many terms)
print("falling factorial r!/(r-k-1)! numerator check at k=r (should vanish):", sp.simplify(falling_at_k_r))
