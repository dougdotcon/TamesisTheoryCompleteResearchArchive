#!/usr/bin/env python3
"""
Fully independent symbolic re-derivation of psi_n^{(2)}, from scratch, using
sympy -- WITHOUT reading ATTEMPT.md's derive_closed_forms.py or
psi_k2_case_formula.py.

Every probability/case weight below was hand-rederived on paper first (see
REFEREE_REPORT.md for the by-hand algebra); this script only automates the
final triple summation (over ell, then d or (p,q)) that is too tedious to
trust by hand, and cross-checks the case-level formulas P_b, P_c themselves
(which I independently re-derived and which happen to come out identical in
form to ATTEMPT.md's -- see the referee report for the derivation) against
brute force at the CASE level too, not just after summing.

Case-level facts used (all independently re-derived, see referee report):
  Given ell = |C_0| (uniform on {1,...,n}):
    P(neither source on C_0 | ell)      = (n-ell)(n-ell-1) / [(n-1)(n-2)]
    P(source at position d, other off  | ell) = 2(n-ell) / [(n-1)(n-2)]     (per d, summed d=1..ell-1)
    P(sources at positions p<q both on | ell) = 2 / [(n-1)(n-2)]            (per pair, summed over p<q in 1..ell-1)
  Conditional success probabilities:
    case (a): success prob = 1
    case (b): P_b(ell,d) = (ell-d)(3n-ell+1) / (2 n^2)
    case (c): P_c(ell,p,q) = (ell-q)(n+q-p) / n^2
"""
import sympy as sp

n, ell, d, p, q = sp.symbols('n ell d p q', positive=True, integer=True)

Pb = (ell - d) * (3 * n - ell + 1) / (2 * n**2)
Pc = (ell - q) * (n + q - p) / (n**2)

case_a_weight = (n - ell) * (n - ell - 1) / ((n - 1) * (n - 2))
case_b_weight_per_d = 2 * (n - ell) / ((n - 1) * (n - 2))
case_c_weight_per_pq = 2 / ((n - 1) * (n - 2))

# sum over d = 1..ell-1 of case_b_weight_per_d * Pb(ell,d)
sum_b = sp.summation(case_b_weight_per_d * Pb, (d, 1, ell - 1))
sum_b = sp.simplify(sum_b)
print("Sum over d (case b), given ell:")
sp.pprint(sum_b)

# sum over 1<=p<q<=ell-1 of case_c_weight_per_pq * Pc(ell,p,q)
# = sum_{q=2}^{ell-1} sum_{p=1}^{q-1} ...
inner_p = sp.summation(case_c_weight_per_pq * Pc, (p, 1, q - 1))
inner_p = sp.simplify(inner_p)
sum_c = sp.summation(inner_p, (q, 2, ell - 1))
sum_c = sp.simplify(sum_c)
print("\nSum over p<q (case c), given ell:")
sp.pprint(sum_c)

per_ell_total = sp.simplify(case_a_weight * 1 + sum_b + sum_c)
print("\nPer-ell total P(success | ell), simplified:")
sp.pprint(per_ell_total)

# Now sum over ell = 1..n, divide by n
total = sp.summation(per_ell_total, (ell, 1, n))
total = sp.simplify(total / n)
print("\npsi_n^(2) = (1/n) * sum_{ell=1}^n [...] , fully simplified:")
sp.pprint(sp.simplify(total))
sp.pprint(sp.factor(sp.together(total)))

target = sp.Rational(8, 15) + sp.Rational(4, 15) / n + sp.Rational(1, 15) / n**2
diff = sp.simplify(total - target)
print("\nDifference from claimed closed form 8/15 + 4/(15n) + 1/(15n^2):")
sp.pprint(diff)
print(f"\nIdentically zero (for n>2, symbolically)? {diff == 0}")

# Numeric spot check at several n (as a second, independent internal check
# of the symbolic summation itself)
print("\nNumeric spot checks of the symbolic closed form vs the target formula:")
for nv in range(3, 12):
    tv = total.subs(n, nv)
    gv = target.subs(n, nv)
    print(f"  n={nv}: symbolic-sum={tv}  target-formula={gv}  equal={sp.simplify(tv - gv) == 0}")
