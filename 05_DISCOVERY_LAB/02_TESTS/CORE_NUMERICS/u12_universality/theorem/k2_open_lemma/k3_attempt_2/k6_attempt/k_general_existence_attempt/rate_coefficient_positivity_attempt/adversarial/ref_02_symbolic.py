"""
ADVERSARIAL REFEREE SCRIPT 2 (from scratch).

Symbolic verification, with K a genuine sympy Symbol (positive integer), of
every load-bearing algebraic step:

  (S1) Lemma 1 collapse:  F_{K-1}(1,1) == [(2K+1) phi_K - 1]/(2K)
       -- done at the level of the GAMMA-function closed form, K symbolic,
          using phi_K = 4^K Gamma(K+1)^2 / Gamma(2K+2) and
          F_{K-1}(1,1) = [Gamma(K)Gamma(K+1)/Gamma(2K+1)] * (4^K - C(2K,K))/2.
  (S2) Theorem A:  K*[phi/4 + Lemma1 - phi] == [(K+2) phi - 2]/4, phi symbolic.
  (S3) Wallis ratio: phi_{K+1}/phi_K == (2K+2)/(2K+3).
  (S4) The load-bearing cancellation: 2(K+1)(K+3) - (K+2)(2K+3) == K.
  (S5) v_1 = 3 phi_1 = 2 exactly.
  (S6) Telescoping increment: v_{K+1} - v_K == K phi_K/(2K+3).
  (S7) Binomial-row-tail identity: sum_{j=K+1}^{2K} C(2K,j) == (4^K - C(2K,K))/2.
  (S8) The "constant in k" claim: (K-1-k) + (K+k+1) == 2K, symbolic in k and K.
  (S9) Second proof's ratio argument for C(2K,K) <= 4^K/sqrt(3K+1):
       a_{K+1}/a_K squared minus 1 has numerator K over positive denominator.
  (S10) The cubic identity: (K+2)^2(3K+1) - (4K+2)^2 == 3K^2(K-1).
  (S11) Asymptotics: c_K ~ sqrt(pi K)/8 from the classical central-binomial
        expansion.
"""

import sympy as sp

K, k, j, ph = sp.symbols('K k j phi', positive=True)

print("=" * 90)
print("S8: the 'constant in k' claim inside Lemma 1")
print("=" * 90)
expr = sp.simplify((K - 1 - k) + (K + k + 1) - 2 * K)
print("  (K-1-k)+(K+k+1) - 2K  simplifies to:", expr, " -> exact identity:", expr == 0)

print()
print("=" * 90)
print("S7: binomial row tail, sum_{j=K+1}^{2K} C(2K,j) = (4^K - C(2K,K))/2")
print("=" * 90)
# Derivation, restated: sum_{j=0}^{2K} C(2K,j) = 2^{2K} = 4^K  (binomial theorem at x=1)
# and C(2K,j) = C(2K,2K-j) (row symmetry) so
#   sum_{j=0}^{K-1} C(2K,j) = sum_{j=K+1}^{2K} C(2K,j) =: S,
# hence 2S + C(2K,K) = 4^K.  Verified numerically-exactly below for many K.
bad = 0
for Kv in list(range(1, 61)) + [100, 250, 501, 1000]:
    S = sum(sp.binomial(2 * Kv, jj) for jj in range(Kv + 1, 2 * Kv + 1))
    rhs = sp.Rational(4 ** Kv - sp.binomial(2 * Kv, Kv), 2)
    full = sum(sp.binomial(2 * Kv, jj) for jj in range(0, 2 * Kv + 1))
    sym = all(sp.binomial(2 * Kv, jj) == sp.binomial(2 * Kv, 2 * Kv - jj)
              for jj in range(0, 2 * Kv + 1))
    if S != rhs or full != 4 ** Kv or not sym:
        bad += 1
        print("  FAIL at K=%d" % Kv)
print("  checked K in 1..60 plus {100,250,501,1000}: failures =", bad)
print("  (row sums = 4^K exactly, row symmetry exact, tail = (4^K - C(2K,K))/2 exactly)")

