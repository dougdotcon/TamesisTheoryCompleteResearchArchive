"""
K3-FULL-CDF-ATTEMPT -- Step 4: final, comprehensive cross-validation of
Proposicao D3 (the closed-form CDF proved symbolically in
symbolic_derivation_full_cdf.py).

Runs three independent checks, all exact (Fraction/Rational, zero
floating point):

  (A) Proposicao D3's formula vs. fresh true brute force of Definition 4
      itself (true_bruteforce_full_cdf_k3.py), n=3..8, EVERY k. This is
      the strongest possible check: full enumeration of n!*n^3
      configurations, no reduced model, no shortcut of any kind.

  (B) Proposicao D3's formula vs. the exact O(n^3) reference engine
      (conditional_cdf.full_cdf_exact, itself built from the proved
      Decomposition Theorem), n=6..40, EVERY k -- far beyond what true
      brute force can reach, still exact.

  (C) Symbolic recovery of THREE independently-established quantities by
      exactly integrating/summing the closed-form CDF (sp.summation, no
      floating point):
        (C1) the mean  phi_n^{(3)} = E[M_n^{(3)}]  -- ALREADY PROVED and
             on record at THEOREM.md line ~1531 (cited, not re-derived):
                phi_n^{(3)} = 16/35 + 1/(14n) + 11/(10n^2) + 23/(35n^3)
                              + 6/(35n^4),  for all n>=4.
             Proposicao D3 must reproduce this EXACTLY (a nontrivial
             symbolic identity -- a wrong CDF would essentially never
             pass this).
        (C2) E[(M_n^{(3)})^2] -> 1/4 as n->infinity, matching Corollary
             NN3.1 (Estagio 35, cited) and the continuum anchor
             E[M_3^2]=1/4 (Estagio 18).
        (C3) E[(M_n^{(3)})^3] -> 16/105 as n->infinity, matching the
             already-proved continuum third moment (THEOREM.md, cited,
             f_{M_3}(x)=6x(1-x^2)^2).
"""
import sys
import sympy as sp
from fractions import Fraction

from conditional_cdf import full_cdf_exact


def F_conjectured_frac(nval, kval):
    nval = Fraction(nval)
    kval = Fraction(kval)
    c2 = 3 * nval ** 2 - 9 * nval - 5
    c1 = 3 * nval ** 2 - 11 * nval - 2
    c0 = 3 * nval ** 4 - 12 * nval ** 3 + 12 * nval ** 2 + 2 * nval
    quartic = kval ** 4 - 4 * kval ** 3 - c2 * kval ** 2 + c1 * kval + c0
    D = nval ** 4 * (nval - 1) * (nval - 2)
    return kval * (kval + 1) * quartic / D


def check_A_true_bruteforce():
    print("(A) Proposicao D3 vs fresh true brute force (Definition 4, n=3..8):")
    from true_bruteforce_full_cdf_k3 import cdf_at_n
    all_ok = True
    for nv in range(3, 9):
        cdf, total = cdf_at_n(nv)
        row_ok = True
        for kv in range(0, nv + 1):
            pred = F_conjectured_frac(nv, kv) if kv < nv else Fraction(1)
            if pred != cdf[kv]:
                row_ok = False
                print(f"    MISMATCH n={nv} k={kv}: D3={pred} true={cdf[kv]}")
        all_ok &= row_ok
        print(f"  n={nv} ({total} exact configs): {'ALL MATCH' if row_ok else 'MISMATCH FOUND'}")
    assert all_ok
    print("  (A) PASSED: zero discrepancies against full exhaustive enumeration.\n")


def check_B_exact_reference_engine():
    print("(B) Proposicao D3 vs O(n^3) exact reference engine, n=6..40, every k:")
    all_ok = True
    checked = 0
    for nv in range(6, 41):
        for kv in range(0, nv):
            pred = F_conjectured_frac(nv, kv)
            ref = full_cdf_exact(nv, kv)
            checked += 1
            if pred != ref:
                all_ok = False
                print(f"    MISMATCH n={nv} k={kv}: D3={pred} ref={ref}")
        if full_cdf_exact(nv, nv) != 1:
            all_ok = False
            print(f"    MISMATCH n={nv} k=n: ref != 1")
    assert all_ok
    print(f"  (B) PASSED: {checked} exact (n,k) pairs, zero discrepancies.\n")


