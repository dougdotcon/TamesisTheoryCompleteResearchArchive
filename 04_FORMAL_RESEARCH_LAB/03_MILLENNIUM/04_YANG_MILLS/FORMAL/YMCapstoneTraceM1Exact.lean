/-
  YM-CAPSTONE-TRACE-M1-EXACT — exact trace of `M1`, narrowed bracket for
  `lambda2 (toEuclideanCLM M1)` (Wave-6 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-6 task instructions on
  build contention with 13 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1..Wave-5 file in this directory. This file does NOT modify
  any other file; it only READS `YMCapstoneDetBracket.lean`,
  `YMCapstoneEigvalDichotomy.lean` (Wave-5), `YMCapstoneBracket.lean`
  (Wave-4), and `YMCapstoneFull.lean` (Wave-4), all in this same
  directory.

  EXACT TASK ATTEMPTED (per the Wave-6 work-item prompt for
  `WAVE6-YM-CAPSTONE-TRACE-M1-EXACT`, candidate
  `YM-CAPSTONE-TRACE-M1-EXACT`). Nothing broader than this was attempted:
  prove `trace_toEuclideanCLM_M1_eq_four_point_one` following the EXACT
  pattern of `trace_toEuclideanCLM_M2_eq_four`
  (`YMCapstoneFull.lean`) — `LinearMap.trace_eq_sum_inner` +
  `Matrix.inner_toEuclideanCLM` + `Fin.sum_univ_two` + `norm_num` — then
  derive a numeric bracket `1.0 ≤ lambda2 (toEuclideanCLM M1) ≤ 1.2` via
  `unfold lambda2; rw [...]; constructor <;> linarith`, exactly as the
  plan specified.

  WHY THIS CLOSES SOMETHING THE WAVE-4 `YMCapstoneFull.lean` GAP
  DIAGNOSIS COULD NOT. `YMCapstoneFull.lean`'s own "PASSO 2 — GAP
  DIAGNOSIS" comment block explains in detail why combining
  `lambdaMax_M1_bracket` (`YMCapstoneBracket.lean`, Wave-4,
  `2.9 ≤ lambdaMax (toEuclideanCLM M1) ≤ 3.1`) with the definition
  `lambda2 T := trace T - lambdaMax T` was NOT possible there: no fact in
  that file's lineage bounded or computed `trace (toEuclideanCLM M1)`
  independently of `lambda2 (toEuclideanCLM M1)` itself, so the
  `lambdaMax` bracket alone said nothing about `lambda2`. This file
  supplies exactly that missing ingredient: an EXACT value for
  `trace (toEuclideanCLM M1) = 4.1` (computed directly, the same way
  `trace_toEuclideanCLM_M2_eq_four` computes `trace (toEuclideanCLM M2) =
  4`, by summing diagonal entries over the fixed orthonormal basis — no
  Lipschitz estimate involved, since `M1`'s own two diagonal entries
  `2` and `2.1` are known exactly from its definition). With that exact
  trace in hand, `lambda2 (toEuclideanCLM M1) = 4.1 - lambdaMax
  (toEuclideanCLM M1)` combines directly with the ALREADY-established
  `lambdaMax_M1_bracket` (`[2.9, 3.1]`) to give
  `lambda2 (toEuclideanCLM M1) ∈ [4.1 - 3.1, 4.1 - 2.9] = [1.0, 1.2]` —
  a bracket of half-width `0.1`, strictly narrower than the `[0.7, 1.3]`
  (half-width `0.3`) obtained in `YMCapstoneFull.lean`'s
  `lambda2_M1_bracket_from_compose` via the indirect Lipschitz-composition
  route on `lambda2` itself. Both brackets are consistent (`[1.0, 1.2] ⊆
  [0.7, 1.3]`), as expected since the new one uses strictly more
  information (an exact trace, not just a Lipschitz estimate on
  `lambda2`).

  RELATION TO WAVE-4 / WAVE-5 (all read in full, NONE imported/modified).
  This file reuses, BYTE-FOR-BYTE REPRODUCED (never imported — see the
  "BUILD-SYSTEM NOTE" below for why, identical reasoning to every prior
  Wave-2..Wave-5 sibling that faces the same free-standing-file
  constraint), the following declarations:
    - `E`, `bddAbove_rayleighQuotient_subtype`, `lambdaMax_hasEigenvalue`,
      `M2`, `M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`,
      `M2_spectrum_eq`, `M2_eigen_three`, `toEuclideanCLM_M2_spectrum_eq`,
      `toEuclideanCLM_M2_endSpectrum_eq`, `toEuclideanCLM_M2_isSymmetric`,
      `lambdaMax_mem_one_three`, `v`, `v_ne_zero`,
      `toEuclideanCLM_M2_apply_v`, `toEuclideanCLM_M2_rayleighQuotient_v`,
      `lambdaMax_ge_three`, `lambdaMax_grounded_eq_three`, `M1`,
      `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
      `sonda2_numeric_norm`, `stability_compose_lambdaMax`,
      `lambdaMax_M1_bracket` — verbatim from `YMCapstoneBracket.lean`
      (Wave-4, `YMCapstoneBracket`, itself verbatim from
      `YMStabilityCompose.lean` / `StabilityGrounded.lean`, Wave-3).
    - `lambdaMax` (the `def`) and `lambdaMax_lipschitz` — verbatim from
      `YMCapstoneFull.lean` (Wave-4, `YMCapstoneFull`, Part 2's
      reproduction, which is the version that coexists correctly with
      `open Matrix`, unlike the `YMCapstoneBracket.lean` version which
      deliberately avoids `open Matrix` — see "WHY `open Matrix` HERE"
      below).
    - `basis2`, `lambda2` — verbatim from `YMCapstoneFull.lean` (Wave-4,
      Part 0d, itself verbatim from `YMStabilityCompose.lean`, Wave-3,
      itself verbatim from `SecondEigenvalueLipschitz.lean`, Wave-2,
      SHARED-2A).
  None of `YMCapstoneBracket.lean`, `YMCapstoneFull.lean`,
  `YMCapstoneDetBracket.lean`, or `YMCapstoneEigvalDichotomy.lean` is
  touched or modified; all are read-only source material. (The latter two
  Wave-5 files were read in full per the task instructions but turn out
  not to supply any NEW ingredient this file needs beyond what
  `YMCapstoneBracket.lean`/`YMCapstoneFull.lean` (Wave-4) already provide
  — `YMCapstoneDetBracket.lean` brackets `det (toEuclideanCLM M1)` and
  `YMCapstoneEigvalDichotomy.lean` establishes an eigenvalue dichotomy for
  `M1`, neither of which this file's falsifiable test needs.)

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). Identical situation and identical reasoning to every prior
  Wave-2..Wave-5 sibling in this directory: none of the four files named
  above is registered in `TamesisLab.lean` (none lives inside the
  `[[lean_lib]] name = "TamesisLab"` module graph declared in
  `lakefile.toml`), so none has a built `.olean` importable by module
  path. Per the Wave-6 task instructions ("do NOT touch any file outside
  your own new file(s)"), this file cannot register any of them into the
  library graph either. The only way to reuse their declarations under
  this constraint is to reproduce them verbatim.

  WHY `open Matrix` HERE, AND WHY THE `lambdaMax_lipschitz` PROOF IS TAKEN
  FROM `YMCapstoneFull.lean` RATHER THAN `YMCapstoneBracket.lean`.
  `YMCapstoneBracket.lean` deliberately avoids `open Matrix` because its
  `lambdaMax_lipschitz` proof cites the bare identifier `sub_apply` in a
  `simp` set, which becomes ambiguous against `Matrix.sub_apply` once
  `Matrix` is opened (documented in that file's own header). This file
  NEEDS `open Matrix` for the mandatory `⬝ᵥ`/`*ᵥ` infix notation used by
  the new `trace_toEuclideanCLM_M1_eq_four_point_one` proof below (the
  same `scoped infixr` situation `YMCapstoneFull.lean`'s header documents
  for `trace_toEuclideanCLM_M2_eq_four`, verified again here by the same
  direct grep of `Mathlib/Data/Matrix/Mul.lean` in the vendored
  snapshot). `YMCapstoneFull.lean` already solved exactly this
  conflict for its own PASSO-2 reproduction of `lambdaMax_lipschitz`: its
  version of the `hsub` step omits `sub_apply` from the `simp` set
  entirely (relying on `ContinuousLinearMap.rayleighQuotient`,
  `ContinuousLinearMap.reApplyInnerSelf_apply`, `inner_sub_left`,
  `sub_div` alone to close the goal, which `simp` manages unaided), so it
  coexists correctly with `open Matrix`. That version (byte-identical
  proof to `YMCapstoneFull.lean`'s Part-2 `lambdaMax_lipschitz`) is
  reproduced below instead of `YMCapstoneBracket.lean`'s.

  MATHLIB TOOLS USED — no new citation beyond what
  `YMCapstoneFull.lean` and `YMCapstoneBracket.lean` already establish in
  their own headers (`LinearMap.trace_eq_sum_inner`,
  `Matrix.inner_toEuclideanCLM`, `EuclideanSpace.basisFun_apply`,
  `Fin.sum_univ_two`, `abs_le`, all already cited there with exact
  Mathlib file/line references against the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`).

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT.
  `trace_toEuclideanCLM_M1_eq_four_point_one` proves
  `(toEuclideanCLM M1 : E →ₗ[ℝ] E).trace ℝ E = 4.1` by the identical
  method `trace_toEuclideanCLM_M2_eq_four` uses for `M2`: expanding the
  trace over the fixed orthonormal basis `basis2` via
  `trace_eq_sum_inner`, rewriting each term to a `Matrix`
  dot-product/mulVec expression via `inner_toEuclideanCLM`, identifying
  each basis vector as `EuclideanSpace.single i 1` via the named-argument
  `basisFun_apply`, and evaluating the resulting 2-term sum:
  `M1 0 0 + M1 1 1 = 2 + 2.1 = 4.1`.
  `lambda2_toEuclideanCLM_M1_bracket` then combines this exact trace with
  the already-established `lambdaMax_M1_bracket` (`[2.9, 3.1]`) via
  `unfold lambda2; rw [trace_toEuclideanCLM_M1_eq_four_point_one];
  constructor <;> linarith` to conclude
  `1.0 ≤ lambda2 (toEuclideanCLM M1) ≤ 1.2` exactly as the falsifiable
  test specified.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-6 instructions). This remains a single hand-picked `2×2` toy
  matrix (`M1`, `M2`); nothing here is about SU(N), any lattice-gauge
  action, reflection positivity, or the continuum limit. The bracket
  `[1.0, 1.2]` is still not the exact value of `lambda2 (toEuclideanCLM
  M1)` — only `lambdaMax (toEuclideanCLM M1)` was bracketed (not computed
  exactly) in the Wave-4 lineage this file builds on, so the resulting
  `lambda2` bracket inherits that same half-width `0.1` slack. This file
  says nothing about Yang-Mills, does not approximate a solution to the
  Clay mass-gap problem, and claims no mathematical novelty — computing
  the trace of a `2×2` symmetric matrix as the sum of its diagonal
  entries via an orthonormal-basis expansion, and subtracting a bracketed
  top eigenvalue, is classical, elementary linear algebra.

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

