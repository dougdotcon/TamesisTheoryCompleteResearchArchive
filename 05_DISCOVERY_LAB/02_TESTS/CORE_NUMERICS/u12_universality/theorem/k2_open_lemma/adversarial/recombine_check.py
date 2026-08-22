#!/usr/bin/env python3
"""
Final assembly: combine my two from-scratch-derived closed forms
  psi_n^{(2)}    = (8n^2+4n+1)/(15n^2)          [independent_symbolic_derivation.py]
  psi_n^{(2),R}  = (n+1)(5n+2)/(12n^2)          [derive_psiR_from_scratch.py, now DERIVED
                                                  not fitted]
via Lemma A: phi_n^{(2)} = (2/n) psi_R + (1-2/n) psi
and check this matches ATTEMPT.md's bonus-rate formula
  phi_n^{(2)} = 8/15 + 1/(30n) + 7/(10n^2) + 1/(5n^3)
symbolically (not just at sampled n), closing the "fitted, not derived" gap.
"""
import sympy as sp

n = sp.symbols('n', positive=True, integer=True)

psi = sp.Rational(8, 15) + sp.Rational(4, 15) / n + sp.Rational(1, 15) / n**2
psiR = (n + 1) * (5 * n + 2) / (12 * n**2)

lemA = sp.Rational(2) / n * psiR + (1 - sp.Rational(2) / n) * psi
lemA = sp.simplify(lemA)
print("Lemma A recombination, from BOTH first-principles-derived pieces:")
sp.pprint(sp.factor(sp.together(lemA)))

claimed = sp.Rational(8, 15) + sp.Rational(1, 30) / n + sp.Rational(7, 10) / n**2 + sp.Rational(1, 5) / n**3
diff = sp.simplify(lemA - claimed)
print(f"\nDifference from ATTEMPT.md's bonus rate formula: {diff}")
print(f"Identically zero (symbolic)? {diff == 0}")

print("\n=> If True: phi_n^{(2)} = 8/15 + 1/(30n) + 7/(10n^2) + 1/(5n^3) is now a fully")
print("   PROVED identity (both Lemma-A ingredients derived from scratch, not fitted),")
print("   not merely 'proved modulo psi_R being fitted' as ATTEMPT.md §6/§8 states.")
