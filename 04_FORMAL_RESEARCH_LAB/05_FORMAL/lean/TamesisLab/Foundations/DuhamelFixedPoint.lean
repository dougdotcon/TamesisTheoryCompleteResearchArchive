/-
Probe FP : the abstract local existence/uniqueness theorem for the Duhamel mild-solution map,
via Banach's fixed point theorem -- GIVEN, as an explicit HYPOTHESIS, that the forcing term
`B : L² → L²` is (globally) Lipschitz with constant `L`. NOT a claim that any concrete
Navier-Stokes-related `B` satisfies this hypothesis (that is `NS-GAP-001`/`004`, explicitly
out of scope here); NOT global existence (only local, on `[0,T]` for `T` small enough,
depending on `L`).

`FOUND-ABSTRACT-DUHAMEL-FIXEDPOINT-001` in `RESEARCH_QUEUE.yaml`, authorized by
`01_PORTFOLIO/PORTFOLIO_REVIEW_ABSTRACT_WELLPOSEDNESS_2026_08_09.md`.

Builds on `TamesisLab.Foundations.DuhamelSkeleton` (`duhamelTerm`, `duhamelIntegrand`,
`heatOpJoint`, `revTime`, and their well-posedness lemmas) and
`TamesisLab.Foundations.HeatSemigroup` (`heatOpL2`, its contraction bound
`norm_heatOpL2_apply_le`).

## Strategy

