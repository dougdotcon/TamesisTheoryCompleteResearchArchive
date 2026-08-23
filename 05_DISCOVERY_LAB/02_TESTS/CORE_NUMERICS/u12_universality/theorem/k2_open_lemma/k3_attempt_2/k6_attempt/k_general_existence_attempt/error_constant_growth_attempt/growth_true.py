"""
growth_true.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

Computes the TRUE (asymptotically tight) residual constant

    D*_r(b) := max_{t in [0,1]} |H_r(t,b)|

exactly, for r up to as large as is tractable, and characterises its growth.

All arithmetic exact (fractions.Fraction).  Floats only in printed columns.

Also verifies, at every r, the structural facts that make D*_r(b) = H_r(1,b):
  (P) every coefficient of H_r(.,b) is >= 0  =>  |H_r| is increasing on [0,1]
      =>  max_{[0,1]}|H_r| = H_r(1,b).
"""

import sys
from fractions import Fraction as Fr
from math import log, sqrt, pi
import core as C

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60

print("=" * 96)
print("PART 1.  Coefficient positivity of H_r(.,b)  (=> max_{[0,1]}|H_r| = H_r(1,b))")
print("=" * 96)
allpos = True
for b in (0, 1, 2, 3):
    bad = []
    for r in range(0, RMAX + 1):
        p = C.H(r, b)
        if any(a < 0 for a in p.c):
            bad.append(r)
    allpos &= (not bad)
    print("  b=%d : r=0..%d  all coefficients of H_r >= 0 : %s   %s"
          % (b, RMAX, not bad, ("violations at r=" + str(bad)) if bad else ""))
print("  => D*_r(b) = H_r(1,b) on this whole range." if allpos else "  => CHECK FAILED")

print()
print("=" * 96)
print("PART 2.  Exact D*_r(b) = H_r(1,b), and its growth")
print("=" * 96)
for b in (0, 1):
    print()
    print("  b = %d" % b)
    print("  %3s  %-34s %-14s %-12s %-12s %-12s %-12s"
          % ("r", "D*_r(b) exact", "D*_r(b)", "ratio", "loglog slope",
             "D*/phi_r", "D*/(phi_r r^2)"))
    prev = None
    prevr = None
    for r in range(1, RMAX + 1):
        v = C.H(r, b).eval(Fr(1))
        fv = float(v)
        ratio = (fv / float(prev)) if (prev and prev != 0) else float("nan")
        slope = (log(fv / float(prev)) / log(r / (r - 1.0))) if (prev and prev != 0) else float("nan")
        ph = float(C.F(r, b).eval(Fr(1)))
        s = str(v)
        if len(s) > 34:
            s = s[:31] + "..."
        if r <= 12 or r % 5 == 0 or r >= RMAX - 2:
            print("  %3d  %-34s %-14.9f %-12.6f %-12.6f %-12.6f %-12.8f"
                  % (r, s, fv, ratio, slope, fv / ph, fv / ph / (r * r)))
        prev = v
        prevr = r

print()
print("=" * 96)
print("PART 3.  Growth diagnostics at b=0 and b=1")
print("=" * 96)
for b in (0, 1):
    xs, ys = [], []
    for r in range(2, RMAX + 1):
        v = float(C.H(r, b).eval(Fr(1)))
        if v > 0:
            xs.append(log(r))
            ys.append(log(v))
    # local log-log slope over the last decade of the range
    print()
    print("  b=%d" % b)
    for lo, hi in [(2, 6), (5, 10), (10, 20), (20, 40), (int(RMAX * 0.5), RMAX)]:
        if hi > RMAX or lo < 2:
            continue
        v1 = float(C.H(lo, b).eval(Fr(1)))
        v2 = float(C.H(hi, b).eval(Fr(1)))
        print("    log-log slope on r=%d..%d : %.6f" % (lo, hi, log(v2 / v1) / log(hi / float(lo))))
    # test the hypothesis  D*_r(b) ~ A * r^(3/2)
    print("    D*_r(b) / r^(3/2) :", end=" ")
    for r in [5, 10, 20, 30, 40, 50, 60, RMAX]:
        if r > RMAX:
            continue
        v = float(C.H(r, b).eval(Fr(1)))
        print("r=%d:%.6f" % (r, v / r ** 1.5), end="  ")
    print()
    # test the hypothesis  D*_r(b) / phi_r ~ A * r^2
    print("    (D*_r/phi_r) / r^2 :", end=" ")
    for r in [5, 10, 20, 30, 40, 50, 60, RMAX]:
        if r > RMAX:
            continue
        v = float(C.H(r, b).eval(Fr(1)))
        ph = float(C.F(r, b).eval(Fr(1)))
        print("r=%d:%.8f" % (r, v / ph / r ** 2), end="  ")
    print()
