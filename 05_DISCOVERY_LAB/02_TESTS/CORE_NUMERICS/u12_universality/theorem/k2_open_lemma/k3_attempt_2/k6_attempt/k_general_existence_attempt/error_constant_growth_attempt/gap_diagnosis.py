"""
gap_diagnosis.py -- error_constant_growth_attempt (DISC-DEC-045, front (b))

WHY the proved bound D_r(b) is so much larger than the true constant D*_r(b),
decomposed into two independent, separately-quantifiable mechanisms, and what
each is worth.

  (G1) SS6 of k_general_existence_attempt/ATTEMPT.md bounds the term
       (r/n) eps^h_{r-1}(a,b+1,n)  by  r C_{r-1}(b+1)/n^2, i.e. it discards the
       explicit factor 1/n.  Since the Target Theorem's standing hypothesis is
       n >= b+r+1, that factor is worth r/n <= r/(b+r+1) < 1.  Keeping it turns
       the amplifying recursion C_r ~ r C_{r-1}  (FACTORIAL) into a bounded one.

  (G2) SS4's Lemma bounds |p(x)| on [0,1] by the coefficient-sum norm
       ||p|| = sum_k |a_k|.  For the reflected polynomials that actually occur
       (Hhat_r(s,b) = (1-s)F_r(1-s,b+1), K_r, and the Taylor tail built from
       them) the reflection s -> 1-s makes every coefficient of a given index
       carry the same sign, so ||F_r(1-.,b)|| = F_r(2,b) EXACTLY -- and
       F_r(2,b) is exponentially larger than sup_{[0,1]}|F_r| = F_r(1,b).
       This script measures that exponential rate.

Exact arithmetic throughout; floats for display only.
"""

import sys
from fractions import Fraction as Fr
from math import log
import core as C
import loose_bound as LB

sys.setrecursionlimit(100000)
RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60

print("=" * 98)
print("G2(a).  ||F_r(1-.,b)|| == F_r(2,b) exactly  (all coefficients of a given")
print("        index share the sign (-1)^j, so the coefficient-sum norm is F_r(2,b)).")
print("=" * 98)
ok = True
for b in range(0, 4):
    for r in range(0, 25):
        lhs = C.F(r, b).shift_1_minus_x().coeff_sum_norm()
        rhs = C.F(r, b).eval(Fr(2))
        ok &= (lhs == rhs)
        lhs2 = C.G(r, b).shift_1_minus_x().coeff_sum_norm()
        rhs2 = C.G(r, b).eval(Fr(2))
        ok &= (lhs2 == rhs2)
        # and ||(1-s)q(s)|| = 2||q|| for such q  -> ||Hhat_r(.,b)|| = 2 F_r(2,b+1)
        ok &= (C.Hhat(r, b).coeff_sum_norm() == 2 * C.F(r, b + 1).eval(Fr(2)))
print("   ||F_r(1-.,b)||==F_r(2,b), ||G_r(1-.,b)||==G_r(2,b), ||Hhat_r||==2F_r(2,b+1)")
print("   r=0..24, b=0..3 :", ok)

print()
print("=" * 98)
print("G2(b).  The exponential rate of the coefficient-sum norm overestimate.")
print("        sup_{[0,1]}|F_r(1-.,b)| = F_r(1,b) = phi_r-ish;  ||.|| = F_r(2,b).")
print("=" * 98)
print("   %4s | %-14s %-14s %-16s %-12s %-14s"
      % ("r", "F_r(1,0)", "F_r(2,0)", "F_r(2,0)/F_r(1,0)", "ratio in r", "/ (9/8)^r"))
prev = None
for r in range(1, RMAX + 1):
    f1 = C.F(r, 0).eval(Fr(1))
    f2 = C.F(r, 0).eval(Fr(2))
    q = f2 / f1
    if r % 5 == 0 or r <= 6:
        print("   %4d | %-14.6g %-14.6g %-16.6g %-12.6f %-14.6g"
              % (r, float(f1), float(f2), float(q),
                 float(q / prev) if prev else float("nan"),
                 float(q) / (9.0 / 8.0) ** r))
    prev = q
