# Adversarial referee, sharp_constant_monotonicity_attempt -- Part 2:
#   Theorem 1:  Q(n) < sqrt(pi n/2) - 1/3 + (1/11) sqrt(pi/(2n))  for every n>=1.
#
#   (A) every step of the proof chain re-derived / re-checked, incl. n=1 edge;
#   (B) CERTIFIED-RATIONAL verification: exact Fraction Q(n) vs. a rational
#       LOWER bound of the RHS built only from integer arithmetic (isqrt) and
#       the classical decimal bounds on pi -- no floating point in the verdict;
#       dense n=1..800 plus sparse to n=12000 (exceeding the target's exact
#       range of 600/10000);
#   (C) high-precision margin scan to n=10^6 (mpmath, Q(n) summed directly from
#       its own defining product with a certified truncation bound), confirming
#       the margin ~ (1/132) sqrt(pi/(2n)) -> 0+ but never nonpositive.
# No randomness. None of the target's scripts/logs was read.
import sys
from fractions import Fraction as F
from math import isqrt
import mpmath as mp

mp.mp.dps = 60
LOG = []
def log(s=""):
    print(s)
    LOG.append(str(s))
fails = 0

# classical decimal bounds on pi (cross-checked against mpmath below)
PI_LO = F(31415926535897932, 10**16)
PI_HI = F(31415926535897933, 10**16)
pi_ok = mp.mpf(PI_LO.numerator)/mp.mpf(PI_LO.denominator) < mp.pi < mp.mpf(PI_HI.numerator)/mp.mpf(PI_HI.denominator)
log(f"pi bracket sanity vs mpmath(60dps): {pi_ok}")
if not pi_ok: fails += 1

D = 10**30  # denominator scale for certified square roots

def sqrt_lo(fr):
    """rational r <= sqrt(fr), via isqrt (floor)."""
    x = (fr.numerator * D * D) // fr.denominator
    return F(isqrt(x), D)

