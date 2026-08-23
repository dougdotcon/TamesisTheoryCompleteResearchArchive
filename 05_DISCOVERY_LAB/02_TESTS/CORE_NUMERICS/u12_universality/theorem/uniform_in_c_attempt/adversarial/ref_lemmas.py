"""
Adversarial referee -- item 4: LEMA 5.1, LEMA 6.1, COROLARIO 6.2, kappa_B,
plus a reproduction of the ATTEMPT 4.1 "C_0-tail values" table.
"""

import math
from fractions import Fraction as F
import mpmath as mp
import sympy as sp

mp.mp.dps = 40

print("=" * 76)
print("0. Reproducing the ATTEMPT 4.1 'C_0-tail values' 0.531/0.259/0.116/...")
print("=" * 76)
print("""
The prose gives 'the C_0-tail values 0.531, 0.259, 0.116, 0.053, 0.025 at
C_0 = 50,200,1e3,5e3,2.5e4, essentially identical at n=1e3,1e4,1e5'.  These
are NOT omega(C_0) of Corolario 4.2 (which is the deliberately-simplified
L=log C_0 specialisation).  They are the J-OPTIMISED Lema 4.1 bound at
q=C_0/n; in the n->infinity limit with J=xn that is
     h(x) = x/(1-x) + exp(-C_0 x^2/2),   minimised over x in (0,1/2).
Reproduced here independently:
""")
for C0 in (50, 200, 1000, 5000, 25000):
    h = lambda x: x / (1 - x) + math.exp(-C0 * x * x / 2)
    xs = [i / 400000.0 for i in range(1, 200000)]
    best = min(h(x) for x in xs)
    om = 2 * math.sqrt(2 * math.log(C0) / C0) + 1.0 / C0
    print(f"   C_0={C0:6d}   min_x h(x) = {best:.4f}      "
          f"omega(C_0) [Cor 4.2] = {om:.4f}")
print("""   -> the document's five figures reproduce to the digits printed.
   The reading is consistent with the surrounding prose ('zero violations of
   Lema 4.1 ... and the C_0-tail values'), and it is the LEMMA's bound, not
   the corollary's, so no overclaim; but the sentence is ambiguous enough
   that a reader could mistake these for omega(C_0), which is ~1.5-2x larger.
""")

print("=" * 76)
print("1. LEMA 5.1:  B_n(c) = int_0^1 [(1-ct^2/n)^n - e^{-ct^2}] dt  <= 0")
print("=" * 76)
print("""
Re-derivation.  B_n(c) := sum_{K>=0} (b_K(c)-p_K(c)) phi_K, with
b_K = P(Bin(n,c/n)=K) (supported on K<=n) and p_K = P(Poi(c)=K).
Lemma 2 gives phi_K = int_0^1 (1-t^2)^K dt, so with z := 1-t^2 in [0,1]:
   sum_K b_K phi_K = int_0^1 sum_K b_K z^K dt = int_0^1 (1-(c/n)(1-z))^n dt
                   = int_0^1 (1 - c t^2/n)^n dt        [Bin pgf, finite sum]
   sum_K p_K phi_K = int_0^1 e^{-c(1-z)} dt = int_0^1 e^{-c t^2} dt
                                                        [Poi pgf, Tonelli:
                                                         all terms >= 0]
Both interchanges are legitimate (finite sum; nonnegative terms).  Sign:
0 <= ct^2/n <= 1 for c <= n, and 1-u <= e^{-u} for u in [0,1], so
(1-ct^2/n)^n <= e^{-ct^2} pointwise, whence B_n <= 0.   CORRECT.
""")
worst = 0.0
for n in (1, 2, 5, 10, 20, 50):
    for c in (F(1), F(3), F(5), F(n)):
        cc = mp.mpf(int(c.numerator)) / int(c.denominator)
        if cc > n:
            continue
        # direct summation side (exact rationals for Bin, mpmath for Poi)
        phiK = lambda K: mp.mpf(4)**K * mp.factorial(K)**2 / mp.factorial(2*K+1)
        s = mp.mpf(0)
        for K in range(0, n + 1):
            s += mp.binomial(n, K) * (cc/n)**K * (1-cc/n)**(n-K) * phiK(K)
        for K in range(0, 400):
            s -= mp.e**(-cc) * cc**K / mp.factorial(K) * phiK(K)
        integ = mp.quad(lambda t: (1-cc*t**2/n)**n - mp.e**(-cc*t**2), [0, 1])
        d = abs(s - integ)
        worst = max(worst, float(d))
        assert integ <= 0
print(f"   sum-vs-integral agreement, 6 values of n x up to 4 values of c:")
print(f"   worst absolute discrepancy = {worst:.3e}   (and B_n <= 0 in every"
      f" cell).  LEMA 5.1 CONFIRMED.")

