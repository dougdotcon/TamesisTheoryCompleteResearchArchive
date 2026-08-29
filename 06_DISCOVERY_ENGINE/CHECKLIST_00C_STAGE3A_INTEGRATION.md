# Checklist — Stage 3a integration

Source: `ROADMAP.md` §1 Stage 3, scoped per `GOAL.md`'s Stage 3 scoping
note (2026-08-29) to the two new-but-tractable products: Hypothesis
Engine and Mathematical Discovery Engine. Mirrors
`CHECKLIST_00B_STAGE2_INTEGRATION.md`'s role for Stage 2.

Depends on Modules 11–12 both being complete (their own checklists fully
checked off, their own tests green) and on Stages 1–2 (already done, see
`GOAL.md`).

## Integration

- [x] `src/tamesis_discovery_engine/__init__.py`'s `DiscoveryEngine`
      facade is extended to expose `HypothesisEngine` and
      `MathDiscoveryPipeline` alongside the existing ten modules,
      sharing the same `data_dir`/`registry` where applicable. Existing
      Stage 1 and Stage 2 facade behavior must not change — running the
      full pre-existing suite after this change must show the same 142
      tests still green (regression check), plus the new Module 11/12
      tests.
- [x] `tests/test_stage3a_integration.py`: a scenario using
      `HypothesisEngine.draft()` to create a claim with a structured
      spec, driving it through the existing Stage 1 lifecycle
      (`lock`/`run`/`reproduce`/`review`/`record_verdict`), then —
      separately — a `MathDiscoveryPipeline.run()` call against a small
      toy problem with 2+ candidates, demonstrating both new modules
      work standalone AND compose with the rest of the engine (the
      Hypothesis Engine claim does not need the Math Discovery Engine
      and vice versa — they are not on the tested claim's own critical
      path, but the test proves both are reachable through the one
      facade).

## Acceptance

- [x] `pytest 06_DISCOVERY_ENGINE/tests/ -v` — the FULL suite (Stages
      1+2+3a together), zero failures, zero skips.
- [x] A short adversarial review pass, by an agent that did not write
      Modules 11–12, over the new code: hunt for the same failure modes
      as Stage 1/2's reviews (fabricated/tautological tests, scope
      bypasses), plus specifically: does `hypothesis_engine.py` contain
      any hidden LLM/NLP call (grep, per `CHECKLIST_11`'s own note)?
      Does `mathematical_discovery_engine.py` genuinely reuse
      `symbolic.py`/`montecarlo.py` rather than reimplementing them
      (grep, per `CHECKLIST_12`'s own note)? Does any `CandidateResult`
      ever report `SURVIVES` when zero stages actually ran?
      Performed: `grep -rniE "openai|anthropic|\bllm\b|\bnlp\b"
      src/tamesis_discovery_engine/hypothesis_engine.py` finds nothing;
      `mathematical_discovery_engine.py` imports
      `verify_identity`/`verify_numeric_spot_check` from `.symbolic` and
      `triangulate` from `.montecarlo`, and contains no
      `sympy.simplify(`/`.equals(`/`default_rng`/`np.mean(`/`np.std(`
      of its own; `_derive_verdict` only sets `ran = True` when a stage
      actually produced a non-`None` outcome and returns `INCONCLUSIVE`
      (never `SURVIVES`) when nothing ran, confirmed both by code
      inspection and by the pre-existing
      `TestNoStageSuppliedIsInconclusiveNeverSurvives` test. No
      fabricated/tautological assertions or scope bypasses found in the
      new integration test.
- [x] `GOAL.md`'s Stage 3 row reflects Stage 3a as done, Simulation Lab
      and Observatory's live-feed capability as still explicitly open
      (per the Stage 3 scoping note) — not silently implied complete.
      Done by the orchestrating session (2026-08-29, outside this
      task's own scope boundary, as the build agent correctly noted):
      `GOAL.md`'s Stage 3 row and log now record Stage 3a as built,
      tested (175/175), and adversarially reviewed — including the one
      real HIGH finding (the Scope-honesty constraint's original
      "impossible to bypass" claim was false; corrected to accurately
      describe the actual, tested, ungated `Registry.advance()`/
      `DiscoveryEngine.advance()` bypass path rather than adding a
      cross-cutting validation hook nobody asked for) — while Simulation
      Lab and Observatory's live-feed half remain explicitly listed as
      deferred, not complete.
