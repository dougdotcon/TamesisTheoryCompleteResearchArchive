"""
Full general-p assembly of D^{*(p)}_r(b) for the extension front, p=11..20,
built from ingredients_ext.py and odd_part_ext.py -- SAME formula as
general_p_dstar_closure_attempt/assemble.py:

  D^{*(p)}_r(b) = (1/2) [ Phi_b(r) * M_p(N) - Strip_p(r,b) ]
                  - sum_{k=1}^{p} o_k * H_{2k-1}(r,b) / 2^{2k-1}

No new mathematics. Two production ingredients are computed via the fast
(cross-validated) routes described in ingredients_ext.py / odd_part_ext.py;
everything else (the even/odd split of Q_p, the strip-sum formula, Phi_b(r))
is unchanged from the closure attempt.

Honest process note (w_i(r,b), the off-by-one class): the closure attempt
self-caught an off-by-one in the strip weight w_i(r,b)'s numerator degree
(i factors used instead of the correct i-1). Per the task's explicit
instruction to be extra careful about this recurring at higher p, the
formula below is written directly in the ALREADY-CORRECTED form (i-1
numerator factors, empty product at i=1) and is additionally verified here
(verify_w_i_correctness, in __main__) against the elementary factorial
identity w_i(r,b) = r!(r+b)!/[(r+i)!(r+b+1-i)!], directly, at a spread of
(r,b,i) -- BEFORE any assembly is trusted, not just at the end. This bug
class is p-independent (w_i does not depend on p at all, only on the strip
index i and b), so there is no reason it would newly reappear here, but it
is checked directly regardless, exactly as the task asked.
"""

import sympy as sp
import math
from fractions import Fraction

import ingredients_ext as ing
import odd_part_ext as op
import ground_truth as gt

r_sym = sp.symbols('r')
v = sp.symbols('v')

_split_cache = {}


def even_odd_split(p, beta_val):
    """Q_p(-(v+beta/2)) = E_p(v) + O_p(v). beta_val must be a concrete
    integer (beta = b+1); the strip sum has a b-dependent number of terms,
    so b must be concrete to assemble a single symbolic-in-r closed form --
    same convention as the closure attempt (and the parent before it)."""
    key = (p, beta_val)
    if key in _split_cache:
        return _split_cache[key]
    Qp_u = ing.Q_p(p)
    u_sym = ing.u
    expr = sp.expand(Qp_u.subs(u_sym, -(v + sp.Rational(beta_val, 2))))
    poly = sp.Poly(expr, v)
    e = {}
    o = {}
    for l in range(0, p + 1):
        e[l] = poly.coeff_monomial(v ** (2 * l)) if 2 * l <= 2 * p else 0
    for k in range(1, p + 1):
        o[k] = poly.coeff_monomial(v ** (2 * k - 1)) if 2 * k - 1 <= 2 * p else 0
    _split_cache[key] = (e, o)
    return e, o


def w_i(i, b_val, r_expr):
    """w_i(r,b) := P_b * C(N,r+i) = r!(r+b)! / [(r+i)!(r+b+1-i)!].
    ALREADY-CORRECTED form (i-1 numerator factors, empty at i=1) -- see the
    module docstring's Honest process note. Verified against the direct
    factorial definition in __main__ before any assembly is trusted."""
    num = sp.Integer(1)
    for t in range(0, i - 1):
        num *= (r_expr + b_val - t)
    den = sp.Integer(1)
    for t in range(1, i + 1):
        den *= (r_expr + t)
    return num / den


def strip_sum(p, b_val, r_expr, e_coeffs):
    beta_val = b_val + 1
    total = sp.Integer(0)
    for i in range(1, b_val + 1):
        vi = sp.Rational(i, 1) - sp.Rational(beta_val, 2)
        Epi = e_coeffs.get(0, 0)
        for l in range(1, p + 1):
            Epi += e_coeffs.get(l, 0) * vi ** (2 * l)
        total += Epi * w_i(i, b_val, r_expr)
    return sp.expand(total)


