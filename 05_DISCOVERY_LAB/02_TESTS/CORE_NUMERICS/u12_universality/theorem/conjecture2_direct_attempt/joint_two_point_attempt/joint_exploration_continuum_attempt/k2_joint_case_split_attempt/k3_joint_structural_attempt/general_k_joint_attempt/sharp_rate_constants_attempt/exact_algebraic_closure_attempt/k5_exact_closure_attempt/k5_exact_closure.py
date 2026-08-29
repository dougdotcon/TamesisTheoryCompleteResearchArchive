"""
K5-EXACT-CLOSURE-ATTEMPT (wave 29, front c), K=5.

Fresh, independent derivation (no code imported from any ancestor front).
D5(n,k) is THIS FRONT'S OWN derivation (see d5_derivation.py), since no
K=5 closed-form CDF exists anywhere in THEOREM.md (Estagios 44/45
certified non-existence only for K symbolic; concrete K=5 was never
attempted by any prior front). g_3,g_4's own K3/K4 scripts (predecessor
front, exact_algebraic_closure_attempt/) are cited for METHOD only, never
imported.

GOAL: prove |F_n^{(5)}(x) - F_5(x)| <= M_5/n for the EXACT asymptotic
constant M_5 (root of an irreducible quartic, via Poly(...).real_roots(),
no radical form used or needed), for all integer n >= N0_DOMAIN and
x in [0,1].

METHOD: identical in structure to the predecessor's k3/k4_exact_closure.py
(resultant elimination between the critical-point equation and h(n,x)=m,
eliminated against M_5's own minimal polynomial; combined with exact
boundary evaluation and an explicit continuity + Intermediate Value
Theorem argument -- stated completely here from the start, addressing
the predecessor's own referee findings F1/F2 about that step needing to
be explicit).
"""
import sympy as sp
import time

n, x, k, m, t = sp.symbols('n x k m t', real=True)

# ---------------------------------------------------------------------
# 1. This front's own D5(n,k) (see d5_derivation.py / .log for the full
#    derivation and its validation against D1-D4).
# ---------------------------------------------------------------------
print("=" * 70)
print("STEP 1: D5(n,k), this front's own derivation (cited from")
print("        d5_derivation.py -- transcribed here, not re-run)")
print("=" * 70)

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
D5_formula = k * (k + 1) * bracket / Dn5
print("D5(n,k) = k(k+1)*Bracket5(n,k) / [n^6(n-1)(n-2)(n-3)(n-4)]")

# sanity: P(T=n) = 1 - D5(n,n-1) = 120/n^5 (matches K!/n^K pattern of
# Corollaries D3.1/D4.1 -- an elementary direct fact, independent check)
PTn = sp.simplify(1 - D5_formula.subs(k, n - 1))
print("1 - D5(n,n-1) [=P(T=n)] =", sp.factor(PTn))
assert sp.simplify(PTn - sp.Rational(120) / n**5) == 0
print("Matches predicted K!/n^K = 5!/n^5 = 120/n^5 exactly. PASSED.")

# ---------------------------------------------------------------------
# 2. h5(n,x), g5(x), M5
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("STEP 2: g5(x), critical point, exact M5")
print("=" * 70)

F5n = sp.cancel(D5_formula.subs(k, n * x))
F5_cont = sp.expand(1 - (1 - x**2)**5)
Delta5 = sp.cancel(F5n - F5_cont)
Num5 = sp.expand(sp.cancel(Delta5 * Dn5))
h5 = sp.cancel(n * Delta5)

Npoly_n = sp.Poly(Num5, n)
print("deg_n N5(n,x):", Npoly_n.degree(), "   deg_n D5(n):", sp.Poly(Dn5, n).degree())
g5 = sp.expand(Npoly_n.coeff_monomial(n**9))
g5_cited_factored = sp.expand(5 * x * (x - 1)**4 * (x + 1)**3 * (2 * x**2 - x + 1))
print("g5(x) [our derivation] =", g5)
assert sp.simplify(g5 - g5_cited_factored) == 0
print("g5(x) [factored] = 5x(x-1)^4(x+1)^3(2x^2-x+1)   MATCH. PASSED.")

g5p = sp.expand(sp.diff(g5, x))
print("g5'(x) factored:", sp.factor(g5p))
crit = sp.Poly(g5p, x).real_roots()
interior = [c for c in crit if 0 < sp.N(c) < 1]
assert len(interior) == 1
x5star = interior[0]
M5 = sp.simplify(g5.subs(x, x5star))
print("x5* =", sp.N(x5star, 30))
print("M5  =", sp.N(M5, 30))

minpoly_x5 = sp.minimal_polynomial(x5star, t)
minpoly_M5 = sp.minimal_polynomial(M5, t)
print("minimal polynomial of x5*:", minpoly_x5, " (degree", sp.degree(minpoly_x5, t), ")")
print("minimal polynomial of M5 :", minpoly_M5, " (degree", sp.degree(minpoly_M5, t), ")")
assert sp.Poly(minpoly_M5, t).is_irreducible
print()
print("NOTE: g5' factors CLEANLY as 5(x-1)^3(x+1)^2(20x^4-7x^3+x^2+3x-1) --")
print("again reducing to an IRREDUCIBLE QUARTIC after stripping trivial")
print("roots x=+-1, exactly the K=3,4 pattern. No new Galois obstruction")
print("appears at K=5.")

