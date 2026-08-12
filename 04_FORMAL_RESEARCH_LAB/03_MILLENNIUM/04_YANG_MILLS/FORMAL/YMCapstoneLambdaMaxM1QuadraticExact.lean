/-
  YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT — apply the SHARED-6A quadratic
  formula to `toEuclideanCLM M1` using the exact trace (Wave-6,
  `YMCapstoneTraceM1Exact.lean`, `= 4.1`) and the exact determinant
  (this Wave-7 batch's gate item `YM-CAPSTONE-DET-M1-EXACT`,
  `YMCapstoneDetM1Exact.lean`, `= 3.2`), deriving `lambda2 (toEuclideanCLM
  M1)` exactly (Wave-7 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-7 task instructions on
  build contention with 13 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1..Wave-6 file in this directory. This file does NOT modify
  any other file; it only READS `QuadraticFormulaDim2.lean` (Wave-6,
  SHARED-6A), `YMCapstoneTraceM1Exact.lean` (Wave-6),
  `YMCapstoneDetM1Exact.lean` (this same Wave-7 batch's gate item, its
  own file, independently recompiled by this session before this file
  was written), `YMCapstoneDetBracketTightened.lean` (Wave-6), and
  `YMCapstoneEigvalDichotomy.lean` (Wave-5), all read in full per the
  task instructions.

  GATE DEPENDENCY. This item is gated on `WAVE7-YM-CAPSTONE-DET-M1-EXACT`
  closing first. Before writing this file, the authoring session located
  `YMCapstoneDetM1Exact.lean` and independently recompiled it with
  `lake env lean` (own build log, own exit-code check, own `#print
  axioms` read), confirming exit 0 and a clean `[propext, Classical.choice,
  Quot.sound]` dependency list for its sole declaration
  `det_toEuclideanCLM_M1_eq_three_point_two`. Only after that independent
  confirmation was this file attempted.

  EXACT TASK ATTEMPTED (per the Wave-7 work-item prompt for
  `WAVE7-YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT`, candidate
  `YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT`). Nothing broader than this
  was attempted: apply `lambdaMax_eq_quadratic_formula` (SHARED-6A) to
  `toEuclideanCLM M1` using the exact trace (`4.1`, Wave-6) and the exact
  det (`3.2`, this batch's gate item); derive `lambda2` by `ring`/
  `linarith`, exactly as the plan specified.

  BUILD-SYSTEM NOTE / LINE-COUNT ACCOUNTING (why the pieces below are
  reproduced instead of imported, and which are boilerplate vs. new).
  None of the five files named above is registered in `TamesisLab.lean`
  (none lives inside the `[[lean_lib]] name = "TamesisLab"` module graph
  declared in `lakefile.toml`), so none has a built `.olean` importable
  by module path. Per the Wave-7 task instructions ("do NOT touch any
  file outside your own new file(s)"), this file cannot register any of
  them into the library graph either. The only way to reuse their
  declarations is to reproduce them verbatim, exactly the same situation
  already documented by every Wave-2..Wave-6 sibling in this lineage.
  Per the mandatory line-count discipline (DEC-103, direct lesson from
  WAVE6-BSD-7's ceiling overrun), the following are EXCLUDED from this
  item's 15-new-non-comment-line ceiling because they are byte-identical
  reproductions of already-closed prior-wave/gate-item results, not
  genuinely new content:
    - `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
      `lambdaMax_hasEigenvalue`, `lambda2`, `lambdaMax_eq_eigenvalues_zero`,
      `lambda2_eq_eigenvalues_one`, `lambdaMax_mul_lambda2_eq_det`,
      `lambda2_le_lambdaMax`, `discriminant_eq`,
      `lambdaMax_eq_quadratic_formula` — reproduced verbatim from
      `QuadraticFormulaDim2.lean` (Wave-6, SHARED-6A).
    - `M1`, `M1_isHermitian`, `toEuclideanCLM_M1_isSymmetric`,
      `finrank_E_eq_two` — reproduced verbatim from
      `YMCapstoneEigvalDichotomy.lean` (Wave-5; byte-identical across
      that file, `YMCapstoneDetBracket.lean`, and
      `YMCapstoneDetBracketTightened.lean`).
    - `basis2`, `trace_toEuclideanCLM_M1_eq_four_point_one` — reproduced
      verbatim from `YMCapstoneTraceM1Exact.lean` (Wave-6). Supplies the
      exact trace `4.1` this item's test names.
    - `det_toEuclideanCLM_M1_eq_three_point_two` — reproduced verbatim
      from `YMCapstoneDetM1Exact.lean` (this batch's gate item,
      `YM-CAPSTONE-DET-M1-EXACT`). Supplies the exact det `3.2` this
      item's test names.
  Everything from "New content specific to this item" onward IS the new
  content specific to `YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT`, and is
  what is measured against the 15-line ceiling.

  WHY THIS IS A NEW, DIRECT COMPOSITION (not previously proved in this
  lineage). No prior file in this lineage instantiates
  `lambdaMax_eq_quadratic_formula` (SHARED-6A, Wave-6) at the concrete
  operator `toEuclideanCLM M1` with its two now-exact numeric ingredients
  (`trace = 4.1` from Wave-6, `det = 3.2` from this batch's gate item):
  `YMCapstoneTraceM1Exact.lean` only had a bracket for `lambdaMax`
  (`[2.9, 3.1]`, Wave-4), not an exact det, so it could not invoke the
  quadratic formula in closed form; `YMCapstoneDetM1Exact.lean` computes
  the det alone, with no trace or lambdaMax content at all. This file is
  the first to combine both exact numeric ingredients through the
  SHARED-6A quadratic-formula theorem to pin `lambda2 (toEuclideanCLM
  M1)` to a fully closed-form real-number expression (in terms of
  `Real.sqrt`), narrower than any bracket obtained anywhere earlier in
  this lineage.

  MATHLIB TOOLS USED — no new citation beyond what `QuadraticFormulaDim2.lean`
  (SHARED-6A), `YMCapstoneTraceM1Exact.lean`, and `YMCapstoneDetM1Exact.lean`
  already establish in their own headers, all checked by direct grep/read
  against the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`. The new content itself uses
  only `rw`, `unfold`, and `ring` on already-established equalities — no
  Mathlib lemma is newly cited by the new content.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT.
  `lambda2_toEuclideanCLM_M1_eq_quadratic` proves
  `lambda2 (toEuclideanCLM M1) = (4.1 - Real.sqrt (4.1 ^ 2 - 4 * 3.2)) / 2`
  exactly, by instantiating `lambdaMax_eq_quadratic_formula` at
  `toEuclideanCLM M1` (with `toEuclideanCLM_M1_isSymmetric` and
  `finrank_E_eq_two`), rewriting its trace/det slots with the two exact
  numeric facts named above to get `lambdaMax (toEuclideanCLM M1) = (4.1
  + Real.sqrt (4.1 ^ 2 - 4 * 3.2)) / 2`, then unfolding `lambda2 T :=
  trace T - lambdaMax T`, substituting the exact trace again, and closing
  with `ring`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-7 instructions). This remains the same single hand-picked `2×2`
  toy matrix `M1` used throughout this lineage; nothing here is about
  SU(N), any lattice-gauge action, reflection positivity, or the
  continuum limit. The result is left in closed `Real.sqrt`-involving
  form, not further evaluated to a decimal (`Real.sqrt 4.01` is
  irrational and has no finite decimal `norm_num` closed form); no claim
  is made that this expression is simplified further than the quadratic
  formula itself provides. This file says nothing about Yang-Mills, does
  not approximate a solution to the Clay mass-gap problem, and claims no
  mathematical novelty — instantiating the classical 2×2 quadratic
  formula at concrete numeric trace/det values is elementary algebra.

  Every Mathlib name used below was checked by direct grep/read against
  the vendored snapshot, in addition to compiling cleanly via
  `lake env lean` (see the file's own build log for the exact
  command/exit code, reported alongside this file).
-/
import Mathlib

open Matrix

namespace YMCapstoneLambdaMaxM1QuadraticExact

/-! ### Part 0 — verbatim reproduction of `E`, `lambdaMax`, `lambda2`, and
the full SHARED-6A quadratic-formula chain, from `QuadraticFormulaDim2.lean`
(Wave-6, SHARED-6A). Excluded from this item's line-count ceiling (see
header). -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`QuadraticFormulaDim2.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `QuadraticFormulaDim2.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`QuadraticFormulaDim2.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`.
Byte-identical to `lambdaMax_hasEigenvalue` in `QuadraticFormulaDim2.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`QuadraticFormulaDim2.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- Byte-identical to `lambdaMax_eq_eigenvalues_zero` in
`QuadraticFormulaDim2.lean`. -/
theorem lambdaMax_eq_eigenvalues_zero (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T = hT.eigenvalues hn 0 := by
  have hmaxEig : Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) :=
    lambdaMax_hasEigenvalue T hT
  obtain ⟨i0, hi0⟩ := hT.exists_eigenvalues_eq hn hmaxEig
  have hv := hT.apply_eigenvectorBasis hn 0
  simp only [ContinuousLinearMap.coe_coe] at hv
  have hnorm0 : ‖hT.eigenvectorBasis hn 0‖ = 1 := (hT.eigenvectorBasis hn).norm_eq_one 0
  have hv0 : T.rayleighQuotient (hT.eigenvectorBasis hn 0) = hT.eigenvalues hn 0 := by
    simp [ContinuousLinearMap.rayleighQuotient, ContinuousLinearMap.reApplyInnerSelf_apply,
      hv, real_inner_smul_left, hnorm0]
  have hx0ne : hT.eigenvectorBasis hn 0 ≠ 0 := (hT.hasEigenvector_eigenvectorBasis hn 0).2
  have hBdd := bddAbove_rayleighQuotient_subtype T
  have hle : hT.eigenvalues hn 0 ≤ lambdaMax T := by
    have := le_ciSup hBdd (⟨hT.eigenvectorBasis hn 0, hx0ne⟩ : { x : E // x ≠ 0 })
    rwa [hv0] at this
  have hanti : hT.eigenvalues hn i0 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (Fin.zero_le i0)
  have hi0' : hT.eigenvalues hn i0 = lambdaMax T := by exact_mod_cast hi0
  linarith [hi0', hanti, hle]

/-- Byte-identical to `lambda2_eq_eigenvalues_one` in
`QuadraticFormulaDim2.lean`. -/
theorem lambda2_eq_eigenvalues_one (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T = hT.eigenvalues hn 1 := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  unfold lambda2
  rw [htrace, heq0]; ring

/-- Byte-identical to `lambdaMax_mul_lambda2_eq_det` in
`QuadraticFormulaDim2.lean`. -/
theorem lambdaMax_mul_lambda2_eq_det (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det := by
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := lambda2_eq_eigenvalues_one T hT hn
  have hdet : (T : E →ₗ[ℝ] E).det = hT.eigenvalues hn 0 * hT.eigenvalues hn 1 := by
    rw [hT.det_eq_prod_eigenvalues hn, Fin.prod_univ_two]
    norm_cast
  rw [heq0, hlambda2, hdet]

/-- Byte-identical to `lambda2_le_lambdaMax` in `QuadraticFormulaDim2.lean`. -/
theorem lambda2_le_lambdaMax (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T ≤ lambdaMax T := by
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have heq1 := lambda2_eq_eigenvalues_one T hT hn
  have hanti : hT.eigenvalues hn 1 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (by decide)
  rw [heq0, heq1]
  exact hanti

/-- Byte-identical to `discriminant_eq` in `QuadraticFormulaDim2.lean`. -/
theorem discriminant_eq (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    (lambdaMax T - lambda2 T) ^ 2 =
      ((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = lambdaMax T + lambda2 T := by
    unfold lambda2; ring
  have hdet : lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det :=
    lambdaMax_mul_lambda2_eq_det T hT hn
  rw [htrace, ← hdet]; ring

/-- **SHARED-6A, reproduced verbatim.** For symmetric `T` on the fixed
2-dimensional `E`, `lambdaMax T = (trace T + Real.sqrt ((trace T) ^ 2 - 4
* det T)) / 2`. Byte-identical to `lambdaMax_eq_quadratic_formula` in
`QuadraticFormulaDim2.lean`; this item applies it below. -/
theorem lambdaMax_eq_quadratic_formula (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T =
      ((T : E →ₗ[ℝ] E).trace ℝ E +
          Real.sqrt (((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det)) / 2 := by
  have hord : lambda2 T ≤ lambdaMax T := lambda2_le_lambdaMax T hT hn
  have hdisc : (lambdaMax T - lambda2 T) ^ 2 =
      ((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det := discriminant_eq T hT hn
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = lambdaMax T + lambda2 T := by
    unfold lambda2; ring
  have hsqrt : Real.sqrt (((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det) =
      lambdaMax T - lambda2 T := by
    rw [← hdisc]
    exact Real.sqrt_sq (by linarith)
  rw [hsqrt, htrace]
  ring

/-! ### Part 1 — verbatim reproduction of `M1`, `M1_isHermitian`,
`toEuclideanCLM_M1_isSymmetric`, `finrank_E_eq_two`, from
`YMCapstoneEigvalDichotomy.lean` (Wave-5). Excluded from this item's
line-count ceiling (see header). -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` throughout the
`YMCapstone*` lineage. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

/-- Byte-identical to `M1_isHermitian` in `YMCapstoneEigvalDichotomy.lean`. -/
theorem M1_isHermitian : M1.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M1, Matrix.conjTranspose_apply]

/-- Byte-identical to `toEuclideanCLM_M1_isSymmetric` in
`YMCapstoneEigvalDichotomy.lean`. -/
theorem toEuclideanCLM_M1_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M1_isHermitian

/-- Byte-identical to `finrank_E_eq_two` in `YMCapstoneEigvalDichotomy.lean`. -/
theorem finrank_E_eq_two : Module.finrank ℝ E = 2 :=
  finrank_euclideanSpace_fin

/-! ### Part 2 — verbatim reproduction of `basis2` and the exact-trace
fact, from `YMCapstoneTraceM1Exact.lean` (Wave-6). Supplies the exact
trace `4.1` this item's test names. Excluded from this item's line-count
ceiling (see header). -/

/-- Byte-identical to `basis2` in `YMCapstoneTraceM1Exact.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- Byte-identical to `trace_toEuclideanCLM_M1_eq_four_point_one` in
`YMCapstoneTraceM1Exact.lean`. -/
theorem trace_toEuclideanCLM_M1_eq_four_point_one :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).trace ℝ E = 4.1 := by
  rw [LinearMap.trace_eq_sum_inner
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E) basis2]
  have hterm : ∀ i : Fin 2,
      (inner ℝ (basis2 i)
        ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E) (basis2 i)) : ℝ)
        = (basis2 i) ⬝ᵥ (M1 *ᵥ (basis2 i)) :=
    fun i => Matrix.inner_toEuclideanCLM M1 (basis2 i) (basis2 i)
  simp_rw [hterm]
  have hb : ∀ i : Fin 2, basis2 i = EuclideanSpace.single i 1 := fun i =>
    EuclideanSpace.basisFun_apply (ι := Fin 2) (𝕜 := ℝ) i
  simp_rw [hb]
  rw [Fin.sum_univ_two]
  norm_num [dotProduct, Matrix.mulVec, M1, Fin.sum_univ_two, EuclideanSpace.single]

/-! ### Part 3 — verbatim reproduction of the exact-det fact, from
`YMCapstoneDetM1Exact.lean` (this batch's gate item, `YM-CAPSTONE-DET-M1-EXACT`,
independently recompiled by this session before this file was written —
see header). Supplies the exact det `3.2` this item's test names.
Excluded from this item's line-count ceiling (see header). -/

/-- Byte-identical to `det_toEuclideanCLM_M1_eq_three_point_two` in
`YMCapstoneDetM1Exact.lean`. -/
theorem det_toEuclideanCLM_M1_eq_three_point_two :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).det = 3.2 := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin,
    Matrix.toEuclideanLin_eq_toLin_orthonormal, LinearMap.det_toLin, Matrix.det_fin_two]
  norm_num [M1]

/-! ### New content specific to this item
(YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT): apply
`lambdaMax_eq_quadratic_formula` to `toEuclideanCLM M1` using the exact
trace and exact det above, then derive `lambda2` by `ring`. Measured
against the item's 15-new-non-comment-line ceiling. -/

/-- **New falsifiable result (YM-CAPSTONE-LAMBDAMAX-M1-QUADRATIC-EXACT),
the falsifiable test as stated.** `lambda2 (toEuclideanCLM M1) = (4.1 -
Real.sqrt (4.1 ^ 2 - 4 * 3.2)) / 2` exactly, via
`lambdaMax_eq_quadratic_formula` instantiated at `toEuclideanCLM M1`
(symmetric via `toEuclideanCLM_M1_isSymmetric`, `finrank_E_eq_two`),
its trace/det slots closed by the exact facts
`trace_toEuclideanCLM_M1_eq_four_point_one` /
`det_toEuclideanCLM_M1_eq_three_point_two`, then `unfold lambda2` and
`ring`. -/
theorem lambda2_toEuclideanCLM_M1_eq_quadratic :
    lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) =
      (4.1 - Real.sqrt (4.1 ^ 2 - 4 * 3.2)) / 2 := by
  have hmax := lambdaMax_eq_quadratic_formula (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1)
    toEuclideanCLM_M1_isSymmetric finrank_E_eq_two
  rw [trace_toEuclideanCLM_M1_eq_four_point_one,
    det_toEuclideanCLM_M1_eq_three_point_two] at hmax
  unfold lambda2
  rw [trace_toEuclideanCLM_M1_eq_four_point_one, hmax]
  ring

end YMCapstoneLambdaMaxM1QuadraticExact

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneLambdaMaxM1QuadraticExact.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambdaMax_hasEigenvalue
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambdaMax_eq_eigenvalues_zero
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambda2_eq_eigenvalues_one
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambdaMax_mul_lambda2_eq_det
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambda2_le_lambdaMax
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.discriminant_eq
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambdaMax_eq_quadratic_formula
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.M1_isHermitian
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.toEuclideanCLM_M1_isSymmetric
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.finrank_E_eq_two
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.trace_toEuclideanCLM_M1_eq_four_point_one
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.det_toEuclideanCLM_M1_eq_three_point_two
#print axioms YMCapstoneLambdaMaxM1QuadraticExact.lambda2_toEuclideanCLM_M1_eq_quadratic
