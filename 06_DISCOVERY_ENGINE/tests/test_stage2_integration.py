"""Stage 2 integration tests (`CHECKLIST_00B_STAGE2_INTEGRATION.md`).

Verifies the facade extension: the five Stage 2 modules (symbolic,
montecarlo, observatory, lean_bridge, atlas) are constructed alongside
Stage 1's original five, sharing one `data_dir` root, and — the real point
of Stage 2 — compose with Stage 1 and each other rather than merely passing
in isolation.

`TestSymbolicLockRunReproduceReviewConfirmFormalizeCatalogue` is the primary
scenario the checklist itself names: a claim whose test plan comes from
Module 6 (`symbolic.make_symbolic_identity_test_plan`), locked/run through
Stage 1's `Runner`, reproduced via Module 6's second, genuinely different
numeric route (`verify_numeric_spot_check`) through Stage 1's `Reproducer`,
reviewed and confirmed through Stage 1's `AdversarialReviewer`, and then —
only once `CONFIRMED` — formalized via Module 9's `LeanBridge` and
catalogued via Module 10's `Atlas`. That already exercises three of the
five new modules (symbolic, lean_bridge, atlas) together through the
facade; `test_montecarlo_and_observatory_wired_and_usable_via_facade`
exercises the remaining two (montecarlo, observatory) so all five are
proven functional, not just constructed.

The Lean bridge test in this file genuinely shells out to `lean` (see
`test_lean_bridge.py`'s own docstring on timing) — expected to be slower
than the rest of the suite, not a bug.
"""

from __future__ import annotations

import pytest
import sympy

from tamesis_discovery_engine import DiscoveryEngine
from tamesis_discovery_engine import montecarlo as montecarlo_module
from tamesis_discovery_engine import symbolic as symbolic_module
from tamesis_discovery_engine.adversarial import SUCCESS_THRESHOLD_KEY, format_threshold_note
from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.reproduction import ReproductionPlan

from .conftest import FakeClock


def make_engine(tmp_path, clock=None):
    return DiscoveryEngine(data_dir=tmp_path / "data", clock=clock or FakeClock())


def numeric_spot_check_reproduction_fn(lhs, rhs, free_symbols=None):
    """A genuinely different verification route than the original run's:

    the original run's test plan (`make_symbolic_identity_test_plan`) decides
    `holds` via `verify_identity`'s symbolic `simplify`/`equals` route; this
    reproduction decides the exact same `lhs == rhs` question via
    `verify_numeric_spot_check`'s numeric substitution route instead, never
    calling `simplify` or `equals` — the "second, independent implementation"
    Module 3 (Reproduction Engine) is meant to check against.
    """
    substitutions = [{"x": value} for value in (-3.0, 0.0, 2.5, 7.25)]
    result = symbolic_module.verify_numeric_spot_check(lhs, rhs, substitutions)
    return {"holds": result.holds}


def test_engine_exposes_five_new_modules_sharing_data_dir(tmp_path):
    engine = make_engine(tmp_path)

    assert engine.symbolic is symbolic_module
    assert engine.montecarlo is montecarlo_module

    assert engine.observatory.data_dir == tmp_path / "data" / "datasets"
    assert engine.atlas.data_dir == tmp_path / "data" / "atlas"
    assert engine.atlas.registry is engine.registry

    assert engine.lean_bridge.registry is engine.registry
    assert engine.lean_bridge.ledger is engine.ledger
    assert engine.lean_bridge.scratch_dir == tmp_path / "lean_scratch"

    assert engine.data_dir == tmp_path / "data"


