/-
HG-4D -- Closure of `IsHolomorphicTransition` under pointwise
multiplication and inversion (Wave-4 item, Hodge line /
03_MILLENNIUM/05_HODGE)

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (the exact residual gap this item closes):
Wave-1's `HolomorphicTransitionProbe.lean` (this directory) built a
predicate `IsHolomorphicTransition g := MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g`
for line-bundle transition functions, proved the bridge lemma
`isHolomorphicTransition_iff_differentiable : IsHolomorphicTransition g ↔
Differentiable ℂ g`, and showed the predicate is statable and satisfiable
(by `Complex.exp`). Wave-3's `HolomorphicTransitionConjugationBridgeProbe.lean`
(HG-4c, this directory) then showed the predicate correctly REJECTS a
real-smooth-but-not-holomorphic example (complex conjugation). Neither of
those files -- nor any other file in this directory as of Wave-4 -- proves
that the predicate is closed under the two pointwise operations line-bundle
transition functions actually need to compose under cocycle conditions:
multiplication (`g * h`, from composing two trivializations' transition
functions) and inversion (`g⁻¹`, from reversing a trivialization, valid
where `g` is everywhere nonvanishing, as any genuine `Cˣ`-valued transition
function must be). This Wave-4 item (HG-4d) closes exactly that: two short
one-line corollaries, nothing broader.

THE TEST, AND THE RESULT: CLOSED.
This file is a new, standalone file (outside the lakefile package, exactly
like its Wave-1/Wave-3 sources) that inlines, byte-identical, the single
short piece needed from `HolomorphicTransitionProbe.lean`: the
`IsHolomorphicTransition` definition and the
`isHolomorphicTransition_iff_differentiable` bridge lemma, inside the same
namespace `HG4HolomorphicTransitionProbe` used there. It then proves, exactly
as scoped by the Wave-4 plan,
  `isHolomorphicTransition_mul : IsHolomorphicTransition g →
    IsHolomorphicTransition h → IsHolomorphicTransition (g * h)`
via `isHolomorphicTransition_iff_differentiable.mpr
((isHolomorphicTransition_iff_differentiable.mp hg).mul
(isHolomorphicTransition_iff_differentiable.mp hh))`, and
  `isHolomorphicTransition_inv : (∀ x, g x ≠ 0) → IsHolomorphicTransition g →
    IsHolomorphicTransition g⁻¹`
via `isHolomorphicTransition_iff_differentiable.mpr
((isHolomorphicTransition_iff_differentiable.mp hg).inv hz)` -- i.e.
unfold the predicate to `Differentiable ℂ` on both sides of `.mp`/`.mpr`
and compose with the pre-existing Mathlib closure lemmas `Differentiable.mul`
(`Analysis/Calculus/FDeriv/Mul.lean:226`) and `Differentiable.inv`
(`Analysis/Calculus/FDeriv/Mul.lean:779`, which takes the nonvanishing
hypothesis `∀ x, h x ≠ 0` as its second argument, exactly as scoped).

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT modify `HolomorphicTransitionProbe.lean` or
  `HolomorphicTransitionConjugationBridgeProbe.lean`; it inlines a copy of
  the one short relevant piece into this new file instead, exactly as the
  Wave-4 plan specifies.
- Does NOT define or touch any `VectorBundle`/`Bundle`/`HolomorphicLineBundle`
  API, and does NOT attempt the original (broader) HG-4 recon test, nor any
  cocycle-condition bookkeeping for an actual line bundle.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: every lemma used
  (`mdifferentiable_iff_differentiable`, `Differentiable.mul`,
  `Differentiable.inv`) is pre-existing, proved Mathlib content; the only
  thing built here is the composition of an already-closed Wave-1 bridge
  lemma with two pre-existing Mathlib closure facts.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by this
file's own successful compilation):
  - `modelWithCornersSelf`, notation `𝓘(𝕜, E)`
                               Geometry/Manifold/IsManifold/Basic.lean:213
  - `mdifferentiable_iff_differentiable`
                               Geometry/Manifold/MFDeriv/FDeriv.lean
  - `Differentiable.mul (ha : Differentiable 𝕜 a) (hb : Differentiable 𝕜 b) :
    Differentiable 𝕜 (a * b)`
                               Analysis/Calculus/FDeriv/Mul.lean:226
  - `Differentiable.inv (hf : Differentiable 𝕜 h) (hz : ∀ x, h x ≠ 0) :
    Differentiable 𝕜 h⁻¹`
                               Analysis/Calculus/FDeriv/Mul.lean:779
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
   PART 2 -- HG-4d: the two closure corollaries, the actual falsifiable
   test for this item. Nothing beyond these two one-line results is
   attempted.
   ============================================================ -/

namespace HG4dHolomorphicTransitionMulInvClosureProbe

open HG4HolomorphicTransitionProbe

/-- The HG-4d multiplicative closure: if two transition functions `g`, `h`
are holomorphic (in the `IsHolomorphicTransition` sense of HG-4/Wave-1),
so is their pointwise product `g * h`. This is exactly the fact needed to
compose transition functions across two overlapping trivializations. -/
theorem isHolomorphicTransition_mul {g h : ℂ → ℂ}
    (hg : IsHolomorphicTransition g) (hh : IsHolomorphicTransition h) :
    IsHolomorphicTransition (g * h) :=
  isHolomorphicTransition_iff_differentiable.mpr
    ((isHolomorphicTransition_iff_differentiable.mp hg).mul
      (isHolomorphicTransition_iff_differentiable.mp hh))

/-- The HG-4d inverse closure: if a transition function `g` is holomorphic
and everywhere nonvanishing (as any genuine `Cˣ`-valued line-bundle
transition function must be), so is its pointwise inverse `g⁻¹`. This is
exactly the fact needed to reverse a trivialization. -/
theorem isHolomorphicTransition_inv {g : ℂ → ℂ} (hz : ∀ x, g x ≠ 0)
    (hg : IsHolomorphicTransition g) :
    IsHolomorphicTransition g⁻¹ :=
  isHolomorphicTransition_iff_differentiable.mpr
    ((isHolomorphicTransition_iff_differentiable.mp hg).inv hz)

#print axioms isHolomorphicTransition_mul
#print axioms isHolomorphicTransition_inv

end HG4dHolomorphicTransitionMulInvClosureProbe

/-
RESULT: CLOSED. Both `isHolomorphicTransition_mul` and
`isHolomorphicTransition_inv` are proved exactly as scoped by the Wave-4
HG-4d test, by inlining the one short piece named (the
`IsHolomorphicTransition` definition plus its `Differentiable ℂ`-bridge
lemma from HG-4/Wave-1) into one new, standalone file and composing it in
each case with a pre-existing Mathlib closure lemma
(`Differentiable.mul`, `Differentiable.inv`). This closes, for pointwise
multiplication and (nonvanishing-guarded) inversion, the residual gap
neither HG-4 (Wave-1) nor HG-4c (Wave-3) addressed: `IsHolomorphicTransition`
is closed under the two pointwise operations line-bundle transition
functions actually need to compose under cocycle conditions. No attempt is
made here at the general `VectorBundle`/`Bundle` API, at any actual cocycle
condition, or at Lefschetz (1,1), the Hodge Conjecture, or any Millennium
Problem.
-/
