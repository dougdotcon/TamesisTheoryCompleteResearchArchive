"""
Task item 2: push the integral representation through the FULL composition
sum. This script builds the "outer" generating-function machinery: an
exact closed-form (in n, and where possible in K) for sums, over the
ENTIRE composition simplex {L_0,...,L_{K-1} >= 1, sum L_i <= n}, of a
fixed "touched-index" monomial pattern -- the natural generating-function
analogue, for the OUTER L-sum, of double_integral_p_disjoint.py's Laplace
transform for the INNER subset sum.

Written fresh from first principles (ordinary generating functions /
stars-and-bars); no file from any front read.

Key building block, derived and verified below:
  For r DISTINCT indices each carrying weight L (power 1), and the
  remaining K-r source-indices "present but untouched" (each ranges freely
  over L>=1, weight 1), and O (>=0, weight 1):

    mu_r(n,K) := sum over the whole composition simplex of
                 L_{i_1} * L_{i_2} * ... * L_{i_r}   (r distinct indices)

  equals, via the ordinary generating function
    prod_{touched}  (t/(1-t)^2)   *  prod_{untouched} (t/(1-t))  *  1/(1-t)
      = t^K / (1-t)^{K+r+1}
  and  [t^n] t^K/(1-t)^D = C(n-K+D-1, D-1):

    mu_r(n,K) = C(n+r, K+r)                      (exact, all n,K,r)

This is the single-variable-power (r indices each to the power 1) case.
The heavier terms inside T(L) (same-arc, outside-arc, cross-arc) need one
or two SPECIAL indices raised to power 2 or 3 (e.g. L_s*(L_s-1) or
L_s*(L_s-1)*(L_s-2)), handled below by a fully general moment function
built from the same GF idea (Eulerian-polynomial generating functions for
higher powers), not hand-derived case by case.
"""
import sympy as sp
from functools import lru_cache

t = sp.symbols('t')


@lru_cache(maxsize=None)
def g_power(a):
    """Sum_{L=1}^infty L^a * t^L, as an exact sympy rational function of t.
    Built by repeated application of the operator (t d/dt) to 1/(1-t),
    the standard way to generate L^a t^L term by term."""
    expr = 1 / (1 - t)
    for _ in range(a):
        expr = sp.together(t * sp.diff(expr, t))
    return sp.together(expr)


def source_gf(power):
    """GF for one source index L_i>=1, raised to `power` (power=0 means
    'present but untouched': weight 1)."""
    if power == 0:
        return sp.together(t / (1 - t))
    return g_power(power)


def outside_gf(power):
    """GF for the O index, O>=0, raised to `power`."""
    if power == 0:
        return sp.together(1 / (1 - t))
    return g_power(power)


def extract_coeff_n(rational_gf, n_sym):
    """Given a rational function N(t)/(1-t)^D, return [t^n] as an exact
    expression in n_sym (valid for all n in the regime this front uses --
    every source has L>=1, and n is always queried well past that point)."""
    num, den = sp.fraction(sp.together(rational_gf))
    num = sp.expand(num)
    D = sp.degree(den, t)
    assert sp.expand(den - (1 - t) ** D) == 0, f"denominator not (1-t)^{D}: {den}"
    poly = sp.Poly(num, t)
    result = sp.Integer(0)
    for (j,), c in poly.terms():
        result += c * sp.binomial(n_sym - j + D - 1, D - 1)
    return sp.expand(result)


def composition_moment_symbolic(n_sym, K, touched_powers, O_power=0):
    """touched_powers: dict {index: power>=1} for a set of DISTINCT
    indices. K: total number of source indices (touched + untouched = K).
    Returns sum_{compositions} Prod_i L_i^{power_i} * O^{O_power}, exact,
    symbolic in n_sym."""
    r = len(touched_powers)
    gf = sp.Integer(1)
    for p in touched_powers.values():
        gf *= source_gf(p)
    gf *= source_gf(0) ** (K - r)
    gf *= outside_gf(O_power)
    return extract_coeff_n(sp.together(gf), n_sym)


if __name__ == "__main__":
    print("=" * 78)
    print("Verify mu_r(n,K) = C(n+r,K+r) via the GF machinery, several (K,r,n)")
    print("=" * 78)
    n_sym = sp.symbols('n')
    all_ok = True
    for K in range(1, 6):
        for r in range(0, K + 1):
            touched = {i: 1 for i in range(r)}
            val = composition_moment_symbolic(n_sym, K, touched, O_power=0)
            expected = sp.binomial(n_sym + r, K + r)
            diff = sp.simplify(sp.expand(val) - sp.expand(expected))
            ok = (diff == 0)
            all_ok = all_ok and ok
            if not ok:
                print(f"  MISMATCH K={K} r={r}: got {val}, expected {expected}, diff={diff}")
    print(f"All mu_r == C(n+r,K+r) checks passed: {all_ok}")

    print()
    print("=" * 78)
    print("Cross-check composition_moment_symbolic against DIRECT enumeration")
    print("(concrete small n,K, general powers including power 2 and power 3)")
    print("=" * 78)

    def direct_moment(n, K, touched_powers, O_power=0):
        total_local = [0]

        def rec(idx, remaining, chosen):
            if idx == K:
                O = remaining
                val = O ** O_power
                for i, p in touched_powers.items():
                    val *= chosen[i] ** p
                total_local[0] += val
                return
            hi = remaining - (K - idx - 1)
            for v in range(1, hi + 1):
                chosen[idx] = v
                rec(idx + 1, remaining - v, chosen)

        rec(0, n, {})
        return total_local[0]

    test_cases = [
        (7, 3, {0: 1}, 0), (7, 3, {0: 2}, 0),
        (8, 4, {0: 1, 1: 1}, 0), (8, 4, {0: 2, 1: 1}, 0),
        (9, 4, {0: 3}, 0), (9, 4, {}, 1), (9, 4, {}, 2),
        (10, 5, {0: 2}, 1), (10, 5, {0: 1, 1: 1, 2: 1}, 0),
    ]
    all_ok2 = True
    for (n, K, touched, Op) in test_cases:
        gf_val = composition_moment_symbolic(sp.Integer(n), K, touched, Op)
        dv = direct_moment(n, K, touched, Op)
        ok = (int(gf_val) == dv)
        all_ok2 = all_ok2 and ok
        print(f"  n={n},K={K},touched={touched},O_power={Op}: GF={gf_val}  direct={dv}  match={ok}")
    print(f"All direct-enumeration cross-checks passed: {all_ok2}")
    print()
    print(f"OVERALL: {all_ok and all_ok2}")
