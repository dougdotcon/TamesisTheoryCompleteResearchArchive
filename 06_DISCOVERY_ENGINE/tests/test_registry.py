from datetime import datetime, timezone

import pytest

from tamesis_discovery_engine.claim import ClaimState, IllegalTransitionError
from tamesis_discovery_engine.registry import ClaimNotFoundError, Registry

from .conftest import FakeClock


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def test_create_starts_in_draft(tmp_path):
    registry = make_registry(tmp_path)
    claim = registry.create("U1/2 limit", "phi_inf(c) has a closed form.")
    assert claim.state is ClaimState.DRAFT
    assert claim.history == []
    assert claim.id.startswith("DISC-2026-")


def test_full_legal_sequence_succeeds_and_is_recorded_in_history(tmp_path):
    clock = FakeClock()
    registry = make_registry(tmp_path, clock=clock)
    claim = registry.create("U1/2 limit", "phi_inf(c) has a closed form.")

    sequence = [
        ClaimState.PRE_REGISTERED,
        ClaimState.LOCKED,
        ClaimState.RUNNING,
        ClaimState.RESULT,
        ClaimState.ADVERSARIAL_REVIEW,
        ClaimState.CONFIRMED,
    ]
    for to_state in sequence:
        claim = registry.advance(claim.id, to_state, note=f"moving to {to_state.value}")

    assert claim.state is ClaimState.CONFIRMED
    assert len(claim.history) == len(sequence)

    expected_from = [ClaimState.DRAFT] + sequence[:-1]
    for record, expected_from_state, expected_to_state in zip(claim.history, expected_from, sequence):
        assert record.from_state is expected_from_state
        assert record.to_state is expected_to_state
        assert isinstance(record.at, datetime)

    timestamps = [record.at for record in claim.history]
    assert timestamps == sorted(timestamps)
    assert len(set(timestamps)) == len(timestamps)


def test_skipping_a_state_raises_illegal_transition_error(tmp_path):
    registry = make_registry(tmp_path)
    claim = registry.create("Skip test", "statement")
    with pytest.raises(IllegalTransitionError):
        registry.advance(claim.id, ClaimState.LOCKED)
    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.DRAFT
    assert reloaded.history == []


def test_transitioning_out_of_terminal_state_raises_illegal_transition_error(tmp_path):
    registry = make_registry(tmp_path)
    claim = registry.create("Terminal test", "statement")
    for to_state in (
        ClaimState.PRE_REGISTERED,
        ClaimState.LOCKED,
        ClaimState.RUNNING,
        ClaimState.RESULT,
        ClaimState.ADVERSARIAL_REVIEW,
        ClaimState.REFUTED,
    ):
        claim = registry.advance(claim.id, to_state)
    assert claim.state is ClaimState.REFUTED

    for attempted_target in (
        ClaimState.CONFIRMED,
        ClaimState.DRAFT,
        ClaimState.ADVERSARIAL_REVIEW,
    ):
        with pytest.raises(IllegalTransitionError):
            registry.advance(claim.id, attempted_target)


def test_persistence_round_trip_after_fresh_registry_instance(tmp_path):
    data_dir = tmp_path / "claims"
    clock = FakeClock()
    registry = Registry(data_dir=data_dir, clock=clock)
    claim = registry.create("Persisted claim", "A falsifiable statement.", metadata={"owner": "doug"})
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED, note="locking in")
    claim = registry.advance(claim.id, ClaimState.LOCKED)

    fresh_registry = Registry(data_dir=data_dir, clock=FakeClock())
    reloaded = fresh_registry.get(claim.id)

    assert reloaded == claim
    assert reloaded.id == claim.id
    assert reloaded.state is ClaimState.LOCKED
    assert len(reloaded.history) == 2
    assert [r.to_state for r in reloaded.history] == [ClaimState.PRE_REGISTERED, ClaimState.LOCKED]


def test_get_raises_for_unknown_claim(tmp_path):
    registry = make_registry(tmp_path)
    with pytest.raises(ClaimNotFoundError):
        registry.get("DISC-2026-99999")


