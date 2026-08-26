"""
symbolic_route.py -- a SEPARATE, sympy-based construction of D^{*(p)}_r(b)
with r kept as a symbolic variable, used ONLY to print a few
representative b=2,3 closed forms (the b=0,1 cases are handled by
assemble.py's own pure-Fraction printed_form_b0/b1, which need no sympy at
all since their remainder is provably a polynomial -- Strip vanishes
identically there). NOT used for the main verification sweep (that is
exact fractions.Fraction arithmetic throughout, in assemble.py).

This route re-uses this directory's own already-verified Fraction-based
ingredients (Q_poly's even/odd split, the H_k polynomial table, the
central-moment polynomials) -- converted to sympy expressions -- plus
sympy's own factorial/cancel machinery for the b>=2 strip-sum
denominators (which are NOT polynomial in r in general, unlike b=0,1).
Every printed formula here is cross-validated against assemble.py's exact
Fraction route (Assembler.D_star) at several concrete integer r before
being trusted, exactly as both predecessor fronts cross-validated their
own symbolic and fast routes against each other.
"""

import sympy as sp

from assemble import Assembler, even_odd_split
from ingredients import poly_compose_linear, poly_eval
from odd_part import build_H_table
import ground_truth as gt


def _poly_to_sympy(poly, x):
    expr = sp.Integer(0)
    for n, c in enumerate(poly):
        if c == 0:
            continue
        expr += sp.Rational(c.numerator, c.denominator) * x ** n
    return expr


def D_star_symbolic(p, b):
    """Returns (coef_expr, remainder_expr) in sympy, r a free Symbol, such
    that D^{*(p)}_r(b) = coef_expr * phi_r + remainder_expr (phi_r kept
    OPAQUE/symbolic, exactly matching the archive's convention of
    presenting these closed forms as "coefficient of phi_r" + "remainder",
    not substituting phi_r's own factorial closed form)."""
    r = sp.Symbol('r', positive=True)
    beta = b + 1
    e, o = even_odd_split(p, b)
    H = build_H_table(p, b)

    # M_p(N), N = 2r+b+1, as a sympy expression in r.
    N_expr = 2 * r + b + 1
    Mp = sp.Integer(0)
    from ingredients import central_moment_poly
    for l, el in e.items():
        if el == 0:
            continue
        mu_poly = central_moment_poly(l)
        mu_expr = sum(sp.Rational(c.numerator, c.denominator) * N_expr ** n
                       for n, c in enumerate(mu_poly) if c != 0)
        Mp += sp.Rational(el.numerator, el.denominator) * mu_expr

    # Phi_b(r)/phi_r ratio = prod_{j=1}^b (2r+2j)/(2r+j+1)
    ratio = sp.Integer(1)
    for j in range(1, b + 1):
        ratio *= sp.Rational(1) * (2 * r + 2 * j) / (2 * r + j + 1)
    coef_expr = sp.cancel(ratio * Mp)

    # Strip_p(r,b) = sum_i E_p(i-beta/2) * w_i(r,b), w_i via sympy.factorial
    Strip = sp.Integer(0)
    for i in range(1, b + 1):
        x_val = sp.Rational(i) - sp.Rational(beta, 2)
        Ep_x = sp.Integer(0)
        for l, el in e.items():
            if el == 0:
                continue
            Ep_x += sp.Rational(el.numerator, el.denominator) * x_val ** (2 * l)
        # w_i(r,b) = r!(r+b)!/[(r+i)!(r+b+1-i)!], rewritten as an explicit
        # ratio of PRODUCTS OF LINEAR FACTORS (not sympy.factorial, which
        # sp.cancel/together cannot simplify against a polynomial
        # denominator without extra help) -- valid since 1<=i<=b here:
        #   (r+b)!/(r+i)! = prod_{t=i+1}^{b} (r+t)     (empty=1 if b==i)
        #   r!/(r+b+1-i)! = 1 / prod_{t=1}^{b+1-i} (r+t)
        num = sp.Integer(1)
        for t in range(i + 1, b + 1):
            num *= (r + t)
        den = sp.Integer(1)
        for t in range(1, b + 2 - i):
            den *= (r + t)
        w_i_expr = sp.cancel(num / den)
        Strip += Ep_x * w_i_expr

    H_sum = sp.Integer(0)
    for k in range(1, p + 1):
        ok = o.get(k, None)
        if ok is None or ok == 0:
            continue
        Hk_expr = _poly_to_sympy(H[k], r)
        H_sum += sp.Rational(ok.numerator, ok.denominator) * Hk_expr / sp.Integer(2) ** (2 * k - 1)

    remainder_expr = sp.cancel(sp.Rational(1, 2) * (-Strip) - H_sum)
    return sp.factor(coef_expr), sp.together(remainder_expr)


def cross_validate(p, b, r_values=(0, 3, 7, 15, 40)):
    coef_expr, rem_expr = D_star_symbolic(p, b)
    r = sp.Symbol('r', positive=True)
    asm = Assembler(p, b)
    ok = True
    for rv in r_values:
        coef_val = coef_expr.subs(r, rv)
        rem_val = rem_expr.subs(r, rv)
        phi_val = sp.Rational(gt.phi_r(rv).numerator, gt.phi_r(rv).denominator)
        # NOTE: deliberately NOT using sp.nsimplify here -- the wave-16
        # predecessor front self-caught and disclosed exactly this
        # function silently corrupting an exact large Rational into a
        # spurious irrational-looking expression
        # (general_p_dstar_extension_attempt/ATTEMPT.md Sec 2.4, cited).
        # coef_val, phi_val, rem_val are already exact sympy Rationals by
        # construction (substitution into a Rational-coefficient
        # expression), so their combination needs no "simplification" --
        # only a plain arithmetic sum, exactly as that front's fix did.
        total = coef_val * phi_val + rem_val
        want = asm.D_star(rv)
        want_sp = sp.Rational(want.numerator, want.denominator)
        if sp.simplify(total - want_sp) != 0:
            print(f"SYMBOLIC MISMATCH p={p} b={b} r={rv}: got {total} want {want_sp}")
            ok = False
    return ok


if __name__ == "__main__":
    all_ok = True
    for p in (21, 25):
        for b in (2, 3):
            ok = cross_validate(p, b)
            all_ok = all_ok and ok
            print(f"p={p} b={b}: cross-validate {'OK' if ok else 'FAIL'}")
    print("symbolic_route.py:", "OK" if all_ok else "FAILURES")
