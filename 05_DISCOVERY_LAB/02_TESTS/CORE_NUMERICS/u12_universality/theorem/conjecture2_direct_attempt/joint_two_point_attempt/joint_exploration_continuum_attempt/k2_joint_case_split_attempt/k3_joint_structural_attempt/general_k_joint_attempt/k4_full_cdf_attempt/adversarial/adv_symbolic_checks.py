#!/usr/bin/env python3
"""
INDEPENDENT symbolic checks of Proposicao D4 and its corollaries, built
entirely from ATTEMPT.md's own PROSE (the stated closed-form formulas),
using sympy from scratch. No .py file from any front was read.

Covers task items (c), (d), (e), (f):
  (c) regime partition/boundary continuity of the single stated formula
      across k=0..n-1 (monotonicity, range [0,1], and the specific
      boundary values quoted in ATTEMPT.md section 4.2's transcript).
  (d) independent re-derivation of Corollary D4.2's mean formula by
      exact symbolic summation of the standard identity
      phi_n^(4) = 1 - (1/n) sum_{k=0}^{n-1} F(k).
  (e) independent re-derivation, via elementary integration of the
      cited general-K continuum density f_{M_K}(x)=2Kx(1-x^2)^{K-1}
      (Estagio 24), of E[M_4^3] and E[M_5^3], to check Corollary
      D4.4's claimed values and its "K=5 instance" cross-check.
  (f) re-derivation and verification of Corollary D4.5's rate-bound
      arithmetic chain.
"""
import sympy as sp

n, k, x = sp.symbols('n k x', positive=True)

def Q_D4(nn, kk):
    return (-kk**6 + 9*kk**5 + (4*nn**2 - 18*nn - 31)*kk**4
            + (-16*nn**2 + 80*nn + 51)*kk**3
            + (-6*nn**4 + 42*nn**3 - 55*nn**2 - 120*nn - 40)*kk**2
            + (6*nn**4 - 50*nn**3 + 97*nn**2 + 70*nn + 12)*kk
            + 4*nn**6 - 30*nn**5 + 74*nn**4 - 52*nn**3 - 30*nn**2 - 12*nn)

def F_D4(nn, kk):
    num = kk*(kk+1)*Q_D4(nn, kk)
    den = nn**5*(nn-1)*(nn-2)*(nn-3)
    return sp.together(num/den)

print("=" * 78)
print("(c) REGIME BOUNDARY / RANGE / MONOTONICITY CHECKS")
print("=" * 78)

# 1. F(n) should be 1 trivially -- but formula is only claimed for k<=n-1;
#    still check F(n-1) < 1 and (separately) that 1-F(n-1) = 24/n^4 (D4.1/regime iv).
val_nm1 = sp.simplify(1 - F_D4(n, n-1))
print(f"1 - F(n-1) [should be 24/n^4, matching D4.1 and ATTEMPT.md's own "
      f"regime (iv) '1-24/n^4']:")
print(f"    = {val_nm1}")
print(f"    matches 24/n^4 exactly: {sp.simplify(val_nm1 - sp.Rational(24,1)/n**4) == 0}")

# 2. Reproduce the three boundary transcripts quoted in section 4.2 verbatim:
target_ii = (n**6 - n**5 - 984*n**2 + 5160*n - 7200)/(n**5*(n-1))
target_iii = (n**5 - 216*n + 480)/n**5
target_iv = 1 - sp.Rational(24,1)/n**4

diff_ii = sp.simplify(F_D4(n, n-3) - target_ii)
diff_iii = sp.simplify(F_D4(n, n-2) - target_iii)
diff_iv = sp.simplify(F_D4(n, n-1) - target_iv)
print(f"\nF(n-3) - [quoted regime(ii) value] = {diff_ii}  (should be 0)")
print(f"F(n-2) - [quoted regime(iii) value] = {diff_iii}  (should be 0)")
print(f"F(n-1) - [quoted regime(iv) value]  = {diff_iv}  (should be 0)")

# 3. F(0) should be 0 (k(k+1) factor forces P(T<=0)=0)
print(f"\nF(0) = {sp.simplify(F_D4(n,0))}  (should be 0)")

# 4. Monotonicity + range check numerically at several concrete n (exact rationals)
print("\nNumeric monotonicity + [0,1]-range spot-check (exact Fractions), "
      "n=4..40:")
