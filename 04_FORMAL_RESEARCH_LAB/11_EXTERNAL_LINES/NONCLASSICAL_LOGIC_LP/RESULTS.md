# LP-001 — Results

See `README.md` for the scope note (`DISC-DEC-102`,
`PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md` §3.1) and why the physical
`.lean` files live under `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/
ExternalLines/NonclassicalLogicLP/` rather than in this directory.

## Files and line counts

| File | Lines | Content |
|---|---:|---|
| `Definitions.lean` | 195 | `LPVal`, order `F<B<T`, `neg`/`and`/`or`, derived `imp`, `D`, `Formula`, `eval`, `Sat`, `Entails`, `Valid`, decidability instances |
| `ValidTheorems.lean` | 148 | LEM, LNC-as-schema, DNE/DNI, adjunction, ∧-elim, ∨-intro, the valid half of the deduction-theorem breakdown |
| `Countermodels.lean` | 115 | The shared witness `a↦B, b↦F`; explosion / MP / disjunctive-syllogism invalidity; the deduction-theorem breakdown, both halves together |
| `CollapseTheorem.lean` | 231 | Classical `BEval`/`BEntails`/`CValid`, `Boolean` valuations, `BooleanEntails`, the collapse `iff`, the one-direction corollary |
| `Audit.lean` | 164 | 30-cell truth-table cross-check vs. Priest 1979 / SEP, `#check` registry, `#print axioms` on every headline result |
| `NonclassicalLogicLP.lean` (aggregator, one level up) | 23 | Top-level import shim + smoke theorem |
| **Total** | **876** | **6 files** |

Pre-registered estimate (`DISC-DEC-102`) was 450–700 lines across 6–8
files. The actual count is **876 lines, 6 files** — about 25% over the
top of the line estimate, file count within range. Reported honestly
rather than trimmed to fit: the overshoot is concentrated in
`CollapseTheorem.lean` (the formula-level homomorphism proof by
structural recursion, `eval_ne_B`/`toBool_eval`, needs one case per
connective × two lemmas ≈ 40 lines that a purely `decide`-based approach
could not have produced, since `Formula Atom` is not finite) and in
`Audit.lean`'s exhaustive 30-cell table (9+9+9+3 `example`s) plus the
`#check`/`#print axioms` registry, which follows this lab's own
`FunctionalGraphs/Audit.lean` house style verbatim. No file was padded;
every line is a proof, a table cell, a check, or documentation carrying
a citation or an explanation of why a step is shaped the way it is.

## Build

```
$ cd 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean
$ lake build
...
✔ [8830/8831] Built TamesisLab (167s)
Build completed successfully (8831 jobs).
```

Full-project `lake build` (whole `TamesisLab` library, 8831 jobs,
includes every pre-existing subsystem plus this one), run after wiring
`import TamesisLab.ExternalLines.NonclassicalLogicLP` into the root
`TamesisLab.lean` shim (the one line touched in a file this lab already
owns — see `README.md`). **Zero errors.** Each new file was also built
individually and cumulatively while under development
(`lake build TamesisLab.ExternalLines.NonclassicalLogicLP.<Name>`), all
green, before the final whole-project build.

Toolchain: `leanprover/lean4:v4.33.0-rc1` (`lean-toolchain`), Mathlib
`v4.33.0-rc1` (`lakefile.toml`), matching the toolchain already installed
for the rest of this lab — no version pin was changed.

## `sorry` / `admit` / `native_decide` audit

```
$ grep -rniE "sorry|admit|native_decide" \
    04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/ExternalLines/
(no output)
```

Zero hits across all 6 files. Every theorem is closed by a genuine
proof term — structural recursion, `decide` over `LPVal`'s 3-element
finite domain (and, in `Countermodels.lean`, over the finite `Bool → LPVal`
valuation space, 9 elements), or ordinary tactic proof. No
`native_decide` is used anywhere (native code execution is never trusted
as a proof step here — every `decide` goes through the Lean kernel's own
reduction).

## Axiom footprint (`#print axioms`)

Run via `Audit.lean`'s `#print axioms` block, `lake build
TamesisLab.ExternalLines.NonclassicalLogicLP.Audit`, info-level output
captured directly from the build log:

| Theorem | Axioms |
|---|---|
| `lem_valid` | `[propext, Classical.choice, Quot.sound]` |
| `lnc_valid` | `[propext, Classical.choice, Quot.sound]` |
| `dne_entails` | `[propext, Classical.choice, Quot.sound]` |
| `dni_entails` | `[propext, Classical.choice, Quot.sound]` |
| `adjunction_valid` | `[propext, Classical.choice, Quot.sound]` |
| `and_elim_left` / `and_elim_right` | `[propext, Classical.choice, Quot.sound]` |
| `or_intro_left` / `or_intro_right` | `[propext, Classical.choice, Quot.sound]` |
| `imp_neg_imp_valid` | `[propext, Classical.choice, Quot.sound]` |
| `explosion_invalid` | `[propext, Classical.choice, Quot.sound]` |
| `mp_invalid` | `[propext, Classical.choice, Quot.sound]` |
| `disjunctive_syllogism_invalid` | `[propext, Classical.choice, Quot.sound]` |
| `deduction_theorem_breakdown` | `[propext, Classical.choice, Quot.sound]` |
| `collapse` | `[propext, Classical.choice, Quot.sound]` |
| `valid_implies_cvalid` | `[propext, Classical.choice, Quot.sound]` |

Every headline theorem — including the four the task singled out (LEM,
explosion-invalidity, MP-invalidity, the collapse theorem) — depends on
exactly the closed Lean/Mathlib standard set
`[propext, Classical.choice, Quot.sound]`, and **nothing beyond it**. No
`sorryAx`. This is the expected Mathlib-idiomatic footprint: the concrete
`decide`-based facts are computationally axiom-free in themselves, but
they are elaborated inside generic Mathlib `Fintype`/`Finset`/order
machinery whose own library proofs use `propext`/`Classical.choice`/
`Quot.sound` upstream (`Finset`/`Multiset` are quotient types;
`LinearOrder.lift'`'s generic transfer lemmas use `propext`) — exactly
the same footprint every other verified theorem in this lab's
`02_FOUNDATIONS/` carries (cross-checked against `EllipticHeight.lean`,
`SobolevSpace.lean`, `SpectralCounting.lean` in the same build log: all
identical `[propext, Classical.choice, Quot.sound]`).

