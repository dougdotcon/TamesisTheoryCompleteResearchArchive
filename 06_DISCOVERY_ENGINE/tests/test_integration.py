import pytest

from tamesis_discovery_engine import DiscoveryEngine
from tamesis_discovery_engine.adversarial import SUCCESS_THRESHOLD_KEY, format_threshold_note
from tamesis_discovery_engine.claim import ClaimState, IllegalTransitionError
from tamesis_discovery_engine.reproduction import ReproductionPlan
from tamesis_discovery_engine.runner import TestPlan

from .conftest import FakeClock


def make_engine(tmp_path, clock=None):
    return DiscoveryEngine(data_dir=tmp_path / "data", clock=clock or FakeClock())


def add_fn(a, b):
    return {"sum": a + b}


def add_fn_independent(a, b):
    total = a
    for _ in range(b):
        total += 1
    return {"sum": total}


def test_engine_shares_one_data_root_across_all_five_modules(tmp_path):
    engine = make_engine(tmp_path)

    assert engine.registry.data_dir == tmp_path / "data" / "claims"
    assert engine.runner.data_dir == tmp_path / "data" / "runs"
    assert engine.reproducer.data_dir == tmp_path / "data" / "reproductions"
    assert engine.reviewer.data_dir == tmp_path / "data" / "reviews"
    assert engine.ledger.ledger_path == tmp_path / "data" / "ledger.jsonl"


def test_full_lifecycle_to_confirmed_via_facade_and_ledger_chain(tmp_path):
    clock = FakeClock()
    engine = make_engine(tmp_path, clock=clock)

    claim = engine.register(
        "Additivity claim",
        "a + b behaves additively for the declared test cases.",
        metadata={SUCCESS_THRESHOLD_KEY: 0.0},
    )
    assert claim.state is ClaimState.DRAFT

    claim = engine.advance(
        claim.id, ClaimState.PRE_REGISTERED, note=format_threshold_note(0.0)
    )
    assert claim.state is ClaimState.PRE_REGISTERED

    test_plan = TestPlan(name="add", version="v1", fn=add_fn, params={"a": 2, "b": 3})
    claim = engine.lock(claim.id, test_plan)
    assert claim.state is ClaimState.LOCKED

    run_record = engine.run(claim.id, test_plan)
    assert run_record.success is True
    assert run_record.result == {"sum": 5}
    assert engine.get(claim.id).state is ClaimState.RESULT

    repro_record = engine.reproduce(
        claim.id,
        ReproductionPlan(name="add-independent", version="v1", fn=add_fn_independent),
        tolerance=1e-9,
    )
    assert repro_record.verdict in ("EXACT_MATCH", "MATCH_WITHIN_TOLERANCE")

    verdict = engine.review(claim.id, test_plan=test_plan)
    assert verdict.recommendation == "CLEAN"
    assert engine.get(claim.id).state is ClaimState.ADVERSARIAL_REVIEW

    final_claim = engine.record_verdict(
        claim.id, ClaimState.CONFIRMED, "Reproduced within tolerance; no adversarial flags."
    )
    assert final_claim.state is ClaimState.CONFIRMED

    with pytest.raises(IllegalTransitionError):
        engine.advance(claim.id, ClaimState.REFUTED, note="cannot leave a terminal state")

    entries = engine.ledger.history(claim_id=claim.id)
    assert [entry.decision_type for entry in entries] == [
        "REGISTER",
        "ADVANCE",
        "LOCK",
        "RUN",
        "REPRODUCE",
        "REVIEW",
        "VERDICT",
    ]
    assert all(entry.claim_id == claim.id for entry in entries)
    assert all(
        entries[i].timestamp < entries[i + 1].timestamp for i in range(len(entries) - 1)
    )
    assert engine.ledger.verify_chain() is True

    reloaded_engine = DiscoveryEngine(data_dir=tmp_path / "data", clock=FakeClock())
    assert reloaded_engine.get(claim.id).state is ClaimState.CONFIRMED
    assert reloaded_engine.ledger.verify_chain() is True
    assert len(reloaded_engine.ledger.history(claim_id=claim.id)) == 7


def test_deliberate_refuted_path_via_facade(tmp_path):
    clock = FakeClock()
    engine = make_engine(tmp_path, clock=clock)

    def broken_fn(x):
        return {"value": x}

    claim = engine.register(
        "Faulty claim", "x is invariant under a transformation it is not.", metadata={SUCCESS_THRESHOLD_KEY: 0.0}
    )
    claim = engine.advance(claim.id, ClaimState.PRE_REGISTERED, note=format_threshold_note(0.0))

    test_plan = TestPlan(name="broken", version="v1", fn=broken_fn, params={"x": 1.0})
    engine.lock(claim.id, test_plan)
    engine.run(claim.id, test_plan)

    def broken_fn_reproduced_but_disagreeing(x):
        return {"value": x + 1000.0}

    repro_record = engine.reproduce(
        claim.id,
        ReproductionPlan(name="disagreeing", version="v1", fn=broken_fn_reproduced_but_disagreeing),
        tolerance=1e-9,
    )
    assert repro_record.verdict == "MISMATCH"

    # AdversarialReviewer.review() only requires a successful reproduction on
    # file (has_successful_reproduction), not that the *latest* one matched —
    # append a second, agreeing reproduction so review() may proceed.
    engine.reproduce(claim.id, ReproductionPlan(name="agreeing", version="v1", fn=broken_fn), tolerance=1e-9)

    engine.review(claim.id, test_plan=test_plan)
    final_claim = engine.record_verdict(
        claim.id, ClaimState.REFUTED, "Independent reproduction disagreed; original result not trustworthy."
    )
    assert final_claim.state is ClaimState.REFUTED

    decision_types = [entry.decision_type for entry in engine.ledger.history(claim_id=claim.id)]
    assert decision_types == [
        "REGISTER",
        "ADVANCE",
        "LOCK",
        "RUN",
        "REPRODUCE",
        "REPRODUCE",
        "REVIEW",
        "VERDICT",
    ]
    assert engine.ledger.verify_chain() is True
