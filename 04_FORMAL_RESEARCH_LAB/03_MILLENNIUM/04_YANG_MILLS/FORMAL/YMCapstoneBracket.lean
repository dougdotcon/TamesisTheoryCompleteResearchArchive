/-
  YM-CAPSTONE-BRACKET — a numeric bracket `2.9 ≤ lambdaMax (toEuclideanCLM
  M1) ≤ 3.1`, obtained by combining the Wave-3 Lipschitz-composition
  result for `M1`/`M2` with the Wave-3 exact grounding
  `lambdaMax (toEuclideanCLM M2) = 3` (Wave-4 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-4 task instructions on
  build contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1/Wave-2/Wave-3/Wave-4 file in this directory. This file
  does NOT modify any other file; it only READS two Wave-3 files.

  EXACT TASK ATTEMPTED (per
  `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md`, candidate
  `YM-CAPSTONE-BRACKET`). Nothing broader than this was attempted: a
  single capstone file deduplicating `E`, `lambdaMax`, `M2` from
  `YMStabilityCompose.lean` and `StabilityGrounded.lean` (Wave-3, both in
  this same directory) under one shared namespace, WITHOUT
  `open Matrix WithLp` (that combinator is vestigial here and, when
  present alongside `YMStabilityCompose.lean`'s verbatim
  `lambdaMax_lipschitz` proof — which relies on the bare identifier
  `sub_apply` resolving unambiguously — causes an "ambiguous, possible
  interpretations" elaboration error against `Matrix.sub_apply` once
  `Matrix` is opened; every reference to a `Matrix`/`WithLp` declaration
  below is therefore fully qualified instead), then proving
  `lambdaMax_M1_bracket : 2.9 ≤ lambdaMax (toEuclideanCLM M1) ∧
  lambdaMax (toEuclideanCLM M1) ≤ 3.1` via exactly
  `rw [lambdaMax_grounded_eq_three] at h; rw [abs_le] at h;
  constructor <;> linarith`, as the plan specified.

  RELATION TO WAVE-3 (both read in full, NEITHER imported/modified). This
  file reuses, BYTE-FOR-BYTE REPRODUCED (never imported — see the
  "BUILD-SYSTEM NOTE" below for why, identical reasoning to every prior
  Wave-2/Wave-3/Wave-4 sibling that faces the same free-standing-file
  constraint), the following declarations. Each is stated once here
  (deduplicated) even though both source files below reproduce it
  independently, since `E`, `lambdaMax`, and `M2` are byte-identical
  across both:
    - `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
      `lambdaMax_lipschitz` — verbatim from `YMStabilityCompose.lean`
      (Wave-3, `YMStabilityCompose`, itself reproduced verbatim from
      `FixedDimEigenvalueStability.lean`, Wave-1, YM-3).
    - `lambdaMax_hasEigenvalue` — verbatim from `StabilityGrounded.lean`
      (Wave-3, `YMStabilityGrounded`, itself reproduced verbatim from
      `FixedDimEigenvalueStability.lean`, Wave-1, YM-3).
    - `M2`, `M1`, `sonda1_bridge`, `diff_eq_diagonal`, `pi_norm_vec`,
      `sonda2_numeric_norm`, `stability_compose_lambdaMax` — verbatim
      from `YMStabilityCompose.lean` (Wave-3, `YMStabilityCompose`; `M1`,
      `M2`, `sonda1_bridge`, `sonda2_numeric_norm`'s own internal
      dependencies `diff_eq_diagonal`/`pi_norm_vec` were themselves
      already reproduced there verbatim from `L2OperatorNormProbe.lean`,
      Wave-2, YM-1+YM-3).
    - `M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`,
      `M2_spectrum_eq`, `M2_eigen_three`, `toEuclideanCLM_M2_spectrum_eq`,
      `toEuclideanCLM_M2_endSpectrum_eq`, `toEuclideanCLM_M2_isSymmetric`,
      `lambdaMax_mem_one_three`, `v`, `v_ne_zero`,
      `toEuclideanCLM_M2_apply_v`, `toEuclideanCLM_M2_rayleighQuotient_v`,
      `lambdaMax_ge_three`, `lambdaMax_grounded_eq_three` — verbatim from
      `StabilityGrounded.lean` (Wave-3, `YMStabilityGrounded`; these were
      themselves already reproduced there verbatim from
      `TransferGapSpectrumCharpoly.lean` (Wave-2, YM-1-CONNECT) and
      `FiniteLatticeTransferGap.lean` (Wave-1, YM-1), per that file's own
      header).
  Neither `YMStabilityCompose.lean` nor `StabilityGrounded.lean` is
  touched or imported; both are read-only source material reproduced
  here (deduplicating their shared `E`/`lambdaMax`/`M2` fragment into one
  copy) under the same free-standing Lake-module-path constraint every
  prior file in this line has already documented. This file deliberately
  drops `lambda2`/`lambda2_lipschitz`/`trace_lipschitz`/`basis2` and
  `stability_compose_lambda2`, since the falsifiable test for this item
  is about `lambdaMax` only.

  BUILD-SYSTEM NOTE (why the pieces above are reproduced instead of
  imported). `YMStabilityCompose.lean` and `StabilityGrounded.lean` are,
  by their own header comments, deliberately free-standing and NOT
  registered in `TamesisLab.lean` — neither lives inside the
  `[[lean_lib]] name = "TamesisLab"` module graph declared in
  `lakefile.toml`, so neither has a built `.olean` that could be
  `import`ed by module name. Per the Wave-4 task instructions ("do NOT
  touch any file outside your own new file(s)"), this file cannot
  register either of them into the library graph. The only way to reuse
  their declarations under this constraint is to reproduce them verbatim
  (byte-identical `def`/`theorem` text, copied directly from the two
  source files named above), which is not a redeclaration of new objects
  but the same `E`, `lambdaMax`, `M1`, `M2`, `lambdaMax_lipschitz`,
  `stability_compose_lambdaMax`, `lambdaMax_grounded_eq_three`, etc.,
  reproduced because the lab's own free-standing-file convention leaves
  no other route to them.

  MATHLIB TOOLS USED — none new beyond what `YMStabilityCompose.lean` and
  `StabilityGrounded.lean` already cite in their own headers (see those
  two files for the exact Mathlib file/line citations for every name
  used below, e.g. `ContinuousLinearMap.rayleighQuotient`,
  `AlgEquiv.spectrum_eq`, `ContinuousLinearMap.spectrum_eq`,
  `Module.End.hasEigenvalue_iff_mem_spectrum`,
  `Matrix.toEuclideanCLM_toLp`, `Matrix.isSymmetric_toEuclideanLin_iff`,
  `Matrix.l2_opNorm_toEuclideanCLM`, `Matrix.l2_opNorm_diagonal`); this
  file adds no citation beyond what those two files already established.
  The one genuinely new combinator step is `abs_le` (root namespace,
  `a ≤ b ↔ -b ≤ a ∧ a ≤ b` variant used here as
  `|a - b| ≤ c ↔ -c ≤ a - b ∧ a - b ≤ c`), applied to
  `stability_compose_lambdaMax` after substituting
  `lambdaMax (toEuclideanCLM M2) = 3` via `lambdaMax_grounded_eq_three`.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT. `stability_compose_lambdaMax`
  gives `|lambdaMax (toEuclideanCLM M1) - lambdaMax (toEuclideanCLM M2)| ≤
  1/10` (Wave-3, reproduced verbatim). `lambdaMax_grounded_eq_three` gives
  `lambdaMax (toEuclideanCLM M2) = 3` (Wave-3, reproduced verbatim).
  `lambdaMax_M1_bracket` combines the two, exactly via
  `rw [lambdaMax_grounded_eq_three] at h; rw [abs_le] at h;
  constructor <;> linarith`, to conclude
  `2.9 ≤ lambdaMax (toEuclideanCLM M1) ≤ 3.1` — a numeric interval around
  `3` of half-width `1/10`, matching `1 * ‖M1 - M2‖ = 1 * (1/10)` exactly,
  no slack anywhere in the chain.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-4 instructions). This remains a single hand-picked `2×2` toy
  matrix pair (`M1`, `M2`, differing only in one diagonal entry by
  `1/10`); nothing here is about SU(N), any lattice-gauge action,
  reflection positivity, or the continuum limit. The bracket
  `[2.9, 3.1]` is not the tightest possible statement obtainable from
  these two facts (the exact value of `lambdaMax (toEuclideanCLM M1)` is
  not computed here, only bracketed); tightening it to an exact value
  would require an independent spectral computation for `M1` itself
  (analogous to what `StabilityGrounded.lean` did for `M2`), which is
  NOT attempted here. This file says nothing about Yang-Mills, does not
  approximate a solution to the Clay mass-gap problem, and claims no
  mathematical novelty — it is pure recombination, via `rw`/`abs_le`/
  `linarith`, of two previously-established, already-type-checked
  Wave-3 facts.
-/
import Mathlib

open scoped Matrix.Norms.L2Operator

namespace YMCapstoneBracket

/-! ### Part 0 — deduplicated shared content: `E`, `lambdaMax` (with its
supporting lemmas `bddAbove_rayleighQuotient_subtype`,
`lambdaMax_lipschitz`, `lambdaMax_hasEigenvalue`), and `M2`. Reproduced
once here even though both `YMStabilityCompose.lean` and
`StabilityGrounded.lean` reproduce it independently, since it is
byte-identical in both. NOTE: deliberately no `open Matrix WithLp` here
(see file header) — every `Matrix`/`WithLp` name below is fully
qualified. -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`YMStabilityCompose.lean` / `StabilityGrounded.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `YMStabilityCompose.lean` / `StabilityGrounded.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`YMStabilityCompose.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim.** `lambdaMax` is 1-Lipschitz
in operator norm on the fixed space `E`. Byte-identical (proof included)
to `lambdaMax_lipschitz` in `YMStabilityCompose.lean`. -/
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
        ContinuousLinearMap.reApplyInnerSelf_apply, sub_apply, inner_sub_left, sub_div]
    rw [hsub]
    exact (le_abs_self _).trans ((A - B).rayleighQuotient_le_norm (x : E))
  have hdiffBA : ∀ x : { x : E // x ≠ 0 },
      B.rayleighQuotient (x : E) - A.rayleighQuotient (x : E) ≤ ‖A - B‖ := by
    intro x
    have hsub : B.rayleighQuotient (x : E) - A.rayleighQuotient (x : E)
        = (B - A).rayleighQuotient (x : E) := by
      simp [ContinuousLinearMap.rayleighQuotient,
        ContinuousLinearMap.reApplyInnerSelf_apply, sub_apply, inner_sub_left, sub_div]
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
Byte-identical to `lambdaMax_hasEigenvalue` in `StabilityGrounded.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- `M2`, byte-for-byte identical across `YMStabilityCompose.lean` and
`StabilityGrounded.lean` (and `YM1.TransferGap.M`). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-! ### Part 1 — from `YMStabilityCompose.lean`: `M1`, `sonda1_bridge`,
`diff_eq_diagonal`, `pi_norm_vec`, `sonda2_numeric_norm`,
`stability_compose_lambdaMax`. -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` in
`YMStabilityCompose.lean` / `L2OperatorNormProbe.lean`. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

/-- **Sonda 1, part b, reproduced verbatim.** `Matrix.l2_opNorm_toEuclideanCLM`
rewrites `‖toEuclideanCLM M1 - toEuclideanCLM M2‖` to `‖M1 - M2‖`.
Byte-identical (proof included) to `sonda1_bridge` in
`YMStabilityCompose.lean`. -/
theorem sonda1_bridge :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 -
        Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2‖ = ‖M1 - M2‖ := by
  rw [← map_sub (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2))]
  exact Matrix.l2_opNorm_toEuclideanCLM (M1 - M2)

