# /goal — active build tracker

**Purpose.** This file is the single continuously-updated tracker for the software
build-out authorized on 2026-08-28: turning the proposals in `ROADMAP.md` into real,
tested code. It is updated at every phase transition — do not let it go stale.

This file tracks **engineering** work (building software). It is separate from
`05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md`, which tracks **mathematical research**
(the `U₁/₂` proof program). The two pipelines run concurrently and neither blocks
the other.

---

## Current objective

Build **Stage 1 — Tamesis Discovery Engine v1**, the 5-module MVP defined in
`ROADMAP.md` §1 ("Stage 1 — MVP"), as real, tested Python code living in
`06_DISCOVERY_ENGINE/`. Per `ROADMAP.md` §3, Stage 1 is not "done" until it
reproduces the `U₁/₂` result end-to-end — `φ_∞(c)`, the `M_K` distribution, the
finite-`n` correction terms, and the `γ = c/n` regime — **starting only from the
bare hypothesis statement, with no hand-holding from `05_DISCOVERY_LAB`'s existing
scripts.** That is the literal acceptance test for this stage; see
`06_DISCOVERY_ENGINE/CHECKLIST_00_INTEGRATION_AND_VALIDATION.md`.

**Scope decision (made 2026-08-28, autonomously, per the roadmap's own dependency
order):** the user's instruction covers "all these new projects" — the 8-product
suite (Stage 3) and Tamesis OS (Stage 4) from the pasted strategic message. Building
those directly would violate `ROADMAP.md` §2's own non-goal ("not treating any
Stage 1–4 software as built until it exists, is tested, and is itself adversarially
reviewed") and the roadmap's explicit stage-dependency rule ("each stage assumes the
previous is real and load-bearing before the next begins"). So: build Stage 1 first,
validate it against `U₁/₂` for real, then use it as the base for Stage 2 expansion
modules, and only then reassess Stage 3. This is slower but honest — it is the same
discipline this archive already applies to every mathematical claim, applied one
level up to the tool that would run the claims.

---

## Status

| Stage | Scope | Status | Checklist |
|---|---|---|---|
| **Stage 1 — MVP** | 5 modules: Hypothesis Registry, Experiment Runner, Reproduction Engine, Adversarial Reviewer, Decision Ledger | 🔧 **IN PROGRESS** — scaffolding + checklists written, build dispatched | see `06_DISCOVERY_ENGINE/CHECKLIST_*.md` |
| Stage 2 — Expansion | Symbolic Mathematics, Monte Carlo Lab, Dataset Observatory, Lean bridge, Universality Atlas | ⏸ Not started — blocked on Stage 1 validation passing | not yet created |
| Stage 3 — Product suite | 8 named products | ⏸ Not started — blocked on Stage 2 | not yet created |
| Stage 4 — Tamesis OS | Unified architecture | ⏸ Not started — blocked on Stage 3 | not yet created |

---

## Log (most recent first)

- **2026-08-28** — Scaffolded `06_DISCOVERY_ENGINE/` (src/tests/benchmarks/data dirs), wrote this
  file and 6 per-module checklists (`CHECKLIST_01`..`CHECKLIST_05` + `CHECKLIST_00_INTEGRATION_AND_VALIDATION.md`).
  Dispatching a Workflow to build all 5 modules in parallel, then integrate, then run a
  hostile adversarial review pass on the engine itself before it is trusted with anything.

---

## Standing rules for this build (carried from the archive's existing discipline)

1. No module is "done" until its own checklist is fully checked off **and its tests pass**.
2. The Stage 1 acceptance test (`test_u12_end_to_end.py`) may not import from
   `05_DISCOVERY_LAB`'s existing proven scripts or hardcode their stored numeric outputs
   as its own computation — it must independently recompute `φ_∞(c)` etc. from the bare
   combinatorial/hypothesis definition, then compare to the closed form. Comparing against
   `THEOREM.md`'s stated closed forms as the assertion target is fine; *computing* the
   candidate value by copy-pasting the archive's own answer is not — that would validate
   nothing.
3. This is software-correctness work, not a new mathematical claim about the world — it
   does **not** get a `DISC-DEC` entry in `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`.
   If in the course of this build a genuinely new mathematical fact is discovered (not just
   re-derived), that finding is escalated into the Discovery Lab pipeline separately.
4. No stage is claimed "built" in `README.md`/`ROADMAP.md` until it is tested and has been
   through its own adversarial review pass, per `ROADMAP.md` §2.
