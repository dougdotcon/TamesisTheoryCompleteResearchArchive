/-
Probe LM : MATRIX Fourier multiplier on L^2 -- the Leray projector symbol.
Builds on the already-versioned scalar theory `TamesisLab.Foundations.FourierMultiplierL2`.
-/
import TamesisLab.Foundations.FourierMultiplierL2

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 2000000

noncomputable section

namespace TamesisProbe

open TamesisLab.Foundations.FourierMultiplierL2

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable {n : ℕ}

/-! ## Step M0 : the L∞ norm of a bounded symbol is bounded by the bound. -/

theorem norm_ofBounded_le {g : E → ℂ} (hm : AEStronglyMeasurable g (volume : Measure E)) (C : ℝ)
    (hC : ∀ x, ‖g x‖ ≤ C) (hC0 : 0 ≤ C) : ‖ofBounded hm C hC‖ ≤ C := by
  rw [Lp.norm_def]
  refine ENNReal.toReal_le_of_le_ofReal hC0 ?_
  unfold ofBounded
  rw [eLpNorm_congr_ae (MemLp.coeFn_toLp _), eLpNorm_exponent_top]
  exact eLpNormEssSup_le_of_ae_bound (.of_forall hC)

/-- The coercion of a finite sum in `Lp` is a.e. the pointwise finite sum. -/
theorem Lp_coeFn_sum {ι G : Type*} [NormedAddCommGroup G] {p : ℝ≥0∞}
    (s : Finset ι) (f : ι → Lp (α := E) G p) :
    ⇑(∑ i ∈ s, f i) =ᵐ[(volume : Measure E)] fun x => ∑ i ∈ s, (f i) x := by
  classical
  refine Finset.induction_on s ?_ ?_
  · filter_upwards [Lp.coeFn_zero G p (volume : Measure E)] with x hx
    simp [hx]
  · intro i s hi ih
    simp only [Finset.sum_insert hi]
    filter_upwards [Lp.coeFn_add (f i) (∑ j ∈ s, f j), ih] with x h1 h2
    simp only [h1, Pi.add_apply, h2]

/-! ## Step M1 : the Leray symbol as a MATRIX `δ_jk - ξ_j ξ_k / |ξ|²`. -/

/-- Real-valued entries of the Leray projector symbol in an orthonormal basis `b`:
`P(ξ)_{jk} = δ_jk - ⟪ξ, b j⟫ ⟪ξ, b k⟫ / ‖ξ‖²`. -/
def lerayMatrixR (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) : ℝ :=
  (if j = k then 1 else 0) - inner ℝ x (b j) * inner ℝ x (b k) / ‖x‖ ^ 2

/-- Complex-valued Leray symbol matrix, the multiplier symbol of the Leray projector. -/
def lerayMatrix (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) : ℂ :=
  ((lerayMatrixR b x j k : ℝ) : ℂ)

