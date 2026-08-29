#!/usr/bin/env python3
"""
INDEPENDENT, from-scratch verification of K=2 claims (item 1 of the referee
mandate). Written without reading the front's own scripts. Source formula
(Proposicao D2) transcribed by hand from THEOREM.md Estagio 42 (line 6262):

    P(M_n^{(2)} <= k/n) = k(k+1)(2n^2-3n+k-k^2) / [n^3(n-1)]     0<=k<=n-1, n>=2

F_2(x) := 1-(1-x^2)^2  (continuum CDF for K=2, from F_K(x)=1-(1-x^2)^K, Estagio 24).
"""
import sympy as sp

n, x, t, k = sp.symbols('n x t k', positive=True)

# --- (a) derive Delta_n(x) and confirm n*Delta_n(x) -> g_1(x) symbolically ---
D2_k = k*(k+1)*(2*n**2 - 3*n + k - k**2) / (n**3*(n-1))
D2_x = sp.together(D2_k.subs(k, n*x))          # substitute k = n*x
D2_x = sp.cancel(D2_x)

F2 = 1 - (1-x**2)**2

Delta = sp.cancel(D2_x - F2)
print("Delta_n(x) [independently re-simplified] =", Delta)

# Put over the common denominator n*(n-1) claimed by the front, verify.
num, den = sp.fraction(sp.together(Delta))
print("numerator:", sp.expand(num))
print("denominator:", sp.factor(den))

# Compare against front's claimed closed form for Delta_n(x):
# (-n*x^4 - n*x^2 + 2*n*x + x^2 - 3*x) / (n*(n-1))
claimed = (-n*x**4 - n*x**2 + 2*n*x + x**2 - 3*x) / (n*(n-1))
diff = sp.simplify(Delta - claimed)
print("Delta - claimed_front_form simplifies to:", diff, " (expect 0)")

# n*Delta_n(x) as n -> infinity: take the limit of n*Delta_n(x) symbolically.
nDelta = sp.cancel(n*Delta)
g1_limit = sp.limit(nDelta, n, sp.oo)
print("lim_{n->oo} n*Delta_n(x) =", sp.expand(g1_limit))

g1 = sp.expand(2*x - x**2 - x**4)
print("claimed g_1(x) = 2x - x^2 - x^4 ; difference from limit:",
      sp.simplify(g1_limit - g1))

# Also derive g1 via polynomial-degree leading-coefficient method (independent
# second method): n*Delta_n(x) - g1(x) should be O(1/n).
rem = sp.cancel(nDelta - g1)
print("n*Delta_n(x) - g1(x) [should be O(1/n), i.e. have n-1 or n factor in denom]:")
print("  =", sp.simplify(rem))

print()
print("="*70)
print("(b) M_2 = max_{[0,1]} g_1(x) via Poly(...).real_roots() -- NOT sp.solve()")
print("="*70)

g1x = g1  # 2x - x^2 - x^4
g1p = sp.diff(g1x, x)
print("g1'(x) =", g1p)

poly = sp.Poly(g1p, x)
roots = poly.real_roots()
print("real_roots of g1'(x)=0:", roots)

# filter to (0,1)
interior = [r for r in roots if r > 0 and r < 1]
print("interior roots in (0,1):", interior)

xstar = interior[0]
xstar_n = sp.nsimplify(xstar)
M2 = g1x.subs(x, xstar)
M2_val = sp.N(M2, 30)
xstar_val = sp.N(xstar, 30)
print("x* =", xstar_val)
print("M_2 = g1(x*) =", M2_val)

# cross check against target claim
target_M2 = sp.Float("0.71072657606222206206", 30)
target_xstar = sp.Float("0.58975451230145838428", 30)
print("front's claimed M_2 =", target_M2, " diff =", M2_val - target_M2)
print("front's claimed x*  =", target_xstar, " diff =", xstar_val - target_xstar)

