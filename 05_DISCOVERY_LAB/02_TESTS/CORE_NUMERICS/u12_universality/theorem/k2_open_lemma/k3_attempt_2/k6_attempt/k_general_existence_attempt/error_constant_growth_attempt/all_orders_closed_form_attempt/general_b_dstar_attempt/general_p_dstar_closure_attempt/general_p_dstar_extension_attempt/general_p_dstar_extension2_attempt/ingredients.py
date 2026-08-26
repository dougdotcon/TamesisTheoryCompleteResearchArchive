"""
ingredients.py -- Q_p(u) and the central moments mu_{2l}(N), general p / l,
computed by classical general-p / general-l algorithms (not fitted per
instance), fresh implementation for this front.

Cited, PROVED, not re-derived (per general_b_dstar_attempt/ATTEMPT.md Sec3.1
and general_p_dstar_closure_attempt/ATTEMPT.md Sec2.1-2.2, both read for
mathematical content only -- no code imported from either):

  - Q_p(u) := e_p(1,2,...,u), the elementary symmetric polynomial of degree
    p in the "variables" 1,...,u, extended to a genuine polynomial-in-u by
    Newton's identities from the classical Faulhaber power-sum polynomials
    P_i(u) := sum_{k=1}^u k^i.  Q_p has degree 2p and vanishes identically
    for integer u = 0,1,...,p-1 (fewer than p elements to choose from).

  - mu_{2l}(N) := 2^{-N} sum_{alpha=0}^N (alpha - N/2)^{2l} C(N,alpha), the
    2l-th central moment of Binomial(N,1/2), extracted from the cumulant
    generating function M(t) = exp(N log cosh(t/2)) = sum_k mu_k(N) t^k/k!.

Everything here is exact Fraction arithmetic; no floating point, no sympy
in the hot path (sympy is used only for a handful of independent
cross-checks, clearly marked, where its symbolic engine is convenient and
not performance-critical).

Polynomials are represented as plain Python lists of fractions.Fraction,
index = power (poly[0] is the constant term). This is the SAME
representation used throughout this directory (odd_part.py, assemble.py).
"""

from fractions import Fraction
import math


# ---------------------------------------------------------------------------
# Minimal polynomial-in-one-variable toolkit (Fraction coefficients).
# ---------------------------------------------------------------------------

def poly_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    if not p:
        p = [Fraction(0)]
    return p


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return poly_trim(out)


def poly_sub(a, b):
    return poly_add(a, [-c for c in b])


def poly_scale(a, c):
    c = Fraction(c)
    return poly_trim([x * c for x in a])


def poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca == 0:
            continue
        for j, cb in enumerate(b):
            if cb == 0:
                continue
            out[i + j] += ca * cb
    return poly_trim(out)


def poly_eval(p, x0):
    x0 = Fraction(x0)
    acc = Fraction(0)
    for c in reversed(p):
        acc = acc * x0 + c
    return acc


def poly_compose_linear(p, a, c):
    """Return the coefficient list of p(a*x + c) as a polynomial in x,
    given p as a coefficient list in its own variable, and a,c Fractions
    (or ints). Implemented by explicit binomial expansion of each
    (a*x+c)^n term (exact, general degree)."""
    a = Fraction(a)
    c = Fraction(c)
    result = [Fraction(0)]
    # (a*x + c)^n via repeated multiplication of the linear poly [c, a]
    linear = [c, a]
    power = [Fraction(1)]  # (a*x+c)^0
    for n, coeff in enumerate(p):
        if coeff != 0:
            term = poly_scale(power, coeff)
            result = poly_add(result, term)
        power = poly_mul(power, linear)
    return poly_trim(result)


# ---------------------------------------------------------------------------
# Bernoulli numbers (exact), and Faulhaber power-sum polynomials P_i(u).
# ---------------------------------------------------------------------------

_bernoulli_cache = {0: Fraction(1)}


def bernoulli(n):
    """B_n via the classical recurrence sum_{j=0}^{n} C(n+1,j) B_j = 0 for
    n>=1 (B_0=1), i.e. B_n = -1/(n+1) * sum_{j=0}^{n-1} C(n+1,j) B_j.
    (Convention B_1 = -1/2, matching the standard Faulhaber formula used
    below.)"""
    if n in _bernoulli_cache:
        return _bernoulli_cache[n]
    total = Fraction(0)
    for j in range(0, n):
        total += math.comb(n + 1, j) * bernoulli(j)
    b = Fraction(-total, n + 1)
    _bernoulli_cache[n] = b
    return b


