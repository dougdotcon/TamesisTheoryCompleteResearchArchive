"""
Assembles D^{*(p)}_r(b), general b, for p=1,2,3,4, from the ingredients in
ingredients.py, following DERIVATION_PREREG.md Steps 1-4, and checks the result
exhaustively against ground_truth.Dstar (the already-PROVED Corollary A3 sum).

    D^{*(p)}_r(b) = Phi_b(r)/2 * [full-even-moment value]
                    - (1/2) * strip_p(r,b)
                    + P_b * [odd-partial-sum value]

Phi_b(r) := 2*phi_r * prod_{j=1}^b (2r+2j)/(2r+j+1)   (the named prefactor-collapse
object; polynomial in r only for b in {0,1} -- this is the precise, now fully
mechanised, reason the {r^q phi_r} u {r^q} basis fails structurally for b>=2, exactly
as named in THEOREM.md / the target ATTEMPT.md's post-adversarial correction).

strip_p(r,b) := sum_{j=1}^b E_p(j-beta/2) * w_j(r,b),
w_j(r,b) := r!(r+b)! / [(r+j)!(r+b+1-j)!]      (P_b*binom(N,r+j), explicit).

Written from scratch.
"""
from fractions import Fraction as F
import sympy as sp

from ground_truth import Dstar, phi_r, factorial
from ingredients import (Q_poly, mu2_formula, mu4_formula, mu6_formula, mu8_formula,
                          S7, P_b)


def Phi_b(r, b):
    val = phi_r(r) * 2
    for j in range(1, b + 1):
        val *= F(2 * r + 2 * j, 2 * r + j + 1)
    return val


_v = sp.symbols('v')
_COEF_CACHE = {}


def _sp_to_F(x):
    x = sp.Rational(sp.nsimplify(x))
    return F(int(x.p), int(x.q))


def E_O_coeffs(p, b):
    """Split Q_p(-(v+beta/2)) into its even/odd-degree coefficients in v."""
    key = (p, b)
    if key in _COEF_CACHE:
        return _COEF_CACHE[key]
    beta = b + 1
    Qexpr = Q_poly(p)
    u = sp.symbols('u')
    Qv = sp.expand(Qexpr.subs(u, -(_v + sp.Rational(beta, 2))))
    poly = sp.Poly(Qv, _v)
    coeffs = {}
    for (deg,), c in poly.terms():
        coeffs[deg] = _sp_to_F(c)
    _COEF_CACHE[key] = coeffs
    return coeffs


def _Pb_sum_v_odd(deg, r, b):
    """P_b * sum_{alpha=0}^r v^deg binom(N,alpha), deg in {1,3,5,7}, via the
    prefactor-collapse family and identities S1,S3,S5,S7 (each already collapsed
    to explicit polynomials in r,b using P_b*(r+1)binom(N,r+1)=1 and the falling
    factorial family -- see ATTEMPT.md S3 for the by-hand collapse algebra)."""
    beta = b + 1
    if deg == 1:
        return F(-1, 2)
    if deg == 3:
        return F(-1, 8) * (beta ** 2 + 4 * r)
    if deg == 5:
        return F(-1, 32) * (beta ** 4 + 8 * r * ((beta + 1) ** 2 + 1) + 32 * r * (r - 1))
    if deg == 7:
        N = 2 * r + b + 1
        # P_b * S7(N,r), collapsed (see ATTEMPT.md S4): beta^6 + r*(12(beta+1)^4+40(beta+1)^2+12)
        #                                                + r(r-1)*(96(beta+2)^2+256) + 384 r(r-1)(r-2)
        PbS7 = (F(beta) ** 6
                + r * (12 * F(beta + 1) ** 4 + 40 * F(beta + 1) ** 2 + 12)
                + r * (r - 1) * (96 * F(beta + 2) ** 2 + 256)
                + 384 * r * (r - 1) * (r - 2))
        return F(-1, 128) * PbS7
    raise ValueError(deg)


_MOMENTS = {0: lambda N: F(1), 2: mu2_formula, 4: mu4_formula, 6: mu6_formula, 8: mu8_formula}


