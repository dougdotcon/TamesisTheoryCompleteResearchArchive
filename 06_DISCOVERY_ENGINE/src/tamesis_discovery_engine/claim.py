"""Claim state machine for the Tamesis Discovery Engine's Hypothesis Registry.

Mirrors the state chain fixed by ``ROADMAP.md`` (Stage 1, Module 1)::

    DRAFT -> PRE_REGISTERED -> LOCKED -> RUNNING -> RESULT -> ADVERSARIAL_REVIEW
                                                                      |
                                                                      v
                                        {CONFIRMED | REFUTED | INCONCLUSIVE | NULL}

This is the pre-registration discipline itself, not an arbitrary state
machine: a claim cannot skip straight from ``DRAFT`` to ``RESULT``, and once
it reaches one of the four terminal verdicts no further transition is legal.
"""

from __future__ import annotations

import dataclasses
import enum
from datetime import datetime
from typing import Any, Dict, FrozenSet, List


class ClaimState(enum.Enum):
    DRAFT = "DRAFT"
    PRE_REGISTERED = "PRE_REGISTERED"
    LOCKED = "LOCKED"
    RUNNING = "RUNNING"
    RESULT = "RESULT"
    ADVERSARIAL_REVIEW = "ADVERSARIAL_REVIEW"
    CONFIRMED = "CONFIRMED"
    REFUTED = "REFUTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    NULL = "NULL"


TERMINAL_STATES: FrozenSet[ClaimState] = frozenset(
    {
        ClaimState.CONFIRMED,
        ClaimState.REFUTED,
        ClaimState.INCONCLUSIVE,
        ClaimState.NULL,
    }
)

TRANSITIONS: Dict[ClaimState, FrozenSet[ClaimState]] = {
    ClaimState.DRAFT: frozenset({ClaimState.PRE_REGISTERED}),
    ClaimState.PRE_REGISTERED: frozenset({ClaimState.LOCKED}),
    ClaimState.LOCKED: frozenset({ClaimState.RUNNING}),
    ClaimState.RUNNING: frozenset({ClaimState.RESULT}),
    ClaimState.RESULT: frozenset({ClaimState.ADVERSARIAL_REVIEW}),
    ClaimState.ADVERSARIAL_REVIEW: frozenset(
        {
            ClaimState.CONFIRMED,
            ClaimState.REFUTED,
            ClaimState.INCONCLUSIVE,
            ClaimState.NULL,
        }
    ),
    ClaimState.CONFIRMED: frozenset(),
    ClaimState.REFUTED: frozenset(),
    ClaimState.INCONCLUSIVE: frozenset(),
    ClaimState.NULL: frozenset(),
}


class IllegalTransitionError(Exception):
    """Raised when a claim transition does not appear in ``TRANSITIONS``.

    Covers both forward-skipping (e.g. ``DRAFT -> RESULT``) and any attempt
    to leave a terminal state.
    """

    def __init__(self, from_state: ClaimState, to_state: ClaimState, claim_id: str | None = None):
        self.from_state = from_state
        self.to_state = to_state
        self.claim_id = claim_id
        subject = f"claim {claim_id}" if claim_id else "claim"
        reason = "state is terminal" if from_state in TERMINAL_STATES else "not a legal step"
        super().__init__(
            f"Illegal transition for {subject}: {from_state.value} -> {to_state.value} "
            f"({reason})"
        )


def is_legal_transition(from_state: ClaimState, to_state: ClaimState) -> bool:
    return to_state in TRANSITIONS.get(from_state, frozenset())


def coerce_state(value: "ClaimState | str") -> ClaimState:
    if isinstance(value, ClaimState):
        return value
    return ClaimState(value)


@dataclasses.dataclass(frozen=True)
class TransitionRecord:
    from_state: ClaimState
    to_state: ClaimState
    at: datetime
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_state": self.from_state.value,
            "to_state": self.to_state.value,
            "at": self.at.isoformat(),
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransitionRecord":
        return cls(
            from_state=ClaimState(data["from_state"]),
            to_state=ClaimState(data["to_state"]),
            at=datetime.fromisoformat(data["at"]),
            note=data.get("note", ""),
        )


@dataclasses.dataclass
class Claim:
    id: str
    title: str
    statement: str
    state: ClaimState
    created_at: datetime
    history: List[TransitionRecord] = dataclasses.field(default_factory=list)
    metadata: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "statement": self.statement,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "history": [record.to_dict() for record in self.history],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Claim":
        return cls(
            id=data["id"],
            title=data["title"],
            statement=data["statement"],
            state=ClaimState(data["state"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            history=[TransitionRecord.from_dict(record) for record in data.get("history", [])],
            metadata=data.get("metadata", {}),
        )
