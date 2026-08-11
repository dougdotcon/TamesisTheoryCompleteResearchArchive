/-
HG-4g -- Quociente por `HolomorphicTransitionSubgroup` e `Nontrivial`
(Wave-6 item WAVE6-HG-4G, Hodge line / 03_MILLENNIUM/05_HODGE).

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (the exact residual gap this item closes):
Wave-5's `HolomorphicTransitionSubgroupProbe.lean` (HG-4e, this
directory) packaged the mul/inv closure of `IsHolomorphicTransition`
(HG-4, Wave-1) as an actual `Subgroup (ℂ → ℂ)ˣ`,
`HolomorphicTransitionSubgroup`. Wave-5's
`HG4FExpConjNotHolomorphicSubgroupProbe.lean` (HG-4f) then supplied a
concrete witness unit -- `expConjUnit`, packaging `Complex.exp ∘
starRingEnd ℂ` -- that lies in `(ℂ → ℂ)ˣ` but NOT in
`HolomorphicTransitionSubgroup`'s carrier, and concluded
`holomorphicTransitionSubgroup_ne_top :
HolomorphicTransitionSubgroup ≠ (⊤ : Subgroup (ℂ → ℂ)ˣ)`. Nothing in
Wave-5 packaged this properness fact as a statement about the QUOTIENT
group `(ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup`. This Wave-6 item
(HG-4g) closes exactly that gap: `N ≠ ⊤` for a subgroup `N` of a group
`G` is, by Mathlib's `QuotientGroup.nontrivial_iff`, definitionally
equivalent to the coset space `G ⧸ N` having a `Nontrivial` instance
(i.e. genuinely more than one coset) -- so `holomorphicTransitionSubgroup
_ne_top` transports, with zero new mathematical content, to
`Nontrivial ((ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup)`. Nothing
broader.

THE TEST, AND THE RESULT: CLOSED, exactly as narrowed by the Onda 6
plan (single line):
  `theorem holomorphicTransitionQuotient_nontrivial :
      Nontrivial ((ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup) :=
    QuotientGroup.nontrivial_iff.mpr holomorphicTransitionSubgroup_ne_top`
This type-checks and proves as written, with no modification needed:
`QuotientGroup.nontrivial_iff {G : Type*} [Group G] {N : Subgroup G} :
Nontrivial (G ⧸ N) ↔ N ≠ ⊤` (Mathlib/GroupTheory/QuotientGroup/Defs.lean)
applies directly to `G := (ℂ → ℂ)ˣ` (a `CommGroup`, hence a `Group`) and
`N := HolomorphicTransitionSubgroup`, and its statement requires no
`Subgroup.Normal` instance (the coset TYPE `G ⧸ N` -- i.e.
`Quotient (QuotientGroup.leftRel N)` via the `HasQuotient` instance --
exists for any subgroup regardless of normality; only the GROUP
structure on that quotient needs normality, which this test does not
use). `.mpr` is fed exactly HG-4f's `holomorphicTransitionSubgroup_ne_top`
(inlined below, verbatim, together with its full HG-4/HG-4d/HG-4e/HG-4f
dependency chain, in the same "inline the short relevant pieces"
pattern HG-4e/HG-4f already used for their own dependencies).

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT modify `HolomorphicTransitionProbe.lean`,
  `HolomorphicTransitionMulInvClosureProbe.lean`,
  `HolomorphicTransitionSubgroupProbe.lean`, or
  `HG4FExpConjNotHolomorphicSubgroupProbe.lean`; it inlines copies of
  the short relevant pieces from all four into this new file, exactly
  as HG-4e/HG-4f inlined their own dependencies.
- Does NOT compute or characterize the quotient group
  `(ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup` any further (no
  cardinality, no explicit coset representatives, no group-structure
  claims beyond the bare `Nontrivial` instance) -- only the exact
  one-line `Nontrivial` test named by the Onda 6 plan is attempted.
- Does NOT define or touch any `VectorBundle`/`Bundle`/
  `HolomorphicLineBundle`/`PicardGroup` API, and does NOT attempt any
  cocycle-condition bookkeeping for an actual line bundle.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: every lemma used
  (`QuotientGroup.nontrivial_iff`, plus everything HG-4/HG-4d/HG-4e/HG-4f
  already used) is pre-existing, proved Mathlib content or a verbatim
  inline of an already-closed prior-wave result; the only new step here
  is the single `.mpr` application named by the plan.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by
