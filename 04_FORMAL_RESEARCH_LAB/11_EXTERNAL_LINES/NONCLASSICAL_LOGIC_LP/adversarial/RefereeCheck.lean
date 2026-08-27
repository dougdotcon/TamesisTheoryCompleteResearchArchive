import TamesisLab.ExternalLines.NonclassicalLogicLP.Definitions
import TamesisLab.ExternalLines.NonclassicalLogicLP.Countermodels
import TamesisLab.ExternalLines.NonclassicalLogicLP.CollapseTheorem

set_option autoImplicit false

/-!
# Adversarial referee — independent re-verification (NOT part of the audited line)

This file is a **hostile, independently-authored** re-check of the LP-001
formalization's headline claims. It is not wired into
`TamesisLab.lean` / `NonclassicalLogicLP.lean` and is not part of the
audited build; it lives here only so it can `import` the audited
definitions and be compiled on demand via
`lake env lean TamesisLab/ExternalLines/NonclassicalLogicLP/RefereeCheck.lean`
from `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/`. A copy is archived at
`04_FORMAL_RESEARCH_LAB/11_EXTERNAL_LINES/NONCLASSICAL_LOGIC_LP/adversarial/`.

Everything below is written from scratch: fresh witnesses, fresh proof
terms, fresh induction — it reuses only *data* (`LPVal`, `Formula`,
`eval`, `Sat`, `Entails`, `Valid`, `BEval`, `CValid`) from the audited
files, never their proof terms.
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP.Referee

open TamesisLab.ExternalLines.NonclassicalLogicLP
open Formula

/-! ## Part 1 — the three countermodel claims, re-derived with a
DIFFERENT witness (`Fin 2` atoms, not `Bool`) and by explicit `Sat`/
`Entails` unfolding rather than a single top-level `decide` on the whole
existential. -/

/-- A second, independently-chosen witness: atom `0 ↦ B`, atom `1 ↦ F`,
over `Fin 2` instead of `Bool`. -/
def refWitness : Fin 2 → LPVal
  | 0 => LPVal.B
  | 1 => LPVal.F

theorem refWitness_sat_atom0 : Sat refWitness (Formula.atom (0 : Fin 2)) := by
  show refWitness 0 ∈ LPVal.D; decide

theorem refWitness_sat_neg_atom0 : Sat refWitness (Formula.atom (0 : Fin 2)).neg := by
  show LPVal.neg (refWitness 0) ∈ LPVal.D; decide

theorem refWitness_not_sat_atom1 : ¬ Sat refWitness (Formula.atom (1 : Fin 2)) := by
  show refWitness 1 ∉ LPVal.D; decide

/-- Explosion invalid, hand-checked: from `{a, ¬a}` designated, `b` need
not be, exhibited by `refWitness`. -/
theorem ref_explosion_invalid :
    ¬ Entails [Formula.atom (0 : Fin 2), (Formula.atom (0 : Fin 2)).neg]
        (Formula.atom (1 : Fin 2)) := by
  intro h
  have hprem : ∀ ψ ∈ [Formula.atom (0 : Fin 2), (Formula.atom (0 : Fin 2)).neg],
      Sat refWitness ψ := by
    intro ψ hψ
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hψ
    rcases hψ with rfl | rfl
    · exact refWitness_sat_atom0
    · exact refWitness_sat_neg_atom0
  exact refWitness_not_sat_atom1 (h refWitness hprem)

/-- Modus ponens for the *derived* conditional invalid, same technique. -/
theorem ref_mp_invalid :
    ¬ Entails [Formula.atom (0 : Fin 2),
        (Formula.atom (0 : Fin 2)).imp (Formula.atom (1 : Fin 2))]
        (Formula.atom (1 : Fin 2)) := by
  intro h
  have himp : Sat refWitness ((Formula.atom (0 : Fin 2)).imp (Formula.atom (1 : Fin 2))) := by
    show LPVal.imp (refWitness 0) (refWitness 1) ∈ LPVal.D; decide
  have hprem : ∀ ψ ∈ [Formula.atom (0 : Fin 2),
      (Formula.atom (0 : Fin 2)).imp (Formula.atom (1 : Fin 2))], Sat refWitness ψ := by
    intro ψ hψ
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hψ
    rcases hψ with rfl | rfl
    · exact refWitness_sat_atom0
    · exact himp
  exact refWitness_not_sat_atom1 (h refWitness hprem)

