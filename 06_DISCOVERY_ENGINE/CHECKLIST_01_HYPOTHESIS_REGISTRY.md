# Checklist — Module 1: Hypothesis Registry

Source: `ROADMAP.md` §1 Stage 1, item 1. "Structured claims with an ID
(`DISC-YYYY-NNNNN`), analogous to this archive's own `CLAIM_LEDGER.yaml`."

File: `src/tamesis_discovery_engine/registry.py` (+ a `claim.py` for the
`Claim` dataclass/state machine if that split reads cleaner). Tests:
`tests/test_registry.py`, `tests/test_claim_state_machine.py`.

## Design

- [ ] `Claim` object with fields: `id` (`DISC-YYYY-NNNNN`), `title`,
      `statement` (free text — the falsifiable hypothesis itself),
      `state`, `created_at`, `history` (ordered list of
      `{from_state, to_state, at, note}` transition records),
      `metadata` (free-form dict: owner, tags, thresholds declared at
      pre-registration time).
- [ ] State machine enum/constants matching `ROADMAP.md` exactly:
      `DRAFT → PRE_REGISTERED → LOCKED → RUNNING → RESULT →
      ADVERSARIAL_REVIEW → {CONFIRMED | REFUTED | INCONCLUSIVE | NULL}`.
- [ ] A transition table encoding exactly which `(from, to)` pairs are
      legal. No skipping states forward (e.g. `DRAFT → RESULT` directly
      is illegal — this is the pre-registration discipline itself, not
      an arbitrary restriction).
- [ ] The four terminal states (`CONFIRMED`, `REFUTED`, `INCONCLUSIVE`,
      `NULL`) are reachable only from `ADVERSARIAL_REVIEW`, and once
      reached, no further transition is legal (terminal).
- [ ] `Registry` class: `create(title, statement, metadata=None) -> Claim`
      (starts in `DRAFT`), `advance(claim_id, to_state, note="") -> Claim`
      (validates the transition, appends to history, persists), `get(id)`,
      `list(state=None, tag=None)`.
- [ ] ID generation: `DISC-{year}-{5-digit sequential}`, unique, sequence
      resets per calendar year, no reuse even across process restarts
      (derive next sequence from persisted state, not an in-memory
      counter).
- [ ] Persistence: JSON files under `data/claims/`, one file per claim
      (or one JSONL ledger — pick one and document why in a short
      module docstring). Must survive a process restart: write, reload
      in a fresh `Registry` instance, get back an identical `Claim`.
- [ ] Illegal transition raises a specific exception
      (`IllegalTransitionError` or similar), not a silent no-op and not
      a bare `Exception`.

## Tests (must all pass)

- [ ] Full legal sequence `DRAFT → PRE_REGISTERED → LOCKED → RUNNING →
      RESULT → ADVERSARIAL_REVIEW → CONFIRMED` succeeds and each step is
      recorded in `history` with a timestamp.
- [ ] Skipping a state (e.g. `DRAFT → LOCKED`) raises
      `IllegalTransitionError`.
- [ ] Transitioning out of a terminal state raises
      `IllegalTransitionError`.
- [ ] Persistence round-trip: create + advance a claim, instantiate a
      fresh `Registry` pointed at the same `data/` dir, `get()` returns
      an equal `Claim` (same id, state, full history).
- [ ] Two claims created in the same year get distinct, sequential ids;
      restarting the process and creating a third claim continues the
      sequence correctly (does not restart at 1 or collide).
- [ ] `list(state=...)` and `list(tag=...)` filter correctly against a
      small fixture set of claims in different states.

## Acceptance

- [ ] `pytest tests/test_registry.py tests/test_claim_state_machine.py -v`
      passes with zero failures and zero skips.
- [ ] No use of `datetime.now()`/`time.time()` results compared without
      tolerance in tests (freeze or inject time where tests assert on
      ordering, to avoid flaky tests).
- [ ] Module has no import from `05_DISCOVERY_LAB` — this is a generic
      engine, not wired to the archive's own math results.
