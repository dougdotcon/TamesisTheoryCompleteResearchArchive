import TamesisLab.ExternalLines.NonclassicalLogicLP.Definitions

set_option autoImplicit false

/-!
# LP-001 — Meta-theorems that SURVIVE the move from classical logic to LP

Everything in this file is a **positive** result: laws that remain valid
(or remain sound entailments) once the semantics moves from two values to
three. Contrast `Countermodels.lean`, where the same machinery is used to
certify the historically load-bearing **failures**.

Every formula-level theorem below reduces, via the `eval_*` equations
from `Definitions.lean`, to a finite fact about `LPVal` (3 or 9 cases),
each closed by `decide`. The formula-level statements themselves quantify
over an arbitrary atom type and arbitrarily large formulas, so they are
*not* decided directly — only the underlying 3-valued truth-table facts
are.

Reference: Graham Priest, "The Logic of Paradox", *J. Phil. Logic* 8
(1979), 219–241.
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP

open Formula

variable {Atom : Type*}

/-! ## Value-level facts (finite, `decide`-checked) -/

namespace LPVal

theorem or_neg_mem_D (x : LPVal) : or x (neg x) ∈ D := by cases x <;> decide

theorem neg_and_neg_mem_D (x : LPVal) : neg (and x (neg x)) ∈ D := by cases x <;> decide

theorem and_mem_D (x y : LPVal) : x ∈ D → y ∈ D → and x y ∈ D := by
  cases x <;> cases y <;> decide

theorem and_mem_D_left (x y : LPVal) : and x y ∈ D → x ∈ D := by
  cases x <;> cases y <;> decide

theorem and_mem_D_right (x y : LPVal) : and x y ∈ D → y ∈ D := by
  cases x <;> cases y <;> decide

theorem or_mem_D_left (x y : LPVal) : x ∈ D → or x y ∈ D := by
  cases x <;> cases y <;> decide

theorem or_mem_D_right (x y : LPVal) : y ∈ D → or x y ∈ D := by
  cases x <;> cases y <;> decide

/-- Value-level content of the deduction-theorem breakdown: the
CONDITIONAL `x → (¬x → y)` is designated for every `x, y`, regardless of
how "false" `x` or `y` are individually (Priest 1979, §II). Contrast
`Countermodels.deduction_theorem_breakdown`, where the corresponding
INFERENCE fails. -/
theorem imp_neg_imp_mem_D (x y : LPVal) : imp x (imp (neg x) y) ∈ D := by
  cases x <;> cases y <;> decide

end LPVal

/-! ## LP-META-001 — LEM retained -/

/-- **Law of Excluded Middle**: `φ ∨ ¬φ` is valid for every `φ`. LP is
paraconsistent (gluts tolerated) but **not** paracomplete (gaps are not):
this is the theorem that draws that line. -/
theorem lem_valid (φ : Formula Atom) : Valid (φ.or φ.neg) :=
  valid_iff.mpr fun v => LPVal.or_neg_mem_D (eval v φ)

/-! ## LP-META-002 — LNC as a valid schema -/

/-- **Law of Non-Contradiction**, retained as a *valid schema*:
`¬(φ ∧ ¬φ)` is valid for every `φ`. This is compatible with `φ ∧ ¬φ`
itself being *satisfiable* (at `B`) — designatedness of the negated
conjunction and satisfiability of the conjunction are not in tension,
because `B` is designated. LP tolerates the glut without asserting it is
forced, and without giving up the schema. -/
theorem lnc_valid (φ : Formula Atom) : Valid (Formula.neg (φ.and φ.neg)) :=
  valid_iff.mpr fun v => LPVal.neg_and_neg_mem_D (eval v φ)

/-! ## LP-META-003 — negation involution, DNE, DNI -/

theorem eval_neg_neg (v : Atom → LPVal) (φ : Formula Atom) :
    eval v φ.neg.neg = eval v φ := by
  simp [eval_neg, LPVal.neg_neg]

/-- **Double Negation Elimination** as an entailment: `¬¬φ ⊢ φ`. -/
theorem dne_entails (φ : Formula Atom) : Entails [φ.neg.neg] φ := by
  intro v hv
  have h : Sat v φ.neg.neg := hv _ (by simp)
  simp only [Sat, eval_neg_neg] at h
  exact h

/-- **Double Negation Introduction** as an entailment: `φ ⊢ ¬¬φ`. -/
theorem dni_entails (φ : Formula Atom) : Entails [φ] φ.neg.neg := by
  intro v hv
  have h : Sat v φ := hv _ (by simp)
  simp only [Sat, eval_neg_neg]
  exact h

/-! ## LP-META-008 — sanity baseline: adjunction, ∧-elimination, ∨-introduction -/

/-- Adjunction / conjunction-introduction, as an entailment: `φ, ψ ⊢ φ ∧ ψ`. -/
theorem adjunction_valid (φ ψ : Formula Atom) : Entails [φ, ψ] (φ.and ψ) := by
  intro v hv
  have hφ : Sat v φ := hv φ (by simp)
  have hψ : Sat v ψ := hv ψ (by simp)
  exact LPVal.and_mem_D (eval v φ) (eval v ψ) hφ hψ

/-- Conjunction-elimination (left), as an entailment: `φ ∧ ψ ⊢ φ`. -/
theorem and_elim_left (φ ψ : Formula Atom) : Entails [φ.and ψ] φ := by
  intro v hv
  have h : Sat v (φ.and ψ) := hv _ (by simp)
  exact LPVal.and_mem_D_left (eval v φ) (eval v ψ) h

/-- Conjunction-elimination (right), as an entailment: `φ ∧ ψ ⊢ ψ`. -/
theorem and_elim_right (φ ψ : Formula Atom) : Entails [φ.and ψ] ψ := by
  intro v hv
  have h : Sat v (φ.and ψ) := hv _ (by simp)
  exact LPVal.and_mem_D_right (eval v φ) (eval v ψ) h

/-- Disjunction-introduction (left), as an entailment: `φ ⊢ φ ∨ ψ`. -/
theorem or_intro_left (φ ψ : Formula Atom) : Entails [φ] (φ.or ψ) := by
  intro v hv
  have h : Sat v φ := hv _ (by simp)
  exact LPVal.or_mem_D_left (eval v φ) (eval v ψ) h

/-- Disjunction-introduction (right), as an entailment: `ψ ⊢ φ ∨ ψ`. -/
theorem or_intro_right (φ ψ : Formula Atom) : Entails [ψ] (φ.or ψ) := by
  intro v hv
  have h : Sat v ψ := hv _ (by simp)
  exact LPVal.or_mem_D_right (eval v φ) (eval v ψ) h

/-! ## LP-META-007a — the valid half of the deduction-theorem breakdown -/

/-- The **conditional form** of explosion, `φ → (¬φ → ψ)`, is valid for
EVERY `φ, ψ` — no restriction on the atom type, no finite check needed at
the formula level (it follows from the 3-case check
`LPVal.imp_neg_imp_mem_D`). Contrast
`Countermodels.deduction_theorem_breakdown`: the corresponding
**inference** `φ, ¬φ ⊢ ψ` is *not* valid, for a concrete witness. Priest's
point (1979, §II) is exactly this gap: LP validates the conditional but
not the inference the deduction theorem would extract from it. -/
theorem imp_neg_imp_valid (φ ψ : Formula Atom) : Valid (φ.imp (φ.neg.imp ψ)) :=
  valid_iff.mpr fun v => LPVal.imp_neg_imp_mem_D (eval v φ) (eval v ψ)

end TamesisLab.ExternalLines.NonclassicalLogicLP
