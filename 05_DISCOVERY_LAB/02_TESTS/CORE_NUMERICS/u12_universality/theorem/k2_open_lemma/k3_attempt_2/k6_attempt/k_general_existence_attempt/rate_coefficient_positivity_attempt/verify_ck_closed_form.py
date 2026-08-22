#!/usr/bin/env python3
"""
verify_ck_closed_form.py  --  wave 9, front (b), RATE-COEFFICIENT-POSITIVITY-ATTEMPT

Purpose
-------
Establish, by EXACT rational arithmetic only (fractions.Fraction), the chain

  (1)  F_r(t,b), re-derived from the DIAGONAL COEFFICIENT RECURSION of
       k6_attempt/ATTEMPT.md  §2.3  (an already-PROVED result, re-transcribed here,
       not re-derived mathematically), agrees with the closed form of that same
       section.  Two independent implementations, exact rationals.

  (2)  c_K := K [ phi_K/4 + F_{K-1}(1,1) - phi_K ]   (the target coefficient,
       DISC-DEC-040 / THEOREM.md Stage 6 item 4) reproduces the tabulated values
       of adversarial/REFEREE_REPORT.md A.7 for K = 1..12.

  (2b) THE HEADLINE COLLAPSE of this document -- everything reduces to the
       Wallis integral phi_K itself:

              F_{K-1}(1,1) = [ (2K+1) phi_K - 1 ] / (2K)
              c_K          = [ (K+2)  phi_K - 2 ] / 4

       so that   c_K > 0  <=>  v_K := (K+2) phi_K > 2,  with equality at K=1.
       And, with phi_{K+1}/phi_K = (2K+2)/(2K+3),

              v_{K+1}/v_K - 1  =  K / ( (K+2)(2K+3) )  >  0   for K >= 1,

       which, with v_1 = 2, IS the entire positivity proof.

  (3)  The equivalent central-binomial identity,

              F_{K-1}(1,1) = [ (K-1)! K! / (2K)! ] * ( 4^K - C(2K,K) ) / 2 .

  (4)  The equivalent central-binomial closed form,

              c_K = (K+2) 4^K / ( 4 (2K+1) C(2K,K) )  -  1/2 .

  (5)  The equivalent ratio identity with u_K := 2 c_K + 1 = v_K/2:

              u_{K+1} / u_K  =  2 (K+1)(K+3) / ( (K+2)(2K+3) )   >  1 ,  u_1 = 1.

  (6)  Direct exact positivity sweep of c_K over a large range of K.

Everything printed as "EXACT" below is a comparison of fractions.Fraction objects
(or of Python integers), never of floats.  Floats appear only in columns explicitly
labelled as decimal display.

Self-contained: no imports from sibling directories.
"""

from fractions import Fraction
from math import comb, factorial, pi, sqrt
import sys

FAIL = []


def check(name, cond, extra=""):
    tag = "OK  " if cond else "FAIL"
    if not cond:
        FAIL.append(name)
    print(f"  [{tag}] {name}{(' :: ' + extra) if extra else ''}")


# ----------------------------------------------------------------------------
# (0)  Already-PROVED closed forms, re-transcribed (NOT re-derived here)
# ----------------------------------------------------------------------------

def phi(K):
    """Wallis integral phi_K = 4^K (K!)^2 / (2K+1)!.  THEOREM.md Lemma 2 (PROVED)."""
    return Fraction(4 ** K * factorial(K) ** 2, factorial(2 * K + 1))


def F_closed(r, t, b):
    """F_r(t,b) = sum_{k=0}^{r} r!/(r-k)! * t^k / prod_{i=1}^{k+1} (r+b+i).

    k6_attempt/ATTEMPT.md  §2.3, 'Theorem (leading-order closed form; PROVED,
    general r)'.  Re-transcribed, exact rationals.  t is a Fraction.
    """
    tot = Fraction(0)
    for k in range(r + 1):
        prod = 1
        for i in range(1, k + 2):
            prod *= (r + b + i)
        tot += Fraction(factorial(r), factorial(r - k)) * (t ** k) / prod
    return tot