print()
print("=" * 90)
print("S1: Lemma 1, K SYMBOLIC, via gamma functions")
print("=" * 90)
phiK = 4 ** K * sp.gamma(K + 1) ** 2 / sp.gamma(2 * K + 2)
central = sp.gamma(2 * K + 1) / sp.gamma(K + 1) ** 2          # C(2K,K)
F_mine = (sp.gamma(K) * sp.gamma(K + 1) / sp.gamma(2 * K + 1)) * (4 ** K - central) / 2
F_target = ((2 * K + 1) * phiK - 1) / (2 * K)
d = sp.simplify(sp.expand_func(sp.simplify(F_mine - F_target)))
print("  F_mine - F_target  simplifies to:", d, " -> identity:", sp.simplify(d) == 0)

print()
print("=" * 90)
print("S2: Theorem A one-line algebra (phi symbolic, K symbolic)")
print("=" * 90)
lemma1 = ((2 * K + 1) * ph - 1) / (2 * K)
cK = K * (ph / 4 + lemma1 - ph)
target = ((K + 2) * ph - 2) / 4
print("  c_K expanded          :", sp.simplify(sp.expand(cK)))
print("  claimed closed form   :", sp.simplify(sp.expand(target)))
print("  difference            :", sp.simplify(sp.expand(cK - target)),
      " -> identity:", sp.simplify(sp.expand(cK - target)) == 0)

print()
print("=" * 90)
print("S3: Wallis ratio phi_{K+1}/phi_K = (2K+2)/(2K+3)")
print("=" * 90)
phiK1 = 4 ** (K + 1) * sp.gamma(K + 2) ** 2 / sp.gamma(2 * K + 4)
ratio = sp.simplify(sp.expand_func(sp.simplify(phiK1 / phiK)))
print("  phi_{K+1}/phi_K =", ratio)
print("  minus (2K+2)/(2K+3) :", sp.simplify(ratio - (2 * K + 2) / (2 * K + 3)))

print()
print("=" * 90)
print("S4: THE load-bearing cancellation  2(K+1)(K+3) - (K+2)(2K+3) = K")
print("=" * 90)
lhs = sp.expand(2 * (K + 1) * (K + 3))
rhs = sp.expand((K + 2) * (2 * K + 3))
print("  2(K+1)(K+3)   =", lhs)
print("  (K+2)(2K+3)   =", rhs)
print("  difference    =", sp.expand(lhs - rhs), " -> equals K:", sp.expand(lhs - rhs - K) == 0)

print()
print("=" * 90)
print("S5: v_1 = 3 phi_1 = 2 exactly")
print("=" * 90)
phi1 = sp.Rational(4 ** 1 * sp.factorial(1) ** 2, sp.factorial(3))
print("  phi_1 =", phi1, "   3*phi_1 =", 3 * phi1, "   == 2 exactly:", 3 * phi1 == 2)
print("  c_1 = ((1+2)*phi_1 - 2)/4 =", sp.Rational((1 + 2) * phi1 - 2, 4),
      " -> EXACTLY zero:", ((1 + 2) * phi1 - 2) / 4 == 0)

print()
print("=" * 90)
print("S6: telescoping increment v_{K+1} - v_K = K phi_K/(2K+3)")
print("=" * 90)
vK = (K + 2) * ph
vK1 = (K + 3) * ph * (2 * K + 2) / (2 * K + 3)   # phi_{K+1} = phi_K (2K+2)/(2K+3)
inc = sp.simplify(sp.expand(vK1 - vK))
print("  v_{K+1} - v_K =", sp.factor(inc))
print("  minus K*phi/(2K+3) :", sp.simplify(inc - K * ph / (2 * K + 3)),
      " -> identity:", sp.simplify(inc - K * ph / (2 * K + 3)) == 0)

print()
print("=" * 90)
print("S9: second proof -- ratio argument for a_K := 4^K/(C(2K,K) sqrt(3K+1))")
print("=" * 90)
# a_{K+1}/a_K = 4 * C(2K,K)/C(2K+2,K+1) * sqrt((3K+1)/(3K+4))
#             = [2(K+1)/(2K+1)] * sqrt((3K+1)/(3K+4))
ratio_binom = sp.simplify(sp.binomial(2 * K + 2, K + 1) / sp.binomial(2 * K, K))
print("  C(2K+2,K+1)/C(2K,K) =", sp.simplify(sp.expand_func(ratio_binom)),
      " (expect 2(2K+1)/(K+1))")
