"""
Checks a specific EXPLANATORY claim in ATTEMPT.md Sec 3.3:

  "... shifts the conditional value from V_a(n)->1/2 to V_b(n)->1/3
  -- an O(1) jump -- which is exactly enough to produce an O(1/n)
  contribution to the overall average (2/n*Theta(1)), DOMINATING
  WHATEVER O(1/n^2) BEHAVIOR CASE (A) ALONE WOULD HAVE SHOWN."

This script checks, by exact symbolic algebra (sympy, no floating
point), whether Case (a) alone (V_a(n)) really does exhibit O(1/n^2)
convergence to 1/2, as claimed, or something else. It also decomposes
the final rate coefficient -1/6 into the two cases' separate
contributions, to see exactly where it comes from.

Purely deterministic/exact computation -- no randomness, no seed
needed.
"""
import sympy as sp

n = sp.symbols('n', positive=True)

Va = sp.Rational(1) * (3 * n + 1) / (6 * n)
Vb = (n + 1) / (3 * n)

print("=" * 78)
print("Claim under test: 'Case (a) alone [V_a(n)] would show O(1/n^2)")
print("behavior' (ATTEMPT.md Sec 3.3)")
print("=" * 78)

Va_minus_half = sp.simplify(Va - sp.Rational(1, 2))
print(f"V_a(n) = {sp.nsimplify(Va)}")
print(f"V_a(n) - 1/2 = {Va_minus_half}")
print(f"  -> this is exactly 1/(6n), i.e. Theta(1/n), NOT Theta(1/n^2).")
print(f"  -> DIRECTLY CONTRADICTS the document's claim that Case(a) alone")
print(f"     would show O(1/n^2) convergence to 1/2.")
assert sp.simplify(Va_minus_half - sp.Rational(1, 6) / n) == 0
print()

Vb_minus_third = sp.simplify(Vb - sp.Rational(1, 3))
print(f"V_b(n) = {sp.nsimplify(Vb)}")
print(f"V_b(n) - 1/3 = {Vb_minus_third}  (= 1/(3n), also Theta(1/n))")
print()

print("=" * 78)
print("Exact decomposition of the OVERALL rate coefficient (-1/6) into")
print("each case's WEIGHTED contribution to P_n^(1)(both) - 1/2")
print("=" * 78)

case_a_weighted = sp.simplify((n - 2) / n * Va)
case_b_weighted = sp.simplify(sp.Rational(2) / n * Vb)
total = sp.simplify(case_a_weighted + case_b_weighted)

print(f"(n-2)/n * V_a(n) = {sp.expand(case_a_weighted)}")
case_a_dev = sp.simplify(case_a_weighted - sp.Rational(1, 2))
print(f"  deviation from 1/2 = {sp.apart(case_a_dev, n)}"
      f"   [as n->infty, leading O(1/n) coefficient = "
      f"{sp.limit(case_a_dev * n, n, sp.oo)}]")
print()
print(f"(2/n) * V_b(n) = {sp.expand(case_b_weighted)}")
case_b_dev = case_b_weighted  # this term has no constant piece
print(f"  this term itself = {sp.apart(case_b_weighted, n)}"
      f"   [as n->infty, leading O(1/n) coefficient = "
      f"{sp.limit(case_b_weighted * n, n, sp.oo)}]")
print()
print(f"Sum = {sp.expand(total)}")
total_dev = sp.simplify(total - sp.Rational(1, 2))
print(f"Sum - 1/2 = {sp.apart(total_dev, n)}")
print(f"Leading O(1/n) coefficient of the SUM: "
      f"{sp.limit(total_dev * n, n, sp.oo)}")
print()

doc_closed_form = sp.Rational(3) * n**2 - n + 2
doc_closed_form = doc_closed_form / (6 * n**2)
assert sp.simplify(total - doc_closed_form) == 0
print("Confirmed: (n-2)/n*V_a(n) + 2/n*V_b(n) exactly equals the "
      "document's closed form (3n^2-n+2)/(6n^2). [sanity check]")
print()

print("=" * 78)
print("VERDICT on the Sec 3.3 causal narrative")
print("=" * 78)
a_coef = sp.limit(case_a_dev * n, n, sp.oo)
b_coef = sp.limit(case_b_weighted * n, n, sp.oo)
total_coef = sp.limit(total_dev * n, n, sp.oo)
print(f"Case (a)'s weighted contribution to the O(1/n) coefficient: {a_coef}")
print(f"Case (b)/(c)'s weighted contribution: {b_coef}")
print(f"Sum of the two (must equal the overall document-claimed -1/6): "
      f"{a_coef + b_coef}  ==  {total_coef}")
print()
print("CONCLUSION: Case (a) alone contributes {} to the O(1/n) rate, "
      "NOT ZERO/O(1/n^2) as the document's narrative claims. Case (b)/(c)'s "
      "contribution ({}) does not simply 'produce' the O(1/n) rate on top "
      "of an O(1/n^2) Case-(a) baseline -- the two O(1/n) contributions "
      "PARTIALLY CANCEL ({} + {} = {}) to give the net -1/6. The document's "
      "explanatory claim that Case (a) alone 'would have shown' O(1/n^2) "
      "behavior is FALSE, directly contradicted by V_a(n)'s own closed "
      "form, (3n+1)/(6n) = 1/2 + 1/(6n).".format(
          a_coef, b_coef, a_coef, b_coef, a_coef + b_coef))
