"""
The H_k(r,b) machine for the extension front (p=11..20): SAME recursion as
general_p_dstar_closure_attempt/odd_part.py (the referee's cited
S_{2k-1}(N,m) recursion, unrolled via identity (E2)), reproduced verbatim
below as H_symbolic()/H_reduced_at_b_slow() for cross-validation -- but
extracted for PRODUCTION use via evaluate-then-interpolate instead of
sympy.cancel, for speed (Honest process note, Sec 0 below). This is exactly
the same kind of performance variant the closure attempt itself already
used (its own H_reduced_at_b substituting b before cancelling, vs
H_reduced's fully symbolic route) -- one step further along the same axis
(substitute r too, at concrete sample points, then interpolate exactly).

(E1), (E2) themselves are unchanged, cited PROVED input (closure attempt
Sec 2.3, itself citing the parent's general-k collapse proposition); not
re-derived again here, since they are unaffected by the extraction-method
change (they are used only inside the SAME H(power,depth) formula, whichever
way that formula is subsequently evaluated).

**Why this is safe, beyond the cross-validation below**: the closure
attempt's own referee (adversarial/REFEREE_REPORT.md Sec 1c) proved, by
induction on depth (decreasing) and then on power, using ONLY (E2) and the
cited S_{2k-1} recursion, that H(power,depth) [as literally defined by the
recursion below] equals P_b*S_power(N-depth,r-depth) for EVERY (power,depth)
-- not just the values checked numerically. That proof is about the
MATHEMATICAL CONTENT of the recursion, independent of how a downstream
script extracts the resulting rational function's polynomial coefficients.
The interpolation route below evaluates that same recursion (character for
character, see Hval() vs the closure attempt's H()) at concrete integer
arguments and recovers the same polynomial via exact interpolation, with a
self-consistency check (extra held-out evaluation points) built into every
call -- so an error in the assumed degree bound is caught immediately, not
silently.
"""

import sympy as sp
import time
from math import comb
from functools import lru_cache
from fractions import Fraction

r_sym, b_sym = sp.symbols('r b')
N_expr = 2 * r_sym + b_sym + 1
beta_expr = b_sym + 1


def falling(x, j):
    out = sp.Integer(1)
    for i in range(j):
        out *= (x - i)
    return out


# ---------------------------------------------------------------------
# SLOW route: verbatim reproduction of the closure attempt's H()/
# H_reduced_at_b (symbolic unrolling + sympy.cancel), kept here ONLY for
# cross-validation against the fast route below, at powers where it is
# still tractable (see DERIVATION_PREREG.md's exploratory timing: this
# route costs 4.5s at power=19, 50s at power=21, 99s at power=25, 171s at
# power=27 -- clearly too slow to reach power=39, the k=20 case needed for
# p=20).
# ---------------------------------------------------------------------

@lru_cache(maxsize=None)
def H_symbolic(power, depth=0):
    beta_local = beta_expr + depth
    lead = beta_local ** (power - 1) * falling(r_sym, depth) / falling(N_expr, depth)
    if power == 1:
        return sp.expand(lead)
    total = lead
    Nd = N_expr - depth
    for s in range(1, power - 1, 2):
        coeff = sp.binomial(power - 1, s)
        total += 2 * Nd * coeff * H_symbolic(s, depth + 1)
    return sp.expand(total)


_H_reduced_slow_cache = {}


def H_reduced_at_b_slow(power, b_val):
    key = (power, b_val)
    if key in _H_reduced_slow_cache:
        return _H_reduced_slow_cache[key]
    raw = H_symbolic(power).subs(b_sym, b_val)
    combined = sp.cancel(sp.together(raw))
    num, den = sp.fraction(combined)
    if sp.expand(den - 1) != 0:
        raise ValueError(f"H_{power}(b={b_val}): did not reduce to a polynomial! den={den}")
    poly = sp.expand(num)
    _H_reduced_slow_cache[key] = poly
    return poly


# ---------------------------------------------------------------------
# FAST route (production, used by assemble_ext.py): the SAME H(power,depth)
# recursion, evaluated at concrete integer (r_val, b_val) via plain
# fractions.Fraction arithmetic (no sympy, no symbolic cancellation needed
# -- with r_val,b_val concrete and chosen large enough that no intermediate
# falling(N,depth) is zero, every term is just a Fraction), then the
# resulting values at deg+1 (plus a few extra, held out for a
# self-consistency check) sample points are combined via EXACT Newton-
# divided-difference interpolation to recover H_k(r,b_val) as a polynomial
# in r. The empirically-observed degree pattern deg_r H_{2k-1}(r,b) = k-1
# (confirmed against the slow route for every power tested below) sets the
# number of sample points; extra held-out points are checked and raise
# immediately on any mismatch, so a wrong degree assumption cannot silently
# produce a wrong "polynomial".
# ---------------------------------------------------------------------

def falling_int(x, j):
    out = 1
    for i in range(j):
        out *= (x - i)
    return out


