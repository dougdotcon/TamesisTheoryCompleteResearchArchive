/-
Probe HS : FM-GAP-001 — `H^s` as a normed TYPE.
Mathlib only has the PREDICATE `MemSobolev s p : 𝓢'(E,F) → Prop`.
Here: the submodule `{f | MemSobolev s 2 f}`, its coercion to a type, and a norm.
-/
import TamesisLab.Foundations.FourierMultiplierL2

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter Metric
open scoped SchwartzMap Topology

set_option maxHeartbeats 1000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.SobolevSpace

open TamesisLab.Foundations.FourierMultiplierL2

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-! ## Step 0 : linearity of the `Lp → 𝓢'` coercion (used repeatedly). -/

theorem coe_L2_add (u v : Lp F 2 (volume : Measure E)) :
    ((u + v : Lp F 2 (volume : Measure E)) : 𝓢'(E, F)) = (u : 𝓢'(E, F)) + (v : 𝓢'(E, F)) :=
  map_add (MeasureTheory.Lp.toTemperedDistributionCLM F (volume : Measure E) 2) u v

theorem coe_L2_smul (c : ℂ) (u : Lp (α := E) F 2) :
    ((c • u : Lp (α := E) F 2) : 𝓢'(E, F)) = c • (u : 𝓢'(E, F)) :=
  map_smul (MeasureTheory.Lp.toTemperedDistributionCLM F (volume : Measure E) 2) c u

theorem coe_L2_zero : ((0 : Lp (α := E) F 2) : 𝓢'(E, F)) = 0 :=
  map_zero (MeasureTheory.Lp.toTemperedDistributionCLM F (volume : Measure E) 2)

/-! ## Step 1 : `H^s` is a `Submodule` of `𝓢'(E,F)`. -/

variable (E F) in
/-- The Sobolev space of order `s`, `p = 2`, as a submodule of the tempered distributions. -/
def sobolevSubmodule (s : ℝ) : Submodule ℂ 𝓢'(E, F) where
  carrier := {f | MemSobolev s 2 f}
  add_mem' hf hg := MemSobolev.add hf hg
  zero_mem' := memSobolev_fun_zero E F s 2
  smul_mem' c _ hf := hf.smul c

@[simp]
theorem mem_sobolevSubmodule {s : ℝ} {f : 𝓢'(E, F)} :
    f ∈ sobolevSubmodule E F s ↔ MemSobolev s 2 f := Iff.rfl

variable (E F) in
/-- **`H^s(E,F)` AS A TYPE.** -/
def Hs (s : ℝ) : Type _ := ↥(sobolevSubmodule E F s)

namespace Hs

/-! ## Step 2 : the algebraic structure. -/

instance instAddCommGroup (s : ℝ) : AddCommGroup (Hs E F s) :=
  inferInstanceAs (AddCommGroup ↥(sobolevSubmodule E F s))

instance instModule (s : ℝ) : Module ℂ (Hs E F s) :=
  inferInstanceAs (Module ℂ ↥(sobolevSubmodule E F s))

/-- The underlying tempered distribution. -/
def toDist {s : ℝ} (f : Hs E F s) : 𝓢'(E, F) :=
  ((show ↥(sobolevSubmodule E F s) from f) : 𝓢'(E, F))

theorem memSobolev_toDist {s : ℝ} (f : Hs E F s) : MemSobolev s 2 (toDist f) :=
  (show ↥(sobolevSubmodule E F s) from f).2

theorem toDist_injective {s : ℝ} : Function.Injective (toDist : Hs E F s → 𝓢'(E, F)) :=
  fun _ _ h => Subtype.coe_injective h

@[simp] theorem toDist_add {s : ℝ} (f g : Hs E F s) :
    toDist (f + g) = toDist f + toDist g := rfl
@[simp] theorem toDist_zero {s : ℝ} : toDist (0 : Hs E F s) = 0 := rfl
@[simp] theorem toDist_smul {s : ℝ} (c : ℂ) (f : Hs E F s) :
    toDist (c • f) = c • toDist f := rfl

/-- The type `Hs E F s` is exactly the Mathlib predicate `MemSobolev s 2`. -/
theorem range_toDist (s : ℝ) :
    Set.range (toDist : Hs E F s → 𝓢'(E, F)) = {f : 𝓢'(E, F) | MemSobolev s 2 f} := by
  ext f
  constructor
  · rintro ⟨g, rfl⟩; exact memSobolev_toDist g
  · intro hf; exact ⟨(show Hs E F s from ⟨f, hf⟩), rfl⟩

/-! ## Step 3 : the `L²` representative, well defined by injectivity. -/

/-- The `L²` function representing `besselPotential s f`. -/
def toL2 {s : ℝ} (f : Hs E F s) : Lp (α := E) F 2 := Classical.choose (memSobolev_toDist f)

theorem besselPotential_toDist {s : ℝ} (f : Hs E F s) :
    besselPotential E F s (toDist f) = ((toL2 f : Lp (α := E) F 2) : 𝓢'(E, F)) :=
  Classical.choose_spec (memSobolev_toDist f)

/-- WELL-DEFINEDNESS: the `L²` representative is unique. -/
theorem toL2_eq {s : ℝ} {f : Hs E F s} {u : Lp (α := E) F 2}
    (h : besselPotential E F s (toDist f) = (u : 𝓢'(E, F))) : toL2 f = u :=
  toTemperedDistribution_injective ((besselPotential_toDist f).symm.trans h)

@[simp] theorem toL2_add {s : ℝ} (f g : Hs E F s) : toL2 (f + g) = toL2 f + toL2 g := by
  refine toL2_eq ?_
  rw [coe_L2_add, toDist_add, map_add, besselPotential_toDist, besselPotential_toDist]

@[simp] theorem toL2_zero {s : ℝ} : toL2 (0 : Hs E F s) = 0 := by
  refine toL2_eq ?_
  rw [coe_L2_zero, toDist_zero, map_zero]

@[simp] theorem toL2_smul {s : ℝ} (c : ℂ) (f : Hs E F s) : toL2 (c • f) = c • toL2 f := by
  refine toL2_eq ?_
  rw [coe_L2_smul, toDist_smul, map_smul, besselPotential_toDist]

theorem toL2_injective {s : ℝ} : Function.Injective (toL2 : Hs E F s → Lp (α := E) F 2) := by
  intro f g h
  refine toDist_injective (besselPotential_injective s ?_)
  rw [besselPotential_toDist, besselPotential_toDist, h]

theorem toL2_surjective {s : ℝ} : Function.Surjective (toL2 : Hs E F s → Lp (α := E) F 2) := by
  intro w
  obtain ⟨v, hv₁, hv₂⟩ := exists_memSobolev_besselPotential_eq s w
  exact ⟨(show Hs E F s from ⟨v, hv₁⟩), toL2_eq hv₂⟩

variable (E F) in
def toL2AddHom (s : ℝ) : Hs E F s →+ Lp (α := E) F 2 where
  toFun := toL2
  map_zero' := toL2_zero
  map_add' := toL2_add

/-! ## Step 4 : the norm `‖f‖_{H^s} = ‖besselPotential s f‖_{L²}`. -/

instance instNormedAddCommGroup (s : ℝ) : NormedAddCommGroup (Hs E F s) :=
  NormedAddCommGroup.induced (Hs E F s) (Lp F 2 (volume : Measure E))
    (toL2AddHom E F s) toL2_injective

@[simp] theorem norm_def {s : ℝ} (f : Hs E F s) : ‖f‖ = ‖toL2 f‖ := rfl

instance instNormedSpace (s : ℝ) : NormedSpace ℂ (Hs E F s) where
  norm_smul_le c f := by
    rw [norm_def, norm_def, toL2_smul]
    exact norm_smul_le c (toL2 f)

variable (E F) in
def toL2ₗ (s : ℝ) : Hs E F s →ₗ[ℂ] Lp (α := E) F 2 where
  toFun := toL2
  map_add' := toL2_add
  map_smul' := toL2_smul

variable (E F) in
/-- **`H^s` is isometrically isomorphic to `L²` via the Bessel potential.** -/
def toL2ₗᵢ (s : ℝ) : Hs E F s ≃ₗᵢ[ℂ] Lp (α := E) F 2 where
  toLinearEquiv := LinearEquiv.ofBijective (toL2ₗ E F s) ⟨toL2_injective, toL2_surjective⟩
  norm_map' _ := rfl

@[simp] theorem toL2ₗᵢ_apply {s : ℝ} (f : Hs E F s) : toL2ₗᵢ E F s f = toL2 f := rfl

instance instCompleteSpace (s : ℝ) : CompleteSpace (Hs E F s) :=
  (toL2ₗᵢ E F s).toIsometryEquiv.completeSpace

/-- The defining property of the norm, in the form asked for. -/
theorem norm_eq_of_besselPotential {s : ℝ} (f : Hs E F s) (u : Lp (α := E) F 2)
    (h : besselPotential E F s (toDist f) = (u : 𝓢'(E, F))) : ‖f‖ = ‖u‖ := by
  rw [norm_def, toL2_eq h]

/-! ## Step 5 : POSITIVE INSTANCE — `Hs E F s` is inhabited by a nonzero element. -/

section Positive

variable (E F)

theorem volume_ball_ne_top : (volume : Measure E) (ball (0 : E) 1) ≠ ⊤ := measure_ball_ne_top

theorem volume_ball_ne_zero : (volume : Measure E) (ball (0 : E) 1) ≠ 0 :=
  (measure_ball_pos volume 0 one_pos).ne'

theorem volume_real_ball_pos : 0 < (volume : Measure E).real (ball (0 : E) 1) := by
  rw [measureReal_def]
  exact ENNReal.toReal_pos (volume_ball_ne_zero E) (volume_ball_ne_top E)

/-- The indicator of the unit ball times the vector `c`: an explicit `L²` function. -/
def bumpL2 (c : F) : Lp F 2 (volume : Measure E) :=
  indicatorConstLp 2 measurableSet_ball (volume_ball_ne_top E) c

theorem norm_bumpL2 (c : F) :
    ‖bumpL2 E F c‖ = ‖c‖ * ((volume : Measure E).real (ball (0 : E) 1)) ^ (1 / 2 : ℝ) := by
  rw [bumpL2, norm_indicatorConstLp (by norm_num) (by norm_num)]
  norm_num

theorem norm_bumpL2_pos {c : F} (hc : c ≠ 0) : 0 < ‖bumpL2 E F c‖ := by
  rw [norm_bumpL2]
  exact mul_pos (norm_pos_iff.mpr hc) (Real.rpow_pos_of_pos (volume_real_ball_pos E) _)

/-- **THE POSITIVE INSTANCE.** An explicit element of `H^s` for every `s` and every `c : F`:
the unique distribution whose Bessel potential of order `s` is `c · 1_{B(0,1)}`. -/
def bump (s : ℝ) (c : F) : Hs E F s := Classical.choose (toL2_surjective (bumpL2 E F c))

theorem toL2_bump (s : ℝ) (c : F) : toL2 (bump E F s c) = bumpL2 E F c :=
  Classical.choose_spec (toL2_surjective (bumpL2 E F c))

/-- Its Bessel potential is literally the indicator function. -/
theorem besselPotential_toDist_bump (s : ℝ) (c : F) :
    besselPotential E F s (toDist (bump E F s c)) =
      ((indicatorConstLp 2 measurableSet_ball (volume_ball_ne_top E) c :
        Lp F 2 (volume : Measure E)) : 𝓢'(E, F)) := by
  rw [besselPotential_toDist, toL2_bump]; rfl

/-- **THE NORM IS COMPUTED**, not merely bounded. -/
theorem norm_bump (s : ℝ) (c : F) :
    ‖bump E F s c‖ = ‖c‖ * ((volume : Measure E).real (ball (0 : E) 1)) ^ (1 / 2 : ℝ) := by
  rw [norm_def, toL2_bump, norm_bumpL2]

theorem norm_bump_pos (s : ℝ) {c : F} (hc : c ≠ 0) : 0 < ‖bump E F s c‖ := by
  rw [norm_def, toL2_bump]; exact norm_bumpL2_pos E F hc

theorem bump_ne_zero (s : ℝ) {c : F} (hc : c ≠ 0) : bump E F s c ≠ 0 :=
  norm_pos_iff.mp (norm_bump_pos E F s hc)

theorem toDist_bump_ne_zero (s : ℝ) {c : F} (hc : c ≠ 0) : toDist (bump E F s c) ≠ 0 := fun h =>
  bump_ne_zero E F s hc (toDist_injective (h.trans toDist_zero.symm))

/-- NON-VACUITY, packaged: `Hs E F s` contains an element that is nonzero, of strictly
positive norm, whose underlying tempered distribution is nonzero and really satisfies the
Mathlib predicate `MemSobolev s 2`. -/
theorem nontrivial_witness [Nontrivial F] (s : ℝ) :
    ∃ f : Hs E F s, f ≠ 0 ∧ 0 < ‖f‖ ∧ toDist f ≠ 0 ∧ MemSobolev s 2 (toDist f) := by
  obtain ⟨c, hc⟩ := exists_ne (0 : F)
  exact ⟨bump E F s c, bump_ne_zero E F s hc, norm_bump_pos E F s hc,
    toDist_bump_ne_zero E F s hc, memSobolev_toDist _⟩

instance instNontrivial [Nontrivial F] (s : ℝ) : Nontrivial (Hs E F s) := by
  obtain ⟨f, hf, -⟩ := nontrivial_witness E F s
  exact ⟨⟨f, 0, hf⟩⟩

end Positive

/-! ## Step 6 : the `L∞` Fourier multiplier as a CLM on `H^s`. -/

variable (E F) in
/-- **Fourier multiplier with an arbitrary `L∞` symbol, as a bounded operator on `H^s`.** -/
def fourierMultiplierSobolevCLM (s : ℝ) (g : Lp ℂ ∞ (volume : Measure E)) :
    Hs E F s →L[ℂ] Hs E F s :=
  (toL2ₗᵢ E F s).symm.toLinearIsometry.toContinuousLinearMap ∘L
    fourierMulL2 F g ∘L (toL2ₗᵢ E F s).toLinearIsometry.toContinuousLinearMap

@[simp] theorem toL2_fourierMultiplierSobolevCLM {s : ℝ} (g : Lp ℂ ∞ (volume : Measure E))
    (f : Hs E F s) :
    toL2 (fourierMultiplierSobolevCLM E F s g f) = fourierMulL2 F g (toL2 f) := by
  show toL2ₗᵢ E F s ((toL2ₗᵢ E F s).symm (fourierMulL2 F g (toL2ₗᵢ E F s f))) = _
  rw [LinearIsometryEquiv.apply_symm_apply, toL2ₗᵢ_apply]

theorem norm_fourierMultiplierSobolevCLM_apply_le {s : ℝ} (g : Lp ℂ ∞ (volume : Measure E))
    (f : Hs E F s) : ‖fourierMultiplierSobolevCLM E F s g f‖ ≤ ‖g‖ * ‖f‖ := by
  rw [norm_def, norm_def, toL2_fourierMultiplierSobolevCLM]
  exact norm_fourierMulL2_apply_le g (toL2 f)

theorem norm_fourierMultiplierSobolevCLM_le {s : ℝ} (g : Lp ℂ ∞ (volume : Measure E)) :
    ‖fourierMultiplierSobolevCLM E F s g‖ ≤ ‖g‖ :=
  ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg g)
    (norm_fourierMultiplierSobolevCLM_apply_le g)

/-- The operator acts on the distribution side exactly by `g(D)` after `besselPotential s`. -/
theorem besselPotential_toDist_fourierMultiplierSobolevCLM {s : ℝ}
    (g : Lp ℂ ∞ (volume : Measure E)) (f : Hs E F s) :
    besselPotential E F s (toDist (fourierMultiplierSobolevCLM E F s g f)) =
      ((fourierMulL2 F g (toL2 f) : Lp (α := E) F 2) : 𝓢'(E, F)) := by
  rw [besselPotential_toDist, toL2_fourierMultiplierSobolevCLM]

/-- Positive instance at operator level: the Leray-type symbol, for which the Mathlib
`fourierMultiplierCLM` is identically `0`, gives a genuine bounded operator on `H^s`. -/
theorem fourierMultiplierSobolevCLM_leray [Nontrivial E] [Nontrivial F] {m : E} (hm : m ≠ 0)
    (s : ℝ) :
    (¬ (lerayComponent m m).HasTemperateGrowth) ∧
    (TemperedDistribution.fourierMultiplierCLM F (lerayComponent m m) =
      (0 : 𝓢'(E, F) →L[ℂ] 𝓢'(E, F))) ∧
    ‖fourierMultiplierSobolevCLM E F s (lerayComponentL2 m m)‖ ≤ ‖lerayComponentL2 m m‖ ∧
    Nontrivial (Hs E F s) :=
  ⟨not_hasTemperateGrowth_lerayComponent hm,
   fourierMultiplierCLM_eq_zero_of_not_temperate (not_hasTemperateGrowth_lerayComponent hm),
   norm_fourierMultiplierSobolevCLM_le _, instNontrivial E F s⟩

end Hs

/-! ## Step 7 : CLOSED, HYPOTHESIS-FREE anti-vacuity statements (`E = ℝ`, `F = ℂ`, `s = 5/2`). -/

open Hs

/-- `H^{5/2}(ℝ; ℂ)` is a complete normed `ℂ`-space with a nonzero element. No hypotheses,
no free variables: this statement cannot be vacuous. -/
theorem concrete_Hs_nontrivial :
    ∃ f : Hs ℝ ℂ (5 / 2 : ℝ), f ≠ 0 ∧ 0 < ‖f‖ ∧ toDist f ≠ 0 ∧
      MemSobolev (5 / 2 : ℝ) 2 (toDist f) :=
  nontrivial_witness ℝ ℂ (5 / 2 : ℝ)

/-- The `H^{5/2}` norm of the explicit witness, computed to a closed-form number. -/
theorem concrete_norm_bump : ‖bump ℝ ℂ (5 / 2 : ℝ) 1‖ = 2 ^ (1 / 2 : ℝ) := by
  rw [norm_bump, norm_one, one_mul, measureReal_def, Real.volume_ball]
  norm_num

theorem concrete_norm_bump_pos : 0 < ‖bump ℝ ℂ (5 / 2 : ℝ) 1‖ := by
  rw [concrete_norm_bump]; positivity

/-- The `L∞` Fourier multiplier is a genuine bounded operator on the concrete `H^{5/2}(ℝ;ℂ)`,
for a symbol on which the Mathlib `fourierMultiplierCLM` is identically zero. -/
theorem concrete_leray_operator :
    ¬ (lerayComponent (1 : ℝ) (1 : ℝ)).HasTemperateGrowth ∧
    TemperedDistribution.fourierMultiplierCLM ℂ (lerayComponent (1 : ℝ) (1 : ℝ))
      = (0 : 𝓢'(ℝ, ℂ) →L[ℂ] 𝓢'(ℝ, ℂ)) ∧
    ‖fourierMultiplierSobolevCLM ℝ ℂ (5 / 2 : ℝ) (lerayComponentL2 (1 : ℝ) (1 : ℝ))‖
      ≤ ‖lerayComponentL2 (1 : ℝ) (1 : ℝ)‖ ∧
    Nontrivial (Hs ℝ ℂ (5 / 2 : ℝ)) :=
  fourierMultiplierSobolevCLM_leray one_ne_zero (5 / 2 : ℝ)

end TamesisLab.Foundations.SobolevSpace

open TamesisLab.Foundations.SobolevSpace TamesisLab.Foundations.SobolevSpace.Hs

#print axioms TamesisLab.Foundations.SobolevSpace.sobolevSubmodule
#print axioms TamesisLab.Foundations.SobolevSpace.Hs
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.instAddCommGroup
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.instModule
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.range_toDist
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.toL2_eq
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.toL2_injective
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.toL2_surjective
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.instNormedAddCommGroup
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.instNormedSpace
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.toL2ₗᵢ
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.instCompleteSpace
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.norm_eq_of_besselPotential
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.besselPotential_toDist_bump
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.norm_bump
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.norm_bump_pos
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.bump_ne_zero
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.nontrivial_witness
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.instNontrivial
#print axioms TamesisLab.Foundations.SobolevSpace.concrete_Hs_nontrivial
#print axioms TamesisLab.Foundations.SobolevSpace.concrete_norm_bump
#print axioms TamesisLab.Foundations.SobolevSpace.concrete_norm_bump_pos
#print axioms TamesisLab.Foundations.SobolevSpace.concrete_leray_operator
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.fourierMultiplierSobolevCLM
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.norm_fourierMultiplierSobolevCLM_le
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.besselPotential_toDist_fourierMultiplierSobolevCLM
#print axioms TamesisLab.Foundations.SobolevSpace.Hs.fourierMultiplierSobolevCLM_leray