/-- The matrix entries are exactly `δ - lerayComponent`, tying the new object to the
already-proved scalar component of the versioned file. -/
theorem lerayMatrix_eq (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    lerayMatrix b x j k = (if j = k then 1 else 0) - lerayComponent (b j) (b k) x := by
  simp only [lerayMatrix, lerayMatrixR, lerayComponent, Complex.ofReal_sub,
    apply_ite (fun r : ℝ => (r : ℂ)), Complex.ofReal_one, Complex.ofReal_zero]

theorem measurable_lerayMatrix (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    Measurable (fun x : E => lerayMatrix b x j k) := by
  simp only [lerayMatrix_eq]
  exact measurable_const.sub (measurable_lerayComponent (b j) (b k))

/-- Essential boundedness of every matrix entry, from `norm_lerayComponent_le`. -/
theorem norm_lerayMatrix_le (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    ‖lerayMatrix b x j k‖ ≤ 2 := by
  rw [lerayMatrix_eq]
  have h1 : ‖(if j = k then (1 : ℂ) else 0)‖ ≤ 1 := by split <;> simp
  have h2 : ‖lerayComponent (b j) (b k) x‖ ≤ 1 := by
    have h := norm_lerayComponent_le (b j) (b k) x
    rwa [b.orthonormal.1 j, b.orthonormal.1 k, one_mul] at h
  calc ‖(if j = k then (1 : ℂ) else 0) - lerayComponent (b j) (b k) x‖
      ≤ ‖(if j = k then (1 : ℂ) else 0)‖ + ‖lerayComponent (b j) (b k) x‖ := norm_sub_le _ _
    _ ≤ 1 + 1 := add_le_add h1 h2
    _ = 2 := by norm_num

/-! ## Step M2 : algebraic identities of the symbol. Parseval on the basis. -/

theorem sum_inner_sq (b : OrthonormalBasis (Fin n) ℝ E) (x : E) :
    ∑ k, inner ℝ x (b k) * inner ℝ x (b k) = ‖x‖ ^ 2 := by
  rw [← real_inner_self_eq_norm_sq, ← b.sum_inner_mul_inner x x]
  exact Finset.sum_congr rfl fun k _ => by rw [real_inner_comm (b k) x]

/-- **IDEMPOTENCE OF THE LERAY SYMBOL** : `P(ξ)² = P(ξ)` for every `ξ ≠ 0`.
This is the heart of the Leray projector. -/
theorem lerayMatrixR_idem (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0) (j l : Fin n) :
    ∑ k, lerayMatrixR b x j k * lerayMatrixR b x k l = lerayMatrixR b x j l := by
  have hN : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hx)
  have hS : ∑ k, inner ℝ x (b k) * inner ℝ x (b k) = ‖x‖ ^ 2 := sum_inner_sq b x
  have hterm : ∀ k : Fin n, lerayMatrixR b x j k * lerayMatrixR b x k l
      = (if j = k then (1 : ℝ) else 0) * (if k = l then (1 : ℝ) else 0)
        - (if j = k then (1 : ℝ) else 0) * (inner ℝ x (b k) * inner ℝ x (b l) / ‖x‖ ^ 2)
        - (if k = l then (1 : ℝ) else 0) * (inner ℝ x (b j) * inner ℝ x (b k) / ‖x‖ ^ 2)
        + inner ℝ x (b j) * inner ℝ x (b l) / (‖x‖ ^ 2 * ‖x‖ ^ 2)
            * (inner ℝ x (b k) * inner ℝ x (b k)) := by
    intro k
    simp only [lerayMatrixR]
    ring
  simp only [hterm]
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_sub_distrib,
    ← Finset.mul_sum, hS]
  have e1 : ∑ k : Fin n, (if j = k then (1 : ℝ) else 0) * (if k = l then (1 : ℝ) else 0)
      = if j = l then (1 : ℝ) else 0 := by simp
  have e2 : ∑ k : Fin n,
        (if j = k then (1 : ℝ) else 0) * (inner ℝ x (b k) * inner ℝ x (b l) / ‖x‖ ^ 2)
      = inner ℝ x (b j) * inner ℝ x (b l) / ‖x‖ ^ 2 := by simp
  have e3 : ∑ k : Fin n,
        (if k = l then (1 : ℝ) else 0) * (inner ℝ x (b j) * inner ℝ x (b k) / ‖x‖ ^ 2)
      = inner ℝ x (b j) * inner ℝ x (b l) / ‖x‖ ^ 2 := by simp
  have e4 : inner ℝ x (b j) * inner ℝ x (b l) / (‖x‖ ^ 2 * ‖x‖ ^ 2) * ‖x‖ ^ 2
      = inner ℝ x (b j) * inner ℝ x (b l) / ‖x‖ ^ 2 := by
    field_simp
  rw [e1, e2, e3, e4]
  simp only [lerayMatrixR]
  ring

/-- **THE SYMBOL KILLS GRADIENTS** : `P(ξ) ξ = 0`. The Fourier symbol of `∇p` is `i ξ p̂`,
so this is exactly "the Leray projector annihilates gradients". -/
theorem lerayMatrixR_apply_inner (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0)
    (j : Fin n) : ∑ k, lerayMatrixR b x j k * inner ℝ x (b k) = 0 := by
  have hN : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hx)
  have hS : ∑ k, inner ℝ x (b k) * inner ℝ x (b k) = ‖x‖ ^ 2 := sum_inner_sq b x
  have hterm : ∀ k : Fin n, lerayMatrixR b x j k * inner ℝ x (b k)
      = (if j = k then (1 : ℝ) else 0) * inner ℝ x (b k)
        - inner ℝ x (b j) / ‖x‖ ^ 2 * (inner ℝ x (b k) * inner ℝ x (b k)) := by
    intro k
    simp only [lerayMatrixR]
    ring
  simp only [hterm]
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, hS]
  have e1 : ∑ k : Fin n, (if j = k then (1 : ℝ) else 0) * inner ℝ x (b k)
      = inner ℝ x (b j) := by simp
  rw [e1]
  field_simp
  ring

/-- The symbol is symmetric. -/
theorem lerayMatrixR_symm (b : OrthonormalBasis (Fin n) ℝ E) (x : E) (j k : Fin n) :
    lerayMatrixR b x j k = lerayMatrixR b x k j := by
  simp only [lerayMatrixR]
  rw [mul_comm (inner ℝ x (b j)) (inner ℝ x (b k))]
  congr 1
  by_cases h : j = k
  · simp [h]
  · simp [h, Ne.symm h]

