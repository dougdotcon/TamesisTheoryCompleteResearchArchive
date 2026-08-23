"""T3, T4 of DERIVATION_PREREG.md.

T3: closed-form phi_n^{(K)} (Corolario A1's psi_n^{(K)} + derived
psi_n^{(K),R} via Theorem B + Reduction Lemma A) vs. chain.py's INDEPENDENT
from-scratch (j,R) recursion, exact Fraction, K=0..9, n=K+1..K+30. Also
checks T(n,K):=n(phi_n^{(K)}-phi_K) is nonincreasing in n on this grid and
that T(K+1,K) = max_n T(n,K) (direct evidence for Claim 2).

T4: exact value of M_K := T(K+1,K) (computed via chain.py's recursion, NOT
the closed form, for independence) vs. Q(K+1)-(K+1)phi_K, exact Fraction,
K=0..40, with an independently-coded exact Q(n).
"""
import sys
sys.path.insert(0, "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/uniform_in_c_attempt")
from fractions import Fraction as Fr
from math import comb, factorial
from chain import phi_condK_exact, phi_K as phi_K_exact


def g(i, n):
    prod = Fr(1)
    for l in range(1, i + 1):
        prod *= Fr(n + l, n)
    return prod


def psi_n_K(n, K):
    A = Fr(factorial(K) ** 2, factorial(2 * K + 1))
    s = Fr(0)
    for j in range(0, K + 1):
        s += comb(2 * K + 1, K - j) * g(j, n)
    return A * s


def psi_n_K_R(n, K):
    if K == 0:
        return None
    kappa = Fr(factorial(K - 1) * factorial(K), factorial(2 * K))
    s = Fr(0)
    for i in range(1, K + 1):
        s += comb(2 * K, K - i) * g(i, n)
    return kappa * s


def phi_n_K_closed(n, K):
    if K == 0:
        return Fr(1)
    psR = psi_n_K_R(n, K)
    ps = psi_n_K(n, K)
    return Fr(K, n) * psR + (1 - Fr(K, n)) * ps


def Q_exact(n):
    s = Fr(0)
    prod = Fr(1)
    for j in range(0, n):
        s += prod
        prod *= Fr(n - j - 1, n)
    return s


print("=== T3: closed form vs chain.py, exact, K=0..9, n=K+1..K+30 ===")
bad3 = 0
tot3 = 0
maxviol = 0
nonmono = 0
for K in range(0, 10):
    Ts = []
    for n in range(K + 1, K + 31):
        want = phi_condK_exact(n, K)
        got = phi_n_K_closed(n, K)
        tot3 += 1
        if want != got:
            bad3 += 1
            print(f"  CLOSED-FORM MISMATCH K={K} n={n}")
        Ts.append((n, n * (want - phi_K_exact(K))))
    # monotonicity + argmax check on this grid
    vals = [t for (_, t) in Ts]
    if any(v < 0 for v in vals):
        maxviol += 1
        print(f"  NEGATIVE T(n,K) at K={K}")
    for i in range(len(vals) - 1):
        if vals[i + 1] > vals[i]:
            nonmono += 1
            print(f"  NON-MONOTONE K={K} at n={Ts[i][0]}->{Ts[i+1][0]}: {float(vals[i])} -> {float(vals[i+1])}")
    if vals[0] != max(vals):
        print(f"  ARGMAX NOT AT n=K+1 for K={K}")
print(f"T3 closed-form match: {tot3 - bad3}/{tot3}")
print(f"T3 monotonicity violations: {nonmono}, negativity violations: {maxviol}")
print("T3 RESULT:", "PASS" if (bad3 == 0 and nonmono == 0 and maxviol == 0) else "FAIL")

print()
print("=== T4: M_K = Q(K+1)-(K+1)phi_K, exact, K=0..40 (via chain.py, independent of closed form) ===")
bad4 = 0
for K in range(0, 41):
    n = K + 1
    Mk = n * (phi_condK_exact(n, K) - phi_K_exact(K))
    rhs = Q_exact(K + 1) - (K + 1) * phi_K_exact(K)
    ok = (Mk == rhs)
    if not ok:
        bad4 += 1
        print(f"  MISMATCH K={K}: M_K={Mk}  Q(K+1)-(K+1)phi_K={rhs}")
print(f"T4 RESULT: {41 - bad4}/41 exact matches;", "PASS" if bad4 == 0 else f"FAIL ({bad4})")
