"""Reproduction Engine — Module 3 of the Tamesis Discovery Engine.

Re-runs a claim's experiment from a second, independent implementation and
diffs its output against the original :class:`~tamesis_discovery_engine.runner.RunRecord`
(``ROADMAP.md`` Stage 1, item 3), building on Module 1's
:class:`~tamesis_discovery_engine.registry.Registry` and Module 2's
:class:`~tamesis_discovery_engine.runner.Runner` rather than redefining either.

Independence, not identity
---------------------------
A :class:`ReproductionPlan` is deliberately *not* Module 2's ``TestPlan``: it
carries only a callable plus identity metadata (``name``/``version``), with
no ``params`` field of its own. :meth:`Reproducer.reproduce` always invokes
the second implementation with the *original run's declared params* — the
whole point of a reproduction is to hold the inputs fixed and let a
different implementation answer the same question, so a caller cannot
silently reproduce a different experiment by supplying different params on
the second plan. There is also no source-hash tamper check here (unlike
Module 2's locking): a reproduction is explicitly allowed, even expected, to
be "a differently-implemented callable" — that is the second, independent
implementation this module exists to run.

Numeric comparison
-------------------
Results are compared recursively over matching dict keys and list indices
(:func:`_diff_values`); a numeric leaf counts as an exact match only on
Python equality, otherwise as within-tolerance if its absolute difference is
at most ``tolerance`` *or* (once that fails) its relative difference against
the larger-magnitude operand is; every other numeric or non-numeric leaf
that fails to match exactly is a mismatch. Only non-exact leaves are kept in
a record's ``deltas`` list, since :meth:`Reproducer.reproduce` reports *what
differed*, not a receipt for every field that already agreed. The record's
overall verdict is the worst of its per-field deltas: no deltas at all is
``EXACT_MATCH``, any mismatch anywhere is ``MISMATCH``, otherwise
(everything differs but only within tolerance) it is
``MATCH_WITHIN_TOLERANCE``.

Persistence and the Module 4/5 guard
--------------------------------------
Unlike a run, a claim can be (and, per the Adversarial Reviewer's own
methodology checks, sometimes should be) reproduced more than once — so
records are appended, not overwritten, one JSON line per attempt under
``data/reproductions/{claim_id}.jsonl``, mirroring the Decision Ledger's
append-only shape rather than the Hypothesis Registry's mutable one.
``has_successful_reproduction`` is exposed as a **module-level** function
(not just a ``Reproducer`` method) because Module 4 checks it as
``reproduction.has_successful_reproduction(claim_id)`` without necessarily
holding a live ``Reproducer`` bound to a ``Registry``/``Runner`` pair — it
only needs to read what is already on disk.
"""

from __future__ import annotations

import dataclasses
import enum
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .claim import ClaimState
from .registry import Registry
from .runner import Runner

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "reproductions"

_REPRODUCIBLE_STATES = frozenset(
    {
        ClaimState.RESULT,
        ClaimState.ADVERSARIAL_REVIEW,
        ClaimState.CONFIRMED,
        ClaimState.REFUTED,
        ClaimState.INCONCLUSIVE,
        ClaimState.NULL,
    }
)


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


class ClaimNotReproducibleError(Exception):
    """Raised when a claim has no successful original result to reproduce.

    A claim must have reached ``RESULT`` (or moved on from it) via Module
    2's ``Runner.run`` before there is a ``RunRecord`` worth diffing against
    — a claim still in ``DRAFT``/``PRE_REGISTERED``/``LOCKED``/``RUNNING``,
    or one whose only run on file failed, is not reproducible yet.
    """

    def __init__(self, claim_id: str, actual_state: ClaimState):
        self.claim_id = claim_id
        self.actual_state = actual_state
        super().__init__(
            f"Cannot reproduce claim {claim_id!r}: expected a successful run "
            f"at state RESULT or later, found {actual_state.value}"
        )


class ReproductionVerdict(enum.Enum):
    EXACT_MATCH = "EXACT_MATCH"
    MATCH_WITHIN_TOLERANCE = "MATCH_WITHIN_TOLERANCE"
    MISMATCH = "MISMATCH"


