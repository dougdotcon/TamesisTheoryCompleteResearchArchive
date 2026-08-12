/-
  QF-13 -- Does the Heisenberg flow `MonoidHom` from QF-10
  (`heisenbergFlowHom : Multiplicative ℝ →* unitary (Matrix (Fin 2) (Fin 2)
  ℂ)`) transport, POINTWISE, along `Matrix.toEuclideanCLM` (the
  `StarAlgEquiv` between `Matrix n n 𝕜` and continuous linear
  endomorphisms of `EuclideanSpace 𝕜 n`) into a bundled `MonoidHom` into
  `unitary (EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2))`, via
  `MonoidHom.mk'` fed by `unitary.map_mem`? Direct extension of Wave-6
  batch item WAVE6-QF-10 (`HeisenbergFlowMonoidHom.lean`, this directory,
  `heisenbergFlowHom`) and Wave-6 batch item WAVE6-QF-11
  (`HeisenbergFlowContinuitySmulProbe.lean`, this directory, confirming
  `NormedSpace.complexToReal`/`ContinuousSMul` friction-free under
  `Matrix.Norms.L2Operator`, not directly reused here but read as
  required context). Wave-7 batch item WAVE7-QF-13.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-7 task instructions on
  build contention with 13 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other file in this directory, none of which import each other -- only
  Mathlib. Consistent with that precedent, this file does NOT `import`
  `HeisenbergFlowMonoidHom.lean` as a Lean module; instead it re-declares
  the identical `heisenbergGenerator` definition and re-derives the
  skew-adjointness, unitarity, addition-law, and `heisenbergFlowHom`
  facts locally, VERBATIM from QF-10 (see below), citing their QF-10
  origin. This reproduced block is BOILERPLATE, excluded from this
  item's 60-line new-content ceiling (see the line-count note at the
  bottom of this header).

  HONESTY NOTE (mandatory, per `../SCOPE.md` in this directory's parent).
  "Quantum-Classical Unification" (QCU-001) is a lab-internal extension,
  informally numbered "Problem 8", added at explicit user request. It is
  **not** one of the seven Clay Millennium Problems, has no official
  recognition, no $1,000,000 prize, and no single agreed formal
  statement. This file makes ZERO claim that any Millennium problem
  (Clay-official or otherwise) is solved, approximated, or reachable,
  and ZERO claim of mathematical novelty: that a `StarAlgEquiv` between
  two star-rings carries a bundled `MonoidHom` in the ambient monoid
  along to a bundled `MonoidHom` between the two associated `unitary`
  subgroups is a completely generic, purely categorical fact (any
  `⋆`-ring homomorphism restricts to unitary subgroups), assembled here
  PURELY by re-packaging QF-10's already-closed `heisenbergFlowHom`
  through Mathlib's generic `unitary.map_mem` lemma -- no new
  mathematical content beyond that transport step, applied to this one
  concrete `2 × 2` matrix / `EuclideanSpace (Fin 2)` pair.

  MOTIVATION / WHAT THIS FILE DOES, exactly as scoped by the Wave-7 plan
  and this item's falsifiable-test description. QF-10 proved
  `heisenbergFlowHom : Multiplicative ℝ →* unitary (Matrix (Fin 2) (Fin
  2) ℂ)`. The falsifiable test asked EXACTLY this, and nothing broader:
  construct `heisenbergFlowEuclideanHom` via `MonoidHom.mk'` applied to
  `fun t => ⟨toEuclideanCLM (heisenbergFlowHom t), unitary.map_mem
  toEuclideanCLM (heisenbergFlowHom t).2⟩` -- the POINTWISE route,
  explicitly NOT the packaged-composition route `unitary.map
  toEuclideanCLM.toStarMonoidHom`, which the test description itself
  flags as unavailable (`StarAlgEquiv` has no `toStarMonoidHom`
  projection to feed `unitary.map`, which wants a bundled `R →⋆* S`).

  RESULT: the pointwise route closes with ZERO friction. `unitary.map_mem`
  (`Mathlib/Algebra/Star/Unitary.lean:300`) has signature `{F : Type*}
  [FunLike F R S] [StarHomClass F R S] [MonoidHomClass F R S] (f : F)
  {r : R} (hr : r ∈ unitary R) : f r ∈ unitary S`, and `Matrix.toEuclideanCLM
  : Matrix n n 𝕜 ≃⋆ₐ[𝕜] (EuclideanSpace 𝕜 n →L[𝕜] EuclideanSpace 𝕜 n)`
  (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:102`) supplies every
  instance `unitary.map_mem` asks for at `F := Matrix n n 𝕜 ≃⋆ₐ[𝕜] (...)`
  via the generic `StarAlgEquiv` instance chain: `NonUnitalAlgEquivClass`
  gives `RingEquivClass`, which gives `RingHomClass`, which EXTENDS
  `MonoidHomClass` (`Mathlib/Algebra/Ring/Hom/Defs.lean:326`); and
  `StarRingEquivClass` (the `StarAlgEquiv` instance at
  `Mathlib/Algebra/Star/StarAlgHom.lean:709`) gives `StarHomClass`
  (`Mathlib/Algebra/Star/StarRingHom.lean:262`). Crucially,
  `Matrix.toEuclideanCLM` itself is declared as a plain (non-`scoped`)
  `def` inside `namespace Matrix` -- unlike the `Matrix.Norms.L2Operator`-
  scoped `NormedRing`/`NormedAlgebra` instances QF-7/.../QF-11 each had
  to hand-manage, `toEuclideanCLM`'s underlying `Ring`/`Star` structure
  on `Matrix n n 𝕜` is the bare algebraic one, present unconditionally,
  with no diamond risk and no scope-opening needed for THIS file's own
  new content (the scope is still opened once, for reproducing QF-10's
  `heisenbergFlowHom` boilerplate, which does need it).

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  in addition to compiling cleanly via `lake env lean`):
    - `Matrix.toEuclideanCLM` (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:102`),
      `unitary.map_mem` (`Mathlib/Algebra/Star/Unitary.lean:300`),
      `RingEquivClass.toRingHomClass` (`Mathlib/Algebra/Ring/Equiv.lean:99`),
      `RingHomClass extends MonoidHomClass`
      (`Mathlib/Algebra/Ring/Hom/Defs.lean:326`),
      `StarRingEquivClass.instStarHomClass`
      (`Mathlib/Algebra/Star/StarRingHom.lean:262`) -- the full instance
      chain making the pointwise construction typecheck.
    - `Submonoid.coe_mul`, `Subtype.ext`, `map_mul` (generic
      `MulHomClass`/`MonoidHomClass` accessor) -- used in the `map_mul'`
      field to transport QF-10's own `heisenbergFlowHom.map_mul` fact
      through the coercion and then through `toEuclideanCLM`.
    - `MonoidHom.mk'` (`Mathlib/Algebra/Group/Hom/Defs.lean:589`), the
      same constructor QF-10 itself used, reused here at
      `M := Multiplicative ℝ`, `G := unitary (EuclideanSpace ℂ (Fin 2)
      →L[ℂ] EuclideanSpace ℂ (Fin 2))`.
    - QF-10's own boilerplate chain (`heisenbergGenerator`,
      `heisenbergGenerator_mem_skewAdjoint`,
      `smul_heisenbergGenerator_mem_skewAdjoint`,
      `exp_heisenbergFlow_mem_unitary`, `heisenbergFlow_add`,
      `heisenbergFlowHom`), reproduced verbatim -- see
      `HeisenbergFlowMonoidHom.lean`, this directory, for the full
      citation trail of each.

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST, exactly as specified.
  Reproduce QF-10's `heisenbergFlowHom : Multiplicative ℝ →* unitary
  (Matrix (Fin 2) (Fin 2) ℂ)` (boilerplate). Construct
  `heisenbergFlowEuclideanHom : Multiplicative ℝ →* unitary (EuclideanSpace
  ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2))` via `MonoidHom.mk'`, with
  `toFun := fun t => ⟨toEuclideanCLM (heisenbergFlowHom t), unitary.map_mem
  toEuclideanCLM (heisenbergFlowHom t).2⟩` -- the exact pointwise
  expression named by the falsifiable test -- and `map_mul'` closed by
  transporting `heisenbergFlowHom`'s own `map_mul` fact through
  `Submonoid.coe_mul` and `toEuclideanCLM`'s `map_mul`. This closes; the
  composition route (`unitary.map toEuclideanCLM.toStarMonoidHom`) was
  NOT attempted, per the falisfiable test's own explicit instruction to
  report BLOCKED on pointwise failure rather than trying it -- moot here
  since the pointwise route succeeded.

  WHAT IS STILL MISSING even on full success of this file (stated
  honestly, per the Wave-7 instructions, mirroring QF-10/QF-11's own
  honesty sections). This file proves ONLY that QF-10's
  `heisenbergFlowHom` transports pointwise into a bundled `MonoidHom`
  targeting `unitary (EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ
  (Fin 2))`. It does **not**: (a) prove any continuity of
  `heisenbergFlowEuclideanHom` or upgrade it to a `ContinuousMonoidHom` --
  a strictly separate concern from QF-11's own (different) continuity
  probe, not attempted here; (b) prove injectivity/surjectivity of
  `toEuclideanCLM`'s restriction to unitary subgroups, or any structural
  property of `heisenbergFlowEuclideanHom` beyond well-definedness as a
  group homomorphism; (c) prove any Ehrenfest theorem, Schrödinger/
  Heisenberg equation of motion, or correspondence-principle statement --
  those remain the separate concerns of QF-5/QF-6 in this same
  directory; (d) extend to `t : ℂ` or any unbounded/physical position-
  momentum generator (per QF-2/QF-3 in this same directory,
  `heisenbergGenerator` is explicitly NOT a physical Hamiltonian); (e)
  connect to any `ħ → 0` classical limit or any physical interpretation
  beyond the bare algebraic transport checked.

  LINE-COUNT DISCIPLINE (mandatory, per DEC-103 / the WAVE6-BSD-7
  lesson). Ceiling: 60 new non-comment lines. The block reproducing
  QF-10's `heisenbergGenerator` through `heisenbergFlowHom` (identical
  declarations, identical proofs, cited above) is BOILERPLATE reused
  verbatim from a prior-wave file and is EXCLUDED from the count, per
  the task instructions. Only the new declarations below
  `heisenbergFlowHom` (this file's own `heisenbergFlowEuclideanHom` and
  its sanity-check corollary) count toward the 60-line ceiling; the
  exact measured count is reported in this item's final report, not
  estimated here.
