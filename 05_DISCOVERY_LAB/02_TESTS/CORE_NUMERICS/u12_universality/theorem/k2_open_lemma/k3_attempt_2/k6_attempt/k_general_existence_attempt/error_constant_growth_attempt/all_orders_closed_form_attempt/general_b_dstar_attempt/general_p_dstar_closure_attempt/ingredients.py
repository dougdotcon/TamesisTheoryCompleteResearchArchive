"""
Ingredients for the general-p assembly, computed for GENERAL p (not fitted
per-p): Q_p(u) via Newton's identities from Faulhaber power sums, and the
central moments mu_{2l}(N) of Bin(N,1/2) via the cumulant generating
function, as a function of l.

Everything here is written from scratch. Q_p(u)'s degree/vanishing is cited
as already PROVED (general_b_dstar_attempt/ATTEMPT.md Sec 3.1); what is
computed here is the actual polynomial, for arbitrary p, via a classical
p-general algorithm (Newton's identities), not interpolation/fitting.
"""

import sympy as sp

u, N, t, x = sp.symbols('u N t x')


def elementary_symmetric_direct(p, uval):
    """Direct definition: Q_p(u) = e_p(1,2,...,u), evaluated at an integer u.
    Used only as an independent cross-check (brute force), not as the
    derivation method."""
    if uval < p:
        return 0
    xs = list(range(1, uval + 1))
    # e_p via generating function coefficient extraction (exact, sympy)
    xsym = sp.symbols('X')
    poly = sp.Integer(1)
    for k in xs:
        poly *= (1 + k * xsym)
    poly = sp.expand(poly)
    return sp.Poly(poly, xsym).coeff_monomial(xsym ** p)


_power_sum_cache = {}


def faulhaber(m, uu):
    """P_m(u) = sum_{k=1}^{u} k^m, as an exact polynomial in symbol uu.
    Computed via sympy's closed-form summation (classical Faulhaber
    formula), general in m."""
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
    """Q_p(u) = e_p(1,...,u) as an exact polynomial in u, via Newton's
    identities applied to the Faulhaber power-sum polynomials P_1,...,P_p.
    General algorithm in p -- computed once per p, cached."""
    if p in _Qp_cache:
        expr = _Qp_cache[p]
    else:
        # Newton's identities: e_0 = 1;
        # p*e_p = sum_{i=1}^{p} (-1)^{i-1} e_{p-i} * P_i(u)
        e = {0: sp.Integer(1)}
        for pp in range(1, p + 1):
            s = sp.Integer(0)
            for i in range(1, pp + 1):
                s += (-1) ** (i - 1) * e[pp - i] * faulhaber(i, u)
            e[pp] = sp.expand(s / pp)
        expr = e[p]
        _Qp_cache[p] = expr
    return sp.expand(expr.subs(u, uu)) if uu is not u else expr


def verify_Qp_against_direct(pmax=6, extra_points=15):
    print(f"--- Q_p(u) via Newton's identities vs direct e_p(1..u), p=0..{pmax} ---")
    total = 0
    fails = 0
    for p in range(0, pmax + 1):
        qp = Q_p(p)
        deg = sp.degree(sp.Poly(qp, u)) if qp != 0 else -1
        # test points: 0..2p (interpolation-determining range) + extra out of sample
        test_pts = list(range(0, 2 * p + 3)) + list(range(2 * p + 3, 2 * p + 3 + extra_points))
        for uv in test_pts:
            total += 1
            lhs = int(qp.subs(u, uv))
            rhs = int(elementary_symmetric_direct(p, uv))
            if lhs != rhs:
                fails += 1
                print(f"MISMATCH p={p} u={uv}: Newton={lhs} direct={rhs}")
        # vanishing check for u < p
        for uv in range(0, p):
            total += 1
            lhs = int(qp.subs(u, uv))
            if lhs != 0:
                fails += 1
                print(f"MISMATCH vanishing p={p} u={uv}: got {lhs}")
        expected_deg = 2 * p if p > 0 else 0
        print(f"p={p}: degree={deg} (expected {expected_deg}), "
              f"Q_p(u)={sp.nsimplify(qp)}")
    print(f"Q_p total checks={total}, fails={fails}")
    return fails


def verify_Qp_matches_parent_printed():
    """Cross-check against the four polynomials printed in the parent
    document's Sec 3.1 (used only as a comparison target, not as derivation
    input -- Q_p here is built from Newton's identities alone)."""
    print("--- cross-check vs parent-document-printed Q_1..Q_4 ---")
    parent = {
        0: sp.Integer(1),
        1: sp.Rational(1, 2) * u ** 2 + sp.Rational(1, 2) * u,
        2: sp.Rational(1, 8) * u ** 4 + sp.Rational(1, 12) * u ** 3
           - sp.Rational(1, 8) * u ** 2 - sp.Rational(1, 12) * u,
        3: sp.Rational(1, 48) * u ** 6 - sp.Rational(1, 48) * u ** 5
           - sp.Rational(1, 16) * u ** 4 + sp.Rational(1, 48) * u ** 3
           + sp.Rational(1, 24) * u ** 2,
        4: sp.Rational(1, 384) * u ** 8 - sp.Rational(1, 96) * u ** 7
           - sp.Rational(1, 576) * u ** 6 + sp.Rational(1, 30) * u ** 5
           - sp.Rational(5, 1152) * u ** 4 - sp.Rational(1, 32) * u ** 3
           + sp.Rational(1, 288) * u ** 2 + sp.Rational(1, 120) * u,
    }
    fails = 0
    for p, expr in parent.items():
        diff = sp.expand(Q_p(p) - expr)
        ok = (diff == 0)
        print(f"p={p}: matches parent printed formula exactly: {ok}")
        if not ok:
            fails += 1
            print("  residual:", diff)
    return fails


