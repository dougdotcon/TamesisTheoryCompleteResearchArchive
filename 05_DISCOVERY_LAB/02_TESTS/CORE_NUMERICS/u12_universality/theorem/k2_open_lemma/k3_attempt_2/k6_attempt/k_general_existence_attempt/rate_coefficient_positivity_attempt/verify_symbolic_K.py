#!/usr/bin/env python3
"""
verify_symbolic_K.py  --  wave 9, front (b), RATE-COEFFICIENT-POSITIVITY-ATTEMPT

Machine verification of every ALGEBRAIC step of the positivity proof with `K`
kept SYMBOLIC (sympy Symbol, positive integer), not sampled.  The one step that
is not a symbolic-`K` simplification -- the binomial-row symmetry
sum_{j=K+1}^{2K} C(2K,j) = (4^K - C(2K,K))/2 -- is a classical two-line fact
proved in prose in ATTEMPT.md §3, Step 3; it is checked numerically here for a
large range as a guard against mis-statement, and its two ingredients
(row sum = 4^K, and C(2K,j) = C(2K,2K-j)) are checked symbolically.

Steps verified, K symbolic:

  S1  prod_{i=1}^{k+1} (K+i)  ==  (K+k+1)! / K!            (k symbolic too)
  S2  the summand of F_{K-1}(1,1) equals (K-1)!K!/((K-1-k)!(K+k+1)!)
  S3  (2K)! / ((K-1-k)!(K+k+1)!) == C(2K, K+k+1)
  S4  binomial row symmetry + row sum   (the two ingredients of Step 3)
  S5  (3/4)phi_K * (2K)!/((K-1)!K!)  ==  (3/4) 4^K K/(2K+1)
  S6  c_K == (K+2)4^K/(4(2K+1)C(2K,K)) - 1/2       [given S1-S5]
  S7  u_{K+1}/u_K == 2(K+1)(K+3)/((K+2)(2K+3))     [THE proof step]
  S8  2(K+1)(K+3) - (K+2)(2K+3) == K  > 0 for K>=1
  S9  u_1 == 1   (equivalently c_1 == 0)
  S10 asymptotics:  c_K = sqrt(pi K)/8 - 1/2 + 13 sqrt(pi)/(64 sqrt(K)) + O(K^-3/2)
  S11 the rigorous elementary lower bound c_K >= (K+2)sqrt(3K+1)/(4(2K+1)) - 1/2,
      via the classical  C(2K,K) <= 4^K/sqrt(3K+1)  (re-proved here by the same
      ratio technique, symbolically)
"""

import sympy as sp

K, k, i, j = sp.symbols('K k i j', positive=True, integer=True)
FAIL = []


def check(name, expr_is_zero, extra=""):
    """expr_is_zero: a sympy expression that must simplify to 0, or a bool."""
    if isinstance(expr_is_zero, bool):
        ok = expr_is_zero
        shown = ""
    else:
        s = sp.simplify(sp.together(sp.expand_func(sp.simplify(expr_is_zero))))
        ok = (s == 0)
        shown = "" if ok else f"  residual = {s}"
    if not ok:
        FAIL.append(name)
    print(f"  [{'OK  ' if ok else 'FAIL'}] {name}{('  :: ' + extra) if extra else ''}{shown}")


print("=" * 78)
print("verify_symbolic_K.py -- K kept SYMBOLIC throughout")
print("=" * 78)
print()
print("PART P -- the PRIMARY route: everything collapses onto phi_K itself.")
print("  (P1-P6 are the proof as ATTEMPT.md §3-§4 states it; S1-S11 below are")
print("   the equivalent central-binomial route, kept as a cross-check.)")
print()

phi_ = 4 ** K * sp.gamma(K + 1) ** 2 / sp.gamma(2 * K + 2)       # Wallis integral
Cb_ = sp.gamma(2 * K + 1) / sp.gamma(K + 1) ** 2                 # C(2K,K)

