/-
  YM-3 — fixed-finite-dimension eigenvalue-gap stability under
  operator-norm convergence (Wave-1 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-1 task instructions on
  build contention with 26 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of
  `InsufficiencyToyModel.lean` and `FiniteLatticeTransferGap.lean` in
  this same directory.

  MOTIVATION / RELATION TO YM-GAP-004. `../GAP_REGISTER.yaml` (gap_id
  `YM-GAP-004`) and `../COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md`
  ("Contraexemplo 3") record that the lab's own insufficiency audit
  found: operator-norm convergence of self-adjoint Hamiltonians
  `H_n → H` does NOT guarantee that a spectral gap survives the limit,
  when the underlying Hilbert space has GROWING/infinite dimension
  (there, a multiplication operator on `L²([0,1])`). That counterexample
  is explicitly NOT formalized in Lean in this lab (see its own
  "não formalizado" note).

  This file is the deliberate CONVERSE diagnostic: in a genuinely FIXED
  finite-dimensional real inner product space, this pathology provably
  cannot happen -- eigenvalues of self-adjoint operators vary
  1-Lipschitz-continuously with the operator in operator norm, via the
  Rayleigh-quotient variational principle. Formalizing this precisely
  delimits which hypothesis of YM-GAP-004 is doing the work: dimension
  held FIXED (this file: stability holds) vs. dimension DIVERGING with
  the lattice spacing (YM-GAP-004: stability can fail). It is not a step
  towards the continuum limit, towards Yang-Mills, or towards the Clay
  mass-gap problem in any sense -- see "WHAT THIS FILE DOES NOT DO"
  below.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/InnerProductSpace/Rayleigh.lean` in the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean`):
    - `ContinuousLinearMap.rayleighQuotient`      (L56)
    - `ContinuousLinearMap.rayleighQuotient_le_norm`  (L112) -- the key
      pointwise bound `|T.rayleighQuotient x| ≤ ‖T‖`, needing NO
      symmetry hypothesis on `T`, which is what makes the Lipschitz
      argument below elementary.
    - `LinearMap.IsSymmetric.hasEigenvalue_iSup_of_finiteDimensional`
      (L325) -- in finite dimension the SIGNED `iSup` of the Rayleigh
      quotient over nonzero vectors is realized as a genuine eigenvalue
      (Weierstrass extreme-value-on-sphere argument), which is what lets
      us honestly call `lambdaMax` below "the top eigenvalue" rather
      than an arbitrary real number.
  `norm_eq_iSup_rayleighQuotient` / `spectralRadius_eq_nnnorm` (also
  present in that file, L120 and L182) were the tools originally cited
  by the adversarial reviewer as sufficient for the `|·|`-sup route; in
  the event, the pointwise bound `rayleighQuotient_le_norm` gives a
  strictly more direct route to the same Lipschitz inequality (no need
  to first identify `‖T‖` with a sup of absolute Rayleigh quotients),
  so this file uses that lemma directly instead. This is a proof-route
  simplification, not a departure from the cited toolset -- all the
  same underlying Rayleigh-quotient API is exercised, and the identity
  `‖A - B‖ = ⨆ x, |(A-B).rayleighQuotient x|` (`norm_eq_iSup_rayleighQuotient`)
  is definitionally what makes `rayleighQuotient_le_norm` true for a
  symmetric `A - B`; the lemma statement just happens to already be
  proved for arbitrary (not necessarily symmetric) `T` in Mathlib, one
  layer down, which is the layer actually needed here.

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST. `E := EuclideanSpace ℝ
  (Fin 2)`, a FIXED 2-dimensional real inner product space (matching the
  originally proposed "cheapest possible falsifiable slice"). For any
  continuous linear `A B : E →L[ℝ] E` (no symmetry hypothesis needed for
  the Lipschitz bound itself; symmetry is used separately only to
  identify `lambdaMax` with a genuine eigenvalue):
    `lambdaMax_lipschitz : |lambdaMax A - lambdaMax B| ≤ ‖A - B‖`
  where `lambdaMax T := ⨆ x : {x : E // x ≠ 0}, T.rayleighQuotient x`.
  Combined with `lambdaMax_hasEigenvalue`, this shows: the top eigenvalue
  (in the Rayleigh-quotient-sup sense that Mathlib's own finite-dim
  existence theorem uses) of a symmetric operator on this FIXED
  2-dimensional space cannot "contract suddenly" under operator-norm
  convergence -- the opposite of what YM-GAP-004's growing-dimension
  counterexample exhibits.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, per Wave-1
  instructions). Only the TOP eigenvalue (`lambdaMax`, the `iSup` of the
  Rayleigh quotient) is treated here. The actual spectral GAP (top minus
  SECOND eigenvalue) would additionally need the analogous statement on
  the orthogonal complement of the top eigenvector -- straightforward in
  principle (restrict to `(ℝ ∙ x₀)ᗮ`, apply the same argument one
  dimension down) but genuinely NOT done in this file: no
  Courant-Fischer / min-max characterization of the k-th eigenvalue was
  found anywhere in the vendored Mathlib snapshot (confirmed by
  whole-tree grep for `Weyl`, `Courant`, `min-max`, `eigenvalues_sub_le`,
  turning up nothing relevant outside Lie-theoretic Weyl groups), so a
  full second-eigenvalue treatment is left as future work, not attempted
  here. This file says nothing about Yang-Mills, nothing about SU(N) or
  any gauge theory, nothing about the continuum/lattice-spacing-to-zero
  limit (the case YM-GAP-004 already shows is NOT covered by this fixed-
  dimension argument), and claims no mathematical novelty -- Lipschitz
  continuity of the top eigenvalue of a self-adjoint operator in operator
  norm, via the variational (Rayleigh-quotient) characterization, is
  classical (Weyl-type / Courant-Fischer perturbation theory, textbook
  linear algebra / functional analysis).
