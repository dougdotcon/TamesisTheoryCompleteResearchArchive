#!/usr/bin/env python3
"""
r06_asymptotic_derivation.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Machine verification of every ALGEBRAIC step in this front's matched-
asymptotics derivation of

    Pi(c) = sqrt(pi/(2c)) - 2/c + O(c^{-3/2}) ,

i.e. (in scaled variables x = s sqrt(c), y = g sqrt(c), eps = c^{-1/2},
y(eps) := Pi * sqrt(2c/pi) = 1 - 2*sqrt(2/pi)*eps + O(eps^2)).

The derivation itself (prose in ATTEMPT.md SS4) is heuristic at exactly two
points (the smoothness/boundedness assumptions behind the Watson expansion
and behind the uniqueness-of-bounded-solution arguments); everything else is
algebra, verified here with sympy:

 V1. THE EXACT REDUCTION  W = Psi - eps * dPsi/dx :
     from (E1) Psi_x = (x+y) Psi - I  and (E3) W = Psi(1-eps(x+y)) + eps I,
     where I(x,y) = int_0^y Phi dy'.
 V2. The scaled mode-E equation (E1) itself from the unscaled PDE of record
     dPsi/ds = c[Psi - W].
 V3. The Watson/Laplace kernel expansion used to expand
     (1/eps) int_0^y e^{-v/eps} G(x+v, y-v) dv  to O(eps^2), on a generic
     bivariate polynomial G (exact, term-by-term).
 V4. R(x) := sqrt(pi/2) erfcx(x/sqrt 2) satisfies R' = xR - 1, R(inf)=0.
 V5. int_0^inf e^{-x^2/2} R(x) dx = 1  (exact).
 V6. inner-layer profile p(x,z) = (1-e^{-z}) R(x) satisfies
     p_x = x p - (1 - e^{-z}), p(x,0)=0; layer deficit
     delta(x) = int_0^inf [R - p] dz = R(x).
 V7. order-eps^2 outer equation psi2' = x psi2 + 2R has bounded solution
     with psi2(0) = -2 int_0^inf e^{-s^2/2} R ds = -2.
 V8. the y-independence consistency: psi(x) with psi' = x psi + h(x)
     satisfies psi_x = (x+y)psi - int_0^y psi dy' + h identically in y.

Deterministic; no randomness.
"""

import sympy as sp

ok_all = True


