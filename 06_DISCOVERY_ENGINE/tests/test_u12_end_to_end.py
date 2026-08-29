"""The required Stage 1 benchmark: reproduce U1/2 end-to-end via the engine.

Per ``CHECKLIST_00_INTEGRATION_AND_VALIDATION.md``, this drives one claim
through the *entire* :class:`~tamesis_discovery_engine.DiscoveryEngine`
lifecycle — ``register -> advance(PRE_REGISTERED) -> lock -> run ->
reproduce -> review -> record_verdict`` — with the locked test plan calling
into ``benchmarks/u12_hypothesis.py``'s brute-force and Monte Carlo
functions (never pre-computed numbers), and asserts at the end that the
independently-computed values agree with THEOREM.md's stated closed forms
for all four items ``ROADMAP.md`` Section 3 requires: ``phi_infinity(c)``,
the ``M_K`` distribution (``K=1``), a finite-`n` correction term, and the
``gamma = c/n`` scaling regime.

The two ``TestPlan``/``ReproductionPlan`` callables below
(``run_u12_benchmark`` and ``run_u12_benchmark_independent``) are wrappers
around the independent benchmark module, kept local to this test file (the
same pattern ``tests/test_reproduction.py`` and ``tests/test_adversarial.py``
use for their own test-plan callables) — the actual combinatorics live in
``benchmarks/u12_hypothesis.py``, never in the engine's own modules.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest
from scipy import stats

import u12_hypothesis as bench

from tamesis_discovery_engine import DiscoveryEngine
from tamesis_discovery_engine.adversarial import SUCCESS_THRESHOLD_KEY, format_threshold_note
from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.reproduction import ReproductionPlan
from tamesis_discovery_engine.runner import TestPlan

from .conftest import FakeClock

# ---------------------------------------------------------------------------
# Locked parameters (declared once, at PRE_REGISTERED/LOCK time, reused
# verbatim by every step — including reproduce()'s reseeded rerun below).
# ---------------------------------------------------------------------------

PARAMS = dict(
    seed=0,
    brute_force_n_values=(2, 3, 4, 5, 6),
    mc_phi_n=3000,
    mc_phi_trials=3000,
    mc_phi_c_values=(1.0, 3.0),
    m1_n=3000,
    m1_trials=3000,
    gamma=0.5,
    n_small_gamma=200,
    n_large_gamma=6000,
    gamma_trials=8000,
)

DECLARED_THRESHOLD = {
    "phi_infinity_mc_abs_tolerance": 0.02,
    "m1_ks_pvalue_min": 0.01,
    "finite_n_correction_abs_tolerance": 1e-9,
    "gamma_scaling_large_n_abs_tolerance": 0.02,
}


def run_u12_benchmark(
    seed,
    brute_force_n_values,
    mc_phi_n,
    mc_phi_trials,
    mc_phi_c_values,
    m1_n,
    m1_trials,
    gamma,
    n_small_gamma,
    n_large_gamma,
    gamma_trials,
):
    """The locked test plan: computes every candidate value from scratch.

    Calls ``benchmarks/u12_hypothesis.py``'s brute-force exact enumeration
    (:func:`bench.brute_force_phi_n_K`) and Monte Carlo simulator
    (:func:`bench.monte_carlo_phi`, :func:`bench.monte_carlo_cyclic_mass_samples`)
    — never a pre-computed number. Nothing in this function references any
    of THEOREM.md's stated closed forms; those are only introduced in this
    test module's final assertions, after ``review``/``record_verdict``.
    """

    rng = np.random.default_rng(seed)

    brute_force_phi_n1 = {
        str(n): float(bench.brute_force_phi_n_K(n, 1)) for n in brute_force_n_values
    }

    mc_phi_infinity = {}
    for c in mc_phi_c_values:
        mean, se = bench.monte_carlo_phi(mc_phi_n, c, mc_phi_trials, rng)
        mc_phi_infinity[str(c)] = {"mean": mean, "se": se}

    m1_samples = bench.monte_carlo_cyclic_mass_samples(m1_n, 1, m1_trials, rng)
    ks = stats.kstest(m1_samples, bench.m1_cdf)

    c_small = gamma * n_small_gamma
    c_large = gamma * n_large_gamma
    mean_small, _ = bench.monte_carlo_phi(n_small_gamma, c_small, gamma_trials, rng)
    mean_large, _ = bench.monte_carlo_phi(n_large_gamma, c_large, gamma_trials, rng)

    return {
        "brute_force_phi_n1": brute_force_phi_n1,
        "mc_phi_infinity": mc_phi_infinity,
        "m1_mean": float(m1_samples.mean()),
        "m1_ks_statistic": float(ks.statistic),
        "m1_ks_pvalue": float(ks.pvalue),
        "gamma_phi_small_n": mean_small,
        "gamma_phi_large_n": mean_large,
    }


def run_u12_benchmark_independent(
    seed,
    brute_force_n_values,
    mc_phi_n,
    mc_phi_trials,
    mc_phi_c_values,
    m1_n,
    m1_trials,
    gamma,
    n_small_gamma,
    n_large_gamma,
    gamma_trials,
):
    """A second, independently-written implementation for the reproduce() step.

    The brute-force half uses :func:`bench.brute_force_phi_n_K_second_algorithm`
    — a differently-structured exact enumeration (dict-based functional graph,
    explicit per-point traversal instead of in-degree peeling) over the same
    Definition 1/4 primitives, per the checklist's "a different enumeration
    order/algorithm for the same combinatorial definition." The Monte Carlo
    half reruns the *same* declared params (as ``Reproducer.reproduce``
    always does — see ``reproduction.py``'s module docstring) through
    :func:`bench.cyclic_mask_via_coloring`, an algorithmically different
    cyclic-point detector (forward path-following/three-coloring instead of
    in-degree peeling) applied to the same seeded random draws.
    """

    rng = np.random.default_rng(seed)

    brute_force_phi_n1 = {
        str(n): float(bench.brute_force_phi_n_K_second_algorithm(n, 1)) for n in brute_force_n_values
    }

    mc_phi_infinity = {}
    for c in mc_phi_c_values:
        mean, se = bench.monte_carlo_phi(
            mc_phi_n, c, mc_phi_trials, rng, cyclic_detector=bench.cyclic_mask_via_coloring
        )
        mc_phi_infinity[str(c)] = {"mean": mean, "se": se}

    m1_samples = bench.monte_carlo_cyclic_mass_samples(
        m1_n, 1, m1_trials, rng, cyclic_detector=bench.cyclic_mask_via_coloring
    )
    ks = stats.kstest(m1_samples, bench.m1_cdf)

    c_small = gamma * n_small_gamma
    c_large = gamma * n_large_gamma
    mean_small, _ = bench.monte_carlo_phi(
        n_small_gamma, c_small, gamma_trials, rng, cyclic_detector=bench.cyclic_mask_via_coloring
    )
    mean_large, _ = bench.monte_carlo_phi(
        n_large_gamma, c_large, gamma_trials, rng, cyclic_detector=bench.cyclic_mask_via_coloring
    )

    return {
        "brute_force_phi_n1": brute_force_phi_n1,
        "mc_phi_infinity": mc_phi_infinity,
        "m1_mean": float(m1_samples.mean()),
        "m1_ks_statistic": float(ks.statistic),
        "m1_ks_pvalue": float(ks.pvalue),
        "gamma_phi_small_n": mean_small,
        "gamma_phi_large_n": mean_large,
    }


def test_u12_hypothesis_end_to_end_via_discovery_engine(tmp_path):
    clock = FakeClock()
    engine = DiscoveryEngine(data_dir=tmp_path / "data", clock=clock)

    # ---- 1. register() ----------------------------------------------------
    claim = engine.register(
        "U1/2 permutation-with-reroutes limit law",
        "phi_infinity(c) = (1/2) sqrt(pi/c) erf(sqrt(c)) as n -> infinity, "
        "for the u12 permutation-with-Poisson-reroutes ensemble.",
        metadata={SUCCESS_THRESHOLD_KEY: DECLARED_THRESHOLD},
    )
    assert claim.state is ClaimState.DRAFT

    # ---- 2. advance() to PRE_REGISTERED with a declared threshold --------
    claim = engine.advance(
        claim.id, ClaimState.PRE_REGISTERED, note=format_threshold_note(DECLARED_THRESHOLD)
    )
    assert claim.state is ClaimState.PRE_REGISTERED

    # ---- 3. advance() to LOCKED, run() calling into the benchmark --------
    test_plan = TestPlan(name="u12-benchmark", version="v1", fn=run_u12_benchmark, params=dict(PARAMS))
    claim = engine.lock(claim.id, test_plan)
    assert claim.state is ClaimState.LOCKED

    run_record = engine.run(claim.id, test_plan)
    assert run_record.success is True
    assert engine.get(claim.id).state is ClaimState.RESULT

    result = run_record.result

    # ---- 4. reproduce() with a second, independent implementation --------
    repro_record = engine.reproduce(
        claim.id,
        ReproductionPlan(name="u12-benchmark-independent", version="v1", fn=run_u12_benchmark_independent),
        tolerance=1e-6,
    )
    assert repro_record.verdict in ("EXACT_MATCH", "MATCH_WITHIN_TOLERANCE"), (
        repro_record.verdict,
        [d.to_dict() for d in repro_record.deltas],
    )

    # ---- 5. review() then record_verdict() --------------------------------
    verdict = engine.review(claim.id)
    assert engine.get(claim.id).state is ClaimState.ADVERSARIAL_REVIEW
    assert not any(flag.severity == "ERROR" for flag in verdict.flags), verdict.flags

    final_claim = engine.record_verdict(
        claim.id,
        ClaimState.CONFIRMED,
        "Independent brute-force + Monte Carlo computation matches THEOREM.md's "
        "phi_infinity(c), M_1 density, finite-n correction, and gamma-scaling "
        "closed forms within the pre-registered thresholds; reproduced by a "
        "second, differently-algorithmed implementation.",
    )
    assert final_claim.state is ClaimState.CONFIRMED
    assert engine.ledger.verify_chain() is True

    # ---- 6. Assert the four required checks against THEOREM.md's closed forms ----

    # (a) phi_infinity(c): brute-force/MC vs. the formula.
    for c_key in ("1.0", "3.0"):
        c = float(c_key)
        mc_mean = result["mc_phi_infinity"][c_key]["mean"]
        target = bench.phi_infinity(c)
        assert mc_mean == pytest.approx(target, abs=DECLARED_THRESHOLD["phi_infinity_mc_abs_tolerance"]), (
            c,
            mc_mean,
            target,
        )

    # (b) The M_K distribution for K=1: f_{M_1}(x) = 2x, i.e. F_{M_1}(x) = x^2
    #     (THEOREM.md section 5.3, proved, not the K>=2 conjecture).
    assert result["m1_ks_pvalue"] > DECLARED_THRESHOLD["m1_ks_pvalue_min"], result["m1_ks_pvalue"]
    assert result["m1_mean"] == pytest.approx(bench.phi_K_mean(1), abs=0.02)

    # (c) A finite-n correction term: phi_n^(1) = 2/3 + 1/(3n^2) (Proposition 4),
    #     exact brute-force enumeration against the exact closed form.
    for n in PARAMS["brute_force_n_values"]:
        exact_value = Fraction(bench.brute_force_phi_n_K(n, 1))
        target_value = Fraction(2, 3) + Fraction(1, 3 * n * n)
        assert exact_value == target_value, (n, exact_value, target_value)
        assert result["brute_force_phi_n1"][str(n)] == pytest.approx(
            bench.phi_n_1_closed_form(n), abs=DECLARED_THRESHOLD["finite_n_correction_abs_tolerance"]
        )

    # (d) The gamma = c/n scaling regime: phi(n, gamma*n)/phi_infinity(gamma*n)
    #     -> sqrt(2/(2-gamma)), confirmed in the right direction as n grows.
    gamma = PARAMS["gamma"]
    target_ratio = bench.gamma_scaling_target(gamma)
    c_small = gamma * PARAMS["n_small_gamma"]
    c_large = gamma * PARAMS["n_large_gamma"]
    ratio_small = result["gamma_phi_small_n"] / bench.phi_infinity(c_small)
    ratio_large = result["gamma_phi_large_n"] / bench.phi_infinity(c_large)

    assert ratio_small > 1.0
    assert ratio_large > 1.0
    err_small = abs(ratio_small - target_ratio)
    err_large = abs(ratio_large - target_ratio)
    assert err_large < err_small, (ratio_small, ratio_large, target_ratio)
    assert err_large < DECLARED_THRESHOLD["gamma_scaling_large_n_abs_tolerance"], (ratio_large, target_ratio)