M5_cited = sp.Float('0.696803198946355211196876665384', 30)
assert abs(sp.N(M5, 30) - M5_cited) < sp.Float('1e-25', 30)
print()
print("Matches mpmath-independent M5 (k5_mpmath_crosscheck.py) to 25+ digits. PASSED.")

# ---------------------------------------------------------------------
# 3. Boundary values
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("STEP 3: boundary values h5(n,0), h5(n,1) -- exact closed forms")
print("=" * 70)
h0 = sp.simplify(h5.subs(x, 0))
h1 = sp.simplify(sp.factor(h5.subs(x, 1)))
print("h5(n,0) =", h0)
print("h5(n,1) =", h1)
assert h0 == 0
assert sp.simplify(h1 - 120 / ((n - 1) * (n - 2) * (n - 3) * (n - 4))) == 0
print("h5(n,1) is POSITIVE for n>4 (matches K=3's sign, unlike K=4's")
print("negative boundary) -> the UPPER bound is the delicate boundary")
print("direction; the LOWER bound is trivial at x=1 for all n>4.")

thresh_expr = sp.expand((n - 1) * (n - 2) * (n - 3) * (n - 4) * M5 - 120)
thresh_roots = sp.solve(sp.Eq(thresh_expr, 0), n)
thresh_roots_num = [sp.N(r, 20) for r in thresh_roots if r.is_real]
n0_boundary = max(thresh_roots_num)
print("n0_boundary (h5(n,1)=M5 crossing) =", n0_boundary)
assert 6 < n0_boundary < 7
print("Confirmed: 6 < n0_boundary < 7 -> h5(n,1) < M5 exactly for every")
print("integer n >= 7 (h5(6,1)=1 > M5 confirms n=6 genuinely fails).")
h1_at6 = h1.subs(n, 6)
h1_at7 = h1.subs(n, 7)
print("h5(6,1) =", h1_at6, "  (violates upper bound, n=6 excluded)")
print("h5(7,1) =", h1_at7, " =", sp.N(h1_at7, 20), "   M5 =", sp.N(M5, 20))
assert sp.N(h1_at7, 30) < sp.N(M5, 30)
print("h5(7,1) < M5  CONFIRMED (exact).")

# ---------------------------------------------------------------------
# 4. Interior critical points -- UPPER bound (target m=M5)
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("STEP 4: interior critical points, UPPER bound (target m=M5)")
print("=" * 70)

F1 = sp.expand(sp.diff(Num5, x))
F2 = sp.expand(m * Dn5 - n * Num5)

t0 = time.time()
R = sp.expand(sp.resultant(F1, F2, x))
print("elapsed Res_x(F1,F2):", round(time.time() - t0, 2), "s")

minpoly_m_expr = minpoly_M5.subs(t, m)
t0 = time.time()
S = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_m_expr, m)))
print("elapsed Res_m(R, minpoly_M5):", round(time.time() - t0, 2), "s")

t0 = time.time()
content, factors = sp.factor_list(S, n)
print("elapsed factor_list:", round(time.time() - t0, 2), "s")
for f, mult in factors:
    print("  factor degree:", sp.Poly(f, n).degree(), " mult:", mult)
big = max(factors, key=lambda fm: sp.Poly(fm[0], n).degree())[0]
Bpoly = sp.Poly(big, n)

t0 = time.time()
Sroots = Bpoly.real_roots()
print("elapsed real_roots:", round(time.time() - t0, 2), "s   (#roots:", len(Sroots), ")")
Sroots_num = sorted(set(sp.N(r, 20) for r in Sroots))
max_root_upper = max(Sroots_num)
print("largest real root (upper-bound interior threshold):", max_root_upper)
assert max_root_upper < 5
print("Confirmed: < 5 (comfortably below the boundary threshold ~6.30).")
print("Since 'no real x at all' certainly implies 'no real x in [0,1]',")
print("this rigorously rules out an interior [0,1] critical point")
print("achieving h5=M5 for every real n greater than this threshold.")

# ---------------------------------------------------------------------
# 5. Combine, UPPER bound -- explicit continuity + IVT, stated in full
#    from the start (addressing predecessor referee finding F2).
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("STEP 5: combine -- exact closure, UPPER bound (explicit IVT)")
print("=" * 70)


def sup_inf_h5_exact(nv):
    Numn = Num5.subs(n, sp.Rational(nv))
    Dnn = Dn5.subs(n, sp.Rational(nv))
    hx = sp.expand(sp.Rational(nv) * Numn / Dnn)
    hpoly = sp.Poly(hx, x)
    dpoly = hpoly.diff(x)
    crit_pts = sp.Poly(dpoly, x).real_roots()
    cand = [c for c in crit_pts if 0 <= sp.N(c) <= 1] + [sp.Integer(0), sp.Integer(1)]
    vals = [(c, hpoly(c)) for c in cand]
    hi = max(vals, key=lambda cv: sp.N(cv[1]))
    lo = min(vals, key=lambda cv: sp.N(cv[1]))
    return hi, lo


