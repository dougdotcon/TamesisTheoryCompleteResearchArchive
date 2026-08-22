#!/usr/bin/env python3
"""
An attempt to promote ATTEMPT.md item #8 (psi_n^{(2),R}, "CONFIRMED BY EXACT
FIT, not derived") to a genuine first-principles derivation, by redoing the
walk/target-set method of ATTEMPT.md section 4 but starting the walk AT
source 0 itself (y_0 = 0, f(0) = U_0 immediately), instead of at a generic
point.

By-hand derivation (see REFEREE_REPORT.md for the full writeup): let D be
source-0's OWN pi-cycle (independent of the reroute -- a pure pi-structural
fact), length m ~ Unif{1,...,n} (same classical fact used throughout
THEOREM.md / ATTEMPT.md). Because the walk from 0 does NOT traverse D before
the first reroute fires (0 is itself a source, so its first move is U_0, not
a step along pi), D stays completely untouched by the exploration until
something actually lands on it -- unlike the generic-point case, where the
reference point's own cycle gets partially "used up" walking up to the first
on-cycle source.

Working through the two sub-cases (source 1 off D / on D at position k) gives
EXACTLY the K=2 generic-point case-b and case-c formulas P_b(ell,d), P_c(ell,
p,q) with "d=0" / "p=0" respectively (0 playing the role of "the source sits
at the very start of its own cycle"):

  source 1 OFF D (prob (n-m)/(n-1) given m):     success = P_b(m, 0) = m(3n-m+1)/(2n^2)
  source 1 ON D at position k (prob 1/(n-1) each, k=1..m-1): success = P_c(m,0,k) = (m-k)(n+k)/n^2

This script sums this over m=1..n with sympy, independently of ATTEMPT.md's
own derive_closed_forms.py (not read before writing this), and checks
whether it reproduces the *fitted* formula (5n+2)(n+1)/(12 n^2) exactly.
"""
import sympy as sp

n, m, k = sp.symbols('n m k', positive=True, integer=True)

Pb0 = m * (3 * n - m + 1) / (2 * n**2)                 # P_b(ell=m, d=0)
Pc0k = (m - k) * (n + k) / (n**2)                      # P_c(ell=m, p=0, q=k)

weight_off = (n - m) / (n - 1)
weight_on_each = 1 / (n - 1)

sum_on = sp.summation(weight_on_each * Pc0k, (k, 1, m - 1))
sum_on = sp.simplify(sum_on)
print("Sum over k=1..m-1 (source1 on D), given m:")
sp.pprint(sum_on)

per_m = sp.simplify(weight_off * Pb0 + sum_on)
print("\nPer-m total P(0 is cyclic | m), simplified:")
sp.pprint(per_m)

total = sp.summation(per_m, (m, 1, n))
total = sp.simplify(total / n)
print("\npsi_n^{(2),R} = (1/n) sum_{m=1}^n [...], fully simplified:")
sp.pprint(sp.factor(sp.together(total)))

claimed = sp.Rational(5, 12) + sp.Rational(7, 12) / n + sp.Rational(1, 6) / n**2
diff = sp.simplify(total - claimed)
print(f"\nDifference from the FITTED formula 5/12+7/(12n)+1/(6n^2)  ((5n+2)(n+1)/(12n^2)):")
sp.pprint(diff)
print(f"Identically zero (symbolic, for general n)? {diff == 0}")

print("\nNumeric spot checks:")
for nv in range(3, 12):
    tv = total.subs(n, nv)
    cv = claimed.subs(n, nv)
    print(f"  n={nv}: derived={tv}  fitted-claim={cv}  equal={sp.simplify(tv-cv)==0}")
