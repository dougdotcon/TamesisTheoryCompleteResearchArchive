"""
k02_growth_exclusion_lemma.py -- MCLUST-H2-VALIDITY-ATTEMPT

The "Growth-Exclusion Lemma" that gives full, rigorous, general-order
content to H2's phrase "excluded by boundedness": for the linear ODE

    u_x(x,y) - (x+y)*u(x,y) = f(x)        (x >= x0, y >= 0 a parameter)

the homogeneous equation u_x = (x+y)*u has general solution
C(y)*e^{x^2/2 + x*y} -- EXACTLY the growth mode named in H2's quoted
statement ("the y-differentiated homogeneous equation's e^{xy+x^2/2}
growth"). This script:

  (A) verifies symbolically (sympy, exact) that phi_h(x,y):=e^{x^2/2+x*y}
      solves the homogeneous ODE exactly;
  (B) verifies symbolically (sympy, exact, via Leibniz differentiation
      under the integral sign) that the explicit "bounded branch"
      candidate solution
        u_p(x,y) := -e^{x^2/2+x*y} * int_x^inf e^{-(t^2/2+t*y)} f(t) dt
      solves u_x - (x+y)*u = f(x) EXACTLY, for a generic f -- this is
      the SAME variation-of-parameters construction the required
      reading already uses for R(x) itself (R solves R'=xR-1, i.e. the
      y=0, f=-1 case, verified as a special case below);
  (C) gives the elementary uniqueness argument (any two solutions
      bounded on [x0,inf) as x->inf differ by C*phi_h(x,y); phi_h->inf
      superexponentially as x->inf for any y>=0, so boundedness forces
      C=0) -- this is a two-line proof, stated here explicitly;
  (D) illustrates numerically (mpmath, dps=60) exactly WHY the exclusion
      matters: starting from the bounded branch for the psi1 equation
      (f=-1, y=0 -- i.e. R(x) itself) and adding a deliberately tiny
      admixture of the excluded homogeneous mode, shows the resulting
      "solution" blows up catastrophically as x grows, while the pure
      bounded branch stays bounded and decays -- a concrete demonstration
      of the mechanism, not just the abstract claim.

No .py file from any ancestor front was opened, read, or imported.
"""

import mpmath as mp
import sympy as sp

mp.mp.dps = 60

x, y, t = sp.symbols('x y t', real=True)
f = sp.Function('f')

print("=" * 78)
print("PART A: homogeneous solution phi_h(x,y) = e^(x^2/2+xy) solves")
print("        phi_h_x = (x+y)*phi_h  exactly")
print("=" * 78)
phi_h = sp.exp(x**2 / 2 + x * y)
lhs = sp.diff(phi_h, x)
rhs = (x + y) * phi_h
check_A = sp.simplify(lhs - rhs)
print(f"  phi_h_x - (x+y)*phi_h = {check_A}")
assert check_A == 0
print("PASS.")

print()
print("=" * 78)
print("PART B: bounded-branch variation-of-parameters formula solves")
print("        u_x - (x+y)*u = f(x)  exactly, for generic f")
print("=" * 78)
# u_p(x,y) = -e^{x^2/2+xy} * int_x^inf e^{-(t^2/2+ty)} f(t) dt
# Differentiate under the integral (Leibniz rule):
#   d/dx[ -e^{x^2/2+xy} * I(x,y) ] where I(x,y):=int_x^inf e^{-(t^2/2+ty)} f(t) dt
#   = -(x+y)*e^{x^2/2+xy}*I(x,y)  -  e^{x^2/2+xy} * dI/dx
#   dI/dx = -e^{-(x^2/2+xy)} * f(x)      [Leibniz: d/dx int_x^inf g(t)dt = -g(x)]
#   => u_p_x = -(x+y)*e^{x^2/2+xy}*I(x,y) - e^{x^2/2+xy}*(-e^{-(x^2/2+xy)}f(x))
#            = (x+y)*u_p(x,y) + f(x)
# i.e. u_p_x - (x+y)*u_p = f(x).  Verify this symbolically with sympy,
# treating I(x,y) as an abstract Function (the Leibniz rule for its
# x-derivative is a standard, elementary fact used as an input, not
# re-derived by sympy's differentiation of an unevaluated Integral --
# exactly as one would state it by hand).
I_xy = sp.Function('I')(x, y)
u_p = -sp.exp(x**2 / 2 + x * y) * I_xy
u_p_x_formal = sp.diff(u_p, x)   # sympy differentiates I(x,y) symbolically as I_x(x,y)
# substitute the Leibniz fact dI/dx = -exp(-(x^2/2+xy)) * f(x):
Ix_replacement = -sp.exp(-(x**2 / 2 + x * y)) * f(x)
u_p_x_val = u_p_x_formal.subs(sp.Derivative(I_xy, x), Ix_replacement)
u_p_val = u_p.subs(I_xy, I_xy)  # unchanged, just for display symmetry
lhs_B = sp.simplify(u_p_x_val - (x + y) * u_p)
rhs_B = f(x)
check_B = sp.simplify(lhs_B - rhs_B)
print(f"  u_p_x - (x+y)*u_p - f(x)  (using Leibniz dI/dx=-e^-(x^2/2+xy) f(x)) = {check_B}")
assert check_B == 0
print("PASS: the bounded-branch formula solves the inhomogeneous ODE exactly.")

