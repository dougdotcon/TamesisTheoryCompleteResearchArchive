import pytest

from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.registry import Registry
from tamesis_discovery_engine.reproduction import (
    ClaimNotReproducibleError,
    Reproducer,
    ReproductionPlan,
    ReproductionVerdict,
    has_successful_reproduction,
)
from tamesis_discovery_engine.runner import Runner, TestPlan

from .conftest import FakeClock


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def make_runner(tmp_path, registry, clock=None):
    return Runner(registry, data_dir=tmp_path / "runs", clock=clock or FakeClock())


def make_reproducer(tmp_path, registry, runner, clock=None):
    return Reproducer(registry, runner, data_dir=tmp_path / "reproductions", clock=clock or FakeClock())


def make_claim_with_result(tmp_path, registry, runner, fn, params, name="original", version="v1"):
    claim = registry.create("Reproducible claim", "A claim with a completed run.")
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED)
    test_plan = TestPlan(name=name, version=version, fn=fn, params=params)
    runner.lock(claim.id, test_plan)
    run_record = runner.run(claim.id, test_plan)
    return claim, run_record


def naive_stats(values):
    total = 0.0
    for value in values:
        total += value
    mean = total / len(values)
    sq = 0.0
    for value in values:
        sq += (value - mean) ** 2
    variance = sq / len(values)
    return {"mean": mean, "variance": variance}


def welford_stats(values):
    n = 0
    mean = 0.0
    m2 = 0.0
    for value in values:
        n += 1
        delta = value - mean
        mean += delta / n
        delta2 = value - mean
        m2 += delta * delta2
    variance = m2 / n
    return {"mean": mean, "variance": variance}


DATASET = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]


