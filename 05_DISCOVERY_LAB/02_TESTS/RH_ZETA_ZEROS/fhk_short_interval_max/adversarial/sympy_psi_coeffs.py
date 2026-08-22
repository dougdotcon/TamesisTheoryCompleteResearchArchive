"""Symbolic derivation of local Taylor coefficients of
Psi(p) = cos(2*pi*(p**2 - p - 1/16)) / cos(2*pi*p)
around its removable singularities p = 1/4 and p = 3/4.
Output: coefficients of sum_k a_k * (p - p0)**k, k = 0..6.
Run once; coefficients are pasted into rs_zeta_adv.py.
"""
import sympy as sp

p = sp.symbols('p')
Psi = sp.cos(2*sp.pi*(p**2 - p - sp.Rational(1, 16))) / sp.cos(2*sp.pi*p)

for p0 in (sp.Rational(1, 4), sp.Rational(3, 4)):
    ser = sp.series(Psi, p, p0, 7).removeO()
    poly = sp.Poly(sp.expand(ser), p - p0) if False else None
    coeffs = []
    x = sp.symbols('x')
    ser_x = sp.expand(ser.subs(p, p0 + x))
    for k in range(7):
        c = sp.simplify(ser_x.coeff(x, k))
        coeffs.append(sp.nsimplify(c))
    print(f"p0 = {p0}")
    for k, c in enumerate(coeffs):
        print(f"  a{k} = {sp.N(c, 20)}")
    # sanity: numeric value close to p0
    f = sp.lambdify(p, Psi, 'mpmath')
    import mpmath
    mpmath.mp.dps = 30
    approx = sum(sp.N(c, 20) * sp.Float(0.01)**k for k, c in enumerate(coeffs))
    print(f"  check Psi(p0+0.01) direct = {f(float(p0) + 0.01)}")
    print(f"  check Taylor(p0+0.01)     = {approx}")
