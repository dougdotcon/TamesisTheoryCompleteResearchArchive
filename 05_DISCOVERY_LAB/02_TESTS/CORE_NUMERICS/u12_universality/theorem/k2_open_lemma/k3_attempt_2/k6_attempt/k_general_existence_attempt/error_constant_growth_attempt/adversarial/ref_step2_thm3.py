"""
STEP 2 -- independent re-derivation of Theorem 3 (the exact D*_r(0) closed form)
and of the binomial machinery it uses.

Everything checked with exact integer / Fraction arithmetic.

My own derivation (full prose in REFEREE_REPORT.md Part 2):

  (2a) H_r(1,b) = r!(r+b)!/N! * sum_{i=0}^{r} w(i) C(N,i),  N := 2r+b+1,
       w(i) := (3u+2)(u-1)u(u+1)/24,  u := r-i.
       [substitute i = r-k-2 in Theorem 1 at t=1; (r-k-2)+(r+b+k+3) = N.]

  (2b) with v := i - N/2 and c := (b+1)/2, u = -(v+c), so
           24 w = 3(v+c)^4 - 2(v+c)^3 - 3(v+c)^2 + 2(v+c).
       At b=0 (c=1/2) this is 3v^4 - (3/2)v^2 + 3/16  +  4v^3 - v.

  (2c) TWO GENERAL BOUNDARY IDENTITIES, proved by hand (induction / Abel):
           I1:  sum_{i=0}^{m} (n-2i)   C(n,i) = (m+1) C(n,m+1)
           I3:  sum_{i=0}^{m} (n-2i)^3 C(n,i) = (n-2m)^2 (m+1) C(n,m+1)
                                                + 4 n m C(n-1,m)
       At n=N=2r+1, m=r these specialise to the target's two identities
           (2r+1)C(2r,r)  and  (2r+1)(4r+1)C(2r,r).
       At n=N=2r+b+1, m=r they give the b>=1 generalisations used in STEP 4.

  (2d) at b=0 only, N odd makes i<=r an exact half-range, so the even part
       contributes exactly half of its full binomial sum, computable from the
       central moments mu_2=N/4, mu_4=N(3N-2)/16 of Bin(N,1/2).
"""

import sys
from fractions import Fraction as Fr
from math import comb, factorial

from ref_core import Ladder, peval, phi

R = int(sys.argv[1]) if len(sys.argv) > 1 else 60

print("=" * 78)
print("STEP 2  Theorem 3, re-derived independently.  R=%d" % R)
print("=" * 78)

# ---------------------------------------------------------------------------
# (2c) the two general boundary identities -- exhaustive exact check
# ---------------------------------------------------------------------------
print()
print("(2c) my two GENERAL boundary identities (exact, brute-forced):")
bad1 = bad3 = 0
n1 = n3 = 0
for n in range(1, 121):
    for m in range(0, n):
        lhs1 = sum((n - 2 * i) * comb(n, i) for i in range(0, m + 1))
        rhs1 = (m + 1) * comb(n, m + 1)
        n1 += 1
        if lhs1 != rhs1:
            bad1 += 1
        lhs3 = sum((n - 2 * i) ** 3 * comb(n, i) for i in range(0, m + 1))
        rhs3 = (n - 2 * m) ** 2 * (m + 1) * comb(n, m + 1) + 4 * n * m * comb(n - 1, m)
        n3 += 1
        if lhs3 != rhs3:
            bad3 += 1
print("   I1  sum_{i<=m}(n-2i)C(n,i) = (m+1)C(n,m+1)          : %d checks, %d fail"
      % (n1, bad1))
print("   I3  sum_{i<=m}(n-2i)^3C(n,i) = (n-2m)^2(m+1)C(n,m+1)")
print("                                  + 4 n m C(n-1,m)      : %d checks, %d fail"
      % (n3, bad3))

print()
print("   their b=0 specialisations (n=2r+1, m=r), the two the target uses:")
badA = badB = 0
for r in range(1, 160):
    N = 2 * r + 1
    A1 = sum((N - 2 * i) * comb(N, i) for i in range(0, r + 1))
    A3 = sum((N - 2 * i) ** 3 * comb(N, i) for i in range(0, r + 1))
    if A1 != (2 * r + 1) * comb(2 * r, r):
        badA += 1
    if A3 != (2 * r + 1) * (4 * r + 1) * comb(2 * r, r):
        badB += 1
print("      sum (N-2i)  C(N,i) = (2r+1)C(2r,r)         : r=1..159, %d fail" % badA)
print("      sum (N-2i)^3C(N,i) = (2r+1)(4r+1)C(2r,r)   : r=1..159, %d fail" % badB)

