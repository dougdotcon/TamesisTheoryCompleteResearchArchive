"""
K6-EXACT-CLOSURE-ATTEMPT. Get precise (many-digit) values for both
interior resultant thresholds via exact-arithmetic bisection directly on
S(n)/S2(n) (sign of an exact rational evaluation -- cheap, no root
isolation), now that the shift-certificate approach (k6_shift_bound.py,
k6_shift_scan.py) has already established rigorous bounds:
  - S(n) [upper target]: NO real root exceeds 8 (shift certificate at
    B=8, immediate). We bisect DOWN from 8 to find where S changes sign,
    to report the actual threshold value (for documentation parity with
    K=2..5's own reported numbers), and to independently confirm the
    upper bound is comfortably small (matching the established pattern
    of interior thresholds << boundary threshold, except this front's
    own lower-target wrinkle).
  - S2(n) [lower target]: sign change confirmed exactly between n=34
    and n=35 (k6_S2_integer_evals.log). Bisect within (34,35) for a
    precise decimal value.
"""
import sympy as sp
from fractions import Fraction
import time

n, x, k, m, t = sp.symbols('n x k m t', real=True)
K = 6

bracket6_str = '''
-k**10 + 25*k**9 + 6*k**8*n**2 - 45*k**8*n - 270*k**8 - 96*k**7*n**2 + 760*k**7*n + 1650*k**7
- 15*k**6*n**4 + 195*k**6*n**3 - 9*k**6*n**2 - 5380*k**6*n - 6273*k**6
+ 135*k**5*n**4 - 1875*k**5*n**3 + 4359*k**5*n**2 + 20734*k**5*n + 15345*k**5
+ 20*k**4*n**6 - 330*k**4*n**5 + 1375*k**4*n**4 + 3600*k**4*n**3 - 22441*k**4*n**2 - 47215*k**4*n - 24080*k**4
- 80*k**3*n**6 + 1440*k**3*n**5 - 7975*k**3*n**4 + 4641*k**3*n**3 + 50821*k**3*n**2 + 64330*k**3*n + 23300*k**3
- 15*k**2*n**8 + 270*k**2*n**7 - 1730*k**2*n**6 + 3435*k**2*n**5 + 7610*k**2*n**4 - 20391*k**2*n**3 - 58916*k**2*n**2 - 50320*k**2*n - 12576*k**2
+ 15*k*n**8 - 310*k*n**7 + 2360*k*n**6 - 7055*k*n**5 + 730*k*n**4 + 20526*k*n**3 + 33716*k*n**2 + 20016*k*n + 2880*k
+ 6*n**10 - 105*n**9 + 720*n**8 - 2375*n**7 + 3384*n**6 - 10*n**5 - 1860*n**4 - 6696*n**3 - 7440*n**2 - 2880*n
'''
bracket6 = sp.sympify(bracket6_str, locals={'n': n, 'k': k})
Dn6 = n ** 7 * (n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)
D6_formula = k * (k + 1) * bracket6 / Dn6

F6n = sp.cancel(D6_formula.subs(k, n * x))
F6_cont = sp.expand(1 - (1 - x ** 2) ** K)
Delta6 = sp.cancel(F6n - F6_cont)
Num6 = sp.expand(sp.cancel(Delta6 * Dn6))

Npoly_n = sp.Poly(Num6, n)
deg_N_n = Npoly_n.degree()
g6 = sp.expand(Npoly_n.coeff_monomial(n ** deg_N_n))
g6p = sp.expand(sp.diff(g6, x))
crit = sp.Poly(g6p, x).real_roots()
x6star = [c for c in crit if 0 < sp.N(c) < 1][0]
M6 = sp.simplify(g6.subs(x, x6star))
minpoly_M6 = sp.minimal_polynomial(M6, t)

F1 = sp.expand(sp.diff(Num6, x))
F2 = sp.expand(m * Dn6 - n * Num6)
t0 = time.time()
R = sp.expand(sp.resultant(F1, F2, x))
print("R computed in", round(time.time() - t0, 2), "s", flush=True)

t0 = time.time()
S = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_M6.subs(t, m), m)))
Spoly = sp.Poly(S, n)
print("S (upper) computed in", round(time.time() - t0, 2), "s, degree", Spoly.degree(), flush=True)

t0 = time.time()
S2 = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_M6.subs(t, -m), m)))
S2poly = sp.Poly(S2, n)
print("S2 (lower) computed in", round(time.time() - t0, 2), "s, degree", S2poly.degree(), flush=True)


def sign_at(poly, val):
    return sp.sign(poly.eval(val))


def bisect(poly, lo, hi, iters=60):
    lo = Fraction(lo)
    hi = Fraction(hi)
    slo = sign_at(poly, sp.Rational(lo.numerator, lo.denominator))
    shi = sign_at(poly, sp.Rational(hi.numerator, hi.denominator))
    assert slo != shi, f"no sign change in [{lo},{hi}]: signs {slo},{shi}"
    for i in range(iters):
        mid = (lo + hi) / 2
        smid = sign_at(poly, sp.Rational(mid.numerator, mid.denominator))
        if smid == 0:
            return mid
        if smid == slo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


print("\n--- Bisecting UPPER target S(n) down from 8 to find sign change ---", flush=True)
# find a bracket below 8 where S changes sign (S has no root >=8 per shift cert)
found_bracket = None
for lo_try in [7, 6, 5, 4, 3, 2, 1, 0]:
    s_lo = sign_at(Spoly, lo_try)
    s_hi = sign_at(Spoly, 8)
    if s_lo != s_hi:
        found_bracket = (lo_try, 8)
        break
print("bracket search result:", found_bracket, flush=True)
if found_bracket:
    root_upper = bisect(Spoly, found_bracket[0], found_bracket[1], iters=80)
    print(f"UPPER interior threshold (bisected, 80 iters): {float(root_upper):.20f}")
    print(f"  as Fraction: {root_upper}")

print("\n--- Bisecting LOWER target S2(n) in (34,35) ---", flush=True)
root_lower = bisect(S2poly, 34, 35, iters=80)
print(f"LOWER interior threshold (bisected, 80 iters): {float(root_lower):.20f}")
print(f"  as Fraction: {root_lower}")

with open('k6_precise_thresholds_results.py', 'w') as f:
    f.write(f"root_upper_float = {float(root_upper) if found_bracket else None}\n")
    f.write(f"root_lower_float = {float(root_lower)}\n")
