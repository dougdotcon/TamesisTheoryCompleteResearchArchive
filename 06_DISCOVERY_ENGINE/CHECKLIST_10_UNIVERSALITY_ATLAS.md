# Checklist — Module 10: Universality Atlas (Stage 2)

Source: `ROADMAP.md` §1 Stage 2, item 10. "A registry of tested
invariants/scaling exponents across domains, so a new candidate can be
checked against everything already tried (this archive's own `TRI-RG`
line — 16 candidates, all `CLOSED_NULL` — is exactly the kind of
negative-result catalogue this module should make queryable instead of
buried in a single markdown file)."

File: `src/tamesis_discovery_engine/atlas.py`. Tests:
`tests/test_atlas.py`. Builds on Stage 1's `Registry`/`claim.py` — read
them first.

The point, concretely: `05_DISCOVERY_LAB`'s own `TRI-RG` line already
does exactly this by hand (a markdown table of tested invariants and why
each was rejected). This module makes that pattern queryable and
enforces that only *disposed* claims (a terminal state reached) get
catalogued — an open, still-running claim has no business being listed
as a tested invariant yet.

## Design

- [x] `AtlasEntry` dataclass: `domain` (free text, e.g. `"TRI-RG"`,
      `"u12_universality"`), `invariant_name`, `value` (float or a
      short formula string — support both, document the convention
      chosen), `source_claim_id`, `verdict` (pulled from the claim's
      terminal state at registration time — `CONFIRMED`/`REFUTED`/
      `INCONCLUSIVE`/`NULL`), `registered_at`.
- [x] `Atlas.register(domain, invariant_name, value, source_claim_id) ->
      AtlasEntry`. **Enforced precondition:** raises unless the claim
      (via Stage 1's `Registry`) is in one of the four terminal states —
      this is the "only catalogue disposed items" discipline. The
      `verdict` field is read from the claim itself, never passed in
      separately (so it can't drift from the claim's actual recorded
      outcome).
- [x] `Atlas.search(domain=None, invariant_name=None) -> list[AtlasEntry]`:
      filter by either/both/neither.
- [x] `Atlas.find_near_duplicates(domain, invariant_name, value,
      tolerance) -> list[AtlasEntry]`: within the same `domain`, find
      existing entries whose `value` is within `tolerance` of the given
      one — regardless of `invariant_name` (two different-sounding
      invariants can turn out to be numerically the same tested
      quantity; that's exactly the kind of duplicate this should catch).
      Only compares entries where `value` is numeric — entries with a
      formula-string `value` are skipped for this check (documented, not
      silently mismatched).

## Tests (must all pass)

- [x] Registering against a claim in a terminal state succeeds and
      `verdict` matches that claim's actual state.
- [x] Registering against a claim in a non-terminal state (e.g. `RESULT`,
      `ADVERSARIAL_REVIEW`) raises, without creating an entry.
- [x] `search(domain=...)`, `search(invariant_name=...)`, and both
      together filter correctly against a small fixture set spanning two
      domains.
- [x] `find_near_duplicates` finds an entry within tolerance and does
      NOT find one just outside tolerance (test both sides of the
      boundary), and correctly scopes the search to the given `domain`
      only (an identical value in a different domain is not a
      duplicate).
- [x] Persistence round-trip: entries survive a fresh `Atlas` instance
      pointed at the same data directory.

## Acceptance

- [x] `pytest tests/test_atlas.py -v` passes with zero failures.
- [x] `Atlas.register` cannot be called with a fabricated `verdict`
      argument — confirm its signature has no such parameter (the
      verdict must only ever come from reading the claim itself).
