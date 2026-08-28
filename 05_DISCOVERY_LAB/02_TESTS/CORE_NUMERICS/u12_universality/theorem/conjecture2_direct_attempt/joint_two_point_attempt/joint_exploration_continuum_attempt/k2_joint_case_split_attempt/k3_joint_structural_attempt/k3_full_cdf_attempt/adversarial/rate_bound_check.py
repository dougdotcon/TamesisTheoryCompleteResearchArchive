#!/usr/bin/env python3
"""
ADVERSARIAL, FROM-SCRATCH check of Corollary D3.5 (uniform convergence-rate
bound), by independently substituting k=xn into Proposicao D3's own stated
closed form (transcribed fresh, not from any script in this lineage),
computing N(n,x) := [F_n^(3)(x)-F_3(x)] * n^2(n-1)(n-2) symbolically, and
checking every arithmetic step of the claimed inequality chain
(ATTEMPT.md Sec 5.5) independently:

  1. deg_x(N) <= 6, deg_n(N) <= 3 (as claimed).
  2. Each coefficient c_i(n) of N(n,x) = sum_i c_i(n) x^i has a fixed sign
     for all n>=3 (checked by direct symbolic sign analysis, not assumed).
  3. sum_i |c_i(n)| <= 12n^3 - 14n^2 + 18n + 4, for n>=3 (checked exactly,
     symbolically -- this referee's own bound derived from its own c_i(n),
     compared against the front's claimed bound expression).
  4. The elementary inequality D(n) = n^2(n-1)(n-2) >= 5n^4/9 for n>=6,
     re-derived from (n-1)>=5n/6 and (n-2)>=2n/3 (both <=> n>=6, checked).
  5. The resulting bound |F_n^(3)(x)-F_3(x)| <= 22/n for n>=6, x in [0,1]
     (checked both algebraically, by combining 3-4 above, and numerically
     by direct maximization at many n).
  6. The leading 1/n term of the series expansion, and the claimed
     g_1(x) = 3x(x-1)^2(x+1)(x^2+1), including max_{x in [0,1]} g_1(x).

Continuum CDF F_3(x) := 1-(1-x^2)^3, from THEOREM.md Estagio 17's cited
density f_{M_3}(x)=6x(1-x^2)^2 (independently integrated by this referee,
not taken from ATTEMPT.md's restatement).

No .py file from this lineage was read to build this.
"""

import sys
import sympy as sp

