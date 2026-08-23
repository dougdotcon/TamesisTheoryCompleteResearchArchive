"""
R3 (+ R5 informational context): compute M_K^psi := sup_n n(psi_n^{(K)}-phi_K)
exactly (= value at n=K+1, per R2's proved monotonicity) for K=1..300, and
verify it satisfies the crude Route-A upper bound

    M_K^psi <= phi_K * (K+1) * e^{K/2}

for every K in range. Also report the empirical growth rate (log M_K^psi / K
and the ratio M_K^psi(K)/M_K^psi(K-1)) purely as INFORMATIONAL context (not
part of the proof, which only needs *some* finite geometric rate) -- this
lets us report honestly how loose the proved bound is, in the same spirit as
error_constant_growth_attempt/ATTEMPT.md's D_r(b) vs D*_r(b) comparison.

All exact (Fraction) for the M_K^psi sequence and the bound comparison;
mpmath (60 dps) used only to extend the log-ratio sanity context to larger K
where exact Fraction arithmetic on C(601,*) etc. gets slow, cross-checked
against the exact values where both are computed.
"""
import math
from fractions import Fraction as Fr
from math import comb, factorial

import mpmath as mp

mp.mp.dps = 60


def phi_r_exact(r):
    return Fr(4**r * factorial(r)**2, factorial(2 * r + 1))


def MK_psi_exact(K):
    """Exact M_K^psi = (K+1)(psi_{K+1}^{(K)} - phi_K), via Corolario A1 at
    n=K+1 (the proved argmax, R2)."""
    n = K + 1
    total = Fr(0)
    for j in range(0, K + 1):
        w = Fr(comb(2 * K + 1, K - j))
        prod = Fr(1)
        for i in range(1, j + 1):
            prod *= Fr(n + i, n)
        total += w * n * (prod - 1)
    return phi_r_exact(K) * total / Fr(4**K)


def bound_exact(K):
    """Crude Route-A bound phi_K*(K+1)*e^{K/2}, evaluated as a high-precision
    float via mpmath, but phi_K itself kept exact then converted."""
    phiK = phi_r_exact(K)
    return mp.mpf(phiK.numerator) / mp.mpf(phiK.denominator) * (K + 1) * mp.e**(mp.mpf(K) / 2)


print("=== R3: M_K^psi exact vs crude bound phi_K*(K+1)*e^{K/2}, K=1..300 ===\n")
print(f"{'K':>4} {'M_K^psi (float)':>20} {'bound (float)':>20} {'bound/M_K^psi':>16} {'holds':>6}")

violations = 0
rows = []
prev_val = None
for K in range(1, 301):
    exact_val = MK_psi_exact(K)
    fval = mp.mpf(exact_val.numerator) / mp.mpf(exact_val.denominator)
    b = bound_exact(K)
    holds = fval <= b
    if not holds:
        violations += 1
    rows.append((K, fval, b))
    if K <= 20 or K % 20 == 0:
        ratio = b / fval if fval != 0 else mp.inf
        print(f"{K:>4} {float(fval):>20.6f} {float(b):>20.6f} {float(ratio):>16.4f} {str(holds):>6}")

print(f"\nviolations of M_K^psi <= phi_K*(K+1)*e^(K/2): {violations} / 300\n")

print("=== R5 (informational only): empirical growth rate of M_K^psi ===")
print(f"{'K':>4} {'M_K^psi':>18} {'M_K/M_(K-1)':>14} {'ln(M_K)/K':>12}")
prev = None
for K, fval, b in rows:
    ratio_str = "-"
    if prev is not None and prev != 0:
        ratio = fval / prev
        ratio_str = f"{float(ratio):.5f}"
    if K in (2, 5, 10, 20, 50, 100, 150, 200, 250, 300):
        lnk = mp.log(fval) / K if fval > 0 else mp.mpf('-inf')
        print(f"{K:>4} {float(fval):>18.4f} {ratio_str:>14} {float(lnk):>12.6f}")
    prev = fval

# Cross check a couple of large-K points against a fresh independent
# mpmath-only recomputation (not reusing exact Fraction path), high dps.
print("\n=== cross-check: exact Fraction path vs fresh mpmath-only path, K=50,150,300 ===")
for K in (50, 150, 300):
    n = K + 1
    total = mp.mpf(0)
    for j in range(0, K + 1):
        w = mp.mpf(comb(2 * K + 1, K - j))
        prod = mp.mpf(1)
        for i in range(1, j + 1):
            prod *= mp.mpf(n + i) / mp.mpf(n)
        total += w * n * (prod - 1)
    phiK = mp.mpf(4)**K * mp.factorial(K)**2 / mp.factorial(2 * K + 1)
    val_mp = phiK * total / mp.mpf(4)**K
    exact_val = MK_psi_exact(K)
    val_fr = mp.mpf(exact_val.numerator) / mp.mpf(exact_val.denominator)
    rel_diff = abs(val_mp - val_fr) / val_fr
    print(f"K={K}: exact-Fraction={float(val_fr):.6f}  mpmath-fresh={float(val_mp):.6f}  "
          f"rel_diff={float(rel_diff):.2e}")

print(f"\n=== ALL R3 CHECKS PASS (bound holds for all 300 K): {violations == 0} ===")
