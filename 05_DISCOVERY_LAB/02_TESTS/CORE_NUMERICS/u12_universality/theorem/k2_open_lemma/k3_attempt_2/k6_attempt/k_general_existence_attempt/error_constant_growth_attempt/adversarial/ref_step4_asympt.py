"""
STEP 4 -- Theorem 4 (growth rate), re-derived, and the b>=1 Stirling step
completed rigorously.

MY OWN DERIVATION (prose in REFEREE_REPORT.md Part 3).  With
    N := 2r+b+1,  beta := b+1,  c := beta/2,  v := i - N/2,  u := r-i = -(v+c)
Theorem 1 at t=1 gives   H_r(1,b) = P_b * sum_{i=0}^{r} w(i) C(N,i),
    P_b := r!(r+b)!/N!,   24 w = 3(v+c)^4 - 2(v+c)^3 - 3(v+c)^2 + 2(v+c).
Split 24w into its parts even and odd in v:
    E(v) = 3v^4 + (4.5 beta^2 - 3 beta - 3) v^2 + (3beta^4/16 - beta^3/4 - 3beta^2/4 + beta)
    O(v) = (6b+4) v^3 + A1 v,  A1 := 1.5 beta^3 - 1.5 beta^2 - 3 beta + 2

ODD PART -- EXACT, every b, no asymptotics.  Using my two proved boundary
identities I1, I3 (STEP 2) at n=N, m=r, together with the two *exact*
prefactor collapses
        P_b * C(N-1,r)   = 1/N            (since N-1-r = r+b)
        P_b * (r+1)C(N,r+1) = 1
one gets, exactly,
        P_b * (1/24) * sum_{i<=r} O(v) C(N,i)
              = -(3b+2) r / 24  -  b(3b+1)(b+2)/48 .

EVEN PART -- EXACT, every b.  N-i reflects i<=r onto i<=r+b, so
        sum_{i<=r} E C = (1/2)[ sum_{i<=N} E C  -  sum_{i=r+1}^{r+b} E C ],
the full sum being 2^N times a polynomial in N via mu_2 = N/4,
mu_4 = N(3N-2)/16, and the "strip" being exactly b terms whose prefactors
P_b C(N,r+j) = r!(r+b)!/((r+j)!(r+b+1-j)!) are explicit rationals of size
O(1/r).  So D*_r(b) has an EXACT closed form for every fixed b -- b=0 collapses
to Theorem 3, and for b>=1 the Stirling step needs no hand-waving at all.

Asymptotically  Phi_b(r) := P_b 2^N = 2 phi_r prod_{j=1}^{b} (2r+2j)/(2r+j+1),
so Phi_b = sqrt(pi/r)(1 + kappa/r + ...), kappa := b(b-1)/4 - 3/8, giving
        D*_r(b) = (3 sqrt pi/64) r^{3/2}
                  - (3b+2) r/24
                  + (sqrt pi/48)[(45/16)beta^2 - (15/16)beta - 63/32] r^{1/2}
                  + O(1).
"""

import sys
from fractions import Fraction as Fr
from math import comb, factorial
import mpmath as mp

from ref_core import Ladder, peval, phi

mp.mp.dps = 60

RCHK = int(sys.argv[1]) if len(sys.argv) > 1 else 40

print("=" * 78)
print("STEP 4  Theorem 4 -- growth rate, and the b>=1 case done exactly")
print("=" * 78)


# ---------------------------------------------------------------------------
# exact pieces
# ---------------------------------------------------------------------------
def Efun(v, beta):
    return (3 * v ** 4 + (Fr(9, 2) * beta ** 2 - 3 * beta - 3) * v ** 2
            + (Fr(3, 16) * beta ** 4 - Fr(1, 4) * beta ** 3
               - Fr(3, 4) * beta ** 2 + beta))


def halfsum(r, b):
    """direct definition:  P_b * sum_{i<=r} w(i) C(N,i)."""
    N = 2 * r + b + 1
    tot = Fr(0)
    for i in range(0, r + 1):
        u = Fr(r - i)
        tot += u * (u + 1) * (u - 1) * (3 * u + 2) / 24 * comb(N, i)
    return Fr(factorial(r) * factorial(r + b), factorial(N)) * tot


def exact_closed(r, b):
    """MY exact closed form for H_r(1,b), every r,b."""
    beta = Fr(b + 1)
    N = 2 * r + b + 1
    # ---- even part: Phi_b/48 * [full even moment polynomial]  -  strip
    Phi = Fr(factorial(r) * factorial(r + b), factorial(N)) * 2 ** N
    bracket = (Fr(3 * N * (3 * N - 2), 16)
               + (Fr(9, 2) * beta ** 2 - 3 * beta - 3) * Fr(N, 4)
               + (Fr(3, 16) * beta ** 4 - Fr(1, 4) * beta ** 3
                  - Fr(3, 4) * beta ** 2 + beta))
    even = Phi * bracket / 48
    for j in range(1, b + 1):
        v = Fr(j) - beta / 2
        pref = Fr(factorial(r) * factorial(r + b),
                  factorial(r + j) * factorial(r + b + 1 - j))
        even -= Efun(v, beta) * pref / 48
    # ---- odd part: exact
    odd = -Fr(3 * b + 2, 24) * r - Fr(b * (3 * b + 1) * (b + 2), 48)
    return even + odd


