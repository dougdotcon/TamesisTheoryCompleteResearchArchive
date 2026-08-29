"""Adversarial Reviewer — Module 4 of the Tamesis Discovery Engine.

Runs a small set of concrete, heuristic sanity checks against a claim that
has already been reproduced (``ROADMAP.md`` Stage 1, item 4, and Stage 3's
"Tamesis Adversarial Reviewer" description), building on Module 1's
:class:`~tamesis_discovery_engine.registry.Registry`, Module 2's
:class:`~tamesis_discovery_engine.runner.Runner`/:class:`~tamesis_discovery_engine.runner.TestPlan`,
and Module 3's :class:`~tamesis_discovery_engine.reproduction.Reproducer` rather
than redefining any of them.

Design honesty constraint
--------------------------
There is no deterministic algorithm that detects "p-hacking" in general.
This module does **not** claim to. It runs four narrow, concrete, testable
heuristics — a post-hoc-threshold check, a reseeded numerical-instability
check, a parameter-count/sample-count smell check, and a calibration/
validation index-overlap check — and is explicit, in every
:class:`ReviewVerdict`, about which of those checks actually ran
(``all_checks_run``) versus which were structurally inapplicable and
skipped (``skipped_checks``). A check that cannot be made concrete and
testable is cut rather than stubbed out as something that always reports
clean.

The verdict this module produces is a *recommendation*, never a claim
verdict by itself: :meth:`AdversarialReviewer.review` only ever drives the
claim from ``RESULT`` into ``ADVERSARIAL_REVIEW`` (an "under review", not a
terminal, state). Moving a claim into one of the four terminal states is a
**separate, explicit** act — :meth:`AdversarialReviewer.record_verdict` —
that always requires a human-authored, non-empty ``rationale`` and can only
be called after at least one real review pass is on record. Automating the
terminal transition end-to-end from a heuristic score would be exactly the
kind of unaccountable automation this archive's own ethos rejects.

Why check 1 reads ``history`` notes, not a metadata-edit log
---------------------------------------------------------------
Module 1's ``Registry`` has no API to edit a claim's ``metadata`` after
``create()`` — metadata is set once, at ``DRAFT`` time, and every later
``advance()`` call only appends a ``TransitionRecord``. So "the threshold
was recorded in history at the ``PRE_REGISTERED`` transition, and metadata
still agrees with it" is checked by comparing ``claim.metadata`` against a
threshold value encoded (via :func:`format_threshold_note`) in the *note*
of the ``DRAFT -> PRE_REGISTERED`` transition record — the one piece of
Module 1's audit trail that is genuinely timestamped and append-only. A
mismatch between the two is the concrete, testable signature of a
post-hoc edit; this module never mutates a claim's metadata to construct
that signature itself (only test fixtures do, by writing directly to the
claim store, simulating the very tampering the check exists to catch).

Why check 2 calls the test plan directly, not ``Runner.run``
------------------------------------------------------------
Module 2's ``LockRecord`` deliberately does not retain the locked
callable (only its source hash), and ``Runner.run`` requires the claim to
be in ``LOCKED`` state and always advances/persists a new ``RunRecord`` —
neither is compatible with re-running an already-``RESULT`` claim "off the
record". So :meth:`AdversarialReviewer.review` accepts an optional
``test_plan`` (the same :class:`~tamesis_discovery_engine.runner.TestPlan`
the caller locked/ran originally) and, when the run's params declare a
``seed``, invokes ``test_plan.fn`` directly with reseeded params — the
same callable the Experiment Runner would invoke, but without going
through ``Runner.lock``/``Runner.run`` and without writing a
``RunRecord`` for the claim.
"""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from .claim import Claim, ClaimState, TransitionRecord, coerce_state
from .registry import Registry
from .reproduction import Reproducer
from .runner import Runner, TestPlan

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "reviews"

CHECK_POST_HOC_THRESHOLD = "post_hoc_threshold"
CHECK_NUMERICAL_INSTABILITY = "numerical_instability"
CHECK_OVERFITTING = "overfitting_parameter_count"
CHECK_LEAKAGE = "leakage"

SUCCESS_THRESHOLD_KEY = "success_threshold"
DEFAULT_INSTABILITY_TOLERANCE = 0.05
_SEED_OFFSETS = (1, 2)

_CALIBRATION_KEYS = ("calibration_indices", "calib_indices")
_VALIDATION_KEYS = ("validation_indices", "val_indices")

_TERMINAL_VERDICT_STATES = frozenset(
    {ClaimState.CONFIRMED, ClaimState.REFUTED, ClaimState.INCONCLUSIVE, ClaimState.NULL}
)

_THRESHOLD_NOTE_PREFIX = "declared_success_threshold="

_MISSING = object()


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


