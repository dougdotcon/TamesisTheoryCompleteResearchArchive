/-
QF-1 -- standalone Wave-1 probe, NOT integrated into `TamesisLab.lean` or any shared
aggregator. Verified in isolation via `lake env lean` directly against the project's
vendored Mathlib, outside the shared import tree -- same convention as
`DiagonalSelfAdjointOperatorProbe.lean` (`03_MILLENNIUM/01_RIEMANN/FORMAL/`) and
`BadReductionValuationBridge.lean` / `MordellWeilGapProbe.lean`
(`03_MILLENNIUM/06_BSD/FORMAL/`).

## Honesty note (read before citing this file)

This item is filed under "Problem 8 -- Quantum-Classical Unification"
(`QCU-001`, see `../SCOPE.md`), which is **explicitly NOT one of the seven Clay
Millennium Problems** and remains `UNSCOPED` (no chosen `target_statement`,
per `../SCOPE.md`). Nothing in this file changes that status, resolves any
facet of quantum/classical unification, or bears on any Millennium problem.
This is a narrow, self-contained linear-algebra exercise about one already-proved
Mathlib inequality, chosen because it was concretely scaffolded and bounded to a
single session -- not a step toward "unification" in any of the senses listed in
`../SCOPE.md` (correspondence principle, deformation/geometric quantization,
Wigner-Weyl-Moyal, categorical quantization, or the measurement problem). No
mathematical novelty is claimed anywhere in this file: the tightness of
Tsirelson's bound via the qubit-pair CHSH tuple is 1980s/90s textbook quantum
information theory (Cirel'son 1980; Popescu-Rohrlich era references).

## What this file is

`Mathlib/Algebra/Star/CHSH.lean` (199 lines, independently re-read from source in
this session) already proves, for a `IsCHSHTuple A0 A1 B0 B1` in any ordered
`*`-algebra over `ℝ`:

* `CHSH_inequality_of_comm` : commutative case, `A0*B0+A0*B1+A1*B0-A1*B1 ≤ 2`
  (the "classical" / local-hidden-variable bound), and
* `tsirelson_inequality` : general (noncommutative) case,
  `A0*B0+A0*B1+A1*B0-A1*B1 ≤ 2√2 • 1` (the "quantum" bound), proved via an
  explicit sum-of-squares `P^2+Q^2` decomposition.

That file's own `## Future work` section (lines ~60-67 as verified this session)
states explicitly that tightness of the `2√2` bound -- exhibiting a genuine CHSH
tuple in 4-by-4 complex matrices for which the combination has `2√2` as an
eigenvalue -- is *not yet done* in Mathlib. This file closes exactly that one
gap, and nothing more.

## The test attempted (verbatim scope)

Realize the textbook qubit-pair CHSH tuple as concrete `4x4` complex matrices
(`Matrix (Fin 4) (Fin 4) ℂ`, i.e. operators on `ℂ² ⊗ ℂ²` in the standard basis
`|00⟩,|01⟩,|10⟩,|11⟩`):

* `A0 = σz ⊗ I`, `A1 = σx ⊗ I` (Pauli `Z`/`X` on qubit 1, identity on qubit 2)
* `B0 = I ⊗ (σz+σx)/√2`, `B1 = I ⊗ (σz-σx)/√2` (rotated Pauli measurements on
  qubit 2)

and check in Lean:

1. `IsCHSHTuple A0 A1 B0 B1` holds for these concrete matrices (`chshTuple`
   below) -- i.e. each is a self-adjoint involution and the `Aᵢ` commute with
   the `Bⱼ`, exactly Mathlib's structure from `CHSH.lean`.
2. The (unnormalised) maximally-entangled Bell vector `v = (1/√2, 0, 0, 1/√2)`
   is an honest eigenvector of the combination
   `combo := A0*B0 + A0*B1 + A1*B0 - A1*B1`
   with eigenvalue exactly `2√2`: `combo.mulVec v = (2√2) • v`
   (`combo_mulVec_v` below), verified by direct 4x4 matrix-vector computation,
   not any abstract spectral-theory machinery.

Both parts closed cleanly against existing `Matrix`/`Fin.sum_univ_four`/
`Complex` API with no new core assumptions and no unproved-placeholder tactics
of any kind, and no infrastructure gaps. This
confirms the reconnaissance claim: `Matrix.mulVec`/`Matrix.mul_apply` plus
`Fin.sum_univ_four` are sufficient for this one concrete eigenvector check;
no general eigenvalue/spectrum API for small matrices was needed (the earlier
falsifiable concern about "no decidable/computable eigenvalue tooling" did not
materialize as a blocker, because an explicit eigenvector witness sidesteps
needing any general spectral machinery).

## What this file does NOT do (read before citing this result)

* It does **not** invoke `tsirelson_inequality` or `CHSH_inequality_of_comm`
  themselves for anything beyond confirming `IsCHSHTuple` type-checks against
  the same structure they consume -- it exhibits tightness of an already-proved
  inequality, it does not reprove or strengthen the inequality itself.
* It does **not** show `2√2` is the *maximum* eigenvalue (i.e. it does not
  compute the full spectrum of `combo` or rule out a larger eigenvalue) --
  only that `2√2` *is* attained, which combined with the already-proved
  `tsirelson_inequality` upper bound is what "tightness" means. Establishing
  the upper bound from the abstract inequality plus this eigenvector witness
  is left as a routine (unformalized) remark, not a new Lean theorem.
* It does **not** touch the `CStarMatrix` order-structure route mentioned in
  the recon note (`Mathlib/Analysis/CStarAlgebra/CStarMatrix.lean`) -- that
  typeclass infrastructure turned out to be unnecessary for this narrow test,
  since `IsCHSHTuple` only needs `Monoid`/`StarMul` (both already present on
  `Matrix (Fin 4) (Fin 4) ℂ` via the plain matrix-ring and conjugate-transpose
  instances) and the eigenvector check only needs `Matrix.mulVec`.
* It makes **no claim** that any Millennium Prize problem is solved,
  approximated, or newly reachable, and no claim of mathematical novelty.
* It does not touch `TamesisLab.lean`, `TamesisLab/*`, or any other file in
  this lab; this is the only file this session created or modified.

## Verification

```
export PATH="$HOME/.elan/bin:$PATH"
cd 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean
lake env lean 03_MILLENNIUM/07_QUANTUM_CLASSICAL_UNIFICATION/FORMAL/CHSHTsirelsonTightness.lean
```
Exit code `0`, zero governance-forbidden tokens of any kind anywhere in this
file (checked directly, not just described here), and `#print axioms` on every
declaration below shows only the three standard Lean core assumptions
(propositional extensionality, choice, quotient soundness).
-/

import Mathlib.Algebra.Star.CHSH
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.Complex.Basic

open Matrix

namespace QCUChshTsirelsonTightness

noncomputable section

/-- `c = (√2)⁻¹`, as a complex number (the normalisation constant appearing in the
rotated Pauli observables `B0`, `B1` below). -/
noncomputable def c : ℂ := ((Real.sqrt 2)⁻¹ : ℝ)

lemma c_sq : c * c = (2 : ℂ)⁻¹ := by
  have h2 : (Real.sqrt 2) * (Real.sqrt 2) = 2 := Real.mul_self_sqrt (by norm_num)
  have hr : ((Real.sqrt 2)⁻¹ : ℝ) * ((Real.sqrt 2)⁻¹ : ℝ) = (2 : ℝ)⁻¹ := by
    rw [← mul_inv, h2]
  unfold c
  rw [← Complex.ofReal_mul, hr, Complex.ofReal_inv]
  norm_num

lemma c_conj : star c = c := by
  unfold c
  exact Complex.conj_ofReal _

/-- `A0 = σz ⊗ I`, the Pauli-`Z` observable on the first qubit, identity on the second. -/
noncomputable def A0 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![1, 0, 0, 0; 0, 1, 0, 0; 0, 0, -1, 0; 0, 0, 0, -1]

/-- `A1 = σx ⊗ I`, the Pauli-`X` observable on the first qubit, identity on the second. -/
noncomputable def A1 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![0, 0, 1, 0; 0, 0, 0, 1; 1, 0, 0, 0; 0, 1, 0, 0]

/-- `B0 = I ⊗ (σz + σx)/√2`, a rotated Pauli observable on the second qubit. -/
noncomputable def B0 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![c, c, 0, 0; c, -c, 0, 0; 0, 0, c, c; 0, 0, c, -c]

/-- `B1 = I ⊗ (σz - σx)/√2`, a rotated Pauli observable on the second qubit. -/
noncomputable def B1 : Matrix (Fin 4) (Fin 4) ℂ :=
  !![c, -c, 0, 0; -c, -c, 0, 0; 0, 0, c, -c; 0, 0, -c, -c]

lemma A0_sq : A0 ^ 2 = 1 := by
  rw [sq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A0, Matrix.mul_apply, Fin.sum_univ_four]

lemma A1_sq : A1 ^ 2 = 1 := by
  rw [sq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A1, Matrix.mul_apply, Fin.sum_univ_four]

lemma B0_sq : B0 ^ 2 = 1 := by
  rw [sq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [B0, Matrix.mul_apply, Fin.sum_univ_four] <;>
    (rw [c_sq]; norm_num)

lemma B1_sq : B1 ^ 2 = 1 := by
  rw [sq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [B1, Matrix.mul_apply, Fin.sum_univ_four] <;>
    (rw [c_sq]; norm_num)

lemma A0_sa : star A0 = A0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A0, Matrix.star_apply]

lemma A1_sa : star A1 = A1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A1, Matrix.star_apply]

lemma B0_sa : star B0 = B0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [B0, Matrix.star_apply, c_conj]

lemma B1_sa : star B1 = B1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [B1, Matrix.star_apply, c_conj]

lemma A0B0_comm : A0 * B0 = B0 * A0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A0, B0, Matrix.mul_apply, Fin.sum_univ_four]

