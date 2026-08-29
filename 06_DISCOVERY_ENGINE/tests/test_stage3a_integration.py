"""Stage 3a integration tests (`CHECKLIST_00C_STAGE3A_INTEGRATION.md`).

Verifies the facade extension: Module 11's `HypothesisEngine` and Module
12's `MathDiscoveryPipeline` are constructed alongside Stage 1/2's ten
existing modules and are reachable through one `DiscoveryEngine` instance.

Both new modules are, by design, stateless (see each module's own "Scope
honesty constraint"): `HypothesisEngine`'s methods take the caller's
`Registry` explicitly rather than holding one, and every
`MathDiscoveryPipeline` method is a pure function of its arguments. So
"sharing the same data_dir/registry where applicable" means: the facade
constructs one instance of each, `engine.hypothesis_engine` is called with
`engine.registry` explicitly, and `engine.math_discovery` needs no registry
at all — it never touches a `Claim`.

`test_hypothesis_engine_claim_drives_full_stage1_lifecycle_and_math_discovery_runs_standalone`
is the primary scenario the checklist names: a claim drafted through
`HypothesisEngine.draft()` with a structured `FalsifiableSpec` is driven
through Stage 1's existing `lock`/`run`/`reproduce`/`review`/`record_verdict`
facade methods to a terminal `CONFIRMED` verdict — proving Module 11
composes with Stage 1 through the facade — and then, in the same test but
deliberately *not* touching that claim or its registry at all, a
`MathDiscoveryPipeline.run()` call against a small toy problem with two
candidates proves Module 12 is independently reachable through the same
facade. Per the checklist: neither module is on the other's (or the
Hypothesis Engine claim's) critical path — this test proves both are
reachable through the one facade, not that they depend on each other.

The Hypothesis Engine scenario is deliberately left to report a `FLAGGED`
review rather than a fabricated `CLEAN` one: `FalsifiableSpec.threshold`
(Module 11's structured spec field) and `SUCCESS_THRESHOLD_KEY` (Module 4's
own declared-success-threshold metadata key, checked by the
`post_hoc_threshold` review check) are two different concepts that this
integration does not silently reconcile — a claim drafted purely through
`HypothesisEngine.draft()` never populates the latter, so the review is
honestly flagged for it, exactly the kind of real (not rigged) outcome this
archive's own ethos requires reporting rather than papering over.
"""

from __future__ import annotations

import pytest
import sympy

from tamesis_discovery_engine import DiscoveryEngine
from tamesis_discovery_engine.adversarial import CHECK_POST_HOC_THRESHOLD
from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.hypothesis_engine import FalsifiableSpec, HypothesisEngine, IncompleteSpecError
from tamesis_discovery_engine.mathematical_discovery_engine import Enumerator, MathDiscoveryPipeline
from tamesis_discovery_engine.reproduction import ReproductionPlan
from tamesis_discovery_engine.runner import TestPlan

from .conftest import FakeClock

GROUP_A = [1.0, 2.0, 1.5, 2.5]
GROUP_B = [4.0, 4.5, 3.5, 5.0]

n = sympy.Symbol("n")
i = sympy.Symbol("i")

TRUE_TRIANGULAR = n * (n + 1) / 2
WRONG_TRIANGULAR = n**2

SYMBOLIC_TRIANGULAR_TARGET = sympy.summation(i, (i, 1, n))

TRIANGULAR_ENUMERATOR_NS = list(range(0, 6))


def make_engine(tmp_path, clock=None):
    return DiscoveryEngine(data_dir=tmp_path / "data", clock=clock or FakeClock())


def make_complete_spec() -> FalsifiableSpec:
    return FalsifiableSpec(
        raw_claim="Toy group B has a materially larger mean than toy group A.",
        prediction="mean(group_b) - mean(group_a) is at least 2.0",
        null_model="mean(group_b) - mean(group_a) equals 0",
        competing_model=None,
        competing_model_rationale="Synthetic toy groups with no plausible confound to model.",
        effect_size_metric="difference of sample means (group_b - group_a)",
        threshold=2.0,
    )