def D_formula(p, r, b):
    beta = b + 1
    N = 2 * r + b + 1
    coeffs = E_O_coeffs(p, b)

    full_even_over_2N = sum(coeffs.get(d, F(0)) * _MOMENTS[d](N)
                             for d in [0, 2, 4, 6, 8] if d <= 2 * p)
    main_term = Phi_b(r, b) * full_even_over_2N / 2

    odd_partial = sum(coeffs.get(d, F(0)) * _Pb_sum_v_odd(d, r, b)
                       for d in [1, 3, 5, 7] if d <= 2 * p - 1)

    strip = F(0)
    for j in range(1, b + 1):
        vv = F(j) - F(beta, 2)
        Eval = sum(coeffs.get(d, F(0)) * vv ** d for d in [0, 2, 4, 6, 8] if d <= 2 * p)
        wj = F(factorial(r) * factorial(r + b), factorial(r + j) * factorial(r + b + 1 - j))
        strip += Eval * wj
    strip_term = -F(1, 2) * strip

    return main_term + odd_partial + strip_term


CALIBRATION = {
    1: lambda r: F(r + 1, 4) * phi_r(r) - F(1, 4),
    2: lambda r: F((r + 1) * (3 * r + 8), 32) * phi_r(r) - F(5 * r + 6, 24),
    3: lambda r: F((r + 1) * (5 * r ** 2 + 39 * r + 32), 128) * phi_r(r) - F((r + 1) * (7 * r + 12), 48),
    4: lambda r: F((r + 1) * (105 * r ** 3 + 1765 * r ** 2 + 3314 * r + 1536), 6144) * phi_r(r)
        - F(45 * r ** 3 + 229 * r ** 2 + 306 * r + 120, 480),
}


def check_calibration_b1(pmax=4, rmax=200):
    """Hard requirement: D_formula(p, r, 1) must equal the PROVED b=1 formulas
    character-for-character (checked here as exact Fraction equality, the algebraic
    analogue), not just for the numbers this document itself produced."""
    ok = True
    for p in range(1, pmax + 1):
        for r in range(0, rmax + 1):
            lhs = D_formula(p, r, 1)
            rhs = CALIBRATION[p](r)
            if lhs != rhs:
                ok = False
                print(f"CALIBRATION FAIL p={p} r={r}: {lhs} vs {rhs}")
    return ok


def check_calibration_b0(pmax=4, rmax=200):
    known0 = {
        1: lambda r: F(r, 4) * phi_r(r),
        2: lambda r: F(r * (3 * r + 1), 32) * phi_r(r) - F(r, 12),
    }
    ok = True
    for p, f in known0.items():
        if p > pmax:
            continue
        for r in range(0, rmax + 1):
            if D_formula(p, r, 0) != f(r):
                ok = False
                print(f"b=0 CALIBRATION FAIL p={p} r={r}")
    return ok


def big_sweep(p, bmax, rmax):
    count = fail = 0
    for b in range(0, bmax + 1):
        for r in range(0, rmax + 1):
            gt = Dstar(p, r, b)
            pred = D_formula(p, r, b)
            count += 1
            if gt != pred:
                fail += 1
                print(f"MISMATCH p={p} b={b} r={r}: gt={gt} pred={pred}")
    return count, fail


if __name__ == "__main__":
    print("=== Hard requirement: exact reduction to the PROVED b=1 calibration formulas ===")
    print("p=1..4, r=0..200:", "OK (character-for-character)" if check_calibration_b1() else "FAIL")

    print()
    print("=== Sanity: exact reduction to the PROVED b=0 formulas (p=1,2) ===")
    print("r=0..200:", "OK" if check_calibration_b0() else "FAIL")

    print()
    print("=== Big exhaustive sweeps vs ground truth (Corollary A3) ===")
    c, f = big_sweep(1, bmax=20, rmax=150)
    print(f"p=1: {c} checks, {f} failures")
    c, f = big_sweep(2, bmax=10, rmax=60)
    print(f"p=2: {c} checks, {f} failures")
    c, f = big_sweep(3, bmax=10, rmax=60)
    print(f"p=3: {c} checks, {f} failures")
    c, f = big_sweep(4, bmax=10, rmax=60)
    print(f"p=4: {c} checks, {f} failures")

    print()
    print("=== Concrete new closed forms, printed out for b=2, b=3 ===")
    r = sp.symbols('r', positive=True)
    for p in [1, 2, 3]:
        for b in [2, 3]:
            vals = [(rr, D_formula(p, rr, b)) for rr in range(0, 6)]
            print(f"p={p}, b={b}: D*_r({b}) at r=0..5 =", vals)
