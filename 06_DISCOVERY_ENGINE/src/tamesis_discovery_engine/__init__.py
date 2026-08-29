"""Tamesis Discovery Engine — Stage 1 MVP facade.

Wires the five independently-testable modules (Hypothesis Registry, Experiment
Runner, Reproduction Engine, Adversarial Reviewer, Decision Ledger) into one
:class:`DiscoveryEngine` object, per
``CHECKLIST_00_INTEGRATION_AND_VALIDATION.md``'s "Integration" section.

Each module keeps owning its own state and its own tests in isolation (see
the per-module ``CHECKLIST_0{1..5}_*.md`` files); this facade adds nothing to
Modules 1-4's internals and does not import :class:`~tamesis_discovery_engine.ledger.Ledger`
into any of them. Instead every :class:`DiscoveryEngine` method is a thin
wrapper: call the underlying module method first, and only once that call has
actually succeeded, append one entry describing it to the shared
:class:`~tamesis_discovery_engine.ledger.Ledger`. A failed call (an illegal
transition, a tampered test plan, a failing experiment, ...) therefore never
produces a ledger entry — the ledger only ever records events that really
happened, mirroring the append-only, hash-chained honesty the ledger itself
enforces on disk.

Data layout: all five modules are constructed to share one ``data/`` root
passed at construction (``data/claims``, ``data/runs``,
``data/reproductions``, ``data/reviews``, ``data/ledger.jsonl`` — exactly the
subpaths each module already defaults to on its own, see each module's
``DEFAULT_DATA_DIR``), so a fresh :class:`DiscoveryEngine` pointed at the same
``data_dir`` sees exactly the same claims/runs/reproductions/reviews/ledger a
previous one left behind.

Event-to-decision-type mapping (the six "major events" the integration
checklist names): ``register()`` -> ``DecisionType.REGISTER``, the generic
``advance()`` (used for the ``DRAFT -> PRE_REGISTERED`` pre-registration step,
the one state-machine step none of Modules 2-4 drives on their own) ->
the free-form ``"ADVANCE"`` decision type (the ledger's ``decision_type`` is
documented as accepting any caller-chosen string, not only
:class:`~tamesis_discovery_engine.ledger.DecisionType`'s controlled
vocabulary), ``lock()`` -> ``DecisionType.LOCK``, ``run()`` ->
``DecisionType.RUN``, ``reproduce()`` -> ``DecisionType.REPRODUCE``,
``review()`` -> ``DecisionType.REVIEW``, ``record_verdict()`` ->
``DecisionType.VERDICT``.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional, Union

from .adversarial import DEFAULT_INSTABILITY_TOLERANCE, AdversarialReviewer, ReviewVerdict
from .claim import Claim, ClaimState
from .ledger import DecisionType, Ledger
from .registry import Registry
from .reproduction import ReproductionPlan, ReproductionRecord, Reproducer
from .runner import RunRecord, Runner, TestPlan

__all__ = ["DiscoveryEngine", "DEFAULT_DATA_DIR"]

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

_ADVANCE_DECISION_TYPE = "ADVANCE"


class DiscoveryEngine:
    """Facade wiring the Hypothesis Registry, Experiment Runner, Reproduction
    Engine, Adversarial Reviewer, and Decision Ledger around one shared
    ``data_dir`` root.

    ``data_dir`` defaults to ``06_DISCOVERY_ENGINE/data`` (created if absent,
    along with its five children); pass an explicit directory (e.g. a pytest
    ``tmp_path``) to keep an engine's state isolated. ``clock`` defaults to
    ``datetime.now(timezone.utc)`` (independently, per module) but can be
    injected once here and is threaded through to every module for
    deterministic, non-flaky timestamp assertions — every module accepts the
    exact same ``Clock`` shape (``Callable[[], datetime]``), so a single
    ``clock`` instance keeps every subsystem's timestamps on one, consistently
    advancing, virtual clock.

    Every method below (``register``, ``advance``, ``lock``, ``run``,
    ``reproduce``, ``review``, ``record_verdict``) drives exactly one
    underlying module call and, only on that call's success, appends one
    entry to :attr:`ledger`. Use :attr:`registry`, :attr:`runner`,
    :attr:`reproducer`, and :attr:`reviewer` directly for anything this
    facade does not wrap (e.g. ``registry.list(...)``).
    """

    def __init__(self, data_dir: Optional[Path | str] = None, clock: Optional[Clock] = None):
        self.data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.registry = Registry(data_dir=self.data_dir / "claims", clock=clock)
        self.runner = Runner(self.registry, data_dir=self.data_dir / "runs", clock=clock)
        self.reproducer = Reproducer(
            self.registry, self.runner, data_dir=self.data_dir / "reproductions", clock=clock
        )
        self.reviewer = AdversarialReviewer(
            self.registry, self.runner, self.reproducer, data_dir=self.data_dir / "reviews", clock=clock
        )
        self.ledger = Ledger(ledger_path=self.data_dir / "ledger.jsonl", clock=clock)

    def register(self, title: str, statement: str, metadata: Optional[Dict] = None) -> Claim:
        claim = self.registry.create(title, statement, metadata=metadata)
        self.ledger.append(
            claim.id,
            DecisionType.REGISTER,
            f"Claim registered: {title!r} — {statement}",
        )
        return claim

    def advance(self, claim_id: str, to_state: Union[ClaimState, str], note: str = "") -> Claim:
        claim = self.registry.advance(claim_id, to_state, note=note)
        summary = f"Claim advanced to {claim.state.value}"
        if note:
            summary += f": {note}"
        self.ledger.append(claim_id, _ADVANCE_DECISION_TYPE, summary)
        return claim

    def lock(self, claim_id: str, test_plan: TestPlan) -> Claim:
        claim = self.runner.lock(claim_id, test_plan)
        self.ledger.append(
            claim_id,
            DecisionType.LOCK,
            f"Locked test plan {test_plan.qualified_name} (source hash {test_plan.source_hash()[:12]}...)",
        )
        return claim

    def run(self, claim_id: str, test_plan: TestPlan) -> RunRecord:
        record = self.runner.run(claim_id, test_plan)
        outcome = "succeeded" if record.success else "failed"
        self.ledger.append(
            claim_id,
            DecisionType.RUN,
            f"Run of {test_plan.qualified_name} {outcome}",
        )
        return record

    def reproduce(
        self,
        claim_id: str,
        second_test_plan: ReproductionPlan,
        tolerance: float = 1e-9,
    ) -> ReproductionRecord:
        record = self.reproducer.reproduce(claim_id, second_test_plan, tolerance=tolerance)
        self.ledger.append(
            claim_id,
            DecisionType.REPRODUCE,
            f"Reproduction via {second_test_plan.qualified_name}: {record.verdict}",
        )
        return record

    def review(
        self,
        claim_id: str,
        test_plan: Optional[TestPlan] = None,
        instability_tolerance: float = DEFAULT_INSTABILITY_TOLERANCE,
    ) -> ReviewVerdict:
        verdict = self.reviewer.review(
            claim_id, test_plan=test_plan, instability_tolerance=instability_tolerance
        )
        self.ledger.append(
            claim_id,
            DecisionType.REVIEW,
            f"Adversarial review recommendation: {verdict.recommendation} "
            f"({len(verdict.flags)} flag(s), {len(verdict.skipped_checks)} check(s) skipped)",
        )
        return verdict

    def record_verdict(self, claim_id: str, verdict: Union[str, ClaimState], rationale: str) -> Claim:
        claim = self.reviewer.record_verdict(claim_id, verdict, rationale)
        self.ledger.append(
            claim_id,
            DecisionType.VERDICT,
            f"Verdict recorded: {claim.state.value} — {rationale}",
        )
        return claim

    def get(self, claim_id: str) -> Claim:
        return self.registry.get(claim_id)