def group_difference_test_plan_fn():
    difference = float(sum(GROUP_B) / len(GROUP_B) - sum(GROUP_A) / len(GROUP_A))
    return {"difference": difference, "holds": difference >= 2.0}


def group_difference_reproduction_fn():
    """A second, independently-written implementation of the same quantity.

    Computes the same group-mean difference via running totals rather than
    ``sum()``/``len()`` division, so this is genuinely a different code path
    from :func:`group_difference_test_plan_fn`, not the same call copied —
    the "second, independent implementation" the Reproduction Engine (Module
    3) exists to check against.
    """

    total_b, count_b = 0.0, 0
    for value in GROUP_B:
        total_b += value
        count_b += 1
    total_a, count_a = 0.0, 0
    for value in GROUP_A:
        total_a += value
        count_a += 1
    difference = (total_b / count_b) - (total_a / count_a)
    return {"difference": difference, "holds": difference >= 2.0}


def exact_triangular(k: int) -> int:
    total = 0
    for value in range(1, k + 1):
        total += value
    return total


def test_engine_exposes_hypothesis_engine_and_math_discovery_sharing_registry(tmp_path):
    engine = make_engine(tmp_path)

    assert isinstance(engine.hypothesis_engine, HypothesisEngine)
    assert isinstance(engine.math_discovery, MathDiscoveryPipeline)

    spec = make_complete_spec()
    claim = engine.hypothesis_engine.draft(engine.registry, "Facade wiring check", spec)

    assert engine.get(claim.id).id == claim.id
    assert engine.registry.get(claim.id).state is ClaimState.DRAFT


class TestHypothesisEngineClaimComposesWithStage1AndMathDiscoveryRunsStandalone:
    def test_hypothesis_engine_claim_drives_full_stage1_lifecycle_and_math_discovery_runs_standalone(
        self, tmp_path
    ):
        clock = FakeClock()
        engine = make_engine(tmp_path, clock=clock)

        # --- Part 1: HypothesisEngine.draft() through Stage 1's existing lifecycle ---

        spec = make_complete_spec()
        claim = engine.hypothesis_engine.draft(engine.registry, "Toy group-difference hypothesis", spec)
        assert claim.state is ClaimState.DRAFT
        assert claim.statement == spec.raw_claim
        assert engine.registry.get(claim.id).metadata["falsifiable_spec"]["prediction"] == spec.prediction

        pre_registered = engine.hypothesis_engine.pre_register(engine.registry, claim.id)
        assert pre_registered.state is ClaimState.PRE_REGISTERED

        test_plan = TestPlan(name="toy-group-difference", version="v1", fn=group_difference_test_plan_fn)
        engine.lock(claim.id, test_plan)

        run_record = engine.run(claim.id, test_plan)
        assert run_record.success is True
        assert run_record.result["holds"] is True
        assert engine.get(claim.id).state is ClaimState.RESULT

        repro_record = engine.reproduce(
            claim.id,
            ReproductionPlan(
                name="toy-group-difference-independent", version="v1", fn=group_difference_reproduction_fn
            ),
            tolerance=1e-9,
        )
        assert repro_record.verdict == "EXACT_MATCH"
        assert repro_record.original_test_plan == "toy-group-difference@v1"

        verdict = engine.review(claim.id, test_plan=test_plan)
        assert engine.get(claim.id).state is ClaimState.ADVERSARIAL_REVIEW
        assert verdict.recommendation == "FLAGGED"
        assert any(flag.check == CHECK_POST_HOC_THRESHOLD for flag in verdict.flags)

        final_claim = engine.record_verdict(
            claim.id,
            ClaimState.CONFIRMED,
            "Independent reproduction is an EXACT_MATCH; the FLAGGED post_hoc_threshold "
            "check reflects that this claim was drafted through HypothesisEngine.draft() "
            "alone, which never declares Module 4's separate success_threshold metadata "
            "key, not a data-integrity problem with the toy result itself.",
        )
        assert final_claim.state is ClaimState.CONFIRMED

        ledger_decision_types = [entry.decision_type for entry in engine.ledger.history(claim_id=claim.id)]
        assert ledger_decision_types == ["LOCK", "RUN", "REPRODUCE", "REVIEW", "VERDICT"]
        assert engine.ledger.verify_chain() is True

        # --- Part 2: MathDiscoveryPipeline.run(), standalone, same facade instance ---
        # Deliberately independent of the claim above: no claim id, no
        # registry access, nothing terminal-state-gated -- proving Module 12
        # is reachable through the facade without being on Module 11's claim's
        # critical path (per the checklist's own framing).

        results = engine.math_discovery.run(
            [("true_triangular", TRUE_TRIANGULAR), ("wrong_triangular", WRONG_TRIANGULAR)],
            free_symbols=[n],
            symbolic_target=SYMBOLIC_TRIANGULAR_TARGET,
            enumerator=Enumerator(fn=exact_triangular, ns=TRIANGULAR_ENUMERATOR_NS, symbol="n"),
        )

        assert [result.candidate_name for result in results] == ["true_triangular", "wrong_triangular"]

        true_result, wrong_result = results
        assert true_result.verdict == "SURVIVES"
        assert true_result.enumeration_match is True
        assert true_result.symbolic_match is True
        assert set(true_result.details) == {"enumeration", "symbolic"}

        assert wrong_result.verdict == "REFUTED"
        assert wrong_result.enumeration_match is False
        assert wrong_result.symbolic_match is False

        # The math-discovery call above touched no claim and no registry.
        assert [c.id for c in engine.registry.list()] == [claim.id]


