"""
Independent, from-scratch referee verification for DIAGONAL-2F0-SUM-ATTEMPT.
Nothing here imports or copies the target's or predecessor's .py files;
every function is written fresh from the mathematical prose of ATTEMPT.md
(target) and the predecessor's ATTEMPT.md, cross-checked against the
target's own reported numbers as an independent confirmation.
"""
import sympy as sp
from sympy import symbols, Rational, binomial, simplify, expand
from fractions import Fraction
from math import comb
import random

n, k, gam = symbols('n k gamma')

def A_k_direct(n_, k_, g_):
    total = sp.Integer(0)
    for m_ in range(0, k_ + 1):
        prod = sp.Integer(1)
        for i in range(1, m_ + 1):
            prod *= (1 - (k_ - i) / n_)
        total += binomial(k_, m_) * g_**m_ * (1 - g_)**(k_ - m_) * prod
    return sp.expand(total)

# ---------------------------------------------------------------------
print("="*78)
print("CHECK 1: A_k = (1-g)^k * 2F0(-k,n-k+1;;w), w=-g/((1-g)n), k=0..8, symbolic")
print("="*78)
def twoF0(a_, b_, z_, kmax):
    total = sp.Integer(0)
    poch_a = sp.Integer(1); poch_b = sp.Integer(1); fact = sp.Integer(1)
    for m_ in range(0, kmax+1):
        if m_ > 0:
            poch_a *= (a_ + m_ - 1)
            poch_b *= (b_ + m_ - 1)
            fact *= m_
        total += (poch_a*poch_b/fact) * z_**m_
    return total

mism = 0
for kk in range(0, 9):
    w = -gam/((1-gam)*n)
    hyp = sp.expand((1-gam)**kk * twoF0(-kk, n-kk+1, w, kk))
    direct = A_k_direct(n, kk, gam)
    d = sp.simplify(direct - hyp)
    print(f"  k={kk}: diff={d}")
    if d != 0: mism += 1
print(f"Mismatches: {mism}/9 (expect 0)\n")

# ---------------------------------------------------------------------
print("="*78)
print("CHECK 2: DLMF Charlier identity, A_k=(1-g)^k C_k(k-n-1;(1-g)n/g), k=0..8, symbolic")
print("(fresh implementation, independent of both predecessor's and target's code)")
print("="*78)
def charlier_DLMF(kk, x_, a_):
    """C_k(x;a) := 2F0(-k,-x;;-1/a), DLMF 18.20.1."""
    return twoF0(-kk, -x_, -1/a_, kk)

def charlier_WRONG(kk, x_, a_):
    """the natural sign slip: 2F0(-k,-x;;+1/a)."""
    return twoF0(-kk, -x_, 1/a_, kk)

mism2 = 0
for kk in range(0, 9):
    x_ = kk - n - 1
    a_ = (1-gam)*n/gam
    via = sp.expand((1-gam)**kk * charlier_DLMF(kk, x_, a_))
    direct = A_k_direct(n, kk, gam)
    d = sp.simplify(direct - via)
    print(f"  k={kk}: DLMF-sign diff={d}")
    if d != 0: mism2 += 1
print(f"Mismatches: {mism2}/9 (expect 0)\n")

print("Wrong-sign residuals at k=1..4 (checking against predecessor's -2g claim, k=1):")
for kk in range(1, 5):
    x_ = kk - n - 1
    a_ = (1-gam)*n/gam
    wrong = sp.expand((1-gam)**kk * charlier_WRONG(kk, x_, a_))
    direct = A_k_direct(n, kk, gam)
    resid = sp.simplify(wrong - direct)
    print(f"  k={kk}: wrong-sign residual = {sp.factor(resid)}")

# ---------------------------------------------------------------------
print()
print("="*78)
print("CHECK 3: hand cross-check that dropping poch_negk in the predecessor's own")
print("Charlier_symbolic (using binomial(k,m) instead of (-k)_m/m!) is ALGEBRAICALLY")
print("IDENTICAL to using +1/a instead of -1/a. I.e. reconstruct predecessor's")
print("literal (buggy) function from their own script 01 and compare to WRONG-sign.")
print("="*78)
def predecessor_charlier_aswritten(kk, x_, a_):
    """Literal transcription of predecessor's script 01 Charlier_symbolic:
    total += binomial(k,m) * poch_negx * (-1/a)**m   [poch_negk computed but UNUSED]"""
    total = sp.Integer(0)
    poch_negx = sp.Integer(1)
    for m_ in range(0, kk+1):
        if m_ > 0:
            poch_negx *= (-x_ + (m_-1))
        total += binomial(kk, m_) * poch_negx * (-1/a_)**m_
    return total

mism3 = 0
for kk in range(0, 7):
    x_ = kk - n - 1
    a_ = (1-gam)*n/gam
    pred_val = sp.expand((1-gam)**kk * predecessor_charlier_aswritten(kk, x_, a_))
    wrong_val = sp.expand((1-gam)**kk * charlier_WRONG(kk, x_, a_))
    d = sp.simplify(pred_val - wrong_val)
    print(f"  k={kk}: predecessor-as-written vs target's WRONG-sign reconstruction, diff={d}")
    if d != 0: mism3 += 1
