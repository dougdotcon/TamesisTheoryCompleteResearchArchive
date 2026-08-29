import pytest

from tamesis_discovery_engine.adversarial import (
    CHECK_LEAKAGE,
    CHECK_NUMERICAL_INSTABILITY,
    CHECK_OVERFITTING,
    CHECK_POST_HOC_THRESHOLD,
    SUCCESS_THRESHOLD_KEY,
    AdversarialReviewer,
    EmptyRationaleError,
    InvalidVerdictError,
    ReviewPreconditionError,
    VerdictWithoutReviewError,
    format_threshold_note,
)
from tamesis_discovery_engine.claim import ClaimState, IllegalTransitionError
from tamesis_discovery_engine.registry import Registry
from tamesis_discovery_engine.reproduction import Reproducer, ReproductionPlan
from tamesis_discovery_engine.runner import Runner, TestPlan

from .conftest import FakeClock


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def make_runner(tmp_path, registry, clock=None):
    return Runner(registry, data_dir=tmp_path / "runs", clock=clock or FakeClock())


def make_reproducer(tmp_path, registry, runner, clock=None):
    return Reproducer(registry, runner, data_dir=tmp_path / "reproductions", clock=clock or FakeClock())


def make_reviewer(tmp_path, registry, runner, reproducer, clock=None):
    return AdversarialReviewer(
        registry, runner, reproducer, data_dir=tmp_path / "reviews", clock=clock or FakeClock()
    )


def make_ready_claim(
    tmp_path,
    registry,
    runner,
    reproducer,
    fn,
    params,
    metadata=None,
    pre_reg_note="",
    name="original",
    version="v1",
):
    """Build a claim that is locked, run, and successfully reproduced.

    This is the shared setup every review()-level test needs: review()'s
    enforced precondition is a successful reproduction on file, so every
    fixture below reproduces against the very same ``fn`` it ran (an exact
    match) purely to clear that gate before exercising a specific check.
    """

    claim = registry.create("Reviewable claim", "A claim with a completed run.", metadata=metadata)
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED, note=pre_reg_note)
    test_plan = TestPlan(name=name, version=version, fn=fn, params=params)
    runner.lock(claim.id, test_plan)
    run_record = runner.run(claim.id, test_plan)
    reproducer.reproduce(claim.id, ReproductionPlan(name="repro", version="v1", fn=fn), tolerance=1e-9)
    return claim, run_record, test_plan


def const_fn(x):
    return {"value": x}


# ---------------------------------------------------------------------------
# Check 1: post-hoc threshold
# ---------------------------------------------------------------------------


