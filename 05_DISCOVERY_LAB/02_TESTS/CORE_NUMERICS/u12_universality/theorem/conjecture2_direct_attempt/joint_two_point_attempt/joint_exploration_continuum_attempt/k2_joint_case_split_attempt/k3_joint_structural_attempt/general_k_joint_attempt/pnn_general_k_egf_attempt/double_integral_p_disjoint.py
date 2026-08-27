"""
Task item 1: derive the integral representation of P_disjoint(s,s'), and
determine whether the naive TWO-variable Laplace transform (one variable
per cycle) collapses to something simpler.

Starting point (predecessor's own PROVED closed form, general_k_joint_attempt
/ATTEMPT.md sec 4.3, quoted verbatim in the mandate and re-read in full
above): for s != s', M := {0,...,K-1} \\ {s,s'} (|M| = K-2),

    P_same(s,s')     = x_s * x_s' * Sum_{S subseteq M} (|S|+1)! * Prod_{u in S} x_u
    P_disjoint(s,s') = x_s * x_s' * Sum_{S1,S2 subseteq M, S1 cap S2 = empty}
                            |S1|! Prod_{u in S1} x_u  *  |S2|! Prod_{u in S2} x_u

Written completely fresh from this mathematical description (THEOREM.md
Estagio 35 + the predecessor's ATTEMPT.md prose, sec 4.2-4.3, read in full).
No .py file from any front (this lineage or any sibling) was opened, read,
or imported.

RESULT (derived below, verified symbolically at |M|=m=0..4 against direct
brute enumeration over all element-to-{neither,S1,S2} assignments, and via
an independent double-integral evaluation for m<=3):

  (a) P_same(s,s') and P_disjoint(s,s'), as functions of x_M, are IDENTICAL
      -- a genuine algebraic identity, not a coincidence at small m (proved
      below by a clean combinatorial argument: for a fixed "active" subset
      S of size k that ends up in S1 union S2, summing |S1|!|S2|! over all
      2^k ways to split S into an ordered pair (S1,S2) gives exactly
      (k+1)! -- Sum_{i=0}^k C(k,i) i! (k-i)! = Sum_{i=0}^k k! = (k+1)k! =
      (k+1)!, using C(k,i)i!(k-i)! = k! -- so BOTH sums equal
      Sum_k (k+1)! e_k(x_M) identically).

  (b) The "genuinely two-variable" double Laplace integral for
      P_disjoint collapses to a SINGLE integral:

        Sum_{S1,S2 disjoint} |S1|!|S2|! Prod_S1 x Prod_S2 x
          = int_0^inf int_0^inf e^{-lam-mu} Prod_{u in M}(1+(lam+mu)x_u) dlam dmu
          = int_0^inf  s * e^{-s} * Prod_{u in M} (1+x_u*s) ds

      via the standard change of variables s=lam+mu (the "sum of two
      independent unit-rate exponentials is Gamma(2,1)" substitution,
      re-derived here directly rather than cited) -- verified below by
      symbolic double integration AND by the direct change-of-variables
      single integral, both matching the combinatorial sum exactly.

  (c) Hence, combining (a) and (b):

        P_{s,s'}(x) = P_same + P_disjoint = 2 * P_same(s,s')
                    = 2 * x_s * x_s' * int_0^inf s*e^{-s}*Prod_{u in M}(1+x_u*s) ds

      A SINGLE integral, not a double one -- and a computational bonus:
      evaluating P_{s,s'} via the subset-sum form Sum_S(|S|+1)!... costs
      O(2^{K-2}) terms, vs. the naive O(3^{K-2}) the two-variable-sum
      formula for P_disjoint alone would suggest if evaluated directly.
"""
import itertools
import sympy as sp


def direct_sum_same(xs):
    """Sum_{S subseteq M} (|S|+1)! * Prod_{u in S} x_u , brute force."""
    m = len(xs)
    total = sp.Integer(0)
    for r in range(m + 1):
        for S in itertools.combinations(range(m), r):
            term = sp.factorial(len(S) + 1)
            for u in S:
                term *= xs[u]
            total += term
    return sp.together(total)


def direct_sum_disjoint(xs):
    """Sum_{S1,S2 disjoint subseteq M} |S1|!|S2|! Prod_S1 x * Prod_S2 x,
    brute force: every element independently assigned to
    'neither'/'S1'/'S2'."""
    m = len(xs)
    total = sp.Integer(0)
    for assignment in itertools.product([0, 1, 2], repeat=m):
        S1 = [u for u in range(m) if assignment[u] == 1]
        S2 = [u for u in range(m) if assignment[u] == 2]
        term = sp.factorial(len(S1)) * sp.factorial(len(S2))
        for u in S1:
            term *= xs[u]
        for u in S2:
            term *= xs[u]
        total += term
    return sp.together(total)


def laplace_single_integral_same(xs):
    """Sum_S (|S|+1)! Prod x = int_0^inf lam*e^{-lam}*Prod(1+x_u*lam) dlam,
    evaluated symbolically (exact, no floating point)."""
    lam = sp.symbols('lam', positive=True)
    integrand = sp.expand(lam * sp.exp(-lam) * sp.prod([1 + x * lam for x in xs]))
    return sp.together(sp.simplify(sp.integrate(integrand, (lam, 0, sp.oo))))


