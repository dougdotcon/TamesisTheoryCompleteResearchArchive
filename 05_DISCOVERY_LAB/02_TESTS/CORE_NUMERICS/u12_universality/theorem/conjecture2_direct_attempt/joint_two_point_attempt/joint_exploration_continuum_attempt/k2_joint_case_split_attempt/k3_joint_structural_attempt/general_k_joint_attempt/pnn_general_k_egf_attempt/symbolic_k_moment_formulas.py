"""
Task item 3a: attempt the derivation symbolically for GENERAL K (K itself a
free sympy symbol). This pushes the moment/GF machinery of
gf_moment_machinery.py / symbolic_pnn_via_composition_gf.py one level
further -- deriving an EXPLICIT closed-form-in-(n,K,r) formula for each
moment type needed by T(L)'s four pieces (rather than a formula that only
exists for concrete K), which is the prerequisite for even attempting to
sum over r with K left symbolic (done in attempt_k_uniform_closure.py).

Written fresh, building on the (already numerically-verified) GF logic of
gf_moment_machinery.py; no file from any front read.

Derivation (worked out here, then implemented and cross-checked below):

  For ONE special index carrying power a (a=0,1,2,3), r OTHER indices
  carrying power 1, K-1-r "fully untouched" sources, and O carrying power b:

    G_a(t) := Sum_{L>=1} L^a t^L = t*E_a(t)/(1-t)^{a+1}   (a>=1; E_1=1)
    G_0(t) := t/(1-t)                                      ("untouched": E_0=1)
    H_b(t) := G_b(t)  (b>=1)   or   1/(1-t)  (b=0)

  Multiplying G_a(t) * G_1(t)^r * G_0(t)^{K-1-r} * H_b(t) and collecting
  powers of t and (1-t) (worked out by hand, verified numerically below):

    b=0:  GF = t^K * E_a(t) / (1-t)^{a+K+r+1}
          moment(a,r,b=0) = Sum_j [t^j] E_a(t)  *  C(n+a+r-j, a+K+r)

    b>=1: GF = t^{K+1} * E_a(t)*E_b(t) / (1-t)^{a+b+K+r+1}
          moment(a,r,b>=1) = Sum_j [t^j] E_a(t)E_b(t)  *  C(n+a+b+r-1-j, a+b+K+r)

  and, with TWO special indices (a0,a1) instead of one (needed for the
  cross-arc piece), b=0:

    GF = t^K * E_{a0}(t)*E_{a1}(t) / (1-t)^{a0+a1+K+r+1}
    moment(a0,a1,r,b=0) = Sum_j [t^j] E_{a0}E_{a1}  *  C(n+a0+a1+r-j, a0+a1+K+r)

Crucially: the binomial coefficients above are C(linear-in(n,K,r), linear-
in(K,r)) -- symbolic in K AND r simultaneously, unlike gf_moment_machinery
.py's extract_coeff_n (which needs a CONCRETE polynomial degree D, hence a
concrete K). This is the genuine "push K itself symbolic" step.
"""
import sympy as sp
from functools import lru_cache

t, n, K, r = sp.symbols('t n K r', positive=True)


@lru_cache(maxsize=None)
def eulerian_poly(a):
    """E_a(t) such that Sum_{L>=1} L^a t^L = t*E_a(t)/(1-t)^{a+1} for a>=1,
    with E_0(t):=1 (matching G_0(t)=t/(1-t)). Computed by dividing out the
    known t/(1-t)^{a+1} factor from the differentiation-built g_power(a)."""
    if a == 0:
        return sp.Integer(1)
    tt = sp.symbols('tt')
    expr = 1 / (1 - tt)
    for _ in range(a):
        expr = sp.together(tt * sp.diff(expr, tt))
    num, den = sp.fraction(sp.together(expr))
    assert sp.expand(den - (1 - tt) ** (a + 1)) == 0
    Ea_tt = sp.expand(sp.cancel(num / tt))
    return sp.Poly(Ea_tt, tt).as_expr().subs(tt, t)


def moment_formula_one_special(a, b):
    """Returns a symbolic expression in n,K,r for moment(a, r, b): one
    special index power a, r plain-touched, O power b."""
    if b == 0:
        poly = sp.Poly(sp.expand(eulerian_poly(a)), t)
        D_extra = a + K + r
    else:
        P = sp.expand(eulerian_poly(a) * eulerian_poly(b))
        poly = sp.Poly(P, t)
        D_extra = a + b + K + r
    expr = sp.Integer(0)
    for (j,), c in poly.terms():
        top = (n + a + r - j) if b == 0 else (n + a + b + r - 1 - j)
        expr += c * sp.binomial(top, D_extra)
    return sp.expand(expr)


def moment_formula_two_special(a0, a1):
    """Two special indices (a0,a1), r plain-touched, O power 0 (the only
    O_power this document's pieces need with two special indices)."""
    P = sp.expand(eulerian_poly(a0) * eulerian_poly(a1))
    poly = sp.Poly(P, t)
    D_extra = a0 + a1 + K + r
    expr = sp.Integer(0)
    for (j,), c in poly.terms():
        top = n + a0 + a1 + r - j
        expr += c * sp.binomial(top, D_extra)
    return sp.expand(expr)


if __name__ == "__main__":
    from gf_moment_machinery import composition_moment_symbolic

    print("=" * 78)
    print("Verify symbolic-in-(n,K,r) moment formulas against")
    print("gf_moment_machinery.py's (already brute-force-validated) numeric")
    print("moment function, at concrete (K,r,a,b)")
    print("=" * 78)
    all_ok = True
    n_sym = sp.symbols('n')
    test_cases = [
        (5, 2, 1, 0), (5, 2, 2, 0), (5, 2, 3, 0),
        (6, 0, 1, 1), (6, 3, 2, 1), (6, 1, 1, 2),
        (7, 4, 1, 0), (4, 0, 3, 0),
    ]
    for (Kval, rval, a, b) in test_cases:
        formula = moment_formula_one_special(a, b)
        val = sp.expand(formula.subs({K: Kval, r: rval}))
        touched = {0: a}
        for j in range(1, rval + 1):
            touched[j] = 1
        direct = composition_moment_symbolic(n_sym, Kval, touched, O_power=b)
        diff = sp.simplify(val.subs(n, n_sym) - direct)
        ok = (diff == 0)
        all_ok = all_ok and ok
        print(f"  K={Kval},r={rval},a={a},b={b}: match={ok}" + ("" if ok else f"  diff={diff}"))

    test_cases2 = [(5, 1, 2, 1), (6, 2, 2, 2), (7, 0, 1, 2)]
    for (Kval, rval, a0, a1) in test_cases2:
        formula = moment_formula_two_special(a0, a1)
        val = sp.expand(formula.subs({K: Kval, r: rval}))
        touched = {0: a0, 1: a1}
        for j in range(2, 2 + rval):
            touched[j] = 1
        direct = composition_moment_symbolic(n_sym, Kval, touched, O_power=0)
        diff = sp.simplify(val.subs(n, n_sym) - direct)
        ok = (diff == 0)
        all_ok = all_ok and ok
        print(f"  [two-special] K={Kval},r={rval},a0={a0},a1={a1}: match={ok}" + ("" if ok else f"  diff={diff}"))

    print(f"\nALL symbolic-(n,K,r) moment formulas verified: {all_ok}")