def D_formula_symbolic_r(p, b_val, r_expr=r_sym, simplify_output=True):
    """Assembled closed form (varphi_coeff, remainder), SYMBOLIC route --
    used for printed representative closed forms and small spot checks,
    NOT for the bulk numeric sweep (see check_against_ground_truth below,
    the fast Fraction route used there)."""
    beta_val = b_val + 1
    N_expr = 2 * r_expr + b_val + 1
    e_coeffs, o_coeffs = even_odd_split(p, beta_val)

    Mp = e_coeffs.get(0, 0) * sp.Integer(1)
    for l in range(1, p + 1):
        el = e_coeffs.get(l, 0)
        if el == 0:
            continue
        mu = ing.central_moment(l)
        Mp += el * mu.subs(ing.N, N_expr)
    Mp = sp.expand(Mp)

    prod_factor = sp.Integer(1)
    for j in range(1, b_val + 1):
        prod_factor *= sp.Rational(2, 1) * (r_expr + j) / (2 * r_expr + j + 1)
    varphi_coeff = sp.expand(sp.Rational(1, 2) * 2 * prod_factor * Mp)

    strip = strip_sum(p, b_val, r_expr, e_coeffs)

    odd_total = sp.Integer(0)
    for k in range(1, p + 1):
        ok = o_coeffs.get(k, 0)
        if ok == 0:
            continue
        Hk_r = op.H_reduced_at_b(2 * k - 1, b_val).subs({op.r_sym: r_expr})
        odd_total += ok * Hk_r / sp.Integer(2) ** (2 * k - 1)

    remainder = sp.expand(-sp.Rational(1, 2) * strip - odd_total)
    if simplify_output:
        varphi_coeff = sp.cancel(varphi_coeff)
        remainder = sp.cancel(remainder)
    return varphi_coeff, remainder


def D_star_predicted(p, r_val, b_val):
    """Honest process note (self-caught bug, distinct from the closure
    attempt's w_i off-by-one): the closure attempt's own D_star_predicted
    ended with `return sp.nsimplify(vc * varphi_r_val + rem)`, copied here
    verbatim at first. vc*varphi_r_val+rem is ALREADY an exact sp.Rational
    once r_val is substituted (sympy auto-combines Rational arithmetic) --
    nsimplify is not merely redundant here, it is actively wrong: for a
    large-numerator/denominator Rational (e.g. p=3,r=15,b=0 gives
    1143904849/80144052), sp.nsimplify's float-based algebraic-constant
    guesser mis-identifies it as an irrational-looking radical expression
    (observed: `3*2**(269/341)*3**(57/682)*5**(290/341)*7**(329/682)/4`)
    rather than recognizing the exact rational it already is. This was
    caught here by exactly the discipline the task asked for -- an
    exhaustive sweep against ground truth failing loudly (2/16 calibration
    spot-checks, both at r=15) -- and never triggered in the closure
    attempt itself only because D_star_predicted was defined there but
    never actually called in its own __main__ (dormant latent bug, not
    previously exercised at any scale). Fix: drop nsimplify entirely; the
    substituted value is already exact."""
    varphi_coeff, remainder = D_formula_symbolic_r(p, b_val, r_expr=r_sym)
    varphi_r_val = sp.Rational(4 ** r_val * math.factorial(r_val) ** 2, math.factorial(2 * r_val + 1))
    vc = varphi_coeff.subs(r_sym, r_val)
    rem = remainder.subs(r_sym, r_val)
    return sp.Rational(vc * varphi_r_val + rem)


def sp_to_fraction(x):
    rx = sp.nsimplify(x, rational=True) if not (x.is_Rational or x.is_Integer) else x
    n, d = sp.fraction(sp.Rational(rx))
    return Fraction(int(n), int(d))


def _eval_fraction_poly(coeffs, xv):
    """coeffs: low-to-high-degree Fraction list; xv: Fraction/int."""
    acc = Fraction(0)
    for c in reversed(coeffs):
        acc = acc * xv + c
    return acc


