# Checklist — Module 3: Reproduction Engine

Source: `ROADMAP.md` §1 Stage 1, item 3. "Re-runs a claim's experiment
from a second, independent implementation."

File: `src/tamesis_discovery_engine/reproduction.py`. Tests:
`tests/test_reproduction.py`. Depends on Modules 1 and 2.

## Design

- [ ] `Reproducer.reproduce(claim_id, second_test_plan, tolerance=1e-9) ->
      ReproductionRecord`: takes a claim that has a `RunRecord` (state
      `RESULT` or later), runs a **second**, independently-supplied test
      plan (deliberately not required to be the literal same function
      object — this models "a second, independent implementation", not
      re-running the same code) with the same declared params, and
      diffs its output against the original `RunRecord`'s result.
- [ ] Numeric comparison must support: scalars (abs/rel tolerance),
      and at minimum flat dicts/lists of scalars (recursively compare
      matching keys/indices). Non-numeric fields (strings, etc.) compare
      by equality.
- [ ] Three possible verdicts, not two: `EXACT_MATCH` (bit-identical),
      `MATCH_WITHIN_TOLERANCE` (differs but within `tolerance`), or
      `MISMATCH` (exceeds tolerance) — and `MISMATCH` must report the
      actual delta per differing field, not just "failed".
- [ ] `ReproductionRecord` persisted (JSON under `data/reproductions/`),
      linked to claim id, storing: verdict, per-field deltas, the
      tolerance used, timestamp.
- [ ] A guard used by Module 4/5: `has_successful_reproduction(claim_id)
      -> bool` — `True` only if there is a `ReproductionRecord` with
      verdict `EXACT_MATCH` or `MATCH_WITHIN_TOLERANCE`. This is the
      precondition the Adversarial Reviewer must check before it will
      run (a claim cannot skip straight from `RESULT` to
      `ADVERSARIAL_REVIEW` without a successful reproduction on file).

## Tests (must all pass)

- [ ] Reproducing with an identical second implementation of the same
      test plan yields `EXACT_MATCH` (or `MATCH_WITHIN_TOLERANCE` if
      floating point) against the original result.
- [ ] Reproducing with a second implementation deliberately perturbed
      (e.g. off by a constant well outside tolerance) is caught as
      `MISMATCH`, and the reported delta matches the actual injected
      perturbation.
- [ ] Tolerance boundary behavior: a delta of exactly `tolerance` (or
      just inside) reports `MATCH_WITHIN_TOLERANCE`; a delta just
      outside reports `MISMATCH` — test both sides of the boundary
      explicitly, don't just test one far-inside and one far-outside
      case.
- [ ] `has_successful_reproduction()` returns `False` before any
      reproduction is run, and `False` after a `MISMATCH`-only
      reproduction, and `True` only after at least one
      `EXACT_MATCH`/`MATCH_WITHIN_TOLERANCE` record exists.

## Acceptance

- [ ] `pytest tests/test_reproduction.py -v` passes with zero failures.
- [ ] The mismatch-detection test is not tautological — it must use a
      genuinely different second implementation (not literally calling
      the exact same function object with the exact same closure), to
      actually exercise "second, independent implementation".
