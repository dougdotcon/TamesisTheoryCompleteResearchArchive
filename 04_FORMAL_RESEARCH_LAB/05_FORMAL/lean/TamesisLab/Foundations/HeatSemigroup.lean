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

`HEAT-GAP-001` (work item `FOUND-HEAT-SEMIGROUP-LAW-001` in `RESEARCH_QUEUE.yaml`) -- the
semigroup law `S(t+r) = S(t) ∘ S(r)` and strong continuity in `t` -- is CLOSED, both halves,
in Step H4 (`heatOpL2_add`/`heatOpL2_add'`) and Step H6 (`heatOpL2_continuousAt`) below.
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

/-! ## Step H4 : the semigroup law `S(t+r) = S(t) ∘ S(r)`, closing `HEAT-GAP-001` (part 1).

The mathematical content is the pointwise identity `exp(-(t+r)‖x‖²) = exp(-t‖x‖²)·exp(-r‖x‖²)`;
the engineering is lifting it through `ofBounded`/`Lp ℂ ∞` (Step (a)-(b)) and then through the
heterogeneous `Lp ∞ → Lp 2 → Lp 2` scalar action `mulL2` (Step (c)), and finally through the
`𝓕⁻/𝓕` round trip already used by `fourierMulL2_apply` (Step (d)). -/

/-- **Step (a).** The heat symbol is pointwise multiplicative in `t`: `exp(-(t+r)‖x‖²)
= exp(-t‖x‖²) · exp(-r‖x‖²)`. Purely `Real.exp_add`. -/
theorem heatSymbol_add (t r : ℝ) (x : E) :
    heatSymbol E (t + r) x = heatSymbol E t x * heatSymbol E r x := by
  unfold heatSymbol
  rw [← Complex.ofReal_mul]
  congr 1
  rw [← Real.exp_add]
  congr 1
  ring

