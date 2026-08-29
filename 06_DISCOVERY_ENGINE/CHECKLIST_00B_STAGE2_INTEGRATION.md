# Checklist — Stage 2 integration

Source: `ROADMAP.md` §1 Stage 2: "Once the MVP passes its own benchmark,
extend it with the machinery this archive already leans on manually" —
five modules (6–10, see `CHECKLIST_06`..`CHECKLIST_10`). This is the
acceptance gate for Stage 2 as a whole, mirroring
`CHECKLIST_00_INTEGRATION_AND_VALIDATION.md`'s role for Stage 1.

Depends on Modules 6–10 all being complete (their own checklists fully
checked off, their own tests green) and on Stage 1 (already done, see
`GOAL.md`).

## Integration

- [x] `src/tamesis_discovery_engine/__init__.py`'s `DiscoveryEngine`
      facade is extended with the five new modules
      (`symbolic`/`montecarlo`/`observatory`/`lean_bridge`/`atlas`),
      constructed alongside the existing five and sharing the same
      `data_dir` root — do not create a second, parallel facade class.
      Existing Stage 1 facade methods/behavior must not change (Stage 1's
      own test suite, `tests/test_integration.py` and
      `tests/test_u12_end_to_end.py`, must still pass unmodified after
      this — that is the regression check).
- [x] `tests/test_stage2_integration.py`: a single scenario exercising at
      least three of the five new modules together through the facade —
      e.g. a claim whose test plan is built via `symbolic.
      make_symbolic_identity_test_plan` (Module 6), locked/run through
      Stage 1's existing `Runner`, reproduced via Module 6's numeric
      route (Module 3), and — once `CONFIRMED` — both formalized via
      Module 9's `LeanBridge` and catalogued via Module 10's `Atlas`.
      This is the point of Stage 2: the new modules should compose with
      Stage 1 and each other, not just pass in isolation.

## Acceptance

- [x] `pytest 06_DISCOVERY_ENGINE/tests/ -v` — the FULL suite (Stage 1 +
      Stage 2 tests together), zero failures, zero skips (the Lean
      bridge tests are allowed to be slow, not skipped — see
      `CHECKLIST_09`'s own acceptance note).
- [x] A short adversarial review pass, by an agent that did not write
      Modules 6–10, over the new code specifically — same standard as
      Stage 1's own required review: hunt for fabricated/tautological
      tests, silently-passing checks, scope bypasses (e.g. `Atlas.
      register` or `LeanBridge.formalize` accepting a non-terminal/
      non-CONFIRMED claim through some code path the module's own tests
      didn't cover), and any accidental write access to
      `04_FORMAL_RESEARCH_LAB/` from `lean_bridge.py`. **Done**: a
      separately-dispatched reviewer read every module and test file in
      full, ran the full suite (142 passed), and hunted all six named
      failure modes — verdict `SOUND`, zero findings, so no fix pass was
      needed. **Independently re-confirmed by the orchestrating session**
      (2026-08-29): re-ran the full suite myself (142/142), grepped
      `src/`/`tests/` for `04_FORMAL_RESEARCH_LAB` (only docstring/regex
      prose, never a write path) and confirmed via `git status` that
      `04_FORMAL_RESEARCH_LAB/` itself is untouched; grepped
      `observatory.py` for network machinery (none); and drove
      `LeanBridge.formalize` myself end-to-end in a throwaway script —
      confirmed a true statement compiles, a false one fails with the
      real Lean compiler error ("Tactic `decide` proved that the
      proposition ... is false"), and a non-`CONFIRMED` claim raises
      `ClaimNotConfirmedError` without invoking the compiler at all.
- [x] `GOAL.md`'s Stage 2 row is not marked done until every box above
      (and every Module 6–10 checklist) is genuinely checked, mirroring
      the same discipline already applied to Stage 1. All six checklists
      (`CHECKLIST_06`..`CHECKLIST_10`, this file) are now fully checked;
      `GOAL.md` updated accordingly.
