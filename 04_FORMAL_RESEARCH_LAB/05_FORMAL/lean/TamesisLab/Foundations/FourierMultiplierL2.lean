/-
Probe A : L^2 Fourier multiplier WITHOUT smoothness.
Target: replace `Function.HasTemperateGrowth` by "measurable + essentially bounded".
-/
import Mathlib.Analysis.Distribution.Sobolev

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 1000000

noncomputable section

namespace TamesisLab.Foundations.FourierMultiplierL2

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-! ## Step 0 : bounded a.e.-measurable symbol is an element of `L∞`. NO smoothness. -/

def ofBounded {g : E → ℂ} (hm : AEStronglyMeasurable g (volume : Measure E)) (C : ℝ)
    (hC : ∀ x, ‖g x‖ ≤ C) : Lp ℂ ∞ (volume : Measure E) :=
  (memLp_top_of_bound hm C (.of_forall hC)).toLp g

/-! ## Step 1 : multiplication by an `L∞` function is bounded on `L²`. -/

variable (F) in
def mulL2 (g : Lp ℂ ∞ (volume : Measure E)) :
    Lp (α := E) F 2 →L[ℂ] Lp (α := E) F 2 :=
  LinearMap.mkContinuous
    { toFun := fun f ↦ g • f
      map_add' := fun f₁ f₂ ↦ Lp.add_smul g f₁ f₂
      map_smul' := fun c f ↦ (Lp.smul_comm c g f).symm }
    ‖g‖ (fun f ↦ Lp.norm_smul_le g f)

@[simp]
theorem mulL2_apply (g : Lp ℂ ∞ (volume : Measure E)) (f : Lp (α := E) F 2) :
    mulL2 F g f = g • f := rfl

theorem norm_mulL2_apply_le (g : Lp ℂ ∞ (volume : Measure E)) (f : Lp (α := E) F 2) :
    ‖mulL2 F g f‖ ≤ ‖g‖ * ‖f‖ := Lp.norm_smul_le g f

theorem norm_mulL2_le (g : Lp ℂ ∞ (volume : Measure E)) :
    ‖mulL2 F g‖ ≤ ‖g‖ :=
  LinearMap.mkContinuous_norm_le _ (norm_nonneg g) _

/-! ## Step 2 : conjugate with the Plancherel isometry. -/

theorem norm_fourierInv_eq (y : Lp (α := E) F 2) :
    ‖(𝓕⁻ y : Lp (α := E) F 2)‖ = ‖y‖ := by
  rw [← Lp.norm_fourier_eq (𝓕⁻ y), fourier_fourierInv_eq]

variable (F) in
/-- The Fourier multiplier on `L²` with an arbitrary `L∞` symbol. No smoothness required. -/
def fourierMulL2 (g : Lp ℂ ∞ (volume : Measure E)) :
    Lp (α := E) F 2 →L[ℂ] Lp (α := E) F 2 :=
  fourierInvCLM ℂ (Lp (α := E) F 2) ∘L mulL2 F g ∘L fourierCLM ℂ (Lp (α := E) F 2)

theorem fourierMulL2_apply (g : Lp ℂ ∞ (volume : Measure E)) (f : Lp (α := E) F 2) :
    fourierMulL2 F g f = 𝓕⁻ (mulL2 F g (𝓕 f)) := rfl

theorem norm_fourierMulL2_apply_le (g : Lp ℂ ∞ (volume : Measure E)) (f : Lp (α := E) F 2) :
    ‖fourierMulL2 F g f‖ ≤ ‖g‖ * ‖f‖ := by
  rw [fourierMulL2_apply, norm_fourierInv_eq]
  refine (norm_mulL2_apply_le g _).trans_eq ?_
  rw [Lp.norm_fourier_eq]

theorem norm_fourierMulL2_le (g : Lp ℂ ∞ (volume : Measure E)) :
    ‖fourierMulL2 F g‖ ≤ ‖g‖ :=
  ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg g) (norm_fourierMulL2_apply_le g)

/-! ## Step 3 : compatibility with the Mathlib multiplier on the temperate overlap. -/