/-- `M1 - M2` is the diagonal matrix `diagonal ![0, 1/10]`. Byte-identical
to `diff_eq_diagonal` in `YMStabilityCompose.lean`. -/
theorem diff_eq_diagonal : M1 - M2 = Matrix.diagonal ![(0 : ℝ), 1 / 10] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [M1, M2]

/-- The Pi *sup*-norm of the concrete vector `![0, 1/10]` is exactly
`1/10`. Byte-identical to `pi_norm_vec` in `YMStabilityCompose.lean`. -/
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
`YMStabilityCompose.lean`. -/
theorem sonda2_numeric_norm : ‖M1 - M2‖ = 1 / 10 := by
  rw [diff_eq_diagonal, Matrix.l2_opNorm_diagonal]
  exact pi_norm_vec

/-- **Wave-3 YM-STABILITY-COMPOSE result, reproduced verbatim.** Chaining
`lambdaMax_lipschitz` with the concrete numeric bound
`sonda1_bridge`/`sonda2_numeric_norm`: the top-eigenvalue candidates of
`toEuclideanCLM M1` and `toEuclideanCLM M2` differ by at most `1/10`.
Byte-identical (proof included) to `stability_compose_lambdaMax` in
`YMStabilityCompose.lean`. -/
theorem stability_compose_lambdaMax :
    |lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 1 / 10 :=
  (lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact sonda2_numeric_norm.le)

