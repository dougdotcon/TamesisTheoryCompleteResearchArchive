/-
  SHARED-2A — second-eigenvalue Lipschitz bound via `trace - lambdaMax`, on
  the FIXED 2-dimensional space `E := EuclideanSpace ℝ (Fin 2)` (Wave-2
  batch, shared-infrastructure item; YM-3, 2D fixed-dimension slice).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-2 task instructions on build
  contention with 19 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1 or other Wave-2 file. It only *reads* the Wave-1 file
  `03_MILLENNIUM/04_YANG_MILLS/FORMAL/FixedDimEigenvalueStability.lean`.

  BUILD-SYSTEM NOTE (why `lambdaMax` / `lambdaMax_lipschitz` are reproduced
  below instead of imported, same situation already documented by the
  Wave-2 sibling `_SHARED_INFRA/FORMAL/HermitianComplexEmbeddingRange.lean`
  for its own Wave-1 dependency). `FixedDimEigenvalueStability.lean` is, by
  its own header, deliberately free-standing and NOT registered in
  `TamesisLab.lean` — it lives outside the `[[lean_lib]] name =
  "TamesisLab"` module graph declared in `lakefile.toml` and has no built
  `.olean`, so it cannot be `import`ed by module name from this file. Per
  the Wave-2 task instructions ("do NOT touch any file outside your own
  new file(s)"), this file cannot register `FixedDimEigenvalueStability.lean`
  into the library graph either. The only way to reuse `lambdaMax` and
  `lambdaMax_lipschitz` under this constraint is to reproduce their
  definitions/proofs VERBATIM (byte-identical, copied directly from
  `FixedDimEigenvalueStability.lean`) rather than inventing different
  ones — this is not a redeclaration of new objects, it is the same
  `lambdaMax` / `lambdaMax_lipschitz`, reproduced because the lab's own
  Wave-1 single-file convention leaves no other route to them. Everything
  from "Now the new part: trace and lambda2" onward IS new content specific
  to this item.

  MOTIVATION / RELATION TO WAVE-1 YM-3. The Wave-1 file
  `FixedDimEigenvalueStability.lean` proves `lambdaMax_lipschitz`
  (`|lambdaMax A - lambdaMax B| ≤ ‖A - B‖`) for the TOP eigenvalue only,
  and its own header explicitly flags what it does NOT do:

    "Only the TOP eigenvalue (`lambdaMax`, the `iSup` of the Rayleigh
    quotient) is treated here. The actual spectral GAP (top minus SECOND
    eigenvalue) would additionally need the analogous statement [...] but
    genuinely NOT done in this file: no Courant-Fischer / min-max
    characterization of the k-th eigenvalue was found anywhere in the
    vendored Mathlib snapshot [...] so a full second-eigenvalue treatment
    is left as future work, not attempted here."

  This Wave-2 item is EXACTLY the falsifiable test proposed to make
  partial progress on that flagged gap, and nothing broader: since
  `dim E = 2`, for a SYMMETRIC operator the sum of its two eigenvalues
  equals `trace`, so "the second eigenvalue" can be recovered algebraically
  as `trace - lambdaMax`, entirely avoiding any Courant-Fischer / min-max
  machinery. Concretely:
    (1) `lambda2 T := (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T` (this is a
        real number for ANY `T`, matching the pattern of `lambdaMax`
        itself in the Wave-1 file: only later results that need to call it
        "the second eigenvalue" require symmetry of `T`, via
        `IsSymmetric.trace_eq_sum_eigenvalues` from
        `Mathlib/Analysis/InnerProductSpace/Trace.lean` — NOT reproved or
        used directly in this file, since the falsifiable test asked for
        is the Lipschitz bound on `lambda2`, not the "genuinely an
        eigenvalue" identification analogous to `lambdaMax_hasEigenvalue`;
        that further step is explicitly left open below, matching the
        Wave-1 precedent of separating "is well-defined" from "is
        genuinely an eigenvalue").
    (2) `trace_lipschitz : |trace A - trace B| ≤ 2 * ‖A - B‖`, proved via
        `LinearMap.trace_eq_sum_inner` (same file) over the FIXED
        orthonormal basis `EuclideanSpace.basisFun (Fin 2) ℝ`: expand the
        trace as a 2-term sum of inner products, bound each term by
        Cauchy-Schwarz (`abs_real_inner_le_norm`) composed with the
        operator-norm bound (`ContinuousLinearMap.le_opNorm`), giving each
        term `≤ ‖A - B‖` (using `‖basis2 i‖ = 1`), hence the 2-term sum is
        `≤ 2 * ‖A - B‖`. No symmetry hypothesis is needed for this bound
        either (same pattern as `lambdaMax_lipschitz`).
    (3) `lambda2_lipschitz : |lambda2 A - lambda2 B| ≤ 3 * ‖A - B‖`, by
        linearly combining (2) with the reproduced `lambdaMax_lipschitz`
        (`|lambdaMax A - lambdaMax B| ≤ ‖A - B‖`) via the triangle
        inequality: `2 * ‖A - B‖ + 1 * ‖A - B‖ = 3 * ‖A - B‖`. This is
        EXACTLY the bound the falsifiable test asked to attempt, and it
        closes with a complete, gap-free proof.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Trace.lean` in the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean`):
    - `LinearMap.trace_eq_sum_inner (T : E →ₗ[𝕜] E) (b : OrthonormalBasis
      ι 𝕜 E) : T.trace 𝕜 E = ∑ i, ⟪b i, T (b i)⟫_𝕜` — used directly, no
      symmetry hypothesis needed (this is the general, non-eigenvalue
      version; `IsSymmetric.trace_eq_sum_eigenvalues`, cited in the
      original test proposal, is a further refinement for symmetric `T`
      that this file does NOT need, since it never has to name the
      individual eigenvalues, only bound the trace's Lipschitz constant).
    - `EuclideanSpace.basisFun (Fin 2) ℝ : OrthonormalBasis (Fin 2) ℝ E`
      (`Mathlib/Analysis/InnerProductSpace/PiL2.lean`) — the fixed
      orthonormal basis the test proposal asked for.
    - `abs_real_inner_le_norm`, `ContinuousLinearMap.le_opNorm`,
      `OrthonormalBasis.norm_eq_one`, `Finset.abs_sum_le_sum_abs` — the
      elementary per-term Cauchy-Schwarz / operator-norm / triangle
      inequality toolkit.
    - `ContinuousLinearMap.rayleighQuotient`,
      `ContinuousLinearMap.rayleighQuotient_le_norm`,
      `LinearMap.IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional` — as
      in the Wave-1 file, underlying the reproduced `lambdaMax` /
      `lambdaMax_lipschitz`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-2 instructions). `lambda2` is an ALGEBRAIC definition
  (`trace - lambdaMax`), not (in this file) independently shown to BE an
  eigenvalue of `T` the way `lambdaMax_hasEigenvalue` does for `lambdaMax`
  in the Wave-1 file — doing so would need
  `IsSymmetric.trace_eq_sum_eigenvalues` plus
  `IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional` applied to the
  restriction of a symmetric `T` to the orthogonal complement of a
  `lambdaMax`-eigenvector, which is exactly the "restrict to `(ℝ ∙
  x₀)ᗮ`... straightforward in principle but genuinely NOT done" gap the
  Wave-1 header already flagged, and remains flagged, not attempted, here.
  This file is specific to `dim E = 2` (the sum-of-eigenvalues-equals-trace
  identity that motivates calling `trace - lambdaMax` "the second
  eigenvalue" only holds in exactly this dimension for a 2-element
  spectrum); no claim is made or attempted about `n > 2`. Nothing here is
  about Yang-Mills, SU(N), the lattice-gauge partition function,
  reflection positivity, or the continuum limit; it says nothing about,
  and does not approximate, a solution to the Clay mass-gap problem. No
  mathematical novelty is claimed: Lipschitz continuity of the trace and
  of the top eigenvalue of an operator on a fixed finite-dimensional
  space, and the elementary algebraic identity
  "second eigenvalue = trace - top eigenvalue" in 2 dimensions, are
  completely classical, elementary facts.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

namespace SHARED2A.SecondEigenvalueLipschitz

/-! ### Reproduced verbatim from the Wave-1 file
`04_YANG_MILLS/FORMAL/FixedDimEigenvalueStability.lean` (see BUILD-SYSTEM
NOTE above for why this cannot instead be an `import`): the fixed
2-dimensional space `E`, `lambdaMax`, and `lambdaMax_lipschitz`. -/

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
to `lambdaMax_lipschitz` in `FixedDimEigenvalueStability.lean`; this is
the "combine linearly with `lambdaMax_lipschitz` (já provado no YM-3)"
ingredient the falsifiable test asks for. -/
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

/-! ### New content specific to this item (SHARED-2A): `trace` and
`lambda2 := trace - lambdaMax`, and their Lipschitz bounds. -/

/-- The fixed orthonormal basis of `E` the falsifiable test asks for
("base ortonormal fixa"): the standard `Fin 2`-indexed basis of
`EuclideanSpace ℝ (Fin 2)`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- **Main new result, part 1.** `trace` (of the `LinearMap` coercion of a
continuous linear self-map of `E`) is `2`-Lipschitz in operator norm on
`E`, via `LinearMap.trace_eq_sum_inner` expanded over the fixed
orthonormal basis `basis2`: `trace = ∑ i, ⟪basis2 i, T (basis2 i)⟫` is a
2-term sum (since `dim E = 2`), each term differs between `A` and `B` by
at most `‖A - B‖` (Cauchy-Schwarz + operator-norm bound, using
`‖basis2 i‖ = 1`), so the 2-term sum differs by at most `2 * ‖A - B‖`. No
symmetry hypothesis on `A` or `B` is needed. -/
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

/-- **The falsifiable test's target quantity.** `lambda2 T := trace T -
lambdaMax T`, an algebraic stand-in for "the second eigenvalue" of `T`
that is well-defined (a real number) for ANY continuous linear self-map of
the fixed 2-dimensional space `E`, mirroring how `lambdaMax` itself is
well-defined for any `T` in the Wave-1 file (symmetry is needed only to
justify the "eigenvalue" reading, which this file does not attempt — see
the header note "WHAT THIS FILE DOES NOT DO"). -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Main result (SHARED-2A), the falsifiable test as stated.**
`lambda2` is `3`-Lipschitz in operator norm on the fixed space `E`,
obtained by linearly combining `trace_lipschitz`
(`|trace A - trace B| ≤ 2 * ‖A - B‖`) with the reproduced Wave-1 result
`lambdaMax_lipschitz` (`|lambdaMax A - lambdaMax B| ≤ ‖A - B‖`) via the
triangle inequality: `2 * ‖A - B‖ + ‖A - B‖ = 3 * ‖A - B‖`. No symmetry
hypothesis on `A` or `B` is needed for this inequality. -/
theorem lambda2_lipschitz (A B : E →L[ℝ] E) :
    |lambda2 A - lambda2 B| ≤ 3 * ‖A - B‖ := by
  have h1 := trace_lipschitz A B
  have h2 := lambdaMax_lipschitz A B
  unfold lambda2
  rw [abs_le] at h1 h2 ⊢
  constructor <;> [linarith [h1.1, h2.1]; linarith [h1.2, h2.2]]

end SHARED2A.SecondEigenvalueLipschitz

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED2A.SecondEigenvalueLipschitz.bddAbove_rayleighQuotient_subtype
#print axioms SHARED2A.SecondEigenvalueLipschitz.lambdaMax_lipschitz
#print axioms SHARED2A.SecondEigenvalueLipschitz.trace_lipschitz
#print axioms SHARED2A.SecondEigenvalueLipschitz.lambda2_lipschitz
