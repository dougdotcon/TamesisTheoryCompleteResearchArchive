# Checklist — Module 8: Dataset Observatory (Stage 2)

Source: `ROADMAP.md` §1 Stage 2, item 8. "Provenance-tracked ingestion
of external reference data (this archive already does this by hand for
PDG, CODATA, Planck, SPARC, Gaia, Odlyzko), so every claim's data
lineage is queryable, not just documented in prose."

File: `src/tamesis_discovery_engine/observatory.py`. Tests:
`tests/test_observatory.py`.

**Scope note:** this module does NOT fetch real external data over the
network — that would make tests network-dependent and flaky, and is out
of scope for Stage 2. It builds the provenance-tracking machinery
(ingest, checksum, version, link-to-claim, query) generically, tested
against small synthetic byte content standing in for a "dataset." Wiring
it to real PDG/CODATA/etc. sources is future work, honestly out of scope
here — say so in the module docstring, don't imply real data sources are
wired up.

## Design

- [ ] `Dataset` dataclass: `name`, `version`, `source_citation` (free
      text — where this data notionally came from), `checksum` (sha256
      hex of the ingested content), `ingested_at`, `size_bytes`.
- [ ] `DatasetRegistry.ingest(name, version, source_citation,
      content: bytes) -> Dataset`: computes the checksum, persists the
      content under `data/datasets/{name}/{version}/` plus a metadata
      JSON, returns the `Dataset` record. Re-ingesting the same
      `(name, version)` with **different** content must raise (a
      version is immutable once ingested — silently overwriting it would
      break every claim that already cited it as provenance).
- [ ] `DatasetRegistry.get(name, version=None) -> Dataset`: `version=None`
      returns the latest ingested version for that name (by
      `ingested_at`).
- [ ] `DatasetRegistry.verify_integrity(name, version) -> bool`:
      recomputes the checksum of the persisted content and compares to
      the recorded one — detects on-disk corruption/tampering, mirroring
      the same tamper-evidence spirit as Stage 1's Ledger.
- [ ] `DatasetRegistry.record_usage(claim_id, name, version)`: appends a
      provenance record ("claim X declares it used dataset Y@version").
      `DatasetRegistry.used_by(name, version) -> list[claim_id]` and
      `DatasetRegistry.datasets_used_by(claim_id) -> list[Dataset]` are
      the two query directions.

## Tests (must all pass)

- [ ] Ingesting a dataset, then `get()` in a fresh `DatasetRegistry`
      instance returns identical metadata (persistence round-trip).
- [ ] Re-ingesting the same `(name, version)` with the same content is a
      no-op (or returns the existing record) — re-ingesting with
      **different** content raises.
- [ ] `verify_integrity` returns `True` untouched, and `False` after the
      persisted content file is directly modified on disk.
- [ ] `get(name)` with no version returns the most recently ingested
      version when multiple versions exist.
- [ ] `record_usage`/`used_by`/`datasets_used_by` round-trip correctly
      for a claim that used two different datasets.

## Acceptance

- [ ] `pytest tests/test_observatory.py -v` passes with zero failures.
- [ ] No network call anywhere in this module — grep for `requests`,
      `urllib`, `httpx`, `socket` to confirm; all tests use in-memory
      synthetic byte content.
