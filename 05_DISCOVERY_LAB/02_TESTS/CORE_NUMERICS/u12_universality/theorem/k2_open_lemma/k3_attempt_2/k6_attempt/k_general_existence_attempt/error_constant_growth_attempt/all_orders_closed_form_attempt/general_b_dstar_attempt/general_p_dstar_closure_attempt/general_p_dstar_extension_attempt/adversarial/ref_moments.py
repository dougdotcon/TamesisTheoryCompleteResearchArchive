# Hostile-referee check 1 (extension front, p=11..20): central moments mu_{2l}(N).
#
# OWN re-derivation, independent implementation. None of the target front's .py
# files were read (per discipline); only ATTEMPT.md's mathematical description.
#
# Derivation (from scratch):
#   X ~ Bin(N, 1/2), centered: M(t) = E[e^{t(X-N/2)}] = (e^{t/2}+e^{-t/2})^N / 2^N
#                                    = cosh(t/2)^N = exp(N log cosh(t/2)).
#   So K(t) = N log cosh(t/2) and mu_m(N) = m! [t^m] exp(K(t)).
#
#   Series recurrences (both re-derived here, textbook):
#   (i) log of a series with constant term 1:  c(t) = cosh(t/2) = sum_j t^{2j}/(4^j (2j)!),
#       f = log c  =>  c = e^f  =>  c' = f' c  =>  n c_n = sum_{k=1}^{n} k f_k c_{n-k}
#       =>  f_n = c_n - (1/n) sum_{k=1}^{n-1} k f_k c_{n-k}.
#   (ii) exp of a series with zero constant term: h = N f, g = e^h
#       =>  g' = h' g  =>  m g_m = sum_{k=1}^{m} k h_k g_{m-k},  g_0 = 1.
#   Then mu_{2l}(N) = (2l)! g_{2l}, a polynomial in N (h_k = N f_k, so each g_m is
#   a polynomial in N with Fraction coefficients).
#
# Cross-check: DIRECT binomial summation (exact Fractions), a route the front's
# production sweep did NOT use:
#   mu_{2l}(N) = 2^{-N} sum_{k=0}^{N} C(N,k) (k-N/2)^{2l}
#              = [ sum_k C(N,k) (2k-N)^{2l} ] / (4^l 2^N).
# The front's own direct-sum check stopped at l=8; here l runs to 20 (mu_40),
# i.e. every moment order actually consumed by the p=11..20 assembly.
#
# Exact arithmetic only (fractions.Fraction). No randomness.

from fractions import Fraction
from math import comb, factorial
import time

LMAX = 20          # moments up to mu_40 (needed for p=20)
ORDER = 2 * LMAX   # series order in t


def cosh_half_coeffs(order):
    """Coefficients of cosh(t/2) = sum_j t^{2j} / (4^j (2j)!), up to t^order."""
    c = [Fraction(0)] * (order + 1)
    for j in range(0, order // 2 + 1):
        c[2 * j] = Fraction(1, (4 ** j) * factorial(2 * j))
    return c


def log_series(c, order):
    """f = log(c) for a series c with c_0 = 1, via n f_n = n c_n - sum_{k<n} k f_k c_{n-k}."""
    assert c[0] == 1
    f = [Fraction(0)] * (order + 1)
    for n in range(1, order + 1):
        acc = n * c[n]
        for k in range(1, n):
            acc -= k * f[k] * c[n - k]
        f[n] = Fraction(acc, n)
    return f


# ---- polynomial-in-N utilities: a poly is a list of Fractions, index = power of N ----

def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_scale(a, s):
    return [x * s for x in a]


def poly_shift_N(a):
    """multiply by N"""
    return [Fraction(0)] + list(a)


def poly_eval(a, N):
    acc = Fraction(0)
    for coef in reversed(a):
        acc = acc * N + coef
    return acc


def exp_series_polyN(f, order):
    """g = exp(N * f) as series in t with polynomial-in-N coefficients.
    m g_m = sum_{k=1}^m k h_k g_{m-k}, h_k = N f_k."""
    g = [[Fraction(1)]]  # g_0 = 1
    for m in range(1, order + 1):
        acc = [Fraction(0)]
        for k in range(1, m + 1):
            if f[k] == 0:
                continue
            term = poly_shift_N(poly_scale(g[m - k], k * f[k]))  # k * (N f_k) * g_{m-k}
            acc = poly_add(acc, term)
        g.append(poly_scale(acc, Fraction(1, m)))
    return g


def mu_polys(lmax=LMAX):
    """Return {l: polynomial-in-N coefficient list for mu_{2l}(N)}, l=1..lmax."""
    order = 2 * lmax
    c = cosh_half_coeffs(order)
    f = log_series(c, order)
    # sanity: f must be even (cosh(t/2) is even)
    assert all(f[n] == 0 for n in range(1, order + 1, 2)), "log cosh series not even!"
    g = exp_series_polyN(f, order)
    # sanity: g must be even too
    for m in range(1, order + 1, 2):
        assert all(x == 0 for x in g[m]), "odd moment nonzero!"
    return {l: poly_scale(g[2 * l], factorial(2 * l)) for l in range(1, lmax + 1)}


def mu_direct(l, N):
    """Direct binomial summation, exact."""
    s = sum(comb(N, k) * (2 * k - N) ** (2 * l) for k in range(N + 1))
    return Fraction(s, (4 ** l) * (2 ** N))


def main():
    t0 = time.time()
    mus = mu_polys(LMAX)
    t_build = time.time() - t0
    print(f"--- referee fast-route mu_(2l)(N), l=1..{LMAX}, built in {t_build:.3f}s ---")

    # structural checks: degree in N must be exactly l
    for l in range(1, LMAX + 1):
        deg = len(mus[l]) - 1
        assert deg == l, (l, deg)
        assert mus[l][-1] != 0
    print(f"degree check: deg_N mu_(2l) == l for every l=1..{LMAX}: OK")

    # spot-print the small ones (classical values, eyeball check)
    print("mu_2(N)  =", mus[1], " (expect [0, 1/4]  i.e. N/4)")
    print("mu_4(N)  =", mus[2], " (expect N(3N-2)/16 = [0, -1/8, 3/16])")

    # cross-check vs direct binomial summation -- ALL l=1..20 (front stopped at l=8)
    checks = 0
    fails = 0
    for l in range(1, LMAX + 1):
        for N in list(range(0, 41)) + [101, 250, 431, 631]:
            want = mu_direct(l, N)
            got = poly_eval(mus[l], N)
            checks += 1
            if want != got:
                fails += 1
                print(f"MISMATCH l={l} N={N}: direct={want} poly={got}")
    print(f"direct-binomial-summation cross-check, l=1..{LMAX}, "
          f"N in 0..40 + {{101,250,431,631}}: {checks} checks, fails={fails}")
    assert fails == 0
    print("ALL REFEREE MOMENT CHECKS PASSED")
    return mus


if __name__ == "__main__":
    main()
