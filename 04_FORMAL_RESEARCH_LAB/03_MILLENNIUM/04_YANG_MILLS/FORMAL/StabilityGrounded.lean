/-
  YM-STABILITY-GROUNDED — grounding `lambdaMax (toEuclideanCLM M2) = 3` by
  connecting to the abstract spectrum `{1, 3}` from YM-1-CONNECT (Wave-3
  batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` -- see the Wave-3 task instructions on build
  contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every other
  Wave-1/Wave-2/Wave-3 file in this directory
  (`InsufficiencyToyModel.lean`, `FiniteLatticeTransferGap.lean`,
  `FixedDimEigenvalueStability.lean`, `TransferGapSpectrumCharpoly.lean`,
  `L2OperatorNormProbe.lean`).

  EXACT TASK ATTEMPTED (per `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md`,
  candidate `YM-STABILITY-GROUNDED`). Nothing broader than this was
  attempted: chain `ContinuousLinearMap.spectrum_eq` (under `CompleteSpace`
  via `FiniteDimensional.complete`) + `AlgEquiv.spectrum_eq` (via the
  `AlgEquivClass` instance that `StarAlgEquiv`/`toEuclideanCLM` carries) +
  `M2_spectrum_eq` (the YM-1-CONNECT closed-form fact `spectrum ℝ M2 =
  {1, 3}`, reproduced below) to obtain
  `spectrum ℝ (toEuclideanCLM M2 : E →L[ℝ] E) = {1, 3}`; then combine
  `Module.End.hasEigenvalue_iff_mem_spectrum` with an explicit-eigenvector
  Rayleigh-quotient computation from `M2_eigen_three` to conclude
  `lambdaMax (toEuclideanCLM M2) = 3`.

  RELATION TO WAVE-1 / WAVE-2 (all read, NONE imported/modified). This file
  reuses, BYTE-FOR-BYTE REPRODUCED (never imported -- see the "BUILD-SYSTEM
  NOTE" below for why, identical reasoning to every prior Wave-2/Wave-3
  sibling that faces the same free-standing-file constraint):
    - `E := EuclideanSpace ℝ (Fin 2)` and
      `lambdaMax (T : E →L[ℝ] E) := ⨆ x : {x : E // x ≠ 0}, T.rayleighQuotient x`
      and `lambdaMax_hasEigenvalue`, verbatim from
      `FixedDimEigenvalueStability.lean` (Wave-1, YM-3, lines 106-144).
    - `M2 := !![2, 1; 1, 2]`, verbatim from `L2OperatorNormProbe.lean`
      (Wave-2, `YM13.L2OperatorNormProbe.M2`, matching
      `YM1.TransferGap.M` exactly).
    - `M2_isHermitian`, `M2_charpoly_eval`, `M2_spectrum_real`,
      `M2_spectrum_eq` (the closed-form real spectrum `{1, 3}`), verbatim
      from `TransferGapSpectrumCharpoly.lean` (Wave-2, YM-1-CONNECT,
      `YM1.TransferGapSpectrum.M`/`M_isHermitian`/`M_charpoly_eval`/
      `M_spectrum_real`/`M_spectrum_eq`).
    - `M2_eigen_three` (the explicit eigenvector `(1,1)` with eigenvalue
      `3`), verbatim from `FiniteLatticeTransferGap.lean` (Wave-1, YM-1,
      `YM1.TransferGap.M_eigen_three`).
  None of these four Wave-1/Wave-2 files is touched or imported; each is
  read-only source material reproduced here under the same free-standing
  Lake-module-path constraint every prior file in this line has already
  documented.

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, toolchain
  `leanprover/lean4:v4.33.0-rc1`, in addition to compiling cleanly via
  `lake env lean`):
    - `AlgEquiv.spectrum_eq`   (`Mathlib/Algebra/Algebra/Spectrum/Basic.lean:429`)
      -- `spectrum R (f a) = spectrum R a` for any `f : F` with
      `[EquivLike F A B] [AlgEquivClass F R A B]`. Applies to
      `Matrix.toEuclideanCLM` because `A ≃⋆ₐ[R] B` (`StarAlgEquiv`) carries
      a `NonUnitalAlgEquivClass` instance (`Mathlib/Algebra/Star/
      StarAlgHom.lean:704`), and there is a further (lower-priority)
      instance converting `[EquivLike F A B] [NonUnitalAlgEquivClass F R A
      B]` into `AlgEquivClass F R A B` when `A`, `B` are `Semiring`+
      `Algebra R` (`Mathlib/Algebra/Star/StarAlgHom.lean:661-663`), which
      both `Matrix (Fin 2) (Fin 2) ℝ` and `E →L[ℝ] E` genuinely are.
    - `ContinuousLinearMap.spectrum_eq` (`Mathlib/Analysis/Normed/
      Operator/Banach.lean:486`) -- `spectrum 𝕜 f = spectrum 𝕜 (f :
      Module.End 𝕜 E)` for `f : E →L[𝕜] E`, under `[CompleteSpace E]`.
      `E := EuclideanSpace ℝ (Fin 2)` is finite-dimensional, so
      `CompleteSpace E` is found automatically by typeclass search via
      `FiniteDimensional.complete` (`Mathlib/Topology/Algebra/Module/
      FiniteDimension.lean:502`) -- no explicit `haveI` was needed in this
      file (Lean's instance search resolves it silently); the name is
      cited here only to document which instance is actually doing the
      work, matching the falsifiable test's own wording.
    - `Module.End.hasEigenvalue_iff_mem_spectrum` (`Mathlib/LinearAlgebra/
      Eigenspace/Basic.lean:507`) -- `f.HasEigenvalue μ ↔ μ ∈ spectrum K f`
      for `f : End K V`, `[FiniteDimensional K V]`.
    - `Matrix.coe_toEuclideanCLM_eq_toEuclideanLin`,
      `Matrix.toEuclideanCLM_toLp`, `Matrix.isSymmetric_toEuclideanLin_iff`
      (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:109`,`114`;
      `Mathlib/Analysis/Matrix/Hermitian.lean:56`) -- the bridge lemmas
      needed to (a) transport `M2_isHermitian` into
      `(toEuclideanCLM M2 : E →ₗ[ℝ] E).IsSymmetric`, the hypothesis
      `lambdaMax_hasEigenvalue` needs, and (b) compute
      `toEuclideanCLM M2` applied to the concrete vector `(1,1)` in terms
      of `M2.mulVec ![1,1]`.
    - `real_inner_smul_left`, `real_inner_self_eq_norm_sq`
      (`Mathlib/Analysis/InnerProductSpace/Basic.lean:108`,`396`) --
      elementary real-inner-product identities used to evaluate the
      Rayleigh quotient at the explicit eigenvector exactly.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT. `toEuclideanCLM_M2_spectrum_eq`
  establishes `spectrum ℝ (toEuclideanCLM M2 : E →L[ℝ] E) = {1, 3}` exactly
  as the test's first half specifies (`AlgEquiv.spectrum_eq` +
  `M2_spectrum_eq`). `lambdaMax_grounded_eq_three` is the main result: it
  combines that spectrum fact (via `ContinuousLinearMap.spectrum_eq` +
  `Module.End.hasEigenvalue_iff_mem_spectrum`, pinning
  `lambdaMax (toEuclideanCLM M2)` down to the two-element set `{1, 3}`)
  with an explicit lower bound `lambdaMax (toEuclideanCLM M2) ≥ 3` (the
  Rayleigh quotient at the eigenvector `(1,1)` from `M2_eigen_three`
  computes to exactly `3`, and `lambdaMax` is a supremum over all nonzero
  vectors, hence dominates it) to rule out the other spectral value `1`
  and conclude `lambdaMax (toEuclideanCLM M2) = 3` on the nose. This is
  the honest closure of the "still missing" item flagged in
  `L2OperatorNormProbe.lean`'s own header ("This file does not connect its
  numeric bound to `YM3.FixedDimEigenvalueStability.lambdaMax_lipschitz`")
  in the one specific direction the Wave-3 test asks for: not the norm
  bound itself, but grounding `lambdaMax` of this same concrete operator
  to an exact numeric eigenvalue via the abstract spectrum.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, per Wave-3
  instructions). This file does not touch `lambdaMax_lipschitz` or the
  `‖M1 - M2‖ = 1/10` numeric bound from `L2OperatorNormProbe.lean` at all
  -- it grounds `lambdaMax` at the single fixed point `toEuclideanCLM M2`,
  not the Lipschitz stability statement combining two nearby operators.
  It says nothing about Yang-Mills, nothing about SU(N) or any gauge
  theory, nothing about the continuum/lattice-spacing-to-zero limit, and
  claims no mathematical novelty -- identifying the Rayleigh-quotient
  supremum of a self-adjoint operator with a concretely known eigenvalue,
  once its full (two-element) spectrum is known in closed form and a
  matching eigenvector Rayleigh-quotient lower bound is exhibited, is
  classical and elementary linear algebra.

  BUILD-SYSTEM NOTE (why `E`/`lambdaMax`/`M2`/etc. are reproduced below
  instead of imported). Identical situation and identical reasoning to
  `TransferGapSpectrumCharpoly.lean`'s own header note: all four Wave-1/
  Wave-2 source files above are, by their own header comments,
  deliberately free-standing and NOT registered in `TamesisLab.lean` --
  they live outside the `lean_lib` module graph declared in
  `lakefile.toml` and have no built `.olean`, so `import`ing them by
  module path is not possible without editing shared Lake configuration,
  which the Wave-3 task instructions explicitly forbid touching. The only
  way to reuse these declarations under that constraint is to reproduce
  them verbatim, exactly as `TransferGapSpectrumCharpoly.lean` (Wave-2)
  and `L2OperatorNormProbe.lean` (Wave-2) already do for their own
  dependencies.

  Every Mathlib name used below was checked by direct grep/read against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`
  (toolchain pinned by `lean-toolchain` in that directory), in addition to
  compiling cleanly via `lake env lean` (see the file's own build log for
  the exact command/exit code, reported alongside this file).
-/
import Mathlib

open Matrix WithLp

namespace YMStabilityGrounded

/-! ### Part 0a — verbatim reproduction of `YM3.FixedDimEigenvalueStability`
(`E`, `lambdaMax`, `lambdaMax_hasEigenvalue`), copied byte-for-byte from
`FixedDimEigenvalueStability.lean` lines 106-144. -/

/-- The fixed finite-dimensional real inner product space (verbatim from
`YM3.FixedDimEigenvalueStability.E`). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- "Candidate top eigenvalue" of a continuous linear self-map of the fixed
space `E` (verbatim from `YM3.FixedDimEigenvalueStability.lambdaMax`). -/
noncomputable def lambdaMax (T : E →L[ℝ] E) : ℝ :=
  ⨆ x : { x : E // x ≠ 0 }, T.rayleighQuotient (x : E)

/-- For symmetric `T`, `lambdaMax T` genuinely IS an eigenvalue of `T`
(verbatim from `YM3.FixedDimEigenvalueStability.lambdaMax_hasEigenvalue`). -/
theorem lambdaMax_hasEigenvalue (T : E →L[ℝ] E)
    (hT : (T : E →ₗ[ℝ] E).IsSymmetric) :
    Module.End.HasEigenvalue (T : E →ₗ[ℝ] E) (lambdaMax T) := by
  have h := hT.hasEigenvalue_iSup_of_finiteDimensional
  simpa [lambdaMax, ContinuousLinearMap.rayleighQuotient,
    ContinuousLinearMap.reApplyInnerSelf_apply] using h

/-! ### Part 0b — verbatim reproduction of `YM1.TransferGapSpectrum`
(`M`, `M_isHermitian`, `M_charpoly_eval`, `M_spectrum_real`,
`M_spectrum_eq`), copied byte-for-byte from
`TransferGapSpectrumCharpoly.lean` lines 104-157, renamed `M` → `M2` to
match the falsifiable test's own naming (matching
`YM13.L2OperatorNormProbe.M2`, which is itself byte-identical to
`YM1.TransferGap.M`). -/

/-- The toy 2×2 "transfer matrix" (verbatim value from `YM1.TransferGap.M`
/ `YM1.TransferGapSpectrum.M` / `YM13.L2OperatorNormProbe.M2`). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-- `M2` is Hermitian (verbatim from `YM1.TransferGapSpectrum.M_isHermitian`). -/
theorem M2_isHermitian : M2.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M2, Matrix.conjTranspose_apply]

/-- The characteristic polynomial of `M2`, evaluated at any real `r`, equals
`(r - 3) * (r - 1)` (verbatim from `YM1.TransferGapSpectrum.M_charpoly_eval`). -/
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
(verbatim from `YM1.TransferGapSpectrum.M_spectrum_real`). -/
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

/-- **YM-1-CONNECT's main result, set form.** The real spectrum of `M2` is
exactly `{1, 3}` (verbatim from `YM1.TransferGapSpectrum.M_spectrum_eq`).
This is the abstract spectrum this Wave-3 item connects `lambdaMax` to. -/
theorem M2_spectrum_eq : spectrum ℝ M2 = ({1, 3} : Set ℝ) := by
  ext r
  rw [M2_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

/-! ### Part 0c — verbatim reproduction of `YM1.TransferGap.M_eigen_three`,
copied byte-for-byte from `FiniteLatticeTransferGap.lean` lines 160-164,
renamed `M` → `M2`. -/

/-- `v₁ = (1,1)` is an eigenvector of `M2` with eigenvalue `3` (verbatim
from `YM1.TransferGap.M_eigen_three`). -/
theorem M2_eigen_three : M2.mulVec ![1, 1] = (3 : ℝ) • ![1, 1] := by
  ext i
  fin_cases i <;>
    simp [M2, Matrix.mulVec, dotProduct, Fin.sum_univ_two] <;> norm_num

/-! ### Part 1 — the falsifiable test's first half: the abstract spectrum
of `toEuclideanCLM M2 : E →L[ℝ] E`, via `AlgEquiv.spectrum_eq` +
`M2_spectrum_eq`. -/

/-- **Falsifiable test, part 1.** `AlgEquiv.spectrum_eq` (`Matrix.toEuclideanCLM`
is a `StarAlgEquiv`, hence carries an `AlgEquivClass` instance transporting
spectra along it) combined with `M2_spectrum_eq` gives the closed-form
abstract spectrum of `toEuclideanCLM M2`, viewed as a continuous linear
endomorphism of `E`. -/
theorem toEuclideanCLM_M2_spectrum_eq :
    spectrum ℝ (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      = ({1, 3} : Set ℝ) := by
  rw [AlgEquiv.spectrum_eq (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2)) M2]
  exact M2_spectrum_eq

/-- Transported to the `Module.End ℝ E` (mere-linear-map) spectrum via
`ContinuousLinearMap.spectrum_eq`, which requires `[CompleteSpace E]` --
found automatically here since `E` is finite-dimensional
(`FiniteDimensional.complete`). -/
theorem toEuclideanCLM_M2_endSpectrum_eq :
    spectrum ℝ ((Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →L[ℝ] E)
      : Module.End ℝ E) = ({1, 3} : Set ℝ) := by
  rw [← ContinuousLinearMap.spectrum_eq]
  exact toEuclideanCLM_M2_spectrum_eq

/-! ### Part 2 — `(toEuclideanCLM M2 : E →ₗ[ℝ] E).IsSymmetric`, transported
from `M2_isHermitian` via `Matrix.isSymmetric_toEuclideanLin_iff`. Needed
to invoke `lambdaMax_hasEigenvalue`. -/

theorem toEuclideanCLM_M2_isSymmetric :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2 : E →ₗ[ℝ] E).IsSymmetric := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr M2_isHermitian

/-! ### Part 3 — `lambdaMax (toEuclideanCLM M2) ∈ {1, 3}`, via
`Module.End.hasEigenvalue_iff_mem_spectrum` (`lambdaMax_hasEigenvalue`
already gives `HasEigenvalue`, hence `mem_spectrum`; combined with Part 1
this pins `lambdaMax` down to `{1, 3}`). -/

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

/-! ### Part 4 — `lambdaMax (toEuclideanCLM M2) ≥ 3`, via the explicit
eigenvector `v = (1,1)` (`M2_eigen_three`): its Rayleigh quotient computes
to exactly `3`, and `lambdaMax` is a supremum over all nonzero vectors. -/

/-- The vector `v = (1,1) ∈ E`, the same eigenvector as `M2_eigen_three`,
transported into `EuclideanSpace ℝ (Fin 2)` via `WithLp.toLp`. -/
noncomputable def v : E := WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)

theorem v_ne_zero : v ≠ 0 := by
  intro h
  have h0 : (WithLp.equiv 2 (Fin 2 → ℝ)) v 0 = (WithLp.equiv 2 (Fin 2 → ℝ)) (0 : E) 0 := by
    rw [h]
  simp [v, WithLp.equiv] at h0

/-- `toEuclideanCLM M2` applied to `v` equals `(3:ℝ) • v`, via
`Matrix.toEuclideanCLM_toLp` (transporting `M2.mulVec` along `toLp`) and
`M2_eigen_three`. -/
theorem toEuclideanCLM_M2_apply_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) v = (3 : ℝ) • v := by
  show (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2)
      (WithLp.toLp 2 (![1, 1] : Fin 2 → ℝ)) = (3 : ℝ) • v
  rw [Matrix.toEuclideanCLM_toLp, M2_eigen_three]
  rfl

