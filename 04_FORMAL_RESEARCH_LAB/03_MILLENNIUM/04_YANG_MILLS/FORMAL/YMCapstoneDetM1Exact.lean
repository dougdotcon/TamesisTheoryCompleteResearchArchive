/-
  YM-CAPSTONE-DET-M1-EXACT — exact value `det(toEuclideanCLM M1) = 3.2`
  (Wave-7 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-7 task instructions on
  build contention with 13 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1..Wave-6 file in this directory. This file does NOT modify
  any other file; it declares its own minimal `E` and `M1` (matching the
  values used throughout the `YMCapstoneBracket.lean` /
  `YMCapstoneDetBracketTightened.lean` / `YMCapstoneTraceM1Exact.lean`
  lineage) and proves a single new fact directly from Mathlib primitives.

  EXACT TASK ATTEMPTED (per the Wave-7 work-item prompt for
  `WAVE7-YM-CAPSTONE-DET-M1-EXACT`, candidate `YM-CAPSTONE-DET-M1-EXACT`).
  Nothing broader than this was attempted: prove
  `det_toEuclideanCLM_M1_eq_three_point_two` via
  `Matrix.coe_toEuclideanCLM_eq_toEuclideanLin` →
  `Matrix.toEuclideanLin_eq_toLin_orthonormal` → `LinearMap.det_toLin`
  (the plan's "`Matrix.det_toLin`" — direct grep of the vendored
  Mathlib snapshot confirms the lemma actually lives in the `LinearMap`
  namespace, not `Matrix`; same statement, correct fully-qualified
  name used below) → `Matrix.det_fin_two` + `norm_num`, exactly as the
  plan specified.

  WHY THIS IS A NEW, DIRECT INGREDIENT (not previously proved in this
  lineage). `YMCapstoneDetBracketTightened.lean`'s own header states
  explicitly, in its "WHAT THIS FILE DOES NOT DO" section: "The exact
  value of `det(toEuclideanCLM M1)` is not computed by this route (it
  is, in fact, computable in closed form as `det M1 = 2 * 2.1 - 1 * 1 =
  3.2`, comfortably inside `[2.9, 3.72]` ... but that direct computation
  is NOT what this file proves or claims — the falsifiable test asked
  for the bracket obtained via the `lambdaMax * lambda2` route
  specifically". This file supplies exactly that missing direct
  computation, by a wholly different (and much shorter) route than the
  `lambdaMax`/`lambda2`/eigenvalue machinery used throughout the rest of
  the `YMCapstone*` lineage: it goes straight from `toEuclideanCLM` to
  `Matrix.det` via the `toEuclideanLin`/`toLin` identification and
  Mathlib's `Matrix.det_toLin`, sidestepping `lambdaMax`, `lambda2`,
  eigenvalues, spectra, and Lipschitz estimates entirely. The result
  `3.2` is consistent with (and, as expected, strictly INSIDE) both the
  Wave-5 bracket `[2.03, 4.03]` (`YMCapstoneDetBracket.lean`) and the
  Wave-6 tightened bracket `[2.9, 3.72]`
  (`YMCapstoneDetBracketTightened.lean`), as it must be: `2.9 ≤ 3.2 ≤
  3.72 ≤ 4.03`.

  RELATION TO PRIOR WAVES (read for context, NONE imported/modified).
  This file's `E` and `M1` are declared fresh here (not imported), with
  values byte-identical to `E`/`M1` in `YMCapstoneBracket.lean` (Wave-4),
  `YMCapstoneDetBracket.lean` (Wave-5), `YMCapstoneDetBracketTightened.lean`
  and `YMCapstoneTraceM1Exact.lean` (Wave-6), and
  `YMCapstoneEigvalDichotomy.lean` (Wave-5) — all five files were read in
  full per the task instructions. None of `lambdaMax`, `lambda2`,
  `basis2`, or any spectral/eigenvalue lemma from those files is needed
  or reproduced here: the falsifiable test's proof route
  (`coe_toEuclideanCLM_eq_toEuclideanLin` →
  `toEuclideanLin_eq_toLin_orthonormal` → `det_toLin` → `det_fin_two`)
  is fully self-contained given only `E` and `M1`, so none of those five
  files is touched, modified, or even needed as a dependency (they are
  cited here purely for the "why this is new" context above).

  BUILD-SYSTEM NOTE. Because this file needs nothing beyond `Mathlib`
  itself plus its own local `E`/`M1` (no reproduction of any prior-wave
  declaration is required for the proof route this item's test
  specifies), there is no free-standing-file reproduction burden here
  unlike most other files in this lineage.

  MATHLIB TOOLS USED (checked by direct grep/read against the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`):
    - `Matrix.coe_toEuclideanCLM_eq_toEuclideanLin`
      (`Mathlib/Analysis/CStarAlgebra/Matrix.lean`): the `LinearMap`
      coercion of `Matrix.toEuclideanCLM A` equals `Matrix.toEuclideanLin A`.
    - `Matrix.toEuclideanLin_eq_toLin_orthonormal`
      (`Mathlib/Analysis/InnerProductSpace/PiL2.lean`): `toEuclideanLin`
      equals `Matrix.toLin` with respect to the orthonormal-basis-derived
      `Basis`es `(EuclideanSpace.basisFun _ _).toBasis`.
    - `Matrix.det_toLin` (`Mathlib/LinearAlgebra/Determinant.lean`):
      `LinearMap.det (Matrix.toLin b b f) = f.det` for any `Basis b`.
    - `Matrix.det_fin_two` (`Mathlib/LinearAlgebra/Matrix/Determinant/Basic.lean`):
      closed form `A.det = A 0 0 * A 1 1 - A 0 1 * A 1 0` for `2×2`
      matrices, closed here by `norm_num` on `M1`'s concrete entries.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT.
  `det_toEuclideanCLM_M1_eq_three_point_two` proves
  `(toEuclideanCLM M1 : E →ₗ[ℝ] E).det = 3.2` exactly, by rewriting the
  `LinearMap`-coerced determinant of `toEuclideanCLM M1` to
  `Matrix.det M1` via the `toEuclideanLin`/`toLin` identification, then
  evaluating `Matrix.det M1 = 2 * 2.1 - 1 * 1 = 3.2` via `det_fin_two`
  and `norm_num`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-7 instructions). This remains the same single hand-picked `2×2`
  toy matrix `M1` used throughout this lineage; nothing here is about
  SU(N), any lattice-gauge action, reflection positivity, or the
  continuum limit. This file says nothing about Yang-Mills, does not
  approximate a solution to the Clay mass-gap problem, and claims no
  mathematical novelty — computing the determinant of an explicit `2×2`
  real matrix is classical, elementary linear algebra.

  Every Mathlib name used below was checked by direct grep/read against
  the vendored snapshot, in addition to compiling cleanly via
  `lake env lean` (see the file's own build log for the exact
  command/exit code, reported alongside this file).
-/
import Mathlib

namespace YMCapstoneDetM1Exact

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E`
throughout the `YMCapstone*` lineage. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- The perturbed matrix `M1`. Byte-identical to `M1` throughout the
`YMCapstone*` lineage. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

/-- **New falsifiable result (YM-CAPSTONE-DET-M1-EXACT), the falsifiable
test as stated.** `det (toEuclideanCLM M1 : E →ₗ[ℝ] E) = 3.2` exactly,
via `coe_toEuclideanCLM_eq_toEuclideanLin` →
`toEuclideanLin_eq_toLin_orthonormal` → `det_toLin` → `det_fin_two` +
`norm_num`. -/
theorem det_toEuclideanCLM_M1_eq_three_point_two :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).det = 3.2 := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin,
    Matrix.toEuclideanLin_eq_toLin_orthonormal, LinearMap.det_toLin, Matrix.det_fin_two]
  norm_num [M1]

end YMCapstoneDetM1Exact

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms the new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneDetM1Exact.det_toEuclideanCLM_M1_eq_three_point_two