check("P0  phi_K == 4^K / ((2K+1) C(2K,K)),  K symbolic",
      sp.simplify(sp.expand_func(phi_ - 4 ** K / ((2 * K + 1) * Cb_))))

check("P1  (K+2)4^K/(4(2K+1)C(2K,K)) - 1/2  ==  [(K+2)phi_K - 2]/4,  K symbolic",
      sp.simplify(sp.expand_func(
          (K + 2) * 4 ** K / (4 * (2 * K + 1) * Cb_) - sp.Rational(1, 2)
          - ((K + 2) * phi_ - 2) / 4)))

check("P2  [(K-1)!K!/(2K)!](4^K - C(2K,K))/2  ==  [(2K+1)phi_K - 1]/(2K),  K symbolic",
      sp.simplify(sp.expand_func(
          sp.gamma(K) * sp.gamma(K + 1) / sp.gamma(2 * K + 1) * (4 ** K - Cb_) / 2
          - ((2 * K + 1) * phi_ - 1) / (2 * K))))

check("P3  phi_{K+1}/phi_K == (2K+2)/(2K+3),  K symbolic",
      sp.simplify(sp.expand_func(sp.simplify(phi_.subs(K, K + 1) / phi_)
                                 - (2 * K + 2) / (2 * K + 3))))

# v_K := (K+2) phi_K  -- the object of the proof
v_ = (K + 2) * phi_
check("P4  v_{K+1}/v_K - 1 == K/((K+2)(2K+3))  > 0 for K>=1,  K symbolic",
      sp.simplify(sp.expand_func(sp.simplify(v_.subs(K, K + 1) / v_) - 1
                                 - K / ((K + 2) * (2 * K + 3)))))

check("P5  v_1 == 2 exactly (the equality case; c_1 = 0)",
      sp.simplify(v_.subs(K, 1) - 2))

# phi_K as an integral and as a product -- both classical, both checked
xv = sp.symbols('xv', positive=True)
bad = [m for m in range(0, 13)
       if sp.simplify(sp.integrate((1 - xv ** 2) ** m, (xv, 0, 1))
                      - sp.Rational(4 ** m * sp.factorial(m) ** 2,
                                    sp.factorial(2 * m + 1))) != 0]
check("P6a phi_K == int_0^1 (1-x^2)^K dx  (checked K=0..12 by symbolic integration)",
      not bad, f"mismatches: {bad}")
check("P6b phi_K == prod_{j=1}^K 2j/(2j+1) follows from P3 with phi_0 = 1",
      sp.simplify(phi_.subs(K, 0) - 1))

# ---- P7 : the MANIFESTLY-POSITIVE representation ---------------------------
# Telescoping v_K = 2 + sum_{j=1}^{K-1} (v_{j+1} - v_j) with
# v_{j+1} - v_j = v_j * j/((j+2)(2j+3)) = j phi_j /(2j+3)   (since v_j = (j+2)phi_j)
# gives  c_K = (v_K - 2)/4 = (1/4) sum_{j=1}^{K-1} j phi_j/(2j+3)  -- every term
# strictly positive.  This is the representation that makes positivity obvious.
jj = sp.symbols('jj', positive=True, integer=True)
phi_j = 4 ** jj * sp.gamma(jj + 1) ** 2 / sp.gamma(2 * jj + 2)
v_j = (jj + 2) * phi_j
check("P7a v_{j+1} - v_j == j*phi_j/(2j+3),  j symbolic  (the telescoping increment)",
      sp.simplify(sp.expand_func(sp.simplify(v_.subs(K, jj + 1) - v_j)
                                 - jj * phi_j / (2 * jj + 3))))
# assembled, exactly, over a range (the telescoping itself is trivial induction)
from fractions import Fraction as Fr
from math import factorial as fct
def phiQ(m):
    return Fr(4 ** m * fct(m) ** 2, fct(2 * m + 1))
bad = [m for m in range(1, 401)
       if sum(Fr(j, 2 * j + 3) * phiQ(j) for j in range(1, m)) / 4
       != ((m + 2) * phiQ(m) - 2) / 4]
