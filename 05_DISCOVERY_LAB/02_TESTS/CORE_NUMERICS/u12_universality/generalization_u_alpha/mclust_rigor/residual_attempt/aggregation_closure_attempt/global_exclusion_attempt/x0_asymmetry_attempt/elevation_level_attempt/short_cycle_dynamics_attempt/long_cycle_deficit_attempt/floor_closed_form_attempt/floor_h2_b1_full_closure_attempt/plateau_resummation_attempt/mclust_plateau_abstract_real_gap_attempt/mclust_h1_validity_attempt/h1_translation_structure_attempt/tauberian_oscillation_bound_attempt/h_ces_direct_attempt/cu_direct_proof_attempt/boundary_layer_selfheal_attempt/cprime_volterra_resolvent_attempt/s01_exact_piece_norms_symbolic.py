"""
s01_exact_piece_norms_symbolic.py -- CPRIME-VOLTERRA-RESOLVENT-ATTEMPT

Fresh, independent symbolic derivation (sympy) of:

  Part 1. ||K_B(h)|| = eps*(1 - exp(-h/eps)) EXACTLY (not a bound), via
          direct evaluation of K_B(h) applied to the constant function 1,
          and the standard fact that a POSITIVE integral operator's
          sup-norm-to-sup-norm operator norm equals its value on the
          constant function 1.

  Part 2. T_w[1](x') = R(x'+w) exactly, from T_w's own raw definition.

  Part 3. The key algebraic collapse x' + w = x + y = z whenever
          x' = x + y - w (i.e. w = y - v, x' = x + v), used throughout.
          Verified purely symbolically.

  Part 4. K_A^raw(y,t)[1](x) = R(z) * eps * (1 - exp(-h/eps)) EXACTLY,
          h := y - t, z := x + y -- derived from the raw double-integral
          definition of K_A^raw, not assumed.

  Part 5. Hence ||K_A^raw(y,t)|| = R(z)*eps*(1-exp(-h/eps)) exactly
          (K_A^raw has positive kernel density too), and
          ||M_y K_A^raw(y,t)|| = |1-eps*z| * R(z) * (1-exp(-h/eps))
          exactly (M_y is a scalar multiplier, doesn't change the sign
          PATTERN of the kernel, only its overall sign).

  Part 6. K(y,t)[1](x), computed EXACTLY (not via the predecessor's
          decomposition, but freshly from K(y,t) = M_y K_A^raw + K_B),
          equals (1-exp(-h/eps)) * [R(z) + eps*sigma(z)], sigma(z):=
          1-z*R(z) -- and this collapses to the ALREADY-established
          O(1/z) leading term of (U) (a consistency / sanity check
          against the cited closed form, not new content by itself).

All checks are exact symbolic algebra; residuals asserted to be 0
(after sympy.simplify / sympy.expand). No numerics, no randomness.
"""
import sympy as sp

x, y, t, w, u, v, eps, z, h = sp.symbols('x y t w u v eps z h', positive=True)
R = sp.Function('R')  # R(arg) := sqrt(pi/2)*erfcx(arg/sqrt2), R'(a)=a*R(a)-1

print("="*70)
print("Part 1: K_B(h)[1](x) exact value")
print("="*70)
# K_B(h) f (x) := int_0^h e^{-v/eps} f(x+v) dv.  f=1:
KB1 = sp.integrate(sp.exp(-v/eps), (v, 0, h))
KB1 = sp.simplify(KB1)
print("K_B(h)[1](x) =", KB1)
expected_KB1 = eps*(1 - sp.exp(-h/eps))
assert sp.simplify(KB1 - expected_KB1) == 0
print("MATCHES eps*(1-exp(-h/eps)) -- residual 0. PASS")
print("Positivity of the kernel e^{-v/eps}>=0 on [0,h] means this IS the")
print("operator sup-norm of K_B(h) (attained exactly at f=+1), not merely")
print("a bound on it -- standard fact for positive integral operators on")
print("C_b: ||A|| = sup_x |A[1](x)| when A has a nonnegative kernel.")