/-- **Step (b).** Lifted to `L∞`: `mulL2` by `heatSymbolL2 (t+r)` agrees, applied to any `L²`
function, with the double application `mulL2 (heatSymbolL2 t) ∘ mulL2 (heatSymbolL2 r)`. Proved
by unfolding both sides to a.e. pointwise statements via `Lp.ext_iff`/`Lp.coeFn_lpSMul`/
`coeFn_heatSymbolL2`, mirroring `inner_smul_Lp_symm` in `LerayOrthogonal.lean`. -/
theorem mulL2_heatSymbolL2_heatSymbolL2 {t r : ℝ} (ht : 0 ≤ t) (hr : 0 ≤ r) (htr : 0 ≤ t + r)
    (f : Lp (α := E) F 2) :
    mulL2 F (heatSymbolL2 (E := E) ht) (mulL2 F (heatSymbolL2 (E := E) hr) f)
      = mulL2 F (heatSymbolL2 (E := E) htr) f := by
  simp only [mulL2_apply]
  rw [Lp.ext_iff]
  filter_upwards [Lp.coeFn_lpSMul (r := (2 : ℝ≥0∞)) (heatSymbolL2 (E := E) ht)
      (heatSymbolL2 (E := E) hr • f),
    Lp.coeFn_lpSMul (r := (2 : ℝ≥0∞)) (heatSymbolL2 (E := E) hr) f,
    Lp.coeFn_lpSMul (r := (2 : ℝ≥0∞)) (heatSymbolL2 (E := E) htr) f,
    coeFn_heatSymbolL2 (E := E) ht, coeFn_heatSymbolL2 (E := E) hr, coeFn_heatSymbolL2 (E := E) htr]
    with x h1 h2 h3 hs1 hs2 hs3
  rw [h1]
  simp only [Pi.smul_apply']
  rw [h2, h3]
  simp only [Pi.smul_apply']
  rw [hs1, hs2, hs3, heatSymbol_add, mul_smul]

/-- **Step (d) / package.** The heat semigroup satisfies the semigroup law `S(t+r) = S(t) ∘ S(r)`
on `L²(E, F)`, for all `t, r ≥ 0`. Closes the first half of `HEAT-GAP-001`. -/
theorem heatOpL2_add {t r : ℝ} (ht : 0 ≤ t) (hr : 0 ≤ r) (htr : 0 ≤ t + r)
    (f : Lp (α := E) F 2) :
    heatOpL2 F htr f = heatOpL2 F ht (heatOpL2 F hr f) := by
  rw [heatOpL2_apply, heatOpL2_apply, heatOpL2_apply, fourier_fourierInv_eq,
    ← mulL2_heatSymbolL2_heatSymbolL2 F ht hr htr]

/-- **The semigroup law, as an equality of continuous linear maps.** -/
theorem heatOpL2_add' {t r : ℝ} (ht : 0 ≤ t) (hr : 0 ≤ r) (htr : 0 ≤ t + r) :
    (heatOpL2 F htr : Lp (α := E) F 2 →L[ℂ] Lp (α := E) F 2)
      = heatOpL2 F ht ∘L heatOpL2 F hr :=
  ContinuousLinearMap.ext fun f => by
    rw [ContinuousLinearMap.comp_apply]
    exact heatOpL2_add F ht hr htr f

/-! ## Step H6 : strong continuity of `t ↦ e^{tΔ}` at every `t₀ ≥ 0`, for each fixed `f ∈ L²`,
closing the second half of `HEAT-GAP-001`.

The domain is the subtype `{t : ℝ // 0 ≤ t}` (with the subspace topology inherited from `ℝ`),
so that `heatOpL2` is a genuinely total function of the index -- no junk value is needed, unlike
for `t < 0` where `heatSymbolL2` is not even *defined* (the symbol `exp(-t‖x‖²)` is unbounded
there).

The proof is dominated convergence on the pointwise squared difference
`‖(heatSymbol t x - heatSymbol t₀ x) • g x‖ₑ²`, dominated by the FIXED integrable function
`4 ‖g x‖ₑ²` -- via the uniform bound `‖heatSymbol t x‖ ≤ 1` (`t ≥ 0`), NOT via a bound on the
`L∞`-essential-sup norm of the symbol difference itself, which does NOT vanish as `t → 0`
(concretely, `‖heatSymbolL2 t - heatSymbolL2 0‖_∞ = 1` for every `t > 0`, since
`sup_{x} |1 - exp(-t‖x‖²)| = 1`). This is exactly the reason strong continuity is a nontrivial
statement beyond the `L∞` contraction bound of Step H2. -/

/-- The heat symbol is continuous in `t`, at every fixed `x`. -/
theorem continuous_heatSymbol_apply (x : E) : Continuous (fun t : ℝ => heatSymbol E t x) := by
  unfold heatSymbol
  fun_prop

/-- **Core `L²` continuity step.** For a fixed `g ∈ L²`, the family `t ↦ heatSymbolL2 t • g`
(`t ≥ 0`, via `mulL2`) is continuous at every `t₀ ≥ 0`, in the `L²` norm. -/
theorem tendsto_mulL2_heatSymbolL2 {t₀ : ℝ} (ht₀ : 0 ≤ t₀) (g : Lp (α := E) F 2) :
    Filter.Tendsto (fun s : {t : ℝ // 0 ≤ t} => mulL2 F (heatSymbolL2 (E := E) s.2) g)
      (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t}))
      (𝓝 (mulL2 F (heatSymbolL2 (E := E) ht₀) g)) := by
  rw [tendsto_iff_norm_sub_tendsto_zero]
  have hgm : AEStronglyMeasurable (⇑g) (volume : Measure E) := Lp.aestronglyMeasurable g
  -- `L²`-finiteness of `‖g‖²`, used both for measurability and for the dominating bound.
  have hgm2 : AEMeasurable (fun x => ‖g x‖ₑ ^ (2 : ℝ)) (volume : Measure E) :=
    (ENNReal.continuous_rpow_const).measurable.comp_aemeasurable hgm.enorm
  have hgsq : (∫⁻ x, ‖g x‖ₑ ^ (2 : ℝ) ∂(volume : Measure E)) ≠ ∞ := by
    have hlt := (Lp.memLp g).2
    rw [eLpNorm_eq_lintegral_rpow_enorm_toReal (p := (2 : ℝ≥0∞)) (by norm_num) (by norm_num)]
      at hlt
    simp only [show ((2 : ℝ≥0∞).toReal) = (2 : ℝ) by norm_num] at hlt
    intro habs
    rw [habs, ENNReal.top_rpow_of_pos (by norm_num)] at hlt
    exact absurd hlt (lt_irrefl _)
  have hbound_fin :
      (∫⁻ x, (4 : ℝ≥0∞) * ‖g x‖ₑ ^ (2 : ℝ) ∂(volume : Measure E)) ≠ ∞ := by
    rw [lintegral_const_mul'' (4 : ℝ≥0∞) hgm2]
    exact ENNReal.mul_ne_top (by norm_num) hgsq
  -- the pointwise a.e. identification of the `L²` difference with the integrand below.
  have hcoe : ∀ s : {t : ℝ // 0 ≤ t},
      ⇑(mulL2 F (heatSymbolL2 (E := E) s.2) g - mulL2 F (heatSymbolL2 (E := E) ht₀) g)
        =ᵐ[(volume : Measure E)]
      fun x => heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x := by
    intro s
    rw [mulL2_apply, mulL2_apply]
    filter_upwards [Lp.coeFn_sub (heatSymbolL2 (E := E) s.2 • g) (heatSymbolL2 (E := E) ht₀ • g),
      Lp.coeFn_lpSMul (r := (2 : ℝ≥0∞)) (heatSymbolL2 (E := E) s.2) g,
      Lp.coeFn_lpSMul (r := (2 : ℝ≥0∞)) (heatSymbolL2 (E := E) ht₀) g,
      coeFn_heatSymbolL2 (E := E) s.2, coeFn_heatSymbolL2 (E := E) ht₀]
      with x hsub h1 h2 hs1 hs2
    rw [hsub]
    simp only [Pi.sub_apply]
    rw [h1, h2]
    simp only [Pi.smul_apply']
    rw [hs1, hs2]
  have hnormEq : ∀ s : {t : ℝ // 0 ≤ t},
      ‖mulL2 F (heatSymbolL2 (E := E) s.2) g - mulL2 F (heatSymbolL2 (E := E) ht₀) g‖
        = ((∫⁻ x, ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖ₑ ^ (2 : ℝ)
            ∂(volume : Measure E)) ^ (1 / (2 : ℝ))).toReal := by
    intro s
    rw [Lp.norm_def, eLpNorm_congr_ae (hcoe s),
      eLpNorm_eq_lintegral_rpow_enorm_toReal (p := (2 : ℝ≥0∞)) (by norm_num) (by norm_num)]
    norm_num
  simp_rw [hnormEq]
  have hlin : Filter.Tendsto
      (fun s : {t : ℝ // 0 ≤ t} =>
        ∫⁻ x, ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖ₑ ^ (2 : ℝ)
          ∂(volume : Measure E))
      (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t})) (𝓝 0) := by
    have hz : (0 : ℝ≥0∞) = ∫⁻ _ : E, (0 : ℝ≥0∞) ∂(volume : Measure E) := by simp
    rw [hz]
    apply tendsto_lintegral_filter_of_dominated_convergence'
      (bound := fun x => (4 : ℝ≥0∞) * ‖g x‖ₑ ^ (2 : ℝ))
    · filter_upwards with s
      have hsub : AEStronglyMeasurable
          (fun x => heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x)
          (volume : Measure E) :=
        ((measurable_heatSymbol s.1).aestronglyMeasurable.smul hgm).sub
          ((measurable_heatSymbol t₀).aestronglyMeasurable.smul hgm)
      exact (ENNReal.continuous_rpow_const).measurable.comp_aemeasurable hsub.enorm
    · filter_upwards with s
      filter_upwards with x
      have h1 : ‖heatSymbol E s.1 x‖ ≤ 1 := norm_heatSymbol_le_one s.2 x
      have h2 : ‖heatSymbol E t₀ x‖ ≤ 1 := norm_heatSymbol_le_one ht₀ x
      have hxle : ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖ ≤ 2 * ‖g x‖ := by
        calc ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖
            ≤ ‖heatSymbol E s.1 x • g x‖ + ‖heatSymbol E t₀ x • g x‖ := norm_sub_le _ _
          _ = ‖heatSymbol E s.1 x‖ * ‖g x‖ + ‖heatSymbol E t₀ x‖ * ‖g x‖ := by
                rw [norm_smul, norm_smul]
          _ ≤ 1 * ‖g x‖ + 1 * ‖g x‖ := by gcongr
          _ = 2 * ‖g x‖ := by ring
      have hxle' : ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖ₑ ≤ 2 * ‖g x‖ₑ := by
        simp only [← ofReal_norm]
        calc ENNReal.ofReal ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖
            ≤ ENNReal.ofReal (2 * ‖g x‖) := ENNReal.ofReal_le_ofReal hxle
          _ = 2 * ENNReal.ofReal ‖g x‖ := by
                rw [ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 2)]; norm_num
      calc ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖ₑ ^ (2 : ℝ)
          ≤ (2 * ‖g x‖ₑ) ^ (2 : ℝ) := ENNReal.rpow_le_rpow hxle' (by norm_num)
        _ = (4 : ℝ≥0∞) * ‖g x‖ₑ ^ (2 : ℝ) := by
              rw [ENNReal.mul_rpow_of_nonneg _ _ (by norm_num : (0 : ℝ) ≤ 2)]
              norm_num
    · exact hbound_fin
    · filter_upwards with x
      have hs1 : Filter.Tendsto (fun s : {t : ℝ // 0 ≤ t} => s.1)
          (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t})) (𝓝 t₀) :=
        continuous_subtype_val.tendsto ⟨t₀, ht₀⟩
      have hs2 : Filter.Tendsto (fun s : {t : ℝ // 0 ≤ t} => heatSymbol E s.1 x • g x)
          (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t})) (𝓝 (heatSymbol E t₀ x • g x)) :=
        ((continuous_heatSymbol_apply x).tendsto t₀).comp hs1 |>.smul tendsto_const_nhds
      have hs3 : Filter.Tendsto
          (fun s : {t : ℝ // 0 ≤ t} => heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x)
          (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t})) (𝓝 (0 : F)) := by
        have := hs2.sub (tendsto_const_nhds (x := heatSymbol E t₀ x • g x))
        simpa using this
      have hs4 := ((ENNReal.continuous_rpow_const (y := (2 : ℝ))).comp
        continuous_enorm).tendsto (0 : F) |>.comp hs3
      simpa only [Function.comp_def, enorm_zero,
        ENNReal.zero_rpow_of_pos (show (0 : ℝ) < 2 by norm_num)] using hs4
  have hrpow : Filter.Tendsto
      (fun s : {t : ℝ // 0 ≤ t} =>
        (∫⁻ x, ‖heatSymbol E s.1 x • g x - heatSymbol E t₀ x • g x‖ₑ ^ (2 : ℝ)
          ∂(volume : Measure E)) ^ (1 / (2 : ℝ)))
      (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t})) (𝓝 ((0 : ℝ≥0∞) ^ (1 / (2 : ℝ)))) :=
    ((ENNReal.continuous_rpow_const (y := 1 / (2 : ℝ))).tendsto 0).comp hlin
  rw [ENNReal.zero_rpow_of_pos (by norm_num)] at hrpow
  have hreal := (ENNReal.tendsto_toReal (a := (0 : ℝ≥0∞)) (by simp)).comp hrpow
  simpa only [Function.comp_def, ENNReal.toReal_zero] using hreal

/-- **Package theorem** (Step H6): the heat semigroup is strongly continuous at every `t₀ ≥ 0`,
for a fixed `f ∈ L²`, on the subtype of nonnegative reals. Closes the second half of
`HEAT-GAP-001`. -/
theorem heatOpL2_continuousAt {t₀ : ℝ} (ht₀ : 0 ≤ t₀) (f : Lp (α := E) F 2) :
    Filter.Tendsto (fun s : {t : ℝ // 0 ≤ t} => heatOpL2 F s.2 f)
      (𝓝 (⟨t₀, ht₀⟩ : {t : ℝ // 0 ≤ t})) (𝓝 (heatOpL2 F ht₀ f)) := by
  simp_rw [heatOpL2_apply]
  exact ((fourierInvCLM ℂ (Lp (α := E) F 2)).continuous.tendsto
      (mulL2 F (heatSymbolL2 (E := E) ht₀) (𝓕 f))).comp
      (tendsto_mulL2_heatSymbolL2 F ht₀ (𝓕 f))

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
que existe uma formalização de solução branda / fórmula de Duhamel
que Navier-Stokes ficou alcançável, ou que NS-GAP-001/004 tem caminho de prova
```

`HEAT-GAP-001` -- lei de semigrupo (`heatOpL2_add`/`heatOpL2_add'`) E continuidade forte
(`heatOpL2_continuousAt`) -- está FECHADO por este arquivo, ambas as metades. -/

end TamesisLab.Foundations.HeatSemigroup

#print axioms TamesisLab.Foundations.HeatSemigroup.norm_heatSymbol_le_one
#print axioms TamesisLab.Foundations.HeatSemigroup.measurable_heatSymbol
#print axioms TamesisLab.Foundations.HeatSemigroup.conj_heatSymbolL2
#print axioms TamesisLab.Foundations.HeatSemigroup.norm_heatOpL2_le
#print axioms TamesisLab.Foundations.HeatSemigroup.inner_heatOpL2_symm
#print axioms TamesisLab.Foundations.HeatSemigroup.heatOpL2_package
#print axioms TamesisLab.Foundations.HeatSemigroup.heatSymbol_add
#print axioms TamesisLab.Foundations.HeatSemigroup.mulL2_heatSymbolL2_heatSymbolL2
#print axioms TamesisLab.Foundations.HeatSemigroup.heatOpL2_add
#print axioms TamesisLab.Foundations.HeatSemigroup.heatOpL2_add'
#print axioms TamesisLab.Foundations.HeatSemigroup.continuous_heatSymbol_apply
#print axioms TamesisLab.Foundations.HeatSemigroup.tendsto_mulL2_heatSymbolL2
#print axioms TamesisLab.Foundations.HeatSemigroup.heatOpL2_continuousAt
#print axioms TamesisLab.Foundations.HeatSemigroup.stokesOpL2
#print axioms TamesisLab.Foundations.HeatSemigroup.norm_stokesOpL2_le
#print axioms TamesisLab.Foundations.HeatSemigroup.norm_stokesOpL2_le'
#print axioms TamesisLab.Foundations.HeatSemigroup.concrete_stokesOpL2_R3