from fractions import Fraction
def Q_num(nn, kk):
    return (-kk**6 + 9*kk**5 + (4*nn**2 - 18*nn - 31)*kk**4
            + (-16*nn**2 + 80*nn + 51)*kk**3
            + (-6*nn**4 + 42*nn**3 - 55*nn**2 - 120*nn - 40)*kk**2
            + (6*nn**4 - 50*nn**3 + 97*nn**2 + 70*nn + 12)*kk
            + 4*nn**6 - 30*nn**5 + 74*nn**4 - 52*nn**3 - 30*nn**2 - 12*nn)
def F_num(nn, kk):
    if kk >= nn:
        return Fraction(1)
    if kk < 0:
        return Fraction(0)
    num = kk*(kk+1)*Q_num(nn, kk)
    den = nn**5*(nn-1)*(nn-2)*(nn-3)
    return Fraction(num, den)

bad = []
for nn in range(4, 41):
    prev = Fraction(0)
    for kk in range(0, nn+1):
        v = F_num(nn, kk)
        if not (Fraction(0) <= v <= Fraction(1)):
            bad.append((nn, kk, v, "out of range"))
        if v < prev:
            bad.append((nn, kk, v, f"decreased from {prev}"))
        prev = v
    if F_num(nn, nn-1) >= Fraction(1):
        bad.append((nn, nn-1, F_num(nn,nn-1), "F(n-1) >= 1, should be < 1"))
print(f"  n=4..40, monotonicity+range violations found: {len(bad)}")
for b in bad[:20]:
    print("   ", b)

print("\n" + "=" * 78)
print("(d) INDEPENDENT RE-DERIVATION OF COROLLARY D4.2's MEAN FORMULA")
print("=" * 78)
kk = sp.symbols('k')
Fk = F_D4(n, kk)
S = sp.summation(Fk, (kk, 0, n-1))
S = sp.simplify(S)
phi = sp.simplify(1 - S/n)
phi = sp.apart(phi, n)
print("phi_n^(4) = 1 - (1/n) sum_{k=0}^{n-1} F(k), computed independently via sp.summation:")
print(f"    = {phi}")

claimed = sp.Rational(128,315) + sp.Rational(23,210)/n + sp.Rational(482,315)/n**2 \
    + sp.Rational(99,70)/n**3 + sp.Rational(7,9)/n**4 + sp.Rational(4,21)/n**5
diff = sp.simplify(phi - claimed)
print(f"\nClaimed D4.2 formula: {claimed}")
print(f"Independent-minus-claimed difference (should be 0): {diff}")

# constant term / 1/n coefficient extraction, cross-check vs cited THEOREM.md
# invariants phi_4=128/315 (Estagio 20/24) and c_4=23/210 (Estagio 7)
const_term = sp.limit(phi, n, sp.oo)
coeff_1_over_n = sp.limit(n*(phi - const_term), n, sp.oo)
print(f"\nconstant term (n->oo limit) = {const_term}  (cited target phi_4=128/315, Estagio 20/24)")
print(f"coefficient of 1/n           = {coeff_1_over_n}  (cited target c_4=23/210, Estagio 7)")
print(f"  MATCH constant: {sp.simplify(const_term - sp.Rational(128,315))==0}")
print(f"  MATCH 1/n coeff: {sp.simplify(coeff_1_over_n - sp.Rational(23,210))==0}")

print("\n" + "=" * 78)
print("(e) INDEPENDENT MOMENT RE-DERIVATION FROM THE CITED CONTINUUM DENSITY, "
      "AND K=5 CROSS-CHECK")
print("=" * 78)
Kx = sp.symbols('K', positive=True, integer=True)
xs = sp.symbols('x', nonnegative=True)
def continuum_density(K):
    return 2*K*xs*(1-xs**2)**(K-1)

for Kval, label in [(4, "K=4 (Corollary D4.4's own claimed limit)"),
                     (5, "K=5 (THEOREM.md Estagio 24's own stated instance)")]:
    dens = continuum_density(Kval)
    m3 = sp.integrate(xs**3 * dens, (xs, 0, 1))
    m3 = sp.nsimplify(sp.simplify(m3))
    print(f"  E[M_{Kval}^3] via int_0^1 x^3 * 2*{Kval}*x*(1-x^2)^{Kval-1} dx "
          f"= {m3}   [{label}]")

print("\n  D4.4 claims E[M_4^3] -> 128/1155 : "
      f"{sp.nsimplify(continuum_density(4)) is not None}")