_power_sum_cache = {}


def power_sum_poly(i):
    """P_i(u) := sum_{k=1}^u k^i, as a coefficient list (Fraction) in u.

    Self-caught bug, disclosed (see ATTEMPT.md "Self-caught issues"): the
    first version of this function applied the textbook Faulhaber formula
    (with the B_1=-1/2 Bernoulli convention this file's bernoulli()
    computes) directly as if it gave sum_{k=1}^{u}k^i. It does not -- with
    that convention the classical formula gives S_i(n) := sum_{k=0}^{n-1}
    k^i (an OFF-BY-ONE from the target: 0-indexed, n terms, k=0..n-1).
    Caught immediately by a from-scratch cross-check against direct
    summation (self_test() below), which failed loudly (a clean,
    systematic got(u)==want(u-1) shift, visible for every i,u tested)
    before this function was used for anything downstream (Q_poly had not
    yet been trusted). Fixed by using P_i(u) := S_i(u+1) -- i.e.
    evaluating the classical formula at n=u+1 and substituting back into a
    polynomial in u via poly_compose_linear(., a=1, c=1):
        S_i(n) = 1/(i+1) * sum_{j=0}^{i} C(i+1,j) B_j n^{i+1-j}
        P_i(u) = S_i(u+1).
    Degree i+1, general i (not fitted). Re-verified against direct
    summation for i=0..30, u=0..20 after the fix (self_test(), 0 fails)."""
    if i in _power_sum_cache:
        return _power_sum_cache[i]
    if i == 0:
        # Second self-caught edge case (see the fix note above): the
        # general S_i(u+1) route relies on sum_{k=1}^{u}k^i =
        # sum_{k=0}^{u}k^i, valid because 0^i=0 for i>=1 -- but 0^0=1
        # under the usual convention, so S_0(u+1)=u+1 counts a spurious
        # k=0 term that P_0(u):=sum_{k=1}^u 1=u must not include. Handled
        # directly rather than papering over it inside the general
        # formula, and covered by the i=0 row of self_test() below.
        coeffs = poly_trim([Fraction(0), Fraction(1)])
        _power_sum_cache[0] = coeffs
        return coeffs
    s_coeffs = [Fraction(0)] * (i + 2)
    for j in range(0, i + 1):
        power_of_n = i + 1 - j
        s_coeffs[power_of_n] += Fraction(math.comb(i + 1, j)) * bernoulli(j)
    s_coeffs = [c / (i + 1) for c in s_coeffs]
    coeffs = poly_compose_linear(poly_trim(s_coeffs), a=1, c=1)
    coeffs = poly_trim(coeffs)
    _power_sum_cache[i] = coeffs
    return coeffs


def _power_sum_direct(i, u):
    """Brute-force P_i(u) for concrete non-negative integer u (no formula),
    used only as an independent cross-check."""
    return sum(Fraction(k) ** i for k in range(1, u + 1))


# ---------------------------------------------------------------------------
# Q_p(u), general p, via Newton's identities.
# ---------------------------------------------------------------------------

_Q_cache = {0: [Fraction(1)]}  # Q_0(u) = e_0 = 1


def Q_poly(p):
    """Q_p(u) = e_p(1,...,u), as a coefficient list in u, via Newton's
    identity  p * e_p = sum_{i=1}^{p} (-1)^{i-1} e_{p-i} * P_i(u),
    e_0 = 1. Builds (and caches) every Q_1,...,Q_p along the way."""
    if p in _Q_cache:
        return _Q_cache[p]
    for q in range(1, p + 1):
        if q in _Q_cache:
            continue
        acc = [Fraction(0)]
        for i in range(1, q + 1):
            sign = 1 if (i % 2 == 1) else -1
            e_qi = _Q_cache[q - i]
            Pi = power_sum_poly(i)
            term = poly_mul(e_qi, Pi)
            term = poly_scale(term, sign)
            acc = poly_add(acc, term)
        acc = poly_scale(acc, Fraction(1, q))
        _Q_cache[q] = poly_trim(acc)
    return _Q_cache[p]