-/
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.Star.Module
import Mathlib.Analysis.RCLike.Basic
import Mathlib.Algebra.Star.Unitary
import Mathlib.Algebra.Group.TypeTags.Basic

open scoped Matrix.Norms.L2Operator
open NormedSpace

namespace QF13.HeisenbergFlowEuclideanCLMHom

-- === BEGIN boilerplate, reproduced verbatim from QF-10
-- (`HeisenbergFlowMonoidHom.lean`, this directory); excluded from this
-- item's 60-line new-content ceiling, see header note above. ===

/-- The fixed generator for this probe, identical to QF-4's/.../QF-10's
`heisenbergGenerator`: `H = diag(i, -i)`, a concrete `2 × 2`
skew-Hermitian complex matrix. Re-declared locally rather than imported,
per this directory's established free-standing-file precedent (see the
header note above). Playing the role of a toy "Hamiltonian-like"
generator for the purposes of this single-identity feasibility test; NOT
claimed to be a physical Hamiltonian (real position/momentum generators
are unbounded, per QF-2 / QF-3 in this same directory). -/
noncomputable def heisenbergGenerator : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.I, 0; 0, -Complex.I]

/-- **Skew-adjoint membership**, identical to QF-7's/.../QF-10's
`heisenbergGenerator_mem_skewAdjoint`. -/
theorem heisenbergGenerator_mem_skewAdjoint :
    heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ) := by
  rw [skewAdjoint.mem_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [heisenbergGenerator, Matrix.conjTranspose_apply]

/-- **Scalar skew-adjointness**, identical to QF-7's/.../QF-10's
`smul_heisenbergGenerator_mem_skewAdjoint`. -/
theorem smul_heisenbergGenerator_mem_skewAdjoint (t : ℝ) :
    t • heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ) :=
  skewAdjoint.smul_mem t heisenbergGenerator_mem_skewAdjoint