/-- The Rayleigh quotient of `toEuclideanCLM M2` at the explicit eigenvector
`v` is exactly `3` -- the elementary computation `⟪3•v, v⟫ / ‖v‖^2 = 3 *
‖v‖^2 / ‖v‖^2 = 3` (`v ≠ 0` so `‖v‖^2 ≠ 0`), via `real_inner_smul_left` and
`real_inner_self_eq_norm_sq`. -/
theorem toEuclideanCLM_M2_rayleighQuotient_v :
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2).rayleighQuotient v = 3 := by
  have hvnorm : ‖v‖ ≠ 0 := norm_ne_zero_iff.mpr v_ne_zero
  rw [ContinuousLinearMap.rayleighQuotient, ContinuousLinearMap.reApplyInnerSelf_apply,
    toEuclideanCLM_M2_apply_v, real_inner_smul_left, real_inner_self_eq_norm_sq]
  rw [RCLike.re_to_real]
  field_simp

/-- **Falsifiable test, part 2 (lower bound half).** `lambdaMax
(toEuclideanCLM M2) ≥ 3`, since `lambdaMax` is the supremum of the
Rayleigh quotient over all nonzero vectors, and the Rayleigh quotient at
`v` is exactly `3`. -/
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

/-! ### Part 5 — the main result: combining Parts 3 and 4 rules out `1`
(since `1 < 3 ≤ lambdaMax`), pinning `lambdaMax (toEuclideanCLM M2)` down
to exactly `3`. -/