this file's own successful compilation):
  - `QuotientGroup.nontrivial_iff {G : Type*} [Group G] {N : Subgroup G} :
    Nontrivial (G ⧸ N) ↔ N ≠ ⊤`
                             GroupTheory/QuotientGroup/Defs.lean:54
    (declared before the `variable (N) [nN : N.Normal]` line at :58, so
    it genuinely requires no `Normal` instance.)
  - `instCommGroupUnits {α} [CommMonoid α] : CommGroup αˣ`
                             Algebra/Group/Units/Defs.lean:265-267
  - HG-4/HG-4d/HG-4e/HG-4f dependencies, inlined verbatim below:
    `IsHolomorphicTransition`, `isHolomorphicTransition_iff_differentiable`
    (HG-4/Wave-1), `isHolomorphicTransition_mul`/`_inv` (HG-4d/Wave-4),
    `HolomorphicTransitionSubgroup` (HG-4e/Wave-5),
    `not_differentiable_exp_comp_conj`, `expConjUnit`,
    `holomorphicTransitionSubgroup_ne_top` (HG-4f/Wave-5) --
    `HG4FExpConjNotHolomorphicSubgroupProbe.lean`, this directory,
    independently recompiled by this file's author with `lake env lean`
    (exit 0, clean `#print axioms` on all of its declarations) before
    this item was attempted.
-/

import Mathlib

open ComplexConjugate

/- ============================================================
   PART 1 -- inlined verbatim from `HolomorphicTransitionProbe.lean`
   (HG-4, Wave-1).
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
   `expConjUnit`, and the properness conclusion
   `holomorphicTransitionSubgroup_ne_top` that this item's test needs.
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

theorem expConjUnit_not_mem :
    expConjUnit ∉ HolomorphicTransitionSubgroup := by
  rw [mem_holomorphicTransitionSubgroup_iff, isHolomorphicTransition_iff_differentiable,
    expConjUnit_coe]
  exact not_differentiable_exp_comp_conj

/-- The HG-4f conclusion, inlined verbatim: `HolomorphicTransitionSubgroup`
is a PROPER subgroup of `(ℂ → ℂ)ˣ`. This is the fact HG-4g's quotient
test transports across `QuotientGroup.nontrivial_iff`. -/
theorem holomorphicTransitionSubgroup_ne_top :
    HolomorphicTransitionSubgroup ≠ (⊤ : Subgroup (ℂ → ℂ)ˣ) := by
  intro htop
  exact expConjUnit_not_mem (htop ▸ Subgroup.mem_top expConjUnit)

end HG4FEstagio2ProperSubgroup

/- ============================================================
   PART 5 -- HG-4g itself: the actual falsifiable test for this item.
   Exactly the one line named by the Onda 6 plan.
   ============================================================ -/

namespace HG4gHolomorphicTransitionQuotientNontrivialProbe

open HG4eHolomorphicTransitionSubgroupProbe
open HG4FEstagio2ProperSubgroup

/-- The Wave-6 HG-4g test itself: the quotient of `(ℂ → ℂ)ˣ` by
`HolomorphicTransitionSubgroup` is genuinely `Nontrivial` (has more than
one coset), by `QuotientGroup.nontrivial_iff` applied to HG-4f's
properness fact `holomorphicTransitionSubgroup_ne_top`. -/
theorem holomorphicTransitionQuotient_nontrivial :
    Nontrivial ((ℂ → ℂ)ˣ ⧸ HolomorphicTransitionSubgroup) :=
  QuotientGroup.nontrivial_iff.mpr holomorphicTransitionSubgroup_ne_top

#print axioms holomorphicTransitionQuotient_nontrivial

end HG4gHolomorphicTransitionQuotientNontrivialProbe

/-
RESULT: CLOSED, exactly as scoped by the Wave-6 HG-4g one-line test.
`QuotientGroup.nontrivial_iff {G} [Group G] {N : Subgroup G} :
Nontrivial (G ⧸ N) ↔ N ≠ ⊤` applies directly to `G := (ℂ → ℂ)ˣ` and
`N := HolomorphicTransitionSubgroup` (no `Subgroup.Normal` instance
needed for this statement); its `.mpr` direction is fed HG-4f's
already-closed `holomorphicTransitionSubgroup_ne_top` (inlined verbatim
above, together with its full HG-4/HG-4d/HG-4e dependency chain), giving
`holomorphicTransitionQuotient_nontrivial : Nontrivial ((ℂ → ℂ)ˣ ⧸
HolomorphicTransitionSubgroup)` with zero new mathematical content beyond
the single `.mpr` application named by the plan. No claim is made about
the quotient's cardinality, structure, or any connection to
`VectorBundle`/`Bundle`/`PicardGroup` machinery, Lefschetz (1,1), the
Hodge Conjecture, or any Millennium Problem.
-/
