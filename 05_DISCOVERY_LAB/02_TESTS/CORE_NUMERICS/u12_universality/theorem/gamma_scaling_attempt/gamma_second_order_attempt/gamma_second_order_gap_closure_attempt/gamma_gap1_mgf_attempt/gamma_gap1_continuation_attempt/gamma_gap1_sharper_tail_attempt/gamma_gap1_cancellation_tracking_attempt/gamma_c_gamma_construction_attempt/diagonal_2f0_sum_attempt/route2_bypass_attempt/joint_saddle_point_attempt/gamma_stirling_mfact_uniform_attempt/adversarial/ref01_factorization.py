#!/usr/bin/env python3
"""
Referee script 01 -- independent re-derivation of the F(n,m,gamma) exact
factorization, from the primary cited definitions, written from scratch
(NOT copied or adapted from the front's own script 01).

Primary cited definitions (grandparent ATTEMPT.md Sec 1, PROVED):
  term_m(n,gamma) := (gamma^m/n^m) * m! * T(n,m)
  T(n,m) = C(n+m+1, 2m+1) * I(n,m,gamma) / B(m+1,m+1)
  B(m+1,m+1) = m!*m!/(2m+1)!
  C(n+m+1,2m+1) = (n+m+1)! / [ (2m+1)! * (n-m)! ]

Claim under test:
  term_m(n,gamma) = F(n,m,gamma) * I(n,m,gamma),
  F(n,m,gamma) := (gamma/n)^m * (n+m+1)! / [ (n-m)! * m! ]
"""
import sympy as sp
from fractions import Fraction
import math, random

n, m, g = sp.symbols('n m gamma', positive=True)

# Build purely from primary definitions, independently of the front's script.
Beta_m1_m1 = sp.factorial(m)*sp.factorial(m)/sp.factorial(2*m+1)
Cnm = sp.factorial(n+m+1) / (sp.factorial(2*m+1) * sp.factorial(n-m))
T_over_I = Cnm / Beta_m1_m1          # T(n,m)/I(n,m,gamma)

term_over_I = (g**m/n**m) * sp.factorial(m) * T_over_I   # term_m / I(n,m,gamma)

F_claim = (g/n)**m * sp.factorial(n+m+1) / (sp.factorial(n-m)*sp.factorial(m))

diff = sp.simplify(term_over_I - F_claim)
print("Symbolic difference term_m/I - F_claim:", diff)
assert diff == 0
print("CONFIRMED: exact algebraic identity holds symbolically (independent re-derivation).")

# Exact-Fraction numeric re-check on a DISJOINT random grid from the front's
# (front used n in {3,5,8,12,20,37}, m<=6, gamma in {1/4,2/7,1/2,5/6}).
random.seed(20260952001)  # deterministic seed, disjoint block just for reproducibility of *this* script's own random grid choice (not drawn from the reserved 20260952000-999 seed block claimed unused by numerics -- this is a pure Python RNG seed for grid selection only, not a probabilistic numerical method)
trials = []
for _ in range(200):
    nn = random.choice([4, 6, 9, 13, 17, 25, 41, 59, 100])
    mm = random.randint(0, min(nn, 9))
    gg = Fraction(random.randint(1, 20), random.randint(21, 40))
    trials.append((nn, mm, gg))

def T_over_I_exact(nn, mm):
    binom = Fraction(math.comb(nn+mm+1, 2*mm+1))
    Bmm = Fraction(math.factorial(mm)**2, math.factorial(2*mm+1))
    return binom / Bmm

max_err = Fraction(0)
for nn, mm, gg in trials:
    term_over_I_val = (gg**mm) * Fraction(1, nn**mm) * Fraction(math.factorial(mm)) * T_over_I_exact(nn, mm)
    F_val = (gg**mm) * Fraction(1, nn**mm) * Fraction(math.factorial(nn+mm+1), math.factorial(nn-mm)*math.factorial(mm))
    err = abs(term_over_I_val - F_val)
    max_err = max(max_err, err)

print(f"{len(trials)} independent random exact-Fraction (n,m,gamma) triples "
      f"(disjoint grid from the front's own, seeded deterministically):")
print("  max |term_m/I - F| =", max_err)
assert max_err == 0
print("CONFIRMED exactly: 0 mismatches. F(n,m,gamma) factorization independently reproduced.")
