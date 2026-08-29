"""Decision Ledger — Module 5 of the Tamesis Discovery Engine.

An append-only, hash-chained, dated record of every verdict, generalized
from the archive's own ``05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml``
beyond this one repository. Each :class:`LedgerEntry` gets a sequential id
(``ENGINE-DEC-NNN``, never reused) and carries ``prev_hash``: the content
hash of the entry before it, or a fixed genesis value (``"0" * 64``) for
the first entry ever appended. This turns the ledger into a hash chain —
tampering with any past entry's content, on disk, after the fact, changes
that entry's recomputed hash and breaks the link the *next* entry's
``prev_hash`` claims, which :meth:`Ledger.verify_chain` detects.

The link-checking loop alone cannot see tampering with the *last*
(tail) entry, since there is no following entry whose ``prev_hash``
would expose it. To close that gap, every :meth:`Ledger.append` also
writes the new tail entry's content hash, out-of-band, to a small
companion file next to the JSONL (``<ledger_path>.head``, containing
just the hex digest) — written atomically (temp file + ``os.replace``)
so it is never left half-written. :meth:`Ledger.verify_chain` checks
the reloaded tail entry's recomputed hash against this externally
committed value, so rewriting the tail entry's content on disk without
also rewriting the head file (which a tamperer, by definition, is not
supposed to be able to do out-of-band) is detected too.

Persistence choice: a single append-only JSONL file (``data/ledger.jsonl``),
one line per entry, written with ``open(..., "a")`` and never rewritten in
place — this is the shape Module 1's docstring calls out as the right one
for a record that must never be edited once written, in contrast to the
Hypothesis Registry's mutable one-file-per-claim documents.

``decision_type`` is a free-form string in the persisted record, but
:class:`DecisionType` documents and the public API accepts the ledger's
own controlled vocabulary (``REGISTER``, ``LOCK``, ``RUN``, ``REPRODUCE``,
``REVIEW``, ``VERDICT``) plus any other caller-chosen string — Modules 1-4
are wired to append here during the Integration phase, each using
whichever of these labels matches its own event.
"""

from __future__ import annotations

import dataclasses
import enum
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DEFAULT_LEDGER_PATH = DEFAULT_DATA_DIR / "ledger.jsonl"

_ID_PREFIX = "ENGINE-DEC"
GENESIS_HASH = "0" * 64


class DecisionType(enum.Enum):
    REGISTER = "REGISTER"
    LOCK = "LOCK"
    RUN = "RUN"
    REPRODUCE = "REPRODUCE"
    REVIEW = "REVIEW"
    VERDICT = "VERDICT"


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


class TamperDetectedError(Exception):
    """Raised by :meth:`Ledger.verify_chain` at the first broken link.

    Broken means either an entry's recomputed content hash no longer
    matches what the following entry's ``prev_hash`` claims, or (for the
    first entry) it does not equal :data:`GENESIS_HASH`, or (for the
    last, tail entry) its recomputed content hash no longer matches the
    externally-committed value in the ``.head`` companion file.
    """

    def __init__(self, index: int, entry_id: str, reason: str):
        self.index = index
        self.entry_id = entry_id
        self.reason = reason
        super().__init__(f"Ledger tamper detected at index {index} ({entry_id}): {reason}")


@dataclasses.dataclass(frozen=True)
class LedgerEntry:
    id: str
    timestamp: datetime
    claim_id: str
    decision_type: str
    summary: str
    prev_hash: str

    def content_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "claim_id": self.claim_id,
            "decision_type": self.decision_type,
            "summary": self.summary,
            "prev_hash": self.prev_hash,
        }

    def canonical_bytes(self) -> bytes:
        return json.dumps(self.content_dict(), sort_keys=True, separators=(",", ":")).encode("utf-8")

    def content_hash(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def to_json_line(self) -> str:
        return json.dumps(self.content_dict(), sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict) -> "LedgerEntry":
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            claim_id=data["claim_id"],
            decision_type=data["decision_type"],
            summary=data["summary"],
            prev_hash=data["prev_hash"],
        )