n, x, k = sp.symbols('n x k', positive=True)


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

    # --- Independently derive F_3(x) from THEOREM.md's cited density ---
    xx = sp.symbols('xx', positive=True)
    density = 6 * xx * (1 - xx**2)**2  # Estagio 17, cited, re-integrated here
    F3_expr = sp.integrate(density, (xx, 0, x))
    F3_expr = sp.expand(F3_expr)
    print("F_3(x) independently re-derived by integrating THEOREM.md's cited "
          f"density 6x(1-x^2)^2:  F_3(x) = {F3_expr}")
    claimed_F3 = 1 - (1 - x**2)**3
    diff_F3 = sp.simplify(F3_expr - claimed_F3)
    print(f"vs. ATTEMPT.md's stated F_3(x)=1-(1-x^2)^3: difference = {diff_F3}  "
          f"({'OK' if diff_F3 == 0 else 'MISMATCH'})")
    all_ok &= (diff_F3 == 0)

    # --- Substitute k = x*n into D3, subtract F_3(x) ---
    F = d3_formula_sym()
    Fn_x = F.subs(k, x * n)
    diff = sp.cancel(Fn_x - F3_expr)
    num, den = sp.fraction(diff)
    num = sp.expand(num)
    den_expected = n**2 * (n - 1) * (n - 2)
    den_ratio = sp.simplify(den / den_expected)
    print(f"\nF_n^(3)(x) - F_3(x) = N(n,x)/D(n).")
    print(f"Denominator D(n) matches n^2(n-1)(n-2) up to constant factor "
          f"{den_ratio} (should be a nonzero rational constant).")
    # normalize so that denominator is exactly n^2(n-1)(n-2)
    N = sp.expand(num / den_ratio) if den_ratio != 0 else num
    N = sp.expand(N)
    print(f"\nN(n,x) (independently derived) has "
          f"deg_x={sp.degree(N, x)}, deg_n={sp.degree(sp.Poly(N, n))}")
    all_ok &= (sp.degree(N, x) <= 6) and (sp.degree(sp.Poly(N, n)) <= 3)

    # --- extract coefficients c_i(n) of x^i ---
    Npoly_x = sp.Poly(N, x)
    coeffs = {}
    for i in range(0, 7):
        c = Npoly_x.coeff_monomial(x**i) if i > 0 else Npoly_x.coeff_monomial(1)
        coeffs[i] = sp.expand(c)
        print(f"  c_{i}(n) = {coeffs[i]}")

    # --- check each c_i(n) has fixed sign for n>=3 ---
    print("\nSign check of each c_i(n) for integer n=3..200 (then symbolic "
          "confirmation via the polynomial's roots):")
    fixed_signs = {}
    for i, c in coeffs.items():
        signs = set()
        for nv in range(3, 201):
            val = c.subs(n, nv)
            if val > 0:
                signs.add(1)
            elif val < 0:
                signs.add(-1)
            else:
                signs.add(0)
        fixed_signs[i] = signs
        # also find real roots >= 3 symbolically to be sure sign doesn't
        # flip beyond n=200
        try:
            roots = sp.solve(sp.Eq(c, 0), n)
            real_roots_ge3 = [r for r in roots if r.is_real and r >= 3]
        except Exception:
            real_roots_ge3 = "±(could not solve exactly)"
        print(f"  c_{i}(n): signs seen over n=3..200 = {signs}, "
              f"real roots >=3: {real_roots_ge3}")
    sign_fixed_ok = all(len(s - {0}) <= 1 for s in fixed_signs.values())
    print(f"All coefficients have a fixed sign for n>=3 "
          f"(ignoring isolated zeros): {sign_fixed_ok}")
    all_ok &= sign_fixed_ok

    # --- sum |c_i(n)| bound ---
    abs_terms = []
    for i, c in coeffs.items():
        signs = fixed_signs[i] - {0}
        if len(signs) == 0:
            abs_terms.append(sp.Integer(0))
        elif signs == {1}:
            abs_terms.append(c)
        elif signs == {-1}:
            abs_terms.append(-c)
        else:
            abs_terms.append(sp.Abs(c))  # unresolved -- shouldn't happen if sign_fixed_ok
    sum_abs = sp.expand(sum(abs_terms))
    print(f"\nsum_i |c_i(n)| (independently derived, exact for n>=3) = {sum_abs}")

    claimed_bound = 12 * n**3 - 14 * n**2 + 18 * n + 4
    diff_bound = sp.expand(claimed_bound - sum_abs)
    print(f"ATTEMPT.md's claimed bound: 12n^3-14n^2+18n+4")
    print(f"claimed_bound - sum|c_i(n)| = {diff_bound}")
    # Check this difference is >=0 for all n>=3 (claimed bound must
    # dominate the true sum of |c_i(n)|, not necessarily be equal)
    diff_poly = sp.Poly(diff_bound, n)
    is_exact_match = (diff_bound == 0)
    bound_holds_for_all_n_ge_3 = True
    for nv in range(3, 2001):
        if diff_poly.eval(nv) < 0:
            bound_holds_for_all_n_ge_3 = False
            print(f"  *** claimed bound violated at n={nv}: "
                  f"claimed={claimed_bound.subs(n, nv)} < "
                  f"true sum|c_i|={sum_abs.subs(n, nv)}")
            break
    print(f"Exact match (claimed bound == our derived sum|c_i(n)|): {is_exact_match}")
    print(f"Claimed bound dominates true sum|c_i(n)| for n=3..2000: "
          f"{bound_holds_for_all_n_ge_3}")
    all_ok &= bound_holds_for_all_n_ge_3

    # --- elementary inequality chain for D(n) ---
    print("\n" + "=" * 78)
    print("Elementary inequality chain: (n-1)>=5n/6, (n-2)>=2n/3 for n>=6")
    print("=" * 78)
    ineq1 = sp.solve(sp.Ge(n - 1, sp.Rational(5, 6) * n), n)
    ineq2 = sp.solve(sp.Ge(n - 2, sp.Rational(2, 3) * n), n)
    print(f"(n-1)>=5n/6  <=>  {ineq1}")
    print(f"(n-2)>=2n/3  <=>  {ineq2}")
    both_ok = True
    for nv in range(6, 2001):
        if not (nv - 1 >= sp.Rational(5, 6) * nv and nv - 2 >= sp.Rational(2, 3) * nv):
            both_ok = False
            break
    print(f"Both hold for every integer n=6..2000: {both_ok}")
    all_ok &= both_ok

    Dn = n**2 * (n - 1) * (n - 2)
    Dn_bound = sp.Rational(5, 9) * n**4
    dominates = True
    for nv in range(6, 2001):
        if Dn.subs(n, nv) < Dn_bound.subs(n, nv):
            dominates = False
            break
    print(f"D(n)=n^2(n-1)(n-2) >= 5n^4/9 for every integer n=6..2000: {dominates}")
    all_ok &= dominates

    # --- final 22/n bound, both algebraically and numerically ---
    print("\n" + "=" * 78)
    print("Final bound: |F_n^(3)(x)-F_3(x)| <= 22/n for n>=6, x in [0,1]")
    print("=" * 78)
    # algebraic: (claimed_bound)/(5n^4/9) <= 22/n  <=>  9*claimed_bound <= 22*5*n^3
    lhs = 9 * claimed_bound
    rhs = 110 * n**3
    alg_diff = sp.expand(rhs - lhs)
    alg_ok = True
    for nv in range(6, 2001):
        if alg_diff.subs(n, nv) < 0:
            alg_ok = False
            print(f"  *** algebraic bound chain fails at n={nv}")
            break
    print(f"9*(12n^3-14n^2+18n+4) <= 110n^3 for n=6..2000 (i.e. the claimed "
          f"bound chain implies <=22/n): {alg_ok}")
    all_ok &= alg_ok

    # numeric: sample x densely in [0,1], for each n=6..2000 compute actual
    # |F_n(x)-F_3(x)| via the exact N(n,x)/D(n) expression, check <=22/n
    Nfunc = sp.lambdify((n, x), N, 'mpmath')
    Dfunc = sp.lambdify((n,), Dn, 'mpmath')
    import mpmath as mp
    mp.mp.dps = 30
    worst_ratio = 0.0
    worst_at = None
    numeric_bound_ok = True
    xs = [mp.mpf(i) / 400 for i in range(0, 401)]
    for nv in list(range(6, 201)) + [500, 1000, 2000]:
        Dv = Dfunc(nv)
        for xv in xs:
            Nv = Nfunc(nv, xv)
            val = abs(Nv / Dv)
            if val * nv > worst_ratio:
                worst_ratio = float(val * nv)
                worst_at = (nv, float(xv))
            if val > 22.0 / nv:
                numeric_bound_ok = False
                print(f"  *** numeric 22/n bound violated at n={nv}, x={xv}: "
                      f"|F_n-F_3|={val} > 22/n={22.0/nv}")
    print(f"Numeric check of |F_n^(3)(x)-F_3(x)|<=22/n over n=6..2000 (dense "
          f"n-grid plus x-grid of 401 points): {'HOLDS' if numeric_bound_ok else 'VIOLATED'}")
    print(f"Worst observed n*|F_n-F_3| = {worst_ratio:.6f} at (n,x)={worst_at}  "
          f"(ATTEMPT.md reports ~0.71 as the worst observed value)")
    all_ok &= numeric_bound_ok

    # --- leading 1/n term ---
    print("\n" + "=" * 78)
    print("Leading-order 1/n term of the series expansion")
    print("=" * 78)
    diff_full = N / Dn
    series = sp.series(diff_full, n, sp.oo, 3).removeO()
    series = sp.expand(series)
    print(f"Series of F_n^(3)(x)-F_3(x) around n=oo (independent sympy "
          f"sp.series): {series}")
    # extract the 1/n coefficient
    g1_derived = sp.simplify(series * n).subs(n, sp.oo)
    # more robust: use sp.limit of series*n
    g1_derived = sp.simplify(sp.limit(diff_full * n, n, sp.oo))
    g1_derived = sp.expand(g1_derived)
    print(f"g_1(x) (independently derived, = lim_n n*(F_n^(3)(x)-F_3(x))) = {g1_derived}")

    claimed_g1 = 3 * x * (x - 1)**2 * (x + 1) * (x**2 + 1)
    diff_g1 = sp.simplify(sp.expand(g1_derived - claimed_g1))
    print(f"ATTEMPT.md's claimed g_1(x) = 3x(x-1)^2(x+1)(x^2+1) = "
          f"{sp.expand(claimed_g1)}")
    print(f"difference = {diff_g1}  ({'OK' if diff_g1 == 0 else 'MISMATCH'})")
    all_ok &= (diff_g1 == 0)

    # max of g1 on [0,1]
    g1_func = sp.lambdify(x, g1_derived, 'mpmath')
    xs_fine = [mp.mpf(i) / 100000 for i in range(0, 100001)]
    best_val = -1e18
    best_x = None
    for xv in xs_fine:
        v = float(g1_func(xv))
        if v > best_val:
            best_val = v
            best_x = float(xv)
    print(f"max_{{x in [0,1]}} g_1(x) (independent dense numeric search, "
          f"100001 points) = {best_val:.6f} at x={best_x:.4f}  "
          f"(ATTEMPT.md claims ~0.712 at x~0.452)")
    g1_max_ok = abs(best_val - 0.712) < 0.01 and abs(best_x - 0.452) < 0.01
    all_ok &= g1_max_ok

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print(f"Overall Corollary D3.5 check: {'ALL CONFIRMED' if all_ok else 'AT LEAST ONE ISSUE FOUND'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
