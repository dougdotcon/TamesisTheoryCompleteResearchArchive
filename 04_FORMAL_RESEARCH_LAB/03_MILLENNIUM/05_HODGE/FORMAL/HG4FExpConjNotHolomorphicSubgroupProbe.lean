/-
HG-4F -- Two-stage item (Wave-5 item WAVE5-HG-4F, Hodge line /
03_MILLENNIUM/05_HODGE): (Estagio 1) non-differentiability of
`Complex.exp ∘ starRingEnd ℂ`, then (Estagio 2, gated on WAVE5-HG-4E)
`HolomorphicTransitionSubgroup` is a PROPER subgroup of `(ℂ → ℂ)ˣ`.

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (the exact residual gap this item closes):
Wave-2's `ConjugationNotHolomorphicProbe.lean` (HG-4b, this directory)
proved `¬ Differentiable ℂ (starRingEnd ℂ)` (plain conjugation is not
holomorphic), via the "real-linear derivative forced to be ℂ-linear"
contradiction at `z = 1` and `z = I`. The Wave-5 recon originally
proposed reusing `starRingEnd ℂ` itself as a witness that
`HolomorphicTransitionSubgroup` (HG-4e, this directory) is a PROPER
subgroup of `(ℂ → ℂ)ˣ` -- but the Wave-5 adversarial review caught a
fatal defect: `starRingEnd ℂ` sends `0 ↦ 0`, so it is NOT a unit of the
pointwise-multiplication monoid `ℂ → ℂ` (a unit of a `Pi`-type valued in
a field must be pointwise nonzero, by `Pi.isUnit_iff` +
`isUnit_iff_ne_zero`) and therefore cannot even be packaged as an
element `u : (ℂ → ℂ)ˣ` to test membership against. The adversarial
review's fix, attempted here EXACTLY as narrowed, is to replace the
witness with `Complex.exp ∘ starRingEnd ℂ` (`z ↦ exp(conj z)`), which
IS everywhere nonzero (`Complex.exp_ne_zero`) and hence genuinely
packages as a unit, while remaining non-holomorphic by the same
"real-linear derivative forced ℂ-linear" contradiction technique,
scaled by the nonzero constant `c = exp(conj x) ≠ 0` instead of `1`.

THE TEST, AND THE RESULT.

ESTAGIO 1 (autonomous, attempted and CLOSED unconditionally):
  `¬ Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ)`.
  Fix the point `x := (1 : ℂ)` (so `conj x = 1`, keeping the scaling
  constant `c = exp(conj x) = exp 1` concretely nonzero and ≠ 1, per the
  Wave-5 plan's "scaled by `c = exp(conj x) ≠ 0`" description, rather
  than trivializing to the `c = 1` case that `x := 0` would give).
    (a) `Complex.hasDerivAt_exp 1 : HasDerivAt Complex.exp (Complex.exp 1) 1`
        converts, via `HasDerivAt.hasFDerivAt` (the explicit bridge named
        by the Wave-5 plan), to
        `HasFDerivAt Complex.exp (toSpanSingleton ℂ (Complex.exp 1)) 1`,
        a ℂ-linear map; `HasFDerivAt.restrictScalars ℝ` turns this into
        the ℝ-linear fact needed to compose with `conj`'s ℝ-linear
        derivative.
    (b) `Complex.conjCLE.hasFDerivAt` + `Complex.conjCLE_apply` gives
        `HasFDerivAt (starRingEnd ℂ) (Complex.conjCLE : ℂ →L[ℝ] ℂ) x`
        (exactly as in HG-4b), and `conj x = conj 1 = 1` matches the
        point in (a).
    (c) `HasFDerivAt.comp` composes (a)'s restricted map with (b) to get
        the REAL-linear derivative of `exp ∘ conj` at `x`:
        `HasFDerivAt (Complex.exp ∘ starRingEnd ℂ)
          ((toSpanSingleton ℂ (Complex.exp 1)).restrictScalars ℝ ∘L
            Complex.conjCLE) x`,
        whose value at any `z` unfolds (via `toSpanSingleton_apply` +
        `conjCLE_apply`) to `conj z * Complex.exp 1`.
    (d) Assume toward contradiction
        `Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ)`. Then at `x`
        there is a ℂ-LINEAR derivative `f' := fderiv ℂ (exp ∘ conj) x`
        with `HasFDerivAt (exp ∘ conj) f' x`; `HasFDerivAt.restrictScalars
        ℝ` gives the matching ℝ-linear fact, and `HasFDerivAt.unique`
        against (c) forces `f'` to agree POINTWISE with `z ↦ conj z *
        exp 1` (evaluating the two equal continuous ℝ-linear maps as
        functions).
    (e) But `f'` is ℂ-linear, so `f' I = I * f' 1`. Plugging in the
        values forced by (d) at `z = 1` (`conj 1 = 1`, so `f' 1 = exp 1`)
        and `z = I` (`conj I = -I`, so `f' I = -I * exp 1`) gives
        `-I * exp 1 = I * exp 1`, i.e. `(2 * I) * exp 1 = 0`. Since
        `Complex.exp_ne_zero` gives `exp 1 ≠ 0` and `2 * I ≠ 0`
        (`I ≠ 0`, `(2:ℂ) ≠ 0`), this is `False` by `mul_ne_zero`.
  This is the EXACT falsifiable claim named by Estagio 1 of the Wave-5
  plan -- nothing broader, no attempt to reconnect to
  `IsHolomorphicTransition` or any `Subgroup` in this stage.

