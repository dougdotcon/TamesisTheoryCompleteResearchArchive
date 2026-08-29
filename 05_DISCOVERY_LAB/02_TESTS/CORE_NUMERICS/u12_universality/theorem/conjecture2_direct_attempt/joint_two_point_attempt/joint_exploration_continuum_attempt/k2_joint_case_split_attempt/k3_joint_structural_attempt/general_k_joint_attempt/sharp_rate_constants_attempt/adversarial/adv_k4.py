#!/usr/bin/env python3
"""
INDEPENDENT, from-scratch verification of K=4 claims (item 3 of the referee
mandate). Written without reading the front's own scripts. Source formula
(Proposicao D4) transcribed by hand from THEOREM.md Estagio 43 (lines 6351-6354):

  P(M_n^{(4)} <= k/n) = k(k+1)*Q(n,k) / [n^5(n-1)(n-2)(n-3)]     0<=k<=n-1, n>=4

  Q(n,k) = -k^6 + 9k^5 + (4n^2-18n-31)k^4 + (-16n^2+80n+51)k^3
           + (-6n^4+42n^3-55n^2-120n-40)k^2 + (6n^4-50n^3+97n^2+70n+12)k
           + 4n^6-30n^5+74n^4-52n^3-30n^2-12n
"""
import sympy as sp
import time

n, x, k = sp.symbols('n x k', positive=True)

Q = ( -k**6 + 9*k**5 + (4*n**2-18*n-31)*k**4 + (-16*n**2+80*n+51)*k**3
      + (-6*n**4+42*n**3-55*n**2-120*n-40)*k**2
      + (6*n**4-50*n**3+97*n**2+70*n+12)*k
      + 4*n**6-30*n**5+74*n**4-52*n**3-30*n**2-12*n )
num_k = k*(k+1)*Q
den_k = n**5*(n-1)*(n-2)*(n-3)
D4_k = num_k/den_k

D4_x = sp.cancel(D4_k.subs(k, n*x))
F4 = 1 - (1-x**2)**4
Delta4 = sp.cancel(D4_x - F4)
numD, denD = sp.fraction(sp.together(Delta4))
print("den:", sp.factor(denD))

print()
print("="*70)
print("(a) leading term g_4(x) as n -> infinity, derived independently")
print("="*70)
nDelta4 = sp.cancel(n*Delta4)
g4_limit = sp.expand(sp.limit(nDelta4, n, sp.oo))
print("lim n*Delta4_n(x) =", g4_limit)

g4_claimed = sp.expand(-6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x)
print("claimed g_4(x) =", g4_claimed)
print("difference:", sp.simplify(g4_limit - g4_claimed))

print()
print("="*70)
print("(b) M_4 = max_[0,1] g_4(x) -- front disclosed no clean closed factorization;")
print("    use Poly(...).real_roots() on g4', matching front's own honest method")
print("="*70)
g4 = g4_limit
g4p = sp.diff(g4, x)
print("g4'(x) =", g4p)
proots = sp.Poly(g4p, x).real_roots()
print("real roots of g4'=0:", [sp.N(r,25) for r in proots])
interior = [r for r in proots if 0 < r < 1]
print("interior critical points in (0,1):", interior)
cands = interior + [sp.Integer(0), sp.Integer(1)]
vals = [(sp.N(g4.subs(x,c),30), sp.N(c,30)) for c in cands]
vals.sort(key=lambda t: t[0], reverse=True)
M4_val, xstar4 = vals[0]
print("all candidate (value, x) pairs:", vals)
print("M_4 =", M4_val, "at x* =", xstar4)

target_M4 = sp.Float("0.70871839340932161418", 30)
target_x4 = sp.Float("0.36988656610088332578", 30)
print("front's claimed M_4 =", target_M4, "diff=", M4_val - target_M4)
print("front's claimed x*  =", target_x4, "diff=", xstar4 - target_x4)

# Independent second method: pure numerical optimization (scipy-free, dense
# grid + local bisection refine) as a cross-check against the exact-algebra
# real_roots method, to catch any real_roots mis-isolation.
import mpmath as mp
mp.mp.dps = 40
g4_f = sp.lambdify(x, g4, 'mpmath')
best_x = None
best_v = mp.mpf('-1e9')
N = 200000
for i in range(N+1):
    xx = mp.mpf(i)/N
    v = g4_f(xx)
    if v > best_v:
        best_v = v
        best_x = xx
print(f"independent dense-grid ({N} points) argmax: x~{float(best_x):.6f}, value~{float(best_v):.10f}")

# sign check g4(x)>=0 on [0,1]: real-root count method (no hand factorization
# available for K=4, disclosed honestly by the front -- reproduce that here)
g4_roots_01 = sp.Poly(g4, x).real_roots()
print("real roots of g4(x)=0:", g4_roots_01, " (only endpoints expected)")
roots_strictly_interior = [r for r in g4_roots_01 if 0 < r < 1]
print("interior roots of g4=0 (should be none, if g4>=0 throughout):", roots_strictly_interior)
# spot numeric sign check across [0,1]
signs_ok = all(float(g4.subs(x, sp.Rational(i,1000))) >= -1e-9 for i in range(0,1001))
print("dense sign spot-check g4(x)>=0 for x in {0,0.001,...,1}:", signs_ok)

print()
print("="*70)
print("(c) exhaustive-window spot-check: >=15 scattered n in [6,999]")
print("     compute EXACT sup_x n*|Delta4_n(x)| per n, confirm <= C_4")
print("="*70)
C4 = sp.Float("0.7345569184500456912259", 30)
print("Using front's claimed C_4 =", C4)

sample_ns = [6,7,8,10,13,20,29,45,63,90,130,180,250,333,420,555,650,777,888,950,999]
print(f"testing {len(sample_ns)} n values:", sample_ns)

t0 = time.time()
results = []
for nn in sample_ns:
    Dn = sp.together(Delta4.subs(n, nn))
    Dnp = sp.diff(Dn, x)
    Dnp_num = sp.Poly(sp.expand(sp.numer(sp.together(Dnp))), x)
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
    ratio = float(nsup / C4)
    ok = ratio <= 1.0 + 1e-9
    results.append((nn, float(sp.N(bestx,10)), float(best), float(nsup), ratio, ok))
    print(f"  n={nn:4d}: worst x*~{float(sp.N(bestx,10)):.6f}  sup|Delta_n|={float(best):.10f}  n*sup={float(nsup):.10f}  ratio to C4={ratio:.8f}  [{'OK' if ok else 'VIOLATION'}]")

t1 = time.time()
print(f"\nElapsed: {t1-t0:.1f}s")
nviol = sum(1 for r in results if not r[5])
print(f"Violations found: {nviol} / {len(results)}")
worst_ratio = max(r[4] for r in results)
print(f"Max ratio observed: {worst_ratio:.8f} (approaches M4/C4={float(sp.N(sp.Float('0.70871839340932161418',30)/C4,10)):.8f})")