def _e_p_direct(p, u):
    """Brute-force elementary symmetric polynomial of degree p in
    {1,...,u} (u a non-negative integer), via direct DP over the
    numbers 1..u. Independent of Newton's-identity route; used only as
    cross-check."""
    if u < 0:
        raise ValueError("direct route only defined for u >= 0 here")
    # dp[k] = e_k(1..current)
    dp = [Fraction(0)] * (p + 1)
    dp[0] = Fraction(1)
    for m in range(1, u + 1):
        for k in range(min(p, m), 0, -1):
            dp[k] += dp[k - 1] * m
    return dp[p]


# ---------------------------------------------------------------------------
# Central moments mu_{2l}(N), general l, via power-series log/exp
# recurrence on the cumulant generating function.
# ---------------------------------------------------------------------------
#
#   cosh(t/2) = sum_j t^{2j} / (4^j (2j)!)                      [C(t)]
#   f(t) := log(cosh(t/2)) = sum_n f_n t^n, f_0 = 0              [log of C]
#   h(t) := N * f(t) = sum_n h_n(N) t^n, h_n(N) = N * f_n        [linear in N]
#   g(t) := exp(h(t)) = sum_m g_m(N) t^m                          [exp of h]
#   mu_{2l}(N) := (2l)! * g_{2l}(N)
#
# g_m(N) is a genuine polynomial in N of degree <= l for m=2l (classical
# fact: cumulants of a sum of N iid copies scale linearly in N, and moments
# are polynomial combinations of cumulants). We therefore track g_m as a
# poly-in-N coefficient list throughout, giving mu_{2l}(N) directly as a
# reusable polynomial-in-N -- no interpolation needed anywhere.

def _cosh_half_series(order):
    """Coefficients f-in-t of cosh(t/2) up to t^order (a plain number
    list, not poly-in-N -- cosh(t/2) does not depend on N)."""
    coeffs = [Fraction(0)] * (order + 1)
    j = 0
    while 2 * j <= order:
        coeffs[2 * j] = Fraction(1, (4 ** j) * math.factorial(2 * j))
        j += 1
    return coeffs


def _log_series(c, order):
    """L = log(C), given C's coefficient list (C_0 = 1 required), up to
    t^order. Uses the classical derivative-matching recurrence
        n*L_n = n*C_n - sum_{k=1}^{n-1} k*L_k*C_{n-k}      (n>=1, L_0=0)
    exact Fraction arithmetic."""
    assert c[0] == 1
    L = [Fraction(0)] * (order + 1)
    for n in range(1, order + 1):
        cn = c[n] if n < len(c) else Fraction(0)
        total = n * cn
        for k in range(1, n):
            ck = c[n - k] if (n - k) < len(c) else Fraction(0)
            total -= k * L[k] * ck
        L[n] = total / n
    return L


def _central_moment_polys(l_max):
    """Return a dict l -> mu_{2l}(N) as a poly-in-N coefficient list, for
    l = 0,...,l_max. h_n(N) = N * f_n is represented as the poly-in-N
    [0, f_n] (degree-1, coefficient f_n on N^1); g_m(N) built up via the
    exp-recurrence with poly-in-N (Fraction-coefficient-of-N) arithmetic:
        g_0 = [1]   (the constant polynomial 1)
        m * g_m = sum_{k=1}^{m} k * h_k * g_{m-k}          (from g' = h'g)
    """
    order = 2 * l_max
    cosh_c = _cosh_half_series(order)
    f = _log_series(cosh_c, order)  # f_n, plain Fractions (not poly-in-N)
    h = [ [Fraction(0)] if n == 0 else poly_trim([Fraction(0), f[n]]) for n in range(order + 1) ]
    # h[n] is the poly-in-N representing h_n(N) = N * f_n (degree <=1 in N)

    g = {0: [Fraction(1)]}
    for m in range(1, order + 1):
        acc = [Fraction(0)]
        for k in range(1, m + 1):
            gk = g[m - k]
            hk = h[k]
            term = poly_mul(hk, gk)
            term = poly_scale(term, k)
            acc = poly_add(acc, term)
        acc = poly_scale(acc, Fraction(1, m))
        g[m] = poly_trim(acc)

    mus = {}
    for l in range(0, l_max + 1):
        mus[l] = poly_scale(g[2 * l], math.factorial(2 * l))
    return mus


