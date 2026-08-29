"""Tests for the Formal Proof / Lean Bridge (`CHECKLIST_09_FORMAL_PROOF_LEAN_BRIDGE.md`).

These tests genuinely shell out to the ``lean`` binary against an isolated
scratch project under a pytest ``tmp_path`` (never the real
``06_DISCOVERY_ENGINE/lean_scratch/``, and never
``04_FORMAL_RESEARCH_LAB/``) — they are slower than the rest of the suite
because of that, which is expected, not a bug (see the module docstring's
"Timing" section: a one-time ~18s cold-start cost the first time any test
in the whole run invokes ``lean``, then ~0.2-0.3s per trivial compile).
"""

from __future__ import annotations

import re

import pytest

from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.ledger import Ledger
from tamesis_discovery_engine.lean_bridge import (
    ClaimNotConfirmedError,
    LeanBridge,
    LeanFormalizationResult,
)
from tamesis_discovery_engine.registry import Registry

from .conftest import FakeClock

CONFIRMED_SEQUENCE = [
    ClaimState.PRE_REGISTERED,
    ClaimState.LOCKED,
    ClaimState.RUNNING,
    ClaimState.RESULT,
    ClaimState.ADVERSARIAL_REVIEW,
    ClaimState.CONFIRMED,
]


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def make_ledger(tmp_path, clock=None):
    return Ledger(ledger_path=tmp_path / "ledger.jsonl", clock=clock or FakeClock())


def make_bridge(tmp_path, registry, ledger):
    return LeanBridge(registry, ledger, scratch_dir=tmp_path / "lean_scratch")


def advance_through(registry, claim, states):
    for state in states:
        claim = registry.advance(claim.id, state)
    return claim


def make_confirmed_claim(registry, title="A genuinely true, trivial fact"):
    claim = registry.create(title, "(1:Nat) + 1 = 2, formalizable with no Mathlib import.")
    return advance_through(registry, claim, CONFIRMED_SEQUENCE)


TRUE_SOURCE = "theorem disc_true : (1:Nat) + 1 = 2 := by decide"
FALSE_SOURCE = "theorem disc_false : (1:Nat) + 1 = 3 := by decide"
MALFORMED_SOURCE = "theorem disc_malformed : (1:Nat) + 1 = 2 := by decide +++ garbage ((("


