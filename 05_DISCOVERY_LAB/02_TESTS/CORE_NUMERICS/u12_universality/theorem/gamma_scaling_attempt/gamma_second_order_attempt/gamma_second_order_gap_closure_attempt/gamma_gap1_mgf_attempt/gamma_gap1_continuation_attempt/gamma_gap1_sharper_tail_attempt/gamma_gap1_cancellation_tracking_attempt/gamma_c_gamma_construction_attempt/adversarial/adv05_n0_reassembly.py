"""
Independent reassembly of the front's final n_0(gamma) table (ATTEMPT.md
Sec.4, "this front, v2" column), built purely from the formulas quoted in
prose in ATTEMPT.md Sec.1-Sec.4 (lambda_tight, K_real, C0_tight_Bernstein,
the Lyapunov bulk/small-k bound, the Bernstein-with-slack tail, the
margin-search convention) -- an independent spot-check per scrutiny item
(e), at 3 of the 8 rows: gamma=0.5, 0.9, 0.01 (spanning small/medium/
near-1 gamma and covering both "bulk-binding" and "small-k-binding"
regimes per script06's own term breakdown).
"""
import time
import mpmath as mp
import sympy as sp
from sympy import symbols, Poly, expand

mp.mp.dps = 80

g, k, n = symbols('gamma k n', positive=True)
D = symbols('D')

# independently re-derived + 4-ways-cross-checked c_i (adv01-03)
c0_expr = (g*k/(12*n**2))*(2*g**2*k**2 - 6*g*k**2 + 3*g*k + 6*k**2 - 6*k + 1)
c1_expr = (1/n**2)*(g**2*k**2/2 - g*k**2 - g*k*n + g*k/2 + k**2/2 + k*n - k/2 - n/2 + sp.Rational(1,12))
c2_expr = (2*g*k - 2*k - 2*n + 1)/(4*n**2)
c3_expr = sp.Rational(1,6)/n**2

# fresh moment recursion (adv04-style, but only need up to order 12 here
# for E[x^4]; re-derive independently once, cache as lambdified function)
from sympy import log, exp, series, factorial as spfact, binomial as spbinom
t = symbols('t')
MAXORD = 12
cgf1 = log(1 - g + g*exp(t))
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
        s += spbinom(nn-1, m-1)*kD[m]*mu[nn-m]
    mu[nn] = expand(s)

x_D = c0_expr + c1_expr*D + c2_expr*D**2 + c3_expr*D**3
x4 = expand(x_D**4)
x4p = Poly(x4, D)
Ex4 = sp.Integer(0)
for j in range(0, 13):
    coeff = x4p.coeff_monomial(D**j) if j > 0 else x4p.coeff_monomial(1)
    Ex4 += coeff*mu[j]
Ex4 = expand(Ex4)

print("Independent Ex4 built, lambdifying...")
Ex4_f = sp.lambdify((k, n, g), Ex4, modules='mpmath')
c0_f = sp.lambdify((k, n, g), c0_expr, modules='mpmath')
c1_f = sp.lambdify((k, n, g), c1_expr, modules='mpmath')
c2_f = sp.lambdify((k, n, g), c2_expr, modules='mpmath')
c3_f = sp.lambdify((k, n, g), c3_expr, modules='mpmath')

def beta_of(gm): return gm*(2-gm)/2
def sigma2_of(gm): return gm*(1-gm)
def lambda_tight_of(gm): return max(mp.mpf(4), 4*(1-gm)**2/(gm*(2-gm)))
def K_real(n_val, gm): return mp.sqrt(4*n_val*mp.log(n_val)/beta_of(gm)) + 1
def G_n_bound(n_val, gm): return mp.sqrt(mp.pi*n_val/beta_of(gm))

def exact_cubic_max_abs(k_val, n_val, gm, Dlo, Dhi):
    c0v=c0_f(k_val,n_val,gm); c1v=c1_f(k_val,n_val,gm)
    c2v=c2_f(k_val,n_val,gm); c3v=c3_f(k_val,n_val,gm)
    def xval(Dv): return c0v+c1v*Dv+c2v*Dv**2+c3v*Dv**3
    cands=[Dlo,Dhi]
    a_,b_,c_=3*c3v,2*c2v,c1v
    if abs(a_) > mp.mpf('1e-90'):
        disc=b_**2-4*a_*c_
        if disc>=0:
            sq=mp.sqrt(disc)
            for r in [(-b_+sq)/(2*a_), (-b_-sq)/(2*a_)]:
                if Dlo<=r<=Dhi: cands.append(r)
    return max(abs(xval(Dv)) for Dv in cands)