namespace YMCapstoneTraceM1Exact

/-! ### Part 0 — verbatim reproduction of `E`, `lambdaMax` (with its
supporting lemmas), `M2`'s spectral chain, `M1`, and the Lipschitz
composition bracket `lambdaMax_M1_bracket`, from `YMCapstoneBracket.lean`
(Wave-4) / `YMCapstoneFull.lean` (Wave-4). -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim.** `lambdaMax` is 1-Lipschitz
in operator norm on the fixed space `E`. Byte-identical (proof included)
to the Part-2 reproduction of `lambdaMax_lipschitz` in
`YMCapstoneFull.lean` (the version that coexists with `open Matrix`; see
file header "WHY `open Matrix` HERE"). -/
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

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`.
Byte-identical to `lambdaMax_hasEigenvalue` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- `M2`, byte-for-byte identical across `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean` (and their own Wave-3/Wave-2/Wave-1 ancestors). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-- The perturbed matrix `M1`. Byte-identical to `M1` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

/-- **Sonda 1, part b, reproduced verbatim.** `Matrix.l2_opNorm_toEuclideanCLM`
rewrites `‖toEuclideanCLM M1 - toEuclideanCLM M2‖` to `‖M1 - M2‖`.
Byte-identical (proof included) to `sonda1_bridge` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem sonda1_bridge :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 -
        Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2‖ = ‖M1 - M2‖ := by
  rw [← map_sub (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2))]
  exact Matrix.l2_opNorm_toEuclideanCLM (M1 - M2)

/-- `M1 - M2` is the diagonal matrix `diagonal ![0, 1/10]`. Byte-identical
to `diff_eq_diagonal` in `YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem diff_eq_diagonal : M1 - M2 = Matrix.diagonal ![(0 : ℝ), 1 / 10] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [M1, M2]

