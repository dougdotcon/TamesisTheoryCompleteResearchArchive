"""
ATTEMPT.md Sec.2.3: verify the closed-form F_r(t,b) = sum_{k=0}^r [r!/(r-k)!] * t^k /
prod_{i=1}^{k+1}(r+b+i) against (a) the exact n->infinity limit of markov_transfer.py's
own g_r(m,b) output (pattern_data.pkl, r=0..5, full b-dependence) and (b) the Wallis
integral phi_K = 4^K(K!)^2/(2K+1)! at t=1,b=0, r=0..6.
"""
import sys
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt
import pickle

b = mt.b
n, mm = mt.n, mt.m


def F_closed(r_val, t_val, b_val):
    total = 0
    for kk in range(0, r_val + 1):
        coeff = sp.factorial(r_val) / sp.factorial(r_val - kk)
        denom = 1
        for i in range(1, kk + 2):
            denom *= (r_val + b_val + i)
        total += coeff * t_val**kk / denom
    return total


with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/pattern_data.pkl', 'rb') as f:
    data = pickle.load(f)
g_full = data['g_full']

print("=== F_r(1,b) vs exact n->infinity limit of markov_transfer's g_r(n,b), r=0..5 ===")
allmatch = True
for rv in range(0, 6):
    pred = F_closed(rv, 1, b)
    expr = g_full[rv].subs(mm, n)
    A = sp.limit(expr, n, sp.oo)
    diff = sp.cancel(sp.together(pred - A))
    ok = (diff == 0)
    allmatch = allmatch and ok
    print(f"r={rv}: A(b)={A}  match={ok}")
print("ALL MATCH:", allmatch)

print()
print("=== F_r(1,0) vs phi_K (Wallis integral), r=0..6 ===")
allmatch2 = True
for rv in range(0, 7):
    pred0 = sp.simplify(F_closed(rv, 1, 0))
    phiK = sp.Rational(4**rv * sp.factorial(rv)**2, sp.factorial(2 * rv + 1))
    ok = sp.simplify(pred0 - phiK) == 0
    allmatch2 = allmatch2 and ok
    print(f"r={rv}: F_r(1,0)={pred0}  phi_{rv}={phiK}  match={ok}")
print("ALL MATCH:", allmatch2)