print()
print("(4a) my exact closed form vs the direct half-sum vs the ODE ladder:")
lad = Ladder(min(RCHK, 30), 6)
bad_a = bad_b = 0
n_a = n_b = 0
for b in range(0, 7):
    for r in range(0, RCHK + 1):
        hs = halfsum(r, b)
        ec = exact_closed(r, b)
        n_a += 1
        if hs != ec:
            bad_a += 1
            if bad_a < 4:
                print("   CLOSED-FORM MISMATCH r=%d b=%d  %s vs %s" % (r, b, hs, ec))
        if r <= min(RCHK, 30) and b <= 6:
            lv = peval(lad.H[(r, b)], 1)
            n_b += 1
            if lv != hs:
                bad_b += 1
print("   exact closed form vs half-sum : %d checks (r=0..%d, b=0..6), %d mismatches"
      % (n_a, RCHK, bad_a))
print("   half-sum vs my ODE ladder     : %d checks, %d mismatches" % (n_b, bad_b))
print("   b=0 specialisation reproduces Theorem 3 :",
      all(exact_closed(r, 0) == Fr(r * (3 * r + 1), 32) * phi(r) - Fr(r, 12)
          for r in range(0, RCHK + 1)))

print()
print("   the EXACT linear-in-r term of D*_r(b) is -(3b+2)r/24 :")
for b in range(0, 5):
    diffs = [exact_closed(r + 1, b) - exact_closed(r, b) for r in (10, 11)]
    print("      b=%d : -(3b+2)/24 = %-8s   odd-part constant -b(3b+1)(b+2)/48 = %s"
          % (b, str(-Fr(3 * b + 2, 24)), str(-Fr(b * (3 * b + 1) * (b + 2), 48))))

# ---------------------------------------------------------------------------
# asymptotics
# ---------------------------------------------------------------------------
print()
print("(4b) large-r asymptotics (mpmath dps=60), using my exact closed form")


def phi_mp(r):
    return mp.mpf(4) ** r * mp.gamma(r + 1) ** 2 / mp.gamma(2 * r + 2)


def Dstar_mp(r, b):
    beta = mp.mpf(b + 1)
    N = 2 * r + b + 1
    Phi = phi_mp(r) * 2
    for j in range(1, b + 1):
        Phi *= mp.mpf(2 * r + 2 * j) / mp.mpf(2 * r + j + 1)
    bracket = (mp.mpf(3 * N * (3 * N - 2)) / 16
               + (mp.mpf(9) / 2 * beta ** 2 - 3 * beta - 3) * mp.mpf(N) / 4
               + (mp.mpf(3) / 16 * beta ** 4 - mp.mpf(1) / 4 * beta ** 3
                  - mp.mpf(3) / 4 * beta ** 2 + beta))
    even = Phi * bracket / 48
    for j in range(1, b + 1):
        v = mp.mpf(j) - beta / 2
        pref = mp.exp(mp.loggamma(r + 1) + mp.loggamma(r + b + 1)
                      - mp.loggamma(r + j + 1) - mp.loggamma(r + b + 2 - j))
        Ev = (3 * v ** 4 + (mp.mpf(9) / 2 * beta ** 2 - 3 * beta - 3) * v ** 2
              + (mp.mpf(3) / 16 * beta ** 4 - mp.mpf(1) / 4 * beta ** 3
                 - mp.mpf(3) / 4 * beta ** 2 + beta))
        even -= Ev * pref / 48
    odd = -mp.mpf(3 * b + 2) / 24 * r - mp.mpf(b * (3 * b + 1) * (b + 2)) / 48
    return even + odd


# cross-check mp vs exact rationals
worst = mp.mpf(0)
for b in range(0, 4):
    for r in (5, 12, 25, 40):
        ex = mp.mpf(exact_closed(r, b).numerator) / mp.mpf(exact_closed(r, b).denominator)
        ap = Dstar_mp(r, b)
        if ex != 0:
            worst = max(worst, abs((ap - ex) / ex))
print("   mpmath vs exact rationals, worst relative discrepancy: %s" % mp.nstr(worst, 5))

