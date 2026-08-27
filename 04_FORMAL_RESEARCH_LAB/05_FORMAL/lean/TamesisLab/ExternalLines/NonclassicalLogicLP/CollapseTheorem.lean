import TamesisLab.ExternalLines.NonclassicalLogicLP.Definitions

set_option autoImplicit false

/-!
# LP-001 — Classical recapture: LP is a conservative generalization of CPL

Unrestricted LP entailment does **not** coincide with classical (CPL)
entailment: that is exactly the content of `Countermodels.explosion_invalid`
and friends. What *does* coincide is LP entailment **restricted to
`B`-free ("Boolean") valuations** — valuations that never assign the
glut value to an atom. This file proves that restricted coincidence
(`collapse`) and draws the cheap one-directional corollary
(`valid_implies_cvalid`): every LP-valid formula is classically valid.

This is the formal content of "LP is a conservative, non-explosive
generalization of classical logic" (Priest 1979, §III; SEP "Paraconsistent
Logic" §3).
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP

open Formula

variable {Atom : Type*}

/-! ## Classical (2-valued) semantics, for comparison -/

/-- Classical Boolean evaluation of the *same* formula language `Formula
Atom`, with `imp` the usual material conditional. -/
def BEval (b : Atom → Bool) : Formula Atom → Bool
  | .atom a => b a
  | .neg φ => !(BEval b φ)
  | .and φ ψ => BEval b φ && BEval b ψ
  | .or φ ψ => BEval b φ || BEval b ψ
  | .imp φ ψ => !(BEval b φ) || BEval b ψ

@[simp] theorem BEval_atom (b : Atom → Bool) (a : Atom) : BEval b (.atom a) = b a := rfl
@[simp] theorem BEval_neg (b : Atom → Bool) (φ : Formula Atom) :
    BEval b (.neg φ) = !(BEval b φ) := rfl
@[simp] theorem BEval_and (b : Atom → Bool) (φ ψ : Formula Atom) :
    BEval b (.and φ ψ) = (BEval b φ && BEval b ψ) := rfl
@[simp] theorem BEval_or (b : Atom → Bool) (φ ψ : Formula Atom) :
    BEval b (.or φ ψ) = (BEval b φ || BEval b ψ) := rfl
@[simp] theorem BEval_imp (b : Atom → Bool) (φ ψ : Formula Atom) :
    BEval b (.imp φ ψ) = (!(BEval b φ) || BEval b ψ) := rfl

/-- Classical entailment: every classical (2-valued) valuation satisfying
`Γ` satisfies `φ`. -/
def BEntails (Γ : List (Formula Atom)) (φ : Formula Atom) : Prop :=
  ∀ b : Atom → Bool, (∀ ψ ∈ Γ, BEval b ψ = true) → BEval b φ = true

/-- Classical validity (tautology-hood). -/
def CValid (φ : Formula Atom) : Prop := BEntails ([] : List (Formula Atom)) φ

instance BEntails.decidable [Fintype Atom] [DecidableEq Atom]
    (Γ : List (Formula Atom)) (φ : Formula Atom) : Decidable (BEntails Γ φ) :=
  inferInstanceAs
    (Decidable (∀ b : Atom → Bool, (∀ ψ ∈ Γ, BEval b ψ = true) → BEval b φ = true))

instance CValid.decidable [Fintype Atom] [DecidableEq Atom] (φ : Formula Atom) :
    Decidable (CValid φ) := inferInstanceAs (Decidable (BEntails ([] : List (Formula Atom)) φ))

/-! ## `B`-free ("Boolean") LP valuations -/

/-- A valuation is *Boolean* iff it never assigns the glut value `B` to
an atom — the restriction under which LP degenerates to CPL. -/
def Boolean (v : Atom → LPVal) : Prop := ∀ a, v a ≠ LPVal.B

/-- LP-entailment restricted to Boolean valuations. This is deliberately
**not** `Entails` itself: over *all* valuations LP entailment does not
coincide with classical entailment (paraconsistency). Restricting the
quantifier to `Boolean` valuations is exactly what recovers the
classical notion — that is the content of `collapse` below. -/
def BooleanEntails (Γ : List (Formula Atom)) (φ : Formula Atom) : Prop :=
  ∀ v : Atom → LPVal, Boolean v → (∀ ψ ∈ Γ, Sat v ψ) → Sat v φ

/-! ## The value-level correspondence -/

namespace LPVal

/-- The two-valued reading of a non-glut LP value (`B` is mapped to
`true` only so the function is total; it is never applied to `B` in any
proof below, guarded throughout by `≠ B` hypotheses coming from
`Boolean`). -/
def toBool : LPVal → Bool
  | T => true
  | B => true
  | F => false