def check_against_ground_truth(p, rmax, bmax, verbose_fail_limit=20):
    """Pure fractions.Fraction verification against ground_truth.D_star,
    using the FAST Fraction-coefficient-list ingredients directly (no
    sympy round-trip in the hot loop) -- this is what makes p=11..20
    tractable at meaningful scale. Mathematical content identical to
    D_formula_symbolic_r / the closure attempt's own check_against_ground_truth."""
    fails = 0
    total = 0
    fail_examples = []

    fact = [1] * (2 * rmax + 3)
    for i in range(1, len(fact)):
        fact[i] = fact[i - 1] * i
    varphi_frac = {rv: Fraction(4 ** rv * fact[rv] ** 2, fact[2 * rv + 1]) for rv in range(0, rmax + 1)}

    for b_val in range(0, bmax + 1):
        beta_val = b_val + 1
        e_coeffs, o_coeffs = even_odd_split(p, beta_val)
        e_frac = {l: sp_to_fraction(e_coeffs.get(l, 0)) for l in range(0, p + 1)}
        o_frac = {k: sp_to_fraction(o_coeffs.get(k, 0)) for k in range(1, p + 1)}

        H_evals = {}
        for k in range(1, p + 1):
            if o_frac[k] == 0:
                continue
            H_evals[k] = op.H_reduced_at_b_fast_fraction(2 * k - 1, b_val)

        mu_evals = {}
        for l in range(1, p + 1):
            if e_frac[l] == 0:
                continue
            mu_evals[l] = ing.central_moment_fast_fraction(l)

        strip_Ep = []
        for i in range(1, b_val + 1):
            vi = Fraction(2 * i - beta_val, 2)
            Epi = e_frac[0]
            vpow = Fraction(1)
            v2 = vi * vi
            for l in range(1, p + 1):
                vpow *= v2
                Epi += e_frac[l] * vpow
            strip_Ep.append(Epi)

        for r_val in range(0, rmax + 1):
            total += 1
            N_val = 2 * r_val + b_val + 1

            Mp = e_frac[0]
            for l in range(1, p + 1):
                if e_frac[l] == 0:
                    continue
                Mp += e_frac[l] * _eval_fraction_poly(mu_evals[l], N_val)

            prod_factor = Fraction(1)
            for j in range(1, b_val + 1):
                prod_factor *= Fraction(2 * (r_val + j), 2 * r_val + j + 1)
            vc_frac = prod_factor * Mp

            strip_total = Fraction(0)
            num = Fraction(1)
            den = Fraction(1)
            for idx, i in enumerate(range(1, b_val + 1), start=0):
                if i >= 2:
                    num *= (r_val + b_val - (i - 2))
                den *= (r_val + i)
                wi = num / den
                strip_total += strip_Ep[idx] * wi

            odd_total = Fraction(0)
            for k in range(1, p + 1):
                if o_frac[k] == 0:
                    continue
                odd_total += o_frac[k] * _eval_fraction_poly(H_evals[k], r_val) / Fraction(2 ** (2 * k - 1))

            rem_frac = -strip_total / 2 - odd_total
            pred_frac = vc_frac * varphi_frac[r_val] + rem_frac

            truth = gt.D_star(p, r_val, b_val)
            if pred_frac != truth:
                fails += 1
                if len(fail_examples) < verbose_fail_limit:
                    fail_examples.append((p, r_val, b_val, pred_frac, truth))
    return total, fails, fail_examples


def verify_w_i_correctness(rmax=15, bmax=10):
    """Honest process note check: w_i(r,b) against the elementary
    factorial identity, directly, BEFORE trusting any assembly."""
    print("--- verifying w_i(r,b) against direct factorial definition ---")
    fails = 0
    total = 0
    for rv in range(0, rmax + 1):
        for bv in range(0, bmax + 1):
            for i in range(1, bv + 1):
                total += 1
                lhs = w_i(i, bv, sp.Integer(rv))
                rhs = sp.Rational(math.factorial(rv) * math.factorial(rv + bv),
                                   math.factorial(rv + i) * math.factorial(rv + bv + 1 - i))
                if lhs != rhs:
                    fails += 1
                    print(f"MISMATCH r={rv} b={bv} i={i}: w_i={lhs} factorial={rhs}")
    print(f"w_i(r,b) vs factorial identity: {total} checks, fails={fails}")
    return fails