# Confirm x* is the root of 2t^3+t-1=0 in (0,1), and that this is the ARGMAX
# location (not the function value) -- explicit distinction check.
cubic = 2*t**3 + t - 1
cubic_roots = sp.Poly(cubic, t).real_roots()
print("real roots of 2t^3+t-1=0:", [sp.N(r,30) for r in cubic_roots])
cubic_root_in01 = [r for r in cubic_roots if 0 < r < 1][0]
print("root of cubic in (0,1):", sp.N(cubic_root_in01, 30))
print("matches x* (argmax location)?", sp.simplify(cubic_root_in01 - xstar) == 0)
print("NOTE: the cubic ROOT equals x*=0.58975..., which is the ARGMAX x-location,")
print("      NOT M_2. M_2=0.71072... is g_1 evaluated AT that root (a different number).")
print("Value of the root itself (for contrast):", sp.N(cubic_root_in01, 15), " != M_2 =", sp.N(M2,15))

# Confirm g1'(x*) = 0 exactly (symbolically, via the algebraic relation of the root)
check = sp.simplify(g1p.subs(x, cubic_root_in01))
print("g1'(x*) simplified (should be 0):", check)

print()
print("="*70)
print("(c) elementary sign argument: n >= 4 threshold re-derivation")
print("="*70)
# Front's claim: n*Delta_n(x) = g1(x) + p(x)/(n-1), p(x) = -x^4 - x
# derive independently: n*Delta_n(x) - g1(x) should equal p(x)/(n-1)
p_claimed = -x**4 - x
check2 = sp.simplify(rem - p_claimed/(n-1))
print("[n*Delta_n(x)-g1(x)] - p(x)/(n-1), p=-x^4-x  (expect 0):", check2)

# Confirm g1(x) >= 0 on [0,1] and p(x) <= 0 on [0,1] elementarily (Poly real_roots
# based sign scan, not sampling): check g1 has no interior sign change other than
# at endpoints; same for p.
print("g1(0), g1(1):", g1x.subs(x,0), g1x.subs(x,1))
print("p(0), p(1):", p_claimed.subs(x,0), p_claimed.subs(x,1))
g1_roots_01 = sp.Poly(g1x, x).real_roots()
p_roots_01 = sp.Poly(p_claimed, x).real_roots()
print("real roots of g1(x)=0:", g1_roots_01)
print("real roots of p(x)=0:", p_roots_01)
# min of p on [0,1]: p is strictly decreasing since p'(x) = -4x^3-1 < 0 for x>=0
pprime = sp.diff(p_claimed, x)
print("p'(x) =", pprime, " -- at x in [0,1], max value of p':", sp.N(pprime.subs(x,1),10), "(should be <0)")
p_min = p_claimed.subs(x,1)
print("p(1) = min of p on [0,1] =", p_min)

# threshold: 2/(n-1) <= M2  <=>  n >= 1+2/M2
thresh = 1 + 2/M2
print("threshold n >= 1+2/M2 =", sp.N(thresh, 15))
import math
print("means smallest integer n is", math.ceil(float(sp.N(thresh,15))) if float(sp.N(thresh,15))!=math.ceil(float(sp.N(thresh,15))) else math.ceil(float(sp.N(thresh,15))))

print()
print("="*70)
print("(d) direct numeric spot-checks of |Delta_n(x)| <= M2/n at n=4,5,10,50")
print("="*70)
M2_f = float(M2_val)
import random
random.seed(12345)  # independent, unrelated to reserved block, purely for adversarial spot-check reproducibility
worst = {}
for nn in [4,5,10,50]:
    bound = M2_f/nn
    xs = [i/2000 for i in range(0,2001)]
    maxviol = -1e9
    worst_x = None
    worst_val = None
    for xx in xs:
        dv = float(Delta.subs({n:nn, x:xx}))
        av = abs(dv)
        ratio = av/bound
        if ratio > maxviol:
            maxviol = ratio
            worst_x = xx
            worst_val = av
    worst[nn] = (worst_x, worst_val, bound, maxviol)
    status = "OK" if maxviol <= 1.0 + 1e-9 else "VIOLATION"
    print(f"n={nn}: bound=M2/n={bound:.8f}  worst |Delta_n(x)| at x~{worst_x:.4f} = {worst_val:.8f}  ratio={maxviol:.6f}  [{status}]")
