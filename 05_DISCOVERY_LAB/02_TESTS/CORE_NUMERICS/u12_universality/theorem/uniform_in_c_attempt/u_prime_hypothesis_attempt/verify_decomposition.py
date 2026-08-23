"""T1, T2 of DERIVATION_PREREG.md.

T1: symbolic identity check (sympy) that
    T(n,K)/A = CONST(K) + sum_{j=1}^K [ C(2K+1,K-j) f_j(n) + B_j(K)(g(j;n)-1) ]
holds as an EXACT rational-function identity in n, for K=0..8, where
    A         = phi_K/4^K = (K!)^2/(2K+1)!
    g(j;n)    = prod_{i=1}^j (1+i/n) = (n+j)!/(n! n^j)
    f_j(n)    = n(g(j;n)-1)
    CONST(K)  = 2^(2K-1) - (2K+1)/2 * C(2K,K)
    B_j(K)    = (2K+1)(j+1)/(K+j+1) * C(2K,K-j)
and T(n,K) := n(phi_n^{(K)} - phi_K), with phi_n^{(K)} assembled via
Corolario A1 (psi_n^{(K)}) + the derived psi_n^{(K),R} (from Theorem B of
all_orders_closed_form_attempt/ATTEMPT.md) + Reduction Lemma A.

T2: the coefficient sub-identity
    (K+1) C(2K,K-j) - K C(2K,K-j-1) == C(2K,K-j) * (2K+1)(j+1)/(K+j+1)
in EXACT integer/Fraction arithmetic, K=0..300, all valid j.
"""
import sympy as sp
from fractions import Fraction as Fr
from math import comb

n, K = sp.symbols('n K', positive=True)


def check_T1(Kval):
    A = sp.Rational(sp.factorial(Kval) ** 2, sp.factorial(2 * Kval + 1))

    def g(j):
        p = sp.Integer(1)
        for l in range(1, j + 1):
            p *= (n + l) / n
        return sp.together(p)

    def C(a, b):
        return sp.binomial(a, b)

    psi = A * sum(C(2 * Kval + 1, Kval - j) * g(j) for j in range(0, Kval + 1))
    if Kval == 0:
        phinK = sp.Integer(1)
    else:
        kappa = sp.Rational(sp.factorial(Kval - 1) * sp.factorial(Kval), sp.factorial(2 * Kval))
        psiR = kappa * sum(C(2 * Kval, Kval - i) * g(i) for i in range(1, Kval + 1))
        phinK = sp.Rational(Kval, 1) / n * psiR + (1 - sp.Rational(Kval, 1) / n) * psi
    phiK = A * 2 ** (2 * Kval)
    T = n * (phinK - phiK)
    lhs = sp.simplify(T / A)

    CONST = sp.Rational(2) ** (2 * Kval - 1) - (2 * Kval + 1) * C(2 * Kval, Kval) / 2
    rhs = sp.Integer(CONST)
    for j in range(1, Kval + 1):
        fj = n * (g(j) - 1)
        Bj = sp.Rational((2 * Kval + 1) * (j + 1), Kval + j + 1) * C(2 * Kval, Kval - j)
        rhs += C(2 * Kval + 1, Kval - j) * fj + Bj * (g(j) - 1)
    rhs = sp.simplify(rhs)

    return sp.simplify(lhs - rhs)


print("=== T1: symbolic decomposition identity, K=0..8 ===")
bad1 = 0
for Kval in range(0, 9):
    d = check_T1(Kval)
    ok = (d == 0)
    if not ok:
        bad1 += 1
    print(f"  K={Kval}: LHS-RHS = {d}   {'OK' if ok else 'FAIL'}")
print("T1 RESULT:", "PASS (0 failures)" if bad1 == 0 else f"FAIL ({bad1} failures)")

print()
print("=== T2: coefficient sub-identity, exact, K=0..300, all j ===")
bad2 = 0
tot2 = 0
for Kval in range(0, 301):
    for j in range(0, Kval + 1):
        lhs = (Kval + 1) * comb(2 * Kval, Kval - j) - Kval * (comb(2 * Kval, Kval - j - 1) if Kval - j - 1 >= 0 else 0)
        rhs = Fr(comb(2 * Kval, Kval - j) * (2 * Kval + 1) * (j + 1), Kval + j + 1)
        tot2 += 1
        if Fr(lhs) != rhs:
            bad2 += 1
            if bad2 <= 5:
                print(f"  MISMATCH K={Kval} j={j}: lhs={lhs} rhs={rhs}")
print(f"T2 RESULT: {tot2 - bad2}/{tot2} exact matches;", "PASS" if bad2 == 0 else f"FAIL ({bad2} mismatches)")
