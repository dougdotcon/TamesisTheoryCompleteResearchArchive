#!/usr/bin/env python3
"""
Script 01 -- light re-derivation of the exact m!/binomial-prefactor
structure F(n,m,gamma) of term_m(n,gamma), and cross-verification
against the CITED (PROVED) definitions.

CITED, not re-derived (per mandate):
  - term_m(n,gamma) := (gamma^m / n^m) * m! * T(n,m)
      [joint_saddle_point_attempt/ATTEMPT.md Sec.1, line 187]
  - T(n,m) = binom(n+m+1, 2m+1) * I(n,m,gamma) / B(m+1,m+1)
      [joint_saddle_point_attempt/ATTEMPT.md Sec.1, line 185, itself
       citing the referee's Beta-integral closed form, PROVED]
  - I(n,m,gamma) := int_0^1 t^m (1-t)^m (1-gamma t)^{n-m} dt
      [same source]

NEW (this front): the exact algebraic simplification

   term_m(n,gamma) = F(n,m,gamma) * I(n,m,gamma),
   F(n,m,gamma) := (gamma/n)^m * (n+m+1)! / ( (n-m)! * m! )

obtained by expanding B(m+1,m+1) = m!^2/(2m+1)! and
binom(n+m+1,2m+1) = (n+m+1)!/((2m+1)!(n-m)!), and observing the
(2m+1)! factors cancel exactly. This is PURE ALGEBRA (an exact
identity, no approximation) -- verified here symbolically (sympy,
exact) and numerically (exact Fraction arithmetic at many integer
(n,m) triples), not merely asserted.

Deliverable of this script: the confirmed exact closed form for F,
which is the sole object this front's Delta_m correction will be
built from (Sec 2-3 apply Stirling's series to its factorial pieces).
"""
import sympy as sp
from sympy import symbols, factorial, gamma as Gamma, binomial, Rational, simplify, nsimplify
from fractions import Fraction
import math

print("="*78)
print("PART A: symbolic exact identity  term_m = F * I")
print("="*78)

n, m, g = symbols('n m gamma', positive=True)

# T(n,m) via the cited Beta-integral closed form (I is left abstract --
# we only manipulate the PREFACTOR outside I).
B_m1_m1 = factorial(m)**2 / factorial(2*m+1)          # B(m+1,m+1)
binom_nm = factorial(n+m+1) / (factorial(2*m+1) * factorial(n-m))

T_prefactor = binom_nm / B_m1_m1     # T(n,m) = T_prefactor * I(n,m,gamma)

term_m_prefactor = (g**m / n**m) * factorial(m) * T_prefactor
term_m_prefactor_simplified = sp.simplify(term_m_prefactor)

F_claimed = (g/n)**m * factorial(n+m+1) / (factorial(n-m) * factorial(m))

diff = sp.simplify(term_m_prefactor_simplified - F_claimed)
print("term_m prefactor (from cited T(n,m), B(m+1,m+1)) simplifies to:")
print(" ", term_m_prefactor_simplified)
print("Claimed F(n,m,gamma):")
print(" ", F_claimed)
print("Symbolic difference (should be exactly 0):", diff)
assert diff == 0, "ALGEBRA MISMATCH -- STOP"
print("CONFIRMED: term_m(n,gamma) = F(n,m,gamma) * I(n,m,gamma) exactly, with")
print("  F(n,m,gamma) = (gamma/n)^m * (n+m+1)! / ( (n-m)! * m! )")
print("The (2m+1)! factors from binom(n+m+1,2m+1) and 1/B(m+1,m+1) cancel exactly.")

print()
print("="*78)
print("PART B: numeric cross-check via exact Fraction arithmetic")
print("="*78)

def T_prefactor_exact(nn, mm):
    # binom(n+m+1,2m+1) / B(m+1,m+1), exact rational
    from math import comb, factorial as fact
    binom = Fraction(comb(nn+mm+1, 2*mm+1))
    Bmm = Fraction(fact(mm)**2, fact(2*mm+1))
    return binom / Bmm

def F_exact(nn, mm, gg: Fraction):
    from math import factorial as fact
    return (gg**mm) * Fraction(1, nn**mm) * Fraction(fact(nn+mm+1), fact(nn-mm)*fact(mm))

trials = [(nn, mm, Fraction(a, b))
          for nn in [3, 5, 8, 12, 20, 37]
          for mm in range(0, min(nn, 6)+1)
          for (a, b) in [(1, 4), (2, 7), (1, 2), (5, 6)]]

max_err = 0
count = 0
for nn, mm, gg in trials:
    # term_m prefactor via literal cited formulas
    term_pref = (gg**mm) * Fraction(1, nn**mm) * Fraction(math.factorial(mm)) * T_prefactor_exact(nn, mm)
    F_val = F_exact(nn, mm, gg)
    diff = term_pref - F_val
    max_err = max(max_err, abs(diff))
    count += 1

print(f"{count} exact-Fraction (n,m,gamma) triples checked, n in [3,37], m<=6,")
print("  gamma in {1/4,2/7,1/2,5/6}: max |term_m_prefactor - F| =", max_err)
assert max_err == 0
print("CONFIRMED exactly (Fraction arithmetic, zero tolerance): 0 mismatches.")

print()
print("="*78)
print("PART C: sanity checks on F alone")
print("="*78)

# m=0 check: F(n,0,gamma) should be 1 exactly (gamma^0=1, (n+1)!/(n!*0!) = n+1... )
# wait: F(n,0,gamma)=(gamma/n)^0 * (n+1)!/(n! * 0!) = (n+1)!/(n!) = n+1. That's NOT 1;
# term_0 = F(n,0,gamma) * I(n,0,gamma). I(n,0,gamma) = int_0^1 (1-gamma t)^n dt
#        = (1-(1-gamma)^{n+1})/(gamma (n+1)).
# term_0 = (n+1) * (1-(1-gamma)^{n+1})/(gamma(n+1)) = (1-(1-gamma)^{n+1})/gamma
# matches the cited sanity limit term_0(n,gamma) -> 1/gamma as n->infty
# (joint_saddle_point_attempt/ATTEMPT.md line 223). Verify this composition:
gg = Rational(1, 3)
nn_sym = symbols('n', positive=True, integer=True)
F0 = F_claimed.subs(m, 0)
F0_simplified = sp.simplify(F0)
print("F(n,0,gamma) simplifies to:", F0_simplified, " (expected: n+1)")
assert sp.simplify(F0_simplified - (n+1)) == 0

I0 = (1 - (1-g)**(n+1)) / (g*(n+1))
term0 = sp.simplify(F0_simplified * I0)
print("term_0(n,gamma) = F(n,0,gamma)*I(n,0,gamma) simplifies to:", term0)
expected = (1 - (1-g)**(n+1)) / g
print("Expected (cited sanity fact):", expected)
assert sp.simplify(term0 - expected) == 0
print("CONFIRMED: m=0 composition matches the cited sanity limit exactly.")

print()
print("All Part A/B/C checks passed. F(n,m,gamma) established as the exact")
print("factorial/binomial-prefactor object this front's Delta_m will approximate.")
