"""
Follow-up referee check: does S(n)'s "largest real root" claim (4.1433...
for the upper bound, 4.3806... for the lower bound) actually account for
ALL real roots of S(n) -- including the small linear (mult 316) and
degree-3 (mult 4) factors that factor_list also produced -- not just the
single largest-DEGREE factor B(n)?  A degree-3 factor could in principle
have a real root larger than B(n)'s largest real root even though B(n)
has far more roots overall; degree alone doesn't bound root location.
"""
import sympy as sp
import time

n, x, k, m, t = sp.symbols('n x k m t', real=True)

bracket_str = '''
k**8 - 16*k**7 - 5*k**6*n**2 + 30*k**6*n + 106*k**6 + 45*k**5*n**2 - 290*k**5*n - 376*k**5
+ 10*k**4*n**4 - 100*k**4*n**3 + 100*k**4*n**2 + 1100*k**4*n + 769*k**4
- 40*k**3*n**4 + 440*k**3*n**3 - 975*k**3*n**2 - 2074*k**3*n - 904*k**3
- 10*k**2*n**6 + 120*k**2*n**5 - 435*k**2*n**4 + 10*k**2*n**3 + 1885*k**2*n**2 + 2014*k**2*n + 564*k**2
+ 10*k*n**6 - 140*k*n**5 + 635*k*n**4 - 650*k*n**3 - 1410*k*n**2 - 924*k*n - 144*k
+ 5*n**8 - 60*n**7 + 265*n**6 - 490*n**5 + 190*n**4 + 300*n**3 + 360*n**2 + 144*n
'''
bracket = sp.sympify(bracket_str, locals={'n': n, 'k': k})
Dn5 = n**6 * (n - 1) * (n - 2) * (n - 3) * (n - 4)
D5 = k * (k + 1) * bracket / Dn5

F5n = sp.cancel(D5.subs(k, n * x))
F5cont = sp.expand(1 - (1 - x**2)**5)
Delta5 = sp.cancel(F5n - F5cont)
Num5 = sp.expand(sp.cancel(Delta5 * Dn5))

g5 = sp.expand(sp.Poly(Num5, n).coeff_monomial(n**9))
g5p = sp.expand(sp.diff(g5, x))
x5star = [c for c in sp.Poly(g5p, x).real_roots() if 0 < sp.N(c) < 1][0]
M5 = sp.simplify(g5.subs(x, x5star))
minpoly_M5 = sp.minimal_polynomial(M5, t)

F1 = sp.expand(sp.diff(Num5, x))
F2 = sp.expand(m * Dn5 - n * Num5)
R = sp.expand(sp.resultant(F1, F2, x))

for label, mp_expr in [("UPPER (target m=M5)", minpoly_M5.subs(t, m)),
                        ("LOWER (target m=-M5)", minpoly_M5.subs(t, -m))]:
    print("=" * 70)
    print(label)
    print("=" * 70)
    S = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(mp_expr, m)))
    content, factors = sp.factor_list(S, n)
    all_real_roots = []
    for f, mult in factors:
        deg = sp.Poly(f, n).degree()
        rr = sp.Poly(f, n).real_roots()
        rr_num = sorted(sp.N(r, 15) for r in rr)
        print(f"  factor degree={deg} mult={mult}  #real_roots={len(rr)}"
              + (f"  poly={sp.factor(f)}" if deg <= 3 else ""))
        if rr_num:
            print(f"    real roots: {rr_num}")
        all_real_roots.extend(rr_num)
    global_max = max(all_real_roots)
    print(f"\n  GLOBAL largest real root across ALL factors of S(n): {global_max}")
