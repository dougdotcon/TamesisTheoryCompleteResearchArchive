"""
Script 02 -- re-examination of the predecessor's Charlier-polynomial
"non-identification" claim (ATTEMPT.md Sec.2 / Sec.8 item 2: "the k=1
residual is an exact, n-independent -2*gamma, ruling out an accidental
near-miss").

We do NOT read or import the predecessor's script (per mandate); we
implement the *standard* Charlier polynomial from its textbook
definition (DLMF 18.20.1 / Koekoek-Swarttouw "Askey scheme"), fresh,
from scratch, and test the natural parameter match by hand-substitution
algebra, independently checked here by sympy.

Standard definition (DLMF 18.20.1):
    C_n(x;a) := 2F0(-n, -x ; ; -1/a)
              = sum_{j=0}^n C(n,j) * (-x)_j * (-1/a)^j / j!        [rising
                Pochhammer (-x)_j = (-x)(-x+1)...(-x+j-1)]

Our exact fact (script 01, PROVED): A_k(n,gamma) = (1-gamma)^k *
2F0(-k, n-k+1;;w), w = -gamma/((1-gamma) n).

Natural parameter match: identify -x = n-k+1 (so x = k-n-1) and
-1/a = w (so a = -1/w = (1-gamma) n / gamma). Since 2F0(A,B;;z) is
manifestly symmetric in (A,B) and this is a *pure substitution* into
the same series, A_k(n,gamma) = (1-gamma)^k * C_k(k-n-1 ; (1-gamma) n
/ gamma) should hold as an algebraic IDENTITY, not something that can
"fail" -- unless a sign or normalization convention is inconsistent.

We test this directly, and ALSO test the single most natural variant
bug (using +1/a instead of the DLMF -1/a inside the 2F0, i.e. a
Charlier "sign convention" mismatch) to see whether it reproduces the
predecessor's reported "-2*gamma at k=1" residual exactly -- which
would identify the predecessor's error precisely, not just assert it.
"""
import sympy as sp

n, k, gam = sp.symbols('n k gamma')
a_sym = sp.symbols('a')

def A_k_direct(n_, k_, gamma_):
    total = sp.Integer(0)
    for m_ in range(0, k_ + 1):
        prod = sp.Integer(1)
        for i in range(1, m_ + 1):
            prod *= (1 - (k_ - i) / n_)
        total += sp.binomial(k_, m_) * gamma_**m_ * (1 - gamma_)**(k_ - m_) * prod
    return sp.expand(total)

def charlier_DLMF(n_, x_, a_):
    """C_n(x;a) = 2F0(-n,-x;;-1/a), standard DLMF 18.20.1 sign convention."""
    total = sp.Integer(0)
    poch_a = sp.Integer(1)  # (-n)_j
    poch_x = sp.Integer(1)  # (-x)_j
    fact = sp.Integer(1)
    z = -1 / a_
    for j in range(0, n_ + 1):
        if j == 0:
            term = sp.Integer(1)
        else:
            poch_a *= (-n_ + j - 1)
            poch_x *= (-x_ + j - 1)
            fact *= j
            term = poch_a * poch_x / fact
        total += term * z**j
    return sp.expand(total)

def charlier_WRONGSIGN(n_, x_, a_):
    """Deliberately mis-signed variant: 2F0(-n,-x;;+1/a) instead of -1/a."""
    total = sp.Integer(0)
    poch_a = sp.Integer(1)
    poch_x = sp.Integer(1)
    fact = sp.Integer(1)
    z = 1 / a_
    for j in range(0, n_ + 1):
        if j == 0:
            term = sp.Integer(1)
        else:
            poch_a *= (-n_ + j - 1)
            poch_x *= (-x_ + j - 1)
            fact *= j
            term = poch_a * poch_x / fact
        total += term * z**j
    return sp.expand(total)

print("=== Part A: correct DLMF-convention Charlier identification, symbolic n,gamma, k=0..6 ===")
mismatches = 0
for kk in range(0, 7):
    direct = A_k_direct(n, kk, gam)
    x_k = kk - n - 1
    a_k = (1 - gam) * n / gam
    via_charlier = sp.expand((1 - gam)**kk * charlier_DLMF(kk, x_k, a_k))
    diff = sp.simplify(direct - via_charlier)
    status = "OK (exact match)" if diff == 0 else "MISMATCH"
    if diff != 0:
        mismatches += 1
    print(f"  k={kk}: {status}  diff={sp.nsimplify(diff) if diff != 0 else 0}")
print(f"Part A mismatches: {mismatches} / 7  "
      f"(0 expected: the DLMF-convention identification is an exact identity)")

