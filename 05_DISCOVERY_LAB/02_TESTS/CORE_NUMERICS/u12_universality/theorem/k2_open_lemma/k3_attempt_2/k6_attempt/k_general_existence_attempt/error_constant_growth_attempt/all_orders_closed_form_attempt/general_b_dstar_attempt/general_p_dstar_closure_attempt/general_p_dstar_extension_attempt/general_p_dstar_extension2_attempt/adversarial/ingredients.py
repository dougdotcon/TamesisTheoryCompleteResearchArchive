"""
Independent, from-scratch construction of:
  (1) Q_p(u) := e_p(1,...,u), the elementary symmetric polynomial of
      degree p in the variables 1,...,u, as an exact polynomial-in-u
      (list of fractions.Fraction coefficients, index = power of u).
  (2) mu_{2l}(N) := 2^{-N} sum_alpha (alpha-N/2)^{2l} C(N,alpha), the
      2l-th central moment of Bin(N,1/2), computed at CONCRETE integer N
      by direct binomial summation (exact, no polynomial-in-N machinery
      needed since every grid point below uses a concrete N).

Route chosen deliberately DIFFERENT from the target document's own
(Bernoulli-number Faulhaber formula for power sums): here power sums are
built via Stirling numbers of the SECOND kind and the hockey-stick
identity, sum_{k=1}^u k^i = sum_j S2(i,j) j! C(u+1,j+1) [with the empty
k=0 falling-factorial-1 term subtracted once at j=0] -- an independent
derivation, written fresh, no Bernoulli numbers involved at all.

Written fresh by the referee. No predecessor .py file was read or used.
"""
from fractions import Fraction
from functools import lru_cache

# ---------------------------------------------------------------------
# Polynomial helpers: a polynomial is a list of Fraction, index = power.
# ---------------------------------------------------------------------

def poly_trim(p):
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


def poly_scale(a, s):
    return poly_trim([c * s for c in a]) if a else [Fraction(0)]


def poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca == 0:
            continue
        for j, cb in enumerate(b):
            out[i + j] += ca * cb
    return poly_trim(out)


def poly_eval(a, x):
    # Horner
    res = Fraction(0)
    for c in reversed(a):
        res = res * x + c
    return res


# ---------------------------------------------------------------------
# Stirling numbers of the second kind, memoized recurrence
# S2(n,k) = k*S2(n-1,k) + S2(n-1,k-1), S2(0,0)=1.
# ---------------------------------------------------------------------

_s2_cache = {(0, 0): 1}


def stirling2(n, k):
    if k < 0 or k > n:
        return 0
    if (n, k) in _s2_cache:
        return _s2_cache[(n, k)]
    if n == 0:
        val = 1 if k == 0 else 0
    else:
        val = k * stirling2(n - 1, k) + stirling2(n - 1, k - 1)
    _s2_cache[(n, k)] = val
    return val


# ---------------------------------------------------------------------
# Falling-factorial-style binomial polynomial: C(u+1, m) as poly in u.
# C(u+1,m) = (u+1)*u*(u-1)*...*(u+2-m) / m!   (m factors)
# ---------------------------------------------------------------------

@lru_cache(maxsize=None)
def binom_poly_u_plus_1(m):
    """Returns C(u+1, m) as a polynomial in u (list of Fraction), m>=0."""
    if m == 0:
        return [Fraction(1)]
    poly = [Fraction(1)]
    for t in range(m):
        # factor (u + 1 - t)
        poly = poly_mul(poly, [Fraction(1 - t), Fraction(1)])
    fact_m = 1
    for i in range(1, m + 1):
        fact_m *= i
    return poly_scale(poly, Fraction(1, fact_m))


@lru_cache(maxsize=None)
def power_sum_poly(i):
    """P_i(u) := sum_{k=1}^u k^i, as an exact polynomial-in-u.
    Via Stirling2 + hockey-stick, independent route (no Bernoulli numbers).
    """
    total = [Fraction(0)]
    for j in range(0, i + 1):
        s2 = stirling2(i, j)
        if s2 == 0:
            continue
        fact_j = 1
        for t in range(1, j + 1):
            fact_j *= t
        term = poly_scale(binom_poly_u_plus_1(j + 1), Fraction(s2 * fact_j))
        total = poly_add(total, term)
    # subtract the spurious k=0 falling-factorial-0 term (only affects j=0,
    # i.e. only i=0 has S2(i,0) != 0)
    if stirling2(i, 0) != 0:
        total = poly_add(total, [Fraction(-stirling2(i, 0))])
    return total


@lru_cache(maxsize=None)
def Q_poly(p):
    """Q_p(u) := e_p(1,...,u), elementary symmetric polynomial, as an
    exact polynomial-in-u, via Newton's identities:
        p*e_p = sum_{i=1}^p (-1)^{i-1} e_{p-i} P_i(u),   e_0 = 1.
    """
    if p == 0:
        return [Fraction(1)]
    acc = [Fraction(0)]
    for i in range(1, p + 1):
        sign = Fraction(1) if i % 2 == 1 else Fraction(-1)
        e_pi = Q_poly(p - i)
        term = poly_mul(e_pi, power_sum_poly(i))
        term = poly_scale(term, sign)
        acc = poly_add(acc, term)
    return poly_scale(acc, Fraction(1, p))


# ---------------------------------------------------------------------
# Direct, independent computation of e_p(1,...,u) via DP over the
# numbers 1,...,u -- used ONLY as a cross-check, a completely different
# algorithm (no power sums, no Newton's identity, no Stirling numbers).
# ---------------------------------------------------------------------

def e_p_direct(p, u):
    """Direct DP for e_p(1,...,u) at a CONCRETE nonnegative integer u."""
    e = [Fraction(0)] * (p + 1)
    e[0] = Fraction(1)
    for k in range(1, u + 1):
        for j in range(min(p, k), 0, -1):
            e[j] = e[j] + k * e[j - 1]
    return e[p]


