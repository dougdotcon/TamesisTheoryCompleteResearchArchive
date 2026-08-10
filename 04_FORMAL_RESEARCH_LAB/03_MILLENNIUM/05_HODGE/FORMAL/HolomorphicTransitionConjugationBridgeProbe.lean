/-
HG-4C -- Reconnect `not_differentiable_starRingEnd` (HG-4b, Wave-2) to the
`IsHolomorphicTransition` predicate (HG-4, Wave-1) (Wave-3 item, Hodge
line / 03_MILLENNIUM/05_HODGE)

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (the exact residual gap this item closes):
Wave-1's `HolomorphicTransitionProbe.lean` (this directory) built a
predicate `IsHolomorphicTransition g := MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g`
for line-bundle transition functions, proved
`isHolomorphicTransition_iff_differentiable : IsHolomorphicTransition g ↔
Differentiable ℂ g`, and showed the predicate is statable and satisfiable
(by `Complex.exp`), but explicitly left open whether the predicate
correctly REJECTS a genuine real-smooth-but-not-holomorphic example, e.g.
complex conjugation. Wave-2's `ConjugationNotHolomorphicProbe.lean` (this
directory) then closed exactly that missing ingredient in isolation:
`not_differentiable_starRingEnd : ¬ Differentiable ℂ (starRingEnd ℂ)`,
but that file's own header says explicitly it does "NOT reconnect this
result to `IsHolomorphicTransition`... and does NOT modify that file."
This Wave-3 item (HG-4c) is exactly that one-line reconnection, attempted
as its own narrow, self-contained, falsifiable claim -- nothing broader.

THE TEST, AND THE RESULT: CLOSED.
This file is a new, standalone file (outside the lakefile package, exactly
like its two Wave-1/Wave-2 sources) that inlines, byte-identical, the two
short pieces needed:
  (1) from `HolomorphicTransitionProbe.lean`: the `IsHolomorphicTransition`
      definition and the `isHolomorphicTransition_iff_differentiable`
      bridge lemma, inside the same namespace
      `HG4HolomorphicTransitionProbe` used there;
  (2) from `ConjugationNotHolomorphicProbe.lean`: the full
      `not_differentiable_starRingEnd` theorem, inside the same namespace
      `HG4bConjugationNotHolomorphicProbe` used there.
It then proves, exactly as scoped by the Wave-3 plan,
  `¬ HG4HolomorphicTransitionProbe.IsHolomorphicTransition (starRingEnd ℂ)`
