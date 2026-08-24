"""
Independent K=2 reduction check (mirrors ATTEMPT.md section 5), built
fresh (not reading r2_k2_reduction_check.py). Applies the SAME general
shape-classification method (cycle detection on 2 nodes, targets in
{1,2,OUT}) to confirm it reproduces the already-proved f_{M_2}=4x(1-x^2).
"""
import sympy as sp
from itertools import product

m1, m2 = sp.symbols('m1 m2', positive=True)
M = {1: m1, 2: m2}
m0 = 1 - m1 - m2
NODES = [1, 2]

def cycle_nodes(g):
    on_cycle = set()
    for start in NODES:
        seen = []
        cur = start
        for _ in range(3):
            if cur == 'OUT':
                break
            if cur in seen:
                idx = seen.index(cur)
                cyc = seen[idx:]
                if start in cyc:
                    on_cycle.add(start)
                break
            seen.append(cur)
            cur = g[cur]
    return on_cycle

def classify(g):
    oc = cycle_nodes(g)
    if len(oc) == 0:
        return 'T0'
    cycles = []
    visited = set()
    for i in oc:
        if i in visited: continue
        cyc = [i]; cur = g[i]
        while cur != i:
            cyc.append(cur); cur = g[cur]
        visited.update(cyc)
        cycles.append(frozenset(cyc))
    sizes = sorted(len(c) for c in cycles)
    if sizes == [1]: return 'T1a'   # single self-loop, other off
    if sizes == [1,1]: return 'T2'  # both self-loop
    if sizes == [2]: return 'T2cyc' # the 2-cycle
    raise ValueError(sizes)

targets = [1, 2, 'OUT']
shape_prob = {}
shape_count = {}
for combo in product(targets, repeat=2):
    g = {1: combo[0], 2: combo[1]}
    shape = classify(g)
    prob = 1
    for i in NODES:
        t = g[i]
        prob *= (M[t] if t != 'OUT' else m0)
    shape_prob[shape] = shape_prob.get(shape, 0) + prob
    shape_count[shape] = shape_count.get(shape, 0) + 1

print("Raw config counts:", shape_count, " total=", sum(shape_count.values()), "(should be 9)")

def tri_integral(expr):
    e = sp.integrate(expr, (m2, 0, 1-m1))
    e = sp.integrate(e, (m1, 0, 1))
    return sp.nsimplify(sp.simplify(e))

print("\nTarget-level probabilities (density 2 on triangle):")
for k,v in shape_prob.items():
    print(f"  {k}: P = {tri_integral(2*sp.expand(v))}")

# Now build densities via the SAME "M2 = 1 - offcycle_m - oncycle_P" rule,
# verified using the independent per-shape continuum MC method (fast, N large)
import numpy as np
rng = np.random.default_rng(np.random.SeedSequence(20260844030))
N = 4_000_000
g = rng.standard_gamma(1.0, size=(N,3))
g /= g.sum(axis=1, keepdims=True)
m1v, m2v, m0v = g[:,0], g[:,1], g[:,2]
u1 = rng.random(N); u2 = rng.random(N)

def region_offset(u, m1v, m2v):
    b1 = m1v; b2 = m1v+m2v
    r = np.full(N, 3, dtype=np.int8)  # 3=OUT
    P = np.zeros(N)
    in1 = u < b1
    in2 = (~in1) & (u < b2)
    inO = (~in1) & (~in2)
    r[in1]=1; P[in1]=u[in1]
    r[in2]=2; P[in2]=u[in2]-b1[in2]
    r[inO]=3; P[inO]=u[inO]-b2[inO]
    return r, P

g1,P1 = region_offset(u1,m1v,m2v)
g2,P2 = region_offset(u2,m1v,m2v)

self1 = (g1==1); self2=(g2==2)
cyc2  = (g1==2)&(g2==1)
oncyc1 = self1 | cyc2
oncyc2 = self2 | cyc2

mmv = {1: m1v, 2: m2v}
target_m1 = np.where(g1==1, m1v, np.where(g1==2, m2v, 0))
target_m2 = np.where(g2==1, m1v, np.where(g2==2, m2v, 0))
nm = np.where(oncyc1, target_m1-P1, 0.0) + np.where(oncyc2, target_m2-P2, 0.0)
M2 = (1-m1v-m2v) + nm

is_T0 = (~oncyc1)&(~oncyc2)
is_T1a = (self1 & ~self2 & ~cyc2) | (self2 & ~self1 & ~cyc2)
is_T2  = self1 & self2
is_T2cyc = cyc2

print("\nShape sample counts:", is_T0.sum(), is_T1a.sum(), is_T2.sum(), is_T2cyc.sum(), " sum=", is_T0.sum()+is_T1a.sum()+is_T2.sum()+is_T2cyc.sum(), "of", N)

from scipy import stats
x = sp.symbols('x')
f_self = 2*x*(1-x**2)          # claimed: matches K2's f_B+f_C
f_bothself = x**2*(1-x)
f_2cyc = x**2*(1-x)
f_T0 = 2*x*(1-x)

for name, mask, fexpr, Pexact in [('single-self(T1a)', is_T1a, f_self, sp.Rational(1,2)),
                                    ('both-self(T2)', is_T2, f_bothself, sp.Rational(1,12)),
                                    ('2cycle', is_T2cyc, f_2cyc, sp.Rational(1,12)),
                                    ('T0', is_T0, f_T0, sp.Rational(1,3))]:
    samples = M2[mask]
    cdf_expr = sp.integrate(fexpr,(x,0,x))/Pexact
    cdf_func = sp.lambdify(x, cdf_expr, 'numpy')
    D,p = stats.kstest(samples, cdf_func)
    print(f"{name}: n={mask.sum()} p_hat={mask.sum()/N:.5f} target_P={float(Pexact):.5f}  KS D={D:.5f} p={p:.4f}")

total = sp.expand(f_self + f_bothself + f_2cyc + f_T0)
print("\nSum of 4 group densities:", total, " vs 4x(1-x^2)=", sp.expand(4*x*(1-x**2)))
print("Match:", sp.simplify(total - 4*x*(1-x**2))==0)
