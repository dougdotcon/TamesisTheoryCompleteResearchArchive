"""
Referee check 01c -- Theorem 1's exact decomposition, pushed to much higher K
via exact Fraction numerics (concrete n), complementing check01's symbolic
sweep (K=0..25) which is sympy-simplify-bound. Also cross-validates a subset
directly against mychain.py's independent (a,b,r) recursion (ground truth,
not the closed forms).
"""
import sys
from fractions import Fraction as F
from math import comb

sys.path.insert(0, ".")
import closed_forms as cf
import mychain as mc

log = open("check01c_theorem1_highK.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


def T_over_A_RHS_value(K, n):
    """Theorem 1's boxed RHS, evaluated at concrete (K,n), exact Fraction."""
    CONST = F(2)**(2 * K - 1) - F(2 * K + 1, 2) * comb(2 * K, K)
    total = CONST
    for j in range(1, K + 1):
        gj_minus_1 = cf.g_of_i(j, n) - 1
        fj = n * gj_minus_1
        Bj = F((2 * K + 1) * (j + 1), K + j + 1) * comb(2 * K, K - j)
        total += comb(2 * K + 1, K - j) * fj + Bj * gj_minus_1
    return total


p("=" * 78)
p("Theorem 1: exact-Fraction identity check, T(n,K)/A vs boxed RHS,")
p("K=0..300, n=K+1..K+8 (2409 (K,n) pairs) -- target's own T2 test only")
p("checked the coefficient sub-identity to K=300, not this full identity")
p("beyond K=8 (symbolic) -- this checks the FULL decomposition, numerically")
p("exact, to K=300.")
p("=" * 78)

count = 0
mism = 0
A_zero_events = 0
for K in range(0, 301):
    A = cf.phi_K(K) / F(4)**K
    for n in range(K + 1, K + 9):
        lhs_T = cf.T_of_nK(K, n)
        rhs = T_over_A_RHS_value(K, n)
        lhs_over_A = lhs_T / A
        count += 1
        if lhs_over_A != rhs:
            mism += 1
            p(f"  MISMATCH K={K} n={n}: T/A={lhs_over_A} RHS={rhs}")
p(f"RESULT: {count} pairs checked, {mism} mismatches "
  f"(K=0..300, n=K+1..K+8).")

p("")
p("Cross-validating a subset directly against mychain.py's independent")
p("(a,b,r) recursion (not the closed forms), K=1..40, n=K+1..K+6:")
count2 = 0
mism2 = 0
for K in range(1, 41):
    for n in range(K + 1, K + 7):
        T_closed = cf.T_of_nK(K, n)
        phi_chain = mc.phi(n, K)
        T_chain = n * (phi_chain - cf.phi_K(K))
        count2 += 1
        if T_closed != T_chain:
            mism2 += 1
            p(f"  MISMATCH K={K} n={n}: closed-form T={T_closed} chain T={T_chain}")
p(f"RESULT: {count2} pairs, {mism2} mismatches (K=1..40, n=K+1..K+6, "
  f"240 pairs total).")

log.close()
print("\nWrote check01c_theorem1_highK.log")
