"""Tests for the Monte Carlo Lab (`CHECKLIST_07_MONTE_CARLO_LAB.md`).

All estimators below independently target ``pi`` so ground truth is known
exactly:

- ``pi_square``: classic hit-or-miss — sample a point uniformly in the unit
  square, indicator scaled by 4 for whether it lands in the unit quarter
  circle.
- ``pi_integral``: a completely different sampling scheme — Monte Carlo
  integration of ``4*sqrt(1-x**2)`` over ``x in [0, 1]``, the area under the
  quarter-circle curve.
- ``pi_biased``: ``pi_square`` with a deliberate, constant ``+0.15`` bias
  baked into every sample, standing in for "samples from the wrong
  distribution" — the bias does not vanish as ``n_trials`` grows, which is
  exactly what should make it fail both triangulation and convergence.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pytest

from tamesis_discovery_engine.montecarlo import (
    ConvergenceResult,
    MonteCarloResult,
    TriangulationResult,
    convergence_check,
    run_estimator,
    triangulate,
)


def pi_square(rng: np.random.Generator) -> float:
    x, y = rng.random(2)
    return 4.0 if x * x + y * y <= 1.0 else 0.0


def pi_integral(rng: np.random.Generator) -> float:
    x = rng.random()
    return 4.0 * math.sqrt(max(0.0, 1.0 - x * x))


def pi_biased(rng: np.random.Generator) -> float:
    return pi_square(rng) + 0.15


class TestRunEstimator:
    def test_reproducible_across_calls_with_same_seed(self):
        result_a = run_estimator(pi_square, n_trials=20_000, seed=42)
        result_b = run_estimator(pi_square, n_trials=20_000, seed=42)

        assert result_a == result_b
        assert result_a.estimate == result_b.estimate
        assert result_a.stderr == result_b.stderr

    def test_estimate_within_a_few_stderrs_of_true_value(self):
        result = run_estimator(pi_square, n_trials=20_000, seed=42)

        assert isinstance(result, MonteCarloResult)
        assert result.n_trials == 20_000
        assert result.seed == 42
        assert abs(result.estimate - math.pi) <= 5.0 * result.stderr

    def test_different_seeds_give_different_estimates(self):
        result_a = run_estimator(pi_square, n_trials=2_000, seed=1)
        result_b = run_estimator(pi_square, n_trials=2_000, seed=2)

        assert result_a.estimate != result_b.estimate

    def test_rejects_n_trials_too_small_for_a_stderr(self):
        with pytest.raises(ValueError):
            run_estimator(pi_square, n_trials=1, seed=0)


class TestTriangulate:
    def test_independent_estimators_of_known_quantity_agree(self):
        result = triangulate(
            [("square", pi_square), ("integral", pi_integral)],
            n_trials=20_000,
            seed=1,
            tolerance=3.0,
        )

        assert isinstance(result, TriangulationResult)
        assert result.agrees is True
        assert result.diverging == []
        assert len(result.results) == 2
        names = [name for name, _ in result.results]
        assert names == ["square", "integral"]

    def test_biased_estimator_breaks_agreement_and_is_identified(self):
        result = triangulate(
            [("square", pi_square), ("integral", pi_integral), ("biased", pi_biased)],
            n_trials=20_000,
            seed=1,
            tolerance=3.0,
        )

        assert result.agrees is False
        assert result.diverging == ["biased"]

    def test_requires_at_least_two_estimators(self):
        with pytest.raises(ValueError):
            triangulate([("square", pi_square)], n_trials=1_000, seed=0, tolerance=3.0)

    def test_reproducible_across_calls_with_same_seed(self):
        result_a = triangulate(
            [("square", pi_square), ("integral", pi_integral)],
            n_trials=5_000,
            seed=9,
            tolerance=3.0,
        )
        result_b = triangulate(
            [("square", pi_square), ("integral", pi_integral)],
            n_trials=5_000,
            seed=9,
            tolerance=3.0,
        )

        assert result_a == result_b


class TestConvergenceCheck:
    SAMPLE_SIZES = [1_000, 10_000, 100_000]

    def test_consistent_estimator_converges_with_decreasing_error(self):
        result = convergence_check(
            pi_square,
            self.SAMPLE_SIZES,
            target=math.pi,
            tolerance=0.02,
            seed=4,
        )

        assert isinstance(result, ConvergenceResult)
        assert result.converged is True
        assert result.sample_sizes == self.SAMPLE_SIZES
        assert len(result.errors) == 3
        assert result.errors[-1] <= 0.02
        assert result.errors[-1] < result.errors[0]

    def test_biased_estimator_does_not_converge(self):
        result = convergence_check(
            pi_biased,
            self.SAMPLE_SIZES,
            target=math.pi,
            tolerance=0.02,
            seed=4,
        )

        assert result.converged is False
        assert all(error > 0.02 for error in result.errors)

    def test_requires_at_least_two_sample_sizes(self):
        with pytest.raises(ValueError):
            convergence_check(pi_square, [1_000], target=math.pi, tolerance=0.02, seed=0)

    def test_requires_strictly_increasing_sample_sizes(self):
        with pytest.raises(ValueError):
            convergence_check(
                pi_square, [10_000, 1_000], target=math.pi, tolerance=0.02, seed=0
            )

    def test_reproducible_across_calls_with_same_seed(self):
        result_a = convergence_check(
            pi_square, self.SAMPLE_SIZES, target=math.pi, tolerance=0.02, seed=4
        )
        result_b = convergence_check(
            pi_square, self.SAMPLE_SIZES, target=math.pi, tolerance=0.02, seed=4
        )

        assert result_a == result_b


class TestNoUnseededGlobalRandom:
    def test_module_never_touches_np_random_without_a_seed_argument(self):
        module_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "tamesis_discovery_engine"
            / "montecarlo.py"
        )
        source = module_path.read_text()
        code_lines = [
            line for line in source.splitlines() if not line.strip().startswith("#")
        ]
        code = "\n".join(code_lines)

        forbidden = re.compile(
            r"\bnp\.random\.(?!default_rng\(|Generator\b)"
        )
        violations = forbidden.findall(code)
        assert violations == [], f"unseeded np.random usage found: {violations}"
