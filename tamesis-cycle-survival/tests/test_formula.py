"""
test_formula.py -- fast pytest suite cross-checking the analytic identities
of proofs/derivation.md against each other and against small brute-force /
Monte Carlo instances. Designed to run in well under a minute.

Run with:  pytest tests/test_formula.py -v
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.special import erf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "simulations"))

from asymptotics import (  # noqa: E402
    phi_inf_erf,
    phi_inf_series,
    phi_K_wallis,
)
from finite_n import (  # noqa: E402
    exact_phi_K,
    exact_phi_K1_formula,
    exact_phi_full,
)
from monte_carlo import count_cyclic_points, mc_estimate, phi_inf_formula  # noqa: E402


# ---------------------------------------------------------------------------
# 1. Series vs. integral (erf) vs. independent quadrature
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("c", [0.0, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
def test_series_matches_erf_form(c: float) -> None:
    a = phi_inf_erf(c)
    b = phi_inf_series(c)
    assert a == pytest.approx(b, abs=1e-9)


@pytest.mark.parametrize("c", [0.01, 0.5, 1.0, 5.0, 25.0, 100.0])
def test_erf_form_matches_independent_quadrature(c: float) -> None:
    a = phi_inf_erf(c)
    d, _ = quad(lambda t: math.exp(-c * t * t), 0.0, 1.0)
    assert a == pytest.approx(d, abs=1e-9)


def test_c_zero_is_one() -> None:
    assert phi_inf_erf(0.0) == 1.0


def test_phi_inf_is_monotonically_decreasing() -> None:
    cs = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
    vals = [phi_inf_erf(c) for c in cs]
    assert all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))


# ---------------------------------------------------------------------------
# 2. Tail asymptotic (Corollary 4.2)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("c", [10.0, 25.0, 50.0, 100.0])
def test_tail_asymptotic_within_rigorous_bound(c: float) -> None:
    exact = phi_inf_erf(c)
    lead = (math.sqrt(math.pi) / 2.0) * c ** -0.5
    R = lead - exact
    bound = math.exp(-c) / (2 * c)
    assert 0 <= R < bound + 1e-300  # generous epsilon guard for float underflow at large c


def test_tail_coefficient_is_sqrt_pi_over_2() -> None:
    A = math.sqrt(math.pi) / 2.0
    assert A == pytest.approx(0.8862269254527579, abs=1e-12)


# ---------------------------------------------------------------------------
# 3. Conditional-K law (Lemma 2, Wallis integral) vs. quadrature
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("K", range(0, 8))
def test_phi_K_wallis_matches_quadrature(K: int) -> None:
    a = phi_K_wallis(K)
    b, _ = quad(lambda t: (1 - t * t) ** K, 0.0, 1.0)
    assert a == pytest.approx(b, abs=1e-9)


def test_phi_K1_is_two_thirds() -> None:
    assert phi_K_wallis(1) == pytest.approx(2.0 / 3.0, abs=1e-12)


def test_phi_K_density_2x_integrates_to_one_and_has_correct_mean() -> None:
    """K=1 density f(x)=2x on (0,1), proved in proofs/derivation.md Lemma 2
    (K=1 case): normalizes to 1 and has mean phi_1=2/3."""
    norm, _ = quad(lambda x: 2 * x, 0.0, 1.0)
    mean, _ = quad(lambda x: x * 2 * x, 0.0, 1.0)
    assert norm == pytest.approx(1.0, abs=1e-9)
    assert mean == pytest.approx(2.0 / 3.0, abs=1e-9)


# ---------------------------------------------------------------------------
# 4. Poisson(c)-mixture of phi_K reproduces phi_inf(c) exactly
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("c", [0.5, 1.0, 3.0])
def test_poisson_mixture_of_phi_K_equals_phi_inf(c: float) -> None:
    total = 0.0
    log_term = -c
    for K in range(200):
        if K > 0:
            log_term += math.log(c) - math.log(K)
        p = math.exp(log_term)
        total += p * phi_K_wallis(K)
        if p < 1e-16 and K > c:
            break
    assert total == pytest.approx(phi_inf_erf(c), abs=1e-8)


# ---------------------------------------------------------------------------
# 5. Exact finite-n brute force vs. proved closed forms (Proposition 4)
# ---------------------------------------------------------------------------

def test_phi_n_K0_is_exactly_one() -> None:
    for n in (1, 2, 3, 5):
        assert exact_phi_K(n, 0) == 1


@pytest.mark.parametrize("n", range(1, 8))
def test_phi_n_K1_matches_closed_form_exactly(n: int) -> None:
    """Proposition 4: phi_n^(1) = 2/3 + 1/(3n^2) exactly, for every n."""
    assert exact_phi_K(n, 1) == exact_phi_K1_formula(n)


def test_phi_n_K1_converges_to_phi_1() -> None:
    for n in (10, 50, 200):
        val = float(exact_phi_K1_formula(n))
        assert abs(val - 2.0 / 3.0) < 1.0 / (3 * n * n) + 1e-12


def test_phi_n_K2_decreases_toward_phi_2() -> None:
    """No closed form is proved for K=2 (open lemma, proofs/derivation.md);
    this only checks the documented monotone-decreasing empirical trend
    toward phi_2=8/15 over a small range, matching the values reported in
    proofs/derivation.md's Open Lemma discussion."""
    vals = [float(exact_phi_K(n, 2)) for n in range(2, 6)]
    target = float(phi_K_wallis(2))
    assert all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    assert all(v > target for v in vals)


def test_exact_full_mixture_converges_toward_phi_inf() -> None:
    """Fact 4.1: exact phi(n,c) (full Binomial mixture over K) should get
    monotonically closer to phi_inf(c) as n grows, for fixed c."""
    c = 0.5
    diffs = [abs(exact_phi_full(n, c) - phi_inf_erf(c)) for n in (2, 3, 4)]
    assert diffs[0] > diffs[1] > diffs[2]


# ---------------------------------------------------------------------------
# 6. Small Monte Carlo vs. formula (statistical, seeded, generous tolerance)
# ---------------------------------------------------------------------------

def test_monte_carlo_matches_formula_within_tolerance() -> None:
    rng = np.random.default_rng(42)
    n = 4000
    trials = 250
    for c in (0.5, 2.0, 10.0):
        mean, sem = mc_estimate(n, c, trials, rng)
        target = phi_inf_formula(c)
        z = abs(mean - target) / sem
        assert z < 5.0, f"c={c}: MC mean {mean} vs target {target}, z={z}"


def test_count_cyclic_points_on_known_permutation() -> None:
    """A pure permutation (no reroutes): every point is cyclic."""
    n = 20
    rng = np.random.default_rng(7)
    perm = rng.permutation(n)
    assert count_cyclic_points(perm) == n


def test_count_cyclic_points_on_all_fixed_points() -> None:
    """The identity map: every point is a fixed point, hence cyclic."""
    n = 10
    f = np.arange(n)
    assert count_cyclic_points(f) == n


def test_count_cyclic_points_on_single_cycle_plus_tail() -> None:
    """f: 0->1->2->0 (a 3-cycle), 3->0, 4->3 (a tail feeding into the
    cycle). Cyclic points are exactly {0,1,2}."""
    f = np.array([1, 2, 0, 0, 3])
    assert count_cyclic_points(f) == 3
