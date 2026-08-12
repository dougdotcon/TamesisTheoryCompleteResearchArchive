/-
HG-4h -- Classe de `expConjUnit` no quociente `(ℂ → ℂ)ˣ ⧸
HolomorphicTransitionSubgroup` != identidade (Wave-7 item WAVE7-HG-4H,
Hodge line / 03_MILLENNIUM/05_HODGE).

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (the exact residual gap this item closes):
Wave-6's `HG4GHolomorphicTransitionQuotientNontrivialProbe.lean` (HG-4g,
this directory) showed the coset space `(ℂ → ℂ)ˣ ⧸
HolomorphicTransitionSubgroup` is `Nontrivial` (has at least two
distinct cosets), via `QuotientGroup.nontrivial_iff.mpr` fed Wave-5's
`holomorphicTransitionSubgroup_ne_top`. That `Nontrivial` instance is a
bare existence claim (SOME two cosets differ) and does not exhibit an
actual representative that differs from the identity coset. This
Wave-7 item (HG-4h) closes exactly that gap: it names the concrete
witness, `expConjUnit` (Wave-5's `HG4FExpConjNotHolomorphicSubgroupProbe
.lean`), and shows directly that its own coset `(expConjUnit : (ℂ → ℂ)ˣ
⧸ HolomorphicTransitionSubgroup)` is NOT the identity coset `1`. Nothing
broader.

THE TEST, AND THE RESULT: CLOSED, exactly as narrowed by the Onda 7
plan (single line, as specified):
  `theorem expConjUnit_coset_ne_one :
      (expConjUnit : (ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup) ≠ 1 :=
    fun h => expConjUnit_not_mem ((QuotientGroup.eq_one_iff _).mp h)`
This type-checks and proves as written, with no modification needed:
`QuotientGroup.eq_one_iff {N : Subgroup G} [N.Normal] (x : G) :
(x : G ⧸ N) = 1 ↔ x ∈ N` (Mathlib/GroupTheory/QuotientGroup/Defs.lean)
applies to `G := (ℂ → ℂ)ˣ`, `N := HolomorphicTransitionSubgroup`,
`x := (expConjUnit : (ℂ → ℂ)ˣ)`. The required `[N.Normal]` instance is
found by typeclass inference with ZERO new code: `(ℂ → ℂ)ˣ` is a
`CommGroup` (`instCommGroupUnits`, already cited by HG-4g), hence
`IsMulCommutative (ℂ → ℂ)ˣ` (via the `CommMagma.to_isCommutative` chain
built into `CommGroup`'s hierarchy), hence, by
`Subgroup.normal_of_isMulCommutative` (a `(priority := 100)` instance:
"every subgroup of a group with `IsMulCommutative` is `Normal`"),
`HolomorphicTransitionSubgroup.Normal` -- fully automatic. `.mp` of
`eq_one_iff` turns the hypothetical coset equality `h` into membership
`expConjUnit ∈ HolomorphicTransitionSubgroup`, refuted directly by
HG-4f's already-closed `expConjUnit_not_mem` (inlined below, verbatim,
together with its full HG-4/HG-4d/HG-4e/HG-4f dependency chain, in the
same "inline the short relevant pieces" pattern HG-4e/HG-4f/HG-4g
already used for their own dependencies).

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT modify `HolomorphicTransitionProbe.lean`,
  `HolomorphicTransitionMulInvClosureProbe.lean`,
  `HolomorphicTransitionSubgroupProbe.lean`,
  `HG4FExpConjNotHolomorphicSubgroupProbe.lean`, or
  `HG4GHolomorphicTransitionQuotientNontrivialProbe.lean`; it inlines
  copies of the short relevant pieces from the first four into this new
  file, exactly as HG-4e/HG-4f/HG-4g inlined their own dependencies.
- Does NOT compute or characterize the quotient group
  `(ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup` any further beyond this one
  witness's coset (no cardinality, no full set of coset representatives,
  no group-structure claims beyond the bare `≠ 1` fact for this one
  element) -- only the exact one-line test named by the Onda 7 plan is
  attempted.
- Does NOT define or touch any `VectorBundle`/`Bundle`/
  `HolomorphicLineBundle`/`PicardGroup` API, and does NOT attempt any
  cocycle-condition bookkeeping for an actual line bundle.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: every lemma used
  (`QuotientGroup.eq_one_iff`, `Subgroup.normal_of_isMulCommutative`,
  plus everything HG-4/HG-4d/HG-4e/HG-4f already used) is pre-existing,
  proved Mathlib content or a verbatim inline of an already-closed
  prior-wave result; the only new step here is the single one-line proof
  named by the plan.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by
this file's own successful compilation):
  - `QuotientGroup.eq_one_iff {N : Subgroup G} [N.Normal] (x : G) :
    (x : G ⧸ N) = 1 ↔ x ∈ N`
                             GroupTheory/QuotientGroup/Defs.lean:120
  - `Subgroup.normal_of_isMulCommutative (priority := 100)
    [IsMulCommutative G] (H : Subgroup G) : H.Normal`
                             Algebra/Group/Subgroup/Defs.lean:631
  - `CommMagma.to_isCommutative : IsMulCommutative G`
                             Algebra/Group/Defs.lean:263
  - `instCommGroupUnits {α} [CommMonoid α] : CommGroup αˣ`
                             Algebra/Group/Units/Defs.lean:265-267
  - HG-4/HG-4d/HG-4e/HG-4f dependencies, inlined verbatim below:
    `IsHolomorphicTransition`, `isHolomorphicTransition_iff_differentiable`
    (HG-4/Wave-1), `isHolomorphicTransition_mul`/`_inv` (HG-4d/Wave-4),
    `HolomorphicTransitionSubgroup` (HG-4e/Wave-5),
    `not_differentiable_exp_comp_conj`, `expConjUnit`,
    `expConjUnit_not_mem` (HG-4f/Wave-5) --
    `HG4FExpConjNotHolomorphicSubgroupProbe.lean`, this directory,
    independently recompiled by this file's author with `lake env lean`
    (exit 0, clean `#print axioms` on all of its declarations) before
    this item was attempted.
-/

import Mathlib

open ComplexConjugate

/- ============================================================
   PART 1 -- inlined verbatim from `HolomorphicTransitionProbe.lean`
   (HG-4, Wave-1), exactly as HG-4g inlined it.
   ============================================================ -/

namespace HG4HolomorphicTransitionProbe

open scoped Manifold

/-- The candidate predicate: "the transition function `g` of a rank-1
trivial bundle over `M := ℂ` (single-chart model `𝓘(ℂ, ℂ)`) is
holomorphic," stated purely in terms of Mathlib's pre-existing manifold
complex-differentiability machinery. -/
def IsHolomorphicTransition (g : ℂ → ℂ) : Prop :=
  MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g

/-- The predicate unfolds, with zero extra infrastructure, to Mathlib's
standard complex-differentiability. -/
theorem isHolomorphicTransition_iff_differentiable {g : ℂ → ℂ} :
    IsHolomorphicTransition g ↔ Differentiable ℂ g := by
  unfold IsHolomorphicTransition
  exact mdifferentiable_iff_differentiable

end HG4HolomorphicTransitionProbe

/- ============================================================
   PART 2 -- inlined verbatim from
   `HolomorphicTransitionMulInvClosureProbe.lean` (HG-4d, Wave-4).
   ============================================================ -/

namespace HG4dHolomorphicTransitionMulInvClosureProbe

open HG4HolomorphicTransitionProbe

theorem isHolomorphicTransition_mul {g h : ℂ → ℂ}
    (hg : IsHolomorphicTransition g) (hh : IsHolomorphicTransition h) :
    IsHolomorphicTransition (g * h) :=
  isHolomorphicTransition_iff_differentiable.mpr
    ((isHolomorphicTransition_iff_differentiable.mp hg).mul
      (isHolomorphicTransition_iff_differentiable.mp hh))

theorem isHolomorphicTransition_inv {g : ℂ → ℂ} (hz : ∀ x, g x ≠ 0)
    (hg : IsHolomorphicTransition g) :
    IsHolomorphicTransition g⁻¹ :=
  isHolomorphicTransition_iff_differentiable.mpr
    ((isHolomorphicTransition_iff_differentiable.mp hg).inv hz)

end HG4dHolomorphicTransitionMulInvClosureProbe

/- ============================================================
   PART 3 -- inlined verbatim from
   `HolomorphicTransitionSubgroupProbe.lean` (HG-4e, Wave-5).
   ============================================================ -/

namespace HG4eHolomorphicTransitionSubgroupProbe

open HG4HolomorphicTransitionProbe HG4dHolomorphicTransitionMulInvClosureProbe

theorem holomorphicTransitionUnit_val_ne_zero (u : (ℂ → ℂ)ˣ) :
    ∀ x, (u : ℂ → ℂ) x ≠ 0 := fun x =>
  isUnit_iff_ne_zero.mp (Pi.isUnit_iff.mp u.isUnit x)

/-- The HG-4e subgroup, inlined verbatim: units of `ℂ → ℂ` whose
underlying function is holomorphic. -/
def HolomorphicTransitionSubgroup : Subgroup (ℂ → ℂ)ˣ where
  carrier := {u | IsHolomorphicTransition (u : ℂ → ℂ)}
  one_mem' := by
    show IsHolomorphicTransition ((1 : (ℂ → ℂ)ˣ) : ℂ → ℂ)
    rw [Units.val_one]
    exact isHolomorphicTransition_iff_differentiable.mpr (differentiable_const 1)
  mul_mem' {u v} hu hv := by
    show IsHolomorphicTransition ((u * v : (ℂ → ℂ)ˣ) : ℂ → ℂ)
    rw [Units.val_mul]
    exact isHolomorphicTransition_mul hu hv
  inv_mem' {u} hu := by
    show IsHolomorphicTransition ((u⁻¹ : (ℂ → ℂ)ˣ) : ℂ → ℂ)
    rw [Units.val_inv_eq_inv_val]
    exact isHolomorphicTransition_inv (holomorphicTransitionUnit_val_ne_zero u) hu

theorem mem_holomorphicTransitionSubgroup_iff {u : (ℂ → ℂ)ˣ} :
    u ∈ HolomorphicTransitionSubgroup ↔ IsHolomorphicTransition (u : ℂ → ℂ) :=
  Iff.rfl

end HG4eHolomorphicTransitionSubgroupProbe

/- ============================================================
   PART 4 -- inlined verbatim from
   `HG4FExpConjNotHolomorphicSubgroupProbe.lean` (HG-4f, Wave-5): the
   non-differentiability of `exp ∘ conj`, its packaging as a unit
   `expConjUnit`, and the non-membership fact `expConjUnit_not_mem` that
   this item's test needs.
   ============================================================ -/

namespace HG4FEstagio1ExpConjNotDifferentiable

/-- `z ↦ exp(conj z)` is NOT complex-differentiable everywhere
(witnessed at `x = 1`), by the "real-linear derivative forced
ℂ-linear" contradiction technique, scaled by the nonzero constant
`c = exp(conj 1) = exp 1`. Inlined verbatim from HG-4f (Wave-5). -/
theorem not_differentiable_exp_comp_conj :
    ¬ Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ) := by
  intro hdiff
  set x : ℂ := 1 with hx
  have hexpC : HasFDerivAt Complex.exp
      (ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ)) : ℂ →L[ℂ] ℂ) (1 : ℂ) :=
    (Complex.hasDerivAt_exp (1 : ℂ)).hasFDerivAt
  have hexpR : HasFDerivAt Complex.exp
      ((ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ))).restrictScalars ℝ) (1 : ℂ) :=
    hexpC.restrictScalars ℝ
  have hconjx : starRingEnd ℂ x = (1 : ℂ) := by simp [hx]
  have hconj : HasFDerivAt (starRingEnd ℂ) (Complex.conjCLE : ℂ →L[ℝ] ℂ) x := by
    have h := (Complex.conjCLE).hasFDerivAt (x := x)
    have hfun : (⇑(Complex.conjCLE) : ℂ → ℂ) = starRingEnd ℂ := funext Complex.conjCLE_apply
    rw [hfun] at h
    exact h
  have hcomp : HasFDerivAt (Complex.exp ∘ starRingEnd ℂ)
      (((ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ))).restrictScalars ℝ).comp
        (Complex.conjCLE : ℂ →L[ℝ] ℂ)) x := by
    have hg : HasFDerivAt Complex.exp
        ((ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ))).restrictScalars ℝ)
        (starRingEnd ℂ x) := by rw [hconjx]; exact hexpR
    exact HasFDerivAt.comp (x := x) hg hconj
  have hcompEval : ∀ z : ℂ,
      (((ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ))).restrictScalars ℝ).comp
        (Complex.conjCLE : ℂ →L[ℝ] ℂ)) z = starRingEnd ℂ z * Complex.exp (1 : ℂ) := by
    intro z
    simp [ContinuousLinearMap.toSpanSingleton_apply, smul_eq_mul]
  have hcdiff : HasFDerivAt (Complex.exp ∘ starRingEnd ℂ)
      (fderiv ℂ (Complex.exp ∘ starRingEnd ℂ) x) x := (hdiff x).hasFDerivAt
  set f' : ℂ →L[ℂ] ℂ := fderiv ℂ (Complex.exp ∘ starRingEnd ℂ) x with hf'
  have hres : HasFDerivAt (Complex.exp ∘ starRingEnd ℂ) (f'.restrictScalars ℝ) x :=
    hcdiff.restrictScalars ℝ
  have huniq : f'.restrictScalars ℝ =
      ((ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ))).restrictScalars ℝ).comp
        (Complex.conjCLE : ℂ →L[ℝ] ℂ) :=
    hres.unique hcomp
  have heval : ∀ z : ℂ, f' z = starRingEnd ℂ z * Complex.exp (1 : ℂ) := by
    intro z
    have hz := congrArg (fun g : ℂ →L[ℝ] ℂ => g z) huniq
    simpa using (hz.trans (hcompEval z))
  have h1 : f' 1 = Complex.exp (1 : ℂ) := by simpa using heval 1
  have hI : f' Complex.I = -Complex.I * Complex.exp (1 : ℂ) := by
    have := heval Complex.I
    rwa [Complex.conj_I] at this
  have hlin : f' Complex.I = Complex.I * f' 1 := by
    have := f'.map_smul Complex.I (1 : ℂ)
    simpa [smul_eq_mul] using this
  rw [h1, hI] at hlin
  have hcontra : (2 : ℂ) * Complex.I * Complex.exp (1 : ℂ) = 0 := by linear_combination -hlin
  have h2I : (2 : ℂ) * Complex.I ≠ 0 :=
    mul_ne_zero two_ne_zero Complex.I_ne_zero
  have hexp1 : Complex.exp (1 : ℂ) ≠ 0 := Complex.exp_ne_zero (1 : ℂ)
  exact (mul_ne_zero h2I hexp1) hcontra

