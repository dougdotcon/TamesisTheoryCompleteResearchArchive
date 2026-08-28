#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check of the three-regime boundary claims
(ATTEMPT.md Sec 4.3) and Corollary D3.1, using Proposicao D3's own formula
(transcribed fresh) plus this referee's own bruteforce/reduced-model data
(bruteforce_full_cdf_results.json, reduced_model_independent.py), NOT any
script from this lineage.

Checks:
  (1) F(n-2) [Proposicao D3 at k=n-2] symbolically equals the front's
      claimed regime-(ii) endpoint value (n^4-42n+72)/n^4.
  (2) F(n-1) symbolically equals 1-6/n^3 (regime-(iii) endpoint,
      = the front's own Corollary D3.1's target).
  (3) Corollary D3.1 (P(T=n)=6/n^3, independent of L) is checked directly
      against TRUE brute force ground truth at n=3..9 (1-F(n-1) computed
      from actual exhaustive counts, not from the D3 formula).
  (4) A genuinely independent re-derivation of Corollary D3.1's own
      elementary argument: T=n requires S={0,1,2} AND V_0=L_0,V_1=L_1,
      V_2=L_2 exactly; using this referee's own re-derived Prop S formula
      P(S={0,1,2}|L)=6p_0p_1p_2 and P(V_s=L_s|S)=1/L_s independence, check
      P(T=n|L)=6/n^3 is independent of L, by direct symbolic substitution
      (own derivation, not copied).
  (5) A structural sanity check that the three k-regimes as described
      (0<=k<=n-3 "generic"; k=n-2; k=n-1) exactly partition {0,...,n-1}
      with no gap or overlap -- trivial but checked explicitly since it
      is exactly the kind of off-by-one error referees are asked to hunt.
"""

import json
import sys
from fractions import Fraction

import sympy as sp

n, k, L0, L1, L2 = sp.symbols('n k L0 L1 L2', positive=True)


def d3_formula_sym():
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
    all_ok = True
    F = d3_formula_sym()

    print("=" * 78)
    print("(1)-(2) Regime endpoint values")
    print("=" * 78)
    F_at_nm2 = sp.simplify(F.subs(k, n - 2))
    claimed_nm2 = (n**4 - 42 * n + 72) / n**4
    diff_nm2 = sp.simplify(F_at_nm2 - claimed_nm2)
    print(f"D3 at k=n-2: F(n-2) = {sp.factor(F_at_nm2)}")
    print(f"claimed regime-(ii) endpoint (n^4-42n+72)/n^4 = {claimed_nm2}")
    print(f"difference = {diff_nm2}  ({'OK' if diff_nm2 == 0 else 'MISMATCH'})")
    all_ok &= (diff_nm2 == 0)

    F_at_nm1 = sp.simplify(F.subs(k, n - 1))
    claimed_nm1 = 1 - 6 / n**3
    diff_nm1 = sp.simplify(F_at_nm1 - claimed_nm1)
    print(f"\nD3 at k=n-1: F(n-1) = {sp.factor(F_at_nm1)}")
    print(f"claimed regime-(iii) endpoint 1-6/n^3 = {sp.nsimplify(claimed_nm1)}")
    print(f"difference = {diff_nm1}  ({'OK' if diff_nm1 == 0 else 'MISMATCH'})")
    all_ok &= (diff_nm1 == 0)

    print("\n" + "=" * 78)
    print("(3) Corollary D3.1 (P(T=n)=6/n^3) vs TRUE brute force")
    print("=" * 78)
    bf_path = __file__.replace("three_regime_boundary_check.py", "bruteforce_full_cdf_results.json")
    with open(bf_path) as fh:
        bf = json.load(fh)
    for nstr in sorted(bf.keys(), key=int):
        nv = int(nstr)
        entry = bf[nstr]
        total = entry["total_configs"]
        counts = entry["counts"]
        count_T_eq_n = counts.get(str(nv), 0)
        p_true = Fraction(count_T_eq_n, total)
        p_claimed = Fraction(6, nv**3)
        ok = (p_true == p_claimed)
        all_ok &= ok
        print(f"  n={nv}: P(T=n) true (bruteforce) = {p_true}, "
              f"claimed 6/n^3 = {p_claimed}  {'OK' if ok else 'MISMATCH'}")

    print("\n" + "=" * 78)
    print("(4) Independent re-derivation of Corollary D3.1's own argument")
    print("=" * 78)
    # Our own re-derived Prop S: P(S={0,1,2}|L) = 6 p0 p1 p2, p_i=L_i/n
    p0, p1, p2 = L0 / n, L1 / n, L2 / n
    P_S_full = 6 * p0 * p1 * p2
    # P(V_0=L_0,V_1=L_1,V_2=L_2 | S={0,1,2}) = 1/(L0*L1*L2) by independence+uniformity
    P_exact_landing = 1 / (L0 * L1 * L2)
    P_T_eq_n_given_L = sp.simplify(P_S_full * P_exact_landing)
    print(f"P(T=n | L0,L1,L2) [own derivation from Prop S + uniform-independent "
          f"V_s] = {P_T_eq_n_given_L}")
    is_L_independent = (len(P_T_eq_n_given_L.free_symbols & {L0, L1, L2}) == 0)
    print(f"Independent of L0,L1,L2 (as claimed): {is_L_independent}, "
          f"value = 6/n^3: {sp.simplify(P_T_eq_n_given_L - 6/n**3) == 0}")
    all_ok &= is_L_independent and (sp.simplify(P_T_eq_n_given_L - 6/n**3) == 0)

    print("\n" + "=" * 78)
    print("(5) Structural partition check: {0<=k<=n-3} u {n-2} u {n-1} == {0,...,n-1}")
    print("=" * 78)
    partition_ok = True
    for nv in range(3, 50):
        regime_i = set(range(0, nv - 2))       # 0..n-3
        regime_ii = {nv - 2}
        regime_iii = {nv - 1}
        union = regime_i | regime_ii | regime_iii
        full = set(range(0, nv))
        overlap = (regime_i & regime_ii) | (regime_i & regime_iii) | (regime_ii & regime_iii)
        if union != full or overlap:
            partition_ok = False
            print(f"  *** partition FAILS at n={nv}: union={sorted(union)}, "
                  f"full={sorted(full)}, overlap={overlap}")
    print(f"Regimes (i)/(ii)/(iii) exactly partition {{0,...,n-1}} with no "
          f"gap/overlap, for n=3..49: {partition_ok}  "
          f"(note: at n=3, regime (i)'s range 0..n-3=0..0 is nonempty and "
          f"regime (ii)=n-2=1, (iii)=n-1=2 -- all three regimes are "
          f"present even at the smallest allowed n=3)")
    all_ok &= partition_ok

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Overall: {'ALL CONFIRMED' if all_ok else 'AT LEAST ONE ISSUE FOUND'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