/-- The Pi *sup*-norm of the concrete vector `![0, 1/10]` is exactly
`1/10`. Byte-identical to `pi_norm_vec` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem pi_norm_vec : ‖(![(0 : ℝ), 1 / 10] : Fin 2 → ℝ)‖ = 1 / 10 := by
  apply le_antisymm
  · rw [pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 10)]
    intro i
    fin_cases i <;> norm_num
  · have := norm_le_pi_norm (![(0 : ℝ), 1 / 10] : Fin 2 → ℝ) 1
    simpa using this

/-- **Sonda 2, closed exactly, reproduced verbatim.** The
`Matrix.Norms.L2Operator`-scoped operator norm of `M1 - M2` is exactly
`1/10`. Byte-identical (proof included) to `sonda2_numeric_norm` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem sonda2_numeric_norm : ‖M1 - M2‖ = 1 / 10 := by
  rw [diff_eq_diagonal, Matrix.l2_opNorm_diagonal]
  exact pi_norm_vec

/-- **Wave-3 YM-STABILITY-COMPOSE result, reproduced verbatim.** Byte-
identical (proof included) to `stability_compose_lambdaMax` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem stability_compose_lambdaMax :
    |lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 1 / 10 :=
  (lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact sonda2_numeric_norm.le)

/-- `M2` is Hermitian. Byte-identical to `M2_isHermitian` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem M2_isHermitian : M2.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M2, Matrix.conjTranspose_apply]

