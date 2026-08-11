/-
  SHARED-4A — two-eigenvalue exhaustiveness in dimension 2: every
  eigenvalue of a symmetric operator on the fixed 2-dimensional space `E`
  equals either `lambdaMax T` or `lambda2 T`. Wave-4 batch,
  shared-infrastructure item, a direct follow-on to the Wave-3 item
  `SHARED-2A-EXT` (`SecondEigenvalueHasEigenvalue.lean`).

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
  dependencies, and by the Wave-2 files before it).
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
  it is the same `E`, `lambdaMax`, `bddAbove_rayleighQuotient_subtype`,
  `lambdaMax_hasEigenvalue`, `lambda2`, reproduced because the lab's own
  single-file convention leaves no other route to them. Everything from
  "New content specific to this item" onward IS new content specific to
  SHARED-4A. Only the definitions and lemmas actually needed for this
  item's proof are reproduced (`basis2`, `trace_lipschitz`,
  `lambdaMax_lipschitz`, `lambda2_lipschitz` from
  `SecondEigenvalueHasEigenvalue.lean` are NOT needed here and are
  therefore NOT reproduced, to keep this file minimal).

  MOTIVATION / RELATION TO WAVE-3 SHARED-2A-EXT. The Wave-3 file
  `SecondEigenvalueHasEigenvalue.lean` proves `lambda2_hasEigenvalue`:
  for symmetric `T` on the fixed 2-dimensional `E`, `lambda2 T := trace T
  - lambdaMax T` is a genuine eigenvalue of `T`. Its proof internally
  derives two facts as unnamed/unexported `have`s inside that one
  theorem's proof term (never promoted to standalone, reusable lemmas):
    - `heq0 : lambdaMax T = hT.eigenvalues hn 0` (line 364 of that file)
    - `hlambda2 : lambda2 T = hT.eigenvalues hn 1` (lines 369-371 of that
      file)
  This Wave-4 item is EXACTLY the falsifiable test proposed to close the
  natural follow-on gap this leaves: since `hT.eigenvalues hn` for `hn :
  finrank ℝ E = 2` has exactly the two indices `0` and `1` (all of
  `Fin 2`), and `Mathlib`'s `exists_eigenvalues_eq` states that EVERY
  eigenvalue `mu` of `T` equals `hT.eigenvalues hn i` for SOME index `i`
  (not just `lambdaMax T`'s own index), combining `exists_eigenvalues_eq`
  with the two promoted facts above and a trivial case-split on `Fin 2`
  gives EXHAUSTIVENESS: every eigenvalue of `T` is either `lambdaMax T`
  or `lambda2 T`, with no third possibility. Nothing broader is attempted
  here.

  PROOF SKETCH.
    (1) `lambdaMax_eq_eigenvalues_zero` (promoting `heq0`): reproduces,
        as a standalone named theorem, exactly the argument
        `SecondEigenvalueHasEigenvalue.lean` uses inside
        `lambda2_hasEigenvalue`'s proof (steps 1-4 of that file's own
        PROOF SKETCH): `lambdaMax T` is an eigenvalue
        (`lambdaMax_hasEigenvalue`), hence `= hT.eigenvalues hn i0` for
        some `i0` (`exists_eigenvalues_eq`); a reverse Rayleigh bound at
        the sorted `0`-th eigenvector (`apply_eigenvectorBasis`,
        `le_ciSup` against `bddAbove_rayleighQuotient_subtype`) gives
        `hT.eigenvalues hn 0 ≤ lambdaMax T`; antitonicity
        (`eigenvalues_antitone`) gives `hT.eigenvalues hn i0 ≤
        hT.eigenvalues hn 0`; combining by `linarith` forces
        `lambdaMax T = hT.eigenvalues hn 0`.
    (2) `lambda2_eq_eigenvalues_one` (promoting `hlambda2`):
        `IsSymmetric.trace_eq_sum_eigenvalues` plus `Fin.sum_univ_two`
        give `trace = hT.eigenvalues hn 0 + hT.eigenvalues hn 1`;
        combined with (1) and the definition of `lambda2`, this forces
        `lambda2 T = hT.eigenvalues hn 1`.
    (3) `eigenvalue_eq_lambdaMax_or_lambda2`, the falsifiable test as
        stated: given ANY eigenvalue `mu` of `T` (`hmu : HasEigenvalue T
        mu`), `hT.exists_eigenvalues_eq hn hmu` gives some `i : Fin 2`
        with `hT.eigenvalues hn i = mu`. Since `Fin 2 = {0, 1}`
        (`fin_cases i`), either `i = 0` — in which case `mu =
        hT.eigenvalues hn 0 = lambdaMax T` by (1) — or `i = 1` — in which
        case `mu = hT.eigenvalues hn 1 = lambda2 T` by (2). Either way
        `mu = lambdaMax T ∨ mu = lambda2 T`, exactly the exhaustiveness
        claim.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Spectrum.lean` and
  `Mathlib/Analysis/InnerProductSpace/Trace.lean` in the vendored
  snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean` — the SAME tools already verified present
  by the Wave-3 file `SecondEigenvalueHasEigenvalue.lean`, plus
  `fin_cases` for the new case-split on `Fin 2`):
    - `LinearMap.IsSymmetric.eigenvalues`, `.exists_eigenvalues_eq`,
      `.eigenvalues_antitone`, `.eigenvectorBasis`,
      `.hasEigenvector_eigenvectorBasis`, `.apply_eigenvectorBasis` —
      from `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`.
    - `LinearMap.IsSymmetric.trace_eq_sum_eigenvalues` from
      `Mathlib/Analysis/InnerProductSpace/Trace.lean`.
    - `le_ciSup`, `real_inner_smul_left`, `Fin.sum_univ_two`,
      `Fin.zero_le` — the elementary supremum / inner-product / finite-
      sum toolkit, matching the reproduced Wave-3 block's own usage.
    - `fin_cases` — the standard Mathlib/Lean tactic for exhaustive
      case-splitting over the (finitely many, here two) inhabitants of
      `Fin 2`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-4 instructions). This file is specific to `dim E = 2`, exactly as
  its Wave-3 predecessor `SecondEigenvalueHasEigenvalue.lean` is; no
  claim is made or attempted about `n > 2`, and no general
  Courant-Fischer / min-max characterization of the `k`-th eigenvalue (or
  general "every eigenvalue equals one of the `n` sorted eigenvalues"
  fact for arbitrary `n`) is proved or used here — that more general
  statement is, in fact, already exactly what `exists_eigenvalues_eq`
  gives for free in Mathlib for any `n`; what THIS file adds beyond that
  is only the dimension-2-specific identification of the two sorted
  eigenvalues `hT.eigenvalues hn 0` / `hT.eigenvalues hn 1` with the
  ALGEBRAIC quantities `lambdaMax T` / `lambda2 T` defined via Rayleigh
  quotient / trace elsewhere in this shared-infra line. Nothing here is
  about Yang-Mills, SU(N), the lattice-gauge partition function,
  reflection positivity, the continuum limit, or any other Millennium
  problem; it says nothing about, and does not approximate, a solution to
  any of them. No mathematical novelty is claimed: that a symmetric
  operator on a 2-dimensional real inner product space has exactly two
  eigenvalues (counted with the sorted-eigenvalue-family convention) is a
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

