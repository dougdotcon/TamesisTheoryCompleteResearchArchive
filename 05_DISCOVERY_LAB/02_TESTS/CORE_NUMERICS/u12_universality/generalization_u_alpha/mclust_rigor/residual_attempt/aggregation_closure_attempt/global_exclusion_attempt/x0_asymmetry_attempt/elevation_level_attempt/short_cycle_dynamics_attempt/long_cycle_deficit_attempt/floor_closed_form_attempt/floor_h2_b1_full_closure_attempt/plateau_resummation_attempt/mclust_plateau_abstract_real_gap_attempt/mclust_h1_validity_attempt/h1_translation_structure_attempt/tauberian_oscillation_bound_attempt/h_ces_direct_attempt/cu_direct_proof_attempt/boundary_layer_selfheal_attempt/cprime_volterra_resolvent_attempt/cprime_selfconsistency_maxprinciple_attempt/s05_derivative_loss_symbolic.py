"""
s05_derivative_loss_symbolic.py

Front: CPRIME-SELFCONSISTENCY-MAXPRINCIPLE-ATTEMPT

Purpose: check whether a NAIVE maximum-principle-for-Lipschitz-constants
argument -- differentiating (E2) directly in x to bound the Lipschitz
constant L_Phi(y):=sup_x|Phi_x(x,y)| (i.e. attack (C') directly, not (B)) --
can bypass the sophisticated (DX-K)-based machinery that
`cu_direct_proof_attempt` (wave 29, DISC-DEC-134, cited not re-derived) built
for exactly this purpose.

Route tested: differentiate (E2) in x (trivial, no x-dependence in the
boundary term e^{-y/eps}):
    Phi_x(x,y) = (1/eps) int_0^y e^{-v/eps} W_x(x+v,y-v) dv
and then differentiate the ALREADY-CITED KEY identity W=Psi-eps*Psi_x in x:
    W_x = Psi_x - eps*Psi_xx

This SECOND line is the crux this script checks, symbolically: does W_x
reduce to first-derivative (Psi_x) content alone, or does it genuinely
require Psi_xx (second derivative)? If the latter (confirmed below), then
this "shortcut" route needs EXACTLY the same second-derivative control that
made (C') hard for `cu_direct_proof_attempt`/`boundary_layer_selfheal_attempt`
to establish (their machinery is built entirely to avoid ever needing a
literal second x-derivative of Phi or Psi, via the (DX-K) identity and the
Fubini-swap trick of the "self-healing" front) -- showing directly on the
ORIGINAL PDE side (KEY/E1/E2), not just on the derived-kernel side, that a
naive differentiation shortcut does not exist.
"""
import sympy as sp

x, y, eps = sp.symbols('x y eps', positive=True)
Psi = sp.Function('Psi')

print("=" * 70)
print("Part 1: differentiate the CITED KEY identity W = Psi - eps*Psi_x")
print("        in x, symbolically")
print("=" * 70)

Psi_xy = Psi(x, y)
W_expr = Psi_xy - eps * sp.diff(Psi_xy, x)
W_x_expr = sp.diff(W_expr, x)
print("W(x,y)   = Psi - eps*Psi_x  =")
sp.pprint(W_expr)
print()
print("W_x(x,y) = d/dx[Psi - eps*Psi_x] =")
sp.pprint(sp.simplify(W_x_expr))

# Confirm the second-derivative term genuinely appears (its coefficient is
# nonzero, i.e. this is not a spurious symbolic artifact that cancels)
second_deriv_term = sp.diff(Psi_xy, x, 2)
coeff_of_second_deriv = sp.diff(W_x_expr, second_deriv_term)
print()
print("Coefficient of Psi_xx (second x-derivative of Psi) in W_x:", coeff_of_second_deriv)
assert coeff_of_second_deriv == -eps, "Second derivative unexpectedly absent or wrong coefficient!"
print("CONFIRMED: W_x = Psi_x - eps*Psi_xx GENUINELY contains a second-derivative")
print("term, with coefficient exactly -eps (nonzero for eps>0) -- not a spurious")
print("or cancelling artifact.")

