"""
K6-EXACT-CLOSURE-ATTEMPT. Exact per-integer-n patch across the gap
[8, 40] -- exactly the K=4 predecessor's own "Step 7" recipe, applied
here because the lower-bound resultant elimination's S2(n) has a
genuine (non-spurious, sign-change-confirmed) real root between n=34
and n=35, analogous to K=4's own lower-bound "wrinkle" (there, a root
near n=64.77; here, near n=34.x -- smaller in magnitude but the same
qualitative phenomenon: an interior-threshold resultant root that does
NOT correspond to an actual violation of the theorem, confirmed here by
DIRECT exact evaluation of min_x h6(n,x) at every integer n in the gap).

For every integer n=8,...,42 (comfortably past the confirmed root
location in (34,35)): compute min_x h6(n,x) EXACTLY (Poly(...).real_roots()
on the degree-12 polynomial dh6/dx, evaluated at the fixed integer n --
a small, fast computation, not the full symbolic-n resultant machinery)
and confirm it exceeds -M6.
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
x6star = [c for c in crit if 0 < sp.N(c) < 1][0]
M6 = sp.simplify(g6.subs(x, x6star))
print("M6 =", sp.N(M6, 30))
negM6 = -M6


def sup_inf_h6_exact(nv):
    Numn = Num6.subs(n, sp.Rational(nv))
    Dnn = Dn6.subs(n, sp.Rational(nv))
    hx = sp.expand(sp.Rational(nv) * Numn / Dnn)
    hpoly = sp.Poly(hx, x)
    dpoly = hpoly.diff(x)
    crit_pts = sp.Poly(dpoly, x).real_roots()
    cand = [c for c in crit_pts if 0 <= sp.N(c) <= 1] + [sp.Integer(0), sp.Integer(1)]
    vals = [(c, hpoly(c)) for c in cand]
    hi = max(vals, key=lambda cv: sp.N(cv[1]))
    lo = min(vals, key=lambda cv: sp.N(cv[1]))
    return hi, lo


t_start = time.time()
all_ok = True
worst_margin = None
worst_n = None
for nv in range(8, 43):
    hi, lo = sup_inf_h6_exact(nv)
    hi_ok = sp.N(hi[1], 30) <= sp.N(M6, 30)
    lo_ok = sp.N(lo[1], 30) >= sp.N(negM6, 30)
    margin = sp.N(lo[1] - negM6, 15)
    if worst_margin is None or margin < worst_margin:
        worst_margin = margin
        worst_n = nv
    ok = hi_ok and lo_ok
    all_ok = all_ok and ok
    print(f"  n={nv:3d}: max_x h6={sp.N(hi[1],18)} (<=M6:{hi_ok})   "
          f"min_x h6={sp.N(lo[1],18)} (>=-M6:{lo_ok})   margin={float(margin):.6f}   OK={ok}",
          flush=True)

print(f"\nTotal elapsed: {time.time()-t_start:.1f}s")
print(f"ALL n=8..42 OK: {all_ok}")
print(f"Worst (smallest) margin: {worst_margin} at n={worst_n}")
assert all_ok, "VIOLATION FOUND in exact patch range!"
print("\nCONFIRMED: zero violations of h6(n,x)>=-M6 across the exact patch")
print("range n=8..42 -- comfortably covers and exceeds the confirmed")
print("S2(n) sign-change location (34,35), confirming that root is an")
print("extraneous/out-of-domain-branch artifact of the resultant")
print("elimination (as at K=4), NOT a genuine violation of the theorem.")
