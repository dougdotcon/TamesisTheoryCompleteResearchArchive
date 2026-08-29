import pytest

from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.registry import Registry
from tamesis_discovery_engine.runner import (
    ClaimNotLockedError,
    Runner,
    RunRecord,
    TestPlan,
    TestPlanTamperedError,
)

from .conftest import FakeClock


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def make_runner(tmp_path, registry, clock=None):
    return Runner(registry, data_dir=tmp_path / "runs", clock=clock or FakeClock())


def make_counting_plan(name="add", version="v1"):
    calls = []

    def fn(a, b):
        calls.append((a, b))
        return {"sum": a + b}

    return TestPlan(name=name, version=version, fn=fn, params={"a": 2, "b": 3}), calls


def make_locked_claim(tmp_path, registry, runner, test_plan):
    claim = registry.create("Sum test", "a + b behaves as expected.")
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED)
    claim = runner.lock(claim.id, test_plan)
    return claim


def test_run_transitions_locked_claim_to_result_with_correct_run_record(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan, calls = make_counting_plan()

    claim = make_locked_claim(tmp_path, registry, runner, test_plan)
    record = runner.run(claim.id, test_plan)

    assert isinstance(record, RunRecord)
    assert record.claim_id == claim.id
    assert record.params == {"a": 2, "b": 3}
    assert record.result == {"sum": 5}
    assert record.success is True
    assert record.exception_type is None
    assert calls == [(2, 3)]

    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.RESULT


def test_run_raises_for_non_locked_claim_without_invoking_callable(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan, calls = make_counting_plan()

    draft_claim = registry.create("Never locked", "should not run.")
    assert draft_claim.state is ClaimState.DRAFT

    with pytest.raises(ClaimNotLockedError):
        runner.run(draft_claim.id, test_plan)

    assert calls == []
    assert registry.get(draft_claim.id).state is ClaimState.DRAFT


@pytest.mark.parametrize(
    "to_state",
    [ClaimState.PRE_REGISTERED, ClaimState.RUNNING, ClaimState.RESULT],
)
def test_run_raises_for_any_non_locked_state(tmp_path, to_state):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan, calls = make_counting_plan()

    claim = registry.create("Wrong state", "statement")
    for state in (ClaimState.PRE_REGISTERED, ClaimState.LOCKED, ClaimState.RUNNING, ClaimState.RESULT):
        claim = registry.advance(claim.id, state)
        if state is to_state:
            break

    with pytest.raises(ClaimNotLockedError):
        runner.run(claim.id, test_plan)
    assert calls == []


def test_run_raises_test_plan_tampered_error_after_source_mutation(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan, original_calls = make_counting_plan()

    claim = make_locked_claim(tmp_path, registry, runner, test_plan)

    tampered_calls = []

    def tampered_fn(a, b):
        tampered_calls.append((a, b))
        return {"sum": a + b, "tampered": True}

    test_plan.fn = tampered_fn

    with pytest.raises(TestPlanTamperedError):
        runner.run(claim.id, test_plan)

    assert tampered_calls == []
    assert original_calls == []
    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.LOCKED


def test_run_records_and_reraises_exception_from_failing_test_plan(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)

    def failing_fn(x):
        raise ValueError("boom: divergent series")

    test_plan = TestPlan(name="failing", version="v1", fn=failing_fn, params={"x": 1})
    claim = make_locked_claim(tmp_path, registry, runner, test_plan)

    with pytest.raises(ValueError, match="boom: divergent series"):
        runner.run(claim.id, test_plan)

    failed_record = runner.get_run(claim.id)
    assert failed_record.success is False
    assert failed_record.result is None
    assert failed_record.exception_type == "ValueError"
    assert "boom: divergent series" in failed_record.exception_message

    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.RUNNING
    assert reloaded.state is not ClaimState.RESULT


def test_run_record_persistence_round_trip_in_fresh_runner(tmp_path):
    clock = FakeClock()
    registry = make_registry(tmp_path, clock=clock)
    runner = make_runner(tmp_path, registry, clock=clock)
    test_plan, _ = make_counting_plan()

    claim = make_locked_claim(tmp_path, registry, runner, test_plan)
    original_record = runner.run(claim.id, test_plan)

    fresh_runner = Runner(registry, data_dir=tmp_path / "runs", clock=FakeClock())
    reloaded_record = fresh_runner.get_run(claim.id)

    assert reloaded_record == original_record


def test_lock_stores_hash_and_advances_claim_to_locked(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan, _ = make_counting_plan()

    claim = registry.create("Lock test", "statement")
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED)
    locked_claim = runner.lock(claim.id, test_plan)

    assert locked_claim.state is ClaimState.LOCKED
    lock_record = runner._load_lock(claim.id)
    assert lock_record.source_hash == test_plan.source_hash()
    assert lock_record.test_plan_name == "add"
    assert lock_record.test_plan_version == "v1"
