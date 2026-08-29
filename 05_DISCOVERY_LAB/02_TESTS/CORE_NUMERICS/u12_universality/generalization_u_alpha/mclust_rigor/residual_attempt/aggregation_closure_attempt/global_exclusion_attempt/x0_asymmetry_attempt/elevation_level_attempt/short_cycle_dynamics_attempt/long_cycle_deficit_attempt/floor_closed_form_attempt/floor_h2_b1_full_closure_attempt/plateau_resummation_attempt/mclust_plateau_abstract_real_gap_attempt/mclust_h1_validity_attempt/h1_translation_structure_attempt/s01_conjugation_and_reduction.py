"""
s01_conjugation_and_reduction.py

H1-TRANSLATION-STRUCTURE-ATTEMPT (wave 25, front c). Part A.

Independently (re-)derives, symbolically, the exact structural facts this
front's main new content is built on:

  1. The kernel of T_w, K_T(x,y;w) := e^{-(y-x)^2/2 - (y-x)(x+w)} (y>=x),
     factors as K_T(x,y;w) = e^{w x} * K_T(x,y;0) * e^{-w y}  -- an exact
     EXPONENTIAL-CONJUGATION (Esscher-tilt) identity for the family {T_w}.
     This is the precise algebraic mechanism by which K_A^raw depends on
     "w" (equivalently, on absolute position along the y-axis) rather than
     only on elapsed time (y-t) -- the root cause of K(y,t)'s failure to
     be a convolution/translation-invariant kernel.

  2. The "x'+w=x+y" cancellation inside K_A^raw's own definition (already
     established in this lineage, DISC-DEC-113 / h1_volterra_attempt Sec
     2.1 / h1_post_correction_attempt Sec 2.1) -- re-derived here totally
     independently (no .py file from any ancestor front opened), as the
     starting point for the NEW reduction in step 3.

  3. A NEW single-integral reduction of K_A^raw(y,t) (collapsing the
     (w,u) double integral it is originally defined over into a (h',u)
     double integral, then a single s=x''-x, h' integral, exposing the
     "aging weight" e^{-u(x+y)} depending on the ABSOLUTE quantity x+y,
     not on t or h=y-t at all) -- this is the exact object the rest of
     this front's asymptotic analysis (s02) works from.

All symbolic checks use exact sympy simplification (residuals forced to
literal 0), not floating point. No randomness anywhere in this script.
"""

import sympy as sp

print("=" * 78)
print("PART 1 -- exact exponential-conjugation identity for {T_w}")
print("=" * 78)

x, y, w, u, s, h = sp.symbols('x y w u s h', real=True)

# T_w f(x) = int_0^inf e^{-u^2/2 - u(x+w)} f(x+u) du.
# Its integral kernel, in terms of the "landing point" y0 = x+u (y0>=x):
#   K_T(x,y0;w) = e^{-(y0-x)^2/2} * e^{-(y0-x)(x+w)}
y0 = sp.symbols('y0', real=True)
K_T = sp.exp(-(y0 - x)**2 / 2) * sp.exp(-(y0 - x) * (x + w))

# Claimed factorization: K_T(x,y0;w) = e^{w*x} * K_T(x,y0;0) * e^{-w*y0}
K_T_0 = K_T.subs(w, 0)
claimed = sp.exp(w * x) * K_T_0 * sp.exp(-w * y0)

diff_exponent = sp.simplify(sp.log(K_T / claimed))
print("log(K_T(x,y0;w) / [e^{wx} K_T(x,y0;0) e^{-w y0}]) simplifies to:")
print(" ", diff_exponent)
assert sp.simplify(diff_exponent) == 0, "conjugation identity FAILED"
print("  => IDENTICALLY ZERO. Conjugation identity CONFIRMED (exact, symbolic).")
print()
print("Operator form: T_w = M_{e^{wx}} o T_0 o M_{e^{-w.}}")
print("i.e. (T_w f)(x) = e^{wx} * (T_0[e^{-w(.)} f])(x)  -- verified directly below.")