class ReviewPreconditionError(Exception):
    """Raised by :meth:`AdversarialReviewer.review` when its precondition fails.

    Review cannot start without a successful reproduction on file (mirrors
    the archive's own "reproduce before referee" order), and cannot be
    (re)started on a claim that is not sitting at ``RESULT`` or already
    ``ADVERSARIAL_REVIEW`` (e.g. a claim that already has a terminal
    verdict is not up for review again).
    """

    def __init__(self, claim_id: str, reason: str):
        self.claim_id = claim_id
        self.reason = reason
        super().__init__(f"Cannot review claim {claim_id!r}: {reason}")


class VerdictWithoutReviewError(Exception):
    """Raised by ``record_verdict`` when no review has ever been recorded."""

    def __init__(self, claim_id: str):
        self.claim_id = claim_id
        super().__init__(
            f"Cannot record a verdict for claim {claim_id!r}: review() has never "
            f"been run for this claim, so there is no adversarial pass on record"
        )


class EmptyRationaleError(Exception):
    """Raised by ``record_verdict`` when ``rationale`` is empty/whitespace."""

    def __init__(self, claim_id: str):
        self.claim_id = claim_id
        super().__init__(
            f"Cannot record a verdict for claim {claim_id!r}: rationale must be a "
            f"non-empty, human-authored explanation of the decision"
        )


class InvalidVerdictError(Exception):
    """Raised by ``record_verdict`` when ``verdict`` is not a terminal state."""

    def __init__(self, claim_id: str, verdict: Any):
        self.claim_id = claim_id
        self.verdict = verdict
        super().__init__(
            f"Cannot record verdict {verdict!r} for claim {claim_id!r}: must be one "
            f"of {sorted(state.value for state in _TERMINAL_VERDICT_STATES)}"
        )


def format_threshold_note(value: Any) -> str:
    """Encode a declared success threshold into a ``TransitionRecord.note``.

    Callers pre-registering a claim should pass
    ``registry.advance(claim_id, PRE_REGISTERED, note=format_threshold_note(value))``
    so the threshold's declaration is captured in Module 1's append-only
    history at the moment it happened.
    """

    return f"{_THRESHOLD_NOTE_PREFIX}{json.dumps(value)}"


def parse_threshold_note(note: Optional[str]) -> Any:
    if not note or not note.startswith(_THRESHOLD_NOTE_PREFIX):
        return None
    try:
        return json.loads(note[len(_THRESHOLD_NOTE_PREFIX) :])
    except json.JSONDecodeError:
        return None


@dataclasses.dataclass
class ReviewFlag:
    check: str
    severity: str
    detail: str

    def to_dict(self) -> Dict[str, Any]:
        return {"check": self.check, "severity": self.severity, "detail": self.detail}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReviewFlag":
        return cls(check=data["check"], severity=data["severity"], detail=data["detail"])


@dataclasses.dataclass
class SkippedCheck:
    check: str
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {"check": self.check, "reason": self.reason}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkippedCheck":
        return cls(check=data["check"], reason=data["reason"])


@dataclasses.dataclass
class ReviewVerdict:
    claim_id: str
    flags: List[ReviewFlag]
    all_checks_run: List[str]
    skipped_checks: List[SkippedCheck]
    recommendation: str
    reviewed_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "flags": [flag.to_dict() for flag in self.flags],
            "all_checks_run": list(self.all_checks_run),
            "skipped_checks": [skipped.to_dict() for skipped in self.skipped_checks],
            "recommendation": self.recommendation,
            "reviewed_at": self.reviewed_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReviewVerdict":
        return cls(
            claim_id=data["claim_id"],
            flags=[ReviewFlag.from_dict(item) for item in data.get("flags", [])],
            all_checks_run=list(data.get("all_checks_run", [])),
            skipped_checks=[SkippedCheck.from_dict(item) for item in data.get("skipped_checks", [])],
            recommendation=data["recommendation"],
            reviewed_at=datetime.fromisoformat(data["reviewed_at"]),
        )


def _reviews_path(claim_id: str, data_dir: Path) -> Path:
    return data_dir / f"{claim_id}.jsonl"


def list_reviews(claim_id: str, data_dir: Optional[Path | str] = None) -> List[ReviewVerdict]:
    directory = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    path = _reviews_path(claim_id, directory)
    if not path.exists():
        return []
    records = []
    with path.open("r") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(ReviewVerdict.from_dict(json.loads(line)))
    return records


def has_been_reviewed(claim_id: str, data_dir: Optional[Path | str] = None) -> bool:
    return len(list_reviews(claim_id, data_dir=data_dir)) > 0


def _find_note_at_transition(history: List[TransitionRecord], target_state: ClaimState) -> Optional[str]:
    for record in history:
        if record.to_state is target_state:
            return record.note
    return None