m3_4 = sp.nsimplify(sp.simplify(sp.integrate(xs**3*continuum_density(4), (xs,0,1))))
m3_5 = sp.nsimplify(sp.simplify(sp.integrate(xs**3*continuum_density(5), (xs,0,1))))
print(f"    independently computed E[M_4^3] = {m3_4}  (claimed 128/1155): "
      f"{m3_4 == sp.Rational(128,1155)}")
print(f"    independently computed E[M_5^3] = {m3_5}  (THEOREM.md Estagio 24's "
      f"own stated K=5 instance, 256/3003): {m3_5 == sp.Rational(256,3003)}")

# general closed form check E[M_K^3] = K! 2^K / prod_{j=0}^{K-1}(2j+5)
from math import factorial
def general_formula(K):
    denom = 1
    for j in range(K):
        denom *= (2*j+5)
    return sp.Rational(factorial(K) * 2**K, denom)
print(f"    general formula K!2^K/prod(2j+5) at K=4: {general_formula(4)} "
      f"(matches independent integral: {general_formula(4)==m3_4})")
print(f"    general formula K!2^K/prod(2j+5) at K=5: {general_formula(5)} "
      f"(matches independent integral and Estagio-24 citation: {general_formula(5)==m3_5})")

print("\n  E[M_4^2] and phi_4 sanity (should be 1/5 and 128/315):")
m2_4 = sp.simplify(sp.integrate(xs**2*continuum_density(4), (xs,0,1)))
m1_4 = sp.simplify(sp.integrate(xs*continuum_density(4), (xs,0,1)))
print(f"    E[M_4^2] = {m2_4}  (cited 1/(K+1)=1/5): {m2_4==sp.Rational(1,5)}")
print(f"    E[M_4]   = {m1_4}  (cited phi_4=128/315): {m1_4==sp.Rational(128,315)}")

print("\n" + "=" * 78)
print("(BONUS) INDEPENDENT RE-DERIVATION OF THE FULL FINITE-n D4.3/D4.4 "
      "FORMULAS (not just their limits), via a DIFFERENT identity "
      "(Abel/survival-function summation) from the one used for D4.2 above")
print("=" * 78)
def moment(p):
    survival = 1 - F_D4(n, kk)
    term = ((kk+1)**p - kk**p) * survival
    Ssum = sp.summation(term, (kk, 0, n-1))
    Ssum = sp.simplify(Ssum)
    return sp.apart(sp.simplify(Ssum/n**p), n)

m2 = moment(2)
m3b = moment(3)
claimed2 = sp.Rational(1,5)+sp.Rational(19,210)/n+sp.Rational(3,2)/n**2+sp.Rational(61,30)/n**3+sp.Rational(199,70)/n**4+sp.Rational(209,105)/n**5+sp.Rational(4,7)/n**6
claimed3b = sp.Rational(128,1155)+sp.Rational(5,77)/n+sp.Rational(9113,6930)/n**2+sp.Rational(4813,2310)/n**3+sp.Rational(5659,1386)/n**4+sp.Rational(719,154)/n**5+sp.Rational(1049,315)/n**6+sp.Rational(236,231)/n**7
print(f"  E[(M_n^4)^2] independent = {m2}")
print(f"    diff vs claimed D4.3 full finite-n formula: {sp.simplify(m2-claimed2)}")
print(f"  E[(M_n^4)^3] independent = {m3b}")
print(f"    diff vs claimed D4.4 full finite-n formula: {sp.simplify(m3b-claimed3b)}")

print("\n" + "=" * 78)
print("(f) COROLLARY D4.5 RATE-BOUND VERIFICATION")
print("=" * 78)
F4_continuum = 1 - (1-xs**2)**4
Fn_at_x = F_D4(n, xs*n)   # substitute k = x*n directly, per ATTEMPT.md's own method
gap = sp.cancel(sp.together(Fn_at_x - F4_continuum))
gap = sp.simplify(gap)
print("F_n^(4)(x) - F_4(x), exact (sp.cancel), as a single rational function:")
num, den = sp.fraction(gap)
num = sp.expand(num)
print(f"  denominator = {sp.factor(den)}")
# Confirm denominator matches ATTEMPT.md's claimed n^3(n-1)(n-2)(n-3)
claimed_den = n**3*(n-1)*(n-2)*(n-3)
print(f"  denominator matches claimed n^3(n-1)(n-2)(n-3): "
      f"{sp.simplify(den - claimed_den)==0 or sp.simplify(den + claimed_den)==0}")