print()
print("   The ratio-in-r column converges to 9/8 = 1.125:  F_r(2,b)/F_r(1,b) = Theta((9/8)^r).")
print("   Reason: F_r(2,0) = (phi_r/4^r) sum_{i<=r} 2^{r-i} C(2r+1,i), whose summand")
print("   peaks at i=(2r-1)/3 INSIDE the range, so the sum is ~ (3/2)^{2r+1} 2^r = ")
print("   1.5*(9/2)^r, giving F_r(2,0) ~ 1.5 phi_r (9/8)^r.")

print()
print("=" * 98)
print("G1.  The factorial amplifier, and the one-line fix.")
print("=" * 98)
print("   ORIGINAL (ATTEMPT.md SS5/SS6):")
print("     D_r(b) = [ r C_{r-1}(b) + A_r(b) ] / (r+b+1)")
print("     C_r(b) = B_r(b) + r C_{r-1}(b+1) + 2 D_r(b+1)")
print("   The C-step multiplies by r with NO compensating division -> C_r >~ r! .")
print("   The discarded factor is legitimate: the term being bounded is")
print("     (r/n) eps^h_{r-1}(a,b+1,n),  |eps^h_{r-1}| <= C_{r-1}(b+1)/n^2,")
print("   and the standing hypothesis is n >= b+r+1, so r/n <= r/(b+r+1) < 1.")
print("   Also (1-s)-(1+b+r)/n = (n-1-a-b-r)/n lies in [0,1] on the valid domain,")
print("   so the factor 2 in front of D_r(b+1) can be 1.")
print("   IMPROVED:")
print("     D'_r(b) = [ r C'_{r-1}(b) + A_r(b) ] / (r+b+1)")
print("     C'_r(b) = B_r(b) + [r/(b+r+1)] C'_{r-1}(b+1) + D'_r(b+1)")

from functools import lru_cache


@lru_cache(maxsize=None)
def Dimp(r, b):
    if r == 0:
        return Fr(0)
    return (r * Cimp(r - 1, b) + LB.A(r, b)) / Fr(r + b + 1)


@lru_cache(maxsize=None)
def Cimp(r, b):
    if r == 0:
        return Fr(0)
    return LB.B(r, b) + Fr(r, b + r + 1) * Cimp(r - 1, b + 1) + Dimp(r, b + 1)


print()
print("   %4s | %-14s %-14s %-14s | %-12s %-12s %-12s"
      % ("r", "D_r(0) orig", "D'_r(0) impr", "D*_r(0) true",
         "orig/true", "impr/true", "D'_r/D'_{r-1}"))
prev = None
RG = int(sys.argv[2]) if len(sys.argv) > 2 else 30
for r in range(1, RG + 1):
    do = LB.Dloose(r, 0)
    di = Dimp(r, 0)
    dt = C.H(r, 0).eval(Fr(1))
    print("   %4d | %-14.6g %-14.6g %-14.6g | %-12.6g %-12.6g %-12.6f"
          % (r, float(do), float(di), float(dt),
             float(do / dt) if dt else float("nan"),
             float(di / dt) if dt else float("nan"),
             float(di / prev) if prev else float("nan")))
    prev = di

print()
print("   %4s | %-14s %-14s | %-12s %-12s"
      % ("r", "C_r(0) orig", "C'_r(0) impr", "C_r/C_{r-1}", "C'_r/C'_{r-1}"))
po = pi_ = None
for r in range(1, RG + 1):
    co = LB.Cloose(r, 0)
    ci = Cimp(r, 0)
    print("   %4d | %-14.6g %-14.6g | %-12.6f %-12.6f"
          % (r, float(co), float(ci),
             float(co / po) if po else float("nan"),
             float(ci / pi_) if pi_ else float("nan")))
    po, pi_ = co, ci

print()
print("=" * 98)
print("SUMMARY of the gap decomposition at b=0")
print("=" * 98)
print("   %4s | %-13s %-13s %-13s | %-13s %-13s"
      % ("r", "D*_r true", "D'_r improved", "D_r original",
         "impr/true", "orig/impr"))
for r in [2, 4, 6, 8, 10, 12, 16, 20, 24, min(30, RG)]:
    if r > RG:
        continue
    dt = C.H(r, 0).eval(Fr(1))
    di = Dimp(r, 0)
    do = LB.Dloose(r, 0)
    print("   %4d | %-13.6g %-13.6g %-13.6g | %-13.6g %-13.6g"
          % (r, float(dt), float(di), float(do),
             float(di / dt) if dt else float("nan"),
             float(do / di) if di else float("nan")))
