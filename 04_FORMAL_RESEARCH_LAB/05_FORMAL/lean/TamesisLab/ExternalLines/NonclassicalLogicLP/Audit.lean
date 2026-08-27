import TamesisLab.ExternalLines.NonclassicalLogicLP.Definitions
import TamesisLab.ExternalLines.NonclassicalLogicLP.ValidTheorems
import TamesisLab.ExternalLines.NonclassicalLogicLP.Countermodels
import TamesisLab.ExternalLines.NonclassicalLogicLP.CollapseTheorem

set_option autoImplicit false

/-!
# LP-001 — Audit: truth tables vs. the textbook presentation, axiom footprint

## Truth-table cross-check

Priest's original 3×3 tables (Priest 1979, pp. 220-221; reproduced e.g.
in the Stanford Encyclopedia of Philosophy's "Paraconsistent Logic"
entry, §3, table for LP), row/column order T, B, F:

```
¬        ∧  T B F        ∨  T B F        →  T B F   (derived: ¬a ∨ b)
T → F    T  T B F        T  T T T        T  T B F
B → B    B  B B F        B  T B B        B  T B B
F → T    F  F F F        F  T B F        F  T T T
```

Every cell below is checked by `decide` against `Definitions.lean`'s
pattern-matched `neg`/`and`/`or`/`imp`, verbatim — no summary statistic,
no sampling.

## References

* Graham Priest, "The Logic of Paradox", *Journal of Philosophical
  Logic* 8 (1979), 219–241.
* Stanford Encyclopedia of Philosophy, "Paraconsistent Logic",
  https://plato.stanford.edu/entries/logic-paraconsistent/, §3.
-/

namespace TamesisLab.ExternalLines.NonclassicalLogicLP.Audit

open TamesisLab.ExternalLines.NonclassicalLogicLP
open TamesisLab.ExternalLines.NonclassicalLogicLP.LPVal

section TruthTables

-- ¬ (3 cells)
example : neg T = F := by decide
example : neg B = B := by decide
example : neg F = T := by decide

-- ∧ (9 cells)
example : and T T = T := by decide
example : and T B = B := by decide
example : and T F = F := by decide
example : and B T = B := by decide
example : and B B = B := by decide
example : and B F = F := by decide
example : and F T = F := by decide
example : and F B = F := by decide
example : and F F = F := by decide

-- ∨ (9 cells)
example : or T T = T := by decide
example : or T B = T := by decide
example : or T F = T := by decide
example : or B T = T := by decide
example : or B B = B := by decide
example : or B F = B := by decide
example : or F T = T := by decide
example : or F B = B := by decide
example : or F F = F := by decide

-- → , derived as `¬a ∨ b` (9 cells) — Priest 1979's table for the
-- material conditional, reproduced exactly by the derived definition.
example : imp T T = T := by decide
example : imp T B = B := by decide
example : imp T F = F := by decide
example : imp B T = T := by decide
example : imp B B = B := by decide
example : imp B F = B := by decide
example : imp F T = T := by decide
example : imp F B = T := by decide
example : imp F F = T := by decide

/-- The full ∧/∨ tables coincide with `min`/`max` under `F < B < T`, all
9 cells of each at once (not merely spot-checked). -/
example : ∀ x y : LPVal, and x y = min x y ∧ or x y = max x y :=
  fun x y => ⟨and_eq_min x y, or_eq_max x y⟩

end TruthTables

section Declarations

-- Registry of signatures made visible in the build log — nothing new
-- proved here, only confirmed to exist with the intended type.

#check @LPVal.neg
#check @LPVal.and
#check @LPVal.or
#check @LPVal.imp
#check @LPVal.D
#check @Formula.eval
#check @Formula.Sat
#check @Formula.Entails
#check @Formula.Valid

#check @lem_valid
#check @lnc_valid
#check @dne_entails
#check @dni_entails
#check @adjunction_valid
#check @and_elim_left
#check @and_elim_right
#check @or_intro_left
#check @or_intro_right
#check @imp_neg_imp_valid

#check @explosion_invalid
#check @mp_invalid
#check @disjunctive_syllogism_invalid
#check @deduction_theorem_breakdown

#check @Boolean
#check @BooleanEntails
#check @BEntails
#check @CValid
#check @collapse
#check @valid_implies_cvalid

end Declarations

section AxiomFootprint

/-!
`#print axioms` on every headline result, against the Lean/Mathlib
standard footprint `[propext, Classical.choice, Quot.sound]`. Every
result here is either `decide`-checked directly or built from such
proofs by pure (intuitionistic) logic, so no result is expected to
depend on anything beyond that closed standard set — several depend on
no axiom at all, `Formula`'s `DecidableEq` derive handler and
`LinearOrder.lift'` both being fully computable (verified: neither
routes through `Classical.dec`, see `Definitions.lean`, `and_eq_min`/
`or_eq_max`).
-/

#print axioms lem_valid
#print axioms lnc_valid
#print axioms dne_entails
#print axioms dni_entails
#print axioms adjunction_valid
#print axioms and_elim_left
#print axioms and_elim_right
#print axioms or_intro_left
#print axioms or_intro_right
#print axioms imp_neg_imp_valid

#print axioms explosion_invalid
#print axioms mp_invalid
#print axioms disjunctive_syllogism_invalid
#print axioms deduction_theorem_breakdown

#print axioms collapse
#print axioms valid_implies_cvalid

end AxiomFootprint

end TamesisLab.ExternalLines.NonclassicalLogicLP.Audit
