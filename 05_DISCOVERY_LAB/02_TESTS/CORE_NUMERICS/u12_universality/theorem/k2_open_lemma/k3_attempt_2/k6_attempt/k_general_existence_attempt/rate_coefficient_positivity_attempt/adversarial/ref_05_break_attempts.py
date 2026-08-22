"""
ADVERSARIAL REFEREE SCRIPT 5 (from scratch).

Deliberate attempts to BREAK the claim, plus two predictions of my own that
go beyond anything the target document tested.

B1. Exhaustive exact positivity + strict-monotonicity sweep, K = 1..3000,
    computed from the CLOSED FORM, and separately K = 1..400 from the RAW
    definition.  Any K with c_K <= 0 (K>=2), or c_{K+1} <= c_K (K>=1), is a
    counterexample and would be printed.

B2. Boundary probing: K = 0 and K = 1 (the equality anchor) and the exact
    values of v_K near the anchor -- is K=1 really the ONLY integer equality
    case for K>=1, and is the equality exact (Fraction) rather than
    float-close?

B3. Does the induction actually need anything the document did not state?
    Re-run it as a literal machine induction over Fractions: start from
    v_1 = 2 and apply ONLY v_{K+1} = v_K * (1 + K/((K+2)(2K+3))), never
    touching phi_K again; check the resulting sequence equals (K+2)phi_K
    and exceeds 2 from K=2 on.  (If the recursion did not actually generate
    v_K, the telescoping/induction would be a non sequitur.)

B4. MY OWN PREDICTIONS, beyond the target's section 6 (which stops at K=9):
    from Theorem A I predict the exact 1/n coefficient of varphi_n^{(K)}
    for K = 10, 11, 12 to be 200965/646646, 106135/312018 and
    1779879/4828850 respectively, and the degree in 1/n to be exactly K+1.
    Tested against my own from-scratch raw-chain implementation with
    out-of-sample validation.  A failure here would mean the object proved
    positive is NOT the rate coefficient.

B5. Is c_K > 0 robust to the exact definition used?  Compute c_K by four
    genuinely different formulas and demand all four agree exactly.
"""

from fractions import Fraction as Fr
from math import factorial, comb
import sys

sys.setrecursionlimit(1000000)


def phi(K):
    return Fr(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def F_closed(r, t, b):
    tot = Fr(0)
    for k in range(r + 1):
        den = 1
        for i in range(1, k + 2):
            den *= (r + b + i)
        tot += Fr(factorial(r), factorial(r - k)) * (t ** k) / den
    return tot


print("=" * 100)
print("B1. exhaustive exact sweep for a counterexample")
print("=" * 100)
prev = None
counter = []
nonmono = []
for K in range(1, 3001):
    c = ((K + 2) * phi(K) - 2) / 4
    if K >= 2 and c <= 0:
        counter.append(K)
    if prev is not None and not (c > prev):
        nonmono.append(K)
    prev = c
print("   closed form, K=1..3000:  counterexamples to c_K>0 (K>=2):", counter or "NONE")
print("                            failures of strict monotonicity:", nonmono or "NONE")

counter2 = []
for K in range(1, 401):
    c = K * (phi(K) / 4 + F_closed(K - 1, Fr(1), 1) - phi(K))
    if K >= 2 and c <= 0:
        counter2.append(K)
    if c != ((K + 2) * phi(K) - 2) / 4:
        counter2.append(("closed-form mismatch", K))
print("   RAW definition, K=1..400: counterexamples / mismatches:", counter2 or "NONE")

print()
print("=" * 100)
print("B2. boundary probing around the equality anchor")
print("=" * 100)
for K in range(0, 6):
    v = (K + 2) * phi(K)
    c = (v - 2) / 4
    print("   K=%d  phi_K=%-12s v_K=(K+2)phi_K=%-12s  v_K-2=%-12s  c_K=%-12s  c_K==0: %s"
          % (K, phi(K), v, v - 2, c, c == 0))
eq = [K for K in range(0, 3001) if (K + 2) * phi(K) == 2]
print("   ALL integers K in 0..3000 with (K+2)phi_K EXACTLY 2:", eq)
print("   -> the equality is exact rational equality (Fraction ==), not float proximity.")
print("   note: K=0 is also an exact equality case (c_0 = 0), outside the K>=1 range")
print("         the document quantifies over; harmless, and consistent with the")
print("         increment K*phi_K/(2K+3) vanishing at K=0.")

print()
print("=" * 100)
print("B3. literal machine induction using ONLY the recursion the proof uses")
print("=" * 100)
v = Fr(2)          # v_1 = 3*phi_1 = 2, the anchor
ok = True
for K in range(1, 1501):
    if v != (K + 2) * phi(K):
        ok = False
        print("   RECURSION DOES NOT GENERATE v_K at K=%d" % K)
        break
    if K >= 2 and not v > 2:
        ok = False
        print("   v_K <= 2 at K=%d" % K)
        break
    v = v * (1 + Fr(K, (K + 2) * (2 * K + 3)))
print("   starting from v_1=2 and applying ONLY v_{K+1}=v_K(1+K/((K+2)(2K+3))):")
print("   generated sequence == (K+2)phi_K for K=1..1500, and > 2 for K>=2 :", ok)

print()
print("=" * 100)
print("B4. MY OWN PREDICTIONS: extend the finite-n corroboration to K=10,11,12")
print("=" * 100)


def chain(n, K):
    gmemo, hmemo = {}, {}

    def g(a, b, r):
        m = n - a
        if m <= 0:
            return Fr(0)
        key = (a, b, r)
        if key in gmemo:
            return gmemo[key]
        val = Fr(1, m)
        if r > 0:
            val += Fr(r, m) * h(a + 1, b, r - 1)
        coef = m - 1 - r - b
        if coef > 0:
            val += Fr(coef, m) * g(a + 1, b, r)
        gmemo[key] = val
        return val

    def h(a, b, r):
        key = (a, b, r)
        if key in hmemo:
            return hmemo[key]
        val = Fr(1, n)
        if r > 0:
            val += Fr(r, n) * h(a, b + 1, r - 1)
        coef = n - 1 - a - b - r
        if coef > 0:
            val += Fr(coef, n) * g(a, b + 1, r)
        hmemo[key] = val
        return val

    return Fr(K, n) * h(0, 0, K - 1) + (1 - Fr(K, n)) * g(0, 0, K)


def solve_exact(A, rhs):
    N = len(A)
    M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
    for col in range(N):
        piv = next(r for r in range(col, N) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(N):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][N] for i in range(N)]


