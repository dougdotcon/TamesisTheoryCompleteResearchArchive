/-
RH-2 (Wave 2) -- standalone probe, NOT integrated into `TamesisLab.lean` or any
shared aggregator. Follows the same convention as
`DiagonalSelfAdjointOperatorProbe.lean` (this directory, Wave 1): a
self-contained Lean file, verified directly via `lake env lean` against the
same vendored Mathlib, outside the shared import tree.

## Why standalone rather than `import`

The natural home for this result is right next to its Wave-1 source,
`TamesisLab.Riemann.ZetaZerosCountingFiniteness`
(`05_FORMAL/lean/TamesisLab/Riemann/ZetaZerosCountingFiniteness.lean`), whose
`zetaZerosInStrip`, `NZeta`, and `NZeta_region_finite` this file reuses
(re-derived below, not copied by `import`). That module is itself not wired
into `TamesisLab.lean`'s import graph, so its `.olean` is not present in this
checkout's build cache (confirmed empirically: `import
TamesisLab.Riemann.ZetaZerosCountingFiniteness` from a scratch file fails with
"object file ... does not exist"). Building it here to satisfy the import
would require `lake build`, which Wave-2 concurrency rules for this item
forbid (20 agents share this build cache). So, exactly as
`DiagonalSelfAdjointOperatorProbe.lean` did for RH-3 in Wave 1, this file
re-derives the small amount of shared infrastructure it needs
(`zetaZerosInStrip`, `NZeta`, `NZeta_region_finite`, and their two supporting
lemmas) verbatim from the Wave-1 file, under a distinct sub-namespace
(`CountingMonotoneVanishingProbe`, not `TamesisLab.Riemann` directly) so that
if a future integration pass ever does import both files together, there is
no `already declared` clash on `NZeta`/`zetaZerosInStrip`/etc. The re-derived
lemmas are proved identically to the Wave-1 originals (same Mathlib lemma
names, same proof terms); nothing about the mathematical content changes.

## What is proved (the Wave-2 RH-2 falsifiable test, exactly as scoped)

1. `NZeta_monotone : Monotone NZeta` -- for `T1 ≤ T2`,
   `zetaZerosInStrip T1 ⊆ zetaZerosInStrip T2` (immediate from the shared
   `0 < im z` lower bound and `im z ≤ T` transitivity), then
   `Set.ncard_le_ncard` against `NZeta_region_finite T2` as the finiteness
   witness gives `NZeta T1 ≤ NZeta T2`.
2. `NZeta_eq_zero_of_nonpos : T ≤ 0 → NZeta T = 0` -- for `T ≤ 0`,
   `Set.Ioc (0:ℝ) T = ∅` (`Set.Ioc_eq_empty_of_le`), so no `z` can satisfy
   `z.im ∈ Set.Ioc 0 T`, so `zetaZerosInStrip T = ∅`, so `NZeta T = 0`.

Both are exactly the two claims named in the Wave-2 RH-2 falsifiable test,
nothing broader.

## What this is explicitly NOT

* **Not** an asymptotic count, an error term, or a Riemann–von Mangoldt
  formula. `NZeta_monotone` says only that the count cannot decrease as the
  window widens; it says nothing about the *rate*.
* **Not** a proof, disproof, or approximation of RH. `zetaZerosInStrip` uses
  the classical non-trivial-zero strip `0 < re z < 1`, not the critical line
  `re z = 1/2`; no claim about zero location within the strip is made.
* **Not** connected to `TamesisLab.RHNogo`. This file shares no definitions
  with `AsymptoticCore`/`Bridge`/`Geometry`/`Composition` and does not touch
  the counting-law / abstract-composition no-go argument.
* **Not** a merge or edit of the Wave-1 `ZetaZerosCountingFiniteness.lean`
  file. That file is untouched by this item; this file only reproduces (under
  a distinct namespace) the small fragment of it needed as a self-contained
  finiteness witness, for the reason explained above.

scientific_novelty: NONE_CLAIMED_MATHLIB_WIRING_ONLY
-/

import Mathlib.NumberTheory.LSeries.ZetaZeros
import Mathlib.Analysis.Complex.ReImTopology

set_option autoImplicit false

namespace TamesisLab.Riemann.CountingMonotoneVanishingProbe

open Set Complex

/-! ## Re-derived shared infrastructure

Verbatim re-derivation (see file header) of `zetaZerosInStrip`, `NZeta`, and
`NZeta_region_finite` from the Wave-1 file
`TamesisLab.Riemann.ZetaZerosCountingFiniteness`, scoped under this file's own
sub-namespace so it cannot clash with that file's declarations. -/

/-- The zeros of `riemannZeta` in the classical non-trivial-zero strip
`0 < re z < 1`, with imaginary part in `(0, T]`. -/
def zetaZerosInStrip (T : ℝ) : Set ℂ :=
  {z : ℂ | z ∈ riemannZetaZeros ∧ z.re ∈ Set.Ioo (0 : ℝ) 1 ∧ z.im ∈ Set.Ioc (0 : ℝ) T}

/-- The counting function `N_ζ(T)`: the number of zeros of `riemannZeta` with
real part in `(0, 1)` and imaginary part in `(0, T]`. -/
noncomputable def NZeta (T : ℝ) : ℕ := (zetaZerosInStrip T).ncard

theorem isCompact_stripRectangle (T : ℝ) :
    IsCompact (Set.Icc (0 : ℝ) 1 ×ℂ Set.Icc (min 0 T) (max 0 T)) :=
  IsCompact.reProdIm isCompact_Icc isCompact_Icc

theorem zetaZerosInStrip_subset_stripRectangle (T : ℝ) :
    zetaZerosInStrip T ⊆ Set.Icc (0 : ℝ) 1 ×ℂ Set.Icc (min 0 T) (max 0 T) := by
  rintro z ⟨-, hre, him⟩
  refine Complex.mem_reProdIm.mpr ⟨⟨hre.1.le, hre.2.le⟩, ?_⟩
  exact ⟨le_trans (min_le_left 0 T) him.1.le, le_trans him.2 (le_max_right 0 T)⟩

/-- For every `T : ℝ`, the set of zeros of `riemannZeta` with real part in
`(0,1)` and imaginary part in `(0,T]` is finite. Re-derivation of the Wave-1
`NZeta_region_finite`; used below purely as the finiteness witness for
`Set.ncard_le_ncard` in `NZeta_monotone`. -/
theorem NZeta_region_finite (T : ℝ) : (zetaZerosInStrip T).Finite := by
  have hcompact := isCompact_stripRectangle T
  have hsubset := zetaZerosInStrip_subset_stripRectangle T
  have hfin := hcompact.inter_riemannZetaZeros_finite
  refine hfin.subset ?_
  intro z hz
  exact ⟨hsubset hz, hz.1⟩

/-! ## RH-2 Wave-2 result 1: monotonicity -/

/-- Widening the window `T1 ≤ T2` only ever adds zeros to the strip region:
the lower bound `0 < im z` and the upper bound `im z ≤ T` are both preserved,
the latter by transitivity along `T1 ≤ T2`. -/
theorem zetaZerosInStrip_subset {T1 T2 : ℝ} (h : T1 ≤ T2) :
    zetaZerosInStrip T1 ⊆ zetaZerosInStrip T2 := by
  rintro z ⟨hz, hre, him⟩
  exact ⟨hz, hre, ⟨him.1, him.2.trans h⟩⟩

/-- **Main result 1 (RH-2 Wave-2).** `NZeta` is monotone in `T`: the count
over `(0, T]` cannot decrease as `T` grows. Proved via
`zetaZerosInStrip_subset` composed with `Set.ncard_le_ncard`, using
`NZeta_region_finite T2` as the finiteness witness for the (larger) target
set, exactly as scoped in the Wave-2 RH-2 falsifiable test. -/
theorem NZeta_monotone : Monotone NZeta := by
  intro T1 T2 hT
  exact Set.ncard_le_ncard (zetaZerosInStrip_subset hT) (NZeta_region_finite T2)

/-! ## RH-2 Wave-2 result 2: vanishing for `T ≤ 0` -/

/-- For `T ≤ 0`, the half-open interval `(0, T]` is empty (`0 < z.im ≤ T ≤ 0`
is impossible), so no zero can lie in the strip region at all. -/
theorem zetaZerosInStrip_eq_empty_of_nonpos {T : ℝ} (hT : T ≤ 0) :
    zetaZerosInStrip T = ∅ := by
  have hIoc : Set.Ioc (0 : ℝ) T = (∅ : Set ℝ) := Set.Ioc_eq_empty_of_le hT
  rw [zetaZerosInStrip]
  ext z
  simp only [Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false]
  rintro ⟨-, -, him⟩
  rw [hIoc] at him
  exact him

/-- **Main result 2 (RH-2 Wave-2).** For `T ≤ 0`, `NZeta T = 0`, via
`zetaZerosInStrip T = ∅` (`Set.Ioc_eq_empty_of_le`) and `Set.ncard_empty`,
exactly as scoped in the Wave-2 RH-2 falsifiable test. -/
theorem NZeta_eq_zero_of_nonpos {T : ℝ} (hT : T ≤ 0) : NZeta T = 0 := by
  rw [NZeta, zetaZerosInStrip_eq_empty_of_nonpos hT, Set.ncard_empty]

/-! ## Axiom audit

Expected for every declaration below: only `propext`, `Classical.choice`,
`Quot.sound` (inherited from Mathlib's own use of classical logic and
quotients) -- nothing locally declared, nothing incomplete. -/

#print axioms zetaZerosInStrip
#print axioms NZeta
#print axioms isCompact_stripRectangle
#print axioms zetaZerosInStrip_subset_stripRectangle
#print axioms NZeta_region_finite
#print axioms zetaZerosInStrip_subset
#print axioms NZeta_monotone
#print axioms zetaZerosInStrip_eq_empty_of_nonpos
#print axioms NZeta_eq_zero_of_nonpos

end TamesisLab.Riemann.CountingMonotoneVanishingProbe
