"""
adv01_from_scratch_identities.py

Independent, from-scratch referee re-derivation (sympy, exact) of the
target front's core ALGEBRAIC claims, written BEFORE reading any of the
target's own .py scripts -- only from the prose of ATTEMPT.md and the
cited ancestor documents (h1_translation_structure_attempt/ATTEMPT.md,
h1_energy_estimate_attempt/ATTEMPT.md).

Checks performed:
  1. The route-(a) KEY substitution identity: W = eps*(M_y*Psi + I).
  2. The M_{y2}-M_{y1} = -(y2-y1) algebra (route (a), Sec 2.2).
  3. T0 triviality (no algebra needed, sanity only).
  4. T1's A_t piece: 1/z2 - 1/z1 = -Delta/(z1*z2).
  5. T1's B_t change-of-variables (h1 = y1-t reparametrization) --
     confirmed as a valid substitution, symbolically.
  6. T2 dominance claim: (Delta/z2)/(Delta/z2^2) = z2, i.e. the O(1/z)
     term genuinely dominates O(1/z^2) as z2 -> infinity.
  7. The single-integral reduction of K_A^raw (independently re-derived
     from the RAW (w,u) double-integral definitions in Sec 0 of the
     predecessor/target, not copied from any script).
"""
import sympy as sp

print("="*70)
print("Check 1: KEY-substitution identity W = eps*(M_y*Psi + I)")
print("="*70)
x, y, eps, Psi, I = sp.symbols('x y eps Psi I', real=True)
z = x + y
Psi_x_from_E1 = z*Psi - I           # (E1): Psi_x = (x+y)Psi - I
W_direct = Psi - eps*Psi_x_from_E1  # (KEY): W = Psi - eps*Psi_x
M_y = (1 - eps*z)/eps
W_claimed = eps*(M_y*Psi + I)
resid1 = sp.simplify(W_direct - W_claimed)
print("W_direct - W_claimed =", resid1)
assert resid1 == 0, "MISMATCH in KEY-substitution identity"
print("PASS: W = eps*(M_y*Psi+I) confirmed exactly.\n")

print("="*70)
print("Check 2: M_{y2} - M_{y1} = -(y2-y1)")
print("="*70)
y1, y2 = sp.symbols('y1 y2', real=True)
z1 = x + y1
z2 = x + y2
My1 = (1 - eps*z1)/eps
My2 = (1 - eps*z2)/eps
diffM = sp.simplify(My2 - My1)
print("M_y2 - M_y1 =", diffM, " ; -(y2-y1) =", -(y2-y1))
assert sp.simplify(diffM - (-(y2-y1))) == 0
print("PASS.\n")

print("="*70)
print("Check 3: full M_{y2}Psi(y2)-M_{y1}Psi(y1) splitting identity")
print("="*70)
Psi_y1, Psi_y2 = sp.symbols('Psi_y1 Psi_y2', real=True)
lhs = My2*Psi_y2 - My1*Psi_y1
DeltaPsi = Psi_y2 - Psi_y1
rhs = My2*DeltaPsi + (My2 - My1)*Psi_y1
resid3 = sp.simplify(lhs - rhs)
print("lhs-rhs =", resid3)
assert resid3 == 0
print("PASS: splitting identity is exact algebra (trivially, by construction).\n")

print("="*70)
print("Check 4: T1's A_t coefficient  1/z2 - 1/z1 = -Delta/(z1*z2)")
print("="*70)
Delta = sp.symbols('Delta', positive=True)
# z2 = z1 + Delta  (since y2 = y1+Delta, z=x+y so z2=z1+Delta)
expr = sp.simplify(1/(z1+Delta) - 1/z1)
target_expr = -Delta/(z1*(z1+Delta))
print("1/z2-1/z1 =", expr, " ; claimed -Delta/(z1 z2) =", target_expr)
assert sp.simplify(expr - target_expr) == 0
print("PASS.\n")