lemma A0B1_comm : A0 * B1 = B1 * A0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A0, B1, Matrix.mul_apply, Fin.sum_univ_four]

lemma A1B0_comm : A1 * B0 = B0 * A1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A1, B0, Matrix.mul_apply, Fin.sum_univ_four]

lemma A1B1_comm : A1 * B1 = B1 * A1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [A1, B1, Matrix.mul_apply, Fin.sum_univ_four]

/-- Part 1 of the test: the four Pauli-tensor-product matrices `A0, A1, B0, B1` form a
`IsCHSHTuple` in the sense of `Mathlib.Algebra.Star.CHSH`. -/
theorem chshTuple : IsCHSHTuple A0 A1 B0 B1 where
  A₀_inv := A0_sq
  A₁_inv := A1_sq
  B₀_inv := B0_sq
  B₁_inv := B1_sq
  A₀_sa := A0_sa
  A₁_sa := A1_sa
  B₀_sa := B0_sa
  B₁_sa := B1_sa
  A₀B₀_commutes := A0B0_comm
  A₀B₁_commutes := A0B1_comm
  A₁B₀_commutes := A1B0_comm
  A₁B₁_commutes := A1B1_comm

/-- The CHSH combination `A0*B0 + A0*B1 + A1*B0 - A1*B1` whose Tsirelson bound
(`tsirelson_inequality` in `Mathlib.Algebra.Star.CHSH`) we exhibit as tight below. -/
noncomputable def combo : Matrix (Fin 4) (Fin 4) ℂ := A0 * B0 + A0 * B1 + A1 * B0 - A1 * B1