ESTAGIO 2 (gated on WAVE5-HG-4E, attempted here because the dependency's
output file, `HolomorphicTransitionSubgroupProbe.lean`, was found in
this directory, independently recompiled by this file's author with
`lake env lean` (exit 0, clean `#print axioms` on all four of its
declarations) BEFORE this stage was attempted -- see the verification
log referenced in the final report):
  Package `Complex.exp ∘ starRingEnd ℂ` as a term
  `u : (ℂ → ℂ)ˣ` (via `Complex.exp_ne_zero` supplying pointwise
  nonvanishing, `Pi.isUnit_iff.mpr` lifting that to `IsUnit` of the
  `Pi`-type, and `Units.ofPowers`... -- concretely, `IsUnit.unit` of
  the `Pi.isUnit_iff.mpr` witness), then show `u ∉
  HolomorphicTransitionSubgroup.carrier` using the Estagio 1 result
  (`IsHolomorphicTransition (u : ℂ → ℂ)` unfolds, via
  `isHolomorphicTransition_iff_differentiable`, to exactly
  `Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ)`, refuted by Estagio
  1), concluding `HolomorphicTransitionSubgroup ≠ ⊤` (a genuinely proper
  subgroup, since `⊤`'s carrier is all of `(ℂ → ℂ)ˣ`, which contains
  `u`, while `HolomorphicTransitionSubgroup`'s carrier does not).
  This is the exact Estagio 2 claim named by the Wave-5 plan; nothing
  broader is attempted (no cocycle-condition bookkeeping, no
  `VectorBundle`/`Bundle` API).

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT modify `ConjugationNotHolomorphicProbe.lean`,
  `HolomorphicTransitionProbe.lean`,
  `HolomorphicTransitionMulInvClosureProbe.lean`, or
  `HolomorphicTransitionSubgroupProbe.lean`; it inlines copies of the
  short relevant pieces from the latter three into this new file, in
  exactly the pattern HG-4d/HG-4e already used for their own
  dependencies.
- Does NOT define or touch any `VectorBundle`/`Bundle`/
  `HolomorphicLineBundle` API, and does NOT attempt any cocycle-condition
  bookkeeping for an actual line bundle.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: every lemma used
  (`Complex.hasDerivAt_exp`, `HasDerivAt.hasFDerivAt`,
  `HasFDerivAt.restrictScalars`, `HasFDerivAt.comp`, `HasFDerivAt.unique`,
  `Complex.exp_ne_zero`, `Complex.conjCLE`/`conjCLE_apply`,
  `Pi.isUnit_iff`, `isUnit_iff_ne_zero`) is pre-existing, proved Mathlib
  content; the only thing built here is their composition into these two
  specific facts.
- Does NOT claim `HolomorphicTransitionSubgroup ≠ ⊤` is a fact "about
  subgroups of `(ℂ → ℂ)ˣ` in general" -- it is a fact about this one
  specific subgroup and this one specific witness `u`.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by this
file's own successful compilation):
  - `Complex.hasDerivAt_exp (x : ℂ) : HasDerivAt exp (exp x) x`
                               Analysis/SpecialFunctions/ExpDeriv.lean:88
  - `HasDerivAt.hasFDerivAt` (alias of `hasDerivAt_iff_hasFDerivAt.mp`,
    producing `HasFDerivAt f (toSpanSingleton 𝕜 f') x`)
                               Analysis/Calculus/Deriv/Basic.lean:202
  - `ContinuousLinearMap.toSpanSingleton_apply (x) (r) :
    toSpanSingleton R₁ x r = r • x`
                               Topology/Algebra/Module/ContinuousLinearMap/Basic.lean:746
  - `HasFDerivAt.restrictScalars`
                               Analysis/Calculus/FDeriv/RestrictScalars.lean:56
  - `HasFDerivAt.comp {g'} (hg : HasFDerivAt g g' (f x)) (hf : HasFDerivAt
    f f' x) : HasFDerivAt (g ∘ f) (g'.comp f') x`
                               Analysis/Calculus/FDeriv/Comp.lean:105
  - `HasFDerivAt.unique`
                               Analysis/Calculus/FDeriv/Basic.lean:174
  - `Complex.exp_ne_zero : exp x ≠ 0`
                               Analysis/Complex/Exponential.lean:162
  - `Complex.conjCLE : ℂ ≃L[ℝ] ℂ`, `Complex.conjCLE_apply`
                               Analysis/Complex/Basic.lean:256, :275
  - `Complex.conj_I : conj I = -I`
                               Data/Complex/Basic.lean:478
  - `Pi.isUnit_iff : IsUnit x ↔ ∀ i, IsUnit (x i)`
                               Algebra/Group/Pi/Units.lean:31
  - `isUnit_iff_ne_zero : IsUnit a ↔ a ≠ 0`
                               Algebra/GroupWithZero/Units/Basic.lean:264
  - HG-4E dependency (Estagio 2 only), inlined verbatim below:
    `IsHolomorphicTransition`, `isHolomorphicTransition_iff_differentiable`
    (HG-4/Wave-1), `isHolomorphicTransition_mul`/`_inv` (HG-4d/Wave-4),
    `HolomorphicTransitionSubgroup` (HG-4e/Wave-5) --
    `HolomorphicTransitionSubgroupProbe.lean`, this directory,
    independently recompiled by this file's author before Estagio 2 was
    attempted (`lake env lean`, exit 0, clean `#print axioms` on all four
    of its declarations).
-/

import Mathlib

open ComplexConjugate

/- ============================================================
   ESTAGIO 1 -- autonomous, non-differentiability of `exp ∘ conj`.
   ============================================================ -/

namespace HG4FEstagio1ExpConjNotDifferentiable

/-- The Estagio 1 falsifiable claim for HG-4F: `z ↦ exp(conj z)` is NOT
complex-differentiable everywhere (witnessed at `x = 1`), by the same
"real-linear derivative forced ℂ-linear" contradiction technique as
HG-4b's `not_differentiable_starRingEnd`, now scaled by the nonzero
constant `c = exp(conj 1) = exp 1` instead of `c = 1`. -/
theorem not_differentiable_exp_comp_conj :
    ¬ Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ) := by
  intro hdiff
  set x : ℂ := 1 with hx
  -- (a) The ℂ-linear derivative of `Complex.exp` at `conj x = 1`,
  -- restricted to ℝ-linearity so it can be composed with `conj`'s own
  -- ℝ-linear derivative.
  have hexpC : HasFDerivAt Complex.exp
      (ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ)) : ℂ →L[ℂ] ℂ) (1 : ℂ) :=
    (Complex.hasDerivAt_exp (1 : ℂ)).hasFDerivAt
  have hexpR : HasFDerivAt Complex.exp
      ((ContinuousLinearMap.toSpanSingleton ℂ (Complex.exp (1 : ℂ))).restrictScalars ℝ) (1 : ℂ) :=
    hexpC.restrictScalars ℝ
  -- (b) The ℝ-linear derivative of `conj` at `x`, from HG-4b's argument.
  have hconjx : starRingEnd ℂ x = (1 : ℂ) := by simp [hx]
  have hconj : HasFDerivAt (starRingEnd ℂ) (Complex.conjCLE : ℂ →L[ℝ] ℂ) x := by
    have h := (Complex.conjCLE).hasFDerivAt (x := x)
    have hfun : (⇑(Complex.conjCLE) : ℂ → ℂ) = starRingEnd ℂ := funext Complex.conjCLE_apply
    rw [hfun] at h
    exact h
  -- (c) Compose: the real-linear derivative of `exp ∘ conj` at `x`.
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
  -- (d) Assume toward contradiction that `exp ∘ conj` is ℂ-differentiable.
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
  -- (e) But `f'` is ℂ-linear, forcing a contradiction at `z = 1` and
  -- `z = I`, using `c := exp 1 ≠ 0`.
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

