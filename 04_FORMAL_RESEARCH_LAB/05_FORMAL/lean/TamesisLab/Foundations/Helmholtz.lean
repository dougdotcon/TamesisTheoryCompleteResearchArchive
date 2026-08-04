/-
Probe HZ : LP-GAP-003 -- the Helmholtz decomposition `Id - P = ∇Δ⁻¹div`,
first at the level of the Fourier SYMBOL, then at the level of the OPERATOR on `L²`.
Builds on the versioned `TamesisLab.Foundations.LerayProjector` (namespace `TamesisProbe`)
and `TamesisLab.Foundations.LerayOrthogonal`.
-/
import TamesisLab.Foundations.LerayOrthogonal

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 4000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.Helmholtz

open TamesisProbe
open TamesisLab.Foundations.FourierMultiplierL2
open TamesisLab.Foundations.LerayOrthogonal

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable {n : ℕ}

/-- Scalar `L²` on `E`. `abbrev` on purpose: `volume_tac` is flaky inside `Lp (α := E) F 2`. -/
abbrev ScalL2 (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] : Type _ :=
  Lp ℂ 2 (volume : Measure E)

/-! ## Step H1 : the LONGITUDINAL symbol `Q(ξ)_{jk} = ξ_j ξ_k / ‖ξ‖²`. -/

/-- Real entries of the complementary (longitudinal / gradient) symbol. -/
def qMatrixR (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) : ℝ :=
  inner ℝ x (b j) * inner ℝ x (b k) / ‖x‖ ^ 2

/-- Complex form of the longitudinal symbol. -/
def qMatrix (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) : ℂ :=
  ((qMatrixR b x j k : ℝ) : ℂ)