# bound each x-coefficient of the numerator (as poly in n) by sum |coeffs|,
# exactly the method ATTEMPT.md describes
num_poly = sp.Poly(num, xs)
bound_expr = 0
for i, c in enumerate(num_poly.all_coeffs()[::-1]):
    c = sp.expand(c)
    cpoly = sp.Poly(c, n)
    coeff_abs_sum = sum(abs(sp.Rational(cc)) if cc.is_number else abs(cc)
                         for cc in cpoly.all_coeffs())
    bound_expr += coeff_abs_sum  # since |x^i|<=1 for x in [0,1]
print(f"\n  Sum of |coefficient-of-n^j| over all (i,j) [our own bound on |N(n,x)| "
      f"for x in [0,1]] = {bound_expr}")

# denominator lower bound n^3(n-1)(n-2)(n-3) >= n^6/8 for n>=6 -- verify directly
lhs = n**3*(n-1)*(n-2)*(n-3)
diff_bound = sp.simplify(lhs - n**6/sp.Rational(8))
print(f"  n^3(n-1)(n-2)(n-3) - n^6/8 = {sp.factor(diff_bound)}")
# check this is >=0 for n>=6 by evaluating at n=6 and checking derivative sign / just numeric scan
ok_bound = all(sp.simplify(lhs.subs(n, nn) - sp.Rational(nn,1)**6/8) >= 0 for nn in range(6, 60))
print(f"  n^3(n-1)(n-2)(n-3) >= n^6/8 holds for n=6..59 (spot scan): {ok_bound}")

final_bound = sp.simplify(bound_expr / sp.Rational(1,8))
print(f"\n  Resulting bound: |F_n^(4)(x)-F_4(x)| <= [{bound_expr}] / (n^6/8) "
      f"= {sp.nsimplify(final_bound)}/n  for n>=6, x in [0,1]")
print(f"  Claimed bound in ATTEMPT.md: 7248/n")
print(f"  Our own bound <= claimed bound (i.e. claimed bound is valid, "
      f"possibly not tight): {final_bound <= 7248}")

# also directly verify claimed 7248/n as an upper bound via a dense numeric scan
# (deterministic grid scan -- no randomness needed here; the mandate's reserved
# seed sub-range 20260926500-20260926799 is used instead in mc_bonus.py's
# genuine Monte Carlo triangulation)
worst_ratio = 0
gap_func = sp.lambdify((n, xs), gap, 'mpmath')
import mpmath as mp
mp.mp.dps = 30
max_violation = None
for nn in [6,7,8,9,10,15,20,30,50,100,300,1000,3000,10000]:
    worst = 0
    for i in range(0, 1001):
        xv = mp.mpf(i)/1000
        g = abs(gap_func(nn, xv))
        bound = mp.mpf(7248)/nn
        if g > bound:
            max_violation = (nn, xv, g, bound)
        worst = max(worst, g)
    ratio = worst / (mp.mpf(7248)/nn)
    if ratio > worst_ratio:
        worst_ratio = ratio
print(f"\n  Dense numeric scan n in {{6..10000}}, x-grid step 0.001: "
      f"worst observed |gap|/(7248/n) = {float(worst_ratio):.6f}")
print(f"  Any bound violation found: {max_violation}")

# also verify the "not proved uniform" leading-order term g_1(x) claimed in
# section 6.4's honest disclosure, and its claimed max ~0.7087 at x~0.3699
g1x = sp.expand(sp.simplify(sp.limit(gap*n, n, sp.oo)))
claimed_g1 = -6*xs**8 + 8*xs**7 + 6*xs**6 - 12*xs**5 + 6*xs**4 - 6*xs**2 + 4*xs
print(f"\n  Leading-order term g_1(x) [our own lim n(F_n-F_4)]: {g1x}")
print(f"  Claimed g_1(x) in ATTEMPT.md section 6.4: {sp.expand(claimed_g1)}")
print(f"  diff: {sp.expand(g1x - claimed_g1)}")
import numpy as np
g1f = sp.lambdify(xs, g1x, 'numpy')
xgrid = np.linspace(0, 1, 2000001)
vals = g1f(xgrid)
imax = np.argmax(vals)
print(f"  numeric max of g_1(x) on [0,1]: {vals[imax]:.6f} at x={xgrid[imax]:.4f} "
      f"(claimed ~0.7087 at x~0.3699)")