def report(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(f"  {name}: {'OK' if cond else 'FAIL'}")


x, y, v, z, s, g, eps, c = sp.symbols('x y v z s g epsilon c', positive=True)

print("V1: exact reduction W = Psi - eps*Psi_x")
Psi = sp.Function('Psi')(x, y)
I = sp.Function('I')(x, y)
# (E1):  Psi_x = (x+y) Psi - I  =>  I = (x+y) Psi - Psi_x
I_sub = (x + y) * Psi - sp.diff(Psi, x)
W = Psi * (1 - eps * (x + y)) + eps * I_sub
report("W - (Psi - eps Psi_x) == 0", sp.simplify(W - (Psi - eps * sp.diff(Psi, x))) == 0)

print("V2: scaled mode-E equation from dPsi/ds = c[Psi - W]")
# unscaled: Psi_s = c Psi - c W,  W = int_0^g Phi dg' + (1-s-g) Psi
# with s = eps x, g = eps y, eps = 1/sqrt(c):  d/ds = sqrt(c) d/dx,
# int_0^g Phi dg' = eps * int_0^y Phi dy'  (denoted eps*Iy)
Psi_f = sp.Function('Psi')(x, y)
Iy = sp.Function('I')(x, y)
lhs = sp.sqrt(c) * sp.diff(Psi_f, x)
Wu = Iy / sp.sqrt(c) + (1 - (x + y) / sp.sqrt(c)) * Psi_f
rhs = c * Psi_f - c * Wu
scaled = sp.expand(lhs - rhs)          # should equal sqrt(c) * [Psi_x - ((x+y)Psi - I)]
target = sp.sqrt(c) * (sp.diff(Psi_f, x) - ((x + y) * Psi_f - Iy))
report("Psi_x = (x+y)Psi - I (exact, all c)", sp.simplify(scaled - target) == 0)

print("V3: Watson expansion of the renewal kernel on generic polynomial G")
# G(x+v, y-v) expanded; (1/eps) int_0^inf e^{-v/eps} v^n dv = n! eps^n
a = sp.IndexedBase('a')
N = 5
G = sum(a[i, j] * x**i * y**j for i in range(N) for j in range(N))
Gs = G.subs([(x, x + v), (y, y - v)], simultaneous=True)
Gser = sp.expand(Gs)
# exact kernel integral, term by term in v (up to needed order), minus the
# exponentially small upper-limit terms (dropped for y >> eps)
poly = sp.Poly(Gser, v)
integral = sum(coeff * sp.factorial(m) * eps**m
               for m, coeff in [(mon[0], poly.coeff_monomial(v**mon[0]))
                                for mon in poly.monoms()])
Gx = sp.diff(G, x)
Gy = sp.diff(G, y)
claim = (G + eps * (Gx - Gy) + eps**2 * (sp.diff(G, x, 2) - 2 * sp.diff(Gx, y)
         + sp.diff(G, y, 2)))
diff = sp.expand(integral - claim)
# difference must be O(eps^3)
diff_low = sp.Poly(diff, eps)
low_orders = [diff_low.coeff_monomial(eps**k) for k in range(3)]
report("kernel expansion exact to O(eps^2)",
       all(sp.simplify(t) == 0 for t in low_orders))

print("V4: R' = xR - 1 and R -> 0")
R = sp.sqrt(sp.pi / 2) * sp.exp(x**2 / 2) * sp.erfc(x / sp.sqrt(2))
report("R' - (xR - 1) == 0", sp.simplify(sp.diff(R, x) - (x * R - 1)) == 0)
report("R(inf) = 0", sp.limit(R, x, sp.oo) == 0)

print("V5: int_0^inf e^{-x^2/2} R dx = 1")
val = sp.integrate(sp.exp(-x**2 / 2) * R, (x, 0, sp.oo))
report("integral == 1", sp.simplify(val - 1) == 0)

print("V6: inner layer p=(1-e^{-z})R solves p_x = xp - (1-e^{-z}); delta=R")
p = (1 - sp.exp(-z)) * R
report("p_x - (x p - (1-e^{-z})) == 0",
       sp.simplify(sp.diff(p, x) - (x * p - (1 - sp.exp(-z)))) == 0)
report("p(x,0) == 0", sp.simplify(p.subs(z, 0)) == 0)
delta = sp.integrate(R - p, (z, 0, sp.oo))
report("delta == R", sp.simplify(delta - R) == 0)

print("V7: psi2(0) = -2")
sig = sp.Symbol('sigma', positive=True)
Rs = sp.sqrt(sp.pi / 2) * sp.exp(sig**2 / 2) * sp.erfc(sig / sp.sqrt(2))
psi2_0 = -sp.integrate(sp.exp(-sig**2 / 2) * 2 * Rs, (sig, 0, sp.oo))
report("psi2(0) == -2", sp.simplify(psi2_0 + 2) == 0)
# and the bounded-branch solution formula solves the ODE:
X = sp.Symbol('X', positive=True)
h = sp.Function('h')
psi2 = -sp.exp(X**2 / 2) * sp.Integral(sp.exp(-sig**2 / 2) * h(sig),
                                       (sig, X, sp.oo))
ode_resid = sp.simplify(sp.diff(psi2.doit(), X) - X * psi2.doit()
                        - h(X)) if False else None
# closed form of the bounded branch: psi2(X) = -2 + 2*X*R(X)
# (obtained by evaluating -e^{X^2/2} int_X^inf e^{-s^2/2} 2R(s) ds using
#  int_a^inf erfc = e^{-a^2}/sqrt(pi) - a*erfc(a)); verify ODE + limits:
RX = sp.sqrt(sp.pi / 2) * sp.exp(X**2 / 2) * sp.erfc(X / sp.sqrt(2))
psi2R = -2 + 2 * X * RX
report("psi2' - (X psi2 + 2R) == 0",
       sp.simplify(sp.diff(psi2R, X) - X * psi2R - 2 * RX) == 0)
report("psi2(0) == -2 (closed form)", psi2R.subs(X, 0) == -2)
report("psi2(inf) == 0 (bounded branch)", sp.limit(psi2R, X, sp.oo) == 0)
# and the closed form matches the integral representation (V7 value above
# already checked psi2(0) = -2 from the integral directly)

print("V8: y-independent psi solves the nonlocal outer equation identically")
psi = sp.Function('psi')(x)
hh = sp.Function('h')(x)
# psi' = x psi + h  =>  RHS of nonlocal eq: (x+y)psi - int_0^y psi dy' + h
rhs_nl = (x + y) * psi - y * psi + hh
report("(x+y)psi - y*psi + h == x*psi + h == psi'",
       sp.simplify(rhs_nl - (x * psi + hh)) == 0)

print("V9: third order -- inner Phi correction and integrated source B(z)")
# Phi_in = e^{-z} + eps*R*[1 - e^{-z} - z e^{-z}] + O(eps^2):
conv = sp.integrate(sp.exp(-sp.Symbol('w', positive=True))
                    * (1 - sp.exp(-(z - sp.Symbol('w', positive=True)))),
                    (sp.Symbol('w', positive=True), 0, z))
report("int_0^z e^{-w} p1(z-w)/R dw == 1 - e^{-z} - z e^{-z}",
       sp.simplify(conv - (1 - sp.exp(-z) - z * sp.exp(-z))) == 0)
Bz = sp.integrate(1 - sp.exp(-z) - z * sp.exp(-z), (z, 0, z))
report("B(z) == z - 2 + 2e^{-z} + z e^{-z}",
       sp.simplify(Bz - (z - 2 + 2 * sp.exp(-z) + z * sp.exp(-z))) == 0)

print("V10: order-eps^2 inner equation p2_x = x p2 + z p1 - R B(z)")
m = 1 - (1 + z) * sp.exp(-z)
psi2x = 2 * x * R - 2          # psi2 in variable x
p2 = m * psi2x
src = z * (1 - sp.exp(-z)) * R - R * (z - 2 + 2 * sp.exp(-z) + z * sp.exp(-z))
report("source == 2R[1-(1+z)e^{-z}]",
       sp.simplify(src - 2 * R * m) == 0)
report("p2_x - (x p2 + 2R m) == 0",
       sp.simplify(sp.diff(p2, x) - (x * p2 + 2 * R * m)) == 0)
report("p2(x,0) == 0", sp.simplify(p2.subs(z, 0)) == 0)
report("p2 -> psi2 as z->inf (matching)", sp.limit(m, z, sp.oo) == 1)

print("V11: delta2 = int_0^inf (psi2 - p2) dz = 2 psi2, and h3 = 7 R'")
d2int = sp.integrate(psi2x - p2, (z, 0, sp.oo))
report("delta2 == 2 psi2", sp.simplify(d2int - 2 * psi2x) == 0)
h3 = psi2x + sp.diff(R, x) + 2 * psi2x   # psi2 + psi1' + delta2
report("h3 == 7 R' == 7(xR - 1)",
       sp.simplify(h3 - 7 * (x * R - 1)) == 0)

print("V12: psi3(0) = -int_0^inf e^{-s^2/2} 7R' ds = (7/2) sqrt(pi/2)")
val3 = -sp.integrate(sp.exp(-sig**2 / 2)
                     * 7 * (sig * Rs - 1), (sig, 0, sp.oo))
report("psi3(0) == (7/2)sqrt(pi/2)",
       sp.simplify(val3 - sp.Rational(7, 2) * sp.sqrt(sp.pi / 2)) == 0)

print("V13: extraction telescoping (1+eps D+eps^2 D^2+...)(1-eps D)Psi = Psi")
# for y-independent Psi(x): D = d/dx; verify to eps^3 on generic f(x)
f = sp.Function('f')(x)
Ser = sum(eps**n * sp.diff(f - eps * sp.diff(f, x), x, n) for n in range(4))
dd = sp.expand(Ser - f)
pol = sp.Poly(dd, eps)
report("telescopes to O(eps^4)",
       all(sp.simplify(pol.coeff_monomial(eps**k)) == 0 for k in range(4)))

print()
print("Assembled result:")
print("  Pi(c) = sqrt(pi/(2c)) - 2/c + (7/2)*sqrt(pi/2)*c^{-3/2} + O(c^-2)")
print("  y(eps) := Pi*sqrt(2c/pi) = 1 - 2*sqrt(2/pi)*eps + (7/2)*eps^2 + O(eps^3)")
print(f"ALL: {'PASS' if ok_all else 'FAIL'}")