The space of candidate mild-solution curves on `[0,T]` is
`Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2` (Mathlib's `BoundedContinuousFunction`, notation `→ᵇ`) --
a complete metric space (`BoundedContinuousFunction.instCompleteSpace`) since the codomain
`Lp F 2` is complete and the domain is compact.

Rather than working with `duhamelTerm`'s dependently-typed `(ht : 0 ≤ t)` argument directly (an
awkward shape for the continuity arguments Mathlib's parametric-integral machinery expects), we
first build a TOTALIZED version `phiTotal : ℝ → Lp F 2`, defined and jointly continuous on ALL of
`ℝ` (reusing the same "totalize via `max _ 0`" trick `DuhamelSkeleton.revTime` already uses for
the integrand), and separately show it agrees with `duhamelTerm` wherever `t ≥ 0`
(`phiTotal_eq_duhamelTerm`). Candidate curves `u : Set.Icc 0 T →ᵇ Lp F 2` are extended to total
continuous functions `ℝ → Lp F 2` via `Set.IccExtend` (clamping outside `[0,T]`), which is the
standard Mathlib device for exactly this situation and keeps every intermediate function
GLOBALLY continuous (no case splits, no junk-value bookkeeping).

The Duhamel map `Φ` is then `u ↦ BoundedContinuousFunction.mkOfCompact ⟨fun t => phiTotal ... t.1,
_⟩`. The contraction estimate is a direct triangle-inequality/Lipschitz computation: the linear
heat term cancels exactly between `Φ u` and `Φ v` (it does not depend on `u`), and the forcing
term is bounded via `‖heatOpL2 · ‖ ≤ 1` (contraction) composed with the Lipschitz bound on `B`
and `‖extend u s - extend v s‖ ≤ dist u v` (Mathlib's `dist_coe_le_dist`, valid for every real
`s`, not just `s ∈ [0,T]`, because `Set.IccExtend` clamps both `u` and `v` to the SAME point of
`[0,T]`). Integrating over `s ∈ [0,t] ⊆ [0,T]` gives `dist (Φ u) (Φ v) ≤ (T * L) * dist u v`, so
for `T * L < 1`, `Φ` is `ContractingWith (T*L).toNNReal`, and Banach's fixed point theorem
(`ContractingWith.fixedPoint`) gives a UNIQUE fixed point -- a mild solution on `[0,T]`.
-/
import TamesisLab.Foundations.DuhamelSkeleton
import Mathlib.Topology.ContinuousMap.Bounded.Basic
import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Topology.Order.ProjIcc

open MeasureTheory Filter Set
open scoped Topology BoundedContinuousFunction NNReal

set_option maxHeartbeats 4000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.DuhamelFixedPoint

open TamesisLab.Foundations.HeatSemigroup
open TamesisLab.Foundations.DuhamelSkeleton

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable (F : Type*) [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-! ## Step FP0 : `revTime`, jointly continuous in `(t, s)`.

`DuhamelSkeleton.continuous_revTime` only gives continuity in `s` for a FIXED `t`. The
parametric-integral continuity lemma we use below (Step FP2) needs joint continuity in both
the upper limit `t` and the integration variable `s`. -/

theorem continuous_revTime2 : Continuous (fun p : ℝ × ℝ => revTime p.1 p.2) :=
  Continuous.subtype_mk ((continuous_fst.sub continuous_snd).max continuous_const) _

variable (B : Lp (α := E) F 2 → Lp (α := E) F 2)

/-! ## Step FP1 : the totalized Duhamel map `phiTotal : ℝ → Lp F 2`, defined and continuous on
ALL of `ℝ` for a fixed candidate curve `u`, and agreeing with `duhamelTerm` on `t ≥ 0`. -/

/-- **The totalized Duhamel map.** Candidate curves `u : Set.Icc 0 T →ᵇ Lp F 2` are extended to
`ℝ → Lp F 2` via `Set.IccExtend` (continuous clamping), and the linear heat term is totalized via
`revTime t 0` exactly as `DuhamelSkeleton.duhamelIntegrand` totalizes `S(t - s)`. -/
def phiTotal {T : ℝ} (hT : (0:ℝ) ≤ T) (u0 : Lp (α := E) F 2)
    (u : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) (t : ℝ) : Lp (α := E) F 2 :=
  heatOpJoint F (revTime t 0, u0) +
    ∫ s in (0:ℝ)..t, duhamelIntegrand F B t (Set.IccExtend hT (⇑u)) s

/-- **`phiTotal` agrees with `duhamelTerm`** whenever `t ≥ 0` (the only case `duhamelTerm` is
meaningful for). -/
theorem phiTotal_eq_duhamelTerm {T : ℝ} (hT : (0:ℝ) ≤ T) (u0 : Lp (α := E) F 2)
    (u : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) {t : ℝ} (ht : 0 ≤ t) :
    phiTotal F B hT u0 u t = duhamelTerm F B t u0 (Set.IccExtend hT (⇑u)) ht := by
  have hrt : revTime t 0 = (⟨t, ht⟩ : {r : ℝ // 0 ≤ r}) :=
    Subtype.ext (by rw [revTime_coe_of_le ht, sub_zero])
  unfold phiTotal duhamelTerm
  rw [hrt]
  rfl

/-- **`phiTotal` is continuous in `t`** (for a fixed candidate curve `u`), given `B` continuous.
Uses `intervalIntegral.continuous_parametric_intervalIntegral_of_continuous` for the integral
term (joint continuity of the integrand in `(t, s)`) and `heatOpJoint_continuous` for the linear
term. -/
theorem phiTotal_continuous {T : ℝ} (hT : (0:ℝ) ≤ T) (hBc : Continuous B)
    (u0 : Lp (α := E) F 2) (u : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) :
    Continuous (phiTotal F B hT u0 u) := by
  have hterm1 : Continuous (fun t : ℝ => heatOpJoint F (revTime t 0, u0)) :=
    (heatOpJoint_continuous F).comp
      ((continuous_revTime2.comp (continuous_id.prodMk continuous_const)).prodMk continuous_const)
  have hf : Continuous
      (Function.uncurry fun (t s : ℝ) => duhamelIntegrand F B t (Set.IccExtend hT (⇑u)) s) := by
    show Continuous
      (fun p : ℝ × ℝ => heatOpJoint F (revTime p.1 p.2, B (Set.IccExtend hT (⇑u) p.2)))
    exact (heatOpJoint_continuous F).comp
      (continuous_revTime2.prodMk
        (hBc.comp ((u.continuous.Icc_extend' (h := hT)).comp continuous_snd)))
  have hterm2 : Continuous
      (fun t : ℝ => ∫ s in (0:ℝ)..t, duhamelIntegrand F B t (Set.IccExtend hT (⇑u)) s) :=
    intervalIntegral.continuous_parametric_intervalIntegral_of_continuous hf continuous_id
  exact hterm1.add hterm2

/-! ## Step FP2 : the (totalized) Duhamel self-map on candidate curves, and its contraction
estimate under the Lipschitz hypothesis on `B`. -/

/-- **The Duhamel map** `Φ : (Set.Icc 0 T →ᵇ Lp F 2) → (Set.Icc 0 T →ᵇ Lp F 2)`. -/
def PhiMap {T : ℝ} (hT : (0:ℝ) ≤ T) (hBc : Continuous B) (u0 : Lp (α := E) F 2)
    (u : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2 :=
  BoundedContinuousFunction.mkOfCompact
    (ContinuousMap.mk (fun t : Set.Icc (0:ℝ) T => phiTotal F B hT u0 u t.1)
      ((phiTotal_continuous F B hT hBc u0 u).comp continuous_subtype_val))

theorem PhiMap_apply {T : ℝ} (hT : (0:ℝ) ≤ T) (hBc : Continuous B) (u0 : Lp (α := E) F 2)
    (u : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) (t : Set.Icc (0:ℝ) T) :
    PhiMap F B hT hBc u0 u t = phiTotal F B hT u0 u t.1 :=
  rfl

/-- **Pointwise contraction estimate** for `phiTotal`, under the global Lipschitz hypothesis on
`B`. The linear heat term cancels exactly (it does not depend on `u`, `v`); the forcing term is
bounded using the heat semigroup's contraction property `‖heatOpL2 · ‖ ≤ 1`
(`norm_heatOpL2_apply_le`), the Lipschitz bound on `B`, and the fact that `Set.IccExtend` clamps
`u` and `v` to the SAME point of `[0,T]` for every `s : ℝ` (`dist_coe_le_dist`). -/
theorem norm_phiTotal_sub_le {T : ℝ} (hT : (0:ℝ) ≤ T) {L : ℝ≥0} (hB : LipschitzWith L B)
    (u0 : Lp (α := E) F 2) (u v : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) {t : ℝ} (ht0 : 0 ≤ t)
    (htT : t ≤ T) :
    ‖phiTotal F B hT u0 u t - phiTotal F B hT u0 v t‖ ≤ T * (L : ℝ) * dist u v := by
  have hu_cont : Continuous (Set.IccExtend hT (⇑u)) := u.continuous.Icc_extend' (h := hT)
  have hv_cont : Continuous (Set.IccExtend hT (⇑v)) := v.continuous.Icc_extend' (h := hT)
  have hu_int : IntervalIntegrable
      (duhamelIntegrand F B t (Set.IccExtend hT (⇑u))) MeasureTheory.volume 0 t :=
    intervalIntegrable_duhamelIntegrand F B ht0 hu_cont.continuousOn hB.continuous
  have hv_int : IntervalIntegrable
      (duhamelIntegrand F B t (Set.IccExtend hT (⇑v))) MeasureTheory.volume 0 t :=
    intervalIntegrable_duhamelIntegrand F B ht0 hv_cont.continuousOn hB.continuous
  have hsub : phiTotal F B hT u0 u t - phiTotal F B hT u0 v t
      = ∫ s in (0:ℝ)..t, (duhamelIntegrand F B t (Set.IccExtend hT (⇑u)) s
          - duhamelIntegrand F B t (Set.IccExtend hT (⇑v)) s) := by
    unfold phiTotal
    rw [add_sub_add_comm, sub_self, zero_add]
    exact (intervalIntegral.integral_sub hu_int hv_int).symm
  have hbound : ∀ s : ℝ, ‖duhamelIntegrand F B t (Set.IccExtend hT (⇑u)) s
      - duhamelIntegrand F B t (Set.IccExtend hT (⇑v)) s‖ ≤ (L : ℝ) * dist u v := by
    intro s
    have hpt : dist (Set.IccExtend hT (⇑u) s) (Set.IccExtend hT (⇑v) s) ≤ dist u v := by
      rw [Set.IccExtend_apply, Set.IccExtend_apply]
      exact u.dist_coe_le_dist _
    unfold duhamelIntegrand heatOpJoint
    rw [← map_sub]
    calc ‖heatOpL2 F (revTime t s).2
          (B (Set.IccExtend hT (⇑u) s) - B (Set.IccExtend hT (⇑v) s))‖
        ≤ ‖B (Set.IccExtend hT (⇑u) s) - B (Set.IccExtend hT (⇑v) s)‖ :=
          norm_heatOpL2_apply_le F (revTime t s).2 _
      _ = dist (B (Set.IccExtend hT (⇑u) s)) (B (Set.IccExtend hT (⇑v) s)) :=
          (dist_eq_norm _ _).symm
      _ ≤ (L : ℝ) * dist (Set.IccExtend hT (⇑u) s) (Set.IccExtend hT (⇑v) s) :=
          hB.dist_le_mul _ _
      _ ≤ (L : ℝ) * dist u v := by gcongr
  rw [hsub]
  calc ‖∫ s in (0:ℝ)..t, (duhamelIntegrand F B t (Set.IccExtend hT (⇑u)) s
        - duhamelIntegrand F B t (Set.IccExtend hT (⇑v)) s)‖
      ≤ (L : ℝ) * dist u v * |t - 0| :=
        intervalIntegral.norm_integral_le_of_norm_le_const (fun s _ => hbound s)
    _ = (L : ℝ) * dist u v * t := by rw [sub_zero, abs_of_nonneg ht0]
    _ ≤ (L : ℝ) * dist u v * T := by gcongr
    _ = T * (L : ℝ) * dist u v := by ring

/-- **`PhiMap` is Lipschitz-close in the sup metric**: `dist (Φ u) (Φ v) ≤ (T * L) * dist u v`.
-/
theorem dist_PhiMap_le {T : ℝ} (hT : (0:ℝ) ≤ T) (hBc : Continuous B) {L : ℝ≥0}
    (hB : LipschitzWith L B) (u0 : Lp (α := E) F 2)
    (u v : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) :
    dist (PhiMap F B hT hBc u0 u) (PhiMap F B hT hBc u0 v) ≤ T * (L : ℝ) * dist u v := by
  apply (BoundedContinuousFunction.dist_le
    (mul_nonneg (mul_nonneg hT L.coe_nonneg) dist_nonneg)).2
  intro t
  rw [PhiMap_apply, PhiMap_apply, dist_eq_norm]
  exact norm_phiTotal_sub_le F B hT hB u0 u v t.2.1 t.2.2

/-! ## Step FP3 : `PhiMap` is a contraction for `T * L < 1`, and therefore has a UNIQUE fixed
point (Banach's fixed point theorem, `ContractingWith.fixedPoint`) -- a mild solution of
Duhamel's formula, LOCAL on `[0,T]`, under the explicit Lipschitz hypothesis on `B`. -/

/-- **`PhiMap` is a contraction** with constant `(T * L).toNNReal < 1`, given `T * L < 1`. -/
theorem contractingWith_PhiMap {T : ℝ} (hT0 : 0 < T) {L : ℝ≥0} (hB : LipschitzWith L B)
    (u0 : Lp (α := E) F 2) (hTL : T * (L : ℝ) < 1) :
    ContractingWith (Real.toNNReal (T * (L : ℝ))) (PhiMap F B hT0.le hB.continuous u0) :=
  ⟨Real.toNNReal_lt_one.mpr hTL,
    LipschitzWith.of_dist_le' (dist_PhiMap_le F B hT0.le hB.continuous hB u0)⟩

/-- **Main theorem (`FOUND-ABSTRACT-DUHAMEL-FIXEDPOINT-001`): abstract local existence and
uniqueness of a mild solution to Duhamel's formula.**

GIVEN, as an explicit HYPOTHESIS, that `B : L²(E,F) → L²(E,F)` is Lipschitz with constant `L`
(`hB : LipschitzWith L B` -- NEVER derived here, NEVER claimed for any concrete Navier-Stokes
`B`), and `T > 0` small enough that `T * L < 1`: there is a UNIQUE bounded continuous curve
`u : [0,T] → L²(E,F)` satisfying the mild-solution (Duhamel) equation
`u(t) = S(t) u₀ + ∫₀ᵗ S(t-s)(B(u(s))) ds` for every `t ∈ [0,T]`.

This is ONLY a local (on `[0,T]`) existence/uniqueness statement, under an assumed abstract
Lipschitz hypothesis on `B` -- it says nothing about whether the real Navier-Stokes forcing term
satisfies this hypothesis (`NS-GAP-001`/`004`, out of scope), and nothing about global
existence. -/
theorem exists_unique_mild_solution {L : ℝ≥0} (hB : LipschitzWith L B)
    (u0 : Lp (α := E) F 2) {T : ℝ} (hT0 : 0 < T) (hTL : T * (L : ℝ) < 1) :
    ∃! u : Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2,
      ∀ t : Set.Icc (0:ℝ) T,
        u t = duhamelTerm F B t.1 u0 (Set.IccExtend hT0.le (⇑u)) t.2.1 := by
  haveI : Nonempty (Set.Icc (0:ℝ) T →ᵇ Lp (α := E) F 2) :=
    ⟨BoundedContinuousFunction.const _ u0⟩
  set K : ContractingWith (Real.toNNReal (T * (L : ℝ))) (PhiMap F B hT0.le hB.continuous u0) :=
    contractingWith_PhiMap F B hT0 hB u0 hTL with hKdef
  refine ⟨ContractingWith.fixedPoint (PhiMap F B hT0.le hB.continuous u0) K, fun t => ?_, ?_⟩
  · have hfix : PhiMap F B hT0.le hB.continuous u0
        (ContractingWith.fixedPoint (PhiMap F B hT0.le hB.continuous u0) K)
        = ContractingWith.fixedPoint (PhiMap F B hT0.le hB.continuous u0) K :=
      K.fixedPoint_isFixedPt
    have hpt := congrFun (congrArg (⇑) hfix) t
    rw [PhiMap_apply, phiTotal_eq_duhamelTerm F B hT0.le u0 _ t.2.1] at hpt
    exact hpt.symm
  · intro w hw
    apply K.fixedPoint_unique
    show PhiMap F B hT0.le hB.continuous u0 w = w
    refine BoundedContinuousFunction.ext fun t => ?_
    rw [PhiMap_apply, phiTotal_eq_duhamelTerm F B hT0.le u0 w t.2.1]
    exact (hw t).symm

end TamesisLab.Foundations.DuhamelFixedPoint

#print axioms TamesisLab.Foundations.DuhamelFixedPoint.continuous_revTime2
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.phiTotal_eq_duhamelTerm
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.phiTotal_continuous
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.PhiMap_apply
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.norm_phiTotal_sub_le
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.dist_PhiMap_le
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.contractingWith_PhiMap
#print axioms TamesisLab.Foundations.DuhamelFixedPoint.exists_unique_mild_solution
