/-
  SHARED-2A-EXT — promoting `lambda2 T := trace - lambdaMax` (Wave-2
  `SHARED-2A`, `SecondEigenvalueLipschitz.lean`) to a GENUINE second
  eigenvalue of `T` in the fixed 2-dimensional space `E := EuclideanSpace
  ℝ (Fin 2)`, for symmetric `T`. Wave-3 batch, shared-infrastructure item,
  a direct narrowing/extension of the Wave-2 `SHARED-2A` angle.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-3 task instructions on
  build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1, Wave-2, or other Wave-3 file. It only *reads* two files:
  `03_MILLENNIUM/04_YANG_MILLS/FORMAL/FixedDimEigenvalueStability.lean`
  (Wave-1, YM-3) and
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueLipschitz.lean`
  (Wave-2, SHARED-2A).

  BUILD-SYSTEM NOTE (why `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
  `lambdaMax_lipschitz`, `lambdaMax_hasEigenvalue`, `basis2`,
  `trace_lipschitz`, `lambda2`, `lambda2_lipschitz` are all reproduced
  below instead of imported — same situation already documented by the
  Wave-2 file `SecondEigenvalueLipschitz.lean` for its own Wave-1
  dependency, and by the Wave-2 sibling
  `_SHARED_INFRA/FORMAL/HermitianComplexEmbeddingRange.lean`).
  `FixedDimEigenvalueStability.lean` and `SecondEigenvalueLipschitz.lean`
  are both, by their own headers, deliberately free-standing and NOT
  registered in `TamesisLab.lean` — they live outside the `[[lean_lib]]
  name = "TamesisLab"` module graph declared in `lakefile.toml` and have
  no built `.olean`, so neither can be `import`ed by module name from
  this file. Per the Wave-3 task instructions ("do NOT touch any file
  outside your own new file(s)"), this file cannot register either of
  them into the library graph. The only way to reuse their content under
  this constraint is to reproduce the relevant definitions/proofs
  VERBATIM (byte-identical, copied directly from the source files named
  in each block's own comment below) rather than inventing different
  ones — this is not a redeclaration of new objects, it is the same
  `lambdaMax`, `lambdaMax_lipschitz`, `lambdaMax_hasEigenvalue`,
  `lambda2`, `trace_lipschitz`, `lambda2_lipschitz`, reproduced because
  the lab's own Wave-1/Wave-2 single-file convention leaves no other
  route to them. Everything from "New content specific to this item"
  onward IS new content specific to SHARED-2A-EXT.

  MOTIVATION / RELATION TO WAVE-2 SHARED-2A. The Wave-2 file
  `SecondEigenvalueLipschitz.lean` defines `lambda2 T := trace T -
  lambdaMax T` as a purely ALGEBRAIC stand-in for "the second
  eigenvalue" and proves it is 3-Lipschitz, but its own header explicitly
  flags what it does NOT do:

    "`lambda2` is an ALGEBRAIC definition (`trace - lambdaMax`), not (in
    this file) independently shown to BE an eigenvalue of `T` the way
    `lambdaMax_hasEigenvalue` does for `lambdaMax` in the Wave-1 file —
    doing so would need `IsSymmetric.trace_eq_sum_eigenvalues` plus
    `IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional` applied to the
    restriction of a symmetric `T` to the orthogonal complement of a
    `lambdaMax`-eigenvector, which is exactly the [...] gap [...] not
    attempted, here."

  This Wave-3 item is EXACTLY the falsifiable test proposed to close that
  flagged gap, and nothing broader: for `T` SYMMETRIC and `dim E = 2`,
  `lambda2 T` genuinely IS an eigenvalue of `T` (`Module.End.HasEigenvalue
  (T : E →ₗ[ℝ] E) (lambda2 T)`), proved via Mathlib's finite-dimensional
  spectral-theorem API for symmetric operators
  (`LinearMap.IsSymmetric.eigenvalues`, sorted in decreasing order) rather
  than by restricting `T` to an orthogonal complement by hand (the route
  the Wave-2 header sketched but did not attempt) — this is a strictly
  more direct route to the same conclusion, using tooling
  (`exists_eigenvalues_eq`, `eigenvalues_antitone`,
  `trace_eq_sum_eigenvalues`, `hasEigenvalue_eigenvalues`) that turned out
  to already be present (verified by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` and
  `Mathlib/Analysis/InnerProductSpace/Trace.lean` in the vendored
  snapshot), exactly as named in the falsifiable test proposal.

  PROOF SKETCH for the new result `lambda2_hasEigenvalue`:
    (1) `lambdaMax T` is an eigenvalue of `(T : E →ₗ[ℝ] E)`
        (`lambdaMax_hasEigenvalue`, reproduced verbatim from the Wave-1
        file below), so by `hT.exists_eigenvalues_eq hn` there is some
        index `i0 : Fin 2` with `hT.eigenvalues hn i0 = lambdaMax T`.
    (2) The REVERSE Rayleigh bound: the `0`-th vector of Mathlib's sorted
        eigenvector basis, `hT.eigenvectorBasis hn 0`, is a genuine
        nonzero eigenvector of `T` with eigenvalue `hT.eigenvalues hn 0`
        (`hasEigenvector_eigenvectorBasis` / `apply_eigenvectorBasis`);
        its Rayleigh quotient therefore equals `hT.eigenvalues hn 0`
        exactly, and by `le_ciSup` (applied to the SAME bounded-above
        family `bddAbove_rayleighQuotient_subtype` used to define
        `lambdaMax` itself) this Rayleigh quotient is `≤ lambdaMax T`.
        Hence `hT.eigenvalues hn 0 ≤ lambdaMax T`.
    (3) `hT.eigenvalues hn` is `Antitone` on `Fin 2`
        (`eigenvalues_antitone`), and `0 ≤ i0` trivially in `Fin 2`, so
        `hT.eigenvalues hn i0 ≤ hT.eigenvalues hn 0`.
    (4) Combining (1)-(3) by `linarith` (`eigenvalues i0 = lambdaMax T`,
        `eigenvalues i0 ≤ eigenvalues 0`, `eigenvalues 0 ≤ lambdaMax T`)
        forces `lambdaMax T = hT.eigenvalues hn 0`: this is the "fixar
        lambdaMax T = eigenvalues 0" step the falsifiable test asked for.
    (5) `IsSymmetric.trace_eq_sum_eigenvalues` plus `Fin.sum_univ_two`
        give `(T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 +
        hT.eigenvalues hn 1`, so (via step 4 and the definition of
        `lambda2`) `lambda2 T = hT.eigenvalues hn 1` exactly.
    (6) `hasEigenvalue_eigenvalues hT hn 1 : Module.End.HasEigenvalue
        (T : E →ₗ[ℝ] E) (hT.eigenvalues hn 1)` closes the goal by
        rewriting with step (5).

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`,
  `Mathlib/Analysis/InnerProductSpace/Trace.lean`, and
  `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean` in the
  vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean`):
    - `LinearMap.IsSymmetric.eigenvalues`, `.exists_eigenvalues_eq`,
      `.eigenvalues_antitone`, `.hasEigenvalue_eigenvalues`,
      `.eigenvectorBasis`, `.hasEigenvector_eigenvectorBasis`,
      `.apply_eigenvectorBasis` — all from
      `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` (the finite-
      dimensional spectral-theorem API for symmetric operators: a sorted-
      decreasing family of eigenvalues `Fin n → ℝ` together with a
      matching orthonormal eigenvector basis).
    - `LinearMap.IsSymmetric.trace_eq_sum_eigenvalues` from
      `Mathlib/Analysis/InnerProductSpace/Trace.lean` — for `𝕜 = ℝ` this
      states `T.trace ℝ E = ∑ i, hT.eigenvalues hn i` directly (no
      `RCLike.re` needed, unlike the general-`𝕜` `re_trace_eq_sum_eigenvalues`
      variant, which this file does not need).
    - `ContinuousLinearMap.coe_coe (f : M₁ →SL[σ₁₂] M₂) : ⇑(f : M₁ →ₛₗ[σ₁₂]
      M₂) = f` from
      `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean` —
      bridges the `ContinuousLinearMap` application `T x` used by
      `ContinuousLinearMap.rayleighQuotient` with the `LinearMap`
      application `(T : E →ₗ[ℝ] E) x` used by `apply_eigenvectorBasis`;
      the two coincide definitionally, and this lemma makes that fact
      `simp`-usable.
    - `le_ciSup`, `real_inner_smul_left`, `real_inner_self_eq_norm_sq`,
      `Fin.sum_univ_two`, `Fin.zero_le` — the elementary supremum /
      inner-product / finite-sum toolkit, matching the reproduced Wave-1
      / Wave-2 blocks' own usage.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-3 instructions). This file is specific to `dim E = 2`: it needs
  `Fin.sum_univ_two` to unfold the sorted-eigenvalue sum into exactly two
  terms, and the whole "reverse Rayleigh bound pins down index 0" argument
  in step (2)-(4) above is stated only for `hT.eigenvalues hn 0`, not for
  a general `i`-th eigenvalue in higher dimension; no claim is made or
  attempted about `n > 2`, and no general Courant-Fischer / min-max
  characterization of the `k`-th eigenvalue is proved or used (matching
  the Wave-1 header's own honest flag that no such general characterization
  was found in the vendored Mathlib snapshot). Nothing here is about
  Yang-Mills, SU(N), the lattice-gauge partition function, reflection
  positivity, or the continuum limit; it says nothing about, and does not
  approximate, a solution to the Clay mass-gap problem. No mathematical
  novelty is claimed: that in a fixed 2-dimensional real inner product
  space the algebraic quantity "trace minus top eigenvalue" of a
  symmetric operator is itself an eigenvalue (namely the smaller one) is
  a completely classical, elementary fact of 2x2 symmetric linear
  algebra, immediate from the spectral theorem.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

namespace SHARED2AEXT.SecondEigenvalueHasEigenvalue

/-! ### Reproduced verbatim from the Wave-2 file
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueLipschitz.lean`
(itself reproduced verbatim from the Wave-1 file
`04_YANG_MILLS/FORMAL/FixedDimEigenvalueStability.lean`; see BUILD-SYSTEM
NOTE above for why this cannot instead be an `import`): the fixed
2-dimensional space `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
and `lambdaMax_lipschitz`. -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`FixedDimEigenvalueStability.lean` and `SecondEigenvalueLipschitz.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `FixedDimEigenvalueStability.lean` and
`SecondEigenvalueLipschitz.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`FixedDimEigenvalueStability.lean` and `SecondEigenvalueLipschitz.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim.** `lambdaMax` is 1-Lipschitz
in operator norm on the fixed space `E`. Byte-identical (proof included)
to `lambdaMax_lipschitz` in `FixedDimEigenvalueStability.lean` and
`SecondEigenvalueLipschitz.lean`. -/
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

/-! ### Reproduced verbatim from the Wave-1 file
`04_YANG_MILLS/FORMAL/FixedDimEigenvalueStability.lean`, lines 139-144
(NOT present in the Wave-2 file `SecondEigenvalueLipschitz.lean`): the
"`lambdaMax` genuinely is an eigenvalue for symmetric `T`" result. -/

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`
(not merely an abstractly-defined real number) -- this is exactly
Mathlib's finite-dimensional existence theorem for the Rayleigh-quotient
supremum, `LinearMap.IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional`,
transported along the (defeq, up to the coercion `ContinuousLinearMap →
LinearMap`) identification between `ContinuousLinearMap.rayleighQuotient`
and the raw Rayleigh-quotient expression that lemma is stated with. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Reproduced verbatim from the Wave-2 file
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueLipschitz.lean`:
`basis2`, `trace_lipschitz`, `lambda2`, and `lambda2_lipschitz`. -/

/-- The fixed orthonormal basis of `E` the falsifiable test asks for
("base ortonormal fixa"): the standard `Fin 2`-indexed basis of
`EuclideanSpace ℝ (Fin 2)`. -/
noncomputable def basis2 : OrthonormalBasis (Fin 2) ℝ E := EuclideanSpace.basisFun (Fin 2) ℝ

/-- **Wave-2 SHARED-2A result, reproduced verbatim.** `trace` (of the
`LinearMap` coercion of a continuous linear self-map of `E`) is
`2`-Lipschitz in operator norm on `E`, via `LinearMap.trace_eq_sum_inner`
expanded over the fixed orthonormal basis `basis2`. No symmetry
hypothesis on `A` or `B` is needed. -/
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

/-- **The falsifiable test's target quantity, reproduced verbatim from
Wave-2 SHARED-2A.** `lambda2 T := trace T - lambdaMax T`, an algebraic
stand-in for "the second eigenvalue" of `T` that is well-defined (a real
number) for ANY continuous linear self-map of the fixed 2-dimensional
space `E`. THIS Wave-3 item's new content (`lambda2_hasEigenvalue` below)
is precisely what upgrades this from "algebraic stand-in" to "genuine
eigenvalue", for symmetric `T`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Wave-2 SHARED-2A result, reproduced verbatim.** `lambda2` is
`3`-Lipschitz in operator norm on the fixed space `E`. No symmetry
hypothesis on `A` or `B` is needed for this inequality. -/
theorem lambda2_lipschitz (A B : E →L[ℝ] E) :
    |lambda2 A - lambda2 B| ≤ 3 * ‖A - B‖ := by
  have h1 := trace_lipschitz A B
  have h2 := lambdaMax_lipschitz A B
  unfold lambda2
  rw [abs_le] at h1 h2 ⊢
  constructor <;> [linarith [h1.1, h2.1]; linarith [h1.2, h2.2]]

/-! ### New content specific to this item (SHARED-2A-EXT): `lambda2 T` is
a genuine eigenvalue of `T` when `T` is symmetric and `dim E = 2`. -/

/-- **Main new result (SHARED-2A-EXT), the falsifiable test as stated.**
For a symmetric `T : E →L[ℝ] E` on the fixed 2-dimensional space `E`,
`lambda2 T := trace T - lambdaMax T` is a GENUINE eigenvalue of `T`, not
merely an algebraically-defined real number. See the PROOF SKETCH in the
file header for the six-step argument: `lambdaMax T` is pinned to
`hT.eigenvalues hn 0` via a reverse Rayleigh bound on Mathlib's sorted
`0`-th eigenvector combined with `eigenvalues_antitone`, then
`trace_eq_sum_eigenvalues` plus `Fin.sum_univ_two` identify `lambda2 T`
with `hT.eigenvalues hn 1`, which `hasEigenvalue_eigenvalues` confirms is
a genuine eigenvalue. -/
theorem lambda2_hasEigenvalue (T : E →L[ℝ] E) (hT : (T : E →ₗ[ℝ] E).IsSymmetric)
    (hn : Module.finrank ℝ E = 2) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambda2 T) := by
  -- Step 1: `lambdaMax T` is an eigenvalue, hence `= hT.eigenvalues hn i0` for some `i0`.
  have hmaxEig : Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) :=
    lambdaMax_hasEigenvalue T hT
  obtain ⟨i0, hi0⟩ := hT.exists_eigenvalues_eq hn hmaxEig
  -- Step 2: reverse Rayleigh bound at the sorted `0`-th eigenvector:
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
  -- Step 3: `eigenvalues` antitone on `Fin 2`, so `eigenvalues i0 ≤ eigenvalues 0`.
  have hanti : hT.eigenvalues hn i0 ≤ hT.eigenvalues hn 0 :=
    hT.eigenvalues_antitone hn (Fin.zero_le i0)
  -- Step 4: combine to pin `lambdaMax T = hT.eigenvalues hn 0`.
  have hi0' : hT.eigenvalues hn i0 = lambdaMax T := by exact_mod_cast hi0
  have heq0 : lambdaMax T = hT.eigenvalues hn 0 := by linarith [hi0', hanti, hle]
  -- Step 5: `trace = eigenvalues 0 + eigenvalues 1`, so `lambda2 T = eigenvalues 1`.
  have htrace : (T : E →ₗ[ℝ] E).trace ℝ E = hT.eigenvalues hn 0 + hT.eigenvalues hn 1 := by
    rw [hT.trace_eq_sum_eigenvalues hn, Fin.sum_univ_two]
    norm_cast
  have hlambda2 : lambda2 T = hT.eigenvalues hn 1 := by
    unfold lambda2
    rw [htrace, heq0]; ring
  -- Step 6: `hT.eigenvalues hn 1` is a genuine eigenvalue.
  rw [hlambda2]
  exact hT.hasEigenvalue_eigenvalues hn 1

end SHARED2AEXT.SecondEigenvalueHasEigenvalue

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED2AEXT.SecondEigenvalueHasEigenvalue.bddAbove_rayleighQuotient_subtype
#print axioms SHARED2AEXT.SecondEigenvalueHasEigenvalue.lambdaMax_lipschitz
#print axioms SHARED2AEXT.SecondEigenvalueHasEigenvalue.lambdaMax_hasEigenvalue
#print axioms SHARED2AEXT.SecondEigenvalueHasEigenvalue.trace_lipschitz
#print axioms SHARED2AEXT.SecondEigenvalueHasEigenvalue.lambda2_lipschitz
#print axioms SHARED2AEXT.SecondEigenvalueHasEigenvalue.lambda2_hasEigenvalue
