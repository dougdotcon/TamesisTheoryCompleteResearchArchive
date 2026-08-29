"""
Referee check (Item 4, extra): verify the K=3 lower-bound "touches-zero"
threshold (largest real root of Res_x(dN/dx, N), ~5.968) corresponds to
a double root of N(n,x) genuinely INSIDE [0,1] -- i.e. confirm the K=3
lower bound does NOT suffer from the same out-of-domain spurious-branch
issue found (and patched) for the K=4 lower bound in Sec 4.5.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

n, x, k = sp.symbols('n x k')
D3_num = k*(k+1)*(k**4 - 4*k**3 - (3*n**2 - 9*n - 5)*k**2 + (3*n**2 - 11*n - 2)*k
                  + (3*n**4 - 12*n**3 + 12*n**2 + 2*n))
D3_den = n**4*(n-1)*(n-2)
F3n = D3_num / D3_den
F3_cont = 1 - (1-x**2)**3
Delta3 = sp.cancel(F3n.subs(k, n*x) - F3_cont)
Nx, Dn = sp.fraction(Delta3)
Nx = sp.expand(Nx)

# Exact largest real root of the touches-zero locus (from adv4):
n_star = mp.mpf('5.968184604630802771859263')

Nx_poly = sp.Poly(Nx, x)
coeffs_fns = [sp.lambdify(n, c, 'mpmath') for c in Nx_poly.all_coeffs()]
coeffs_num = [mp.mpf(str(cf(n_star))) for cf in coeffs_fns]
roots_x = mp.polyroots([complex(c) for c in coeffs_num], maxsteps=300, extraprec=400)
print("All roots of N(n_star, x)=0:")
for r in roots_x:
    print("  ", r)
real_roots = [r.real for r in roots_x if abs(r.imag) < mp.mpf('1e-30')]
print("\nReal roots:", real_roots)

F1 = sp.expand(sp.diff(Nx, x))
F1_poly = sp.Poly(F1, x)
coeffs_fns1 = [sp.lambdify(n, c, 'mpmath') for c in F1_poly.all_coeffs()]
coeffs_num1 = [mp.mpf(str(cf(n_star))) for cf in coeffs_fns1]

def eval_poly(coeffs, xv):
    v = mp.mpf(0)
    for c in coeffs:
        v = v*xv + c
    return v

print("\nChecking F1 (dN/dx) at each real root of N (double root => both ~0):")
for r in real_roots:
    val = eval_poly(coeffs_num1, r)
    print(f"  x={r}   N=0 (by construction)  dN/dx={val}   in[0,1]? {0<=r<=1}")
