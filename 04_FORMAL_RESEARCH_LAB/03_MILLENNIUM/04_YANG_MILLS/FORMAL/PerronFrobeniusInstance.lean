/-
  YM-2 — Perron-Frobenius spectral-gap instance check (Wave-1 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-1 task instructions on build
  contention with 26 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; this file is intentionally free-standing, following
  the precedent of `InsufficiencyToyModel.lean` and `FiniteLatticeTransferGap.lean`
  in this same directory (the latter is the YM-1 sibling item of this same
  Wave-1 batch).

  MOTIVATION / RELATION TO YANG-MILLS. The rigorous finite-volume
  lattice-gauge notion of a mass gap (Glimm-Jaffe / Osterwalder-Seiler
  style: gap = -log(λ₂/λ₁) for a transfer matrix, with λ₁ simple by
  Perron-Frobenius) needs the Perron-Frobenius eigenvalue-gap theorem for
  primitive nonnegative matrices. Mathlib recently added the
  graph-theoretic groundwork for this notion —
  `Mathlib/LinearAlgebra/Matrix/Irreducible/Defs.lean`, the ONLY file in
  that directory (confirmed via `find` in this session), defines
  `Matrix.toQuiver`, `Matrix.IsIrreducible`, `Matrix.IsPrimitive`, and
  proves `Matrix.isIrreducible_iff_exists_pow_pos` and
  `Matrix.IsPrimitive.isIrreducible` (NOT `.to_IsIrreducible` — that
  string appears only in the module docstring's prose, a stale doc
  comment; the real declaration name, confirmed by direct read of the
  file this session, is `Matrix.IsPrimitive.isIrreducible` at line 182),
  citing Seneta 2006 and tagging the file's own `## Tags` line with
  `perron-frobenius`, marking it as an intentional forward reference.
  Confirmed by a whole-tree grep this session: outside that one file,
  Mathlib has ZERO occurrences of `PerronFrobenius`, `perron_frobenius`,
  or (case-insensitively) `perron` beyond unrelated "Perron integral" /
  "Perrone"-author false positives — the actual eigenvalue theorem
  (dominant real eigenvalue, simple, strictly larger in modulus than
  every other eigenvalue) is genuinely absent from Mathlib.

  THE TEST ATTEMPTED HERE (exactly the Wave-1-assigned falsifiable test,
  nothing broader — the GENERAL Perron-Frobenius eigenvalue-gap theorem is
  deliberately NOT attempted). Per the task instructions: pick one
  concrete 3×3 primitive nonnegative matrix, prove `Matrix.IsPrimitive`
  for it directly, then attempt strict eigenvalue dominance for THAT
  SPECIFIC matrix using only Mathlib's EXISTING charpoly/eigenvalue tools
  (`Mathlib/LinearAlgebra/Matrix/Charpoly/Eigs.lean`,
  `Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean`), with no new general
  machinery invented. The chosen matrix is the real symmetric
  `A = !![2,1,1;1,2,1;1,1,2]` (`= I + J` with `J` the all-ones 3×3
  matrix), all of whose entries are already strictly positive, so
  `IsPrimitive` holds trivially at exponent `k = 1` — this deliberately
  makes the primitivity half of the test as easy as the definitional API
  allows, putting the entire burden of the test on the eigenvalue half.

  RESULT: the eigenvalue half of the test SUCCEEDED using only existing
  tools, via a route that turned out to be more direct than the "charpoly
  as a polynomial in `R[X]`, factor it symbolically" route contemplated by
  the task prompt: `Matrix.eval_charpoly` (`Charpoly/Basic.lean`) reduces
  `A.charpoly.eval r` for a NUMERIC real `r` directly to
  `(Matrix.scalar _ r - A).det`, an ordinary real-number determinant, which
  `Matrix.det_fin_three` (`Determinant/Basic.lean`) then expands into a
  closed-form real cubic in `r` that `ring` confirms equals
  `(r - 4) * (r - 1) ^ 2`. Combined with `Matrix.mem_spectrum_iff_isRoot_charpoly`
  (`Charpoly/Eigs.lean`, the field-only direction), this gives a complete,
  closed-form characterization of the REAL spectrum of `A`:
  `r ∈ spectrum ℝ A ↔ r = 4 ∨ r = 1`, from which strict dominance
  (`∀ r ∈ spectrum ℝ A, r ≠ 4 → |r| < 4`) is immediate arithmetic. No
  polynomial-ring algebra over `ℝ[X]` was needed at any point — evaluating
  the characteristic polynomial at a point turns the whole problem into
  bare real-number linear algebra, which is well within existing `ring`/
  `nlinarith`/`det_fin_three` reach. Per the task's own falsifiable
  criterion ("if the specific-instance proof goes through with existing
  tools in a session, the general theorem is a realistic multi-session
  target"): OUTCOME = the specific-instance test CLOSES successfully;
  see the honest scope note below for exactly what is and is not thereby
  established.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-1 instructions). (1) This is the REAL spectrum only:
  `spectrum ℝ A`, i.e. real numbers `r` with `r • 1 - A` singular over
  `ℝ`. It does NOT separately verify that `A`, viewed as a complex matrix
  (`A.map (algebraMap ℝ ℂ)`), has no non-real complex eigenvalues — a
  fully general Perron-Frobenius statement is usually phrased over `ℂ`
  precisely because a general nonnegative matrix (not assumed symmetric)
  can have genuine complex eigenvalues, and the theorem's content is that
  even those are dominated in modulus. Because `A` here is symmetric,
  this is classically automatic (all eigenvalues of a real symmetric
  matrix are real), but that extra fact is NOT independently re-derived
  in this file; only the elementary real-spectrum computation is done.
  (2) Nothing here proves, or even states, the GENERAL Perron-Frobenius
  theorem for arbitrary irreducible/primitive matrices — no new lemma is
  added to the `Matrix.IsPrimitive`/`Matrix.IsIrreducible` API, and no
  attempt is made at simplicity-of-the-top-eigenvalue or
  positivity-of-the-eigenvector in the abstract case. This file is
  exactly what the task asked for: a single concrete instance check, nothing
  more. (3) Nothing here is about Yang-Mills, SU(N), lattice gauge
  actions, reflection positivity, the transfer matrix of any actual
  lattice theory, or the continuum limit; it says nothing about, and does
  not approximate, a solution to the Clay mass-gap problem. `A` is a
  hand-picked 3×3 rational symmetric matrix chosen to have an integer
  spectral gap, exactly analogous to the 2×2 matrix `M` in the YM-1
  sibling file `FiniteLatticeTransferGap.lean` in this directory. No
  mathematical novelty is claimed anywhere in this file: everything proved
  here (symmetric matrix with constant row sums has a positive
  eigenvector with eigenvalue equal to the row sum, dominating the rest of
  the spectrum) is classical and elementary.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`
  (toolchain pinned by `lean-toolchain` in that directory), in addition to
  compiling cleanly via `lake env lean` (see the file's own build log for
  the exact command/exit code, reported alongside this file).
-/
import Mathlib

open Matrix Polynomial

namespace YM2.PerronFrobeniusInstance

/-! ### Part 1 — the concrete matrix and its primitivity

`A = !![2,1,1;1,2,1;1,1,2] = I + J` (`J` the all-ones `3×3` matrix) is
real, symmetric, entrywise nonnegative, and in fact entrywise strictly
positive already at the first power (`k = 1`), so `Matrix.IsPrimitive A`
holds by the most direct possible instance of the algebraic definition in
`Mathlib.LinearAlgebra.Matrix.Irreducible.Defs`, with no quiver/path
reasoning needed. -/

/-- The concrete `3×3` test matrix: `A = I + J`, symmetric and entrywise
positive. -/
def A : Matrix (Fin 3) (Fin 3) ℝ := !![2, 1, 1; 1, 2, 1; 1, 1, 2]

/-- `A` is entrywise nonnegative (in fact strictly positive). -/
theorem A_nonneg (i j : Fin 3) : 0 ≤ A i j := by
  fin_cases i <;> fin_cases j <;> simp [A]

/-- `A` is entrywise strictly positive. -/
theorem A_pos (i j : Fin 3) : 0 < A i j := by
  fin_cases i <;> fin_cases j <;> simp [A]

/-- **`A` is primitive** (`Matrix.IsPrimitive`, `Irreducible/Defs.lean`),
witnessed directly at exponent `k = 1` since `A` itself is already
entrywise positive: no quiver/path search is needed for this particular
instance. -/
theorem A_isPrimitive : Matrix.IsPrimitive A := by
  refine ⟨A_nonneg, 1, one_pos, ?_⟩
  simpa using A_pos

/-- **`A` is irreducible** (`Matrix.IsIrreducible`), obtained for free from
primitivity via the sibling file's own
`Matrix.IsPrimitive.isIrreducible` — exercising that this Wave-1 target's
scaffolding is genuinely usable end-to-end on a concrete instance, not
just self-consistent in the abstract. -/
theorem A_isIrreducible : Matrix.IsIrreducible A := A_isPrimitive.isIrreducible

/-! ### Part 2 — the real spectrum of `A`, in closed form

The key step of the test: evaluate the characteristic polynomial of `A`
at an arbitrary real point `r` via `Matrix.eval_charpoly`
(`M.charpoly.eval t = (Matrix.scalar _ t - M).det`, `Charpoly/Basic.lean`),
then expand the resulting `3×3` determinant with `Matrix.det_fin_three`
(`Determinant/Basic.lean`) into ordinary real arithmetic — no polynomial
ring (`ℝ[X]`) manipulation is needed at any point. -/

/-- The characteristic polynomial of `A`, evaluated at any real `r`,
equals `(r - 4) * (r - 1) ^ 2` — a closed-form real-number identity,
checked by `Matrix.det_fin_three` plus `ring`. -/
theorem A_charpoly_eval (r : ℝ) : A.charpoly.eval r = (r - 4) * (r - 1) ^ 2 := by
  have h00 : A 0 0 = 2 := rfl
  have h01 : A 0 1 = 1 := rfl
  have h02 : A 0 2 = 1 := rfl
  have h10 : A 1 0 = 1 := rfl
  have h11 : A 1 1 = 2 := rfl
  have h12 : A 1 2 = 1 := rfl
  have h20 : A 2 0 = 1 := rfl
  have h21 : A 2 1 = 1 := rfl
  have h22 : A 2 2 = 2 := rfl
  rw [Matrix.eval_charpoly, Matrix.det_fin_three]
  simp [Matrix.sub_apply, Matrix.scalar_apply,
    h00, h01, h02, h10, h11, h12, h20, h21, h22]
  ring

/-- **Closed-form real spectrum of `A`.** A real number `r` is an
eigenvalue of `A` (i.e. `r ∈ spectrum ℝ A`, equivalently `r • 1 - A` is
singular over `ℝ`) if and only if `r = 4` or `r = 1`. Obtained by
combining `Matrix.mem_spectrum_iff_isRoot_charpoly` (`Charpoly/Eigs.lean`,
valid over any field) with `A_charpoly_eval` above. -/
theorem A_spectrum_real (r : ℝ) : r ∈ spectrum ℝ A ↔ r = 4 ∨ r = 1 := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly]
  show A.charpoly.eval r = 0 ↔ r = 4 ∨ r = 1
  rw [A_charpoly_eval]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h4 | h1
    · exact Or.inl (by linarith)
    · exact Or.inr (by nlinarith [sq_eq_zero_iff.mp h1])
  · rintro (rfl | rfl) <;> ring

/-! ### Part 3 — the two eigenvalues exhibited by explicit eigenvectors

Ties `A_spectrum_real` back to genuine eigenvectors, matching the
explicit-eigenvector style of the YM-1 sibling file
`FiniteLatticeTransferGap.lean`. -/

/-- `v₁ = (1,1,1)` is an eigenvector of `A` with eigenvalue `4` (the
constant row sum of `A`, as expected for `A = I + J`). -/
theorem A_eigen_four : A.mulVec ![1, 1, 1] = (4 : ℝ) • ![1, 1, 1] := by
  ext i
  fin_cases i <;>
    simp [A, Matrix.mulVec, dotProduct, Fin.sum_univ_three] <;> norm_num

/-- `v₂ = (1,-1,0)` is an eigenvector of `A` with eigenvalue `1`. -/
theorem A_eigen_one : A.mulVec ![1, -1, 0] = (1 : ℝ) • ![1, -1, 0] := by
  ext i
  fin_cases i <;>
    simp [A, Matrix.mulVec, dotProduct, Fin.sum_univ_three] <;> norm_num

/-- `4 ∈ spectrum ℝ A`, confirmed both abstractly (via `A_spectrum_real`)
and concretely (via the exhibited eigenvector `A_eigen_four`). -/
theorem A_four_mem_spectrum : (4 : ℝ) ∈ spectrum ℝ A := (A_spectrum_real 4).mpr (Or.inl rfl)

/-- `1 ∈ spectrum ℝ A`, confirmed both abstractly (via `A_spectrum_real`)
and concretely (via the exhibited eigenvector `A_eigen_one`). -/
theorem A_one_mem_spectrum : (1 : ℝ) ∈ spectrum ℝ A := (A_spectrum_real 1).mpr (Or.inr rfl)

/-! ### Part 4 — the main result: strict Perron-Frobenius-style dominance
for this one instance -/

/-- **Main result (YM-2 instance test).** Every real eigenvalue of the
primitive matrix `A` other than the top eigenvalue `4` is strictly
smaller than `4` in absolute value — the Perron-Frobenius eigenvalue-gap
conclusion, verified for this ONE concrete `3×3` primitive matrix using
only Mathlib's existing charpoly/spectrum/determinant tools, with no new
general machinery. This is a single-instance fact, not the general
theorem for arbitrary irreducible/primitive matrices — see the header
comment for exactly what remains open. -/
theorem A_perron_gap_instance :
    ∀ r ∈ spectrum ℝ A, r ≠ 4 → |r| < 4 := by
  intro r hr hne
  rw [A_spectrum_real] at hr
  rcases hr with h4 | h1
  · exact absurd h4 hne
  · rw [h1]; norm_num

/-- The gap itself, as a bare positive real number: `4 - 1 = 3 > 0`,
matching the elementary `2×2` gap `3 - 1 = 2` of the YM-1 sibling
`M_spectral_gap` in `FiniteLatticeTransferGap.lean`. -/
theorem A_spectral_gap : (4 : ℝ) - 1 = 3 ∧ (0 : ℝ) < 3 := ⟨by norm_num, by norm_num⟩

end YM2.PerronFrobeniusInstance
