import Mathlib.Order.Basic
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Finset.Insert

set_option autoImplicit false

/-!
# LP-001 — Priest's Logic of Paradox: values, connectives, formulas, semantics

This is a **new, standalone** Lean4 formalization of Priest's LP (Logic of
Paradox), the classic 3-valued paraconsistent logic. It is tracked under
`05_DISCOVERY_LAB` (`DISC-DEC-102`), not under this lab's own portfolio
gate — see `04_FORMAL_RESEARCH_LAB/11_EXTERNAL_LINES/NONCLASSICAL_LOGIC_LP/
README.md` for the scope note. The physical `.lean` files live here only
because `lake`'s module resolution requires source under the package's
existing `TamesisLab/` tree; this is infrastructure reuse, not a claim on
`02_FOUNDATIONS/`'s numbered track.

## Content of this file

* `LPVal` — the three truth values `{T, B, F}` with `F < B < T`.
* Connectives on `LPVal`: `neg` (involution), `and` (min), `or` (max),
  and the **derived** material conditional `imp a b := (neg a).or b`.
* `Formula Atom` — propositional formulas, with `imp` its own constructor
  (not unfolded notation) so conditional-specific failures (§ Countermodels)
  are visible at the formula level.
* `eval`, `Sat`, `Entails`, `Valid` — the homomorphic semantics and the
  associated satisfaction/entailment/validity notions.
* Decidability instances making `Sat`/`Entails`/`Valid` `decide`-checkable
  on any finite atom set.

## References

* Graham Priest, "The Logic of Paradox", *Journal of Philosophical Logic*
  8 (1979), 219–241. (Truth tables: neg/and/or as below; `D = {T, B}`.)