def make_H_eval(b_val):
    @lru_cache(maxsize=None)
    def Hval(power, depth, r_val):
        N_val = 2 * r_val + b_val + 1
        beta_local = (b_val + 1) + depth
        Nd_fall = falling_int(N_val, depth)
        lead = Fraction(beta_local ** (power - 1) * falling_int(r_val, depth), Nd_fall)
        if power == 1:
            return lead
        total = lead
        Nd = N_val - depth
        s = 1
        while s <= power - 2:
            coeff = comb(power - 1, s)
            total += 2 * Nd * coeff * Hval(s, depth + 1, r_val)
            s += 2
        return total
    return Hval


def _newton_interp_fraction(xs, ys):
    """Exact polynomial interpolation via Newton divided differences.
    Returns coefficient list c[0..d] (c[i] = coeff of x^i), Fraction."""
    n = len(xs)
    table = [list(ys)]
    for level in range(1, n):
        prev = table[-1]
        cur = [(prev[i + 1] - prev[i]) / (xs[i + level] - xs[i]) for i in range(n - level)]
        table.append(cur)
    coeffs_newton = [table[level][0] for level in range(n)]
    poly = [Fraction(0)]
    basis = [Fraction(1)]
    for i in range(n):
        for k in range(len(basis)):
            if k >= len(poly):
                poly.append(Fraction(0))
            poly[k] += coeffs_newton[i] * basis[k]
        newbasis = [Fraction(0)] * (len(basis) + 1)
        for k in range(len(basis)):
            newbasis[k] += -xs[i] * basis[k]
            newbasis[k + 1] += basis[k]
        basis = newbasis
    return poly


_H_fast_cache = {}


def H_reduced_at_b_fast_fraction(power, b_val, extra_check_pts=3):
    """H_k(r,b_val) as an exact Fraction coefficient list (low-to-high
    degree in r). Production route."""
    key = (power, b_val)
    if key in _H_fast_cache:
        return _H_fast_cache[key]
    k = (power + 1) // 2
    deg_guess = k - 1
    Hval = make_H_eval(b_val)
    npts = deg_guess + 1
    offset = power + 10  # keeps every intermediate falling(N,depth) nonzero
    xs = [offset + i for i in range(npts)]
    ys = [Hval(power, 0, x) for x in xs]
    poly = _newton_interp_fraction(xs, ys)
    while len(poly) < npts:
        poly.append(Fraction(0))
    for j in range(extra_check_pts):
        xt = offset + npts + j + 5
        yt = Hval(power, 0, xt)
        acc = Fraction(0)
        for c in reversed(poly):
            acc = acc * xt + c
        if acc != yt:
            raise ValueError(
                f"H_{power}(b={b_val}) interpolation SELF-CHECK FAILED at r={xt}: "
                f"poly={acc} true={yt} (degree_guess={deg_guess} likely wrong)")
    _H_fast_cache[key] = poly
    return poly


def H_reduced_at_b(power, b_val):
    """Public entry point used by assemble_ext.py: exact sympy polynomial
    in r_sym, via the fast route (production)."""
    coeffs = H_reduced_at_b_fast_fraction(power, b_val)
    expr = sp.Integer(0)
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        expr += sp.Rational(c.numerator, c.denominator) * r_sym ** i
    return sp.expand(expr)


# ---------------------------------------------------------------------
# Cross-validation: fast vs slow, and both vs brute force / the closure
# attempt's own printed k=1..4 brackets.
# ---------------------------------------------------------------------

def verify_E2(jmax=10, rmax=15, bmax=10):
    import math as _math
    print("--- verifying (E2): P_b*C(N-j,r-j+1) = [r]_j/([N]_j*(r-j+1)) ---")
    fails = 0
    total = 0
    for rv in range(0, rmax + 1):
        for bv in range(0, bmax + 1):
            Nv = 2 * rv + bv + 1
            Pb = sp.Rational(_math.factorial(rv) * _math.factorial(rv + bv), _math.factorial(Nv))
            for j in range(0, min(jmax, rv + 2) + 1):
                total += 1
                lhs = Pb * sp.binomial(Nv - j, rv - j + 1)
                rj = falling(rv, j)
                Nj = falling(Nv, j)
                denom = Nj * (rv - j + 1)
                if denom == 0:
                    if rj != 0:
                        fails += 1
                    continue
                rhs = sp.Rational(rj, denom)
                if lhs != rhs:
                    fails += 1
                    print(f"MISMATCH r={rv} b={bv} j={j}")
    print(f"(E2) checks: {total}, fails={fails}")
    return fails