/-- `Q = δ − P` at the level of the real symbol. -/
theorem qMatrixR_eq_sub (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    qMatrixR b x j k = (if j = k then (1 : ℝ) else 0) - lerayMatrixR b x j k := by
  simp only [qMatrixR, lerayMatrixR]
  ring

/-- `P = δ − Q`. -/
theorem lerayMatrixR_eq_sub (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    lerayMatrixR b x j k = (if j = k then (1 : ℝ) else 0) - qMatrixR b x j k := by
  simp only [qMatrixR, lerayMatrixR]

theorem qMatrix_eq (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    qMatrix b x j k = (if j = k then 1 else 0) - lerayMatrix b x j k := by
  have h : qMatrixR b x j k = (if j = k then (1 : ℝ) else 0) - lerayMatrixR b x j k :=
    qMatrixR_eq_sub b x j k
  simp only [qMatrix, lerayMatrix, h, Complex.ofReal_sub,
    apply_ite (fun r : ℝ => (r : ℂ)), Complex.ofReal_one, Complex.ofReal_zero]

/-! ## Step H2 : algebra of the longitudinal symbol. -/

/-- Parseval, general form: `∑_k ξ_k v_k = ⟪v, ξ⟫`. -/
theorem sum_inner_mul_inner_real (b : OrthonormalBasis (Fin n) ℝ E) (x v : E) :
    ∑ k, inner ℝ x (b k) * inner ℝ v (b k) = inner ℝ v x := by
  rw [← b.sum_inner_mul_inner v x]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [real_inner_comm (b k) x]
  ring

/-- The longitudinal symbol is symmetric. -/
theorem qMatrixR_symm (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    qMatrixR b x j k = qMatrixR b x k j := by
  simp only [qMatrixR]
  ring

/-- **RANK ONE.** `Q(ξ) = u ⊗ u` with `u = ξ/‖ξ‖` the unit vector in the direction `ξ`. -/
theorem qMatrixR_rank_one (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    qMatrixR b x j k = (inner ℝ x (b j) / ‖x‖) * (inner ℝ x (b k) / ‖x‖) := by
  simp only [qMatrixR]
  rw [div_mul_div_comm, ← pow_two]

/-- **IDEMPOTENCE** of the longitudinal symbol : `Q(ξ)² = Q(ξ)`. -/
theorem qMatrixR_idem (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0) (j l : Fin n) :
    ∑ k, qMatrixR b x j k * qMatrixR b x k l = qMatrixR b x j l := by
  have hN : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hx)
  have hS : ∑ k, inner ℝ x (b k) * inner ℝ x (b k) = ‖x‖ ^ 2 := sum_inner_sq b x
  have hterm : ∀ k : Fin n, qMatrixR b x j k * qMatrixR b x k l
      = inner ℝ x (b j) * inner ℝ x (b l) / (‖x‖ ^ 2 * ‖x‖ ^ 2)
          * (inner ℝ x (b k) * inner ℝ x (b k)) := by
    intro k
    simp only [qMatrixR]
    ring
  calc ∑ k, qMatrixR b x j k * qMatrixR b x k l
      = ∑ k, inner ℝ x (b j) * inner ℝ x (b l) / (‖x‖ ^ 2 * ‖x‖ ^ 2)
          * (inner ℝ x (b k) * inner ℝ x (b k)) :=
        Finset.sum_congr rfl fun k _ => hterm k
    _ = inner ℝ x (b j) * inner ℝ x (b l) / (‖x‖ ^ 2 * ‖x‖ ^ 2) * ‖x‖ ^ 2 := by
        rw [← Finset.mul_sum, hS]
    _ = qMatrixR b x j l := by
        simp only [qMatrixR]
        field_simp

/-- **TRACE ONE** : `Q(ξ)` is a rank-one projection. -/
theorem trace_qMatrixR (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0) :
    ∑ j, qMatrixR b x j j = 1 := by
  have hN : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hx)
  simp only [qMatrixR]
  rw [← Finset.sum_div, sum_inner_sq b x]
  exact div_self hN

/-! ## Step H3 : THE POINT. `Q(ξ) v` is the component of `v` along `ξ`. -/

/-- **`Q(ξ)` PROJECTS ONTO THE DIRECTION `ξ`.**
`∑_k Q(ξ)_{jk} v_k = (⟪v, ξ⟫ / ‖ξ‖²) ξ_j`, i.e. `Q(ξ) v` is the longitudinal
(gradient) part of `v`. This is `∇Δ⁻¹div` on the Fourier side. -/
theorem qMatrixR_apply_vec (b : OrthonormalBasis (Fin n) ℝ E) (x v : E) (j : Fin n) :
    ∑ k, qMatrixR b x j k * inner ℝ v (b k)
      = inner ℝ v x / ‖x‖ ^ 2 * inner ℝ x (b j) := by
  have hS : ∑ k, inner ℝ x (b k) * inner ℝ v (b k) = inner ℝ v x :=
    sum_inner_mul_inner_real b x v
  have hterm : ∀ k : Fin n, qMatrixR b x j k * inner ℝ v (b k)
      = inner ℝ x (b j) / ‖x‖ ^ 2 * (inner ℝ x (b k) * inner ℝ v (b k)) := by
    intro k
    simp only [qMatrixR]
    ring
  simp only [hterm]
  rw [← Finset.mul_sum, hS]
  ring

/-- `Q(ξ) ξ = ξ` : the longitudinal projector fixes the frequency direction. -/
theorem qMatrixR_apply_inner (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0)
    (j : Fin n) : ∑ k, qMatrixR b x j k * inner ℝ x (b k) = inner ℝ x (b j) := by
  have hN : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hx)
  rw [qMatrixR_apply_vec b x x j, real_inner_self_eq_norm_sq]
  field_simp

/-- **HELMHOLTZ AT THE SYMBOL LEVEL.** `P(ξ) v + Q(ξ) v = v` for every `ξ` and `v`. -/
theorem helmholtz_symbol (b : OrthonormalBasis (Fin n) ℝ E) (x v : E) (j : Fin n) :
    (∑ k, lerayMatrixR b x j k * inner ℝ v (b k))
      + (∑ k, qMatrixR b x j k * inner ℝ v (b k)) = inner ℝ v (b j) := by
  rw [← Finset.sum_add_distrib]
  have hterm : ∀ k : Fin n, lerayMatrixR b x j k * inner ℝ v (b k)
      + qMatrixR b x j k * inner ℝ v (b k)
      = (if j = k then (1 : ℝ) else 0) * inner ℝ v (b k) := by
    intro k
    simp only [qMatrixR, lerayMatrixR]
    ring
  simp only [hterm]
  simp

/-- The transverse (solenoidal) part of `v` in closed form. -/
theorem lerayMatrixR_apply_vec (b : OrthonormalBasis (Fin n) ℝ E) (x v : E) (j : Fin n) :
    ∑ k, lerayMatrixR b x j k * inner ℝ v (b k)
      = inner ℝ v (b j) - inner ℝ v x / ‖x‖ ^ 2 * inner ℝ x (b j) := by
  have h := helmholtz_symbol b x v j
  have h2 := qMatrixR_apply_vec b x v j
  linarith

/-- `P(ξ) Q(ξ) = 0`. -/
theorem lerayMatrixR_mul_qMatrixR (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0)
    (j l : Fin n) : ∑ k, lerayMatrixR b x j k * qMatrixR b x k l = 0 := by
  have hterm : ∀ k : Fin n, lerayMatrixR b x j k * qMatrixR b x k l
      = (lerayMatrixR b x j k * inner ℝ x (b k)) * (inner ℝ x (b l) / ‖x‖ ^ 2) := by
    intro k
    simp only [qMatrixR]
    ring
  simp only [hterm]
  rw [← Finset.sum_mul, lerayMatrixR_apply_inner b hx j, zero_mul]

/-- `Q(ξ) P(ξ) = 0`. -/
theorem qMatrixR_mul_lerayMatrixR (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0)
    (j l : Fin n) : ∑ k, qMatrixR b x j k * lerayMatrixR b x k l = 0 := by
  have h := lerayMatrixR_mul_qMatrixR b hx l j
  rw [← h]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [qMatrixR_symm b x j k, lerayMatrixR_symm b x k l]
  ring

/-! ## Step H3' : the symbol of `∇ Δ⁻¹ div` IS `Q`. -/

/-- Symbol of `∂_j` (component `j` of `∇`) : `i ξ_j`. -/
def gradSymbol (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j : Fin n) : ℂ :=
  Complex.I * ((inner ℝ x (b j) : ℝ) : ℂ)

/-- Symbol of `div` contracted against the component `k` : `i ξ_k`. -/
def divSymbol (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (k : Fin n) : ℂ :=
  Complex.I * ((inner ℝ x (b k) : ℝ) : ℂ)

/-- Symbol of `Δ⁻¹` : `-1/‖ξ‖²`. -/
def invLaplaceSymbol (x : E) : ℂ := -1 / ((‖x‖ ^ 2 : ℝ) : ℂ)

/-- **`∇ Δ⁻¹ div` HAS SYMBOL `ξ_j ξ_k / ‖ξ‖²`.**
`(i ξ_j) · (−1/‖ξ‖²) · (i ξ_k) = ξ_j ξ_k / ‖ξ‖²`, because `i² = −1` cancels the sign
of the inverse Laplacian. -/
theorem gradInvLapDiv_eq_qMatrix (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    gradSymbol b x j * invLaplaceSymbol x * divSymbol b x k = qMatrix b x j k := by
  have hI : Complex.I * Complex.I = -1 := Complex.I_mul_I
  have hq : qMatrix b x j k
      = ((inner ℝ x (b j) : ℝ) : ℂ) * ((inner ℝ x (b k) : ℝ) : ℂ)
          / ((‖x‖ ^ 2 : ℝ) : ℂ) := by
    simp only [qMatrix, qMatrixR, Complex.ofReal_div, Complex.ofReal_mul]
  rw [hq, gradSymbol, divSymbol, invLaplaceSymbol]
  calc Complex.I * ((inner ℝ x (b j) : ℝ) : ℂ) * (-1 / ((‖x‖ ^ 2 : ℝ) : ℂ))
        * (Complex.I * ((inner ℝ x (b k) : ℝ) : ℂ))
      = (Complex.I * Complex.I) *
          (-(((inner ℝ x (b j) : ℝ) : ℂ) * ((inner ℝ x (b k) : ℝ) : ℂ)
            / ((‖x‖ ^ 2 : ℝ) : ℂ))) := by ring
    _ = ((inner ℝ x (b j) : ℝ) : ℂ) * ((inner ℝ x (b k) : ℝ) : ℂ)
          / ((‖x‖ ^ 2 : ℝ) : ℂ) := by rw [hI]; ring

/-- **`Id − P = ∇ Δ⁻¹ div` AT THE SYMBOL LEVEL, applied to a vector.** -/
theorem gradInvLapDiv_apply_vec (b : OrthonormalBasis (Fin n) ℝ E) (x v : E) (j : Fin n) :
    ∑ k, (gradSymbol b x j * invLaplaceSymbol x * divSymbol b x k)
        * ((inner ℝ v (b k) : ℝ) : ℂ)
      = ((inner ℝ v x / ‖x‖ ^ 2 * inner ℝ x (b j) : ℝ) : ℂ) := by
  have h : ∀ k : Fin n, (gradSymbol b x j * invLaplaceSymbol x * divSymbol b x k)
      * ((inner ℝ v (b k) : ℝ) : ℂ)
      = ((qMatrixR b x j k * inner ℝ v (b k) : ℝ) : ℂ) := by
    intro k
    rw [gradInvLapDiv_eq_qMatrix]
    simp only [qMatrix, Complex.ofReal_mul]
  simp only [h]
  rw [← Complex.ofReal_sum, qMatrixR_apply_vec]

/-! ## Step H4 : the complementary operator `Q = Id − P` on `L²` vector fields. -/

/-- The Fourier multiplier `Q = Id − P` on `L²` vector fields. -/
def qOpL2 (b : OrthonormalBasis (Fin n) ℝ E) : (VecL2 E n) →L[ℂ] (VecL2 E n) :=
  ContinuousLinearMap.id ℂ (VecL2 E n) - lerayOpL2 b

theorem qOpL2_apply (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    qOpL2 b f = f - lerayOpL2 b f := by
  simp [qOpL2]

/-- **HELMHOLTZ AT THE OPERATOR LEVEL (decomposition).** `P f + Q f = f`. -/
theorem lerayOpL2_add_qOpL2 (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    lerayOpL2 b f + qOpL2 b f = f := by
  rw [qOpL2_apply]
  abel

/-- **`P ∘ Q = 0`.** -/
theorem lerayOpL2_comp_qOpL2 [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    (lerayOpL2 b) ∘L (qOpL2 b) = 0 := by
  refine ContinuousLinearMap.ext fun f => ?_
  simp only [ContinuousLinearMap.coe_comp', Function.comp_apply,
    ContinuousLinearMap.zero_apply]
  rw [qOpL2_apply, map_sub, lerayOpL2_apply_idem, sub_self]

/-- **`Q ∘ P = 0`.** -/
theorem qOpL2_comp_lerayOpL2 [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    (qOpL2 b) ∘L (lerayOpL2 b) = 0 := by
  refine ContinuousLinearMap.ext fun f => ?_
  simp only [ContinuousLinearMap.coe_comp', Function.comp_apply,
    ContinuousLinearMap.zero_apply]
  rw [qOpL2_apply, lerayOpL2_apply_idem, sub_self]

/-- **`Q` is idempotent.** -/
theorem qOpL2_idem [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    (qOpL2 b) ∘L (qOpL2 b) = qOpL2 b := by
  refine ContinuousLinearMap.ext fun f => ?_
  simp only [ContinuousLinearMap.coe_comp', Function.comp_apply]
  rw [qOpL2_apply (f := qOpL2 b f), qOpL2_apply (f := f), map_sub, lerayOpL2_apply_idem,
    sub_self, sub_zero]

/-- **`Q` is symmetric.** -/
theorem inner_qOpL2_symm (b : OrthonormalBasis (Fin n) ℝ E) (f g : VecL2 E n) :
    inner ℂ (qOpL2 b f) g = inner ℂ f (qOpL2 b g) := by
  rw [qOpL2_apply, qOpL2_apply, inner_sub_left, inner_sub_right, inner_lerayOpL2_symm]

/-- **`Q` is self-adjoint.** -/
theorem adjoint_qOpL2 (b : OrthonormalBasis (Fin n) ℝ E) :
    ContinuousLinearMap.adjoint (qOpL2 b) = qOpL2 b :=
  ((ContinuousLinearMap.eq_adjoint_iff (qOpL2 b) (qOpL2 b)).mpr (inner_qOpL2_symm b)).symm

theorem isSelfAdjoint_qOpL2 (b : OrthonormalBasis (Fin n) ℝ E) :
    IsSelfAdjoint (qOpL2 b) :=
  ContinuousLinearMap.isSelfAdjoint_iff'.mpr (adjoint_qOpL2 b)

/-- **PYTHAGORAS FOR THE HELMHOLTZ SPLITTING.** `‖f‖² = ‖P f‖² + ‖Q f‖²`. -/
theorem norm_sq_helmholtz [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    ‖f‖ ^ 2 = ‖lerayOpL2 b f‖ ^ 2 + ‖qOpL2 b f‖ ^ 2 := by
  rw [qOpL2_apply]
  exact norm_sq_lerayOpL2_pythagoras b f

theorem norm_qOpL2_apply_le [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    ‖qOpL2 b f‖ ≤ ‖f‖ := by
  have h := norm_sq_helmholtz b f
  nlinarith [sq_nonneg ‖lerayOpL2 b f‖, norm_nonneg (qOpL2 b f), norm_nonneg f]

/-- **`Q` is a contraction.** -/
theorem norm_qOpL2_le_one [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    ‖qOpL2 b‖ ≤ 1 :=
  ContinuousLinearMap.opNorm_le_bound _ zero_le_one fun f => by
    simpa using norm_qOpL2_apply_le b f

/-! ## Step H5 : `Q` IS the Fourier multiplier with symbol `ξ_jξ_k/‖ξ‖²`. -/

theorem measurable_qMatrix (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    Measurable (fun x : E => qMatrix b x j k) := by
  simp only [qMatrix_eq]
  exact measurable_const.sub (measurable_lerayMatrix b j k)

theorem norm_qMatrix_le (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    ‖qMatrix b x j k‖ ≤ 3 := by
  rw [qMatrix_eq]
  have h1 : ‖(if j = k then (1 : ℂ) else 0)‖ ≤ 1 := by split <;> simp
  have h2 : ‖lerayMatrix b x j k‖ ≤ 2 := norm_lerayMatrix_le b x j k
  calc ‖(if j = k then (1 : ℂ) else 0) - lerayMatrix b x j k‖
      ≤ ‖(if j = k then (1 : ℂ) else 0)‖ + ‖lerayMatrix b x j k‖ := norm_sub_le _ _
    _ ≤ 1 + 2 := add_le_add h1 h2
    _ = 3 := by norm_num

/-- Each longitudinal entry as an element of `L∞`. -/
def qEntryL2 (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    Lp ℂ ∞ (volume : Measure E) :=
  ofBounded (measurable_qMatrix b j k).aestronglyMeasurable 3
    (fun x => norm_qMatrix_le b x j k)

theorem coeFn_qEntryL2 (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    ⇑(qEntryL2 b j k) =ᵐ[(volume : Measure E)] fun x => qMatrix b x j k := by
  unfold qEntryL2 ofBounded
  exact MemLp.coeFn_toLp _

variable (E) in
/-- The constant symbol `1` as an element of `L∞`. -/
def oneL2 : Lp ℂ ∞ (volume : Measure E) :=
  ofBounded (g := fun _ : E => (1 : ℂ)) measurable_const.aestronglyMeasurable 1
    (fun _ => by norm_num)

theorem coeFn_oneL2 : ⇑(oneL2 E) =ᵐ[(volume : Measure E)] fun _ => (1 : ℂ) := by
  unfold oneL2 ofBounded
  exact MemLp.coeFn_toLp _

theorem oneL2_smul (f : ScalL2 E) : (oneL2 E • f : ScalL2 E) = f := by
  rw [Lp.ext_iff]
  filter_upwards [Lp.coeFn_lpSMul (r := 2) (oneL2 E) f, coeFn_oneL2 (E := E)] with x h1 h2
  rw [h1]
  simp only [Pi.smul_apply', h2, one_smul]

/-- The multiplier with symbol `1` is the identity. -/
theorem fourierMulL2_oneL2 :
    fourierMulL2 ℂ (oneL2 E) = ContinuousLinearMap.id ℂ (ScalL2 E) := by
  refine ContinuousLinearMap.ext fun f => ?_
  rw [fourierMulL2_apply, mulL2_apply, oneL2_smul, FourierTransform.fourierInv_fourier_eq]
  rfl

/-- **`P + Q = δ` AT THE LEVEL OF THE `L∞` SYMBOLS.** -/
theorem lerayEntryL2_add_qEntryL2 (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    lerayEntryL2 b j k + qEntryL2 b j k = (if j = k then oneL2 E else 0) := by
  by_cases h : j = k
  · rw [if_pos h, Lp.ext_iff]
    filter_upwards [Lp.coeFn_add (lerayEntryL2 b j k) (qEntryL2 b j k),
      coeFn_lerayEntryL2 b j k, coeFn_qEntryL2 b j k, coeFn_oneL2 (E := E)]
      with x hadd hL hQ hone
    rw [hadd, hone]
    simp only [Pi.add_apply, hL, hQ, qMatrix_eq, if_pos h]
    ring
  · rw [if_neg h, Lp.ext_iff]
    filter_upwards [Lp.coeFn_add (lerayEntryL2 b j k) (qEntryL2 b j k),
      coeFn_lerayEntryL2 b j k, coeFn_qEntryL2 b j k,
      Lp.coeFn_zero ℂ ∞ (volume : Measure E)] with x hadd hL hQ hzero
    rw [hadd, hzero]
    simp only [Pi.add_apply, Pi.zero_apply, hL, hQ, qMatrix_eq, if_neg h]
    ring

/-- **`Id − P = ∇Δ⁻¹div` AT THE OPERATOR LEVEL.**
The `q`-th coordinate of `Q f` is exactly `∑_k M[ξ_qξ_k/‖ξ‖²] f_k`, i.e. `Q` is the
matrix Fourier multiplier whose symbol is the longitudinal projector `ξ_jξ_k/‖ξ‖²`. -/
theorem coordProj_qOpL2 (b : OrthonormalBasis (Fin n) ℝ E) (q : Fin n) (f : VecL2 E n) :
    (coordProj E q) (qOpL2 b f)
      = ∑ k : Fin n, (fourierMulL2 ℂ (qEntryL2 b q k)) ((coordProj E k) f) := by
  have hsplit : ∀ k : Fin n,
      (fourierMulL2 ℂ (lerayEntryL2 b q k)) ((coordProj E k) f)
        + (fourierMulL2 ℂ (qEntryL2 b q k)) ((coordProj E k) f)
      = (if q = k then (coordProj E q) f else 0) := by
    intro k
    rw [← ContinuousLinearMap.add_apply, ← fourierMulL2_add, lerayEntryL2_add_qEntryL2]
    by_cases h : q = k
    · subst h
      simp [fourierMulL2_oneL2]
    · simp [h, fourierMulL2_zero]
  have hsum : ∑ k : Fin n,
      ((fourierMulL2 ℂ (lerayEntryL2 b q k)) ((coordProj E k) f)
        + (fourierMulL2 ℂ (qEntryL2 b q k)) ((coordProj E k) f))
      = (coordProj E q) f := by
    simp only [hsplit]
    simp
  rw [Finset.sum_add_distrib] at hsum
  rw [qOpL2_apply, map_sub, coordProj_lerayOpL2, ← hsum]
  abel

/-! ## Step H6 : ANTI-VACUITY of the complement. `Q ≠ 0`, so the splitting is
nontrivial on BOTH sides. -/

theorem fourierMulL2_eq_zero_of_qOpL2_eq_zero (b : OrthonormalBasis (Fin n) ℝ E)
    (h : qOpL2 b = 0) (q j : Fin n) (u : ScalL2 E) :
    fourierMulL2 ℂ (qEntryL2 b q j) u = 0 := by
  have h1 := coordProj_qOpL2 b q (coordIncl E j u)
  rw [h] at h1
  simp only [ContinuousLinearMap.zero_apply, map_zero] at h1
  have h2 : ∑ k : Fin n,
      (fourierMulL2 ℂ (qEntryL2 b q k)) ((coordProj E k) ((coordIncl E j) u))
      = fourierMulL2 ℂ (qEntryL2 b q j) u := by
    rw [Finset.sum_eq_single j]
    · rw [coordProj_coordIncl, if_pos rfl]
    · intro k _ hkj
      rw [coordProj_coordIncl, if_neg (Ne.symm hkj), map_zero]
    · intro hj
      exact absurd (Finset.mem_univ j) hj
  rw [← h2, ← h1]

/-- **ANTI-VACUITY.** The longitudinal projector `Q = Id − P` is a NONZERO operator:
its symbol has trace `1` at every nonzero frequency. -/
theorem qOpL2_ne_zero [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    qOpL2 b ≠ 0 := by
  intro h
  have hz : ∀ p j : Fin n, qEntryL2 b p j = 0 := fun p j =>
    eq_zero_of_smul_L2_eq_zero _ (smul_eq_zero_of_fourierMulL2_eq_zero _
      (fourierMulL2_eq_zero_of_qOpL2_eq_zero b h p j))
  have hcoe : ∀ᵐ x ∂(volume : Measure E), ∀ j : Fin n, qMatrix b x j j = 0 := by
    rw [ae_all_iff]
    intro j
    have hz2 : ⇑(qEntryL2 b j j) =ᵐ[(volume : Measure E)] (0 : E → ℂ) := by
      rw [hz j j]; exact Lp.coeFn_zero ℂ ∞ (volume : Measure E)
    filter_upwards [coeFn_qEntryL2 b j j, hz2] with x h1 h2
    rw [← h1]
    simpa using h2
  have hne0 : ∀ᵐ x ∂(volume : Measure E), x ≠ (0 : E) := by
    have h0 : (volume : Measure E) {(0 : E)} = 0 := measure_singleton _
    rw [ae_iff]
    simpa using h0
  obtain ⟨x, hx1, hx2⟩ := (hcoe.and hne0).exists
  have htr := trace_qMatrixR b hx2
  have hzero : ∑ j : Fin n, qMatrixR b x j j = 0 :=
    Finset.sum_eq_zero fun j _ => by
      have hj := hx1 j
      simpa [qMatrix] using hj
  rw [hzero] at htr
  exact absurd htr (by norm_num)

/-! ## Step H7 : FINAL PACKAGE. -/

/-- **HELMHOLTZ / LERAY DECOMPOSITION PACKAGE.**
`L²(E; ℂⁿ) = ker(div) ⊕ ran(∇)` : `P` and `Q = Id − P` are complementary orthogonal
projections, `Q` is the Fourier multiplier with symbol `ξ_jξ_k/‖ξ‖²` = the symbol of
`∇Δ⁻¹div`, and both summands are nonzero when `2 ≤ n`. -/
theorem helmholtz_package [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    (∀ f : VecL2 E n, lerayOpL2 b f + qOpL2 b f = f) ∧
    ((lerayOpL2 b) ∘L (qOpL2 b) = 0) ∧
    ((qOpL2 b) ∘L (lerayOpL2 b) = 0) ∧
    ((qOpL2 b) ∘L (qOpL2 b) = qOpL2 b) ∧
    ContinuousLinearMap.adjoint (qOpL2 b) = qOpL2 b ∧
    IsSelfAdjoint (qOpL2 b) ∧
    ‖qOpL2 b‖ ≤ 1 ∧
    (∀ f : VecL2 E n, ‖f‖ ^ 2 = ‖lerayOpL2 b f‖ ^ 2 + ‖qOpL2 b f‖ ^ 2) ∧
    (∀ q : Fin n, ∀ f : VecL2 E n, (coordProj E q) (qOpL2 b f)
        = ∑ k : Fin n, (fourierMulL2 ℂ (qEntryL2 b q k)) ((coordProj E k) f)) ∧
    (∀ x : E, ∀ j k : Fin n,
        gradSymbol b x j * invLaplaceSymbol x * divSymbol b x k = qMatrix b x j k) ∧
    qOpL2 b ≠ 0 ∧
    (2 ≤ n → lerayOpL2 b ≠ 0) :=
  ⟨lerayOpL2_add_qOpL2 b, lerayOpL2_comp_qOpL2 b, qOpL2_comp_lerayOpL2 b, qOpL2_idem b,
   adjoint_qOpL2 b, isSelfAdjoint_qOpL2 b, norm_qOpL2_le_one b, norm_sq_helmholtz b,
   fun q f => coordProj_qOpL2 b q f, fun x j k => gradInvLapDiv_eq_qMatrix b x j k,
   qOpL2_ne_zero b, fun hn => lerayOpL2_ne_zero b hn⟩

/-! ## Step H8 : POSITIVE INSTANCE on `ℝ³`. Both halves of the splitting are nonzero. -/

section Concrete

/-- A concrete test vector field value : `v = e₀ + e₁`, neither parallel nor orthogonal
to the test frequency `ξ = e₀`. -/
def v3 : E3 := b3 0 + b3 1

theorem inner_v3_b3 (j : Fin 3) :
    inner ℝ v3 (b3 j)
      = (if (0 : Fin 3) = j then (1 : ℝ) else 0)
        + (if (1 : Fin 3) = j then (1 : ℝ) else 0) := by
  simp only [v3, inner_add_left, inner_basis]

theorem norm_b3_zero : ‖(b3 0 : E3)‖ = 1 := b3.orthonormal.1 0

theorem b3_zero_ne_zero : (b3 0 : E3) ≠ 0 := by
  intro h
  have := norm_b3_zero
  rw [h, norm_zero] at this
  exact zero_ne_one this

/-- `Q(e₀) v = e₀ ≠ 0` : the LONGITUDINAL part of `v` is nonzero. -/
theorem q_component_v3 : ∑ k, qMatrixR b3 (b3 0) 0 k * inner ℝ v3 (b3 k) = 1 := by
  rw [qMatrixR_apply_vec, inner_v3_b3, inner_basis, norm_b3_zero]
  norm_num

/-- `P(e₀) v = e₁ ≠ 0` : the TRANSVERSE part of `v` is nonzero. -/
theorem p_component_v3 : ∑ k, lerayMatrixR b3 (b3 0) 1 k * inner ℝ v3 (b3 k) = 1 := by
  rw [lerayMatrixR_apply_vec, inner_v3_b3, inner_v3_b3, inner_basis, norm_b3_zero]
  norm_num

/-- **POSITIVE INSTANCE ON `ℝ³`.** With `ξ = e₀` and `v = e₀ + e₁` the Helmholtz
splitting is genuinely nontrivial on BOTH sides: the longitudinal part `Q(ξ)v` and the
transverse part `P(ξ)v` are both nonzero, they add up to `v`, they are mutually
annihilating, and at the operator level both `P` and `Q` are nonzero orthogonal
projections summing to the identity. -/
theorem positive_instance_helmholtz_R3 :
    ((b3 0 : E3) ≠ 0) ∧
    (∑ k, qMatrixR b3 (b3 0) 0 k * inner ℝ v3 (b3 k)) ≠ 0 ∧
    (∑ k, lerayMatrixR b3 (b3 0) 1 k * inner ℝ v3 (b3 k)) ≠ 0 ∧
    (∀ j : Fin 3, (∑ k, lerayMatrixR b3 (b3 0) j k * inner ℝ v3 (b3 k))
        + (∑ k, qMatrixR b3 (b3 0) j k * inner ℝ v3 (b3 k)) = inner ℝ v3 (b3 j)) ∧
    (∀ j l : Fin 3, ∑ k, lerayMatrixR b3 (b3 0) j k * qMatrixR b3 (b3 0) k l = 0) ∧
    (∀ j l : Fin 3, ∑ k, qMatrixR b3 (b3 0) j k * lerayMatrixR b3 (b3 0) k l = 0) ∧
    (∑ j, qMatrixR b3 (b3 0) j j = 1) ∧
    (∀ j l : Fin 3, ∑ k, qMatrixR b3 (b3 0) j k * qMatrixR b3 (b3 0) k l
        = qMatrixR b3 (b3 0) j l) ∧
    (∀ x : E3, ∀ j k : Fin 3,
        gradSymbol b3 x j * invLaplaceSymbol x * divSymbol b3 x k = qMatrix b3 x j k) ∧
    (∀ f : VecL2 E3 3, lerayOpL2 b3 f + qOpL2 b3 f = f) ∧
    ((lerayOpL2 b3) ∘L (qOpL2 b3) = 0) ∧
    (lerayOpL2 b3 ≠ 0) ∧
    (qOpL2 b3 ≠ 0) ∧
    ‖qOpL2 b3‖ ≤ 1 ∧
    (∀ f : VecL2 E3 3, ‖f‖ ^ 2 = ‖lerayOpL2 b3 f‖ ^ 2 + ‖qOpL2 b3 f‖ ^ 2) := by
  refine ⟨b3_zero_ne_zero, ?_, ?_, fun j => helmholtz_symbol b3 (b3 0) v3 j,
    fun j l => lerayMatrixR_mul_qMatrixR b3 b3_zero_ne_zero j l,
    fun j l => qMatrixR_mul_lerayMatrixR b3 b3_zero_ne_zero j l,
    trace_qMatrixR b3 b3_zero_ne_zero,
    fun j l => qMatrixR_idem b3 b3_zero_ne_zero j l,
    fun x j k => gradInvLapDiv_eq_qMatrix b3 x j k,
    lerayOpL2_add_qOpL2 b3, lerayOpL2_comp_qOpL2 b3,
    lerayOpL2_ne_zero b3 (by norm_num), qOpL2_ne_zero b3, norm_qOpL2_le_one b3,
    norm_sq_helmholtz b3⟩
  · rw [q_component_v3]; norm_num
  · rw [p_component_v3]; norm_num

end Concrete

end TamesisLab.Foundations.Helmholtz

#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_eq_sub
#print axioms TamesisLab.Foundations.Helmholtz.lerayMatrixR_eq_sub
#print axioms TamesisLab.Foundations.Helmholtz.qMatrix_eq
#print axioms TamesisLab.Foundations.Helmholtz.sum_inner_mul_inner_real
#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_symm
#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_rank_one
#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_idem
#print axioms TamesisLab.Foundations.Helmholtz.trace_qMatrixR
#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_apply_vec
#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_apply_inner
#print axioms TamesisLab.Foundations.Helmholtz.helmholtz_symbol
#print axioms TamesisLab.Foundations.Helmholtz.lerayMatrixR_apply_vec
#print axioms TamesisLab.Foundations.Helmholtz.lerayMatrixR_mul_qMatrixR
#print axioms TamesisLab.Foundations.Helmholtz.qMatrixR_mul_lerayMatrixR
#print axioms TamesisLab.Foundations.Helmholtz.gradInvLapDiv_eq_qMatrix
#print axioms TamesisLab.Foundations.Helmholtz.gradInvLapDiv_apply_vec
#print axioms TamesisLab.Foundations.Helmholtz.qOpL2_apply
#print axioms TamesisLab.Foundations.Helmholtz.lerayOpL2_add_qOpL2
#print axioms TamesisLab.Foundations.Helmholtz.lerayOpL2_comp_qOpL2
#print axioms TamesisLab.Foundations.Helmholtz.qOpL2_comp_lerayOpL2
#print axioms TamesisLab.Foundations.Helmholtz.qOpL2_idem
#print axioms TamesisLab.Foundations.Helmholtz.inner_qOpL2_symm
#print axioms TamesisLab.Foundations.Helmholtz.adjoint_qOpL2
#print axioms TamesisLab.Foundations.Helmholtz.isSelfAdjoint_qOpL2
#print axioms TamesisLab.Foundations.Helmholtz.norm_sq_helmholtz
#print axioms TamesisLab.Foundations.Helmholtz.norm_qOpL2_apply_le
#print axioms TamesisLab.Foundations.Helmholtz.norm_qOpL2_le_one
#print axioms TamesisLab.Foundations.Helmholtz.measurable_qMatrix
#print axioms TamesisLab.Foundations.Helmholtz.norm_qMatrix_le
#print axioms TamesisLab.Foundations.Helmholtz.coeFn_qEntryL2
#print axioms TamesisLab.Foundations.Helmholtz.coeFn_oneL2
#print axioms TamesisLab.Foundations.Helmholtz.oneL2_smul
#print axioms TamesisLab.Foundations.Helmholtz.fourierMulL2_oneL2
#print axioms TamesisLab.Foundations.Helmholtz.lerayEntryL2_add_qEntryL2
#print axioms TamesisLab.Foundations.Helmholtz.coordProj_qOpL2
#print axioms TamesisLab.Foundations.Helmholtz.fourierMulL2_eq_zero_of_qOpL2_eq_zero
#print axioms TamesisLab.Foundations.Helmholtz.qOpL2_ne_zero
#print axioms TamesisLab.Foundations.Helmholtz.helmholtz_package
#print axioms TamesisLab.Foundations.Helmholtz.inner_v3_b3
#print axioms TamesisLab.Foundations.Helmholtz.q_component_v3
#print axioms TamesisLab.Foundations.Helmholtz.p_component_v3
#print axioms TamesisLab.Foundations.Helmholtz.positive_instance_helmholtz_R3