/-! ### Part 2 — from `StabilityGrounded.lean`: grounding
`lambdaMax (toEuclideanCLM M2) = 3` via the abstract spectrum `{1, 3}`. -/

/-- `M2` is Hermitian. Byte-identical to `M2_isHermitian` in
`StabilityGrounded.lean`. -/
theorem M2_isHermitian : M2.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M2, Matrix.conjTranspose_apply]

/-- The characteristic polynomial of `M2`, evaluated at any real `r`, equals
`(r - 3) * (r - 1)`. Byte-identical to `M2_charpoly_eval` in
`StabilityGrounded.lean`. -/
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
Byte-identical to `M2_spectrum_real` in `StabilityGrounded.lean`. -/
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
`M2_spectrum_eq` in `StabilityGrounded.lean`. -/
theorem M2_spectrum_eq : spectrum ℝ M2 = ({1, 3} : Set ℝ) := by
  ext r
  rw [M2_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

/-- `v₁ = (1,1)` is an eigenvector of `M2` with eigenvalue `3`.
Byte-identical to `M2_eigen_three` in `StabilityGrounded.lean`. -/
theorem M2_eigen_three : M2.mulVec ![1, 1] = (3 : ℝ) • ![1, 1] := by
  ext i
  fin_cases i <;>
    simp [M2, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-- The closed-form abstract spectrum of `toEuclideanCLM M2`, via
`AlgEquiv.spectrum_eq` + `M2_spectrum_eq`. Byte-identical to
`toEuclideanCLM_M2_spectrum_eq` in `StabilityGrounded.lean`. -/
theorem toEuclideanCLM_M2_spectrum_eq :
    spectrum ℝ (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      = ({1, 3} : Set ℝ) := by
  rw [AlgEquiv.spectrum_eq (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2)) M2]
  exact M2_spectrum_eq

/-- Transported to the `Module.End ℝ E` spectrum via
`ContinuousLinearMap.spectrum_eq`. Byte-identical to
`toEuclideanCLM_M2_endSpectrum_eq` in `StabilityGrounded.lean`. -/
theorem toEuclideanCLM_M2_endSpectrum_eq :
    spectrum ℝ ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      : Module.End ℝ E) = ({1, 3} : Set ℝ) := by
  rw [← ContinuousLinearMap.spectrum_eq]
  exact toEuclideanCLM_M2_spectrum_eq

/-- `(toEuclideanCLM M2 : E →ₗ[ℝ] E).IsSymmetric`, transported from
`M2_isHermitian`. Byte-identical to `toEuclideanCLM_M2_isSymmetric` in
`StabilityGrounded.lean`. -/
theorem toEuclideanCLM_M2_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M2_isHermitian

/-- `lambdaMax (toEuclideanCLM M2) ∈ {1, 3}`, via
`Module.End.hasEigenvalue_iff_mem_spectrum`. Byte-identical to
`lambdaMax_mem_one_three` in `StabilityGrounded.lean`. -/
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

/-- The vector `v = (1,1) ∈ E`, the same eigenvector as `M2_eigen_three`,
transported into `EuclideanSpace ℝ (Fin 2)` via `WithLp.toLp`.
Byte-identical to `v` in `StabilityGrounded.lean`. -/
noncomputable def v : E := WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)