# ---------------------------------------------------------------------
# Central moments of Bin(N,1/2), general order, via cumulant generating
# function. K(t) = N*log(cosh(t/2)); M(t)=exp(K(t)) = sum mu_k(N) t^k/k!.
# ---------------------------------------------------------------------

_mu_cache = {}


def central_moment(l, order_cap=None):
    """mu_{2l}(N) via Taylor expansion of exp(N*log(cosh(t/2))) to the
    needed order. General in l (not degree-limited): recomputes the series
    to whatever order 2l+2 is required, caching intermediate results."""
    if l in _mu_cache:
        return _mu_cache[l]
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
    _mu_cache[l] = mu
    return mu


def verify_moments_direct(lmax=5, Nmax=22):
    print(f"--- central moments mu_2l(N) via cumulant GF vs direct sum, l=1..{lmax} ---")
    fails = 0
    total = 0
    for l in range(1, lmax + 1):
        formula = central_moment(l)
        print(f"mu_{2*l}(N) = {formula}")
        for Nv in range(2 * l, Nmax + 1):
            total += 1
            # direct: mu_{2l}(N) = 2^{-N} sum_{a=0}^N (a-N/2)^{2l} C(N,a)
            direct = sp.Rational(0)
            for a in range(0, Nv + 1):
                direct += (sp.Rational(a) - sp.Rational(Nv, 2)) ** (2 * l) * sp.binomial(Nv, a)
            direct = direct / 2 ** Nv
            pred = formula.subs(N, Nv)
            if sp.simplify(direct - pred) != 0:
                fails += 1
                print(f"MISMATCH l={l} N={Nv}: direct={direct} pred={pred}")
        print(f"  l={l}: checked N={2*l}..{Nmax}, fails so far={fails}")
    print(f"central moments total checks={total}, fails={fails}")
    return fails


def verify_moments_match_parent_printed():
    print("--- cross-check vs parent-document-printed mu_2,4,6,8 ---")
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
            print("  residual:", diff)
    return fails


# ---------------------------------------------------------------------
# Independent spot-check of the referee's general-k odd-power identity
# (cited as PROVED input, per task instructions). Re-derived here from
# scratch via the same Abel-summation-by-parts recipe, and checked against
# brute-force summation for the specific k values needed by this front.
# ---------------------------------------------------------------------

def S_odd_bruteforce(power, Nv, m):
    """S_{power}(N,m) = sum_{i=0}^m (N-2i)^power * C(N,i), power odd,
    direct summation, no recursion."""
    if m < 0:
        return sp.Integer(0)
    total = sp.Integer(0)
    for i in range(0, m + 1):
        total += (Nv - 2 * i) ** power * sp.binomial(Nv, i)
    return total


def S_odd_via_referee_recursion(power, Nv, m):
    """S_{2k-1}(N,m) via the referee's cited recursion:
    S_{2k-1}(N,m) = (N-2m)^{2k-2}(m+1)C(N,m+1)
                    + 2N * sum_{s odd,1<=s<=2k-3} C(2k-2,s) S_s(N-1,m-1)
    base case S_1(N,m) = (m+1) C(N,m+1)."""
    if power == 1:
        if m < 0:
            return sp.Integer(0)
        return (m + 1) * sp.binomial(Nv, m + 1)
    lead = (Nv - 2 * m) ** (power - 1) * (m + 1) * sp.binomial(Nv, m + 1) if m >= 0 else sp.Integer(0)
    total = lead
    for s in range(1, power - 1, 2):
        coeff = sp.binomial(power - 1, s)
        total += 2 * Nv * coeff * S_odd_via_referee_recursion(s, Nv - 1, m - 1)
    return total


def verify_referee_identity_spotcheck(powers=(1, 3, 5, 7, 9, 11, 13, 15), Nmax=30):
    print(f"--- spot-check of referee's general-k odd-power identity, powers={powers} ---")
    total = 0
    fails = 0
    for power in powers:
        for Nv in range(power, Nmax + 1):
            for m in range(-1, Nv + 1):
                total += 1
                a = S_odd_bruteforce(power, Nv, m)
                b = S_odd_via_referee_recursion(power, Nv, m)
                if a != b:
                    fails += 1
                    print(f"MISMATCH power={power} N={Nv} m={m}: bruteforce={a} recursion={b}")
    print(f"referee-identity spot-check: {total} checks, fails={fails}")
    return fails


if __name__ == "__main__":
    f1 = verify_Qp_against_direct(pmax=6, extra_points=15)
    f2 = verify_Qp_matches_parent_printed()
    f3 = verify_moments_direct(lmax=5, Nmax=22)
    f4 = verify_moments_match_parent_printed()
    f5 = verify_referee_identity_spotcheck(powers=(1, 3, 5, 7, 9, 11, 13, 15), Nmax=30)
    print()
    print("=== ingredients.py summary ===")
    print(f"Q_p Newton-identity vs direct e_p: fails={f1}")
    print(f"Q_p vs parent printed: fails={f2}")
    print(f"central moments vs direct sum: fails={f3}")
    print(f"central moments vs parent printed: fails={f4}")
    print(f"referee general-k odd-power identity spot-check: fails={f5}")
    assert f1 == 0 and f2 == 0 and f3 == 0 and f4 == 0 and f5 == 0, "INGREDIENT FAILURE"
    print("ALL INGREDIENT CHECKS PASSED")
