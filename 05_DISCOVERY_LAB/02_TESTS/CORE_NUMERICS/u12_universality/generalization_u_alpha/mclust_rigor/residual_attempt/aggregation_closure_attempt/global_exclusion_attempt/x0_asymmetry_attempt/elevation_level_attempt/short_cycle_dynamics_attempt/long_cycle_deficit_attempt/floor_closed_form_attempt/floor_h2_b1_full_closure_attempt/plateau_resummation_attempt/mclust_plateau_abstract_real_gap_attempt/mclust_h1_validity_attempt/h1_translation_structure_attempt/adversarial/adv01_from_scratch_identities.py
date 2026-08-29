"""
adv01_from_scratch_identities.py

INDEPENDENT ADVERSARIAL RE-DERIVATION -- H1-TRANSLATION-STRUCTURE-ATTEMPT
referee check. Written entirely from the prose definitions in the required
reading (h1_post_correction_attempt/ATTEMPT.md Sec 0, PROOF_DEPENDENCY_MAP.md
DISC-DEC-113/115 addenda) BEFORE opening any .py file of the target front
(h1_translation_structure_attempt/). Verifies, from scratch:

  (1) T_w f(x) = int_0^inf e^{-u^2/2-u(x+w)} f(x+u) du   [ORIGINAL definition,
      as given in h1_post_correction_attempt/ATTEMPT.md Sec 0 -- NOT redefined
      here]
  (2) The claimed exponential-conjugation identity
        T_w = M_(e^{w x}) o T_0 o M_(e^{-w .})
      i.e. (T_w f)(x) = e^{w x} * (T_0[e^{-w(.)} f])(x)
      is checked as a genuine algebraic CONSEQUENCE of (1), not a silent
      redefinition.
  (3) K_A^raw's raw (w,u) double-integral definition is reduced, via the
      substitution h' := y - w, to the single-integral form
        K_A^raw(y,t) f(x) = int_0^h e^{-h'/eps} [int_0^inf e^{-u^2/2-u(x+y)}
                                                    f(x+h'+u) du] dh'
      -- re-derived symbolically from the raw definition, independent of the
      target's own s01_conjugation_and_reduction.py (not read before this
      script was written).
  (4) K_B(h) is checked to depend on (y,t) ONLY through h=y-t (trivial, but
      confirmed directly from its integral definition).

All checks are exact symbolic algebra (sympy), matching the archive's own
"no randomness needed" discipline for this sub-lineage.
"""

import sympy as sp

print("=" * 78)
print("CHECK 1 -- exponential-conjugation identity T_w = M_(e^{wx}) T_0 M_(e^{-w.})")
print("=" * 78)
print("""
Original definition (h1_post_correction_attempt/ATTEMPT.md Sec 0, cited
verbatim, NOT altered here):

  (T_w f)(x) := int_0^inf e^{-u^2/2 - u(x+w)} f(x+u) du

Claim to check: (T_w f)(x) == e^{wx} * (T_0[e^{-w(.)} f])(x), where
(T_0 g)(x) = int_0^inf e^{-u^2/2 - u x} g(x+u) du and (M_(e^{-w.})f)(x'):=
e^{-w x'} f(x').

Pointwise-in-u integrand check (sufficient, since both sides are the SAME
integration variable u over the SAME domain [0,inf) -- if the integrands
agree identically for every u, the integrals agree):
""")

x, w, u = sp.symbols('x w u', real=True)
f = sp.Function('f')

# LHS integrand (from the ORIGINAL T_w definition)
lhs_integrand = sp.exp(-u**2/2 - u*(x + w)) * f(x + u)

# RHS: e^{wx} * [ e^{-u^2/2 - u x} * (e^{-w(x+u)} f(x+u)) ]
#   -- the inner bracket is T_0 applied to g(x') := e^{-w x'} f(x'), evaluated
#      pointwise at the same landing point x+u, i.e. g(x+u) = e^{-w(x+u)} f(x+u)
rhs_integrand = sp.exp(w*x) * sp.exp(-u**2/2 - u*x) * (sp.exp(-w*(x+u)) * f(x+u))

diff = sp.simplify(sp.expand(lhs_integrand - rhs_integrand))
print("LHS integrand - RHS integrand, simplified:", diff)
assert diff == 0, "exponential-conjugation identity FAILS at the integrand level"
print("=> IDENTICAL (0), for every u. The exponential-conjugation identity is a")
print("   GENUINE, exact algebraic consequence of the ORIGINAL T_w definition --")
print("   not a silent redefinition. CONFIRMED independently.")

print()
print("=" * 78)
print("CHECK 2 -- the x'+w = x+y cancellation (independent re-derivation)")
print("=" * 78)
y, t = sp.symbols('y t', real=True)
xprime = x + y - w  # landing point of S_{y-w} applied before T_w acts
expr = sp.simplify(xprime + w - (x + y))
print("(x + y - w) + w - (x+y) simplifies to:", expr)
assert expr == 0
print("=> CONFIRMED exactly 0, independent of w: x'+w = x+y.")