_SUCCESSFUL_VERDICTS = frozenset(
    {ReproductionVerdict.EXACT_MATCH.value, ReproductionVerdict.MATCH_WITHIN_TOLERANCE.value}
)


@dataclasses.dataclass
class ReproductionPlan:
    """A second, independently-authored implementation to check a claim against.

    ``fn`` must accept exactly the keyword arguments the original claim's
    ``RunRecord.params`` declared and return a JSON-serializable ``dict`` —
    the same contract Module 2's ``TestPlan.fn`` has, minus the params
    (those come from the original run, not from here; see module docstring).
    """

    name: str
    version: str
    fn: Callable[..., Dict[str, Any]]

    @property
    def qualified_name(self) -> str:
        return f"{self.name}@{self.version}"


@dataclasses.dataclass
class FieldDelta:
    field: str
    original: Any
    reproduced: Any
    delta: Optional[float]
    verdict: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "original": self.original,
            "reproduced": self.reproduced,
            "delta": self.delta,
            "verdict": self.verdict,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FieldDelta":
        return cls(
            field=data["field"],
            original=data["original"],
            reproduced=data["reproduced"],
            delta=data.get("delta"),
            verdict=data["verdict"],
        )


@dataclasses.dataclass
class ReproductionRecord:
    claim_id: str
    original_test_plan: str
    reproduction_test_plan: str
    params: Dict[str, Any]
    tolerance: float
    verdict: str
    deltas: List[FieldDelta]
    original_result: Optional[Dict[str, Any]]
    reproduced_result: Optional[Dict[str, Any]]
    started_at: datetime
    ended_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "original_test_plan": self.original_test_plan,
            "reproduction_test_plan": self.reproduction_test_plan,
            "params": self.params,
            "tolerance": self.tolerance,
            "verdict": self.verdict,
            "deltas": [delta.to_dict() for delta in self.deltas],
            "original_result": self.original_result,
            "reproduced_result": self.reproduced_result,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReproductionRecord":
        return cls(
            claim_id=data["claim_id"],
            original_test_plan=data["original_test_plan"],
            reproduction_test_plan=data["reproduction_test_plan"],
            params=data.get("params", {}),
            tolerance=data["tolerance"],
            verdict=data["verdict"],
            deltas=[FieldDelta.from_dict(item) for item in data.get("deltas", [])],
            original_result=data.get("original_result"),
            reproduced_result=data.get("reproduced_result"),
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]),
        )


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _within_tolerance(a: float, b: float, tolerance: float) -> bool:
    diff = abs(a - b)
    if diff <= tolerance:
        return True
    denom = max(abs(a), abs(b))
    if denom == 0:
        return False
    return (diff / denom) <= tolerance


def _diff_values(original: Any, reproduced: Any, tolerance: float, path: str, out: List[FieldDelta]) -> None:
    if isinstance(original, dict) and isinstance(reproduced, dict):
        for key in sorted(set(original) | set(reproduced), key=str):
            sub_path = f"{path}.{key}" if path else str(key)
            if key not in original or key not in reproduced:
                out.append(
                    FieldDelta(
                        sub_path,
                        original.get(key),
                        reproduced.get(key),
                        None,
                        ReproductionVerdict.MISMATCH.value,
                    )
                )
                continue
            _diff_values(original[key], reproduced[key], tolerance, sub_path, out)
        return

    if isinstance(original, list) and isinstance(reproduced, list):
        if len(original) != len(reproduced):
            out.append(FieldDelta(path, original, reproduced, None, ReproductionVerdict.MISMATCH.value))
            return
        for index, (original_item, reproduced_item) in enumerate(zip(original, reproduced)):
            _diff_values(original_item, reproduced_item, tolerance, f"{path}[{index}]", out)
        return

    if _is_number(original) and _is_number(reproduced):
        if original == reproduced:
            return
        delta = abs(original - reproduced)
        verdict = (
            ReproductionVerdict.MATCH_WITHIN_TOLERANCE
            if _within_tolerance(original, reproduced, tolerance)
            else ReproductionVerdict.MISMATCH
        )
        out.append(FieldDelta(path, original, reproduced, delta, verdict.value))
        return

    if original != reproduced:
        out.append(FieldDelta(path, original, reproduced, None, ReproductionVerdict.MISMATCH.value))


