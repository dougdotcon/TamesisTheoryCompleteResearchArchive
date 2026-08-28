#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check of Corollary D3.2 (mean recovery) and
D3.3-D3.4 (second/third moment limits), by independently, symbolically
integrating Proposicao D3's own stated closed form (transcribed fresh
from ATTEMPT.md Sec 4.1, not from any script in this lineage) and
comparing against:

  (i) THEOREM.md Estagio 4's cited finite-n mean formula, transcribed
      independently from THEOREM.md's own prose (line "phi_n^(3) = 16/35
      + 1/(14n) + 11/(10n^2) + 23/(35n^3) + 6/(35n^4)  (todo n>=4)",
      read directly by this referee, not taken on the front's word);
  (ii) THEOREM.md Estagio 17's cited continuum moments (E[M_3]=16/35,
       E[M_3^2]=1/4, E[M_3^3]=16/105), also independently re-read from
       THEOREM.md's own prose;
  (iii) the true brute-force distribution of T at n=3..9
        (bruteforce_full_cdf_results.json, this directory), to check the
        n=3 edge case explicitly, since THEOREM.md Estagio 4 states its
        mean formula only for "todo n>=4" -- this script checks whether
        the formula (and Corollary D3.2's claimed identity) also happens
        to hold at n=3, or whether there is a silent edge-case gap.

No .py file from this lineage was read to build this.
"""

import json
import sys
from fractions import Fraction

import sympy as sp

n, k = sp.symbols('n k', positive=True)


def d3_formula_sym():
    """Proposicao D3, transcribed fresh (symbolic) from ATTEMPT.md Sec 4.1."""
    return (
        k * (k + 1) * (
            k**4 - 4 * k**3
            - (3 * n**2 - 9 * n - 5) * k**2
            + (3 * n**2 - 11 * n - 2) * k
            + (3 * n**4 - 12 * n**3 + 12 * n**2 + 2 * n)
        )
        / (n**4 * (n - 1) * (n - 2))
    )


def main():
    F = d3_formula_sym()
    print("D3 formula (symbolic, transcribed independently):")
    sp.pprint(F)
    print()

    # --- Corollary D3.2: mean recovery ---
    print("=" * 78)
    print("Corollary D3.2: mean recovery")
    print("=" * 78)
    S = sp.summation(F, (k, 0, n - 1))
    S = sp.simplify(S)
    mean_from_D3 = sp.simplify(1 - S / n)
    mean_from_D3 = sp.nsimplify(sp.factor(sp.together(mean_from_D3)))
    mean_from_D3 = sp.apart(mean_from_D3, n)
    print("phi_n^(3) derived from D3 (symbolic, sympy sp.summation, exact) =")
    sp.pprint(sp.simplify(sp.expand(mean_from_D3)))

    # Estagio 4's cited formula, transcribed independently from THEOREM.md's
    # own prose (this referee re-read THEOREM.md directly, not the front's
    # transcription):
    phi_n3_cited = sp.Rational(16, 35) + sp.Rational(1, 14) / n + sp.Rational(11, 10) / n**2 \
        + sp.Rational(23, 35) / n**3 + sp.Rational(6, 35) / n**4

    diff = sp.simplify(mean_from_D3 - phi_n3_cited)
    print(f"\nphi_n^(3) cited from THEOREM.md Estagio 4 (independently "
          f"re-transcribed by this referee) = {phi_n3_cited}")
    print(f"difference (D3-derived minus THEOREM.md-cited), symbolic = {diff}")
    d32_ok = (diff == 0)
    print(f"Corollary D3.2 (exact symbolic mean recovery): "
          f"{'CONFIRMED' if d32_ok else '*** FAILS ***'}")

    # --- n=3 edge case: THEOREM.md states the mean formula "todo n>=4" ---
    print()
    print("-" * 78)
    print("Edge case: THEOREM.md's own text states phi_n^(3) 'para todo "
          "n>=4' -- does the formula (and hence Corollary D3.2's identity) "
          "also silently hold at n=3, where D3 itself claims validity "
          "('para todo n>=3')?")
    print("-" * 78)
    bf_path = __file__.replace("mean_and_moments_check.py", "bruteforce_full_cdf_results.json")
    with open(bf_path) as fh:
        bf = json.load(fh)
    n3 = bf.get("3")
    if n3 is not None:
        total = n3["total_configs"]
        counts = n3["counts"]
        ET = sum(int(t) * c for t, c in counts.items())
        mean_true_n3 = Fraction(ET, total * 3)  # E[T]/n
        mean_formula_at_3 = phi_n3_cited.subs(n, 3)
        mean_d3_at_3 = mean_from_D3.subs(n, 3)
        print(f"True bruteforce E[M_3^(3)] at n=3 (exact)        = {mean_true_n3}")
        print(f"THEOREM.md Estagio-4 formula evaluated at n=3     = {sp.nsimplify(mean_formula_at_3)}")
        print(f"D3-derived mean formula evaluated at n=3          = {sp.nsimplify(mean_d3_at_3)}")
        edge_ok_true_vs_d3 = (sp.Rational(mean_true_n3.numerator, mean_true_n3.denominator) == sp.nsimplify(mean_d3_at_3))
        edge_ok_formula_vs_true = (sp.Rational(mean_true_n3.numerator, mean_true_n3.denominator) == sp.nsimplify(mean_formula_at_3))
        print(f"  true == D3-derived-formula-at-n=3 : {edge_ok_true_vs_d3}")
        print(f"  true == Estagio4-formula-at-n=3   : {edge_ok_formula_vs_true} "
              f"(NOTE: THEOREM.md itself does not claim this formula for n=3; "
              f"this is purely an out-of-stated-range extrapolation check.)")
    else:
        print("n=3 bruteforce data not found -- skipping edge case check.")

    # --- Corollaries D3.3 / D3.4: second/third moment limits ---
    print()
    print("=" * 78)
    print("Corollaries D3.3/D3.4: 2nd/3rd moment limits")
    print("=" * 78)
    # E[T^2]/n^2 and E[T^3]/n^3 via E[X] = sum_{k=0}^{n-1} P(X>k) generalizes
    # for higher moments via E[g(T)] = g(0) + sum_{t=0}^{n-1}(g(t+1)-g(t)) P(T>t)
    # Simpler: directly compute E[T^2] = sum_{t=0}^n t^2 P(T=t) using pmf
    # p(t) = F(t)-F(t-1) (with F(-1)=0), from D3's own F.
    def Fk(kk):
        if kk < 0:
            return sp.Integer(0)
        expr = F.subs(k, kk)
        return expr
    # But k must range 0..n-1 symbolically for pmf except top mass at t=n.
    # Build pmf symbolically: p(t) = F(t) - F(t-1) for t=0..n-1, p(n) = 1-F(n-1).
    t = sp.symbols('t', integer=True, nonnegative=True)
    Ft = F  # F(k) with symbol k already; reuse via substitution
    Ft_minus1 = F.subs(k, k - 1)
    pmf_t = sp.simplify(Ft - Ft_minus1)  # valid for k=1..n-1 (k=0: F(0)-F(-1)=F(0))
    # E[T^2] = sum_{k=0}^{n-1} k^2 * pmf(k)  +  n^2 * (1 - F(n-1))
    ET2_inner = sp.summation(sp.expand(k**2 * pmf_t), (k, 1, n - 1))
    F0 = F.subs(k, 0)
    ET2 = sp.simplify(ET2_inner + 0**2 * F0 + n**2 * (1 - F.subs(k, n - 1)))
    EM2 = sp.simplify(ET2 / n**2)
    EM2 = sp.apart(sp.factor(sp.together(EM2)), n)
    print("E[(M_n^(3))^2] derived from D3 (independent symbolic derivation) =")
    sp.pprint(sp.expand(EM2))
    lim_EM2 = sp.limit(EM2, n, sp.oo)
    print(f"limit n->oo = {lim_EM2}  (continuum anchor E[M_3^2]=1/4, "
          f"THEOREM.md Estagio 17, independently re-read)")
    d33_ok = (lim_EM2 == sp.Rational(1, 4))

    ET3_inner = sp.summation(sp.expand(k**3 * pmf_t), (k, 1, n - 1))
    ET3 = sp.simplify(ET3_inner + 0**3 * F0 + n**3 * (1 - F.subs(k, n - 1)))
    EM3 = sp.simplify(ET3 / n**3)
    EM3 = sp.apart(sp.factor(sp.together(EM3)), n)
    print("\nE[(M_n^(3))^3] derived from D3 (independent symbolic derivation) =")
    sp.pprint(sp.expand(EM3))
    lim_EM3 = sp.limit(EM3, n, sp.oo)
    print(f"limit n->oo = {lim_EM3}  (continuum anchor E[M_3^3]=16/105, "
          f"THEOREM.md Estagio 17, independently re-read)")
    d34_ok = (lim_EM3 == sp.Rational(16, 105))

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Corollary D3.2 (mean recovery, zero symbolic remainder): "
          f"{'CONFIRMED' if d32_ok else 'FAILS'}")
    print(f"Corollary D3.3 (2nd moment limit = 1/4): "
          f"{'CONFIRMED' if d33_ok else 'FAILS'}")
    print(f"Corollary D3.4 (3rd moment limit = 16/105): "
          f"{'CONFIRMED' if d34_ok else 'FAILS'}")

    all_ok = d32_ok and d33_ok and d34_ok
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
