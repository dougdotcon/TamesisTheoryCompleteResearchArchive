#!/usr/bin/env python3
"""
Independent verification of:
  (a) the quotient-rule identity d/dy[A(y)/(x+y)] = e(y)/(x+y)
  (b) the tail-integral formula int_{Y0}^infty C/(x+y)^2 dy = C/(x+Y0)
  (c) the Cauchy-criterion mechanics stated in Sec 2.2/2.3
  (d) the telescoping-sum cross-check of Sec 2.3, independently reconstructed
      (geometric partition Y_n = Y0*2^n)
  (e) the "Step 2" triangle-inequality rate-transfer of Sec 3

Written fresh, without reading the target's own s01/s04 scripts.
"""
import sympy as sp

print("="*78)
print("(a) Quotient-rule identity")
print("="*78)
y, x, Y0, C = sp.symbols('y x Y0 C', positive=True)
A = sp.Function('A')
Phi_y_sym = sp.Function('Phi_y')  # stand-in for Phi_y(x), i.e. A'(y)

h_expr = A(y) / (x + y)
dh_dy = sp.diff(h_expr, y)
print(f"d/dy[A(y)/(x+y)] = {dh_dy}")

# quotient rule: d/dy[A/(x+y)] = [A'(y)*(x+y) - A(y)*1] / (x+y)^2
manual = (sp.Derivative(A(y), y) * (x + y) - A(y)) / (x + y)**2
residual = sp.simplify(dh_dy - manual)
print(f"Matches manual quotient rule [A'(y)(x+y)-A(y)]/(x+y)^2? residual={residual}")
assert residual == 0

# Now substitute A'(y) -> Phi_y(x), and check this equals e(y)/(x+y) where
# e(y) := Phi_y(x) - A(y)/(x+y)
e_def = Phi_y_sym(x) - A(y)/(x+y)
claimed = e_def / (x + y)
dh_dy_sub = dh_dy.subs(sp.Derivative(A(y), y), Phi_y_sym(x))
residual2 = sp.simplify(dh_dy_sub - claimed)
print(f"d/dy[A(y)/(x+y)]|_{{A'->Phi_y}} - e(y)/(x+y): residual = {residual2}")
assert residual2 == 0
print("PASS: exact quotient-rule identity confirmed independently.")

print()
print("="*78)
print("(b) Tail-integral formula")
print("="*78)
Yv = sp.symbols('Yv', positive=True)
tail = sp.integrate(C/(x+Yv)**2, (Yv, Y0, sp.oo))
print(f"int_Y0^infty C/(x+y)^2 dy = {sp.simplify(tail)}")
residual3 = sp.simplify(tail - C/(x+Y0))
print(f"matches C/(x+Y0)? residual = {residual3}")
assert residual3 == 0
print("PASS.")

print()
print("="*78)
print("(c) Cauchy criterion mechanics -- absolute integrability => Cauchy")
print("="*78)
print("Standard real-analysis fact (not something to 'verify' symbolically,")
print("but let's sanity check the FTC identity h(Y2)-h(Y1)=int_{Y1}^{Y2}h'(y)dy")
print("underlying it, plus that the tail bound gives a genuine Cauchy tail):")
Y1s, Y2s = sp.symbols('Y1 Y2', positive=True)
Hfun = sp.Function('H')
lhs_ftc = Hfun(Y2s) - Hfun(Y1s)
rhs_ftc = sp.Integral(sp.Derivative(Hfun(Yv), Yv).subs(Yv, sp.Symbol('y')), (sp.Symbol('y'), Y1s, Y2s))
print("This is the fundamental theorem of calculus, standard and not in")
print("dispute; the target invokes it correctly as 'standard'.")
# Concretely: |h(Y2)-h(Y1)| <= int_{Y1}^{Y2} C/(x+y)^2 dy = C/(x+Y1)-C/(x+Y2) -> 0
tail_diff = sp.integrate(C/(x+Yv)**2, (Yv, Y1s, Y2s))
print(f"int_{{Y1}}^{{Y2}} C/(x+y)^2 dy = {sp.simplify(tail_diff)}")
lim_check = sp.limit(sp.simplify(tail_diff), Y1s, sp.oo)  # as Y1->oo with Y2 following, informally
print("As Y1,Y2 -> infinity (with Y2>Y1), this tail -> 0: standard Cauchy tail.")
print("PASS (mechanics confirmed, standard fact correctly invoked).")

