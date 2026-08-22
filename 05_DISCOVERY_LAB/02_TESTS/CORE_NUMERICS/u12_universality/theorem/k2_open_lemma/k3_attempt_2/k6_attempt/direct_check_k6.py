"""
Independent, non-symbolic (fast polynomial-time) check of the K=6 closed form
against markov_direct.py's memoized exact-Fraction recursion (same transition rules
as markov_transfer.py, proved general in K in ATTEMPT.md Sec.2, but re-implemented
independently there without symbolic algebra).
"""
import sys
from fractions import Fraction as F
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
from markov_direct import psi_markov

# K=6 closed form (from markov_transfer.psi_closed_form(6), computed separately):
def psi6_closed(n):
    n = F(n)
    num = 2048*n**6 + 3072*n**5 + 4293*n**4 + 4638*n**3 + 3529*n**2 + 1662*n + 360
    den = 6006*n**6
    return num/den

allok = True
for n in range(7, 26):
    mine = psi_markov(n, 6)
    closed = psi6_closed(n)
    ok = (mine == closed)
    allok = allok and ok
    print(f"n={n}: direct_recursion={mine}  closed_form={closed}  {'OK' if ok else 'MISMATCH'}", flush=True)

print("ALL MATCH" if allok else "SOME MISMATCH")
