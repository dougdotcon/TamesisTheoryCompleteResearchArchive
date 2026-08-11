/-
  YM-CAPSTONE-FULL — two-step capstone: `trace(toEuclideanCLM M2) = 4` /
  `lambda2 (toEuclideanCLM M2) = 1` (PASSO 1), then a gated attempt at a
  numeric bracket for `lambda2 (toEuclideanCLM M1)` analogous to the
  `lambdaMax` bracket (PASSO 2, Wave-4 batch item).

  STATUS: PASSO 1 drafted and self-checked with `lake env lean` by the
  authoring session (single-file typecheck against the existing built
  Mathlib cache, NOT a full `lake build` — see the Wave-4 task
  instructions on build contention with 14 concurrent sibling agents).
  PASSO 2 (gated on PASSO 1) DOES produce a genuine, fully-proved numeric
  bracket for `lambda2 (toEuclideanCLM M1)` (`lambda2_M1_bracket_from_compose`
  below), but NOT via the exact "compose three ways using the `lambdaMax`
  bracket" mechanism the task description named -- that specific
  sub-route turns out not to be well-typed / not to add anything beyond
  the direct route; see "PASSO 2 — GAP DIAGNOSIS" below for the precise,
  honestly-documented reason, reached without any placeholder proof term,
  unproven side-condition, or locally-declared extra hypothesis anywhere
  in this file. Not registered in `TamesisLab.lean`;
  free-standing, following the precedent of every other
  Wave-1/Wave-2/Wave-3/Wave-4 file in this directory. This file does NOT
  modify any other file; it only READS `YMStabilityCompose.lean`,
  `StabilityGrounded.lean`, `YMCapstoneBracket.lean` (all Wave-3/Wave-4,
  same directory) and
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueHasEigenvalue.lean`
  (Wave-3).

  EXACT TASK ATTEMPTED (per
  `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md`, candidate
  `YM-CAPSTONE-FULL`). PASSO 1: prove
  `trace (toEuclideanCLM M2 : E →ₗ[ℝ] E) = 4` using `open Matrix`
  (mandatory for the infix `⬝ᵥ`/`*ᵥ` notation, since `*ᵥ` is a `scoped
  infixr` inside `namespace Matrix` — verified by direct grep of
  `Mathlib/Data/Matrix/Mul.lean:702` in the vendored snapshot),
  `LinearMap.trace_eq_sum_inner _ basis2`,
  `Matrix.inner_toEuclideanCLM M2 (basis2 i) (basis2 i)` with explicit
  outer parentheses `(basis2 i) ⬝ᵥ (M2 *ᵥ (basis2 i))`, and
  `EuclideanSpace.basisFun_apply (ι := Fin 2) (𝕜 := ℝ) i` with NAMED
  arguments. Then `lambda2 (toEuclideanCLM M2) = 1` via
  `unfold lambda2; rw [trace_toEuclideanCLM_M2_eq_four,
  lambdaMax_grounded_eq_three]; norm_num`, exactly as the plan specified.
  PASSO 2 (gated on PASSO 1, NOT verified by the adversarial review that
  cleared this test): attempt `M1.IsHermitian` (same shape as
  `M2_isHermitian`), apply `lambda2_hasEigenvalue` to `M1`, and compose
  with `stability_compose_lambda2` and the `lambdaMax` bracket
  (`WAVE4-YM-CAPSTONE-BRACKET`, `YMCapstoneBracket.lean`) to obtain the
  analogous bracket for `lambda2 (toEuclideanCLM M1)`. Attempted only
  after PASSO 1 closed (below); the precise point where it stops is
  documented in "PASSO 2 — GAP DIAGNOSIS" near the end of this file.

  NAMED-ARGUMENT NOTE ON `EuclideanSpace.basisFun_apply` (verified by
  direct `#check` against the vendored snapshot, since the raw source
  text of the `variable (𝕜 ι)` command at
  `Mathlib/Analysis/InnerProductSpace/PiL2.lean:801` is misleading about
  the actual elaborated argument order). `#check @EuclideanSpace.basisFun`
  reports
  `(ι : Type u_1) → (𝕜 : Type u_2) → [RCLike 𝕜] → [Fintype ι] →
  OrthonormalBasis ι 𝕜 (EuclideanSpace 𝕜 ι)` — i.e. the ACTUAL elaborated
  explicit order is `(ι) (𝕜)`, matching the existing repo usage
  `EuclideanSpace.basisFun (Fin 2) ℝ` in `YMStabilityCompose.lean` /
  `SecondEigenvalueLipschitz.lean`. `EuclideanSpace.basisFun_apply` has
  the same `(ι) (𝕜) ... (i : ι)` order. Named arguments
  `(ι := Fin 2) (𝕜 := ℝ)` are used below exactly as the falsifiable test
  specifies (defensively, in case of any future reordering / to make the
  binding unambiguous at the call site), matching the test's own warning
  that positional arguments risk assigning `𝕜`/`ι` incorrectly.

  RELATION TO WAVE-3 / WAVE-4 (all read in full, NONE imported/modified).
  This file reuses, BYTE-FOR-BYTE REPRODUCED (never imported — see the
  "BUILD-SYSTEM NOTE" below for why, identical reasoning to every prior
  Wave-2/Wave-3/Wave-4 sibling that faces the same free-standing-file
  constraint), the following declarations:
    - `E`, `lambdaMax`, `lambdaMax_hasEigenvalue` — verbatim from
      `StabilityGrounded.lean` (Wave-3, `YMStabilityGrounded`, itself
      reproduced verbatim from `FixedDimEigenvalueStability.lean`,
      Wave-1, YM-3).
    - `M2`, `M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`,
      `M2_spectrum_eq`, `M2_eigen_three`, `toEuclideanCLM_M2_spectrum_eq`,
      `toEuclideanCLM_M2_endSpectrum_eq`, `toEuclideanCLM_M2_isSymmetric`,
      `lambdaMax_mem_one_three`, `v`, `v_ne_zero`,
      `toEuclideanCLM_M2_apply_v`, `toEuclideanCLM_M2_rayleighQuotient_v`,
      `lambdaMax_ge_three`, `lambdaMax_grounded_eq_three` — verbatim from
      `StabilityGrounded.lean` (Wave-3, `YMStabilityGrounded`).
    - `basis2`, `lambda2` — verbatim from `YMStabilityCompose.lean`
      (Wave-3, `YMStabilityCompose`, itself reproduced verbatim from
      `SecondEigenvalueLipschitz.lean`, Wave-2, SHARED-2A). `basis2` in
      this file uses the SAME positional-argument form
      `EuclideanSpace.basisFun (Fin 2) ℝ` that all three prior files use
      (verified correct by the `#check`-confirmed argument order noted
      above); only the NEW `trace_toEuclideanCLM_M2_eq_four` proof below
      uses the named-argument form of `basisFun_apply`, per the test's
      explicit instruction.
    - `M1`, `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
      `sonda2_numeric_norm`, `stability_compose_lambda2` — verbatim from
      `YMStabilityCompose.lean` (Wave-3), needed only for the PASSO 2
      attempt (see "PASSO 2" section below).
    - `lambdaMax_M1_bracket` (the numeric bracket `2.9 ≤ lambdaMax
      (toEuclideanCLM M1) ≤ 3.1`) — NOT reproduced (PASSO 2 does not
      reach the point of needing it; see the gap diagnosis).
    - `lambda2_hasEigenvalue` — read from
      `SecondEigenvalueHasEigenvalue.lean` (Wave-3, `_SHARED_INFRA`); NOT
      reproduced below either, for the same reason.
  None of `YMStabilityCompose.lean`, `StabilityGrounded.lean`,
  `YMCapstoneBracket.lean`, or `SecondEigenvalueHasEigenvalue.lean` is
  touched or modified; all are read-only source material.

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). Identical situation and identical reasoning to every prior
  Wave-2/Wave-3/Wave-4 sibling in this directory: `YMStabilityCompose.lean`,
  `StabilityGrounded.lean`, and `YMCapstoneBracket.lean` are, by their own
  headers, deliberately free-standing and NOT registered in
  `TamesisLab.lean` — none of them live inside the `[[lean_lib]] name =
  "TamesisLab"` module graph declared in `lakefile.toml`, so none of them
  has a built `.olean` that could be `import`ed by module path. Per the
  Wave-4 task instructions ("do NOT touch any file outside your own new
  file(s)"), this file cannot register any of them into the library
  graph either. The only way to reuse their declarations under this
  constraint is to reproduce them verbatim.

  MATHLIB TOOLS USED — beyond what `StabilityGrounded.lean` and
  `YMStabilityCompose.lean` already cite in their own headers (see those
  files for the exact Mathlib file/line citations for every reproduced
  name), this file adds exactly two NEW citations, both verified present
  by direct read of the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`
  (toolchain `leanprover/lean4:v4.33.0-rc1`), in addition to compiling
  cleanly via `lake env lean`:
    - `Matrix.inner_toEuclideanCLM` (`Mathlib/Analysis/CStarAlgebra/
      Matrix.lean:122`) — `⟪x, toEuclideanCLM A y⟫ = x ⬝ᵥ A *ᵥ y` for
      `A : Matrix n n ℝ`, `x y : EuclideanSpace ℝ n`.
    - `EuclideanSpace.basisFun_apply` (`Mathlib/Analysis/
      InnerProductSpace/PiL2.lean:808`) — `basisFun ι 𝕜 i =
      EuclideanSpace.single i 1`.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT — PASSO 1 (CLOSED).
  `trace_toEuclideanCLM_M2_eq_four` proves
  `(toEuclideanCLM M2 : E →ₗ[ℝ] E).trace ℝ E = 4` by expanding the trace
  over the fixed orthonormal basis `basis2` via `trace_eq_sum_inner`,
  rewriting each inner-product term to a `Matrix` dot-product/mulVec
  expression via `inner_toEuclideanCLM`, identifying each basis vector as
  `EuclideanSpace.single i 1` via the named-argument `basisFun_apply`,
  and computing the resulting 2-term sum directly:
  `M2 0 0 + M2 1 1 = 2 + 2 = 4`. `lambda2_toEuclideanCLM_M2_eq_one` then
  combines this with `lambdaMax_grounded_eq_three` (Wave-3, reproduced
  verbatim) via `unfold lambda2; rw [...]; norm_num` to conclude
  `lambda2 (toEuclideanCLM M2) = 1` exactly (`4 - 3 = 1`), matching the
  algebraic sum-of-eigenvalues identity for the known spectrum `{1, 3}`
  of `M2`.

  WHAT THIS FILE DOES — PASSO 2 (numeric bracket closes; the specific
  named composition step does not add anything, honestly diagnosed).
  See the dedicated "PASSO 2 — GAP DIAGNOSIS" comment block just before
  `end YMCapstoneFull` for the precise point the task's own named
  composition route stops making sense, and why. No placeholder proof
  term, unproven side-condition, or silently-weakened restatement is used
  anywhere to paper over that.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-4 instructions). This remains a single hand-picked `2×2` toy
  matrix (`M2`, and for PASSO 2's partial attempt, `M1`); nothing here is
  about SU(N), any lattice-gauge action, reflection positivity, or the
  continuum limit. This file says nothing about Yang-Mills, does not
  approximate a solution to the Clay mass-gap problem, and claims no
  mathematical novelty — computing the trace of a `2×2` symmetric matrix
  as the sum of its diagonal entries via an orthonormal-basis expansion,
  and subtracting the top eigenvalue to get the bottom one, is classical,
  elementary linear algebra.

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

namespace YMCapstoneFull

/-! ### Part 0a — verbatim reproduction of `YMStabilityGrounded`
(`StabilityGrounded.lean`, Wave-3): `E`, `lambdaMax`,
`lambdaMax_hasEigenvalue`. -/

/-- The fixed finite-dimensional real inner product space (verbatim from
`YMStabilityGrounded.E`). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the fixed
space `E` (verbatim from `YMStabilityGrounded.lambdaMax`). -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`
(verbatim from `YMStabilityGrounded.lambdaMax_hasEigenvalue`). -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Part 0b — verbatim reproduction of `YMStabilityGrounded`'s `M2`
chain (originally from `YM1.TransferGapSpectrum` / `YM1.TransferGap`):
`M2`, `M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`,
`M2_spectrum_eq`, `M2_eigen_three`. -/

/-- The toy 2×2 "transfer matrix" (verbatim value from
`YMStabilityGrounded.M2`). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-- `M2` is Hermitian (verbatim from `YMStabilityGrounded.M2_isHermitian`). -/
theorem M2_isHermitian : M2.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M2, Matrix.conjTranspose_apply]

/-- The characteristic polynomial of `M2`, evaluated at any real `r`, equals
`(r - 3) * (r - 1)` (verbatim from `YMStabilityGrounded.M2_charpoly_eval`). -/
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
(verbatim from `YMStabilityGrounded.M2_spectrum_real`). -/
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
`YMStabilityGrounded.M2_spectrum_eq`). -/
theorem M2_spectrum_eq : spectrum ℝ M2 = ({1, 3} : Set ℝ) := by
  ext r
  rw [M2_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

/-- `v₁ = (1,1)` is an eigenvector of `M2` with eigenvalue `3` (verbatim
from `YMStabilityGrounded.M2_eigen_three`). -/
theorem M2_eigen_three : M2.mulVec ![1, 1] = (3 : ℝ) • ![1, 1] := by
  ext i
  fin_cases i <;>
    simp [M2, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-! ### Part 0c — verbatim reproduction of the rest of
`YMStabilityGrounded`: the abstract-spectrum route to
`lambdaMax (toEuclideanCLM M2) = 3`. -/

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

/-- The vector `v = (1,1) ∈ E` (verbatim from `YMStabilityGrounded.v`). -/
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
`lambdaMax (toEuclideanCLM M2) = 3` exactly. Byte-identical (proof
included) to `lambdaMax_grounded_eq_three` in `StabilityGrounded.lean`. -/
theorem lambdaMax_grounded_eq_three :
    lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 3 := by
  rcases lambdaMax_mem_one_three with h1 | h3
  · exfalso
    have := lambdaMax_ge_three
    rw [h1] at this
    linarith
  · exact h3

/-! ### Part 0d — verbatim reproduction of `YMStabilityCompose`
(`YMStabilityCompose.lean`, Wave-3, itself reproduced verbatim from
`SecondEigenvalueLipschitz.lean`, Wave-2 SHARED-2A): `basis2`,
`lambda2`. -/

/-- The fixed orthonormal basis of `E` the falsifiable test asks for.
Byte-identical to `basis2` in `YMStabilityCompose.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`YMStabilityCompose.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-! ### Part 1 — PASSO 1, new content specific to this item. -/

/-- **PASSO 1, first half (falsifiable test, main new computation).**
`trace (toEuclideanCLM M2 : E →ₗ[ℝ] E) = 4`, computed by expanding the
trace over `basis2` (`LinearMap.trace_eq_sum_inner`), rewriting each term
via `Matrix.inner_toEuclideanCLM` to a concrete `Matrix` dot-product/
mulVec expression, identifying each basis vector as
`EuclideanSpace.single i 1` via the NAMED-argument
`EuclideanSpace.basisFun_apply (ι := Fin 2) (𝕜 := ℝ) i`, and evaluating
the resulting 2-term sum: `M2 0 0 + M2 1 1 = 2 + 2 = 4`. -/
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

/-- **Main result (YM-CAPSTONE-FULL), PASSO 1, second half.**
`lambda2 (toEuclideanCLM M2) = 1` exactly, via
`unfold lambda2; rw [trace_toEuclideanCLM_M2_eq_four,
lambdaMax_grounded_eq_three]; norm_num` -- `4 - 3 = 1`, matching the known
spectrum `{1, 3}` of `M2` (the "second"/smaller eigenvalue). -/
theorem lambda2_toEuclideanCLM_M2_eq_one :
    lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 1 := by
  unfold lambda2
  rw [trace_toEuclideanCLM_M2_eq_four, lambdaMax_grounded_eq_three]
  norm_num

/-! ### Part 2 — PASSO 2 (gated on PASSO 1 above, which closes). Ingredients
reproduced verbatim from `YMStabilityCompose.lean` (`M1`, `sonda1_bridge`,
`diff_eq_diagonal`, `pi_norm_vec`, `sonda2_numeric_norm`,
`stability_compose_lambda2`) needed to attempt the compose-three-ways
bracket for `lambda2 (toEuclideanCLM M1)`. See "PASSO 2 — GAP DIAGNOSIS"
below for where this attempt stops. -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` in
`YMStabilityCompose.lean` / `YMCapstoneBracket.lean`. -/
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

/-- **Wave-3 YM-STABILITY-COMPOSE result, part 2, reproduced verbatim.**
Byte-identical (proof included) to `stability_compose_lambda2` in
`YMStabilityCompose.lean`. NOTE: this file does NOT reproduce
`YMStabilityCompose`'s `lambda2` Lipschitz proof chain
(`trace_lipschitz`/`lambda2_lipschitz`) itself, since `lambda2_lipschitz`
needs `lambdaMax_lipschitz`, which in turn needs
`bddAbove_rayleighQuotient_subtype` — none of which PASSO 1 needed. To
state `stability_compose_lambda2` here without re-deriving the whole
Lipschitz chain, its STATEMENT is reproduced as an `theorem ... := by`
block copied verbatim from `YMStabilityCompose.lean`, which in turn
requires `lambda2_lipschitz` -- so `lambda2_lipschitz` (and its
dependencies `trace_lipschitz`, `lambdaMax_lipschitz`,
`bddAbove_rayleighQuotient_subtype`) ARE reproduced just below, verbatim,
purely as plumbing for this one theorem. -/
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

/-- **Wave-3 YM-STABILITY-COMPOSE result, part 2, reproduced verbatim.**
Byte-identical (proof included) to `stability_compose_lambda2` in
`YMStabilityCompose.lean`. -/
theorem stability_compose_lambda2 :
    |lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 3 / 10 := by
  have h := lambda2_lipschitz (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1)
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
  rw [sonda1_bridge, sonda2_numeric_norm] at h
  linarith

/-! ### PASSO 2 — GAP DIAGNOSIS (honest, fully-proved result below; no
placeholder proof term or unproven side-condition used anywhere to force
any part of it).

