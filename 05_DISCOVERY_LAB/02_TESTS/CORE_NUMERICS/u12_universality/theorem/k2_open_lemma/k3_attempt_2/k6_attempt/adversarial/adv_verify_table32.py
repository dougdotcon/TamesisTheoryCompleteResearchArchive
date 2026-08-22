"""
PART B, supplementary spot-check: independently confirm every entry of
ATTEMPT.md Sec.3.2's table (G_r(1,0) vs r*phi_r/4, r=1..8), using the
already-independently-proved closed form for d_k^{(r)}(b) (adv_verify_d_
recursion_part2.py) evaluated directly at b=0, t=1, with fresh plain-
Fraction code (no sympy, no import of any document script).
"""
from fractions import Fraction as F


def d_k_r_0(rr, kk):
    falling = 1
    for i in range(rr - kk, rr + 1):
        falling *= i
    den = 1
    for i in range(1, kk + 3):
        den *= (rr + i)
    return F((kk + 1) * (kk + 2), 2) * F(falling, den)


def phi(r):
    fact_r = 1
    for i in range(1, r + 1):
        fact_r *= i
    fact_2r1 = 1
    for i in range(1, 2 * r + 2):
        fact_2r1 *= i
    return F(4 ** r * fact_r * fact_r, fact_2r1)


table = {1: '1/6', 2: '4/15', 3: '12/35', 4: '128/315', 5: '320/693',
         6: '512/1001', 7: '3584/6435', 8: '65536/109395'}
allok = True
for r in range(1, 9):
    S = sum(d_k_r_0(r, k) for k in range(0, r))
    target = F(r, 4) * phi(r)
    doc_ok = (str(S) == table[r])
    ok = (S == target) and doc_ok
    allok = allok and ok
    print(f"r={r}: G_r(1,0)={S}  r*phi_r/4={target}  match={S==target}  "
          f"doc_table_value={table[r]}  matches_document={doc_ok}")
print("ALL 8 ENTRIES OF SEC.3.2's TABLE INDEPENDENTLY CONFIRMED:", allok)