def _aggregate_verdict(deltas: List[FieldDelta]) -> ReproductionVerdict:
    if not deltas:
        return ReproductionVerdict.EXACT_MATCH
    if any(delta.verdict == ReproductionVerdict.MISMATCH.value for delta in deltas):
        return ReproductionVerdict.MISMATCH
    return ReproductionVerdict.MATCH_WITHIN_TOLERANCE


def _reproductions_path(claim_id: str, data_dir: Path) -> Path:
    return data_dir / f"{claim_id}.jsonl"


def list_reproductions(claim_id: str, data_dir: Optional[Path | str] = None) -> List[ReproductionRecord]:
    directory = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    path = _reproductions_path(claim_id, directory)
    if not path.exists():
        return []
    records = []
    with path.open("r") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(ReproductionRecord.from_dict(json.loads(line)))
    return records


def has_successful_reproduction(claim_id: str, data_dir: Optional[Path | str] = None) -> bool:
    return any(
        record.verdict in _SUCCESSFUL_VERDICTS for record in list_reproductions(claim_id, data_dir=data_dir)
    )


class Reproducer:
    """Runs a second, independent implementation against a claim's original result.

    ``registry`` and ``runner`` are the Module 1/2 objects this class reads
    claim state and the original ``RunRecord`` through — it never mutates a
    ``Claim`` or writes a new ``RunRecord`` itself. ``data_dir`` defaults to
    ``06_DISCOVERY_ENGINE/data/reproductions`` (created if absent); pass an
    explicit directory (e.g. a pytest ``tmp_path``) to keep reproductions
    isolated. ``clock`` defaults to ``datetime.now(timezone.utc)`` but can be
    injected for deterministic timestamp assertions.
    """

    def __init__(
        self,
        registry: Registry,
        runner: Runner,
        data_dir: Optional[Path | str] = None,
        clock: Optional[Clock] = None,
    ):
        self.registry = registry
        self.runner = runner
        self.data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._clock = clock or _default_clock

    def reproduce(
        self,
        claim_id: str,
        second_test_plan: ReproductionPlan,
        tolerance: float = 1e-9,
    ) -> ReproductionRecord:
        claim = self.registry.get(claim_id)
        if claim.state not in _REPRODUCIBLE_STATES:
            raise ClaimNotReproducibleError(claim_id, claim.state)

        original = self.runner.get_run(claim_id)
        if not original.success:
            raise ClaimNotReproducibleError(claim_id, claim.state)

        original_result = original.result if original.result is not None else {}

        started_at = self._clock()
        reproduced_result = second_test_plan.fn(**original.params)
        ended_at = self._clock()

        deltas: List[FieldDelta] = []
        _diff_values(original_result, reproduced_result, tolerance, "", deltas)
        verdict = _aggregate_verdict(deltas)

        record = ReproductionRecord(
            claim_id=claim_id,
            original_test_plan=f"{original.test_plan_name}@{original.test_plan_version}",
            reproduction_test_plan=second_test_plan.qualified_name,
            params=dict(original.params),
            tolerance=tolerance,
            verdict=verdict.value,
            deltas=deltas,
            original_result=original.result,
            reproduced_result=reproduced_result,
            started_at=started_at,
            ended_at=ended_at,
        )
        self._append(record)
        return record

    def list_reproductions(self, claim_id: str) -> List[ReproductionRecord]:
        return list_reproductions(claim_id, data_dir=self.data_dir)

    def has_successful_reproduction(self, claim_id: str) -> bool:
        return has_successful_reproduction(claim_id, data_dir=self.data_dir)

    def _append(self, record: ReproductionRecord) -> None:
        path = _reproductions_path(record.claim_id, self.data_dir)
        with path.open("a") as handle:
            handle.write(json.dumps(record.to_dict()) + "\n")
