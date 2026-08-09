/-
`FOUND-DUHAMEL-FIXEDPOINT-INSTANCE-001` : a CONCRETE, non-degenerate positive instance of
`TamesisLab.Foundations.DuhamelFixedPoint.exists_unique_mild_solution`
(`FOUND-ABSTRACT-DUHAMEL-FIXEDPOINT-001`).

That theorem was closed GIVEN, as an explicit hypothesis, that the forcing term
`B : L²(E,F) → L²(E,F)` is Lipschitz with constant `L`, and shipped WITHOUT a witness showing the
hypotheses are jointly satisfiable in a non-degenerate way (`L > 0`) -- breaking the pattern every
other major result of this session followed (`concrete_stokesOpL2_R3`,
`concrete_lerayOpHs_orthogonal_R3`, `positive_instance_helmholtz_R3`, etc.). This file closes that
gap, per `01_PORTFOLIO/PORTFOLIO_REVIEW_DUHAMEL_FIXEDPOINT_INSTANCE_2026_08_09.md`.

## What is instantiated, and why

* `E := TamesisProbe.E3 = EuclideanSpace ℝ (Fin 3)`, `F := EuclideanSpace ℂ (Fin 3)` -- the SAME
  concrete `ℝ³`-flavoured Hilbert spaces already used for the other "positive instance" theorems
  in this codebase (`concrete_stokesOpL2_R3` in `HeatSemigroup.lean`, etc.), so the state space
  `V3 := Lp (α := E3) F3 2` is a genuine, already-vetted concrete instantiation, not a fresh
  ad-hoc one.
* `B := concreteB`, scalar multiplication by `1/2` on `V3`, packaged as a `ContinuousLinearMap`.
  This is a completely generic example of a bounded linear forcing term in an abstract semilinear
  evolution equation -- NOT `B = 0` (already covered, trivially, by
  `DuhamelSkeleton.duhamelTerm_of_zero`), and NOT any approximation of, or claim about, the actual
  Navier-Stokes nonlinearity (`NS-GAP-001`/`004` remain completely untouched and out of scope).
* `L := 1/2 : ℝ≥0`, STRICTLY POSITIVE, obtained from a genuine operator-norm bound on `concreteB`
  (via `ContinuousLinearMap.opNorm_smul_le` and `ContinuousLinearMap.norm_id_le`), not asserted by
  fiat.
* `T := 1`, satisfying `0 < T` and `T * L = 1/2 < 1`, both by direct numeral computation.
* `u0 := 0`, since the non-degeneracy content of this instance is entirely in `B`/`L`, not `u0`.

The result: `exists_unique_mild_solution` really does produce an actual `∃!` mild solution on
`[0,1]` for this concrete, non-degenerate `B`, confirming the abstract theorem is not vacuous.
-/
import TamesisLab.Foundations.DuhamelFixedPoint

open MeasureTheory
open scoped BoundedContinuousFunction NNReal

set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.DuhamelFixedPoint

open TamesisProbe (E3)
open TamesisLab.Foundations.DuhamelSkeleton

/-! ## The concrete Hilbert spaces -/

/-- The concrete codomain fiber `ℂ³`, matching the `F` used by the other "positive instance"
theorems of this codebase (e.g. `concrete_stokesOpL2_R3` in `HeatSemigroup.lean`). -/
abbrev F3 : Type := EuclideanSpace ℂ (Fin 3)

/-- The concrete state space `L²(ℝ³; ℂ³)` for this instance. -/
abbrev V3 : Type := Lp (α := E3) F3 2

/-! ## The concrete forcing operator -/

/-- **The concrete forcing operator**: scalar multiplication by `1/2` on `V3`, as a bounded
`ℂ`-linear map. A generic, abstract example of a bounded linear forcing term -- NOT `B = 0`
(the trivial case, already covered by `DuhamelSkeleton.duhamelTerm_of_zero`), and unrelated to
the Navier-Stokes nonlinearity. -/
def concreteB : V3 →L[ℂ] V3 := (1 / 2 : ℂ) • ContinuousLinearMap.id ℂ V3

/-- `‖(1/2 : ℂ)‖ = 1/2`. -/
private theorem norm_half_C : ‖(1 / 2 : ℂ)‖ = (1 / 2 : ℝ) := by
  rw [show (1 / 2 : ℂ) = (1 : ℂ) / (2 : ℂ) from by norm_num, norm_div, norm_one,
    RCLike.norm_ofNat]

/-- `concreteB` has operator norm at most `1/2`. -/
theorem norm_concreteB_le : ‖concreteB‖ ≤ (1 / 2 : ℝ) := by
  calc ‖concreteB‖
      ≤ ‖(1 / 2 : ℂ)‖ * ‖ContinuousLinearMap.id ℂ V3‖ :=
        ContinuousLinearMap.opNorm_smul_le (1 / 2 : ℂ) (ContinuousLinearMap.id ℂ V3)
    _ ≤ ‖(1 / 2 : ℂ)‖ * 1 := by
        gcongr
        exact ContinuousLinearMap.norm_id_le
    _ = (1 / 2 : ℝ) := by rw [norm_half_C]; ring

/-- **`concreteB` is Lipschitz with the concrete, STRICTLY POSITIVE constant `L = 1/2`.** -/
theorem lipschitzWith_concreteB : LipschitzWith (1 / 2 : ℝ≥0) (⇑concreteB) := by
  rw [← ContinuousLinearMap.opNorm_le_iff_lipschitz]
  simpa using norm_concreteB_le

/-- The chosen Lipschitz constant `1/2` is strictly positive -- the whole point of this instance,
against the shipped-but-unwitnessed abstract theorem. -/
theorem concreteB_L_pos : (0 : ℝ≥0) < (1 / 2 : ℝ≥0) := by norm_num

/-! ## The concrete instance -/

/-- **Concrete non-degenerate instance (`FOUND-DUHAMEL-FIXEDPOINT-INSTANCE-001`)** of
`exists_unique_mild_solution`: on `L²(ℝ³; ℂ³)`, with `B` the nonzero scalar-multiplication-by-
`1/2` operator (Lipschitz with the strictly positive constant `L = 1/2`) and `T = 1`
(`T * L = 1/2 < 1`), the abstract mild-solution theorem produces an actual `∃!` witness. This
confirms `exists_unique_mild_solution` is not vacuous. It is NOT a Navier-Stokes statement: `B`
here is a generic bounded linear operator, unrelated to and not approximating the actual
Navier-Stokes forcing term (`NS-GAP-001`/`004` untouched, out of scope). -/
theorem concrete_mild_solution_instance :
    ∃! u : Set.Icc (0 : ℝ) (1 : ℝ) →ᵇ V3,
      ∀ t : Set.Icc (0 : ℝ) (1 : ℝ),
        u t = duhamelTerm F3 (⇑concreteB) t.1 (0 : V3)
          (Set.IccExtend zero_le_one (⇑u)) t.2.1 :=
  exists_unique_mild_solution F3 (⇑concreteB) lipschitzWith_concreteB (0 : V3)
    zero_lt_one (by
      have hL : ((1 / 2 : ℝ≥0) : ℝ) < 1 := by norm_num
      calc (1 : ℝ) * ((1 / 2 : ℝ≥0) : ℝ) = ((1 / 2 : ℝ≥0) : ℝ) := by ring
        _ < 1 := hL)

end TamesisLab.Foundations.DuhamelFixedPoint

#print axioms TamesisLab.Foundations.DuhamelFixedPoint.norm_concreteB_le
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.lipschitzWith_concreteB
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.concreteB_L_pos
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.concrete_mild_solution_instance
