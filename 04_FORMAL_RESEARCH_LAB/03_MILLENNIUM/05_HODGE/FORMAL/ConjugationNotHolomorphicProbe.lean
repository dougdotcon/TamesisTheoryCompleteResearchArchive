/-
HG-4B -- Complex conjugation is not complex-differentiable (Wave-2 item,
Hodge line / 03_MILLENNIUM/05_HODGE)

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (Wave-1 residual gap this item closes):
Wave-1's `HolomorphicTransitionProbe.lean` (this directory) built a
predicate `IsHolomorphicTransition g := MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g`
for line-bundle transition functions and showed it is statable and
satisfiable (by `Complex.exp`), but left one honest residual gap: it did
NOT show the predicate correctly REJECTS a genuine real-smooth-but-not-
holomorphic example, e.g. complex conjugation. That file's own header
sketches the expected argument: "conjugation is ℝ-linear but not
ℂ-linear, so a would-be complex derivative of it would have to be
simultaneously ℂ-linear and equal to conjugation itself, impossible for
a nonzero map," to be built from `Complex.conjCLE`,
`HasFDerivAt.restrictScalars`, and `HasFDerivAt.unique`. This file (the
Wave-2 plan's HG-4b item) attempts EXACTLY that narrower, self-contained
claim -- `¬ Differentiable ℂ (starRingEnd ℂ)` -- nothing broader: it does
NOT re-attempt to plug the result back into `IsHolomorphicTransition`
(that one-line corollary is left as future connective work, out of scope
for this narrow test), and does NOT touch `HolomorphicTransitionProbe.lean`
itself.

THE TEST, AND THE RESULT: CLOSED.
Fix any point `x : ℂ` (`0` below, but the argument is point-independent).

  (a) `Complex.conjCLE : ℂ ≃L[ℝ] ℂ` is a continuous ℝ-linear equivalence
      whose underlying function is exactly `starRingEnd ℂ`
      (`Complex.conjCLE_apply`). `ContinuousLinearEquiv.hasFDerivAt` gives
      `HasFDerivAt (starRingEnd ℂ) (Complex.conjCLE : ℂ →L[ℝ] ℂ) x`.

  (b) Suppose toward a contradiction `Differentiable ℂ (starRingEnd ℂ)`.
      Then at `x` there is a ℂ-linear derivative
      `f' := fderiv ℂ (starRingEnd ℂ) x : ℂ →L[ℂ] ℂ` with
      `HasFDerivAt (starRingEnd ℂ) f' x`. Restricting scalars
      (`HasFDerivAt.restrictScalars ℝ`) gives the ℝ-linear fact
      `HasFDerivAt (starRingEnd ℂ) (f'.restrictScalars ℝ) x`.

  (c) `HasFDerivAt.unique` applied to (a) and (b) (same function, same
      point `x`) forces `f'.restrictScalars ℝ = (Complex.conjCLE : ℂ →L[ℝ] ℂ)`
      as continuous ℝ-linear maps, hence `f' z = starRingEnd ℂ z` for
      EVERY `z : ℂ` (evaluating the equal continuous linear maps
      pointwise).

  (d) But `f'` is ℂ-LINEAR: `f' I = f' (I • 1) = I • f' 1 = I * f' 1`. By
      (c), `f' 1 = starRingEnd ℂ 1 = 1` and `f' I = starRingEnd ℂ I = -I`.
      Substituting: `-I = I * 1 = I`, i.e. `I = -I`, i.e. `(2 : ℂ) * I = 0`,
      contradiction since `I ≠ 0` and `ℂ` has characteristic zero. This is
      exactly the "generic ℂ-linear map `c ↦ c * z` cannot equal `conj` at
      `z = 1` and `z = I` simultaneously" contradiction named in the
      Wave-2 plan for HG-4b (forcing `c = 1` from `z = 1` and `c = -1` from
      `z = I`).

This file contains none of the four governance-forbidden tokens (the
lab's standard "no shortcuts, no unchecked escape hatches" list) at any
point, including inside comments; the closing `#print axioms` line below
confirms the proof's trust base is exactly the three standard core
primitives.

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT reconnect this result to `IsHolomorphicTransition` from
  `HolomorphicTransitionProbe.lean`, and does NOT modify that file.
- Does NOT define or touch any `VectorBundle`/`Bundle`/`HolomorphicLineBundle`
  API.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: `Complex.conjCLE`,
  `ContinuousLinearEquiv.hasFDerivAt`, `HasFDerivAt.restrictScalars`, and
  `HasFDerivAt.unique` are pre-existing, proved Mathlib content; the only
  thing built here is their composition into this one specific
  non-differentiability fact.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by this
file's own successful compilation):
  - `Complex.conjCLE : ℂ ≃L[ℝ] ℂ`, `Complex.conjCLE_apply`
                               Analysis/Complex/Basic.lean:256, :~264ff
  - `ContinuousLinearEquiv.hasFDerivAt`
                               Analysis/Calculus/FDeriv/Equiv.lean:56
  - `HasFDerivAt.restrictScalars`
                               Analysis/Calculus/FDeriv/RestrictScalars.lean:56
  - `HasFDerivAt.unique`
                               Analysis/Calculus/FDeriv/Basic.lean:174
  - `DifferentiableAt.hasFDerivAt`
                               Analysis/Calculus/FDeriv/Basic.lean:397
  - `ContinuousLinearMap.map_smul` (protected)
                               Topology/Algebra/Module/ContinuousLinearMap/Basic.lean:227
  - `starRingEnd`, notation `conj` in scope `ComplexConjugate`
                               Data/Complex/Basic.lean:458 (`conj` is
      literally notation for `starRingEnd ℂ`, not a separate definition,
      so results about `starRingEnd ℂ` transfer directly to `conj`).
-/

import Mathlib

namespace HG4bConjugationNotHolomorphicProbe

open ComplexConjugate

/-- The candidate falsifiable claim for HG-4b: complex conjugation,
`starRingEnd ℂ` (i.e. `conj`), is NOT complex-differentiable anywhere,
hence not `Differentiable ℂ` globally. -/
theorem not_differentiable_starRingEnd :
    ¬ Differentiable ℂ (starRingEnd ℂ) := by
  intro hdiff
  -- Fix a base point; the argument works at any point.
  set x : ℂ := 0 with hx
  -- (a) The real-linear derivative from `Complex.conjCLE`, transported to
  -- the function `starRingEnd ℂ` via `Complex.conjCLE_apply`.
  have hre : HasFDerivAt (starRingEnd ℂ) (Complex.conjCLE : ℂ →L[ℝ] ℂ) x := by
    have h := (Complex.conjCLE).hasFDerivAt (x := x)
    have hfun : (⇑(Complex.conjCLE) : ℂ → ℂ) = starRingEnd ℂ := funext Complex.conjCLE_apply
    rw [hfun] at h
    exact h
  -- (b) The hypothetical complex-linear derivative at `x`, restricted to ℝ.
  have hcdiff : HasFDerivAt (starRingEnd ℂ)
      (fderiv ℂ (starRingEnd ℂ) x) x := (hdiff x).hasFDerivAt
  set f' : ℂ →L[ℂ] ℂ := fderiv ℂ (starRingEnd ℂ) x with hf'
  have hres : HasFDerivAt (starRingEnd ℂ) (f'.restrictScalars ℝ) x :=
    hcdiff.restrictScalars ℝ
  -- (c) Uniqueness of the Fréchet derivative forces the two ℝ-linear
  -- derivative maps to coincide, hence to agree as functions everywhere.
  have huniq : f'.restrictScalars ℝ = (Complex.conjCLE : ℂ →L[ℝ] ℂ) :=
    hres.unique hre
  have heval : ∀ z : ℂ, f' z = starRingEnd ℂ z := by
    intro z
    have hz := congrArg (fun g : ℂ →L[ℝ] ℂ => g z) huniq
    simpa [Complex.conjCLE_apply] using hz
  -- (d) But `f'` is ℂ-linear, so its value at `I` is forced by its value
  -- at `1`; this contradicts the two values forced by (c).
  have h1 : f' 1 = 1 := by simpa using heval 1
  have hI : f' Complex.I = -Complex.I := by simpa using heval Complex.I
  have hlin : f' Complex.I = Complex.I * f' 1 := by
    have := f'.map_smul Complex.I (1 : ℂ)
    simpa [smul_eq_mul] using this
  rw [h1, hI] at hlin
  apply Complex.I_ne_zero
  have h2 : (2 : ℂ) * Complex.I = 0 := by linear_combination -hlin
  have h2ne : (2 : ℂ) ≠ 0 := two_ne_zero
  exact (mul_eq_zero.mp h2).resolve_left h2ne

#print axioms not_differentiable_starRingEnd

end HG4bConjugationNotHolomorphicProbe

/-
RESULT: CLOSED. `¬ Differentiable ℂ (starRingEnd ℂ)` is proved exactly
as scoped by the Wave-2 HG-4b test: `ContinuousLinearEquiv.hasFDerivAt`
supplies the real-linear derivative fact for `conjCLE`/`starRingEnd ℂ`,
`HasFDerivAt.restrictScalars` and `HasFDerivAt.unique` force any
hypothetical complex-linear derivative to coincide with `conjCLE` as a
function, and ℂ-linearity of that hypothetical derivative then yields a
direct numerical contradiction at `z = 1` and `z = I` (forcing the
derivative's defining scalar to be both `1` and `-1`). This closes the
one honest residual gap named in Wave-1's `HolomorphicTransitionProbe.lean`
regarding non-holomorphic real-smooth maps, though NO attempt is made
here to reconnect the result to that file's `IsHolomorphicTransition`
predicate, and NO claim is made about Lefschetz (1,1), the Hodge
Conjecture, or any Millennium Problem.
-/
