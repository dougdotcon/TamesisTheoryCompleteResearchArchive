"""Experiment Runner — Module 2 of the Tamesis Discovery Engine.

Executes a pre-registered, locked test plan against declared data/code
(``ROADMAP.md`` Stage 1, item 2), building on the :class:`~tamesis_discovery_engine.registry.Registry`
and :mod:`~tamesis_discovery_engine.claim` state machine from Module 1 rather
than redefining either.

Tamper-evidence design
-----------------------
A :class:`TestPlan` bundles a callable, its declared ``params``, and identity
metadata (``name``/``version``). Locking a claim to a test plan is a distinct
act from bare state-machine advancement: :meth:`Runner.lock` hashes the
callable's *current* source (``hashlib.sha256`` of ``inspect.getsource(fn)``)
at the moment the claim transitions ``PRE_REGISTERED -> LOCKED`` (delegating
the transition itself to ``Registry.advance`` — this module never mutates
``TRANSITIONS`` or a ``Claim``'s state directly), and persists that hash in a
:class:`LockRecord` keyed by claim id.

``Registry`` exposes no API for attaching arbitrary data to a stored claim
outside of ``create()``, and reaching into its private ``_save`` to smuggle a
hash into ``claim.metadata`` would be exactly the kind of state-machine
side-channel this module is told not to build. So the lock record lives in
its own small JSON store next to the run records, associated with the claim
by id — the same "retrievable by claim id" shape ``RunRecord`` uses.

:meth:`Runner.run` recomputes the hash of the test plan's *current* source
right before executing it and compares against the ``LockRecord``. Because
``TestPlan.fn`` is a plain mutable attribute, tampering (reassigning ``fn``
to a differently-implemented callable after locking, even while keeping the
same ``name``/``version``) changes the recomputed hash and is caught as
``TestPlanTamperedError`` — the run is refused before the callable is ever
invoked.

Failure handling: if the callable raises, the exception is never swallowed.
A failed ``RunRecord`` is persisted first (capturing the exception's type and
message alongside the params and timing that were actually used), and then
the original exception is re-raised. The claim is left in ``RUNNING`` rather
than being forced into ``RESULT`` — ``RUNNING`` is not a legal predecessor of
``RESULT`` for a run that never produced one, and the existing state machine
has no separate "failed" state to fake; ``RUNNING`` (which no successful run
ever leaves stale) together with the persisted failed ``RunRecord`` is what
makes the failure durably visible rather than silent.
"""

from __future__ import annotations

import dataclasses
import hashlib
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from .claim import ClaimState
from .registry import Registry

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "runs"


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


def _hash_source(fn: Callable[..., Any]) -> str:
    return hashlib.sha256(inspect.getsource(fn).encode("utf-8")).hexdigest()


class ClaimNotLockedError(Exception):
    """Raised by ``Runner.run`` when the claim is not in ``LOCKED`` state.

    A runner must never execute against a ``DRAFT`` or ``PRE_REGISTERED``
    claim (or any other non-``LOCKED`` state) — that is the whole point of
    requiring a lock before a run.
    """

    def __init__(self, claim_id: str, actual_state: ClaimState):
        self.claim_id = claim_id
        self.actual_state = actual_state
        super().__init__(
            f"Cannot run claim {claim_id!r}: expected state LOCKED, found "
            f"{actual_state.value}"
        )


class MissingLockRecordError(Exception):
    """Raised when a claim reports ``LOCKED`` but has no ``LockRecord``.

    This only happens if a claim was moved to ``LOCKED`` some way other than
    ``Runner.lock`` (e.g. calling ``Registry.advance`` directly), so there is
    no hash to check the test plan against.
    """

    def __init__(self, claim_id: str):
        self.claim_id = claim_id
        super().__init__(
            f"Claim {claim_id!r} is LOCKED but was never locked via "
            f"Runner.lock(); no source hash is on record to verify against"
        )


class TestPlanTamperedError(Exception):
    """Raised when a test plan's source hash no longer matches lock time.

    This is the "no post-hoc rewriting after locking" check: the callable's
    source changed between ``Runner.lock`` and ``Runner.run``.
    """

    __test__ = False  # not a pytest test class; name is fixed by the checklist

    def __init__(self, claim_id: str, expected_hash: str, actual_hash: str):
        self.claim_id = claim_id
        self.expected_hash = expected_hash
        self.actual_hash = actual_hash
        super().__init__(
            f"Test plan for claim {claim_id!r} was tampered with after "
            f"locking: expected source hash {expected_hash!r}, got "
            f"{actual_hash!r}"
        )


@dataclasses.dataclass
class TestPlan:
    """A pre-registrable test plan: a callable plus its declared inputs.

    ``fn`` must accept exactly the keyword arguments in ``params`` and
    return a JSON-serializable ``dict``. ``name``/``version`` identify the
    plan for humans and for the persisted records; they are not part of the
    tamper-evidence hash (only ``fn``'s source is), since ``run()`` refuses
    to execute anything but the exact source that was locked in regardless
    of what it is labeled.
    """

    __test__ = False  # not a pytest test class; name is fixed by the checklist

    name: str
    version: str
    fn: Callable[..., Dict[str, Any]]
    params: Dict[str, Any] = dataclasses.field(default_factory=dict)

    @property
    def qualified_name(self) -> str:
        return f"{self.name}@{self.version}"

    def source_hash(self) -> str:
        return _hash_source(self.fn)