/-- The LP reading of a classical value. -/
def ofBool : Bool → LPVal
  | true => T
  | false => F

theorem ofBool_ne_B (b : Bool) : ofBool b ≠ B := by cases b <;> decide

theorem toBool_ofBool (b : Bool) : toBool (ofBool b) = b := by cases b <;> decide

theorem toBool_eq_true_iff (x : LPVal) : x ≠ B → (toBool x = true ↔ x = T) := by
  cases x <;> decide

/-- On non-`B` values LP negation matches classical negation
(Priest 1979, §III — the "collapse" behind classical recapture). -/
theorem toBool_neg (x : LPVal) : x ≠ B → toBool (neg x) = !(toBool x) := by
  cases x <;> decide

theorem toBool_and (x y : LPVal) :
    x ≠ B → y ≠ B → toBool (and x y) = (toBool x && toBool y) := by
  cases x <;> cases y <;> decide

theorem toBool_or (x y : LPVal) :
    x ≠ B → y ≠ B → toBool (or x y) = (toBool x || toBool y) := by
  cases x <;> cases y <;> decide

theorem toBool_imp (x y : LPVal) :
    x ≠ B → y ≠ B → toBool (imp x y) = (!(toBool x) || toBool y) := by
  cases x <;> cases y <;> decide

theorem neg_ne_B (x : LPVal) : x ≠ B → neg x ≠ B := by cases x <;> decide

theorem and_ne_B (x y : LPVal) : x ≠ B → y ≠ B → and x y ≠ B := by
  cases x <;> cases y <;> decide

theorem or_ne_B (x y : LPVal) : x ≠ B → y ≠ B → or x y ≠ B := by
  cases x <;> cases y <;> decide

theorem imp_ne_B (x y : LPVal) : x ≠ B → y ≠ B → imp x y ≠ B := by
  cases x <;> cases y <;> decide

end LPVal

/-! ## Formula-level lifting, by structural recursion on `φ` -/

/-- Under a Boolean valuation, no formula evaluates to the glut `B`. -/
theorem eval_ne_B {v : Atom → LPVal} (hv : Boolean v) :
    ∀ φ : Formula Atom, eval v φ ≠ LPVal.B
  | .atom a => hv a
  | .neg φ => by simpa [eval_neg] using LPVal.neg_ne_B _ (eval_ne_B hv φ)
  | .and φ ψ => by
      simpa [eval_and] using LPVal.and_ne_B _ _ (eval_ne_B hv φ) (eval_ne_B hv ψ)
  | .or φ ψ => by
      simpa [eval_or] using LPVal.or_ne_B _ _ (eval_ne_B hv φ) (eval_ne_B hv ψ)
  | .imp φ ψ => by
      simpa [eval_imp] using LPVal.imp_ne_B _ _ (eval_ne_B hv φ) (eval_ne_B hv ψ)

/-- Under a Boolean valuation, LP evaluation and classical evaluation
agree once read through `LPVal.toBool` — the homomorphism at the heart
of classical recapture. -/
theorem toBool_eval {v : Atom → LPVal} (hv : Boolean v) :
    ∀ φ : Formula Atom, LPVal.toBool (eval v φ) = BEval (fun a => LPVal.toBool (v a)) φ
  | .atom _ => rfl
  | .neg φ => by
      have ih := toBool_eval hv φ
      simp only [eval_neg, BEval_neg]
      rw [LPVal.toBool_neg _ (eval_ne_B hv φ), ih]
  | .and φ ψ => by
      have ihφ := toBool_eval hv φ
      have ihψ := toBool_eval hv ψ
      simp only [eval_and, BEval_and]
      rw [LPVal.toBool_and _ _ (eval_ne_B hv φ) (eval_ne_B hv ψ), ihφ, ihψ]
  | .or φ ψ => by
      have ihφ := toBool_eval hv φ
      have ihψ := toBool_eval hv ψ
      simp only [eval_or, BEval_or]
      rw [LPVal.toBool_or _ _ (eval_ne_B hv φ) (eval_ne_B hv ψ), ihφ, ihψ]
  | .imp φ ψ => by
      have ihφ := toBool_eval hv φ
      have ihψ := toBool_eval hv ψ
      simp only [eval_imp, BEval_imp]
      rw [LPVal.toBool_imp _ _ (eval_ne_B hv φ) (eval_ne_B hv ψ), ihφ, ihψ]