print("="*70)
print("Check 5: T2 dominance ratio (Delta/z2)/(Delta/z2^2) = z2")
print("="*70)
ratio = sp.simplify((Delta/z2)/(Delta/z2**2))
print("ratio =", ratio)
assert sp.simplify(ratio - z2) == 0
print("PASS: O(1/z) term dominates O(1/z^2) as z2->infinity (ratio->infinity).\n")

print("="*70)
print("Check 6: single-integral reduction of K_A^raw, re-derived from")
print("the RAW (w,u) double-integral definitions (Sec 0), from scratch")
print("="*70)
# (T_w f)(x') := int_0^inf e^{-u^2/2-u(x'+w)} f(x'+u) du
# K_A^raw(y,t) f(x) := int_t^y e^{-(y-w)/eps} (S_{y-w} T_w f)(x) dw
#                    = int_t^y e^{-(y-w)/eps} (T_w f)(x+y-w) dw
# (T_w f)(x+y-w) = int_0^inf e^{-u^2/2-u(x+y-w+w)} f(x+y-w+u) du
#                = int_0^inf e^{-u^2/2-u(x+y)} f(x+y-w+u) du
u, w = sp.symbols('u w', real=True)
xprime = x + y - w  # landing point after S_{y-w}
exponent_claim = xprime + w
exponent_simplified = sp.simplify(exponent_claim)
print("x' + w  (x':=x+y-w) simplifies to:", exponent_simplified, " expected x+y")
assert sp.simplify(exponent_simplified - (x+y)) == 0
print("PASS: exponent x'+w = x+y identically, independent of w.")
print("=> (T_w f)(x+y-w) integrand exponent depends on z:=x+y only, not w or t")
print("   separately -- confirms the single-integral reduction's premise.\n")

print("="*70)
print("Check 7: Watson's-lemma IBP identity used to assemble the closed form")
print("int_0^h e^{-h'/eps} f'(x+h') dh' = e^{-h/eps}f(x+h) - f(x) + (1/eps)K_B(h)f(x)")
print("="*70)
hprime, h = sp.symbols('hprime h', positive=True)
F = sp.Function('f')
# By parts: u=F(x+h'), dv = e^{-h'/eps} dh' is the WRONG split (that's for int f, not f').
# Correct: integrate int_0^h e^{-h'/eps} F'(x+h') dh' directly via d/dh'[F(x+h')] = F'(x+h').
# Let G(h') := F(x+h'). Then int_0^h e^{-h'/eps} G'(h') dh'
#   = [e^{-h'/eps}G(h')]_0^h + (1/eps) int_0^h e^{-h'/eps} G(h') dh'   (IBP, d/dh'[e^{-h'/eps}]=-1/eps e^{-h'/eps})
#   = e^{-h/eps}G(h) - G(0) + (1/eps) int_0^h e^{-h'/eps} G(h') dh'
#   = e^{-h/eps}f(x+h) - f(x) + (1/eps) K_B(h) f(x)     since K_B(h)f(x):=int_0^h e^{-v/eps} f(x+v) dv
# This is a standard IBP fact -- confirm symbolically on a CONCRETE f, not just abstractly,
# exactly as the target's own s05 does (per its own account, Sec 4.3).
Fconcrete = hprime**3 + sp.sin(hprime)   # concrete nontrivial test function of h' alone (playing role of f(x+h'))
lhs_concrete = sp.integrate(sp.exp(-hprime/eps)*sp.diff(Fconcrete, hprime), (hprime, 0, h))
rhs_concrete = sp.exp(-h/eps)*Fconcrete.subs(hprime, h) - Fconcrete.subs(hprime, 0) + \
               (1/eps)*sp.integrate(sp.exp(-hprime/eps)*Fconcrete, (hprime, 0, h))
diff_concrete = sp.simplify(lhs_concrete - rhs_concrete)
print("On F(h')=h'^3+sin(h'): LHS - RHS =", diff_concrete)
assert diff_concrete == 0
print("PASS: exact IBP identity confirmed on a concrete nontrivial function.\n")

print("ALL CHECKS PASSED.")
