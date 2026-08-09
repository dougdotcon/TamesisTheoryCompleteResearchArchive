/-
Probe HS : the heat semigroup e^{tΔ} as a bounded, self-adjoint, real-symbol Fourier
multiplier on L² -- composed with the already fully characterized Leray projector
`lerayOpL2` to give the Stokes operator `P · e^{tΔ}`, the standard building block for a
future Duhamel formula / mild-solution formalization of Navier-Stokes.

Builds on `TamesisLab.Foundations.FourierMultiplierL2` (`fourierMulL2`, no
`HasTemperateGrowth` required) and `TamesisLab.Foundations.LerayOrthogonal`
(`inner_fourierMulL2_symm`, generic self-adjointness for any real-valued bounded symbol,
and `VecL2`) and `TamesisLab.Foundations.LerayProjector` (`lerayOpL2`, the matrix Leray
projector).

DELIBERATELY OUT OF SCOPE (see `RESEARCH_QUEUE.yaml`, work item
`FOUND-HEAT-SEMIGROUP-001`, and `01_PORTFOLIO/STRATEGIC_REVIEW_BATTLE_MAP_2026_08_09.md`):
the semigroup law `S(t+r) = S(t) ∘ S(r)` and strong continuity in `t`. Registered as
`HEAT-GAP-001`, open, requires algebra on products of `Lp ∞` symbols not verified in this
session.
-/
import TamesisLab.Foundations.LerayOrthogonal

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.HeatSemigroup

open TamesisProbe
open TamesisLab.Foundations.FourierMultiplierL2
open TamesisLab.Foundations.LerayOrthogonal (VecL2 inner_fourierMulL2_symm)

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-! ## Step H0 : the heat symbol `exp(-t‖ξ‖²)`, real-valued, bounded by 1 for `t ≥ 0`. -/

/-- The heat kernel symbol, real-valued (cast to `ℂ`). -/
def heatSymbol (E : Type*) [NormedAddCommGroup E] (t : ℝ) (x : E) : ℂ :=
  ((Real.exp (-(t * ‖x‖ ^ 2)) : ℝ) : ℂ)

