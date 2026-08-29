import dataclasses
import json

import pytest

from tamesis_discovery_engine.ledger import (
    GENESIS_HASH,
    DecisionType,
    Ledger,
    LedgerEntry,
    TamperDetectedError,
)

from .conftest import FakeClock


def make_ledger(tmp_path, clock=None):
    return Ledger(ledger_path=tmp_path / "ledger.jsonl", clock=clock or FakeClock())


def test_append_three_entries_then_verify_chain_is_clean(tmp_path):
    ledger = make_ledger(tmp_path)
    ledger.append("DISC-2026-00001", DecisionType.REGISTER, "Claim registered.")
    ledger.append("DISC-2026-00001", DecisionType.LOCK, "Pre-registration locked.")
    ledger.append("DISC-2026-00001", DecisionType.RUN, "Experiment executed.")

    assert ledger.verify_chain() is True

    entries = ledger.history()
    assert len(entries) == 3
    assert entries[0].prev_hash == GENESIS_HASH
    assert entries[1].prev_hash == entries[0].content_hash()
    assert entries[2].prev_hash == entries[1].content_hash()


def test_tampering_with_a_persisted_entry_is_detected_by_a_fresh_ledger(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = Ledger(ledger_path=ledger_path, clock=FakeClock())
    ledger.append("DISC-2026-00001", DecisionType.REGISTER, "Claim registered.")
    ledger.append("DISC-2026-00001", DecisionType.LOCK, "Pre-registration locked.")
    ledger.append("DISC-2026-00001", DecisionType.RUN, "Experiment executed.")

    assert Ledger(ledger_path=ledger_path, clock=FakeClock()).verify_chain() is True

    lines = ledger_path.read_text().splitlines()
    tampered = json.loads(lines[1])
    assert tampered["summary"] == "Pre-registration locked."
    tampered["summary"] = "Pre-registration locked (secretly altered after the fact)."
    lines[1] = json.dumps(tampered, sort_keys=True)
    ledger_path.write_text("\n".join(lines) + "\n")

    fresh_ledger = Ledger(ledger_path=ledger_path, clock=FakeClock())
    with pytest.raises(TamperDetectedError) as excinfo:
        fresh_ledger.verify_chain()
    assert excinfo.value.index == 2
    assert excinfo.value.entry_id == "ENGINE-DEC-003"


def test_tampering_with_the_last_persisted_entry_is_detected_by_a_fresh_ledger(tmp_path):
    """Regression test for the tail-entry gap: the per-link loop in
    verify_chain() only ever exposes tampering with entry i's content via
    entry i+1's prev_hash — the *last* entry has no following entry, so
    rewriting only its content (leaving every prev_hash on disk untouched)
    used to leave verify_chain() reporting a clean chain. The out-of-band
    .head commitment file written by append() closes that gap.
    """
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = Ledger(ledger_path=ledger_path, clock=FakeClock())
    ledger.append("DISC-2026-00001", DecisionType.REGISTER, "Claim registered.")
    ledger.append("DISC-2026-00001", DecisionType.LOCK, "Pre-registration locked.")
    ledger.append("DISC-2026-00001", DecisionType.VERDICT, "REFUTED: effect did not replicate.")

    assert Ledger(ledger_path=ledger_path, clock=FakeClock()).verify_chain() is True

    lines = ledger_path.read_text().splitlines()
    tampered = json.loads(lines[2])
    assert tampered["summary"] == "REFUTED: effect did not replicate."
    tampered["summary"] = "CONFIRMED: effect replicated cleanly."
    lines[2] = json.dumps(tampered, sort_keys=True)
    ledger_path.write_text("\n".join(lines) + "\n")

    # prev_hash values are untouched, so a naive link-only check would say
    # the chain is clean even though the tail entry's content was rewritten.
    fresh_ledger = Ledger(ledger_path=ledger_path, clock=FakeClock())
    assert fresh_ledger.history()[-1].summary == "CONFIRMED: effect replicated cleanly."
    with pytest.raises(TamperDetectedError) as excinfo:
        fresh_ledger.verify_chain()
    assert excinfo.value.index == 2
    assert excinfo.value.entry_id == "ENGINE-DEC-003"


def test_ids_are_sequential_gap_free_and_survive_reload(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger = Ledger(ledger_path=ledger_path, clock=FakeClock())
    first = ledger.append("DISC-2026-00001", DecisionType.REGISTER, "First.")
    second = ledger.append("DISC-2026-00001", DecisionType.LOCK, "Second.")

    assert first.id == "ENGINE-DEC-001"
    assert second.id == "ENGINE-DEC-002"

    fresh_ledger = Ledger(ledger_path=ledger_path, clock=FakeClock())
    third = fresh_ledger.append("DISC-2026-00002", DecisionType.REGISTER, "Third, after restart.")
    assert third.id == "ENGINE-DEC-003"

    ids = [entry.id for entry in fresh_ledger.history()]
    assert ids == ["ENGINE-DEC-001", "ENGINE-DEC-002", "ENGINE-DEC-003"]
    assert len(set(ids)) == len(ids)


def test_history_filters_by_claim_id_in_order(tmp_path):
    ledger = make_ledger(tmp_path)
    a1 = ledger.append("DISC-2026-00001", DecisionType.REGISTER, "Claim A registered.")
    ledger.append("DISC-2026-00002", DecisionType.REGISTER, "Claim B registered.")
    a2 = ledger.append("DISC-2026-00001", DecisionType.LOCK, "Claim A locked.")
    ledger.append("DISC-2026-00002", DecisionType.LOCK, "Claim B locked.")
    a3 = ledger.append("DISC-2026-00001", DecisionType.RUN, "Claim A run.")

    claim_a_history = ledger.history(claim_id="DISC-2026-00001")
    assert [entry.id for entry in claim_a_history] == [a1.id, a2.id, a3.id]
    assert all(entry.claim_id == "DISC-2026-00001" for entry in claim_a_history)

    claim_b_history = ledger.history(claim_id="DISC-2026-00002")
    assert len(claim_b_history) == 2

    missing_claim_history = ledger.history(claim_id="DISC-2026-99999")
    assert missing_claim_history == []

    assert len(ledger.history()) == 5


def test_no_public_delete_or_update_method_is_exposed(tmp_path):
    ledger = make_ledger(tmp_path)
    ledger.append("DISC-2026-00001", DecisionType.REGISTER, "Claim registered.")

    for forbidden in ("delete", "remove", "update", "edit", "mutate", "rewrite", "pop"):
        assert not hasattr(ledger, forbidden), f"Ledger must not expose a {forbidden!r} method"

    public_callables = {
        name for name in dir(ledger) if not name.startswith("_") and callable(getattr(ledger, name))
    }
    assert public_callables == {"append", "history", "verify_chain"}


def test_entry_is_immutable(tmp_path):
    ledger = make_ledger(tmp_path)
    entry = ledger.append("DISC-2026-00001", DecisionType.REGISTER, "Claim registered.")
    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.summary = "tampered in memory"
    assert entry.summary == "Claim registered."


def test_decision_type_accepts_free_form_strings(tmp_path):
    ledger = make_ledger(tmp_path)
    entry = ledger.append("DISC-2026-00001", "CUSTOM_EVENT", "A non-enum decision type.")
    assert entry.decision_type == "CUSTOM_EVENT"
    assert ledger.verify_chain() is True