def F_from_recursion(rmax, btop):
    """Independent construction of the coefficients c_k^{(r)}(b) of F_r(t,b)
    STRAIGHT FROM the diagonal recursion of §2.3 -- i.e. NOT using the closed form:

        c_0^{(r)}(b) = 1/(1+r+b)
        c_k^{(r)}(b) = r/(k+1+r+b) * c_{k-1}^{(r-1)}(b+1)     (1 <= k <= r)

    Returns dict (r,b) -> list of Fractions [c_0,...,c_r], for r <= rmax and
    b <= btop - r (so that the (r-1, b+1) entry the recursion needs is present).
    """
    C = {}
    for r in range(rmax + 1):
        for b in range(btop - r + 1):
            coeffs = [Fraction(1, 1 + r + b)]
            for k in range(1, r + 1):
                prev = C[(r - 1, b + 1)][k - 1]   # exists: b+1 <= btop-(r-1)
                coeffs.append(Fraction(r, k + 1 + r + b) * prev)
            C[(r, b)] = coeffs
    return C


# ----------------------------------------------------------------------------
# (1)  recursion  vs  closed form
# ----------------------------------------------------------------------------
print("=" * 78)
print("(1)  F_r(t,b): diagonal recursion (2.3) vs closed form (2.3) -- exact")
print("=" * 78)

RMAX, BMAX, BTOP = 24, 8, 40
Crec = F_from_recursion(RMAX, BTOP)
n_ok = 0
ts = [Fraction(1), Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 4),
      Fraction(1, 5), Fraction(7, 11)]
for r in range(RMAX + 1):
    for b in range(0, BMAX + 1):
        rec = Crec[(r, b)]
        for t in ts:
            v_rec = sum(rec[k] * t ** k for k in range(r + 1))
            v_cf = F_closed(r, t, b)
            assert isinstance(v_rec, Fraction) and isinstance(v_cf, Fraction)
            if v_rec != v_cf:
                FAIL.append(f"F mismatch r={r} b={b} t={t}")
            else:
                n_ok += 1
check(f"F_r(t,b) recursion == closed form, r=0..{RMAX}, b=0..{BMAX}, "
      f"{len(ts)} values of t", not FAIL, f"{n_ok} exact agreements")

# Sanity: F_r(1,0) must equal the Wallis integral phi_r (k6 2.3's own check,
# there done for r<=6; extended here).
bad = [r for r in range(RMAX + 1) if F_closed(r, Fraction(1), 0) != phi(r)]
check(f"F_r(1,0) == phi_r for r=0..{RMAX}", not bad, f"mismatches: {bad}")


# ----------------------------------------------------------------------------
# (2)  c_K by DEFINITION, vs the referee report's A.7 table
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(2)  c_K := K[phi_K/4 + F_{K-1}(1,1) - phi_K]  vs  REFEREE_REPORT A.7")
print("=" * 78)

def c_def(K):
    """The target coefficient, exactly as defined in DISC-DEC-041 / Stage 6 item 4."""
    return K * (phi(K) / 4 + F_closed(K - 1, Fraction(1), 1) - phi(K))

A7 = {  # transcribed from adversarial/REFEREE_REPORT.md  A.7
    1: (Fraction(2, 3),        Fraction(1, 2),          Fraction(0)),
    2: (Fraction(8, 15),       Fraction(5, 12),         Fraction(1, 30)),
    3: (Fraction(16, 35),      Fraction(11, 30),        Fraction(1, 14)),
    4: (Fraction(128, 315),    Fraction(93, 280),       Fraction(23, 210)),
    5: (Fraction(256, 693),    Fraction(193, 630),      Fraction(29, 198)),
    6: (Fraction(1024, 3003),  Fraction(793, 2772),     Fraction(1093, 6006)),
    7: (Fraction(2048, 6435),  Fraction(1619, 6006),    Fraction(309, 1430)),
    8: (Fraction(32768, 109395), Fraction(26333, 102960), Fraction(10889, 43758)),
}
ok = True
print(f"  {'K':>3} {'phi_K':>22} {'F_{K-1}(1,1)':>22} {'c_K':>22}")
for K in sorted(A7):
    p, f, c = A7[K]
    got_p, got_f, got_c = phi(K), F_closed(K - 1, Fraction(1), 1), c_def(K)
    same = (p == got_p and f == got_f and c == got_c)
    ok &= same
    print(f"  {K:>3} {str(got_p):>22} {str(got_f):>22} {str(got_c):>22}"
          f"   {'match' if same else 'MISMATCH'}")
check("A.7 table (K=1..8) reproduced exactly, all three columns", ok)
check("c_1 == 0 exactly", c_def(1) == 0)