theorem norm_heatSymbol_le_one {t : ℝ} (ht : 0 ≤ t) (x : E) :
    ‖heatSymbol E t x‖ ≤ 1 := by
  rw [heatSymbol, Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  calc Real.exp (-(t * ‖x‖ ^ 2)) ≤ Real.exp 0 :=
        Real.exp_le_exp.mpr (by nlinarith [mul_nonneg ht (sq_nonneg ‖x‖)])
    _ = 1 := Real.exp_zero

theorem measurable_heatSymbol (t : ℝ) : Measurable (heatSymbol E t) := by
  unfold heatSymbol
  fun_prop

theorem conj_heatSymbol (t : ℝ) (x : E) :
    (starRingEnd ℂ) (heatSymbol E t x) = heatSymbol E t x := by
  rw [heatSymbol]
  exact Complex.conj_ofReal _

/-! ## Step H1 : the `L∞` package and the `L²` operator, via the versioned `fourierMulL2`. -/

/-- The heat symbol packaged as an `L∞` element, for `t ≥ 0`. -/
def heatSymbolL2 {t : ℝ} (ht : 0 ≤ t) : Lp ℂ ∞ (volume : Measure E) :=
  ofBounded (measurable_heatSymbol (E := E) t).aestronglyMeasurable 1 (norm_heatSymbol_le_one ht)

theorem coeFn_heatSymbolL2 {t : ℝ} (ht : 0 ≤ t) :
    ⇑(heatSymbolL2 (E := E) ht) =ᵐ[(volume : Measure E)] fun x => heatSymbol E t x := by
  unfold heatSymbolL2 ofBounded
  exact MemLp.coeFn_toLp _

theorem norm_heatSymbolL2_le_one {t : ℝ} (ht : 0 ≤ t) :
    ‖heatSymbolL2 (E := E) ht‖ ≤ 1 :=
  norm_ofBounded_le _ 1 (norm_heatSymbol_le_one ht) zero_le_one

theorem conj_heatSymbolL2 {t : ℝ} (ht : 0 ≤ t) :
    ∀ᵐ x ∂(volume : Measure E),
      (starRingEnd ℂ) (heatSymbolL2 (E := E) ht x) = heatSymbolL2 (E := E) ht x := by
  filter_upwards [coeFn_heatSymbolL2 ht] with x hx
  rw [hx]
  exact conj_heatSymbol t x

variable (F : Type*) [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- **The heat semigroup `e^{tΔ}` (`t ≥ 0`) as a bounded operator on `L²(E, F)`,** via the
already-versioned `fourierMulL2` Fourier multiplier calculus (no smoothness required of the
symbol). -/
def heatOpL2 {t : ℝ} (ht : 0 ≤ t) :
    Lp (α := E) F 2 →L[ℂ] Lp (α := E) F 2 :=
  fourierMulL2 F (heatSymbolL2 (E := E) ht)

theorem heatOpL2_apply {t : ℝ} (ht : 0 ≤ t) (f : Lp (α := E) F 2) :
    heatOpL2 F ht f = 𝓕⁻ (mulL2 F (heatSymbolL2 (E := E) ht) (𝓕 f)) :=
  fourierMulL2_apply _ _

/-! ## Step H2 : contraction, `‖e^{tΔ}‖ ≤ 1`. -/

theorem norm_heatOpL2_apply_le {t : ℝ} (ht : 0 ≤ t) (f : Lp (α := E) F 2) :
    ‖heatOpL2 F ht f‖ ≤ ‖f‖ := by
  have h := norm_fourierMulL2_apply_le (F := F) (heatSymbolL2 (E := E) ht) f
  calc ‖heatOpL2 F ht f‖ ≤ ‖heatSymbolL2 (E := E) ht‖ * ‖f‖ := h
    _ ≤ 1 * ‖f‖ := by gcongr; exact norm_heatSymbolL2_le_one ht
    _ = ‖f‖ := one_mul _

theorem norm_heatOpL2_le {t : ℝ} (ht : 0 ≤ t) :
    ‖(heatOpL2 F ht : Lp (α := E) F 2 →L[ℂ] Lp (α := E) F 2)‖ ≤ 1 :=
  ContinuousLinearMap.opNorm_le_bound _ zero_le_one
    (fun f => by simpa using norm_heatOpL2_apply_le F ht f)

/-! ## Step H3 : self-adjointness, by reuse of the already-versioned generic real-symbol
lemma `inner_fourierMulL2_symm` -- no new symmetry proof needed.

Stated as the raw inner-product identity, NOT wrapped in `IsSelfAdjoint` /
`ContinuousLinearMap.adjoint`: the latter need the `Lp (α := E) F 2` `Module ℂ` instance
reached through `InnerProductSpace.toNormedSpace.toModule`, while `heatOpL2` (built via
`fourierMulL2`/`LinearMap.mkContinuous` in `FourierMultiplierL2.lean`, which does not import
`Mathlib.Analysis.InnerProductSpace.Adjoint`) carries the plain `Lp.instModule` path. The two
are almost certainly defeq, but the metavariable unification `ContinuousLinearMap.adjoint`'s
statement requires does not resolve this automatically, and forcing it is out of scope here
-- same category of prudent restraint as the `Hs E F s` decision in `LP-GAP-005`
(pullback pairing instead of a global instance). The inner-product identity below is the
mathematical content; no bureaucratic wrapper is attempted. -/

theorem inner_heatOpL2_symm {t : ℝ} (ht : 0 ≤ t) (f g : Lp (α := E) F 2) :
    inner ℂ (heatOpL2 F ht f) g = inner ℂ f (heatOpL2 F ht g) :=
  inner_fourierMulL2_symm (heatSymbolL2 (E := E) ht) (conj_heatSymbolL2 ht) f g

/-- **Package theorem**: the heat semigroup at any `t ≥ 0` is a contraction on `L²(E, F)`
and symmetric for the `L²` inner product. -/
theorem heatOpL2_package {t : ℝ} (ht : 0 ≤ t) :
    ‖(heatOpL2 F ht : Lp (α := E) F 2 →L[ℂ] Lp (α := E) F 2)‖ ≤ 1 ∧
    ∀ f g : Lp (α := E) F 2, inner ℂ (heatOpL2 F ht f) g = inner ℂ f (heatOpL2 F ht g) :=
  ⟨norm_heatOpL2_le F ht, inner_heatOpL2_symm F ht⟩

/-! ## Step H5 : the Stokes operator `P · e^{tΔ}`, composing the heat semigroup with the
already fully characterized matrix Leray projector `lerayOpL2` (bounded, idempotent,
self-adjoint orthogonal projection, all proved in `LerayProjector.lean` /
`LerayOrthogonal.lean`). This is the standard building block a future Duhamel-formula /
mild-solution formalization of Navier-Stokes would need. NOT a claim that such a
formalization exists, nor that it would resolve `NS-GAP-001`. -/

open TamesisProbe (lerayOpL2 norm_lerayOpL2_le E3 b3)

variable {n : ℕ}

/-- **The Stokes operator** `P · e^{tΔ}` on divergence-free `L²` vector fields, for `t ≥ 0`. -/
def stokesOpL2 (b : OrthonormalBasis (Fin n) ℝ E) {t : ℝ} (ht : 0 ≤ t) :
    VecL2 E n →L[ℂ] VecL2 E n :=
  lerayOpL2 b ∘L heatOpL2 (EuclideanSpace ℂ (Fin n)) ht

theorem norm_stokesOpL2_le (b : OrthonormalBasis (Fin n) ℝ E) {t : ℝ} (ht : 0 ≤ t) :
    ‖stokesOpL2 b ht‖ ≤ ‖lerayOpL2 b‖ := by
  calc ‖stokesOpL2 b ht‖
      ≤ ‖lerayOpL2 b‖ * ‖(heatOpL2 (EuclideanSpace ℂ (Fin n)) ht :
          VecL2 E n →L[ℂ] VecL2 E n)‖ := ContinuousLinearMap.opNorm_comp_le _ _
    _ ≤ ‖lerayOpL2 b‖ * 1 :=
        mul_le_mul_of_nonneg_left (norm_heatOpL2_le (EuclideanSpace ℂ (Fin n)) ht)
          (norm_nonneg _)
    _ = ‖lerayOpL2 b‖ := mul_one _

theorem norm_stokesOpL2_le' (b : OrthonormalBasis (Fin n) ℝ E) {t : ℝ} (ht : 0 ≤ t) :
    ‖stokesOpL2 b ht‖ ≤ 2 * (n : ℝ) ^ 2 :=
  (norm_stokesOpL2_le b ht).trans (norm_lerayOpL2_le b)

/-! Concrete instance on `ℝ³`, reusing the `E3`/`b3` already established in
`LerayProjector.lean` (via `TamesisProbe`) instead of redefining them -- avoids installing
a second, redundant `MeasurableSpace`/`BorelSpace` instance for the same underlying type. -/

/-- **Concrete positive instance**: on `ℝ³`, at `t = 1`, the Stokes operator `P·e^{Δ}` is a
bounded operator with an explicit numeric norm bound, and the underlying heat semigroup is
symmetric for the `L²` inner product on every pair of vectors -- non-vacuous. -/
theorem concrete_stokesOpL2_R3 :
    ‖stokesOpL2 b3 (t := 1) zero_le_one‖ ≤ 18 ∧
    ∀ f g : Lp (α := E3) (EuclideanSpace ℂ (Fin 3)) 2,
      inner ℂ (heatOpL2 (E := E3) (EuclideanSpace ℂ (Fin 3)) (t := 1) zero_le_one f) g
        = inner ℂ f (heatOpL2 (E := E3) (EuclideanSpace ℂ (Fin 3)) (t := 1) zero_le_one g) :=
  ⟨(norm_stokesOpL2_le' b3 zero_le_one).trans_eq (by norm_num),
    inner_heatOpL2_symm (E := E3) _ zero_le_one⟩

/-! ## O que NÃO é afirmado

```text
que S(t+r) = S(t) ∘ S(r) (lei de semigrupo) -- HEAT-GAP-001, aberto
que t ↦ heatOpL2 t é fortemente contínuo -- HEAT-GAP-001, aberto
que existe uma formalização de solução branda / fórmula de Duhamel
que Navier-Stokes ficou alcançável, ou que NS-GAP-001/004 tem caminho de prova
```
-/

end TamesisLab.Foundations.HeatSemigroup

#print axioms TamesisLab.Foundations.HeatSemigroup.norm_heatSymbol_le_one
#print axioms TamesisLab.Foundations.HeatSemigroup.measurable_heatSymbol
#print axioms TamesisLab.Foundations.HeatSemigroup.conj_heatSymbolL2
#print axioms TamesisLab.Foundations.HeatSemigroup.norm_heatOpL2_le
#print axioms TamesisLab.Foundations.HeatSemigroup.inner_heatOpL2_symm
#print axioms TamesisLab.Foundations.HeatSemigroup.heatOpL2_package
#print axioms TamesisLab.Foundations.HeatSemigroup.stokesOpL2
#print axioms TamesisLab.Foundations.HeatSemigroup.norm_stokesOpL2_le
#print axioms TamesisLab.Foundations.HeatSemigroup.norm_stokesOpL2_le'
#print axioms TamesisLab.Foundations.HeatSemigroup.concrete_stokesOpL2_R3
