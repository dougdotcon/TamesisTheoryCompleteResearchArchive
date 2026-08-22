"""
adv_downstream_consequences.py -- what the Target Theorem actually licenses
downstream, checked independently.

If the Target Theorem is correct, then combining it with Reduction Lemma A
    phi_n^(K) = (K/n) psi_n^(K,R) + (1-K/n) psi_n^(K),
    psi_n^(K) = g_K(n,0),  psi_n^(K,R) = h_{K-1}(0,0)
gives, for EVERY K, the exact 1/n coefficient of phi_n^(K):

    phi_n^(K) - phi_K = [ K*phi_K/4 + K*(Hhat_{K-1}(0,0) - phi_K) ] / n + O(1/n^2)
                      = K*[ phi_K/4 + F_{K-1}(1,1) - phi_K ] / n + O(1/n^2)

(using Hhat_{K-1}(0,0) = (1-0) F_{K-1}(1,1)).

This is a NEW, sharper statement than k6_attempt/ATTEMPT.md section 5's
"phi_n^(K)-phi_K = Theta(1/n) for every K>=1".  Here I compute the coefficient
for K=1..12 and check it against the exact closed forms wherever available.
"""

from fractions import Fraction as Fr
import math
from adv_core import Chain
from adv_numerics import F_fr

print("=" * 88)
print("The predicted 1/n coefficient of phi_n^(K) - phi_K, from the Target Theorem")
print("=" * 88)


def phi(K):
    return Fr(4**K * math.factorial(K)**2, math.factorial(2 * K + 1))


print(f"  {'K':>3} {'phi_K':>16} {'F_(K-1)(1,1)':>16} {'predicted 1/n coeff':>24}")
coeffs = {}
for K in range(1, 13):
    pk = phi(K)
    fk = F_fr(K - 1, 1, Fr(1))
    co = K * (pk / 4 + fk - pk)
    coeffs[K] = co
    print(f"  {K:>3} {str(pk):>16} {str(fk):>16} {str(co):>24}   ({float(co):+.8f})")
print()
print("  NOTE  K=1 gives EXACTLY 0 -- so phi_n^(1) - phi_1 is NOT Theta(1/n).")
print("        (wave 5 already recorded this: the two Theta(1/n) parts cancel.)")
print("        Every K>=2 checked gives a strictly positive coefficient.")
print()

print("=" * 88)
print("CROSS-CHECK against exact finite-n values computed by my own chain")
print("=" * 88)
for K in [1, 2, 3, 6]:
    print(f"  K={K}: n * (phi_n^(K) - phi_K) for growing n  [predict -> {float(coeffs[K]):+.8f}]")
    for n in [K + 2, 10, 20, 40, 80, 160]:
        if n <= K + 1:
            continue
        ch = Chain(n)
        psi = ch.g(0, 0, K)
        psiR = ch.h(0, 0, K - 1)
        phin = Fr(K, n) * psiR + (1 - Fr(K, n)) * psi
        val = n * (phin - phi(K))
        print(f"     n={n:>4}: {str(val):>34} = {float(val):+.10f}")
    print()

print("=" * 88)
print("K=1 in closed form, from my own chain (exact)")
print("=" * 88)
for n in [3, 5, 10, 20, 40]:
    ch = Chain(n)
    psi = ch.g(0, 0, 1)
    psiR = ch.h(0, 0, 0)
    phin = Fr(1, n) * psiR + (1 - Fr(1, n)) * psi
    print(f"  n={n:>3}: phi_n^(1) = {phin}, phi_n^(1)-2/3 = {phin - Fr(2,3)}, "
          f"n^2*(phi_n^(1)-2/3) = {n*n*(phin - Fr(2,3))}")
print("  --> phi_n^(1) - phi_1 = 1/(3 n^2) exactly: Theta(1/n^2), NOT Theta(1/n).")
