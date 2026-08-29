"""
INDEPENDENT REFEREE re-derivation of g_5(x), M_5, and the resultant-
elimination thresholds for K=5, starting from the D5 formula this
referee already independently re-derived and cross-checked against a
fresh brute force (my_D5_derivation.py, my_bruteforce_def4_k5.py).

Everything below is typed fresh; no code copied from the target's
k5_exact_closure.py (which was read only for its PROSE claims/numbers).
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

print("=" * 70)
print("STEP 1: g5(x) extraction")
print("=" * 70)
F5n = sp.cancel(D5.subs(k, n * x))
F5cont = sp.expand(1 - (1 - x**2)**5)
Delta5 = sp.cancel(F5n - F5cont)
Num5 = sp.expand(sp.cancel(Delta5 * Dn5))
Npoly = sp.Poly(Num5, n)
print("deg_n Num5 =", Npoly.degree(), "  deg_n Dn5 =", sp.Poly(Dn5, n).degree())
g5 = sp.expand(Npoly.coeff_monomial(n**9))
print("g5(x) =", g5)
g5_factored_claim = sp.expand(5 * x * (x - 1)**4 * (x + 1)**3 * (2 * x**2 - x + 1))
diff_g5 = sp.simplify(g5 - g5_factored_claim)
print("Claimed factorization diff:", diff_g5)
assert diff_g5 == 0
print("g5 factorization CONFIRMED (independent).")

# independent sign check on [0,1]
print()
print("Sign check g5(x)>=0 on [0,1]: factor 2x^2-x+1 discriminant =",
      sp.discriminant(2*x**2 - x + 1, x), "(negative => always positive)")
assert sp.discriminant(2*x**2 - x + 1, x) < 0
for xv in [sp.Rational(i, 10) for i in range(0, 11)]:
    val = g5.subs(x, xv)
    assert val >= 0, (xv, val)
print("g5(x) >= 0 sampled densely on [0,1]. PASSED.")
assert g5.subs(x, 0) == 0 and g5.subs(x, 1) == 0
print("g5(0)=g5(1)=0 CONFIRMED.")

print()
print("=" * 70)
print("STEP 2: g5'(x) factorization, x5*, M5, minimal polynomial")
print("=" * 70)
g5p = sp.expand(sp.diff(g5, x))
g5p_factored = sp.factor(g5p)
print("g5'(x) factored (independent) =", g5p_factored)
claim_factor = sp.expand(5 * (x - 1)**3 * (x + 1)**2 * (20*x**4 - 7*x**3 + x**2 + 3*x - 1))
diff_g5p = sp.simplify(g5p - claim_factor)
print("Claimed g5' factorization diff:", diff_g5p)
assert diff_g5p == 0
print("g5' factorization CONFIRMED (independent).")

quartic = 20*x**4 - 7*x**3 + x**2 + 3*x - 1
irr = sp.Poly(quartic, x).is_irreducible
print("Interior quartic 20x^4-7x^3+x^2+3x-1 irreducible over Q:", irr)
assert irr

crit = sp.Poly(g5p, x).real_roots()
print("All real roots of g5'(x):", [sp.N(c, 15) for c in crit])
interior = [c for c in crit if 0 < sp.N(c) < 1]
assert len(interior) == 1
x5star = interior[0]
M5 = sp.simplify(g5.subs(x, x5star))
print("x5* =", sp.N(x5star, 30))
print("M5  =", sp.N(M5, 30))

minpoly_M5 = sp.minimal_polynomial(M5, t)
print("minimal polynomial of M5 (independent sp.minimal_polynomial call):")
print(" ", minpoly_M5)
assert sp.Poly(minpoly_M5, t).is_irreducible
print("Irreducible over Q: CONFIRMED.")

claimed_minpoly = (1024000000000*t**4 - 887007704239*t**3 - 7821482127360*t**2
                    + 14635525734400*t - 6341787648000)
diff_minpoly = sp.expand(minpoly_M5 - claimed_minpoly)
print("Diff vs target's claimed minimal polynomial:", diff_minpoly)
# minimal polynomials are unique up to sign/scaling by a rational; check
# ratio is a nonzero rational constant if not literally equal
if diff_minpoly != 0:
    ratio = sp.simplify(sp.Poly(minpoly_M5, t).all_coeffs()[0] /
                         sp.Poly(claimed_minpoly, t).all_coeffs()[0])
    print("  (leading-coeff ratio, in case of a scaling difference):", ratio)
assert diff_minpoly == 0
print("Minimal polynomial of M5 MATCHES target's claim EXACTLY (independent).")

# High precision cross-check via mpmath, no sympy symbolic machinery
import mpmath as mp
mp.mp.dps = 50
g5_mpf = lambda xv: 5*xv*(xv-1)**4*(xv+1)**3*(2*xv**2 - xv + 1)
g5p_mpf = lambda xv: mp.diff(g5_mpf, xv)
x5_mp = mp.findroot(g5p_mpf, mp.mpf('0.31'))
M5_mp = g5_mpf(x5_mp)
print()
print("mpmath cross-check (zero sympy symbolic machinery, 50 dps):")
print("  x5* (mpmath) =", x5_mp)
print("  M5  (mpmath) =", M5_mp)
M5_sp_str = str(sp.N(M5, 50))
print("  M5  (sympy)  =", M5_sp_str)
assert abs(M5_mp - mp.mpf(M5_sp_str)) < mp.mpf('1e-40')
print("  mpmath and sympy M5 AGREE to 40+ digits. PASSED.")

print()
print("=" * 70)
print("STEP 3: boundary threshold n0_boundary (h5(n,1) = M5 crossing)")
print("=" * 70)
h5 = sp.cancel(n * Delta5)
h1 = sp.factor(sp.simplify(h5.subs(x, 1)))
print("h5(n,1) =", h1)
assert sp.simplify(h1 - 120/((n-1)*(n-2)*(n-3)*(n-4))) == 0
thresh_poly = sp.expand((n-1)*(n-2)*(n-3)*(n-4)*M5 - 120)
roots = sp.solve(sp.Eq(thresh_poly, 0), n)
real_roots_num = sorted(sp.N(r, 20) for r in roots if r.is_real)
print("real roots of boundary-crossing equation:", real_roots_num)
n0_boundary = max(real_roots_num)
print("n0_boundary =", n0_boundary)
assert 6 < n0_boundary < 7
print("CONFIRMED: 6 < n0_boundary < 7 (matches claimed ~6.2962).")

print()
print("=" * 70)
print("STEP 4: interior resultant elimination -- UPPER bound (target m=M5)")
print("=" * 70)
F1 = sp.expand(sp.diff(Num5, x))
F2 = sp.expand(m * Dn5 - n * Num5)
t0 = time.time()
R = sp.expand(sp.resultant(F1, F2, x))
print(f"Res_x(F1,F2) computed in {time.time()-t0:.1f}s, degree in n:",
      sp.Poly(R, n).degree(), " degree in m:", sp.Poly(R, m).degree())

minpoly_m = minpoly_M5.subs(t, m)
t0 = time.time()
S_upper = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_m, m)))
print(f"Res_m(R, minpoly(M5)) computed in {time.time()-t0:.1f}s")
t0 = time.time()
content, factors = sp.factor_list(S_upper, n)
print(f"factor_list computed in {time.time()-t0:.1f}s")
for f, mult in factors:
    print("  factor deg:", sp.Poly(f, n).degree(), " mult:", mult)
biggest = max(factors, key=lambda fm: sp.Poly(fm[0], n).degree())[0]
Bp = sp.Poly(biggest, n)
t0 = time.time()
roots_upper = Bp.real_roots()
print(f"real_roots computed in {time.time()-t0:.1f}s, count={len(roots_upper)}")
max_upper = max(sp.N(r, 20) for r in roots_upper)
print("Largest real root (upper interior threshold):", max_upper)
assert max_upper < n0_boundary
print("CONFIRMED: interior upper threshold < boundary threshold n0_boundary.")

print()
print("=" * 70)
print("STEP 5: interior resultant elimination -- LOWER bound (target m=-M5)")
print("=" * 70)
minpoly_negm = minpoly_M5.subs(t, -m)
t0 = time.time()
S_lower = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_negm, m)))
print(f"Res_m(R, minpoly(-M5)) computed in {time.time()-t0:.1f}s")
t0 = time.time()
content2, factors2 = sp.factor_list(S_lower, n)
print(f"factor_list computed in {time.time()-t0:.1f}s")
for f, mult in factors2:
    print("  factor deg:", sp.Poly(f, n).degree(), " mult:", mult)
biggest2 = max(factors2, key=lambda fm: sp.Poly(fm[0], n).degree())[0]
Bp2 = sp.Poly(biggest2, n)
t0 = time.time()
roots_lower = Bp2.real_roots()
print(f"real_roots computed in {time.time()-t0:.1f}s, count={len(roots_lower)}")
max_lower = max(sp.N(r, 20) for r in roots_lower)
print("Largest real root (lower interior threshold):", max_lower)
assert max_lower < n0_boundary
print("CONFIRMED: interior lower threshold < boundary threshold n0_boundary too.")
print("=> NO K=4-style 'wrinkle' possible: neither interior threshold exceeds")
print("   the boundary threshold, so the boundary term alone pins n0, and")
print("   there is no out-of-domain-branch inflation issue to diagnose here.")

print()
print("=" * 70)
print(f"FINAL: n0 = max(boundary, upper_interior, lower_interior) = {n0_boundary}")
print(f"       => smallest integer n0 with the theorem's domain = 7")
print("=" * 70)
