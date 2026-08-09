/-
BSD-HYP-MATRIX-001 -- formal guardrail sketch (self-contained, no Mathlib import)

STATUS: BUILT (`lake env lean`, exit 0) by the orchestrating session
during serial integration -- the original parallel draft correctly did
not run `lake build` (five parallel audit fronts share one lake cache;
concurrent builds were explicitly forbidden for this wave, see AGENTS.md
and PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md). Two fixes were needed: a
doc-comment (`/-- ... -/`) directly preceded `section`, which is not a
declaration Lean can attach a doc-comment to -- changed to a plain
comment (`/- ... -/`); `toy_not_universal` used `by decide` on
`¬toyP false`, which failed to synthesize `Decidable` through the
unreduced `def toyP` -- replaced with `simp [toyP] at h`. Still NOT
imported by TamesisLab.lean or registered anywhere.

WHAT THIS IS: this file formalizes, at the level of pure
propositional/predicate logic, the *exact shape* of the fallacy that
BSD-HYP-MATRIX-001's stop_condition forbids committing:

    "tratar produto/uniao de casos cobertos como cobertura universal
     da conjectura"

i.e.: knowing that a conclusion `P` holds on every curve satisfying
hypothesis `H_1`, and on every curve satisfying `H_2`, ..., `H_n`
(a "matrix" of independently-proved conditional theorems, exactly the
shape of KNOWN_RESULTS_MATRIX.md) does NOT, by itself, give
`∀ E, P E` -- unless one *additionally* proves that every curve
satisfies at least one `H_i` (an exhaustiveness lemma). No source
audited in KNOWN_RESULTS_MATRIX.md claims this exhaustiveness; it is
recorded as OPEN in GAP_REGISTER.yaml (BSD-GAP-005).

WHAT THIS IS NOT: this file proves nothing about elliptic curves,
L-functions, Selmer groups, or Sha. `Curve`, `H`, `P` below are opaque
parameters -- the content is purely about the logical shape of the
inference, not about BSD. It does not approach, prove, or approximate
any Millennium Problem. No incomplete proof, no unjustified premise.
-/

namespace BSDHypothesisPartitionGuardrail

section Abstract

variable {Curve : Type} {n : Nat}
variable (H : Fin n → Curve → Prop) (P : Curve → Prop)

/-- What a matrix of independently-proved conditional theorems (in the
shape of KNOWN_RESULTS_MATRIX.md: Gross-Zagier/Kolyvagin, Rubin,
Skinner-Urban, BCS, BSTW, CGS, ...) actually gives: `P` holds on every
curve satisfying *at least one* of the known hypotheses. This is the
honest, provable consequence of a hypothesis-partition matrix. -/
theorem union_of_covered_cases
    (covered : ∀ i : Fin n, ∀ E : Curve, H i E → P E)
    (E : Curve) (h : ∃ i : Fin n, H i E) : P E := by
  obtain ⟨i, hi⟩ := h
  exact covered i E hi

/-- The missing, unestablished step that would be required to upgrade
`union_of_covered_cases` into a universal statement: every curve
satisfies at least one of the known hypotheses. BSD-HYP-MATRIX-001
does not claim this holds; it is recorded as OPEN
(GAP_REGISTER.yaml, BSD-GAP-005). -/
def Exhaustive : Prop := ∀ E : Curve, ∃ i : Fin n, H i E

/-- IF exhaustiveness held, THEN (and only then) the union theorem
upgrades to full universal coverage of `P`. This is a conditional
statement about the logical structure, not a claim that its
antecedent (`Exhaustive H`) is known or true for actual elliptic
curves. -/
theorem exhaustive_union_gives_universal
    (covered : ∀ i : Fin n, ∀ E : Curve, H i E → P E)
    (hex : Exhaustive H) : ∀ E : Curve, P E := by
  intro E
  obtain ⟨i, hi⟩ := hex E
  exact covered i E hi

end Abstract

/- Concrete 2-point counterexample showing `union_of_covered_cases`
does NOT, by itself, extend to `∀ E, P E`: a minimal model
(`Curve := Bool`) where the single known hypothesis is satisfied
exactly by `true`, the covering theorem holds trivially, and yet the
universal conclusion fails for `false`. This is the formal counterpart
of the exact fallacy the legacy document `ANALISE_CRITICA_BSD.md`
performs informally with its `0.99 * 100% + 0.01 * 95% = 99.95%`
arithmetic: treating a union of proper, non-exhaustive subsets of
"known covered cases" as if it summed to (near-)total coverage of the
conjecture. -/
section ConcreteCounterexample

/-- Toy "known hypothesis": satisfied by exactly one of the two model
curves (`true`), mirroring e.g. "rank_an ∈ {0,1}" covering some but not
all curves in KNOWN_RESULTS_MATRIX.md. -/
def toyH : Fin 1 → Bool → Prop := fun _ E => E = true

/-- Toy conclusion predicate ("the BSD rank formula holds for this
curve"), true exactly on the covered curve in this minimal model. -/
def toyP : Bool → Prop := fun E => E = true

/-- The covering theorem holds in this toy model: trivial, since
`toyH` and `toyP` coincide by construction (mirrors: "the theorem for
hypothesis H_i really does prove P on the curves satisfying H_i"). -/
theorem toy_covered : ∀ i : Fin 1, ∀ E : Bool, toyH i E → toyP E := by
  intro _ _ hE
  exact hE

/-- Sanity check: the union theorem instantiates correctly on this toy
model (this is the legitimate, provable consequence of a hypothesis
matrix). -/
example (E : Bool) (h : ∃ i : Fin 1, toyH i E) : toyP E :=
  union_of_covered_cases toyH toyP toy_covered E h

/-- The union of covered cases is NOT universal coverage: `false` is a
curve satisfying no known hypothesis, and indeed `toyP false` fails.
This is the formal shape of the stop_condition this audit was
instructed to respect -- a matrix of covered cases is not, by itself,
a proof or near-proof of the universal conjecture. -/
theorem toy_not_universal : ¬ (∀ E : Bool, toyP E) := by
  intro hcontra
  have h := hcontra false
  simp [toyP] at h

end ConcreteCounterexample

end BSDHypothesisPartitionGuardrail
