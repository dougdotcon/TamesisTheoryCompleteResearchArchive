/-
  QF-8 -- Norm / inner-product preservation under the Heisenberg flow
  `exp (t • heisenbergGenerator)`, `t : ℝ`. Direct extension of Wave-4
  batch item WAVE4-QF-7 (`HeisenbergFlowUnitarity.lean`, this directory),
  which established `exp (t • heisenbergGenerator) ∈ unitary (Matrix
  (Fin 2) (Fin 2) ℂ)`. Sibling also of WAVE2-QF-5
  (`HeisenbergCommutatorFlowIdentity.lean`) and WAVE3-QF-6
  (`EhrenfestExpectationValueIdentity.lean`), this directory. Wave-5
  batch item WAVE5-QF-8.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-5 task instructions on
  build contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other file in this directory, none of which import each other -- only
  Mathlib. Consistent with that precedent, this file does NOT `import`
  `HeisenbergFlowUnitarity.lean` as a Lean module; instead it re-declares
  the identical `heisenbergGenerator` definition and the QF-7 unitarity
  chain locally (see below), citing their QF-4/QF-7 origin.

  HONESTY NOTE (mandatory, per `../SCOPE.md` in this directory's parent).
  "Quantum-Classical Unification" (QCU-001) is a lab-internal extension,
  informally numbered "Problem 8", added at explicit user request. It is
  **not** one of the seven Clay Millennium Problems, has no official
  recognition, no $1,000,000 prize, and no single agreed formal
  statement. This file makes ZERO claim that any Millennium problem
  (Clay-official or otherwise) is solved, approximated, or reachable,
  and ZERO claim of mathematical novelty: that a unitary operator
  preserves norms and inner products is one of the most standard facts
  in operator theory, assembled here from three existing Mathlib
  lemmas applied at a concrete instance, not a new theorem.

  MOTIVATION / WHAT THIS FILE DOES, exactly as scoped by the Wave-5
  plan. QF-7 proved `exp (t • heisenbergGenerator) ∈ unitary (Matrix
  (Fin 2) (Fin 2) ℂ)` for every `t : ℝ`, a bare algebraic submonoid
  membership fact (`star U * U = 1 ∧ U * star U = 1`), but explicitly
  did NOT connect this to preservation of any inner product / norm of a
  state vector (QF-7's own "WHAT IS STILL MISSING" item (c)). This file
  closes exactly that one gap, via the prescribed 3-step method:
    (a) transport `exp (t • heisenbergGenerator) ∈ unitary (Matrix
        (Fin 2) (Fin 2) ℂ)` (QF-7's result, re-derived locally) along
        the ⋆-algebra equivalence `Matrix.toEuclideanCLM : Matrix n n 𝕜
        ≃⋆ₐ[𝕜] (EuclideanSpace 𝕜 n →L[𝕜] EuclideanSpace 𝕜 n)`
        (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:102`) using
        `Unitary.map_mem` (`Mathlib/Algebra/Star/Unitary.lean:300`),
        giving `Matrix.toEuclideanCLM (exp (t • heisenbergGenerator)) ∈
        unitary (EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ
        (Fin 2))`;
    (b) `ContinuousLinearMap.norm_map_of_mem_unitary`
        (`Mathlib/Analysis/InnerProductSpace/Adjoint.lean:862`), applied
        to (a), gives `‖Matrix.toEuclideanCLM (exp (t •
        heisenbergGenerator)) x‖ = ‖x‖` for every `x : EuclideanSpace ℂ
        (Fin 2)`;
    (c) `ContinuousLinearMap.inner_map_map_of_mem_unitary`
        (`Mathlib/Analysis/InnerProductSpace/Adjoint.lean:868`), applied
        to (a), gives `⟪Matrix.toEuclideanCLM (exp (t •
        heisenbergGenerator)) x, Matrix.toEuclideanCLM (exp (t •
        heisenbergGenerator)) y⟫_ℂ = ⟪x, y⟫_ℂ` for every `x y :
        EuclideanSpace ℂ (Fin 2)`.
  RESULT: all three steps went through with ZERO friction beyond
  re-establishing QF-7's own unitarity chain (which itself needed the
  `Matrix.Norms.L2Operator` norm-scope substitution QF-7 documents in
  full; that substitution is reused here verbatim, not re-derived). No
  new friction point specific to this file's own falsifiable test
  (the `toEuclideanCLM` / `Unitary.map_mem` / `norm_map_of_mem_unitary`
  / `inner_map_map_of_mem_unitary` chain) was encountered:
  `Matrix.toEuclideanCLM` is defined purely algebraically (via
  `LinearMap.toMatrixOrthonormal` and `LinearMap.toContinuousLinearMap`,
  `Mathlib/Analysis/CStarAlgebra/Matrix.lean:102`), with no dependency
  on which scoped norm instance for `Matrix (Fin 2) (Fin 2) ℂ` happens
  to be open, so it composes with the `Matrix.Norms.L2Operator`-scoped
  unitarity fact from QF-7 with no diamond.

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  in addition to compiling cleanly via `lake env lean`):
    - `skewAdjoint.smul_mem`, `exp_mem_unitary_of_mem_skewAdjoint`,
      `NormedAlgebra.restrictScalars`, and the `Matrix.Norms.L2Operator`
      scoped instance chain -- all reused verbatim from QF-7
      (`HeisenbergFlowUnitarity.lean`, this directory; see that file's
      header for the full citation trail of each).
    - `Matrix.toEuclideanCLM`
      (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:102`)
      `Matrix n n 𝕜 ≃⋆ₐ[𝕜] (EuclideanSpace 𝕜 n →L[𝕜] EuclideanSpace 𝕜
      n)`, instantiated at `n := Fin 2`, `𝕜 := ℂ`.
    - `Unitary.map_mem` (`Mathlib/Algebra/Star/Unitary.lean:300`)
      `[FunLike F R S] [StarHomClass F R S] [MonoidHomClass F R S] (f :
      F) {r : R} (hr : r ∈ unitary R) : f r ∈ unitary S`, fed by the
      automatic `RingEquivClass`/`StarHomClass` instances for
      `StarAlgEquiv` (`Mathlib/Algebra/Star/StarAlgHom.lean:650`ff, the
      `NonUnitalAlgEquivClass` chain giving `RingEquivClass` hence
      `MonoidHomClass`, plus the direct `StarHomClass` instance for
      `StarAlgEquiv`), applied to `f := Matrix.toEuclideanCLM`.
    - `ContinuousLinearMap.norm_map_of_mem_unitary`,
      `ContinuousLinearMap.inner_map_map_of_mem_unitary`
      (`Mathlib/Analysis/InnerProductSpace/Adjoint.lean:862,868`)
      `{u : H →L[𝕜] H} (hu : u ∈ unitary (H →L[𝕜] H)) (x : H) : ‖u x‖ =
      ‖x‖`, resp. `(x y : H) : ⟪u x, u y⟫_𝕜 = ⟪x, y⟫_𝕜`, instantiated at
      `H := EuclideanSpace ℂ (Fin 2)`, `𝕜 := ℂ` (a finite-dimensional,
      hence complete, inner product space, so `[CompleteSpace H]`
      resolves automatically).

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST, exactly as specified.
  Fix the same `2 × 2` skew-Hermitian generator `heisenbergGenerator =
  diag(i, -i)` as QF-4/QF-5/QF-6/QF-7. Re-derive QF-7's `exp (t •
  heisenbergGenerator) ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ)` for every
  `t : ℝ`, then prove that the associated continuous linear map on
  `EuclideanSpace ℂ (Fin 2)` obtained via `Matrix.toEuclideanCLM`
  preserves both the norm and the inner product of every vector, via
  exactly the three-step method prescribed: `Matrix.toEuclideanCLM` +
  `Unitary.map_mem`, then `norm_map_of_mem_unitary` /
  `inner_map_map_of_mem_unitary`, reusing QF-7's unitarity proof.

  WHAT IS STILL MISSING even on full success of this file (stated
  honestly, per the Wave-5 instructions, mirroring QF-4/QF-5/QF-6/QF-7's
  own honesty sections). This file proves ONLY that norm and inner
  product on the finite-dimensional coordinate space `EuclideanSpace ℂ
  (Fin 2)` are preserved by the linear-map incarnation of the fixed toy
  generator's flow, at every real time `t`. It does **not**: (a) prove
  any Ehrenfest theorem, Schrödinger/Heisenberg equation of motion, or
  correspondence-principle statement -- those are the separate concerns
  of QF-5/QF-6 in this same directory; (b) extend to `t : ℂ` (shown
  false in general in QF-7's header) or to any unbounded/physical
  position-momentum generator (per QF-2/QF-3 in this same directory,
  this bounded/finite-dimensional setting cannot even realize the
  canonical commutation relation, so `heisenbergGenerator` is explicitly
  NOT a physical Hamiltonian, and `EuclideanSpace ℂ (Fin 2)` is
  explicitly NOT a physical quantum state space); (c) connect to any
  `ħ → 0` classical limit or any physical interpretation of norm/inner-
  product preservation beyond the bare linear-algebraic fact; (d) prove
  anything about the identification `Matrix.toEuclideanCLM` beyond
  reusing it off-the-shelf -- no new algebraic or analytic infrastructure
  is built in this file, only an existing equivalence and two existing
  general lemmas are composed at one concrete instance.
-/
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.Star.Module
import Mathlib.Analysis.RCLike.Basic

open scoped Matrix.Norms.L2Operator
open scoped InnerProductSpace
open NormedSpace

namespace QF8.HeisenbergFlowNormPreservation

/-- The fixed generator for this probe, identical to QF-4's/QF-5's/
QF-6's/QF-7's `heisenbergGenerator`: `H = diag(i, -i)`, a concrete
`2 × 2` skew-Hermitian complex matrix. Re-declared locally rather than
imported, per this directory's established free-standing-file
precedent (see the header note above). Playing the role of a toy
"Hamiltonian-like" generator for the purposes of this single-identity
feasibility test; NOT claimed to be a physical Hamiltonian (real
position/momentum generators are unbounded, per QF-2/QF-3 in this same
directory). -/
noncomputable def heisenbergGenerator : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.I, 0; 0, -Complex.I]

/-- **Skew-adjoint membership**, identical to QF-7's
`heisenbergGenerator_mem_skewAdjoint`: `heisenbergGenerator ∈
skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ)`, i.e. `star heisenbergGenerator
= -heisenbergGenerator`, proved by the same concrete entrywise
computation QF-4/QF-7 use. -/
theorem heisenbergGenerator_mem_skewAdjoint :
    heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ) := by
  rw [skewAdjoint.mem_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [heisenbergGenerator, Matrix.conjTranspose_apply]

/-- **Scalar skew-adjointness**, identical to QF-7's
`smul_heisenbergGenerator_mem_skewAdjoint`: `t • heisenbergGenerator ∈
skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ)` for every `t : ℝ`, via
`skewAdjoint.smul_mem`. See QF-7's header for the full instance-chain
citation (`TrivialStar ℝ`, `StarModule ℝ (Matrix (Fin 2) (Fin 2) ℂ)`). -/
theorem smul_heisenbergGenerator_mem_skewAdjoint (t : ℝ) :
    t • heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ) :=
  skewAdjoint.smul_mem t heisenbergGenerator_mem_skewAdjoint

/-- **QF-7's unitarity result, re-derived locally.** The Heisenberg flow
`exp (t • heisenbergGenerator)` is unitary in `Matrix (Fin 2) (Fin 2)
ℂ` for every real time `t : ℝ`. Identical statement and proof to QF-7's
`exp_heisenbergFlow_mem_unitary` (`HeisenbergFlowUnitarity.lean`, this
directory); see that file's header for the full friction-point report
on why the `Matrix.Norms.L2Operator` scope (rather than
`Matrix.Norms.Operator`) is needed here. This file's own new content
begins at `toEuclideanCLM_exp_heisenbergFlow_mem_unitary` below. -/
theorem exp_heisenbergFlow_mem_unitary (t : ℝ) :
    exp (t • heisenbergGenerator) ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ) :=
  haveI : NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2) ℂ) :=
    NormedAlgebra.restrictScalars ℚ ℂ (Matrix (Fin 2) (Fin 2) ℂ)
  exp_mem_unitary_of_mem_skewAdjoint (smul_heisenbergGenerator_mem_skewAdjoint t)

/-- **Falsifiable-test step (a), the new content of this file.**
Transporting QF-7's unitarity fact along the ⋆-algebra equivalence
`Matrix.toEuclideanCLM` via `Unitary.map_mem`: the continuous linear
endomorphism of `EuclideanSpace ℂ (Fin 2)` induced by `exp (t •
heisenbergGenerator)` is unitary in `EuclideanSpace ℂ (Fin 2) →L[ℂ]
EuclideanSpace ℂ (Fin 2)`, for every `t : ℝ`. -/
theorem toEuclideanCLM_exp_heisenbergFlow_mem_unitary (t : ℝ) :
    Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ) (exp (t • heisenbergGenerator)) ∈
      unitary (EuclideanSpace ℂ (Fin 2) →L[ℂ] EuclideanSpace ℂ (Fin 2)) :=
  Unitary.map_mem (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ))
    (exp_heisenbergFlow_mem_unitary t)

/-- **Main result (QF-8), falsifiable-test step (b): norm
preservation.** The Heisenberg flow `exp (t • heisenbergGenerator)`,
viewed as a continuous linear map on `EuclideanSpace ℂ (Fin 2)` via
`Matrix.toEuclideanCLM`, preserves the norm of every vector, at every
real time `t : ℝ`. Direct application of
`ContinuousLinearMap.norm_map_of_mem_unitary` to the unitarity fact
above. -/
theorem norm_toEuclideanCLM_exp_heisenbergFlow (t : ℝ)
    (x : EuclideanSpace ℂ (Fin 2)) :
    ‖Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ) (exp (t • heisenbergGenerator)) x‖ = ‖x‖ :=
  ContinuousLinearMap.norm_map_of_mem_unitary
    (toEuclideanCLM_exp_heisenbergFlow_mem_unitary t) x

/-- **Main result (QF-8), falsifiable-test step (c): inner-product
preservation.** The Heisenberg flow `exp (t • heisenbergGenerator)`,
viewed as a continuous linear map on `EuclideanSpace ℂ (Fin 2)` via
`Matrix.toEuclideanCLM`, preserves the inner product of every pair of
vectors, at every real time `t : ℝ`. Direct application of
`ContinuousLinearMap.inner_map_map_of_mem_unitary` to the unitarity
fact above. -/
theorem inner_toEuclideanCLM_exp_heisenbergFlow (t : ℝ)
    (x y : EuclideanSpace ℂ (Fin 2)) :
    ⟪Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ) (exp (t • heisenbergGenerator)) x,
        Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℂ) (exp (t • heisenbergGenerator)) y⟫_ℂ =
      ⟪x, y⟫_ℂ :=
  ContinuousLinearMap.inner_map_map_of_mem_unitary
    (toEuclideanCLM_exp_heisenbergFlow_mem_unitary t) x y

end QF8.HeisenbergFlowNormPreservation

#print axioms QF8.HeisenbergFlowNormPreservation.heisenbergGenerator_mem_skewAdjoint
#print axioms QF8.HeisenbergFlowNormPreservation.smul_heisenbergGenerator_mem_skewAdjoint
#print axioms QF8.HeisenbergFlowNormPreservation.exp_heisenbergFlow_mem_unitary
#print axioms QF8.HeisenbergFlowNormPreservation.toEuclideanCLM_exp_heisenbergFlow_mem_unitary
#print axioms QF8.HeisenbergFlowNormPreservation.norm_toEuclideanCLM_exp_heisenbergFlow
#print axioms QF8.HeisenbergFlowNormPreservation.inner_toEuclideanCLM_exp_heisenbergFlow
