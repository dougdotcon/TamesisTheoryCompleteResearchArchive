/-
  YM-CAPSTONE-EIGVAL-DICHOTOMY — eigenvalue dichotomy exhaustiveness for
  `toEuclideanCLM M1`: EVERY eigenvalue `mu` of `toEuclideanCLM M1` lies in
  the numeric interval `[2.9, 3.1]` OR the numeric interval `[0.7, 1.3]`,
  with no third possibility. Wave-5 batch item, a direct follow-on
  composition of two Wave-4 capstone brackets
  (`WAVE4-YM-CAPSTONE-BRACKET`, `WAVE4-YM-CAPSTONE-FULL`) with the Wave-4
  shared-infrastructure two-eigenvalue exhaustiveness fact
  (`WAVE4-SHARED-4A`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-5 task instructions on
  build contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1/Wave-2/Wave-3/Wave-4/Wave-5 file in this directory. This
  file does NOT modify any other file; it only READS four Wave-4 files
  (see RELATION TO WAVE-4 below).

  EXACT TASK ATTEMPTED (per the Wave-5 work-item prompt, candidate
  `YM-CAPSTONE-EIGVAL-DICHOTOMY`, itself matching
  `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md`). Nothing broader
  than this was attempted: prove
  `(2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (0.7 ≤ mu ∧ mu ≤ 1.3)` for every eigenvalue
  `mu` of `toEuclideanCLM M1`, via exactly
  `rcases eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
  finrank_E_eq_two hmu with h | h`, substituting the two ALREADY-CLOSED
  numeric brackets (`lambdaMax_M1_bracket` from `YMCapstoneBracket.lean`,
  `lambda2_M1_bracket_from_compose` from `YMCapstoneFull.lean`) into the
  two resulting cases, exactly as the task specified.

  RELATION TO WAVE-4 (all four files read in full, NONE
  imported/modified). This file reuses, BYTE-FOR-BYTE REPRODUCED (never
  imported — see the BUILD-SYSTEM NOTE below for why, identical reasoning
  to every prior Wave-2/Wave-3/Wave-4 sibling that faces the same
  free-standing-file constraint), declarations from FOUR Wave-4 files:
    - `E`, `lambdaMax`, `lambdaMax_hasEigenvalue`, `M2` chain
      (`M2_isHermitian` .. `lambdaMax_grounded_eq_three`), `basis2`,
      `lambda2`, `trace_toEuclideanCLM_M2_eq_four`,
      `lambda2_toEuclideanCLM_M2_eq_one`, `M1`, `sonda1_bridge`,
      `diff_eq_diagonal`, `pi_norm_vec`, `sonda2_numeric_norm`,
      `bddAbove_rayleighQuotient_subtype`, `lambdaMax_lipschitz`,
      `trace_lipschitz`, `lambda2_lipschitz`, `stability_compose_lambda2`,
      `M1_isHermitian`, `toEuclideanCLM_M1_isSymmetric`,
      `finrank_E_eq_two`, `lambda2_M1_bracket_from_compose` — verbatim
      from `YMCapstoneFull.lean` (Wave-4, `YMCapstoneFull`).
    - `stability_compose_lambdaMax`, `lambdaMax_M1_bracket` — verbatim
      from `YMCapstoneBracket.lean` (Wave-4, `YMCapstoneBracket`),
      re-derived here from the `YMCapstoneFull`-style ingredients above
      (identical proof text; `YMCapstoneFull.lean` does not itself state
      `lambdaMax_M1_bracket`, only `lambda2_M1_bracket_from_compose`, so
      this file adds the `lambdaMax` half back in, verbatim from
      `YMCapstoneBracket.lean`).
    - `lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`,
      `eigenvalue_eq_lambdaMax_or_lambda2` — verbatim from
      `TwoEigenvalueExhaustiveness.lean` (Wave-4,
      `SHARED4A.TwoEigenvalueExhaustiveness`, `03_MILLENNIUM/_SHARED_INFRA/FORMAL`).
    - `LambdaMaxMulLambda2EqDet.lean` (Wave-4, `SHARED4B`) was read in
      full per the task instructions but is NOT used: this item's
      falsifiable test does not need `det = lambdaMax * lambda2`, only
      the two-eigenvalue exhaustiveness dichotomy plus the two numeric
      brackets, so nothing from that file is reproduced here.
  None of `YMCapstoneFull.lean`, `YMCapstoneBracket.lean`,
  `TwoEigenvalueExhaustiveness.lean`, or `LambdaMaxMulLambda2EqDet.lean`
  is touched or modified; all four are read-only source material.

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). Identical situation and identical reasoning to every prior
  Wave-2/Wave-3/Wave-4 sibling in this directory: none of the four Wave-4
  source files above live inside the `[[lean_lib]] name = "TamesisLab"`
  module graph declared in `lakefile.toml`, so none of them has a built
  `.olean` that could be `import`ed by module path. Per the Wave-5 task
  instructions ("do NOT touch any file outside your own new file(s)"),
  this file cannot register any of them into the library graph either.
  The only way to reuse their declarations under this constraint is to
  reproduce them verbatim.

  MATHLIB TOOLS USED — none new beyond what `YMCapstoneFull.lean`,
  `YMCapstoneBracket.lean`, and `TwoEigenvalueExhaustiveness.lean` already
  cite in their own headers (see those three files for the exact Mathlib
  file/line citations for every reproduced name). This file adds no new
  citation beyond what those three files already established; the only
  genuinely new step is the final combination
  `rcases eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
  finrank_E_eq_two hmu with h | h`, followed by `rw`/`linarith` against the
  two already-closed brackets, exactly per the task's own falsifiable-test
  wording.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT.
  `eigenvalue_eq_lambdaMax_or_lambda2` (reproduced from
  `TwoEigenvalueExhaustiveness.lean`) says: for symmetric `T` on the fixed
  2-dimensional `E`, EVERY eigenvalue `mu` of `T` equals `lambdaMax T` or
  `lambda2 T` — no third possibility. Applying this to
  `T = toEuclideanCLM M1` (symmetric via `toEuclideanCLM_M1_isSymmetric`,
  reproduced from `YMCapstoneFull.lean`), and substituting the two
  ALREADY-CLOSED Wave-4 numeric brackets
  `lambdaMax_M1_bracket : 2.9 ≤ lambdaMax (toEuclideanCLM M1) ≤ 3.1` and
  `lambda2_M1_bracket_from_compose : 7/10 ≤ lambda2 (toEuclideanCLM M1) ≤
  13/10` into the two respective cases of the dichotomy, gives EXACTLY
  the target statement: every eigenvalue `mu` of `toEuclideanCLM M1`
  satisfies `(2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (0.7 ≤ mu ∧ mu ≤ 1.3)` (note
  `7/10 = 0.7` and `13/10 = 1.3` exactly). This is genuinely
  EXHAUSTIVE for `toEuclideanCLM M1`: since `dim E = 2`, `M1` (symmetric)
  has EXACTLY two eigenvalues counted with the sorted-eigenvalue-family
  convention, and both are now pinned to disjoint numeric intervals.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-5 instructions). This remains the same single hand-picked `2×2`
  toy matrix pair (`M1`, `M2`) already used throughout the Wave-3/Wave-4
  `YM-STABILITY`/`YM-CAPSTONE` lineage; nothing here is about SU(N), any
  lattice-gauge action, reflection positivity, or the continuum limit.
  The two numeric brackets combined here (`[2.9,3.1]` and `[0.7,1.3]`)
  are exactly as tight as the Wave-4 files that proved them — no
  tightening or new numeric computation is attempted here, only the
  EXHAUSTIVENESS combination (that these two brackets, via the
  two-eigenvalue dichotomy, actually cover ALL eigenvalues of
  `toEuclideanCLM M1`, not just the two named quantities `lambdaMax` and
  `lambda2` in isolation). This file says nothing about Yang-Mills, does
  not approximate a solution to the Clay mass-gap problem, and claims no
  mathematical novelty — combining an already-proved exhaustive
  two-eigenvalue case split with two already-proved numeric brackets via
  `rcases`/`rw`/`linarith` is routine proof composition, not a new
  mathematical result.

  Every Mathlib name used below was checked by direct grep/read against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

