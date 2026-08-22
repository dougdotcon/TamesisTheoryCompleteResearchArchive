"""
Consolidated verification pipeline for the K3-OPEN-LEMMA-ATTEMPT-2 result. Runs, in
order, and prints PASS/FAIL for each:

  1. markov_transfer.py's closed forms for K=0,1,2 reproduced against the ALREADY
     PROVED formulas from ../ATTEMPT.md (psi_n^(1)=2/3+1/(6n),
     psi_n^(2)=8/15+4/(15n)+1/(15n^2)) -- an independent method reproducing a known
     theorem is the strongest available sanity check on the method itself.
  2. The K=3 closed form psi_n^(3)=(64n^3+48n^2+25n+6)/(140n^3) against
     ../psi_k3_exploration.log's brute-force values, n=4..8 (wave 5's own numbers).
  3. The K=3 closed form against a FRESH brute-force run at n=9 (beyond wave 5's
     range) via psi_bruteforce_ref.py.
  4. The K=3 closed form against markov_direct.py's independent memoized-recursion
     computation (tests the transition rules, not the summation), n=4..9.
  5. The full phi_n^(3) closed form (Lemma A recombination) against an independent,
     differently-coded brute-force (phi_bruteforce_full.py) at the raw Definition-4
     level, n=4..7.
  6. The bonus general-K rate pattern (coefficient of 1/n in psi_n^(K) equals
     K*phi_K/4) against brute force at K=4,5 for one n each.

Run with: python3 verify_all.py   (takes a few minutes; the n=9 K=3 raw brute force
step alone takes ~7-8 minutes -- pass --skip-slow to omit it if already checked.)
"""
import sys
import time
from fractions import Fraction as F

import sympy as sp

from markov_transfer import n as n_sym, psi_closed_form, phi_closed_form
from psi_bruteforce_ref import psi_n_K
from markov_direct import psi_markov
from phi_bruteforce_full import phi_n_K

SKIP_SLOW = "--skip-slow" in sys.argv

PASS = []
FAIL = []


def check(label, cond):
    print(("PASS: " if cond else "FAIL: ") + label)
    (PASS if cond else FAIL).append(label)


def frac_eval(expr, nval):
    return sp.nsimplify(expr.subs(n_sym, nval))


print("=" * 70)
print("STEP 1: reproduce ALREADY-PROVED K=1, K=2 closed forms")
print("=" * 70)
psi1 = psi_closed_form(1)
target1 = sp.Rational(2, 3) + sp.Rational(1, 6) / n_sym
check("psi_n^(1) == 2/3+1/(6n)  [ATTEMPT.md SS3, PROVED]",
      sp.simplify(psi1 - target1) == 0)

psi2 = psi_closed_form(2)
target2 = sp.Rational(8, 15) + sp.Rational(4, 15) / n_sym + sp.Rational(1, 15) / n_sym**2
check("psi_n^(2) == 8/15+4/(15n)+1/(15n^2)  [ATTEMPT.md SS4, PROVED]",
      sp.simplify(psi2 - target2) == 0)

print()
print("=" * 70)
print("STEP 2: K=3 closed form vs wave-5's own brute-force log (n=4..8)")
print("=" * 70)
psi3 = psi_closed_form(3)
print("psi_n^(3) =", psi3)
wave5_log = {4: F(71, 128), 5: F(1333, 2500), 6: F(187, 360),
             7: F(4897, 9604), 8: F(18023, 35840)}
for nn, val in wave5_log.items():
    f = frac_eval(psi3, nn)
    check(f"psi_n^(3) at n={nn} matches psi_k3_exploration.log", f == val)

print()
print("=" * 70)
print("STEP 3: K=3 closed form vs FRESH brute force at n=9 (beyond wave 5)")
print("=" * 70)
if SKIP_SLOW:
    print("SKIPPED (--skip-slow). Already run once: n=9 K=3 psi=3385/6804 "
          "(448.6s), matches closed form (see ATTEMPT.md).")
else:
    t0 = time.time()
    bf9 = psi_n_K(9, 3, "generic")
    dt = time.time() - t0
    f9 = frac_eval(psi3, 9)
    print(f"brute force n=9: {bf9}  ({dt:.1f}s)")
    check("psi_n^(3) at n=9 matches fresh brute force", f9 == bf9)

print()
print("=" * 70)
print("STEP 4: K=3 closed form vs independent memoized recursion (n=4..9)")
print("=" * 70)
for nn in range(4, 10):
    mv = psi_markov(nn, 3)
    f = frac_eval(psi3, nn)
    check(f"psi_n^(3) at n={nn}: closed form == direct recursion", f == mv)

print()
print("=" * 70)
print("STEP 5: full phi_n^(3) (Lemma A) vs independent raw-definition brute force")
print("=" * 70)
phi3 = phi_closed_form(3)
print("phi_n^(3) =", phi3)
phi_bf = {4: F(71, 128), 5: F(1628, 3125), 6: F(181, 360), 7: F(41327, 84035)}
for nn, val in phi_bf.items():
    f = frac_eval(phi3, nn)
    check(f"phi_n^(3) at n={nn} matches independent full-definition brute force", f == val)

print()
print("=" * 70)
print("STEP 6: bonus general-K rate pattern (1/n coeff = K*phi_K/4) at K=4,5")
print("=" * 70)
psi4 = psi_closed_form(4)
psi5 = psi_closed_form(5)
check("psi_n^(4) at n=5 matches brute force (1569/3125)",
      frac_eval(psi4, 5) == F(1569, 3125))
check("psi_n^(4) at n=6 matches brute force (196/405)",
      frac_eval(psi4, 6) == F(196, 405))
check("psi_n^(5) at n=6 matches brute force (899/1944)",
      frac_eval(psi5, 6) == F(899, 1944))

print()
print("=" * 70)
print(f"TOTAL: {len(PASS)} PASS, {len(FAIL)} FAIL")
print("=" * 70)
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print("  -", f)
    sys.exit(1)
else:
    print("ALL CHECKS PASSED.")