def _check_post_hoc_threshold(claim: Claim) -> Optional[ReviewFlag]:
    declared = claim.metadata.get(SUCCESS_THRESHOLD_KEY, _MISSING)
    if declared is _MISSING:
        return ReviewFlag(
            CHECK_POST_HOC_THRESHOLD,
            "ERROR",
            f"No {SUCCESS_THRESHOLD_KEY!r} present in claim metadata: no success "
            f"threshold/criterion was ever declared.",
        )

    pre_reg_note = _find_note_at_transition(claim.history, ClaimState.PRE_REGISTERED)
    recorded = parse_threshold_note(pre_reg_note)
    if recorded is None:
        return ReviewFlag(
            CHECK_POST_HOC_THRESHOLD,
            "ERROR",
            f"{SUCCESS_THRESHOLD_KEY!r} is present in metadata but was never recorded "
            f"in history at the PRE_REGISTERED transition — it was not declared "
            f"before locking.",
        )

    if recorded != declared:
        return ReviewFlag(
            CHECK_POST_HOC_THRESHOLD,
            "ERROR",
            f"{SUCCESS_THRESHOLD_KEY!r} in metadata ({declared!r}) does not match the "
            f"value recorded at PRE_REGISTERED time ({recorded!r}) — looks like a "
            f"post-hoc edit made after locking.",
        )

    return None


def _flatten_numeric(value: Any, prefix: str, out: Dict[str, float]) -> None:
    if isinstance(value, dict):
        for key in sorted(value, key=str):
            _flatten_numeric(value[key], f"{prefix}.{key}" if prefix else str(key), out)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _flatten_numeric(item, f"{prefix}[{index}]", out)
        return
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        out[prefix] = float(value)


def _lookup_field(params: Dict[str, Any], result: Optional[Dict[str, Any]], key: str) -> Any:
    if key in params:
        return params[key]
    if isinstance(result, dict) and key in result:
        return result[key]
    return None


def _lookup_index_set(params: Dict[str, Any], aliases: tuple) -> Any:
    for alias in aliases:
        if alias in params:
            return params[alias]
    return None


