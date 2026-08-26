"""
ingredients.py -- two of the assembly's cited, PROVED-general-p ingredients,
written FRESH for this front (no predecessor .py file opened/read/imported):

  (A) Q_p(u) := e_p(1,2,...,u), the p-th elementary symmetric polynomial in
      1,...,u, as an exact polynomial in u -- via Newton's identity
        p*e_p = sum_{i=1}^p (-1)^{i-1} e_{p-i} * P_i(u)
      where P_i(u) := sum_{k=1}^u k^i is the classical Faulhaber power-sum
      polynomial, built from Bernoulli numbers (own from-scratch recurrence,
      B_1=-1/2 convention).

  (B) The central moments mu_{2l}(N) of Bin(N,1/2) centered at N/2, as exact
      polynomials in N, via the moment generating function
        M(t) = E[e^{t(X-N/2)}] = cosh(t/2)^N = exp(N * log(cosh(t/2)))
      extracted by the classical "log-then-exp" power-series recurrence
      (own from-scratch derivation of both recurrences).

Polynomials are represented throughout as plain Python lists of
fractions.Fraction, ascending order (index i = coefficient of x^i).
"""
from fractions import Fraction
from math import comb

# ----------------------------------------------------------------------
# Small polynomial-in-one-variable utilities (ascending-order Fraction lists)
# ----------------------------------------------------------------------

def poly_zero():
    return [Fraction(0)]


def poly_trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
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


def poly_scale(a, s):
    return poly_trim([c * s for c in a])


def poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca == 0:
            continue
        for j, cb in enumerate(b):
            out[i + j] += ca * cb
    return poly_trim(out)


def poly_eval(a, x):
    """Evaluate polynomial a at x (x a Fraction or int)."""
    total = Fraction(0)
    for c in reversed(a):
        total = total * x + c
    return total


def poly_compose_linear(a, m, c):
    """Return the polynomial a(m*x + c) as a new polynomial in x."""
    # (m*x+c)^k built incrementally
    result = poly_zero()
    power = [Fraction(1)]  # (m*x+c)^0
    base = [Fraction(c), Fraction(m)]  # m*x + c, ascending
    for k, coeff in enumerate(a):
        if coeff != 0:
            result = poly_add(result, poly_scale(power, coeff))
        if k != len(a) - 1:
            power = poly_mul(power, base)
    return poly_trim(result)


# ----------------------------------------------------------------------
# (A) Bernoulli numbers, power sums, Q_p(u)
# ----------------------------------------------------------------------

_bernoulli_cache = {0: Fraction(1)}


def bernoulli(n):
    """B_n, with the B_1 = -1/2 convention, via the standard recurrence
    sum_{k=0}^{n} C(n+1,k) B_k = 0  for n >= 1."""
    if n in _bernoulli_cache:
        return _bernoulli_cache[n]
    total = Fraction(0)
    for k in range(0, n):
        total += comb(n + 1, k) * bernoulli(k)
    b_n = -total / (n + 1)
    _bernoulli_cache[n] = b_n
    return b_n


def _power_sum_direct(i, u):
    """Direct (unoptimized) computation of P_i(u) := sum_{k=1}^u k^i, used
    only as an independent cross-check."""
    return Fraction(sum(k ** i for k in range(1, u + 1)))


_power_sum_poly_cache = {}


def power_sum_poly(i):
    """P_i(u) := sum_{k=1}^u k^i, as an exact polynomial in u (ascending
    Fraction list).

    i=0: P_0(u) = u  (special case: sum of u ones).
    i>=1: the classical Faulhaber formula
        sum_{k=0}^{n-1} k^i = (1/(i+1)) sum_{j=0}^{i} C(i+1,j) B_j n^{i+1-j}
    computes sum_{k=0}^{n-1} k^i; since 0^i=0 for i>=1,
    sum_{k=1}^{u} k^i = sum_{k=0}^{u} k^i = [that formula at n=u+1].
    """
    if i in _power_sum_poly_cache:
        return _power_sum_poly_cache[i]
    if i == 0:
        poly = [Fraction(0), Fraction(1)]  # P_0(u) = u
        _power_sum_poly_cache[i] = poly
        return poly
    # Build the classical formula as a polynomial in n, then substitute
    # n = u+1 (poly_compose_linear with m=1, c=1).
    # F(n) = (1/(i+1)) * sum_{j=0}^{i} C(i+1,j) B_j * n^{i+1-j}
    deg = i + 1
    coeffs_in_n = [Fraction(0)] * (deg + 1)  # ascending, index = power of n
    for j in range(0, i + 1):
        power_of_n = i + 1 - j
        coeffs_in_n[power_of_n] += Fraction(comb(i + 1, j)) * bernoulli(j)
    F_n = poly_scale(poly_trim(coeffs_in_n), Fraction(1, i + 1))
    poly = poly_compose_linear(F_n, Fraction(1), Fraction(1))  # n = u+1
    poly = poly_trim(poly)
    _power_sum_poly_cache[i] = poly
    return poly


