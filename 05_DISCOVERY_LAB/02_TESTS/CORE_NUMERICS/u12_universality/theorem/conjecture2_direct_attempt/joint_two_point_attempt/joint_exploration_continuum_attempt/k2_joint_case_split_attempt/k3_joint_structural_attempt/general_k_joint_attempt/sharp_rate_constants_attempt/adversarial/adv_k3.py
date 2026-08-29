#!/usr/bin/env python3
"""
INDEPENDENT, from-scratch verification of K=3 claims (item 2 of the referee
mandate). Written without reading the front's own scripts. Source formula
(Proposicao D3) transcribed by hand from THEOREM.md Estagio 40 (line 6028):

  P(M_n^{(3)} <= k/n) =
    k(k+1)*[k^4 - 4k^3 - (3n^2-9n-5)k^2 + (3n^2-11n-2)k + (3n^4-12n^3+12n^2+2n)]
    / [n^4(n-1)(n-2)]                                    0<=k<=n-1, n>=3
"""
import sympy as sp
import time

n, x, k = sp.symbols('n x k', positive=True)

num_k = k*(k+1)*( k**4 - 4*k**3 - (3*n**2-9*n-5)*k**2 + (3*n**2-11*n-2)*k
                   + (3*n**4-12*n**3+12*n**2+2*n) )
den_k = n**4*(n-1)*(n-2)
D3_k = num_k/den_k

D3_x = sp.cancel(D3_k.subs(k, n*x))
F3 = 1 - (1-x**2)**3
Delta3 = sp.cancel(D3_x - F3)
print("Delta3_n(x) [independent] numerator/denominator:")
numD, denD = sp.fraction(sp.together(Delta3))
numD = sp.expand(numD)
print("den:", sp.factor(denD))

print()
print("="*70)
print("(a) leading term g_3(x) as n -> infinity, derived independently")
print("="*70)
nDelta3 = sp.cancel(n*Delta3)
g3_limit = sp.expand(sp.limit(nDelta3, n, sp.oo))
print("lim n*Delta3_n(x) =", g3_limit)

g3_claimed_factored = 3*x*(x-1)**2*(x+1)*(x**2+1)
g3_claimed_expanded = sp.expand(g3_claimed_factored)
print("claimed factored form expands to:", g3_claimed_expanded)
print("difference from independently-derived limit:", sp.simplify(g3_limit - g3_claimed_expanded))

print()
print("="*70)
print("(b) M_3 = max_[0,1] g_3(x) via Poly(...).real_roots()")
print("="*70)
g3 = g3_limit
g3p = sp.diff(g3, x)
proots = sp.Poly(g3p, x).real_roots()
print("real roots of g3'(x)=0:", [sp.N(r,20) for r in proots])
interior = [r for r in proots if 0 < r < 1]
print("interior roots (0,1):", interior)
cands = interior + [sp.Integer(0), sp.Integer(1)]
vals = [(sp.N(g3.subs(x,c),30), sp.N(c,30)) for c in cands]
vals.sort(key=lambda t: t[0], reverse=True)
M3_val, xstar3 = vals[0]
print("M_3 =", M3_val, " at x* =", xstar3)

target_M3 = sp.Float("0.71207155813802780842", 30)
target_x3 = sp.Float("0.45219215045425892654", 30)
print("front's claimed M_3 =", target_M3, "diff=", M3_val-target_M3)
print("front's claimed x*  =", target_x3, "diff=", xstar3-target_x3)

# sign check of g3 on [0,1] via factored form (elementary, not sampled)
print("g3(x)=3x(x-1)^2(x+1)(x^2+1): each factor sign on [0,1]: x>=0, (x-1)^2>=0, (x+1)>0, (x^2+1)>0 => g3>=0 on [0,1]. Confirmed by construction.")

print()
print("="*70)
print("(c) exhaustive-window spot-check: >=15 scattered n in [6,999]")
print("     compute EXACT sup_x n*|Delta3_n(x)| per n (own critical-point calc)")
print("     confirm <= C_3 for each")
print("="*70)

C3 = sp.Float("0.71833358218612400080", 30)
print("Using front's claimed C_3 =", C3)

sample_ns = [6,7,8,10,13,20,29,45,63,90,130,180,250,333,420,555,650,777,888,950,999]
print(f"testing {len(sample_ns)} n values:", sample_ns)

t0 = time.time()
results = []
for nn in sample_ns:
    Dn = Delta3.subs(n, nn)
    Dn = sp.together(Dn)
    Dnp = sp.diff(Dn, x)
    Dnp_num = sp.numer(sp.together(Dnp))
    Dnp_num = sp.Poly(sp.expand(Dnp_num), x)
    croots = Dnp_num.real_roots()
    croots_interior = [r for r in croots if 0 <= r <= 1]
    cand_pts = croots_interior + [sp.Integer(0), sp.Integer(1)]
    best = None
    bestx = None
    for c in cand_pts:
        v = sp.N(sp.Abs(Dn.subs(x, c)), 30)
        if best is None or v > best:
            best = v
            bestx = c
    nsup = sp.N(nn * best, 30)
    ratio = float(nsup / C3)
    ok = ratio <= 1.0 + 1e-9
    results.append((nn, float(sp.N(bestx,10)), float(best), float(nsup), ratio, ok))
    print(f"  n={nn:4d}: worst x*~{float(sp.N(bestx,10)):.6f}  sup|Delta_n|={float(best):.10f}  n*sup={float(nsup):.10f}  ratio to C3={ratio:.8f}  [{'OK' if ok else 'VIOLATION'}]")

t1 = time.time()
print(f"\nElapsed: {t1-t0:.1f}s")
nviol = sum(1 for r in results if not r[5])
print(f"Violations found: {nviol} / {len(results)}")
worst_ratio = max(r[4] for r in results)
print(f"Max ratio observed (n*sup/C3): {worst_ratio:.8f}  (approaches M3/C3={float(sp.N(sp.Float('0.71207155813802780842',30)/C3,10)):.8f} as n->large)")