print()
print("="*70)
print("Part 2: T_w[1](x') exact value, from T_w's raw definition")
print("="*70)
# T_w f(x') := int_0^inf e^{-u^2/2 - u(x'+w)} f(x'+u) du.  f=1:
xprime = sp.symbols('xprime', positive=True)
Tw1_integrand = sp.exp(-u**2/2 - u*(xprime + w))
# int_0^inf e^{-u^2/2 - u*a} du =: R(a) by definition (cited, not re-derived)
# so symbolically we just record the substitution a = xprime + w
a_arg = xprime + w
print("T_w[1](x') = int_0^inf e^{-u^2/2-u*(x'+w)} du =: R(x'+w)   (by R's own definition)")
print("i.e. T_w[1](x') = R(", a_arg, ")  -- definitional, not an assertion needing proof beyond R's def.")

print()
print("="*70)
print("Part 3: the collapse identity x' + w = x + y = z")
print("="*70)
# Used with the substitution w = y-v (v:=y-w in[0,h]), x' = x+v :
xprime_sub = x + v
w_sub = y - v
collapse = sp.expand(xprime_sub + w_sub)
print("x' + w  with x'=x+v, w=y-v  ->  ", collapse)
assert sp.simplify(collapse - (x+y)) == 0
print("Equals x+y = z identically in v -- residual 0. PASS")
print("(This is why T_{y-v} applied at the point x+v, for ANY v, always")
print(" sees Gaussian-tilt parameter exactly z = x+y, independent of v.)")

print()
print("="*70)
print("Part 4: K_A^raw(y,t)[1](x) exact value, from the raw definition")
print("="*70)
# K_A^raw(y,t) f(x) := int_t^y e^{-(y-w)/eps} (S_{y-w} T_w f)(x) dw
#                    = int_t^y e^{-(y-w)/eps} T_w f(x+y-w) dw
# Substitute v = y-w  (w=y-v, dw=-dv; w:t->y  <=>  v:h->0, h:=y-t)
# => K_A^raw(y,t) f(x) = int_0^h e^{-v/eps} T_{y-v} f(x+v) dv
# For f=1: T_{y-v}[1](x+v) = R((x+v)+(y-v)) = R(x+y) = R(z), CONSTANT in v
# (Part 3's collapse). So the whole v-integral factors:
h_ = sp.symbols('h', positive=True)
Rz = sp.symbols('Rz', positive=True)  # stands for R(z), constant w.r.t. v
KAraw1 = sp.integrate(sp.exp(-v/eps) * Rz, (v, 0, h_))
KAraw1 = sp.simplify(KAraw1)
print("K_A^raw(y,t)[1](x) =", KAraw1)
expected_KAraw1 = Rz * eps * (1 - sp.exp(-h_/eps))
assert sp.simplify(KAraw1 - expected_KAraw1) == 0
print("MATCHES R(z)*eps*(1-exp(-h/eps)) -- residual 0. PASS")
print("Since T_w has a nonnegative kernel (Gaussian-tilt e^{-u^2/2-u(.)}>=0)")
print("and the v-integral weight e^{-v/eps}>=0 too, K_A^raw(y,t) is itself")
print("a positive operator -- so this IS its exact operator norm, not a bound.")

print()
print("="*70)
print("Part 5: ||M_y K_A^raw(y,t)|| exact value (M_y is a SCALAR)")
print("="*70)
# M_y := multiplication by (1-eps*z)/eps, a CONSTANT scalar (independent
# of the integration variables w,u,v) once x is fixed -- it does not
# alter the SIGN PATTERN of K_A^raw's kernel (single overall sign flip).
My = (1 - eps*z)/eps
MyKAraw1 = sp.simplify(My * KAraw1.subs(Rz, sp.Symbol('R_z')))
print("M_y * K_A^raw(y,t)[1](x) =", MyKAraw1)
print("||M_y K_A^raw(y,t)|| = |M_y| * ||K_A^raw(y,t)|| ")
print("  = |(1-eps*z)/eps| * R(z) * eps * (1-exp(-h/eps))")
print("  = |1-eps*z| * R(z) * (1-exp(-h/eps))        (eps cancels exactly)")
abs_form = sp.Abs(1 - eps*z) * sp.Symbol('R_z') * (1 - sp.exp(-h_/eps))
# sanity: eps*|My| = |1-eps*z|
lhs_eps_My = sp.simplify(eps * sp.Abs(My))
assert sp.simplify(lhs_eps_My - sp.Abs(1 - eps*z)) == 0
print("Cancellation eps*|M_y| = |1-eps*z| confirmed symbolically -- residual 0. PASS")