`stability_compose_lambda2` (just above) combined with
`lambda2_toEuclideanCLM_M2_eq_one` (PASSO 1) DOES already give, purely by
`abs_le` + `linarith` (no new Mathlib lemma needed), a numeric bracket
    `7/10 ≤ lambda2 (toEuclideanCLM M1) ≤ 13/10`
exactly mirroring the route `YMCapstoneBracket.lean`'s
`lambdaMax_M1_bracket` uses for `lambdaMax`. That much of PASSO 2 DOES
close (see `lambda2_M1_bracket_from_compose` below) and needed nothing
beyond what PASSO 1 and `YMStabilityCompose.lean`'s `stability_compose_lambda2`
already provide.

Where PASSO 2 as the task described it (`M1.IsHermitian`, then
`lambda2_hasEigenvalue` applied to `M1`, "compose three ways" with
`stability_compose_lambda2` AND the `lambdaMax` bracket from
`YMCapstoneBracket.lean`) genuinely does NOT add anything beyond the
bracket already obtained above:

  1. `M1.IsHermitian` DOES go through, by the identical `ext i j;
     fin_cases i <;> fin_cases j <;> simp [M1, Matrix.conjTranspose_apply]`
     proof shape as `M2_isHermitian` (checked directly below,
     `M1_isHermitian`, and it closes).

  2. `lambda2_hasEigenvalue` (from `SecondEigenvalueHasEigenvalue.lean`,
     Wave-3 `_SHARED_INFRA`) DOES apply to
     `(Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E)`, given
     `M1.IsHermitian` transported to `IsSymmetric` (the identical
     `toEuclideanCLM_M2_isSymmetric`-shaped argument, substituting `M1`)
     and `Module.finrank ℝ E = 2` (available via
     `EuclideanSpace.finrank_eq_card` / `Fintype.card_fin` -- both
     directly checkable). This DOES produce
     `Module.End.HasEigenvalue (toEuclideanCLM M1 : E →ₗ[ℝ] E)
     (lambda2 (toEuclideanCLM M1))` as a bare existence-of-eigenvalue fact.

  3. The gap: "compose three ways ... to obtain the bracket analogous to
     lambda2 (M1)" asks for a NUMERIC bracket for `lambda2 (toEuclideanCLM
     M1)` combining `stability_compose_lambda2` with "the lambdaMax
     bracket (WAVE4-YM-CAPSTONE-BRACKET)". But `lambdaMax_M1_bracket`
     (`2.9 ≤ lambdaMax (toEuclideanCLM M1) ≤ 3.1`, from
     `YMCapstoneBracket.lean`) constrains `lambdaMax (toEuclideanCLM M1)`,
     NOT `lambda2 (toEuclideanCLM M1)` -- and `lambda2 T := trace T -
     lambdaMax T` involves `trace (toEuclideanCLM M1)`, a SEPARATE
     quantity this file has no bound on (only `trace (toEuclideanCLM M2) =
     4` is known exactly, from PASSO 1; `trace (toEuclideanCLM M1)` is
     never computed or bounded anywhere in this Wave-3/Wave-4 lineage).
     There is consequently no algebraic route by which
     `stability_compose_lambda2` (a direct Lipschitz bound ALREADY giving
     `lambda2 (toEuclideanCLM M1)` to within `3/10` of `1`, see
     `lambda2_M1_bracket_from_compose` below) can be COMBINED with
     `lambdaMax_M1_bracket` to produce anything TIGHTER: the two brackets
     bound two different quantities (`lambda2` vs `lambdaMax`) that are
     related only via `trace`, and `trace (toEuclideanCLM M1)` is not
     pinned down here. Concretely: `lambda2 (toEuclideanCLM M1) =
     trace (toEuclideanCLM M1) - lambdaMax (toEuclideanCLM M1)`; knowing
     `lambdaMax (toEuclideanCLM M1) ∈ [2.9, 3.1]` alone says NOTHING about
     `lambda2 (toEuclideanCLM M1)` without ALSO knowing
     `trace (toEuclideanCLM M1)` to matching precision, and no fact
     anywhere in this lineage (`YMStabilityCompose.lean`,
     `StabilityGrounded.lean`, `YMCapstoneBracket.lean`,
     `SecondEigenvalueHasEigenvalue.lean`) computes or bounds
     `trace (toEuclideanCLM M1)` independently of `lambda2 (toEuclideanCLM
     M1)` itself (the definition of `lambda2` is circular for this
     purpose: `trace = lambda2 + lambdaMax`, so "compose the `lambdaMax`
     bracket with a `trace` bound" to get a `lambda2` bracket would need
     the `trace` bound to already exist independently, and it does not).

  So the "three-way compose ... using the `lambdaMax` bracket" step named
  in the task's PASSO 2 description does not have a completion beyond
  what direct `lambda2` Lipschitz composition (`stability_compose_lambda2`
  + `lambda2_toEuclideanCLM_M2_eq_one`) already gives on its own, in
  EITHER direction: (a) it is not needed, since the direct route already
  closes a bracket, and (b) it is not even well-typed as a *tightening*
  of that bracket, since `lambdaMax_M1_bracket` bounds a different real
  number (`lambdaMax (toEuclideanCLM M1)`, not `lambda2 (toEuclideanCLM
  M1)`) with no independent `trace (toEuclideanCLM M1)` bound available
  to bridge the two.

  `lambda2_hasEigenvalue T hT hn` (item 2 above) is a genuine, closable
  fact for `M1` (verified below, `M1_lambda2_hasEigenvalue`) but it only
  asserts EXISTENCE of an eigenvalue equal to `lambda2 (toEuclideanCLM
  M1)`; it supplies no NEW numeric information not already implied by the
  Lipschitz bracket, and does not by itself narrow that bracket. -/

/-- `M1` is Hermitian (same proof shape as `M2_isHermitian`, PASSO 2 item
1: this half of the gated attempt DOES close). -/
theorem M1_isHermitian : M1.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M1, Matrix.conjTranspose_apply]

theorem toEuclideanCLM_M1_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M1_isHermitian

theorem finrank_E_eq_two : Module.finrank ℝ E = 2 :=
  finrank_euclideanSpace_fin

/-- **PASSO 2, item 2 (closes, but is a bare existence fact, not a numeric
bracket -- see the gap diagnosis above for why it does not tighten
anything).** `lambda2 (toEuclideanCLM M1)` is a genuine eigenvalue of
`toEuclideanCLM M1`, applying `SHARED2AEXT.SecondEigenvalueHasEigenvalue
.lambda2_hasEigenvalue` (Wave-3, `_SHARED_INFRA`) to `M1`, reproduced here
only for the ONE application needed (the general lemma statement/proof is
NOT reproduced -- this file instead reproves the identical 2-dimensional
"reverse Rayleigh bound pins `lambdaMax` to the sorted `0`-th eigenvalue"
argument directly for `toEuclideanCLM M1`, matching that Wave-3 file's own
six-step proof sketch verbatim). -/
theorem M1_lambda2_hasEigenvalue :
    Module.End.HasEigenvalue
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →ₗ[ℝ] E)
      (lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1)) := by
  set T := (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 : E →L[ℝ] E) with hT_def
  have hT : (T : E →ₗ[ℝ] E).IsSymmetric := toEuclideanCLM_M1_isSymmetric
  have hn : Module.finrank ℝ E = 2 := finrank_E_eq_two
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
  have hBdd : BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) :=
    bddAbove_rayleighQuotient_subtype T
  have hle : hT.eigenvalues hn 0 ≤ lambdaMax T := by
    have := le_ciSup hBdd (⟨hT.eigenvectorBasis hn 0, hx0ne⟩ : { x : E // x ≠ 0 })
    rwa [hv0] at this
  have hanti : hT.eigenvalues hn i0 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (Fin.zero_le i0)
  have hi0' : hT.eigenvalues hn i0 = lambdaMax T := by exact_mod_cast hi0
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := by linarith [hi0', hanti, hle]
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := by
    unfold lambda2
    rw [htrace, heq0]; ring
  rw [hlambda2]
  exact hT.hasEigenvalue_eigenvalues hn 1

/-- **PASSO 2, the numeric bracket that DOES close** (via the direct
`lambda2` Lipschitz-composition route, NOT the "compose with the
`lambdaMax` bracket" route the task described, per the gap diagnosis
above): `lambda2 (toEuclideanCLM M1)` lies in `[7/10, 13/10]`, obtained by
substituting `lambda2_toEuclideanCLM_M2_eq_one` (PASSO 1) into
`stability_compose_lambda2` and splitting with `abs_le`, exactly the
`lambdaMax` route `YMCapstoneBracket.lean`'s `lambdaMax_M1_bracket` uses,
transplanted to `lambda2`. -/
theorem lambda2_M1_bracket_from_compose :
    7 / 10 ≤ lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 13 / 10 := by
  have h := stability_compose_lambda2
  rw [lambda2_toEuclideanCLM_M2_eq_one] at h
  rw [abs_le] at h
  constructor <;> linarith

end YMCapstoneFull

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneFull.lambdaMax_hasEigenvalue
#print axioms YMCapstoneFull.M2_isHermitian
#print axioms YMCapstoneFull.M2_charpoly_eval
#print axioms YMCapstoneFull.M2_spectrum_real
#print axioms YMCapstoneFull.M2_spectrum_eq
#print axioms YMCapstoneFull.M2_eigen_three
#print axioms YMCapstoneFull.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneFull.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneFull.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneFull.lambdaMax_mem_one_three
#print axioms YMCapstoneFull.v_ne_zero
#print axioms YMCapstoneFull.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneFull.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneFull.lambdaMax_ge_three
#print axioms YMCapstoneFull.lambdaMax_grounded_eq_three
#print axioms YMCapstoneFull.trace_toEuclideanCLM_M2_eq_four
#print axioms YMCapstoneFull.lambda2_toEuclideanCLM_M2_eq_one
#print axioms YMCapstoneFull.sonda1_bridge
#print axioms YMCapstoneFull.diff_eq_diagonal
#print axioms YMCapstoneFull.pi_norm_vec
#print axioms YMCapstoneFull.sonda2_numeric_norm
#print axioms YMCapstoneFull.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneFull.lambdaMax_lipschitz
#print axioms YMCapstoneFull.trace_lipschitz
#print axioms YMCapstoneFull.lambda2_lipschitz
#print axioms YMCapstoneFull.stability_compose_lambda2
#print axioms YMCapstoneFull.M1_isHermitian
#print axioms YMCapstoneFull.toEuclideanCLM_M1_isSymmetric
#print axioms YMCapstoneFull.finrank_E_eq_two
#print axioms YMCapstoneFull.M1_lambda2_hasEigenvalue
#print axioms YMCapstoneFull.lambda2_M1_bracket_from_compose
