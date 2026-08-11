/-
  SHARED-4B — `det = lambdaMax * lambda2` in dimension 2: for a symmetric
  operator `T` on the fixed 2-dimensional space `E`, the determinant of
  (the `LinearMap` coercion of) `T` equals the product of `lambdaMax T`
  and `lambda2 T`. Wave-4 batch, shared-infrastructure item, a direct
  follow-on to the Wave-3 item `SHARED-2A-EXT`
  (`SecondEigenvalueHasEigenvalue.lean`) — same internal facts this
  batch's sibling item `SHARED-4A` (`TwoEigenvalueExhaustiveness.lean`)
  also promotes to named lemmas.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-4 task instructions on
  build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1, Wave-2, Wave-3, or other Wave-4 file. It only *reads*
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueHasEigenvalue.lean`
  (Wave-3, SHARED-2A-EXT).

  BUILD-SYSTEM NOTE (why `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
  `lambdaMax_hasEigenvalue`, and `lambda2` are all reproduced below instead
  of imported — same situation already documented by the Wave-3 file
  `SecondEigenvalueHasEigenvalue.lean` for its own Wave-1/Wave-2
  dependencies, and by the Wave-2 files before it, and by this batch's
  sibling `TwoEigenvalueExhaustiveness.lean` (SHARED-4A)).
  `SecondEigenvalueHasEigenvalue.lean` is, by its own header, deliberately
  free-standing and NOT registered in `TamesisLab.lean` — it lives outside
  the `[[lean_lib]] name = "TamesisLab"` module graph declared in
  `lakefile.toml` and has no built `.olean`, so it cannot be `import`ed by
  module name from this file. Per the Wave-4 task instructions ("do NOT
  touch any file outside your own new file(s)"), this file cannot
  register `SecondEigenvalueHasEigenvalue.lean` into the library graph
  either. The only way to reuse its content under this constraint is to
  reproduce the relevant definitions/proofs VERBATIM (byte-identical,
  copied directly from `SecondEigenvalueHasEigenvalue.lean`) rather than
  inventing different ones — this is not a redeclaration of new objects,
  it is the same `lambdaMax`, `lambda2`, etc., reproduced because the
  lab's own single-file convention leaves no other route to them. This
  file's own `SHARED-4A` sibling (`TwoEigenvalueExhaustiveness.lean`) is
  NOT imported either, for the same reason plus an additional one: per
  the Wave-4 task instructions, this file must not depend on another
  Wave-4 item's own new file (14 agents working concurrently in this same
  checkout — that file's final on-disk content while this session runs is
  not something this file's correctness should rely on). Everything from
  "New content specific to this item" onward IS new content specific to
  SHARED-4B.

  MOTIVATION / RELATION TO WAVE-3 SHARED-2A-EXT. The Wave-3 file
  `SecondEigenvalueHasEigenvalue.lean` proves `lambda2 T` is a genuine
  eigenvalue of `T` (for symmetric `T`, `dim E = 2`), and along the way
  its `lambda2_hasEigenvalue` proof establishes, as two internal,
  UNNAMED `have`s, exactly the two facts this item needs:
    - `heq0 : lambdaMax T = hT.eigenvalues hn 0` (line 364 of that file)
    - `hlambda2 : lambda2 T = hT.eigenvalues hn 1` (lines 369-371 of that
      file)
  This item promotes both to standalone named lemmas (below), then
  combines them with Mathlib's `LinearMap.IsSymmetric.det_eq_prod_eigenvalues`
  and `Fin.prod_univ_two` to get the falsifiable test as stated: the
  determinant of a symmetric operator on the fixed 2-dimensional `E`
  equals the product of its two eigenvalues `lambdaMax T` and `lambda2 T`.
  This is the "product half" of the classical trace/determinant pair for
  a 2x2 symmetric operator; the "sum half"
  (`trace = lambdaMax + lambda2`) is free by the very DEFINITION of
  `lambda2 := trace - lambdaMax` in the Wave-2 file `SecondEigenvalueLipschitz.lean`,
  and is correctly NOT claimed here as new work.

  PROOF SKETCH for the new result `lambdaMax_mul_lambda2_eq_det`:
    (1) `lambdaMax_eq_eigenvalues_zero` (promoting `heq0`): reproduces,
        verbatim, steps 1-4 of the PROOF SKETCH in
        `SecondEigenvalueHasEigenvalue.lean`'s header — `lambdaMax T` is
        an eigenvalue, hence equals `hT.eigenvalues hn i0` for some `i0`;
        a reverse Rayleigh bound at Mathlib's sorted `0`-th eigenvector
        gives `hT.eigenvalues hn 0 ≤ lambdaMax T`; `eigenvalues_antitone`
        gives `hT.eigenvalues hn i0 ≤ hT.eigenvalues hn 0`; combining
        pins `lambdaMax T = hT.eigenvalues hn 0`.
    (2) `lambda2_eq_eigenvalues_one` (promoting `hlambda2`): reproduces,
        verbatim, step 5 of the same PROOF SKETCH —
        `IsSymmetric.trace_eq_sum_eigenvalues` plus `Fin.sum_univ_two`
        give `trace = eigenvalues 0 + eigenvalues 1`, so (via step (1)
        and the definition of `lambda2`) `lambda2 T = hT.eigenvalues hn 1`.
    (3) NEW for this item: `LinearMap.IsSymmetric.det_eq_prod_eigenvalues`
        gives `(T : E →ₗ[ℝ] E).det = ∏ i, (hT.eigenvalues hn i : ℝ)`;
        `Fin.prod_univ_two` unfolds this to
        `hT.eigenvalues hn 0 * hT.eigenvalues hn 1` (the cast to `ℝ` is
        the identity since `𝕜 = ℝ` here, closed by `norm_cast`, matching
        the analogous `htrace` step in `SecondEigenvalueHasEigenvalue.lean`).
    (4) Rewriting the goal `lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det`
        with (1), (2), (3) turns both sides into
        `hT.eigenvalues hn 0 * hT.eigenvalues hn 1`, closing the goal.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` and
  `Mathlib/Algebra/BigOperators/Fin.lean` in the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean`):
    - `LinearMap.IsSymmetric.det_eq_prod_eigenvalues` (`Spectrum.lean:391-394`):
      `T.det = ∏ i, (hT.eigenvalues hn i : 𝕜)`, stated for the `LinearMap`
      `T` itself (its ambient variable at `Spectrum.lean:84` is
      `T : E →ₗ[𝕜] E`), matching this file's target quantity
      `(T : E →ₗ[ℝ] E).det` exactly — not a mismatched
      `ContinuousLinearMap.det`.
    - `Fin.prod_univ_two` (`Algebra/BigOperators/Fin.lean:111`):
      `∏ i, f i = f 0 * f 1` for `f : Fin 2 → M`.
    - Every tool used by the reproduced `lambdaMax`/`lambda2`/
      `lambdaMax_eq_eigenvalues_zero`/`lambda2_eq_eigenvalues_one` blocks
      below — see the header of `SecondEigenvalueHasEigenvalue.lean` for
      the full list (`LinearMap.IsSymmetric.eigenvalues`,
      `.exists_eigenvalues_eq`, `.eigenvalues_antitone`,
      `.eigenvectorBasis`, `.hasEigenvector_eigenvectorBasis`,
      `.apply_eigenvectorBasis`, `.trace_eq_sum_eigenvalues`,
      `ContinuousLinearMap.coe_coe`, `le_ciSup`, `real_inner_smul_left`,
      `Fin.sum_univ_two`, `Fin.zero_le`).

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-4 instructions). This file is specific to `dim E = 2`, exactly as
  its two Wave-3/Wave-4 predecessors are: `Fin.prod_univ_two` unfolds the
  sorted-eigenvalue product into exactly two terms, and no claim is made
  or attempted about `n > 2`, nor any general
  `det = ∏ eigenvalues` statement beyond what Mathlib already proves for
  arbitrary finite `n` (this file only specializes it to `n = 2`, it does
  not reprove or extend it). Nothing here is about Yang-Mills, SU(N), the
  lattice-gauge partition function, reflection positivity, or the
  continuum limit; it says nothing about, and does not approximate, a
  solution to the Clay mass-gap problem or any other Millennium problem.
  No mathematical novelty is claimed: that the determinant of a 2x2
  symmetric operator equals the product of its two eigenvalues is a
  completely classical, elementary fact of linear algebra, immediate from
  the spectral theorem.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

