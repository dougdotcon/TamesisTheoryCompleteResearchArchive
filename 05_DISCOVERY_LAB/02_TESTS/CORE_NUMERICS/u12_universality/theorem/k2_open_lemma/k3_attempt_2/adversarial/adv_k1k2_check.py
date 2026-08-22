"""
Independent check (task item 4): recompute psi_n^(1), psi_n^(1),R, psi_n^(2),
psi_n^(2),R via THIS review's own symbolic ladder (adv_symbolic_recursion.py,
levels r=1 and r=2, which were independently derived and independently verified
against the defining recursion in that script) and confirm they match wave 5's
already-proved ATTEMPT.md formulas EXACTLY (symbolic difference == 0), not merely
numerically.
"""
import contextlib
import io
import sympy as sp

with contextlib.redirect_stdout(io.StringIO()):
    import adv_symbolic_recursion as A  # noqa: E402  (import prints suppressed)

n = A.n

psi1 = sp.simplify(A.g1_func(n).subs(A.b, 0))
psi1R = sp.simplify(A.h0(0, 0))
psi2 = sp.simplify(A.g2_func(n).subs(A.b, 0))
psi2R = sp.simplify(A.h1(0, 0))

t1 = sp.Rational(2, 3) + sp.Rational(1, 6) / n
t1R = sp.Rational(1, 2) + sp.Rational(1, 2) / n
t2 = sp.Rational(8, 15) + sp.Rational(4, 15) / n + sp.Rational(1, 15) / n**2
t2R = sp.together((5 * n + 2) * (n + 1)) / (12 * n**2)

print("psi_n^(1)  (my ladder) =", psi1, "  target (ATTEMPT.md SS3) =", t1,
      "  MATCH =", sp.simplify(psi1 - t1) == 0)
print("psi_n^(1),R (my ladder) =", psi1R, "  target (ATTEMPT.md SS3) =", t1R,
      "  MATCH =", sp.simplify(psi1R - t1R) == 0)
print("psi_n^(2)  (my ladder) =", psi2, "  target (ATTEMPT.md SS4.4) =", t2,
      "  MATCH =", sp.simplify(psi2 - t2) == 0)
print("psi_n^(2),R (my ladder) =", psi2R, "  target (ATTEMPT.md SS6) =", t2R,
      "  MATCH =", sp.simplify(psi2R - t2R) == 0)

# also confirm the Lemma-A recombination reproduces THEOREM.md Prop. 4 exactly at K=1
phi1 = sp.simplify(sp.together(sp.Rational(1, 1) / n * psi1R + (1 - sp.Rational(1, 1) / n) * psi1))
target_phi1 = sp.Rational(2, 3) + sp.Rational(1, 3) / n**2
print("phi_n^(1) via Lemma A =", phi1, "  target (THEOREM.md Prop.4) =", target_phi1,
      "  MATCH =", sp.simplify(phi1 - target_phi1) == 0)

# and K=2's bonus rate
phi2 = sp.simplify(sp.together(sp.Rational(2, 1) / n * psi2R + (1 - sp.Rational(2, 1) / n) * psi2))
target_phi2 = sp.Rational(8, 15) + sp.Rational(1, 30) / n + sp.Rational(7, 10) / n**2 + sp.Rational(1, 5) / n**3
print("phi_n^(2) via Lemma A =", phi2, "  target (ATTEMPT.md SS6) =", target_phi2,
      "  MATCH =", sp.simplify(phi2 - target_phi2) == 0)