print()
print("=" * 70)
print("Part 2: consequence for the naive Phi_x recursion")
print("=" * 70)
print("Phi_x(x,y) = (1/eps) int_0^y e^{-v/eps} W_x(x+v,y-v) dv")
print("           = (1/eps) int_0^y e^{-v/eps} [Psi_x(x+v,y-v) - eps*Psi_xx(x+v,y-v)] dv")
print()
print("This requires bounding Psi_xx (a SECOND x-derivative of Psi) directly,")
print("via THIS route -- something no closed-form bound is cited for anywhere")
print("in the record (only Psi and Psi_x-level quantities have established")
print("bounds: M_Psi<=M_Phi via s03; the (star-star) oscillation bound of")
print("DISC-DEC-100 Sec 5; no Psi_xx bound is cited or established).")
print()
print("This is EXACTLY the 'derivative loss' phenomenon already named in the")
print("record: DISC-DEC-100 Sec 8.4 ('differentiating (BB-Psi') in x requires")
print("control of d_x(Delta Phi), not merely Delta Phi -- an honest derivative")
print("loss obstruction') and DISC-DEC-134's whole Sec 5 machinery (the (DX-K)")
print("identity), which was built SPECIFICALLY to sidestep ever forming a")
print("literal Phi_xx/Psi_xx term, by instead differentiating the FULL Volterra")
print("equation (VOLTERRA-Phi) itself (an identity for Phi_y', not Phi_x) and")
print("bounding the resulting forcing term via K_A^raw/M_y*N structure (no")
print("second x-derivative anywhere in that route).")
print()
print("CONCLUSION (this script confirms symbolically, on the ORIGINAL PDE side")
print("via KEY/E1/E2 directly, not merely by citing the derived-kernel side):")
print("naive differentiation of (E2) in x to attack (C') directly hits the SAME")
print("second-derivative obstruction that motivated the archive's entire")
print("(DX-K)-based machinery (waves 29-30) -- there is no shortcut available")
print("via this route that avoids that machinery's own work.")

print()
print("=" * 70)
print("Part 3: for completeness -- does the SAME issue arise differentiating")
print("        (E1) instead (the other cited exact identity)?")
print("=" * 70)
Phi_ = sp.Function('Phi')
I_expr = sp.Integral(Phi_(x, sp.Symbol('yp')), (sp.Symbol('yp'), 0, y))
# (E1): Psi_x = (x+y)*Psi - I  =>  Psi_xx = Psi + (x+y)*Psi_x - I_x
# I_x(x,y) = int_0^y Phi_x(x,y')dy'  -- a first derivative of Phi, integrated over y'.
print("(E1): Psi_x = (x+y)*Psi - I.  Differentiating in x again:")
print("  Psi_xx = Psi + (x+y)*Psi_x - I_x,   I_x(x,y) := int_0^y Phi_x(x,y')dy'")
print()
print("So Psi_xx (needed by Part 2) reduces to Psi, Psi_x, and I_x -- and I_x is")
print("built from Phi_x itself (a FIRST derivative of Phi, i.e. exactly L_Phi(y')")
print("-level content, for y'<=y). This CLOSES the loop back onto L_Phi -- i.e.")
print("the naive route is genuinely SELF-REFERENTIAL at the derivative level")
print("(L_Phi needs Psi_xx needs L_Phi again), not merely 'hard' -- a second,")
print("independent confirmation (via (E1) instead of (BB-Psi')) of the same")
print("derivative-loss obstruction.")

x_sym, y_sym = sp.symbols('x_sym y_sym')
print()
print("Symbolic re-derivation of this specific consequence of (E1), confirming")
print("no algebra error in the paragraph above:")
Psi_f = sp.Function('Psi')(x, y)
E1_rhs = (x+y)*Psi_f - sp.Symbol('I')  # symbolic stand-in, I is cited/opaque here
Psi_x_from_E1 = E1_rhs
Psi_xx_from_E1 = sp.diff(Psi_x_from_E1, x) + sp.diff(Psi_f, x)  # chain rule wrt x on RHS, plus d(Psi_f)/dx from (x+y)*Psi term
# do it properly: treat I as I(x,y) a function of x too
I_func = sp.Function('I')(x, y)
Psi_x_from_E1_full = (x+y)*Psi_f - I_func
Psi_xx_from_E1_full = sp.diff(Psi_x_from_E1_full, x)
sp.pprint(sp.simplify(Psi_xx_from_E1_full))
print("(= Psi(x,y) + (x+y)*Psi_x(x,y) - I_x(x,y), matching the paragraph above)")
