/-
Probe DUH : the abstract Duhamel-formula / mild-solution scaffolding for the heat semigroup
`heatOpL2`, with a COMPLETELY ABSTRACT forcing term `B : L² → L²` -- only `Continuous B` is
assumed, nothing else (no Lipschitz/bilinear estimate, no fixed point).

Builds on `TamesisLab.Foundations.HeatSemigroup` (`heatOpL2`, its contraction bound
`norm_heatOpL2_apply_le`, and its strong continuity `heatOpL2_continuousAt` on the subtype
`{t : ℝ // 0 ≤ t}`).

`FOUND-DUHAMEL-SKELETON-001` in `RESEARCH_QUEUE.yaml`. Scope: define the Duhamel integrand
`s ↦ S(t-s)(B(u(s)))` and the Duhamel term `u(t) = S(t)u₀ + ∫₀ᵗ S(t-s)(B(u(s))) ds`, and prove
the defining Bochner integral is well-posed (`IntervalIntegrable`) given `u` continuous on
`[0,t]` and `B` continuous -- nothing more. NOT an existence/uniqueness/fixed-point argument,
NOT an estimate on `B` (that is `NS-GAP-001`/`004`, explicitly out of scope here).
-/
import TamesisLab.Foundations.HeatSemigroup
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

open MeasureTheory Filter
open scoped Topology

set_option maxHeartbeats 2000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.DuhamelSkeleton