/-- On the overlap (temperate + bounded symbol) the new `L²` operator IS the Mathlib
`TemperedDistribution.fourierMultiplierCLM`. This is what makes the `L²` operator a genuine
extension rather than an unrelated new object. -/
theorem toTemperedDistribution_fourierMulL2_eq {g : E → ℂ} (hg₁ : g.HasTemperateGrowth)
    (hm : AEStronglyMeasurable g (volume : Measure E)) (C : ℝ) (hC : ∀ x, ‖g x‖ ≤ C)
    (u : Lp (α := E) F 2) :
    ((fourierMulL2 F (ofBounded hm C hC) u : Lp (α := E) F 2) : 𝓢'(E, F))
      = TemperedDistribution.fourierMultiplierCLM F g (u : 𝓢'(E, F)) := by
  rw [fourierMulL2_apply, mulL2_apply, ← Lp.fourierInv_toTemperedDistribution_eq]
  unfold ofBounded
  rw [Lp.toTemperedDistribution_smul_eq hg₁ (memLp_top_of_bound hm C (.of_forall hC)) (𝓕 u),
    ← Lp.fourier_toTemperedDistribution_eq, TemperedDistribution.fourierMultiplierCLM_apply]

/-! ## Step 4 : Sobolev level. -/

theorem memSobolev_besselPotential_neg_coe (s : ℝ) (w : Lp (α := E) F 2) :
    MemSobolev s 2 (besselPotential E F (-s) (w : 𝓢'(E, F))) := by
  rw [memSobolev_besselPotential_iff, neg_add_cancel]
  exact memSobolev_zero_iff.mpr ⟨w, rfl⟩

/-- Every `L²` function is the order-`s` Bessel potential of some `H^s` distribution. -/
theorem exists_memSobolev_besselPotential_eq (s : ℝ) (w : Lp (α := E) F 2) :
    ∃ v : 𝓢'(E, F), MemSobolev s 2 v ∧ besselPotential E F s v = (w : 𝓢'(E, F)) := by
  refine ⟨besselPotential E F (-s) (w : 𝓢'(E, F)), memSobolev_besselPotential_neg_coe s w, ?_⟩
  rw [besselPotential_besselPotential_apply, neg_add_cancel, besselPotential_zero]
  rfl

/-- **Piece A, L² form (general symbol).** For ANY `L∞` symbol `g` (measurable, essentially
bounded, NO smoothness) and any `L²` function `u`, there is a tempered distribution `v ∈ H^s`
whose Bessel potential of order `s` is the `L²` function `g(D) u`, with the Plancherel bound
`‖g(D) u‖₂ ≤ ‖g‖_∞ ‖u‖₂`. -/
theorem exists_memSobolev_besselPotential_eq_fourierMulL2 (s : ℝ)
    (g : Lp ℂ ∞ (volume : Measure E)) (u : Lp (α := E) F 2) :
    ∃ v : 𝓢'(E, F), MemSobolev s 2 v ∧
      besselPotential E F s v = ((fourierMulL2 F g u : Lp (α := E) F 2) : 𝓢'(E, F)) ∧
      ‖(fourierMulL2 F g u : Lp (α := E) F 2)‖ ≤ ‖g‖ * ‖u‖ := by
  obtain ⟨v, hv₁, hv₂⟩ := exists_memSobolev_besselPotential_eq s (fourierMulL2 F g u)
  exact ⟨v, hv₁, hv₂, norm_fourierMulL2_apply_le g u⟩

/-- **Piece A, temperate overlap, tied to `f`.** If `u` is the `L²` representative of
`besselPotential s f`, then the Mathlib multiplier applied to `f` has `L²` representative
`g(D) u` after applying `besselPotential s`; i.e. the multiplier commutes with the Bessel
potential and acts on the `L²` side exactly by `fourierMulL2`. -/
theorem besselPotential_fourierMultiplierCLM_eq {s : ℝ} {f : 𝓢'(E, F)} {u : Lp (α := E) F 2}
    (hu : besselPotential E F s f = (u : 𝓢'(E, F)))
    {g : E → ℂ} (hg₁ : g.HasTemperateGrowth)
    (hm : AEStronglyMeasurable g (volume : Measure E)) (C : ℝ) (hC : ∀ x, ‖g x‖ ≤ C) :
    besselPotential E F s (TemperedDistribution.fourierMultiplierCLM F g f) =
      ((fourierMulL2 F (ofBounded hm C hC) u : Lp (α := E) F 2) : 𝓢'(E, F)) := by
  rw [toTemperedDistribution_fourierMulL2_eq hg₁ hm C hC u, ← hu]
  simp only [besselPotential]
  rw [fourierMultiplierCLM_fourierMultiplierCLM_apply hg₁ (by fun_prop),
    fourierMultiplierCLM_fourierMultiplierCLM_apply (by fun_prop) hg₁, mul_comm g]

/-! ## Step 4b : canonicity — the produced `v` is UNIQUE. -/

theorem toTemperedDistribution_injective :
    Function.Injective (fun w : Lp (α := E) F 2 ↦ (w : 𝓢'(E, F))) := by
  have h := MeasureTheory.Lp.ker_toTemperedDistributionCLM_eq_bot
    (E := E) (F := F) (μ := (volume : Measure E)) (p := 2)
  exact LinearMap.ker_eq_bot.mp h

theorem besselPotential_injective (s : ℝ) :
    Function.Injective (besselPotential E F s) := by
  intro a b h
  have h' := congrArg (besselPotential E F (-s)) h
  rw [besselPotential_besselPotential_apply, besselPotential_besselPotential_apply,
    add_neg_cancel, besselPotential_zero] at h'
  simpa using h'

/-- **Piece A, final H^s form.** For a Sobolev distribution `f ∈ H^s` and ANY essentially
bounded measurable symbol `g` (no smoothness, no continuity), there is a UNIQUE tempered
distribution `v` such that `v ∈ H^s` and `besselPotential s v = g(D) (besselPotential s f)`
on the `L²` side. `hf` is genuinely used: it supplies the `L²` representative. -/
theorem MemSobolev.existsUnique_fourierMulL2 {s : ℝ} {f : 𝓢'(E, F)} (hf : MemSobolev s 2 f)
    (g : Lp ℂ ∞ (volume : Measure E)) :
    ∃! v : 𝓢'(E, F), MemSobolev s 2 v ∧ ∃ u : Lp (α := E) F 2,
      besselPotential E F s f = (u : 𝓢'(E, F)) ∧
      besselPotential E F s v = ((fourierMulL2 F g u : Lp (α := E) F 2) : 𝓢'(E, F)) ∧
      ‖(fourierMulL2 F g u : Lp (α := E) F 2)‖ ≤ ‖g‖ * ‖u‖ := by
  obtain ⟨u, hu⟩ := hf
  obtain ⟨v, hv₁, hv₂, hv₃⟩ := exists_memSobolev_besselPotential_eq_fourierMulL2 s g u
  refine ⟨v, ⟨hv₁, u, hu, hv₂, hv₃⟩, ?_⟩
  rintro y ⟨-, u', hu', hy, -⟩
  have hueq : u' = u := toTemperedDistribution_injective (hu'.symm.trans hu)
  subst hueq
  exact besselPotential_injective s (hy.trans hv₂.symm)

/-! ## Step 5 : the vacuity trap for the naive weakening. -/

/-- A Leray-type symbol : bounded, measurable, discontinuous at the origin. -/
def leraySymbol (E : Type*) [NormedAddCommGroup E] : E → ℂ :=
  Set.indicator {(0 : E)}ᶜ (fun _ ↦ 1)

theorem norm_leraySymbol_le (x : E) : ‖leraySymbol E x‖ ≤ 1 :=
  (norm_indicator_le_norm_self (fun _ ↦ (1 : ℂ)) x).trans (by simp)

theorem measurable_leraySymbol : Measurable (leraySymbol E) :=
  measurable_const.indicator ((T1Space.t1 (0 : E)).measurableSet.compl)

theorem leraySymbol_zero : leraySymbol E (0 : E) = 0 := by
  simp [leraySymbol]

theorem leraySymbol_of_ne {x : E} (hx : x ≠ 0) : leraySymbol E x = 1 := by
  simp [leraySymbol, hx]

theorem not_hasTemperateGrowth_leraySymbol [Nontrivial E] :
    ¬ (leraySymbol E).HasTemperateGrowth := by
  intro h
  have hc : Continuous (leraySymbol E) := h.1.continuous
  have h1 : Tendsto (leraySymbol E) (𝓝[≠] (0 : E)) (𝓝 (0 : ℂ)) := by
    rw [← leraySymbol_zero (E := E)]
    exact (hc.tendsto (0 : E)).mono_left nhdsWithin_le_nhds
  have h2 : Tendsto (leraySymbol E) (𝓝[≠] (0 : E)) (𝓝 (1 : ℂ)) := by
    refine (tendsto_const_nhds (x := (1 : ℂ))).congr' ?_
    filter_upwards [self_mem_nhdsWithin] with x hx
    exact (leraySymbol_of_ne hx).symm
  exact zero_ne_one (tendsto_nhds_unique h1 h2)

/-- The existing `fourierMultiplierCLM` COLLAPSES TO ZERO on non-temperate symbols:
`smulLeftCLM` is a `dite` on `HasTemperateGrowth` with junk value `0`. -/
theorem fourierMultiplierCLM_eq_zero_of_not_temperate {g : E → ℂ} (hg : ¬ g.HasTemperateGrowth) :
    TemperedDistribution.fourierMultiplierCLM F g = 0 := by
  ext f u
  rw [TemperedDistribution.fourierMultiplierCLM_apply_apply]
  rw [show SchwartzMap.smulLeftCLM ℂ g (𝓕⁻ u) = 0 by simp [SchwartzMap.smulLeftCLM, hg]]
  simp

/-- Consequence: deleting `HasTemperateGrowth` from the Mathlib lemma yields a VACUOUS
statement for Leray-type symbols — the conclusion is a statement about `0`. -/
theorem fourierMultiplierCLM_leraySymbol_eq_zero [Nontrivial E] :
    TemperedDistribution.fourierMultiplierCLM F (leraySymbol E) = (0 : 𝓢'(E, F) →L[ℂ] 𝓢'(E, F)) :=
  fourierMultiplierCLM_eq_zero_of_not_temperate not_hasTemperateGrowth_leraySymbol

/-- **THE NAIVE WEAKENING IS PROVABLE — AND VACUOUS.** Deleting `HasTemperateGrowth` from
`TemperedDistribution.MemSobolev.fourierMultiplierCLM_of_bounded` gives a theorem that is
proved in five lines by a case split, because on the non-temperate branch the operator is
identically `0`. It therefore says NOTHING about Leray-type symbols. -/
theorem MemSobolev.fourierMultiplierCLM_of_bounded_no_smoothness {s : ℝ} {f : 𝓢'(E, F)}
    (hf : MemSobolev s 2 f) {g : E → ℂ} (hg₂ : ∃ C, ∀ x, ‖g x‖ ≤ C) :
    MemSobolev s 2 (TemperedDistribution.fourierMultiplierCLM F g f) := by
  by_cases hg₁ : g.HasTemperateGrowth
  · exact TemperedDistribution.MemSobolev.fourierMultiplierCLM_of_bounded hf hg₁ hg₂
  · rw [fourierMultiplierCLM_eq_zero_of_not_temperate hg₁]
    simpa using memSobolev_fun_zero E F s 2

/-! ## Step 6 : positive instance for the new L² operator. -/

def leraySymbolL2 : Lp ℂ ∞ (volume : Measure E) :=
  ofBounded (measurable_leraySymbol (E := E)).aestronglyMeasurable 1 norm_leraySymbol_le

/-- POSITIVE INSTANCE: the new `L²` theorem is non-vacuous — it applies to a genuinely
discontinuous, non-temperate, essentially bounded symbol, for which the Mathlib operator
is identically `0`. -/
theorem positive_instance [Nontrivial E] (s : ℝ) (u : Lp (α := E) F 2) :
    (¬ (leraySymbol E).HasTemperateGrowth) ∧
    (TemperedDistribution.fourierMultiplierCLM F (leraySymbol E) =
      (0 : 𝓢'(E, F) →L[ℂ] 𝓢'(E, F))) ∧
    ∃ v : 𝓢'(E, F), MemSobolev s 2 v ∧
      besselPotential E F s v =
        ((fourierMulL2 F (leraySymbolL2 (E := E)) u : Lp (α := E) F 2) : 𝓢'(E, F)) ∧
      ‖(fourierMulL2 F (leraySymbolL2 (E := E)) u : Lp (α := E) F 2)‖ ≤
        ‖(leraySymbolL2 (E := E))‖ * ‖u‖ :=
  ⟨not_hasTemperateGrowth_leraySymbol, fourierMultiplierCLM_leraySymbol_eq_zero,
    exists_memSobolev_besselPotential_eq_fourierMulL2 s _ u⟩

/-- POSITIVE INSTANCE for the canonical (unique) form. -/
theorem positive_instance_unique [Nontrivial E] {s : ℝ} {f : 𝓢'(E, F)} (hf : MemSobolev s 2 f) :
    ∃! v : 𝓢'(E, F), MemSobolev s 2 v ∧ ∃ u : Lp (α := E) F 2,
      besselPotential E F s f = (u : 𝓢'(E, F)) ∧
      besselPotential E F s v =
        ((fourierMulL2 F (leraySymbolL2 (E := E)) u : Lp (α := E) F 2) : 𝓢'(E, F)) ∧
      ‖(fourierMulL2 F (leraySymbolL2 (E := E)) u : Lp (α := E) F 2)‖ ≤
        ‖(leraySymbolL2 (E := E))‖ * ‖u‖ :=
  MemSobolev.existsUnique_fourierMulL2 hf _

/-! ## Step 7 : the REAL Leray projector symbol component `ξ ↦ ⟪ξ,m⟫⟪ξ,n⟫/‖ξ‖²`. -/

/-- A genuine off-diagonal component of the Leray projector symbol. In coordinates this is
`ξ_j ξ_k / |ξ|²`. Bounded by `‖m‖‖n‖`, measurable, discontinuous at the origin. -/
def lerayComponent (m n : E) : E → ℂ :=
  fun x ↦ ((inner ℝ x m * inner ℝ x n / ‖x‖ ^ 2 : ℝ) : ℂ)

theorem lerayComponent_zero (m n : E) : lerayComponent m n (0 : E) = 0 := by
  simp [lerayComponent]

theorem norm_lerayComponent_le (m n : E) (x : E) : ‖lerayComponent m n x‖ ≤ ‖m‖ * ‖n‖ := by
  rcases eq_or_ne x 0 with rfl | hx
  · rw [lerayComponent_zero, norm_zero]; positivity
  · have hpos : (0 : ℝ) < |‖x‖ ^ 2| := abs_pos.mpr (pow_ne_zero 2 (norm_ne_zero_iff.mpr hx))
    rw [lerayComponent, Complex.norm_real, Real.norm_eq_abs, abs_div, abs_mul,
      div_le_iff₀ hpos, abs_pow, abs_norm]
    calc |inner ℝ x m| * |inner ℝ x n| ≤ (‖x‖ * ‖m‖) * (‖x‖ * ‖n‖) :=
          mul_le_mul (abs_real_inner_le_norm x m) (abs_real_inner_le_norm x n)
            (abs_nonneg _) (by positivity)
      _ = ‖m‖ * ‖n‖ * ‖x‖ ^ 2 := by ring

theorem measurable_lerayComponent (m n : E) : Measurable (lerayComponent m n) := by
  unfold lerayComponent
  fun_prop

theorem lerayComponent_smul_self {m : E} (hm : m ≠ 0) {t : ℝ} (ht : t ≠ 0) :
    lerayComponent m m (t • m) = ((‖m‖ ^ 2 : ℝ) : ℂ) := by
  have hn : ‖m‖ ≠ 0 := norm_ne_zero_iff.mpr hm
  have hin : inner ℝ (t • m) m = t * ‖m‖ ^ 2 := by
    rw [real_inner_smul_left, real_inner_self_eq_norm_sq]
  have hnn : ‖t • m‖ ^ 2 = t ^ 2 * ‖m‖ ^ 2 := by
    rw [norm_smul, Real.norm_eq_abs, mul_pow, sq_abs]
  rw [lerayComponent, hin, hnn]
  congr 1
  field_simp

theorem not_hasTemperateGrowth_lerayComponent {m : E} (hm : m ≠ 0) :
    ¬ (lerayComponent m m).HasTemperateGrowth := by
  intro h
  have hc : Continuous (lerayComponent m m) := h.1.continuous
  have hline : Continuous (fun t : ℝ ↦ t • m) := by fun_prop
  have h1 : Tendsto (fun t : ℝ ↦ lerayComponent m m (t • m)) (𝓝[≠] (0 : ℝ)) (𝓝 (0 : ℂ)) := by
    have h0 : lerayComponent m m ((0 : ℝ) • m) = 0 := by
      rw [zero_smul, lerayComponent_zero]
    rw [← h0]
    exact ((hc.comp hline).tendsto (0 : ℝ)).mono_left nhdsWithin_le_nhds
  have h2 : Tendsto (fun t : ℝ ↦ lerayComponent m m (t • m)) (𝓝[≠] (0 : ℝ))
      (𝓝 ((‖m‖ ^ 2 : ℝ) : ℂ)) := by
    refine (tendsto_const_nhds (x := ((‖m‖ ^ 2 : ℝ) : ℂ))).congr' ?_
    filter_upwards [self_mem_nhdsWithin] with t ht
    exact (lerayComponent_smul_self hm ht).symm
  have hzero : ((‖m‖ ^ 2 : ℝ) : ℂ) = 0 := (tendsto_nhds_unique h1 h2).symm
  exact pow_ne_zero 2 (norm_ne_zero_iff.mpr hm) (by exact_mod_cast hzero)

def lerayComponentL2 (m n : E) : Lp ℂ ∞ (volume : Measure E) :=
  ofBounded (measurable_lerayComponent m n).aestronglyMeasurable (‖m‖ * ‖n‖)
    (norm_lerayComponent_le m n)

/-- POSITIVE INSTANCE WITH THE REAL SYMBOL: for `ξ ↦ ⟪ξ,m⟫⟪ξ,m⟫/‖ξ‖²` (a component of the
Leray projector symbol) the Mathlib operator is identically `0`, while the new `L²` operator
gives a unique `H^s` solution with the Plancherel bound. -/
theorem positive_instance_leray {m : E} (hm : m ≠ 0) {s : ℝ} {f : 𝓢'(E, F)}
    (hf : MemSobolev s 2 f) :
    (¬ (lerayComponent m m).HasTemperateGrowth) ∧
    (TemperedDistribution.fourierMultiplierCLM F (lerayComponent m m) =
      (0 : 𝓢'(E, F) →L[ℂ] 𝓢'(E, F))) ∧
    ∃! v : 𝓢'(E, F), MemSobolev s 2 v ∧ ∃ u : Lp (α := E) F 2,
      besselPotential E F s f = (u : 𝓢'(E, F)) ∧
      besselPotential E F s v =
        ((fourierMulL2 F (lerayComponentL2 m m) u : Lp (α := E) F 2) : 𝓢'(E, F)) ∧
      ‖(fourierMulL2 F (lerayComponentL2 m m) u : Lp (α := E) F 2)‖ ≤
        ‖(lerayComponentL2 m m : Lp ℂ ∞ (volume : Measure E))‖ * ‖u‖ :=
  ⟨not_hasTemperateGrowth_lerayComponent hm,
   fourierMultiplierCLM_eq_zero_of_not_temperate (not_hasTemperateGrowth_lerayComponent hm),
   MemSobolev.existsUnique_fourierMulL2 hf _⟩

end TamesisLab.Foundations.FourierMultiplierL2

#print axioms TamesisLab.Foundations.FourierMultiplierL2.mulL2
#print axioms TamesisLab.Foundations.FourierMultiplierL2.norm_mulL2_le
#print axioms TamesisLab.Foundations.FourierMultiplierL2.fourierMulL2
#print axioms TamesisLab.Foundations.FourierMultiplierL2.norm_fourierMulL2_le
#print axioms TamesisLab.Foundations.FourierMultiplierL2.toTemperedDistribution_fourierMulL2_eq
#print axioms TamesisLab.Foundations.FourierMultiplierL2.besselPotential_fourierMultiplierCLM_eq
#print axioms TamesisLab.Foundations.FourierMultiplierL2.exists_memSobolev_besselPotential_eq_fourierMulL2
#print axioms TamesisLab.Foundations.FourierMultiplierL2.MemSobolev.existsUnique_fourierMulL2
#print axioms TamesisLab.Foundations.FourierMultiplierL2.not_hasTemperateGrowth_leraySymbol
#print axioms TamesisLab.Foundations.FourierMultiplierL2.fourierMultiplierCLM_leraySymbol_eq_zero
#print axioms TamesisLab.Foundations.FourierMultiplierL2.positive_instance
#print axioms TamesisLab.Foundations.FourierMultiplierL2.positive_instance_unique
#print axioms TamesisLab.Foundations.FourierMultiplierL2.not_hasTemperateGrowth_lerayComponent
#print axioms TamesisLab.Foundations.FourierMultiplierL2.norm_lerayComponent_le
#print axioms TamesisLab.Foundations.FourierMultiplierL2.positive_instance_leray
#print axioms TamesisLab.Foundations.FourierMultiplierL2.MemSobolev.fourierMultiplierCLM_of_bounded_no_smoothness
