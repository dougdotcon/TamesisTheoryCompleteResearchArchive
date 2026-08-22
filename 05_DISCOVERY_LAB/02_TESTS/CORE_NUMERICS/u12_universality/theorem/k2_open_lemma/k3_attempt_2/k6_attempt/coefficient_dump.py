"""
ATTEMPT.md Sec.3.2: extract and factor the G_r(t,b) coefficients d_k^{(r)}(b), r=1..8,
from rate_ode_data.pkl (produced by rate_ode.py), to show the pattern that led to the
Sec.3.3 closed-form conjecture (numerator = C(k+2,2) * r!/(r-k-1)!, denominator =
prod_{i=1}^{k+2}(r+b+i)).
"""
import pickle
import sympy as sp

t, b = sp.symbols('t b', nonnegative=True)

with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/rate_ode_data.pkl', 'rb') as f:
    data = pickle.load(f)
G = data['G']

for r in range(1, 9):
    poly = sp.Poly(sp.expand(G[r]), t)
    coeffs = {m[0]: c for c, m in zip(poly.coeffs(), poly.monoms())}
    print(f"r={r}:")
    for k in sorted(coeffs):
        num, den = sp.fraction(sp.together(coeffs[k]))
        print(f"   d_{k}^({r})(b) = {sp.factor(num)} / {sp.factor(den)}")