/-- The trace of the symbol is `n - 1` : it is the projection onto a hyperplane. -/
theorem trace_lerayMatrixR (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0) :
    ∑ j, lerayMatrixR b x j j = (n : ℝ) - 1 := by
  have hN : ‖x‖ ^ 2 ≠ 0 := pow_ne_zero 2 (norm_ne_zero_iff.mpr hx)
  have hS : ∑ k, inner ℝ x (b k) * inner ℝ x (b k) = ‖x‖ ^ 2 := sum_inner_sq b x
  have hterm : ∀ j : Fin n, lerayMatrixR b x j j
      = 1 - 1 / ‖x‖ ^ 2 * (inner ℝ x (b j) * inner ℝ x (b j)) := by
    intro j
    show (if j = j then (1 : ℝ) else 0) - inner ℝ x (b j) * inner ℝ x (b j) / ‖x‖ ^ 2
        = 1 - 1 / ‖x‖ ^ 2 * (inner ℝ x (b j) * inner ℝ x (b j))
    rw [show (if j = j then (1 : ℝ) else 0) = 1 from if_pos rfl]
    ring
  simp only [hterm]
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum, hS, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, mul_one]
  field_simp

/-! ## Step M3 : positive instance for the symbol at a concrete nonzero point. -/

theorem inner_basis (b : OrthonormalBasis (Fin n) ℝ E) (i k : Fin n) :
    inner ℝ (b i) (b k) = if i = k then (1 : ℝ) else 0 :=
  orthonormal_iff_ite.mp b.orthonormal i k

theorem lerayMatrixR_basis (b : OrthonormalBasis (Fin n) ℝ E) (i j k : Fin n) :
    lerayMatrixR b (b i) j k
      = (if j = k then (1 : ℝ) else 0)
        - (if i = j then (1 : ℝ) else 0) * (if i = k then (1 : ℝ) else 0) := by
  have hb : ‖b i‖ = 1 := b.orthonormal.1 i
  simp only [lerayMatrixR, inner_basis, hb]
  norm_num

/-- **POSITIVE INSTANCE.** At the concrete nonzero frequency `ξ = b i` the Leray symbol is
a genuine nontrivial idempotent: it is idempotent, it kills `ξ`, it is NOT the zero matrix
(`P_jj = 1` for `j ≠ i`) and it is NOT the identity (`P_ii = 0`), and its trace is `n-1`. -/
theorem positive_instance_lerayMatrix (b : OrthonormalBasis (Fin n) ℝ E) {i j : Fin n}
    (hij : i ≠ j) :
    (b i ≠ 0) ∧
    (∀ p q, ∑ k, lerayMatrixR b (b i) p k * lerayMatrixR b (b i) k q
        = lerayMatrixR b (b i) p q) ∧
    (∀ p, ∑ k, lerayMatrixR b (b i) p k * inner ℝ (b i) (b k) = 0) ∧
    lerayMatrixR b (b i) i i = 0 ∧
    lerayMatrixR b (b i) j j = 1 ∧
    ∑ p, lerayMatrixR b (b i) p p = (n : ℝ) - 1 := by
  have hb : ‖b i‖ = 1 := b.orthonormal.1 i
  have hbi : b i ≠ 0 := by
    intro h
    rw [h, norm_zero] at hb
    exact zero_ne_one hb
  refine ⟨hbi, fun p q => lerayMatrixR_idem b hbi p q, fun p => lerayMatrixR_apply_inner b hbi p,
    ?_, ?_, trace_lerayMatrixR b hbi⟩
  · rw [lerayMatrixR_basis]; norm_num
  · rw [lerayMatrixR_basis]; simp [hij]

/-! ## Step M4 : the matrix multiplier operator on `L²` vector fields. -/

variable (E) in
/-- Coordinate `k` of an `L²` vector field, as a bounded operator into scalar `L²`. -/
def coordProj (k : Fin n) :
    Lp (α := E) (EuclideanSpace ℂ (Fin n)) 2 →L[ℂ] Lp (α := E) ℂ 2 :=
  (EuclideanSpace.proj (𝕜 := ℂ) k).compLpL 2 (volume : Measure E)

variable (E) in
/-- Inclusion of a scalar `L²` function as the `j`-th coordinate of an `L²` vector field. -/
def coordIncl (j : Fin n) :
    Lp (α := E) ℂ 2 →L[ℂ] Lp (α := E) (EuclideanSpace ℂ (Fin n)) 2 :=
  (ContinuousLinearMap.toSpanSingleton ℂ
    (EuclideanSpace.single j (1 : ℂ))).compLpL 2 (volume : Measure E)

