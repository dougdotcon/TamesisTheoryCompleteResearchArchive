"""
Full independent assembly of D^{*(p)}_r(b), p=1,2,3,4, general b, built from
scratch out of the pieces verified in full_rederivation.py / abel_identities.py
/ collapse_proposition.py, and checked exhaustively against own_ground_truth's
D_star (independent Corollary A3 implementation).

    D^{*(p)}_r(b) = P_b/2 * [ FullEvenSum(N,beta) - StripEvenSum(r,b) ]
                    + OddSumTotal(r,b)

  FullEvenSum(N,beta) := 2^N * sum_{l=0}^{p} e_{2l}(beta) * mu_{2l}(N)
  StripEvenSum(r,b)   := sum_{alpha=r+1}^{r+b} E_p(alpha-N/2) * C(N,alpha)   (finite, computed directly)
  OddSumTotal(r,b)    := sum_{k=1}^{p} o_{2k-1}(beta) * (-1/2^{2k-1}) * Pcollapse(2k-1,r,b)

No file from general_b_dstar_attempt is imported. Q_p(u), mu_{2l}, and
Pcollapse are all independently derived in the sibling scripts.
"""
from fractions import Fraction
import sympy as sp

from own_ground_truth import D_star, fact
from full_rederivation import build_Qp_poly, derive_moments, Pcollapse_symbolic, binom_conv, P_b_val

v, beta_sym = sp.symbols('v beta')


def even_odd_split(p):
    """Q_p(-(v+beta/2)), expanded and split into even-in-v and odd-in-v
    parts, coefficients left symbolic in beta."""
    Qp, u = build_Qp_poly(p)
    sub = Qp.subs(u, -(v + beta_sym / 2))
    sub = sp.expand(sub)
    poly = sp.Poly(sub, v)
    even_terms = sp.Integer(0)
    odd_terms = sp.Integer(0)
    for (deg,), coeff in poly.terms():
        term = coeff * v ** deg
        if deg % 2 == 0:
            even_terms += term
        else:
            odd_terms += term
    return sp.expand(even_terms), sp.expand(odd_terms)


def extract_even_coeffs(even_poly, p):
    """Return dict l -> coefficient of v^{2l} (as sympy expr in beta), for
    l=0..p."""
    poly = sp.Poly(even_poly, v)
    coeffs = {}
    for l in range(0, p + 1):
        deg = 2 * l
        c = poly.coeff_monomial(v ** deg) if deg > 0 else poly.coeff_monomial(1)
        coeffs[l] = sp.expand(c) if c is not None else sp.Integer(0)
    return coeffs


def extract_odd_coeffs(odd_poly, p):
    """Return dict k -> coefficient of v^{2k-1} (as sympy expr in beta), for
    k=1..p."""
    poly = sp.Poly(odd_poly, v)
    coeffs = {}
    for k in range(1, p + 1):
        deg = 2 * k - 1
        c = poly.coeff_monomial(v ** deg)
        coeffs[k] = sp.expand(c) if c is not None else sp.Integer(0)
    return coeffs


_moments_cache = derive_moments(4)  # mu_0..mu_8, l=0..4


def full_even_sum(p, N_val, beta_val, even_coeffs):
    N_sym = sp.symbols('N')
    total = sp.Integer(0)
    for l in range(0, p + 1):
        mu = _moments_cache[l].subs(N_sym, N_val)
        ce = even_coeffs[l].subs(beta_sym, beta_val)
        total += ce * mu
    return sp.Rational(2) ** N_val * total


def strip_even_sum(r, b, even_coeffs, N_val, beta_val):
    total = Fraction(0)
    for alpha in range(r + 1, r + b + 1):
        vv = Fraction(2 * alpha - N_val, 2)
        Eval = Fraction(0)
        for l, ce in even_coeffs.items():
            coeff = sp.Rational(ce.subs(beta_sym, beta_val))
            Eval += Fraction(coeff.p, coeff.q) * (vv ** (2 * l))
        total += Eval * binom_conv(N_val, alpha)
    return total


def odd_sum_total(r, b, odd_coeffs, beta_val):
    total = Fraction(0)
    for k, co in odd_coeffs.items():
        coeff = sp.Rational(co.subs(beta_sym, beta_val))
        coeff_frac = Fraction(coeff.p, coeff.q)
        pc = Pcollapse_symbolic(2 * k - 1, sp.Integer(r), sp.Integer(b))
        pc_frac = Fraction(sp.Rational(pc).p, sp.Rational(pc).q)
        total += coeff_frac * Fraction(-1, 2 ** (2 * k - 1)) * pc_frac
    return total


_p_data_cache = {}


def get_p_data(p):
    if p in _p_data_cache:
        return _p_data_cache[p]
    even_poly, odd_poly = even_odd_split(p)
    ec = extract_even_coeffs(even_poly, p)
    oc = extract_odd_coeffs(odd_poly, p)
    _p_data_cache[p] = (ec, oc)
    return ec, oc


def D_assembled(p, r, b):
    N = 2 * r + b + 1
    beta_val = b + 1
    ec, oc = get_p_data(p)
    Pb = P_b_val(r, b)

    fes = full_even_sum(p, N, beta_val, ec)
    fes_frac = Fraction(sp.Rational(fes).p, sp.Rational(fes).q)

    ses = strip_even_sum(r, b, ec, N, beta_val)

    ost = odd_sum_total(r, b, oc, beta_val)

    result = Pb * Fraction(1, 2) * (fes_frac - ses) + ost
    return result


def sweep(p, r_max, b_max, label=""):
    fails = 0
    checks = 0
    first_fail = None
    for r in range(0, r_max + 1):
        for b in range(0, b_max + 1):
            got = D_assembled(p, r, b)
            want = D_star(p, r, b)
            checks += 1
            if got != want:
                fails += 1
                if first_fail is None:
                    first_fail = (r, b, got, want)
    print(f"sweep p={p} r<= {r_max} b<= {b_max} {label}: {checks} checks, {fails} failures"
          + (f" first fail: {first_fail}" if first_fail else ""))
    return fails, checks


if __name__ == "__main__":
    total_fails = 0
    total_checks = 0
    import time
    for p in [1, 2, 3, 4]:
        t0 = time.time()
        f, c = sweep(p, r_max=150, b_max=25)
        total_fails += f
        total_checks += c
        print(f"  (elapsed {time.time()-t0:.1f}s)")
    print(f"TOTAL: {total_checks} checks, {total_fails} failures")