/-- The characteristic polynomial of `M2`, evaluated at any real `r`, equals
`(r - 3) * (r - 1)`. Byte-identical to `M2_charpoly_eval` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
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
Byte-identical to `M2_spectrum_real` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
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

/-- The real spectrum of `M2` is exactly `{1, 3}`. Byte-identical to
`M2_spectrum_eq` in `YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem M2_spectrum_eq : spectrum ℝ M2 = ({1, 3} : Set ℝ) := by
  ext r
  rw [M2_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

/-- `v₁ = (1,1)` is an eigenvector of `M2` with eigenvalue `3`.
Byte-identical to `M2_eigen_three` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem M2_eigen_three : M2.mulVec ![1, 1] = (3 : ℝ) • ![1, 1] := by
  ext i
  fin_cases i <;>
    simp [M2, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-- The closed-form abstract spectrum of `toEuclideanCLM M2`. Byte-identical
to `toEuclideanCLM_M2_spectrum_eq` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem toEuclideanCLM_M2_spectrum_eq :
    spectrum ℝ (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      = ({1, 3} : Set ℝ) := by
  rw [AlgEquiv.spectrum_eq (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2)) M2]
  exact M2_spectrum_eq

/-- Transported to the `Module.End ℝ E` spectrum. Byte-identical to
`toEuclideanCLM_M2_endSpectrum_eq` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem toEuclideanCLM_M2_endSpectrum_eq :
    spectrum ℝ ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      : Module.End ℝ E) = ({1, 3} : Set ℝ) := by
  rw [← ContinuousLinearMap.spectrum_eq]
  exact toEuclideanCLM_M2_spectrum_eq

/-- `(toEuclideanCLM M2 : E →ₗ[ℝ] E).IsSymmetric`, transported from
`M2_isHermitian`. Byte-identical to `toEuclideanCLM_M2_isSymmetric` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
theorem toEuclideanCLM_M2_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M2_isHermitian

/-- `lambdaMax (toEuclideanCLM M2) ∈ {1, 3}`. Byte-identical to
`lambdaMax_mem_one_three` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
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

/-- The vector `v = (1,1) ∈ E`. Byte-identical to `v` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
noncomputable def v : E := WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)

/-- Byte-identical to `v_ne_zero` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem v_ne_zero : v ≠ 0 := by
  intro h
  have h0 : (WithLp.equiv 2 (Fin 2 → ℝ)) v 0 = (WithLp.equiv 2 (Fin 2 → ℝ)) (0 : E) 0 := by
    rw [h]
  simp [v, WithLp.equiv] at h0

/-- `toEuclideanCLM M2` applied to `v` equals `(3:ℝ) • v`. Byte-identical
to `toEuclideanCLM_M2_apply_v` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem toEuclideanCLM_M2_apply_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) v = (3 : ℝ) • v := by
  show (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
      (WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)) = (3 : ℝ) • v
  rw [Matrix.toEuclideanCLM_toLp, M2_eigen_three]
  rfl

/-- The Rayleigh quotient of `toEuclideanCLM M2` at the explicit
eigenvector `v` is exactly `3`. Byte-identical to
`toEuclideanCLM_M2_rayleighQuotient_v` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem toEuclideanCLM_M2_rayleighQuotient_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2).rayleighQuotient v = 3 := by
  have hvnorm : ‖v‖ ≠ 0 := norm_ne_zero_iff.mpr v_ne_zero
  rw [ContinuousLinearMap.rayleighQuotient, ContinuousLinearMap.reApplyInnerSelf_apply,
    toEuclideanCLM_M2_apply_v, real_inner_smul_left, real_inner_self_eq_norm_sq]
  rw [RCLike.re_to_real]
  field_simp

/-- `lambdaMax (toEuclideanCLM M2) ≥ 3`. Byte-identical to
`lambdaMax_ge_three` in `YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
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
`lambdaMax (toEuclideanCLM M2) = 3` exactly. Byte-identical (proof
included) to `lambdaMax_grounded_eq_three` in `YMCapstoneBracket.lean` /
`YMCapstoneFull.lean`. -/
theorem lambdaMax_grounded_eq_three :
    lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 3 := by
  rcases lambdaMax_mem_one_three with h1 | h3
  · exfalso
    have := lambdaMax_ge_three
    rw [h1] at this
    linarith
  · exact h3