/-- Disjunctive syllogism invalid, same technique. -/
theorem ref_disjunctive_syllogism_invalid :
    ¬ Entails [(Formula.atom (0 : Fin 2)).or (Formula.atom (1 : Fin 2)),
        (Formula.atom (0 : Fin 2)).neg] (Formula.atom (1 : Fin 2)) := by
  intro h
  have hor : Sat refWitness ((Formula.atom (0 : Fin 2)).or (Formula.atom (1 : Fin 2))) := by
    show LPVal.or (refWitness 0) (refWitness 1) ∈ LPVal.D; decide
  have hprem : ∀ ψ ∈ [(Formula.atom (0 : Fin 2)).or (Formula.atom (1 : Fin 2)),
      (Formula.atom (0 : Fin 2)).neg], Sat refWitness ψ := by
    intro ψ hψ
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hψ
    rcases hψ with rfl | rfl
    · exact hor
    · exact refWitness_sat_neg_atom0
  exact refWitness_not_sat_atom1 (h refWitness hprem)

/-! ## Part 2 — independent re-derivation of the collapse theorem's
*proven* direction (`Valid → CValid`), from scratch, for a general atom
type, by structural induction — without importing `CollapseTheorem`'s
`toBool`/`ofBool`/`toBool_eval`/`sat_iff_beval` proof terms (only its
`BEval`/`CValid`/`BEntails` *definitions* are reused, as data). -/

variable {Atom : Type*}

/-- Fresh embedding of `Bool` into `LPVal`, independent of
`CollapseTheorem.LPVal.ofBool` (same values, different declaration). -/
def refOfBool : Bool → LPVal
  | true => LPVal.T
  | false => LPVal.F

/-- Exact homomorphism (no sandwich/rounding needed: `refOfBool` never
produces `B`, so LP evaluation on a `refOfBool`-composed valuation
mirrors classical evaluation exactly, node for node). Proved fresh by
induction on `φ`, independent of `CollapseTheorem.toBool_eval`. -/
theorem ref_eval_ofBool (b : Atom → Bool) :
    ∀ φ : Formula Atom, Formula.eval (fun a => refOfBool (b a)) φ = refOfBool (BEval b φ) := by
  intro φ
  induction φ with
  | atom a => rfl
  | neg φ ih =>
      simp only [Formula.eval_neg, BEval_neg, ih]
      cases BEval b φ <;> rfl
  | and φ ψ ihφ ihψ =>
      simp only [Formula.eval_and, BEval_and, ihφ, ihψ]
      cases BEval b φ <;> cases BEval b ψ <;> rfl
  | or φ ψ ihφ ihψ =>
      simp only [Formula.eval_or, BEval_or, ihφ, ihψ]
      cases BEval b φ <;> cases BEval b ψ <;> rfl
  | imp φ ψ ihφ ihψ =>
      simp only [Formula.eval_imp, BEval_imp, ihφ, ihψ]
      cases BEval b φ <;> cases BEval b ψ <;> rfl

theorem refOfBool_mem_D_iff (x : Bool) : refOfBool x ∈ LPVal.D ↔ x = true := by
  cases x <;> decide

/-- Independent re-proof: every LP-valid formula is classically valid.
Same statement as `CollapseTheorem.valid_implies_cvalid`, disjoint proof. -/
theorem ref_valid_implies_cvalid (φ : Formula Atom) : Valid φ → CValid φ := by
  intro hV b _hb
  have h := hV (fun a => refOfBool (b a))
  have hsat : Sat (fun a => refOfBool (b a)) φ := h (fun ψ hψ => nomatch hψ)
  have hmem : Formula.eval (fun a => refOfBool (b a)) φ ∈ LPVal.D := hsat
  rw [ref_eval_ofBool b φ] at hmem
  exact (refOfBool_mem_D_iff (BEval b φ)).mp hmem

