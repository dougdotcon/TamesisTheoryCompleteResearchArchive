/-
Probe LO : LP-GAP-002 (self-adjointness) and LP-GAP-001 (optimal bound `‖P‖ ≤ 1`)
for the Leray projector `lerayOpL2` of `TamesisLab.Foundations.LerayProjector`.
-/
import TamesisLab.Foundations.LerayProjector
import Mathlib.Analysis.InnerProductSpace.Adjoint

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.LerayOrthogonal

open TamesisProbe
open TamesisLab.Foundations.FourierMultiplierL2

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable {n : ℕ}

/-- The space of `L²` vector fields on `E` with `n` complex components. -/
abbrev VecL2 (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E] (n : ℕ) : Type _ :=
  Lp (EuclideanSpace ℂ (Fin n)) 2 (volume : Measure E)

/-! ## Step L1 : multiplication by a conjugation-invariant `L∞` symbol is symmetric on `L²`. -/

section Symbol

variable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- If the `L∞` symbol `g` is a.e. real (conjugation-invariant) then multiplication by `g`
is symmetric for the `L²` inner product. -/
theorem inner_smul_Lp_symm (g : Lp ℂ ∞ (volume : Measure E))
    (hg : ∀ᵐ x ∂(volume : Measure E), (starRingEnd ℂ) (g x) = g x)
    (f h : Lp F 2 (volume : Measure E)) :
    inner ℂ (g • f : Lp F 2 (volume : Measure E)) h
      = inner ℂ f (g • h : Lp F 2 (volume : Measure E)) := by
  rw [L2.inner_def, L2.inner_def]
  refine integral_congr_ae ?_
  filter_upwards [Lp.coeFn_lpSMul (r := 2) g f, Lp.coeFn_lpSMul (r := 2) g h, hg]
    with x h1 h2 h3
  rw [h1, h2]
  simp only [Pi.smul_apply']
  rw [inner_smul_left, inner_smul_right, h3]

/-- **SYMMETRY OF THE `L²` FOURIER MULTIPLIER WITH A REAL SYMBOL.** -/
theorem inner_fourierMulL2_symm (g : Lp ℂ ∞ (volume : Measure E))
    (hg : ∀ᵐ x ∂(volume : Measure E), (starRingEnd ℂ) (g x) = g x)
    (f h : Lp F 2 (volume : Measure E)) :
    inner ℂ (fourierMulL2 F g f) h = inner ℂ f (fourierMulL2 F g h) := by
  have h1 : inner ℂ (fourierMulL2 F g f) h
      = inner ℂ (𝓕 (fourierMulL2 F g f)) (𝓕 h) := (Lp.inner_fourier_eq _ _).symm
  have h2 : inner ℂ f (fourierMulL2 F g h)
      = inner ℂ (𝓕 f) (𝓕 (fourierMulL2 F g h)) := (Lp.inner_fourier_eq _ _).symm
  rw [h1, h2, fourierMulL2_apply, fourierMulL2_apply, fourier_fourierInv_eq,
    fourier_fourierInv_eq, mulL2_apply, mulL2_apply]
  exact inner_smul_Lp_symm g hg (𝓕 f) (𝓕 h)

end Symbol

/-! ## Step L2 : the Leray symbol entries are real-valued, hence conjugation-invariant. -/

/-- The `L∞` entries of the Leray symbol are a.e. fixed by complex conjugation. -/
theorem conj_lerayEntryL2 (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    ∀ᵐ x ∂(volume : Measure E),
      (starRingEnd ℂ) (lerayEntryL2 b j k x) = lerayEntryL2 b j k x := by
  filter_upwards [coeFn_lerayEntryL2 b j k] with x hx
  rw [hx]
  simp [lerayMatrix]

/-! ## Step L3 : `coordIncl` and `coordProj` are mutually adjoint. -/

theorem inner_coordIncl_left (j : Fin n) (u : Lp ℂ 2 (volume : Measure E))
    (v : VecL2 E n) :
    inner ℂ (coordIncl E j u) v = inner ℂ u (coordProj E j v) := by
  rw [L2.inner_def, L2.inner_def]
  refine integral_congr_ae ?_
  filter_upwards [ContinuousLinearMap.coeFn_compLpL (p := 2) (μ := (volume : Measure E))
      (ContinuousLinearMap.toSpanSingleton ℂ (EuclideanSpace.single j (1 : ℂ))) u,
    ContinuousLinearMap.coeFn_compLpL (p := 2) (μ := (volume : Measure E))
      (EuclideanSpace.proj (𝕜 := ℂ) j) v] with x hx1 hx2
  have e1 : ((coordIncl E j) u) x
      = (ContinuousLinearMap.toSpanSingleton ℂ (EuclideanSpace.single j (1 : ℂ))) (u x) := hx1
  have e2 : ((coordProj E j) v) x = (EuclideanSpace.proj (𝕜 := ℂ) j) (v x) := hx2
  rw [e1, e2]
  rw [ContinuousLinearMap.toSpanSingleton_apply, inner_smul_left,
    EuclideanSpace.inner_single_left, RCLike.inner_apply']
  simp

theorem inner_coordIncl_right (j : Fin n) (v : VecL2 E n) (u : Lp ℂ 2 (volume : Measure E)) :
    inner ℂ v (coordIncl E j u) = inner ℂ (coordProj E j v) u := by
  have h := congrArg (starRingEnd ℂ) (inner_coordIncl_left j u v)
  rwa [inner_conj_symm, inner_conj_symm] at h

/-! ## Step L4 : LP-GAP-002. The Leray projector is symmetric, hence self-adjoint. -/

/-- **LP-GAP-002 (weak form).** `⟪P f, g⟫ = ⟪f, P g⟫` for the Leray projector on `L²`
vector fields. Uses only: the entries are real-valued, the Fourier transform is an `L²`
isometry, and the symbol matrix is symmetric. -/
theorem inner_lerayOpL2_symm (b : OrthonormalBasis (Fin n) ℝ E) (f g : VecL2 E n) :
    inner ℂ (lerayOpL2 b f) g = inner ℂ f (lerayOpL2 b g) := by
  have hL : inner ℂ (lerayOpL2 b f) g
      = ∑ j : Fin n, ∑ k : Fin n,
          inner ℂ ((coordProj E k) f)
            ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ((coordProj E j) g)) := by
    rw [lerayOpL2_apply, sum_inner]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [sum_inner]
    refine Finset.sum_congr rfl fun k _ => ?_
    rw [inner_coordIncl_left]
    exact inner_fourierMulL2_symm _ (conj_lerayEntryL2 b j k) _ _
  have hR : inner ℂ f (lerayOpL2 b g)
      = ∑ j : Fin n, ∑ k : Fin n,
          inner ℂ ((coordProj E j) f)
            ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ((coordProj E k) g)) := by
    rw [lerayOpL2_apply, inner_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [inner_sum]
    refine Finset.sum_congr rfl fun k _ => ?_
    rw [inner_coordIncl_right]
  rw [hL, hR]
  conv_lhs => rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun k _ => ?_
  rw [lerayEntryL2_symm b k j]

/-- **LP-GAP-002 (strong form).** The Hilbert adjoint of the Leray projector is itself. -/
theorem adjoint_lerayOpL2 (b : OrthonormalBasis (Fin n) ℝ E) :
    ContinuousLinearMap.adjoint (lerayOpL2 b) = lerayOpL2 b :=
  ((ContinuousLinearMap.eq_adjoint_iff (lerayOpL2 b) (lerayOpL2 b)).mpr
    (inner_lerayOpL2_symm b)).symm

theorem isSelfAdjoint_lerayOpL2 (b : OrthonormalBasis (Fin n) ℝ E) :
    IsSelfAdjoint (lerayOpL2 b) :=
  ContinuousLinearMap.isSelfAdjoint_iff'.mpr (adjoint_lerayOpL2 b)

/-! ## Step L5 : LP-GAP-001. The optimal bound `‖P‖ ≤ 1`. -/

theorem lerayOpL2_apply_idem [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    lerayOpL2 b (lerayOpL2 b f) = lerayOpL2 b f := by
  have h := congrArg (fun T : (VecL2 E n) →L[ℂ] (VecL2 E n) => T f) (lerayOpL2_idem b)
  simpa using h

theorem inner_self_lerayOpL2 [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    inner ℂ (lerayOpL2 b f) (lerayOpL2 b f) = inner ℂ f (lerayOpL2 b f) := by
  rw [inner_lerayOpL2_symm b f (lerayOpL2 b f), lerayOpL2_apply_idem]

/-- **LP-GAP-001, pointwise.** `‖P f‖ ≤ ‖f‖`. -/
theorem norm_lerayOpL2_apply_le_one [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E)
    (f : VecL2 E n) : ‖lerayOpL2 b f‖ ≤ ‖f‖ := by
  have hsq : ‖lerayOpL2 b f‖ ^ 2 ≤ ‖f‖ * ‖lerayOpL2 b f‖ := by
    have h1 : ‖lerayOpL2 b f‖ ^ 2 = ‖inner ℂ f (lerayOpL2 b f)‖ := by
      rw [← inner_self_lerayOpL2 b f, inner_self_eq_norm_sq_to_K]
      simp
    rw [h1]
    exact norm_inner_le_norm _ _
  rcases eq_or_lt_of_le (norm_nonneg (lerayOpL2 b f)) with hz | hpos
  · rw [← hz]; exact norm_nonneg f
  · refine le_of_mul_le_mul_right ?_ hpos
    calc ‖lerayOpL2 b f‖ * ‖lerayOpL2 b f‖ = ‖lerayOpL2 b f‖ ^ 2 := by ring
      _ ≤ ‖f‖ * ‖lerayOpL2 b f‖ := hsq

/-- **LP-GAP-001.** The Leray projector on `L²` vector fields is a CONTRACTION:
`‖P‖ ≤ 1`, replacing the previous bound `2n²`. -/
theorem norm_lerayOpL2_le_one [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    ‖lerayOpL2 b‖ ≤ 1 :=
  ContinuousLinearMap.opNorm_le_bound _ zero_le_one fun f => by
    simpa using norm_lerayOpL2_apply_le_one b f

/-- **OPTIMALITY.** The bound `1` is attained whenever the projector is nonzero. -/
theorem norm_lerayOpL2_eq_one [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E)
    (hne : lerayOpL2 b ≠ 0) : ‖lerayOpL2 b‖ = 1 := by
  refine le_antisymm (norm_lerayOpL2_le_one b) ?_
  have hpos : 0 < ‖lerayOpL2 b‖ := norm_pos_iff.mpr hne
  have h : ‖lerayOpL2 b‖ ≤ ‖lerayOpL2 b‖ * ‖lerayOpL2 b‖ := by
    conv_lhs => rw [← lerayOpL2_idem b]
    exact ContinuousLinearMap.opNorm_comp_le _ _
  nlinarith

/-! ## Step L6 : `P` is an ORTHOGONAL projection; Pythagoras. -/

/-- The range of `P` is orthogonal to the range of `1 - P`. -/
theorem inner_lerayOpL2_sub [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (f : VecL2 E n) :
    inner ℂ (lerayOpL2 b f) (f - lerayOpL2 b f) = 0 := by
  rw [inner_sub_right, inner_lerayOpL2_symm b f f, inner_self_lerayOpL2 b f, sub_self]

/-- **PYTHAGORAS.** `‖f‖² = ‖P f‖² + ‖(1 − P) f‖²`. -/
theorem norm_sq_lerayOpL2_pythagoras [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E)
    (f : VecL2 E n) :
    ‖f‖ ^ 2 = ‖lerayOpL2 b f‖ ^ 2 + ‖f - lerayOpL2 b f‖ ^ 2 := by
  have h := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero (𝕜 := ℂ)
    (lerayOpL2 b f) (f - lerayOpL2 b f) (inner_lerayOpL2_sub b f)
  have hf : lerayOpL2 b f + (f - lerayOpL2 b f) = f := by abel
  rw [hf] at h
  simp only [pow_two]
  exact h

/-- Pythagoras in the `1 - P` operator form. -/
theorem norm_sq_lerayOpL2_pythagoras_id [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E)
    (f : VecL2 E n) :
    ‖f‖ ^ 2 = ‖lerayOpL2 b f‖ ^ 2
      + ‖(ContinuousLinearMap.id ℂ (VecL2 E n) - lerayOpL2 b) f‖ ^ 2 := by
  have h : (ContinuousLinearMap.id ℂ (VecL2 E n) - lerayOpL2 b) f = f - lerayOpL2 b f := by simp
  rw [h]
  exact norm_sq_lerayOpL2_pythagoras b f

/-! ## Step L7 : ANTI-VACUITY. The projector is NOT the zero operator (for `n ≥ 2`),
so `‖P‖ = 1` is unconditional and `adjoint P = P` is not a statement about `0`. -/

/-- An `L∞` symbol that annihilates every `L²` function is `0`. -/
theorem eq_zero_of_smul_L2_eq_zero (g : Lp ℂ ∞ (volume : Measure E))
    (h : ∀ u : Lp ℂ 2 (volume : Measure E), (g • u : Lp ℂ 2 (volume : Measure E)) = 0) :
    g = 0 := by
  have key : ∀ R : ℕ, ∀ᵐ x ∂(volume : Measure E),
      x ∈ Metric.closedBall (0 : E) (R : ℝ) → g x = 0 := by
    intro R
    have hs : MeasurableSet (Metric.closedBall (0 : E) (R : ℝ)) := measurableSet_closedBall
    have hμs : (volume : Measure E) (Metric.closedBall (0 : E) (R : ℝ)) ≠ ∞ :=
      measure_closedBall_lt_top.ne
    set u : Lp ℂ 2 (volume : Measure E) := indicatorConstLp 2 hs hμs (1 : ℂ) with hu_def
    have hu : (g • u : Lp ℂ 2 (volume : Measure E)) = 0 := h u
    have h1 : ⇑(g • u : Lp ℂ 2 (volume : Measure E))
        =ᵐ[(volume : Measure E)] (0 : E → ℂ) := by
      rw [hu]; exact Lp.coeFn_zero ℂ 2 (volume : Measure E)
    have h3 : ⇑u =ᵐ[(volume : Measure E)]
        Set.indicator (Metric.closedBall (0 : E) (R : ℝ)) (fun _ => (1 : ℂ)) :=
      indicatorConstLp_coeFn
    filter_upwards [h1, Lp.coeFn_lpSMul (r := 2) g u, h3] with x hx1 hx2 hx3 hxs
    rw [hx2] at hx1
    simp only [Pi.smul_apply', smul_eq_mul] at hx1
    rw [hx3, Set.indicator_of_mem hxs, mul_one] at hx1
    simpa using hx1
  have hall : ∀ᵐ x ∂(volume : Measure E), g x = 0 := by
    filter_upwards [ae_all_iff.mpr key] with x hx
    refine hx ⌈‖x‖⌉₊ ?_
    simp only [Metric.mem_closedBall, dist_zero_right]
    exact Nat.le_ceil _
  rw [Lp.ext_iff]
  filter_upwards [hall, Lp.coeFn_zero ℂ ∞ (volume : Measure E)] with x h1 h2
  rw [h1, h2]
  rfl

/-- A Fourier multiplier that kills every `L²` function has an `L∞` symbol killing every
`L²` function (conjugate back through the Plancherel isometry). -/
theorem smul_eq_zero_of_fourierMulL2_eq_zero (g : Lp ℂ ∞ (volume : Measure E))
    (h : ∀ u : Lp ℂ 2 (volume : Measure E), fourierMulL2 ℂ g u = 0)
    (v : Lp ℂ 2 (volume : Measure E)) : (g • v : Lp ℂ 2 (volume : Measure E)) = 0 := by
  have h1 := h (𝓕⁻ v)
  rw [fourierMulL2_apply, mulL2_apply, fourier_fourierInv_eq] at h1
  have hnorm : ‖(g • v : Lp ℂ 2 (volume : Measure E))‖ = 0 := by
    rw [← norm_fourierInv_eq (g • v : Lp ℂ 2 (volume : Measure E)), h1, norm_zero]
  exact norm_eq_zero.mp hnorm

/-- If the assembled operator vanishes, every scalar entry multiplier vanishes. -/
theorem fourierMulL2_eq_zero_of_lerayOpL2_eq_zero (b : OrthonormalBasis (Fin n) ℝ E)
    (h : lerayOpL2 b = 0) (q j : Fin n) (u : Lp ℂ 2 (volume : Measure E)) :
    fourierMulL2 ℂ (lerayEntryL2 b q j) u = 0 := by
  have h1 := coordProj_lerayOpL2 b q (coordIncl E j u)
  rw [h] at h1
  simp only [ContinuousLinearMap.zero_apply, map_zero] at h1
  have h2 : ∑ k : Fin n,
      (fourierMulL2 ℂ (lerayEntryL2 b q k)) ((coordProj E k) ((coordIncl E j) u))
      = fourierMulL2 ℂ (lerayEntryL2 b q j) u := by
    rw [Finset.sum_eq_single j]
    · rw [coordProj_coordIncl, if_pos rfl]
    · intro k _ hkj
      rw [coordProj_coordIncl, if_neg (Ne.symm hkj), map_zero]
    · intro hj
      exact absurd (Finset.mem_univ j) hj
  rw [← h2, ← h1]

/-- **ANTI-VACUITY.** For `n = finrank E ≥ 2` the Leray projector is a NONZERO operator.
Proof: if it were `0`, every symbol entry would be `0` in `L∞`, hence a.e. zero; but the
trace of the symbol is `n − 1 ≠ 0` at every nonzero frequency. -/
theorem lerayOpL2_ne_zero [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (hn : 2 ≤ n) :
    lerayOpL2 b ≠ 0 := by
  intro h
  have hz : ∀ q j : Fin n, lerayEntryL2 b q j = 0 := fun q j =>
    eq_zero_of_smul_L2_eq_zero _ (smul_eq_zero_of_fourierMulL2_eq_zero _
      (fourierMulL2_eq_zero_of_lerayOpL2_eq_zero b h q j))
  have hcoe : ∀ᵐ x ∂(volume : Measure E), ∀ j : Fin n, lerayMatrix b x j j = 0 := by
    rw [ae_all_iff]
    intro j
    have hz2 : ⇑(lerayEntryL2 b j j) =ᵐ[(volume : Measure E)] (0 : E → ℂ) := by
      rw [hz j j]; exact Lp.coeFn_zero ℂ ∞ (volume : Measure E)
    filter_upwards [coeFn_lerayEntryL2 b j j, hz2] with x h1 h2
    rw [← h1]
    simpa using h2
  have hne0 : ∀ᵐ x ∂(volume : Measure E), x ≠ (0 : E) := by
    have h0 : (volume : Measure E) {(0 : E)} = 0 := measure_singleton _
    rw [ae_iff]
    simpa using h0
  obtain ⟨x, hx1, hx2⟩ := (hcoe.and hne0).exists
  have htr := trace_lerayMatrixR b hx2
  have hzero : ∑ j : Fin n, lerayMatrixR b x j j = 0 :=
    Finset.sum_eq_zero fun j _ => by
      have hj := hx1 j
      simpa [lerayMatrix] using hj
  rw [hzero] at htr
  have hn1 : (n : ℝ) = 1 := by linarith
  have : n = 1 := by exact_mod_cast hn1
  omega

/-- **UNCONDITIONAL OPTIMALITY** for `n ≥ 2`: the operator norm is exactly `1`. -/
theorem norm_lerayOpL2_eq_one_of_two_le [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E)
    (hn : 2 ≤ n) : ‖lerayOpL2 b‖ = 1 :=
  norm_lerayOpL2_eq_one b (lerayOpL2_ne_zero b hn)

/-! ## Step L7 : final package. -/

/-- **PACKAGE.** The Leray projector on `L²(E; ℂⁿ)` is an ORTHOGONAL PROJECTION:
self-adjoint (`adjoint P = P`), idempotent (`P ∘ P = P`), a contraction (`‖P‖ ≤ 1`,
strictly better than the previous `2n²`), and it splits `L²` orthogonally (Pythagoras). -/
theorem leray_orthogonal_projector_package [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    ContinuousLinearMap.adjoint (lerayOpL2 b) = lerayOpL2 b ∧
    IsSelfAdjoint (lerayOpL2 b) ∧
    ((lerayOpL2 b) ∘L (lerayOpL2 b) = lerayOpL2 b) ∧
    ‖lerayOpL2 b‖ ≤ 1 ∧
    (∀ f g : VecL2 E n, inner ℂ (lerayOpL2 b f) g = inner ℂ f (lerayOpL2 b g)) ∧
    (∀ f : VecL2 E n, ‖f‖ ^ 2 = ‖lerayOpL2 b f‖ ^ 2 + ‖f - lerayOpL2 b f‖ ^ 2) ∧
    (lerayOpL2 b ≠ 0 → ‖lerayOpL2 b‖ = 1) ∧
    (2 ≤ n → lerayOpL2 b ≠ 0 ∧ ‖lerayOpL2 b‖ = 1) :=
  ⟨adjoint_lerayOpL2 b, isSelfAdjoint_lerayOpL2 b, lerayOpL2_idem b, norm_lerayOpL2_le_one b,
   inner_lerayOpL2_symm b, norm_sq_lerayOpL2_pythagoras b, norm_lerayOpL2_eq_one b,
   fun hn => ⟨lerayOpL2_ne_zero b hn, norm_lerayOpL2_eq_one_of_two_le b hn⟩⟩

/-! ## Step L8 : concrete instance on `ℝ³`, and the comparison with the old bound. -/

section Concrete

/-- On `ℝ³` the Leray projector is a self-adjoint idempotent contraction, and the new
bound `1` is strictly better than the previously proved `2·3² = 18`. -/
theorem leray_R3_orthogonal_projector :
    ContinuousLinearMap.adjoint (lerayOpL2 b3) = lerayOpL2 b3 ∧
    IsSelfAdjoint (lerayOpL2 b3) ∧
    ((lerayOpL2 b3) ∘L (lerayOpL2 b3) = lerayOpL2 b3) ∧
    ‖lerayOpL2 b3‖ ≤ 1 ∧
    (1 : ℝ) < 2 * (3 : ℝ) ^ 2 ∧
    (∀ f : VecL2 E3 3, ‖f‖ ^ 2 = ‖lerayOpL2 b3 f‖ ^ 2 + ‖f - lerayOpL2 b3 f‖ ^ 2) ∧
    lerayOpL2 b3 ≠ 0 ∧
    ‖lerayOpL2 b3‖ = 1 :=
  ⟨adjoint_lerayOpL2 b3, isSelfAdjoint_lerayOpL2 b3, lerayOpL2_idem b3,
   norm_lerayOpL2_le_one b3, by norm_num,
   norm_sq_lerayOpL2_pythagoras b3, lerayOpL2_ne_zero b3 (by norm_num),
   norm_lerayOpL2_eq_one_of_two_le b3 (by norm_num)⟩

end Concrete

end TamesisLab.Foundations.LerayOrthogonal

#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_smul_Lp_symm
#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_fourierMulL2_symm
#print axioms TamesisLab.Foundations.LerayOrthogonal.conj_lerayEntryL2
#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_coordIncl_left
#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_coordIncl_right
#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_lerayOpL2_symm
#print axioms TamesisLab.Foundations.LerayOrthogonal.adjoint_lerayOpL2
#print axioms TamesisLab.Foundations.LerayOrthogonal.isSelfAdjoint_lerayOpL2
#print axioms TamesisLab.Foundations.LerayOrthogonal.lerayOpL2_apply_idem
#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_self_lerayOpL2
#print axioms TamesisLab.Foundations.LerayOrthogonal.norm_lerayOpL2_apply_le_one
#print axioms TamesisLab.Foundations.LerayOrthogonal.norm_lerayOpL2_le_one
#print axioms TamesisLab.Foundations.LerayOrthogonal.norm_lerayOpL2_eq_one
#print axioms TamesisLab.Foundations.LerayOrthogonal.inner_lerayOpL2_sub
#print axioms TamesisLab.Foundations.LerayOrthogonal.norm_sq_lerayOpL2_pythagoras
#print axioms TamesisLab.Foundations.LerayOrthogonal.norm_sq_lerayOpL2_pythagoras_id
#print axioms TamesisLab.Foundations.LerayOrthogonal.eq_zero_of_smul_L2_eq_zero
#print axioms TamesisLab.Foundations.LerayOrthogonal.smul_eq_zero_of_fourierMulL2_eq_zero
#print axioms TamesisLab.Foundations.LerayOrthogonal.fourierMulL2_eq_zero_of_lerayOpL2_eq_zero
#print axioms TamesisLab.Foundations.LerayOrthogonal.lerayOpL2_ne_zero
#print axioms TamesisLab.Foundations.LerayOrthogonal.norm_lerayOpL2_eq_one_of_two_le
#print axioms TamesisLab.Foundations.LerayOrthogonal.leray_orthogonal_projector_package
#print axioms TamesisLab.Foundations.LerayOrthogonal.leray_R3_orthogonal_projector
