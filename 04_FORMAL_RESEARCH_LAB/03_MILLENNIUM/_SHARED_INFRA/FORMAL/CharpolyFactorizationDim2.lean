/-
  SHARED-5A — characteristic-polynomial factorization in dimension 2: for
  a symmetric operator `T` on the fixed 2-dimensional space `E`, the
  characteristic polynomial of (the `LinearMap` coercion of) `T` factors
  as `(X - C (lambdaMax T)) * (X - C (lambda2 T))`. Wave-5 batch,
  shared-infrastructure item, a direct follow-on to the Wave-4 item
  `SHARED-4A` (`TwoEigenvalueExhaustiveness.lean`) and the Wave-3 item
  `SHARED-2A-EXT` (`SecondEigenvalueHasEigenvalue.lean`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` — see the Wave-5 task instructions on
  build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1, Wave-2, Wave-3, Wave-4, or other Wave-5 file. It only *reads*
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/TwoEigenvalueExhaustiveness.lean`
  (Wave-4, SHARED-4A) and, transitively via that file's own header,
  `03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueHasEigenvalue.lean`
  (Wave-3, SHARED-2A-EXT).

  BUILD-SYSTEM NOTE (why `E`, `lambdaMax`,
  `bddAbove_rayleighQuotient_subtype`, `lambdaMax_hasEigenvalue`,
  `lambda2`, `lambdaMax_eq_eigenvalues_zero`, and
  `lambda2_eq_eigenvalues_one` are all reproduced below instead of
  imported — same situation already documented by the Wave-4 file
  `TwoEigenvalueExhaustiveness.lean` for its own Wave-3 dependency, and
  by the Wave-3/Wave-2 files before it). `TwoEigenvalueExhaustiveness.lean`
  is, by its own header, deliberately free-standing and NOT registered in
  `TamesisLab.lean` — it lives outside the `[[lean_lib]] name =
  "TamesisLab"` module graph declared in `lakefile.toml` and has no built
  `.olean`, so it cannot be `import`ed by module name from this file. Per
  the Wave-5 task instructions ("do NOT touch any file outside your own
  new file(s)"), this file cannot register `TwoEigenvalueExhaustiveness.lean`
  into the library graph either. The only way to reuse its content under
  this constraint is to reproduce the relevant definitions/proofs
  VERBATIM (byte-identical, copied directly from
  `TwoEigenvalueExhaustiveness.lean`) rather than inventing different
  ones — this is not a redeclaration of new objects, it is the same `E`,
  `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
  `lambdaMax_hasEigenvalue`, `lambda2`, `lambdaMax_eq_eigenvalues_zero`,
  `lambda2_eq_eigenvalues_one`, reproduced because the lab's own
  single-file convention leaves no other route to them. Everything from
  "New content specific to this item" onward IS new content specific to
  SHARED-5A. The exhaustiveness theorem itself
  (`eigenvalue_eq_lambdaMax_or_lambda2`) is NOT needed for this item's
  proof and is therefore NOT reproduced, to keep this file minimal.

  MOTIVATION / RELATION TO WAVE-4 SHARED-4A AND WAVE-3 SHARED-2A-EXT. The
  Wave-3 file `SecondEigenvalueHasEigenvalue.lean` establishes
  `lambdaMax T = hT.eigenvalues hn 0` and `lambda2 T = hT.eigenvalues hn
  1` for symmetric `T` on the fixed 2-dimensional `E` (originally as
  unnamed internal `have`s, promoted to the standalone named lemmas
  `lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one` by the
  Wave-4 file `TwoEigenvalueExhaustiveness.lean`). Separately, Mathlib's
  `LinearMap.IsSymmetric.charpoly_eq` states, for ANY `n` and any
  symmetric `T` with `Module.finrank 𝕜 E = n`, that `T.charpoly = ∏ i,
  (X - C (hT.eigenvalues hn i))`. This Wave-5 item is EXACTLY the
  falsifiable test proposed to combine these two facts in the
  dimension-2 case: unfolding the product over `Fin 2` via
  `Fin.prod_univ_two` and rewriting the two factors with
  `lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one` gives the
  explicit two-root factorization `T.charpoly = (X - C (lambdaMax T)) *
  (X - C (lambda2 T))`, with NO detour through `Matrix.charpoly_fin_two`,
  no `ToMatrix` bridge, and no explicit choice of basis — exactly as the
  falsifiable test specifies ("Sem Matrix.charpoly_fin_two, sem ponte
  ToMatrix, sem base explicita").

  PROOF SKETCH for the new result `charpoly_factorization`:
    (1) `hT.charpoly_eq hn : T.charpoly = ∏ i : Fin 2, (X - C
        (hT.eigenvalues hn i))` (Mathlib, `Analysis/InnerProductSpace/
        Spectrum.lean`, specialized to `n = 2` via `hn`).
    (2) `Fin.prod_univ_two` unfolds the two-element product: `∏ i : Fin
        2, (X - C (hT.eigenvalues hn i)) = (X - C (hT.eigenvalues hn 0))
        * (X - C (hT.eigenvalues hn 1))`.
    (3) `lambdaMax_eq_eigenvalues_zero T hT hn : lambdaMax T =
        hT.eigenvalues hn 0` and `lambda2_eq_eigenvalues_one T hT hn :
        lambda2 T = hT.eigenvalues hn 1` (both reproduced verbatim below
        from the Wave-4 file, themselves reproducing the Wave-3 file's
        internal argument — see that file's own PROOF SKETCH for the
        six-step derivation) let the two factors from (2) be rewritten
        as `X - C (lambdaMax T)` and `X - C (lambda2 T)` respectively.
    (4) Chaining (1)-(3) by `rw` gives exactly the falsifiable test's
        claimed equality, `T.charpoly = (X - C (lambdaMax T)) * (X - C
        (lambda2 T))`, with the final goal closing by `rfl` (definitional
        equality after both sides have been rewritten to the identical
        term).

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` in the vendored
  snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean` — the SAME tools already verified present
  by the Wave-3/Wave-4 files, plus `Fin.prod_univ_two` and the
  `Polynomial` notation `X`/`C` for the new factorization step):
    - `LinearMap.IsSymmetric.charpoly_eq` — from
      `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` (`open
      Polynomial in theorem charpoly_eq (hT : T.IsSymmetric) (hn :
      Module.finrank 𝕜 E = n) : T.charpoly = ∏ i, (X - C (hT.eigenvalues
      hn i : 𝕜))`, in the `LinearMap.IsSymmetric` namespace, `Version2`
      section).
    - `LinearMap.IsSymmetric.eigenvalues`, `.exists_eigenvalues_eq`,
      `.eigenvalues_antitone`, `.eigenvectorBasis`,
      `.hasEigenvector_eigenvectorBasis`, `.apply_eigenvectorBasis` —
      from the same file, needed only inside the reproduced
      `lambdaMax_eq_eigenvalues_zero` / `lambda2_eq_eigenvalues_one`
      block (unchanged from the Wave-4 file).
    - `LinearMap.IsSymmetric.trace_eq_sum_eigenvalues` from
      `Mathlib/Analysis/InnerProductSpace/Trace.lean` — needed only
      inside the reproduced `lambda2_eq_eigenvalues_one` block.
    - `Fin.prod_univ_two : ∏ i : Fin 2, f i = f 0 * f 1` — the finite
      two-element product-unfolding lemma this item's new step needs (the
      multiplicative analogue of `Fin.sum_univ_two`, already used by the
      reproduced Wave-3/Wave-4 block).
    - `le_ciSup`, `real_inner_smul_left`, `Fin.zero_le` — the elementary
      supremum / inner-product toolkit, matching the reproduced Wave-4
      block's own usage.
    - `Polynomial.X`, `Polynomial.C` — the indeterminate and constant-
      polynomial embedding notation used to state the factorization,
      opened via `open Polynomial`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-5 instructions). This file is specific to `dim E = 2`, exactly as
  its Wave-3/Wave-4 predecessors are; no claim is made or attempted about
  `n > 2`, and no general factorization of the characteristic polynomial
  into `n` linear factors for arbitrary `n` is proved here beyond what
  `LinearMap.IsSymmetric.charpoly_eq` already gives for free in Mathlib
  for any `n` (as a product over `Fin n`, not yet identified with any
  ALGEBRAIC quantities like `lambdaMax`/`lambda2` outside the `n = 2`
  case handled by this shared-infra line). Nothing here is about
  Yang-Mills, SU(N), the lattice-gauge partition function, reflection
  positivity, the continuum limit, or any other Millennium problem; it
  says nothing about, and does not approximate, a solution to any of
  them. No mathematical novelty is claimed: that the characteristic
  polynomial of a symmetric operator on a 2-dimensional real inner
  product space factors as `(X - lambda_max)(X - lambda_min)` is a
  completely classical, elementary fact of 2x2 symmetric linear algebra,
  immediate from the spectral theorem.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

open Polynomial

namespace SHARED5A.CharpolyFactorizationDim2

/-! ### Reproduced verbatim from the Wave-4 file
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/TwoEigenvalueExhaustiveness.lean`
(itself reproduced verbatim from the Wave-3 file
`SecondEigenvalueHasEigenvalue.lean`; see BUILD-SYSTEM NOTE above for why
this cannot instead be an `import`): the fixed 2-dimensional space `E`,
`lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
`lambdaMax_hasEigenvalue`, `lambda2`, `lambdaMax_eq_eigenvalues_zero`,
and `lambda2_eq_eigenvalues_one`. -/

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Byte-identical to `E` in
`TwoEigenvalueExhaustiveness.lean`. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of `E`: the
supremum of the Rayleigh quotient over nonzero vectors. Byte-identical to
`lambdaMax` in `TwoEigenvalueExhaustiveness.lean`. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every nonzero
vector. Byte-identical to `bddAbove_rayleighQuotient_subtype` in
`TwoEigenvalueExhaustiveness.lean`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

/-- **Wave-1 YM-3 result, reproduced verbatim (via the Wave-3/Wave-4
files).** For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of
`T`. Byte-identical (proof included) to `lambdaMax_hasEigenvalue` in
`TwoEigenvalueExhaustiveness.lean`. -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-- **Reproduced verbatim from `TwoEigenvalueExhaustiveness.lean`
(itself reproduced verbatim from Wave-2 SHARED-2A).** `lambda2 T :=
trace T - lambdaMax T`, an algebraic stand-in for "the second
eigenvalue" of `T`, well-defined (a real number) for ANY continuous
linear self-map of the fixed 2-dimensional space `E`. -/
noncomputable def lambda2 (T : E →L[ℝ] E) : ℝ :=
  (T : E →ₗ[ℝ] E).trace ℝ E - lambdaMax T

/-- **Reproduced verbatim from `TwoEigenvalueExhaustiveness.lean`.** For
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

/-- **Reproduced verbatim from `TwoEigenvalueExhaustiveness.lean`.** For
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

/-! ### New content specific to this item (SHARED-5A): the falsifiable
test itself, `charpoly_factorization` — the characteristic polynomial of
a symmetric `T` on the fixed 2-dimensional `E` factors as `(X - C
(lambdaMax T)) * (X - C (lambda2 T))`, via `hT.charpoly_eq hn`,
`Fin.prod_univ_two`, and the two eigenvalue-identification lemmas above.
No `Matrix.charpoly_fin_two`, no `ToMatrix` bridge, no explicit choice of
basis. -/

/-- **Main new result (SHARED-5A), the falsifiable test as stated.**
Characteristic-polynomial factorization in dimension 2: for symmetric `T
: E →L[ℝ] E` on the fixed 2-dimensional `E`, the characteristic
polynomial of `(T : E →ₗ[ℝ] E)` factors explicitly as `(X - C (lambdaMax
T)) * (X - C (lambda2 T))`. Proof: `hT.charpoly_eq hn` gives `T.charpoly
= ∏ i : Fin 2, (X - C (hT.eigenvalues hn i))`; `Fin.prod_univ_two`
unfolds this to `(X - C (hT.eigenvalues hn 0)) * (X - C (hT.eigenvalues
hn 1))`; `lambdaMax_eq_eigenvalues_zero` and `lambda2_eq_eigenvalues_one`
identify the two indices with `lambdaMax T` and `lambda2 T`
respectively. -/
theorem charpoly_factorization (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2) :
    (T : E →ₗ[ℝ] E).charpoly = (X - C (lambdaMax T)) * (X - C (lambda2 T)) := by
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have heq1 := lambda2_eq_eigenvalues_one T hT hn
  rw [hT.charpoly_eq hn, Fin.prod_univ_two]
  -- Mathlib's `charpoly_eq` states the factors with an `RCLike.ofReal`
  -- coercion `(hT.eigenvalues hn i : 𝕜)`; specialized to `𝕜 = ℝ` this
  -- coercion is definitionally `id` (`RCLike.ofReal_real_eq_id`), so
  -- `simp` clears it before the final rewrite by `heq0`/`heq1`.
  simp only [RCLike.ofReal_real_eq_id, id_eq]
  rw [heq0, heq1]

end SHARED5A.CharpolyFactorizationDim2

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED5A.CharpolyFactorizationDim2.bddAbove_rayleighQuotient_subtype
#print axioms SHARED5A.CharpolyFactorizationDim2.lambdaMax_hasEigenvalue
#print axioms SHARED5A.CharpolyFactorizationDim2.lambdaMax_eq_eigenvalues_zero
#print axioms SHARED5A.CharpolyFactorizationDim2.lambda2_eq_eigenvalues_one
#print axioms SHARED5A.CharpolyFactorizationDim2.charpoly_factorization
