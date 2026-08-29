"""Dataset Observatory — Stage 2 module of the Tamesis Discovery Engine.

Provenance-tracking machinery for external reference data
(``ROADMAP.md`` Stage 2, item 8): the archive already tracks PDG,
CODATA, Planck, SPARC, Gaia and Odlyzko data by hand, in prose, spread
across many claims' writeups. This module makes that lineage queryable
instead — ingest a dataset once under a ``(name, version)`` key, get back
a checksummed :class:`Dataset` record, verify the persisted bytes have
not been silently altered, and query which claims declared they used
which dataset version in either direction.

**Scope note — no real data sources are wired up here.** This module
does NOT fetch PDG, CODATA, Planck, SPARC, Gaia, Odlyzko or any other
data over the network; :meth:`DatasetRegistry.ingest` takes caller-supplied
``bytes`` and is tested exclusively against small synthetic byte content
standing in for a "dataset". Nothing in this file opens a network
connection of any kind. Wiring real fetches for the archive's actual
reference sources is future work, deliberately out of scope for Stage 2.

Persistence choice: one directory per ``(name, version)`` under
``data/datasets/{name}/{version}/``, holding the raw ingested bytes
(``content.bin``) alongside a ``metadata.json`` sidecar (the persisted
form of :class:`Dataset`) — mirroring Module 1's one-file/dir-per-record
layout, since a dataset version is written once and read many times, not
appended to like Module 5's ledger. A version is immutable once
ingested: re-ingesting the same ``(name, version)`` with content whose
sha256 differs from what is already on disk raises
:class:`DatasetConflictError` rather than silently overwriting it, since
any claim that already cited that version as provenance would otherwise
have its cited data change out from under it after the fact. Re-ingesting
with byte-identical content is treated as a no-op and simply hands back
the existing record.

:meth:`DatasetRegistry.verify_integrity` recomputes the sha256 of the
persisted ``content.bin`` and compares it to the checksum recorded in
``metadata.json`` at ingest time — the same tamper-evidence spirit as
Module 5's :meth:`~tamesis_discovery_engine.ledger.Ledger.verify_chain`,
scoped to one dataset version rather than a hash chain, since dataset
content (unlike a ledger entry) has no "previous entry" to link against.

Usage records (``claim X declares it used dataset Y@version``) are
appended, one JSON object per line, to ``data/datasets/usage.jsonl`` —
the same append-only-log shape Module 5 uses for the same reason: a
provenance declaration, once made, is not something a later call should
silently edit or remove.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional

__all__ = [
    "Dataset",
    "DatasetRegistry",
    "DatasetNotFoundError",
    "DatasetConflictError",
]

Clock = Callable[[], datetime]

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "datasets"

_CONTENT_FILENAME = "content.bin"
_METADATA_FILENAME = "metadata.json"
_USAGE_FILENAME = "usage.jsonl"


def _default_clock() -> datetime:
    return datetime.now(timezone.utc)


class DatasetNotFoundError(KeyError):
    def __init__(self, name: str, version: Optional[str] = None):
        self.name = name
        self.version = version
        if version is None:
            message = f"No dataset has ever been ingested under name {name!r}"
        else:
            message = f"No dataset ingested for name {name!r}, version {version!r}"
        super().__init__(message)


class DatasetConflictError(Exception):
    """Raised by :meth:`DatasetRegistry.ingest` when re-ingesting an
    already-ingested ``(name, version)`` with content whose checksum
    differs from what was recorded the first time — a dataset version is
    immutable once ingested, so this is refused rather than silently
    overwriting data that some claim may already cite as provenance.
    """

    def __init__(self, name: str, version: str, existing_checksum: str, new_checksum: str):
        self.name = name
        self.version = version
        self.existing_checksum = existing_checksum
        self.new_checksum = new_checksum
        super().__init__(
            f"Dataset {name!r} version {version!r} was already ingested with checksum "
            f"{existing_checksum!r}; refusing to re-ingest it with different content "
            f"(checksum {new_checksum!r}) — a version is immutable once ingested."
        )


@dataclasses.dataclass(frozen=True)
class Dataset:
    name: str
    version: str
    source_citation: str
    checksum: str
    ingested_at: datetime
    size_bytes: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "source_citation": self.source_citation,
            "checksum": self.checksum,
            "ingested_at": self.ingested_at.isoformat(),
            "size_bytes": self.size_bytes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Dataset":
        return cls(
            name=data["name"],
            version=data["version"],
            source_citation=data["source_citation"],
            checksum=data["checksum"],
            ingested_at=datetime.fromisoformat(data["ingested_at"]),
            size_bytes=data["size_bytes"],
        )


class DatasetRegistry:
    """Owns ingestion, integrity verification, lookup, and claim-usage
    provenance queries for :class:`Dataset` records.

    ``data_dir`` defaults to ``06_DISCOVERY_ENGINE/data/datasets``
    (created if absent); pass an explicit directory (e.g. a pytest
    ``tmp_path``) to keep a registry isolated. ``clock`` defaults to
    ``datetime.now(timezone.utc)`` but can be injected for deterministic,
    non-flaky ``ingested_at`` assertions.
    """

    def __init__(self, data_dir: Optional[Path | str] = None, clock: Optional[Clock] = None):
        self.data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.usage_path = self.data_dir / _USAGE_FILENAME
        self._clock = clock or _default_clock

    def ingest(self, name: str, version: str, source_citation: str, content: bytes) -> Dataset:
        checksum = hashlib.sha256(content).hexdigest()
        metadata_path = self._metadata_path(name, version)

        if metadata_path.exists():
            existing = Dataset.from_dict(json.loads(metadata_path.read_text()))
            if existing.checksum != checksum:
                raise DatasetConflictError(name, version, existing.checksum, checksum)
            return existing

        version_dir = self._version_dir(name, version)
        version_dir.mkdir(parents=True, exist_ok=True)
        self._content_path(name, version).write_bytes(content)

        dataset = Dataset(
            name=name,
            version=version,
            source_citation=source_citation,
            checksum=checksum,
            ingested_at=self._clock(),
            size_bytes=len(content),
        )
        metadata_path.write_text(json.dumps(dataset.to_dict(), indent=2))
        return dataset

    def get(self, name: str, version: Optional[str] = None) -> Dataset:
        if version is not None:
            return self._load_metadata(name, version)

        versions = self._list_versions(name)
        if not versions:
            raise DatasetNotFoundError(name)
        candidates = [self._load_metadata(name, v) for v in versions]
        return max(candidates, key=lambda dataset: dataset.ingested_at)

    def verify_integrity(self, name: str, version: str) -> bool:
        dataset = self._load_metadata(name, version)
        content_path = self._content_path(name, version)
        if not content_path.exists():
            return False
        actual_checksum = hashlib.sha256(content_path.read_bytes()).hexdigest()
        return actual_checksum == dataset.checksum

    def record_usage(self, claim_id: str, name: str, version: str) -> None:
        self._load_metadata(name, version)
        record = {"claim_id": claim_id, "name": name, "version": version}
        with self.usage_path.open("a") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def used_by(self, name: str, version: str) -> List[str]:
        return [
            record["claim_id"]
            for record in self._load_usage()
            if record["name"] == name and record["version"] == version
        ]

    def datasets_used_by(self, claim_id: str) -> List[Dataset]:
        seen_keys: set[tuple[str, str]] = set()
        datasets: List[Dataset] = []
        for record in self._load_usage():
            if record["claim_id"] != claim_id:
                continue
            key = (record["name"], record["version"])
            if key in seen_keys:
                continue
            seen_keys.add(key)
            datasets.append(self.get(record["name"], record["version"]))
        return datasets

    def _version_dir(self, name: str, version: str) -> Path:
        return self.data_dir / name / version

    def _metadata_path(self, name: str, version: str) -> Path:
        return self._version_dir(name, version) / _METADATA_FILENAME

    def _content_path(self, name: str, version: str) -> Path:
        return self._version_dir(name, version) / _CONTENT_FILENAME

    def _load_metadata(self, name: str, version: str) -> Dataset:
        path = self._metadata_path(name, version)
        if not path.exists():
            raise DatasetNotFoundError(name, version)
        return Dataset.from_dict(json.loads(path.read_text()))

    def _list_versions(self, name: str) -> List[str]:
        name_dir = self.data_dir / name
        if not name_dir.exists():
            return []
        return [
            path.name
            for path in name_dir.iterdir()
            if path.is_dir() and (path / _METADATA_FILENAME).exists()
        ]

    def _load_usage(self) -> List[dict]:
        if not self.usage_path.exists():
            return []
        records = []
        with self.usage_path.open("r") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records
