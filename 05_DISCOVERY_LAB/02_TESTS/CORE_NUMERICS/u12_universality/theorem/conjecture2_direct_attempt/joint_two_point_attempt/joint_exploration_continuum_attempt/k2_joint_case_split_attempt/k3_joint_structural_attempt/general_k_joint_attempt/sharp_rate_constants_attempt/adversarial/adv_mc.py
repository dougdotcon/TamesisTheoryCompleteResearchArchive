#!/usr/bin/env python3
"""
Independent re-run of the Monte Carlo stress test, using MY OWN
independently-derived Delta_n(x) expressions (built from scratch above in
adv_k2.py/adv_k3.py/adv_k4.py, re-derived here again standalone), with the
SAME seeds the front used (20260929001-003, read from ATTEMPT.md/its script,
not invented by me) to check reproducibility of their claimed worst-ratios.
"""
import random
import sympy as sp

n, x, k = sp.symbols('n x k')

# K=2
D2_k = k*(k+1)*(2*n**2-3*n+k-k**2)/(n**3*(n-1))
F2 = 1-(1-x**2)**2
Delta2 = sp.cancel(D2_k.subs(k, n*x) - F2)

# K=3
D3_k = k*(k+1)*( k**4 - 4*k**3 - (3*n**2-9*n-5)*k**2 + (3*n**2-11*n-2)*k
                  + (3*n**4-12*n**3+12*n**2+2*n) ) / (n**4*(n-1)*(n-2))
F3 = 1-(1-x**2)**3
Delta3 = sp.cancel(D3_k.subs(k, n*x) - F3)

# K=4
Q = ( -k**6 + 9*k**5 + (4*n**2-18*n-31)*k**4 + (-16*n**2+80*n+51)*k**3
      + (-6*n**4+42*n**3-55*n**2-120*n-40)*k**2
      + (6*n**4-50*n**3+97*n**2+70*n+12)*k
      + 4*n**6-30*n**5+74*n**4-52*n**3-30*n**2-12*n )
D4_k = k*(k+1)*Q / (n**5*(n-1)*(n-2)*(n-3))
F4 = 1-(1-x**2)**4
Delta4 = sp.cancel(D4_k.subs(k, n*x) - F4)

DELTA = {2: Delta2, 3: Delta3, 4: Delta4}
C_CONST = {
    2: sp.Float("0.71072657606222206206", 50),
    3: sp.Float("0.7183335821861240008038727732851894951722", 50),
    4: sp.Float("0.7345569184500456912259247911642612891263", 50),
}
DOMAIN_N0 = {2: 4, 3: 6, 4: 6}
SEEDS = {2: 20260929001, 3: 20260929002, 4: 20260929003}
NSAMPLES = 3000
NMAX = 10**6

for K in (2, 3, 4):
    rng = random.Random(SEEDS[K])
    expr = DELTA[K]
    worst_ratio = None
    worst_case = None
    nviol = 0
    for _ in range(NSAMPLES):
        nn = rng.randint(DOMAIN_N0[K], NMAX)
        xnum = rng.randint(0, 10**6)
        xx = sp.Rational(xnum, 10**6)
        val = abs(sp.N(expr.subs({n: sp.Integer(nn), x: xx}), 50))
        bound = C_CONST[K] / nn
        ratio = float(val / bound)
        if worst_ratio is None or ratio > worst_ratio:
            worst_ratio = ratio
            worst_case = (nn, xx)
        if ratio > 1.0 + 1e-9:
            nviol += 1
    print(f"[K={K}] seed={SEEDS[K]}  worst ratio={worst_ratio:.10f} at n,x={worst_case}  violations={nviol}/{NSAMPLES}")