C0 = 3 * mp.sqrt(mp.pi) / 64
print("   3*sqrt(pi)/64 = %s" % mp.nstr(C0, 20))
print()
print("   table of D*_r(b)  (compare to the target's Sec 5.2 table):")
print("        r          b=0            b=1            b=2            b=3")
for r in (10, 100, 1000, 10000, 100000):
    print("   %8d %14.6g %14.6g %14.6g %14.6g"
          % (r, Dstar_mp(r, 0), Dstar_mp(r, 1), Dstar_mp(r, 2), Dstar_mp(r, 3)))

print()
print("   D*_r(b)/r^{3/2}  ->  3 sqrt(pi)/64 = %.10f ?" % C0)
for r in (1000, 10000, 100000, 1000000, 10000000):
    row = "   r=%9d :" % r
    for b in range(0, 4):
        row += " %14.10f" % (Dstar_mp(r, b) / mp.mpf(r) ** mp.mpf(1.5))
    print(row)

print()
print("   THE THIRD TERM.  target claims  D*_r(0) = C0 r^{3/2} - r/12 + (sqrt(pi)/128) r^{1/2} + O(1)")
print("   my derivation says the r^{1/2} coefficient is -sqrt(pi)/512, not +sqrt(pi)/128.")
print("   measured  [D*_r(0) - C0 r^{3/2} + r/12] / r^{1/2} :")
print("      target's claim  +sqrt(pi)/128 = %+.10f" % (mp.sqrt(mp.pi) / 128))
print("      my claim        -sqrt(pi)/512 = %+.10f" % (-mp.sqrt(mp.pi) / 512))
for r in (100, 1000, 10000, 100000, 1000000, 10000000, 100000000):
    val = (Dstar_mp(r, 0) - C0 * mp.mpf(r) ** mp.mpf(1.5) + mp.mpf(r) / 12) / mp.sqrt(r)
    print("      r=%11d :  %+.10f" % (r, val))

print()
print("   general-b r^{1/2} coefficient  (sqrt(pi)/48)[(45/16)beta^2-(15/16)beta-63/32]:")
for b in range(0, 4):
    beta = mp.mpf(b + 1)
    pred = mp.sqrt(mp.pi) / 48 * (mp.mpf(45) / 16 * beta ** 2
                                  - mp.mpf(15) / 16 * beta - mp.mpf(63) / 32)
    print("      b=%d predicted %+.10f  |  measured:" % (b, pred), end="")
    for r in (10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8):
        val = ((Dstar_mp(r, b) - C0 * mp.mpf(r) ** mp.mpf(1.5)
                + mp.mpf(3 * b + 2) * mp.mpf(r) / 24) / mp.sqrt(r))
        print(" %+.8f" % val, end="")
    print()

print()
print("   THE LINEAR TERM.  target's executive summary claims, for every b,")
print("      D*_r(b) = C0 r^{3/2} - r/12 + O(sqrt r).")
print("   my exact result says the linear coefficient is -(3b+2)/24, i.e.")
print("      b=0 -> -1/12 = %.8f   b=1 -> -5/24 = %.8f" % (-1 / 12, -5 / 24))
print("      b=2 -> -1/3  = %.8f   b=3 -> -11/24 = %.8f" % (-1 / 3, -11 / 24))
print("   measured  [D*_r(b) - C0 r^{3/2}] / r  (should tend to -(3b+2)/24):")
for b in range(0, 4):
    row = "      b=%d :" % b
    for r in (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10):
        row += " %14.9f" % ((Dstar_mp(r, b) - C0 * mp.mpf(r) ** mp.mpf(1.5)) / r)
    row += "    -> -(3b+2)/24 = %.9f" % (-(3 * b + 2) / 24)
    print(row)

print()
print("   [D*_r(0) - D*_r(b)] / r  (should tend to +3b/24 = b/8):")
for b in (1, 2, 3):
    row = "      b=%d :" % b
    for r in (10 ** 3, 10 ** 5, 10 ** 7):
        row += " %12.8f" % ((Dstar_mp(r, 0) - Dstar_mp(r, b)) / r)
    row += "   -> b/8 = %.8f" % (b / 8)
    print(row)

print()
print("   local log-log slope d log D* / d log r near r=1e5 (target reports 1.5022..1.5119):")
for b in range(0, 4):
    r1, r2 = mp.mpf(30000), mp.mpf(100000)
    sl = (mp.log(Dstar_mp(int(r2), b)) - mp.log(Dstar_mp(int(r1), b))) / (mp.log(r2) - mp.log(r1))
    r3, r4 = mp.mpf(10) ** 9, mp.mpf(10) ** 10
    sl2 = (mp.log(Dstar_mp(int(r4), b)) - mp.log(Dstar_mp(int(r3), b))) / (mp.log(r4) - mp.log(r3))
    print("      b=%d : slope(3e4..1e5) = %.4f    slope(1e9..1e10) = %.6f" % (b, sl, sl2))