@dataclasses.dataclass
class LockRecord:
    claim_id: str
    test_plan_name: str
    test_plan_version: str
    source_hash: str
    params: Dict[str, Any]
    locked_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "test_plan_name": self.test_plan_name,
            "test_plan_version": self.test_plan_version,
            "source_hash": self.source_hash,
            "params": self.params,
            "locked_at": self.locked_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LockRecord":
        return cls(
            claim_id=data["claim_id"],
            test_plan_name=data["test_plan_name"],
            test_plan_version=data["test_plan_version"],
            source_hash=data["source_hash"],
            params=data.get("params", {}),
            locked_at=datetime.fromisoformat(data["locked_at"]),
        )


@dataclasses.dataclass
class RunRecord:
    claim_id: str
    test_plan_name: str
    test_plan_version: str
    params: Dict[str, Any]
    source_hash: str
    started_at: datetime
    ended_at: datetime
    success: bool
    result: Optional[Dict[str, Any]] = None
    exception_type: Optional[str] = None
    exception_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "test_plan_name": self.test_plan_name,
            "test_plan_version": self.test_plan_version,
            "params": self.params,
            "source_hash": self.source_hash,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
            "success": self.success,
            "result": self.result,
            "exception_type": self.exception_type,
            "exception_message": self.exception_message,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RunRecord":
        return cls(
            claim_id=data["claim_id"],
            test_plan_name=data["test_plan_name"],
            test_plan_version=data["test_plan_version"],
            params=data.get("params", {}),
            source_hash=data["source_hash"],
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]),
            success=data["success"],
            result=data.get("result"),
            exception_type=data.get("exception_type"),
            exception_message=data.get("exception_message"),
        )


class Runner:
    """Locks test plans to claims and executes them.

    ``registry`` is the Module 1 ``Registry`` this runner drives claim state
    transitions through — this class never mutates a ``Claim`` or the
    ``TRANSITIONS`` table itself. ``data_dir`` defaults to
    ``06_DISCOVERY_ENGINE/data/runs`` (created if absent); pass an explicit
    directory (e.g. a pytest ``tmp_path``) to keep runs isolated. ``clock``
    defaults to ``datetime.now(timezone.utc)`` but can be injected for
    deterministic timestamp assertions.
    """

    def __init__(
        self,
        registry: Registry,
        data_dir: Optional[Path | str] = None,
        clock: Optional[Clock] = None,
    ):
        self.registry = registry
        self.data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._clock = clock or _default_clock

    def lock(self, claim_id: str, test_plan: TestPlan):
        source_hash = test_plan.source_hash()
        claim = self.registry.advance(
            claim_id,
            ClaimState.LOCKED,
            note=f"Locked test plan {test_plan.qualified_name}",
        )
        lock_record = LockRecord(
            claim_id=claim_id,
            test_plan_name=test_plan.name,
            test_plan_version=test_plan.version,
            source_hash=source_hash,
            params=dict(test_plan.params),
            locked_at=self._clock(),
        )
        self._save_lock(lock_record)
        return claim

    def run(self, claim_id: str, test_plan: TestPlan) -> RunRecord:
        claim = self.registry.get(claim_id)
        if claim.state is not ClaimState.LOCKED:
            raise ClaimNotLockedError(claim_id, claim.state)

        lock_record = self._load_lock(claim_id)
        current_hash = test_plan.source_hash()
        if current_hash != lock_record.source_hash:
            raise TestPlanTamperedError(claim_id, lock_record.source_hash, current_hash)

        self.registry.advance(
            claim_id,
            ClaimState.RUNNING,
            note=f"Executing {test_plan.qualified_name}",
        )

        started_at = self._clock()
        try:
            result = test_plan.fn(**test_plan.params)
        except Exception as exc:
            ended_at = self._clock()
            failed_record = RunRecord(
                claim_id=claim_id,
                test_plan_name=test_plan.name,
                test_plan_version=test_plan.version,
                params=dict(test_plan.params),
                source_hash=current_hash,
                started_at=started_at,
                ended_at=ended_at,
                success=False,
                result=None,
                exception_type=type(exc).__name__,
                exception_message=str(exc),
            )
            self._save_run(failed_record)
            raise

        ended_at = self._clock()
        record = RunRecord(
            claim_id=claim_id,
            test_plan_name=test_plan.name,
            test_plan_version=test_plan.version,
            params=dict(test_plan.params),
            source_hash=current_hash,
            started_at=started_at,
            ended_at=ended_at,
            success=True,
            result=result,
        )
        self._save_run(record)
        self.registry.advance(claim_id, ClaimState.RESULT, note="Run completed")
        return record

    def get_run(self, claim_id: str) -> RunRecord:
        path = self._run_path(claim_id)
        if not path.exists():
            raise KeyError(f"No run record for claim {claim_id!r}")
        return RunRecord.from_dict(json.loads(path.read_text()))

    def _run_path(self, claim_id: str) -> Path:
        return self.data_dir / f"{claim_id}.json"

    def _lock_path(self, claim_id: str) -> Path:
        return self.data_dir / f"{claim_id}.lock.json"

    def _save_run(self, record: RunRecord) -> None:
        self._run_path(record.claim_id).write_text(json.dumps(record.to_dict(), indent=2))

    def _save_lock(self, record: LockRecord) -> None:
        self._lock_path(record.claim_id).write_text(json.dumps(record.to_dict(), indent=2))

    def _load_lock(self, claim_id: str) -> LockRecord:
        path = self._lock_path(claim_id)
        if not path.exists():
            raise MissingLockRecordError(claim_id)
        return LockRecord.from_dict(json.loads(path.read_text()))
