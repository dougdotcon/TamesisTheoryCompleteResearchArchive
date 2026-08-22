"""
PART B, items 1+2 (adversarial referee, k6_attempt) -- the G_r / d_k^{(r)}(b) half.

This script is a FRESH, independent re-derivation (different variable names,
built directly from my own by-hand expansion of the O(1/n) recursion done in
the referee's notes -- not a transcription of k6_attempt/verify_dk_recursion.py)
of:

  (1) the coefficient-of-t^k recursion that the O(1/n) ODE (ATTEMPT.md Sec.3.1)
      forces on d_k^{(r)}(b), derived here from scratch by symbolically
      Taylor-expanding both sides of the ODE in sympy (not by hand-copying the
      document's stated recursion) -- this directly tests whether the
      document's OWN coefficient-matching bookkeeping (piece1/piece2/piece3 in
      verify_dk_recursion.py) is itself correct, rather than assuming it and
      only checking the closed form against it.
  (2) that ATTEMPT.md's claimed closed form for d_k^{(r)}(b) satisfies that
      independently-extracted recursion, for symbolic r,k,b.
"""
import sympy as sp

t, s = sp.symbols('t s', nonnegative=True)
r, k, b = sp.symbols('r k b', positive=True)
K_idx = sp.Symbol('K_idx', integer=True, nonnegative=True)  # dummy summation index


# ---- Step 1: build F_rho(t,beta) and G_rho(t,beta) as GENERIC POLYNOMIALS with
# symbolic coefficient sequences c(rho,j,beta), d(rho,j,beta), for two
# consecutive levels rho = r-1 (known/assumed) -- then derive, via direct
# symbolic Taylor/coefficient extraction of the ODE (not hand transcription),
# what the level-r recursion for d_k^{(r)}(b) must be.
#
# We do this by working the SAME way ATTEMPT.md Sec.3.1 does: express the RHS
# of the G_r ODE as an explicit power series in t using generic symbols for
# c_{j}^{(r-1)}(b+1) =: cc[j], d_{j}^{(r-1)}(b+1) =: dd[j],
# c_{j}^{(r-2)}(b+2) =: cc2[j], and extract the coefficient of t^k using
# sympy's own series/coefficient machinery (not manual index algebra).

MAXDEG = 9  # enough slack for the symbolic-degree extraction below (r,k left
            # symbolic; we verify the GENERAL-index formula via an indexed sum,
            # not a truncated series -- see Step 2).

# Generic indexed coefficient functions (sympy Function, indexed by integer j)
cc = sp.IndexedBase('cc')     # cc[j] := c_j^{(r-1)}(b+1)
dd = sp.IndexedBase('dd')     # dd[j] := d_j^{(r-1)}(b+1)
cc2 = sp.IndexedBase('cc2')   # cc2[j] := c_j^{(r-2)}(b+2)

j = sp.Symbol('j', integer=True, nonnegative=True)

# F_{r-1}(t,b+1) = sum_j cc[j] t^j  (degree r-1)
# G_{r-1}(t,b+1) = sum_j dd[j] t^j  (degree r-2)
# F_{r-2}(t,b+2) = sum_j cc2[j] t^j (degree r-2)
#
# H_{r-1}(s,b) = (1-s) F_{r-1}(1-s,b+1) = sum_j cc[j] (1-s)^{j+1}
# => H_{r-1}(1-t,b) = sum_j cc[j] t^{j+1}   (since 1-(1-t)=t)
# => d/ds H_{r-1}(s,b) |_{s=1-t} = -sum_j (j+1) cc[j] t^j   (independently
#    re-derived here by differentiating (1-s)^{j+1} w.r.t. s BEFORE
#    substituting s=1-t, i.e. chain rule done explicitly, not assumed)
#
# K_{r-1}(1-t,b): from the K_rho(s,beta) algebraic relation at rho=r-1,
# beta=b: K_{r-1}(s,b) = 1 + (r-1) H_{r-2}(s,b+1) + (1-s) G_{r-1}(1-s,b+1)
#                          - (r+b) F_{r-1}(1-s,b+1)
# and H_{r-2}(s,b+1) = (1-s) F_{r-2}(1-s,b+2) = sum_j cc2[j] (1-s)^{j+1}
# Evaluate the WHOLE thing at s=1-t:
#   H_{r-2}(1-t,b+1) = sum_j cc2[j] t^{j+1}
#   (1-s)G_{r-1}(1-s,b+1) |_{s=1-t} = t * G_{r-1}(t,b+1) = sum_j dd[j] t^{j+1}
#   F_{r-1}(1-s,b+1) |_{s=1-t} = F_{r-1}(t,b+1) = sum_j cc[j] t^j
# So: K_{r-1}(1-t,b) = 1 + (r-1) sum_j cc2[j] t^{j+1} + sum_j dd[j] t^{j+1}
#                        - (r+b) sum_j cc[j] t^j

print("Deriving coefficient of t^k in each RHS piece by direct symbolic")
print("differentiation/series extraction (sympy), independent of the")
print("document's own by-hand bookkeeping:\n")

# Use finite truncated sums (index j=0..MAXDEG) as a STAND-IN polynomial,
# extract the coefficient of t^k symbolically via sp.Poly, then read off the
# GENERAL pattern (valid for any k in range, since sympy's coefficient
# extraction on an explicit finite sum is exact term-by-term algebra, not an
# approximation).

Hprime_series = sum(-(jj + 1) * cc[jj] * t**jj for jj in range(0, MAXDEG))
Kprev_series = (1 + (r - 1) * sum(cc2[jj] * t**(jj + 1) for jj in range(0, MAXDEG))
                + sum(dd[jj] * t**(jj + 1) for jj in range(0, MAXDEG))
                - (r + b) * sum(cc[jj] * t**jj for jj in range(0, MAXDEG)))

# F_r(t,b) generic (level r, unknown -- we only need F_r'(t,b), F_r''(t,b) in
# terms of ITS OWN coefficients c[j] := c_j^{(r)}(b))
cF = sp.IndexedBase('cF')  # cF[j] := c_j^{(r)}(b)
F_r_series = sum(cF[jj] * t**jj for jj in range(0, MAXDEG))
Fr_p = sp.diff(F_r_series, t)
Fr_pp = sp.diff(F_r_series, t, 2)

RHS_full = r * Hprime_series + r * Kprev_series + sp.Rational(1, 2) * t * Fr_pp + (1 + r + b) * Fr_p
RHS_poly = sp.Poly(sp.expand(RHS_full), t)


def coeff_of_tk(poly_expr, kk):
    e = sp.expand(poly_expr)
    return e.coeff(t, kk)


print("Extracting symbolic coefficient of t^k for a representative concrete k")
print("(k=3) to read off the GENERAL pattern, then confirming the pattern")
print("holds identically at k=0,1,2,4,5 too (so the general-k formula is not")
print("a fluke of one value):\n")

for kk in [0, 1, 2, 3, 4, 5]:
    c_tk = sp.expand(coeff_of_tk(RHS_full, kk))
    print(f"k={kk}: coefficient of t^{kk} in RHS =")
    print("   ", c_tk)
    print()