check("P7b c_K == (1/4) sum_{j=1}^{K-1} j*phi_j/(2j+3), exact, K=1..400", not bad,
      f"mismatches: {bad}")
check("P7c every term j*phi_j/(2j+3) is strictly positive (phi_j > 0, j >= 1)",
      all(Fr(j, 2 * j + 3) * phiQ(j) > 0 for j in range(1, 401)))
print()
print("PART S -- the equivalent central-binomial route (cross-check)")
print()

# ---- S1 : the product in the denominator of F_r(t,b) at r=K-1, b=1 -----------
lhs = sp.product(K + i, (i, 1, k + 1))
rhs = sp.gamma(K + k + 2) / sp.gamma(K + 1)
check("S1  prod_{i=1}^{k+1}(K+i) == (K+k+1)!/K!,  K,k symbolic",
      sp.simplify(sp.expand_func(lhs - rhs)))

# ---- S2 : the summand of F_{K-1}(1,1) ---------------------------------------
# F_r(t,b) = sum_{k=0}^{r} r!/(r-k)! t^k / prod_{i=1}^{k+1}(r+b+i)      [k6 §2.3]
# at r = K-1, b = 1, t = 1:  (K-1)!/(K-1-k)! / prod_{i=1}^{k+1}(K+i)
summand_raw = sp.gamma(K) / sp.gamma(K - k) / rhs
summand_tgt = sp.gamma(K) * sp.gamma(K + 1) / (sp.gamma(K - k) * sp.gamma(K + k + 2))
check("S2  summand == (K-1)!K!/((K-1-k)!(K+k+1)!),  K,k symbolic",
      sp.simplify(sp.expand_func(summand_raw - summand_tgt)))

# ---- S3 : that summand, times (2K)!, is a central-binomial-row entry ---------
lhs3 = sp.gamma(2 * K + 1) / (sp.gamma(K - k) * sp.gamma(K + k + 2))
rhs3 = sp.binomial(2 * K, K + k + 1)
check("S3  (2K)!/((K-1-k)!(K+k+1)!) == C(2K,K+k+1),  K,k symbolic",
      sp.simplify(sp.expand_func(sp.rewrite(lhs3, sp.gamma) if hasattr(sp, 'rewrite')
                                 else lhs3) - sp.expand_func(rhs3.rewrite(sp.gamma))))

# ---- S4 : the two ingredients of the binomial-row step ----------------------
check("S4a C(2K,j) == C(2K,2K-j),  K,j symbolic",
      sp.simplify(sp.expand_func((sp.binomial(2 * K, j)
                                  - sp.binomial(2 * K, 2 * K - j)).rewrite(sp.gamma))))
n_ = sp.symbols('n_', positive=True, integer=True)
check("S4b sum_{j=0}^{2K} C(2K,j) == 4^K  (binomial theorem)",
      sp.simplify(sp.Sum(sp.binomial(2 * K, j), (j, 0, 2 * K)).doit() - 4 ** K))
# guard: the assembled identity, numerically, over a wide range
bad = [m for m in range(1, 301)
       if 2 * sum(sp.binomial(2 * m, jj) for jj in range(m + 1, 2 * m + 1))
       != 4 ** m - sp.binomial(2 * m, m)]
check("S4c assembled: 2*sum_{j=K+1}^{2K}C(2K,j) == 4^K - C(2K,K), K=1..300", not bad)

# ---- S5 : the phi_K side ----------------------------------------------------
phi_K = 4 ** K * sp.gamma(K + 1) ** 2 / sp.gamma(2 * K + 2)
lhs5 = sp.Rational(3, 4) * phi_K * sp.gamma(2 * K + 1) / (sp.gamma(K) * sp.gamma(K + 1))
rhs5 = sp.Rational(3, 4) * 4 ** K * K / (2 * K + 1)
check("S5  (3/4)phi_K*(2K)!/((K-1)!K!) == (3/4)4^K K/(2K+1),  K symbolic",
      sp.simplify(sp.expand_func(lhs5 - rhs5)))