class Ledger:
    """Append-only, hash-chained decision ledger.

    ``ledger_path`` defaults to ``06_DISCOVERY_ENGINE/data/ledger.jsonl``
    (parent directory created if absent); pass an explicit path (e.g. under
    a pytest ``tmp_path``) to keep a ledger isolated. ``clock`` defaults to
    ``datetime.now(timezone.utc)`` but can be injected for deterministic
    tests. Existing entries are loaded from disk on construction, so a
    fresh ``Ledger`` instance pointed at the same path picks up exactly
    where a previous one left off.

    No method here mutates or removes a persisted entry: ``append`` only
    ever adds a new line to the file, and there is no ``delete`` or
    ``update`` on the public API.
    """

    def __init__(self, ledger_path: Optional[Path | str] = None, clock: Optional[Clock] = None):
        self.ledger_path = Path(ledger_path) if ledger_path is not None else DEFAULT_LEDGER_PATH
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        # Companion file: holds just the hex content_hash() of the most
        # recently appended entry, as an out-of-band commitment verify_chain
        # can check the reloaded tail entry against (see module docstring).
        self.head_path = Path(str(self.ledger_path) + ".head")
        self._clock = clock or _default_clock
        self._entries: List[LedgerEntry] = self._load()
        self._head_hash: Optional[str] = self._load_head()

    def append(self, claim_id: str, decision_type: "DecisionType | str", summary: str) -> LedgerEntry:
        type_value = decision_type.value if isinstance(decision_type, DecisionType) else str(decision_type)
        prev_hash = self._entries[-1].content_hash() if self._entries else GENESIS_HASH
        entry = LedgerEntry(
            id=self._next_id(),
            timestamp=self._clock(),
            claim_id=claim_id,
            decision_type=type_value,
            summary=summary,
            prev_hash=prev_hash,
        )
        with self.ledger_path.open("a") as handle:
            handle.write(entry.to_json_line() + "\n")
        self._write_head(entry.content_hash())
        self._entries.append(entry)
        return entry

    def history(self, claim_id: Optional[str] = None) -> List[LedgerEntry]:
        if claim_id is None:
            return list(self._entries)
        return [entry for entry in self._entries if entry.claim_id == claim_id]

    def verify_chain(self) -> bool:
        expected_prev = GENESIS_HASH
        for index, entry in enumerate(self._entries):
            if entry.prev_hash != expected_prev:
                raise TamperDetectedError(
                    index,
                    entry.id,
                    f"prev_hash is {entry.prev_hash!r}, expected {expected_prev!r} "
                    "(a preceding entry's content was altered after being written)",
                )
            expected_prev = entry.content_hash()

        # The loop above only ever catches tampering with entry i's content
        # via entry i+1's prev_hash — it has nothing to check the *last*
        # entry against, since there is no entry after it. Close that gap
        # by checking the reloaded tail entry against the hash committed,
        # out-of-band, into the .head companion file at append() time.
        if self._entries and self._head_hash is not None:
            tail_index = len(self._entries) - 1
            tail_entry = self._entries[tail_index]
            tail_hash = tail_entry.content_hash()
            if tail_hash != self._head_hash:
                raise TamperDetectedError(
                    tail_index,
                    tail_entry.id,
                    f"content_hash() is {tail_hash!r}, but the externally-committed head "
                    f"hash is {self._head_hash!r} (tail entry was rewritten after being written)",
                )
        return True

    def _next_id(self) -> str:
        return f"{_ID_PREFIX}-{len(self._entries) + 1:03d}"

    def _load(self) -> List[LedgerEntry]:
        if not self.ledger_path.exists():
            return []
        entries = []
        with self.ledger_path.open("r") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                entries.append(LedgerEntry.from_dict(json.loads(line)))
        return entries

    def _load_head(self) -> Optional[str]:
        if not self.head_path.exists():
            return None
        return self.head_path.read_text().strip() or None

    def _write_head(self, content_hash: str) -> None:
        """Atomically persist ``content_hash`` as the committed tail hash."""
        tmp_path = Path(str(self.head_path) + ".tmp")
        tmp_path.write_text(content_hash)
        os.replace(tmp_path, self.head_path)
        self._head_hash = content_hash
