"""
Referee check: does the target's K=4 lower-bound proof, AS WRITTEN, have
a complete logical chain for integer n>=65 (the region "covered" by
Step 6's n>64.77 elimination threshold)?

Step 6 shows: no real x (unrestricted) with dN/dx=0 has h(n,x)=-M4, for
real n>64.768366... This rules out h(n,x)=-M4 EXACTLY at any interior
critical point for n in that ray. Combined with the boundary facts
(h(n,0)=0, h(n,1)>-M4 for n>=6), this shows m(n):=min_x h(n,x) is NEVER
EXACTLY -M4 for real n>64.77. But non-equality alone does not pin the
SIGN of m(n)-(-M4) without an anchor point + IVT/continuity argument,
which is not explicitly given in the target's script for this specific
unbounded tail (unlike the upper bound, which explicitly anchors at
a(6)). This script:
  1. Directly, exactly computes m(n) for several n > 64.77 (65, 70, 100,
     1000) via the SAME real_roots-based method as the exhaustive patch,
     to confirm no violation exists there (closing the gap empirically
     with the same exactness standard used elsewhere in this document).
  2. Establishes the actually-missing ingredient explicitly: g_4(x)>=0
     on [0,1] (via real_roots, independent of predecessor), which
     together with the uniform-in-x convergence h(n,x)->g_4(x) (a
     standard consequence of the deg_n N = deg_n D - 1 structural fact
     already used in Step 1 of both scripts) legitimately anchors the
     n->infinity end of the IVT argument, completing the proof.
"""
import sympy as sp
import pickle

n, x = sp.symbols('n x')

with open('/tmp/claude-0/-home-user-TamesisTheoryCompleteResearchArchive/e9ab1ff0-e9f9-5b73-816d-aec417acf7b1/scratchpad/k4_Nx_Dn.pkl','rb') as f:
    d = pickle.load(f)
Nx, Dn = d['Nx'], d['Dn']

g4 = -6*x**8 + 8*x**7 + 6*x**6 - 12*x**5 + 6*x**4 - 6*x**2 + 4*x
g4p_poly = sp.Poly(sp.diff(g4,x), x)
x4star = [r for r in g4p_poly.real_roots() if 0 < r < 1][0]
M4 = sp.simplify(g4.subs(x, x4star))
M4_num = sp.N(M4, 30)

def sup_inf_h_exact(nv):
    Numn = sp.expand(Nx.subs(n, nv))
    Dnn = Dn.subs(n, nv)
    hx = sp.cancel(nv*Numn/Dnn)
    hpoly = sp.Poly(hx, x)
    dpoly = hpoly.diff(x)
    crit = sp.Poly(dpoly, x).real_roots()
    cand = [c for c in crit if 0 <= c <= 1] + [sp.Integer(0), sp.Integer(1)]
    vals = [(c, sp.N(hpoly(c), 30)) for c in cand]
    hi = max(vals, key=lambda cv: cv[1])
    lo = min(vals, key=lambda cv: cv[1])
    return hi, lo

print("="*70)
print("Part 1: direct exact check that the alleged 'gap' (n>=65, not")
print("explicitly anchored in the target's own proof) is in fact safe")
print("="*70)
for nv in [65, 70, 100, 1000]:
    hi, lo = sup_inf_h_exact(nv)
    ok_lower = lo[1] > -M4_num
    ok_upper = hi[1] < M4_num
    print(f"n={nv:5d}: min_x h = {float(lo[1]):+.8f} (>-M4? {ok_lower})   "
          f"max_x h = {float(hi[1]):+.8f} (<M4? {ok_upper})")

print()
print("="*70)
print("Part 2: establish g_4(x) >= 0 on [0,1] directly (closes the")
print("missing anchor: as n->infinity, h(n,x)->g_4(x) pointwise/uniformly")
print("on the compact [0,1] since deg_n N = deg_n D - 1, a structural")
print("fact already used in both scripts' own Step 1 -- hence m(n) ->")
print("min_x g_4(x) >= 0 > -M4, anchoring the IVT argument for the whole")
print("unbounded ray n>64.77, which the target's own script leaves implicit)")
print("="*70)
g4_poly = sp.Poly(g4, x)
g4_roots = g4_poly.real_roots()
g4_roots_in_01 = [r for r in g4_roots if sp.N(r) >= 0 and sp.N(r) <= 1]
print("real roots of g4(x) itself:", g4_roots)
print("roots landing in [0,1]:", g4_roots_in_01)
# check sign at a few sample points
import random as _r  # only for a quick internal sanity spot-check, not used in any proof
samples = [sp.Rational(i,20) for i in range(0,21)]
neg_found = [s for s in samples if sp.N(g4.subs(x,s)) < 0]
print("any sample point in [0,1] with g4<0?:", neg_found)
print("g4(0) =", g4.subs(x,0), "  g4(1) =", sp.simplify(g4.subs(x,1)))
