"""Hypothesis Registry — Module 1 of the Tamesis Discovery Engine.

Structured claims with an id (``DISC-YYYY-NNNNN``), analogous to the
archive's own ``05_DISCOVERY_LAB/00_GOVERNANCE/CLAIM_LEDGER.yaml`` but
generalized: a ``Registry`` owns creation, state-machine-checked
transitions, lookup, and filtering for :class:`~tamesis_discovery_engine.claim.Claim`
objects (see ``claim.py`` for the state machine itself).

Persistence choice: one JSON file per claim under ``data/claims/``
(``DISC-YYYY-NNNNN.json``), rather than a single append-only JSONL ledger.
A claim's *state* is mutated in place many times over its lifetime while
its *history* only grows by appending transition records; a one-file-per-
claim document maps directly onto the ``get(id)`` access pattern (load one
small file, no replay of a shared log needed) and keeps each write cheap
and independent of every other claim. An append-only JSONL ledger is the
right shape for Module 5 (Decision Ledger), where a verdict must never be
edited after the fact once written — that is a different requirement from
this module's mutable-claim-record.

ID generation derives the next per-year sequence number by scanning
``data/claims/`` for existing ``DISC-{year}-*.json`` files and taking the
highest sequence found, plus one (or 1 if none exist for that year yet).
Uniqueness is therefore a property of what is actually persisted on disk,
not of an in-memory counter that would reset — and collide — across
process restarts.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

from .claim import (
    Claim,
    ClaimState,
    IllegalTransitionError,
    TransitionRecord,
    coerce_state,
    is_legal_transition,
)

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "claims"

_ID_PREFIX = "DISC"


class ClaimNotFoundError(KeyError):
    def __init__(self, claim_id: str):
        self.claim_id = claim_id
        super().__init__(f"No claim registered with id {claim_id!r}")


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


class Registry:
    """Owns creation, transitions, lookup and filtering of Claims.

    ``data_dir`` defaults to ``06_DISCOVERY_ENGINE/data/claims`` (created if
    absent); pass an explicit directory (e.g. a pytest ``tmp_path``) to keep
    a registry isolated. ``clock`` defaults to ``datetime.now(timezone.utc)``
    but can be injected for deterministic, non-flaky timestamp assertions.
    """

    def __init__(self, data_dir: Optional[Path | str] = None, clock: Optional[Clock] = None):
        self.data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._clock = clock or _default_clock

    def create(self, title: str, statement: str, metadata: Optional[Dict] = None) -> Claim:
        now = self._clock()
        claim = Claim(
            id=self._generate_id(now),
            title=title,
            statement=statement,
            state=ClaimState.DRAFT,
            created_at=now,
            history=[],
            metadata=dict(metadata) if metadata else {},
        )
        self._save(claim)
        return claim

    def advance(self, claim_id: str, to_state: "ClaimState | str", note: str = "") -> Claim:
        claim = self.get(claim_id)
        from_state = claim.state
        target = coerce_state(to_state)
        if not is_legal_transition(from_state, target):
            raise IllegalTransitionError(from_state, target, claim_id)
        record = TransitionRecord(
            from_state=from_state,
            to_state=target,
            at=self._clock(),
            note=note,
        )
        claim.history.append(record)
        claim.state = target
        self._save(claim)
        return claim

    def get(self, claim_id: str) -> Claim:
        path = self._claim_path(claim_id)
        if not path.exists():
            raise ClaimNotFoundError(claim_id)
        return Claim.from_dict(json.loads(path.read_text()))

    def list(
        self,
        state: Optional["ClaimState | str"] = None,
        tag: Optional[str] = None,
    ) -> List[Claim]:
        target_state = coerce_state(state) if state is not None else None
        claims = []
        for path in sorted(self.data_dir.glob(f"{_ID_PREFIX}-*.json")):
            claim = Claim.from_dict(json.loads(path.read_text()))
            if target_state is not None and claim.state != target_state:
                continue
            if tag is not None and tag not in claim.metadata.get("tags", []):
                continue
            claims.append(claim)
        return claims

    def _claim_path(self, claim_id: str) -> Path:
        return self.data_dir / f"{claim_id}.json"

    def _generate_id(self, at: datetime) -> str:
        year = at.year
        return f"{_ID_PREFIX}-{year}-{self._next_sequence(year):05d}"

    def _next_sequence(self, year: int) -> int:
        prefix = f"{_ID_PREFIX}-{year}-"
        max_seq = 0
        for path in self.data_dir.glob(f"{prefix}*.json"):
            suffix = path.stem[len(prefix):]
            if suffix.isdigit():
                max_seq = max(max_seq, int(suffix))
        return max_seq + 1

    def _save(self, claim: Claim) -> None:
        self._claim_path(claim.id).write_text(json.dumps(claim.to_dict(), indent=2))
