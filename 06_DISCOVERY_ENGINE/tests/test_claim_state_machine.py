from datetime import datetime, timezone

import pytest

from tamesis_discovery_engine.claim import (
    TERMINAL_STATES,
    TRANSITIONS,
    Claim,
    ClaimState,
    IllegalTransitionError,
    TransitionRecord,
    coerce_state,
    is_legal_transition,
)


def test_state_machine_matches_roadmap_chain():
    assert is_legal_transition(ClaimState.DRAFT, ClaimState.PRE_REGISTERED)
    assert is_legal_transition(ClaimState.PRE_REGISTERED, ClaimState.LOCKED)
    assert is_legal_transition(ClaimState.LOCKED, ClaimState.RUNNING)
    assert is_legal_transition(ClaimState.RUNNING, ClaimState.RESULT)
    assert is_legal_transition(ClaimState.RESULT, ClaimState.ADVERSARIAL_REVIEW)
    for verdict in (
        ClaimState.CONFIRMED,
        ClaimState.REFUTED,
        ClaimState.INCONCLUSIVE,
        ClaimState.NULL,
    ):
        assert is_legal_transition(ClaimState.ADVERSARIAL_REVIEW, verdict)


@pytest.mark.parametrize(
    "from_state,to_state",
    [
        (ClaimState.DRAFT, ClaimState.LOCKED),
        (ClaimState.DRAFT, ClaimState.RUNNING),
        (ClaimState.DRAFT, ClaimState.RESULT),
        (ClaimState.DRAFT, ClaimState.ADVERSARIAL_REVIEW),
        (ClaimState.DRAFT, ClaimState.CONFIRMED),
        (ClaimState.PRE_REGISTERED, ClaimState.RUNNING),
        (ClaimState.PRE_REGISTERED, ClaimState.DRAFT),
        (ClaimState.LOCKED, ClaimState.RESULT),
        (ClaimState.RUNNING, ClaimState.ADVERSARIAL_REVIEW),
        (ClaimState.RESULT, ClaimState.CONFIRMED),
    ],
)
def test_skipping_a_state_is_illegal(from_state, to_state):
    assert not is_legal_transition(from_state, to_state)


@pytest.mark.parametrize(
    "terminal_state",
    [ClaimState.CONFIRMED, ClaimState.REFUTED, ClaimState.INCONCLUSIVE, ClaimState.NULL],
)
def test_terminal_states_have_no_outgoing_transitions(terminal_state):
    assert terminal_state in TERMINAL_STATES
    assert TRANSITIONS[terminal_state] == frozenset()
    for candidate in ClaimState:
        assert not is_legal_transition(terminal_state, candidate)


def test_terminal_states_reachable_only_from_adversarial_review():
    non_review_sources = [s for s in ClaimState if s is not ClaimState.ADVERSARIAL_REVIEW]
    for terminal_state in TERMINAL_STATES:
        for source in non_review_sources:
            assert not is_legal_transition(source, terminal_state)


def test_every_state_has_a_transition_table_entry():
    for state in ClaimState:
        assert state in TRANSITIONS


def test_coerce_state_accepts_enum_and_string():
    assert coerce_state(ClaimState.DRAFT) is ClaimState.DRAFT
    assert coerce_state("LOCKED") is ClaimState.LOCKED
    with pytest.raises(ValueError):
        coerce_state("NOT_A_REAL_STATE")


def test_illegal_transition_error_reports_states_and_claim_id():
    err = IllegalTransitionError(ClaimState.DRAFT, ClaimState.RESULT, claim_id="DISC-2026-00001")
    assert err.from_state is ClaimState.DRAFT
    assert err.to_state is ClaimState.RESULT
    assert err.claim_id == "DISC-2026-00001"
    assert "DISC-2026-00001" in str(err)
    assert "DRAFT" in str(err)
    assert "RESULT" in str(err)
    assert isinstance(err, Exception)
    assert type(err) is not Exception


def test_transition_record_round_trips_through_dict():
    at = datetime(2026, 3, 4, 12, 0, 0, tzinfo=timezone.utc)
    record = TransitionRecord(
        from_state=ClaimState.DRAFT,
        to_state=ClaimState.PRE_REGISTERED,
        at=at,
        note="pre-registration locked",
    )
    data = record.to_dict()
    assert data == {
        "from_state": "DRAFT",
        "to_state": "PRE_REGISTERED",
        "at": at.isoformat(),
        "note": "pre-registration locked",
    }
    assert TransitionRecord.from_dict(data) == record


def test_claim_round_trips_through_dict_with_history():
    created = datetime(2026, 1, 1, tzinfo=timezone.utc)
    advanced_at = datetime(2026, 1, 2, tzinfo=timezone.utc)
    claim = Claim(
        id="DISC-2026-00001",
        title="Test claim",
        statement="Some falsifiable statement.",
        state=ClaimState.PRE_REGISTERED,
        created_at=created,
        history=[
            TransitionRecord(
                from_state=ClaimState.DRAFT,
                to_state=ClaimState.PRE_REGISTERED,
                at=advanced_at,
                note="locked in",
            )
        ],
        metadata={"owner": "doug", "tags": ["u12"]},
    )
    restored = Claim.from_dict(claim.to_dict())
    assert restored == claim
    assert restored.state is ClaimState.PRE_REGISTERED
    assert restored.history[0].from_state is ClaimState.DRAFT


def test_claim_defaults_history_and_metadata_when_absent_from_dict():
    minimal = {
        "id": "DISC-2026-00002",
        "title": "Minimal",
        "statement": "Statement.",
        "state": "DRAFT",
        "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc).isoformat(),
    }
    claim = Claim.from_dict(minimal)
    assert claim.history == []
    assert claim.metadata == {}