_Qp_cache = {0: [Fraction(1)]}  # Q_0(u) = 1


def Q_poly(p):
    """Q_p(u) := e_p(1,...,u), as an exact polynomial in u, via Newton's
    identity: p*e_p = sum_{i=1}^p (-1)^{i-1} e_{p-i} P_i(u), e_0 = 1."""
    if p in _Qp_cache:
        return _Qp_cache[p]
    for pp in range(1, p + 1):
        if pp in _Qp_cache:
            continue
        acc = poly_zero()
        for i in range(1, pp + 1):
            term = poly_mul(_Qp_cache[pp - i], power_sum_poly(i))
            sign = Fraction(1) if (i % 2 == 1) else Fraction(-1)
            acc = poly_add(acc, poly_scale(term, sign))
        e_pp = poly_scale(acc, Fraction(1, pp))
        _Qp_cache[pp] = poly_trim(e_pp)
    return _Qp_cache[p]


def _e_p_direct(p, u):
    """Direct DP computation of e_p(1,...,u) at a concrete integer u -- a
    THIRD, independent route (no Newton's identity, no power sums, no
    Bernoulli numbers): standard elementary-symmetric-polynomial DP."""
    # dp[k] = e_k(x_1,...,x_j) built incrementally as j runs 1..u
    dp = [Fraction(0)] * (p + 1)
    dp[0] = Fraction(1)
    for x in range(1, u + 1):
        for k in range(min(p, x), 0, -1):
            dp[k] += dp[k - 1] * x
    return dp[p]


# ----------------------------------------------------------------------
# (B) Central moments mu_{2l}(N), via log(cosh) then exp, as polynomials in N
# ----------------------------------------------------------------------

def _log_series(c, order):
    """Given a power series c = [c_0=1, c_1, c_2, ...] (ascending, plain
    Fraction coefficients, c_0 must be 1), return L = log(c) as a power
    series up to the given order (inclusive), via the standard recurrence
    obtained from L'(t) c(t) = c'(t):
        n*l_n = n*c_n - sum_{k=1}^{n-1} k*l_k*c_{n-k}     (n>=1), l_0 = 0.
    """
    assert c[0] == 1
    c = c + [Fraction(0)] * (order + 1 - len(c)) if len(c) < order + 1 else c
    l = [Fraction(0)] * (order + 1)
    for n in range(1, order + 1):
        total = Fraction(n) * (c[n] if n < len(c) else Fraction(0))
        for k in range(1, n):
            total -= Fraction(k) * l[k] * (c[n - k] if n - k < len(c) else Fraction(0))
        l[n] = total / n
    return l


def _exp_series_with_poly_coeffs(g, order):
    """Given a power series g = [g_0=poly_zero, g_1, g_2, ...] whose
    coefficients are themselves polynomials-in-N (ascending Fraction
    lists), with g_0 = 0, return F = exp(g) as a power series (coefficients
    also polynomials-in-N) up to the given order, via
        n*f_n = sum_{k=1}^{n} k*g_k*f_{n-k},   f_0 = 1 (poly).
    """
    f = [None] * (order + 1)
    f[0] = [Fraction(1)]
    for n in range(1, order + 1):
        acc = poly_zero()
        for k in range(1, n + 1):
            gk = g[k] if k < len(g) else poly_zero()
            acc = poly_add(acc, poly_scale(poly_mul(gk, f[n - k]), Fraction(k)))
        f[n] = poly_scale(acc, Fraction(1, n))
    return f


_moment_cache = {}
_MAX_MOMENT_ORDER_BUILT = [0]
_cosh_log_series_cache = [None]


def _build_moment_table(max_order):
    """Build f_n(N) = [t^n] exp(N * log(cosh(t/2))) for n=0..max_order, as
    polynomials in N. mu_n(N) = n! * f_n(N) (odd n give mu_n=0 automatically,
    since cosh is even)."""
    if _MAX_MOMENT_ORDER_BUILT[0] >= max_order and _cosh_log_series_cache[0] is not None:
        return
    order = max_order
    # cosh(t/2) = sum_k (t/2)^{2k} / (2k)!  =  sum_k t^k * a_k with
    # a_k = 0 for odd k, a_k = 1/(2^k k!) for even k=2j -> 1/(2^{2j}(2j)!)
    import math as _m
    c = [Fraction(0)] * (order + 1)
    c[0] = Fraction(1)
    k = 2
    while k <= order:
        c[k] = Fraction(1, (2 ** k) * _m.factorial(k))
        k += 2
    L = _log_series(c, order)  # log(cosh(t/2)), plain Fraction coefficients
    # g_k(N) := N * L[k]  (a degree-1 polynomial in N: [0, L[k]])
    g = [poly_zero() if k == 0 else [Fraction(0), L[k]] for k in range(order + 1)]
    F = _exp_series_with_poly_coeffs(g, order)  # f_n(N), polynomials in N
    _cosh_log_series_cache[0] = F
    _MAX_MOMENT_ORDER_BUILT[0] = order