print("  check                :",
      sp.simplify(sp.expand_func(ratio_binom) - 2 * (2 * K + 1) / (K + 1)))
sq = sp.together(4 * (K + 1) ** 2 * (3 * K + 1) / ((2 * K + 1) ** 2 * (3 * K + 4)))
num = sp.expand(4 * (K + 1) ** 2 * (3 * K + 1))
den = sp.expand((2 * K + 1) ** 2 * (3 * K + 4))
print("  (a_{K+1}/a_K)^2 numerator  :", num)
print("  (a_{K+1}/a_K)^2 denominator:", den)
print("  numerator - denominator    :", sp.expand(num - den), " -> equals K:",
      sp.expand(num - den - K) == 0)

print()
print("=" * 90)
print("S10: the cubic identity  (K+2)^2(3K+1) - (4K+2)^2 = 3K^2(K-1)")
print("=" * 90)
lhs2 = sp.expand((K + 2) ** 2 * (3 * K + 1) - (4 * K + 2) ** 2)
print("  LHS expanded =", lhs2)
print("  3K^2(K-1)    =", sp.expand(3 * K ** 2 * (K - 1)))
print("  difference   =", sp.expand(lhs2 - 3 * K ** 2 * (K - 1)),
      " -> identity:", sp.expand(lhs2 - 3 * K ** 2 * (K - 1)) == 0)

print()
print("=" * 90)
print("S9b: is C(2K,K) <= 4^K/sqrt(3K+1) actually TRUE?  exact rational check")
print("=" * 90)
bad = 0
tight = []
for Kv in list(range(0, 201)) + [500, 1000, 3000]:
    lhs_sq = sp.Integer(sp.binomial(2 * Kv, Kv)) ** 2 * (3 * Kv + 1)
    rhs_sq = sp.Integer(4) ** (2 * Kv)
    if lhs_sq > rhs_sq:
        bad += 1
        print("  FAIL at K=%d" % Kv)
    if lhs_sq == rhs_sq:
        tight.append(Kv)
print("  C(2K,K)^2 (3K+1) <= 16^K for K in 0..200 plus {500,1000,3000}: failures =", bad)
print("  equality cases found at K =", tight)

print()
print("=" * 90)
print("S11: asymptotics of c_K")
print("=" * 90)
n = sp.symbols('n', positive=True)
# classical: C(2K,K) = 4^K/sqrt(pi K) * (1 - 1/(8K) + 1/(128 K^2) + ...)
# so phi_K = 4^K/((2K+1) C(2K,K)) = sqrt(pi K)/(2K+1) * (1 + 1/(8K) + ...)
ser = sp.series(sp.gamma(2 * n + 1) / sp.gamma(n + 1) ** 2 * sp.sqrt(sp.pi * n) / 4 ** n,
                n, sp.oo, 3)
print("  C(2K,K) sqrt(pi K)/4^K  ~", sp.simplify(ser))
phi_asym = sp.sqrt(sp.pi * n) / (2 * n + 1) * (1 / sp.simplify(ser.removeO()))
cK_asym = ((n + 2) * phi_asym - 2) / 4
print("  c_K expansion at K->oo :",
      sp.simplify(sp.series(cK_asym, n, sp.oo, 2)))
print("  leading term should be sqrt(pi K)/8 = %s" % sp.sqrt(sp.pi * n) / 8)
print("  numeric ratio c_K / (sqrt(pi K)/8):")
from fractions import Fraction as Fr
from math import factorial
for Kv in (10, 100, 1000, 10000, 100000):
    ph_ex = Fr(4 ** Kv * factorial(Kv) ** 2, factorial(2 * Kv + 1))
    c_ex = ((Kv + 2) * ph_ex - 2) / 4
    print("    K=%-7d  c_K=%.6f   sqrt(pi K)/8=%.6f   ratio=%.8f   c_K-(sqrt(piK)/8-1/2)=%.3e"
          % (Kv, float(c_ex), float(sp.sqrt(sp.pi * Kv) / 8),
             float(c_ex) / float(sp.sqrt(sp.pi * Kv) / 8),
             float(c_ex) - (float(sp.sqrt(sp.pi * Kv) / 8) - 0.5)))
