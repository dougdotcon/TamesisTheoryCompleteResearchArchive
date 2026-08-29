"""
Independent re-check of the Lyapunov pointwise bound R_k_exact <= R_k_bound
(script06 Check A's claim), at FRESH (k,n,gamma) points not used by the
target's own script06 (which used k in {10,30,80}, n in {1000,20000},
gamma in {0.2,0.5,0.8}). This spot-checks item (b)/(c) of the scrutiny
list -- is the bound actually valid, or did the target get lucky with its
own sample grid?
"""
import mpmath as mp
import sympy as sp
from sympy import symbols, Poly, expand

mp.mp.dps = 80

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')
c0_expr = (g*k/(12*n**2))*(2*g**2*k**2 - 6*g*k**2 + 3*g*k + 6*k**2 - 6*k + 1)
c1_expr = (1/n**2)*(g**2*k**2/2 - g*k**2 - g*k*n + g*k/2 + k**2/2 + k*n - k/2 - n/2 + sp.Rational(1,12))
c2_expr = (2*g*k - 2*k - 2*n + 1)/(4*n**2)
c3_expr = sp.Rational(1,6)/n**2
c0_f = sp.lambdify((k,n,g), c0_expr, modules='mpmath')
c1_f = sp.lambdify((k,n,g), c1_expr, modules='mpmath')
c2_f = sp.lambdify((k,n,g), c2_expr, modules='mpmath')
c3_f = sp.lambdify((k,n,g), c3_expr, modules='mpmath')

from sympy import log, exp, series, factorial as spfact, binomial as spbinom
t = symbols('t')
MAXORD = 12
cgf1 = log(1-g+g*exp(t))
ser = series(cgf1, t, 0, MAXORD+1).removeO()
poly = Poly(ser, t)
kt = {0: sp.Integer(0)}
for j in range(1, MAXORD+1):
    kt[j] = expand(spfact(j)*poly.coeff_monomial(t**j))
kD = {0: sp.Integer(0), 1: sp.Integer(0)}
for j in range(2, MAXORD+1):
    kD[j] = k*kt[j]
mu = {0: sp.Integer(1)}
for nn in range(1, MAXORD+1):
    s = sp.Integer(0)
    for m in range(1, nn+1):
        s += spbinom(nn-1,m-1)*kD[m]*mu[nn-m]
    mu[nn] = expand(s)
x_D = c0_expr + c1_expr*D + c2_expr*D**2 + c3_expr*D**3
x4 = expand(x_D**4); x4p = Poly(x4, D)
Ex4 = sp.Integer(0)
for j in range(0,13):
    coeff = x4p.coeff_monomial(D**j) if j>0 else x4p.coeff_monomial(1)
    Ex4 += coeff*mu[j]
Ex4_f = sp.lambdify((k,n,g), expand(Ex4), modules='mpmath')

def exact_cubic_max_abs(k_val,n_val,gm,Dlo,Dhi):
    c0v=c0_f(k_val,n_val,gm); c1v=c1_f(k_val,n_val,gm)
    c2v=c2_f(k_val,n_val,gm); c3v=c3_f(k_val,n_val,gm)
    def xval(Dv): return c0v+c1v*Dv+c2v*Dv**2+c3v*Dv**3
    cands=[Dlo,Dhi]
    a_,b_,c_=3*c3v,2*c2v,c1v
    if abs(a_)>mp.mpf('1e-90'):
        disc=b_**2-4*a_*c_
        if disc>=0:
            sq=mp.sqrt(disc)
            for r in [(-b_+sq)/(2*a_),(-b_-sq)/(2*a_)]:
                if Dlo<=r<=Dhi: cands.append(r)
    return max(abs(xval(Dv)) for Dv in cands)

def x_val_mp(k_val,n_val,gm,Dv):
    return (c0_f(k_val,n_val,gm)+c1_f(k_val,n_val,gm)*Dv
            +c2_f(k_val,n_val,gm)*Dv**2+c3_f(k_val,n_val,gm)*Dv**3)

def R_k_exact(k_val,n_val,gm):
    total=mp.mpf(0)
    for m in range(0,k_val+1):
        p=mp.binomial(k_val,m)*mp.mpf(gm)**m*mp.mpf(1-gm)**(k_val-m)
        Dv=mp.mpf(m)-gm*k_val
        xv=x_val_mp(k_val,n_val,gm,Dv)
        total += p*abs(xv)**3*mp.e**abs(xv)
    return total/6

# FRESH sample points, deliberately different from the target's own grid
# (k in {10,30,80}, n in {1000,20000}, gamma in {0.2,0.5,0.8}):
FRESH = [
    (5, 500, mp.mpf('0.1')), (5, 500, mp.mpf('0.9')),
    (15, 3000, mp.mpf('0.4')), (15, 3000, mp.mpf('0.6')),
    (45, 7000, mp.mpf('0.15')), (45, 7000, mp.mpf('0.95')),
    (100, 15000, mp.mpf('0.5')), (100, 50000, mp.mpf('0.99')),
    (60, 2000, mp.mpf('0.03')), (2, 100, mp.mpf('0.5')),
]

print("Fresh pointwise Lyapunov-bound check (k,n,gamma NOT used by target's own script06):")
viol=0
for k_val, n_val, gm in FRESH:
    Dlo=-gm*k_val; Dhi=(1-gm)*k_val
    H=exact_cubic_max_abs(k_val,n_val,gm,Dlo,Dhi)
    E4=Ex4_f(k_val,n_val,gm)
    if E4<0: E4=mp.mpf(0)
    Rbound = mp.mpf(1)/6*mp.e**H*E4**mp.mpf('0.75')
    Rexact = R_k_exact(k_val,n_val,gm)
    ok = Rexact <= Rbound*(1+mp.mpf('1e-20'))
    if not ok: viol+=1
    ratio = Rbound/Rexact if Rexact>0 else mp.inf
    print(f"  k={k_val:>4} n={n_val:>6} gamma={float(gm):.2f}: "
          f"R_exact={mp.nstr(Rexact,6):>14} R_bound={mp.nstr(Rbound,6):>14} "
          f"ratio={mp.nstr(ratio,6):>10} {'OK' if ok else 'VIOLATION!!'}")
print(f"\n{len(FRESH)} fresh checks, {viol} violations")
