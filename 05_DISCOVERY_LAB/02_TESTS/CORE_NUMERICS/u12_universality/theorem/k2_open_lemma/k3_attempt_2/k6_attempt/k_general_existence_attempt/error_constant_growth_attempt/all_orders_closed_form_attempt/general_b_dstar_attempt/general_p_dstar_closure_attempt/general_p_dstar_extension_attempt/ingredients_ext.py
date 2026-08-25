"""
Ingredients for the extension front (p=11..20): Q_p(u) via Newton's
identities (UNCHANGED from general_p_dstar_closure_attempt/ingredients.py --
already fast enough at every p up to 20, timed below, no performance issue
found), and central moments mu_{2l}(N) of Bin(N,1/2) via the cumulant
generating function -- SAME generating function, SAME Taylor-extraction
target as the closure attempt, but computed via the classical power-series-
exponentiation recurrence instead of sympy's generic series()/exp()
pipeline, for speed (Honest process note, Sec 0 below).

Everything here is written fresh in this directory.
"""

import sympy as sp
from fractions import Fraction
from math import factorial
import time

u, N = sp.symbols('u N')

# ---------------------------------------------------------------------
# Q_p(u), UNCHANGED method from the closure attempt (Newton's identities
# from Faulhaber power sums). Timed below to confirm it remains cheap
# through p=20 -- it does (see __main__ output), so no performance variant
# is needed for this ingredient.
# ---------------------------------------------------------------------

_power_sum_cache = {}


def faulhaber(m, uu):
    if m in _power_sum_cache:
        expr = _power_sum_cache[m]
    else:
        kk = sp.symbols('kk')
        expr = sp.summation(kk ** m, (kk, 1, u))
        expr = sp.expand(expr)
        _power_sum_cache[m] = expr
    return expr.subs(u, uu)


_Qp_cache = {}


def Q_p(p, uu=u):
    """Q_p(u) = e_p(1,...,u), Newton's identities, general p."""
    if p in _Qp_cache:
        expr = _Qp_cache[p]
    else:
        e = {0: sp.Integer(1)}
        for pp in range(1, p + 1):
            s = sp.Integer(0)
            for i in range(1, pp + 1):
                s += (-1) ** (i - 1) * e[pp - i] * faulhaber(i, u)
            e[pp] = sp.expand(s / pp)
        expr = e[p]
        _Qp_cache[p] = expr
    return sp.expand(expr.subs(u, uu)) if uu is not u else expr


def elementary_symmetric_direct(p, uval):
    """Direct definition e_p(1,...,u), brute force -- independent
    cross-check, not the derivation method."""
    if uval < p:
        return 0
    xsym = sp.symbols('X')
    poly = sp.Integer(1)
    for k in range(1, uval + 1):
        poly *= (1 + k * xsym)
    poly = sp.expand(poly)
    return sp.Poly(poly, xsym).coeff_monomial(xsym ** p)


def verify_Qp_against_direct(pmax=8, extra_points=10):
    print(f"--- Q_p(u) via Newton's identities vs direct e_p(1..u), p=0..{pmax} ---")
    total = 0
    fails = 0
    for p in range(0, pmax + 1):
        qp = Q_p(p)
        test_pts = list(range(0, 2 * p + 3)) + list(range(2 * p + 3, 2 * p + 3 + extra_points))
        for uv in test_pts:
            total += 1
            lhs = int(qp.subs(u, uv))
            rhs = int(elementary_symmetric_direct(p, uv))
            if lhs != rhs:
                fails += 1
                print(f"MISMATCH p={p} u={uv}: Newton={lhs} direct={rhs}")
        for uv in range(0, p):
            total += 1
            if int(qp.subs(u, uv)) != 0:
                fails += 1
                print(f"MISMATCH vanishing p={p} u={uv}")
    print(f"Q_p total checks={total}, fails={fails}")
    return fails


def time_Qp_through_20():
    print("--- Q_p(u) timing, p=1..20 (confirms this ingredient needs no speed-up) ---")
    t0 = time.time()
    for p in range(1, 21):
        ta = time.time()
        qp = Q_p(p)
        tb = time.time()
        print(f"  Q_{p}: {tb-ta:.3f}s, degree={sp.degree(qp, u)}")
    print(f"total Q_p(1..20) time: {time.time()-t0:.2f}s")


# ---------------------------------------------------------------------
# Central moments mu_{2l}(N), general l. SLOW route (copied verbatim from
# the closure attempt's ingredients.py, kept here ONLY for the
# cross-validation below -- not used in production beyond l=10, since it
# is too slow past that, timed and documented in Sec 0/DERIVATION_PREREG).
# ---------------------------------------------------------------------