/-- **QF-7's unitarity result, re-derived locally**, identical to QF-10's
`exp_heisenbergFlow_mem_unitary`. -/
theorem exp_heisenbergFlow_mem_unitary (t : ℝ) :
    exp (t • heisenbergGenerator) ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ) :=
  haveI : NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2) ℂ) :=
    NormedAlgebra.restrictScalars ℚ ℂ (Matrix (Fin 2) (Fin 2) ℂ)
  exp_mem_unitary_of_mem_skewAdjoint (smul_heisenbergGenerator_mem_skewAdjoint t)

/-- **QF-9's addition law, re-derived locally**, identical to QF-10's
`heisenbergFlow_add`. -/
theorem heisenbergFlow_add (s t : ℝ) :
    exp ((s + t) • heisenbergGenerator) =
      exp (s • heisenbergGenerator) * exp (t • heisenbergGenerator) := by
  haveI : NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2) ℂ) :=
    NormedAlgebra.restrictScalars ℚ ℂ (Matrix (Fin 2) (Fin 2) ℂ)
  rw [add_smul]
  exact exp_add_of_commute
    (((Commute.refl heisenbergGenerator).smul_right t).smul_left s)

/-- **QF-10's bundled `MonoidHom`**, identical to QF-10's
`heisenbergFlowHom`, reproduced verbatim as the input this file's own
new content (below) transports through `Matrix.toEuclideanCLM`. -/
noncomputable def heisenbergFlowHom :
    Multiplicative ℝ →* unitary (Matrix (Fin 2) (Fin 2) ℂ) :=
  MonoidHom.mk'
    (fun t => ⟨exp (t.toAdd • heisenbergGenerator),
      exp_heisenbergFlow_mem_unitary t.toAdd⟩)
    (fun a b => by
      apply Subtype.ext
      show exp ((a * b).toAdd • heisenbergGenerator) =
          exp (a.toAdd • heisenbergGenerator) * exp (b.toAdd • heisenbergGenerator)
      rw [toAdd_mul]
      exact heisenbergFlow_add a.toAdd b.toAdd)

