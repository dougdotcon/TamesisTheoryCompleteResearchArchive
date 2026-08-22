"""
PART B, item 4 (adversarial referee, k6_attempt) -- THE CENTRAL QUESTION.

A specific, substantive stress-test that ATTEMPT.md itself never performs:
every single cross-check in the document (Sec.2.3's table, Sec.3.3's B_r(b)
cross-check, Sec.3.4's rate matches) evaluates F_r/G_r ONLY AT t=1 (since
psi_n^{(K)} = g_K(n,0), i.e. m=n, i.e. t=m/n=1 exactly). The homogeneous
solution of the governing ODE (t X'(t) + (1+r+b)X(t) = 0) is
X(t) = C*t^{-(1+r+b)}, which importantly EQUALS 1 at t=1 for ANY (1+r+b) --
so a nonzero homogeneous admixture at any t=1-only check would be invisible
UNLESS it shows up as an extra additive constant (which the t=1 checks DO
catch, since they compare against exact numbers). But the coefficient-by-
coefficient shape of F_r(t,b)/G_r(t,b) AWAY from t=1 -- the actual polynomial
structure the "diagonal coefficient matching" argument produces -- is NEVER
compared against the true (m,b)-symbolic exact discrete data at any t != 1
anywhere in the document.

This script does exactly that: using markov_transfer.py's own exact,
independently-derived (m,b)-symbolic g_r(m,b) data (pattern_data.pkl, r=0..5,
the SAME ground truth the document's own t=1 checks use), compute
F_r(t,b) := lim_{n->infty} g_r(n*t, b) at SEVERAL VALUES OF t < 1 (not just
t=1), and compare against ATTEMPT.md Sec.2.3's closed form.

This is a genuinely new check, not present anywhere in ATTEMPT.md, aimed
directly at task item B.4(b): does the polynomial-in-t ansatz actually match
the true asymptotic shape away from the single point t=1, or could a
homogeneous-solution-type discrepancy be lurking there (invisible to a
t=1-only check unless it happens to also perturb the t=1 value)?
"""
import sys
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt
import pickle

n_sym = mt.n
b_sym = mt.b
m_sym = mt.m

with open('/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/pattern_data.pkl', 'rb') as f:
    data = pickle.load(f)
g_full = data['g_full']  # g_full[r] = g_r(m,b) EXACT, symbolic in m, b, n


def F_closed_doc(r_val, t_val, b_val):
    """ATTEMPT.md Sec.2.3's claimed closed form for F_r(t,b)."""
    total = 0
    for kk in range(0, r_val + 1):
        coeff = sp.factorial(r_val) / sp.factorial(r_val - kk)
        denom = 1
        for i in range(1, kk + 2):
            denom *= (r_val + b_val + i)
        total += coeff * t_val**kk / denom
    return total


print("=" * 78)
print("Testing F_r(t,b) at t = 1/2, 1/3, 2/3, 3/4 (NOT just t=1) against the")
print("TRUE n->infinity limit of markov_transfer's own exact g_r(m,b), r=0..5,")
print("general symbolic b.")
print("=" * 78)

t_values = [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(3, 4), sp.Rational(1, 5)]

all_match = True
for rv in range(0, 6):
    for tv in t_values:
        expr = g_full[rv].subs(m_sym, n_sym * tv)
        true_limit = sp.limit(expr, n_sym, sp.oo)
        true_limit = sp.simplify(true_limit)
        pred = sp.simplify(F_closed_doc(rv, tv, b_sym))
        diff = sp.simplify(pred - true_limit)
        ok = (diff == 0)
        all_match = all_match and ok
        print(f"r={rv} t={tv}: true_limit(b)={true_limit}   pred(b)={pred}   match={ok}")
    print()

print("ALL MATCH (F_r away from t=1, general b, r=0..5):", all_match)