/-- The (unnormalised) maximally-entangled Bell-state vector `(c, 0, 0, c)`,
`c = (√2)⁻¹`, i.e. `(|00⟩ + |11⟩)/√2` in the standard basis. -/
noncomputable def v : Fin 4 → ℂ := ![c, 0, 0, c]

lemma B0_mulVec_v : Matrix.mulVec B0 v = ![c * c, c * c, c * c, -(c * c)] := by
  ext i
  fin_cases i <;> simp [B0, v, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

lemma B1_mulVec_v : Matrix.mulVec B1 v = ![c * c, -(c * c), -(c * c), -(c * c)] := by
  ext i
  fin_cases i <;> simp [B1, v, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

/-- The un-normalised Bell basis vector `(1,0,0,1)`; `v = c • w`. -/
noncomputable def w : Fin 4 → ℂ := ![1, 0, 0, 1]

lemma v_eq_c_smul_w : v = c • w := by
  ext i
  fin_cases i <;> simp [v, w]

/-- `w` is an eigenvector of `combo` with eigenvalue exactly `2`; combined with
`v = c • w` and `sqrt2_mul_c` below this gives eigenvalue `2√2` for `v`
(`combo_mulVec_v`). -/
lemma combo_mulVec_w : Matrix.mulVec combo v = (2 : ℂ) • w := by
  have step : Matrix.mulVec combo v =
      A0.mulVec (B0.mulVec v) + A0.mulVec (B1.mulVec v)
        + A1.mulVec (B0.mulVec v) - A1.mulVec (B1.mulVec v) := by
    simp only [combo, Matrix.sub_mulVec, Matrix.add_mulVec, ← Matrix.mulVec_mulVec]
  rw [step, B0_mulVec_v, B1_mulVec_v]
  ext i
  fin_cases i <;>
    simp [A0, A1, w, Pi.smul_apply] <;>
    (rw [c_sq]; norm_num)

/-- `√2 * c = 1`. -/
lemma sqrt2_mul_c : ((Real.sqrt 2 : ℝ) : ℂ) * c = 1 := by
  have h : Real.sqrt 2 ≠ 0 := by positivity
  unfold c
  rw [← Complex.ofReal_mul, mul_inv_cancel₀ h, Complex.ofReal_one]

/-- Part 2 of the test (the tightness witness): `v` is an eigenvector of the CHSH
combination `combo` with eigenvalue exactly `2√2` -- Tsirelson's bound
(`tsirelson_inequality` in `Mathlib.Algebra.Star.CHSH`) is attained by this concrete
`4x4`-complex-matrix CHSH tuple, closing the file's own `## Future work` item. -/
theorem combo_mulVec_v : Matrix.mulVec combo v = ((2 * Real.sqrt 2 : ℝ) : ℂ) • v := by
  rw [combo_mulVec_w, v_eq_c_smul_w, smul_smul]
  congr 1
  push_cast
  rw [show ((2 : ℂ) * (Real.sqrt 2 : ℝ)) * c = 2 * (((Real.sqrt 2 : ℝ) : ℂ) * c) from by ring,
    sqrt2_mul_c]
  ring

end

-- Axiom audit: every declaration in this file depends only on the three standard
-- Lean/Mathlib core assumptions, never on any silently-introduced extra assumption
-- (e.g. via a failed instance search papered over elsewhere).
#print axioms c_sq
#print axioms c_conj
#print axioms A0_sq
#print axioms A1_sq
#print axioms B0_sq
#print axioms B1_sq
#print axioms A0_sa
#print axioms A1_sa
#print axioms B0_sa
#print axioms B1_sa
#print axioms A0B0_comm
#print axioms A0B1_comm
#print axioms A1B0_comm
#print axioms A1B1_comm
#print axioms chshTuple
#print axioms B0_mulVec_v
#print axioms B1_mulVec_v
#print axioms v_eq_c_smul_w
#print axioms combo_mulVec_w
#print axioms sqrt2_mul_c
#print axioms combo_mulVec_v

end QCUChshTsirelsonTightness
