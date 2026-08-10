/-
  SHARED-2B — `(A.map (algebraMap R C)).IsHermitian` and spectrum inclusion
  in `range(algebraMap R C)`, for the concrete YM-2 matrix (Wave-2 batch,
  shared-infrastructure item).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-2 task instructions on build
  contention with 19 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1 or other Wave-2 file. It only *reads* the Wave-1 file
  `03_MILLENNIUM/04_YANG_MILLS/FORMAL/PerronFrobeniusInstance.lean`.

  BUILD-SYSTEM NOTE (why `A` is reproduced below instead of imported,
  confirmed directly this session). `PerronFrobeniusInstance.lean` is, by
  its own header, deliberately free-standing and NOT registered in
  `TamesisLab.lean` — it lives outside the `[[lean_lib]] name =
  "TamesisLab"` module graph declared in `lakefile.toml` and has no built
  `.olean`; `lake env lean` on a file importing
  `«03_MILLENNIUM».«04_YANG_MILLS».FORMAL.PerronFrobeniusInstance` fails
  with `unknown module prefix '03_MILLENNIUM'` (exactly the same failure
  already documented by the Wave-2 sibling
  `04_YANG_MILLS/FORMAL/TransferGapSpectrumCharpoly.lean` for the
  analogous Wave-1 file `FiniteLatticeTransferGap.lean`). Per the Wave-2
  task instructions ("do NOT touch any file outside your own new
  file(s)"), this file cannot register `PerronFrobeniusInstance.lean` into
  the library graph either. The only way to reuse `A` under this
  constraint is to reproduce its definition VERBATIM (byte-identical `def`
  text, copied directly from `PerronFrobeniusInstance.lean`'s own `A`)
  rather than inventing a different matrix — this is not a redeclaration
  of a new object, it is the same concrete `3×3` matrix, reproduced
  because the lab's own Wave-1 single-file convention leaves no other
  route to it. (`A_isHermitian` below is NOT reproduced from anywhere — it
  does not exist in `PerronFrobeniusInstance.lean`; it is proved fresh
  here, since that fact is exactly this item's own gap to close.)

  MOTIVATION / RELATION TO WAVE-1 YM-2. The Wave-1 file
  `PerronFrobeniusInstance.lean` computes the REAL spectrum of the
  concrete `3×3` real symmetric matrix
  `A := !![2,1,1;1,2,1;1,1,2] : Matrix (Fin 3) (Fin 3) ℝ`
  in closed form (`spectrum ℝ A = {1, 4}`), and its own header explicitly
  flags what it does NOT do:

    "It does NOT separately verify that `A`, viewed as a complex matrix
    (`A.map (algebraMap ℝ ℂ)`), has no non-real complex eigenvalues — [...]
    that extra fact is NOT independently re-derived in this file."

  This Wave-2 item is EXACTLY the falsifiable test that closes that
  flagged gap, and nothing broader: (1) prove
  `(A.map (algebraMap ℝ ℂ)).IsHermitian` via `Matrix.isHermitian_iff_isSymm`
  (or, as it worked out below, directly via `Matrix.IsHermitian.map` using
  the semiconjugacy of `algebraMap ℝ ℂ` with `star` — see the ROUTE note
  below for exactly why `isHermitian_iff_isSymm` itself was NOT the tool
  actually used), then (2) apply
  `Matrix.IsHermitian.spectrum_eq_image_range`
  (`Mathlib/Analysis/Matrix/Spectrum.lean`) to conclude
  `spectrum ℂ (A.map (algebraMap ℝ ℂ)) ⊆ Set.range (algebraMap ℝ ℂ)`, i.e.
  every complex eigenvalue of the complexified matrix is in fact real
  (lies in the range of the real-to-complex embedding).

  ROUTE ACTUALLY TAKEN (adversarial-test statement said
  "isHermitian_iff_isSymm + IsHermitian.map"; here is the precise shape
  that compiles). `Matrix.IsHermitian.map` has signature
  `(h : A.IsHermitian) (f : α → β) (hf : Function.Semiconj f star star) :
  (A.map f).IsHermitian` (`Mathlib/LinearAlgebra/Matrix/Hermitian.lean`).
  So the two ingredients needed are: (a) `A.IsHermitian` itself (proved
  directly below by `ext`/`fin_cases`/`simp`, exactly the same style as
  the Wave-1 YM-1 sibling's `M_isHermitian` in
  `FiniteLatticeTransferGap.lean` — `isHermitian_iff_isSymm` was not
  separately invoked because `IsHermitian.ext`/direct `ext` unification is
  already the most direct route for a literal `!![...]` matrix, matching
  the existing lab precedent); and (b)
  `Function.Semiconj (algebraMap ℝ ℂ) star star`, i.e.
  `∀ x, algebraMap ℝ ℂ (star x) = star (algebraMap ℝ ℂ x)`, which is
  EXACTLY the general lemma `algebraMap_star_comm`
  (`Mathlib/Algebra/Star/Module.lean`, requiring
  `[CommSemiring R] [StarRing R] [Semiring A] [StarMul A] [Algebra R A]
  [StarModule R A]` — all five instances are available for `R := ℝ`,
  `A := ℂ` in the vendored Mathlib snapshot, confirmed by direct grep this
  session: `StarModule ℝ ℂ` is `instance` at
  `Mathlib/LinearAlgebra/Complex/Module.lean:107`, and ℝ/ℂ already carry
  the ambient `CommSemiring`/`StarRing`/`Semiring`/`StarMul`/`Algebra`
  instances used throughout the lab). Combining (a)+(b) via
  `IsHermitian.map` gives `(A.map (algebraMap ℝ ℂ)).IsHermitian` with no
  detour through `isHermitian_iff_isSymm` needed — the semiconjugacy proof
  obligation the adversarial test anticipated ("semiconjugacao trivial")
  is discharged in one line by the pre-existing general Mathlib lemma,
  exactly as hoped.

  For step (2), `Matrix.IsHermitian.spectrum_eq_image_range` states
  `spectrum 𝕜 A = RCLike.ofReal '' Set.range hA.eigenvalues` for
  `[RCLike 𝕜]`; specialized at `𝕜 := ℂ` this gives the complex spectrum of
  `A.map (algebraMap ℝ ℂ)` as the image of a set under `RCLike.ofReal`,
  hence (unfolding the image membership pointwise) every element of the
  spectrum is `RCLike.ofReal r` for some real `r`. The identification
  `RCLike.ofReal = algebraMap ℝ ℂ` used to restate `RCLike.ofReal r` as
  `algebraMap ℝ ℂ r` (matching the task's literal "range(R)" phrasing) is
  the existing Mathlib simp lemma
  `RCLike.algebraMap_eq_ofReal : ⇑(algebraMap ℝ K) = ofReal`
  (`Mathlib/Analysis/RCLike/Basic.lean`). NOTE: a direct whole-goal
  `rw [A_complex_isHermitian.spectrum_eq_image_range, RCLike.algebraMap_eq_ofReal]`
  does NOT work here — Lean rejects it with "motive is not type correct",
  because `algebraMap ℝ ℂ` also occurs inside the *type* of
  `A_complex_isHermitian` (hence inside the dependent type of
  `.eigenvalues`), so rewriting it breaks the motive. The proof below
  instead unfolds set-image membership by hand (`intro`/`obtain`) and only
  rewrites at the resulting first-order equality goal `algebraMap ℝ ℂ r =
  RCLike.ofReal r`, where no such dependency is in scope.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-2 instructions). This is a single concrete `3×3` matrix, not a
  general theorem about "any real matrix mapped into ℂ is Hermitian" (that
  is false in general — it needs `A` itself to be real-symmetric first,
  which is exactly what `A_isHermitian` below re-derives for this specific
  `A`). Nothing here computes the actual eigenvalues of the complexified
  matrix beyond what the real-spectrum computation in
  `PerronFrobeniusInstance.lean` already gives (that file's
  `A_spectrum_real` already shows the real spectrum is `{1, 4}`; this file
  independently confirms, via the general Hermitian-spectrum machinery
  rather than a second charpoly computation, that the COMPLEX spectrum of
  the complexified matrix contains nothing else, i.e. no genuinely
  non-real eigenvalues can hide). Nothing here is about Yang-Mills, SU(N),
  the lattice-gauge partition function, reflection positivity, or the
  continuum limit; it says nothing about, and does not approximate, a
  solution to the Clay mass-gap problem. No mathematical novelty is
  claimed: that a real symmetric matrix, viewed over ℂ, is Hermitian with
  wholly real spectrum is a completely classical, elementary fact.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib

open Matrix

namespace SHARED2B.HermitianComplexEmbeddingRange

/-! ### The concrete matrix, reproduced verbatim (see BUILD-SYSTEM NOTE above)

`A` is byte-identical to the Wave-1 YM-2 matrix
`YM2.PerronFrobeniusInstance.A : Matrix (Fin 3) (Fin 3) ℝ`
(`!![2, 1, 1; 1, 2, 1; 1, 1, 2]`), the same concrete `3×3` real symmetric
matrix, not a new/different object. -/

/-- The concrete `3×3` test matrix `A = I + J`, identical to
`YM2.PerronFrobeniusInstance.A` in the Wave-1 file
`04_YANG_MILLS/FORMAL/PerronFrobeniusInstance.lean`. -/
def A : Matrix (Fin 3) (Fin 3) ℝ := !![2, 1, 1; 1, 2, 1; 1, 1, 2]

/-- `A` is Hermitian, i.e. (since it is real) symmetric. Proved directly by
`ext`/`fin_cases`/`simp`, matching the style of the Wave-1 YM-1 sibling's
`M_isHermitian` in `FiniteLatticeTransferGap.lean`. This fact is NOT
reproduced from `PerronFrobeniusInstance.lean` (it does not state it); it
is proved fresh here, since it is exactly this item's own gap to close. -/
theorem A_isHermitian : A.IsHermitian := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [A, Matrix.conjTranspose_apply]

/-! ### Step 1 — the complexified matrix is Hermitian

`Function.Semiconj (algebraMap ℝ ℂ) star star` is exactly the general
Mathlib lemma `algebraMap_star_comm` (`Mathlib/Algebra/Star/Module.lean`),
available here because `StarModule ℝ ℂ` is an existing Mathlib instance. -/

/-- The semiconjugacy hypothesis needed by `Matrix.IsHermitian.map`: the
real-to-complex embedding commutes with `star` (trivially, since `star` is
the identity on `ℝ` and fixes the real subfield of `ℂ` pointwise). -/
theorem algebraMap_semiconj_star :
    Function.Semiconj (algebraMap ℝ ℂ) star star :=
  algebraMap_star_comm

/-- **Step 1 (SHARED-2B main test, part 1).** The complexification
`A.map (algebraMap ℝ ℂ)` of the Wave-1 YM-2 matrix is Hermitian over `ℂ`. -/
theorem A_complex_isHermitian :
    (A.map (algebraMap ℝ ℂ)).IsHermitian :=
  A_isHermitian.map (algebraMap ℝ ℂ) algebraMap_semiconj_star

/-! ### Step 2 — the complex spectrum lies in the range of `algebraMap ℝ ℂ`

Via `Matrix.IsHermitian.spectrum_eq_image_range`
(`Mathlib/Analysis/Matrix/Spectrum.lean`), specialized at `𝕜 := ℂ`. -/

/-- **Step 2 (SHARED-2B main test, part 2) — the actual falsifiable
target.** Every element of the complex spectrum of the complexified
matrix lies in the range of `algebraMap ℝ ℂ` — i.e. every complex
eigenvalue of `A.map (algebraMap ℝ ℂ)` is (the image of) a real number.
This is the "YM-2 realness gap" the Wave-1 file's header flagged as not
independently re-derived. -/
theorem A_complex_spectrum_subset_range :
    spectrum ℂ (A.map (algebraMap ℝ ℂ))
      ⊆ Set.range (algebraMap ℝ ℂ) := by
  intro x hx
  rw [A_complex_isHermitian.spectrum_eq_image_range] at hx
  obtain ⟨r, -, rfl⟩ := hx
  exact ⟨r, by rw [RCLike.algebraMap_eq_ofReal]⟩

end SHARED2B.HermitianComplexEmbeddingRange

/-! ### Axiom audit (verification-protocol requirement, not part of the
mathematical content). Confirms every new declaration above depends only
on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED2B.HermitianComplexEmbeddingRange.A_isHermitian
#print axioms SHARED2B.HermitianComplexEmbeddingRange.algebraMap_semiconj_star
#print axioms SHARED2B.HermitianComplexEmbeddingRange.A_complex_isHermitian
#print axioms SHARED2B.HermitianComplexEmbeddingRange.A_complex_spectrum_subset_range