if __name__ == "__main__":
    print("=== assemble_ext.py: general-p closed form for D^{*(p)}_r(b), p=11..20 ===\n")

    fw = verify_w_i_correctness(rmax=15, bmax=10)
    assert fw == 0, "w_i(r,b) FAILED against factorial definition -- STOP"
    print()

    print("--- calibration: reproduce closure attempt's p=1..4 results exactly (sanity gate) ---")
    calib_fails = 0
    # Symbolic reduction to the PROVED b=0,1 formulas was already exhaustively
    # confirmed by the closure attempt for p<=10; here we just confirm THIS
    # (fast-ingredient) implementation reproduces p<=4 exactly against ground
    # truth at a handful of points, as an end-to-end sanity gate on the new
    # fast ingredients before trusting them for p=11..20.
    for p_test in (1, 2, 3, 4):
        for r_val in (0, 3, 7, 15):
            for b_val in (0, 1, 2, 3):
                pred = D_star_predicted(p_test, r_val, b_val)
                truth = gt.D_star(p_test, r_val, b_val)
                if sp.Rational(pred) != sp.Rational(truth.numerator, truth.denominator):
                    calib_fails += 1
                    print(f"CALIBRATION MISMATCH p={p_test} r={r_val} b={b_val}: pred={pred} truth={truth}")
    print(f"calibration spot-checks (p=1..4, fast ingredients, symbolic route): fails={calib_fails}")
    assert calib_fails == 0, "CALIBRATION FAILURE -- fast ingredients disagree with p<=4 -- STOP"

    print()
    print("--- exhaustive checks vs independent ground truth (Corollary A3), p=11..20 ---")
    import time as _time
    total_all = 0
    fails_all = 0
    # Scale: r=0..200, b=0..30 for EVERY p=11..20 -- matching the closure
    # attempt's own referee's scale CEILING (the largest scale reached
    # anywhere in this lineage, previously only for p=5,6) uniformly across
    # all ten new p values. This is possible (not merely "attempted and
    # scaled down") because the fast ingredients (Sec above) make the whole
    # sweep run in seconds-to-tens-of-seconds even at p=20, unlike the
    # closure attempt's own slow routes, which would not have reached this
    # scale even for p=11 in reasonable time (see DERIVATION_PREREG.md).
    scales = {p: (200, 30) for p in range(11, 21)}
    timings = {}
    for p, (rmax, bmax) in scales.items():
        t0 = _time.time()
        total, fails, examples = check_against_ground_truth(p, rmax, bmax)
        t1 = _time.time()
        timings[p] = t1 - t0
        total_all += total
        fails_all += fails
        print(f"p={p}: r=0..{rmax}, b=0..{bmax} -> {total} checks, fails={fails}, time={t1-t0:.2f}s")
        for ex in examples:
            print("   FAIL:", ex)

    print()
    print(f"TOTAL: {total_all} checks, {fails_all} fails, "
          f"total sweep time={sum(timings.values()):.2f}s")

    print()
    print("--- explicit new closed forms, p=11..20, b=0,1 (full list, .log) ---")
    for p in range(11, 21):
        for b_val in (0, 1):
            vc, rem = D_formula_symbolic_r(p, b_val)
            print(f"p={p}, b={b_val}:")
            print(f"   varphi_r coeff = {sp.factor(vc)}")
            print(f"   remainder      = {sp.factor(rem) if rem != 0 else 0}")

    print()
    print("--- explicit new closed forms, p=11,15,20, b=2,3 (denominator-pattern check) ---")
    for p in (11, 15, 20):
        for b_val in (2, 3):
            vc, rem = D_formula_symbolic_r(p, b_val)
            print(f"p={p}, b={b_val}:")
            print(f"   varphi_r coeff = {sp.factor(vc)}")
            print(f"   remainder      = {sp.factor(rem) if rem != 0 else 0}")

    assert fails_all == 0, "ASSEMBLY MISMATCH FOUND"
    print()
    print("ALL ASSEMBLY CHECKS PASSED, p=11..20")