print(f"Mismatches: {mism3}/7 (expect 0 -- confirms target's diagnosis IS the predecessor's actual bug, not merely a coincidentally-matching alternative bug)\n")

# ---------------------------------------------------------------------
print("="*78)
print("CHECK 4: Vandermonde-type convolution sum_j C(j+m,m)C(n-j,m) = C(n+m+1,2m+1)")
print("extended range 0<=m<=n<=12 (target checked <=8)")
print("="*78)
mism4 = 0
cnt4 = 0
for n_val in range(0, 13):
    for m_val in range(0, n_val+1):
        lhs = sum(sp.binomial(j+m_val, m_val)*sp.binomial(n_val-j, m_val) for j in range(0, n_val-m_val+1))
        rhs = sp.binomial(n_val+m_val+1, 2*m_val+1)
        cnt4 += 1
        if sp.simplify(lhs-rhs) != 0:
            mism4 += 1
            print(f"  MISMATCH n={n_val} m={m_val}")
print(f"Mismatches: {mism4}/{cnt4} (expect 0)\n")

# ---------------------------------------------------------------------
print("="*78)
print("CHECK 5: double-sum swap identity S_n' = sum_m (g^m/n^m) m! T(n,m), fresh (n,g)")
print("(different sample points than target's script 03: n in {4,7,10,15}, new gammas)")
print("="*78)
def A_k_num(n_, k_, g: Fraction):
    total = Fraction(0)
    for m_ in range(0, k_+1):
        prod = Fraction(1)
        for i in range(1, m_+1):
            prod *= Fraction(n_-(k_-i), n_)
        total += comb(k_, m_) * g**m_ * (1-g)**(k_-m_) * prod
    return total

def S_n_direct(n_, g):
    return sum(A_k_num(n_, k_, g) for k_ in range(1, n_+1))

def T_exact(n_, m_, g):
    return sum(comb(j+m_, m_)*comb(n_-j, m_)*(1-g)**j for j in range(0, n_-m_+1))

def S_n_prime_swap(n_, g):
    total = Fraction(0)
    for m_ in range(0, n_+1):
        fact_m = 1
        for t in range(2, m_+1): fact_m *= t
        total += (g**m_ / Fraction(n_)**m_) * fact_m * T_exact(n_, m_, g)
    return total

mism5 = 0
cnt5 = 0
for n_val in [4, 7, 10, 15]:
    for gn, gd in [(1,4),(3,10),(5,9),(9,13)]:
        g = Fraction(gn, gd)
        direct = S_n_direct(n_val, g) + 1
        swap = S_n_prime_swap(n_val, g)
        cnt5 += 1
        ok = direct == swap
        if not ok: mism5 += 1
        print(f"  n={n_val:3d} g={gn}/{gd}: {'OK' if ok else 'MISMATCH: '+str(direct)+' vs '+str(swap)}")
print(f"Mismatches: {mism5}/{cnt5} (expect 0)\n")

# ---------------------------------------------------------------------
print("="*78)
print("CHECK 6: hand-derived c(gamma)=2(1-gamma)/gamma via explicit asymptotic")
print("expansion of term_0, term_1 (independent symbolic route, series-based not")
print("exact-sum based, to cross-validate script 07's exact-sum-then-limit route)")
print("="*78)
g_s = symbols('g', positive=True)
N = symbols('N', positive=True)
# term0(n,g) = (1-(1-g)^{n+1})/g  -> exact; drop exp-small piece for large-n asymptotics
term0_asym = 1/g_s
# term1(n,g) asymptotic large-n part (from target's script 07 sympy output, re-derived
# here independently via direct polynomial-part extraction of the finite sum formula
# using sympy.summation fresh, not copying the script's variable names/structure)
j = symbols('j')
T1_full = sp.summation((j+1)*(N-j)*(1-g_s)**j, (j, 0, N-1))
term1_full = sp.simplify((g_s/N)*T1_full)
print("term1_full (independent symbolic re-derivation):")
print(" ", term1_full)
# drop exponentially small (1-g)^N, (1-g)^(N-1) terms for the n->oo asymptotic behavior
term1_poly = sp.simplify(term1_full.subs({(1-g_s)**N: 0, (1-g_s)**(N-1): 0}))
print("term1 (poly part, exp-small dropped):", term1_poly)
ratio = sp.simplify(term0_asym/term1_poly)
logratio = sp.series(sp.log(ratio), N, sp.oo, 3)
print("log(term0/term1) series in 1/N:", logratio)
climit = sp.limit(N*sp.log(term0_asym/term1_poly), N, sp.oo)
print("N*log(term0/term1) -> ", sp.simplify(climit))
predicted = 2*(1-g_s)/g_s
print("predicted c=2(1-g)/g:", predicted)
print("difference:", sp.simplify(climit - predicted))

print()
print("ALL CHECKS DONE.")
