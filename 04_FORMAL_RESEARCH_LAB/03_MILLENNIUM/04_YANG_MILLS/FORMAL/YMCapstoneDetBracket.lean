/-
  YM-CAPSTONE-DET-BRACKET — a numeric bracket `2.03 ≤ det(toEuclideanCLM
  M1) ≤ 4.03`, obtained by combining three already-established Wave-4
  facts: the `lambdaMax (toEuclideanCLM M1)` bracket `[2.9, 3.1]`
  (`WAVE4-YM-CAPSTONE-BRACKET`, `YMCapstoneBracket.lean`), the
  `lambda2 (toEuclideanCLM M1)` bracket `[7/10, 13/10]`
  (`WAVE4-YM-CAPSTONE-FULL`, `YMCapstoneFull.lean`), and the identity
  `det = lambdaMax * lambda2` for a symmetric operator on the fixed
  2-dimensional `E` (`WAVE4-SHARED-4B`, `LambdaMaxMulLambda2EqDet.lean`).
  Wave-5 batch item, `YM-CAPSTONE-DET-BRACKET`.

  STATUS: CLOSED. Drafted and self-checked with `lake env lean` by the
  authoring session (single-file typecheck against the existing built
  Mathlib cache, NOT a full `lake build` — see the Wave-5 task
  instructions on build contention with 14 concurrent sibling agents).
  Not registered in `TamesisLab.lean`; free-standing, following the
  precedent of every other Wave-1/Wave-2/Wave-3/Wave-4 file in this
  directory. This file does NOT modify any other file; it only READS
  four prior-wave files (named above, plus `TwoEigenvalueExhaustiveness.lean`
  read for cross-checking but not needed as a dependency — see below).

  EXACT TASK ATTEMPTED (per the Wave-5 work-item prompt, candidate
  `YM-CAPSTONE-DET-BRACKET`): prove
  `2.03 ≤ det(toEuclideanCLM M1) ≤ 4.03` via
  `have hdet := lambdaMax_mul_lambda2_eq_det (toEuclideanCLM M1)
  toEuclideanCLM_M1_isSymmetric finrank_E_eq_two; constructor <;>
  nlinarith [...]`. This is EXACTLY what the final theorem below does
  (`det_M1_bracket`): `hdet` plus the two raw interval-endpoint bounds
  `hMax.1/hMax.2/hL2.1/hL2.2` are handed straight to
  `constructor <;> nlinarith [...]`, and `nlinarith` closes BOTH
  resulting goals directly from those five facts with no further help —
  the primary route the task specifies works exactly as stated, without
  needing the `mul_le_mul` fallback the task prompt names ("Fallback:
  mul_le_mul explicito se nlinarith não fechar"). That fallback route was
  tried anyway, purely to double-check robustness, and it also closes
  (`mul_le_mul hMax.1 hL2.1 (by norm_num) (by linarith [hMax.1])` /
  `mul_le_mul hMax.2 hL2.2 (by linarith [hL2.1]) (by norm_num)` fed as
  extra `nlinarith` hints) — but since the plain, unhinted route already
  succeeds, the final theorem below uses that simpler plain
  `nlinarith [hdet, hMax.1, hMax.2, hL2.1, hL2.2]` form, matching the
  task's own primary line verbatim.

  WHY THE NUMBERS 2.03 / 4.03 ARE EXACTLY RIGHT (not a coincidence, this
  is the whole point of the test). `YMCapstoneBracket.lean`'s
  `lambdaMax_M1_bracket` gives `lambdaMax (toEuclideanCLM M1) ∈
  [2.9, 3.1]`. `YMCapstoneFull.lean`'s `lambda2_M1_bracket_from_compose`
  gives `lambda2 (toEuclideanCLM M1) ∈ [7/10, 13/10] = [0.7, 1.3]`. Since
  both intervals consist of strictly positive reals, the extreme products
  of the box `[2.9,3.1] × [0.7,1.3]` are attained at the corners
  `(2.9, 0.7)` and `(3.1, 1.3)`: `2.9 * 0.7 = 2.03` and
  `3.1 * 1.3 = 4.03` — exactly the bracket the task specifies. This file
  does not re-derive either the `lambdaMax` bracket or the `lambda2`
  bracket; both are BYTE-FOR-BYTE REPRODUCED below (see BUILD-SYSTEM NOTE)
  and only the final multiplication step is new.

  RELATION TO WAVE-4 (all four read in full, NONE imported/modified).
  This file reuses, BYTE-FOR-BYTE REPRODUCED (never imported — see
  BUILD-SYSTEM NOTE below for why, identical reasoning to every Wave-2/
  Wave-3/Wave-4 sibling that faces the same free-standing-file
  constraint):
    - `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
      `lambdaMax_lipschitz`, `lambdaMax_hasEigenvalue` — verbatim from
      `YMCapstoneFull.lean` (Wave-4, `YMCapstoneFull`, Part 0a; the
      `lambdaMax_lipschitz` proof body specifically, since that file's
      version is the one written to be safe under `open Matrix`, which
      this file also needs for the trace computation below — see the
      "OPEN MATRIX NOTE" below).
    - `M2`, `M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`,
      `M2_spectrum_eq`, `M2_eigen_three`, `toEuclideanCLM_M2_spectrum_eq`,
      `toEuclideanCLM_M2_endSpectrum_eq`, `toEuclideanCLM_M2_isSymmetric`,
      `lambdaMax_mem_one_three`, `v`, `v_ne_zero`,
      `toEuclideanCLM_M2_apply_v`, `toEuclideanCLM_M2_rayleighQuotient_v`,
      `lambdaMax_ge_three`, `lambdaMax_grounded_eq_three` — verbatim from
      `YMCapstoneFull.lean` (Wave-4, Part 0b/0c; itself reproduced
      verbatim from `StabilityGrounded.lean`, Wave-3).
    - `M1`, `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
      `sonda2_numeric_norm`, `stability_compose_lambdaMax` — verbatim
      from `YMCapstoneBracket.lean` (Wave-4, Part 1; itself reproduced
      verbatim from `YMStabilityCompose.lean`, Wave-3).
    - `lambdaMax_M1_bracket` — verbatim from `YMCapstoneBracket.lean`
      (Wave-4, Part 3), the exact `2.9 ≤ ... ∧ ... ≤ 3.1` result.
    - `basis2`, `lambda2`, `trace_toEuclideanCLM_M2_eq_four`,
      `lambda2_toEuclideanCLM_M2_eq_one` — verbatim from
      `YMCapstoneFull.lean` (Wave-4, Part 0d / Part 1, PASSO 1).
    - `trace_lipschitz`, `lambda2_lipschitz`, `stability_compose_lambda2`
      — verbatim from `YMCapstoneFull.lean` (Wave-4, Part 2, PASSO 2
      plumbing).
    - `lambda2_M1_bracket_from_compose` — verbatim from
      `YMCapstoneFull.lean` (Wave-4, Part 2), the exact
      `7/10 ≤ ... ∧ ... ≤ 13/10` result.
    - `M1_isHermitian`, `toEuclideanCLM_M1_isSymmetric`,
      `finrank_E_eq_two` — verbatim from `YMCapstoneFull.lean` (Wave-4,
      PASSO 2 gap-diagnosis section).
    - `lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`,
      `lambdaMax_mul_lambda2_eq_det` — verbatim from
      `LambdaMaxMulLambda2EqDet.lean` (Wave-4, `SHARED-4B`,
      `03_MILLENNIUM/_SHARED_INFRA/FORMAL/`).
  `TwoEigenvalueExhaustiveness.lean` (Wave-4, `SHARED-4A`) was read in
  full for cross-checking (its `lambdaMax_eq_eigenvalues_zero` /
  `lambda2_eq_eigenvalues_one` are the same two facts `SHARED-4B`
  independently promotes) but is NOT a dependency of anything below —
  this file takes those two lemmas from `SHARED-4B` only, since
  `SHARED-4B` is also where `lambdaMax_mul_lambda2_eq_det` itself lives.
  None of the four source files is touched or modified; all are
  read-only source material.

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). Identical situation and identical reasoning to every prior
  Wave-2/Wave-3/Wave-4 sibling in this lineage: `YMCapstoneBracket.lean`,
  `YMCapstoneFull.lean`, and `LambdaMaxMulLambda2EqDet.lean` are, by their
  own headers, deliberately free-standing and NOT registered in
  `TamesisLab.lean` — none of them live inside the
  `[[lean_lib]] name = "TamesisLab"` module graph declared in
  `lakefile.toml`, so none has a built `.olean` that could be `import`ed
  by module path. Per the Wave-5 task instructions ("do NOT touch any
  file outside your own new file(s)"), this file cannot register any of
  them into the library graph either. The only way to reuse their
  declarations under this constraint is to reproduce them verbatim.

  OPEN MATRIX NOTE. This file uses `open Matrix` (needed for the `⬝ᵥ`/`*ᵥ`
  notation inside `trace_toEuclideanCLM_M2_eq_four`, exactly as
  `YMCapstoneFull.lean` does). Consequently the `lambdaMax_lipschitz`
  proof reproduced below is `YMCapstoneFull.lean`'s version specifically
  (which omits the bare `sub_apply` simp-lemma reference that becomes
  ambiguous against `Matrix.sub_apply` once `Matrix` is opened — see
  `YMCapstoneBracket.lean`'s own header for the original discovery of
  this ambiguity), NOT `YMCapstoneBracket.lean`'s version (which instead
  avoids `open Matrix` entirely and fully qualifies every `Matrix`/`WithLp`
  name).

  WHY PLAIN NLINARITH ALREADY SUFFICES (verified directly, not assumed).
  Proving `2.03 ≤ x * y` (resp. `x * y ≤ 4.03`) from `2.9 ≤ x ≤ 3.1` and
  `7/10 ≤ y ≤ 13/10` needs a nonlinear cross-term such as
  `(x - 2.9) * y ≥ 0`. `nlinarith`'s default preprocessing multiplies
  PAIRS of the hypotheses/goal-atoms it is given together before calling
  `linarith`, and with exactly the four raw interval-endpoint hypotheses
  plus the negated goal available, the pairing it needs (an `x`-bound
  times a `y`-bound) IS among the pairs it tries automatically — so
  `constructor <;> nlinarith [hdet, hMax.1, hMax.2, hL2.1, hL2.2]` closes
  both goals directly, with no explicit product hint required. This was
  checked two ways before settling on the plain form used below: (a) an
  isolated standalone example with the same four hypothesis shapes over
  `ℝ`, and (b) an in-file variant of `det_M1_bracket` itself with the
  `mul_le_mul` hints removed — both close with `lake env lean` exit code
  `0`. The task's own named fallback (`mul_le_mul hMax.1 hL2.1
  (by norm_num) (by linarith [hMax.1])` and the symmetric upper-bound
  term, fed as extra `nlinarith` hints) was also checked and independently
  closes both goals — it simply turned out not to be necessary here.

  MATHLIB TOOLS USED — no new Mathlib citation beyond what the four
  source files above already establish (see their own headers for the
  full list: `LinearMap.IsSymmetric.eigenvalues`/`.exists_eigenvalues_eq`/
  `.eigenvalues_antitone`/`.eigenvectorBasis`/
  `.hasEigenvector_eigenvectorBasis`/`.apply_eigenvectorBasis`/
  `.trace_eq_sum_eigenvalues`/`.det_eq_prod_eigenvalues`,
  `Fin.prod_univ_two`, `Fin.sum_univ_two`, `le_ciSup`,
  `real_inner_smul_left`, `AlgEquiv.spectrum_eq`,
  `ContinuousLinearMap.spectrum_eq`,
  `Module.End.hasEigenvalue_iff_mem_spectrum`,
  `Matrix.toEuclideanCLM_toLp`, `Matrix.isSymmetric_toEuclideanLin_iff`,
  `Matrix.l2_opNorm_toEuclideanCLM`, `Matrix.l2_opNorm_diagonal`,
  `Matrix.inner_toEuclideanCLM`, `EuclideanSpace.basisFun_apply`,
  `finrank_euclideanSpace_fin`); this file's own final theorem needs no
  NEW Mathlib citation beyond `nlinarith` itself, which closes both
  halves directly from the raw interval-endpoint hypotheses (see "WHY
  PLAIN NLINARITH ALREADY SUFFICES" above).

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT. `det_M1_bracket` proves
  `2.03 ≤ (toEuclideanCLM M1 : E →ₗ[ℝ] E).det ∧
  (toEuclideanCLM M1 : E →ₗ[ℝ] E).det ≤ 4.03`, exactly the falsifiable
  test as stated, by rewriting `det = lambdaMax * lambda2`
  (`lambdaMax_mul_lambda2_eq_det`) and bounding the product of the two
  already-established brackets `[2.9,3.1]` and `[7/10,13/10]` via
  `nlinarith`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-5 instructions). This remains the same single hand-picked `2×2`
  toy matrix pair (`M1`, `M2`) as every prior file in this lineage;
  nothing here is about SU(N), any lattice-gauge action, reflection
  positivity, or the continuum limit. The bracket `[2.03, 4.03]` inherits
  ALL the slack already present in the two brackets it composes (the
  `lambdaMax` bracket has half-width `0.1` around `3`, the `lambda2`
  bracket has half-width `0.3` around `1`); no attempt is made here to
  tighten either input bracket, and the exact value of
  `det(toEuclideanCLM M1)` is not computed (it is, in fact, computable in
  closed form as `det M1 = 2 * 2.1 - 1 * 1 = 3.2`, comfortably inside
  `[2.03, 4.03]`, but that direct computation is NOT what this file
  proves or claims — the falsifiable test asked for the bracket obtained
  via the `lambdaMax * lambda2` route specifically, and that is exactly
  what is proved). This file says nothing about Yang-Mills, does not
  approximate a solution to the Clay mass-gap problem or any other
  Millennium problem, and claims no mathematical novelty — bounding a
  product of two known real intervals by evaluating it at corners is
  completely elementary.

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

namespace YMCapstoneDetBracket

/-! ### Part 0a — verbatim reproduction of `YMCapstoneFull.lean`'s Part 0a
(`E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
`lambdaMax_lipschitz`, `lambdaMax_hasEigenvalue`). -/