def test_sequential_ids_within_a_year_are_distinct_and_survive_restart(tmp_path):
    data_dir = tmp_path / "claims"
    same_year_clock = FakeClock(start=datetime(2026, 5, 1, tzinfo=timezone.utc))
    registry = Registry(data_dir=data_dir, clock=same_year_clock)

    first = registry.create("Claim one", "statement one")
    second = registry.create("Claim two", "statement two")

    assert first.id == "DISC-2026-00001"
    assert second.id == "DISC-2026-00002"
    assert first.id != second.id

    restarted_clock = FakeClock(start=datetime(2026, 6, 1, tzinfo=timezone.utc))
    restarted_registry = Registry(data_dir=data_dir, clock=restarted_clock)
    third = restarted_registry.create("Claim three", "statement three")

    assert third.id == "DISC-2026-00003"
    assert len({first.id, second.id, third.id}) == 3


def test_sequence_resets_per_calendar_year(tmp_path):
    data_dir = tmp_path / "claims"
    year_2026_clock = FakeClock(start=datetime(2026, 12, 31, tzinfo=timezone.utc))
    registry_2026 = Registry(data_dir=data_dir, clock=year_2026_clock)
    claim_2026 = registry_2026.create("End of 2026", "statement")
    assert claim_2026.id == "DISC-2026-00001"

    year_2027_clock = FakeClock(start=datetime(2027, 1, 1, tzinfo=timezone.utc))
    registry_2027 = Registry(data_dir=data_dir, clock=year_2027_clock)
    claim_2027 = registry_2027.create("Start of 2027", "statement")
    assert claim_2027.id == "DISC-2027-00001"


def test_list_filters_by_state(tmp_path):
    registry = make_registry(tmp_path)
    draft = registry.create("Draft claim", "s1")
    pre_registered = registry.create("Pre-registered claim", "s2")
    pre_registered = registry.advance(pre_registered.id, ClaimState.PRE_REGISTERED)
    locked = registry.create("Locked claim", "s3")
    locked = registry.advance(locked.id, ClaimState.PRE_REGISTERED)
    locked = registry.advance(locked.id, ClaimState.LOCKED)

    draft_results = registry.list(state=ClaimState.DRAFT)
    assert [c.id for c in draft_results] == [draft.id]

    pre_registered_results = registry.list(state=ClaimState.PRE_REGISTERED)
    assert [c.id for c in pre_registered_results] == [pre_registered.id]

    locked_results = registry.list(state=ClaimState.LOCKED)
    assert [c.id for c in locked_results] == [locked.id]

    running_results = registry.list(state=ClaimState.RUNNING)
    assert running_results == []

    assert len(registry.list()) == 3


def test_list_filters_by_tag(tmp_path):
    registry = make_registry(tmp_path)
    u12_claim = registry.create("U12 claim", "s1", metadata={"tags": ["u12", "core-numerics"]})
    sparc_claim = registry.create("SPARC claim", "s2", metadata={"tags": ["sparc"]})
    untagged_claim = registry.create("Untagged claim", "s3")

    u12_results = registry.list(tag="u12")
    assert [c.id for c in u12_results] == [u12_claim.id]

    sparc_results = registry.list(tag="sparc")
    assert [c.id for c in sparc_results] == [sparc_claim.id]

    missing_tag_results = registry.list(tag="nonexistent")
    assert missing_tag_results == []

    assert untagged_claim.id not in [c.id for c in u12_results + sparc_results]


def test_list_combines_state_and_tag_filters(tmp_path):
    registry = make_registry(tmp_path)
    match = registry.create("Match", "s1", metadata={"tags": ["u12"]})
    match = registry.advance(match.id, ClaimState.PRE_REGISTERED)

    wrong_state = registry.create("Wrong state", "s2", metadata={"tags": ["u12"]})
    wrong_tag = registry.create("Wrong tag", "s3", metadata={"tags": ["other"]})
    wrong_tag = registry.advance(wrong_tag.id, ClaimState.PRE_REGISTERED)

    results = registry.list(state=ClaimState.PRE_REGISTERED, tag="u12")
    assert [c.id for c in results] == [match.id]


def test_create_copies_caller_metadata_dict(tmp_path):
    registry = make_registry(tmp_path)
    metadata = {"tags": ["u12"]}
    claim = registry.create("Claim", "statement", metadata=metadata)

    metadata["tags"] = ["mutated-after-create"]
    metadata["owner"] = "someone-else"

    assert claim.metadata == {"tags": ["u12"]}
    reloaded = registry.get(claim.id)
    assert reloaded.metadata == {"tags": ["u12"]}
