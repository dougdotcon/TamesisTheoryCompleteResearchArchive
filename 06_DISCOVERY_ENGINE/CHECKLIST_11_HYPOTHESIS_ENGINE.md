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
an unstructured free-text `statement` string — and make it impossible to
pre-register a claim (Module 1's `PRE_REGISTERED` state) without that
structure being complete. The "encodes the discipline" part is the
validation + wiring, not automated understanding.

## Design

- [ ] `FalsifiableSpec` dataclass: `raw_claim` (the original vague
      free-text idea, kept for provenance), `prediction` (what the
      hypothesis predicts, specific enough to check), `null_model`
      (what "no effect" looks like), `competing_model` (an alternative
      explanation the spec must be checkable against — may be `None`
      with an explicit `competing_model_rationale` explaining why none
      applies, but not silently absent), `effect_size_metric` (the named
      quantity that will be measured), `threshold` (the pre-registered
      decision criterion, e.g. "effect size > X" or "p < Y" — a string
      or number, whichever is natural, but never empty).
- [ ] `FalsifiableSpec.validate() -> list[str]`: returns a list of
      problems (empty list = valid). Checks: `prediction`, `null_model`,
      `effect_size_metric`, `threshold` are all non-empty; either
      `competing_model` or `competing_model_rationale` is present (not
      both empty). Does NOT try to judge whether the *content* is
      scientifically sound — that's what Module 4 (Adversarial Reviewer)
      is for, applied later in the claim's life. This module only
      enforces *structural* completeness.
- [ ] `FalsifiableSpec.to_claim_metadata() -> dict`: formats the spec for
      passing into Stage 1's `Registry.create(metadata=...)` — this is
      the actual integration point. The resulting claim's `metadata`
      must contain enough to reconstruct the spec later (round-trippable
      via a `FalsifiableSpec.from_claim_metadata(dict)` classmethod).
- [ ] `HypothesisEngine.draft(registry, title, spec: FalsifiableSpec) ->
      Claim`: creates a claim (via `Registry.create`) carrying the spec
      in its metadata. **Enforced precondition:** raises (with the
      validation problems included in the error) if `spec.validate()` is
      non-empty — a structurally incomplete spec cannot even become a
      `DRAFT` claim through this path (an incomplete idea can still be
      scribbled directly via `Registry.create` itself with a free-text
      `statement`, per Module 1's own contract — this module's value is
      the enforced path for claims that go through it).
- [ ] `HypothesisEngine.pre_register(registry, claim_id) -> Claim`:
      wraps `Registry.advance(claim_id, PRE_REGISTERED)`, but first
      re-validates the spec stored in the claim's metadata (in case it
      was hand-edited after `draft()`) and raises if it's now
      incomplete — this is where "encodes the pre-registration
      discipline" actually bites: you cannot lock in a claim as
      pre-registered with a broken spec.

## Tests (must all pass)

- [ ] `validate()` returns an empty list for a genuinely complete spec,
      and a non-empty list (naming the missing field) for each of: empty
      `prediction`, empty `null_model`, empty `effect_size_metric`, empty
      `threshold`, and both `competing_model`/`competing_model_rationale`
      empty at once.
- [ ] `to_claim_metadata()` / `from_claim_metadata()` round-trip an
      equal `FalsifiableSpec`.
- [ ] `HypothesisEngine.draft()` with a valid spec creates a `DRAFT`
      claim whose metadata reconstructs the same spec; with an invalid
      spec, raises without creating any claim (assert via
      `registry.list()` before/after — nothing was created).
- [ ] `HypothesisEngine.pre_register()` on a claim with a still-valid
      spec succeeds and transitions the claim; on a claim whose metadata
      was hand-tampered to remove a required field, raises and the claim
      stays in `DRAFT` (state unchanged).

## Acceptance

- [ ] `pytest tests/test_hypothesis_engine.py -v` passes with zero
      failures.
- [ ] `grep -rn "openai\|anthropic\|llm\|nlp" src/tamesis_discovery_engine/hypothesis_engine.py`
      (case-insensitive) finds nothing — confirms no hidden AI-inference
      dependency contradicting this checklist's scope constraint.
