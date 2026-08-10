/-
  WAVE2-YM-1-YM-3 — operator-norm bound probe for `L2Operator` composition
  of YM-1 / YM-3 (Wave-2 batch item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-2 task instructions on
  build contention with 19 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of
  `InsufficiencyToyModel.lean`, `FiniteLatticeTransferGap.lean` (YM-1),
  and `FixedDimEigenvalueStability.lean` (YM-3) in this same directory.

  EXACT TASK ATTEMPTED (per `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`,
  candidate `YM-1+YM-3`, revised test). Nothing broader than this was
  attempted:
    Sonda 1: `open scoped Matrix.Norms.L2Operator`; verify that
      `Matrix.toEuclideanCLM (!![2,1;1,2.1] - !![2,1;1,2])` unifies with
      `(E →L[R] E)`, and that `Matrix.l2_opNorm_toEuclideanCLM` rewrites
      `‖toEuclideanCLM (M1 - M2)‖` to `‖M1 - M2‖` via `map_sub`.
    Sonda 2 (the real question): find/prove a numeric bound on that
      L2Operator norm, either via `ContinuousLinearMap.opNorm_le_bound`,
      or via an entrywise/Frobenius-vs-op-norm comparison lemma.

  RELATION TO WAVE-1 YM-1 / YM-3 (read, NOT imported). This file reuses
  the *values* of `YM1.TransferGap.M` (`FiniteLatticeTransferGap.lean`,
  `M := !![2,1;1,2]`) and the *ambient space* of
  `YM3.FixedDimEigenvalueStability.E` (`FixedDimEigenvalueStability.lean`,
  `E := EuclideanSpace ℝ (Fin 2)`) as `M2` / `E` below, to match the plan
  text exactly. Those two Wave-1 files live outside the `TamesisLab`
  Lake source root (under `03_MILLENNIUM/...`, not `05_FORMAL/lean/
  TamesisLab/...`) and, per their own header comments, are deliberately
  free-standing, single-file-typechecked artifacts, not Lake library
  modules -- there is no `import`-able module path to them without
  editing shared Lake configuration (`lakefile.toml`), which the Wave-2
  instructions explicitly forbid touching. This file therefore
  RE-DECLARES the same numeric matrix `M2` locally (byte-for-byte
  identical RHS to `YM1.TransferGap.M`) rather than importing it, exactly
  as every other Wave-1/Wave-2 file in this directory does for its own
  numeric instances. `YM3.FixedDimEigenvalueStability.lambdaMax_lipschitz`
  itself is cited only as motivation in the plan text, not as a lemma
  this file's Sonda 1/Sonda 2 statements literally invoke (see the plan's
  own "Teste revisado" wording); reproducing that theorem's ~60-line
  Rayleigh-quotient proof here would be well outside "attempt EXACTLY
  this test, nothing broader" -- it is NOT attempted in this file.

  MATHLIB TOOLS USED (verified present by direct read of
  `Mathlib/Analysis/CStarAlgebra/Matrix.lean` in the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`, in addition to compiling
  cleanly via `lake env lean`):
    - `Matrix.toEuclideanCLM`            (L102) -- the star-algebra
      equivalence `Matrix n n 𝕜 ≃⋆ₐ[𝕜] (EuclideanSpace 𝕜 n →L[𝕜]
      EuclideanSpace 𝕜 n)`, the "bridge" the plan's adversarial review
      confirmed already exists (no missing infrastructure here).
    - `Matrix.l2_opNorm_toEuclideanCLM`  (L228) -- `‖toEuclideanCLM A‖ =
      ‖A‖`, `rfl`, valid under the SCOPED `NormedAddCommGroup (Matrix n n
      𝕜)` instance in `Matrix.Norms.L2Operator` (distinct from the
      default `linftyOp`/Frobenius instances, confirmed genuinely absent
      of a bridge by the plan's review).
    - `map_sub` (generic, via the `AddEquiv`/`RingEquiv` layer of
      `StarAlgEquiv`) -- rewrites `toEuclideanCLM (M1 - M2)` to
      `toEuclideanCLM M1 - toEuclideanCLM M2`.
    - `Matrix.l2_opNorm_diagonal`        (L232) -- `‖diagonal v‖ = ‖v‖`
      (with `‖v‖` the ordinary Pi *sup* norm on `n → 𝕜`, per that
      lemma's own proof, which cites `pi_norm_le_iff_of_nonneg` /
      `norm_le_pi_norm`) -- the entrywise-vs-L2Operator-norm comparison
      lemma this file uses to close Sonda 2, for the DIAGONAL special
      case (see "WHAT THIS FILE DOES NOT DO" below for the scope of
      this).
    - `pi_norm_le_iff_of_nonneg`, `norm_le_pi_norm` (`Analysis/Normed/
      Group/Constructions.lean`) -- used to compute the Pi sup norm of
      the concrete vector `![0, 1/10]` exactly.

  WHAT THIS FILE DOES / THE FALSIFIABLE RESULT. `M1 := !![2,1;1,2.1]`,
  `M2 := !![2,1;1,2]` (the latter matching `YM1.TransferGap.M` exactly),
  both in `Matrix (Fin 2) (Fin 2) ℝ`. Sonda 1 is confirmed in full:
  `diffCLM := Matrix.toEuclideanCLM (M1 - M2) : E →L[ℝ] E` type-checks
  (the "unifies with `E →L[R] E`" claim), and `sonda1_bridge` rewrites
  `‖toEuclideanCLM M1 - toEuclideanCLM M2‖` to `‖M1 - M2‖` via `map_sub`
  followed by `l2_opNorm_toEuclideanCLM`, exactly as specified. Sonda 2
  is answered for this concrete instance: `M1 - M2` happens to be the
  DIAGONAL matrix `diagonal ![0, 1/10]` (`diff_eq_diagonal`), so
  `Matrix.l2_opNorm_diagonal` gives the EXACT value (not merely a bound)
  `‖M1 - M2‖ = 1/10` (`sonda2_numeric_norm`), hence also
  `‖diffCLM‖ = 1/10` (`sonda2_diffCLM_norm`, via `l2_opNorm_toEuclideanCLM`
  directly) -- a numeric operator-norm value for the L2Operator-scoped
  norm of this concrete operator difference, which is in particular a
  numeric BOUND (`‖diffCLM‖ ≤ 1/10`, immediate corollary), closing the
  falsifiable test as stated.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, per Wave-2
  instructions). The numeric closure above is special-cased: it works
  BECAUSE `M1 - M2` happens to be diagonal for this specific choice of
  `M1`/`M2` (only the `(1,1)` entry differs). `Matrix.l2_opNorm_diagonal`
  is a comparison lemma between the L2Operator norm and the entrywise Pi
  sup-norm of the diagonal vector ONLY for diagonal matrices; a whole-tree
  grep of the vendored Mathlib snapshot for a GENERAL entrywise-vs-
  L2Operator or Frobenius-vs-L2Operator comparison lemma (for arbitrary,
  non-diagonal matrices) found nothing beyond what is cited above, which
  matches the plan's own review finding ("nenhuma lema de comparacao
  entrywise/Frobenius-vs-L2Operator foi encontrada"). Neither
  `ContinuousLinearMap.opNorm_le_bound` nor a general comparison lemma
  was needed or used here, precisely because the concrete numeric
  instance chosen degenerates to the diagonal case; a genuinely
  off-diagonal difference matrix (e.g. differing in the `(0,1)`/`(1,0)`
  entries) would still need one of those two routes and is NOT attempted
  here. This file does not connect its numeric bound to
  `YM3.FixedDimEigenvalueStability.lambdaMax_lipschitz` (see the
  "RELATION TO WAVE-1" note above for why not) -- doing so would require
  either an importable copy of that theorem or reproducing its proof,
  both out of scope for this narrow probe. This file says nothing about
  Yang-Mills, nothing about SU(N) or any gauge theory, nothing about the
  continuum limit, and claims no mathematical novelty (norm computations
  for a diagonal matrix, and the star-algebra-equivalence norm-transport
  identity, are classical and elementary).

  Every Mathlib name used below was checked by direct grep against the
  vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

open scoped Matrix.Norms.L2Operator

namespace YM13.L2OperatorNormProbe

/-- The fixed finite-dimensional real inner product space, matching
`YM3.FixedDimEigenvalueStability.E` (re-declared locally; see the header
comment on why this file does not `import` that free-standing file). -/
abbrev E := EuclideanSpace ℝ (Fin 2)

/-- The perturbed matrix `M1`: `YM1.TransferGap.M` with its `(1,1)` entry
bumped from `2` to `2.1`. -/
def M1 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2.1]

/-- `M2`, byte-for-byte identical to `YM1.TransferGap.M` (re-declared
locally; see the header comment on why this file does not `import` that
free-standing file). -/
def M2 : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

/-! ### Sonda 1 — the bridge (`toEuclideanCLM` / `l2_opNorm_toEuclideanCLM`)

Both halves of Sonda 1, exactly as specified in the plan. -/

/-- **Sonda 1, part a.** `Matrix.toEuclideanCLM (M1 - M2)` unifies with
the type `E →L[ℝ] E` -- i.e. this `def` elaborates at all, which is the
literal content of "unifica com `(E →L[R] E)`". -/
noncomputable def diffCLM : E →L[ℝ] E :=
  Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) (M1 - M2)

/-- **Sonda 1, part b.** `Matrix.l2_opNorm_toEuclideanCLM` rewrites
`‖toEuclideanCLM M1 - toEuclideanCLM M2‖` to `‖M1 - M2‖`, via `map_sub`
(`toEuclideanCLM (M1 - M2) = toEuclideanCLM M1 - toEuclideanCLM M2`,
since `toEuclideanCLM` is a star-algebra equivalence, hence additive)
followed by `l2_opNorm_toEuclideanCLM` itself. This is the "bridge"
connecting the `E →L[ℝ] E` operator-norm difference (the type used by
`YM3.FixedDimEigenvalueStability.lambdaMax_lipschitz`) to the
`Matrix.Norms.L2Operator`-scoped matrix norm of the entry-wise
difference. -/
theorem sonda1_bridge :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M1 -
        Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2) M2‖ = ‖M1 - M2‖ := by
  rw [← map_sub (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin 2))]
  exact Matrix.l2_opNorm_toEuclideanCLM (M1 - M2)

/-! ### Sonda 2 — the numeric bound

The real question. `M1 - M2` happens to be diagonal for this concrete
instance, which lets `Matrix.l2_opNorm_diagonal` (an entrywise-vs-
L2Operator-norm comparison lemma, for diagonal matrices) close this
exactly rather than merely bound it. See the header comment for why this
does NOT generalize to arbitrary (non-diagonal) matrix differences. -/

/-- `M1 - M2` is the diagonal matrix `diagonal ![0, 1/10]` (only the
`(1,1)` entry of `M1`/`M2` differs, by `2.1 - 2 = 1/10`). -/
theorem diff_eq_diagonal : M1 - M2 = Matrix.diagonal ![(0 : ℝ), 1 / 10] := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [M1, M2]

/-- The Pi *sup*-norm (the norm `Matrix.l2_opNorm_diagonal` is stated
against) of the concrete vector `![0, 1/10]` is exactly `1/10`. -/
theorem pi_norm_vec : ‖(![(0 : ℝ), 1 / 10] : Fin 2 → ℝ)‖ = 1 / 10 := by
  apply le_antisymm
  · rw [pi_norm_le_iff_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 10)]
    intro i
    fin_cases i <;> norm_num
  · have := norm_le_pi_norm (![(0 : ℝ), 1 / 10] : Fin 2 → ℝ) 1
    simpa using this

/-- **Sonda 2, closed exactly (stronger than "a bound").** The
`Matrix.Norms.L2Operator`-scoped operator norm of `M1 - M2` is exactly
`1/10`, via `diff_eq_diagonal` + `Matrix.l2_opNorm_diagonal` +
`pi_norm_vec`. In particular `‖M1 - M2‖ ≤ 1/10` (the numeric bound the
falsifiable test asked for). -/
theorem sonda2_numeric_norm : ‖M1 - M2‖ = 1 / 10 := by
  rw [diff_eq_diagonal, Matrix.l2_opNorm_diagonal]
  exact pi_norm_vec

/-- **Main result (WAVE2-YM-1-YM-3).** Combining Sonda 1's bridge with
Sonda 2's exact value: the operator norm (in `E →L[ℝ] E`, the type used
by `YM3.FixedDimEigenvalueStability.lambdaMax_lipschitz`) of the
difference of the two continuous linear maps induced by `M1` and `M2` is
exactly `1/10`, hence in particular bounded by `1/10`. This is the
falsifiable numeric claim Sonda 1 + Sonda 2 together were testing. -/
theorem sonda2_diffCLM_norm : ‖diffCLM‖ = 1 / 10 := by
  unfold diffCLM
  rw [Matrix.l2_opNorm_toEuclideanCLM]
  exact sonda2_numeric_norm

/-- Immediate corollary stated as an explicit bound (rather than an
equality), to match the falsifiable test's literal "bound numerico"
wording. -/
theorem sonda2_diffCLM_bound : ‖diffCLM‖ ≤ 1 / 10 :=
  sonda2_diffCLM_norm.le

end YM13.L2OperatorNormProbe
