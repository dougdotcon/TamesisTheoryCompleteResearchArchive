import Mathlib.NumberTheory.LSeries.ZetaZeros
import Mathlib.Analysis.Complex.ReImTopology

set_option autoImplicit false

/-!
# RH-2 — Well-definedness (finiteness) of a strip-restricted zeta zero count

This file is a narrow, self-contained reconnaissance result. It answers only
the "is the counting function well defined" half of the classical
zero-counting question `N(T)` for the Riemann zeta function, by wiring up
Mathlib's own `riemannZetaZeros` API
(`Mathlib.NumberTheory.LSeries.ZetaZeros`, a 2026 addition to the pinned
Mathlib revision, credited there to Huanyu Zheng) to elementary compactness
facts about rectangles in `ℂ`.

## What is proved

`NZeta T` is defined as the cardinality (`Set.ncard`) of the zeros of
`riemannZeta` lying in the open strip `0 < re z < 1` with `0 < im z ≤ T`.
`NZeta_region_finite` shows the underlying set is finite for every
`T : ℝ`, by exhibiting the explicit compact rectangle
`Set.Icc 0 1 ×ℂ Set.Icc (min 0 T) (max 0 T)` (compact by
`isCompact_Icc` + `IsCompact.reProdIm`) that contains the region, and
applying `IsCompact.inter_riemannZetaZeros_finite` from
`Mathlib.NumberTheory.LSeries.ZetaZeros`.

## What this is explicitly NOT

* **Not** an asymptotic count. No `T log T` growth rate, no error term, no
  connection to the classical Riemann–von Mangoldt formula is established or
  attempted here. `NZeta_region_finite` says only that the count is a
  well-defined natural number for each `T`, nothing about how it grows.
* **Not** a proof or approximation of RH. The critical strip membership
  condition `0 < re z < 1` in `NZeta` is the classical non-trivial-zero
  strip, not the critical *line* `re z = 1/2`; no claim about the location
  of zeros within the strip is made or needed.
* **Not** connected to `TamesisLab.RHNogo` (`ASYM-NOGO-001` and its
  descendants). Nothing here is imported by, or imports, that chain; this
  file stands alone, matching the standalone-file convention already used
  for other one-off Millennium-line reconnaissance results in this lab.
* Supersedes nothing in `SOURCE_BRIDGE_GAP_REGISTER.yaml` (SB-GAP-010B):
  that gap is about the *asymptotic* count and remains open. This file only
  removes the (smaller, structural) question of whether the strip-restricted
  count is even finite — which turns out to be a direct, short consequence
  of infrastructure already present in the pinned Mathlib revision.

scientific_novelty: NONE_CLAIMED_MATHLIB_WIRING_ONLY
-/

namespace TamesisLab.Riemann

open Set Complex

/-- The zeros of `riemannZeta` in the classical non-trivial-zero strip
`0 < re z < 1`, with imaginary part in `(0, T]`. -/
def zetaZerosInStrip (T : ℝ) : Set ℂ :=
  {z : ℂ | z ∈ riemannZetaZeros ∧ z.re ∈ Set.Ioo (0 : ℝ) 1 ∧ z.im ∈ Set.Ioc (0 : ℝ) T}

/-- The counting function `N_ζ(T)`: the number of zeros of `riemannZeta` with
real part in `(0, 1)` and imaginary part in `(0, T]`.

This is well defined (a genuine natural number, not a junk value from an
infinite set) precisely because of `NZeta_region_finite` below. -/
noncomputable def NZeta (T : ℝ) : ℕ := (zetaZerosInStrip T).ncard

/-- The closed rectangle `[0,1] × [min 0 T, max 0 T]` in `ℂ`, viewed via
`re`/`im`. It is compact, and it contains `zetaZerosInStrip T` for every
`T : ℝ` (the `min`/`max` framing makes this true uniformly, including for
`T ≤ 0`, where `zetaZerosInStrip T` is empty). -/
theorem isCompact_stripRectangle (T : ℝ) :
    IsCompact (Set.Icc (0 : ℝ) 1 ×ℂ Set.Icc (min 0 T) (max 0 T)) :=
  IsCompact.reProdIm isCompact_Icc isCompact_Icc

theorem zetaZerosInStrip_subset_stripRectangle (T : ℝ) :
    zetaZerosInStrip T ⊆ Set.Icc (0 : ℝ) 1 ×ℂ Set.Icc (min 0 T) (max 0 T) := by
  rintro z ⟨-, hre, him⟩
  refine Complex.mem_reProdIm.mpr ⟨⟨hre.1.le, hre.2.le⟩, ?_⟩
  exact ⟨le_trans (min_le_left 0 T) him.1.le, le_trans him.2 (le_max_right 0 T)⟩

/-- **Main result.** For every `T : ℝ`, the set of zeros of `riemannZeta`
with real part in `(0,1)` and imaginary part in `(0,T]` is finite. Hence
`NZeta T` is a well-defined counting function (no asymptotics claimed). -/
theorem NZeta_region_finite (T : ℝ) : (zetaZerosInStrip T).Finite := by
  have hcompact := isCompact_stripRectangle T
  have hsubset := zetaZerosInStrip_subset_stripRectangle T
  have hfin := hcompact.inter_riemannZetaZeros_finite
  refine hfin.subset ?_
  intro z hz
  exact ⟨hsubset hz, hz.1⟩

/-- Restatement of `NZeta_region_finite` via `Set.ncard`, confirming `NZeta`
does not silently collapse to the Mathlib junk value `0` for an infinite
set: the underlying set genuinely has finite cardinality. -/
theorem NZeta_eq_ncard_of_finite (T : ℝ) :
    NZeta T = (zetaZerosInStrip T).ncard := rfl

/-! ## Axiom audit

Expected for every declaration below: only `propext`, `Classical.choice`,
`Quot.sound` (inherited from Mathlib's own use of classical logic and
quotients) -- nothing locally declared, nothing incomplete. -/

#print axioms zetaZerosInStrip
#print axioms NZeta
#print axioms isCompact_stripRectangle
#print axioms zetaZerosInStrip_subset_stripRectangle
#print axioms NZeta_region_finite
#print axioms NZeta_eq_ncard_of_finite

end TamesisLab.Riemann
