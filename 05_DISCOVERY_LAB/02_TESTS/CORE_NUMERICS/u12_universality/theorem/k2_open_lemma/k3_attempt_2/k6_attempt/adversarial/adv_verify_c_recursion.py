"""
PART B, item 2 (adversarial referee, k6_attempt) -- the F_r / c_k^{(r)}(b) half.

Independently (a) re-derive, by hand-then-sympy, the "diagonal coefficient
matching" recursion that the leading-order ODE (Sec.2.2) forces on
c_k^{(r)}(b), and (b) verify -- for SYMBOLIC r,k,b, not looped over concrete
values -- that ATTEMPT.md's claimed closed form

    c_k^{(r)}(b) = [r!/(r-k)!] / prod_{i=1}^{k+1}(r+b+i)

satisfies that recursion. This is the "simpler special case" ATTEMPT.md
Sec.2.3 says was checked in verify_dk_recursion.py but does not show
separately -- this script does it explicitly, independently, from scratch.

The recursion (independently re-derived by hand from the leading-order ODE
t F_r'(t,b) + (1+r+b) F_r(t,b) = 1 + r*Ĥ_{r-1}(1-t,b), using
Ĥ_{r-1}(1-t,b) = t F_{r-1}(t,b+1) -- itself re-derived from the algebraic
h-relation Ĥ_r(s,b) = (1-s) F_r(1-s,b+1) -- and matching coefficients of t^k
on both sides):

    (k+1+r+b) c_k^{(r)}(b) = 1                              if k = 0
    (k+1+r+b) c_k^{(r)}(b) = r * c_{k-1}^{(r-1)}(b+1)        if k >= 1
"""
import sympy as sp

r, k, b = sp.symbols('r k b', positive=True)


def c_sym(rr, kk, bb):
    num = sp.factorial(rr) / sp.factorial(rr - kk)
    den = sp.rf(rr + bb + 1, kk + 1)  # (r+b+1)(r+b+2)...(r+b+k+1), k+1 factors
    return num / den


print("=== k=0 boundary case, symbolic r,b ===")
lhs0 = (0 + 1 + r + b) * c_sym(r, 0, b)
rhs0 = sp.Integer(1)
diff0 = sp.simplify(lhs0 - rhs0)
print("LHS-RHS simplify =", diff0)
assert diff0 == 0

print()
print("=== k>=1 general case, symbolic r,k,b ===")
lhs = (k + 1 + r + b) * c_sym(r, k, b)
rhs = r * c_sym(r - 1, k - 1, b + 1)
diff = sp.simplify(lhs - rhs)
print("LHS-RHS simplify =", diff)
assert diff == 0

print()
print("BOTH IDENTITIES REDUCE TO 0 SYMBOLICALLY -- c_k^{(r)}(b) closed form")
print("independently confirmed to satisfy the diagonal recursion for every r,k,b.")

print()
print("=== Cross-check: does c_k^{(r)}(b) obey the STATED boundary c_k=0 for")
print("    k>r (i.e. the sum genuinely terminates at k=r, not merely truncated")
print("    by convention)? Check c_{r+1}^{(r)}(b) via the SAME closed-form")
print("    expression (not the truncated sum) -- factorial(r)/factorial(-1) is")
print("    formally a pole (1/Gamma(0)=0), so the closed form self-terminates.")
print("=== ")
# r!/(r-k)! at k=r+1 means r!/(-1)! -- sympy factorial(-1) is zoo (undefined),
# so instead check the equivalent falling-factorial form r*(r-1)*...*(r-k+1)
# directly (this is how the "unrolling" in Sec.2.3 is actually used/interpreted):
kk_test = r + 1
i = sp.Symbol('i')
falling = sp.Product(r - i, (i, 0, kk_test - 1)).doit()
print("Falling factorial r(r-1)...(r-k+1) at k=r+1, symbolic r:", sp.simplify(falling))
print("(should be 0: the product includes the factor (r-r)=0 exactly once)")