print()
print("  Special case y=0, f(x)=-1: recovers the required reading's own R(x).")
# u_p(x,0) = -e^{x^2/2} * int_x^inf e^{-t^2/2} * (-1) dt = e^{x^2/2} int_x^inf e^{-t^2/2} dt = R(x)
x_num = mp.mpf('1.3')
R_direct = mp.e**(x_num**2 / 2) * mp.quad(lambda tt: mp.e**(-tt**2 / 2), [x_num, mp.inf])
u_p_special = mp.e**(x_num**2 / 2) * mp.quad(lambda tt: mp.e**(-tt**2 / 2), [x_num, mp.inf])
print(f"  R({x_num}) via direct formula        = {R_direct}")
print(f"  u_p({x_num},0) via general B formula = {u_p_special}  (f=-1 case)")
assert mp.fabs(R_direct - u_p_special) < mp.mpf('1e-50')
print("PASS: matches to 50+ digits (trivially -- same formula -- kept as an")
print("      explicit sanity check that the sign convention is the one used")
print("      throughout this front, matching the required reading's R(x)).")

print()
print("=" * 78)
print("PART C: uniqueness -- the two-line elementary proof")
print("=" * 78)
print("""
  Claim: if u1(.,y), u2(.,y) both solve u_x-(x+y)u=f(x) on [x0,inf) and
  both are bounded there, then u1 == u2.

  Proof: d := u1-u2 solves the HOMOGENEOUS equation d_x=(x+y)*d, so by
  Part A, d(x,y) = C(y)*e^{x^2/2+xy} for some C(y). If d is bounded on
  [x0,inf) (difference of two bounded functions), and phi_h(x,y) =
  e^{x^2/2+xy} -> +infinity as x->infinity for EVERY y>=0 (the x^2/2
  term alone already forces this, regardless of the sign or size of the
  xy term), boundedness forces C(y)=0 for every y. Hence d==0. QED.

  This is the FULLY GENERAL, order-independent, completely rigorous
  content of H2's "growth excluded by boundedness" phrase -- it holds
  for ANY order n's chi_n equation (once shown homogeneous, per k01),
  and does not depend on the specific family {P(s)+Q(s)erfcx(...)} that
  the required reading's remark "(proved only within fields where...)"
  seemed to restrict it to. The family-restriction in the ancestor's H2
  statement is NOT needed for this uniqueness argument itself -- it
  would only be needed to separately establish EXISTENCE of a bounded
  solution (via Part B's explicit formula, which converges whenever f
  has at most sub-Gaussian growth, true at every order tested in k01,
  since every f_n encountered there is either identically 0 or built
  from R(x) and finitely many of its derivatives, all bounded).
""")

print("=" * 78)
print("PART D: numerical illustration -- adding a tiny homogeneous")
print("admixture to the bounded branch causes catastrophic blow-up")
print("=" * 78)


def R_mp(xv):
    return mp.e**(xv**2 / 2) * mp.quad(lambda tt: mp.e**(-tt**2 / 2), [xv, mp.inf])


def phi_h_mp(xv, yv=mp.mpf('0')):
    return mp.e**(xv**2 / 2 + xv * yv)


print(f"  {'x':>6} {'R(x) [bounded branch]':>26} {'R(x)+1e-30*phi_h(x)':>26} {'rel. blow-up':>16}")
for xv in [mp.mpf(v) for v in [0, 2, 5, 8, 10, 12, 15]]:
    r = R_mp(xv)
    perturbed = r + mp.mpf('1e-30') * phi_h_mp(xv)
    rel_blowup = mp.fabs(perturbed - r) / mp.fabs(r) if r != 0 else mp.inf
    print(f"  {float(xv):6.1f} {mp.nstr(r, 12):>26} {mp.nstr(perturbed, 12):>26} "
          f"{mp.nstr(rel_blowup, 8):>16}")

print()
print("  Reading: R(x) itself decays like ~1/x for large x (its true")
print("  asymptotic behaviour, R(x) ~ 1/x - 1/x^3 + ...), staying bounded")
print("  and small; the SAME size (1e-30, chosen tiny at x=0) admixture of")
print("  the excluded mode phi_h(x)=e^{x^2/2} overtakes it completely by")
print("  x~12-15 and diverges -- exactly the mechanism that makes")
print("  'boundedness excludes the homogeneous mode' the CORRECT and")
print("  UNIQUE selection principle, not merely a convenient simplification.")
print()
print("ALL PARTS PASS.")