#print axioms not_differentiable_exp_comp_conj

end HG4FEstagio1ExpConjNotDifferentiable

/- ============================================================
   ESTAGIO 2 -- gated on WAVE5-HG-4E. Inlines the HG-4/HG-4d/HG-4e
   machinery (verbatim, exactly as HG-4e inlined HG-4/HG-4d), then packages
   `exp ∘ conj` as a unit and shows `HolomorphicTransitionSubgroup ≠ ⊤`.
   ============================================================ -/

/- ---- Part 1: inlined verbatim from `HolomorphicTransitionProbe.lean`
   (HG-4, Wave-1). ---- -/

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

/- ---- Part 2: inlined verbatim from
   `HolomorphicTransitionMulInvClosureProbe.lean` (HG-4d, Wave-4). ---- -/

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

/- ---- Part 3: inlined verbatim from
   `HolomorphicTransitionSubgroupProbe.lean` (HG-4e, Wave-5). ---- -/

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

/- ---- Part 4: HG-4F Estagio 2 itself -- the actual falsifiable test for
   this gated stage. Package `exp ∘ conj` as a unit, show it is not in
   the carrier (via Estagio 1), conclude the subgroup is proper. ---- -/

namespace HG4FEstagio2ProperSubgroup

open HG4HolomorphicTransitionProbe HG4eHolomorphicTransitionSubgroupProbe
open HG4FEstagio1ExpConjNotDifferentiable
open ComplexConjugate

