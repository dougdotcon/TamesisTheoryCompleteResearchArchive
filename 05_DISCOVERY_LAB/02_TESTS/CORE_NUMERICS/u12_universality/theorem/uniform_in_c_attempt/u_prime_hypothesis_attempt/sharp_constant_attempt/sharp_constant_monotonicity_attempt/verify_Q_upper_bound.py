"""
DISC-DEC-066, wave 16 front (b).

T4: Theorem 1 of ATTEMPT.md -- the new elementary Q(n) upper bound:

    Q(n) < sqrt(pi n/2) - 1/3 + (1/11) sqrt(pi/(2n))     for every integer n>=1.

Derivation chain (each step cited or elementary, proved in ATTEMPT.md Sec.2):
  Q(n) = A(n)/2 - theta(n),  A(n):=n! e^n/n^n                      [Lemma 1]
  A(n) < sqrt(2 pi n) e^{1/(12n)}                                  [Robbins 1955]
  theta(n) >= 1/3 + 4/(135(n+8/45)) > 1/3                          [FGKP95 Thm 7, dropping a positive term]
  e^{1/(12n)} <= 1/(1 - 1/(12n)) = 12n/(12n-1)                     [e^x <= 1/(1-x), 0<=x<1; x=1/(12n)<1 for n>=1]
  sqrt(pi n/2) * 12n/(12n-1) = sqrt(pi n/2)(1+1/(12n-1))
     <= sqrt(pi n/2) + sqrt(pi n/2)/(11n)                          [12n-1 >= 11n for n>=1, equality at n=1]
     =  sqrt(pi n/2) + (1/11) sqrt(pi/(2n))

This script verifies the FINAL bound directly against EXACT Q(n) (fractions.Fraction).
"""
import json
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 50
LOG = []


def log(msg):
    print(msg)
    LOG.append(msg)


def frac2mp(fr):
    return mp.mpf(fr.numerator) / mp.mpf(fr.denominator)


def Q_exact(n):
    total = Fraction(0)
    prod = Fraction(1)
    total += prod
    for i in range(1, n):
        prod *= Fraction(n - i, n)
        total += prod
    return total


def Q_upper_elem(n):
    n_ = mp.mpf(n)
    return mp.sqrt(mp.pi * n_ / 2) - mp.mpf(1) / 3 + mp.mpf(1) / 11 * mp.sqrt(mp.pi / (2 * n_))


log("=== T4: Q(n) < sqrt(pi n/2) - 1/3 + (1/11) sqrt(pi/(2n)), exact Q(n) via Fraction ===")
viol = 0
worst_margin = None
Ns = list(range(1, 601)) + [700, 900, 1200, 1600, 2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000]
results = {}
for n in Ns:
    Qn = frac2mp(Q_exact(n))
    bound = Q_upper_elem(n)
    margin = bound - Qn  # want strictly > 0
    results[n] = float(margin)
    if margin <= 0:
        viol += 1
        log(f"VIOLATION n={n}: Q(n)={Qn}, bound={bound}, margin={margin}")
    if worst_margin is None or margin < worst_margin[1]:
        worst_margin = (n, margin)
log(f"n in dense 1..600 + sparse to n=10000 ({len(Ns)} points): violations={viol}")
log(f"worst (smallest) margin: n={worst_margin[0]}, margin={mp.nstr(worst_margin[1],10)}")
log(f"margin at n=1: {mp.nstr(results[1],10)}  (largest slack, small-n regime)")
log(f"margin at n=10000: {mp.nstr(results[10000],10)}  (smallest slack in this sample -- shrinks like "
    f"~(1/132)*sqrt(pi/(2n)) but the derivation guarantees it stays POSITIVE for every finite n, "
    f"since every step above is a proved inequality, not an asymptotic approximation)")

with open('verify_Q_upper_bound.log', 'w') as f:
    f.write('\n'.join(LOG) + '\n')
print("\nLog written to verify_Q_upper_bound.log")