def bulk_term(k_val,n_val,gm,Theta):
    Dlo=max(-gm*k_val,-Theta); Dhi=min((1-gm)*k_val,Theta)
    H=exact_cubic_max_abs(k_val,n_val,gm,Dlo,Dhi)
    E4=Ex4_f(k_val,n_val,gm)
    if E4<0: E4=mp.mpf(0)
    return mp.mpf(1)/6*mp.e**H*E4**mp.mpf('0.75')

def tail_term(K_val,n_val,gm,C,a):
    Dlo=-gm*K_val; Dhi=(1-gm)*K_val
    H=exact_cubic_max_abs(K_val,n_val,gm,Dlo,Dhi)
    s2=sigma2_of(gm)
    expo=-(C**2)/((2+a)*s2)*mp.log(n_val)
    return mp.mpf(1)/6*2*mp.e**expo*H**3*mp.e**H

def k2_of(n_val,gm,C,a):
    s2=sigma2_of(gm)
    return (2*C/(3*a*s2))**2*mp.log(n_val)

def small_k_term(n_val,gm,C,a):
    k2=k2_of(n_val,gm,C,a)
    k2i=max(mp.mpf(1),k2)
    Dlo=-gm*k2i; Dhi=(1-gm)*k2i
    H=exact_cubic_max_abs(k2i,n_val,gm,Dlo,Dhi)
    E4=Ex4_f(k2i,n_val,gm)
    if E4<0: E4=mp.mpf(0)
    return k2i*mp.mpf(1)/6*mp.e**H*E4**mp.mpf('0.75')

def W_total(n_val,gm,C,a):
    K=K_real(n_val,gm)
    Theta=C*mp.sqrt(K*mp.log(n_val))
    bulk=bulk_term(K,n_val,gm,Theta)
    tail=tail_term(K,n_val,gm,C,a)
    Gn=G_n_bound(n_val,gm)
    sk=small_k_term(n_val,gm,C,a)
    return Gn*(bulk+tail)+sk

def find_n0(gm,C,a,lo=5,hi=200):
    def f(l10n):
        nv=mp.mpf(10)**l10n
        try:
            w=W_total(nv,gm,C,a)
        except Exception:
            return mp.mpf('inf')
        return mp.log(w) if w>0 else mp.mpf('-inf')
    lo_,hi_=mp.mpf(lo),mp.mpf(hi)
    if f(hi_)>=0: return None
    if f(lo_)<0: return lo_
    for _ in range(60):
        mid=(lo_+hi_)/2
        if f(mid)>=0: lo_=mid
        else: hi_=mid
    return hi_

A_SLACK=mp.mpf('0.05')
MARGINS=[mp.mpf(x) for x in ['1.01','1.05','1.10','1.20','1.50','2.0']]

targets = {
    '0.5': mp.mpf('16.4628'),
    '0.9': mp.mpf('10.1536'),
    '0.01': mp.mpf('31.4117'),
}

print("\nIndependent n0(gamma) bisection at 3 sample gamma (fresh implementation):")
for gm_s, target in targets.items():
    gm = mp.mpf(gm_s)
    C0 = mp.sqrt((2+A_SLACK)*sigma2_of(gm)*(lambda_tight_of(gm)+mp.mpf('0.5')))
    best = None
    for m in MARGINS:
        C = m*C0
        n0 = find_n0(gm, C, A_SLACK)
        if n0 is not None and (best is None or n0 < best[1]):
            best = (m, n0, C)
    m, n0, C = best
    diff = abs(n0-target)
    print(f"  gamma={gm_s}: my n0=10^{mp.nstr(n0,8)}  (best margin={float(m)})  "
          f"target(front's v2)=10^{mp.nstr(target,8)}  |diff|={mp.nstr(diff,4)} decades")