PREDICT = {10: Fr(200965, 646646), 11: Fr(106135, 312018), 12: Fr(1779879, 4828850)}
allok = True
for K in (10, 11, 12):
    D = K + 1
    nfit = list(range(K + 3, K + 3 + D + 1))
    A = [[Fr(1, n) ** j for j in range(D + 1)] for n in nfit]
    rhs = [chain(n, K) for n in nfit]
    alpha = solve_exact(A, rhs)
    noos = list(range(nfit[-1] + 1, nfit[-1] + 7))
    oos = all(sum(alpha[j] * Fr(1, n) ** j for j in range(D + 1)) == chain(n, K)
              for n in noos)
    a0 = (alpha[0] == phi(K))
    a1 = (alpha[1] == PREDICT[K])
    # degree really K+1?  top coefficient must be nonzero
    topnz = (alpha[D] != 0)
    if not (oos and a0 and a1 and topnz):
        allok = False
    print("   K=%-3d  alpha_0==phi_K:%-6s  alpha_1==PREDICTED %-16s :%-6s  "
          "deg=K+1 (top coef != 0):%-6s  out-of-sample(6 new n):%s"
          % (K, a0, str(PREDICT[K]), a1, topnz, oos))
print("   ALL THREE OF MY PREDICTIONS CONFIRMED EXACTLY:", allok)

print()
print("=" * 100)
print("B5. four genuinely different formulas for c_K must agree exactly")
print("=" * 100)


def prod_form(K):
    p = Fr(1)
    for j in range(1, K + 1):
        p *= Fr(2 * j, 2 * j + 1)
    return (K + 2) * p / 4 - Fr(1, 2)


def binom_form(K):
    return Fr((K + 2) * 4 ** K, 4 * (2 * K + 1) * comb(2 * K, K)) - Fr(1, 2)


def telescope(K):
    return Fr(1, 4) * sum(Fr(j) * phi(j) / (2 * j + 3) for j in range(1, K))


def raw(K):
    return K * (phi(K) / 4 + F_closed(K - 1, Fr(1), 1) - phi(K))


bad = [K for K in range(1, 301)
       if not (raw(K) == prod_form(K) == binom_form(K) == telescope(K)
               == ((K + 2) * phi(K) - 2) / 4)]
print("   raw def == product form == central-binomial form == telescoping sum ==")
print("   Theorem A, for K=1..300:  disagreements:", bad or "NONE")

print()
print("VERDICT OF THIS SCRIPT:",
      "NO COUNTEREXAMPLE FOUND; every break attempt failed."
      if (not counter and not counter2 and not nonmono and ok and allok and not bad)
      else "SOMETHING BROKE -- see above")
