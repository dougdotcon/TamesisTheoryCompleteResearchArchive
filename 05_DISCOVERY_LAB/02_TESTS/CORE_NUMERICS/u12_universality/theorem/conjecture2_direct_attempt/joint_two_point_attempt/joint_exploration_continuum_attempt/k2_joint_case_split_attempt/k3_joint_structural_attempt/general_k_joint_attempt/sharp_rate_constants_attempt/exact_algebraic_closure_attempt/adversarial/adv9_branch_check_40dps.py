"""
Independent, high-precision numeric confirmation of the K=4 lower-bound
wrinkle's root cause: at n = n_spurious (~64.768366227610798420), find
ALL real critical points x of h(n,.) (roots of F1(n,x)=0, a degree-7
polynomial in x for fixed n), evaluate h(n,x)=m at each, and confirm
that the critical point whose m-value matches the "other conjugate"
root (~+2.897959841839993) of -M4's minimal quartic sits at x outside
[0,1] (target claims x ~ -0.957).
"""
import sympy as sp
import mpmath as mp
import pickle

mp.mp.dps = 40

n, x = sp.symbols('n x')

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_Nx_Dn.pkl','rb') as f:
    d = pickle.load(f)
Nx, Dn = d['Nx'], d['Dn']

n_spurious = mp.mpf('64.768366227610798420')

F1 = sp.expand(sp.diff(Nx, x))
F1_at_n = F1.subs(n, sp.nsimplify(str(n_spurious)))  # not exact but fine for numeric root find
# better: lambdify F1 in x with n as high-precision numeric substitution via mpmath directly
F1_poly = sp.Poly(F1, x)
coeffs_n = F1_poly.all_coeffs()  # list of expressions in n, highest degree first

# Evaluate each coefficient at n = n_spurious using mpmath (via sympy lambdify with mpmath backend)
f_coeffs = [sp.lambdify(n, c, 'mpmath') for c in coeffs_n]
coeffs_num = [mp.mpf(fc(n_spurious).real) if hasattr(fc(n_spurious),'real') else mp.mpf(fc(n_spurious)) for fc in f_coeffs]
print("F1 coefficients at n=n_spurious (degree", len(coeffs_num)-1, "):")
for c in coeffs_num:
    print("  ", c)

# find all roots of this polynomial in x using mpmath.polyroots
roots_x = mp.polyroots([complex(c) for c in coeffs_num], maxsteps=200, extraprec=400)
print("\nAll roots of F1(n_spurious, x)=0:")
for r in roots_x:
    print("  ", r)

real_roots_x = [r.real for r in roots_x if abs(r.imag) < mp.mpf('1e-20')]
print("\nReal roots (imag~0):", real_roots_x)

# Now evaluate h(n,x) = n*Nx(n,x)/Dn(n) at each real root, at n=n_spurious
Nx_poly_x = sp.Poly(Nx, x)
Nx_coeffs_n = Nx_poly_x.all_coeffs()
g_coeffs = [sp.lambdify(n, c, 'mpmath') for c in Nx_coeffs_n]
Nx_coeffs_num = [mp.mpf(gc(n_spurious).real) if hasattr(gc(n_spurious),'real') else mp.mpf(gc(n_spurious)) for gc in g_coeffs]

def eval_poly(coeffs_highest_first, xv):
    val = mp.mpf(0)
    for c in coeffs_highest_first:
        val = val*xv + c
    return val

Dn_num = sp.lambdify(n, Dn, 'mpmath')(n_spurious)

print("\nh(n_spurious, x) = n*N(n,x)/D(n) at each real critical x:")
for xr in real_roots_x:
    Nval = eval_poly(Nx_coeffs_num, xr)
    hval = n_spurious * Nval / Dn_num
    print(f"  x = {xr}   h(n,x) = {hval}   [in [0,1]? {0 <= xr <= 1}]")

M4_other_root = mp.mpf('2.897959841839993074210129')
negM4 = mp.mpf('-0.7087183934093216141786607')
print(f"\nTarget conjugate values: -M4 = {negM4}, other real root = {M4_other_root}")