_mu_cache_slow = {}


def central_moment_slow(l):
    if l in _mu_cache_slow:
        return _mu_cache_slow[l]
    need = 2 * l + 2
    tt = sp.symbols('tt')
    Nsym = sp.symbols('Nn')
    K = Nsym * sp.log(sp.cosh(tt / 2))
    M = sp.series(sp.exp(K), tt, 0, need).removeO()
    M = sp.expand(M)
    coeff = M.coeff(tt, 2 * l)
    mu = sp.factorial(2 * l) * coeff
    mu = sp.expand(mu.subs(Nsym, N))
    mu = sp.simplify(mu)
    _mu_cache_slow[l] = mu
    return mu


# ---------------------------------------------------------------------
# Central moments mu_{2l}(N), FAST route: same cumulant generating
# function K(t) = N*log(cosh(t/2)), M(t) = exp(K(t)), same Taylor
# extraction target mu_{2l}(N) = (2l)! [t^{2l}] M(t) -- computed via the
# classical power-series-exponentiation recurrence (same algorithmic class
# as Newton's identities: if h(t)=sum h_n t^n with h_0=0, g(t):=exp(h(t))
# satisfies g_0=1, m*g_m = sum_{k=1}^m k*h_k*g_{m-k}, from g'=h'*g). Here
# h(t) = N*f(t), f(t):=log(cosh(t/2)), so h_k = N*f_k, and g_m comes out
# an exact polynomial in N of degree <= m. f(t)'s own coefficients are
# gotten from cosh(t/2)'s (elementary, closed form 1/((2j)! 2^{2j})) by
# the standard power-series-division/integration recipe for log of a
# series with constant term 1 -- all exact Fraction arithmetic, no sympy,
# no floating point anywhere.
# ---------------------------------------------------------------------

def log_cosh_half_coeffs(max_order):
    """f_n := coeff of t^n in log(cosh(t/2)), n=0..max_order, exact
    Fraction, via c*f' = c' (power-series division) then integration,
    where c(t):=cosh(t/2) = sum c_{2j} t^{2j}, c_{2j}=1/((2j)! 2^{2j})."""
    c = [Fraction(0)] * (max_order + 1)
    j = 0
    while 2 * j <= max_order:
        c[2 * j] = Fraction(1, factorial(2 * j) * (2 ** (2 * j)))
        j += 1
    cprime = [(n + 1) * c[n + 1] if n + 1 <= max_order else Fraction(0)
              for n in range(max_order + 1)]
    assert c[0] == 1
    fprime = [Fraction(0)] * (max_order + 1)
    for n in range(max_order + 1):
        s = cprime[n]
        for k in range(1, n + 1):
            s -= c[k] * fprime[n - k]
        fprime[n] = s  # / c[0], c[0]==1
    f = [Fraction(0)] * (max_order + 2)
    for n in range(max_order + 1):
        f[n + 1] = fprime[n] / (n + 1)
    return f


def exp_N_times_series(f_coeffs, order):
    """g(t) = exp(N*f(t)), f_coeffs[0]==0. Returns g[m] for m=0..order,
    each an exact Fraction coefficient list in N (low-to-high degree)."""
    g = [None] * (order + 1)
    g[0] = [Fraction(1)]
    for m in range(1, order + 1):
        acc = {}
        for k in range(1, m + 1):
            fk = f_coeffs[k] if k < len(f_coeffs) else Fraction(0)
            if fk == 0:
                continue
            coeff_k = k * fk
            gmk = g[m - k]
            for deg, cc in enumerate(gmk):
                if cc == 0:
                    continue
                acc[deg + 1] = acc.get(deg + 1, Fraction(0)) + coeff_k * cc
        maxdeg = max(acc.keys()) if acc else 0
        poly = [Fraction(0)] * (maxdeg + 1)
        for deg, cc in acc.items():
            poly[deg] = cc
        g[m] = [cc / m for cc in poly]
    return g


_mu_cache_fast = {}


def central_moment_fast_fraction(l):
    """mu_{2l}(N) as an exact Fraction coefficient list (low-to-high
    degree in N). This is the production route used for l=11..20."""
    if l in _mu_cache_fast:
        return _mu_cache_fast[l]
    order = 2 * l
    f = log_cosh_half_coeffs(order + 2)
    g = exp_N_times_series(f, order)
    mu = [factorial(2 * l) * cc for cc in g[2 * l]]
    _mu_cache_fast[l] = mu
    return mu


