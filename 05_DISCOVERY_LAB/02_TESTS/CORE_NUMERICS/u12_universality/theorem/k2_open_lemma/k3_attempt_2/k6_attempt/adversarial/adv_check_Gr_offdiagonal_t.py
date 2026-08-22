"""
PART B, item 4 continued -- the G_r (O(1/n) term) analogue of
adv_check_offdiagonal_t.py, and the MORE important one: unlike F_r
(which is a priori bounded in [0,1] since g_r itself is a probability --
an argument that rules out a homogeneous-solution admixture C*t^{-(1+r+b)}
at the F_r level, independently reconstructed by this referee since
ATTEMPT.md's own promised "Sec.2.4" elaboration of this point does not
exist anywhere in the document -- see REFEREE_REPORT.md), G_r is an
UNBOUNDED O(1/n) correction term with NO analogous a priori bound. If a
homogeneous-solution-type discrepancy were going to show up anywhere
undetected by the document's own (t=1-only) checks, this is the place to
look for it: at t far from 1.

Ground truth: B_r(t,b) := lim_{n->infty} n*[g_r(n*t,b) - F_r(t,b)], computed
DIRECTLY from markov_transfer's own exact (m,b,n)-symbolic g_r output
(pattern_data.pkl) -- totally independent of the whole continuum-ODE
machinery -- compared against ATTEMPT.md Sec.3.3's claimed G_r(t,b) closed
form, at t=1/2, 1/3, 2/3 (not just t=1), for r=1..5, symbolic b.
"""
import sys
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt
import pickle
import time

n_sym = mt.n
b_sym = mt.b
m_sym = mt.m

with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/pattern_data.pkl', 'rb') as f:
    data = pickle.load(f)
g_full = data['g_full']


def F_closed_doc(r_val, t_val, b_val):
    total = 0
    for kk in range(0, r_val + 1):
        coeff = sp.factorial(r_val) / sp.factorial(r_val - kk)
        denom = 1
        for i in range(1, kk + 2):
            denom *= (r_val + b_val + i)
        total += coeff * t_val**kk / denom
    return total


def G_closed_doc(r_val, t_val, b_val):
    total = 0
    for kk in range(0, r_val):
        num = sp.Rational((kk + 1) * (kk + 2), 2) * sp.factorial(r_val) / sp.factorial(r_val - kk - 1)
        den = 1
        for i in range(1, kk + 3):
            den *= (r_val + b_val + i)
        total += num * t_val**kk / den
    return total


t_values = [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3)]

print("=" * 78)
print("Testing G_r(t,b) at t != 1 against the TRUE n->infinity 1/n-coefficient")
print("of markov_transfer's own exact g_r(m,b), r=1..5, general symbolic b.")
print("(This is the check ATTEMPT.md itself never performs -- everywhere in")
print(" the document, G_r is only ever checked at t=1.)")
print("=" * 78)

all_match = True
for rv in range(1, 6):
    for tv in t_values:
        t0 = time.time()
        expr = g_full[rv].subs(m_sym, n_sym * tv)
        F_true = sp.limit(expr, n_sym, sp.oo)
        B_true = sp.limit((expr - F_true) * n_sym, n_sym, sp.oo)
        B_true = sp.simplify(B_true)
        pred = sp.simplify(G_closed_doc(rv, tv, b_sym))
        diff = sp.simplify(pred - B_true)
        ok = (diff == 0)
        all_match = all_match and ok
        dt = time.time() - t0
        print(f"r={rv} t={tv}: true_B_r(b)={B_true}")
        print(f"           pred_G_r(b)={pred}")
        print(f"           match={ok}  ({dt:.1f}s)")
    print()

print("ALL MATCH (G_r away from t=1, general b, r=1..5):", all_match)