def sqrt_hi(fr):
    """rational r >= sqrt(fr), via isqrt (ceil)."""
    x = -((-fr.numerator * D * D) // fr.denominator)   # ceil division
    return F(isqrt(x) + 1, D)

def Q_exact(n):
    t = n ** (n - 1)
    tot = t
    for j in range(1, n):
        t = (t // n) * (n - j)
        tot += t
    return F(tot, n ** (n - 1))

def rhs_lower(n):
    """certified rational LOWER bound of sqrt(pi n/2) + (1/11)sqrt(pi/(2n)) - 1/3."""
    return sqrt_lo(PI_LO * n / 2) + F(1, 11) * sqrt_lo(PI_LO / (2 * n)) - F(1, 3)

log("")
log("=" * 78)
log("(A) THE PROOF CHAIN, STEP BY STEP (referee re-derivation)")
log("=" * 78)
log(" 1. Lemma 1 (independently re-proved, Part 1):  Q(n) = A(n)/2 - theta(n),")
log("    A(n) = n! e^n / n^n.")
log(" 2. Robbins (correct form, Part 1):  A(n) < sqrt(2 pi n) e^{1/(12n)},")
log("    STRICT for every n>=1  =>  A(n)/2 < sqrt(pi n/2) e^{1/(12n)}.")
log(" 3. FGKP95 lower bound: theta(n) >= 1/3 + 4/(135(n+8/45)) > 1/3, STRICT.")
log(" 4. e^x <= 1/(1-x) on [0,1): equivalent to 1-x <= e^{-x} (true for all real")
log("    x, strict for x != 0); x = 1/(12n) in (0, 1/12] subset [0,1) for n>=1. OK")
log(" 5. e^{1/(12n)} <= 12n/(12n-1) = 1 + 1/(12n-1); 12n-1 >= 11n <=> n >= 1,")
log("    equality exactly at n=1;  sqrt(pi n/2)/(12n-1) <= sqrt(pi n/2)/(11n)")
log("    = (1/11) sqrt(pi/(2n)).   All steps valid for EVERY n>=1; the strict")
log("    steps 2-3 make the assembled bound strict at every n>=1.")
log("    Domain notes: step 4 needs x<1 (true, x<=1/12); step 5's division by")
log("    12n-1 needs 12n-1>0 (true).  n=1 edge: x=1/12, 12n-1=11=11n (equality),")
log("    all inequalities remain valid.")

# symbolic cross-check of the two rewrites used
import sympy as sp
nsym = sp.symbols('n', positive=True)
chk1 = sp.simplify(sp.sqrt(sp.pi*nsym/2)/(11*nsym) - sp.sqrt(sp.pi/(2*nsym))/11)
chk2 = sp.simplify(12*nsym/(12*nsym-1) - (1 + 1/(12*nsym-1)))
log(f"    sympy: sqrt(pi n/2)/(11n) - (1/11)sqrt(pi/(2n)) == {chk1};  "
    f"12n/(12n-1) - (1+1/(12n-1)) == {chk2}")
if chk1 != 0 or chk2 != 0: fails += 1

log("")
log("=" * 78)
log("(B) CERTIFIED-RATIONAL VERIFICATION,  Q(n) < RHS  (exact Fraction vs")
log("    rational lower bound of RHS; verdict involves NO floating point)")
log("=" * 78)
dense = list(range(1, 801))
sparse = [900, 1000, 1200, 1500, 2000, 3000, 5000, 8000, 12000]
viol = []
worst_margin = None
mp_margins = {}
for n in dense + sparse:
    q = Q_exact(n)
    rl = rhs_lower(n)
    if not (q < rl):
        viol.append(n)
    # display margin via mpmath (display only, not the verdict)
    m = (mp.sqrt(mp.pi*n/2) + mp.sqrt(mp.pi/(2*n))/11 - mp.mpf(1)/3
         - mp.mpf(q.numerator)/mp.mpf(q.denominator))
    mp_margins[n] = m
    if worst_margin is None or m < worst_margin[0]:
        worst_margin = (m, n)
log(f"  {len(dense)+len(sparse)} points (dense 1..800 + sparse to 12000), "
    f"violations: {viol if viol else 'NONE -- Q(n) < RHS certified at every point'}")
log(f"  margin at n=1:      {mp.nstr(mp_margins[1], 6)}   (target document reports 0.0339)")
log(f"  margin at n=12000:  {mp.nstr(mp_margins[12000], 6)}")
log(f"  smallest margin:    {mp.nstr(worst_margin[0], 6)} at n={worst_margin[1]}")
if viol: fails += 1

q1 = Q_exact(1)
log(f"  n=1 edge exact: Q(1) = {q1}; certified rational RHS lower bound = "
    f"{float(rhs_lower(1)):.6f} > 1: {q1 < rhs_lower(1)}")

log("")
log("=" * 78)
log("(C) DEEP MARGIN SCAN to n = 10^6 (mpmath 60dps; Q(n) summed directly from")
log("    its own product definition, truncated when P_j < 10^-50 -- certified")
log("    tail < n * 10^-50 <= 10^-44, far below every observed margin)")
log("=" * 78)

def Q_direct(n):
    P = mp.mpf(1)
    tot = mp.mpf(1)
    tiny = mp.mpf(10) ** (-50)
    for j in range(1, n):
        P *= (1 - mp.mpf(j) / n)
        tot += P
        if P < tiny:
            break
    return tot  # tail terms are decreasing, < tiny each, < n of them

for n in [10**4, 3*10**4, 10**5, 3*10**5, 10**6]:
    q = Q_direct(n)
    bound = mp.sqrt(mp.pi*n/2) + mp.sqrt(mp.pi/(2*n))/11 - mp.mpf(1)/3
    margin = bound - q
    pred = mp.sqrt(mp.pi/(2*n)) / 132   # expected leading margin (1/11-1/12)
    ok = margin > mp.mpf(10) ** (-40)
    log(f"  n={n:>8}: margin = {mp.nstr(margin, 6)}  "
        f"(predicted ~(1/132)sqrt(pi/2n) = {mp.nstr(pred, 6)})  positive: {ok}")
    if not ok: fails += 1
log("  -> margin -> 0+ like (1/132)sqrt(pi/(2n)) (the 1/11 in the bound vs the")
log("     classical next-order 1/12), consistent with the document's own report")
log("     (0.0000979 at n=10^4) and with strict positivity at every n -- the")
log("     bound is proved by a chain of everywhere-valid inequalities, so the")
log("     shrinking margin is expected and harmless.")

# cross-validate Q_direct against exact at overlap
qx = Q_exact(2000)
d = abs(Q_direct(2000) - mp.mpf(qx.numerator)/mp.mpf(qx.denominator))
log(f"  cross-validation Q_direct vs exact Fraction at n=2000: |diff| = {mp.nstr(d, 4)}")
if d > mp.mpf(10) ** (-40): fails += 1

log("")
log("=" * 78)
log(f"PART-2 RESULT: {'ALL CHECKS PASSED (0 failures)' if fails == 0 else f'{fails} FAILURE GROUPS'}")
log("=" * 78)
with open(__file__.replace(".py", ".log"), "w") as f:
    f.write("\n".join(LOG) + "\n")
sys.exit(0 if fails == 0 else 1)
