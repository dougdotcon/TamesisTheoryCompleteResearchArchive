/-
  YM-STABILITY-COMPOSE — chaining the Lipschitz bounds for `lambdaMax` /
  `lambda2` with the concrete L2-operator-norm bound on the toy matrices
  `M1`, `M2` (Wave-3 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-3 task instructions on build
  contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other Wave-1/Wave-2/Wave-3 file in this directory. This file does NOT
  modify any other file; it only READS three Wave-1/Wave-2 files.

  EXACT TASK ATTEMPTED (per
  `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md`, candidate
  `YM-STABILITY-COMPOSE`). Nothing broader than this was attempted: a new
  autonomous file reproducing VERBATIM `E`, `lambdaMax`,
  `lambdaMax_lipschitz`, `lambda2`, `lambda2_lipschitz` (from the two
  "Lipschitz files" below) plus `M1`, `M2`, `sonda1_bridge`,
  `sonda2_numeric_norm` (from `L2OperatorNormProbe.lean`), then proving
  the two composed corollaries:
    `|lambdaMax (toEuclideanCLM M1) - lambdaMax (toEuclideanCLM M2)| ≤ 1/10`
    `|lambda2 (toEuclideanCLM M1) - lambda2 (toEuclideanCLM M2)| ≤ 3/10`
  via `(lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact
  sonda2_numeric_norm.le)`, and the same route for `lambda2`.

  BUILD-SYSTEM NOTE (why the pieces below are reproduced instead of
  imported — same situation already documented by every Wave-2/Wave-3
  sibling that reuses a free-standing file in this lab).
  `FixedDimEigenvalueStability.lean` (Wave-1, YM-3),
  `SecondEigenvalueLipschitz.lean` (Wave-2, SHARED-2A, at
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/`), and `L2OperatorNormProbe.lean`
  (Wave-2, YM-1+YM-3) are all, by their own headers, deliberately
  free-standing and NOT registered in `TamesisLab.lean` — none of them
  live inside the `[[lean_lib]] name = "TamesisLab"` module graph
  declared in `lakefile.toml`, so none of them has a built `.olean` that
  could be `import`ed by module name. Per the Wave-3 task instructions
  ("do NOT touch any file outside your own new file(s)"), this file
  cannot register any of them into the library graph either. The only
  way to reuse their declarations under this constraint is to reproduce
  them VERBATIM (byte-identical `def`/`theorem` text, copied directly
  from the three source files named above) rather than inventing
  different ones — this is not a redeclaration of new objects, it is the
  same `E`, `lambdaMax`, `lambdaMax_lipschitz`, `lambda2`,
  `lambda2_lipschitz`, `M1`, `M2`, `sonda1_bridge`, `sonda2_numeric_norm`
  (plus their own small internal dependencies, `bddAbove_rayleighQuotient_
  subtype`, `basis2`, `trace_lipschitz`, `diff_eq_diagonal`,
  `pi_norm_vec`), reproduced because the lab's own free-standing-file
  convention leaves no other route to them. Everything from "### New
  content specific to this item" onward IS new content specific to this
  item.

  MATHLIB TOOLS USED — none new. Every Mathlib name appearing below
  (`ContinuousLinearMap.rayleighQuotient`,
  `ContinuousLinearMap.rayleighQuotient_le_norm`,
  `LinearMap.trace_eq_sum_inner`, `EuclideanSpace.basisFun`,
  `abs_real_inner_le_norm`, `ContinuousLinearMap.le_opNorm`,
  `OrthonormalBasis.norm_eq_one`, `Finset.abs_sum_le_sum_abs`,
  `Matrix.toEuclideanCLM`, `Matrix.l2_opNorm_toEuclideanCLM`,
  `Matrix.l2_opNorm_diagonal`, `pi_norm_le_iff_of_nonneg`,
  `norm_le_pi_norm`, `map_sub`) was already verified present, at the
  cited locations, by the Wave-1/Wave-2 authoring sessions of the three
  source files (see those files' own header comments for the exact
  Mathlib file/line citations); this file adds no citation beyond what
  those three files already established, matching the plan's own finding
  that this item is "recombinacao pura de tres pecas ja type-checadas"
  (pure recombination of three already type-checked pieces).

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT. Both composed corollaries
  close exactly via the route the plan specified:
    `stability_compose_lambdaMax : |lambdaMax (toEuclideanCLM M1) -
      lambdaMax (toEuclideanCLM M2)| ≤ 1/10`
    `stability_compose_lambda2 : |lambda2 (toEuclideanCLM M1) -
      lambda2 (toEuclideanCLM M2)| ≤ 3/10`
  Each is `(lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact
  sonda2_numeric_norm.le)` / the analogous one-line combination for
  `lambda2_lipschitz`, i.e. exactly `1 * (1/10) = 1/10` and
  `3 * (1/10) = 3/10`, no slack anywhere in the chain.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-3 instructions). This remains a single hand-picked `2×2` toy
  matrix pair (`M1`, `M2`, differing only in one diagonal entry by
  `1/10`) with a fixed perturbation size; nothing here is about SU(N),
  any lattice-gauge action, reflection positivity, or the continuum
  limit. `lambda2` is (per `SecondEigenvalueLipschitz.lean`'s own header)
  an ALGEBRAIC stand-in (`trace - lambdaMax`) for "the second
  eigenvalue", not independently shown to be a genuine eigenvalue of
  `toEuclideanCLM M1`/`M2` in this file (that identification, for `M2`
  specifically, is the separate Wave-3 item `YM-STABILITY-GROUNDED`, not
  attempted here). This file says nothing about Yang-Mills, does not
  approximate a solution to the Clay mass-gap problem, and claims no
  mathematical novelty — it is pure recombination, via `.trans` and
  `rw`, of three previously-established, already-type-checked
  inequalities/identities.
-/
import Mathlib

open scoped Matrix.Norms.L2Operator

namespace YMStabilityCompose

/-! ### Reproduced verbatim from `FixedDimEigenvalueStability.lean`
(Wave-1, YM-3): `E`, `lambdaMax`, and its supporting lemmas. -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`FixedDimEigenvalueStability.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `FixedDimEigenvalueStability.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`FixedDimEigenvalueStability.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim.** `lambdaMax` is 1-Lipschitz
in operator norm on the fixed space `E`. Byte-identical (proof included)
to `lambdaMax_lipschitz` in `FixedDimEigenvalueStability.lean`. -/
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

/-! ### Reproduced verbatim from `SecondEigenvalueLipschitz.lean`
(Wave-2, SHARED-2A): `basis2`, `trace_lipschitz`, `lambda2`, and
`lambda2_lipschitz`. -/

/-- The fixed orthonormal basis of `E` the falsifiable test asks for.
Byte-identical to `basis2` in `SecondEigenvalueLipschitz.lean`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- `trace` is `2`-Lipschitz in operator norm on `E`. Byte-identical
(proof included) to `trace_lipschitz` in `SecondEigenvalueLipschitz.lean`. -/
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
        = (A - B) (basis2 i) := by simp [sub_apply]
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

/-- `lambda2 T := trace T - lambdaMax T`. Byte-identical to `lambda2` in
`SecondEigenvalueLipschitz.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Wave-2 SHARED-2A result, reproduced verbatim.** `lambda2` is
`3`-Lipschitz in operator norm on `E`. Byte-identical (proof included) to
`lambda2_lipschitz` in `SecondEigenvalueLipschitz.lean`. -/
theorem lambda2_lipschitz (A B : E →L[ℝ] E) :
    |lambda2 A - lambda2 B| ≤ 3 * ‖A - B‖ := by
  have h1 := trace_lipschitz A B
  have h2 := lambdaMax_lipschitz A B
  unfold lambda2
  rw [abs_le] at h1 h2 ⊢
  constructor <;> [linarith [h1.1, h2.1]; linarith [h1.2, h2.2]]

/-! ### Reproduced verbatim from `L2OperatorNormProbe.lean` (Wave-2,
YM-1+YM-3): `M1`, `M2`, and the exact numeric bound
`sonda1_bridge` + `sonda2_numeric_norm` (plus their own small internal
dependencies `diff_eq_diagonal`, `pi_norm_vec`). -/

/-- The perturbed matrix `M1`. Byte-identical to `M1` in
`L2OperatorNormProbe.lean`. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

/-- `M2`, byte-for-byte identical to `YM1.TransferGap.M`. Byte-identical
to `M2` in `L2OperatorNormProbe.lean`. -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-- **Sonda 1, part b, reproduced verbatim.** `Matrix.l2_opNorm_toEuclideanCLM`
rewrites `‖toEuclideanCLM M1 - toEuclideanCLM M2‖` to `‖M1 - M2‖`.
Byte-identical (proof included) to `sonda1_bridge` in
`L2OperatorNormProbe.lean`. -/
theorem sonda1_bridge :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 -
        Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2‖ = ‖M1 - M2‖ := by
  rw [← map_sub (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2))]
  exact Matrix.l2_opNorm_toEuclideanCLM (M1 - M2)

/-- `M1 - M2` is the diagonal matrix `diagonal ![0, 1/10]`. Byte-identical
to `diff_eq_diagonal` in `L2OperatorNormProbe.lean`. -/
theorem diff_eq_diagonal : M1 - M2 = Matrix.diagonal ![(0 : ℝ), 1 / 10] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [M1, M2]

/-- The Pi *sup*-norm of the concrete vector `![0, 1/10]` is exactly
`1/10`. Byte-identical to `pi_norm_vec` in `L2OperatorNormProbe.lean`. -/
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
`L2OperatorNormProbe.lean`. -/
theorem sonda2_numeric_norm : ‖M1 - M2‖ = 1 / 10 := by
  rw [diff_eq_diagonal, Matrix.l2_opNorm_diagonal]
  exact pi_norm_vec

/-! ### New content specific to this item (YM-STABILITY-COMPOSE): the two
composed corollaries chaining `lambdaMax_lipschitz` / `lambda2_lipschitz`
with `sonda1_bridge` + `sonda2_numeric_norm`, exactly via the route the
plan specified. -/

/-- **Main result (YM-STABILITY-COMPOSE), part 1.** Chaining
`lambdaMax_lipschitz` with the concrete numeric bound
`sonda1_bridge`/`sonda2_numeric_norm`: the top-eigenvalue candidates of
`toEuclideanCLM M1` and `toEuclideanCLM M2` (both `E →L[ℝ] E`) differ by
at most `1/10`, exactly `1 * ‖M1 - M2‖ = 1 * (1/10)`. Proved by
`(lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact
sonda2_numeric_norm.le)`, as the plan specified. -/
theorem stability_compose_lambdaMax :
    |lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 1 / 10 :=
  (lambdaMax_lipschitz _ _).trans (by rw [sonda1_bridge]; exact sonda2_numeric_norm.le)

/-- **Main result (YM-STABILITY-COMPOSE), part 2.** Same route via
`lambda2_lipschitz` instead of `lambdaMax_lipschitz`: the algebraic
"second eigenvalue" candidates of `toEuclideanCLM M1` and
`toEuclideanCLM M2` differ by at most `3/10`, exactly
`3 * ‖M1 - M2‖ = 3 * (1/10)`. -/
theorem stability_compose_lambda2 :
    |lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1) -
        lambda2 (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)| ≤ 3 / 10 := by
  have h := lambda2_lipschitz (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1)
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
  rw [sonda1_bridge, sonda2_numeric_norm] at h
  linarith

end YMStabilityCompose

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms YMStabilityCompose.bddAbove_rayleighQuotient_subtype
#print axioms YMStabilityCompose.lambdaMax_lipschitz
#print axioms YMStabilityCompose.trace_lipschitz
#print axioms YMStabilityCompose.lambda2_lipschitz
#print axioms YMStabilityCompose.sonda1_bridge
#print axioms YMStabilityCompose.diff_eq_diagonal
#print axioms YMStabilityCompose.pi_norm_vec
#print axioms YMStabilityCompose.sonda2_numeric_norm
#print axioms YMStabilityCompose.stability_compose_lambdaMax
#print axioms YMStabilityCompose.stability_compose_lambda2
