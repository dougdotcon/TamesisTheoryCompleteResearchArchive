/-
  SHARED-7A — negative branch of the quadratic formula in dimension 2: for
  a symmetric operator `T` on the fixed 2-dimensional space `E`, the
  corollary `lambda2 T = (trace T - Real.sqrt ((trace T) ^ 2 - 4 * det
  T)) / 2`, i.e. `lambda2 T` is the "minus" root of the classical
  quadratic formula, exactly as `lambdaMax T` (Wave-6 SHARED-6A,
  `lambdaMax_eq_quadratic_formula`) is the "plus" root. Wave-7 batch,
  shared-infrastructure item, a direct follow-on to the Wave-6 item
  `SHARED-6A` (`QuadraticFormulaDim2.lean`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-7 task instructions on
  build contention with 13 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1 through Wave-6 file, nor any other Wave-7 item's file. It only
  *reads* `03_MILLENNIUM/_SHARED_INFRA/FORMAL/QuadraticFormulaDim2.lean`
  (Wave-6, SHARED-6A) for reference on the existing `lambdaMax`/`lambda2`
  API and the already-closed `lambdaMax_eq_quadratic_formula`, without
  importing it (see BUILD-SYSTEM NOTE below).

  BUILD-SYSTEM NOTE (why `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
  `lambdaMax_hasEigenvalue`, `lambda2`, `lambdaMax_eq_eigenvalues_zero`,
  `lambda2_eq_eigenvalues_one`, `lambdaMax_mul_lambda2_eq_det`,
  `lambda2_le_lambdaMax`, `discriminant_eq`, and
  `lambdaMax_eq_quadratic_formula` are all reproduced below instead of
  imported — same situation already documented by the Wave-4/5/6 files
  for their own dependencies). `QuadraticFormulaDim2.lean` is, by its own
  header, deliberately free-standing and NOT registered in
  `TamesisLab.lean` — it lives outside the `[[lean_lib]] name =
  "TamesisLab"` module graph declared in `lakefile.toml` and has no built
  `.olean`, so it cannot be `import`ed by module name from this file. Per
  the Wave-7 task instructions ("do NOT touch any file outside your own
  new file(s) for this item"), this file cannot register it into the
  library graph. The only way to reuse its content under this constraint
  is to reproduce the relevant definitions/proofs VERBATIM (byte-identical,
  copied directly from `QuadraticFormulaDim2.lean`) rather than inventing
  different ones — this is not a redeclaration of new objects, it is the
  same `E`, `lambdaMax`, `lambda2`, `lambdaMax_eq_quadratic_formula`, etc.,
  reproduced because the lab's own single-file convention leaves no other
  route to them. Everything from "New content specific to this item"
  onward IS new content specific to SHARED-7A; everything above it is the
  reproduced SHARED-6A block, unchanged.

  MOTIVATION / RELATION TO WAVE-6 SHARED-6A. SHARED-6A proves
  `lambdaMax_eq_quadratic_formula`: `lambdaMax T = (trace T + Real.sqrt
  ((trace T) ^ 2 - 4 * det T)) / 2`, the "plus" root of the classical
  quadratic formula for a 2x2 symmetric operator. Since `lambda2 T :=
  trace T - lambdaMax T` by definition (Wave-2
  `SecondEigenvalueLipschitz.lean`), substituting the SHARED-6A result
  and simplifying with `ring` gives the "minus" root directly — exactly
  the falsifiable test proposed for this item:
    `lambda2_eq_quadratic_formula`: `unfold lambda2` turns the goal
    `lambda2 T = (trace T - sqrt(...)) / 2` into `trace T - lambdaMax T =
    (trace T - sqrt(...)) / 2`; rewriting `lambdaMax T` via
    `lambdaMax_eq_quadratic_formula` and closing with `ring` proves it.

  PROOF SKETCH: exactly the one step above, `lambda2_eq_quadratic_formula`
  in the "New content" section below.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`,
  `Mathlib/Analysis/InnerProductSpace/Trace.lean`, and
  `Mathlib/Analysis/Real/Sqrt.lean` in the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean` — the SAME tools already verified present by
  the Wave-3/4/5/6 files; the new step needs nothing beyond `unfold` and
  `ring` applied to the already-closed SHARED-6A result):
    - All tools listed in the header of `QuadraticFormulaDim2.lean`
      (`LinearMap.IsSymmetric.eigenvalues`, `.exists_eigenvalues_eq`,
      `.eigenvalues_antitone`, `.eigenvectorBasis`,
      `.hasEigenvector_eigenvectorBasis`, `.apply_eigenvectorBasis`,
      `.trace_eq_sum_eigenvalues`, `.det_eq_prod_eigenvalues`,
      `Fin.prod_univ_two`, `Fin.sum_univ_two`, `le_ciSup`,
      `real_inner_smul_left`, `Fin.zero_le`, `Real.sqrt_sq`), needed only
      inside the reproduced blocks (unchanged from the Wave-6 file).
    - `ring` — the only tactic the new `lambda2_eq_quadratic_formula` step
      itself needs, beyond `unfold`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-7 instructions). This file is specific to `dim E = 2`, exactly as
  its Wave-3/4/5/6 predecessors are; no claim is made or attempted about
  `n > 2`, and no general quadratic-formula-style closed form for the
  eigenvalues of an `n`-dimensional symmetric operator is proved here.
  Nothing here is about Yang-Mills, SU(N), the lattice-gauge partition
  function, reflection positivity, the continuum limit, P vs NP, BSD, or
  any other Millennium problem; it says nothing about, and does not
  approximate, a solution to any of them. No mathematical novelty is
  claimed: that the two eigenvalues of a 2x2 symmetric matrix/operator
  are given by the classical quadratic formula `(tr ± sqrt(tr² - 4 det)) /
  2` is a completely elementary, standard fact of 2x2 linear algebra; this
  file only supplies the "minus" branch alongside SHARED-6A's already-
  closed "plus" branch, by the same free algebraic substitution.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

namespace SHARED7A.QuadraticFormulaDim2NegativeBranch

/-! ### Reproduced verbatim from the Wave-6 file
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/QuadraticFormulaDim2.lean` (itself
reproduced verbatim from earlier Wave-4/5 files; see BUILD-SYSTEM NOTE
above for why this cannot instead be an `import`): the fixed
2-dimensional space `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
`lambdaMax_hasEigenvalue`, `lambda2`, `lambdaMax_eq_eigenvalues_zero`,
`lambda2_eq_eigenvalues_one`, `lambdaMax_mul_lambda2_eq_det`,
`lambda2_le_lambdaMax`, `discriminant_eq`, and
`lambdaMax_eq_quadratic_formula`. -/

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

/-- **Wave-1 YM-3 result, reproduced verbatim (via the Wave-3/4/5/6
files).** For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of
`T`. Byte-identical (proof included) to `lambdaMax_hasEigenvalue` in
`QuadraticFormulaDim2.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean` (itself
reproduced verbatim from earlier waves).** `lambda2 T := trace T -
lambdaMax T`, an algebraic stand-in for "the second eigenvalue" of `T`,
well-defined (a real number) for ANY continuous linear self-map of the
fixed 2-dimensional space `E`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean`.** For
symmetric `T` on the fixed 2-dimensional `E`, `lambdaMax T` coincides
with the `0`-th (largest) entry of Mathlib's sorted eigenvalue family
`hT.eigenvalues hn`. -/
theorem lambdaMax_eq_eigenvalues_zero (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T = hT.eigenvalues hn 0 := by
  -- `lambdaMax T` is an eigenvalue, hence `= hT.eigenvalues hn i0` for some `i0`.
  have hmaxEig : Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) :=
    lambdaMax_hasEigenvalue T hT
  obtain ⟨i0, hi0⟩ := hT.exists_eigenvalues_eq hn hmaxEig
  -- Reverse Rayleigh bound at the sorted `0`-th eigenvector:
  -- `hT.eigenvalues hn 0 ≤ lambdaMax T`.
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
  -- `eigenvalues` antitone on `Fin 2`, so `eigenvalues i0 ≤ eigenvalues 0`.
  have hanti : hT.eigenvalues hn i0 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (Fin.zero_le i0)
  -- Combine to pin `lambdaMax T = hT.eigenvalues hn 0`.
  have hi0' : hT.eigenvalues hn i0 = lambdaMax T := by exact_mod_cast hi0
  linarith [hi0', hanti, hle]

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean`.** For
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

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean` (Wave-4,
SHARED-4B, via Wave-6).** For a symmetric `T : E →L[ℝ] E` on the fixed
2-dimensional `E`, `lambdaMax T * lambda2 T = det T`. -/
theorem lambdaMax_mul_lambda2_eq_det (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det := by
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := lambda2_eq_eigenvalues_one T hT hn
  have hdet : (T : E →ₗ[ℝ] E).det = hT.eigenvalues hn 0 * hT.eigenvalues hn 1 := by
    rw [hT.det_eq_prod_eigenvalues hn, Fin.prod_univ_two]
    norm_cast
  rw [heq0, hlambda2, hdet]

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean` (Wave-6,
SHARED-6A, new result 1/3).** For symmetric `T` on the fixed
2-dimensional `E`, `lambda2 T ≤ lambdaMax T`. -/
theorem lambda2_le_lambdaMax (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T ≤ lambdaMax T := by
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have heq1 := lambda2_eq_eigenvalues_one T hT hn
  have hanti : hT.eigenvalues hn 1 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (by decide)
  rw [heq0, heq1]
  exact hanti

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean` (Wave-6,
SHARED-6A, new result 2/3), the discriminant identity.** For symmetric
`T` on the fixed 2-dimensional `E`, `(lambdaMax T - lambda2 T) ^ 2 =
(trace T) ^ 2 - 4 * det T`. -/
theorem discriminant_eq (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    (lambdaMax T - lambda2 T) ^ 2 =
      ((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = lambdaMax T + lambda2 T := by
    unfold lambda2; ring
  have hdet : lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det :=
    lambdaMax_mul_lambda2_eq_det T hT hn
  rw [htrace, ← hdet]; ring

/-- **Reproduced verbatim from `QuadraticFormulaDim2.lean` (Wave-6,
SHARED-6A, new result 3/3), the "plus" quadratic-formula corollary this
item's negative branch is the counterpart of.** For symmetric `T` on the
fixed 2-dimensional `E`, `lambdaMax T = (trace T + Real.sqrt ((trace T) ^
2 - 4 * det T)) / 2`. -/
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

/-! ### New content specific to this item (SHARED-7A): the falsifiable
test itself, the negative-branch corollary `lambda2_eq_quadratic_formula`,
proved from the reproduced `lambdaMax_eq_quadratic_formula` block above by
`unfold lambda2` and `ring`. -/

/-- **New result (SHARED-7A), the falsifiable test as stated: the
negative-branch quadratic-formula corollary.** For symmetric `T` on the
fixed 2-dimensional `E`, `lambda2 T = (trace T - Real.sqrt ((trace T) ^ 2
- 4 * det T)) / 2`, where `trace T` and `det T` abbreviate `(T : E →ₗ[ℝ]
E).trace ℝ E` and `(T : E →ₗ[ℝ] E).det`. Proof: `unfold lambda2` turns the
goal into `trace T - lambdaMax T = (trace T - sqrt(...)) / 2`; rewriting
`lambdaMax T` via `lambdaMax_eq_quadratic_formula` (SHARED-6A) and closing
with `ring` proves it. -/
theorem lambda2_eq_quadratic_formula (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T =
      ((T : E →ₗ[ℝ] E).trace ℝ E -
          Real.sqrt (((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det)) / 2 := by
  have hmax := lambdaMax_eq_quadratic_formula T hT hn
  unfold lambda2
  rw [hmax]; ring

end SHARED7A.QuadraticFormulaDim2NegativeBranch

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.bddAbove_rayleighQuotient_subtype
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambdaMax_hasEigenvalue
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambdaMax_eq_eigenvalues_zero
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambda2_eq_eigenvalues_one
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambdaMax_mul_lambda2_eq_det
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambda2_le_lambdaMax
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.discriminant_eq
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambdaMax_eq_quadratic_formula
#print axioms SHARED7A.QuadraticFormulaDim2NegativeBranch.lambda2_eq_quadratic_formula