def test_identical_second_implementation_matches_within_tolerance(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    claim, run_record = make_claim_with_result(
        tmp_path, registry, runner, naive_stats, {"values": DATASET}
    )

    record = reproducer.reproduce(
        claim.id,
        ReproductionPlan(name="welford", version="v1", fn=welford_stats),
        tolerance=1e-9,
    )

    assert record.verdict in (
        ReproductionVerdict.EXACT_MATCH.value,
        ReproductionVerdict.MATCH_WITHIN_TOLERANCE.value,
    )
    assert record.reproduced_result["mean"] == pytest.approx(run_record.result["mean"], abs=1e-9)
    assert record.reproduced_result["variance"] == pytest.approx(run_record.result["variance"], abs=1e-9)
    assert record.original_result == run_record.result
    assert record.params == {"values": DATASET}


def test_perturbed_second_implementation_is_caught_as_mismatch_with_correct_delta(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    claim, run_record = make_claim_with_result(
        tmp_path, registry, runner, naive_stats, {"values": DATASET}
    )

    injected_offset = 1000.0

    def perturbed_stats(values):
        n = len(values)
        mean = sum(values) / n
        variance = sum((value - mean) ** 2 for value in values) / n
        return {"mean": mean + injected_offset, "variance": variance}

    record = reproducer.reproduce(
        claim.id,
        ReproductionPlan(name="perturbed", version="v1", fn=perturbed_stats),
        tolerance=1e-9,
    )

    assert record.verdict == ReproductionVerdict.MISMATCH.value

    mean_deltas = [delta for delta in record.deltas if delta.field == "mean"]
    assert len(mean_deltas) == 1
    assert mean_deltas[0].verdict == ReproductionVerdict.MISMATCH.value
    assert mean_deltas[0].delta == pytest.approx(injected_offset, abs=1e-6)
    assert mean_deltas[0].original == pytest.approx(run_record.result["mean"])
    assert mean_deltas[0].reproduced == pytest.approx(run_record.result["mean"] + injected_offset)


def test_tolerance_boundary_at_and_just_outside(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    def zero(x):
        return {"value": x}

    claim, run_record = make_claim_with_result(tmp_path, registry, runner, zero, {"x": 0.0})
    assert run_record.result == {"value": 0.0}

    tolerance = 0.001

    def at_boundary(x):
        return {"value": x + tolerance}

    def just_outside(x):
        return {"value": x + tolerance + 1e-6}

    inside_record = reproducer.reproduce(
        claim.id,
        ReproductionPlan(name="at-boundary", version="v1", fn=at_boundary),
        tolerance=tolerance,
    )
    assert inside_record.verdict == ReproductionVerdict.MATCH_WITHIN_TOLERANCE.value
    assert inside_record.deltas[0].delta == pytest.approx(tolerance)

    outside_record = reproducer.reproduce(
        claim.id,
        ReproductionPlan(name="just-outside", version="v1", fn=just_outside),
        tolerance=tolerance,
    )
    assert outside_record.verdict == ReproductionVerdict.MISMATCH.value
    assert outside_record.deltas[0].delta == pytest.approx(tolerance + 1e-6)


def test_has_successful_reproduction_lifecycle(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    def base(x):
        return {"value": x}

    claim, _ = make_claim_with_result(tmp_path, registry, runner, base, {"x": 1.0})

    assert reproducer.has_successful_reproduction(claim.id) is False
    assert has_successful_reproduction(claim.id, data_dir=reproducer.data_dir) is False

    def bad(x):
        return {"value": x + 1000.0}

    reproducer.reproduce(claim.id, ReproductionPlan(name="bad", version="v1", fn=bad), tolerance=1e-9)
    assert reproducer.has_successful_reproduction(claim.id) is False
    assert has_successful_reproduction(claim.id, data_dir=reproducer.data_dir) is False

    def good(x):
        return {"value": x}

    reproducer.reproduce(claim.id, ReproductionPlan(name="good", version="v1", fn=good), tolerance=1e-9)
    assert reproducer.has_successful_reproduction(claim.id) is True
    assert has_successful_reproduction(claim.id, data_dir=reproducer.data_dir) is True


def test_has_successful_reproduction_false_for_unknown_claim(tmp_path):
    assert has_successful_reproduction("DISC-2026-99999", data_dir=tmp_path / "reproductions") is False


def test_reproduce_raises_for_claim_without_a_successful_run(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    claim = registry.create("Not run yet", "No RunRecord exists.")

    def fn(x):
        return {"value": x}

    with pytest.raises(ClaimNotReproducibleError):
        reproducer.reproduce(claim.id, ReproductionPlan(name="p", version="v1", fn=fn), tolerance=1e-9)


def test_reproduce_recursively_diffs_nested_dicts_and_lists(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    def original_nested(n):
        return {"label": "ok", "metrics": {"a": 1.0, "series": [1.0, 2.0, 3.0]}}

    claim, _ = make_claim_with_result(tmp_path, registry, runner, original_nested, {"n": 3})

    def broken_nested(n):
        return {"label": "ok", "metrics": {"a": 1.0, "series": [1.0, 999.0, 3.0]}}

    record = reproducer.reproduce(
        claim.id,
        ReproductionPlan(name="broken-nested", version="v1", fn=broken_nested),
        tolerance=1e-9,
    )

    assert record.verdict == ReproductionVerdict.MISMATCH.value
    fields = {delta.field: delta for delta in record.deltas}
    assert "metrics.series[1]" in fields
    assert fields["metrics.series[1]"].verdict == ReproductionVerdict.MISMATCH.value
    assert "label" not in fields
    assert "metrics.a" not in fields


def test_reproduction_record_persistence_round_trip_in_fresh_reproducer(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    def base(x):
        return {"value": x}

    claim, _ = make_claim_with_result(tmp_path, registry, runner, base, {"x": 2.5})

    original_record = reproducer.reproduce(
        claim.id, ReproductionPlan(name="base-copy", version="v1", fn=base), tolerance=1e-9
    )

    fresh_reproducer = Reproducer(registry, runner, data_dir=reproducer.data_dir, clock=FakeClock())
    reloaded = fresh_reproducer.list_reproductions(claim.id)

    assert len(reloaded) == 1
    assert reloaded[0] == original_record