# ---- S6 : the assembled closed form for c_K --------------------------------
# c_K = K[phi_K/4 + F - phi_K] = K[F - (3/4)phi_K]
#     = K * (K-1)!K!/(2K)! * [ (4^K - C(2K,K))/2 - (3/4)4^K K/(2K+1) ]
Cbin = sp.gamma(2 * K + 1) / sp.gamma(K + 1) ** 2          # C(2K,K)
c_assembled = (K * sp.gamma(K) * sp.gamma(K + 1) / sp.gamma(2 * K + 1)
               * ((4 ** K - Cbin) / 2 - sp.Rational(3, 4) * 4 ** K * K / (2 * K + 1)))
c_closed = (K + 2) * 4 ** K / (4 * (2 * K + 1) * Cbin) - sp.Rational(1, 2)
check("S6  c_K == (K+2)4^K/(4(2K+1)C(2K,K)) - 1/2,  K symbolic",
      sp.simplify(sp.expand_func(c_assembled - c_closed)))

# ---- S7 : THE proof step ----------------------------------------------------
def u_of(x):
    Cb = sp.gamma(2 * x + 1) / sp.gamma(x + 1) ** 2
    return (x + 2) * 4 ** x / (2 * (2 * x + 1) * Cb)

ratio = sp.simplify(sp.expand_func(sp.simplify(u_of(K + 1) / u_of(K))))
target = 2 * (K + 1) * (K + 3) / ((K + 2) * (2 * K + 3))
check("S7  u_{K+1}/u_K == 2(K+1)(K+3)/((K+2)(2K+3)),  K symbolic",
      sp.simplify(ratio - target), extra=f"sympy got {sp.nsimplify(ratio)}")

# ---- S8 : the sign of the ratio minus one -----------------------------------
check("S8  2(K+1)(K+3) - (K+2)(2K+3) == K   (>0 for K>=1),  K symbolic",
      sp.expand(2 * (K + 1) * (K + 3) - (K + 2) * (2 * K + 3) - K))

# ---- S9 : the anchor --------------------------------------------------------
check("S9  u_1 == 1  (equivalently c_1 == 0)",
      sp.simplify(u_of(1) - 1))
check("S9' c_K at K=1 is 0", sp.simplify(c_closed.subs(K, 1)))

# ---- S10 : asymptotics ------------------------------------------------------
# sympy has no gamma-at-infinity aseries, so feed it the CLASSICAL Wallis-ratio
# expansion (a standard, textbook fact, used here only for a corroborative
# asymptotic -- it is NOT part of the positivity proof, which is S7-S9):
#     C(2K,K)/4^K = (pi K)^{-1/2} (1 - 1/(8K) + 1/(128 K^2) + 5/(1024 K^3) + ...)
x = sp.symbols('x', positive=True)          # x = 1/K
W = sp.sqrt(x / sp.pi) * (1 - x / 8 + x ** 2 / 128 + 5 * x ** 3 / 1024)
c_in_x = ((1 / x + 2) / (4 * (2 / x + 1))) / W - sp.Rational(1, 2)
print()
print("  S10  asymptotic expansion of c_K as K -> oo, via the classical Wallis ratio:")
asy = sp.series(sp.simplify(c_in_x), x, 0, sp.Rational(3, 2)).removeO()
print(f"       c_K ~ {sp.simplify(asy.subs(x, 1 / K))}")
lead = sp.sqrt(sp.pi * K) / 8 - sp.Rational(1, 2) + 13 * sp.sqrt(sp.pi) / (64 * sp.sqrt(K))
check("S10a sympy's series agrees with the claimed 3 terms",
      sp.simplify(sp.expand(asy.subs(x, 1 / K) - lead)))