namespace SHARED4B.LambdaMaxMulLambda2EqDet

/-! ### Reproduced verbatim from the Wave-3 file
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueHasEigenvalue.lean`
(itself reproduced verbatim from earlier Wave-1/Wave-2 files; see
BUILD-SYSTEM NOTE above for why this cannot instead be an `import`): the
fixed 2-dimensional space `E`, `lambdaMax`,
`bddAbove_rayleighQuotient_subtype`, `lambdaMax_hasEigenvalue`, and
`lambda2`. -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`SecondEigenvalueHasEigenvalue.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `SecondEigenvalueHasEigenvalue.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`SecondEigenvalueHasEigenvalue.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim (via the Wave-3 file).**
For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`.
Byte-identical (proof included) to `lambdaMax_hasEigenvalue` in
`SecondEigenvalueHasEigenvalue.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- **The falsifiable test's target quantity, reproduced verbatim from
`SecondEigenvalueHasEigenvalue.lean` (itself reproduced verbatim from
Wave-2 SHARED-2A).** `lambda2 T := trace T - lambdaMax T`, an algebraic
stand-in for "the second eigenvalue" of `T`, well-defined (a real number)
for ANY continuous linear self-map of the fixed 2-dimensional space `E`.
Byte-identical to `lambda2` in `SecondEigenvalueHasEigenvalue.lean`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-! ### New content specific to this item (SHARED-4B). Section 1: promote
the two internal, unnamed `have`s of `SecondEigenvalueHasEigenvalue.lean`'s
`lambda2_hasEigenvalue` proof (`heq0` at its line 364, `hlambda2` at its
lines 369-371) to standalone, reusable, named theorems. (This batch's
sibling item `SHARED-4A`, `TwoEigenvalueExhaustiveness.lean`, promotes the
same two internal facts, independently, in its own free-standing file —
per the Wave-4 constraint against depending on another Wave-4 item's file,
this file does not import that one and instead reproduces the same short
derivation itself.) -/

