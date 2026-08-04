/-
  PROBE SI — SC-GAP-001.
  Positive instance in INFINITE dimension for TamesisLab.Foundations.SpectralCounting.

  Space:    H2 = lp (fun _ : ℕ => ℂ) 2   (separable, infinite dimensional)
  Operator: T  = diagonal multiplication by dseq i = 1/(i+1)

  NO sorry / NO admit / NO local axiom.
-/
import Mathlib
import TamesisLab.Foundations.SpectralCounting

open scoped ENNReal lp InnerProductSpace
open Filter Topology

namespace TamesisLab.Foundations.SpectralCounting.InfDim

/-! ## §0 — the space -/

/-- The concrete separable infinite-dimensional Hilbert space. -/
noncomputable abbrev H2 := lp (fun _ : ℕ => ℂ) 2

example : CompleteSpace H2 := inferInstance

/-! ## §1 — the diagonal sequence  dseq i = 1/(i+1) -/

noncomputable def dseq : ℕ → ℝ := fun i => 1 / (i + 1)

lemma dseq_pos (i : ℕ) : 0 < dseq i := by unfold dseq; positivity

lemma dseq_le_one (i : ℕ) : dseq i ≤ 1 := by
  have h1 : (0 : ℝ) < (i : ℝ) + 1 := by positivity
  show 1 / ((i : ℝ) + 1) ≤ 1
  rw [div_le_one h1]
  have : (0 : ℝ) ≤ (i : ℝ) := Nat.cast_nonneg i
  linarith

lemma dseq_abs_le_one (i : ℕ) : |dseq i| ≤ 1 := by
  rw [abs_of_pos (dseq_pos i)]; exact dseq_le_one i

lemma dseq_antitone : Antitone dseq := by
  intro i j hij
  have h0 : (0 : ℝ) < (i : ℝ) + 1 := by positivity
  have h1 : (i : ℝ) + 1 ≤ (j : ℝ) + 1 := by
    have : (i : ℝ) ≤ (j : ℝ) := by exact_mod_cast hij
    linarith
  show 1 / ((j : ℝ) + 1) ≤ 1 / ((i : ℝ) + 1)
  exact one_div_le_one_div_of_le h0 h1

lemma dseq_tendsto : Tendsto dseq atTop (𝓝 0) :=
  tendsto_one_div_add_atTop_nhds_zero_nat

lemma dseq_injective : Function.Injective dseq := by
  intro i j h
  have h' : 1 / ((i : ℝ) + 1) = 1 / ((j : ℝ) + 1) := h
  have hi : ((i : ℝ) + 1) ≠ 0 := by positivity
  have hj : ((j : ℝ) + 1) ≠ 0 := by positivity
  have h2 : (i : ℝ) = (j : ℝ) := by field_simp at h'; linarith
  exact_mod_cast h2

@[simp] lemma dseq_zero : dseq 0 = 1 := by norm_num [dseq]
@[simp] lemma dseq_one : dseq 1 = 1 / 2 := by norm_num [dseq]
@[simp] lemma dseq_two : dseq 2 = 1 / 3 := by norm_num [dseq]

/-! ## §2 — the diagonal (multiplication) operator -/

lemma memOf (c : ℕ → ℝ) (C : ℝ) (hC : ∀ i, |c i| ≤ C) (f : H2) :
    Memℓp (fun i => (c i : ℂ) * f i) 2 := by
  refine Memℓp.mono (g := fun i => (max C 1) * ‖(f : ∀ _ : ℕ, ℂ) i‖)
    ((lp.memℓp f).norm.const_mul (max C 1)) ?_
  intro i
  have h1 : |c i| ≤ max C 1 := (hC i).trans (le_max_left _ _)
  rw [norm_mul, Complex.norm_real, Real.norm_eq_abs]
  exact mul_le_mul_of_nonneg_right h1 (norm_nonneg _)