def check_C_moment_recovery():
    print("(C) Symbolic recovery of independently-established moments:")
    n_, k_ = sp.symbols('n k', positive=True)
    c2 = 3 * n_ ** 2 - 9 * n_ - 5
    c1 = 3 * n_ ** 2 - 11 * n_ - 2
    c0 = 3 * n_ ** 4 - 12 * n_ ** 3 + 12 * n_ ** 2 + 2 * n_
    quartic = k_ ** 4 - 4 * k_ ** 3 - c2 * k_ ** 2 + c1 * k_ + c0
    D = n_ ** 4 * (n_ - 1) * (n_ - 2)
    F = sp.expand(k_ * (k_ + 1) * quartic / D)

    Fk, Fkm1 = F, F.subs(k_, k_ - 1)
    pmf_mid = sp.simplify(Fk - Fkm1)  # P(T=k), valid k=1..n-1

    # (C1) mean
    ET = sp.simplify(n_ - sp.summation(F, (k_, 0, n_ - 1)))
    phi = sp.simplify(ET / n_)
    target_phi = (sp.Rational(16, 35) + sp.Rational(1, 14) / n_
                  + sp.Rational(11, 10) / n_ ** 2 + sp.Rational(23, 35) / n_ ** 3
                  + sp.Rational(6, 35) / n_ ** 4)
    d1 = sp.simplify(phi - target_phi)
    print(f"  (C1) phi_n^(3) derived from D3   = {sp.expand(phi)}")
    print(f"       phi_n^(3) cited (THEOREM.md) = {sp.expand(target_phi)}")
    print(f"       difference = {d1}")
    assert d1 == 0
    print("       (C1) PASSED: EXACT symbolic match, for all n, to the already-proved mean.\n")

    # (C2) second moment limit
    ET2 = (0 ** 2 * F.subs(k_, 0) + n_ ** 2 * sp.simplify(1 - F.subs(k_, n_ - 1))
           + sp.summation(k_ ** 2 * pmf_mid, (k_, 1, n_ - 1)))
    m2 = sp.simplify(ET2 / n_ ** 2)
    lim2 = sp.limit(m2, n_, sp.oo)
    print(f"  (C2) E[(M_n^(3))^2] derived from D3 = {sp.apart(m2, n_)}")
    print(f"       limit as n->oo = {lim2}  (must equal 1/4, Corollary NN3.1 / Estagio 18)")
    assert lim2 == sp.Rational(1, 4)
    print("       (C2) PASSED.\n")

    # (C3) third moment limit
    ET3 = (0 ** 3 * F.subs(k_, 0) + n_ ** 3 * sp.simplify(1 - F.subs(k_, n_ - 1))
           + sp.summation(k_ ** 3 * pmf_mid, (k_, 1, n_ - 1)))
    m3 = sp.simplify(ET3 / n_ ** 3)
    lim3 = sp.limit(m3, n_, sp.oo)
    print(f"  (C3) E[(M_n^(3))^3] derived from D3 = {sp.apart(m3, n_)}")
    print(f"       limit as n->oo = {lim3}  (must equal 16/105, continuum f_M3, THEOREM.md)")
    assert lim3 == sp.Rational(16, 105)
    print("       (C3) PASSED.\n")


def check_corollary_D3_1():
    print("Corollary D3.1 (elementary, hand-provable): P(T=n) = 6/n^3 exactly.")
    n_, k_ = sp.symbols('n k', positive=True)
    c2 = 3 * n_ ** 2 - 9 * n_ - 5
    c1 = 3 * n_ ** 2 - 11 * n_ - 2
    c0 = 3 * n_ ** 4 - 12 * n_ ** 3 + 12 * n_ ** 2 + 2 * n_
    quartic = k_ ** 4 - 4 * k_ ** 3 - c2 * k_ ** 2 + c1 * k_ + c0
    D = n_ ** 4 * (n_ - 1) * (n_ - 2)
    F = k_ * (k_ + 1) * quartic / D
    val = sp.simplify(1 - F.subs(k_, n_ - 1))
    print(f"  1 - F(n-1) = {val}")
    assert val == 6 / n_ ** 3
    print("  matches 6/n^3 exactly, for all n (symbolic). PASSED.\n")


if __name__ == "__main__":
    check_corollary_D3_1()
    check_A_true_bruteforce()
    check_B_exact_reference_engine()
    check_C_moment_recovery()
    print("=" * 78)
    print("ALL FINAL VERIFICATION CHECKS PASSED.")
    print("=" * 78)
