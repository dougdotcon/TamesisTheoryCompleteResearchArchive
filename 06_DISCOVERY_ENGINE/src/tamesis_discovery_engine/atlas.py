"""Universality Atlas — Stage 2 module of the Tamesis Discovery Engine.

Source: ``ROADMAP.md`` Stage 2, item 10 — a registry of tested
invariants/scaling exponents across domains, so a new candidate can be
checked against everything already tried. The archive's own ``TRI-RG``
line (``05_DISCOVERY_LAB``) already keeps exactly this kind of catalogue
by hand: a markdown table of tested invariants and why each was
rejected, 16 candidates, all ``CLOSED_NULL``. This module makes that
pattern queryable instead of buried in a single markdown file.

The discipline this module exists to enforce: only *disposed* claims —
one of Module 1's four terminal states (``CONFIRMED``/``REFUTED``/
``INCONCLUSIVE``/``NULL``, see ``claim.py``) — may be catalogued as a
tested invariant. An open, still-running claim has no business being
listed next to closed results yet, since its outcome could still
change. :meth:`Atlas.register` therefore takes a ``source_claim_id``,
not a caller-supplied verdict, and reads the claim's own recorded state
back from Stage 1's :class:`~tamesis_discovery_engine.registry.Registry`
at registration time — the verdict can never drift from what the claim
itself actually recorded, because it is never accepted as a separate
argument in the first place.

``value`` convention: an invariant's tested value is either a ``float``
(a numeric scaling exponent, critical value, or similar) or a short
formula ``str`` (e.g. ``"pi**2 / 6"``, for an invariant whose tested
quantity is more naturally expressed symbolically than as one number).
:meth:`Atlas.find_near_duplicates` only ever compares the numeric form —
entries whose ``value`` is a formula string are skipped for that check
(documented here, not silently coerced or mismatched against a number).

Persistence choice: a single append-only JSONL file
(``data/atlas/entries.jsonl``), one line per entry, mirroring the
Decision Ledger's (Module 5) and Dataset Observatory's (Module 8) choice
for the same reason — an atlas entry, once registered against a
disposed claim, is a historical record of what was tested and is never
edited or removed after the fact, in contrast to Module 1's mutable
one-file-per-claim documents.
"""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime, timezone
from numbers import Real
from pathlib import Path
from typing import Callable, List, Optional, Union

from .claim import TERMINAL_STATES, ClaimState
from .registry import Registry

__all__ = [
    "AtlasEntry",
    "Atlas",
    "NonTerminalClaimError",
]

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "atlas"

_ENTRIES_FILENAME = "entries.jsonl"


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


def _is_numeric(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


class NonTerminalClaimError(Exception):
    """Raised by :meth:`Atlas.register` when the source claim has not yet
    reached one of Module 1's four terminal states — an open claim has no
    disposed outcome to catalogue as a tested invariant yet.
    """

    def __init__(self, claim_id: str, state: ClaimState):
        self.claim_id = claim_id
        self.state = state
        terminal = ", ".join(sorted(s.value for s in TERMINAL_STATES))
        super().__init__(
            f"Claim {claim_id!r} is in state {state.value}, not one of the terminal "
            f"states ({terminal}); only disposed claims may be catalogued in the Atlas."
        )


@dataclasses.dataclass(frozen=True)
class AtlasEntry:
    domain: str
    invariant_name: str
    value: Union[float, str]
    source_claim_id: str
    verdict: ClaimState
    registered_at: datetime

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "invariant_name": self.invariant_name,
            "value": self.value,
            "source_claim_id": self.source_claim_id,
            "verdict": self.verdict.value,
            "registered_at": self.registered_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AtlasEntry":
        return cls(
            domain=data["domain"],
            invariant_name=data["invariant_name"],
            value=data["value"],
            source_claim_id=data["source_claim_id"],
            verdict=ClaimState(data["verdict"]),
            registered_at=datetime.fromisoformat(data["registered_at"]),
        )


class Atlas:
    """Owns registration, search, and near-duplicate detection for
    :class:`AtlasEntry` records.

    ``registry`` is Stage 1's :class:`~tamesis_discovery_engine.registry.Registry`
    — the sole source of truth :meth:`register` reads a claim's terminal
    state and verdict from. ``data_dir`` defaults to
    ``06_DISCOVERY_ENGINE/data/atlas`` (created if absent); pass an
    explicit directory (e.g. a pytest ``tmp_path``) to keep an atlas
    isolated. ``clock`` defaults to ``datetime.now(timezone.utc)`` but can
    be injected for deterministic, non-flaky ``registered_at`` assertions.
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
        self.entries_path = self.data_dir / _ENTRIES_FILENAME
        self._clock = clock or _default_clock

    def register(
        self,
        domain: str,
        invariant_name: str,
        value: Union[float, str],
        source_claim_id: str,
    ) -> AtlasEntry:
        claim = self.registry.get(source_claim_id)
        if claim.state not in TERMINAL_STATES:
            raise NonTerminalClaimError(source_claim_id, claim.state)

        entry = AtlasEntry(
            domain=domain,
            invariant_name=invariant_name,
            value=value,
            source_claim_id=source_claim_id,
            verdict=claim.state,
            registered_at=self._clock(),
        )
        with self.entries_path.open("a") as handle:
            handle.write(json.dumps(entry.to_dict()) + "\n")
        return entry

    def search(
        self,
        domain: Optional[str] = None,
        invariant_name: Optional[str] = None,
    ) -> List[AtlasEntry]:
        return [
            entry
            for entry in self._load_entries()
            if (domain is None or entry.domain == domain)
            and (invariant_name is None or entry.invariant_name == invariant_name)
        ]

    def find_near_duplicates(
        self,
        domain: str,
        invariant_name: str,
        value: float,
        tolerance: float,
    ) -> List[AtlasEntry]:
        # invariant_name is deliberately not part of the filter below: two
        # differently-named invariants can turn out to be the same tested
        # quantity, which is exactly the duplicate this method must catch.
        if not _is_numeric(value):
            raise TypeError(f"find_near_duplicates requires a numeric value, got {value!r}")

        return [
            entry
            for entry in self._load_entries()
            if entry.domain == domain
            and _is_numeric(entry.value)
            and abs(entry.value - value) <= tolerance
        ]

    def _load_entries(self) -> List[AtlasEntry]:
        if not self.entries_path.exists():
            return []
        entries = []
        with self.entries_path.open("r") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    entries.append(AtlasEntry.from_dict(json.loads(line)))
        return entries