/-- **Wave-4 YM-CAPSTONE-BRACKET result, reproduced verbatim.**
`lambdaMax (toEuclideanCLM M1)` lies in the numeric interval `[2.9, 3.1]`.
Byte-identical (proof included) to `lambdaMax_M1_bracket` in
`YMCapstoneBracket.lean`. -/
theorem lambdaMax_M1_bracket :
    2.9 ≤ lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 3.1 := by
  have h := stability_compose_lambdaMax
  rw [lambdaMax_grounded_eq_three] at h
  rw [abs_le] at h
  constructor <;> linarith

/-! ### Part 1 — verbatim reproduction of `basis2`, `lambda2` from
`YMCapstoneFull.lean` (Wave-4, Part 0d). -/

/-- The fixed orthonormal basis of `E` the falsifiable test's trace
computation needs. Byte-identical to `basis2` in `YMCapstoneFull.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`YMCapstoneFull.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-! ### Part 2 — new content specific to this item
(YM-CAPSTONE-TRACE-M1-EXACT). -/

/-- **New falsifiable result, main computation.**
`trace (toEuclideanCLM M1 : E →ₗ[ℝ] E) = 4.1`, computed by expanding the
trace over `basis2` (`LinearMap.trace_eq_sum_inner`), rewriting each term
via `Matrix.inner_toEuclideanCLM` to a concrete `Matrix` dot-product/
mulVec expression, identifying each basis vector as
`EuclideanSpace.single i 1` via the NAMED-argument
`EuclideanSpace.basisFun_apply (ι := Fin 2) (𝕜 := ℝ) i`, and evaluating
the resulting 2-term sum: `M1 0 0 + M1 1 1 = 2 + 2.1 = 4.1`. EXACT same
proof shape as `trace_toEuclideanCLM_M2_eq_four` in `YMCapstoneFull.lean`,
substituting `M1` for `M2` and `4.1` for `4`. -/
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