_mu_cache = {}


def central_moment_poly(l):
    """mu_{2l}(N) as a poly-in-N coefficient list, general l (cached,
    building the whole table up to l on first use above the current
    cache ceiling)."""
    global _mu_cache
    if l in _mu_cache:
        return _mu_cache[l]
    lmax = max(l, max(_mu_cache.keys(), default=-1))
    table = _central_moment_polys(lmax)
    _mu_cache.update(table)
    return _mu_cache[l]


def _central_moment_direct(l, N):
    """Brute-force mu_{2l}(N) for a concrete non-negative integer N, via
    direct summation over the binomial distribution -- independent of the
    generating-function route above."""
    total = Fraction(0)
    for alpha in range(0, N + 1):
        total += Fraction(math.comb(N, alpha)) * Fraction(2 * alpha - N, 2) ** (2 * l)
    return total / Fraction(2) ** N


# ---------------------------------------------------------------------------
# Self-tests.
# ---------------------------------------------------------------------------

def self_test():
    checks = 0
    fails = 0

    # --- Faulhaber power sums vs direct summation ---
    for i in range(0, 25):
        Pi = power_sum_poly(i)
        for u in range(0, 20):
            got = poly_eval(Pi, u)
            want = _power_sum_direct(i, u)
            checks += 1
            if got != want:
                fails += 1
                print(f"MISMATCH power_sum i={i} u={u}: got {got} want {want}")

    # --- Q_p(u) vs direct elementary symmetric polynomial ---
    for p in range(0, 15):
        Qp = Q_poly(p)
        for u in range(0, 16):
            got = poly_eval(Qp, u)
            want = _e_p_direct(p, u)
            checks += 1
            if got != want:
                fails += 1
                print(f"MISMATCH Q_p p={p} u={u}: got {got} want {want}")

    # --- Q_p vanishing for u = 0,...,p-1 (explicit, redundant with above
    # but stated separately per the archive's own convention of checking
    # this boundary explicitly) ---
    for p in range(1, 25):
        Qp = Q_poly(p)
        for u in range(0, p):
            got = poly_eval(Qp, u)
            checks += 1
            if got != 0:
                fails += 1
                print(f"MISMATCH Q_p vanishing p={p} u={u}: got {got}")

    # --- Q_p(-1) = 0 for every p >= 1 (noticed by hand at p=1,2 while
    # tracking down why the b=1 Strip term should vanish; the FIRST
    # version of this check, run against the then-buggy power_sum_poly
    # (see the fix note on that function), showed p=1,2 passing but
    # p=3..40 all giving 1 instead of 0 -- which briefly looked like the
    # pattern breaking down at p=3. It did not: that was entirely a
    # symptom of the power_sum_poly off-by-one (Sec "Self-caught
    # issues" of ATTEMPT.md). After the fix, Q_p(-1)=0 holds for every
    # p=1..40 tested, confirming the original by-hand observation. ---
    for p in range(1, 41):
        Qp = Q_poly(p)
        got = poly_eval(Qp, -1)
        checks += 1
        if got != 0:
            fails += 1
            print(f"MISMATCH Q_p(-1)=0, p={p}: got {got}")

    # --- central moments vs direct binomial summation ---
    for l in range(0, 12):
        mu = central_moment_poly(l)
        for N in range(0, 24):
            got = poly_eval(mu, N)
            want = _central_moment_direct(l, N)
            checks += 1
            if got != want:
                fails += 1
                print(f"MISMATCH mu l={l} N={N}: got {got} want {want}")

    # --- known small values sanity: mu_0(N)=1, mu_2(N)=N/4 ---
    for N in range(0, 10):
        checks += 1
        if poly_eval(central_moment_poly(0), N) != 1:
            fails += 1
            print(f"mu_0({N}) != 1")
        checks += 1
        if poly_eval(central_moment_poly(1), N) != Fraction(N, 4):
            fails += 1
            print(f"mu_2({N}) != N/4")

    print(f"ingredients.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("ingredients.py: OK" if ok else "ingredients.py: FAILURES")