via `isHolomorphicTransition_iff_differentiable.not.mpr
not_differentiable_starRingEnd` -- i.e. contrapose the iff bridge lemma
against the already-proved non-differentiability fact. `Iff.not : (a ↔ b)
→ (¬a ↔ ¬b)` is a pre-existing Mathlib alias for `not_congr`
(`Mathlib/Logic/Basic.lean:278`, confirmed to exist by grep against the
vendored snapshot and by this file's own successful compilation), so
`.not.mpr` turns the forward direction of the iff into exactly the
"reject conjugation" direction needed here.

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT modify `HolomorphicTransitionProbe.lean` or
  `ConjugationNotHolomorphicProbe.lean`; it inlines copies of their short
  relevant pieces into this new file instead, exactly as the Wave-3 plan
  specifies.
- Does NOT define or touch any `VectorBundle`/`Bundle`/`HolomorphicLineBundle`
  API, and does NOT attempt the original (broader) HG-4 recon test.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: every lemma used
  (`mdifferentiable_iff_differentiable`, `Complex.conjCLE`,
  `ContinuousLinearEquiv.hasFDerivAt`, `HasFDerivAt.restrictScalars`,
  `HasFDerivAt.unique`, `Iff.not`/`not_congr`) is pre-existing, proved
  Mathlib content; the only thing built here is the composition of two
  already-closed Wave-1/Wave-2 results into one reconnecting corollary.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by this
file's own successful compilation):
  - `modelWithCornersSelf`, notation `𝓘(𝕜, E)`
                               Geometry/Manifold/IsManifold/Basic.lean:213
  - `mdifferentiable_iff_differentiable`
                               Geometry/Manifold/MFDeriv/FDeriv.lean
  - `Complex.conjCLE : ℂ ≃L[ℝ] ℂ`, `Complex.conjCLE_apply`
                               Analysis/Complex/Basic.lean:256, :~264ff
  - `ContinuousLinearEquiv.hasFDerivAt`
                               Analysis/Calculus/FDeriv/Equiv.lean:56
  - `HasFDerivAt.restrictScalars`
                               Analysis/Calculus/FDeriv/RestrictScalars.lean:56
  - `HasFDerivAt.unique`
                               Analysis/Calculus/FDeriv/Basic.lean:174
  - `starRingEnd`, notation `conj` in scope `ComplexConjugate`
                               Data/Complex/Basic.lean:458
  - `Iff.not` (alias for `not_congr`)
                               Logic/Basic.lean:278
-/

import Mathlib

/- ============================================================
   PART 1 -- inlined verbatim from `HolomorphicTransitionProbe.lean`
   (HG-4, Wave-1): only the definition and bridge lemma needed below.
   ============================================================ -/

namespace HG4HolomorphicTransitionProbe

open scoped Manifold

/-- The candidate predicate: "the transition function `g` of a rank-1
trivial bundle over `M := ℂ` (single-chart model `𝓘(ℂ, ℂ)`) is
holomorphic," stated purely in terms of Mathlib's pre-existing manifold
complex-differentiability machinery. This is the statability question
the narrowed HG-4 test asks: does this even type-check at all? -/
def IsHolomorphicTransition (g : ℂ → ℂ) : Prop :=
  MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g

/-- The predicate unfolds, with zero extra infrastructure, to Mathlib's
standard complex-differentiability -- confirming this is genuinely the
COMPLEX notion (parametrized by the field `𝕜 = ℂ`), not a disguised
real-smoothness predicate. -/
theorem isHolomorphicTransition_iff_differentiable {g : ℂ → ℂ} :
    IsHolomorphicTransition g ↔ Differentiable ℂ g := by
  unfold IsHolomorphicTransition
  exact mdifferentiable_iff_differentiable

end HG4HolomorphicTransitionProbe

/- ============================================================
   PART 2 -- inlined verbatim from `ConjugationNotHolomorphicProbe.lean`
   (HG-4b, Wave-2): the full non-differentiability theorem.
   ============================================================ -/

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

end HG4bConjugationNotHolomorphicProbe

/- ============================================================
   PART 3 -- HG-4c: the reconnection, the actual falsifiable test for
   this item. Nothing beyond this one corollary is attempted.
   ============================================================ -/

namespace HG4cTransitionConjugationBridgeProbe

open HG4HolomorphicTransitionProbe
open HG4bConjugationNotHolomorphicProbe

/-- The HG-4c reconnection: complex conjugation is a real-smooth-but-not-
holomorphic example that the `IsHolomorphicTransition` predicate from
HG-4 (Wave-1) correctly REJECTS, via the HG-4b (Wave-2)
non-differentiability fact composed with the HG-4 bridge lemma. This
closes the residual gap explicitly left open by both source files. -/
theorem not_isHolomorphicTransition_starRingEnd :
    ¬ HG4HolomorphicTransitionProbe.IsHolomorphicTransition (starRingEnd ℂ) :=
  isHolomorphicTransition_iff_differentiable.not.mpr not_differentiable_starRingEnd

#print axioms not_isHolomorphicTransition_starRingEnd

end HG4cTransitionConjugationBridgeProbe

/-
RESULT: CLOSED. `¬ HG4HolomorphicTransitionProbe.IsHolomorphicTransition
(starRingEnd ℂ)` is proved exactly as scoped by the Wave-3 HG-4c test, by
inlining the two short pieces named (the `IsHolomorphicTransition`
definition plus its `Differentiable ℂ`-bridge lemma from HG-4/Wave-1, and
the full `not_differentiable_starRingEnd` non-differentiability theorem
from HG-4b/Wave-2) into one new, standalone file and composing them with
`Iff.not.mpr` (`not_congr`, pre-existing Mathlib content). This closes,
concretely and for this one specific example, the residual gap both
source files explicitly left open: `IsHolomorphicTransition` is not only
statable and satisfiable (HG-4's `Complex.exp` witness) but also
genuinely discriminating -- it rejects a real-smooth, non-holomorphic
transition function, complex conjugation. No attempt is made here at the
general `VectorBundle`/`Bundle` API, and no claim is made about Lefschetz
(1,1), the Hodge Conjecture, or any Millennium Problem.
-/