end HG4FEstagio1ExpConjNotDifferentiable

namespace HG4FEstagio2ProperSubgroup

open HG4HolomorphicTransitionProbe HG4eHolomorphicTransitionSubgroupProbe
open HG4FEstagio1ExpConjNotDifferentiable
open ComplexConjugate

/-- `exp ∘ conj` is everywhere nonzero, hence (by `Pi.isUnit_iff.mpr`) a
unit of the pointwise-multiplication monoid `ℂ → ℂ`. Inlined verbatim
from HG-4f. -/
theorem isUnit_exp_comp_conj : IsUnit (Complex.exp ∘ starRingEnd ℂ) :=
  Pi.isUnit_iff.mpr fun x => isUnit_iff_ne_zero.mpr (Complex.exp_ne_zero (starRingEnd ℂ x))

/-- The witness unit `u : (ℂ → ℂ)ˣ` packaging `exp ∘ conj`. Inlined
verbatim from HG-4f. -/
noncomputable def expConjUnit : (ℂ → ℂ)ˣ := isUnit_exp_comp_conj.unit

@[simp] theorem expConjUnit_coe : (expConjUnit : ℂ → ℂ) = Complex.exp ∘ starRingEnd ℂ :=
  isUnit_exp_comp_conj.unit_spec

/-- The witness's non-membership in `HolomorphicTransitionSubgroup`'s
carrier -- the fact this Wave-7 item's coset test needs. Inlined
verbatim from HG-4f. -/
theorem expConjUnit_not_mem :
    expConjUnit ∉ HolomorphicTransitionSubgroup := by
  rw [mem_holomorphicTransitionSubgroup_iff, isHolomorphicTransition_iff_differentiable,
    expConjUnit_coe]
  exact not_differentiable_exp_comp_conj

