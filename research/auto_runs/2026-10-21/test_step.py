"""numeric_probe: sanidade cruzada de A_m(gamma) por rotas independentes."""
import pytest
import sympy as sp
import mpmath


def _A_sym():
    m, g = sp.symbols('m gamma', positive=True)
    return m * (m + 3) / (2 * g) - m * (m + 1) / g**2, m, g


def test_A0_identically_zero():
    A, m, g = _A_sym()
    assert sp.simplify(A.subs(m, 0)) == 0


def test_neg_gamma_A1_equals_c_gamma():
    A, m, g = _A_sym()
    c = 2 * (1 - g) / g
    assert sp.simplify(-g * A.subs(m, 1) - c) == 0


def test_partial_sum_symbolic():
    k = sp.Symbol('k', nonneg=True, integer=True)
    M = sp.Symbol('M', positive=True, integer=True)
    g = sp.Symbol('gamma', positive=True)
    A_k = k * (k + 3) / (2 * g) - k * (k + 1) / g**2
    direct = sp.summation(A_k, (k, 0, M))
    closed = M * (M + 1) * ((M + 5) * g - 2 * (M + 2)) / (6 * g**2)
    assert sp.simplify(sp.expand(direct - closed)) == 0


@pytest.mark.parametrize("gamma", [0.3, 0.5, 0.8, 1.0, 1.5])
@pytest.mark.parametrize("M", [1, 5, 10, 50, 100])
def test_partial_sum_numeric(M, gamma):
    direct = sum(
        m * (m + 3) / (2 * gamma) - m * (m + 1) / gamma**2
        for m in range(M + 1)
    )
    closed = M * (M + 1) * ((M + 5) * gamma - 2 * (M + 2)) / (6 * gamma**2)
    assert abs(direct - closed) < 1e-10 * (abs(closed) + 1)


def test_Am_gamma1_symbolic():
    A, m, g = _A_sym()
    assert sp.simplify(A.subs(g, 1) + m * (m - 1) / 2) == 0


def test_reciprocal_series_gamma1():
    mpmath.mp.dps = 50
    N = 200
    s = sum(mpmath.mpf(-2) / (k * (k - 1)) for k in range(2, N + 1))
    expected = mpmath.mpf(-2) * (1 - mpmath.mpf(1) / N)
    assert abs(s - expected) < mpmath.mpf(10)**(-40)


def test_Am_gamma_half_symbolic():
    A, m, g = _A_sym()
    assert sp.simplify(A.subs(g, sp.Rational(1, 2)) + m * (3 * m + 1)) == 0


def test_reciprocal_series_gamma_half():
    mpmath.mp.dps = 50
    N = 1000
    s = sum(
        mpmath.mpf(-1) / (k * (3 * k + 1))
        for k in range(1, N + 1)
    )
    # 1/(m(3m+1)) = (1/m - 3/(3m+1)) via partial fractions
    # sum = H_N - [psi(N+4/3) - psi(4/3)] / 1
    # Use direct digamma route:
    ana = -(
        mpmath.digamma(mpmath.mpf(N + 1)) + mpmath.euler
        + mpmath.digamma(mpmath.mpf(4) / 3)
        - mpmath.digamma(mpmath.mpf(N) + mpmath.mpf(4) / 3)
    )
    assert abs(s - ana) < mpmath.mpf(10)**(-35), f"|diff|={float(abs(s - ana)):.2e}"


def test_A_table_values():
    """Tabela A_2..A_4 contra valores explícitos."""
    g = sp.Symbol('gamma', positive=True)
    A_expr = lambda k: k * (k + 3) / (2 * g) - k * (k + 1) / g**2
    assert sp.simplify(A_expr(2) - (5 / g - 6 / g**2)) == 0
    assert sp.simplify(A_expr(3) - (9 / g - 12 / g**2)) == 0
    assert sp.simplify(A_expr(4) - (14 / g - 20 / g**2)) == 0