/-- The multiplication (diagonal) operator as a plain linear map. -/
noncomputable def mulLin (c : ℕ → ℝ) (C : ℝ) (hC : ∀ i, |c i| ≤ C) : H2 →ₗ[ℂ] H2 where
  toFun f := ⟨fun i => (c i : ℂ) * f i, memOf c C hC f⟩
  map_add' f g := by ext i; exact mul_add _ _ _
  map_smul' a f := by ext i; exact mul_left_comm _ _ _

@[simp] lemma mulLin_apply (c : ℕ → ℝ) (C : ℝ) (hC : ∀ i, |c i| ≤ C) (f : H2) (i : ℕ) :
    (mulLin c C hC f : ∀ _ : ℕ, ℂ) i = (c i : ℂ) * f i := rfl

lemma mulLin_norm_le (c : ℕ → ℝ) (C : ℝ) (hC : ∀ i, |c i| ≤ C) (hC0 : 0 ≤ C) (f : H2) :
    ‖mulLin c C hC f‖ ≤ C * ‖f‖ := by
  have key : ‖mulLin c C hC f‖ ≤ ‖(C : ℝ) • f‖ := by
    apply lp.norm_mono (p := (2 : ℝ≥0∞)) (by norm_num)
    intro i
    rw [mulLin_apply, norm_mul, Complex.norm_real, Real.norm_eq_abs, lp.coeFn_smul]
    simp only [Pi.smul_apply, norm_smul, Real.norm_eq_abs, abs_of_nonneg hC0]
    exact mul_le_mul_of_nonneg_right (hC i) (norm_nonneg _)
  rwa [norm_smul, Real.norm_eq_abs, abs_of_nonneg hC0] at key

/-- The multiplication operator as a continuous linear map. -/
noncomputable def mulOp (c : ℕ → ℝ) (C : ℝ) (hC : ∀ i, |c i| ≤ C) (hC0 : 0 ≤ C) : H2 →L[ℂ] H2 :=
  (mulLin c C hC).mkContinuous C (mulLin_norm_le c C hC hC0)

/-- **The operator.** Diagonal on ℓ²(ℕ,ℂ) with diagonal `1/(i+1)`. -/
noncomputable def T : H2 →L[ℂ] H2 := mulOp dseq 1 dseq_abs_le_one zero_le_one

@[simp] lemma T_apply (f : H2) (i : ℕ) : ((T f : H2) : ∀ _ : ℕ, ℂ) i = (dseq i : ℂ) * f i := rfl

/-! ## §3 — eigenvectors -/

/-- Standard basis vector. -/
noncomputable def e (i : ℕ) : H2 := lp.single (E := fun _ : ℕ => ℂ) 2 i (1 : ℂ)

lemma e_apply (i j : ℕ) : ((e i : H2) : ∀ _ : ℕ, ℂ) j = if j = i then 1 else 0 := by
  unfold e
  rw [lp.coeFn_single]
  simp [Pi.single_apply]

lemma e_ne_zero (i : ℕ) : e i ≠ 0 := by
  intro h
  have h1 : ((e i : H2) : ∀ _ : ℕ, ℂ) i = ((0 : H2) : ∀ _ : ℕ, ℂ) i := by rw [h]
  rw [e_apply] at h1
  simp at h1

lemma hasEigenvector_T (i : ℕ) :
    Module.End.HasEigenvector (T : Module.End ℂ H2) ((dseq i : ℂ)) (e i) := by
  refine ⟨?_, e_ne_zero i⟩
  rw [Module.End.mem_eigenspace_iff]
  ext j
  rw [ContinuousLinearMap.coe_coe, T_apply, lp.coeFn_smul]
  simp only [Pi.smul_apply, smul_eq_mul, e_apply]
  by_cases hij : j = i
  · subst hij; simp
  · simp [hij]

lemma hasEigenvalue_T (i : ℕ) :
    Module.End.HasEigenvalue (T : Module.End ℂ H2) ((dseq i : ℂ)) :=
  Module.End.hasEigenvalue_of_hasEigenvector (hasEigenvector_T i)