/-- Byte-identical to `v_ne_zero` in `StabilityGrounded.lean`. -/
theorem v_ne_zero : v ≠ 0 := by
  intro h
  have h0 : (WithLp.equiv 2 (Fin 2 → ℝ)) v 0 = (WithLp.equiv 2 (Fin 2 → ℝ)) (0 : E) 0 := by
    rw [h]
  simp [v, WithLp.equiv] at h0

/-- `toEuclideanCLM M2` applied to `v` equals `(3:ℝ) • v`. Byte-identical
to `toEuclideanCLM_M2_apply_v` in `StabilityGrounded.lean`. -/
theorem toEuclideanCLM_M2_apply_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) v = (3 : ℝ) • v := by
  show (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
      (WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)) = (3 : ℝ) • v
  rw [Matrix.toEuclideanCLM_toLp, M2_eigen_three]
  rfl

/-- The Rayleigh quotient of `toEuclideanCLM M2` at the explicit
eigenvector `v` is exactly `3`. Byte-identical to
`toEuclideanCLM_M2_rayleighQuotient_v` in `StabilityGrounded.lean`. -/
theorem toEuclideanCLM_M2_rayleighQuotient_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2).rayleighQuotient v = 3 := by
  have hvnorm : ‖v‖ ≠ 0 := norm_ne_zero_iff.mpr v_ne_zero
  rw [ContinuousLinearMap.rayleighQuotient, ContinuousLinearMap.reApplyInnerSelf_apply,
    toEuclideanCLM_M2_apply_v, real_inner_smul_left, real_inner_self_eq_norm_sq]
  rw [RCLike.re_to_real]
  field_simp