theorem norm_coordProj_le (k : Fin n) : ‖coordProj E k‖ ≤ 1 := by
  refine (ContinuousLinearMap.norm_compLpL_le _).trans ?_
  refine ContinuousLinearMap.opNorm_le_bound _ zero_le_one fun x => ?_
  simpa using PiLp.norm_apply_le x k

theorem norm_coordIncl_le (j : Fin n) : ‖coordIncl E j‖ ≤ 1 := by
  refine (ContinuousLinearMap.norm_compLpL_le _).trans ?_
  rw [ContinuousLinearMap.norm_toSpanSingleton]
  simp [EuclideanSpace.single]

/-- Each matrix entry as an element of `L∞`. -/
def lerayEntryL2 (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    Lp ℂ ∞ (volume : Measure E) :=
  ofBounded (measurable_lerayMatrix b j k).aestronglyMeasurable 2
    (fun x => norm_lerayMatrix_le b x j k)

theorem norm_lerayEntryL2_le (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    ‖lerayEntryL2 b j k‖ ≤ 2 :=
  norm_ofBounded_le _ _ _ (by norm_num)

/-- **THE MATRIX FOURIER MULTIPLIER : the Leray projector on `L²` vector fields.**
Defined as the finite sum of scalar `L²` Fourier multipliers, each one the versioned
`fourierMulL2` applied to a bounded measurable (non-temperate!) entry of the Leray symbol. -/
def lerayOpL2 (b : OrthonormalBasis (Fin n) ℝ E) :
    Lp (α := E) (EuclideanSpace ℂ (Fin n)) 2 →L[ℂ]
      Lp (α := E) (EuclideanSpace ℂ (Fin n)) 2 :=
  ∑ j : Fin n, ∑ k : Fin n,
    (coordIncl E j) ∘L ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (coordProj E k))

theorem norm_lerayOpL2_term_le (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    ‖(coordIncl E j) ∘L ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (coordProj E k))‖ ≤ 2 := by
  have h1 : ‖coordIncl E j‖ ≤ 1 := norm_coordIncl_le j
  have h2 : ‖fourierMulL2 ℂ (lerayEntryL2 b j k)‖ ≤ 2 :=
    (norm_fourierMulL2_le _).trans (norm_lerayEntryL2_le b j k)
  have h3 : ‖coordProj E k‖ ≤ 1 := norm_coordProj_le k
  calc ‖(coordIncl E j) ∘L ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (coordProj E k))‖
      ≤ ‖coordIncl E j‖ * ‖(fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (coordProj E k)‖ :=
        ContinuousLinearMap.opNorm_comp_le _ _
    _ ≤ ‖coordIncl E j‖ * (‖fourierMulL2 ℂ (lerayEntryL2 b j k)‖ * ‖coordProj E k‖) :=
        mul_le_mul_of_nonneg_left (ContinuousLinearMap.opNorm_comp_le _ _) (norm_nonneg _)
    _ ≤ 1 * (2 * 1) := by gcongr
    _ = 2 := by norm_num

/-- **NORM BOUND FOR THE MATRIX MULTIPLIER.** -/
theorem norm_lerayOpL2_le (b : OrthonormalBasis (Fin n) ℝ E) :
    ‖lerayOpL2 b‖ ≤ 2 * (n : ℝ) ^ 2 := by
  calc ‖lerayOpL2 b‖
      ≤ ∑ j : Fin n, ‖∑ k : Fin n,
          (coordIncl E j) ∘L ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (coordProj E k))‖ :=
        norm_sum_le _ _
    _ ≤ ∑ j : Fin n, ∑ k : Fin n,
          ‖(coordIncl E j) ∘L ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (coordProj E k))‖ :=
        Finset.sum_le_sum fun j _ => norm_sum_le _ _
    _ ≤ ∑ _j : Fin n, ∑ _k : Fin n, (2 : ℝ) :=
        Finset.sum_le_sum fun j _ => Finset.sum_le_sum fun k _ => norm_lerayOpL2_term_le b j k
    _ = 2 * (n : ℝ) ^ 2 := by
        simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
        ring

/-! ## Step M5 : the multiplier calculus is an algebra homomorphism (probe). -/

section Algebra

