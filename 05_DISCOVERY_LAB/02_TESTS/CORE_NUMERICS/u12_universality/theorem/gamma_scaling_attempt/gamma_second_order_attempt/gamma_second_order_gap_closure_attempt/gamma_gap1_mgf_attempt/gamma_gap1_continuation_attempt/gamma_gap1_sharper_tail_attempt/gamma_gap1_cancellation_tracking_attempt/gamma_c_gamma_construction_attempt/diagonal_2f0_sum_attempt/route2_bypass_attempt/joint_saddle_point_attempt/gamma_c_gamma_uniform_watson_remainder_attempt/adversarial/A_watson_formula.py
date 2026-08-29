"""
Independent referee re-derivation A: general 2nd-order Watson/Laplace
remainder formula, from scratch (no front code read/imported).

I = int e^{g(t)} dt, unique interior nondegenerate max at t*.
s = t-t*, A=-g''(t*). g(t*+s) = g(t*) - A/2 s^2 + g3/6 s^3 + g4/24 s^4 + O(s^5)
Substitute s = u/sqrt(A):
  g(t*+u/sqrt(A)) - g(t*) = -u^2/2 + e3 u^3 + e4 u^4 + O(u^5/A^{5/2})
  e3 = g3/(6 A^{3/2}),  e4 = g4/(24 A^2)

exp(e3 u^3 + e4 u^4) = 1 + e3 u^3 + e4 u^4 + e3^2/2 u^6 + O(higher)
(cross term e3*e4 u^7 is odd -> integrates to 0 against symmetric Gaussian;
 e3^3 u^9 also odd -> 0; next even contributing term is e4^2 u^8 which is
 higher order than what we keep, and e3^4 u^12 even higher -- both dropped
 as beyond the order we're deriving)

integrate against unit Gaussian measure du e^{-u^2/2}/sqrt(2pi):
 <u^0>=1, <u^3>=0 (odd), <u^4>=3, <u^6>=15
 => bracket = 1 + 3 e4 + (15/2) e3^2
 => Delta = 3 e4 + 15/2 e3^2
substitute back:
 Delta = 3*g4/(24 A^2) + 15/2 * g3^2/(36 A^3)
       = g4/(8A^2) + 5 g3^2/(24 A^3)
"""
import sympy as sp

u = sp.symbols('u', real=True)
e3, e4 = sp.symbols('e3 e4', real=True)
A, g3, g4 = sp.symbols('A g3 g4', positive=True)

print("=== independent re-derivation, from scratch ===")
# exact unit-Gaussian moments via sympy integration (not hardcoded factorial2)
moments = {}
for k in range(0, 8):
    m = sp.integrate(u**k * sp.exp(-u**2/2), (u, -sp.oo, sp.oo)) / sp.sqrt(2*sp.pi)
    moments[k] = sp.nsimplify(sp.simplify(m))
    print(f"  <u^{k}> = {moments[k]}")

# integrand expansion of exp(g(t*+u/sqrtA)-g(t*)) to the order producing
# a Delta of size O(1/A):
# exp(-u^2/2) * exp(e3 u^3 + e4 u^4 + O(u^5 A^{-5/2}))
# expand exp(e3 u^3+e4 u^4) in powers of e3,e4 keeping total "weight"
# (deg in e3 * 1 + deg in e4 * 1) <= ... actually keep all terms whose
# u-power is <=6 AND whose coefficient is not asymptotically higher order
# than e3^2,e4 (i.e. drop e3*e4 (u^7, but also odd->vanishes anyway),
# e4^2 (u^8, higher order in 1/A), e3^3(u^9, odd->vanishes), e3^4 (u^12)).
expr = 1 + e3*u**3 + e4*u**4 + sp.Rational(1,2)*e3**2*u**6
total = 0
for term in sp.Add.make_args(sp.expand(expr)):
    coeff, u_pow = term.as_independent(u)
    # extract exponent
    p = sp.Poly(term, u).monoms()[0][0] if term.has(u) else 0
    total += coeff * moments.get(p, sp.nan)
total = sp.expand(total)
print("\nbracket [1+Delta] =", total)
Delta_formal = sp.expand(total - 1)
print("Delta (in eps3,eps4) =", Delta_formal)

Delta_explicit = sp.simplify(Delta_formal.subs({e3: g3/(6*A**sp.Rational(3,2)), e4: g4/(24*A**2)}))
print("\nDelta(A,g3,g4) =", Delta_explicit)
claim = g4/(8*A**2) + 5*g3**2/(24*A**3)
print("claimed closed form g4/(8A^2) + 5 g3^2/(24 A^3)")
print("difference:", sp.simplify(Delta_explicit - claim), " (expect 0)")

print("\n=== external validation: Stirling series for Gamma(z+1) ===")
z, tt = sp.symbols('z tt', positive=True)
g_gamma = z*sp.log(tt) - tt
gpp = sp.diff(g_gamma, tt, 2)
gppp = sp.diff(g_gamma, tt, 3)
gpppp = sp.diff(g_gamma, tt, 4)
tstar = z
Aval = sp.simplify(-gpp.subs(tt, tstar))
g3val = sp.simplify(gppp.subs(tt, tstar))
g4val = sp.simplify(gpppp.subs(tt, tstar))
print("A =", Aval, " g3 =", g3val, " g4 =", g4val)
Delta_gamma = sp.simplify(claim.subs({A: Aval, g3: g3val, g4: g4val}))
print("Delta computed =", Delta_gamma)
print("difference from known 1/(12z):", sp.simplify(Delta_gamma - sp.Rational(1,12)/z), " (expect 0)")