theorem sat_iff_eq_T {v : Atom → LPVal} (hv : Boolean v) (φ : Formula Atom) :
    Sat v φ ↔ eval v φ = LPVal.T := by
  rw [sat_iff]
  constructor
  · rintro (h | h)
    · exact h
    · exact absurd h (eval_ne_B hv φ)
  · exact Or.inl

theorem sat_iff_beval {v : Atom → LPVal} (hv : Boolean v) (φ : Formula Atom) :
    Sat v φ ↔ BEval (fun a => LPVal.toBool (v a)) φ = true := by
  rw [sat_iff_eq_T hv φ, ← toBool_eval hv φ]
  exact (LPVal.toBool_eq_true_iff (eval v φ) (eval_ne_B hv φ)).symm

/-! ## LP-META-009: classical recapture -/

/-- **Classical recapture / collapse theorem.** Restricted to Boolean
valuations, LP entailment coincides *exactly* with classical two-valued
entailment, for the same `Γ, φ`. LP is a conservative, non-explosive
generalization of classical logic: nothing classical is lost on the
`B`-free fragment, and nothing classical is gained back on the full
3-valued semantics (that would contradict `Countermodels.explosion_invalid`). -/
theorem collapse (Γ : List (Formula Atom)) (φ : Formula Atom) :
    BooleanEntails Γ φ ↔ BEntails Γ φ := by
  constructor
  · intro h b hb
    have hv : Boolean (fun a => LPVal.ofBool (b a)) := fun a => LPVal.ofBool_ne_B (b a)
    have hbv : (fun a => LPVal.toBool (LPVal.ofBool (b a) : LPVal)) = b := by
      funext a; exact LPVal.toBool_ofBool (b a)
    have hΓ' : ∀ ψ ∈ Γ, Sat (fun a => LPVal.ofBool (b a)) ψ := by
      intro ψ hψ
      rw [sat_iff_beval hv ψ, hbv]
      exact hb ψ hψ
    have hres := h (fun a => LPVal.ofBool (b a)) hv hΓ'
    rw [sat_iff_beval hv φ, hbv] at hres
    exact hres
  · intro h v hv hΓ
    have hΓ' : ∀ ψ ∈ Γ, BEval (fun a => LPVal.toBool (v a)) ψ = true := by
      intro ψ hψ
      rw [← sat_iff_beval hv ψ]
      exact hΓ ψ hψ
    have hres := h (fun a => LPVal.toBool (v a)) hΓ'
    rw [← sat_iff_beval hv φ] at hres
    exact hres

/-! ## LP-META-011: one direction, cheaply -/

/-- **Corollary of the collapse theorem.** Every LP-valid formula is
classically valid.

**[Correção datada, 2026-08-27 — revisão adversarial, `DISC-DEC-105`,
severidade MODERADA.]** Uma versão anterior deste docstring afirmava "a
recíproca falha" (`CValid φ → Valid φ` não se sustentaria), justificando
com um exemplo no nível de *inferência* (`φ, ¬φ ⊢ ψ`) que não estabelece
nada sobre validade de fórmula única — nenhuma fórmula classicamente
válida mas LP-inválida foi, ou pôde ser, exibida. Revisão adversarial
independente (busca de literatura + busca computacional por força bruta
sobre 300k+ fórmulas + prova Lean independente parcial, ver
`04_FORMAL_RESEARCH_LAB/11_EXTERNAL_LINES/NONCLASSICAL_LOGIC_LP/
adversarial/REFEREE_REPORT.md`) não encontrou nenhum contraexemplo e
corrobora o fato padrão da literatura de lógica paraconsistente: LP e a
lógica clássica têm exatamente as mesmas fórmulas válidas — `Valid φ ↔
CValid φ` deveria valer como `iff` completo, não apenas a direção
provada aqui. O que genuinamente diverge entre LP e a lógica clássica
não é a validade de fórmula única, mas a relação de consequência: a
*inferência* `φ, ¬φ ⊢ ψ` é classicamente válida mas LP-inválida
(`Countermodels.explosion_invalid`), exatamente como
`deduction_theorem_breakdown` já documenta corretamente. Este teorema
(`valid_implies_cvalid`) permanece verdadeiro e corretamente demonstrado
como está — apenas a alegação em prosa sobre "a recíproca" foi removida
por ser não-sustentada e provavelmente falsa; a recíproca geral
permanece um resultado citável da literatura, não uma prova Lean nova
desta linha. -/
theorem valid_implies_cvalid (φ : Formula Atom) : Valid φ → CValid φ := by
  intro hφ
  have h1 : BooleanEntails ([] : List (Formula Atom)) φ := fun v _ _ => valid_iff.mp hφ v
  exact (collapse [] φ).mp h1

end TamesisLab.ExternalLines.NonclassicalLogicLP