/-- **Promotion of `heq0` (line 364 of `SecondEigenvalueHasEigenvalue.lean`)
to a standalone named lemma.** For symmetric `T` on the fixed
2-dimensional `E`, `lambdaMax T` coincides with the `0`-th (largest)
entry of Mathlib's sorted eigenvalue family `hT.eigenvalues hn`. Proof
reproduces, verbatim, steps 1-4 of the PROOF SKETCH in
`SecondEigenvalueHasEigenvalue.lean`'s header (and the corresponding code
inside its `lambda2_hasEigenvalue` proof). -/
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

/-- **Promotion of `hlambda2` (lines 369-371 of
`SecondEigenvalueHasEigenvalue.lean`) to a standalone named lemma.** For
symmetric `T` on the fixed 2-dimensional `E`, `lambda2 T` coincides with
the `1`-st (smaller) entry of Mathlib's sorted eigenvalue family
`hT.eigenvalues hn`. Proof reproduces, verbatim, step 5 of the PROOF
SKETCH in `SecondEigenvalueHasEigenvalue.lean`'s header, built on top of
`lambdaMax_eq_eigenvalues_zero` above (the promoted `heq0`). -/
theorem lambda2_eq_eigenvalues_one (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T = hT.eigenvalues hn 1 := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  unfold lambda2
  rw [htrace, heq0]; ring

/-! ### New content specific to this item (SHARED-4B). Section 2: the
falsifiable test itself, `lambdaMax_mul_lambda2_eq_det` — for symmetric
`T` on the fixed 2-dimensional `E`, `(T : E →ₗ[ℝ] E).det = lambdaMax T *
lambda2 T`, via `LinearMap.IsSymmetric.det_eq_prod_eigenvalues`,
`Fin.prod_univ_two`, and the two promoted lemmas above. -/

/-- **Main new result (SHARED-4B), the falsifiable test as stated.** For a
symmetric `T : E →L[ℝ] E` on the fixed 2-dimensional `E`, the determinant
of (the `LinearMap` coercion of) `T` equals the product `lambdaMax T *
lambda2 T`. Proof: `hT.det_eq_prod_eigenvalues hn` gives
`(T : E →ₗ[ℝ] E).det = ∏ i, (hT.eigenvalues hn i : ℝ)`; `Fin.prod_univ_two`
unfolds this to `hT.eigenvalues hn 0 * hT.eigenvalues hn 1`; the two
promoted lemmas `lambdaMax_eq_eigenvalues_zero` and
`lambda2_eq_eigenvalues_one` identify `lambdaMax T` and `lambda2 T` with
exactly these two factors. -/
theorem lambdaMax_mul_lambda2_eq_det (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det := by
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := lambda2_eq_eigenvalues_one T hT hn
  have hdet : (T : E →ₗ[ℝ] E).det = hT.eigenvalues hn 0 * hT.eigenvalues hn 1 := by
    rw [hT.det_eq_prod_eigenvalues hn, Fin.prod_univ_two]
    norm_cast
  rw [heq0, hlambda2, hdet]

end SHARED4B.LambdaMaxMulLambda2EqDet

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED4B.LambdaMaxMulLambda2EqDet.bddAbove_rayleighQuotient_subtype
#print axioms SHARED4B.LambdaMaxMulLambda2EqDet.lambdaMax_hasEigenvalue
#print axioms SHARED4B.LambdaMaxMulLambda2EqDet.lambdaMax_eq_eigenvalues_zero
#print axioms SHARED4B.LambdaMaxMulLambda2EqDet.lambda2_eq_eigenvalues_one
#print axioms SHARED4B.LambdaMaxMulLambda2EqDet.lambdaMax_mul_lambda2_eq_det
