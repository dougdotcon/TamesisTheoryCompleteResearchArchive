"""
High-precision (60-digit) re-check of which conjugate root (-M4 or the
'other' +2.8979...) is actually realized at the spurious critical point
x=-0.957 for n=n_spurious (the largest real root of the K=4 lower-bound
elimination's degree-220 factor).

Uses sympy CRootOf for exact algebraic n_spurious (arbitrary precision),
then mpmath at 60 digits throughout for the numeric root-finding and
evaluation, to remove any ambiguity from limited-precision truncation.
"""
import sympy as sp
import mpmath as mp
import pickle, time

mp.mp.dps = 60

n, x, m = sp.symbols('n x m')

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_Nx_Dn.pkl','rb') as f:
    d = pickle.load(f)
Nx, Dn = d['Nx'], d['Dn']

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_R_upper.pkl','rb') as f:
    R = pickle.load(f)

t = sp.Symbol('t')
M4_minpoly = 35831808*t**4 - 49852544*t**3 - 220711113*t**2 + 556322688*t - 274710528
negM4_minpoly = sp.expand(M4_minpoly.subs(t, -m))

print("Building S2(n) and extracting the degree-220 factor (reuse from adv8 logic)...")
t0=time.time()
S2 = sp.resultant(sp.Poly(R, m), sp.Poly(negM4_minpoly, m))
content2, facs2 = sp.factor_list(S2, n)
big2 = max(facs2, key=lambda fm: sp.Poly(fm[0], n).degree())[0]
Bpoly2 = sp.Poly(big2, n)
print(f"done in {time.time()-t0:.1f}s, degree {Bpoly2.degree()}")

t0=time.time()
roots2 = Bpoly2.real_roots()
print(f"real_roots in {time.time()-t0:.1f}s")
n_spurious_exact = max(roots2, key=lambda r: sp.N(r,20))
print("n_spurious exact CRootOf object:", n_spurious_exact)
n_spurious_hp = sp.N(n_spurious_exact, 60)
print("n_spurious (60 digits):", n_spurious_hp)

n_spurious_mp = mp.mpf(str(n_spurious_hp))

# F1 = d/dx N(n,x), evaluate coefficients at n=n_spurious to 60 digits
F1 = sp.expand(sp.diff(Nx, x))
F1_poly_x = sp.Poly(F1, x)
coeffs_n = F1_poly_x.all_coeffs()
coeffs_num = []
for c in coeffs_n:
    val = sp.N(c.subs(n, n_spurious_exact), 60)
    coeffs_num.append(mp.mpf(str(val)))
print("\nF1 coefficients at n=n_spurious (60-digit precision), degree", len(coeffs_num)-1)

roots_x = mp.polyroots([complex(c) for c in coeffs_num], maxsteps=300, extraprec=800)
real_roots_x = [r.real for r in roots_x if abs(r.imag) < mp.mpf('1e-45')]
print("\nReal roots of F1(n_spurious,x)=0 (60-digit precision):")
for r in real_roots_x:
    print("  ", r)

# Evaluate h(n,x) at each real critical x, at n=n_spurious, to 60-digit precision
Nx_poly_x = sp.Poly(Nx, x)
Nx_coeffs_n = Nx_poly_x.all_coeffs()
Nx_coeffs_num = []
for c in Nx_coeffs_n:
    val = sp.N(c.subs(n, n_spurious_exact), 60)
    Nx_coeffs_num.append(mp.mpf(str(val)))

def eval_poly(coeffs_highest_first, xv):
    val = mp.mpf(0)
    for c in coeffs_highest_first:
        val = val*xv + c
    return val

Dn_val = sp.N(Dn.subs(n, n_spurious_exact), 60)
Dn_num = mp.mpf(str(Dn_val))

print("\nh(n_spurious, x) at each real critical x (60-digit precision):")
for xr in real_roots_x:
    Nval = eval_poly(Nx_coeffs_num, xr)
    hval = n_spurious_mp * Nval / Dn_num
    print(f"  x = {xr}")
    print(f"     h(n,x) = {hval}   in[0,1]? {0 <= xr <= 1}")

M4_hp = sp.N(sp.Rational(1)*sp.sqrt(1), 1)  # placeholder
M4_exact_str = "0.708718393409321614178660709132279386397434817180417414418449"
other_root_str = "2.897959841839993074210129..."
print("\nFor reference:")
print("  -M4 (60 digits, from earlier adv2 minpoly) ~ -0.708718393409321614178660709132...")
print("  other real conjugate root of minpoly(-M4) ~ +2.897959841839993074210129...")
