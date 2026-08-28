# Tamesis Roadmap: From Research Archive to Discovery Infrastructure

**Status: proposed vision, not a committed plan or a claimed deliverable.** Nothing on this page is built, funded, or scheduled. It exists to make one strategic argument explicit and give it a chronological shape, in the same spirit the rest of this archive already uses for separating hypothesis from evidence: **the most defensible thing this project has produced is not a physical theory — it is a falsification methodology and one genuine mathematical result produced by that methodology.** This document proposes what follows *if* that argument is accepted. It carries the same disclaimers as everything else here: no Millennium Problem is claimed solved, no physical law is claimed confirmed, no software below exists yet unless explicitly marked otherwise.

Origin: this roadmap was assembled 2026-08-28 from an external strategic review of the archive's state at that date (post `DISC-DEC-115`, Estágios 1–42, 16 Discovery Lab test lines, 1 proved positive mathematical result). See `README.md` for the archive's actual current state; this document only extrapolates forward from it.

---

## 0. The reframing this roadmap is built on

The strongest asset in this repository, read plainly, is not the physical ontology — it is:

1. **One real, adversarially-verified mathematical result** (the `U₁/₂` limit law and its general-`K` extensions, `THEOREM.md`), reached by rejecting a first guess `(1+c)^{-1/2}` that exact enumeration refuted, and replacing it with the correct closed form `φ_∞(c) = ½√(π/c)·erf(√c)` — a textbook example of a hypothesis losing while the mechanism and the research process survive.
2. **A falsification engine** (`05_DISCOVERY_LAB`) that has spent most of its effort trying to *kill* Tamesis's own hypotheses, not confirm them — 16 test lines, most closed `NULL`/`INCONCLUSIVE`/`REFUTED`, with fabricated legacy data caught and redone, estimator bugs found and fixed, and a running two-tier public correction record (`correção` / `nota`) for every mistake this archive itself has made.
3. **A structural pattern**: a discrete combinatorial system (permutation → rerouting → cycles → survival) collapsing onto a strikingly simple continuous limit law — exactly the shape of result that belongs to probability theory, random mappings, and universality-class classification, independent of any physical interpretation layered on top.

The reframing this roadmap assumes: **Tamesis is a research system designed to discover where its own hypotheses fail, not a theory that assumes it is right.** Physics is one possible *application* of that system, not the premise the rest of it depends on. Under that framing, the highest-value next artifact is not a bigger physical claim — it is packaging the falsification methodology itself as reusable infrastructure, with `U₁/₂` kept permanently as its first benchmark case.

---

## 1. Chronological trail

Five stages, each assuming the previous one is real and load-bearing before the next begins. Nothing here implies a fixed calendar — "stage" denotes dependency order, not a date.

### Stage 0 — Foundation (already exists today)

What's already on record and does not need to be built:
- The Discovery Lab pre-registration → adversarial-review → decision-ledger pipeline (`05_DISCOVERY_LAB/00_GOVERNANCE/`), run by hand across 16 test lines and 115 governance decisions.
- The `U₁/₂` result family in `THEOREM.md`, with its own audit trail: exact enumeration, closed-form derivation, proofs for every `K`, uniform convergence, sharp rate constants, `γ = c/n` scaling, the full distributional law for `K ≥ 1`, and dozens of independent adversarial reproduction rounds.
- The two-tier honesty convention (dated `correção` for real errors, dated `nota` for clarifications) applied consistently, including to this archive's own mistakes.

This stage is the *proof of concept* the rest of the roadmap tries to generalize into software — it is manual and slow today, run by a human/agent pipeline rather than a product.

### Stage 1 — MVP: Tamesis Discovery Engine v1

A minimal software encoding of the Stage 0 workflow, five modules only:

1. **Hypothesis Registry** — structured claims with an ID (`DISC-YYYY-NNNNN`), analogous to this archive's own `CLAIM_LEDGER.yaml`.
2. **Experiment Runner** — executes a pre-registered, locked test plan against declared data/code.
3. **Reproduction Engine** — re-runs a claim's experiment from a second, independent implementation.
4. **Adversarial Reviewer** — a dedicated hostile-review pass, structurally separated from the claim's own author (this archive already does this with separately-dispatched referee agents; Stage 1 encodes it as a first-class step, not a manual habit).
5. **Decision Ledger** — an append-only, dated record of every verdict, exactly as `DECISION_LEDGER.yaml` already is, generalized beyond this one repository.

