/-
  YM-1-CONNECT — closed-form real spectrum of the YM-1 toy transfer matrix
  `M`, via characteristic polynomial (Wave-2 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-2 task instructions on build
  contention with 19 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; this file is intentionally free-standing, following
  the precedent of `InsufficiencyToyModel.lean` and its Wave-1 siblings in
  this same directory. This file does NOT modify any Wave-1 file; it only
  imports/reuses declarations from `FiniteLatticeTransferGap.lean` by
  fully-qualified name (`YM1.TransferGap.M`, `YM1.TransferGap.M_isHermitian`).

  MOTIVATION / RELATION TO WAVE-1. `FiniteLatticeTransferGap.lean` (Wave-1,
  item YM-1) proves the toy 2×2 transfer matrix `M := !![2,1;1,2]` has
  eigenvalues `3` and `1` via EXPLICIT EIGENVECTORS, deliberately bypassing
  Mathlib's abstract `Matrix.IsHermitian.eigenvalues` API (that file's
  header explains why: `eigenvalues` is `noncomputable`/choice-based, built
  through `eigenvalues₀`/`Fintype.equivOfCardEq`, not something one can
  "just evaluate" on a concrete matrix without translation work). Separately,
  `PerronFrobeniusInstance.lean` (Wave-1, item YM-2) shows a DIFFERENT route
  works cleanly on a concrete matrix: evaluate the characteristic polynomial
  pointwise via `Matrix.eval_charpoly` + `Matrix.det_fin_three`, then apply
  `Matrix.mem_spectrum_iff_isRoot_charpoly` to get a closed-form description
  of `spectrum ℝ A` (that file's `A_spectrum_real`). This Wave-2 item is
  EXACTLY the falsifiable test of connecting those two Wave-1 results:
  mirror `A_spectrum_real`'s charpoly route (using `Matrix.det_fin_two`
  instead of `det_fin_three`, since `M` is `2×2`) to compute
  `spectrum ℝ YM1.TransferGap.M = {1, 3}` in closed form, then use the
  translation lemma `Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues`
  (`Mathlib/Analysis/Matrix/Spectrum.lean`) to conclude
  `Set.range YM1.TransferGap.M_isHermitian.eigenvalues = {1, 3}` — i.e. to
  finally connect Wave-1's concrete, explicit-eigenvector treatment of `M`
  to Mathlib's own abstract `IsHermitian.eigenvalues` function, closing the
  exact gap the Wave-1 YM-1 file's header flagged as "not attempted in this
  pass" (the `eigenvalues_eq`/`charpoly_eq` stretch goal).

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-2 instructions). Nothing here is about the continuum limit, about
  SU(N) or any actual gauge group, about the lattice-gauge partition
  function, about reflection positivity, or about any physical transfer
  matrix built from a genuine lattice action — `M` is the same hand-picked
  toy `2×2` matrix as in the Wave-1 YM-1 file, unchanged. This file
  connects two existing finite-dimensional linear-algebra descriptions of
  the SAME concrete matrix's spectrum (explicit eigenvectors vs.
  charpoly-roots vs. Mathlib's abstract `eigenvalues` indexing function);
  it does not add any new eigenvalue, does not weaken or reinterpret
  Wave-1's result, and claims no mathematical novelty — the underlying fact
  (a `2×2` real symmetric matrix's spectrum is exactly the root set of its
  characteristic polynomial, and Mathlib's `IsHermitian.eigenvalues`
  indexing enumerates precisely that root set) is classical and, given the
  cited Mathlib lemmas, a routine translation exercise. It says nothing
  about Yang-Mills, does not approximate a solution to the Clay mass-gap
  problem.

  BUILD-SYSTEM NOTE (why `M` is reproduced below instead of imported). The
  Wave-1 sibling file `FiniteLatticeTransferGap.lean` is, by its OWN header
  comment, deliberately "free-standing" and "NOT registered in
  `TamesisLab.lean`" — it lives outside the `lean_lib` module graph declared
  in `lakefile.toml` (which only declares `[[lean_lib]] name = "TamesisLab"`,
  rooted at the `TamesisLab/` source directory) and has no built `.olean`.
  Confirmed directly in this session: `lake env lean` on a file that tries
  `import «03_MILLENNIUM».«04_YANG_MILLS».FORMAL.FiniteLatticeTransferGap`
  fails with `unknown module prefix '03_MILLENNIUM'` — the Wave-1 file
  simply is not on Lean's module search path, by the same free-standing
  convention it documents about itself. Per the Wave-2 task instructions
  ("do NOT touch any file outside your own new file(s)"), this file cannot
  register `FiniteLatticeTransferGap.lean` into the library graph either.
  The only way to reuse `M` under this constraint is to reproduce its
  definition VERBATIM (byte-identical `def`/`theorem` text, copied directly
  from `FiniteLatticeTransferGap.lean` lines 129-139) rather than inventing
  a different matrix — this is not a redeclaration of a new object, it is
  the same concrete `2×2` matrix and the same Hermitian-ness proof,
  reproduced because the lab's own Wave-1 single-file convention leaves no
  other route to it.

  Every Mathlib name used below was checked by direct grep/read against the
  vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`
  (toolchain pinned by `lean-toolchain` in that directory):
    - `Matrix.eval_charpoly`                    (`Charpoly/Basic.lean:135`)
    - `Matrix.det_fin_two`                      (`Determinant/Basic.lean:807`)
    - `Matrix.mem_spectrum_iff_isRoot_charpoly`  (`Charpoly/Eigs.lean:80`)
    - `Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues`
                                                  (`Analysis/Matrix/Spectrum.lean:211`)
  in addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this file).
-/
import Mathlib

open Matrix

namespace YM1.TransferGapSpectrum

/-! ### Part 0 — verbatim reproduction of `YM1.TransferGap.M`

Copied byte-for-byte from `FiniteLatticeTransferGap.lean` (Wave-1, item
YM-1), for the build-system reason explained in the header comment above.
`M` and `M_isHermitian` here are definitionally and propositionally the
exact same matrix and the exact same proof as in the Wave-1 file — this
section adds nothing new. -/

/-- The toy 2×2 "transfer matrix" (verbatim from `YM1.TransferGap.M`). -/
def M : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-- `M` is Hermitian (verbatim from `YM1.TransferGap.M_isHermitian`). -/
theorem M_isHermitian : M.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [M, Matrix.conjTranspose_apply]

/-! ### Part 1 — the characteristic polynomial of `M`, evaluated in closed form

Mirrors `PerronFrobeniusInstance.lean`'s `A_charpoly_eval`, using
`Matrix.det_fin_two` (the `2×2` sibling of that file's `det_fin_three`)
since `M` is `2×2` rather than `3×3`. -/

/-- The characteristic polynomial of `M`, evaluated at any real `r`, equals
`(r - 3) * (r - 1)` — a closed-form real-number identity, checked by
`Matrix.det_fin_two` plus `ring`. Matches `YM1.TransferGap`'s
`M_gap_matches_quadratic_formula`'s roots `3` and `1`. -/
theorem M_charpoly_eval (r : ℝ) :
    M.charpoly.eval r = (r - 3) * (r - 1) := by
  have h00 : M 0 0 = 2 := rfl
  have h01 : M 0 1 = 1 := rfl
  have h10 : M 1 0 = 1 := rfl
  have h11 : M 1 1 = 2 := rfl
  rw [Matrix.eval_charpoly, Matrix.det_fin_two]
  simp [Matrix.sub_apply, Matrix.scalar_apply, h00, h01, h10, h11]
  ring

/-! ### Part 2 — the real spectrum of `M`, in closed form -/

/-- **Closed-form real spectrum of `M` (pointwise characterization).** A
real number `r` is an eigenvalue of `M` (i.e. `r ∈ spectrum ℝ M`) iff
`r = 3` or `r = 1`. Obtained by combining
`Matrix.mem_spectrum_iff_isRoot_charpoly` with `M_charpoly_eval` above,
exactly mirroring `PerronFrobeniusInstance.lean`'s `A_spectrum_real`. -/
theorem M_spectrum_real (r : ℝ) :
    r ∈ spectrum ℝ M ↔ r = 3 ∨ r = 1 := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly]
  show M.charpoly.eval r = 0 ↔ r = 3 ∨ r = 1
  rw [M_charpoly_eval]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h3 | h1
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)
  · rintro (rfl | rfl) <;> ring

/-- **Main result (YM-1-CONNECT), set form.** The real spectrum of `M` is
exactly `{1, 3}`, as a `Set ℝ`. Immediate reformulation of
`M_spectrum_real` as a set equality via `Set.ext`. -/
theorem M_spectrum_eq : spectrum ℝ M = ({1, 3} : Set ℝ) := by
  ext r
  rw [M_spectrum_real]
  simp [Set.mem_insert_iff, Set.mem_singleton_iff, or_comm]

/-! ### Part 3 — connecting to Mathlib's abstract `IsHermitian.eigenvalues`

The falsifiable test's second half: transport `M_spectrum_eq` along
`Matrix.IsHermitian.spectrum_real_eq_range_eigenvalues`
(`spectrum ℝ A = Set.range hA.eigenvalues`, for `A` Hermitian over an
`RCLike` field — here `ℝ` itself, `RCLike ℝ` is a standing Mathlib
instance) to describe the RANGE of Mathlib's own abstract, choice-based
`eigenvalues : Fin 2 → ℝ` indexing function for `M`, using the verbatim
reproduction `M_isHermitian` from Part 0 above (propositionally the exact
same Hermitian-ness fact as `YM1.TransferGap.M_isHermitian` in the Wave-1
sibling file). -/

/-- **Main result (YM-1-CONNECT).** The range of Mathlib's abstract
`IsHermitian.eigenvalues` indexing function for `M` (built via
`M_isHermitian : M.IsHermitian`) is exactly `{1, 3}` — connecting Wave-1's
concrete explicit-eigenvector treatment of `M` to Mathlib's own
eigenvalue-enumeration API, via the characteristic polynomial as the
bridge. This is the precise Wave-2 test target:
`Set.range M_isHermitian.eigenvalues = {1, 3}`. -/
theorem M_range_eigenvalues_eq :
    Set.range M_isHermitian.eigenvalues = ({1, 3} : Set ℝ) := by
  rw [← M_isHermitian.spectrum_real_eq_range_eigenvalues]
  exact M_spectrum_eq

#print axioms YM1.TransferGapSpectrum.M_isHermitian
#print axioms YM1.TransferGapSpectrum.M_charpoly_eval
#print axioms YM1.TransferGapSpectrum.M_spectrum_real
#print axioms YM1.TransferGapSpectrum.M_spectrum_eq
#print axioms YM1.TransferGapSpectrum.M_range_eigenvalues_eq

end YM1.TransferGapSpectrum
