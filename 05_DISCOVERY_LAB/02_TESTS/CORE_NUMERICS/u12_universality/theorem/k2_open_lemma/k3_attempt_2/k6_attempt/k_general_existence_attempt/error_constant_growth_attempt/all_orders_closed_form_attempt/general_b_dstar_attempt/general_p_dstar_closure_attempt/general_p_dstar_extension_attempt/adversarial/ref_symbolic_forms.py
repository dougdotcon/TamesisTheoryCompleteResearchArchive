# Hostile-referee check 5 (extension front): SYMBOLIC reconstruction of every
# printed closed form, from this referee's own ingredients, plus verification of
# the claimed structural signature:
#   b in {0,1}: varphi_r-coefficient polynomial (no (2r+3) denominator),
#               remainder a genuine polynomial;
#   b in {2,3}: varphi_r-coefficient denominator exactly const*(2r+3),
#               remainder denominator const*(r+1) at b=2, const*(r+1)(r+2) at b=3.
#
# Reconstruction route (all referee-own):
#   varphi-coeff(r) = M_p(N)|_{N=2r+b+1} * prod_{j=1}^{b} (2r+2j)/(2r+j+1)
#     [uses (E1): Phi_b(r) = P_b 2^N = 2 varphi_r prod_j (2r+2j)/(2r+j+1); (E1) is
#      cited PROVED upstream but ALSO re-verified numerically here, r,b <= 20]
#   remainder(r)   = -(1/2) sum_{i=1}^b E_p(i - beta/2) w_i(r,b)
#                    - sum_{k=1}^p o_k H_{2k-1}(r,b) / 2^{2k-1}
#     with w_i(r,b) = prod_{t=0}^{i-2}(r+b-t) / prod_{t=1}^{i}(r+t)  (factorial def)
#     and H_{2k-1}(r,b) = A_k(2r+b+1, r)/(r+1)   (referee's ref_hk.py route).
# Then sympy.cancel(mine - printed) must be 0 for every one of the 26 printed forms.
# Exact arithmetic only. No randomness. No sp.nsimplify anywhere.

from fractions import Fraction
from math import factorial
import os
import sys
import time

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_assembly_sweep as ras
import ref_moments
from ref_printed_forms import parse_log_forms, rsym


def frac2sp(fr):
    return sp.Rational(fr.numerator, fr.denominator)


def verify_E1():
    """(E1): P_b 2^N == 2 varphi_r prod_{j=1}^b (2r+2j)/(2r+j+1), numerically."""
    fails = checks = 0
    for r in range(0, 21):
        phi = Fraction(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))
        for b in range(0, 21):
            N = 2 * r + b + 1
            lhs = Fraction(factorial(r) * factorial(r + b) * 2 ** N, factorial(N))
            prod = Fraction(1)
            for j in range(1, b + 1):
                prod *= Fraction(2 * r + 2 * j, 2 * r + j + 1)
            checks += 1
            if lhs != 2 * phi * prod:
                fails += 1
                print("E1 FAIL", r, b)
    print(f"(E1) numeric re-verification, r,b=0..20: {checks} checks, fails={fails}")
    assert fails == 0


def build_symbolic(p, b):
    asm = ras.Assembly(p, b)
    beta = b + 1
    # M_p(N) at N = 2r+b+1, symbolic in r
    Nexpr = 2 * rsym + b + 1
    M = frac2sp(asm.e_even[0])
    for l in range(1, p + 1):
        e = asm.e_even[l]
        if e == 0:
            continue
        mu = ref_moments  # mu poly in N
        mupoly = sum(frac2sp(cf) * Nexpr ** i for i, cf in enumerate(ras.MUS[l]))
        M += frac2sp(e) * mupoly
    prod = sp.Integer(1)
    for j in range(1, b + 1):
        prod *= sp.Rational(1) * (2 * rsym + 2 * j) / (2 * rsym + j + 1)
    coeff = sp.cancel(sp.expand(M) * prod)

    rem = sp.Integer(0)
    for i in range(1, b + 1):
        Ei = frac2sp(asm.E_at(i - Fraction(beta, 2)))
        num = sp.Integer(1)
        for t in range(0, i - 1):
            num *= (rsym + b - t)
        den = sp.Integer(1)
        for t in range(1, i + 1):
            den *= (rsym + t)
        rem += Ei * num / den
    rem = -rem / 2
    for k in range(1, p + 1):
        o = asm.o_odd[k - 1]
        if o == 0:
            continue
        Ak = sum(c * Nexpr ** iN * rsym ** im for (iN, im), c in ras.ADICTS[k].items())
        Hk = sp.cancel(sp.expand(Ak) / (rsym + 1))
        rem -= frac2sp(o) * Hk / 2 ** (2 * k - 1)
    rem = sp.cancel(rem)
    return coeff, rem


def denom_structure(expr):
    """factored denominator of a cancelled rational function in r"""
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    return sp.factor(den)


def main():
    verify_E1()
    forms = parse_log_forms()
    n_ok = 0
    for (p, b) in sorted(forms):
        t0 = time.time()
        cexpr_log, rexpr_log = forms[(p, b)]
        cmine, rmine = build_symbolic(p, b)
        dc = sp.cancel(sp.together(cmine - cexpr_log))
        dr = sp.cancel(sp.together(rmine - rexpr_log))
        ok = (dc == 0) and (dr == 0)
        print(f"p={p:2d} b={b}: symbolic reconstruction == printed form: "
              f"{'OK' if ok else 'FAIL  dc=%s dr=%s' % (dc, dr)}  "
              f"({time.time()-t0:.1f}s)")
        assert ok
        n_ok += 1

        # denominator-pattern verification (on the printed = reconstructed forms)
        den_c = denom_structure(cexpr_log)
        den_r = denom_structure(rexpr_log)
        if b in (0, 1):
            assert den_c.is_Integer, (p, b, den_c)
            assert den_r.is_Integer, (p, b, den_r)  # genuine polynomial remainder
        elif b == 2:
            q, rr = sp.div(sp.Poly(den_c, rsym), sp.Poly(2 * rsym + 3, rsym))
            assert rr.is_zero and q.degree() == 0, (p, b, den_c)
            q, rr = sp.div(sp.Poly(den_r, rsym), sp.Poly(rsym + 1, rsym))
            assert rr.is_zero and q.degree() == 0, (p, b, den_r)
        elif b == 3:
            q, rr = sp.div(sp.Poly(den_c, rsym), sp.Poly(2 * rsym + 3, rsym))
            assert rr.is_zero and q.degree() == 0, (p, b, den_c)
            q, rr = sp.div(sp.Poly(den_r, rsym),
                           sp.Poly((rsym + 1) * (rsym + 2), rsym))
            assert rr.is_zero and q.degree() == 0, (p, b, den_r)
    print(f"symbolic reconstruction + denominator signature: {n_ok}/26 forms OK")
    print("  b=0,1: polynomial remainder, no (2r+3) in varphi-coefficient: CONFIRMED")
    print("  b=2:   varphi-coeff denom = const*(2r+3), remainder denom = const*(r+1): CONFIRMED")
    print("  b=3:   varphi-coeff denom = const*(2r+3), remainder denom = const*(r+1)(r+2): CONFIRMED")
    print("ALL SYMBOLIC-FORM CHECKS PASSED")


if __name__ == "__main__":
    main()
