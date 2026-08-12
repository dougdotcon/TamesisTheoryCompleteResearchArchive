/-
  YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED — narrowed eigenvalue dichotomy
  for `toEuclideanCLM M1`: EVERY eigenvalue `mu` of `toEuclideanCLM M1`
  lies in the numeric interval `[2.9, 3.1]` OR the numeric interval
  `[1.0, 1.2]`, with no third possibility. Wave-7 batch item, gated on no
  bracket from the Wave-6 batch (independent composition of two
  already-closed Wave-6 facts), a direct tightening of the Wave-5 item
  `YM-CAPSTONE-EIGVAL-DICHOTOMY` (`YMCapstoneEigvalDichotomy.lean`), whose
  second interval was the wider `[0.7, 1.3]`.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-7 task instructions on
  build contention with 13 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1..Wave-6 file in this directory. This file does NOT modify
  any other file; it only READS `YMCapstoneEigvalDichotomy.lean` (Wave-5)
  and `YMCapstoneTraceM1Exact.lean` (Wave-6), both in this same
  directory.

  EXACT TASK ATTEMPTED (per the Wave-7 work-item prompt, candidate
  `YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED`). Nothing broader than this was
  attempted: prove `eigenvalue_dichotomy_toEuclideanCLM_M1_tightened` —
  for every eigenvalue `mu` of `toEuclideanCLM M1`,
  `(2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (1.0 ≤ mu ∧ mu ≤ 1.2)` — by exactly the Wave-5
  pattern `rcases eigenvalue_eq_lambdaMax_or_lambda2 _
  toEuclideanCLM_M1_isSymmetric finrank_E_eq_two hmu with h | h`,
  substituting `lambdaMax_M1_bracket` (`[2.9, 3.1]`, UNCHANGED from
  Wave-4/Wave-5) into the first case and the Wave-6
  `lambda2_toEuclideanCLM_M1_bracket` (`[1.0, 1.2]`, strictly narrower
  than Wave-5's `lambda2_M1_bracket_from_compose : [0.7, 1.3]`) into the
  second, then `linarith`.

  WHY THE SECOND INTERVAL IS TIGHTER (not a coincidence, this is the
  whole point of the test). `YMCapstoneEigvalDichotomy.lean` (Wave-5)
  used `lambda2_M1_bracket_from_compose : [7/10, 13/10] = [0.7, 1.3]`
  (half-width `0.3`), obtained via a Lipschitz estimate on `lambda2`
  itself composed against `‖M1 - M2‖ = 1/10`. `YMCapstoneTraceM1Exact.lean`
  (Wave-6) instead computes `trace (toEuclideanCLM M1) = 4.1` EXACTLY
  (summing the two diagonal entries `2` and `2.1` of `M1` directly, no
  Lipschitz estimate on the trace needed), then combines that exact trace
  with the UNCHANGED `lambdaMax_M1_bracket : [2.9, 3.1]` via
  `lambda2 T = trace T - lambdaMax T` to get
  `lambda2 (toEuclideanCLM M1) ∈ [4.1 - 3.1, 4.1 - 2.9] = [1.0, 1.2]`
  (half-width `0.1`), strictly inside `[0.7, 1.3]`
  (`0.7 ≤ 1.0` and `1.2 ≤ 1.3`, both strict). Since the two-eigenvalue
  exhaustiveness dichotomy `eigenvalue_eq_lambdaMax_or_lambda2` (Wave-4,
  SHARED-4A) is unchanged, substituting the tighter `lambda2` bracket into
  its second case directly tightens the overall eigenvalue dichotomy for
  `toEuclideanCLM M1`, exactly as this item's task specifies.

  RELATION TO WAVE-5/WAVE-6 (both named files read in full, NEITHER
  imported/modified). This file reuses, BYTE-FOR-BYTE REPRODUCED (never
  imported — see BUILD-SYSTEM NOTE below for why, identical reasoning to
  every prior Wave-2..Wave-6 sibling that faces the same free-standing-
  file constraint):
    - `E`, `lambdaMax`, `lambdaMax_hasEigenvalue`, `M2` chain
      (`M2_isHermitian` .. `lambdaMax_grounded_eq_three`), `basis2`,
      `lambda2`, `M1`, `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
      `sonda2_numeric_norm`, `bddAbove_rayleighQuotient_subtype`,
      `lambdaMax_lipschitz`, `stability_compose_lambdaMax`,
      `lambdaMax_M1_bracket`, `M1_isHermitian`,
      `toEuclideanCLM_M1_isSymmetric`, `finrank_E_eq_two`,
      `lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`,
      `eigenvalue_eq_lambdaMax_or_lambda2` — verbatim from
      `YMCapstoneEigvalDichotomy.lean` (Wave-5).
    - `trace_toEuclideanCLM_M1_eq_four_point_one`,
      `lambda2_toEuclideanCLM_M1_bracket` (the tightened `[1.0, 1.2]`
      bracket) — verbatim from `YMCapstoneTraceM1Exact.lean` (Wave-6),
      in place of Wave-5's own `lambda2_M1_bracket_from_compose`
      (`[0.7, 1.3]`); this is the ONE substantively new ingredient
      relative to `YMCapstoneEigvalDichotomy.lean`.
  Neither `YMCapstoneEigvalDichotomy.lean` nor
  `YMCapstoneTraceM1Exact.lean` is touched or modified; both are
  read-only source material.

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). Identical situation and identical reasoning to every prior
  Wave-2..Wave-6 sibling in this directory: neither file named above is
  registered in `TamesisLab.lean` (neither lives inside the
  `[[lean_lib]] name = "TamesisLab"` module graph declared in
  `lakefile.toml`), so neither has a built `.olean` importable by module
  path. Per the Wave-7 task instructions ("do NOT touch any file outside
  your own new file(s)"), this file cannot register either into the
  library graph. The only way to reuse their declarations under this
  constraint is to reproduce them verbatim.

  MATHLIB TOOLS USED — none new beyond what `YMCapstoneEigvalDichotomy.lean`
  and `YMCapstoneTraceM1Exact.lean` already cite in their own headers (see
  those two files for the exact Mathlib file/line citations for every
  reproduced name). This file adds no new citation; the only genuinely
  new step is the final combination `rcases
  eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
  finrank_E_eq_two hmu with h | h`, followed by `rw`/`exact` against the
  two already-closed brackets, exactly per this item's own falsifiable-
  test wording.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT.
  `eigenvalue_dichotomy_toEuclideanCLM_M1_tightened` proves: for every
  eigenvalue `mu` of `toEuclideanCLM M1`,
  `(2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (1.0 ≤ mu ∧ mu ≤ 1.2)`. This is genuinely
  EXHAUSTIVE for `toEuclideanCLM M1` (via
  `eigenvalue_eq_lambdaMax_or_lambda2`, reproduced from Wave-4/Wave-5):
  since `dim E = 2`, `M1` (symmetric) has EXACTLY two eigenvalues counted
  with the sorted-eigenvalue-family convention, and both are now pinned
  to disjoint numeric intervals strictly narrower, on the second
  interval, than the Wave-5 result.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-7 instructions). This remains the same single hand-picked `2×2`
  toy matrix pair (`M1`, `M2`) already used throughout the
  Wave-3..Wave-6 `YM-STABILITY`/`YM-CAPSTONE` lineage; nothing here is
  about SU(N), any lattice-gauge action, reflection positivity, or the
  continuum limit. The `lambdaMax` half of the dichotomy (`[2.9, 3.1]`)
  is UNCHANGED from Wave-4/Wave-5 — only the `lambda2` half is tightened
  here (via the already-closed Wave-6 bracket), from half-width `0.3` to
  half-width `0.1`. This file says nothing about Yang-Mills, does not
  approximate a solution to the Clay mass-gap problem or any other
  Millennium problem, and claims no mathematical novelty — combining an
  already-proved exhaustive two-eigenvalue case split with two
  already-proved numeric brackets via `rcases`/`rw`/`exact` is routine
  proof composition, not a new mathematical result.

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

namespace YMCapstoneEigvalDichotomyTightened

/-! ### Part 0a — verbatim reproduction of `YMCapstoneEigvalDichotomy`'s
`E`, `lambdaMax`, `lambdaMax_hasEigenvalue`. -/

/-- The fixed finite-dimensional real inner product space (verbatim from
`YMCapstoneEigvalDichotomy.E`). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the fixed
space `E` (verbatim from `YMCapstoneEigvalDichotomy.lambdaMax`). -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`
(verbatim from `YMCapstoneEigvalDichotomy.lambdaMax_hasEigenvalue`). -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Part 0b — verbatim reproduction of the `M2` chain (originally from
`YM1.TransferGapSpectrum` / `YM1.TransferGap`): `M2`, `M2_isHermitian`,
`M2_charpoly_eval`, `M2_spectrum_real`, `M2_spectrum_eq`,
`M2_eigen_three`. -/

/-- The toy 2×2 "transfer matrix" (verbatim value). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

theorem M2_isHermitian : M2.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M2, Matrix.conjTranspose_apply]

theorem M2_charpoly_eval (r : ℝ) :
    M2.charpoly.eval r = (r - 3) * (r - 1) := by
  have h00 : M2 0 0 = 2 := rfl
  have h01 : M2 0 1 = 1 := rfl
  have h10 : M2 1 0 = 1 := rfl
  have h11 : M2 1 1 = 2 := rfl
  rw [Matrix.eval_charpoly, Matrix.det_fin_two]
  simp [Matrix.sub_apply, Matrix.scalar_apply, h00, h01, h10, h11]
  ring

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

theorem M2_spectrum_eq : spectrum ℝ M2 = ({1, 3} : Set ℝ) := by
  ext r
  rw [M2_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

theorem M2_eigen_three : M2.mulVec ![1, 1] = (3 : ℝ) • ![1, 1] := by
  ext i
  fin_cases i <;>
    simp [M2, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-! ### Part 0c — verbatim reproduction of the rest of the abstract-
spectrum route to `lambdaMax (toEuclideanCLM M2) = 3`. -/

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

/-- The vector `v = (1,1) ∈ E` (verbatim). -/
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

/-- **Wave-3 YM-STABILITY-GROUNDED result, reproduced verbatim.**
`lambdaMax (toEuclideanCLM M2) = 3` exactly. -/
theorem lambdaMax_grounded_eq_three :
    lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 3 := by
  rcases lambdaMax_mem_one_three with h1 | h3
  · exfalso
    have := lambdaMax_ge_three
    rw [h1] at this
    linarith
  · exact h3

/-! ### Part 0d — verbatim reproduction of `basis2`, `lambda2`. -/

/-- The fixed orthonormal basis of `E`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `lambda2 T := trace T - lambdaMax T`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-! ### Part 1 — verbatim reproduction of `M1`, `sonda1_bridge`,
`diff_eq_diagonal`, `pi_norm_vec`, `sonda2_numeric_norm`,
`bddAbove_rayleighQuotient_subtype`, `lambdaMax_lipschitz`,
`stability_compose_lambdaMax`, `lambdaMax_M1_bracket`, `M1_isHermitian`,
`toEuclideanCLM_M1_isSymmetric`, `finrank_E_eq_two`. -/

/-- The perturbed matrix `M1`. -/
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

theorem stability_compose_lambdaMax :
    |lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 1 / 10 :=
  (lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact sonda2_numeric_norm.le)

/-- **Wave-4 YM-CAPSTONE-BRACKET result, reproduced verbatim, UNCHANGED
across Wave-4/5/6/7.** `lambdaMax (toEuclideanCLM M1)` lies in the numeric
interval `[2.9, 3.1]`. -/
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

/-! ### Part 2 — verbatim reproduction of `YMCapstoneTraceM1Exact`'s
`trace_toEuclideanCLM_M1_eq_four_point_one` and
`lambda2_toEuclideanCLM_M1_bracket` (Wave-6): the NEW, tightened `lambda2`
bracket `[1.0, 1.2]` this item's task specifies, in place of Wave-5's
wider `lambda2_M1_bracket_from_compose : [0.7, 1.3]`. -/

/-- **Wave-6 YM-CAPSTONE-TRACE-M1-EXACT result, reproduced verbatim.**
`trace (toEuclideanCLM M1 : E →ₗ[ℝ] E) = 4.1`, computed by expanding the
trace over `basis2` and evaluating the resulting 2-term sum:
`M1 0 0 + M1 1 1 = 2 + 2.1 = 4.1`. Byte-identical (proof included) to
`trace_toEuclideanCLM_M1_eq_four_point_one` in
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

/-- **Wave-6 YM-CAPSTONE-TRACE-M1-EXACT result, reproduced verbatim — the
NEW, tightened `lambda2` bracket this item's task specifies.**
`lambda2 (toEuclideanCLM M1)` lies in the numeric interval `[1.0, 1.2]`,
strictly narrower than Wave-5's `[0.7, 1.3]`. Byte-identical (proof
included) to `lambda2_toEuclideanCLM_M1_bracket` in
`YMCapstoneTraceM1Exact.lean`. -/
theorem lambda2_toEuclideanCLM_M1_bracket :
    1.0 ≤ lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 1.2 := by
  unfold lambda2
  rw [trace_toEuclideanCLM_M1_eq_four_point_one]
  obtain ⟨hlo, hhi⟩ := lambdaMax_M1_bracket
  constructor <;> linarith

/-! ### Part 3 — verbatim reproduction of `TwoEigenvalueExhaustiveness.lean`
(Wave-4, `SHARED4A`, also reproduced in `YMCapstoneEigvalDichotomy.lean`,
Wave-5): the two-eigenvalue exhaustiveness dichotomy
`eigenvalue_eq_lambdaMax_or_lambda2`, via its two supporting promoted
lemmas `lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one`. -/

/-- **Promotion of `heq0`, reproduced verbatim.** For symmetric `T` on the
fixed 2-dimensional `E`, `lambdaMax T` coincides with the `0`-th (largest)
entry of Mathlib's sorted eigenvalue family `hT.eigenvalues hn`. -/
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

/-- **Promotion of `hlambda2`, reproduced verbatim.** For symmetric `T` on
the fixed 2-dimensional `E`, `lambda2 T` coincides with the `1`-st
(smaller) entry of Mathlib's sorted eigenvalue family `hT.eigenvalues hn`. -/
theorem lambda2_eq_eigenvalues_one (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T = hT.eigenvalues hn 1 := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  unfold lambda2
  rw [htrace, heq0]; ring

/-- **Wave-4 SHARED-4A result, reproduced verbatim.** Two-eigenvalue
exhaustiveness in dimension 2: for symmetric `T : E →L[ℝ] E` on the fixed
2-dimensional `E`, EVERY eigenvalue `mu` of `T` equals either `lambdaMax
T` or `lambda2 T` — there is no third possibility. -/
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
(YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED): the falsifiable test as stated,
combining `eigenvalue_eq_lambdaMax_or_lambda2` (Part 3) with the two
already-closed numeric brackets `lambdaMax_M1_bracket` (Part 1, UNCHANGED)
and the TIGHTENED `lambda2_toEuclideanCLM_M1_bracket` (Part 2), applied to
`T = toEuclideanCLM M1`. -/

/-- **Main new result (YM-CAPSTONE-EIGVAL-DICHOTOMY-TIGHTENED), the
falsifiable test as stated.** Every eigenvalue `mu` of `toEuclideanCLM M1`
lies in `[2.9, 3.1]` or in `[1.0, 1.2]` — no third possibility, strictly
narrower on the second disjunct than the Wave-5
`eigenvalue_dichotomy_toEuclideanCLM_M1` (`[2.9,3.1]` or `[0.7,1.3]`). -/
theorem eigenvalue_dichotomy_toEuclideanCLM_M1_tightened
    {mu : ℝ} (hmu : Module.End.HasEigenvalue
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E) mu) :
    (2.9 ≤ mu ∧ mu ≤ 3.1) ∨ (1.0 ≤ mu ∧ mu ≤ 1.2) := by
  rcases eigenvalue_eq_lambdaMax_or_lambda2 _ toEuclideanCLM_M1_isSymmetric
      finrank_E_eq_two hmu with h | h
  · left
    rw [h]
    exact lambdaMax_M1_bracket
  · right
    rw [h]
    exact lambda2_toEuclideanCLM_M1_bracket

end YMCapstoneEigvalDichotomyTightened

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_hasEigenvalue
#print axioms YMCapstoneEigvalDichotomyTightened.M2_isHermitian
#print axioms YMCapstoneEigvalDichotomyTightened.M2_charpoly_eval
#print axioms YMCapstoneEigvalDichotomyTightened.M2_spectrum_real
#print axioms YMCapstoneEigvalDichotomyTightened.M2_spectrum_eq
#print axioms YMCapstoneEigvalDichotomyTightened.M2_eigen_three
#print axioms YMCapstoneEigvalDichotomyTightened.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneEigvalDichotomyTightened.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneEigvalDichotomyTightened.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_mem_one_three
#print axioms YMCapstoneEigvalDichotomyTightened.v_ne_zero
#print axioms YMCapstoneEigvalDichotomyTightened.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneEigvalDichotomyTightened.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_ge_three
#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_grounded_eq_three
#print axioms YMCapstoneEigvalDichotomyTightened.sonda1_bridge
#print axioms YMCapstoneEigvalDichotomyTightened.diff_eq_diagonal
#print axioms YMCapstoneEigvalDichotomyTightened.pi_norm_vec
#print axioms YMCapstoneEigvalDichotomyTightened.sonda2_numeric_norm
#print axioms YMCapstoneEigvalDichotomyTightened.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_lipschitz
#print axioms YMCapstoneEigvalDichotomyTightened.stability_compose_lambdaMax
#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_M1_bracket
#print axioms YMCapstoneEigvalDichotomyTightened.M1_isHermitian
#print axioms YMCapstoneEigvalDichotomyTightened.toEuclideanCLM_M1_isSymmetric
#print axioms YMCapstoneEigvalDichotomyTightened.finrank_E_eq_two
#print axioms YMCapstoneEigvalDichotomyTightened.trace_toEuclideanCLM_M1_eq_four_point_one
#print axioms YMCapstoneEigvalDichotomyTightened.lambda2_toEuclideanCLM_M1_bracket
#print axioms YMCapstoneEigvalDichotomyTightened.lambdaMax_eq_eigenvalues_zero
#print axioms YMCapstoneEigvalDichotomyTightened.lambda2_eq_eigenvalues_one
#print axioms YMCapstoneEigvalDichotomyTightened.eigenvalue_eq_lambdaMax_or_lambda2
#print axioms YMCapstoneEigvalDichotomyTightened.eigenvalue_dichotomy_toEuclideanCLM_M1_tightened