/-- The fixed finite-dimensional real inner product space (verbatim from
`YMCapstoneFull.E`). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the fixed
space `E` (verbatim from `YMCapstoneFull.lambdaMax`). -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector (verbatim from `YMCapstoneFull.bddAbove_rayleighQuotient_subtype`). -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim.** `lambdaMax` is 1-Lipschitz
in operator norm on the fixed space `E`. Byte-identical (proof included)
to `lambdaMax_lipschitz` in `YMCapstoneFull.lean` (the `open Matrix`-safe
variant — see the "OPEN MATRIX NOTE" in this file's header). -/
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

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`
(verbatim from `YMCapstoneFull.lambdaMax_hasEigenvalue`). -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Part 0b/0c — verbatim reproduction of `YMCapstoneFull.lean`'s
`M2` chain and the abstract-spectrum route to
`lambdaMax (toEuclideanCLM M2) = 3`. -/

/-- The toy 2×2 "transfer matrix" (verbatim value from
`YMCapstoneFull.M2`). -/
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

/-! ### Part 1 — verbatim reproduction of `YMCapstoneBracket.lean`'s Part 1
(`M1`, `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
`sonda2_numeric_norm`, `stability_compose_lambdaMax`) and Part 3
(`lambdaMax_M1_bracket`). -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` in
`YMCapstoneBracket.lean` / `YMCapstoneFull.lean`. -/
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

/-- **Wave-3 YM-STABILITY-COMPOSE result, reproduced verbatim.** -/
theorem stability_compose_lambdaMax :
    |lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 1 / 10 :=
  (lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact sonda2_numeric_norm.le)

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

/-! ### Part 2 — verbatim reproduction of `YMCapstoneFull.lean`'s Part 0d
(`basis2`, `lambda2`) and Part 1, PASSO 1
(`trace_toEuclideanCLM_M2_eq_four`, `lambda2_toEuclideanCLM_M2_eq_one`). -/

/-- The fixed orthonormal basis of `E`. Byte-identical to `basis2` in
`YMCapstoneFull.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`YMCapstoneFull.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

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

/-- **Wave-4 YM-CAPSTONE-FULL result (PASSO 1), reproduced verbatim.**
`lambda2 (toEuclideanCLM M2) = 1` exactly. -/
theorem lambda2_toEuclideanCLM_M2_eq_one :
    lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 1 := by
  unfold lambda2
  rw [trace_toEuclideanCLM_M2_eq_four, lambdaMax_grounded_eq_three]
  norm_num

/-! ### Part 3 — verbatim reproduction of `YMCapstoneFull.lean`'s Part 2
plumbing (`trace_lipschitz`, `lambda2_lipschitz`,
`stability_compose_lambda2`) and its `lambda2_M1_bracket_from_compose`. -/

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

/-- **Wave-3 YM-STABILITY-COMPOSE result, part 2, reproduced verbatim.** -/
theorem stability_compose_lambda2 :
    |lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 3 / 10 := by
  have h := lambda2_lipschitz (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1)
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
  rw [sonda1_bridge, sonda2_numeric_norm] at h
  linarith

/-- **Wave-4 YM-CAPSTONE-FULL result (PASSO 2), reproduced verbatim.**
`lambda2 (toEuclideanCLM M1)` lies in `[7/10, 13/10]`. Byte-identical
(proof included) to `lambda2_M1_bracket_from_compose` in
`YMCapstoneFull.lean`. -/
theorem lambda2_M1_bracket_from_compose :
    7 / 10 ≤ lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 13 / 10 := by
  have h := stability_compose_lambda2
  rw [lambda2_toEuclideanCLM_M2_eq_one] at h
  rw [abs_le] at h
  constructor <;> linarith

/-! ### Part 4 — verbatim reproduction of `YMCapstoneFull.lean`'s
`M1_isHermitian`, `toEuclideanCLM_M1_isSymmetric`, `finrank_E_eq_two`. -/

theorem M1_isHermitian : M1.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M1, Matrix.conjTranspose_apply]

theorem toEuclideanCLM_M1_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M1_isHermitian

theorem finrank_E_eq_two : Module.finrank ℝ E = 2 :=
  finrank_euclideanSpace_fin

/-! ### Part 5 — verbatim reproduction of `LambdaMaxMulLambda2EqDet.lean`
(Wave-4, `SHARED-4B`): `lambdaMax_eq_eigenvalues_zero`,
`lambda2_eq_eigenvalues_one`, `lambdaMax_mul_lambda2_eq_det`. -/

/-- **Promotion of `heq0`, reproduced verbatim from `SHARED4B`.** For
symmetric `T` on the fixed 2-dimensional `E`, `lambdaMax T` coincides with
the `0`-th (largest) entry of Mathlib's sorted eigenvalue family
`hT.eigenvalues hn`. -/
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

/-- **Promotion of `hlambda2`, reproduced verbatim from `SHARED4B`.** For
symmetric `T` on the fixed 2-dimensional `E`, `lambda2 T` coincides with
the `1`-st (smaller) entry of Mathlib's sorted eigenvalue family
`hT.eigenvalues hn`. -/
theorem lambda2_eq_eigenvalues_one (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T = hT.eigenvalues hn 1 := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  unfold lambda2
  rw [htrace, heq0]; ring

/-- **Wave-4 SHARED-4B result, reproduced verbatim.** For a symmetric
`T : E →L[ℝ] E` on the fixed 2-dimensional `E`, the determinant of (the
`LinearMap` coercion of) `T` equals the product `lambdaMax T * lambda2 T`.
Byte-identical (proof included) to `lambdaMax_mul_lambda2_eq_det` in
`LambdaMaxMulLambda2EqDet.lean`. -/
theorem lambdaMax_mul_lambda2_eq_det (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det := by
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := lambda2_eq_eigenvalues_one T hT hn
  have hdet : (T : E →ₗ[ℝ] E).det = hT.eigenvalues hn 0 * hT.eigenvalues hn 1 := by
    rw [hT.det_eq_prod_eigenvalues hn, Fin.prod_univ_two]
    norm_cast
  rw [heq0, hlambda2, hdet]

/-! ### Part 6 — new content specific to this item
(YM-CAPSTONE-DET-BRACKET): the falsifiable test itself, `det_M1_bracket`,
combining `lambdaMax_mul_lambda2_eq_det` (Part 5) with the two brackets
`lambdaMax_M1_bracket` (Part 1) and `lambda2_M1_bracket_from_compose`
(Part 3), exactly as the task's `have hdet := ...; constructor <;>
nlinarith [...]` specifies — `nlinarith` closes both resulting goals
directly from the raw interval-endpoint hypotheses, with no need for the
`mul_le_mul` fallback the task itself names (see "WHY PLAIN NLINARITH
ALREADY SUFFICES" in this file's header, which reports both routes were
checked). -/

/-- **Main new result (YM-CAPSTONE-DET-BRACKET), the falsifiable test as
stated.** The determinant of (the `LinearMap` coercion of)
`toEuclideanCLM M1` lies in the numeric interval `[2.03, 4.03]`. -/
theorem det_M1_bracket :
    2.03 ≤ (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).det ∧
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).det ≤ 4.03 := by
  have hdet := lambdaMax_mul_lambda2_eq_det
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) toEuclideanCLM_M1_isSymmetric
    finrank_E_eq_two
  have hMax := lambdaMax_M1_bracket
  have hL2 := lambda2_M1_bracket_from_compose
  constructor <;> nlinarith [hdet, hMax.1, hMax.2, hL2.1, hL2.2]

end YMCapstoneDetBracket

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneDetBracket.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneDetBracket.lambdaMax_lipschitz
#print axioms YMCapstoneDetBracket.lambdaMax_hasEigenvalue
#print axioms YMCapstoneDetBracket.M2_isHermitian
#print axioms YMCapstoneDetBracket.M2_charpoly_eval
#print axioms YMCapstoneDetBracket.M2_spectrum_real
#print axioms YMCapstoneDetBracket.M2_spectrum_eq
#print axioms YMCapstoneDetBracket.M2_eigen_three
#print axioms YMCapstoneDetBracket.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneDetBracket.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneDetBracket.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneDetBracket.lambdaMax_mem_one_three
#print axioms YMCapstoneDetBracket.v_ne_zero
#print axioms YMCapstoneDetBracket.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneDetBracket.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneDetBracket.lambdaMax_ge_three
#print axioms YMCapstoneDetBracket.lambdaMax_grounded_eq_three
#print axioms YMCapstoneDetBracket.sonda1_bridge
#print axioms YMCapstoneDetBracket.diff_eq_diagonal
#print axioms YMCapstoneDetBracket.pi_norm_vec
#print axioms YMCapstoneDetBracket.sonda2_numeric_norm
#print axioms YMCapstoneDetBracket.stability_compose_lambdaMax
#print axioms YMCapstoneDetBracket.lambdaMax_M1_bracket
#print axioms YMCapstoneDetBracket.trace_toEuclideanCLM_M2_eq_four
#print axioms YMCapstoneDetBracket.lambda2_toEuclideanCLM_M2_eq_one
#print axioms YMCapstoneDetBracket.trace_lipschitz
#print axioms YMCapstoneDetBracket.lambda2_lipschitz
#print axioms YMCapstoneDetBracket.stability_compose_lambda2
#print axioms YMCapstoneDetBracket.lambda2_M1_bracket_from_compose
#print axioms YMCapstoneDetBracket.M1_isHermitian
#print axioms YMCapstoneDetBracket.toEuclideanCLM_M1_isSymmetric
#print axioms YMCapstoneDetBracket.finrank_E_eq_two
#print axioms YMCapstoneDetBracket.lambdaMax_eq_eigenvalues_zero
#print axioms YMCapstoneDetBracket.lambda2_eq_eigenvalues_one
#print axioms YMCapstoneDetBracket.lambdaMax_mul_lambda2_eq_det
#print axioms YMCapstoneDetBracket.det_M1_bracket