print(f"       claimed:  sqrt(pi*K)/8 - 1/2 + 13*sqrt(pi)/(64*sqrt(K)) + O(K^-3/2)")
diffs = []
for m in [200, 1000, 5000, 20000, 100000]:
    exact = sp.Rational((m + 2) * 4 ** m, 4 * (2 * m + 1) * sp.binomial(2 * m, m)) - sp.Rational(1, 2)
    approx = sp.N(lead.subs(K, m), 30)
    d = abs(sp.N(exact, 30) - approx)
    diffs.append((m, sp.N(exact, 20), approx, d, d * m ** sp.Rational(3, 2)))
print(f"       {'K':>8} {'c_K exact':>20} {'3-term asympt.':>20} {'|diff|':>12} "
      f"{'|diff|*K^{3/2}':>16}")
for m, e, a, d, s in diffs:
    print(f"       {m:>8} {float(e):>20.12f} {float(a):>20.12f} {float(d):>12.3e} "
          f"{float(s):>16.6f}")
check("S10 |c_K - 3-term asymptotic| * K^{3/2} stays bounded (=> the expansion is "
      "right and c_K -> +oo like sqrt(pi K)/8)",
      all(float(s) < 1.0 for _, _, _, _, s in diffs))

# ---- S11 : the elementary rigorous lower bound ------------------------------
# classical: a_K := C(2K,K) sqrt(3K+1) / 4^K is non-increasing, a_0 = a_1 = 1.
aK = sp.binomial(2 * K, K) * sp.sqrt(3 * K + 1) / 4 ** K
ratio_a = sp.simplify(sp.expand_func(sp.simplify(
    (sp.gamma(2 * K + 3) / sp.gamma(K + 2) ** 2 * sp.sqrt(3 * K + 4) / 4 ** (K + 1))
    / (sp.gamma(2 * K + 1) / sp.gamma(K + 1) ** 2 * sp.sqrt(3 * K + 1) / 4 ** K))))
target_a = (2 * K + 1) / (2 * (K + 1)) * sp.sqrt((3 * K + 4) / (3 * K + 1))
check("S11a a_{K+1}/a_K == (2K+1)/(2(K+1)) * sqrt((3K+4)/(3K+1)),  K symbolic",
      sp.simplify(ratio_a - target_a))
check("S11b 4(K+1)^2(3K+1) - (2K+1)^2(3K+4) == K  (>=0), so a_K non-increasing",
      sp.expand(4 * (K + 1) ** 2 * (3 * K + 1) - (2 * K + 1) ** 2 * (3 * K + 4) - K))
# hence C(2K,K) <= 4^K/sqrt(3K+1), hence:
lb = (K + 2) * sp.sqrt(3 * K + 1) / (4 * (2 * K + 1)) - sp.Rational(1, 2)
check("S11c the lower bound is positive for K>=2:  (4K+2)^2 < (K+2)^2(3K+1) "
      "reduces to 3K^2 < 3K^3", sp.expand((K + 2) ** 2 * (3 * K + 1) - (4 * K + 2) ** 2
                                          - 3 * K ** 3 + 3 * K ** 2))
print()
print("  S11  the resulting explicit rigorous lower bound c_K >= "
      "(K+2)sqrt(3K+1)/(4(2K+1)) - 1/2 :")
print(f"       {'K':>8} {'lower bound':>18} {'c_K exact':>18} {'bound valid':>12}")
allok = True
for m in [2, 3, 13, 20, 100, 1000, 10000]:
    exact = sp.Rational((m + 2) * 4 ** m, 4 * (2 * m + 1) * sp.binomial(2 * m, m)) - sp.Rational(1, 2)
    bnd = sp.N(lb.subs(K, m), 25)
    v = (bnd <= sp.N(exact, 25)) and (bnd > 0)
    allok &= bool(v)
    print(f"       {m:>8} {float(bnd):>18.12f} {float(exact):>18.12f} "
          f"{'yes' if v else 'NO':>12}")
check("S11d lower bound is valid and strictly positive at K=2,3,13,20,100,1000,10000",
      allok)

print()
if FAIL:
    print("RESULT:  ***FAILURES***:", FAIL)
    raise SystemExit(1)
print("RESULT:  every symbolic-K step of the positivity proof verified by sympy.")
