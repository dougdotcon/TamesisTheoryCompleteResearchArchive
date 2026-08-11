/-
  YM-CAPSTONE-DET-BRACKET-TIGHTENED — a tightened numeric bracket
  `2.9 ≤ det(toEuclideanCLM M1) ≤ 3.72`, obtained by combining
  `lambdaMax_mul_lambda2_eq_det` (`WAVE4-SHARED-4B`,
  `LambdaMaxMulLambda2EqDet.lean`) with the ALREADY-established
  `lambdaMax (toEuclideanCLM M1)` bracket `[2.9, 3.1]`
  (`WAVE4-YM-CAPSTONE-BRACKET`, `YMCapstoneBracket.lean`) and the NEW,
  strictly narrower `lambda2 (toEuclideanCLM M1)` bracket `[1.0, 1.2]`
  proved by this batch's gate item `WAVE6-YM-CAPSTONE-TRACE-M1-EXACT`
  (`YMCapstoneTraceM1Exact.lean`), in place of the wider `[0.7, 1.3]`
  bracket `YMCapstoneDetBracket.lean` (Wave-5) used. Wave-6 batch item,
  `YM-CAPSTONE-DET-BRACKET-TIGHTENED`, GATED on
  `WAVE6-YM-CAPSTONE-TRACE-M1-EXACT` closing first.

  STATUS: CLOSED. Drafted and self-checked with `lake env lean` by the
  authoring session (single-file typecheck against the existing built
  Mathlib cache, NOT a full `lake build` — see the Wave-6 task
  instructions on build contention with 13 concurrent sibling agents).
  Not registered in `TamesisLab.lean`; free-standing, following the
  precedent of every other Wave-1..Wave-5 file in this directory. This
  file does NOT modify any other file; it only READS
  `YMCapstoneTraceM1Exact.lean` (Wave-6, the gate item for this one),
  `YMCapstoneDetBracket.lean` (Wave-5), `YMCapstoneBracket.lean`
  (Wave-4), `YMCapstoneFull.lean` (Wave-4), and
  `LambdaMaxMulLambda2EqDet.lean` (Wave-4, `SHARED-4B`,
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/`).

  GATE VERIFICATION (mandatory per the Wave-6 task instructions for this
  specific item). Before writing any new content below, this file's
  authoring session independently recompiled the gate dependency itself
  — NOT trusting that file's own self-report alone:
    `lake env lean YMCapstoneTraceM1Exact.lean` → observed exit code `0`,
  read the full resulting log (27 lines, all `#print axioms` output),
  and confirmed every one of its 24 `#print axioms` lines shows ONLY
  `[propext, Classical.choice, Quot.sound]` — in particular
  `YMCapstoneTraceM1Exact.trace_toEuclideanCLM_M1_eq_four_point_one` and
  `YMCapstoneTraceM1Exact.lambda2_toEuclideanCLM_M1_bracket`, the two
  declarations this file's numbers below depend on. Only after this
  independent confirmation did work on this file's own new content
  begin. (See this file's own build log, reported alongside this file,
  for the exact command/exit code this session personally observed for
  ITS OWN file; the gate-verification command/log above is reported
  separately in this session's final report, not re-embedded as a
  build artifact of this file.)

  EXACT TASK ATTEMPTED (per the Wave-6 work-item prompt, candidate
  `YM-CAPSTONE-DET-BRACKET-TIGHTENED`): prove
  `2.9 ≤ det(toEuclideanCLM M1) ≤ 3.72` via `lambdaMax_mul_lambda2_eq_det`
  + `lambdaMax_M1_bracket` + the new bracket `[1.0, 1.2]` of `lambda2`;
  `constructor <;> nlinarith [...]`. This is EXACTLY what the final
  theorem below does (`det_M1_bracket_tightened`): `hdet` plus the four
  raw interval-endpoint bounds `hMax.1/hMax.2/hL2.1/hL2.2` are handed
  straight to `constructor <;> nlinarith [...]`, and `nlinarith` closes
  BOTH resulting goals directly from those five facts with no further
  help, exactly as the analogous step in `YMCapstoneDetBracket.lean`
  (Wave-5) already found sufficient for the wider bracket.

  WHY THE NUMBERS 2.9 / 3.72 ARE EXACTLY RIGHT (not a coincidence, this
  is the whole point of the test — and why this bracket is strictly
  TIGHTER than Wave-5's). `YMCapstoneBracket.lean`'s `lambdaMax_M1_bracket`
  gives `lambdaMax (toEuclideanCLM M1) ∈ [2.9, 3.1]` (UNCHANGED from
  Wave-5 — this file does not attempt to tighten it). This batch's gate
  item `YMCapstoneTraceM1Exact.lean` gives
  `lambda2 (toEuclideanCLM M1) ∈ [1.0, 1.2]` — narrower than Wave-5's
  `lambda2_M1_bracket_from_compose : [7/10, 13/10] = [0.7, 1.3]`, because
  it derives from an EXACT trace value (`4.1`) combined with the
  `lambdaMax` bracket, rather than from a separate Lipschitz estimate on
  `lambda2` itself (see `YMCapstoneTraceM1Exact.lean`'s own header for
  the full comparison). Since both intervals `[2.9,3.1]` and `[1.0,1.2]`
  consist of strictly positive reals, the extreme products of the box
  `[2.9,3.1] × [1.0,1.2]` are attained at the corners `(2.9, 1.0)` and
  `(3.1, 1.2)`: `2.9 * 1.0 = 2.9` and `3.1 * 1.2 = 3.72` — exactly the
  bracket the task specifies, and strictly inside Wave-5's `[2.03, 4.03]`
  (`2.03 ≤ 2.9` and `3.72 ≤ 4.03`, both strict), as expected since it
  composes strictly more information (the exact `M1` trace) than the
  Wave-5 bracket did. This file does not re-derive the `lambdaMax`
  bracket, the `lambda2` bracket, or the `det = lambdaMax * lambda2`
  identity; all three are BYTE-FOR-BYTE REPRODUCED below (see
  BUILD-SYSTEM NOTE) and only the final multiplication step is new.

  RELATION TO WAVE-4/WAVE-5/WAVE-6 (all named files read in full, NONE
  imported/modified). This file reuses, BYTE-FOR-BYTE REPRODUCED (never
  imported — see BUILD-SYSTEM NOTE below for why, identical reasoning to
  every prior Wave-2..Wave-5 sibling that faces the same free-standing-
  file constraint):
    - `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
      `lambdaMax_lipschitz`, `lambdaMax_hasEigenvalue`, `M2` chain
      (`M2_isHermitian` .. `lambdaMax_grounded_eq_three`), `M1`,
      `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
      `sonda2_numeric_norm`, `stability_compose_lambdaMax`,
      `lambdaMax_M1_bracket`, `M1_isHermitian`,
      `toEuclideanCLM_M1_isSymmetric`, `finrank_E_eq_two` — verbatim from
      `YMCapstoneDetBracket.lean` (Wave-5), itself reproduced verbatim
      from `YMCapstoneBracket.lean` / `YMCapstoneFull.lean` (Wave-4).
    - `lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`,
      `lambdaMax_mul_lambda2_eq_det` — verbatim from
      `LambdaMaxMulLambda2EqDet.lean` (Wave-4, `SHARED-4B`,
      `03_MILLENNIUM/_SHARED_INFRA/FORMAL/`), also reproduced identically
      in `YMCapstoneDetBracket.lean` (Wave-5).
    - `basis2`, `lambda2`, `trace_toEuclideanCLM_M1_eq_four_point_one`,
      `lambda2_toEuclideanCLM_M1_bracket` — verbatim from
      `YMCapstoneTraceM1Exact.lean` (Wave-6, this item's gate
      dependency, independently recompiled first — see GATE
      VERIFICATION above). THIS is the one substantively new ingredient
      relative to `YMCapstoneDetBracket.lean` (Wave-5): that file used
      `lambda2_M1_bracket_from_compose` (`[0.7, 1.3]`, from
      `YMCapstoneFull.lean`'s Lipschitz-composition route) instead.
  None of `YMCapstoneTraceM1Exact.lean`, `YMCapstoneDetBracket.lean`,
  `YMCapstoneBracket.lean`, `YMCapstoneFull.lean`, or
  `LambdaMaxMulLambda2EqDet.lean` is touched or modified; all five are
  read-only source material.

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). Identical situation and identical reasoning to every prior
  Wave-2..Wave-5 sibling in this lineage: none of the five files named
  above is registered in `TamesisLab.lean` (none lives inside the
  `[[lean_lib]] name = "TamesisLab"` module graph declared in
  `lakefile.toml`), so none has a built `.olean` importable by module
  path. Per the Wave-6 task instructions ("do NOT touch any file outside
  your own new file(s)"), this file cannot register any of them into the
  library graph either. The only way to reuse their declarations under
  this constraint is to reproduce them verbatim. (This is a genuine,
  narrow exception to the general "don't depend on a same-wave sibling
  file" caution other Wave-6 items observe: THIS item's own task
  explicitly names `YMCapstoneTraceM1Exact.lean` — a DIFFERENT Wave-6
  item — as its mandatory gate dependency, and instructs reusing its
  proved bracket; the independent recompilation in GATE VERIFICATION
  above is the safeguard against trusting unverified sibling content.)

  OPEN MATRIX NOTE. This file uses `open Matrix` (needed for the `⬝ᵥ`/`*ᵥ`
  notation inside `trace_toEuclideanCLM_M1_eq_four_point_one`, reproduced
  from `YMCapstoneTraceM1Exact.lean`, which itself needs it for exactly
  the same reason `YMCapstoneFull.lean` and `YMCapstoneDetBracket.lean`
  do). Consequently the `lambdaMax_lipschitz` proof reproduced below is
  the `open Matrix`-safe variant (omitting the bare `sub_apply` simp-
  lemma reference that becomes ambiguous against `Matrix.sub_apply` once
  `Matrix` is opened — see `YMCapstoneBracket.lean`'s own header for the
  original discovery of this ambiguity), matching
  `YMCapstoneDetBracket.lean`'s and `YMCapstoneTraceM1Exact.lean`'s
  choice, NOT `YMCapstoneBracket.lean`'s own version (which instead
  avoids `open Matrix` entirely).

  WHY PLAIN NLINARITH ALREADY SUFFICES (verified directly, not assumed —
  same check `YMCapstoneDetBracket.lean` already ran for the wider
  bracket, re-run here for the tightened one). Proving `2.9 ≤ x * y`
  (resp. `x * y ≤ 3.72`) from `2.9 ≤ x ≤ 3.1` and `1.0 ≤ y ≤ 1.2` needs a
  nonlinear cross-term such as `(x - 2.9) * y ≥ 0`. `nlinarith`'s default
  preprocessing multiplies PAIRS of the hypotheses/goal-atoms it is given
  together before calling `linarith`, and with exactly the four raw
  interval-endpoint hypotheses plus the negated goal available, the
  pairing it needs (an `x`-bound times a `y`-bound) IS among the pairs it
  tries automatically — so
  `constructor <;> nlinarith [hdet, hMax.1, hMax.2, hL2.1, hL2.2]` closes
  both goals directly, with no explicit product hint required. Verified
  by `lake env lean` exit code `0` on this file (see this file's own
  build log).

  MATHLIB TOOLS USED — no new Mathlib citation beyond what
  `YMCapstoneTraceM1Exact.lean`, `YMCapstoneDetBracket.lean`, and
  `LambdaMaxMulLambda2EqDet.lean` already establish (see their own
  headers for the full list); this file's own final theorem needs no NEW
  Mathlib citation beyond `nlinarith` itself.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT.
  `det_M1_bracket_tightened` proves
  `2.9 ≤ (toEuclideanCLM M1 : E →ₗ[ℝ] E).det ∧
  (toEuclideanCLM M1 : E →ₗ[ℝ] E).det ≤ 3.72`, exactly the falsifiable
  test as stated, by rewriting `det = lambdaMax * lambda2`
  (`lambdaMax_mul_lambda2_eq_det`) and bounding the product of the two
  already-established brackets `[2.9,3.1]` and `[1.0,1.2]` via
  `nlinarith`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-6 instructions). This remains the same single hand-picked `2×2`
  toy matrix pair (`M1`, `M2`) as every prior file in this lineage;
  nothing here is about SU(N), any lattice-gauge action, reflection
  positivity, or the continuum limit. The bracket `[2.9, 3.72]` still
  inherits ALL the slack present in the `lambdaMax` bracket (half-width
  `0.1` around `3`, NOT tightened by this file or its gate dependency);
  only the `lambda2` half was tightened, from half-width `0.3` to
  half-width `0.1`. The exact value of `det(toEuclideanCLM M1)` is not
  computed by this route (it is, in fact, computable in closed form as
  `det M1 = 2 * 2.1 - 1 * 1 = 3.2`, comfortably inside `[2.9, 3.72]`, and
  also inside the Wave-5 `[2.03, 4.03]` bracket, consistent with both —
  but that direct computation is NOT what this file proves or claims —
  the falsifiable test asked for the bracket obtained via the
  `lambdaMax * lambda2` route specifically, using the newly tightened
  `lambda2` bracket, and that is exactly what is proved). This file says
  nothing about Yang-Mills, does not approximate a solution to the Clay
  mass-gap problem or any other Millennium problem, and claims no
  mathematical novelty — bounding a product of two known real intervals
  by evaluating it at corners is completely elementary.

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

namespace YMCapstoneDetBracketTightened

/-! ### Part 0a — verbatim reproduction of `E`, `lambdaMax`,
`bddAbove_rayleighQuotient_subtype`, `lambdaMax_lipschitz`,
`lambdaMax_hasEigenvalue`, from `YMCapstoneDetBracket.lean` (Wave-5). -/

/-- The fixed finite-dimensional real inner product space (verbatim from
`YMCapstoneDetBracket.E`). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the fixed
space `E` (verbatim from `YMCapstoneDetBracket.lambdaMax`). -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector (verbatim from `YMCapstoneDetBracket.bddAbove_rayleighQuotient_subtype`). -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim.** `lambdaMax` is 1-Lipschitz
in operator norm on the fixed space `E`. Byte-identical (proof included)
to `lambdaMax_lipschitz` in `YMCapstoneDetBracket.lean` (the `open
Matrix`-safe variant — see the "OPEN MATRIX NOTE" in this file's header). -/
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
(verbatim from `YMCapstoneDetBracket.lambdaMax_hasEigenvalue`). -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Part 0b/0c — verbatim reproduction of the `M2` chain and the
abstract-spectrum route to `lambdaMax (toEuclideanCLM M2) = 3`, from
`YMCapstoneDetBracket.lean` (Wave-5). -/

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

/-! ### Part 1 — verbatim reproduction of `M1`, `sonda1_bridge`,
`diff_eq_diagonal`, `pi_norm_vec`, `sonda2_numeric_norm`,
`stability_compose_lambdaMax`, `lambdaMax_M1_bracket`, from
`YMCapstoneDetBracket.lean` (Wave-5). NOT tightened here — this file's
task attempts ONLY the `lambda2` half, per the falsifiable test as
stated. -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` throughout this
lineage. -/
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

/-- **Wave-4 YM-CAPSTONE-BRACKET result, reproduced verbatim, UNCHANGED
from Wave-5.** `lambdaMax (toEuclideanCLM M1)` lies in the numeric
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

/-! ### Part 2 — verbatim reproduction of `basis2`, `lambda2`,
`trace_toEuclideanCLM_M1_eq_four_point_one`,
`lambda2_toEuclideanCLM_M1_bracket`, from `YMCapstoneTraceM1Exact.lean`
(Wave-6, this item's independently-recompiled gate dependency — see GATE
VERIFICATION in this file's header). THIS PART is the substantively new
ingredient relative to `YMCapstoneDetBracket.lean` (Wave-5), which used
`YMCapstoneFull.lean`'s wider `lambda2_M1_bracket_from_compose`
(`[0.7, 1.3]`) in its place. -/

/-- The fixed orthonormal basis of `E`. Byte-identical to `basis2` in
`YMCapstoneTraceM1Exact.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`YMCapstoneTraceM1Exact.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Wave-6 YM-CAPSTONE-TRACE-M1-EXACT gate result, reproduced
verbatim.** `trace (toEuclideanCLM M1 : E →ₗ[ℝ] E) = 4.1`, computed by
expanding the trace over `basis2` and evaluating the resulting 2-term
sum: `M1 0 0 + M1 1 1 = 2 + 2.1 = 4.1`. Byte-identical (proof included)
to `trace_toEuclideanCLM_M1_eq_four_point_one` in
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

/-- **Wave-6 YM-CAPSTONE-TRACE-M1-EXACT gate result, reproduced
verbatim — the NEW, tightened `lambda2` bracket this item's task
specifies.** `lambda2 (toEuclideanCLM M1)` lies in the numeric interval
`[1.0, 1.2]`, strictly narrower than the Wave-5 `[0.7, 1.3]`.
Byte-identical (proof included) to `lambda2_toEuclideanCLM_M1_bracket`
in `YMCapstoneTraceM1Exact.lean`. -/
theorem lambda2_toEuclideanCLM_M1_bracket :
    1.0 ≤ lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 1.2 := by
  unfold lambda2
  rw [trace_toEuclideanCLM_M1_eq_four_point_one]
  obtain ⟨hlo, hhi⟩ := lambdaMax_M1_bracket
  constructor <;> linarith

/-! ### Part 3 — verbatim reproduction of `LambdaMaxMulLambda2EqDet.lean`
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

/-! ### Part 4 — new content specific to this item
(YM-CAPSTONE-DET-BRACKET-TIGHTENED): the falsifiable test itself,
`det_M1_bracket_tightened`, combining `lambdaMax_mul_lambda2_eq_det`
(Part 3) with the UNCHANGED `lambdaMax_M1_bracket` (Part 1) and the NEW,
tightened `lambda2_toEuclideanCLM_M1_bracket` (Part 2), exactly as the
task's `constructor <;> nlinarith [...]` specifies — `nlinarith` closes
both resulting goals directly from the raw interval-endpoint hypotheses
(see "WHY PLAIN NLINARITH ALREADY SUFFICES" in this file's header). -/

/-- **Main new result (YM-CAPSTONE-DET-BRACKET-TIGHTENED), the
falsifiable test as stated.** The determinant of (the `LinearMap`
coercion of) `toEuclideanCLM M1` lies in the numeric interval
`[2.9, 3.72]`, strictly narrower than the Wave-5 `[2.03, 4.03]`. -/
theorem det_M1_bracket_tightened :
    2.9 ≤ (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).det ∧
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).det ≤ 3.72 := by
  have hdet := lambdaMax_mul_lambda2_eq_det
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) toEuclideanCLM_M1_isSymmetric
    finrank_E_eq_two
  have hMax := lambdaMax_M1_bracket
  have hL2 := lambda2_toEuclideanCLM_M1_bracket
  constructor <;> nlinarith [hdet, hMax.1, hMax.2, hL2.1, hL2.2]

end YMCapstoneDetBracketTightened

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneDetBracketTightened.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneDetBracketTightened.lambdaMax_lipschitz
#print axioms YMCapstoneDetBracketTightened.lambdaMax_hasEigenvalue
#print axioms YMCapstoneDetBracketTightened.M2_isHermitian
#print axioms YMCapstoneDetBracketTightened.M2_charpoly_eval
#print axioms YMCapstoneDetBracketTightened.M2_spectrum_real
#print axioms YMCapstoneDetBracketTightened.M2_spectrum_eq
#print axioms YMCapstoneDetBracketTightened.M2_eigen_three
#print axioms YMCapstoneDetBracketTightened.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneDetBracketTightened.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneDetBracketTightened.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneDetBracketTightened.lambdaMax_mem_one_three
#print axioms YMCapstoneDetBracketTightened.v_ne_zero
#print axioms YMCapstoneDetBracketTightened.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneDetBracketTightened.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneDetBracketTightened.lambdaMax_ge_three
#print axioms YMCapstoneDetBracketTightened.lambdaMax_grounded_eq_three
#print axioms YMCapstoneDetBracketTightened.sonda1_bridge
#print axioms YMCapstoneDetBracketTightened.diff_eq_diagonal
#print axioms YMCapstoneDetBracketTightened.pi_norm_vec
#print axioms YMCapstoneDetBracketTightened.sonda2_numeric_norm
#print axioms YMCapstoneDetBracketTightened.stability_compose_lambdaMax
#print axioms YMCapstoneDetBracketTightened.lambdaMax_M1_bracket
#print axioms YMCapstoneDetBracketTightened.M1_isHermitian
#print axioms YMCapstoneDetBracketTightened.toEuclideanCLM_M1_isSymmetric
#print axioms YMCapstoneDetBracketTightened.finrank_E_eq_two
#print axioms YMCapstoneDetBracketTightened.trace_toEuclideanCLM_M1_eq_four_point_one
#print axioms YMCapstoneDetBracketTightened.lambda2_toEuclideanCLM_M1_bracket
#print axioms YMCapstoneDetBracketTightened.lambdaMax_eq_eigenvalues_zero
#print axioms YMCapstoneDetBracketTightened.lambda2_eq_eigenvalues_one
#print axioms YMCapstoneDetBracketTightened.lambdaMax_mul_lambda2_eq_det
#print axioms YMCapstoneDetBracketTightened.det_M1_bracket_tightened
