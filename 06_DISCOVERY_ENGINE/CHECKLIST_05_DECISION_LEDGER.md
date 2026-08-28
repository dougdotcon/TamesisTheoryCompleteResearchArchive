# Checklist — Module 5: Decision Ledger

Source: `ROADMAP.md` §1 Stage 1, item 5. "An append-only, dated record
of every verdict, exactly as `DECISION_LEDGER.yaml` already is,
generalized beyond this one repository."

File: `src/tamesis_discovery_engine/ledger.py`. Tests:
`tests/test_ledger.py`. Can be built independently of Modules 1–4, but
Modules 1–4 should each append an entry here for their own major
events (registry creation/advance, run, reproduction, review verdict) —
wire this in during the Integration phase (see
`CHECKLIST_00_INTEGRATION_AND_VALIDATION.md`), not necessarily inside
this module's own checklist.

## Design

- [ ] `LedgerEntry`: `id` (`ENGINE-DEC-NNN`, sequential, never reused),
      `timestamp`, `claim_id`, `decision_type` (one of `REGISTER`,
      `LOCK`, `RUN`, `REPRODUCE`, `REVIEW`, `VERDICT`, or a free-form
      string — pick one and document it), `summary` (text), and
      `prev_hash` (hash of the previous entry's canonical serialization,
      or a fixed genesis value `"0"*64` for the first entry).
- [ ] `Ledger.append(claim_id, decision_type, summary) -> LedgerEntry`:
      computes `prev_hash` from the current last entry, computes this
      entry's own content hash, persists it (append to a JSONL file
      under `data/ledger.jsonl` — never rewrite prior lines).
- [ ] `Ledger.history(claim_id=None) -> list[LedgerEntry]`: full history,
      optionally filtered by claim.
- [ ] `Ledger.verify_chain() -> bool` (or raises with the first bad
      index): recomputes every entry's hash from its own content and
      checks it matches what the *next* entry's `prev_hash` claims —
      i.e. detects if any past entry's content was edited after the
      fact, not just whether the file parses.
- [ ] No `delete`/`update` method exposed on the public API — append-only
      is enforced by the interface, not just by convention.

## Tests (must all pass)

- [ ] Appending 3 entries, then `verify_chain()` returns `True`
      (or equivalent "clean" result).
- [ ] Directly editing one field of one persisted entry on disk (e.g.
      rewriting `summary` in the JSONL file for entry 2 without
      recomputing hashes) and then calling `verify_chain()` in a fresh
      `Ledger` instance **detects** the tamper — this is the actual
      point of hash-chaining and must be tested, not just the happy
      path.
- [ ] IDs are sequential and gap-free across a fresh sequence of
      appends; persisted, then reloaded in a fresh `Ledger`, the next
      `append()` continues the sequence correctly (no restart at 1, no
      collision).
- [ ] `history(claim_id=...)` returns only entries for that claim, in
      order.
- [ ] Confirm no public method allows deleting or mutating an existing
      entry (e.g. assert the class has no such method, or that
      attempting to call something like `_entries[i] = ...` from outside
      the module doesn't have a sanctioned API path — a simple `assert
      not hasattr(ledger, "delete")`-style check is enough; don't
      over-engineer this into an access-control system).

## Acceptance

- [ ] `pytest tests/test_ledger.py -v` passes with zero failures.
- [ ] The tamper-detection test is the one that actually matters here —
      do not let it become a no-op that always passes; verify it fails
      (red) if you temporarily comment out the hash check in
      `verify_chain()`, then confirm it passes (green) with the check
      restored, before considering this module done.