open Matrix
open scoped Matrix.Norms.L2Operator

namespace YMCapstoneEigvalDichotomy

/-! ### Part 0a — verbatim reproduction of `YMCapstoneFull`'s `E`,
`lambdaMax`, `lambdaMax_hasEigenvalue` (Wave-4, itself reproduced verbatim
from `StabilityGrounded.lean`, Wave-3). -/

/-- The fixed finite-dimensional real inner product space (verbatim from
`YMCapstoneFull.E`). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the fixed
space `E` (verbatim from `YMCapstoneFull.lambdaMax`). -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`
(verbatim from `YMCapstoneFull.lambdaMax_hasEigenvalue`). -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Part 0b — verbatim reproduction of `YMCapstoneFull`'s `M2` chain
(originally from `YM1.TransferGapSpectrum` / `YM1.TransferGap`): `M2`,
`M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`, `M2_spectrum_eq`,
`M2_eigen_three`. -/

/-- The toy 2×2 "transfer matrix" (verbatim value from `YMCapstoneFull.M2`). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-- `M2` is Hermitian (verbatim from `YMCapstoneFull.M2_isHermitian`). -/
theorem M2_isHermitian : M2.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M2, Matrix.conjTranspose_apply]

/-- The characteristic polynomial of `M2`, evaluated at any real `r`, equals
`(r - 3) * (r - 1)` (verbatim from `YMCapstoneFull.M2_charpoly_eval`). -/
theorem M2_charpoly_eval (r : ℝ) :
    M2.charpoly.eval r = (r - 3) * (r - 1) := by
  have h00 : M2 0 0 = 2 := rfl
  have h01 : M2 0 1 = 1 := rfl
  have h10 : M2 1 0 = 1 := rfl
  have h11 : M2 1 1 = 2 := rfl
  rw [Matrix.eval_charpoly, Matrix.det_fin_two]
  simp [Matrix.sub_apply, Matrix.scalar_apply, h00, h01, h10, h11]
  ring

/-- **Closed-form real spectrum of `M2` (pointwise characterization).**
(verbatim from `YMCapstoneFull.M2_spectrum_real`). -/
theorem M2_spectrum_real (r : ℝ) :
    r ∈ spectrum ℝ M2 ↔ r = 3 ∨ r = 1 := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly]
  show M2.charpoly.eval r = 0 ↔ r = 3 ∨ r = 1
  rw [M2_charpoly_eval]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h3 | h1
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)
  · rintro (rfl | rfl) <;> ring

/-- The real spectrum of `M2` is exactly `{1, 3}` (verbatim from
`YMCapstoneFull.M2_spectrum_eq`). -/
theorem M2_spectrum_eq : spectrum ℝ M2 = ({1, 3} : Set ℝ) := by
  ext r
  rw [M2_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

/-- `v₁ = (1,1)` is an eigenvector of `M2` with eigenvalue `3` (verbatim
from `YMCapstoneFull.M2_eigen_three`). -/
theorem M2_eigen_three : M2.mulVec ![1, 1] = (3 : ℝ) • ![1, 1] := by
  ext i
  fin_cases i <;>
    simp [M2, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-! ### Part 0c — verbatim reproduction of the rest of `YMCapstoneFull`'s
abstract-spectrum route to `lambdaMax (toEuclideanCLM M2) = 3`. -/

theorem toEuclideanCLM_M2_spectrum_eq :
    spectrum ℝ (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      = ({1, 3} : Set ℝ) := by
  rw [AlgEquiv.spectrum_eq (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2)) M2]
  exact M2_spectrum_eq

theorem toEuclideanCLM_M2_endSpectrum_eq :
    spectrum ℝ ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      : Module.End ℝ E) = ({1, 3} : Set ℝ) := by
  rw [← ContinuousLinearMap.spectrum_eq]
  exact toEuclideanCLM_M2_spectrum_eq

theorem toEuclideanCLM_M2_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M2_isHermitian

theorem lambdaMax_mem_one_three :
    lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 1
      ∨ lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 3 := by
  have hEig := lambdaMax_hasEigenvalue _ toEuclideanCLM_M2_isSymmetric
  have hMem : lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) ∈
      spectrum ℝ ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
        : Module.End ℝ E) := by
    rw [Module.End.hasEigenvalue_iff_mem_spectrum] at hEig
    exact hEig
  rw [toEuclideanCLM_M2_endSpectrum_eq] at hMem
  simpa [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm] using hMem

/-- The vector `v = (1,1) ∈ E` (verbatim from `YMCapstoneFull.v`). -/
noncomputable def v : E := WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)

theorem v_ne_zero : v ≠ 0 := by
  intro h
  have h0 : (WithLp.equiv 2 (Fin 2 → ℝ)) v 0 = (WithLp.equiv 2 (Fin 2 → ℝ)) (0 : E) 0 := by
    rw [h]
  simp [v, WithLp.equiv] at h0

theorem toEuclideanCLM_M2_apply_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) v = (3 : ℝ) • v := by
  show (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
      (WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)) = (3 : ℝ) • v
  rw [Matrix.toEuclideanCLM_toLp, M2_eigen_three]
  rfl

theorem toEuclideanCLM_M2_rayleighQuotient_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2).rayleighQuotient v = 3 := by
  have hvnorm : ‖v‖ ≠ 0 := norm_ne_zero_iff.mpr v_ne_zero
  rw [ContinuousLinearMap.rayleighQuotient, ContinuousLinearMap.reApplyInnerSelf_apply,
    toEuclideanCLM_M2_apply_v, real_inner_smul_left, real_inner_self_eq_norm_sq]
  rw [RCLike.re_to_real]
  field_simp

theorem lambdaMax_ge_three :
    3 ≤ lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) := by
  have hBdd : BddAbove (Set.range fun x : { x : E // x ≠ 0 } =>
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2).rayleighQuotient (x : E)) := by
    refine ⟨‖Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2‖, ?_⟩
    rintro _ ⟨x, rfl⟩
    exact (le_abs_self _).trans
      ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2).rayleighQuotient_le_norm (x : E))
  have := le_ciSup hBdd (⟨v, v_ne_zero⟩ : { x : E // x ≠ 0 })
  rw [toEuclideanCLM_M2_rayleighQuotient_v] at this
  exact this

/-- **Wave-3 YM-STABILITY-GROUNDED result, reproduced verbatim (via
`YMCapstoneFull.lean`).** `lambdaMax (toEuclideanCLM M2) = 3` exactly. -/
theorem lambdaMax_grounded_eq_three :
    lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 3 := by
  rcases lambdaMax_mem_one_three with h1 | h3
  · exfalso
    have := lambdaMax_ge_three
    rw [h1] at this
    linarith
  · exact h3

/-! ### Part 0d — verbatim reproduction of `YMCapstoneFull`'s `basis2`,
`lambda2`. -/

/-- The fixed orthonormal basis of `E`. Byte-identical to `basis2` in
`YMCapstoneFull.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`YMCapstoneFull.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-! ### Part 1 — verbatim reproduction of `YMCapstoneFull`'s PASSO 1
(`trace_toEuclideanCLM_M2_eq_four`, `lambda2_toEuclideanCLM_M2_eq_one`). -/

theorem trace_toEuclideanCLM_M2_eq_four :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E).trace ℝ E = 4 := by
  rw [LinearMap.trace_eq_sum_inner
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E) basis2]
  have hterm : ∀ i : Fin 2,
      (inner ℝ (basis2 i)
        ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E) (basis2 i)) : ℝ)
        = (basis2 i) ⬝ᵥ (M2 *ᵥ (basis2 i)) :=
    fun i => Matrix.inner_toEuclideanCLM M2 (basis2 i) (basis2 i)
  simp_rw [hterm]
  have hb : ∀ i : Fin 2, basis2 i = EuclideanSpace.single i 1 := fun i =>
    EuclideanSpace.basisFun_apply (ι := Fin 2) (𝕜 := ℝ) i
  simp_rw [hb]
  rw [Fin.sum_univ_two]
  norm_num [dotProduct, Matrix.mulVec, M2, Fin.sum_univ_two, EuclideanSpace.single]

theorem lambda2_toEuclideanCLM_M2_eq_one :
    lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 1 := by
  unfold lambda2
  rw [trace_toEuclideanCLM_M2_eq_four, lambdaMax_grounded_eq_three]
  norm_num

/-! ### Part 2 — verbatim reproduction of `YMCapstoneFull`'s PASSO 2
plumbing needed for BOTH numeric brackets (`M1`, `sonda1_bridge`,
`diff_eq_diagonal`, `pi_norm_vec`, `sonda2_numeric_norm`,
`bddAbove_rayleighQuotient_subtype`, `lambdaMax_lipschitz`,
`trace_lipschitz`, `lambda2_lipschitz`, `stability_compose_lambda2`),
PLUS the `lambdaMax` composition step `stability_compose_lambdaMax`
(verbatim from `YMCapstoneBracket.lean`, not present in
`YMCapstoneFull.lean`, needed here to also close the `lambdaMax` bracket
below). -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` in
`YMCapstoneFull.lean` / `YMCapstoneBracket.lean`. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