class TestFormalizeTrueStatement:
    def test_true_statement_against_confirmed_claim_compiles(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        result = bridge.formalize(claim.id, TRUE_SOURCE, "disc_true")

        assert isinstance(result, LeanFormalizationResult)
        assert result.compiled is True
        assert result.stderr == ""
        assert result.duration_seconds >= 0.0
        assert result.lean_file_path.endswith(f"{claim.id}.lean")

    def test_lean_source_file_is_written_under_generated(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        result = bridge.formalize(claim.id, TRUE_SOURCE, "disc_true")

        written_path = tmp_path / "lean_scratch" / "generated" / f"{claim.id}.lean"
        assert written_path.exists()
        assert written_path.read_text() == TRUE_SOURCE
        assert result.lean_file_path == str(written_path)

    def test_scratch_project_has_no_lakefile_and_pins_toolchain(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        bridge.formalize(claim.id, TRUE_SOURCE, "disc_true")

        scratch_dir = tmp_path / "lean_scratch"
        toolchain_path = scratch_dir / "lean-toolchain"
        assert toolchain_path.exists()
        assert toolchain_path.read_text().strip() == "leanprover/lean4:v4.33.0-rc1"
        assert not (scratch_dir / "lakefile.toml").exists()
        assert not (scratch_dir / "lakefile.lean").exists()


class TestFormalizeFalseStatement:
    def test_false_statement_against_confirmed_claim_fails_with_real_error(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        result = bridge.formalize(claim.id, FALSE_SOURCE, "disc_false")

        assert result.compiled is False
        combined = result.stdout + result.stderr
        assert combined.strip() != ""
        assert "false" in combined.lower() or "error" in combined.lower()
        assert "generic" not in combined.lower()
        assert "1 + 1 = 3" in combined or "1+1=3" in combined.replace(" ", "")


class TestFormalizeMalformedStatement:
    def test_malformed_source_fails_without_crashing(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        result = bridge.formalize(claim.id, MALFORMED_SOURCE, "disc_malformed")

        assert result.compiled is False
        combined = result.stdout + result.stderr
        assert combined.strip() != ""

    def test_malformed_failure_text_differs_from_false_statement_failure_text(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)

        false_claim = make_confirmed_claim(registry, title="False fact")
        false_result = bridge.formalize(false_claim.id, FALSE_SOURCE, "disc_false")

        malformed_claim = make_confirmed_claim(registry, title="Malformed source")
        malformed_result = bridge.formalize(malformed_claim.id, MALFORMED_SOURCE, "disc_malformed")

        assert false_result.compiled is False
        assert malformed_result.compiled is False
        assert (false_result.stdout + false_result.stderr) != (
            malformed_result.stdout + malformed_result.stderr
        )


class TestNonConfirmedClaimRaisesWithoutInvokingCompiler:
    def _claim_in_state(self, registry, state):
        claim = registry.create("Not yet confirmed", "statement pending review.")
        if state is ClaimState.DRAFT:
            return claim
        index = CONFIRMED_SEQUENCE.index(state)
        return advance_through(registry, claim, CONFIRMED_SEQUENCE[: index + 1])

    @pytest.mark.parametrize(
        "state",
        [ClaimState.DRAFT, ClaimState.RESULT, ClaimState.REFUTED],
    )
    def test_raises_claim_not_confirmed_error(self, tmp_path, state, monkeypatch):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)

        if state is ClaimState.REFUTED:
            claim = registry.create("Refuted claim", "statement.")
            claim = advance_through(
                registry,
                claim,
                [
                    ClaimState.PRE_REGISTERED,
                    ClaimState.LOCKED,
                    ClaimState.RUNNING,
                    ClaimState.RESULT,
                    ClaimState.ADVERSARIAL_REVIEW,
                    ClaimState.REFUTED,
                ],
            )
        else:
            claim = self._claim_in_state(registry, state)

        assert claim.state is state

        def _fail_if_called(*args, **kwargs):
            raise AssertionError("subprocess.run must not be invoked for a non-CONFIRMED claim")

        monkeypatch.setattr("tamesis_discovery_engine.lean_bridge.subprocess.run", _fail_if_called)

        with pytest.raises(ClaimNotConfirmedError) as exc_info:
            bridge.formalize(claim.id, TRUE_SOURCE, "disc_true")

        assert exc_info.value.claim_id == claim.id
        assert exc_info.value.actual_state is state

        generated_dir = tmp_path / "lean_scratch" / "generated"
        assert not generated_dir.exists() or list(generated_dir.iterdir()) == []


class TestLedgerRecording:
    def test_successful_formalize_appends_exactly_one_ledger_entry(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        before = len(ledger.history(claim.id))
        result = bridge.formalize(claim.id, TRUE_SOURCE, "disc_true")
        after = ledger.history(claim.id)

        assert len(after) == before + 1
        assert result.compiled is True
        entry = after[-1]
        assert entry.decision_type == "LEAN_FORMALIZE"
        assert entry.claim_id == claim.id
        assert "disc_true" in entry.summary

    def test_failed_formalize_still_appends_exactly_one_ledger_entry(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = make_confirmed_claim(registry)

        before = len(ledger.history(claim.id))
        result = bridge.formalize(claim.id, FALSE_SOURCE, "disc_false")
        after = ledger.history(claim.id)

        assert len(after) == before + 1
        assert result.compiled is False
        entry = after[-1]
        assert entry.decision_type == "LEAN_FORMALIZE"

    def test_raising_on_non_confirmed_claim_appends_no_ledger_entry(self, tmp_path):
        registry = make_registry(tmp_path)
        ledger = make_ledger(tmp_path)
        bridge = make_bridge(tmp_path, registry, ledger)
        claim = registry.create("Draft claim", "statement.")

        before = len(ledger.history(claim.id))
        with pytest.raises(ClaimNotConfirmedError):
            bridge.formalize(claim.id, TRUE_SOURCE, "disc_true")
        after = len(ledger.history(claim.id))

        assert after == before


class TestModuleNeverWritesIntoFormalResearchLab:
    def test_source_contains_no_write_call_targeting_formal_research_lab(self):
        from pathlib import Path

        module_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "tamesis_discovery_engine"
            / "lean_bridge.py"
        )
        source = module_path.read_text()

        write_call_pattern = re.compile(
            r"(open\([^)]*04_FORMAL_RESEARCH_LAB|write_text\([^)]*04_FORMAL_RESEARCH_LAB"
            r"|04_FORMAL_RESEARCH_LAB[^\"']*\.write)"
        )
        assert write_call_pattern.search(source) is None