def test_facade_advance_bypasses_hypothesis_engine_pre_register_completeness_check(tmp_path):
    """Scope honesty regression (see hypothesis_engine.py's module docstring
    and CHECKLIST_11's "Scope honesty constraint"): `HypothesisEngine.pre_register()`
    enforces `FalsifiableSpec` completeness only for callers that go through
    it. The facade's own generic `DiscoveryEngine.advance()` -- named by this
    module's own docstring as "the DRAFT -> PRE_REGISTERED pre-registration
    step" and used for exactly that purpose elsewhere in this test suite
    (`test_integration.py`) -- drives the same transition with zero spec
    checking, because it (like `Registry.advance()` underneath it) knows
    nothing about `HypothesisEngine` or `FalsifiableSpec`.

    This pins down that a claim drafted through `HypothesisEngine.draft()`,
    then hand-tampered into an incomplete spec, is correctly rejected by
    `HypothesisEngine.pre_register()` but reaches `PRE_REGISTERED` anyway
    via `engine.advance()` -- so this behavior cannot be silently
    "fixed" by a future doc edit alone without a test failing first.
    """
    engine = make_engine(tmp_path)

    spec = make_complete_spec()
    claim = engine.hypothesis_engine.draft(engine.registry, "Toy group-difference hypothesis", spec)

    tampered = engine.registry.get(claim.id)
    tampered.metadata["falsifiable_spec"]["prediction"] = ""
    engine.registry._save(tampered)

    with pytest.raises(IncompleteSpecError):
        engine.hypothesis_engine.pre_register(engine.registry, claim.id)
    assert engine.registry.get(claim.id).state is ClaimState.DRAFT

    # The generic facade method bypasses the completeness check entirely.
    advanced = engine.advance(claim.id, ClaimState.PRE_REGISTERED)
    assert advanced.state is ClaimState.PRE_REGISTERED
    assert engine.registry.get(claim.id).state is ClaimState.PRE_REGISTERED