* Stanford Encyclopedia of Philosophy, "Paraconsistent Logic"
  (https://plato.stanford.edu/entries/logic-paraconsistent/), §3 (LP).
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP

/-- The three truth values of Priest's LP: **T**rue only, **B**oth
(true and false — the paradoxical/glutty value), **F**alse only.
Ordered `F < B < T` ("degree of truth"). -/
inductive LPVal where
  | F
  | B
  | T
  deriving DecidableEq, Repr

namespace LPVal

instance : Fintype LPVal where
  elems := {F, B, T}
  complete := fun x => by cases x <;> decide

/-- Embedding into `Fin 3` used solely to install the linear order
`F < B < T` via `LinearOrder.lift'`. Not used anywhere else: `neg`/`and`/
`or` below are independent, explicit truth tables, and their agreement
with `min`/`max` under this order is *proved* (`and_eq_min`, `or_eq_max`),
not assumed. -/
def rank : LPVal → Fin 3
  | F => 0
  | B => 1
  | T => 2

theorem rank_injective : Function.Injective rank := by decide

instance : LinearOrder LPVal := LinearOrder.lift' rank rank_injective

@[simp] theorem F_lt_B : F < B := by decide
@[simp] theorem B_lt_T : B < T := by decide
@[simp] theorem F_lt_T : F < T := by decide

theorem F_le (x : LPVal) : F ≤ x := by cases x <;> decide
theorem le_T (x : LPVal) : x ≤ T := by cases x <;> decide

/-- Negation: swaps `T` and `F`, fixes `B`. An involution
(`neg_neg` below): this is exactly what makes DNE/DNI hold in LP even
though other classical laws break. -/
def neg : LPVal → LPVal
  | T => F
  | B => B
  | F => T

/-- Conjunction, as an explicit 3×3 truth table (Priest 1979, the LP
table for `∧`). Equal to `min` under `F < B < T` — proved as
`and_eq_min`, not definitional. -/
def and : LPVal → LPVal → LPVal
  | T, T => T | T, B => B | T, F => F
  | B, T => B | B, B => B | B, F => F
  | F, T => F | F, B => F | F, F => F

/-- Disjunction, as an explicit 3×3 truth table (Priest 1979, the LP
table for `∨`). Equal to `max` under `F < B < T` — proved as
`or_eq_max`, not definitional. -/
def or : LPVal → LPVal → LPVal
  | T, _ => T
  | B, T => T | B, B => B | B, F => B
  | F, T => T | F, B => B | F, F => F

/-- The material conditional is **derived**, not primitive:
`a → b := ¬a ∨ b`. This is the classical definition transplanted
verbatim into LP — and it is exactly this transplant that fails to
support Modus Ponens (`Countermodels.mp_invalid`). -/
def imp (a b : LPVal) : LPVal := (neg a).or b

/-- Designated values: `{T, B}`, the values counted as "holding". A
formula gets to keep an inference license iff its value lands here. -/
def D : Finset LPVal := {T, B}

@[simp] theorem T_mem_D : T ∈ D := by decide
@[simp] theorem B_mem_D : B ∈ D := by decide
@[simp] theorem F_not_mem_D : F ∉ D := by decide

theorem mem_D_iff {x : LPVal} : x ∈ D ↔ x = T ∨ x = B := by
  cases x <;> decide

@[simp] theorem neg_neg (x : LPVal) : neg (neg x) = x := by cases x <;> rfl

theorem and_eq_min (x y : LPVal) : and x y = min x y := by
  cases x <;> cases y <;> decide

theorem or_eq_max (x y : LPVal) : or x y = max x y := by
  cases x <;> cases y <;> decide

end LPVal

/-- Propositional formulas over an atom type `Atom`. `imp` is kept as its
**own constructor** (not desugared to `neg φ |>.or ψ` at the formula
level) precisely so its failures — Modus Ponens, the deduction theorem —
are visible as failures of formulas built with `Formula.imp`, not merely
of a derived abbreviation. -/
inductive Formula (Atom : Type*) where
  | atom : Atom → Formula Atom
  | neg : Formula Atom → Formula Atom
  | and : Formula Atom → Formula Atom → Formula Atom
  | or : Formula Atom → Formula Atom → Formula Atom
  | imp : Formula Atom → Formula Atom → Formula Atom
  deriving DecidableEq

namespace Formula

variable {Atom : Type*}

/-- Homomorphic evaluation: `eval v` extends a valuation `v : Atom → LPVal`
to all formulas, `imp` going through the *derived* `LPVal.imp`. -/
def eval (v : Atom → LPVal) : Formula Atom → LPVal
  | atom a => v a
  | neg φ => LPVal.neg (eval v φ)
  | and φ ψ => LPVal.and (eval v φ) (eval v ψ)
  | or φ ψ => LPVal.or (eval v φ) (eval v ψ)
  | imp φ ψ => LPVal.imp (eval v φ) (eval v ψ)

@[simp] theorem eval_atom (v : Atom → LPVal) (a : Atom) : eval v (atom a) = v a := rfl
@[simp] theorem eval_neg (v : Atom → LPVal) (φ : Formula Atom) :
    eval v (neg φ) = LPVal.neg (eval v φ) := rfl
@[simp] theorem eval_and (v : Atom → LPVal) (φ ψ : Formula Atom) :
    eval v (and φ ψ) = LPVal.and (eval v φ) (eval v ψ) := rfl
@[simp] theorem eval_or (v : Atom → LPVal) (φ ψ : Formula Atom) :
    eval v (or φ ψ) = LPVal.or (eval v φ) (eval v ψ) := rfl
@[simp] theorem eval_imp (v : Atom → LPVal) (φ ψ : Formula Atom) :
    eval v (imp φ ψ) = LPVal.imp (eval v φ) (eval v ψ) := rfl

/-- `φ` is satisfied by `v` iff `eval v φ` is designated. -/
def Sat (v : Atom → LPVal) (φ : Formula Atom) : Prop := eval v φ ∈ LPVal.D

instance Sat.decidable (v : Atom → LPVal) (φ : Formula Atom) : Decidable (Sat v φ) :=
  inferInstanceAs (Decidable (eval v φ ∈ LPVal.D))

theorem sat_iff {v : Atom → LPVal} {φ : Formula Atom} :
    Sat v φ ↔ eval v φ = LPVal.T ∨ eval v φ = LPVal.B := LPVal.mem_D_iff

/-- `Γ` LP-entails `φ` iff every valuation satisfying every premise in
`Γ` also satisfies `φ`. -/
def Entails (Γ : List (Formula Atom)) (φ : Formula Atom) : Prop :=
  ∀ v : Atom → LPVal, (∀ ψ ∈ Γ, Sat v ψ) → Sat v φ

instance Entails.decidable [Fintype Atom] [DecidableEq Atom]
    (Γ : List (Formula Atom)) (φ : Formula Atom) : Decidable (Entails Γ φ) :=
  inferInstanceAs (Decidable (∀ v : Atom → LPVal, (∀ ψ ∈ Γ, Sat v ψ) → Sat v φ))

/-- `φ` is LP-valid iff it is entailed by the empty premise set, i.e.
designated under **every** valuation. -/
def Valid (φ : Formula Atom) : Prop := Entails ([] : List (Formula Atom)) φ

instance Valid.decidable [Fintype Atom] [DecidableEq Atom] (φ : Formula Atom) :
    Decidable (Valid φ) := inferInstanceAs (Decidable (Entails ([] : List (Formula Atom)) φ))

theorem valid_iff {φ : Formula Atom} : Valid φ ↔ ∀ v : Atom → LPVal, Sat v φ :=
  ⟨fun h v => h v (by simp), fun h v _ => h v⟩

end Formula

end TamesisLab.ExternalLines.NonclassicalLogicLP