print()
print("=== Part B: diagnosing the predecessor's claimed '-2*gamma at k=1' residual ===")
# predecessor's own naive match, per their ATTEMPT.md Sec.2: x = k-n-1, a=(1-gamma)n/gamma
x1 = 1 - n - 1  # k=1
a1 = (1 - gam) * n / gam
direct_A1 = A_k_direct(n, 1, gam)
correct_C1 = sp.expand((1 - gam)**1 * charlier_DLMF(1, x1, a1))
wrongsign_C1 = sp.expand((1 - gam)**1 * charlier_WRONGSIGN(1, x1, a1))
print(f"  A_1 (direct, ground truth)           = {sp.simplify(direct_A1)}")
print(f"  (1-gamma)*C_1(x;a) [DLMF -1/a sign]   = {sp.simplify(correct_C1)}   "
      f"(residual vs A_1: {sp.simplify(correct_C1 - direct_A1)})")
print(f"  (1-gamma)*C_1(x;a) [WRONG +1/a sign]  = {sp.simplify(wrongsign_C1)}   "
      f"(residual vs A_1: {sp.simplify(wrongsign_C1 - direct_A1)})")

print()
print("=== Part C: same diagnosis at k=2 (to rule out a k=1 coincidence) ===")
x2 = 2 - n - 1
a2 = (1 - gam) * n / gam
direct_A2 = A_k_direct(n, 2, gam)
correct_C2 = sp.expand((1 - gam)**2 * charlier_DLMF(2, x2, a2))
wrongsign_C2 = sp.expand((1 - gam)**2 * charlier_WRONGSIGN(2, x2, a2))
print(f"  A_2 (direct, ground truth)            = {sp.simplify(direct_A2)}")
print(f"  (1-gamma)^2*C_2(x;a) [DLMF sign]       = {sp.simplify(correct_C2)}   "
      f"(residual: {sp.simplify(correct_C2 - direct_A2)})")
print(f"  (1-gamma)^2*C_2(x;a) [WRONG sign]      = {sp.simplify(wrongsign_C2)}   "
      f"(residual: {sp.simplify(wrongsign_C2 - direct_A2)})")

print()
print("=== Part D: numeric exact-Fraction cross-check of the DLMF identification, fresh points ===")
import random
from fractions import Fraction
from math import comb
random.seed(20260943002)  # reserved block, disclosed

def A_k_direct_num(n_, k_, g):
    total = Fraction(0)
    for m_ in range(0, k_ + 1):
        prod = Fraction(1)
        for i in range(1, m_ + 1):
            prod *= Fraction(n_ - (k_ - i), n_)
        total += comb(k_, m_) * g**m_ * (1 - g)**(k_ - m_) * prod
    return total

def charlier_DLMF_num(n_, x_, a_):
    total = Fraction(0)
    poch_n = Fraction(1)
    poch_x = Fraction(1)
    fact = 1
    z = Fraction(-1) / a_
    for j in range(0, n_ + 1):
        if j == 0:
            term = Fraction(1)
        else:
            poch_n *= (Fraction(-n_) + j - 1)
            poch_x *= (-x_ + j - 1)
            fact *= j
            term = poch_n * poch_x / fact
        total += term * z**j
    return total

mismatches_D = 0
for _ in range(50):
    n_val = random.randint(2, 300)
    k_val = random.randint(0, min(n_val, 40))
    gd = random.choice([2, 3, 5, 7, 11, 13])
    gn = random.randint(1, gd - 1)
    g = Fraction(gn, gd)
    direct = A_k_direct_num(n_val, k_val, g)
    x_k = Fraction(k_val - n_val - 1)
    a_k = (1 - g) * n_val / g
    via = (1 - g)**k_val * charlier_DLMF_num(k_val, x_k, a_k)
    if direct != via:
        mismatches_D += 1
        print(f"  MISMATCH n={n_val} k={k_val} gamma={g}: direct={direct} via={via}")
print(f"Part D: {mismatches_D} mismatches / 50 exact spot checks (seed 20260943002)")

print()
print("=== SUMMARY ===")
print("The DLMF-convention Charlier identification A_k = (1-gamma)^k C_k(k-n-1; "
      "(1-gamma)n/gamma) is CONFIRMED as an EXACT algebraic identity (0 mismatches, "
      "symbolic k=0..6 + 50 numeric spot checks).")
print("The predecessor's reported '-2*gamma at k=1 residual, ruling out Charlier' "
      "is REPRODUCED EXACTLY by using the WRONG sign convention (+1/a instead of "
      "DLMF's -1/a) inside the 2F0 -- see Part B/C above -- strongly suggesting a "
      "sign-convention bug in the predecessor's own Charlier implementation, not a "
      "genuine mathematical non-identification.")