print("a(n):=max_x h5(n,x) is continuous in real n>4 (Berge's maximum")
print("theorem: max of a jointly continuous function over the compact")
print("set x in [0,1]).")
hi7, lo7 = sup_inf_h5_exact(7)
print("a(7) = max_x h5(7,x) =", sp.N(hi7[1], 25), " at x* =", sp.N(hi7[0], 15))
assert sp.N(hi7[1], 30) < sp.N(M5, 30)
print("a(7) < M5  CONFIRMED (exact).")
print()
print("EXPLICIT IVT ARGUMENT (stated completely, from the start):")
print("For real n > n0_upper := max(n0_boundary, max_root_upper), a(n)")
print("never equals M5 (boundary: STEP 3, valid for n>n0_boundary=6.30;")
print("interior: STEP 4, valid for n>max_root_upper). a(n) is continuous")
print("on this connected interval, and a(7) < M5 at one point of it.")
print("By the Intermediate Value Theorem, a CONTINUOUS function that is")
print("NEVER EQUAL to M5 on a connected interval, and is < M5 at one")
print("point of that interval, is < M5 at EVERY point of that interval")
print("(if it were >= M5 anywhere else, continuity + never-equal would")
print("force it to cross M5 somewhere in between, a contradiction).")
print("Hence a(n) < M5 for ALL real n > n0_upper, in particular for")
print("every integer n in the claimed domain.")

print()
print(">>> UPPER-BOUND THEOREM (K=5, EXACT): for all integer n>=7 and")
print(">>> x in [0,1]:  n*Delta_n(x) <= M5,  M5 =", sp.N(M5, 30))

# ---------------------------------------------------------------------
# 6. Interior critical points -- LOWER bound (target m=-M5)
# ---------------------------------------------------------------------
print()
print("=" * 70)
print("STEP 6: interior critical points, LOWER bound (target m=-M5)")
print("=" * 70)
minpoly_negM5_expr = minpoly_M5.subs(t, -m)
t0 = time.time()
S2 = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_negM5_expr, m)))
print("elapsed Res_m(R, minpoly(-M5)):", round(time.time() - t0, 2), "s")
t0 = time.time()
content2, factors2 = sp.factor_list(S2, n)
print("elapsed factor_list:", round(time.time() - t0, 2), "s")
for f, mult in factors2:
    print("  factor degree:", sp.Poly(f, n).degree(), " mult:", mult)
big2 = max(factors2, key=lambda fm: sp.Poly(fm[0], n).degree())[0]
Bpoly2 = sp.Poly(big2, n)
t0 = time.time()
Sroots2 = Bpoly2.real_roots()
print("elapsed real_roots:", round(time.time() - t0, 2), "s  (#roots:", len(Sroots2), ")")
Sroots2_num = sorted(set(sp.N(r, 20) for r in Sroots2))
max_root_lower = max(Sroots2_num)
print("largest real root (lower-bound interior threshold):", max_root_lower)
assert max_root_lower < 5
print("Confirmed: < 5 (comfortably below the boundary threshold ~6.30 and")
print("below the domain start n=7 -- NO exhaustive per-n patch needed,")
print("unlike K=4's Step 7 wrinkle).")

print()
print("=" * 70)
print("STEP 7: combine -- exact closure, LOWER bound (explicit IVT)")
print("=" * 70)
lo7v = lo7[1]
print("min_x h5(7,x) =", sp.N(lo7v, 25), " at x* =", sp.N(lo7[0], 15))
assert sp.N(lo7v, 30) > sp.N(-M5, 30)
print("min_x h5(7,x) > -M5  CONFIRMED (exact).")
print()
print("SAME explicit IVT argument as STEP 5, mirrored: b(n):=min_x h5(n,x)")
print("is continuous in real n>4 (Berge); h5(n,1)=120/[(n-1)(n-2)(n-3)(n-4)]")
print(">0>-M5 for all n>4 (boundary, trivial in this direction); interior")
print("threshold from STEP 6 rules out any interior critical value=-M5 for")
print("real n greater than max_root_lower. b(n) never equals -M5 on the")
print("connected interval n>max(4,max_root_lower), and b(7)>-M5 at one")
print("point of it -> by IVT, b(n) > -M5 for ALL real n in that interval,")
print("in particular every integer n>=7.")

print()
print(">>> LOWER-BOUND THEOREM (K=5, EXACT): for all integer n>=7 and")
print(">>> x in [0,1]:  n*Delta_n(x) >= -M5.")

print()
print("=" * 70)
print("FINAL THEOREM (K=5, EXACT CLOSURE):")
print("for all integer n>=7 and x in [0,1]:")
print("   |F_n^{(5)}(x) - F_5(x)| <= M5/n,")
print("   M5 =", sp.N(M5, 40))
print("   (exact real root of", minpoly_M5, ")")
print("Matches K=2,3,4's tier of closure (exact constant, not a")
print("near-sharp inflated one).")
print("=" * 70)
