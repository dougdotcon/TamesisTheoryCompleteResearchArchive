# Checklist — Module 11: Hypothesis Engine (Stage 3a)

Source: `ROADMAP.md` §1 Stage 3 product table. "Turns a vague claim
('I think X causes Y') into a structured, falsifiable spec (prediction,
null model, competing model, effect size, threshold). Encodes the
pre-registration discipline this archive already requires by hand."

File: `src/tamesis_discovery_engine/hypothesis_engine.py`. Tests:
`tests/test_hypothesis_engine.py`. Builds on Stage 1's
`registry.py`/`claim.py` — read them first.

**Scope honesty constraint (read before writing code):** this module
does **not** use any NLP/LLM inference to "understand" a vague free-text
claim and auto-generate its null model, competing model, etc. — that
would be exactly the kind of fabricated rigor this archive's own ethos
(and `CHECKLIST_04`'s own precedent) rejects. What it actually does:
provide a **structured spec type** with validation, so that turning a
vague idea into a falsifiable spec is a deliberate, explicit authoring
step (done by a human or an agent, filling in real fields) rather than
an unstructured free-text `statement` string.

**This is not a system-wide guarantee — do not describe it as one.**
`HypothesisEngine.pre_register()` enforces spec completeness only for
callers that go through it. `Registry.advance()`/`DiscoveryEngine.advance()`
remain generic, ungated transitions (as they are for every other Stage 1
state change, and as Stage 1's own tests already rely on to pre-register
spec-less claims) and do not check `FalsifiableSpec` completeness, because
neither method knows this module or `FalsifiableSpec` exists. A caller
that bypasses `HypothesisEngine.pre_register()` — including via
`Registry.advance(claim_id, PRE_REGISTERED)` or the facade's
`DiscoveryEngine.advance(claim_id, PRE_REGISTERED)`, for a claim that
`HypothesisEngine.draft()` itself created — also bypasses this discipline.
The "encodes the discipline" part is the validation performed by
`HypothesisEngine.draft()`/`HypothesisEngine.pre_register()` themselves,
not a hook wired into `Registry.create`/`Registry.advance`.

## Design

- [x] `FalsifiableSpec` dataclass: `raw_claim` (the original vague
      free-text idea, kept for provenance), `prediction` (what the
      hypothesis predicts, specific enough to check), `null_model`
      (what "no effect" looks like), `competing_model` (an alternative
      explanation the spec must be checkable against — may be `None`
      with an explicit `competing_model_rationale` explaining why none
      applies, but not silently absent), `effect_size_metric` (the named
      quantity that will be measured), `threshold` (the pre-registered
      decision criterion, e.g. "effect size > X" or "p < Y" — a string
      or number, whichever is natural, but never empty).
- [x] `FalsifiableSpec.validate() -> list[str]`: returns a list of
      problems (empty list = valid). Checks: `prediction`, `null_model`,
      `effect_size_metric`, `threshold` are all non-empty; either
      `competing_model` or `competing_model_rationale` is present (not
      both empty). Does NOT try to judge whether the *content* is
      scientifically sound — that's what Module 4 (Adversarial Reviewer)
      is for, applied later in the claim's life. This module only
      enforces *structural* completeness.
- [x] `FalsifiableSpec.to_claim_metadata() -> dict`: formats the spec for
      passing into Stage 1's `Registry.create(metadata=...)` — this is
      the actual integration point. The resulting claim's `metadata`
      must contain enough to reconstruct the spec later (round-trippable
      via a `FalsifiableSpec.from_claim_metadata(dict)` classmethod).
- [x] `HypothesisEngine.draft(registry, title, spec: FalsifiableSpec) ->
      Claim`: creates a claim (via `Registry.create`) carrying the spec
      in its metadata. **Enforced precondition:** raises (with the
      validation problems included in the error) if `spec.validate()` is
      non-empty — a structurally incomplete spec cannot even become a
      `DRAFT` claim through this path (an incomplete idea can still be
      scribbled directly via `Registry.create` itself with a free-text
      `statement`, per Module 1's own contract — this module's value is
      the enforced path for claims that go through it).
- [x] `HypothesisEngine.pre_register(registry, claim_id) -> Claim`:
      wraps `Registry.advance(claim_id, PRE_REGISTERED)`, but first
      re-validates the spec stored in the claim's metadata (in case it
      was hand-edited after `draft()`) and raises if it's now
      incomplete — this is where "encodes the pre-registration
      discipline" actually bites: you cannot lock in a claim as
      pre-registered with a broken spec **through this method**.
      `Registry.advance()`/`DiscoveryEngine.advance()` called directly
      remain ungated (see the Scope honesty constraint above) — this is
      documentation-and-test-pinned current behavior
      (`tests/test_hypothesis_engine.py::test_registry_advance_bypasses_pre_register_completeness_check`,
      `tests/test_stage3a_integration.py::test_facade_advance_bypasses_hypothesis_engine_pre_register_completeness_check`),
      not a gap this checklist claims is closed.

## Tests (must all pass)

- [x] `validate()` returns an empty list for a genuinely complete spec,
      and a non-empty list (naming the missing field) for each of: empty
      `prediction`, empty `null_model`, empty `effect_size_metric`, empty
      `threshold`, and both `competing_model`/`competing_model_rationale`
      empty at once.
- [x] `to_claim_metadata()` / `from_claim_metadata()` round-trip an
      equal `FalsifiableSpec`.
- [x] `HypothesisEngine.draft()` with a valid spec creates a `DRAFT`
      claim whose metadata reconstructs the same spec; with an invalid
      spec, raises without creating any claim (assert via
      `registry.list()` before/after — nothing was created).
- [x] `HypothesisEngine.pre_register()` on a claim with a still-valid
      spec succeeds and transitions the claim; on a claim whose metadata
      was hand-tampered to remove a required field, raises
      `IncompleteSpecError` (not a bare `TypeError`/`KeyError`) and the
      claim stays in `DRAFT` (state unchanged) — covered for both ways a
      field can go missing: emptied to `""` (spec reconstructs but fails
      `validate()`) and the key deleted outright from
      `metadata['falsifiable_spec']` (spec reconstruction itself raises
      `TypeError`, caught alongside the no-entry-at-all `KeyError` case).

## Acceptance

- [x] `pytest tests/test_hypothesis_engine.py -v` passes with zero
      failures.
- [x] `grep -rn "openai\|anthropic\|llm\|nlp" src/tamesis_discovery_engine/hypothesis_engine.py`
      (case-insensitive) finds nothing — confirms no hidden AI-inference
      dependency contradicting this checklist's scope constraint.