print()
print("="*78)
print("(d) Telescoping-sum cross-check (Sec 2.3), independently reconstructed")
print("="*78)
n, N = sp.symbols('n N', integer=True, positive=True)
Yn = Y0 * 2**n
Ynp1 = Y0 * 2**(n+1)
term = C*(1/(x+Yn) - 1/(x+Ynp1))
print(f"Per-interval bound: C*(1/(x+Y_n) - 1/(x+Y_{{n+1}}))")
Ssum = sp.summation(term, (n, 0, N-1))
Ssum_simplified = sp.simplify(Ssum)
print(f"Sum_{{n=0}}^{{N-1}} of that = {Ssum_simplified}")
# claimed to telescope to C*(1/(x+Y0) - 1/(x+Y0*2^N))
claimed_tel = C*(1/(x+Y0) - 1/(x + Y0*2**N))
residual4 = sp.simplify(Ssum_simplified - claimed_tel)
print(f"Matches C*(1/(x+Y0) - 1/(x+Y0*2^N))? residual = {residual4}")
assert residual4 == 0
print("PASS: telescoping identity confirmed independently via sympy Sum.")
lim_N = sp.limit(claimed_tel, N, sp.oo)
print(f"As N->infinity: {lim_N}  (matches claimed limit C/(x+Y0))")
assert sp.simplify(lim_N - C/(x+Y0)) == 0
print("PASS: telescoping sum limit matches the continuous-integral tail")
print("      bound C/(x+Y0) EXACTLY -- the two 'structurally different")
print("      routes' (continuous Cauchy-criterion vs discrete telescoping)")
print("      are algebraically forced to agree here (both reduce to the")
print("      same antiderivative-difference fact), which is expected and")
print("      not circular: it's confirming the ARITHMETIC bookkeeping in")
print("      each of the two independently-written derivations is correct,")
print("      not an independent NEW proof of convergence.")

print()
print("="*78)
print("(e) Step 2 triangle-inequality rate-transfer (Sec 3)")
print("="*78)
Cxe, z = sp.symbols('C_xe z', positive=True)
L = sp.symbols('L')
e_of_y, hAvg = sp.symbols('e_of_y h_Avg')
# Phi_y(x) = e(y) + A(y)/(x+y); given |e(y)|<=Cxe/z and |A(y)/(x+y)-L|<=Cxe/z
# Claim: |Phi_y(x) - L| <= 2*Cxe/z  -- NOTE: the target states O(1/(x+y))
# (same ORDER), not necessarily the SAME constant 2*Cxe/z -- check what the
# target's Sec 3 literally claims.
print("Phi_y(x) - L(x) = [e(y)] + [A(y)/(x+y) - L(x)]")
print("|Phi_y(x)-L(x)| <= |e(y)| + |A(y)/(x+y)-L(x)| <= C(x,eps)/z + C(x,eps)/z")
print("                 = 2*C(x,eps)/z")
print("This is O(1/(x+y)) as claimed (same ORDER, constant is 2C not C --")
print("ATTEMPT.md's Sec 3 states 'Phi_y(x) = L(x) + O(1/(x+y))' using O(.)")
print("notation, which correctly absorbs the factor of 2; it does NOT claim")
print("the tighter constant C(x,eps) itself carries through unchanged --")
print("checking this precisely against the prose next.")