def laplace_double_integral_disjoint(xs):
    """Sum_{S1,S2 disjoint} |S1|!|S2|! Prod = int int e^{-lam-mu}
    Prod_u(1+(lam+mu)x_u) dlam dmu, evaluated as a genuine DOUBLE integral
    (independent check that it equals the direct combinatorial sum, before
    invoking the change-of-variables collapse)."""
    lam, mu = sp.symbols('lam mu', positive=True)
    integrand = sp.expand(sp.exp(-lam - mu) * sp.prod([1 + (lam + mu) * x for x in xs]))
    inner = sp.simplify(sp.integrate(integrand, (mu, 0, sp.oo)))
    return sp.together(sp.simplify(sp.integrate(inner, (lam, 0, sp.oo))))


def single_integral_via_gamma2_substitution(xs):
    """The collapsed single integral: int_0^inf s*e^{-s}*Prod(1+x_u*s) ds."""
    s = sp.symbols('s', positive=True)
    integrand = sp.expand(s * sp.exp(-s) * sp.prod([1 + x * s for x in xs]))
    return sp.together(sp.integrate(integrand, (s, 0, sp.oo)))


if __name__ == "__main__":
    print("=" * 78)
    print("PART 1: P_same == P_disjoint as pure algebraic sums (identity)?")
    print("=" * 78)
    all_ok = True
    for m in range(0, 5):
        xs = list(sp.symbols(f'x0:{m}', positive=True))
        same_direct = direct_sum_same(xs)
        disj_direct = direct_sum_disjoint(xs)
        identity_holds = sp.simplify(same_direct - disj_direct) == 0
        all_ok = all_ok and identity_holds
        print(f"\n--- m = |M| = {m} ---")
        print(f"  Sum_S (|S|+1)! Prod x            = {same_direct}")
        print(f"  Sum_{{S1,S2 disjoint}} |S1|!|S2|! Prod = {disj_direct}")
        print(f"  IDENTICAL? {identity_holds}")

        single_int = laplace_single_integral_same(xs)
        match_single = sp.simplify(single_int - same_direct) == 0
        all_ok = all_ok and match_single
        print(f"  single integral int s*e^-s*Prod(1+x_u*s) ds = {single_int}  matches P_same sum? {match_single}")

        if m <= 3:
            double_int = laplace_double_integral_disjoint(xs)
            match_double = sp.simplify(double_int - disj_direct) == 0
            all_ok = all_ok and match_double
            print(f"  double integral (genuine 2-D Laplace) = {double_int}  matches P_disjoint sum? {match_double}")
        else:
            single_via_collapse = single_integral_via_gamma2_substitution(xs)
            match_collapse = sp.simplify(single_via_collapse - disj_direct) == 0
            all_ok = all_ok and match_collapse
            print(f"  (double integral skipped at this m for time; collapsed single-integral form")
            print(f"   matches P_disjoint sum directly? {match_collapse})")

    print("\n" + "=" * 78)
    print(f"ALL CHECKS PASSED: {all_ok}")
    print("=" * 78)

    print("\nPART 2: explicit change-of-variables collapse (double -> single),")
    print("independent of PART 1's brute-force anchor, m=0..3:")
    for m in range(0, 4):
        xs = list(sp.symbols(f'y0:{m}', positive=True))
        collapsed = single_integral_via_gamma2_substitution(xs)
        direct = direct_sum_disjoint(xs)
        ok = sp.simplify(collapsed - direct) == 0
        print(f"  m={m}: int s*e^-s*Prod(1+x_u s) ds = {collapsed}   direct disjoint sum = {direct}   match={ok}")

    print("\nPART 3: cross-check against K=3 (M size 1) -- the concrete case")
    print("named in the mandate, tying back to Proposition NN3's own K=3")
    print("derivation (k3_joint_structural_attempt front, PROVED, cited).")
    print("For K=3, M = {the third source}, |M|=1, x_M =: c:")
    c = sp.symbols('c', positive=True)
    xs, xps = sp.symbols('x_s x_sp', positive=True)
    P_same_K3 = direct_sum_same([c])       # = 1 + 2c
    P_disj_K3 = direct_sum_disjoint([c])   # = 1 + 2c  (identical, per PART 1)
    P_ss_K3 = xs * xps * (P_same_K3 + P_disj_K3)
    print(f"  P_same(s,s') [K=3] = x_s x_s' * ({P_same_K3})")
    print(f"  P_disjoint(s,s') [K=3] = x_s x_s' * ({P_disj_K3})  (same, per identity above)")
    print(f"  => P_{{s,s'}}(K=3) = x_s x_s' * (2 + 4c) = {sp.expand(P_ss_K3)}")
    print("  This exact per-(s,s') formula is used (via the full T(L) assembly")
    print("  in symbolic_pnn_via_composition_gf.py) to reproduce Proposition NN3")
    print("  (P_nn(n,3) = (35n^3+38n^2+23n+6)/(140n^3)) exactly -- see that")
    print("  script's own verification output for the end-to-end confirmation.")
