import TamesisLab.ExternalLines.NonclassicalLogicLP.Definitions
import TamesisLab.ExternalLines.NonclassicalLogicLP.ValidTheorems

set_option autoImplicit false

/-!
# LP-001 — The historically load-bearing INVALIDITIES

This is the point of formalizing a paraconsistent logic at all: the
laws that classical logic validates and LP does not, all on a **single,
shared countermodel**.

## The countermodel

Two atoms `a ≠ b` (concretely `a := true`, `b := false : Bool`) and one
valuation:

```
witness true  = B   (the glut: `a` is both true and false)
witness false = F   (`b` is simply false)
```

Under `witness`:
* `atom a` is satisfied (`B` is designated).
* `(atom a).neg` is satisfied too (`¬B = B`, still designated) — the
  glut satisfies a formula and its negation simultaneously.
* `atom b` is **not** satisfied (`F` is not designated).

That one valuation is enough to break Explosion, Modus Ponens, and
Disjunctive Syllogism at once — they all ask a designated `b` to follow
from designated premises built from `a`, and `witness` supplies
designated premises with `eval witness (atom b) = F`.

Reference: Graham Priest, "The Logic of Paradox", *J. Phil. Logic* 8
(1979), 219–241, the countermodel behind Priest's own headline
observations about EFQ and Modus Ponens (§§ I, IV).
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP

open Formula

/-! ## The witness, spelled out -/

/-- The canonical LP countermodel: `a ↦ B`, `b ↦ F`. -/
def witness : Bool → LPVal
  | true => LPVal.B
  | false => LPVal.F

@[simp] theorem witness_true : witness true = LPVal.B := rfl
@[simp] theorem witness_false : witness false = LPVal.F := rfl

/-- `witness` satisfies `atom a` and `(atom a).neg`, but not `atom b`,
for the distinct pair `a = true`, `b = false`. This is the shared fact
behind every invalidity theorem below. -/
theorem witness_certificate :
    Sat witness (Formula.atom true) ∧
    Sat witness (Formula.atom true).neg ∧
    ¬ Sat witness (Formula.atom false) := by decide

/-! ## LP-META-004: Explosion (ex falso quodlibet) is INVALID -/

/-- **Explosion fails in LP.** From `a` and `¬a`, `b` does *not* follow —
the headline result of paraconsistency. Witnessed exactly as specified:
`v a = B`, `v b = F`. -/
theorem explosion_invalid :
    ∃ a b : Bool, a ≠ b ∧
      ¬ Entails [Formula.atom a, (Formula.atom a).neg] (Formula.atom b) := by
  decide

/-! ## LP-META-005: Modus Ponens for the material conditional is INVALID -/

/-- **Modus Ponens fails in LP** — Priest's own famous result about the
*derived* material conditional (`Definitions.LPVal.imp`). Same
countermodel as `explosion_invalid`: `imp (atom a) (atom b)` is
satisfied (`imp B F = B`), `atom a` is satisfied, `atom b` is not. -/
theorem mp_invalid :
    ∃ a b : Bool, a ≠ b ∧
      ¬ Entails [Formula.atom a, (Formula.atom a).imp (Formula.atom b)]
        (Formula.atom b) := by
  decide

/-! ## LP-META-006: Disjunctive Syllogism is INVALID -/

/-- **Disjunctive Syllogism fails in LP** — historically the most-cited
LP invalidity (`a ∨ b, ¬a ⊬ b`). Same countermodel again: `or (atom a)
(atom b)` is satisfied (`or B F = B`), `(atom a).neg` is satisfied
(`¬B = B`), `atom b` is not. -/
theorem disjunctive_syllogism_invalid :
    ∃ a b : Bool, a ≠ b ∧
      ¬ Entails [(Formula.atom a).or (Formula.atom b), (Formula.atom a).neg]
        (Formula.atom b) := by
  decide

/-! ## LP-META-007: the deduction-theorem breakdown, both halves together -/

/-- **The deduction theorem breaks down in LP**, stated as a single
theorem so the gap is explicit:

* the *conditional* `φ → (¬φ → ψ)` is valid for **every** `φ, ψ`
  (`ValidTheorems.imp_neg_imp_valid` — no atom-set restriction needed);
* the corresponding *inference* `φ, ¬φ ⊢ ψ` is **not** valid, witnessed
  concretely by `a = true, b = false` under `witness`.

If the deduction theorem held in LP, the first bullet would force the
second to hold too. It doesn't — and this is exactly why Modus Ponens
and Explosion can fail while their "internalized" conditional form
remains a theorem. -/
theorem deduction_theorem_breakdown {Atom : Type*} :
    (∀ φ ψ : Formula Atom, Valid (φ.imp (φ.neg.imp ψ))) ∧
    ∃ a b : Bool, a ≠ b ∧
      ¬ Entails [Formula.atom a, (Formula.atom a).neg] (Formula.atom b) :=
  ⟨imp_neg_imp_valid, explosion_invalid⟩

end TamesisLab.ExternalLines.NonclassicalLogicLP
