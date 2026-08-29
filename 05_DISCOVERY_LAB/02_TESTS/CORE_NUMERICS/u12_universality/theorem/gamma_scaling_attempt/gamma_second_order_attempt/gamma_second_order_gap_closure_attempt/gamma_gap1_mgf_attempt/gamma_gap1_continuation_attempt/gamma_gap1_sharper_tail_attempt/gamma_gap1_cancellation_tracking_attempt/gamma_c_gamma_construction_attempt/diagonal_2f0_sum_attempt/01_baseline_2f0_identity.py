"""
Script 01 -- fresh, independent re-derivation and verification of the
predecessor's exact 2F0 fact for A_k(n,gamma), written from scratch
(no code imported from any ancestor/predecessor -- only the *statement*
is cited, per mandate).

Claim under test (cited from
  .../gamma_c_gamma_construction_attempt/ATTEMPT.md Sec.2, itself citing
  Lemma 1 of .../gamma_scaling_attempt/ATTEMPT.md Sec.1):

    A_k(n,gamma) = sum_{m=0}^{k} C(k,m) gamma^m (1-gamma)^{k-m} P_{k,m}
    P_{k,m} := prod_{i=1}^{m} (1 - (k-i)/n) = (n-k+1)_m / n^m   (rising
               Pochhammer ratio)

    A_k(n,gamma) = (1-gamma)^k * 2F0(-k, n-k+1 ; ; w),  w := -gamma/((1-gamma) n)

This script re-derives the Pochhammer rewriting and the 2F0 identity
independently, from the raw sum-over-m definition, with fresh sympy
code.
"""
import sympy as sp

n, k, gam, m = sp.symbols('n k gamma m', positive=True)

def P_direct(n_, k_, m_):
    """P_{k,m} as a literal product, straight from Lemma 1's definition."""
    prod = sp.Integer(1)
    for i in range(1, m_ + 1):
        prod *= (1 - (k_ - i) / n_)
    return sp.simplify(prod)

def A_k_direct(n_, k_, gamma_):
    """A_k via the raw sum-over-m definition (Lemma 1), symbolic n, gamma."""
    total = sp.Integer(0)
    for m_ in range(0, k_ + 1):
        total += sp.binomial(k_, m_) * gamma_**m_ * (1 - gamma_)**(k_ - m_) * P_direct(n_, k_, m_)
    return sp.expand(total)

def twoF0_poly(a_, b_, w_, kmax):
    """2F0(a,b;;w) truncated sum, terminates exactly at m=kmax when a=-kmax."""
    total = sp.Integer(0)
    poch_a = sp.Integer(1)
    poch_b = sp.Integer(1)
    fact = sp.Integer(1)
    for mm in range(0, kmax + 1):
        if mm == 0:
            term = sp.Integer(1)
        else:
            poch_a *= (a_ + mm - 1)
            poch_b *= (b_ + mm - 1)
            fact *= mm
            term = poch_a * poch_b / fact
        total += term * w_**mm
    return total

def A_k_via_2F0(n_, k_, gamma_):
    w_ = -gamma_ / ((1 - gamma_) * n_)
    return sp.expand((1 - gamma_)**k_ * twoF0_poly(-k_, n_ - k_ + 1, w_, k_))

print("=== Part A: Pochhammer rewriting of P_{k,m}, symbolic n ===")
mismatches_A = 0
for kk in range(0, 8):
    for mm in range(0, kk + 1):
        direct = P_direct(n, kk, mm)
        poch = sp.Rational(1) * sp.rf(n - kk + 1, mm) / n**mm  # rising factorial (n-k+1)_m / n^m
        poch = sp.simplify(poch)
        diff = sp.simplify(direct - poch)
        if diff != 0:
            mismatches_A += 1
            print(f"  MISMATCH k={kk} m={mm}: direct={direct}  poch={poch}  diff={diff}")
print(f"Part A mismatches: {mismatches_A} / checked all (k,m), k=0..7")

print()
print("=== Part B: A_k = (1-gamma)^k * 2F0(-k, n-k+1;;w), symbolic n, gamma ===")
mismatches_B = 0
for kk in range(0, 8):
    direct = A_k_direct(n, kk, gam)
    via2f0 = A_k_via_2F0(n, kk, gam)
    diff = sp.simplify(direct - via2f0)
    status = "OK" if diff == 0 else "MISMATCH"
    if diff != 0:
        mismatches_B += 1
    print(f"  k={kk}: {status}  (diff simplifies to {diff})")
print(f"Part B mismatches: {mismatches_B} / 8")

print()
print("=== Part C: numeric exact-Fraction spot check, fresh random points ===")
import random
random.seed(20260943001)  # reserved block, disclosed
from fractions import Fraction

def P_direct_num(n_, k_, m_):
    prod = Fraction(1)
    for i in range(1, m_ + 1):
        prod *= Fraction(n_ - (k_ - i), n_)
    return prod

def A_k_direct_num(n_, k_, gamma_num, gamma_den):
    # gamma represented exactly as Fraction(gamma_num, gamma_den)
    g = Fraction(gamma_num, gamma_den)
    total = Fraction(0)
    for m_ in range(0, k_ + 1):
        from math import comb
        total += comb(k_, m_) * g**m_ * (1 - g)**(k_ - m_) * P_direct_num(n_, k_, m_)
    return total

def A_k_via_2F0_num(n_, k_, gamma_num, gamma_den):
    g = Fraction(gamma_num, gamma_den)
    n_frac = Fraction(n_)
    w = Fraction(-1) * g / ((1 - g) * n_frac)
    # 2F0(-k, n-k+1;;w) terminating sum, exact Fraction arithmetic throughout
    total = Fraction(0)
    poch_a = Fraction(1)
    poch_b = Fraction(1)
    fact = 1
    b0 = n_frac - k_ + 1
    for mm in range(0, k_ + 1):
        if mm == 0:
            term = Fraction(1)
        else:
            poch_a *= (Fraction(-k_) + mm - 1)
            poch_b *= (b0 + mm - 1)
            fact *= mm
            term = poch_a * poch_b / fact
        total += term * w**mm
    return (1 - g)**k_ * total

mismatches_C = 0
n_checked = 0
for _ in range(60):
    n_val = random.randint(3, 400)
    k_val = random.randint(0, n_val)
    gd = random.choice([2, 3, 5, 7, 11])
    gn = random.randint(1, gd - 1)
    direct = A_k_direct_num(n_val, k_val, gn, gd)
    via = A_k_via_2F0_num(n_val, k_val, gn, gd)
    n_checked += 1
    if direct != via:
        mismatches_C += 1
        print(f"  MISMATCH n={n_val} k={k_val} gamma={gn}/{gd}: direct={direct} via={via}")
print(f"Part C: {mismatches_C} mismatches / {n_checked} exact-Fraction spot checks "
      f"(seed 20260943001, reserved block)")

print()
print("=== SUMMARY ===")
print(f"Part A (Pochhammer rewriting): {mismatches_A} mismatches (expect 0)")
print(f"Part B (2F0 identity, symbolic k=0..7): {mismatches_B} mismatches (expect 0)")
print(f"Part C (2F0 identity, 60 exact numeric spot checks): {mismatches_C} mismatches (expect 0)")