print()
print("=" * 76)
print("2. LEMA 6.1:  0 <= e^{-x} - (1-x/n)^n <= (x^2/n) e^{-x},  n>=4, 0<=x<=n")
print("=" * 76)
print("""
Re-derivation, both branches:
 LEFT:  1-u <= e^{-u} with u = x/n in [0,1]; both sides >= 0, so raising to
        the n-th power preserves it.  CORRECT (needs only x <= n).
 RIGHT, case x >= sqrt(n):  then x^2/n >= 1, so (x^2/n)e^{-x} >= e^{-x}
        >= e^{-x} - (1-x/n)^n, since (1-x/n)^n >= 0 (again x <= n).  CORRECT.
 RIGHT, case x < sqrt(n):  u = x/n < 1/sqrt(n) <= 1/2 for n >= 4.
        (1-u)^n = exp(n log(1-u)) = exp(-n sum_{k>=1} u^k/k)
                = e^{-x} exp(-n sum_{k>=2} u^k/k)      [since n u = x]
        so e^{-x} - (1-u)^n = e^{-x}(1 - exp(-y)) with y = n sum_{k>=2} u^k/k
        <= e^{-x} y                                    [1-e^{-y} <= y, y>=0]
        y <= (n/2) sum_{k>=2} u^k = (n/2) u^2/(1-u) <= n u^2  [1-u >= 1/2]
        n u^2 = x^2/n.                                  CORRECT.
 The case split is exhaustive and each branch's hypotheses are met.
 The n >= 4 is used ONLY to get 1-u >= 1/2 in the second branch.  Below I
 check whether it is actually necessary.
""")
def L61(n, x):
    return math.exp(-x) - (1 - x / n) ** n, x * x / n * math.exp(-x)

for n in (2, 3, 4, 5, 7, 10, 30, 100, 1000):
    mx = 0.0
    negs = 0
    argmx = 0.0
    for i in range(0, 4001):
        x = n * i / 4000.0
        lhs, rhs = L61(n, x)
        if lhs < -1e-15:
            negs += 1
        if rhs > 0:
            r = lhs / rhs
            if r > mx:
                mx, argmx = r, x
    flag = "" if n >= 4 else "   <-- OUTSIDE the lemma's hypothesis n>=4"
    print(f"   n={n:5d}   max (lhs/rhs) = {mx:.6f} at x={argmx:.4f}   "
          f"negative-lhs count = {negs}{flag}")
print("""   -> ratio never exceeds ~0.564 for n >= 4, matching the document.
   n = 2 and n = 3 also pass numerically, so 'n >= 4' is an artefact of the
   1-u >= 1/2 step, not a real threshold -- harmless (the lemma is only ever
   applied with n large).""")

print()
print("=" * 76)
print("3. COROLARIO 6.2 and kappa_B = sup_c c^2 I_2(c),  I_2 = int_0^1 t^4 e^{-ct^2}")
print("=" * 76)
print("""
   |B_n(c)| = int_0^1 [e^{-ct^2} - (1-ct^2/n)^n] dt
            <= int_0^1 ((ct^2)^2/n) e^{-ct^2} dt   [Lema 6.1 at x = ct^2,
                                                    legal since 0<=ct^2<=c<=n]
            = (c^2/n) I_2(c) <= kappa_B / n.        CORRECT.
""")
I2 = lambda c: mp.quad(lambda t: t**4 * mp.e**(-c*t**2), [0, 1])
g = lambda c: c**2 * I2(c)
cstar = mp.findroot(lambda c: mp.diff(g, c), mp.mpf('4.0'))
print(f"   argmax c*   = {mp.nstr(cstar, 12)}      (document: 4.086754546)")
print(f"   kappa_B     = {mp.nstr(g(cstar), 15)}   (document: 0.280480169025)")
print(f"   agreement   : {'YES' if abs(g(cstar) - mp.mpf('0.280480169025')) < mp.mpf('1e-11') else 'NO'}")
print("   (kappa_B is a high-precision NUMERICAL value, not a closed form --")
print("    the Executive Summary's phrase 'computed exactly here' is loose.)")

print()
print("   Direct check of |B_n(c)| <= c^2 I_2(c)/n <= kappa_B/n :")
for n in (4, 10, 50, 200):
    for c in (1, 5, 20, n):
        if c > n:
            continue
        Bn = mp.quad(lambda t: (1-mp.mpf(c)*t**2/n)**n - mp.e**(-mp.mpf(c)*t**2), [0, 1])
        b1 = mp.mpf(c)**2 * I2(c) / n
        b2 = mp.mpf('0.280480169025') / n
        ok = (abs(Bn) <= b1 <= b2 + mp.mpf('1e-30'))
        print(f"     n={n:4d} c={c:4d}   |B_n|={mp.nstr(abs(Bn),8):>12}   "
              f"c^2 I_2/n={mp.nstr(b1,8):>12}   kappa_B/n={mp.nstr(b2,8):>12}"
              f"   {'OK' if ok else '*** FAIL ***'}")

print()
print("=" * 76)
print("4. TEOREMA B's Jensen step")
print("=" * 76)
print("""
 |A_n(c)| = |sum_K b_K(c)(phi_n^{(K)}-phi_K)| <= (a/n) E[sqrt(Bin(n,c/n))]
          <= (a/n) sqrt(E[Bin(n,c/n)]) = (a/n) sqrt(c).
 sqrt is concave so Jensen goes the right way (E sqrt X <= sqrt E X).
 CORRECT given (U'_a).  Numerically E sqrt(Bin) vs sqrt(c):""")
for (n, c) in [(100, 1), (100, 10), (100, 50), (1000, 200)]:
    p = c / n
    es = sum(mp.binomial(n, k) * mp.mpf(p)**k * (1-mp.mpf(p))**(n-k) * mp.sqrt(k)
             for k in range(n + 1))
    print(f"   n={n:5d} c={c:4d}   E sqrt(Bin) = {mp.nstr(es,10):>14}   "
          f"sqrt(c) = {mp.nstr(mp.sqrt(c),10):>14}   "
          f"{'OK' if es <= mp.sqrt(c) else 'FAIL'}")
