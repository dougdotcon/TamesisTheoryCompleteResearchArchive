import sympy as sp
import pickle, time

n = sp.Symbol('n')

with open('k4_S_upper.pkl','rb') as f:
    S = pickle.load(f)

t0=time.time()
content, facs = sp.factor_list(S, n)
t1=time.time()
print(f"factor_list in {t1-t0:.2f}s")
# find the degree-216 factor
B = None
for fac, mult in facs:
    dpoly = sp.Poly(fac, n)
    if dpoly.degree() == 216:
        B = fac
        print("Found B, mult=", mult)
    else:
        print("other factor deg=", dpoly.degree(), "mult=", mult)

assert B is not None
Bpoly = sp.Poly(B, n)
print("B irreducible over QQ:", Bpoly.is_irreducible)

t0=time.time()
roots_B = Bpoly.real_roots()
t1=time.time()
print(f"real_roots(B) in {t1-t0:.2f}s: {len(roots_B)} real roots")
roots_num = sorted(sp.N(r,20) for r in roots_B)
for r in roots_num:
    print("  ", r)
print("\nLargest real root of B:", roots_num[-1])