/-- `exp ∘ conj` is everywhere nonzero, hence (by `Pi.isUnit_iff.mpr`) a
unit of the pointwise-multiplication monoid `ℂ → ℂ`. -/
theorem isUnit_exp_comp_conj : IsUnit (Complex.exp ∘ starRingEnd ℂ) :=
  Pi.isUnit_iff.mpr fun x => isUnit_iff_ne_zero.mpr (Complex.exp_ne_zero (starRingEnd ℂ x))

/-- The witness unit `u : (ℂ → ℂ)ˣ` packaging `exp ∘ conj`. -/
noncomputable def expConjUnit : (ℂ → ℂ)ˣ := isUnit_exp_comp_conj.unit

@[simp] theorem expConjUnit_coe : (expConjUnit : ℂ → ℂ) = Complex.exp ∘ starRingEnd ℂ :=
  isUnit_exp_comp_conj.unit_spec

/-- The Estagio 2 test: `expConjUnit` genuinely fails to lie in
`HolomorphicTransitionSubgroup`'s carrier, by the Estagio 1
non-differentiability result. -/
theorem expConjUnit_not_mem :
    expConjUnit ∉ HolomorphicTransitionSubgroup := by
  rw [mem_holomorphicTransitionSubgroup_iff, isHolomorphicTransition_iff_differentiable,
    expConjUnit_coe]
  exact not_differentiable_exp_comp_conj