# ---------------------------------------------------------------------
# Central moments mu_{2l}(N) of Bin(N,1/2), centered, at CONCRETE
# integer N, via direct binomial summation.
# mu_{2l}(N) = 2^{-N} sum_{alpha=0}^N (2*alpha - N)^{2l} * C(N,alpha) / 4^l
# ---------------------------------------------------------------------

def binom_int(n, k):
    if k < 0 or k > n:
        return 0
    num = 1
    kk = min(k, n - k)
    for t in range(kk):
        num = num * (n - t) // (t + 1)
    return num


def mu_2l_direct(l, N):
    """mu_{2l}(N) at concrete integer N, direct binomial sum, exact Fraction."""
    total = Fraction(0)
    for alpha in range(0, N + 1):
        total += Fraction((2 * alpha - N) ** (2 * l)) * binom_int(N, alpha)
    total = total / Fraction(2 ** N)
    total = total / Fraction(4 ** l)
    return total


# ---------------------------------------------------------------------
# FAST route for mu_{2l}(N): power-series log(cosh)/exp recurrence,
# giving mu_{2l} as a polynomial in N once, reusable at every grid
# point (much faster than direct summation for N up to ~430 and l up
# to 40). Independent re-derivation (own from-scratch derivation of
# both the log and exp recurrences), matching the document's own
# *class* of algorithm but implemented fresh here.
# ---------------------------------------------------------------------


@lru_cache(maxsize=None)
def _cosh_half_coeff(n):
    """Coefficient of t^n in cosh(t/2) = sum_j t^{2j} / (4^j (2j)!)."""
    if n % 2 != 0:
        return Fraction(0)
    j = n // 2
    fact2j = 1
    for t in range(1, 2 * j + 1):
        fact2j *= t
    return Fraction(1, (4 ** j) * fact2j)


@lru_cache(maxsize=None)
def _log_cosh_half_coeff(n):
    """Coefficient L_n of t^n in log(cosh(t/2)), via f=cosh(t/2)=e^{L},
    using n f_n = sum_{k=1}^n k L_k f_{n-k}, f_0 = 1.
    """
    if n == 0:
        return Fraction(0)
    fn = _cosh_half_coeff(n)
    s = Fraction(0)
    for k in range(1, n):
        s += k * _log_cosh_half_coeff(k) * _cosh_half_coeff(n - k)
    Ln = (n * fn - s) / n  # since f_0=1, the k=n term is n*L_n*f_0
    return Ln


@lru_cache(maxsize=None)
def _g_coeff(m):
    """Coefficient g_m(N) of t^m in g(t) = exp(N * log cosh(t/2)), as a
    polynomial-in-N (list of Fraction, degree <= m). g_0 = 1 (constant).
    Uses m g_m = sum_{k=1}^m k h_k g_{m-k}, h_k = N * L_k (linear in N).
    """
    if m == 0:
        return [Fraction(1)]
    acc = [Fraction(0)]
    for k in range(1, m + 1):
        Lk = _log_cosh_half_coeff(k)
        if Lk == 0:
            continue
        g_mk = _g_coeff(m - k)
        # h_k * g_{m-k} = (N * Lk) * g_{m-k}(N)  -> shift g_{m-k} up by one
        # power of N and scale by Lk
        shifted = [Fraction(0)] + [c * Lk for c in g_mk]
        acc = poly_add(acc, poly_scale(shifted, Fraction(k)))
    return poly_scale(acc, Fraction(1, m))


@lru_cache(maxsize=None)
def mu_2l_poly(l):
    """mu_{2l}(N) as an exact polynomial-in-N (list of Fraction)."""
    if l == 0:
        return [Fraction(1)]
    m = 2 * l
    gm = _g_coeff(m)
    fact_m = 1
    for t in range(1, m + 1):
        fact_m *= t
    return poly_scale(gm, Fraction(fact_m))


def mu_2l_fast(l, N):
    return poly_eval(mu_2l_poly(l), Fraction(N))


# ---------------------------------------------------------------------
# Self tests
# ---------------------------------------------------------------------

def self_test():
    checks = 0
    fails = 0

    # Q_p(u) via Newton's identities vs direct DP, general p, general u
    for p in range(0, 15):
        for u in range(0, 16):
            got = poly_eval(Q_poly(p), Fraction(u))
            want = e_p_direct(p, u)
            checks += 1
            if got != want:
                fails += 1
                print("FAIL Q_p vs direct: p=", p, "u=", u, got, want)

    # vanishing boundary Q_p(u) = 0 for u = 0,...,p-1
    for p in range(1, 41):
        for u in range(0, p):
            got = poly_eval(Q_poly(p), Fraction(u))
            checks += 1
            if got != 0:
                fails += 1
                print("FAIL Q_p vanishing: p=", p, "u=", u, got)

    # central moments: fast route vs direct binomial summation
    for l in range(0, 12):
        for N in range(0, 24):
            got = mu_2l_fast(l, N)
            want = mu_2l_direct(l, N)
            checks += 1
            if got != want:
                fails += 1
                print("FAIL mu vs direct: l=", l, "N=", N, got, want)

    # sanity: mu_0(N) = 1, mu_2(N) = N/4
    for N in range(0, 10):
        checks += 1
        if mu_2l_fast(0, N) != 1:
            fails += 1
            print("FAIL mu_0 sanity N=", N)
        checks += 1
        if mu_2l_fast(1, N) != Fraction(N, 4):
            fails += 1
            print("FAIL mu_2 sanity N=", N)

    print(f"ingredients.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("ingredients.py:", "OK" if ok else "FAILED")