end HG4FEstagio2ProperSubgroup

/- ============================================================
   PART 5 -- HG-4h itself: the actual falsifiable test for this item.
   Exactly the one line named by the Onda 7 plan. This is the only NEW
   content added by this Wave-7 file; Parts 1-4 above are verbatim
   inlines of already-closed prior-wave (HG-4/HG-4d/HG-4e/HG-4f) results,
   reproduced here only so this file compiles standalone, exactly as
   HG-4e/HG-4f/HG-4g already did for their own dependencies.
   ============================================================ -/

namespace HG4hExpConjUnitCosetNeOneProbe

open HG4eHolomorphicTransitionSubgroupProbe
open HG4FEstagio2ProperSubgroup

/-- The Wave-7 HG-4h test itself: the coset of `expConjUnit` in
`(ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup` is genuinely NOT the identity
coset, by `QuotientGroup.eq_one_iff` (the required `Normal` instance for
`HolomorphicTransitionSubgroup` resolves automatically from `(ℂ → ℂ)ˣ`
being a `CommGroup`) applied contrapositively against HG-4f's
already-closed `expConjUnit_not_mem`. -/
theorem expConjUnit_coset_ne_one :
    (expConjUnit : (ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup) ≠ 1 :=
  fun h => expConjUnit_not_mem ((QuotientGroup.eq_one_iff _).mp h)

#print axioms expConjUnit_coset_ne_one

end HG4hExpConjUnitCosetNeOneProbe

/-
RESULT: CLOSED, exactly as scoped by the Wave-7 HG-4h one-line test.
`QuotientGroup.eq_one_iff {N : Subgroup G} [N.Normal] (x : G) :
(x : G ⧸ N) = 1 ↔ x ∈ N` applies to `G := (ℂ → ℂ)ˣ`,
`N := HolomorphicTransitionSubgroup`, `x := expConjUnit`, with the
`[N.Normal]` instance resolved automatically (no new code) via
`Subgroup.normal_of_isMulCommutative` since `(ℂ → ℂ)ˣ` is a `CommGroup`;
`.mp` turns a hypothetical coset equality into membership, refuted by
HG-4f's already-closed `expConjUnit_not_mem` (inlined verbatim above,
together with its full HG-4/HG-4d/HG-4e dependency chain), giving
`expConjUnit_coset_ne_one : (expConjUnit : (ℂ → ℂ)ˣ ⧸
HolomorphicTransitionSubgroup) ≠ 1` with zero new mathematical content
beyond the single one-line proof named by the plan. No claim is made
about the quotient's cardinality, structure, or any connection to
`VectorBundle`/`Bundle`/`PicardGroup` machinery, Lefschetz (1,1), the
Hodge Conjecture, or any Millennium Problem.
-/