## Meta-theorem checklist (spec → theorem)

| # | Requirement (task spec) | Theorem | File |
|---|---|---|---|
| 1 | LEM valid | `lem_valid` | `ValidTheorems.lean` |
| 2 | LNC valid as a schema | `lnc_valid` | `ValidTheorems.lean` |
| 3 | Negation involution; DNE/DNI valid | `LPVal.neg_neg`, `dne_entails`, `dni_entails` | `Definitions.lean`, `ValidTheorems.lean` |
| 4 | Explosion invalid, `a↦B,b↦F` witness, `decide`-checkable | `explosion_invalid` | `Countermodels.lean` |
| 5 | Modus Ponens invalid, same countermodel | `mp_invalid` | `Countermodels.lean` |
| 6 | Disjunctive syllogism invalid, same countermodel | `disjunctive_syllogism_invalid` | `Countermodels.lean` |
| 7 | Deduction-theorem breakdown, both halves in one theorem | `deduction_theorem_breakdown` | `Countermodels.lean` (uses `imp_neg_imp_valid` from `ValidTheorems.lean`) |
| 8 | Adjunction, ∧-elim, ∨-intro (sanity baseline) | `adjunction_valid`, `and_elim_left`/`right`, `or_intro_left`/`right` | `ValidTheorems.lean` |
| 9 | Classical-recapture/collapse theorem under B-free valuations | `collapse` (`BooleanEntails Γ φ ↔ BEntails Γ φ`) | `CollapseTheorem.lean` |
| 10 | Decidability instances for `Sat`/`Entails`/`Valid` | `Formula.Sat.decidable`, `Formula.Entails.decidable`, `Formula.Valid.decidable` (and the classical mirrors `BEntails.decidable`, `CValid.decidable`) | `Definitions.lean`, `CollapseTheorem.lean` |
| 11 | LP-valid ⟹ classically valid (cheap corollary) | `valid_implies_cvalid` | `CollapseTheorem.lean` |

All 11 numbered items delivered; item 3 counted as one line since
involution and DNE/DNI share a single short block. The specified
formula grammar (`atom`/`neg`/`and`/`or`/`imp`, `imp` its own
constructor rather than notation) and semantics (`eval`/`Sat`/`Entails`/
`Valid` exactly as specified) match `Definitions.lean` verbatim.

## Truth-table conformance (Audit.lean)

All 3 (¬) + 9 (∧) + 9 (∨) + 9 (derived →) = 30 cells checked individually
by `decide` against Priest (1979), Table for LP (also reproduced in the
SEP "Paraconsistent Logic" entry, §3), plus a closing fact that the full
∧/∨ tables coincide with `min`/`max` under `F < B < T` — all cells,
both directions, not sampled.

## What was deliberately not touched

* `04_FORMAL_RESEARCH_LAB/00_GOVERNANCE/` — untouched.
* `04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/` — untouched (`RESEARCH_QUEUE.yaml`,
  `DECISION_LEDGER.yaml` of this lab not edited; this line is tracked only
  in `05_DISCOVERY_LAB`, per `DISC-DEC-102`).
* No adversarial self-review was run here by design — a separate hostile
  referee pass is expected as a follow-up, per the calling session's
  instructions.

## Revisão adversarial (`DISC-DEC-105`, 2026-08-27)

Referee hostil dedicado, agente separado: re-derivou os 12 metateoremas
independentemente contra Priest (1979)/SEP, checou cada enunciado de
teorema à mão (não apenas que compila), verificou os três testemunhos
de invalidade e o `iff` de colapso por conta própria, e reconstruiu a
prova numa nova instância Lean do zero. Veredito **SOUND WITH NAMED
ISSUES** — 1 achado MODERADO (não 0): o docstring de
`valid_implies_cvalid` em `CollapseTheorem.lean` afirmava, sem sustentação,
que "a recíproca falha" — achado real de documentação (não de prova),
já corrigido no próprio arquivo por adendo datado (ver
`CollapseTheorem.lean`). Nenhum dos 12 teoremas provados, nenhum
testemunho de contramodelo, nem o `iff` de colapso foram invalidados.
Relatório completo em `adversarial/REFEREE_REPORT.md`.