def test_check1_missing_threshold_is_flagged(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(
        tmp_path, registry, runner, reproducer, const_fn, {"x": 1.0}, metadata=None
    )

    verdict = reviewer.review(claim.id)

    threshold_flags = [f for f in verdict.flags if f.check == CHECK_POST_HOC_THRESHOLD]
    assert len(threshold_flags) == 1
    assert CHECK_POST_HOC_THRESHOLD in verdict.all_checks_run
    assert verdict.recommendation == "FLAGGED"


def test_check1_declared_and_unaltered_threshold_passes_clean(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(
        tmp_path,
        registry,
        runner,
        reproducer,
        const_fn,
        {"x": 1.0},
        metadata={SUCCESS_THRESHOLD_KEY: 0.05},
        pre_reg_note=format_threshold_note(0.05),
    )

    verdict = reviewer.review(claim.id)

    threshold_flags = [f for f in verdict.flags if f.check == CHECK_POST_HOC_THRESHOLD]
    assert threshold_flags == []
    assert CHECK_POST_HOC_THRESHOLD in verdict.all_checks_run

    # No seed/n_params/leakage params were declared for this fixture, so those
    # three checks are honestly reported as skipped rather than silently clean.
    assert verdict.recommendation == "CLEAN"
    skip_names = {s.check for s in verdict.skipped_checks}
    assert skip_names == {CHECK_NUMERICAL_INSTABILITY, CHECK_OVERFITTING, CHECK_LEAKAGE}


def test_check1_threshold_edited_after_locking_is_flagged(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(
        tmp_path,
        registry,
        runner,
        reproducer,
        const_fn,
        {"x": 1.0},
        metadata={SUCCESS_THRESHOLD_KEY: 0.05},
        pre_reg_note=format_threshold_note(0.05),
    )

    # Simulate an out-of-band edit to the claim's metadata after locking —
    # exactly the tampering this check exists to catch. Registry itself
    # exposes no public API to edit metadata post-creation, so the fixture
    # reaches into the same JSON store Registry writes to.
    tampered = registry.get(claim.id)
    tampered.metadata[SUCCESS_THRESHOLD_KEY] = 0.50
    registry._save(tampered)

    verdict = reviewer.review(claim.id)

    threshold_flags = [f for f in verdict.flags if f.check == CHECK_POST_HOC_THRESHOLD]
    assert len(threshold_flags) == 1
    assert "0.05" in threshold_flags[0].detail
    assert "0.5" in threshold_flags[0].detail


# ---------------------------------------------------------------------------
# Check 2: numerical instability
# ---------------------------------------------------------------------------


def test_check2_seed_sensitive_result_is_flagged(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def seed_sensitive_fn(seed, n):
        return {"value": float(seed) * 1000.0}

    claim, _, test_plan = make_ready_claim(
        tmp_path, registry, runner, reproducer, seed_sensitive_fn, {"seed": 1, "n": 10}
    )

    verdict = reviewer.review(claim.id, test_plan=test_plan)

    instability_flags = [f for f in verdict.flags if f.check == CHECK_NUMERICAL_INSTABILITY]
    assert len(instability_flags) == 1
    assert CHECK_NUMERICAL_INSTABILITY in verdict.all_checks_run
    assert not any(s.check == CHECK_NUMERICAL_INSTABILITY for s in verdict.skipped_checks)


def test_check2_seed_stable_result_passes_clean(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def seed_stable_fn(seed, n):
        return {"value": 42.0}

    claim, _, test_plan = make_ready_claim(
        tmp_path, registry, runner, reproducer, seed_stable_fn, {"seed": 1, "n": 10}
    )

    verdict = reviewer.review(claim.id, test_plan=test_plan)

    instability_flags = [f for f in verdict.flags if f.check == CHECK_NUMERICAL_INSTABILITY]
    assert instability_flags == []
    assert CHECK_NUMERICAL_INSTABILITY in verdict.all_checks_run


def test_check2_no_seed_param_is_skipped_not_silently_passed(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def no_seed_fn(x):
        return {"value": x * 2}

    claim, _, test_plan = make_ready_claim(tmp_path, registry, runner, reproducer, no_seed_fn, {"x": 3})

    verdict = reviewer.review(claim.id, test_plan=test_plan)

    assert CHECK_NUMERICAL_INSTABILITY not in verdict.all_checks_run
    skip_names = {s.check for s in verdict.skipped_checks}
    assert CHECK_NUMERICAL_INSTABILITY in skip_names


# ---------------------------------------------------------------------------
# Check 3: overfitting / parameter-count smell
# ---------------------------------------------------------------------------


def test_check3_n_params_gte_n_samples_is_flagged(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def overfit_fn(n_params, n_samples):
        return {"n_params": n_params, "n_samples": n_samples, "score": 1.0}

    claim, _, _ = make_ready_claim(
        tmp_path, registry, runner, reproducer, overfit_fn, {"n_params": 50, "n_samples": 20}
    )

    verdict = reviewer.review(claim.id)

    overfitting_flags = [f for f in verdict.flags if f.check == CHECK_OVERFITTING]
    assert len(overfitting_flags) == 1
    assert CHECK_OVERFITTING in verdict.all_checks_run


def test_check3_n_params_lt_n_samples_passes_clean(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def well_fit_fn(n_params, n_samples):
        return {"n_params": n_params, "n_samples": n_samples, "score": 1.0}

    claim, _, _ = make_ready_claim(
        tmp_path, registry, runner, reproducer, well_fit_fn, {"n_params": 5, "n_samples": 100}
    )

    verdict = reviewer.review(claim.id)

    overfitting_flags = [f for f in verdict.flags if f.check == CHECK_OVERFITTING]
    assert overfitting_flags == []
    assert CHECK_OVERFITTING in verdict.all_checks_run


# ---------------------------------------------------------------------------
# Check 4: leakage
# ---------------------------------------------------------------------------


def test_check4_overlapping_indices_is_flagged(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def split_fn(calibration_indices, validation_indices):
        return {"n": len(calibration_indices) + len(validation_indices)}

    claim, _, _ = make_ready_claim(
        tmp_path,
        registry,
        runner,
        reproducer,
        split_fn,
        {"calibration_indices": [1, 2, 3, 4], "validation_indices": [4, 5, 6]},
    )

    verdict = reviewer.review(claim.id)

    leakage_flags = [f for f in verdict.flags if f.check == CHECK_LEAKAGE]
    assert len(leakage_flags) == 1
    assert "4" in leakage_flags[0].detail
    assert CHECK_LEAKAGE in verdict.all_checks_run


def test_check4_disjoint_indices_passes_clean(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    def split_fn(calibration_indices, validation_indices):
        return {"n": len(calibration_indices) + len(validation_indices)}

    claim, _, _ = make_ready_claim(
        tmp_path,
        registry,
        runner,
        reproducer,
        split_fn,
        {"calibration_indices": [1, 2, 3], "validation_indices": [4, 5, 6]},
    )

    verdict = reviewer.review(claim.id)

    leakage_flags = [f for f in verdict.flags if f.check == CHECK_LEAKAGE]
    assert leakage_flags == []
    assert CHECK_LEAKAGE in verdict.all_checks_run


# ---------------------------------------------------------------------------
# review() precondition
# ---------------------------------------------------------------------------


def test_review_raises_without_successful_reproduction(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim = registry.create("No reproduction", "Has a run but no reproduction on file.")
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED)
    test_plan = TestPlan(name="p", version="v1", fn=const_fn, params={"x": 1.0})
    runner.lock(claim.id, test_plan)
    runner.run(claim.id, test_plan)

    with pytest.raises(ReviewPreconditionError):
        reviewer.review(claim.id)


# ---------------------------------------------------------------------------
# record_verdict()
# ---------------------------------------------------------------------------


def test_record_verdict_raises_if_review_never_ran(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(tmp_path, registry, runner, reproducer, const_fn, {"x": 1.0})

    with pytest.raises(VerdictWithoutReviewError):
        reviewer.record_verdict(claim.id, "CONFIRMED", "Looks solid.")


def test_record_verdict_raises_on_empty_rationale(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(tmp_path, registry, runner, reproducer, const_fn, {"x": 1.0})
    reviewer.review(claim.id)

    with pytest.raises(EmptyRationaleError):
        reviewer.record_verdict(claim.id, "CONFIRMED", "   ")


def test_record_verdict_raises_on_invalid_verdict_literal(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(tmp_path, registry, runner, reproducer, const_fn, {"x": 1.0})
    reviewer.review(claim.id)

    with pytest.raises(InvalidVerdictError):
        reviewer.record_verdict(claim.id, "MAYBE", "Not a real terminal state.")


def test_record_verdict_transitions_to_terminal_state_and_becomes_immutable(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)
    reviewer = make_reviewer(tmp_path, registry, runner, reproducer)

    claim, _, _ = make_ready_claim(tmp_path, registry, runner, reproducer, const_fn, {"x": 1.0})
    reviewer.review(claim.id)

    updated = reviewer.record_verdict(
        claim.id, "CONFIRMED", "Passed all applicable adversarial checks; reproduced exactly."
    )
    assert updated.state is ClaimState.CONFIRMED

    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.CONFIRMED
    assert reloaded.history[-1].note == "Passed all applicable adversarial checks; reproduced exactly."

    with pytest.raises(IllegalTransitionError):
        registry.advance(claim.id, ClaimState.REFUTED, note="trying to change my mind")