Claim state machine (mirrors what this archive already does informally):

```
DRAFT → PRE_REGISTERED → LOCKED → RUNNING → RESULT → ADVERSARIAL_REVIEW → {CONFIRMED | REFUTED | INCONCLUSIVE | NULL}
```

**Required validation before Stage 1 counts as done:** the MVP must reproduce the `U₁/₂` result end-to-end — `φ_∞(c)`, the `M_K` distribution, the finite-`n` corrections, and the `γ = c/n` regime — starting only from the hypothesis statement, with no hand-holding from this archive's existing scripts. If the software cannot rediscover what a human/agent pipeline already proved, it is not ready to test anything new.

### Stage 2 — Expansion modules

Once the MVP passes its own benchmark, extend it with the machinery this archive already leans on manually:

6. **Symbolic Mathematics** — computer-algebra support (`sympy`-class tooling) wired directly into the Hypothesis Registry, not bolted on afterward.
7. **Monte Carlo Lab** — a standard library for the triangulation-only Monte Carlo checks this archive already runs alongside every exact result.
8. **Dataset Observatory** — provenance-tracked ingestion of external reference data (this archive already does this by hand for PDG, CODATA, Planck, SPARC, Gaia, Odlyzko), so every claim's data lineage is queryable, not just documented in prose.
9. **Formal Proof / Lean integration** — a bridge from a CONFIRMED claim into `04_FORMAL_RESEARCH_LAB`-style Lean4 formalization, for the subset of results with a genuine mathematical core (this archive already draws this line explicitly; the module should enforce it, not blur it).
10. **Universality Atlas** — a registry of tested invariants/scaling exponents across domains, so a new candidate can be checked against everything already tried (this archive's own `TRI-RG` line — 16 candidates, all `CLOSED_NULL` — is exactly the kind of negative-result catalogue this module should make queryable instead of buried in a single markdown file).

### Stage 3 — The product suite

If Stages 1–2 hold up under real use, the roadmap widens into distinct, separately-usable tools built on the same core:

| Product | What it does | Relationship to this archive |
|---|---|---|
| **Tamesis Discovery Lab** | The main platform: hypothesis dashboard, claim states, reproduction/adversarial pipeline | Direct generalization of `05_DISCOVERY_LAB` itself |
| **Tamesis Hypothesis Engine** | Turns a vague claim ("I think X causes Y") into a structured, falsifiable spec (prediction, null model, competing model, effect size, threshold) | Encodes the pre-registration discipline this archive already requires by hand |
| **Tamesis Adversarial Reviewer** | Runs an automated hostile-review pass over a result — checks for p-hacking, leakage, post-hoc thresholds, confounders, overfitting, numerical instability | Generalizes the hostile-referee-agent pattern this session already uses for every mathematical claim |
| **Tamesis Mathematical Discovery Engine** | Given a combinatorial/asymptotic system definition, runs exact enumeration → symbolic algebra → simulation → asymptotic fitting → proof-candidate search | Generalizes exactly the `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS` workflow that produced the `U₁/₂` family |
| **Tamesis Universality Atlas** | Given a new dynamical system, searches known invariants/scaling laws for a match or a genuinely new universality class | Generalizes the `TRI-RG` cross-domain-invariant search |
| **Tamesis Simulation Lab** | A visual environment for building agent-based / network complex systems and observing emergent statistics | New — no direct precedent in this archive yet |
| **Tamesis Observatory** | Continuously tests a locked prediction against live public datasets (Gaia, SPARC, Planck, LIGO, CERN, EEG, magnetometer feeds, etc.) | Generalizes the archive's own SPARC/Gaia/RH-REAL testing lines into an always-on service instead of one-shot analyses |
| **Tamesis Scientific Ledger** | The versioned, auditable substrate underneath all of the above — claim → version → hypothesis → prediction → data → code → result → reproduction → adversarial attack → verdict → new version | Generalizes `DECISION_LEDGER.yaml` + `CLAIM_LEDGER.yaml` into a first-class, queryable object instead of two YAML files |

The operating analogy for the Scientific Ledger, stated plainly because it is the clearest way to explain why this differs from a normal paper-publication model:

```
Traditional software      Traditional science           Tamesis
Code                       Hypothesis                     Hypothesis
  ↓                          ↓                               ↓
Test                       Experiment                      Pre-registration
  ↓                          ↓                               ↓
CI                         Paper                            Prediction
  ↓                          ↓                               ↓
Bug                        Publication                      Experiment
  ↓                                                          ↓
Issue                                                       Data
  ↓                                                          ↓
Fix                                                         Reproduction
  ↓                                                          ↓
Release                                                     Adversarial attack
                                                              ↓
                                                             Verdict
                                                              ↓
                                                             New version
```

### Stage 4 — Unified architecture ("Tamesis OS")

If enough of Stage 3 exists independently and holds together, the long-term shape is one platform with three labs sharing a common evidence/decision substrate:

```
                    TAMESIS OS
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   Discovery       Simulation      Evidence
      Lab             Lab            Lab
        │              │              │
        ▼              ▼              ▼
  Hypotheses        Models          Datasets
  Predictions       Monte Carlo     References
  Pre-registration  Numerics        Provenance
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                Adversarial Engine
                       │
                       ▼
                Reproduction Engine
                       │
                       ▼
                 Decision Ledger
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       PROVED       REFUTED     INCONCLUSIVE
```

Candidate stack (unevaluated, listed only because a concrete stack was part of the originating proposal): PostgreSQL, Python, FastAPI, Celery, Redis, Docker, Git, Jupyter, SymPy, NumPy, SciPy, Lean. None of this is committed; it is a starting guess consistent with what the archive already uses (Lean4 for `04_FORMAL_RESEARCH_LAB`, Python/SymPy throughout `05_DISCOVERY_LAB`).

---

## 2. Explicit non-goals for now

Carried over deliberately from the originating proposal, because they match this archive's existing discipline against overclaiming:

- **Not** pursuing a "Tamesis solves physics" narrative as the near-term goal. Lines `A`, `H`, `I`, `J`, `O` (the physical-ontology lines) remain far from a closed physical theory, by this archive's own accounting.
- **Not** treating any Stage 1–4 software as built until it exists, is tested, and — per this repository's standing rule — is itself adversarially reviewed before being trusted.
- **Not** skipping the formalization chain a genuine physical claim would need: axiom → action → equations → parameters → units → symmetry → conservation law → prediction → experiment → replication. Until a physical line reaches that chain, it stays labeled hypothesis, exactly as `README.md`'s status table already does.
- **Not** using this roadmap as a claim of funding, timeline, or team commitment. It is a prioritization argument, nothing more, until someone decides to act on it.

---

## 3. Why `U₁/₂` is the required first benchmark, not an example

Any Stage 1 implementation is validated against one fixed target before it is trusted with anything new:

1. Reproduce `φ_∞(c)` from the bare hypothesis statement.
2. Reproduce the `M_K` distribution for general `K`.
3. Reproduce the finite-`n` correction terms.
4. Reproduce the `γ = c/n` scaling regime.

If a candidate Discovery Engine cannot re-derive what this archive's own manual pipeline already proved and adversarially confirmed, it has no business being pointed at an unproven hypothesis. This is the same discipline `05_DISCOVERY_LAB` already applies to every new numerical pipeline (`build+validate against synthetic ground truth before real data` — see almost every wave in `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`), just applied one level up, to the tool that would run the pipelines.

---

## 4. One-line positioning statement

> Tamesis is not a theory that assumes it is right. It is a research system designed to discover where its own theories fail — and `U₁/₂` is the first case where a hypothesis survived the entire funnel: 280 archive records → 19 Phase-0 candidates → 18 eliminated → 1 surviving line → 20+ waves of adversarial attack → exact enumeration → simulation → proof for every `K` → repeated hostile referee review → a closed-form, adversarially-verified result.

This is the sentence the rest of this roadmap is trying to turn into reusable infrastructure.