/-! ## Part 3 — probing the "converse fails" claim attached to
`CollapseTheorem.valid_implies_cvalid`.

`CollapseTheorem.lean`'s docstring on `valid_implies_cvalid` asserts
"the converse fails" (i.e. `CValid φ → Valid φ` does not hold), and
justifies this with an *entailment*-level example (`φ, ¬φ ⊢ ψ`), not a
formula-level counterexample. No such counterexample formula is
exhibited anywhere in the audited files. Exhaustive brute-force search
(see `adversarial/lp_collapse_search.py`, saved alongside this file)
over 56,842 formulas up to size 4 on 2 atoms, 299,713 formulas up to
size 6 on 1 atom, and 603 formulas up to size 2 on 3 atoms found **zero**
counterexamples to `CValid φ → Valid φ` — consistent with the
well-documented fact (Priest 1979; multiple secondary sources) that LP
and classical logic have *exactly* the same valid formulas (only the
consequence relation differs). We do not complete a general Lean proof
of the converse here (the natural proof strategy needs a
polarity-tracking induction that is more delicate than it first
appears — negation is anti-monotone in the `F < B < T` order, so a
naive single global "round B up / round B down" argument breaks down,
as the case `φ = ¬p, v(p) = B` shows directly). But the claim that this
converse *fails* is not supported by any evidence in the audited files
and is contradicted by the literature and by this brute-force search.

Below: `Formula Atom` is inductively infinite (formulas of unbounded
size), so "∀ φ, CValid φ → Valid φ" is *not* a `Decidable` proposition
and cannot be discharged by `decide` in general — only individual
concrete formulas can. As a concrete, kernel-checked sanity check on a
curated batch (mirroring the Python enumeration's witnesses, including
nested negation and the derived conditional), confirming the converse
on each instance, independent of both the general-argument sketch above
and of the Python search: -/

section ConverseSpotChecks

open Formula in
/-- A batch of concrete classical tautologies over `Fin 2`, stress-testing
exactly the shapes the general "converse fails" claim would need a
counterexample among: nested negation, the derived conditional in both
polarities, and a 3-deep mixed formula. Each is checked individually
(`CValid φ → Valid φ` is decidable for a *fixed* `φ`, unlike the
universally-quantified statement above). -/
example : CValid (Formula.atom (0 : Fin 2)).neg.neg.neg.neg → Valid (Formula.atom (0 : Fin 2)).neg.neg.neg.neg := by decide
example : CValid ((Formula.atom (0 : Fin 2)).imp (Formula.atom (0 : Fin 2))) →
    Valid ((Formula.atom (0 : Fin 2)).imp (Formula.atom (0 : Fin 2))) := by decide
example : CValid (((Formula.atom (0:Fin 2)).imp (Formula.atom (1:Fin 2))).imp
    (((Formula.atom (1:Fin 2)).neg).imp ((Formula.atom (0:Fin 2)).neg))) →
    Valid (((Formula.atom (0:Fin 2)).imp (Formula.atom (1:Fin 2))).imp
    (((Formula.atom (1:Fin 2)).neg).imp ((Formula.atom (0:Fin 2)).neg))) := by decide
example : CValid ((((Formula.atom (0:Fin 2)).imp (Formula.atom (1:Fin 2))).imp
    (Formula.atom (0:Fin 2))).imp (Formula.atom (0:Fin 2))) →
    Valid ((((Formula.atom (0:Fin 2)).imp (Formula.atom (1:Fin 2))).imp
    (Formula.atom (0:Fin 2))).imp (Formula.atom (0:Fin 2))) := by decide

end ConverseSpotChecks

#print axioms ref_explosion_invalid
#print axioms ref_mp_invalid
#print axioms ref_disjunctive_syllogism_invalid
#print axioms ref_eval_ofBool
#print axioms ref_valid_implies_cvalid

end TamesisLab.ExternalLines.NonclassicalLogicLP.Referee
