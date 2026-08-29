"""
Quick scan: for the LOWER-target S2(n) (which failed the B=8,10 shift
certificate), try a range of larger integer bounds B to find where the
shifted polynomial's coefficients finally become uniform in sign
(proving no real root exceeds B) -- cheap (each shift ~0.05-0.1s), so
scan broadly. This will help diagnose whether K=6 has a K=4-style
"wrinkle" (a genuine but harmless large spurious root in this specific
resultant branch) and, if so, roughly where it lives.
"""
import sympy as sp
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
interior = [c for c in crit if 0 < sp.N(c) < 1]
x6star = interior[0]
M6 = sp.simplify(g6.subs(x, x6star))
minpoly_M6 = sp.minimal_polynomial(M6, t)

F1 = sp.expand(sp.diff(Num6, x))
F2 = sp.expand(m * Dn6 - n * Num6)
t0 = time.time()
R = sp.expand(sp.resultant(F1, F2, x))
print("R computed in", round(time.time() - t0, 2), "s", flush=True)

t0 = time.time()
S2 = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_M6.subs(t, -m), m)))
print("S2 computed in", round(time.time() - t0, 2), "s, degree", sp.Poly(S2, n).degree(), flush=True)
S2poly = sp.Poly(S2, n)

print("\nScanning shift bounds B to find where certificate clears:", flush=True)
for B in [12, 15, 20, 25, 30, 40, 50, 60, 65, 70, 80, 100, 150, 200, 300]:
    t0 = time.time()
    shifted = S2poly.shift(B)
    coeffs = shifted.all_coeffs()
    signs = set(sp.sign(c) for c in coeffs if c != 0)
    el = time.time() - t0
    status = "CLEARED (no root > B)" if len(signs) <= 1 else "still mixed"
    print(f"  B={B:4d}: signs={signs}  {status}  ({el:.3f}s)", flush=True)
    if len(signs) <= 1:
        print(f"\n  => First clearing bound found: B={B}. The true largest real root")
        print(f"     of S2(n) is somewhere below {B} (this bound is an upper bound,")
        print(f"     not necessarily tight).")
        break