-/
import Mathlib

namespace YM3.FixedDimEigenvalueStability

/-- The fixed finite-dimensional real inner product space for this test:
`ℝ²` with its standard Euclidean inner product. Deliberately fixed once
and for all -- no sequence of growing-dimension spaces is involved
anywhere in this file, in contrast to YM-GAP-004. -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the
fixed space `E`: the supremum of the Rayleigh quotient over nonzero
vectors. For a symmetric `T` this is genuinely an eigenvalue of `T`
(`lambdaMax_hasEigenvalue` below); for general `T` it is still a
well-defined real number (bounded by `rayleighQuotient_le_norm`), which
is all the Lipschitz bound (`lambdaMax_lipschitz`) needs. -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- `lambdaMax` is bounded above by the operator norm along every
nonzero vector: `T.rayleighQuotient x ≤ ‖T‖` for all `x`, hence the
defining `iSup` is over a set bounded above by `‖T‖`. Uses
`ContinuousLinearMap.rayleighQuotient_le_norm`, which needs no symmetry
hypothesis on `T`. -/
theorem bddAbove_rayleighQuotient_subtype (T : E →L[ℝ] E) :
    BddAbove (Set.range fun x : { x : E // x ≠ 0 } => T.rayleighQuotient (x : E)) := by
  refine ⟨‖T‖, ?_⟩
  rintro _ ⟨x, rfl⟩
  exact (le_abs_self _).trans (T.rayleighQuotient_le_norm (x : E))

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

/-- **Main result (YM-3).** `lambdaMax` is 1-Lipschitz in operator norm
on the FIXED finite-dimensional space `E`: two continuous linear
operators close in operator norm have close Rayleigh-quotient suprema.
No symmetry hypothesis on `A` or `B` is needed for this inequality
itself (only `lambdaMax_hasEigenvalue` above needs symmetry, to justify
calling `lambdaMax` "the top eigenvalue"). This is the precise converse
of YM-GAP-004: that counterexample's spectral contraction under
operator-norm convergence relies on the ambient space's dimension
growing with `n`; here, with dimension held fixed once and for all, no
such contraction can occur -- `lambdaMax` cannot move by more than
`‖A - B‖`. -/
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

/-- **Corollary, the falsifiable test as originally stated.** For
self-adjoint (here: symmetric) `A B : E →L[ℝ] E` with `‖A - B‖ < ε`, the
top eigenvalues are within `ε`: `|lambdaMax A - lambdaMax B| ≤ ε`.
Immediate from `lambdaMax_lipschitz`; symmetry of `A`, `B` is not even
used in the inequality (only carried as hypotheses to match the original
test statement and because `lambdaMax_hasEigenvalue` needs it to justify
the "eigenvalue" reading of `lambdaMax`). -/
theorem eigenvalue_gap_stable_fixed_dim (A B : E →L[ℝ] E)
    (_hA : (A : E →ₗ[ℝ] E).IsSymmetric) (_hB : (B : E →ₗ[ℝ] E).IsSymmetric)
    (ε : ℝ) (hε : ‖A - B‖ < ε) :
    |lambdaMax A - lambdaMax B| ≤ ε :=
  (lambdaMax_lipschitz A B).trans hε.le

end YM3.FixedDimEigenvalueStability