open TamesisLab.Foundations.HeatSemigroup

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable (F : Type*) [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-! ## Step D0 : the heat semigroup, jointly continuous in `(t, f)`.

`heatOpL2_continuousAt` (in `HeatSemigroup.lean`) only gives continuity in `t` for a FIXED
`f`. To feed a *moving* argument `B (u s)` into `heatOpL2 F (t - s)` we need joint continuity
in both the time index and the `L²` argument. This follows from combining the pointwise
strong continuity in `t` (`heatOpL2_continuousAt`) with the UNIFORM (in `t`) contraction bound
`norm_heatOpL2_apply_le`, via the standard triangle-inequality splitting
`S(t)f - S(t₀)f₀ = S(t)(f - f₀) + (S(t)f₀ - S(t₀)f₀)`. -/

/-- **The heat semigroup as a single function of the pair `(t, f)`,** `t` ranging over the
subtype of nonnegative reals. -/
def heatOpJoint (p : {t : ℝ // 0 ≤ t} × Lp (α := E) F 2) : Lp (α := E) F 2 :=
  heatOpL2 F p.1.2 p.2

theorem heatOpJoint_continuousAt (p₀ : {t : ℝ // 0 ≤ t} × Lp (α := E) F 2) :
    ContinuousAt (heatOpJoint F) p₀ := by
  rw [ContinuousAt, tendsto_iff_norm_sub_tendsto_zero]
  -- The "frozen argument" half: `t ↦ S(t) f₀`, tending to `S(t₀) f₀` by strong continuity.
  have h1 : Filter.Tendsto (fun p => heatOpL2 F p.1.2 p₀.2) (𝓝 p₀) (𝓝 (heatOpL2 F p₀.1.2 p₀.2)) :=
    (heatOpL2_continuousAt F p₀.1.2 p₀.2).comp (continuous_fst.tendsto p₀)
  have h1' : Filter.Tendsto (fun p => ‖heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2‖)
      (𝓝 p₀) (𝓝 0) :=
    tendsto_iff_norm_sub_tendsto_zero.mp h1
  -- The "frozen time" half: `f ↦ ‖f - f₀‖`, tending to `0` by continuity of `Prod.snd`.
  have h2 : Filter.Tendsto (fun p => ‖p.2 - p₀.2‖) (𝓝 p₀) (𝓝 0) :=
    tendsto_iff_norm_sub_tendsto_zero.mp (continuous_snd.tendsto p₀)
  have hsum : Filter.Tendsto
      (fun p => ‖p.2 - p₀.2‖ + ‖heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2‖)
      (𝓝 p₀) (𝓝 0) := by
    simpa using h2.add h1'
  -- The triangle-inequality squeeze.
  have hle : ∀ p, ‖heatOpJoint F p - heatOpJoint F p₀‖
        ≤ ‖p.2 - p₀.2‖ + ‖heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2‖ := by
    intro p
    have heq : heatOpJoint F p - heatOpJoint F p₀
        = heatOpL2 F p.1.2 (p.2 - p₀.2) + (heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2) := by
      unfold heatOpJoint
      rw [map_sub]
      abel
    rw [heq]
    calc ‖heatOpL2 F p.1.2 (p.2 - p₀.2) + (heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2)‖
        ≤ ‖heatOpL2 F p.1.2 (p.2 - p₀.2)‖
            + ‖heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2‖ := norm_add_le _ _
      _ ≤ ‖p.2 - p₀.2‖ + ‖heatOpL2 F p.1.2 p₀.2 - heatOpL2 F p₀.1.2 p₀.2‖ := by
            gcongr
            exact norm_heatOpL2_apply_le F p.1.2 (p.2 - p₀.2)
  exact squeeze_zero (fun p => norm_nonneg _) hle hsum

/-- **The heat semigroup, jointly continuous** in `(t, f) : {t : ℝ // 0 ≤ t} × L²`. -/
theorem heatOpJoint_continuous : Continuous (heatOpJoint (E := E) F) :=
  continuous_iff_continuousAt.mpr (heatOpJoint_continuousAt F)

/-! ## Step D1 : the Duhamel integrand `s ↦ S(t-s)(B(u(s)))`.

Made TOTAL (no junk-avoidance subtype restriction needed) by feeding `heatOpL2` the
nonnegativity proof of `max (t - s) 0` rather than of `t - s` itself: for `s ≤ t` this agrees
with the genuine `t - s`, and for `s > t` it silently evaluates the semigroup at `0` instead
(irrelevant junk, since the integral below is only ever taken over `s ∈ [0, t]`). -/

variable (B : Lp (α := E) F 2 → Lp (α := E) F 2)

/-- The time-reversal map `s ↦ ⟨max (t - s) 0, _⟩` into `{t : ℝ // 0 ≤ t}`, continuous on all
of `ℝ`. -/
def revTime (t : ℝ) (s : ℝ) : {t : ℝ // 0 ≤ t} :=
  ⟨max (t - s) 0, le_max_right _ _⟩

theorem continuous_revTime (t : ℝ) : Continuous (revTime t) :=
  Continuous.subtype_mk ((continuous_const.sub continuous_id).max continuous_const) _

theorem revTime_coe_of_le {t s : ℝ} (hs : s ≤ t) : (revTime t s : ℝ) = t - s := by
  simp [revTime, max_eq_left (sub_nonneg.mpr hs)]

/-- **The Duhamel integrand**: `s ↦ S(t-s)(B(u(s)))`, for a candidate curve `u : ℝ → L²` and a
fixed `t`. Total on all of `ℝ` (see `revTime`); the genuine Duhamel content is only its
restriction to `s ∈ [0, t]`. -/
def duhamelIntegrand (t : ℝ) (u : ℝ → Lp (α := E) F 2) (s : ℝ) : Lp (α := E) F 2 :=
  heatOpJoint F (revTime t s, B (u s))

/-! ## Step D2 : continuity of the integrand on `[0, t]`. -/

theorem continuousOn_duhamelIntegrand {t : ℝ} {u : ℝ → Lp (α := E) F 2}
    (hu : ContinuousOn u (Set.Icc 0 t)) (hB : Continuous B) :
    ContinuousOn (duhamelIntegrand F B t u) (Set.Icc 0 t) := by
  have hpair : ContinuousOn (fun (s : ℝ) => (revTime t s, B (u s))) (Set.Icc 0 t) :=
    (continuous_revTime t).continuousOn.prodMk (hB.comp_continuousOn hu)
  exact (heatOpJoint_continuous F).comp_continuousOn hpair

/-! ## Step D3 : the Duhamel integral is well-defined. -/

theorem intervalIntegrable_duhamelIntegrand {t : ℝ} (ht : 0 ≤ t) {u : ℝ → Lp (α := E) F 2}
    (hu : ContinuousOn u (Set.Icc 0 t)) (hB : Continuous B) :
    IntervalIntegrable (duhamelIntegrand F B t u) MeasureTheory.volume 0 t :=
  (continuousOn_duhamelIntegrand F B hu hB).intervalIntegrable_of_Icc ht

/-! ## Step D4 : the Duhamel term itself,
`u(t) = S(t) u₀ + ∫₀ᵗ S(t-s)(B(u(s))) ds`. -/

/-- **The Duhamel term.** -/
def duhamelTerm (t : ℝ) (u0 : Lp (α := E) F 2) (u : ℝ → Lp (α := E) F 2) (ht : 0 ≤ t) :
    Lp (α := E) F 2 :=
  heatOpL2 F ht u0 + ∫ s in (0:ℝ)..t, duhamelIntegrand F B t u s

/-! ## Step D5 : sanity check -- with no forcing (`B = 0`), Duhamel reduces to pure linear
evolution `u(t) = S(t) u₀`, for ANY candidate curve `u`. -/

theorem duhamelTerm_of_zero (t : ℝ) (u0 : Lp (α := E) F 2) (u : ℝ → Lp (α := E) F 2)
    (ht : 0 ≤ t) :
    duhamelTerm F (fun _ => 0) t u0 u ht = heatOpL2 F ht u0 := by
  unfold duhamelTerm
  have hzero : duhamelIntegrand F (fun _ => 0) t u = fun _ => (0 : Lp (α := E) F 2) := by
    funext s
    unfold duhamelIntegrand heatOpJoint
    exact map_zero _
  rw [hzero, intervalIntegral.integral_zero, add_zero]

end TamesisLab.Foundations.DuhamelSkeleton

#print axioms TamesisLab.Foundations.DuhamelSkeleton.heatOpJoint_continuousAt
#print axioms TamesisLab.Foundations.DuhamelSkeleton.heatOpJoint_continuous
#print axioms TamesisLab.Foundations.DuhamelSkeleton.continuous_revTime
#print axioms TamesisLab.Foundations.DuhamelSkeleton.revTime_coe_of_le
#print axioms TamesisLab.Foundations.DuhamelSkeleton.continuousOn_duhamelIntegrand
#print axioms TamesisLab.Foundations.DuhamelSkeleton.intervalIntegrable_duhamelIntegrand
#print axioms TamesisLab.Foundations.DuhamelSkeleton.duhamelTerm_of_zero