/-! ## §4 — self-adjointness -/

theorem T_isSymmetric : LinearMap.IsSymmetric (T : H2 →ₗ[ℂ] H2) := by
  intro f g
  show ⟪T f, g⟫_ℂ = ⟪f, T g⟫_ℂ
  rw [lp.inner_eq_tsum, lp.inner_eq_tsum]
  refine tsum_congr (fun i => ?_)
  rw [RCLike.inner_apply, RCLike.inner_apply, T_apply, T_apply]
  simp only [map_mul, Complex.conj_ofReal]
  ring

/-! ## §5 — compactness (norm limit of finite-rank truncations) -/

/-- Coordinate evaluation as a continuous linear functional. -/
noncomputable def ev (i : ℕ) : H2 →L[ℂ] ℂ :=
  LinearMap.mkContinuous
    { toFun := fun f => (f : ∀ _ : ℕ, ℂ) i
      map_add' := fun f g => rfl
      map_smul' := fun a f => rfl } 1
    (fun f => by
      show ‖(f : ∀ _ : ℕ, ℂ) i‖ ≤ 1 * ‖f‖
      rw [one_mul]
      exact lp.norm_apply_le_norm (p := (2 : ℝ≥0∞)) (by norm_num) f i)

@[simp] lemma ev_apply (i : ℕ) (f : H2) : ev i f = (f : ∀ _ : ℕ, ℂ) i := rfl

/-- The embedding `c ↦ c • e i`. -/
noncomputable def emb (i : ℕ) : ℂ →L[ℂ] H2 :=
  ContinuousLinearMap.smulRight (ContinuousLinearMap.id ℂ ℂ) (e i)

@[simp] lemma emb_apply (i : ℕ) (c : ℂ) : emb i c = c • e i := rfl

/-- Rank-one operator `f ↦ f i • e i`. -/
noncomputable def rk (i : ℕ) : H2 →L[ℂ] H2 := (emb i).comp (ev i)

lemma rk_apply (i : ℕ) (f : H2) (j : ℕ) :
    ((rk i f : H2) : ∀ _ : ℕ, ℂ) j = if j = i then (f : ∀ _ : ℕ, ℂ) i else 0 := by
  show ((emb i (ev i f) : H2) : ∀ _ : ℕ, ℂ) j = _
  rw [emb_apply, ev_apply, lp.coeFn_smul]
  simp only [Pi.smul_apply, smul_eq_mul, e_apply]
  by_cases hij : j = i <;> simp [hij]

lemma isCompactOperator_rk (i : ℕ) : IsCompactOperator (rk i) := by
  have h : IsCompactOperator (emb i) := isCompactOperator_of_locallyCompactSpace_rng (emb i)
  exact h.comp_clm (ev i)

/-- Finite-rank truncation. -/
noncomputable def Tn (n : ℕ) : H2 →L[ℂ] H2 := ∑ i ∈ Finset.range n, (dseq i : ℂ) • rk i

lemma Tn_succ (k : ℕ) : Tn (k + 1) = Tn k + (dseq k : ℂ) • rk k := by
  simp [Tn, Finset.sum_range_succ]

lemma isCompactOperator_Tn (n : ℕ) : IsCompactOperator (Tn n) := by
  induction n with
  | zero =>
      have : Tn 0 = 0 := by simp [Tn]
      rw [this]
      exact isCompactOperator_zero
  | succ k ih =>
      have h1 : IsCompactOperator (⇑((dseq k : ℂ) • rk k)) :=
        (isCompactOperator_rk k).smul ((dseq k : ℂ))
      rw [Tn_succ]
      exact ih.add h1

lemma Tn_apply (n : ℕ) (f : H2) (j : ℕ) :
    ((Tn n f : H2) : ∀ _ : ℕ, ℂ) j = if j < n then (dseq j : ℂ) * (f : ∀ _ : ℕ, ℂ) j else 0 := by
  induction n with
  | zero => simp [Tn]
  | succ k ih =>
      rw [Tn_succ]
      rw [ContinuousLinearMap.add_apply, ContinuousLinearMap.smul_apply, lp.coeFn_add,
        Pi.add_apply, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul, ih, rk_apply]
      rcases lt_trichotomy j k with h | h | h
      · have h1 : j < k + 1 := by omega
        have h2 : j ≠ k := by omega
        simp [h, h1, h2]
      · subst h
        simp
      · have h1 : ¬ (j < k) := by omega
        have h2 : ¬ (j < k + 1) := by omega
        have h3 : j ≠ k := by omega
        simp [h1, h2, h3]

lemma norm_T_sub_Tn (n : ℕ) : ‖T - Tn n‖ ≤ dseq n := by
  refine ContinuousLinearMap.opNorm_le_bound _ (dseq_pos n).le (fun f => ?_)
  have key : ‖(T - Tn n) f‖ ≤ ‖(dseq n : ℝ) • f‖ := by
    apply lp.norm_mono (p := (2 : ℝ≥0∞)) (by norm_num)
    intro j
    rw [ContinuousLinearMap.sub_apply, lp.coeFn_sub, Pi.sub_apply, T_apply, Tn_apply,
      lp.coeFn_smul]
    simp only [Pi.smul_apply, norm_smul, Real.norm_eq_abs, abs_of_pos (dseq_pos n)]
    by_cases hj : j < n
    · rw [if_pos hj, sub_self, norm_zero]
      exact mul_nonneg (dseq_pos n).le (norm_nonneg _)
    · rw [if_neg hj, sub_zero, norm_mul, Complex.norm_real, Real.norm_eq_abs,
        abs_of_pos (dseq_pos j)]
      exact mul_le_mul_of_nonneg_right (dseq_antitone (not_lt.mp hj)) (norm_nonneg _)
  rwa [norm_smul, Real.norm_eq_abs, abs_of_pos (dseq_pos n)] at key

lemma tendsto_Tn : Tendsto Tn atTop (𝓝 T) := by
  rw [tendsto_iff_norm_sub_tendsto_zero]
  refine squeeze_zero (fun n => norm_nonneg _) (fun n => ?_) dseq_tendsto
  rw [← norm_neg, neg_sub]
  exact norm_T_sub_Tn n

/-- `T` is a compact operator. -/
theorem T_isCompactOperator : IsCompactOperator T :=
  isCompactOperator_of_tendsto tendsto_Tn (Filter.Eventually.of_forall isCompactOperator_Tn)

/-! ## §6 — NEW: the exact spectrum.  Every eigenvalue is some `dseq i`. -/

lemma exists_ne_zero_coord {f : H2} (hf : f ≠ 0) : ∃ i : ℕ, (f : ∀ _ : ℕ, ℂ) i ≠ 0 := by
  by_contra hc
  push Not at hc
  exact hf (by ext i; simpa using hc i)

/-- **Converse to `hasEigenvalue_T`.** The spectrum of a diagonal operator is contained in
the closure of its diagonal; here `0` is not an eigenvalue, so every eigenvalue is a `dseq i`. -/
theorem eigenvalue_mem_range {μ : ℂ}
    (h : Module.End.HasEigenvalue (T : Module.End ℂ H2) μ) : ∃ i : ℕ, (dseq i : ℂ) = μ := by
  obtain ⟨f, hfmem, hf0⟩ := h.exists_hasEigenvector
  rw [Module.End.mem_eigenspace_iff] at hfmem
  obtain ⟨i, hi⟩ := exists_ne_zero_coord hf0
  refine ⟨i, ?_⟩
  have hcoord := congrArg (fun g : H2 => (g : ∀ _ : ℕ, ℂ) i) hfmem
  simp only [ContinuousLinearMap.coe_coe, T_apply, lp.coeFn_smul, Pi.smul_apply,
    smul_eq_mul] at hcoord
  exact mul_right_cancel₀ hi hcoord

/-- **Exact real spectrum**: `μ` is an eigenvalue iff `μ = 1/(i+1)` for some `i`. -/
theorem real_hasEigenvalue_iff (μ : ℝ) :
    Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ)) ↔ ∃ i : ℕ, dseq i = μ := by
  constructor
  · intro h
    obtain ⟨i, hi⟩ := eigenvalue_mem_range h
    exact ⟨i, by exact_mod_cast hi⟩
  · rintro ⟨i, rfl⟩
    exact hasEigenvalue_T i