def central_moment(l):
    """Public entry point used by assemble_ext.py: exact sympy expression
    in N, via the fast route (production)."""
    coeffs = central_moment_fast_fraction(l)
    expr = sp.Integer(0)
    for i, cc in enumerate(coeffs):
        if cc == 0:
            continue
        expr += sp.Rational(cc.numerator, cc.denominator) * N ** i
    return sp.expand(expr)


def verify_moments_fast_vs_slow(lmax=10):
    """Honest process note: this is the load-bearing cross-check before
    the fast route is trusted for l=11..20 -- character-for-character
    against the closure attempt's own (slow) sympy cumulant-GF route,
    reproduced verbatim above as central_moment_slow, for every l where
    the slow route is still tractable (l=1..10; l=11 already took 45s,
    l=12 158s in exploratory timing -- see DERIVATION_PREREG.md)."""
    print(f"--- fast (power-series recurrence) vs slow (sympy series) central moments, l=1..{lmax} ---")
    fails = 0
    for l in range(1, lmax + 1):
        slow = central_moment_slow(l)
        fast = central_moment(l)
        diff = sp.expand(slow - fast)
        ok = (diff == 0)
        print(f"  l={l} (mu_{2*l}): match={ok}")
        if not ok:
            fails += 1
            print("    residual:", diff)
    return fails


def verify_moments_direct(lmax=8, extra_Ns=(30, 45, 60)):
    print(f"--- fast central moments vs DIRECT binomial summation, l=1..{lmax} ---")
    fails = 0
    total = 0
    for l in range(1, lmax + 1):
        coeffs = central_moment_fast_fraction(l)

        def ev(Nv, coeffs=coeffs):
            acc = Fraction(0)
            for cc in reversed(coeffs):
                acc = acc * Nv + cc
            return acc

        for Nv in list(range(2 * l, 2 * l + 6)) + list(extra_Ns):
            total += 1
            direct = Fraction(0)
            for a in range(0, Nv + 1):
                direct += Fraction((a - Fraction(Nv, 2)) ** (2 * l)) * \
                    Fraction(sp.binomial(Nv, a))
            direct /= 2 ** Nv
            pred = ev(Nv)
            if direct != pred:
                fails += 1
                print(f"MISMATCH l={l} N={Nv}: direct={direct} fast={pred}")
    print(f"direct-sum cross-check: {total} checks, fails={fails}")
    return fails, total


def verify_moments_match_parent_printed():
    print("--- cross-check vs parent-document-printed mu_2,4,6,8 (character-for-character) ---")
    parent = {
        1: N / 4,
        2: N * (3 * N - 2) / 16,
        3: N * (15 * N ** 2 - 30 * N + 16) / 64,
        4: sp.Rational(105, 256) * N ** 4 - sp.Rational(105, 64) * N ** 3
           + sp.Rational(147, 64) * N ** 2 - sp.Rational(17, 16) * N,
    }
    fails = 0
    for l, expr in parent.items():
        diff = sp.simplify(central_moment(l) - expr)
        ok = (diff == 0)
        print(f"l={l} (mu_{2*l}): matches parent printed formula exactly: {ok}")
        if not ok:
            fails += 1
    return fails


def time_moments_fast_through_20():
    print("--- central moments, FAST route, timing l=1..20 ---")
    t0 = time.time()
    for l in range(1, 21):
        ta = time.time()
        mu = central_moment(l)
        tb = time.time()
        deg = sp.degree(mu, N) if mu != 0 else 'NA'
        print(f"  mu_{2*l}: {tb-ta:.4f}s, degree={deg}")
    print(f"total fast-route mu(1..20) time: {time.time()-t0:.3f}s")


if __name__ == "__main__":
    f1 = verify_Qp_against_direct(pmax=8, extra_points=10)
    time_Qp_through_20()
    print()
    f2 = verify_moments_fast_vs_slow(lmax=10)
    f3, n3 = verify_moments_direct(lmax=8)
    f4 = verify_moments_match_parent_printed()
    print()
    time_moments_fast_through_20()
    print()
    print("=== ingredients_ext.py summary ===")
    print(f"Q_p Newton-identity vs direct e_p: fails={f1}")
    print(f"central moments fast vs slow (l=1..10): fails={f2}")
    print(f"central moments fast vs direct sum: fails={f3}/{n3}")
    print(f"central moments fast vs parent printed (l=1..4): fails={f4}")
    total_fails = f1 + f2 + f3 + f4
    assert total_fails == 0, "INGREDIENT FAILURE"
    print(f"ALL INGREDIENT CHECKS PASSED (total fails={total_fails})")
