/-
  YM-2-SIMPLE — root multiplicities of `A.charpoly` via `Polynomial.funext`
  decomposition (Wave-2 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-2 task instructions on build
  contention with 19 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; this file is intentionally free-standing, following
  the precedent of `InsufficiencyToyModel.lean` and its Wave-1/Wave-2
  siblings in this same directory.

  MOTIVATION / RELATION TO WAVE-1. `PerronFrobeniusInstance.lean` (Wave-1,
  item YM-2) proves, for the concrete `3×3` real symmetric matrix
  `A := !![2,1,1;1,2,1;1,1,2]` (`= I + J`), the closed-form real-number
  identity `A.charpoly.eval r = (r - 4) * (r - 1) ^ 2` for every `r : ℝ`
  (`A_charpoly_eval`), and from it the pointwise spectrum description
  `r ∈ spectrum ℝ A ↔ r = 4 ∨ r = 1` (`A_spectrum_real`). That file does
  NOT compute anything about `A.charpoly` as an element of the polynomial
  ring `ℝ[X]` itself — only its evaluations at individual points. This
  Wave-2 item is EXACTLY the falsifiable test of taking that one step
  further: via `Polynomial.funext` (an `Infinite R` polynomial is
  determined by its evaluations), upgrade the pointwise identity to an
  honest polynomial-ring equality
  `A.charpoly = (X - C 4) * (X - C 1) ^ 2`, then decompose
  `Polynomial.rootMultiplicity` across the product using
  `Polynomial.rootMultiplicity_mul` (for the nonzero product),
  `Polynomial.rootMultiplicity_X_sub_C_pow` /
  `Polynomial.rootMultiplicity_X_sub_C_self` (for the matching linear
  factor) and `Polynomial.rootMultiplicity_eq_zero` (for the
  non-matching factor, which contributes `0`), to conclude
  `A.charpoly.rootMultiplicity 4 = 1` and `A.charpoly.rootMultiplicity 1 = 2`
  — i.e. the exact algebraic-multiplicity statement that `A_charpoly_eval`
  only implies indirectly (as the multiplicity of a root of the associated
  real cubic), never previously stated in `Polynomial.rootMultiplicity`
  terms in the Wave-1 file.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-2 instructions). Nothing here is about the continuum limit, about
  SU(N) or any actual gauge group, about the lattice-gauge partition
  function, about reflection positivity, or about any physical transfer
  matrix built from a genuine lattice action — `A` is the same hand-picked
  toy `3×3` matrix as in the Wave-1 YM-2 file, unchanged. This file adds
  a polynomial-ring-level (as opposed to pointwise-evaluation-level)
  description of the SAME already-known charpoly of the SAME concrete
  matrix; it does not add any new eigenvalue, does not relate algebraic
  multiplicity to geometric multiplicity (dimension of the eigenspace),
  does not touch minimal polynomials or Jordan-block structure, and
  claims no mathematical novelty — that a `3×3` polynomial with three
  known real roots (with multiplicity) over an integral domain factors as
  a product of linear factors matching those roots and multiplicities is
  classical and, given the cited Mathlib lemmas, a routine translation
  exercise. It says nothing about Yang-Mills, does not approximate a
  solution to the Clay mass-gap problem.

  BUILD-SYSTEM NOTE (why `A` and `A_charpoly_eval` are reproduced below
  instead of imported). The Wave-1 sibling file `PerronFrobeniusInstance.lean`
  is, by its OWN header comment, deliberately "free-standing" and "NOT
  registered in `TamesisLab.lean`" — it lives outside the `lean_lib` module
  graph declared in `lakefile.toml` (which only declares
  `[[lean_lib]] name = "TamesisLab"`, rooted at the `TamesisLab/` source
  directory) and has no built `.olean`. The Wave-2 sibling file
  `TransferGapSpectrumCharpoly.lean` in this same directory confirmed
  directly in its own session that `lake env lean` on a file that tries
  `import «03_MILLENNIUM».«04_YANG_MILLS».FORMAL.PerronFrobeniusInstance`
  (analogous import path) fails with `unknown module prefix '03_MILLENNIUM'`
  — the Wave-1 file simply is not on Lean's module search path, by the
  same free-standing convention it documents about itself. Per the Wave-2
  task instructions ("do NOT touch any file outside your own new file(s)"),
  this file cannot register `PerronFrobeniusInstance.lean` into the
  library graph either. The only way to reuse `A` and its charpoly
  evaluation under this constraint is to reproduce the definition and its
  proof VERBATIM (byte-identical `def`/`theorem` text, copied directly
  from `PerronFrobeniusInstance.lean` lines 128 and 165-178) rather than
  inventing a different matrix — this is not a redeclaration of a new
  object, it is the same concrete `3×3` matrix and the same
  charpoly-evaluation proof, reproduced because the lab's own Wave-1
  single-file convention leaves no other route to it. (This mirrors
  exactly the precedent set by `TransferGapSpectrumCharpoly.lean` for its
  own Wave-1 dependency `YM1.TransferGap.M`.)

  Every Mathlib name used below was checked by direct grep/read against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`
  (toolchain pinned by `lean-toolchain` in that directory):
    - `Matrix.eval_charpoly`                 (`Charpoly/Basic.lean:135`)
    - `Matrix.det_fin_three`                 (`Determinant/Basic.lean`)
    - `Polynomial.funext`                    (`Algebra/Polynomial/Roots.lean:459`,
                                               requires `[Infinite R]`, `ℝ` qualifies)
    - `Polynomial.X_sub_C_ne_zero`           (`Algebra/Polynomial/Degree/Operations.lean:773`)
    - `Polynomial.rootMultiplicity_mul`      (`Algebra/Polynomial/RingDivision.lean:291`,
                                               requires `p * q ≠ 0`)
    - `Polynomial.rootMultiplicity_X_sub_C_pow`
                                              (`Algebra/Polynomial/RingDivision.lean:162`)
    - `Polynomial.rootMultiplicity_X_sub_C_self`
                                              (`Algebra/Polynomial/RingDivision.lean:167`)
    - `Polynomial.rootMultiplicity_eq_zero`  (`Algebra/Polynomial/Div.lean:636`,
                                               takes `¬ IsRoot p x`)
  in addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this file).
-/
import Mathlib

open Matrix Polynomial

namespace YM2.RootMultiplicities

/-! ### Part 0 — verbatim reproduction of `YM2.PerronFrobeniusInstance.A`
and `A_charpoly_eval`

Copied byte-for-byte from `PerronFrobeniusInstance.lean` (Wave-1, item
YM-2), for the build-system reason explained in the header comment above.
`A` and `A_charpoly_eval` here are definitionally and propositionally the
exact same matrix and the exact same evaluated-charpoly identity as in the
Wave-1 file — this section adds nothing new. -/

/-- The concrete `3×3` test matrix (verbatim from `YM2.PerronFrobeniusInstance.A`):
`A = I + J`, symmetric and entrywise positive. -/
def A : Matrix (Fin 3) (Fin 3) ℝ := !![2, 1, 1; 1, 2, 1; 1, 1, 2]

/-- The characteristic polynomial of `A`, evaluated at any real `r`, equals
`(r - 4) * (r - 1) ^ 2` (verbatim from `YM2.PerronFrobeniusInstance.A_charpoly_eval`). -/
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

/-! ### Part 1 — upgrading the pointwise identity to a polynomial-ring
equality, via `Polynomial.funext`

`Polynomial.funext` (`[Infinite R] : (∀ r, p.eval r = q.eval r) → p = q`)
applies here because `ℝ` is an `Infinite` type; combined with
`A_charpoly_eval` above and the evaluation lemmas for `X - C a` and its
powers, this promotes the closed-form real-number identity to an actual
equality of polynomials in `ℝ[X]`. -/

/-- **`A.charpoly` as a product of linear factors.** `A.charpoly` equals
`(X - C 4) * (X - C 1) ^ 2` as an element of `ℝ[X]` — not merely at each
evaluation point, obtained from `A_charpoly_eval` via `Polynomial.funext`
since `ℝ` is infinite. -/
theorem A_charpoly_eq : A.charpoly = (X - C 4) * (X - C 1) ^ 2 := by
  apply Polynomial.funext
  intro r
  rw [A_charpoly_eval]
  simp

/-- The product `(X - C 4) * (X - C 1) ^ 2` is nonzero in `ℝ[X]`, since
`ℝ[X]` is an integral domain and each factor (`X - C a ≠ 0` via
`Polynomial.X_sub_C_ne_zero`) is nonzero. Feeds `Polynomial.rootMultiplicity_mul`
below, which requires the product to be nonzero. -/
theorem A_charpoly_factored_ne_zero :
    (X - C (4 : ℝ)) * (X - C (1 : ℝ)) ^ 2 ≠ 0 :=
  mul_ne_zero (Polynomial.X_sub_C_ne_zero 4)
    (pow_ne_zero 2 (Polynomial.X_sub_C_ne_zero 1))

/-! ### Part 2 — root multiplicities of `A.charpoly`, via
`Polynomial.rootMultiplicity_mul` decomposition

For each of the two roots `4` and `1`, split `A.charpoly`'s
`rootMultiplicity` across the product `A_charpoly_eq` exhibits, using
`Polynomial.rootMultiplicity_mul` (valid since the product is nonzero,
`A_charpoly_factored_ne_zero`). The factor whose root matches the point
contributes its exact multiplicity via `rootMultiplicity_X_sub_C_self` /
`rootMultiplicity_X_sub_C_pow`; the non-matching factor contributes `0`
via `Polynomial.rootMultiplicity_eq_zero` (since the point is not one of
its roots). -/

/-- **Main result, first root (YM-2-SIMPLE).** The root multiplicity of
`4` in `A.charpoly` is `1` — i.e. `4` is a SIMPLE root of `A`'s
characteristic polynomial, matching the top Perron-Frobenius eigenvalue
of `A` from `PerronFrobeniusInstance.lean` (Wave-1) being simple. -/
theorem A_charpoly_rootMultiplicity_four :
    A.charpoly.rootMultiplicity 4 = 1 := by
  rw [A_charpoly_eq, Polynomial.rootMultiplicity_mul A_charpoly_factored_ne_zero]
  have h1 : (X - C (4 : ℝ)).rootMultiplicity 4 = 1 :=
    Polynomial.rootMultiplicity_X_sub_C_self
  have h2 : ((X - C (1 : ℝ)) ^ 2).rootMultiplicity 4 = 0 := by
    apply Polynomial.rootMultiplicity_eq_zero
    show ¬ ((X - C (1 : ℝ)) ^ 2).eval 4 = 0
    simp only [Polynomial.eval_pow, Polynomial.eval_sub, Polynomial.eval_X, Polynomial.eval_C]
    norm_num
  rw [h1, h2]

/-- **Main result, second root (YM-2-SIMPLE).** The root multiplicity of
`1` in `A.charpoly` is `2` — i.e. `1` is a DOUBLE root of `A`'s
characteristic polynomial, matching the two-dimensional eigenspace of the
non-top Perron-Frobenius eigenvalue of `A` from `PerronFrobeniusInstance.lean`
(Wave-1). -/
theorem A_charpoly_rootMultiplicity_one :
    A.charpoly.rootMultiplicity 1 = 2 := by
  rw [A_charpoly_eq, Polynomial.rootMultiplicity_mul A_charpoly_factored_ne_zero]
  have h1 : (X - C (4 : ℝ)).rootMultiplicity 1 = 0 := by
    apply Polynomial.rootMultiplicity_eq_zero
    show ¬ (X - C (4 : ℝ)).eval 1 = 0
    simp only [Polynomial.eval_sub, Polynomial.eval_X, Polynomial.eval_C]
    norm_num
  have h2 : ((X - C (1 : ℝ)) ^ 2).rootMultiplicity 1 = 2 :=
    Polynomial.rootMultiplicity_X_sub_C_pow 1 2
  rw [h1, h2]

#print axioms YM2.RootMultiplicities.A_charpoly_eval
#print axioms YM2.RootMultiplicities.A_charpoly_eq
#print axioms YM2.RootMultiplicities.A_charpoly_factored_ne_zero
#print axioms YM2.RootMultiplicities.A_charpoly_rootMultiplicity_four
#print axioms YM2.RootMultiplicities.A_charpoly_rootMultiplicity_one

end YM2.RootMultiplicities