/-- The eigenvalue set is INFINITE: the operator has infinitely many distinct eigenvalues. -/
theorem infinite_eigenvalues :
    {μ : ℝ | Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Infinite := by
  apply Set.Infinite.mono (s := Set.range dseq)
  · rintro x ⟨i, rfl⟩; exact hasEigenvalue_T i
  · exact Set.infinite_range_of_injective dseq_injective

/-! ## §7 — the space really is infinite dimensional -/

theorem not_finiteDimensional : ¬ FiniteDimensional ℂ H2 := by
  intro hfd
  haveI : Module.Finite ℂ H2 := hfd
  have hinj : Function.Injective (fun i : ℕ => ((dseq i : ℝ) : ℂ)) := by
    intro i j hij
    simp only [Complex.ofReal_inj] at hij
    exact dseq_injective hij
  have hli : LinearIndependent ℂ e :=
    Module.End.eigenvectors_linearIndependent' (T : Module.End ℂ H2)
      (fun i : ℕ => ((dseq i : ℝ) : ℂ)) hinj e (fun i => hasEigenvector_T i)
  exact Module.Finite.not_linearIndependent_of_infinite e hli

/-! ## §8 — the bridge to `eigCount` -/

lemma eigCount_def (lam : ℝ) :
    eigCount T lam =
      {μ : ℝ | lam ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.ncard :=
  rfl

/-- **THE POINT (finiteness).** For every `lam > 0` the band above `lam` is finite —
this is `finite_eigenvalues_above` applied to an operator with an INFINITE spectrum. -/
theorem finite_above (lam : ℝ) (hlam : 0 < lam) :
    {μ : ℝ | lam ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Finite :=
  finite_eigenvalues_above T_isCompactOperator T_isSymmetric hlam

/-- **THE POINT (non-vacuity).** For `0 < lam ≤ 1` the band above `lam` is NON-EMPTY. -/
theorem nonempty_above (lam : ℝ) (hlam1 : lam ≤ 1) :
    {μ : ℝ | lam ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Nonempty := by
  refine ⟨1, ?_, ?_⟩
  · rwa [abs_one]
  · have := hasEigenvalue_T 0
    rwa [dseq_zero, Complex.ofReal_one] at this

/-! ## §9 — the exact counting function:  N(lam) = ⌊1/lam⌋ -/

lemma le_dseq_iff {lam : ℝ} (hlam : 0 < lam) (i : ℕ) :
    lam ≤ dseq i ↔ i < ⌊(1 : ℝ) / lam⌋₊ := by
  have hpos : (0 : ℝ) < (i : ℝ) + 1 := by positivity
  have hinv : (0 : ℝ) ≤ 1 / lam := by positivity
  have key : lam ≤ dseq i ↔ ((i : ℝ) + 1) ≤ 1 / lam := by
    unfold dseq
    rw [le_div_iff₀ hpos, le_div_iff₀ hlam, mul_comm]
  rw [key, Nat.lt_iff_add_one_le, Nat.le_floor_iff hinv]
  push_cast
  tauto

/-- The eigenvalue band above `lam` is exactly `dseq '' {0, …, ⌊1/lam⌋-1}`. -/
theorem eigenvalues_above_eq_image {lam : ℝ} (hlam : 0 < lam) :
    {μ : ℝ | lam ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}
      = dseq '' ↑(Finset.range ⌊(1 : ℝ) / lam⌋₊) := by
  ext μ
  simp only [Set.mem_setOf_eq, Finset.coe_range, Set.mem_image, Set.mem_Iio]
  constructor
  · rintro ⟨habs, hev⟩
    obtain ⟨i, rfl⟩ := (real_hasEigenvalue_iff μ).mp hev
    rw [abs_of_pos (dseq_pos i)] at habs
    exact ⟨i, (le_dseq_iff hlam i).mp habs, rfl⟩
  · rintro ⟨i, hi, rfl⟩
    refine ⟨?_, hasEigenvalue_T i⟩
    rw [abs_of_pos (dseq_pos i)]
    exact (le_dseq_iff hlam i).mpr hi

/-- **EXPLICIT WEYL-TYPE LAW.** `eigCount T lam = ⌊1/lam⌋` for every `lam > 0`. -/
theorem eigCount_eq_floor {lam : ℝ} (hlam : 0 < lam) :
    eigCount T lam = ⌊(1 : ℝ) / lam⌋₊ := by
  rw [eigCount_def, eigenvalues_above_eq_image hlam,
    Set.ncard_image_of_injective _ dseq_injective, Set.ncard_coe_finset, Finset.card_range]

/-- Positive count for every `0 < lam ≤ 1`. -/
theorem eigCount_pos {lam : ℝ} (hlam0 : 0 < lam) (hlam1 : lam ≤ 1) : 0 < eigCount T lam := by
  rw [eigCount_def, Set.ncard_pos (finite_above lam hlam0)]
  exact nonempty_above lam hlam1

/-! ## §10 — fully explicit values -/

/-- `eigCount T 1 = 1`. -/
theorem eigCount_one : eigCount T 1 = 1 := by
  rw [eigCount_eq_floor (by norm_num)]
  norm_num

/-- `eigCount T (1/3) = 3`. -/
theorem eigCount_third : eigCount T (1 / 3) = 3 := by
  rw [eigCount_eq_floor (by norm_num)]
  norm_num

/-- `eigCount T (1/10) = 10`. -/
theorem eigCount_tenth : eigCount T (1 / 10) = 10 := by
  rw [eigCount_eq_floor (by norm_num)]
  norm_num

/-- The band above `1/3` is exactly `{1, 1/2, 1/3}`. -/
theorem eigenvalues_above_third :
    {μ : ℝ | (1 / 3 : ℝ) ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}
      = ({1, 1 / 2, 1 / 3} : Set ℝ) := by
  rw [eigenvalues_above_eq_image (by norm_num : (0 : ℝ) < 1 / 3)]
  have hfl : ⌊(1 : ℝ) / (1 / 3)⌋₊ = 3 := by norm_num
  rw [hfl, show (Finset.range 3 : Finset ℕ) = {0, 1, 2} from by decide]
  simp only [Finset.coe_insert, Finset.coe_singleton, Set.image_insert_eq, Set.image_singleton,
    dseq_zero, dseq_one, dseq_two]

/-- Genuine ZERO (not the `ncard` junk value): above `lam = 2` there is no eigenvalue. -/
theorem eigCount_two : eigCount T 2 = 0 := by
  rw [eigCount_eq_floor (by norm_num), Nat.floor_eq_zero]
  norm_num

/-- ... and it really means "no eigenvalue", via the parent module's `eigCount_eq_zero_iff`. -/
theorem no_eigenvalue_above_two (μ : ℝ) (hμ : (2 : ℝ) ≤ |μ|) :
    ¬ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ)) :=
  (eigCount_eq_zero_iff T_isCompactOperator T_isSymmetric (by norm_num)).mp eigCount_two μ hμ

/-! ## §10b — cross-check: the count 3 computed a second, independent way -/

theorem ncard_triple : ({1, 1 / 2, 1 / 3} : Set ℝ).ncard = 3 := by
  rw [Set.ncard_insert_of_notMem (by norm_num) (Set.toFinite _),
    Set.ncard_insert_of_notMem (by norm_num) (Set.toFinite _), Set.ncard_singleton]

/-- Same number, obtained through the explicit set `{1, 1/2, 1/3}` instead of `⌊1/lam⌋`. -/
theorem eigCount_third_cross_check :
    eigCount T (1 / 3) = ({1, 1 / 2, 1 / 3} : Set ℝ).ncard := by
  rw [eigCount_def, eigenvalues_above_third]

example : eigCount T (1 / 3) = 3 := by rw [eigCount_third_cross_check, ncard_triple]

/-! ## §11 — the assembled positive instance -/

/-- **SC-GAP-001 CLOSED.**  On the infinite-dimensional separable Hilbert space
`ℓ²(ℕ, ℂ)` the diagonal operator `T` with diagonal `1/(i+1)` is compact and symmetric,
its space is NOT finite dimensional, its eigenvalue set is INFINITE, yet every band
`{μ : lam ≤ |μ|}` is finite and — for `0 < lam ≤ 1` — non-empty, with the exact count
`eigCount T lam = ⌊1/lam⌋`.  The counting theorem therefore has genuine content in
infinite dimension. -/
theorem positive_instance_infinite_dimensional :
    ¬ FiniteDimensional ℂ H2 ∧
    IsCompactOperator T ∧
    LinearMap.IsSymmetric (T : H2 →ₗ[ℂ] H2) ∧
    {μ : ℝ | Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Infinite ∧
    (∀ lam : ℝ, 0 < lam →
      {μ : ℝ | lam ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Finite) ∧
    (∀ lam : ℝ, 0 < lam → lam ≤ 1 →
      {μ : ℝ | lam ≤ |μ| ∧
        Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Nonempty) ∧
    (∀ lam : ℝ, 0 < lam → lam ≤ 1 → 0 < eigCount T lam) ∧
    (∀ lam : ℝ, 0 < lam → eigCount T lam = ⌊(1 : ℝ) / lam⌋₊) ∧
    eigCount T (1 / 3) = 3 :=
  ⟨not_finiteDimensional, T_isCompactOperator, T_isSymmetric, infinite_eigenvalues,
    fun lam h => finite_above lam h,
    fun lam _ h1 => nonempty_above lam h1,
    fun _ h0 h1 => eigCount_pos h0 h1,
    fun _ h => eigCount_eq_floor h,
    eigCount_third⟩

/-- The parent module's `eigCount_antitone` is non-vacuous here: strictly decreasing counts. -/
theorem eigCount_strict_example : eigCount T (1 / 3) < eigCount T (1 / 10) := by
  rw [eigCount_third, eigCount_tenth]; norm_num

/-- And `eigCount_eq_finset_card` produces a genuine `Finset` of size 3 above `1/3`. -/
theorem finset_above_third :
    ∃ F : Finset ℝ, (↑F : Set ℝ) = ({1, 1 / 2, 1 / 3} : Set ℝ) ∧ F.card = 3 := by
  obtain ⟨F, hF, hcard⟩ :=
    eigCount_eq_finset_card T_isCompactOperator T_isSymmetric (by norm_num : (0 : ℝ) < 1 / 3)
  exact ⟨F, hF.trans eigenvalues_above_third, hcard.trans eigCount_third⟩

end TamesisLab.Foundations.SpectralCounting.InfDim

#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.T_isCompactOperator
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.T_isSymmetric
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.not_finiteDimensional
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.infinite_eigenvalues
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigenvalue_mem_range
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.real_hasEigenvalue_iff
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.finite_above
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.nonempty_above
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigCount_eq_floor
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigCount_pos
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigCount_third
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigenvalues_above_third
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigCount_third_cross_check
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.eigCount_two
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.no_eigenvalue_above_two
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.positive_instance_infinite_dimensional
#print axioms TamesisLab.Foundations.SpectralCounting.InfDim.finset_above_third
