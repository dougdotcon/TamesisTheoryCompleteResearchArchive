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

- [x] `LedgerEntry`: `id` (`ENGINE-DEC-NNN`, sequential, never reused),
      `timestamp`, `claim_id`, `decision_type` (one of `REGISTER`,
      `LOCK`, `RUN`, `REPRODUCE`, `REVIEW`, `VERDICT`, or a free-form
      string — pick one and document it), `summary` (text), and
      `prev_hash` (hash of the previous entry's canonical serialization,
      or a fixed genesis value `"0"*64` for the first entry).
- [x] `Ledger.append(claim_id, decision_type, summary) -> LedgerEntry`:
      computes `prev_hash` from the current last entry, computes this
      entry's own content hash, persists it (append to a JSONL file
      under `data/ledger.jsonl` — never rewrite prior lines).
- [x] `Ledger.history(claim_id=None) -> list[LedgerEntry]`: full history,
      optionally filtered by claim.
- [x] `Ledger.verify_chain() -> bool` (or raises with the first bad
      index): recomputes every entry's hash from its own content and
      checks it matches what the *next* entry's `prev_hash` claims —
      i.e. detects if any past entry's content was edited after the
      fact, not just whether the file parses. The link-only check
      above cannot, by itself, see tampering with the **last** entry
      (there is no following entry whose `prev_hash` would expose it).
      Closed via an out-of-band commitment: `append()` also writes the
      new tail entry's `content_hash()`, atomically (temp file +
      `os.replace`), to a companion file `<ledger_path>.head`;
      `verify_chain()` checks the reloaded tail entry against that
      externally-committed hash and raises `TamperDetectedError` if
      they disagree. Both middle-entry and tail-entry tampering are
      now covered — see the two regression tests below.
- [x] No `delete`/`update` method exposed on the public API — append-only
      is enforced by the interface, not just by convention.

## Tests (must all pass)

- [x] Appending 3 entries, then `verify_chain()` returns `True`
      (or equivalent "clean" result).
- [x] Directly editing one field of one persisted **middle** entry on
      disk (e.g. rewriting `summary` in the JSONL file for entry 2 of
      3 without recomputing hashes) and then calling `verify_chain()`
      in a fresh `Ledger` instance **detects** the tamper via the
      broken `prev_hash` link — this is the actual point of
      hash-chaining and must be tested, not just the happy path.
      (`test_tampering_with_a_persisted_entry_is_detected_by_a_fresh_ledger`)
- [x] Directly editing one field of the persisted **last/tail** entry
      on disk (e.g. rewriting a `VERDICT` entry's `summary` from
      "REFUTED..." to "CONFIRMED...", leaving every `prev_hash`
      untouched — there is no following entry to expose the change via
      the link check) and then calling `verify_chain()` in a fresh
      `Ledger` instance also **detects** the tamper, via the `.head`
      out-of-band commitment file. This was a real gap found by
      adversarial review (the link-only check is structurally blind to
      tail-entry tampering) and is now closed and covered by its own
      regression test, not folded silently into the middle-entry case.
      (`test_tampering_with_the_last_persisted_entry_is_detected_by_a_fresh_ledger`)
- [x] IDs are sequential and gap-free across a fresh sequence of
      appends; persisted, then reloaded in a fresh `Ledger`, the next
      `append()` continues the sequence correctly (no restart at 1, no
      collision).
- [x] `history(claim_id=...)` returns only entries for that claim, in
      order.
- [x] Confirm no public method allows deleting or mutating an existing
      entry (e.g. assert the class has no such method, or that
      attempting to call something like `_entries[i] = ...` from outside
      the module doesn't have a sanctioned API path — a simple `assert
      not hasattr(ledger, "delete")`-style check is enough; don't
      over-engineer this into an access-control system).

## Acceptance

- [x] `pytest tests/test_ledger.py -v` passes with zero failures
      (8/8, including both tamper-detection tests below).
- [x] The tamper-detection tests are the ones that actually matter here
      — do not let either become a no-op that always passes. Verified
      by temporarily short-circuiting the tail-hash check in
      `verify_chain()` (`if self._entries and self._head_hash is not
      None:` → `if False and ...`): the new tail-tampering test went
      red (`DID NOT RAISE TamperDetectedError`) as expected, confirming
      it is not vacuous; the check was then restored and the suite
      re-run to confirm green (78/78 across the full package suite).