namespace SHARED4A.TwoEigenvalueExhaustiveness

/-! ### Reproduced verbatim from the Wave-3 file
`03_MILLENNIUM/_SHARED_INFRA/FORMAL/SecondEigenvalueHasEigenvalue.lean`
(see BUILD-SYSTEM NOTE above for why this cannot instead be an
`import`): the fixed 2-dimensional space `E`, `lambdaMax`,
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

/-! ### New content specific to this item (SHARED-4A). Section 1: promote
the two internal, unnamed `have`s of `SecondEigenvalueHasEigenvalue.lean`'s
`lambda2_hasEigenvalue` proof (`heq0` at its line 364, `hlambda2` at its
lines 369-371) to standalone, reusable, named theorems. -/

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

/-! ### New content specific to this item (SHARED-4A). Section 2: the
falsifiable test itself, `eigenvalue_eq_lambdaMax_or_lambda2` — every
eigenvalue of a symmetric `T` on the fixed 2-dimensional `E` equals
`lambdaMax T` or `lambda2 T`, via `exists_eigenvalues_eq` applied to an
arbitrary eigenvalue `mu`, the two promoted lemmas above, and a
case-split on `Fin 2`. -/

/-- **Main new result (SHARED-4A), the falsifiable test as stated.**
Two-eigenvalue exhaustiveness in dimension 2: for symmetric `T : E →L[ℝ]
E` on the fixed 2-dimensional `E`, EVERY eigenvalue `mu` of `T` equals
either `lambdaMax T` or `lambda2 T` — there is no third possibility.
Proof: `hT.exists_eigenvalues_eq hn hmu` gives some index `i : Fin 2`
with `hT.eigenvalues hn i = mu`; `fin_cases i` exhausts the two
possibilities `i = 0` and `i = 1`, resolved respectively by
`lambdaMax_eq_eigenvalues_zero` and `lambda2_eq_eigenvalues_one`. -/
theorem eigenvalue_eq_lambdaMax_or_lambda2 (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) (hn : Module.finrank ℝ E = 2)
    {mu : ℝ} (hmu : Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) mu) :
    mu = lambdaMax T ∨ mu = lambda2 T := by
  obtain ⟨i, hi⟩ := hT.exists_eigenvalues_eq hn hmu
  have heq0 := lambdaMax_eq_eigenvalues_zero T hT hn
  have heq1 := lambda2_eq_eigenvalues_one T hT hn
  fin_cases i
  · left; rw [← hi]; exact heq0.symm
  · right; rw [← hi]; exact heq1.symm

end SHARED4A.TwoEigenvalueExhaustiveness

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED4A.TwoEigenvalueExhaustiveness.bddAbove_rayleighQuotient_subtype
#print axioms SHARED4A.TwoEigenvalueExhaustiveness.lambdaMax_hasEigenvalue
#print axioms SHARED4A.TwoEigenvalueExhaustiveness.lambdaMax_eq_eigenvalues_zero
#print axioms SHARED4A.TwoEigenvalueExhaustiveness.lambda2_eq_eigenvalues_one
#print axioms SHARED4A.TwoEigenvalueExhaustiveness.eigenvalue_eq_lambdaMax_or_lambda2