/-- `lambdaMax (toEuclideanCLM M2) ≥ 3`. Byte-identical to
`lambdaMax_ge_three` in `StabilityGrounded.lean`. -/
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

/-! ### Part 3 — new content specific to this item (YM-CAPSTONE-BRACKET):
the numeric bracket for `lambdaMax (toEuclideanCLM M1)`, obtained by
combining `stability_compose_lambdaMax` (Part 1) with
`lambdaMax_grounded_eq_three` (Part 2) exactly via the route the plan
specified. -/

/-- **Main result (YM-CAPSTONE-BRACKET).** `lambdaMax (toEuclideanCLM M1)`
lies in the numeric interval `[2.9, 3.1]`, obtained by substituting the
exact grounded value `lambdaMax (toEuclideanCLM M2) = 3`
(`lambdaMax_grounded_eq_three`) into the Lipschitz-composition bound
`|lambdaMax (toEuclideanCLM M1) - lambdaMax (toEuclideanCLM M2)| ≤ 1/10`
(`stability_compose_lambdaMax`) and splitting the resulting absolute-value
bound with `abs_le`. Proved exactly via
`rw [lambdaMax_grounded_eq_three] at h; rw [abs_le] at h;
constructor <;> linarith`, as the plan specified. -/
theorem lambdaMax_M1_bracket :
    2.9 ≤ lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ∧
      lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) ≤ 3.1 := by
  have h := stability_compose_lambdaMax
  rw [lambdaMax_grounded_eq_three] at h
  rw [abs_le] at h
  constructor <;> linarith

end YMCapstoneBracket

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMCapstoneBracket.bddAbove_rayleighQuotient_subtype
#print axioms YMCapstoneBracket.lambdaMax_lipschitz
#print axioms YMCapstoneBracket.lambdaMax_hasEigenvalue
#print axioms YMCapstoneBracket.sonda1_bridge
#print axioms YMCapstoneBracket.diff_eq_diagonal
#print axioms YMCapstoneBracket.pi_norm_vec
#print axioms YMCapstoneBracket.sonda2_numeric_norm
#print axioms YMCapstoneBracket.stability_compose_lambdaMax
#print axioms YMCapstoneBracket.M2_isHermitian
#print axioms YMCapstoneBracket.M2_charpoly_eval
#print axioms YMCapstoneBracket.M2_spectrum_real
#print axioms YMCapstoneBracket.M2_spectrum_eq
#print axioms YMCapstoneBracket.M2_eigen_three
#print axioms YMCapstoneBracket.toEuclideanCLM_M2_spectrum_eq
#print axioms YMCapstoneBracket.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMCapstoneBracket.toEuclideanCLM_M2_isSymmetric
#print axioms YMCapstoneBracket.lambdaMax_mem_one_three
#print axioms YMCapstoneBracket.v_ne_zero
#print axioms YMCapstoneBracket.toEuclideanCLM_M2_apply_v
#print axioms YMCapstoneBracket.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMCapstoneBracket.lambdaMax_ge_three
#print axioms YMCapstoneBracket.lambdaMax_grounded_eq_three
#print axioms YMCapstoneBracket.lambdaMax_M1_bracket
