/-
  SHARED-6A — discriminant / quadratic formula in dimension 2: for a
  symmetric operator `T` on the fixed 2-dimensional space `E`, (1)
  `lambda2 T ≤ lambdaMax T` (the two algebraic eigenvalue stand-ins are
  correctly ordered), (2) the discriminant identity `(lambdaMax T -
  lambda2 T) ^ 2 = (trace T) ^ 2 - 4 * det T`, and (3) the resulting
  quadratic-formula corollary `lambdaMax T = (trace T + Real.sqrt ((trace
  T) ^ 2 - 4 * det T)) / 2`. Wave-6 batch, shared-infrastructure item, a
  direct follow-on to the Wave-4 items `SHARED-4A`
  (`TwoEigenvalueExhaustiveness.lean`) and `SHARED-4B`
  (`LambdaMaxMulLambda2EqDet.lean`), and the Wave-5 item `SHARED-5A`
  (`CharpolyFactorizationDim2.lean`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-6 task instructions on
  build contention with 13 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1 through Wave-5 file, nor any other Wave-6 item's file. It only
  *reads* `03_MILLENNIUM/_SHARED_INFRA/FORMAL/TwoEigenvalueExhaustiveness.lean`
  (Wave-4, SHARED-4A) and `LambdaMaxMulLambda2EqDet.lean` (Wave-4,
  SHARED-4B) for reference on the existing `lambdaMax`/`lambda2` API,
  without importing either (see BUILD-SYSTEM NOTE below).

  BUILD-SYSTEM NOTE (why `E`, `lambdaMax`,
  `bddAbove_rayleighQuotient_subtype`, `lambdaMax_hasEigenvalue`,
  `lambda2`, `lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`,
  and `lambdaMax_mul_lambda2_eq_det` are all reproduced below instead of
  imported — same situation already documented by the Wave-4 and Wave-5
  files for their own dependencies). `TwoEigenvalueExhaustiveness.lean`
  and `LambdaMaxMulLambda2EqDet.lean` are, by their own headers,
  deliberately free-standing and NOT registered in `TamesisLab.lean` —
  they live outside the `[[lean_lib]] name = "TamesisLab"` module graph
  declared in `lakefile.toml` and have no built `.olean`, so neither can
  be `import`ed by module name from this file. Per the Wave-6 task
  instructions ("do NOT touch any file outside your own new file(s) for
  this item"), this file cannot register either into the library graph.
  The only way to reuse their content under this constraint is to
  reproduce the relevant definitions/proofs VERBATIM (byte-identical,
  copied directly from `LambdaMaxMulLambda2EqDet.lean`, which is itself
  byte-identical on this shared portion to `TwoEigenvalueExhaustiveness.lean`
  and `CharpolyFactorizationDim2.lean`) rather than inventing different
  ones — this is not a redeclaration of new objects, it is the same `E`,
  `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
  `lambdaMax_hasEigenvalue`, `lambda2`, `lambdaMax_eq_eigenvalues_zero`,
  `lambda2_eq_eigenvalues_one`, `lambdaMax_mul_lambda2_eq_det`,
  reproduced because the lab's own single-file convention leaves no other
  route to them. Everything from "New content specific to this item"
  onward IS new content specific to SHARED-6A.

  MOTIVATION / RELATION TO WAVE-4 SHARED-4A/4B AND WAVE-5 SHARED-5A. The
  Wave-4 files establish `lambdaMax T = hT.eigenvalues hn 0`,
  `lambda2 T = hT.eigenvalues hn 1` (as named lemmas
  `lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one`), and
  `lambdaMax_mul_lambda2_eq_det`. Separately, `lambda2 T := trace T -
  lambdaMax T` by definition (Wave-2 `SecondEigenvalueLipschitz.lean`),
  so `trace T = lambdaMax T + lambda2 T` is free algebra, not new work.
  This Wave-6 item is exactly the falsifiable test proposed to combine
  these three already-closed facts into the classical discriminant
  identity and quadratic formula for a 2x2 symmetric operator:
    (1) `lambda2_le_lambdaMax`: `hT.eigenvalues_antitone hn (by decide :
        (0 : Fin 2) ≤ 1)` gives `hT.eigenvalues hn 1 ≤ hT.eigenvalues hn
        0`; rewriting both sides via `lambdaMax_eq_eigenvalues_zero` /
        `lambda2_eq_eigenvalues_one` gives `lambda2 T ≤ lambdaMax T`.
    (2) `discriminant_eq`: `(lambdaMax T - lambda2 T) ^ 2 = (trace T) ^ 2
        - 4 * det T` by pure `ring` algebra once `trace T = lambdaMax T +
        lambda2 T` (free from the definition of `lambda2`) and
        `lambdaMax T * lambda2 T = det T` (`lambdaMax_mul_lambda2_eq_det`,
        reproduced from SHARED-4B) are substituted in.
    (3) `lambdaMax_eq_quadratic_formula`: `Real.sqrt_sq` applied to (1)
        (`0 ≤ lambdaMax T - lambda2 T`) and (2) gives `Real.sqrt ((trace
        T) ^ 2 - 4 * det T) = lambdaMax T - lambda2 T`; substituting
        `trace T = lambdaMax T + lambda2 T` and clearing with `ring`
        gives exactly the falsifiable test's claimed quadratic-formula
        equality `lambdaMax T = (trace T + Real.sqrt ((trace T) ^ 2 - 4 *
        det T)) / 2`.

  PROOF SKETCH: see the three numbered steps immediately above, which map
  directly onto the three new theorems `lambda2_le_lambdaMax`,
  `discriminant_eq`, `lambdaMax_eq_quadratic_formula` in the "New content"
  section below.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`,
  `Mathlib/Analysis/InnerProductSpace/Trace.lean`, and
  `Mathlib/Analysis/Real/Sqrt.lean` in the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean` — the SAME tools already verified present by
  the Wave-3/4/5 files, plus `Real.sqrt_sq` for the new quadratic-formula
  step):
    - `LinearMap.IsSymmetric.eigenvalues`, `.exists_eigenvalues_eq`,
      `.eigenvalues_antitone`, `.eigenvectorBasis`,
      `.hasEigenvector_eigenvectorBasis`, `.apply_eigenvectorBasis`,
      `.trace_eq_sum_eigenvalues`, `.det_eq_prod_eigenvalues` — from
      `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` /
      `Trace.lean`, needed only inside the reproduced blocks (unchanged
      from the Wave-4 files) plus, directly, inside the new
      `lambda2_le_lambdaMax` proof (`eigenvalues_antitone`).
    - `Fin.prod_univ_two`, `Fin.sum_univ_two` — the finite two-element
      product/sum-unfolding lemmas, matching the reproduced Wave-4 block's
      own usage.
    - `le_ciSup`, `real_inner_smul_left`, `Fin.zero_le` — the elementary
      supremum / inner-product toolkit, matching the reproduced Wave-4
      block's own usage.
    - `Real.sqrt_sq (h : 0 ≤ x) : Real.sqrt (x ^ 2) = x`
      (`Mathlib/Analysis/Real/Sqrt.lean:181`) — the new tool this item's
      quadratic-formula step needs, applied at `x = lambdaMax T - lambda2
      T` using the ordering fact `lambda2_le_lambdaMax`.
    - `ring`, `linarith`, `norm_cast`, `decide` — elementary closing
      tactics; `decide` specifically discharges `(0 : Fin 2) ≤ 1` for the
      `eigenvalues_antitone` application in `lambda2_le_lambdaMax`, as the
      falsifiable test specifies.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-6 instructions). This file is specific to `dim E = 2`, exactly as
  its Wave-3/4/5 predecessors are; no claim is made or attempted about `n
  > 2`, and no general quadratic-formula-style closed form for the
  eigenvalues of an `n`-dimensional symmetric operator is proved here.
  Nothing here is about Yang-Mills, SU(N), the lattice-gauge partition
  function, reflection positivity, the continuum limit, P vs NP, BSD, or
  any other Millennium problem; it says nothing about, and does not
  approximate, a solution to any of them. No mathematical novelty is
  claimed: that the two eigenvalues of a 2x2 symmetric matrix/operator
  are given by the classical quadratic formula `(tr ± sqrt(tr² - 4 det)) /
  2` is a completely elementary, standard fact of 2x2 linear algebra.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

namespace SHARED6A.QuadraticFormulaDim2

/-! ### Reproduced verbatim from the Wave-4 files
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/TwoEigenvalueExhaustiveness.lean` and
`LambdaMaxMulLambda2EqDet.lean` (themselves reproduced verbatim from
earlier Wave-1/2/3 files; see BUILD-SYSTEM NOTE above for why this cannot
instead be an `import`): the fixed 2-dimensional space `E`, `lambdaMax`,
`bddAbove_rayleighQuotient_subtype`, `lambdaMax_hasEigenvalue`,
`lambda2`, `lambdaMax_eq_eigenvalues_zero`, `lambda2_eq_eigenvalues_one`,
and `lambdaMax_mul_lambda2_eq_det`. -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`LambdaMaxMulLambda2EqDet.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `LambdaMaxMulLambda2EqDet.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`LambdaMaxMulLambda2EqDet.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim (via the Wave-3/4 files).**
For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`.
Byte-identical (proof included) to `lambdaMax_hasEigenvalue` in
`LambdaMaxMulLambda2EqDet.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- **Reproduced verbatim from `LambdaMaxMulLambda2EqDet.lean` (itself
reproduced verbatim from Wave-2 SHARED-2A).** `lambda2 T := trace T -
lambdaMax T`, an algebraic stand-in for "the second eigenvalue" of `T`,
well-defined (a real number) for ANY continuous linear self-map of the
fixed 2-dimensional space `E`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Reproduced verbatim from `LambdaMaxMulLambda2EqDet.lean`.** For
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

/-- **Reproduced verbatim from `LambdaMaxMulLambda2EqDet.lean`.** For
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

/-- **Reproduced verbatim from `LambdaMaxMulLambda2EqDet.lean` (Wave-4,
SHARED-4B).** For a symmetric `T : E →L[ℝ] E` on the fixed 2-dimensional
`E`, `lambdaMax T * lambda2 T = det T`. -/
theorem lambdaMax_mul_lambda2_eq_det (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det := by
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := lambda2_eq_eigenvalues_one T hT hn
  have hdet : (T : E →ₗ[ℝ] E).det = hT.eigenvalues hn 0 * hT.eigenvalues hn 1 := by
    rw [hT.det_eq_prod_eigenvalues hn, Fin.prod_univ_two]
    norm_cast
  rw [heq0, hlambda2, hdet]

/-! ### New content specific to this item (SHARED-6A): the falsifiable
test itself — the correct ordering `lambda2 T ≤ lambdaMax T`
(`lambda2_le_lambdaMax`), the discriminant identity `discriminant_eq`,
and the resulting quadratic-formula corollary
`lambdaMax_eq_quadratic_formula`. -/

/-- **New result 1/3 (SHARED-6A).** For symmetric `T` on the fixed
2-dimensional `E`, `lambda2 T ≤ lambdaMax T`: the two algebraic
eigenvalue stand-ins are correctly ordered, matching the "largest" /
"second" naming. Proof: `hT.eigenvalues_antitone hn (by decide : (0 :
Fin 2) ≤ 1)` gives `hT.eigenvalues hn 1 ≤ hT.eigenvalues hn 0`;
`lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one` identify
the two sides with `lambdaMax T` / `lambda2 T`. -/
theorem lambda2_le_lambdaMax (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    lambda2 T ≤ lambdaMax T := by
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have heq1 := lambda2_eq_eigenvalues_one T hT hn
  have hanti : hT.eigenvalues hn 1 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (by decide)
  rw [heq0, heq1]
  exact hanti

/-- **New result 2/3 (SHARED-6A), the discriminant identity.** For
symmetric `T` on the fixed 2-dimensional `E`,
`(lambdaMax T - lambda2 T) ^ 2 = (trace T) ^ 2 - 4 * det T`, where `trace
T` and `det T` abbreviate `(T : E →ₗ[ℝ] E).trace ℝ E` and
`(T : E →ₗ[ℝ] E).det`. Proof: `trace T = lambdaMax T + lambda2 T` is free
algebra from the definition of `lambda2`; `lambdaMax T * lambda2 T =
det T` is `lambdaMax_mul_lambda2_eq_det` (reproduced from Wave-4
SHARED-4B); substituting both into the goal and closing with `ring`. -/
theorem discriminant_eq (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    (lambdaMax T - lambda2 T) ^ 2 =
      ((T : E →ₗ[ℝ] E).trace ℝ E) ^ 2 - 4 * (T : E →ₗ[ℝ] E).det := by
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = lambdaMax T + lambda2 T := by
    unfold lambda2; ring
  have hdet : lambdaMax T * lambda2 T = (T : E →ₗ[ℝ] E).det :=
    lambdaMax_mul_lambda2_eq_det T hT hn
  rw [htrace, ← hdet]; ring

/-- **New result 3/3 (SHARED-6A), the falsifiable test as stated: the
quadratic-formula corollary.** For symmetric `T` on the fixed
2-dimensional `E`, `lambdaMax T = (trace T + Real.sqrt ((trace T) ^ 2 - 4
* det T)) / 2`, where `trace T` and `det T` abbreviate
`(T : E →ₗ[ℝ] E).trace ℝ E` and `(T : E →ₗ[ℝ] E).det`. Proof:
`Real.sqrt_sq`, applied at `x = lambdaMax T - lambda2 T` using
`lambda2_le_lambdaMax` (`0 ≤ x`) and `discriminant_eq` (rewriting `x ^ 2`
as `(trace T) ^ 2 - 4 * det T`), gives `Real.sqrt ((trace T) ^ 2 - 4 *
det T) = lambdaMax T - lambda2 T`; substituting `trace T = lambdaMax T +
lambda2 T` (free from the definition of `lambda2`) and closing with
`ring` gives the claimed equality. -/
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

end SHARED6A.QuadraticFormulaDim2

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED6A.QuadraticFormulaDim2.bddAbove_rayleighQuotient_subtype
#print axioms SHARED6A.QuadraticFormulaDim2.lambdaMax_hasEigenvalue
#print axioms SHARED6A.QuadraticFormulaDim2.lambdaMax_eq_eigenvalues_zero
#print axioms SHARED6A.QuadraticFormulaDim2.lambda2_eq_eigenvalues_one
#print axioms SHARED6A.QuadraticFormulaDim2.lambdaMax_mul_lambda2_eq_det
#print axioms SHARED6A.QuadraticFormulaDim2.lambda2_le_lambdaMax
#print axioms SHARED6A.QuadraticFormulaDim2.discriminant_eq
#print axioms SHARED6A.QuadraticFormulaDim2.lambdaMax_eq_quadratic_formula