theorem sonda1_bridge :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 -
        Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2‖ = ‖M1 - M2‖ := by
  rw [← map_sub (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2))]
  exact Matrix.l2_opNorm_toEuclideanCLM (M1 - M2)

theorem diff_eq_diagonal : M1 - M2 = Matrix.diagonal ![(0 : ℝ), 1 / 10] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [M1, M2]

theorem pi_norm_vec : ‖(![(0 : ℝ), 1 / 10] : Fin 2 → ℝ)‖ = 1 / 10 := by
  apply le_antisymm
  · rw [pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 10)]
    intro i
    fin_cases i <;> norm_num
  · have := norm_le_pi_norm (![(0 : ℝ), 1 / 10] : Fin 2 → ℝ) 1
    simpa using this

theorem sonda2_numeric_norm : ‖M1 - M2‖ = 1 / 10 := by
  rw [diff_eq_diagonal, Matrix.l2_opNorm_diagonal]
  exact pi_norm_vec

theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

theorem lambdaMax_lipschitz (A B : E →L[ℝ] E) :
    |lambdaMax A - lambdaMax B| ≤ ‖A - B‖ := by
  have hBddA := bddAbove_rayleighQuotient_subtype A
  have hBddB := bddAbove_rayleighQuotient_subtype B
  have hdiffAB : ∀ x : { x : E // x ≠ 0 },
      A.rayleighQuotient (x : E) - B.rayleighQuotient (x : E) ≤ ‖A - B‖ := by
    intro x
    have hsub : A.rayleighQuotient (x : E) - B.rayleighQuotient (x : E)
        = (A - B).rayleighQuotient (x : E) := by
      simp [ContinuousLinearMap.rayleighQuotient,
        ContinuousLinearMap.reApplyInnerSelf_apply, inner_sub_left, sub_div]
    rw [hsub]
    exact (le_abs_self _).trans ((A - B).rayleighQuotient_le_norm (x : E))
  have hdiffBA : ∀ x : { x : E // x ≠ 0 },
      B.rayleighQuotient (x : E) - A.rayleighQuotient (x : E) ≤ ‖A - B‖ := by
    intro x
    have hsub : B.rayleighQuotient (x : E) - A.rayleighQuotient (x : E)
        = (B - A).rayleighQuotient (x : E) := by
      simp [ContinuousLinearMap.rayleighQuotient,
        ContinuousLinearMap.reApplyInnerSelf_apply, inner_sub_left, sub_div]
    rw [hsub]
    calc (B - A).rayleighQuotient (x : E)
        ≤ |(B - A).rayleighQuotient (x : E)| := le_abs_self _
      _ ≤ ‖B - A‖ := (B - A).rayleighQuotient_le_norm (x : E)
      _ = ‖A - B‖ := (norm_sub_rev A B).symm
  obtain ⟨x0, hx0⟩ := exists_ne (0 : E)
  haveI : Nonempty { x : E // x ≠ 0 } := ⟨⟨x0, hx0⟩⟩
  have hA_le : lambdaMax A ≤ lambdaMax B + ‖A - B‖ := by
    apply ciSup_le
    intro x
    have h1 : B.rayleighQuotient (x : E) ≤ lambdaMax B := le_ciSup hBddB x
    have h2 := hdiffAB x
    linarith
  have hB_le : lambdaMax B ≤ lambdaMax A + ‖A - B‖ := by
    apply ciSup_le
    intro x
    have h1 : A.rayleighQuotient (x : E) ≤ lambdaMax A := le_ciSup hBddA x
    have h2 := hdiffBA x
    linarith
  rw [abs_sub_le_iff]
  exact ⟨by linarith, by linarith⟩

theorem trace_lipschitz (A B : E →L[ℝ] E) :
    |(A : E →ₗ[ℝ] E).trace ℝ E - (B : E →ₗ[ℝ] E).trace ℝ E| ≤ 2 * ‖A - B‖ := by
  have hA := LinearMap.trace_eq_sum_inner (A : E →ₗ[ℝ] E) basis2
  have hB := LinearMap.trace_eq_sum_inner (B : E →ₗ[ℝ] E) basis2
  rw [hA, hB, ← Finset.sum_sub_distrib]
  have hterm : ∀ i : Fin 2,
      (inner ℝ (basis2 i) ((A : E →ₗ[ℝ] E) (basis2 i))
        - inner ℝ (basis2 i) ((B : E →ₗ[ℝ] E) (basis2 i)) : ℝ)
        = inner ℝ (basis2 i) ((A - B) (basis2 i)) := by
    intro i
    have hsub : (A : E →ₗ[ℝ] E) (basis2 i) - (B : E →ₗ[ℝ] E) (basis2 i)
        = (A - B) (basis2 i) := by simp [_root_.sub_apply]
    rw [← hsub, inner_sub_right]
  simp_rw [hterm]
  calc |∑ i : Fin 2, inner ℝ (basis2 i) ((A - B) (basis2 i))|
      ≤ ∑ i : Fin 2, |inner ℝ (basis2 i) ((A - B) (basis2 i))| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _i : Fin 2, ‖A - B‖ := by
        apply Finset.sum_le_sum
        intro i _
        have h1 : |inner ℝ (basis2 i) ((A - B) (basis2 i))|
            ≤ ‖basis2 i‖ * ‖(A - B) (basis2 i)‖ := abs_real_inner_le_norm _ _
        have h2 : ‖(A - B) (basis2 i)‖ ≤ ‖A - B‖ * ‖basis2 i‖ := (A - B).le_opNorm _
        have h3 : ‖basis2 i‖ = 1 := basis2.norm_eq_one i
        rw [h3] at h1 h2
        linarith
    _ = 2 * ‖A - B‖ := by
        rw [Finset.sum_const, Finset.card_univ]
        simp [two_mul]

theorem lambda2_lipschitz (A B : E →L[ℝ] E) :
    |lambda2 A - lambda2 B| ≤ 3 * ‖A - B‖ := by
  have h1 := trace_lipschitz A B
  have h2 := lambdaMax_lipschitz A B
  unfold lambda2
  rw [abs_le] at h1 h2 ⊢
  constructor <;> [linarith [h1.1, h2.1]; linarith [h1.2, h2.2]]

theorem stability_compose_lambda2 :
    |lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 3 / 10 := by
  have h := lambda2_lipschitz (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1)
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
  rw [sonda1_bridge, sonda2_numeric_norm] at h
  linarith

/-- **Wave-3 YM-STABILITY-COMPOSE result, part 1, reproduced verbatim (via
`YMCapstoneBracket.lean`).** Chaining `lambdaMax_lipschitz` with the
concrete numeric bound `sonda1_bridge`/`sonda2_numeric_norm`: the
top-eigenvalue candidates of `toEuclideanCLM M1` and `toEuclideanCLM M2`
differ by at most `1/10`. Needed here (in addition to
`stability_compose_lambda2` above) to also close the `lambdaMax` bracket
below — `YMCapstoneFull.lean` alone does not state this theorem. -/
theorem stability_compose_lambdaMax :
    |lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 1 / 10 :=
  (lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact sonda2_numeric_norm.le)

/-- **Wave-4 YM-CAPSTONE-BRACKET result, reproduced verbatim (via
`YMCapstoneBracket.lean`).** `lambdaMax (toEuclideanCLM M1)` lies in the
numeric interval `[2.9, 3.1]`. -/
theorem lambdaMax_M1_bracket :
    2.9 ≤ lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 3.1 := by
  have h := stability_compose_lambdaMax
  rw [lambdaMax_grounded_eq_three] at h
  rw [abs_le] at h
  constructor <;> linarith

theorem M1_isHermitian : M1.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M1, Matrix.conjTranspose_apply]

theorem toEuclideanCLM_M1_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M1_isHermitian

theorem finrank_E_eq_two : Module.finrank ℝ E = 2 :=
  finrank_euclideanSpace_fin

/-- **Wave-4 YM-CAPSTONE-FULL result, reproduced verbatim (via
`YMCapstoneFull.lean`).** `lambda2 (toEuclideanCLM M1)` lies in the
numeric interval `[7/10, 13/10]`. -/
theorem lambda2_M1_bracket_from_compose :
    7 / 10 ≤ lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 13 / 10 := by
  have h := stability_compose_lambda2
  rw [lambda2_toEuclideanCLM_M2_eq_one] at h
  rw [abs_le] at h
  constructor <;> linarith

/-! ### Part 3 — verbatim reproduction of `TwoEigenvalueExhaustiveness.lean`
(Wave-4, `SHARED4A`): the two-eigenvalue exhaustiveness dichotomy
`eigenvalue_eq_lambdaMax_or_lambda2`, via its two supporting promoted
lemmas `lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one`. -/

/-- **Promotion of `heq0`, reproduced verbatim from
`TwoEigenvalueExhaustiveness.lean`.** For symmetric `T` on the fixed
2-dimensional `E`, `lambdaMax T` coincides with the `0`-th (largest) entry
of Mathlib's sorted eigenvalue family `hT.eigenvalues hn`. -/
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

/-- **Promotion of `hlambda2`, reproduced verbatim from
`TwoEigenvalueExhaustiveness.lean`.** For symmetric `T` on the fixed
2-dimensional `E`, `lambda2 T` coincides with the `1`-st (smaller) entry
of Mathlib's sorted eigenvalue family `hT.eigenvalues hn`. -/
theorem lambda2_eq_eigenvalues_one (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T = hT.eigenvalues hn 1 := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  unfold lambda2
  rw [htrace, heq0]; ring

/-- **Wave-4 SHARED-4A result, reproduced verbatim from
`TwoEigenvalueExhaustiveness.lean`.** Two-eigenvalue exhaustiveness in
dimension 2: for symmetric `T : E →L[ℝ] E` on the fixed 2-dimensional `E`,
EVERY eigenvalue `mu` of `T` equals either `lambdaMax T` or `lambda2 T` —
there is no third possibility. -/
theorem eigenvalue_eq_lambdaMax_or_lambda2 (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2)
    {mu : ℝ} (hmu : Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) mu) :
    mu = lambdaMax T ∨ mu = lambda2 T := by
  obtain ⟨i, hi⟩ := hT.exists_eigenvalues_eq hn hmu
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have heq1 := lambda2_eq_eigenvalues_one T hT hn
  fin_cases i
  · left; rw [← hi]; exact heq0.symm
  · right; rw [← hi]; exact heq1.symm

/-! ### Part 4 — new content specific to this item
(YM-CAPSTONE-EIGVAL-DICHOTOMY): the falsifiable test as stated, combining
`eigenvalue_eq_lambdaMax_or_lambda2` (Part 3) with the two already-closed
numeric brackets `lambdaMax_M1_bracket` and `lambda2_M1_bracket_from_compose`
(Part 2), applied to `T = toEuclideanCLM M1`. -/

/-- **Main new result (YM-CAPSTONE-EIGVAL-DICHOTOMY), the falsifiable test
as stated.** Every eigenvalue `mu` of `toEuclideanCLM M1` lies in
`[2.9, 3.1]` or in `[0.7, 1.3]` — no third possibility, and (via
`eigenvalue_eq_lambdaMax_or_lambda2`) this is genuinely EXHAUSTIVE: since
`toEuclideanCLM M1` is symmetric on the fixed 2-dimensional `E`, it has
exactly two eigenvalues (sorted-eigenvalue-family convention), and both
are now pinned to these two disjoint numeric intervals. Proof: exactly
`rcases eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
finrank_E_eq_two hmu with h | h`, substituting the two already-closed
brackets `lambdaMax_M1_bracket` / `lambda2_M1_bracket_from_compose` into
the two resulting cases (`7/10 = 0.7`, `13/10 = 1.3` exactly), as the task
specified. -/
theorem eigenvalue_dichotomy_toEuclideanCLM_M1
    {mu : ℝ} (hmu : Module.End.HasEigenvalue
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E) mu) :
    (2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (0.7 ≤ mu ∧ mu ≤ 1.3) := by
  rcases eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
      finrank_E_eq_two hmu with h | h
  · left
    rw [h]
    exact lambdaMax_M1_bracket
  · right
    rw [h]
    obtain ⟨hlo, hhi⟩ := lambda2_M1_bracket_from_compose
    constructor <;> linarith

end YMCapstoneEigvalDichotomy

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneEigvalDichotomy.lambdaMax_hasEigenvalue
#print axioms YMCapstoneEigvalDichotomy.M2_isHermitian
#print axioms YMCapstoneEigvalDichotomy.M2_charpoly_eval
#print axioms YMCapstoneEigvalDichotomy.M2_spectrum_real
#print axioms YMCapstoneEigvalDichotomy.M2_spectrum_eq
#print axioms YMCapstoneEigvalDichotomy.M2_eigen_three
#print axioms YMCapstoneEigvalDichotomy.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneEigvalDichotomy.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneEigvalDichotomy.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneEigvalDichotomy.lambdaMax_mem_one_three
#print axioms YMCapstoneEigvalDichotomy.v_ne_zero
#print axioms YMCapstoneEigvalDichotomy.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneEigvalDichotomy.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneEigvalDichotomy.lambdaMax_ge_three
#print axioms YMCapstoneEigvalDichotomy.lambdaMax_grounded_eq_three
#print axioms YMCapstoneEigvalDichotomy.trace_toEuclideanCLM_M2_eq_four
#print axioms YMCapstoneEigvalDichotomy.lambda2_toEuclideanCLM_M2_eq_one
#print axioms YMCapstoneEigvalDichotomy.sonda1_bridge
#print axioms YMCapstoneEigvalDichotomy.diff_eq_diagonal
#print axioms YMCapstoneEigvalDichotomy.pi_norm_vec
#print axioms YMCapstoneEigvalDichotomy.sonda2_numeric_norm
#print axioms YMCapstoneEigvalDichotomy.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneEigvalDichotomy.lambdaMax_lipschitz
#print axioms YMCapstoneEigvalDichotomy.trace_lipschitz
#print axioms YMCapstoneEigvalDichotomy.lambda2_lipschitz
#print axioms YMCapstoneEigvalDichotomy.stability_compose_lambda2
#print axioms YMCapstoneEigvalDichotomy.stability_compose_lambdaMax
#print axioms YMCapstoneEigvalDichotomy.lambdaMax_M1_bracket
#print axioms YMCapstoneEigvalDichotomy.M1_isHermitian
#print axioms YMCapstoneEigvalDichotomy.toEuclideanCLM_M1_isSymmetric
#print axioms YMCapstoneEigvalDichotomy.finrank_E_eq_two
#print axioms YMCapstoneEigvalDichotomy.lambda2_M1_bracket_from_compose
#print axioms YMCapstoneEigvalDichotomy.lambdaMax_eq_eigenvalues_zero
#print axioms YMCapstoneEigvalDichotomy.lambda2_eq_eigenvalues_one
#print axioms YMCapstoneEigvalDichotomy.eigenvalue_eq_lambdaMax_or_lambda2
#print axioms YMCapstoneEigvalDichotomy.eigenvalue_dichotomy_toEuclideanCLM_M1