-- === END boilerplate reproduced from QF-10. Everything below this line
-- is this item's own new content, subject to the 60-line ceiling. ===

/-- **Main result (QF-13), the falsifiable test exactly as specified,
via the POINTWISE route (NOT the unavailable `unitary.map
toEuclideanCLM.toStarMonoidHom` composition route, per the test's own
explicit instruction).** QF-10's `heisenbergFlowHom`, transported
pointwise along `Matrix.toEuclideanCLM`, assembles into a bundled
`MonoidHom` into `unitary (EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace
ℂ (Fin 2))`, via `MonoidHom.mk'` fed by `unitary.map_mem` (for
`toFun`) and `heisenbergFlowHom.map_mul` transported through
`Submonoid.coe_mul` and `toEuclideanCLM`'s own `map_mul` (for
`map_mul'`). See the file header's "RESULT" section for the full
instance-chain reasoning on why `unitary.map_mem` applies directly to
`Matrix.toEuclideanCLM` with zero friction. -/
noncomputable def heisenbergFlowEuclideanHom :
    Multiplicative ℝ →*
      unitary (EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2)) :=
  MonoidHom.mk'
    (fun t => ⟨(Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ)) (heisenbergFlowHom t),
      Unitary.map_mem (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ)) (heisenbergFlowHom t).2⟩)
    (fun a b => by
      apply Subtype.ext
      show (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ))
            (heisenbergFlowHom (a * b) : Matrix (Fin 2) (Fin 2) ℂ) =
          (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ))
              (heisenbergFlowHom a : Matrix (Fin 2) (Fin 2) ℂ) *
            (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ))
              (heisenbergFlowHom b : Matrix (Fin 2) (Fin 2) ℂ)
      rw [congrArg Subtype.val (map_mul heisenbergFlowHom a b), Submonoid.coe_mul,
        map_mul])

/-- **Sanity-check corollary**, immediate from `heisenbergFlowEuclideanHom`'s
bundled `MonoidHom` structure: its underlying continuous linear map at
`Multiplicative.ofAdd t` is exactly `toEuclideanCLM` applied to the
QF-10 flow value, confirming the transport did not silently change the
underlying object. Not part of the falsifiable test itself; included
only as an explicit unfolding check. -/
theorem coe_heisenbergFlowEuclideanHom_apply (t : ℝ) :
    (heisenbergFlowEuclideanHom (Multiplicative.ofAdd t) :
        EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2)) =
      (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ))
        (heisenbergFlowHom (Multiplicative.ofAdd t)) := rfl

end QF13.HeisenbergFlowEuclideanCLMHom

#print axioms QF13.HeisenbergFlowEuclideanCLMHom.heisenbergGenerator_mem_skewAdjoint
#print axioms QF13.HeisenbergFlowEuclideanCLMHom.smul_heisenbergGenerator_mem_skewAdjoint
#print axioms QF13.HeisenbergFlowEuclideanCLMHom.exp_heisenbergFlow_mem_unitary
#print axioms QF13.HeisenbergFlowEuclideanCLMHom.heisenbergFlow_add
#print axioms QF13.HeisenbergFlowEuclideanCLMHom.heisenbergFlowHom
#print axioms QF13.HeisenbergFlowEuclideanCLMHom.heisenbergFlowEuclideanHom
#print axioms QF13.HeisenbergFlowEuclideanCLMHom.coe_heisenbergFlowEuclideanHom_apply