variable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- Associativity of the heterogeneous `L∞`-action on `L²`. -/
theorem smul_smul_Lp (g h : Lp ℂ ∞ (volume : Measure E)) (f : Lp (α := E) F 2) :
    (g • (h • f : Lp (α := E) F 2) : Lp (α := E) F 2)
      = ((g • h : Lp ℂ ∞ (volume : Measure E)) • f : Lp (α := E) F 2) := by
  rw [Lp.ext_iff]
  filter_upwards [Lp.coeFn_lpSMul (r := 2) g (h • f : Lp (α := E) F 2),
    Lp.coeFn_lpSMul (r := 2) h f,
    Lp.coeFn_lpSMul (r := ∞) g h,
    Lp.coeFn_lpSMul (r := 2) (g • h : Lp ℂ ∞ (volume : Measure E)) f]
    with x h1 h2 h3 h4
  simp only [h1, h4, Pi.smul_apply', h2, h3, smul_eq_mul, mul_smul]

/-- **MULTIPLICATIVITY OF THE `L²` MULTIPLIER CALCULUS.** -/
theorem fourierMulL2_comp (g h : Lp ℂ ∞ (volume : Measure E)) :
    (fourierMulL2 F g) ∘L (fourierMulL2 F h)
      = fourierMulL2 F (g • h : Lp ℂ ∞ (volume : Measure E)) := by
  refine ContinuousLinearMap.ext fun f => ?_
  simp only [ContinuousLinearMap.coe_comp', Function.comp_apply]
  rw [fourierMulL2_apply, fourierMulL2_apply, fourierMulL2_apply, mulL2_apply, mulL2_apply,
    mulL2_apply, fourier_fourierInv_eq, smul_smul_Lp]

/-- **ADDITIVITY OF THE `L²` MULTIPLIER CALCULUS.** -/
theorem fourierMulL2_add (g h : Lp ℂ ∞ (volume : Measure E)) :
    fourierMulL2 F (g + h) = fourierMulL2 F g + fourierMulL2 F h := by
  refine ContinuousLinearMap.ext fun f => ?_
  simp only [fourierMulL2, ContinuousLinearMap.coe_comp', Function.comp_apply,
    ContinuousLinearMap.add_apply, mulL2_apply, Lp.smul_add, map_add]

theorem fourierMulL2_zero :
    fourierMulL2 F (0 : Lp ℂ ∞ (volume : Measure E)) = 0 := by
  refine ContinuousLinearMap.ext fun f => ?_
  simp [fourierMulL2, mulL2_apply]

theorem fourierMulL2_sum {ι : Type*} (s : Finset ι) (t : ι → Lp ℂ ∞ (volume : Measure E)) :
    fourierMulL2 F (∑ i ∈ s, t i) = ∑ i ∈ s, fourierMulL2 F (t i) := by
  classical
  refine Finset.induction_on s ?_ ?_
  · simp [fourierMulL2_zero]
  · intro i s hi ih
    rw [Finset.sum_insert hi, Finset.sum_insert hi, fourierMulL2_add, ih]

end Algebra

/-! ## Step M6 : idempotence at the operator level. -/

theorem lerayMatrix_idem (b : OrthonormalBasis (Fin n) ℝ E) {x : E} (hx : x ≠ 0) (j l : Fin n) :
    ∑ k, lerayMatrix b x j k * lerayMatrix b x k l = lerayMatrix b x j l := by
  calc ∑ k, lerayMatrix b x j k * lerayMatrix b x k l
      = ((∑ k, lerayMatrixR b x j k * lerayMatrixR b x k l : ℝ) : ℂ) := by
        rw [Complex.ofReal_sum]
        exact Finset.sum_congr rfl fun k _ => by simp [lerayMatrix]
    _ = lerayMatrix b x j l := by rw [lerayMatrixR_idem b hx]; rfl

theorem coeFn_lerayEntryL2 (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    ⇑(lerayEntryL2 b j k) =ᵐ[(volume : Measure E)] fun x => lerayMatrix b x j k := by
  unfold lerayEntryL2 ofBounded
  exact MemLp.coeFn_toLp _

/-- **IDEMPOTENCE OF THE SYMBOL MATRIX IN `L∞`.** -/
theorem lerayEntryL2_idem [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (j l : Fin n) :
    ∑ k : Fin n, (lerayEntryL2 b j k • lerayEntryL2 b k l : Lp ℂ ∞ (volume : Measure E))
      = lerayEntryL2 b j l := by
  rw [Lp.ext_iff]
  have hcoe : ∀ᵐ x ∂(volume : Measure E), ∀ p : Fin n, ∀ q : Fin n,
      (lerayEntryL2 b p q) x = lerayMatrix b x p q := by
    rw [ae_all_iff]
    intro p
    rw [ae_all_iff]
    intro q
    exact coeFn_lerayEntryL2 b p q
  have hprod : ∀ᵐ x ∂(volume : Measure E), ∀ k : Fin n,
      ((lerayEntryL2 b j k • lerayEntryL2 b k l : Lp ℂ ∞ (volume : Measure E))) x
        = (lerayEntryL2 b j k) x * (lerayEntryL2 b k l) x := by
    rw [ae_all_iff]
    intro k
    filter_upwards [Lp.coeFn_lpSMul (r := ∞) (lerayEntryL2 b j k) (lerayEntryL2 b k l)] with x hx
    simpa using hx
  have hne : ∀ᵐ x ∂(volume : Measure E), x ≠ (0 : E) := by
    have h0 : (volume : Measure E) {(0 : E)} = 0 := measure_singleton _
    rw [ae_iff]
    simpa using h0
  filter_upwards [Lp_coeFn_sum Finset.univ
      (fun k : Fin n => (lerayEntryL2 b j k • lerayEntryL2 b k l : Lp ℂ ∞ (volume : Measure E))),
    hcoe, hprod, hne] with x hsum hcoex hprodx hxne
  rw [hsum, hcoex j l, ← lerayMatrix_idem b hxne j l]
  exact Finset.sum_congr rfl fun k _ => by rw [hprodx k, hcoex j k, hcoex k l]

/-- **THE LERAY PROJECTOR IS IDEMPOTENT ON `L²`.** The matrix of scalar `L²` Fourier
multipliers `M j k = fourierMulL2 (δ_jk - ξ_jξ_k/|ξ|²)` satisfies `∑_k M_jk ∘ M_kl = M_jl`.
No smoothness of the symbol is used anywhere. -/
theorem lerayMul_idem [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) (j l : Fin n) :
    ∑ k : Fin n,
        (fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (fourierMulL2 ℂ (lerayEntryL2 b k l))
      = fourierMulL2 ℂ (lerayEntryL2 b j l) := by
  have h1 : ∀ k : Fin n,
      (fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (fourierMulL2 ℂ (lerayEntryL2 b k l))
        = fourierMulL2 ℂ
            ((lerayEntryL2 b j k • lerayEntryL2 b k l : Lp ℂ ∞ (volume : Measure E))) :=
    fun k => fourierMulL2_comp _ _
  simp only [h1]
  rw [← fourierMulL2_sum, lerayEntryL2_idem]

/-- The multiplier matrix is symmetric. -/
theorem lerayEntryL2_symm (b : OrthonormalBasis (Fin n) ℝ E) (j k : Fin n) :
    lerayEntryL2 b j k = lerayEntryL2 b k j := by
  rw [Lp.ext_iff]
  filter_upwards [coeFn_lerayEntryL2 b j k, coeFn_lerayEntryL2 b k j] with x h1 h2
  rw [h1, h2]
  simp only [lerayMatrix, lerayMatrixR_symm]

/-! ## Step M7 : idempotence of the full operator on `L²` vector fields. -/

theorem coordProj_coordIncl (j k : Fin n) (f : Lp (α := E) ℂ 2) :
    (coordProj E k) ((coordIncl E j) f) = (if j = k then f else 0) := by
  have hae : ⇑((coordProj E k) ((coordIncl E j) f)) =ᵐ[(volume : Measure E)]
      fun x => f x * (if k = j then (1 : ℂ) else 0) := by
    have h1 := ContinuousLinearMap.coeFn_compLpL (p := 2) (μ := (volume : Measure E))
      (EuclideanSpace.proj (𝕜 := ℂ) k) ((coordIncl E j) f)
    have h2 := ContinuousLinearMap.coeFn_compLpL (p := 2) (μ := (volume : Measure E))
      (ContinuousLinearMap.toSpanSingleton ℂ (EuclideanSpace.single j (1 : ℂ))) f
    filter_upwards [h1, h2] with x hx1 hx2
    have e1 : ((coordProj E k) ((coordIncl E j) f)) x
        = (EuclideanSpace.proj (𝕜 := ℂ) k) (((coordIncl E j) f) x) := hx1
    have e2 : ((coordIncl E j) f) x
        = (ContinuousLinearMap.toSpanSingleton ℂ (EuclideanSpace.single j (1 : ℂ))) (f x) := hx2
    rw [e1, e2]
    simp
  by_cases h : j = k
  · rw [if_pos h, Lp.ext_iff]
    filter_upwards [hae] with x hx
    rw [hx, if_pos h.symm, mul_one]
  · rw [if_neg h, Lp.ext_iff]
    filter_upwards [hae, Lp.coeFn_zero ℂ 2 (volume : Measure E)] with x hx hz
    simp [hx, hz, Ne.symm h]

theorem lerayOpL2_apply (b : OrthonormalBasis (Fin n) ℝ E)
    (f : Lp (α := E) (EuclideanSpace ℂ (Fin n)) 2) :
    lerayOpL2 b f = ∑ j : Fin n, ∑ k : Fin n,
      (coordIncl E j) ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ((coordProj E k) f)) := by
  simp only [lerayOpL2, ContinuousLinearMap.sum_apply, ContinuousLinearMap.coe_comp,
    Function.comp_apply]

theorem coordProj_lerayOpL2 (b : OrthonormalBasis (Fin n) ℝ E) (q : Fin n)
    (f : Lp (α := E) (EuclideanSpace ℂ (Fin n)) 2) :
    (coordProj E q) (lerayOpL2 b f)
      = ∑ k : Fin n, (fourierMulL2 ℂ (lerayEntryL2 b q k)) ((coordProj E k) f) := by
  have hstep : ∀ j : Fin n, (coordProj E q) (∑ k : Fin n,
      (coordIncl E j) ((fourierMulL2 ℂ (lerayEntryL2 b j k)) ((coordProj E k) f)))
      = if j = q then
          (∑ k : Fin n, (fourierMulL2 ℂ (lerayEntryL2 b j k)) ((coordProj E k) f)) else 0 := by
    intro j
    rw [map_sum]
    by_cases h : j = q
    · rw [if_pos h]
      exact Finset.sum_congr rfl fun k _ => by rw [coordProj_coordIncl, if_pos h]
    · rw [if_neg h]
      exact Finset.sum_eq_zero fun k _ => by rw [coordProj_coordIncl, if_neg h]
  rw [lerayOpL2_apply, map_sum]
  simp only [hstep]
  simp

/-- **THE LERAY PROJECTOR ON `L²` VECTOR FIELDS IS IDEMPOTENT: `P ∘ P = P`.** -/
theorem lerayOpL2_idem [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    (lerayOpL2 b) ∘L (lerayOpL2 b) = lerayOpL2 b := by
  refine ContinuousLinearMap.ext fun f => ?_
  show lerayOpL2 b (lerayOpL2 b f) = lerayOpL2 b f
  rw [lerayOpL2_apply (f := lerayOpL2 b f)]
  have h1 : ∀ j q : Fin n,
      (coordIncl E j) ((fourierMulL2 ℂ (lerayEntryL2 b j q)) ((coordProj E q) (lerayOpL2 b f)))
      = ∑ k : Fin n, (coordIncl E j)
          ((fourierMulL2 ℂ (lerayEntryL2 b j q))
            ((fourierMulL2 ℂ (lerayEntryL2 b q k)) ((coordProj E k) f))) := by
    intro j q
    rw [coordProj_lerayOpL2, map_sum, map_sum]
  simp only [h1]
  rw [lerayOpL2_apply]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [← map_sum]
  congr 1
  have h2 := congrArg
    (fun T : Lp (α := E) ℂ 2 →L[ℂ] Lp (α := E) ℂ 2 => T ((coordProj E k) f))
    (lerayMul_idem b j k)
  simpa [ContinuousLinearMap.sum_apply] using h2

/-- **FINAL PACKAGE.** For a nontrivial finite-dimensional real inner product space `E`
with orthonormal basis `b`, the Leray multiplier matrix on `L²(E)` exists, is bounded
entrywise by `2`, is symmetric, is idempotent, and assembles into a bounded operator on
`L²` vector fields with `‖P‖ ≤ 2n²`. -/
theorem leray_projector_package [Nontrivial E] (b : OrthonormalBasis (Fin n) ℝ E) :
    (∀ j k : Fin n, ‖fourierMulL2 ℂ (lerayEntryL2 b j k)‖ ≤ 2) ∧
    (∀ j k : Fin n, lerayEntryL2 b j k = lerayEntryL2 b k j) ∧
    (∀ j l : Fin n, ∑ k : Fin n,
        (fourierMulL2 ℂ (lerayEntryL2 b j k)) ∘L (fourierMulL2 ℂ (lerayEntryL2 b k l))
        = fourierMulL2 ℂ (lerayEntryL2 b j l)) ∧
    ‖lerayOpL2 b‖ ≤ 2 * (n : ℝ) ^ 2 ∧
    ((lerayOpL2 b) ∘L (lerayOpL2 b) = lerayOpL2 b) ∧
    (∀ x : E, x ≠ 0 → ∀ j : Fin n,
        ∑ k, lerayMatrixR b x j k * inner ℝ x (b k) = 0) :=
  ⟨fun j k => (norm_fourierMulL2_le _).trans (norm_lerayEntryL2_le b j k),
   fun j k => lerayEntryL2_symm b j k,
   fun j l => lerayMul_idem b j l,
   norm_lerayOpL2_le b,
   lerayOpL2_idem b,
   fun x hx j => lerayMatrixR_apply_inner b hx j⟩

/-! ## Step M8 : NON-VACUITY. A concrete model of every hypothesis. -/

section Concrete

/-- Concrete frequency space: `ℝ³`. -/
abbrev E3 : Type := EuclideanSpace ℝ (Fin 3)

/-- Concrete orthonormal basis. -/
def b3 : OrthonormalBasis (Fin 3) ℝ E3 := EuclideanSpace.basisFun (Fin 3) ℝ

/-- **POSITIVE INSTANCE / NON-VACUITY.** Every hypothesis of the general theory is
simultaneously satisfiable: on `E = ℝ³` with the standard basis the Leray projector on
`L²(ℝ³; ℂ³)` exists, is bounded, is idempotent, its symbol matrix is idempotent, kills
frequencies, and is a NONTRIVIAL projection (neither `0` nor the identity). -/
theorem nonvacuous_leray_R3 :
    ((lerayOpL2 b3) ∘L (lerayOpL2 b3) = lerayOpL2 b3) ∧
    ‖lerayOpL2 b3‖ ≤ 18 ∧
    (∀ j l : Fin 3, ∑ k : Fin 3,
      (fourierMulL2 ℂ (lerayEntryL2 b3 j k)) ∘L (fourierMulL2 ℂ (lerayEntryL2 b3 k l))
        = fourierMulL2 ℂ (lerayEntryL2 b3 j l)) ∧
    (b3 0 ≠ 0) ∧
    (∀ p q : Fin 3, ∑ k, lerayMatrixR b3 (b3 0) p k * lerayMatrixR b3 (b3 0) k q
        = lerayMatrixR b3 (b3 0) p q) ∧
    (∀ p : Fin 3, ∑ k, lerayMatrixR b3 (b3 0) p k * inner ℝ (b3 0) (b3 k) = 0) ∧
    lerayMatrixR b3 (b3 0) 0 0 = 0 ∧
    lerayMatrixR b3 (b3 0) 1 1 = 1 ∧
    ∑ p, lerayMatrixR b3 (b3 0) p p = (3 : ℝ) - 1 := by
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ :=
    positive_instance_lerayMatrix b3 (i := (0 : Fin 3)) (j := (1 : Fin 3)) (by decide)
  refine ⟨lerayOpL2_idem b3, ?_, fun j l => lerayMul_idem b3 j l, h1, h2, h3, h4, h5, ?_⟩
  · have := norm_lerayOpL2_le b3
    norm_num at this ⊢
    linarith
  · rw [h6]
    norm_num

end Concrete

end TamesisProbe

#print axioms TamesisProbe.nonvacuous_leray_R3
#print axioms TamesisProbe.smul_smul_Lp
#print axioms TamesisProbe.fourierMulL2_comp
#print axioms TamesisProbe.fourierMulL2_add
#print axioms TamesisProbe.fourierMulL2_sum
#print axioms TamesisProbe.Lp_coeFn_sum
#print axioms TamesisProbe.lerayMatrix_idem
#print axioms TamesisProbe.lerayEntryL2_idem
#print axioms TamesisProbe.lerayMul_idem
#print axioms TamesisProbe.lerayEntryL2_symm
#print axioms TamesisProbe.coordProj_coordIncl
#print axioms TamesisProbe.lerayOpL2_apply
#print axioms TamesisProbe.coordProj_lerayOpL2
#print axioms TamesisProbe.lerayOpL2_idem
#print axioms TamesisProbe.leray_projector_package
#print axioms TamesisProbe.norm_ofBounded_le
#print axioms TamesisProbe.lerayMatrix_eq
#print axioms TamesisProbe.norm_lerayMatrix_le
#print axioms TamesisProbe.sum_inner_sq
#print axioms TamesisProbe.lerayMatrixR_idem
#print axioms TamesisProbe.lerayMatrixR_apply_inner
#print axioms TamesisProbe.lerayMatrixR_symm
#print axioms TamesisProbe.trace_lerayMatrixR
#print axioms TamesisProbe.positive_instance_lerayMatrix
#print axioms TamesisProbe.norm_coordProj_le
#print axioms TamesisProbe.norm_coordIncl_le
#print axioms TamesisProbe.norm_lerayEntryL2_le
#print axioms TamesisProbe.lerayOpL2
#print axioms TamesisProbe.norm_lerayOpL2_le