print()
print("="*70)
print("Part 6: K(y,t)[1](x) exact value (both pieces combined)")
print("="*70)
# K(y,t)[1](x) = M_y K_A^raw(y,t)[1](x) + K_B(h)[1](x)
#              = (1-eps*z)*R(z)*(1-exp(-h/eps)) + eps*(1-exp(-h/eps))
#              = (1-exp(-h/eps)) * [ (1-eps*z)*R(z) + eps ]
Rz_s, z_s, eps_s, h_s = sp.symbols('Rz z eps h', positive=True)
bracket = (1 - eps_s*z_s)*Rz_s + eps_s
Ktotal1 = (1 - sp.exp(-h_s/eps_s)) * bracket
print("K(y,t)[1](x) = (1-exp(-h/eps)) * [ (1-eps*z)*R(z) + eps ]")
# Rewrite bracket via sigma(z) := 1 - z*R(z)  <=>  z*R(z) = 1-sigma(z)
sigma_s = sp.symbols('sigma', positive=True)
bracket_sub = (Rz_s - eps_s*(1-sigma_s)) + eps_s  # (1-eps z)R = R - eps*z*R = R - eps*(1-sigma)
bracket_expected = Rz_s + eps_s*sigma_s
assert sp.simplify(sp.expand(bracket_sub) - sp.expand(bracket_expected)) == 0
print("Bracket (1-eps*z)*R(z) + eps  ==  R(z) + eps*sigma(z)   [sigma:=1-z*R(z)] -- residual 0. PASS")
print()
print("=> K(y,t)[1](x) = (1-exp(-h/eps)) * [ R(z) + eps*sigma(z) ]   EXACTLY")
print()
print("Cross-check against the ALREADY-CITED closed form (cu_direct_proof_")
print("attempt Sec 3.1, wave 30 Sec 3.1): for f=1, f'=0 identically, so")
print("rho(h',z)=0 and E_full(z)=0 in that decomposition, and the leading")
print("term [f(x)-e^{-h/eps}f(x+h)]/z = (1-e^{-h/eps})/z exactly.")
print("Since R(z)=(1-sigma(z))/z, R(z)+eps*sigma(z) = 1/z + sigma(z)*(eps-1/z),")
lhs_check = sp.simplify(sp.expand(Rz_s + eps_s*sigma_s) - sp.expand((1-sigma_s)/z_s + eps_s*sigma_s))
print("Rewriting R(z)=(1-sigma)/z and simplifying:")
alt = sp.simplify((1-sigma_s)/z_s + eps_s*sigma_s - (1/z_s + sigma_s*(eps_s - 1/z_s)))
assert sp.simplify(alt) == 0
print("R(z)+eps*sigma(z) == 1/z + sigma(z)*(eps-1/z)  -- residual 0. PASS")
print("so K(y,t)[1](x) = (1-e^{-h/eps})/z + (1-e^{-h/eps})*sigma(z)*(eps-1/z),")
print("matching leading term (1-e^{-h/eps})/z EXACTLY plus a remainder of")
print("size O(sigma(z))=O(1/z^2) (already established via (G2) in the")
print("predecessor -- consistent, NOT new content; recorded here purely as")
print("an independent cross-check that this front's own from-scratch raw-")
print("operator computation reproduces the cited closed form on this")
print("trivial test case, before using the SAME raw-operator machinery to")
print("derive genuinely new content in s02/s03 below.")

print()
print("ALL PART 1-6 SYMBOLIC CHECKS PASSED. Zero residual in every assertion.")