class AdversarialReviewer:
    """Runs the adversarial checks and records the accountable verdict.

    ``registry``/``runner``/``reproducer`` are the Module 1/2/3 objects this
    class reads claim state, the original ``RunRecord``, and reproduction
    status through — it never mutates a ``Claim``'s ``metadata`` or writes a
    ``RunRecord`` itself. ``data_dir`` defaults to
    ``06_DISCOVERY_ENGINE/data/reviews`` (created if absent); pass an
    explicit directory (e.g. a pytest ``tmp_path``) to keep reviews
    isolated. ``clock`` defaults to ``datetime.now(timezone.utc)`` but can
    be injected for deterministic timestamp assertions.
    """

    def __init__(
        self,
        registry: Registry,
        runner: Runner,
        reproducer: Reproducer,
        data_dir: Optional[Path | str] = None,
        clock: Optional[Clock] = None,
    ):
        self.registry = registry
        self.runner = runner
        self.reproducer = reproducer
        self.data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._clock = clock or _default_clock

    def review(
        self,
        claim_id: str,
        test_plan: Optional[TestPlan] = None,
        instability_tolerance: float = DEFAULT_INSTABILITY_TOLERANCE,
    ) -> ReviewVerdict:
        if not self.reproducer.has_successful_reproduction(claim_id):
            raise ReviewPreconditionError(
                claim_id, "no successful reproduction is on file for this claim yet"
            )

        claim = self.registry.get(claim_id)
        if claim.state is ClaimState.RESULT:
            claim = self.registry.advance(
                claim_id, ClaimState.ADVERSARIAL_REVIEW, note="Adversarial review started"
            )
        elif claim.state is not ClaimState.ADVERSARIAL_REVIEW:
            raise ReviewPreconditionError(
                claim_id,
                f"claim must be at RESULT or ADVERSARIAL_REVIEW to be (re)reviewed, "
                f"found {claim.state.value}",
            )

        run_record = self.runner.get_run(claim_id)

        flags: List[ReviewFlag] = []
        all_checks_run: List[str] = []
        skipped: List[SkippedCheck] = []

        all_checks_run.append(CHECK_POST_HOC_THRESHOLD)
        threshold_flag = _check_post_hoc_threshold(claim)
        if threshold_flag is not None:
            flags.append(threshold_flag)

        if "seed" not in run_record.params:
            skipped.append(
                SkippedCheck(CHECK_NUMERICAL_INSTABILITY, "no seed parameter declared in the test plan")
            )
        elif test_plan is None:
            skipped.append(
                SkippedCheck(
                    CHECK_NUMERICAL_INSTABILITY,
                    "seed parameter declared but no test_plan was supplied to review() "
                    "for an off-the-record rerun",
                )
            )
        else:
            all_checks_run.append(CHECK_NUMERICAL_INSTABILITY)
            instability_flag = self._check_numerical_instability(
                claim, run_record.params, run_record.result, test_plan, instability_tolerance
            )
            if instability_flag is not None:
                flags.append(instability_flag)

        n_params = _lookup_field(run_record.params, run_record.result, "n_params")
        n_samples = _lookup_field(run_record.params, run_record.result, "n_samples")
        if n_params is None or n_samples is None:
            skipped.append(
                SkippedCheck(CHECK_OVERFITTING, "n_params and/or n_samples not declared in params/result")
            )
        else:
            all_checks_run.append(CHECK_OVERFITTING)
            if n_params >= n_samples:
                flags.append(
                    ReviewFlag(
                        CHECK_OVERFITTING,
                        "WARNING",
                        f"n_params ({n_params}) >= n_samples ({n_samples}): parameter "
                        f"count meets or exceeds sample count, a classic overfitting smell.",
                    )
                )

        calibration = _lookup_index_set(run_record.params, _CALIBRATION_KEYS)
        validation = _lookup_index_set(run_record.params, _VALIDATION_KEYS)
        if calibration is None or validation is None:
            skipped.append(
                SkippedCheck(
                    CHECK_LEAKAGE,
                    "calibration_indices and/or validation_indices not declared in params",
                )
            )
        else:
            all_checks_run.append(CHECK_LEAKAGE)
            overlap = set(calibration) & set(validation)
            if overlap:
                flags.append(
                    ReviewFlag(
                        CHECK_LEAKAGE,
                        "ERROR",
                        f"calibration and validation index sets overlap at "
                        f"{sorted(overlap)}: calibration data leaked into validation.",
                    )
                )

        recommendation = "FLAGGED" if flags else "CLEAN"
        verdict = ReviewVerdict(
            claim_id=claim_id,
            flags=flags,
            all_checks_run=all_checks_run,
            skipped_checks=skipped,
            recommendation=recommendation,
            reviewed_at=self._clock(),
        )
        self._append(verdict)
        return verdict

    def _check_numerical_instability(
        self,
        claim: Claim,
        original_params: Dict[str, Any],
        baseline_result: Optional[Dict[str, Any]],
        test_plan: TestPlan,
        default_tolerance: float,
    ) -> Optional[ReviewFlag]:
        tolerance = claim.metadata.get("instability_tolerance", default_tolerance)
        base_seed = original_params["seed"]

        results = [baseline_result or {}]
        seeds_tried = []
        for offset in _SEED_OFFSETS:
            variant_params = dict(original_params)
            variant_seed = base_seed + offset
            variant_params["seed"] = variant_seed
            seeds_tried.append(variant_seed)
            results.append(test_plan.fn(**variant_params))

        fields: Dict[str, List[float]] = {}
        for result in results:
            flattened: Dict[str, float] = {}
            _flatten_numeric(result, "", flattened)
            for key, value in flattened.items():
                fields.setdefault(key, []).append(value)

        offending = []
        for key, values in fields.items():
            if len(values) < 2:
                continue
            spread = max(values) - min(values)
            scale = max(abs(v) for v in values) or 1.0
            if (spread / scale) > tolerance:
                offending.append((key, spread))

        if offending:
            detail = ", ".join(f"{key} spread={spread:.6g}" for key, spread in offending)
            return ReviewFlag(
                CHECK_NUMERICAL_INSTABILITY,
                "ERROR",
                f"Results vary beyond instability tolerance {tolerance} across reruns "
                f"with seeds {seeds_tried} (baseline seed {base_seed}): {detail}",
            )
        return None

    def record_verdict(
        self,
        claim_id: str,
        verdict: Union[str, ClaimState],
        rationale: str,
    ) -> Claim:
        if not has_been_reviewed(claim_id, data_dir=self.data_dir):
            raise VerdictWithoutReviewError(claim_id)

        if not rationale or not rationale.strip():
            raise EmptyRationaleError(claim_id)

        try:
            target_state = coerce_state(verdict)
        except ValueError as exc:
            raise InvalidVerdictError(claim_id, verdict) from exc
        if target_state not in _TERMINAL_VERDICT_STATES:
            raise InvalidVerdictError(claim_id, verdict)

        return self.registry.advance(claim_id, target_state, note=rationale)

    def list_reviews(self, claim_id: str) -> List[ReviewVerdict]:
        return list_reviews(claim_id, data_dir=self.data_dir)

    def has_been_reviewed(self, claim_id: str) -> bool:
        return has_been_reviewed(claim_id, data_dir=self.data_dir)

    def _append(self, verdict: ReviewVerdict) -> None:
        path = _reviews_path(verdict.claim_id, self.data_dir)
        with path.open("a") as handle:
            handle.write(json.dumps(verdict.to_dict()) + "\n")