# ----------------------------------------------------------------------------
# (2b)  THE HEADLINE COLLAPSE:  everything is the Wallis integral phi_K itself
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(2b) HEADLINE:  F_{K-1}(1,1) = [(2K+1)phi_K - 1]/(2K)")
print("                c_K          = [(K+2)phi_K - 2]/4")
print("=" * 78)

def F_via_phi(K):
    return ((2 * K + 1) * phi(K) - 1) / (2 * K)

def c_via_phi(K):
    return ((K + 2) * phi(K) - 2) / 4

NHEAD = 300
bad = [K for K in range(1, 121) if F_closed(K - 1, Fraction(1), 1) != F_via_phi(K)]
check("F_{K-1}(1,1) == [(2K+1)phi_K - 1]/(2K) exactly, K=1..120", not bad,
      f"mismatches: {bad}")
bad = [K for K in range(1, 121) if c_def(K) != c_via_phi(K)]
check("c_K == [(K+2)phi_K - 2]/4 exactly, K=1..120", not bad, f"mismatches: {bad}")

# phi_K as the Wallis product, and the ratio that drives the whole proof
p = Fraction(1)
bad = []
for K in range(0, NHEAD + 1):
    if phi(K) != p:
        bad.append(K)
    p *= Fraction(2 * (K + 1), 2 * (K + 1) + 1)
check(f"phi_K == prod_{{j=1..K}} 2j/(2j+1) exactly, K=0..{NHEAD}", not bad,
      f"mismatches: {bad}")
bad = [K for K in range(0, NHEAD + 1)
       if phi(K + 1) / phi(K) != Fraction(2 * K + 2, 2 * K + 3)]
check(f"phi_{{K+1}}/phi_K == (2K+2)/(2K+3) exactly, K=0..{NHEAD}", not bad)

# v_K := (K+2) phi_K   -- the object the proof is about
def v(K):
    return (K + 2) * phi(K)

check("v_1 == 2 exactly (the equality case, c_1 = 0)", v(1) == 2)
bad = [K for K in range(1, NHEAD + 1)
       if v(K + 1) / v(K) - 1 != Fraction(K, (K + 2) * (2 * K + 3))]
check(f"v_{{K+1}}/v_K - 1 == K/((K+2)(2K+3)) > 0 exactly, K=1..{NHEAD}", not bad,
      f"mismatches: {bad}")
bad = [K for K in range(2, NHEAD + 1) if v(K) <= 2]
check(f"v_K > 2 exactly for every K = 2..{NHEAD}  (<=> c_K > 0)", not bad,
      f"violations: {bad[:10]}")

# THE MANIFESTLY-POSITIVE REPRESENTATION (telescoping the increment above):
#     c_K = (1/4) sum_{j=1}^{K-1} j phi_j / (2j+3)
# every term strictly positive; empty sum at K=1 gives c_1 = 0.
def c_as_sum(K):
    return sum(Fraction(j, 2 * j + 3) * phi(j) for j in range(1, K)) / 4

bad = [K for K in range(1, NHEAD + 1) if c_as_sum(K) != c_via_phi(K)]
check(f"c_K == (1/4) sum_{{j=1..K-1}} j*phi_j/(2j+3) exactly, K=1..{NHEAD}", not bad,
      f"mismatches: {bad}")
check("every summand j*phi_j/(2j+3) is strictly positive",
      all(Fraction(j, 2 * j + 3) * phi(j) > 0 for j in range(1, NHEAD + 1)))
print("       e.g.  c_4 = (1/4)[ 1*phi_1/5 + 2*phi_2/7 + 3*phi_3/9 ] = "
      f"{c_as_sum(4)}   (= {c_def(4)})")


# ----------------------------------------------------------------------------
# (3)  the equivalent central-binomial identity for F_{K-1}(1,1)
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(3)  equivalent form:  F_{K-1}(1,1) = [(K-1)!K!/(2K)!] * (4^K - C(2K,K))/2")
print("=" * 78)

def F_binom(K):
    return (Fraction(factorial(K - 1) * factorial(K), factorial(2 * K))
            * Fraction(4 ** K - comb(2 * K, K), 2))

bad = [K for K in range(1, 121) if F_closed(K - 1, Fraction(1), 1) != F_binom(K)]
check("identity holds exactly for K=1..120", not bad, f"mismatches: {bad}")

# also verify the tail-of-binomial-row step in isolation
bad2 = [K for K in range(1, 201)
        if sum(comb(2 * K, K + k + 1) for k in range(K)) * 2 != 4 ** K - comb(2 * K, K)]