def verify_fast_vs_slow(powers=(1, 3, 5, 7, 9, 11, 13, 15, 17, 19), b_vals=(0, 1, 2, 5, 8)):
    print(f"--- fast (interpolation) vs slow (sympy.cancel) H_k, powers up to {max(powers)} ---")
    fails = 0
    total = 0
    for power in powers:
        for bv in b_vals:
            total += 1
            slow_poly = H_reduced_at_b_slow(power, bv)
            slow_coeffs = sp.Poly(slow_poly, r_sym).all_coeffs()[::-1] if slow_poly != 0 else [sp.Integer(0)]
            fast_coeffs_frac = H_reduced_at_b_fast_fraction(power, bv)
            L = max(len(slow_coeffs), len(fast_coeffs_frac))
            slow_frac = []
            for c in slow_coeffs:
                slow_frac.append(Fraction(int(c.p), int(c.q)) if hasattr(c, 'p') else Fraction(int(c)))
            slow_frac += [Fraction(0)] * (L - len(slow_frac))
            fast_frac = list(fast_coeffs_frac) + [Fraction(0)] * (L - len(fast_coeffs_frac))
            if slow_frac != fast_frac:
                fails += 1
                print(f"MISMATCH power={power} b={bv}: slow={slow_frac} fast={fast_frac}")
    print(f"fast-vs-slow H_k cross-check: {total} checks, fails={fails}")
    return fails


def S_bruteforce(power, Nv, m):
    if m < 0:
        return sp.Integer(0)
    total = sp.Integer(0)
    for i in range(0, m + 1):
        total += (Nv - 2 * i) ** power * sp.binomial(Nv, i)
    return total


def verify_H_bruteforce(powers=(1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21), rmax=10, bmax=6):
    print(f"--- verifying (fast route) H_k vs brute-force P_b*S_power(N,r), powers up to {max(powers)} ---")
    import math as _math
    fails = 0
    total = 0
    for power in powers:
        for rv in range(0, rmax + 1):
            for bv in range(0, bmax + 1):
                total += 1
                Nv = 2 * rv + bv + 1
                Pb = sp.Rational(_math.factorial(rv) * _math.factorial(rv + bv), _math.factorial(Nv))
                brute = Pb * S_bruteforce(power, Nv, rv)
                coeffs = H_reduced_at_b_fast_fraction(power, bv)
                pred = Fraction(0)
                for c in reversed(coeffs):
                    pred = pred * rv + c
                brute_frac = Fraction(int(sp.nsimplify(brute).p), int(sp.nsimplify(brute).q))
                if brute_frac != pred:
                    fails += 1
                    print(f"MISMATCH power={power} r={rv} b={bv}: brute={brute_frac} pred={pred}")
    print(f"brute-force checks: {total}, fails={fails}")
    return fails


def verify_H_matches_parent_printed():
    print("--- cross-check vs closure-attempt-printed k=1,2,3,4 brackets (character-for-character) ---")
    beta = beta_expr
    parent = {
        1: sp.Rational(-1, 2),
        3: sp.Rational(-1, 8) * (beta ** 2 + 4 * r_sym),
        5: sp.Rational(-1, 32) * (beta ** 4 + 8 * r_sym * ((beta + 1) ** 2 + 1) + 32 * r_sym * (r_sym - 1)),
        7: sp.Rational(-1, 128) * (beta ** 6 + r_sym * (12 * (beta + 1) ** 4 + 40 * (beta + 1) ** 2 + 12)
                                    + r_sym * (r_sym - 1) * (96 * (beta + 2) ** 2 + 256)
                                    + 384 * r_sym * (r_sym - 1) * (r_sym - 2)),
    }
    fails = 0
    for k2m1, expr in parent.items():
        # For this bracket comparison we need H_k(r,b) fully symbolic in b,
        # not at a fixed b value -- use the slow symbolic route here (cheap
        # at these small powers) rather than the fast (b-concrete) route.
        mine = sp.expand(-H_symbolic(k2m1) / sp.Integer(2) ** k2m1)
        diff = sp.simplify(mine - expr)
        ok = (diff == 0)
        print(f"power={k2m1}: matches printed bracket exactly: {ok}")
        if not ok:
            fails += 1
            print("  residual:", diff)
    return fails


if __name__ == "__main__":
    f0 = verify_E2(jmax=12, rmax=15, bmax=10)
    f1 = verify_fast_vs_slow(powers=(1, 3, 5, 7, 9, 11, 13, 15, 17, 19), b_vals=(0, 1, 2, 5, 8))
    f2 = verify_H_bruteforce(powers=(1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21), rmax=10, bmax=6)
    f3 = verify_H_matches_parent_printed()

    print()
    print("--- fast-route timing, power up to 39 (k=20, needed for p=20), b=1 ---")
    t0 = time.time()
    for power in range(1, 40, 2):
        ta = time.time()
        poly = H_reduced_at_b_fast_fraction(power, 1)
        tb = time.time()
        print(f"  power={power} (k={(power+1)//2}): {tb-ta:.4f}s degree={len(poly)-1}")
    print(f"total fast-route H(1..39, b=1) time: {time.time()-t0:.3f}s")

    print()
    print("=== odd_part_ext.py summary ===")
    print(f"(E2): fails={f0}")
    print(f"fast vs slow H_k (power up to 19): fails={f1}")
    print(f"fast H_k vs brute force (power up to 21): fails={f2}")
    print(f"fast H_k vs closure-attempt-printed k=1..4 brackets: fails={f3}")
    total_fails = f0 + f1 + f2 + f3
    assert total_fails == 0, "ODD-PART FAILURE"
    print(f"ALL ODD-PART CHECKS PASSED (total fails={total_fails})")
