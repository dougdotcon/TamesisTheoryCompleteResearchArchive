"""Tests for the Mathematical Discovery Engine (`CHECKLIST_12_MATHEMATICAL_DISCOVERY_ENGINE.md`).

Toy problem: Q(n) = sum_{i=1}^{n} i**2, the sum of the first n squares.

Three genuinely independent pieces of evidence about Q are used, each
implemented without deriving one from another:

- ``exact_sum_of_squares``: the enumerator, a direct brute-force Python
  loop — no algebra at all.
- ``make_uniform_reweight_estimator``: the Monte Carlo estimator, using the
  standard "estimate a finite sum by reweighted uniform sampling" trick
  (``E[n * f(I)] = sum_i f(i)`` for ``I`` uniform on ``{1, ..., n}``) — a
  sampling technique unrelated to both the closed-form algebra and the
  brute-force loop.
- ``sympy.summation``: an independent symbolic derivation of the same
  closed form, used as ``symbolic_target``.

Candidates:

- ``true_factored``: ``n*(n+1)*(2*n+1)/6`` — the standard closed form.
- ``true_expanded``: ``(2*n**3 + 3*n**2 + n)/6`` — algebraically identical,
  written differently (tests that symbolic equivalence, not textual
  equality, is what matters).
- ``wrong_leading_order``: ``n**3/3`` — the correct *leading-order*
  asymptotic term but the wrong exact formula: it is refuted by the exact
  stages (enumeration, symbolic, Monte Carlo at a finite n) while still
  passing the asymptotic-fit stage, which is exactly what an asymptotic
  approximation should do and demonstrates genuine per-stage attribution
  rather than a single bare pass/fail.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import sympy

from tamesis_discovery_engine.mathematical_discovery_engine import (
    AsymptoticCheck,
    CandidateResult,
    Enumerator,
    MathDiscoveryPipeline,
    MonteCarloCheck,
)

n = sympy.Symbol("n")
i = sympy.Symbol("i")

TRUE_FACTORED = n * (n + 1) * (2 * n + 1) / 6
TRUE_EXPANDED = (2 * n**3 + 3 * n**2 + n) / 6
WRONG_LEADING_ORDER = n**3 / 3

SYMBOLIC_TARGET = sympy.summation(i**2, (i, 1, n))

ENUMERATOR_NS = list(range(0, 7))


def exact_sum_of_squares(k: int) -> int:
    total = 0
    for value in range(1, k + 1):
        total += value * value
    return total


def make_uniform_reweight_estimator(k: int):
    def estimator(rng: np.random.Generator) -> float:
        sample = int(rng.integers(1, k + 1))
        return float(k * sample * sample)

    return estimator


def default_enumerator() -> Enumerator:
    return Enumerator(fn=exact_sum_of_squares, ns=ENUMERATOR_NS, symbol="n")


def default_mc_check(k: int = 20, n_trials: int = 20_000, seed: int = 7) -> MonteCarloCheck:
    return MonteCarloCheck(
        estimators=[("uniform_reweight", make_uniform_reweight_estimator(k))],
        substitution={"n": k},
        n_trials=n_trials,
        seed=seed,
        tolerance=3.0,
    )


def default_asymptotic_check() -> AsymptoticCheck:
    return AsymptoticCheck(
        target=lambda k: k**3 / 3,
        ns=[1_000, 10_000, 100_000],
        symbol="n",
        tolerance=1e-2,
    )


def full_kwargs():
    return dict(
        free_symbols=[n],
        symbolic_target=SYMBOLIC_TARGET,
        enumerator=default_enumerator(),
        mc_estimators=default_mc_check(),
        asymptotic_target=default_asymptotic_check(),
    )


class TestSingleTrueCandidateAllFourStages:
    def test_true_candidate_survives_with_every_stage_agreeing(self):
        pipeline = MathDiscoveryPipeline()

        result = pipeline.run_candidate("true_factored", TRUE_FACTORED, **full_kwargs())

        assert isinstance(result, CandidateResult)
        assert result.enumeration_match is True
        assert result.symbolic_match is True
        assert result.mc_triangulates is True
        assert result.asymptotic_fit_residual is not None
        assert result.asymptotic_fit_residual <= default_asymptotic_check().tolerance
        assert result.verdict == "SURVIVES"
        assert set(result.details) == {"enumeration", "symbolic", "mc", "asymptotic"}


class TestDeliberatelyWrongCandidateIsCaughtWithAttribution:
    def test_wrong_candidate_is_refuted_and_stage_attribution_is_visible(self):
        pipeline = MathDiscoveryPipeline()

        result = pipeline.run_candidate("wrong_leading_order", WRONG_LEADING_ORDER, **full_kwargs())

        assert result.verdict == "REFUTED"
        # caught by the exact stages...
        assert result.enumeration_match is False
        assert result.symbolic_match is False
        assert result.mc_triangulates is False
        # ...specifically, not just "some bare False somewhere": the detail
        # strings name which n / which estimator / which method disagreed.
        assert "n=" in result.details["enumeration"] or "mismatch" in result.details["enumeration"]
        assert "candidate" in result.details["mc"]
        assert result.details["symbolic"]
        # ...while the asymptotic stage, correctly, does NOT catch it: n**3/3
        # is exactly the correct leading-order term.
        assert result.asymptotic_fit_residual is not None
        assert result.asymptotic_fit_residual <= default_asymptotic_check().tolerance


class TestOnlySymbolicStageSupplied:
    def test_true_candidate_survives_from_symbolic_alone_other_fields_stay_none(self):
        pipeline = MathDiscoveryPipeline()

        result = pipeline.run_candidate(
            "true_expanded",
            TRUE_EXPANDED,
            free_symbols=[n],
            symbolic_target=SYMBOLIC_TARGET,
        )

        assert result.symbolic_match is True
        assert result.verdict == "SURVIVES"
        assert result.enumeration_match is None
        assert result.mc_triangulates is None
        assert result.asymptotic_fit_residual is None
        assert set(result.details) == {"symbolic"}

    def test_wrong_candidate_is_refuted_from_symbolic_alone_other_fields_stay_none(self):
        pipeline = MathDiscoveryPipeline()

        result = pipeline.run_candidate(
            "wrong_leading_order",
            WRONG_LEADING_ORDER,
            free_symbols=[n],
            symbolic_target=SYMBOLIC_TARGET,
        )

        assert result.symbolic_match is False
        assert result.verdict == "REFUTED"
        assert result.enumeration_match is None
        assert result.mc_triangulates is None
        assert result.asymptotic_fit_residual is None


class TestNoStageSuppliedIsInconclusiveNeverSurvives:
    def test_zero_stages_run_reports_inconclusive_not_survives(self):
        pipeline = MathDiscoveryPipeline()

        result = pipeline.run_candidate("unchecked", TRUE_FACTORED)

        assert result.enumeration_match is None
        assert result.symbolic_match is None
        assert result.mc_triangulates is None
        assert result.asymptotic_fit_residual is None
        assert result.verdict == "INCONCLUSIVE"
        assert result.details == {}


class TestRunSeparatesSeveralCandidates:
    def test_run_with_two_true_forms_and_one_wrong_form_separates_them(self):
        pipeline = MathDiscoveryPipeline()

        results = pipeline.run(
            [
                ("true_factored", TRUE_FACTORED),
                ("true_expanded", TRUE_EXPANDED),
                ("wrong_leading_order", WRONG_LEADING_ORDER),
            ],
            free_symbols=[n],
            symbolic_target=SYMBOLIC_TARGET,
            enumerator=default_enumerator(),
        )

        assert [r.candidate_name for r in results] == [
            "true_factored",
            "true_expanded",
            "wrong_leading_order",
        ]
        assert results[0].verdict == "SURVIVES"
        assert results[1].verdict == "SURVIVES"
        assert results[2].verdict == "REFUTED"
        assert results[0].enumeration_match is True
        assert results[1].enumeration_match is True
        assert results[2].enumeration_match is False


class TestToyProblemEvidenceIsIndependentlyImplemented:
    def test_enumerator_matches_closed_form_by_direct_computation(self):
        for k in ENUMERATOR_NS:
            assert exact_sum_of_squares(k) == sum(v * v for v in range(1, k + 1))

    def test_uniform_reweight_estimator_is_unbiased_for_the_same_quantity(self):
        k = 20
        estimator = make_uniform_reweight_estimator(k)
        rng = np.random.default_rng(123)
        samples = [estimator(rng) for _ in range(50_000)]
        estimate = sum(samples) / len(samples)

        exact = exact_sum_of_squares(k)
        assert abs(estimate - exact) / exact < 0.02

    def test_enumerator_and_estimator_disagree_when_the_true_value_is_wrong(self):
        # Sanity check that the two independent evidence sources actually
        # measure the same thing: they must not both happen to endorse the
        # wrong leading-order candidate at a finite, small n.
        k = 20
        wrong_value = float(WRONG_LEADING_ORDER.subs(n, k))
        assert exact_sum_of_squares(k) != wrong_value


class TestReusesModule6And7NotReimplemented:
    SOURCE = (
        Path(__file__).resolve().parent.parent
        / "src"
        / "tamesis_discovery_engine"
        / "mathematical_discovery_engine.py"
    ).read_text()

    def test_imports_symbolic_and_montecarlo(self):
        assert "from .symbolic import verify_identity, verify_numeric_spot_check" in self.SOURCE
        assert "from .montecarlo import" in self.SOURCE

    def test_no_direct_sympy_simplify_or_equals_reimplementation(self):
        assert "sympy.simplify(" not in self.SOURCE
        assert ".equals(" not in self.SOURCE

    def test_no_direct_rng_estimator_loop_reimplementation(self):
        assert "default_rng" not in self.SOURCE
        assert "np.mean(" not in self.SOURCE
        assert "np.std(" not in self.SOURCE