check("sum_{j=K+1}^{2K} C(2K,j) == (4^K - C(2K,K))/2, K=1..200", not bad2)


# ----------------------------------------------------------------------------
# (4)  the new closed form for c_K
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(4)  NEW closed form:  c_K = (K+2)4^K / (4(2K+1)C(2K,K))  -  1/2")
print("=" * 78)

def c_cf(K):
    return Fraction((K + 2) * 4 ** K, 4 * (2 * K + 1) * comb(2 * K, K)) - Fraction(1, 2)

bad = [K for K in range(1, 121) if c_def(K) != c_cf(K)]
check("c_def(K) == c_cf(K) exactly for K=1..120", not bad, f"mismatches: {bad}")


# ----------------------------------------------------------------------------
# (5)  the ratio identity  --  this IS the positivity proof
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(5)  u_K := 2c_K + 1 = (K+2)4^K/(2(2K+1)C(2K,K));")
print("     claim  u_1 = 1  and  u_{K+1}/u_K = 2(K+1)(K+3)/((K+2)(2K+3)) > 1")
print("=" * 78)

def u(K):
    return Fraction((K + 2) * 4 ** K, 2 * (2 * K + 1) * comb(2 * K, K))

check("u_1 == 1 exactly", u(1) == 1)
bad = [K for K in range(1, 401)
       if u(K + 1) / u(K) != Fraction(2 * (K + 1) * (K + 3), (K + 2) * (2 * K + 3))]
check("ratio identity exact for K=1..400", not bad, f"mismatches: {bad}")
# the ratio minus 1, in lowest terms, must be K/(2K^2+7K+6)
bad = [K for K in range(1, 401)
       if Fraction(2 * (K + 1) * (K + 3), (K + 2) * (2 * K + 3)) - 1
       != Fraction(K, 2 * K * K + 7 * K + 6)]
check("ratio - 1 == K/(2K^2+7K+6) > 0 for K=1..400", not bad)
bad = [K for K in range(1, 401) if u(K) != 2 * c_def(K) + 1 if K <= 120]
check("u_K == 2c_K + 1 exactly for K=1..120", not bad)

# telescoped product form
def u_prod(K):
    p = Fraction(1)
    for j in range(1, K):
        p *= Fraction(2 * (j + 1) * (j + 3), (j + 2) * (2 * j + 3))
    return p
bad = [K for K in range(1, 301) if u_prod(K) != u(K)]
check("u_K == prod_{j=1}^{K-1} 2(j+1)(j+3)/((j+2)(2j+3)), K=1..300", not bad)


# ----------------------------------------------------------------------------
# (6)  exact positivity + strict monotonicity sweep
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(6)  exact sweep: c_K > 0 and c_{K+1} > c_K, K = 2 .. KMAX")
print("=" * 78)

KMAX = 5000
prev = c_via_phi(1)
neg, nonmono = [], []
for K in range(2, KMAX + 1):
    cK = c_via_phi(K)
    if cK != c_cf(K):
        FAIL.append(f"c_via_phi != c_cf at K={K}")
    if cK <= 0:
        neg.append(K)
    if cK <= prev:
        nonmono.append(K)
    prev = cK
check(f"c_K > 0 exactly for every K = 2..{KMAX}", not neg, f"violations: {neg[:10]}")
check(f"c_K strictly increasing for K = 1..{KMAX}", not nonmono,
      f"violations: {nonmono[:10]}")

print()
print("  decimal display of the trend (floats here are DISPLAY ONLY):")
print(f"  {'K':>6} {'c_K (exact, decimal)':>22} {'sqrt(pi K)/8 - 1/2':>22} {'ratio':>10}")
for K in [2, 3, 5, 10, 12, 13, 20, 50, 100, 500, 1000, 5000]:
    cK = c_via_phi(K)
    asym = sqrt(pi * K) / 8 - 0.5
    print(f"  {K:>6} {float(cK):>22.12f} {asym:>22.12f} {float(cK)/asym:>10.7f}")

print()
print("  exact values of c_K for K = 9..16 (extending A.7's table):")
for K in range(9, 17):
    print(f"    c_{K:<3} = {c_def(K)}   (= {float(c_def(K)):.10f})")

print()
if FAIL:
    print("RESULT:  ***FAILURES***:", FAIL)
    sys.exit(1)
print("RESULT:  every check above passed, exact rational arithmetic throughout.")