/-- **Main result (YM-CAPSTONE-TRACE-M1-EXACT), the falsifiable test's
target.** `lambda2 (toEuclideanCLM M1)` lies in the numeric interval
`[1.0, 1.2]`, obtained by substituting the exact trace
`trace_toEuclideanCLM_M1_eq_four_point_one` into `lambda2`'s definition
and combining with `lambdaMax_M1_bracket` (`[2.9, 3.1]`), via exactly
`unfold lambda2; rw [trace_toEuclideanCLM_M1_eq_four_point_one];
constructor <;> linarith`, as the falsifiable test specified. -/
theorem lambda2_toEuclideanCLM_M1_bracket :
    1.0 ≤ lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 1.2 := by
  unfold lambda2
  rw [trace_toEuclideanCLM_M1_eq_four_point_one]
  obtain ⟨hlo, hhi⟩ := lambdaMax_M1_bracket
  constructor <;> linarith

end YMCapstoneTraceM1Exact

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneTraceM1Exact.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneTraceM1Exact.lambdaMax_lipschitz
#print axioms YMCapstoneTraceM1Exact.lambdaMax_hasEigenvalue
#print axioms YMCapstoneTraceM1Exact.sonda1_bridge
#print axioms YMCapstoneTraceM1Exact.diff_eq_diagonal
#print axioms YMCapstoneTraceM1Exact.pi_norm_vec
#print axioms YMCapstoneTraceM1Exact.sonda2_numeric_norm
#print axioms YMCapstoneTraceM1Exact.stability_compose_lambdaMax
#print axioms YMCapstoneTraceM1Exact.M2_isHermitian
#print axioms YMCapstoneTraceM1Exact.M2_charpoly_eval
#print axioms YMCapstoneTraceM1Exact.M2_spectrum_real
#print axioms YMCapstoneTraceM1Exact.M2_spectrum_eq
#print axioms YMCapstoneTraceM1Exact.M2_eigen_three
#print axioms YMCapstoneTraceM1Exact.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneTraceM1Exact.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneTraceM1Exact.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneTraceM1Exact.lambdaMax_mem_one_three
#print axioms YMCapstoneTraceM1Exact.v_ne_zero
#print axioms YMCapstoneTraceM1Exact.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneTraceM1Exact.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneTraceM1Exact.lambdaMax_ge_three
#print axioms YMCapstoneTraceM1Exact.lambdaMax_grounded_eq_three
#print axioms YMCapstoneTraceM1Exact.lambdaMax_M1_bracket
#print axioms YMCapstoneTraceM1Exact.trace_toEuclideanCLM_M1_eq_four_point_one
#print axioms YMCapstoneTraceM1Exact.lambda2_toEuclideanCLM_M1_bracket