def warm_up_moments(max_order):
    """Pre-build the moment table up to max_order in ONE pass. Calling this
    once (with the largest order that will ever be needed) before any
    mu_poly(n) calls for smaller n avoids the pathological incremental
    rebuild that mu_poly's lazy max()-based growth would otherwise trigger
    if called with strictly increasing n one at a time (each such call
    would re-run the whole O(order^2) log/exp recurrence from scratch)."""
    _build_moment_table(max_order)


def mu_poly(n):
    """mu_n(N), the n-th central moment of Bin(N,1/2) about N/2, as an exact
    polynomial in N (ascending Fraction list). mu_n = 0 for odd n (by
    symmetry, confirmed structurally: log(cosh) is an even series so every
    odd-order f_n is identically the zero polynomial)."""
    if n in _moment_cache:
        return _moment_cache[n]
    _build_moment_table(max(n, _MAX_MOMENT_ORDER_BUILT[0]))
    F = _cosh_log_series_cache[0]
    import math as _m
    fn = F[n]
    mu = poly_scale(fn, Fraction(_m.factorial(n)))
    _moment_cache[n] = poly_trim(mu)
    return _moment_cache[n]


def mu_direct_binomial(n, N):
    """Direct binomial-summation computation of mu_n(N) at a concrete
    integer N, used only as an independent cross-check:
        mu_n(N) = 2^{-N} * sum_{a=0}^{N} (a - N/2)^n * C(N,a).
    """
    total = Fraction(0)
    for a in range(0, N + 1):
        total += Fraction((2 * a - N) ** n, 2 ** n) * comb(N, a)
    return total / (2 ** N)


# ----------------------------------------------------------------------
# Self-tests
# ----------------------------------------------------------------------

def self_test():
    checks = 0
    fails = 0

    # B_1 = -1/2 sanity check.
    checks += 1
    if bernoulli(1) != Fraction(-1, 2):
        fails += 1
        print(f"MISMATCH bernoulli(1): {bernoulli(1)}")

    # power_sum_poly vs direct summation.
    for i in range(0, 25):
        for u in range(0, 20):
            checks += 1
            got = poly_eval(power_sum_poly(i), Fraction(u))
            want = _power_sum_direct(i, u)
            if got != want:
                fails += 1
                print(f"MISMATCH power_sum i={i} u={u}: got={got} want={want}")

    # Q_p(u) vs direct DP e_p computation, third independent route.
    for p in range(0, 15):
        for u in range(0, 16):
            checks += 1
            got = poly_eval(Q_poly(p), Fraction(u))
            want = _e_p_direct(p, u)
            if got != want:
                fails += 1
                print(f"MISMATCH Q_poly p={p} u={u}: got={got} want={want}")

    # deg Q_p(u) = 2p (cited fact, THEOREM.md "Estagio 16": "Q_p(u) tem
    # grau 2p genuino"), checked directly, p=0,...,80 (this front's full
    # target range) -- load-bearing for the moment-table order needed by
    # assemble.py's Assembler.
    for p in range(0, 81):
        checks += 1
        deg = len(poly_trim(Q_poly(p))) - 1
        if deg != 2 * p:
            fails += 1
            print(f"MISMATCH deg Q_poly p={p}: got_deg={deg} want_deg={2 * p}")

    # Vanishing boundary: Q_p(u) = 0 for u = 0,...,p-1, p=1,...,80
    # (needed up to p=80 for this front's target range).
    for p in range(1, 81):
        for u in range(0, p):
            checks += 1
            if poly_eval(Q_poly(p), Fraction(u)) != 0:
                fails += 1
                print(f"MISMATCH vanishing p={p} u={u}")

    # Central moments vs direct binomial summation.
    for l in range(0, 12):
        for N in range(0, 24):
            checks += 1
            got = poly_eval(mu_poly(2 * l), Fraction(N))
            want = mu_direct_binomial(2 * l, N)
            if got != want:
                fails += 1
                print(f"MISMATCH mu l={l} N={N}: got={got} want={want}")

    # mu_0(N)=1, mu_2(N)=N/4 sanity checks.
    for N in range(0, 10):
        checks += 1
        if poly_eval(mu_poly(0), Fraction(N)) != 1:
            fails += 1
            print(f"MISMATCH mu_0 N={N}")
        checks += 1
        if poly_eval(mu_poly(2), Fraction(N)) != Fraction(N, 4):
            fails += 1
            print(f"MISMATCH mu_2 N={N}")

    # Odd central moments vanish identically (structural check).
    for n in (1, 3, 5, 7, 9, 21, 41):
        checks += 1
        if poly_trim(mu_poly(n)) != [Fraction(0)]:
            fails += 1
            print(f"MISMATCH odd moment not zero, n={n}: {mu_poly(n)}")

    print(f"ingredients.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    # Pre-build the tables needed for this front's target scale (p up to 80;
    # Q_p(u) has genuine degree 2p, so moments are needed up to order 160)
    # before running self-tests.
    Q_poly(80)
    warm_up_moments(160)
    ok = self_test()
    print("ingredients.py: OK" if ok else "ingredients.py: FAILED")
