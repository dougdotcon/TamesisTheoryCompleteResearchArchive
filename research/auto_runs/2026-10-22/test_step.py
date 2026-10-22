import pytest
import sympy as sp
from sympy import Rational as Q, symbols, simplify
import numpy as np


def A_m(m, gamma):
    """A_m(gamma) = m(m+3)/(2*gamma) - m(m+1)/gamma**2."""
    return m * (m + 3) / (2 * gamma) - m * (m + 1) / gamma**2


# --- 1. Reproduce Stage 60 known checks (baseline) ---

def test_A0_vanishes():
    g = symbols('gamma', positive=True)
    assert simplify(A_m(0, g)) == 0


def test_neg_gamma_A1_equals_c_gamma():
    g = symbols('gamma', positive=True)
    c_gamma = 2 * (1 - g) / g
    assert simplify(-g * A_m(1, g) - c_gamma) == 0


# --- 2. Partial-sum closed form (NEW, not in Stage 60) ---

def test_partial_sum_closed_form():
    """Sum_{m=0}^{M} A_m(gamma) = M(M+1)*[(M+5)*gamma - 2*(M+2)] / (6*gamma**2)."""
    gammas = [Q(3, 10), Q(1, 2), Q(4, 5), Q(1, 1), Q(3, 2), Q(5, 1)]
    for M in [0, 1, 2, 3, 5, 10, 25, 50]:
        for gv in gammas:
            direct = sum(A_m(m, gv) for m in range(M + 1))
            closed = Q(M * (M + 1)) * (Q(M + 5) * gv - 2 * Q(M + 2)) / (6 * gv**2)
            assert direct == closed, f"M={M}, gamma={gv}: {direct} != {closed}"


# --- 3. Large-M cubic scaling ---

def test_partial_sum_cubic_scaling():
    """Sum A_m / M**3 -> (gamma-2)/(6*gamma**2) as M -> inf."""
    for gamma in [0.3, 0.5, 0.8, 1.0, 1.5, 3.0]:
        target = (gamma - 2) / (6 * gamma**2)
        for M in [200, 1000]:
            S = sum(float(A_m(m, gamma)) for m in range(M + 1))
            ratio = S / M**3
            assert abs(ratio - target) < 15.0 / M, \
                f"gamma={gamma}, M={M}: ratio={ratio:.8e}, target={target:.8e}"


# --- 4. Second difference is constant (A_m quadratic in m) ---

def test_second_difference_constant():
    """Delta^2 A_m = 1/gamma - 2/gamma**2, independent of m."""
    g = symbols('gamma', positive=True)
    expected = 1 / g - 2 / g**2
    for m_val in range(0, 15):
        d2 = A_m(m_val + 2, g) - 2 * A_m(m_val + 1, g) + A_m(m_val, g)
        assert simplify(d2 - expected) == 0, \
            f"Delta^2 A at m={m_val} != 1/gamma - 2/gamma^2"


def test_second_difference_vanishes_at_gamma_2():
    """At gamma=2, Delta^2 A_m = 0 => A_m is LINEAR in m.
    Indeed A_m(2) = m/2."""
    for m in range(0, 51):
        val = float(A_m(m, 2.0))
        assert abs(val - m / 2.0) < 1e-12, \
            f"A_{m}(2) = {val}, expected {m/2}"


# --- 5. Zero locus gamma*(m) = 2(m+1)/(m+3) ---

def test_zero_locus_and_monotonicity():
    prev = 0.0
    for m in range(1, 201):
        gs = 2.0 * (m + 1) / (m + 3)
        assert abs(A_m(m, gs)) < 1e-12, f"A_{m}({gs}) != 0"
        assert gs > prev, f"gamma* not increasing at m={m}"
        prev = gs
    # Limit -> 2
    assert abs(prev - 2.0) < 0.02, f"gamma*(200) = {prev}, not near 2"


# --- 6. Sign structure in physical range ---

def test_A_m_negative_in_physical_range():
    """For gamma in (0,1) and m >= 1, A_m < 0 always
    (since gamma*(m) >= 1 for m >= 1)."""
    for gamma in [0.05, 0.1, 0.25, 0.5, 0.75, 0.99]:
        for m in range(1, 101):
            val = float(A_m(m, gamma))
            assert val < 0, f"A_{m}({gamma}) = {val} >= 0"


# --- 7. Rates at special gamma values ---

def test_rate_at_gamma_half():
    """-gamma * A_m(1/2) = m(3m+1)/2."""
    g = Q(1, 2)
    for m in range(0, 21):
        rate = -g * A_m(m, g)
        expected = Q(m * (3 * m + 1), 2)
        assert rate == expected, f"m={m}: {rate} != {expected}"


def test_rate_at_gamma_one():
    """-gamma * A_m(1) = m(m-1)/2 (triangular numbers)."""
    for m in range(0, 21):
        val = float(-1.0 * A_m(m, 1.0))
        expected = m * (m - 1) / 2.0
        assert abs(val - expected) < 1e-12, \
            f"m={m}: {val} != {expected}"


def test_rate_at_gamma_two():
    """-gamma * A_m(2) = -m."""
    for m in range(0, 21):
        val = float(-2.0 * A_m(m, 2.0))
        assert abs(val - (-m)) < 1e-12, \
            f"m={m}: -2*A_{m}(2) = {val} != {-m}"
