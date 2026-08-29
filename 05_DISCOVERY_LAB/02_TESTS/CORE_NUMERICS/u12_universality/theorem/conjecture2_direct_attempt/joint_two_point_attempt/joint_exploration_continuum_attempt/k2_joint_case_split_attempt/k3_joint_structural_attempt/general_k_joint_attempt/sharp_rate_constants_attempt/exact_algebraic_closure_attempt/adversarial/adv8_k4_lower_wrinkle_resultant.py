"""
Independent, from-scratch investigation of the K=4 lower-bound "wrinkle"
(target Sec 4.5): verify that S2(n)'s spurious largest real root (~64.768)
corresponds to the OTHER real root of minpoly(-M4) (not -M4 itself),
realized at some x outside [0,1].

This script does NOT reuse the target's R(n,m) computation results by
reading them from target's files -- it recomputes independently using
my own Nx,Dn from adv5 (already independently re-derived from THEOREM.md
D4 by hand). It DOES reuse the previously-computed R(n,m) pickle from
adv6 (my own independent resultant, computed before I read the target's
script), to avoid re-doing the ~1s resultant step, since I already
verified that computation matches the target's numbers to full precision.
"""
import sympy as sp
import pickle, time

n, x, m, t = sp.symbols('n x m t')

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_R_upper.pkl','rb') as f:
    R = pickle.load(f)

M4_minpoly = 35831808*t**4 - 49852544*t**3 - 220711113*t**2 + 556322688*t - 274710528

print("="*70)
print("Step A: real roots of M4's own minimal quartic (both real roots)")
print("="*70)
mp_poly = sp.Poly(M4_minpoly, t)
mp_roots = mp_poly.real_roots()
mp_roots_num = sorted(sp.N(r, 25) for r in mp_roots)
print("real roots of minpoly_M4(t):", mp_roots_num)
M4_val = mp_roots_num[-1]  # the larger one should be M4 itself (~0.7087)... check
print("(expect one of these ~0.7087 = M4, the other some other real conjugate)")

print("\n" + "="*70)
print("Step B: minpoly(-M4)(m) = minpoly_M4(-m); its real roots")
print("="*70)
negM4_minpoly = sp.expand(M4_minpoly.subs(t, -m))
negmp_poly = sp.Poly(negM4_minpoly, m)
negmp_roots = negmp_poly.real_roots()
negmp_roots_num = sorted(sp.N(r,25) for r in negmp_roots)
print("real roots of minpoly(-M4)(m):", negmp_roots_num)
print("(expect -M4 ~ -0.7087 and the OTHER conjugate, positive, ~+2.898 per target's claim)")

print("\n" + "="*70)
print("Step C: independently build S2(n) = Res_m(R(n,m), minpoly(-M4)(m))")
print("="*70)
t0=time.time()
S2 = sp.resultant(sp.Poly(R, m), sp.Poly(negM4_minpoly, m))
t1=time.time()
print(f"S2(n) computed in {t1-t0:.2f}s, degree {sp.degree(S2,n)}")

t0=time.time()
content2, facs2 = sp.factor_list(S2, n)
t1=time.time()
print(f"factor_list in {t1-t0:.2f}s")
big2 = max(facs2, key=lambda fm: sp.Poly(fm[0], n).degree())
print("largest-degree factor: deg=", sp.Poly(big2[0],n).degree(), "mult=", big2[1])
for fac,mult in facs2:
    print("  deg=", sp.Poly(fac,n).degree(), "mult=",mult)

t0=time.time()
roots2 = sp.Poly(big2[0], n).real_roots()
t1=time.time()
print(f"real_roots in {t1-t0:.2f}s: {len(roots2)} roots")
roots2_num = sorted(sp.N(r,20) for r in roots2)
for r in roots2_num:
    print("  ", r)
n_spurious = roots2_num[-1]
print("\nLargest real root of S2's genuine factor:", n_spurious)