/-- **Main result (YM-STABILITY-GROUNDED).** `lambdaMax (toEuclideanCLM
M2) = 3` exactly, grounded via the abstract spectrum `{1, 3}` of
`toEuclideanCLM M2` (`toEuclideanCLM_M2_spectrum_eq`, itself obtained from
`M2_spectrum_eq`, the closed-form spectrum of `M2` from YM-1-CONNECT) and
the explicit eigenvector lower bound `lambdaMax ≥ 3`
(`lambdaMax_ge_three`, from `M2_eigen_three`). This is the falsifiable
claim as stated: `lambdaMax` of this concrete Wave-1/Wave-2 operator is
not merely known to lie in an abstractly-characterized two-point spectrum,
but is pinned down to the specific value `3`. -/
theorem lambdaMax_grounded_eq_three :
    lambdaMax (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2) = 3 := by
  rcases lambdaMax_mem_one_three with h1 | h3
  · exfalso
    have := lambdaMax_ge_three
    rw [h1] at this
    linarith
  · exact h3

#print axioms YMStabilityGrounded.M2_isHermitian
#print axioms YMStabilityGrounded.M2_charpoly_eval
#print axioms YMStabilityGrounded.M2_spectrum_real
#print axioms YMStabilityGrounded.M2_spectrum_eq
#print axioms YMStabilityGrounded.M2_eigen_three
#print axioms YMStabilityGrounded.toEuclideanCLM_M2_spectrum_eq
#print axioms YMStabilityGrounded.toEuclideanCLM_M2_endSpectrum_eq
#print axioms YMStabilityGrounded.toEuclideanCLM_M2_isSymmetric
#print axioms YMStabilityGrounded.lambdaMax_mem_one_three
#print axioms YMStabilityGrounded.v_ne_zero
#print axioms YMStabilityGrounded.toEuclideanCLM_M2_apply_v
#print axioms YMStabilityGrounded.toEuclideanCLM_M2_rayleighQuotient_v
#print axioms YMStabilityGrounded.lambdaMax_ge_three
#print axioms YMStabilityGrounded.lambdaMax_grounded_eq_three

end YMStabilityGrounded