# ---------------------------------------------------------------------------
# (2b) the even/odd split of 24w at b=0
# ---------------------------------------------------------------------------
print()
print("(2b) 24w(i) = [3v^4 - (3/2)v^2 + 3/16] + [4v^3 - v] at b=0, v=i-N/2:")
badw = nw = 0
for r in range(0, 60):
    N = 2 * r + 1
    for i in range(0, r + 1):
        u = Fr(r - i)
        w24 = u * (u + 1) * (u - 1) * (3 * u + 2)
        v = Fr(i) - Fr(N, 2)
        ev = 3 * v ** 4 - Fr(3, 2) * v ** 2 + Fr(3, 16)
        od = 4 * v ** 3 - v
        nw += 1
        if w24 != ev + od:
            badw += 1
print("   %d checks, %d fail" % (nw, badw))

# ---------------------------------------------------------------------------
# (2d) the even half-sum
# ---------------------------------------------------------------------------
print()
print("(2d) sum_{i=0}^{N}[3v^4-(3/2)v^2+3/16]C(N,i) = 2^N*3(3N-1)(N-1)/16,")
print("     half-range value = 4^r * 3r(3r+1)/4 :")
bade = ne = 0
for r in range(0, 60):
    N = 2 * r + 1
    full = sum((3 * (Fr(i) - Fr(N, 2)) ** 4 - Fr(3, 2) * (Fr(i) - Fr(N, 2)) ** 2
                + Fr(3, 16)) * comb(N, i) for i in range(0, N + 1))
    half = sum((3 * (Fr(i) - Fr(N, 2)) ** 4 - Fr(3, 2) * (Fr(i) - Fr(N, 2)) ** 2
                + Fr(3, 16)) * comb(N, i) for i in range(0, r + 1))
    ne += 2
    if full != Fr(2 ** N * 3 * (3 * N - 1) * (N - 1), 16):
        bade += 1
    if half != Fr(full, 2) or half != Fr(4 ** r * 3 * r * (3 * r + 1), 4):
        bade += 1
print("   %d checks, %d fail" % (ne, bade))

# ---------------------------------------------------------------------------
# (2a) the half-sum representation + Theorem 3, against MY OWN H_r(1,b)
# ---------------------------------------------------------------------------
print()
print("(2a)/(Thm 3) against MY OWN ODE-solved H_r(1,0):")
lad = Ladder(min(R, 45), 3)


def halfsum(r, b):
    N = 2 * r + b + 1
    tot = Fr(0)
    for i in range(0, r + 1):
        u = Fr(r - i)
        w = u * (u + 1) * (u - 1) * (3 * u + 2) / 24
        tot += w * comb(N, i)
    return Fr(factorial(r) * factorial(r + b), factorial(N)) * tot


def thm3(r):
    return Fr(r * (3 * r + 1), 32) * phi(r) - Fr(r, 12)


bad_hs = bad_t3 = 0
rows = []
for r in range(0, min(R, 45) + 1):
    mine = peval(lad.H[(r, 0)], 1)
    hs = halfsum(r, 0)
    t3 = thm3(r)
    if mine != hs:
        bad_hs += 1
        print("   HALF-SUM MISMATCH r=%d  %s vs %s" % (r, mine, hs))
    if mine != t3:
        bad_t3 += 1
        print("   THM3 MISMATCH r=%d  %s vs %s" % (r, mine, t3))
    if r <= 7:
        rows.append((r, mine))
print("   half-sum representation vs my H_r(1,0):  r=0..%d, %d mismatches"
      % (min(R, 45), bad_hs))
print("   Theorem 3 closed form vs my H_r(1,0):    r=0..%d, %d mismatches"
      % (min(R, 45), bad_t3))
print("   table r=0..7:", [(r, str(v)) for r, v in rows])
print("   (target's own table: 0, 0, 1/15, 5/28, 103/315, 1405/2772, 1431/2002, 2219/2340)")

# Theorem 3 pushed further using the half-sum representation only (cheap)
bad_far = 0
for r in range(0, R + 1):
    if halfsum(r, 0) != thm3(r):
        bad_far += 1
print("   Theorem 3 vs half-sum representation, r=0..%d: %d mismatches" % (R, bad_far))

# Corollary 3a
print()
print("(Cor 3a) D*_0(0) = %s ;  D*_1(0) = %s   (exact cancellation 1/12 - 1/12)"
      % (thm3(0), thm3(1)))
print("         3*phi_1 = %s ;  r(3r+1)/32*phi_1 = %s ; r/12 = %s"
      % (3 * phi(1), Fr(1 * 4, 32) * phi(1), Fr(1, 12)))

# ---------------------------------------------------------------------------
# b >= 1: is there a clean closed form?  (target says no; check the residual)
# ---------------------------------------------------------------------------
print()
print("b>=1 residual  r(3r+1)/32*F_r(1,b) - H_r(1,b)  (target quotes 5/96, 61/480, 963/4480 at b=1):")
for b in (0, 1, 2):
    vals = []
    for r in range(2, 6):
        Fr1b = peval(lad.F[(r, b)], 1)
        vals.append(str(Fr(r * (3 * r + 1), 32) * Fr1b - peval(lad.H[(r, b)], 1)))
    print("   b=%d : %s" % (b, vals))
