# Checklist — Module 4: Adversarial Reviewer

Source: `ROADMAP.md` §1 Stage 1, item 4, and Stage 3's "Tamesis
Adversarial Reviewer" description: "checks for p-hacking, leakage,
post-hoc thresholds, confounders, overfitting, numerical instability."
"Structurally separated from the claim's own author... a first-class
step, not a manual habit."

File: `src/tamesis_discovery_engine/adversarial.py`. Tests:
`tests/test_adversarial.py`. Depends on Modules 1–3.

**Design honesty constraint (important — read before writing code):** do
not fabricate statistical rigor. This module implements a **small set of
concrete, real, testable heuristic checks** — not a general p-hacking
detector (that doesn't exist as a deterministic algorithm). Each check
below must have a crafted "bad" fixture it correctly flags and a
crafted "clean" fixture it correctly passes. If a check can't be made
concrete and testable, cut it rather than stub it with a check that
always passes.

## Design

- [x] `AdversarialReviewer.review(claim_id) -> ReviewVerdict`.
      **Precondition, enforced:** raises if
      `reproduction.has_successful_reproduction(claim_id)` is `False` —
      review cannot start without a successful reproduction on file
      (mirrors the archive's own "reproduce before referee" order).
- [x] Check 1 — **post-hoc threshold**: the claim's `metadata` declared
      at `PRE_REGISTERED` time (before `RUNNING`) must include a named
      success threshold/criterion. The reviewer verifies that threshold
      was recorded in `history` at or before the `PRE_REGISTERED`
      transition, not added/edited afterward. Flags if the threshold is
      missing, or if `metadata` shows a later edit to the threshold
      after `LOCKED`.
- [x] Check 2 — **numerical instability**: if the test plan declares a
      `seed` parameter, the reviewer re-runs it with 2–3 different seed
      values (via the Experiment Runner, off the record — not mutating
      the claim's own `RunRecord`) and flags if results vary beyond a
      declared instability tolerance. If no seed param is declared,
      this check is skipped and says so explicitly in the verdict (not
      silently passed as if it ran).
- [x] Check 3 — **overfitting/parameter-count smell**: if the test plan
      declares `n_params` and `n_samples` in its params/result, flags a
      warning if `n_params >= n_samples` (a real, simple, honestly-
      labeled heuristic — not a general overfitting detector).
- [x] Check 4 — **leakage**: if the test plan declares
      `calibration_indices` and `validation_indices` (or similarly named
      sets) in its params, flags if the two sets intersect.
- [x] `ReviewVerdict`: `{flags: [{check, severity, detail}], all_checks_run:
      [...], skipped_checks: [...]}` plus a `recommendation` (`CLEAN` if
      no flags, `FLAGGED` otherwise) — **not** itself a final claim
      verdict. Automating the terminal-state transition end-to-end from
      a heuristic score would be exactly the kind of unaccountable
      automation this archive's own ethos rejects.
- [x] A **separate, explicit** method `record_verdict(claim_id, verdict:
      Literal[CONFIRMED, REFUTED, INCONCLUSIVE, NULL], rationale: str)`
      that performs the `ADVERSARIAL_REVIEW → {terminal}` transition.
      Raises if called before `review()` has been run at least once for
      this claim (no verdict without an actual adversarial pass on
      record). `rationale` is stored in `history`, required non-empty —
      this is the accountable-decision requirement, deliberately not
      automatic even when `review()` returns `CLEAN`.

## Tests (must all pass)

- [x] Check 1: a claim whose `PRE_REGISTERED` metadata has no threshold
      is flagged; a claim with the threshold declared at
      `PRE_REGISTERED` time and never altered passes clean.
- [x] Check 2: a test plan whose result is seed-sensitive beyond
      tolerance is flagged; a seed-stable test plan passes; a test plan
      with no seed param results in `skipped_checks` containing this
      check, not a false pass.
- [x] Check 3: `n_params >= n_samples` fixture is flagged;
      `n_params < n_samples` fixture passes clean.
- [x] Check 4: overlapping calibration/validation index sets are
      flagged; disjoint sets pass clean.
- [x] `review()` raises if called before a successful reproduction
      exists on the claim.
- [x] `record_verdict()` raises if called before `review()` has run;
      raises on empty `rationale`; on success, transitions the claim to
      the given terminal state and it becomes immutable (a further
      `advance()` call from Module 1 on this claim raises).

## Acceptance

- [x] `pytest tests/test_adversarial.py -v` passes with zero failures.
- [x] No check silently reports "clean" when it didn't actually run —
      grep the test file to confirm each check has both a triggering
      and a non-triggering fixture.