/-- The HG-4F Estagio 2 conclusion: `HolomorphicTransitionSubgroup` is a
PROPER subgroup of `(ℂ → ℂ)ˣ` -- it does not contain every unit, since it
misses `expConjUnit`. -/
theorem holomorphicTransitionSubgroup_ne_top :
    HolomorphicTransitionSubgroup ≠ (⊤ : Subgroup (ℂ → ℂ)ˣ) := by
  intro htop
  exact expConjUnit_not_mem (htop ▸ Subgroup.mem_top expConjUnit)

#print axioms isUnit_exp_comp_conj
#print axioms expConjUnit_coe
#print axioms expConjUnit_not_mem
#print axioms holomorphicTransitionSubgroup_ne_top

end HG4FEstagio2ProperSubgroup

/-
RESULT.

ESTAGIO 1: CLOSED. `¬ Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ)` is
proved exactly as scoped by the Wave-5 HG-4F Estagio 1 test: the
`HasDerivAt.hasFDerivAt` bridge converts `Complex.hasDerivAt_exp`'s
scalar derivative into a ℂ-linear `HasFDerivAt` fact, restricted to
ℝ-linearity and composed (`HasFDerivAt.comp`) with `conj`'s own
ℝ-linear derivative (`Complex.conjCLE`) to get the real-linear derivative
of `exp ∘ conj` at `x = 1`; `HasFDerivAt.unique` against a hypothetical
ℂ-linear derivative forces the two to coincide pointwise, and ℂ-linearity
of the hypothetical derivative then contradicts the two forced values at
`z = 1` and `z = I`, using `Complex.exp_ne_zero` to rule out the
degenerate case `exp 1 = 0` in the final `mul_ne_zero` step. This closes
the autonomous half of the Wave-5 HG-4F item.

ESTAGIO 2: CLOSED, GATED ON WAVE5-HG-4E (whose output file,
`HolomorphicTransitionSubgroupProbe.lean`, was found already present in
this directory and independently recompiled by this file's author with
`lake env lean` before this stage was attempted -- exit 0, clean
`#print axioms` on all four of its declarations, confirming HG-4E is
genuinely closed and not merely claimed closed by its own header
comment). `Complex.exp ∘ starRingEnd ℂ` is packaged as a unit
`expConjUnit : (ℂ → ℂ)ˣ` via `Complex.exp_ne_zero` + `Pi.isUnit_iff.mpr`
+ `IsUnit.unit`; `expConjUnit_not_mem` shows it is NOT a member of
`HolomorphicTransitionSubgroup`'s carrier, by unfolding membership
(`mem_holomorphicTransitionSubgroup_iff`,
`isHolomorphicTransition_iff_differentiable`) to exactly the
Estagio-1-refuted claim `Differentiable ℂ (Complex.exp ∘ starRingEnd ℂ)`;
`holomorphicTransitionSubgroup_ne_top` then concludes
`HolomorphicTransitionSubgroup ≠ ⊤` from `Subgroup.mem_top`. This closes
the gated half of the Wave-5 HG-4F item exactly as narrowed by the
adversarial review: a genuine properness fact about THIS specific
subgroup, witnessed by THIS specific unit -- no claim about
`VectorBundle`/`Bundle` machinery, cocycle conditions, Lefschetz (1,1),
the Hodge Conjecture, or any Millennium Problem is made anywhere in this
file.
-/