print()
print("=" * 78)
print("CHECK 3 -- single-integral reduction of K_A^raw via h' := y-w substitution")
print("=" * 78)
print("""
Raw definition (cited, h1_post_correction_attempt/ATTEMPT.md Sec 0):

  K_A^raw(y,t) f(x) := int_t^y e^{-(y-w)/eps} (S_{y-w} T_w f)(x) dw

(S_{y-w} T_w f)(x) = (T_w f)(x + y - w) = (T_w f)(x')  with x' = x+y-w (as above)
                    = int_0^inf e^{-u^2/2 - u(x'+w)} f(x'+u) du
                    = int_0^inf e^{-u^2/2 - u(x+y)} f(x+y-w+u) du     [Check 2]

So (exact, before any substitution):

  K_A^raw(y,t) f(x) = int_t^y e^{-(y-w)/eps}
                         [ int_0^inf e^{-u^2/2-u(x+y)} f(x+y-w+u) du ] dw

Substitute h' := y - w  (dh' = -dw; w=t -> h'=y-t=:h; w=y -> h'=0):

  K_A^raw(y,t) f(x) = int_0^h e^{-h'/eps}
                         [ int_0^inf e^{-u^2/2-u(x+y)} f(x+h'+u) du ] dh'

Checked below symbolically: the substituted-variable outer integrand,
expressed as a function of h', matches the target's claimed formula
EXACTLY, by direct symbolic substitution (not numerically approximated).
""")
hprime, eps, h = sp.symbols("h' eps h", positive=True)
# Represent the w-integrand symbolically (as an opaque function of the
# u-integral's VALUE, call it Phi_u(arg) standing for the inner u-integral
# evaluated with shift 'arg' inside f(...)). We check the ARGUMENT of f
# inside the u-integral transforms correctly under w -> h' = y-w.
w_expr = y - hprime
shift_before = (x + y - w_expr)  # this is what appears in "f(x+y-w+u)" minus u
shift_after_target = x + hprime  # target's claimed "f(x+h'+u)" minus u
print("Argument inside f(...) [minus the +u part], before substitution "
      "(x+y-w) with w=y-h':", sp.simplify(shift_before))
print("Target's claimed argument (x+h'):", shift_after_target)
assert sp.simplify(shift_before - shift_after_target) == 0
print("=> MATCH. The single-integral reduction is a correct, exact change of")
print("   variables (w -> h'=y-w) applied to the raw double-integral")
print("   definition -- re-derived here independently, not copied.")

# Also check the outer exponential weight and integration-bound transform:
outer_weight_before = sp.exp(-(y - w_expr)/eps)  # e^{-(y-w)/eps} with w=y-h'
outer_weight_target = sp.exp(-hprime/eps)
print()
print("Outer weight e^{-(y-w)/eps} with w=y-h', simplified:",
      sp.simplify(outer_weight_before))
print("Target's claimed outer weight e^{-h'/eps}:", outer_weight_target)
assert sp.simplify(outer_weight_before - outer_weight_target) == 0
print("=> MATCH (bounds w in [t,y] <-> h' in [0,h] under h'=y-w, standard).")

print()
print("=" * 78)
print("CHECK 4 -- K_B(h) depends on (y,t) only through h=y-t (trivial, by")
print("           inspection of its own definition -- confirmed directly)")
print("=" * 78)
print("""
K_B(h) := int_0^h e^{-v/eps} S_v dv,  (S_v f)(x) = f(x+v)

This expression's only free parameters are h and eps; y and t do not appear
except through h=y-t. Trivially translation-invariant: K_B evaluated at
(y+a, t+a) for any real shift a has h=(y+a)-(t+a)=y-t unchanged, hence
IDENTICAL operator. No algebra needed beyond this inspection; confirmed
formally below by substituting y->y+a, t->t+a and checking h is invariant.
""")
a = sp.symbols('a', real=True)
h_shifted = (y + a) - (t + a)
h_original = y - t
assert sp.simplify(h_shifted - h_original) == 0
print("h(y+a,t+a) - h(y,t) simplifies to 0 for all a: CONFIRMED, K_B trivially")
print("translation-invariant, exactly as claimed.")

print()
print("=" * 78)
print("ALL FOUR CHECKS PASS. Summary:")
print("=" * 78)
print("""
1. T_w = M_(e^{wx}) T_0 M_(e^{-w.})  -- GENUINE consequence of the ORIGINAL
   T_w definition (h1_post_correction_attempt Sec 0), re-derived from
   scratch. Not a redefinition.
2. x'+w = x+y cancellation -- re-confirmed independently.
3. K_A^raw single-integral reduction -- re-derived independently via the
   h'=y-w substitution applied directly to the raw double-integral
   definition; matches the target's claimed formula exactly.
4. K_B(h) exact translation-invariance -- confirmed trivially from its own
   definition.
""")