# Direct operator-level check (not just the kernel): apply both sides to a
# concrete symbolic test function and confirm the INTEGRANDS agree pointwise
# in u (stronger than agreement after integration -- avoids relying on
# convergence/interchange subtleties for the check itself).
f = sp.Function('f')
lhs_integrand = sp.exp(-u**2/2 - u*(x + w)) * f(x + u)
# RHS: e^{wx} * [T_0 applied to e^{-w(.)} f](x), with T_0[g](x) = int e^{-u^2/2-ux} g(x+u) du
g = lambda arg: sp.exp(-w * arg) * f(arg)
rhs_integrand = sp.exp(w * x) * sp.exp(-u**2/2 - u*x) * g(x + u)
rhs_integrand = sp.simplify(rhs_integrand)
diff2 = sp.simplify(lhs_integrand - rhs_integrand)
print()
print("Pointwise-in-u integrand check, LHS - RHS simplifies to:", diff2)
assert diff2 == 0, "operator-level conjugation identity FAILED"
print("  => IDENTICALLY ZERO. Operator identity T_w = M_(e^{wx}) T_0 M_(e^{-w.}) CONFIRMED.")

print()
print("=" * 78)
print("PART 2 -- the x'+w=x+y cancellation inside K_A^raw (independent re-derivation)")
print("=" * 78)

# K_A^raw(y,t) f (x) = int_t^y e^{-(y-w)/eps} (S_{y-w} T_w f)(x) dw
#                     = int_t^y e^{-(y-w)/eps} (T_w f)(x + y - w) dw
# (T_w f)(x') at x' = x+y-w:
xprime = x + y - w
exponent_full = -u**2/2 - u*(xprime + w)
exponent_reduced = -u**2/2 - u*(x + y)
diff3 = sp.simplify(exponent_full - exponent_reduced)
print("[-u^2/2 - u(x'+w)] - [-u^2/2 - u(x+y)]  with x'=x+y-w, simplifies to:")
print(" ", diff3)
assert diff3 == 0
print("  => IDENTICALLY ZERO. x'+w = x+y, INDEPENDENT of w. Re-confirmed independently.")

print()
print("=" * 78)
print("PART 3 -- NEW single-integral reduction of K_A^raw(y,t)")
print("=" * 78)
print("""
Consequence of Part 2: (S_{y-w} T_w f)(x) = int_0^inf e^{-u^2/2-u(x+y)} f(x+y-w+u) du
                                            (weight depends on x+y ONLY, not on w)

Substituting h' := y-w (h' ranges 0..y-t as w ranges t..y; dw=-dh'):

  K_A^raw(y,t) f (x)
    = int_0^{y-t} e^{-h'/eps} [ int_0^inf e^{-u^2/2-u(x+y)} f(x+h'+u) du ] dh'

Further substituting s := h'+u (s = x''-x, the landing offset), for fixed s
the inner h' ranges over [0, min(h,s)] with u=s-h'>=0, h:=y-t:

  K_A^raw(y,t) f (x) = int_0^inf f(x+s) * kappa_A(s; h, z) ds,   z := x+y

  kappa_A(s; h, z) := int_0^{min(h,s)} e^{-h'/eps} e^{-(s-h')^2/2 - (s-h')z} dh'

This kernel kappa_A depends on x ONLY through z=x+y (not through x and t
separately) -- the precise, minimal statement of "K(y,t) is not a function
of (y-t) alone": the weight's dependence on the ABSOLUTE coordinate x+y is
what breaks translation invariance, since a genuine convolution kernel
kappa(s;h) would depend on h=y-t and s only, never on x+y itself.

By contrast, kappa_B(s;h) := e^{-s/eps} 1_{[0,h]}(s) (from K_B(h)) depends
ONLY on s and h -- K_B alone IS an exact convolution / translation-invariant
kernel. K_A (equivalently M_y o K_A^raw) is the entire source of
non-invariance in K(y,t) = M_y K_A^raw(y,t) + K_B(y-t).
""")

# Numerically cross-check the reduction against the ORIGINAL raw (w,u) double
# integral for several concrete (x,y,t,eps) and a concrete test function f,
# via independent high-precision quadrature (mpmath), confirming the algebra
# above did not introduce an error. Done in s01b (separate file) to keep
# this file's role purely symbolic/exact.
print("Numerical cross-check of this reduction against the raw (w,u) double")
print("integral is performed independently in s01b_reduction_numeric_check.py")
print("(kept separate so this file remains pure exact symbolic algebra).")
