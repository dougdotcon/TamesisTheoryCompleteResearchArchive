"""
Adversarial (referee) independent re-derivation of the Growth-Exclusion Lemma,
ATTEMPT.md Section 2. Built entirely from the prose statement of the lemma;
no .py file from the target front or any ancestor front was opened.

Lemma under test (verbatim from ATTEMPT.md Section 2.1):
  ODE:  u_x(x,y) - (x+y)*u(x,y) = f(x),   x >= x0,  y >= 0 fixed parameter.
  (i) Existence: u_p(x,y) = -e^{x^2/2+xy} * int_x^inf e^{-(t^2/2+ty)} f(t) dt
      solves the inhomogeneous equation, bounded as x->inf, for f of
      sub-Gaussian growth.
  (ii) Uniqueness: general solution is u_p + C(y) e^{x^2/2+xy}; since
      e^{x^2/2+xy} -> +inf as x->inf for every y>=0, boundedness forces C(y)=0.

We check:
  A. e^{x^2/2+xy} solves the homogeneous ODE u_x = (x+y) u.
  B. u_p solves the inhomogeneous ODE exactly (Leibniz differentiation under
     the integral), for a SYMBOLIC/abstract f (not a specific f), to make
     sure the argument is not an artifact of one f.
  C. The y=0, f=-1 special case reduces exactly to R(x) = e^{x^2/2}
     int_x^inf e^{-t^2/2} dt (the record's own closed form for psi1), and
     that this equals sqrt(pi/2) erfcx(x/sqrt2) as claimed.
  D. A concrete numerical growth-mode illustration independent of the
     front's own (x=0..15, 1e-30 admixture) table: different x-grid,
     different admixture size, to make sure the qualitative blow-up claim
     is not cherry picked.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 60

print("="*70)
print("PART A: e^{x^2/2+xy} solves the homogeneous ODE u_x = (x+y) u")
print("="*70)
x, y, t = sp.symbols('x y t', real=True)
u_h = sp.exp(x**2/2 + x*y)
lhs = sp.diff(u_h, x) - (x+y)*u_h
lhs_simplified = sp.simplify(lhs)
print("u_x - (x+y)*u =", lhs_simplified)
assert lhs_simplified == 0, "Homogeneous solution FAILS to solve u_x=(x+y)u"
print("PASS: homogeneous solution verified symbolically, exact.\n")

print("="*70)
print("PART B: u_p solves u_x - (x+y) u = f(x) for an ABSTRACT f")
print("="*70)
# Use an abstract function f(t), and represent I(x,y) = int_x^inf e^{-(t^2/2+ty)} f(t) dt
# symbolically via sympy's Function + Integral, then differentiate under the
# integral sign via Leibniz's rule manually (since sympy can't always do this
# automatically for an abstract Function integrand with x as a bound), and
# verify the ODE holds by direct algebraic substitution of the Leibniz result.

f = sp.Function('f')
I = sp.Function('I')(x, y)  # I(x,y) := int_x^inf e^{-(t^2/2+ty)} f(t) dt
# By Leibniz's rule (differentiating an integral wrt its lower limit x, with
# the INTEGRAND itself not depending on x -- only the limit does):
#   d/dx int_x^inf g(t) dt = -g(x)     (g(t) = e^{-(t^2/2+ty)} f(t), no x-dependence in g)
# so dI/dx = -e^{-(x^2/2+xy)} f(x).  This is the single non-trivial calculus step
# in the whole lemma; verify it independently on a CONCRETE f where sympy CAN do
# the integral/derivative symbolically end to end, then re-affirm the abstract
# argument is just Leibniz's rule for a limit-only dependency (no integrand x-dependence).
print("Sub-check B1: Leibniz rule confirmed on a concrete decaying f(t)=t")
f_concrete = t
I_concrete = sp.integrate(sp.exp(-(t**2/2 + t*y)) * f_concrete, (t, x, sp.oo))
print("I(x,y) [f=t] =", I_concrete)
dI_dx_direct = sp.diff(I_concrete, x)
dI_dx_leibniz = -sp.exp(-(x**2/2 + x*y)) * f_concrete.subs(t, x)
diff_check = sp.simplify(dI_dx_direct - dI_dx_leibniz)
print("dI/dx (direct diff of closed form) - (-e^{-(x^2/2+xy)} f(x)) =", diff_check)
assert diff_check == 0
print("PASS: Leibniz rule confirmed exactly on concrete f=t.\n")

print("Sub-check B2: general abstract-f argument, symbolic manipulation")
# u_p = -e^{x^2/2+xy} * I(x,y),  I as an abstract Function of x (with dI/dx = -e^{-(x^2/2+xy)} f(x))
Ifun = sp.Function('I')(x)
u_p = -sp.exp(x**2/2 + x*y) * Ifun
dIdx_sym = sp.Symbol('dIdx')  # placeholder for dI/dx
u_p_x = sp.diff(u_p, x)
# substitute the known value of dI/dx (Leibniz result) into u_p_x
u_p_x_sub = u_p_x.subs(sp.Derivative(Ifun, x), -sp.exp(-(x**2/2 + x*y))*sp.Function('f')(x))
lhs2 = sp.simplify(u_p_x_sub - (x+y)*u_p.subs(Ifun, sp.Function('I')(x)))
# Rebuild lhs2 properly: u_p_x_sub - (x+y)*u_p, both with I(x) as abstract Function(x)
u_p_check = -sp.exp(x**2/2 + x*y) * sp.Function('I')(x)
lhs_full = sp.diff(u_p_check, x).subs(sp.Derivative(sp.Function('I')(x), x),
                                       -sp.exp(-(x**2/2+x*y))*sp.Function('f')(x)) \
           - (x+y)*u_p_check
lhs_full_simplified = sp.simplify(sp.expand(lhs_full))
print("u_p_x - (x+y) u_p  [after substituting Leibniz value of dI/dx] =", lhs_full_simplified)
assert sp.simplify(lhs_full_simplified - sp.Function('f')(x)) == 0
print("PASS: u_p solves the inhomogeneous ODE exactly, for abstract f, given only")
print("      the Leibniz-rule fact dI/dx = -e^{-(x^2/2+xy)} f(x).\n")

print("="*70)
print("PART C: uniqueness argument + y=0,f=-1 special case reduces to R(x)")
print("="*70)
# General solution = u_p + C(y) e^{x^2/2+xy}. Growth of e^{x^2/2+xy} as x->inf:
# for FIXED y>=0, x^2/2 dominates xy (which is at most linear), so this ->inf.
# Verify this claim symbolically via limit for several representative y (including
# y negative-ish edge y=0, and a generic positive y, and a symbolic y with assumption y>=0).
yy = sp.Symbol('yy', nonnegative=True)
lim_val = sp.limit(sp.exp(x**2/2 + x*yy), x, sp.oo)
print("lim_{x->inf} e^{x^2/2+xy} for symbolic y>=0:", lim_val)
assert lim_val == sp.oo
print("PASS: growth mode diverges as x->inf for every y>=0 (symbolic, general y).\n")

print("y=0, f=-1 special case:")
# u_p(x,0) with f(t)=-1:
I_y0 = sp.integrate(sp.exp(-t**2/2)*(-1), (t, x, sp.oo))
u_p_y0 = sp.simplify(-sp.exp(x**2/2) * I_y0)
print("u_p(x,0) [f=-1] =", u_p_y0)
R_closed = sp.sqrt(sp.pi/2) * sp.erfc(x/sp.sqrt(2)) * sp.exp(x**2/2)
# erfcx(z) := e^{z^2} erfc(z); record's R(x) = sqrt(pi/2) erfcx(x/sqrt2)
#           = sqrt(pi/2) * e^{x^2/2} * erfc(x/sqrt2)
diff_R = sp.simplify(u_p_y0 - R_closed)
print("u_p(x,0) - sqrt(pi/2) erfcx(x/sqrt2) [as e^{x^2/2} erfc(x/sqrt2)] =", diff_R)
assert diff_R == 0
print("PASS: y=0,f=-1 special case is EXACTLY R(x), matching the record's closed form.\n")

# Also directly check R(x) = e^{x^2/2} int_x^inf e^{-t^2/2} dt using the OTHER
# closed form int_x^inf e^{-t^2/2} dt = sqrt(pi/2) erfc(x/sqrt2)
direct_int = sp.integrate(sp.exp(-t**2/2), (t, x, sp.oo))
print("int_x^inf e^{-t^2/2} dt (sympy) =", direct_int)
assert sp.simplify(direct_int - sp.sqrt(sp.pi/2)*sp.erfc(x/sp.sqrt(2))) == 0
print("PASS: consistent with erfc definition.\n")

print("="*70)
print("PART D: numerical illustration of growth-mode blow-up (independent grid/size)")
print("="*70)
def R_mp(xv):
    xv = mp.mpf(xv)
    return mp.e**(xv**2/2) * mp.quad(lambda t: mp.e**(-t**2/2), [xv, xv+50, mp.inf])

admix = mp.mpf('1e-25')  # different size than the front's 1e-30
xs = [0, 5, 9, 11, 13, 14, 16]  # different grid than the front's 0,8,10,12,15
print(f"{'x':>4} | {'R(x)':>22} | {'R(x)+{}·e^(x²/2)'.format(admix):>26} | relative blow-up")
for xv in xs:
    Rval = R_mp(xv)
    contaminated = Rval + admix * mp.e**(mp.mpf(xv)**2/2)
    rel = abs(contaminated - Rval)/abs(Rval) if Rval != 0 else mp.inf
    print(f"{xv:>4} | {mp.nstr(Rval, 12):>22} | {mp.nstr(contaminated, 12):>26} | {mp.nstr(rel, 6)}")

print("\nQualitative check: blow-up should be increasing/eventually dominant.")
rels = []
for xv in xs:
    Rval = R_mp(xv)
    contaminated = Rval + admix * mp.e**(mp.mpf(xv)**2/2)
    rels.append(abs(contaminated - Rval)/abs(Rval))
monotone_growth = all(rels[i] <= rels[i+1]*1.01 for i in range(len(rels)-1)) or rels[-1] > rels[0]*1e6
print("Blow-up grows dramatically over the grid (independent confirmation):", rels[-1] > rels[0]*1e6)
assert rels[-1] > rels[0] * 1e6
print("PASS: independent numerical illustration confirms qualitative claim (different grid/admixture).\n")

print("ALL PART A-D CHECKS PASSED.")
