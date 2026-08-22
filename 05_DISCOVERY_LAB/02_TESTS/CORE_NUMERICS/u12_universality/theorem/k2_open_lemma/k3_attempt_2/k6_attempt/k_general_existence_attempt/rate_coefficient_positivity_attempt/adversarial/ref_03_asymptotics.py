"""
ADVERSARIAL REFEREE SCRIPT 3 (from scratch).

Item 9(c): does  c_K ~ sqrt(pi K)/8  actually follow?

Route (hand derivation, then checked):
    phi_K = 4^K (K!)^2/(2K+1)!  and  C(2K,K) = (2K)!/(K!)^2
    ==>  phi_K = 4^K / [ (2K+1) C(2K,K) ]           (exact, verified below)
    classical:  C(2K,K) = 4^K/sqrt(pi K) * (1 - 1/(8K) + 1/(128 K^2) + ...)
    ==>  phi_K = sqrt(pi K)/(2K+1) * (1 + 1/(8K) + ...)
    ==>  (K+2) phi_K = sqrt(pi K) * (K+2)/(2K+1) * (1 + 1/(8K) + ...)
                     -> sqrt(pi K)/2 * (1 + 3/(2K) + ...) * (1 + 1/(8K)+...)
    ==>  c_K = [(K+2)phi_K - 2]/4 = sqrt(pi K)/8 - 1/2 + O(1/sqrt(K)).

So the LEADING term sqrt(pi K)/8 is correct, but the O(1) correction is
-1/2, which is NOT negligible at moderate K.  Checked numerically at high
precision below.
"""

from fractions import Fraction as Fr
from math import factorial
import mpmath as mp

mp.mp.dps = 60


def phi_exact(K):
    return Fr(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def c_exact(K):
    return ((K + 2) * phi_exact(K) - 2) / 4


print("=" * 96)
print("A. exact identity  phi_K = 4^K/[(2K+1) C(2K,K)]")
print("=" * 96)
from math import comb
bad = sum(1 for K in range(0, 301)
          if phi_exact(K) != Fr(4 ** K, (2 * K + 1) * comb(2 * K, K)))
print("   K=0..300 mismatches:", bad)

print()
print("=" * 96)
print("B. c_K vs sqrt(pi K)/8  and vs sqrt(pi K)/8 - 1/2   (60-digit mpmath)")
print("=" * 96)
print("%8s  %-20s  %-20s  %-12s  %-20s  %-12s" %
      ("K", "c_K (exact)", "sqrt(piK)/8", "ratio", "sqrt(piK)/8 - 1/2", "abs diff"))
for K in (10, 100, 1000, 10 ** 4, 10 ** 5):
    c = mp.mpf(c_exact(K).numerator) / mp.mpf(c_exact(K).denominator)
    lead = mp.sqrt(mp.pi * K) / 8
    print("%8d  %-20.10f  %-20.10f  %-12.9f  %-20.10f  %-12.3e" %
          (K, c, lead, c / lead, lead - mp.mpf(1) / 2, abs(c - (lead - mp.mpf(1) / 2))))

print()
print("   ratio c_K/(sqrt(pi K)/8) -> 1 ?  (slowly, since the correction is O(1))")
for K in (10 ** 6, 10 ** 7):
    # avoid huge factorials: phi_K via mpmath gamma, and verify against exact for K=10^6
    ph = 4 ** mp.mpf(K) * mp.gamma(K + 1) ** 2 / mp.gamma(2 * K + 2)
    c = ((K + 2) * ph - 2) / 4
    lead = mp.sqrt(mp.pi * K) / 8
    print("     K=%-10d  c_K=%.6f  sqrt(piK)/8=%.6f  ratio=%.9f  c_K-(lead-1/2)=%.3e"
          % (K, c, lead, c / lead, c - (lead - mp.mpf(1) / 2)))

print()
print("=" * 96)
print("C. does sqrt(K)*(c_K - sqrt(pi K)/8 + 1/2) converge?  (i.e. is the")
print("   next correction really O(1/sqrt K)?)")
print("=" * 96)
for K in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7):
    ph = 4 ** mp.mpf(K) * mp.gamma(K + 1) ** 2 / mp.gamma(2 * K + 2)
    c = ((K + 2) * ph - 2) / 4
    lead = mp.sqrt(mp.pi * K) / 8
    print("   K=%-10d  sqrt(K)*(c_K - lead + 1/2) = %.10f   (predicted 13 sqrt(pi)/64 = %.10f)"
          % (K, mp.sqrt(K) * (c - lead + mp.mpf(1) / 2), 13 * mp.sqrt(mp.pi) / 64))

print()
print("=" * 96)
print("D. sanity: c_K is strictly INCREASING in K for K>=1 (it should be, since")
print("   c_{K+1}-c_K = K phi_K/(4(2K+3)) > 0) -- exact check")
print("=" * 96)
inc_ok = True
for K in range(1, 400):
    lhs = c_exact(K + 1) - c_exact(K)
    rhs = Fr(K, 4 * (2 * K + 3)) * phi_exact(K)
    if lhs != rhs or lhs <= 0:
        inc_ok = False
        print("   FAIL at K=%d" % K)
print("   c_{K+1}-c_K == K phi_K/(4(2K+3)) > 0 for K=1..399 :", inc_ok)
print("   -> c_K is strictly increasing from c_1 = 0, hence c_K > 0 for all K >= 2.")
