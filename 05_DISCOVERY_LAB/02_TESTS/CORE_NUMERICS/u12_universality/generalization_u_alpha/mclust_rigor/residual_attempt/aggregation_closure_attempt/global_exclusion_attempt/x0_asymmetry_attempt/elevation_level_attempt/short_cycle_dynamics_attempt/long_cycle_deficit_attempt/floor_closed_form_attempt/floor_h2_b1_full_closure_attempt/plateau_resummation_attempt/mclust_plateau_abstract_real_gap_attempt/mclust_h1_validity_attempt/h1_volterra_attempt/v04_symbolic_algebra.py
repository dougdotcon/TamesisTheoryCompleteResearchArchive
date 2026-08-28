"""
v04_symbolic_algebra.py -- trivial but load-bearing symbolic sanity checks
(sympy, exact) of the pure algebra used to derive (NEW-W) and (E2') from
the required reading's own (E1)/(KEY)/(E2), for h1_volterra_attempt.
"""
import sympy as sp

x, y, v, eps, I, Psi, Psi_x = sp.symbols('x y v eps I Psi Psi_x', real=True)

# (E1): Psi_x = (x+y)*Psi - I     (given, cited)
E1_rhs = (x + y) * Psi - I

# (KEY): W = Psi - eps*Psi_x      (given, cited)
W_original = Psi - eps * Psi_x

# Substitute (E1) into (KEY):
W_new = W_original.subs(Psi_x, E1_rhs)
W_new_expanded = sp.expand(W_new)
target = (1 - eps * (x + y)) * Psi + eps * I
diff = sp.simplify(W_new_expanded - sp.expand(target))
print("Check A: W (via KEY+E1 substitution) - (1-eps(x+y))Psi - eps*I  simplifies to:", diff)
assert diff == 0, "NEW-W algebra check FAILED"
print("  PASS: W = (1 - eps*(x+y))*Psi + eps*I   is an exact algebraic consequence of (E1)+(KEY).")

print()
# Check B: along the (E2) convolution direction (x -> x+v, y -> y-v), x+y is invariant.
xp = x + v
yp = y - v
inv_check = sp.simplify((xp + yp) - (x + y))
print("Check B: (x+v)+(y-v) - (x+y) simplifies to:", inv_check)
assert inv_check == 0
print("  PASS: x+y is exactly invariant along the (E2) shift (x,y)->(x+v,y-v).")
print("  => the coefficient (1-eps(x'+y')) at the shifted point (x+v,y-v) equals")
print("     (1-eps(x+y)) at the ORIGINAL point -- a CONSTANT w.r.t. the integration")
print("     variable v -- hence can be pulled outside the v-integral in (E2), giving (E2').")

print()
# Check C: symbolic derivation of (E2') from (E2)+(NEW-W), fully expanded.
Wfun = sp.Function('W')
Psifun = sp.Function('Psi')
Ifun = sp.Function('I')
v_ = sp.symbols('v', real=True)
xi = x + y  # invariant along the shift
# W(x+v, y-v) = (1-eps*xi)*Psi(x+v,y-v) + eps*I(x+v,y-v)   [xi CONSTANT in v, by Check B]
W_shifted = (1 - eps * xi) * Psifun(x + v_, y - v_) + eps * Ifun(x + v_, y - v_)
A = sp.Function('A')(x, y)   # int_0^y e^{-v/eps} Psi(x+v,y-v) dv  (defined, not evaluated symbolically here)
Bfun = sp.Function('B')(x, y)
# (E2): Phi = e^{-y/eps} + (1/eps)*int_0^y e^{-v/eps} W(x+v,y-v) dv
# substitute W_shifted, using linearity of the integral and that (1-eps*xi) is
# v-independent so it factors out of the integral over the Psi-piece:
print("Check C (structural, by inspection -- linearity of integration):")
print("  (1/eps) * int_0^y e^{-v/eps} * [(1-eps*xi)*Psi(x+v,y-v) + eps*I(x+v,y-v)] dv")
print("  = [(1-eps*xi)/eps] * int_0^y e^{-v/eps} Psi(x+v,y-v) dv   +   int_0^y e^{-v/eps} I(x+v,y-v) dv")
print("  = [(1-eps*(x+y))/eps] * A(x,y)  +  B(x,y)                         (E2')")
print("  -- valid because (1-eps*xi) does not depend on the integration variable v")
print("     (Check B), so it is a legitimate constant-factor pull-out, not an approximation.")
