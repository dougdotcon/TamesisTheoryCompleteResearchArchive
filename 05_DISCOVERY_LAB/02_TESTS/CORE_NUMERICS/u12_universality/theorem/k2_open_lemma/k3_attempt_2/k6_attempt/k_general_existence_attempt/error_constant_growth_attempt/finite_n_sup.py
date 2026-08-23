"""
finite_n_sup.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

The mandate names  S_r(b) := sup_{m,n} n^2 |R_r(m,b,n)|  (sup over ALL valid n,
not just the limit).  This script separates the two questions:

  (a) WHERE is the sup attained?  (cross_checks.py X2 found (n,m)=(b+r+1,b+r+1)
      for every r<=14; here that is re-checked at larger r by exhaustive scan.)
  (b) Given that, S_r(b) = (b+r+1)^2 |R_r(b+r+1, b, b+r+1)| is ONE exact number
      per r, so it can be pushed much further in r than a full scan allows.
      How does S_r(b)/D*_r(b) behave -- bounded, or slowly growing?

Exact arithmetic throughout; floats for display only.
"""

import sys
from fractions import Fraction as Fr
from math import log
import core as C

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 45
SCAN_R = int(sys.argv[2]) if len(sys.argv) > 2 else 22
NSCAN = int(sys.argv[3]) if len(sys.argv) > 3 else 60

print("=" * 96)
print("(a)  Exhaustive scan over ALL valid n <= %d and ALL m: where is the sup?" % NSCAN)
print("=" * 96)
print("   %3s %3s | %-16s %-14s | argmax(n,m)   at minimal n?" % ("r", "b", "sup n^2|R_r|", "D*_r(b)"))
for b in (0, 1):
    for r in range(15, SCAN_R + 1):
        best = Fr(0)
        arg = None
        for n in range(b + r + 1, NSCAN + 1):
            ch = C.Chain(n)
            for m in range(b + r + 1, n + 1):
                v = abs(C.R_resid(ch, r, m, b)) * n * n
                if v > best:
                    best, arg = v, (n, m)
        print("   %3d %3d | %-16.9f %-14.9f | (%d,%d)   %s"
              % (r, b, float(best), float(C.H(r, b).eval(Fr(1))), arg[0], arg[1],
                 "YES" if arg == (b + r + 1, b + r + 1) else "*** NO ***"))

print()
print("=" * 96)
print("(b)  S_r(b) at the minimal state (n=m=b+r+1), exactly, pushed in r.")
print("=" * 96)
print("   %4s %3s | %-18s %-18s %-10s %-14s"
      % ("r", "b", "S_r(b)", "D*_r(b)", "S/D*", "(S/D*-1)*r"))
for b in (0, 1):
    prev = None
    for r in range(2, RMAX + 1):
        n = b + r + 1
        ch = C.Chain(n)
        s = abs(C.R_resid(ch, r, n, b)) * n * n
        d = C.H(r, b).eval(Fr(1))
        ratio = float(s / d) if d else float("nan")
        if r % 3 == 0 or r < 8:
            print("   %4d %3d | %-18.9f %-18.9f %-10.5f %-14.5f"
                  % (r, b, float(s), float(d), ratio, (ratio - 1) * r))
    print()

print("=" * 96)
print("(c)  Growth law of S_r(0) itself.")
print("=" * 96)
print("   %4s | %-16s %-14s %-14s %-16s"
      % ("r", "S_r(0)", "S_r/r^{3/2}", "loglog slope", "S_r/(r^{3/2} log r)"))
prev = None
prevr = None
for r in range(4, RMAX + 1):
    n = r + 1
    ch = C.Chain(n)
    s = float(abs(C.R_resid(ch, r, n, 0)) * n * n)
    sl = (log(s / prev) / log(r / float(prevr))) if prev else float("nan")
    if r % 3 == 0 or r < 8:
        print("   %4d | %-16.9f %-14.8f %-14.6f %-16.8f"
              % (r, s, s / r ** 1.5, sl, s / (r ** 1.5 * log(r))))
    prev, prevr = s, r
print()
print("   3 sqrt(pi)/64 = 0.08308377 is the limit of D*_r(0)/r^{3/2}.")
