"""numeric_probe (sanidade): propriedades algébricas de A_m(γ)."""
import sympy as sp
import numpy as np


def _A(m, g):
    """A_m(γ) = m(m+3)/(2γ) - m(m+1)/γ²."""
    return m * (m + 3) / (2 * g) - m * (m + 1) / g**2


# ── verificações simbólicas ──────────────────────────────────────────

def test_A0_vanishes_symbolically():
    """A_0(γ) ≡ 0 para todo γ."""
    g = sp.Symbol('gamma', positive=True)
    A0 = sp.Integer(0)*(sp.Integer(0)+3)/(2*g) - sp.Integer(0)*(sp.Integer(0)+1)/g**2
    assert A0 == 0


def test_minus_gamma_A1_equals_c_gamma():
    """-γ·A_1(γ) = c(γ) = 2(1−γ)/γ exatamente."""
    g = sp.Symbol('gamma', positive=True)
    A1 = sp.Rational(1,1)*(sp.Rational(1,1)+3)/(2*g) - sp.Rational(1,1)*(sp.Rational(1,1)+1)/g**2
    c_g = 2*(1 - g)/g
    assert sp.simplify(-g * A1 - c_g) == 0


def test_Am_negative_threshold():
    """A_m<0 para m≥1, γ∈(0,1): limiar γ*=2(m+1)/(m+3)≥1."""
    m = sp.Symbol('m', positive=True, integer=True)
    g_star = 2*(m + 1)/(m + 3)
    diff = sp.simplify(g_star - 1)
    # diff = (m−1)/(m+3) ≥ 0 para m ≥ 1
    assert sp.simplify(diff - (m - 1)/(m + 3)) == 0
    for mv in range(1, 21):
        assert float(g_star.subs(m, mv)) >= 1.0


def test_matched_leading_coefficient():
    """Sob m=λ√n, A_m/n → λ²(γ−2)/(2γ²) quando n→∞."""
    lam, n, g = sp.symbols('lambda n gamma', positive=True)
    A_sub = (lam*sp.sqrt(n))*(lam*sp.sqrt(n)+3)/(2*g) \
          - (lam*sp.sqrt(n))*(lam*sp.sqrt(n)+1)/g**2
    leading = sp.limit(A_sub / n, n, sp.oo)
    expected = lam**2 * (g - 2) / (2 * g**2)
    assert sp.simplify(leading - expected) == 0


def test_linear_coeff_vanishes_at_two_thirds():
    """Coef. linear-em-m de A_m é (3γ−2)/(2γ²); zero único em γ=2/3."""
    g = sp.Symbol('gamma', positive=True)
    lin_coeff = sp.Rational(3, 2)/g - 1/g**2
    sols = sp.solve(lin_coeff, g)
    assert len(sols) == 1 and sp.Rational(2, 3) in sols


def test_Am_monomial_at_two_thirds():
    """Em γ=2/3, A_m = −3m²/2 (monômio puro, sem termo linear)."""
    m, g = sp.Symbol('m', positive=True), sp.Rational(2, 3)
    A_sym = m*(m+3)/(2*g) - m*(m+1)/g**2
    assert sp.simplify(A_sym - (-3*m**2/2)) == 0


# ── verificações numéricas (numpy) ──────────────────────────────────

def test_partial_sum_closed_form():
    """Σ_{m=0}^M A_m(γ) bate com a fórmula cúbica fechada."""
    def partial_direct(M, g):
        return sum(_A(mv, g) for mv in range(M + 1))

    def partial_formula(M, g):
        s1 = M*(M+1)*(2*M+1)/6 + 3*M*(M+1)/2
        s2 = M*(M+1)*(2*M+1)/6 + M*(M+1)/2
        return s1/(2*g) - s2/g**2

    for M in [5, 10, 20, 50]:
        for g in [0.3, 0.5, 0.8]:
            np.testing.assert_allclose(
                partial_direct(M, g), partial_formula(M, g),
                rtol=1e-11, err_msg=f"M={M}, γ={g}")


def test_Am_strictly_negative_grid():
    """Sinal: A_m(γ)<0 para m∈[1,20], γ em grade fina de (0,1)."""
    for mv in range(1, 21):
        for g in np.linspace(0.01, 0.99, 200):
            assert _A(mv, g) < 0, f"m={mv}, γ={g:.4f}"


def test_Am_at_two_thirds_numpy():
    """Checagem float: A_m(2/3) = −3m²/2 para m=0..20."""
    g = 2.0/3.0
    for mv in range(21):
        np.testing.assert_allclose(
            _A(mv, g), -1.5*mv**2, atol=1e-12,
            err_msg=f"m={mv}")


def test_leading_negative_on_unit_interval():
    """λ²(γ−2)/(2γ²)<0 para todo γ∈(0,1) (matched-leading sempre negativo)."""
    for g in np.linspace(0.01, 0.99, 300):
        val = (g - 2) / (2 * g**2)
        assert val < 0, f"γ={g:.4f}"