class TestSymbolicLockRunReproduceReviewConfirmFormalizeCatalogue:
    def test_full_stage2_scenario_through_the_facade(self, tmp_path):
        clock = FakeClock()
        engine = make_engine(tmp_path, clock=clock)

        x = sympy.Symbol("x")
        test_plan = engine.symbolic.make_symbolic_identity_test_plan(
            "expand-square", (x + 1) ** 2, x**2 + 2 * x + 1, free_symbols=[x]
        )

        claim = engine.register(
            "Binomial square expansion",
            "(x + 1)**2 equals x**2 + 2*x + 1 for all real x.",
            metadata={SUCCESS_THRESHOLD_KEY: 0.0},
        )
        assert claim.state is ClaimState.DRAFT

        engine.advance(claim.id, ClaimState.PRE_REGISTERED, note=format_threshold_note(0.0))
        engine.lock(claim.id, test_plan)

        run_record = engine.run(claim.id, test_plan)
        assert run_record.success is True
        assert run_record.result == {"holds": True}
        assert engine.get(claim.id).state is ClaimState.RESULT

        repro_record = engine.reproduce(
            claim.id,
            ReproductionPlan(name="numeric-spot-check", version="v1", fn=numeric_spot_check_reproduction_fn),
            tolerance=1e-9,
        )
        assert repro_record.verdict == "EXACT_MATCH"
        assert repro_record.original_test_plan == "expand-square@v1"
        assert repro_record.reproduction_test_plan == "numeric-spot-check@v1"

        verdict = engine.review(claim.id, test_plan=test_plan)
        assert verdict.recommendation == "CLEAN"
        assert engine.get(claim.id).state is ClaimState.ADVERSARIAL_REVIEW

        final_claim = engine.record_verdict(
            claim.id,
            ClaimState.CONFIRMED,
            "Symbolic simplification holds and an independent numeric spot-check agrees.",
        )
        assert final_claim.state is ClaimState.CONFIRMED

        theorem_name = f"stage2_{claim.id.replace('-', '_')}"
        lean_source = f"theorem {theorem_name} : (1:Nat) + 1 = 2 := by decide"
        ledger_entries_before = len(engine.ledger.history(claim_id=claim.id))

        formalization = engine.lean_bridge.formalize(claim.id, lean_source, theorem_name)
        assert formalization.compiled is True

        ledger_entries_after = engine.ledger.history(claim_id=claim.id)
        assert len(ledger_entries_after) == ledger_entries_before + 1
        assert ledger_entries_after[-1].decision_type == "LEAN_FORMALIZE"
        assert theorem_name in ledger_entries_after[-1].summary

        entry = engine.atlas.register(
            domain="symbolic_algebra",
            invariant_name="binomial_square_expansion_offset",
            value=0.0,
            source_claim_id=claim.id,
        )
        assert entry.verdict is ClaimState.CONFIRMED
        assert entry.source_claim_id == claim.id

        found = engine.atlas.search(domain="symbolic_algebra")
        assert entry in found

        near_dupes = engine.atlas.find_near_duplicates(
            domain="symbolic_algebra", invariant_name="anything_else", value=0.0, tolerance=1e-9
        )
        assert entry in near_dupes

        assert engine.ledger.verify_chain() is True

    def test_lean_bridge_refuses_to_formalize_before_confirmed(self, tmp_path):
        from tamesis_discovery_engine.lean_bridge import ClaimNotConfirmedError

        engine = make_engine(tmp_path)
        claim = engine.register("Unconfirmed claim", "not yet reviewed.")

        with pytest.raises(ClaimNotConfirmedError):
            engine.lean_bridge.formalize(claim.id, "theorem t : (1:Nat) + 1 = 2 := by decide", "t")

    def test_atlas_refuses_to_catalogue_a_non_terminal_claim(self, tmp_path):
        from tamesis_discovery_engine.atlas import NonTerminalClaimError

        engine = make_engine(tmp_path)
        claim = engine.register("Open claim", "still running.")

        with pytest.raises(NonTerminalClaimError):
            engine.atlas.register("domain", "invariant", 1.0, source_claim_id=claim.id)


def test_montecarlo_and_observatory_wired_and_usable_via_facade(tmp_path):
    clock = FakeClock()
    engine = make_engine(tmp_path, clock=clock)

    def constant_estimator(rng):
        return 1.0

    triangulation = engine.montecarlo.triangulate(
        estimators=[("estimator-a", constant_estimator), ("estimator-b", constant_estimator)],
        n_trials=5,
        seed=1,
    )
    assert triangulation.agrees is True

    claim = engine.register("Reference dataset claim", "A claim that cites external reference data.")

    dataset = engine.observatory.ingest(
        "toy-reference-table", "2024", "synthetic stand-in citation, not a real data source", b"synthetic-bytes"
    )
    engine.observatory.record_usage(claim.id, dataset.name, dataset.version)

    assert engine.observatory.verify_integrity(dataset.name, dataset.version) is True
    assert claim.id in engine.observatory.used_by(dataset.name, dataset.version)
    assert dataset in engine.observatory.datasets_used_by(claim.id)
