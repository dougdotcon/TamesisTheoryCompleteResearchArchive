/-
WAVE7-BSD-8 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`BSD1Step5Compose.lean`, `BSD6LFunctionEqOnPrimePowers.lean`,
`BSD7CoeffCSeqBridge.lean`, `02_NAVIER_STOKES/FORMAL/`).

## What this file is

This item, `WAVE7-BSD-8`, is a direct bounded follow-on to
`WAVE6-BSD-7` (`BSD7CoeffCSeqBridge.lean`), which computed the
coefficients of `WeierstrassCurve.localPowerSeries` ONLY at a
good-reduction place (the `if`-branch `1 - a T + q T ^ 2` of
`WeierstrassCurve.localPolynomial`,
`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean:43-50`). This
item covers the coefficient identities on the three remaining
(non-good-reduction) branches of that same `if`/`else` chain, each as
its own self-contained theorem:

1. split-multiplicative reduction (`1 - X` branch):
   `coeff n (W.localPowerSeries R) = 1` for every `n`.
2. non-split-multiplicative reduction (`1 + X` branch, i.e.
   `HasMultiplicativeReduction` but NOT `HasSplitMultiplicativeReduction`):
   `coeff n (W.localPowerSeries R) = (-1) ^ n` for every `n`.
3. additive reduction (`1` branch): `W.localPowerSeries R = 1` outright
   (not merely a per-coefficient statement, since the power series
   itself is the constant `1`).

Each is a bare algebraic identity about how `PowerSeries.invOfUnit` of
one of these three elementary polynomials expands, driven entirely by
`if_pos`/`if_neg` selection of the correct branch of
`WeierstrassCurve.localPolynomial`'s `if`/`else` chain plus one
Mathlib lemma per branch (`PowerSeries.mk_one_mul_one_sub_eq_one` for
branch 1, additionally `PowerSeries.rescale_neg_one_X` for branch 2,
and `PowerSeries.mul_invOfUnit` alone for branch 3). NO Hasse bound,
NO summability claim, NO connection to `TamesisLab.BSD3.cSeq` (unlike
`WAVE6-BSD-7`, which is unrelated here since these three branches are
not of the two-term-recursion shape `cSeq` models).

Each branch is a SINGLE top-level theorem (the `if`-unfolding step and
the `invOfUnit` identity step are both inlined as `have`s in one proof,
rather than split into separate reusable lemmas as in
`BSD7CoeffCSeqBridge.lean`) -- a deliberate line-count-driven choice for
this item, since three separate branches sharing one 90-line ceiling
leaves no room for the repeated theorem-header boilerplate that a
fully-factored style would cost.

This file makes **zero** claim of progress toward, or reachability of,
the Birch and Swinnerton-Dyer conjecture (a Clay Millennium Problem),
and does **not** touch `BSD-GAP-008` (Mordell-Weil, unrelated, still
`OPEN`). Matching a generating function to its own coefficients is one
of the most elementary facts possible about formal power series;
nothing here concerns convergence of `LSeries`, analytic continuation,
a functional equation, a conductor, or Mordell-Weil rank.

## Reproduction convention (same as `BSD6LFunctionEqOnPrimePowers.lean`,
`BSD7CoeffCSeqBridge.lean`)

None of the sibling `03_MILLENNIUM/06_BSD/FORMAL/*.lean` files live
under the `05_FORMAL/lean/` project root, so a plain `import` of a
sibling file does not resolve. This file needs NO prior-wave sibling
content at all (unlike `BSD7CoeffCSeqBridge.lean`, which reproduced
`TamesisLab.BSD3.cSeq`): every declaration below is either a direct
`import Mathlib...` citation or new content of this item.

## Result

All three branch theorems typecheck cleanly, using no tactic or
construct from this lab's forbidden-token list (see the lab's
governance scanner policy), and leave no unproved side gaps -- see the
`#print axioms` output at the bottom of this file.

## Line-count discipline (DEC-103 lesson, applied explicitly here)

This item has a hard ceiling of 90 new non-comment lines across all
three branches, measured after EACH branch closes (not only at the
end), per this item's own stop_condition. See the final report for the
exact measured counts per branch. An earlier draft of this file split
each branch into 3 separate top-level theorems (matching
`BSD7CoeffCSeqBridge.lean`'s style); that draft measured 38 lines for
branch 1 and 88 cumulative after branch 2, leaving no room for branch
3. This is the consolidated (single-theorem-per-branch) rewrite,
adopted specifically to fit all three branches inside the ceiling
without weakening any statement.
-/

import Mathlib.AlgebraicGeometry.EllipticCurve.LFunction
import Mathlib.RingTheory.PowerSeries.WellKnown

namespace BSD8LocalPowerSeriesBadReductionCoeffs

variable {R : Type*} [CommRing R] [IsDomain R] [IsDiscreteValuationRing R] {K : Type*}
  [Field K] [Algebra R K] [IsFractionRing R K] (W : WeierstrassCurve K)

section SplitMultiplicative

/-! **Branch 1 (`WAVE7-BSD-8`, split-multiplicative reduction).** Falsifiable test: `coeff n
(W.localPowerSeries R) = 1` for every `n`, at a split-multiplicative place. `if_neg` (via
`HasMultiplicativeReduction.not_hasGoodReduction`, since `HasSplitMultiplicativeReduction`
extends `HasMultiplicativeReduction`) eliminates the good-reduction branch of
`WeierstrassCurve.localPolynomial`'s `if`/`else` chain, then `if_pos hsplit` selects the
split-multiplicative branch, landing on `1 - X`. `PowerSeries.mul_invOfUnit` (giving
`(1 - X) * invOfUnit (1 - X) 1 = 1`) and `PowerSeries.mk_one_mul_one_sub_eq_one` (giving
`mk 1 * (1 - X) = 1`) then identify `invOfUnit (1 - X) 1` with `mk 1`, the all-ones power
series, by the standard "both are inverses of the same element in a commutative ring"
rearrangement. -/
theorem coeff_localPowerSeries_eq_one_of_hasSplitMultiplicativeReduction
    (hsplit : (W.minimal R).HasSplitMultiplicativeReduction R) (n : ℕ) :
    PowerSeries.coeff n (W.localPowerSeries R) = 1 := by
  unfold WeierstrassCurve.localPowerSeries WeierstrassCurve.localPolynomial
  rw [if_neg hsplit.toHasMultiplicativeReduction.not_hasGoodReduction, if_pos hsplit,
      show ((1 - Polynomial.X : Polynomial ℤ) : PowerSeries ℤ) = 1 - PowerSeries.X by simp]
  have h : (1 - PowerSeries.X : PowerSeries ℤ) *
      PowerSeries.invOfUnit (1 - PowerSeries.X) 1 = 1 :=
    PowerSeries.mul_invOfUnit _ 1 (by simp)
  have heq : PowerSeries.invOfUnit (1 - PowerSeries.X : PowerSeries ℤ) 1 = PowerSeries.mk 1 := by
    calc PowerSeries.invOfUnit (1 - PowerSeries.X : PowerSeries ℤ) 1
        = 1 * PowerSeries.invOfUnit (1 - PowerSeries.X) 1 := (one_mul _).symm
      _ = (PowerSeries.mk 1 * (1 - PowerSeries.X)) *
            PowerSeries.invOfUnit (1 - PowerSeries.X) 1 := by
          rw [PowerSeries.mk_one_mul_one_sub_eq_one]
      _ = PowerSeries.mk 1 *
            ((1 - PowerSeries.X) * PowerSeries.invOfUnit (1 - PowerSeries.X) 1) := by ring
      _ = PowerSeries.mk (1 : ℕ → ℤ) * 1 := by rw [h]
      _ = PowerSeries.mk 1 := mul_one _
  rw [heq, PowerSeries.coeff_mk]
  rfl

end SplitMultiplicative

section NonsplitMultiplicative

/-! **Branch 2 (`WAVE7-BSD-8`, non-split-multiplicative reduction).** Falsifiable test: `coeff n
(W.localPowerSeries R) = (-1) ^ n` for every `n`, at a place with `HasMultiplicativeReduction`
but NOT `HasSplitMultiplicativeReduction` (the Mathlib docstring's own "non-split" case,
`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean:74`). `if_neg`/`if_neg`/`if_pos` selects
the `1 + X` branch. Applying the ring homomorphism `PowerSeries.rescale (-1)` to
`mk 1 * (1 - X) = 1` and using `PowerSeries.rescale_neg_one_X` to rewrite `rescale (-1) (1 - X)`
as `1 + X` shows `rescale (-1) (mk 1)` is a two-sided inverse of `1 + X`; the same "both are
inverses of the same element" rearrangement as branch 1 then identifies it with
`invOfUnit (1 + X) 1`. -/
theorem coeff_localPowerSeries_eq_neg_one_pow_of_hasMultiplicativeReduction_of_not_hasSplitMultiplicativeReduction
    (hmult : (W.minimal R).HasMultiplicativeReduction R)
    (hnsplit : ¬ (W.minimal R).HasSplitMultiplicativeReduction R) (n : ℕ) :
    PowerSeries.coeff n (W.localPowerSeries R) = (-1 : ℤ) ^ n := by
  unfold WeierstrassCurve.localPowerSeries WeierstrassCurve.localPolynomial
  rw [if_neg hmult.not_hasGoodReduction, if_neg hnsplit, if_pos hmult,
      show ((1 + Polynomial.X : Polynomial ℤ) : PowerSeries ℤ) = 1 + PowerSeries.X by simp]
  have hrw : PowerSeries.rescale (-1 : ℤ) (1 - PowerSeries.X : PowerSeries ℤ) =
      1 + PowerSeries.X := by
    rw [map_sub, map_one, PowerSeries.rescale_neg_one_X, sub_neg_eq_add]
  have hmul : PowerSeries.rescale (-1 : ℤ) (PowerSeries.mk 1) *
      (1 + PowerSeries.X : PowerSeries ℤ) = 1 := by
    rw [← hrw, ← map_mul, PowerSeries.mk_one_mul_one_sub_eq_one, map_one]
  have h : (1 + PowerSeries.X : PowerSeries ℤ) *
      PowerSeries.invOfUnit (1 + PowerSeries.X) 1 = 1 :=
    PowerSeries.mul_invOfUnit _ 1 (by simp)
  have heq : PowerSeries.invOfUnit (1 + PowerSeries.X : PowerSeries ℤ) 1 =
      PowerSeries.rescale (-1 : ℤ) (PowerSeries.mk 1) := by
    calc PowerSeries.invOfUnit (1 + PowerSeries.X : PowerSeries ℤ) 1
        = 1 * PowerSeries.invOfUnit (1 + PowerSeries.X) 1 := (one_mul _).symm
      _ = (PowerSeries.rescale (-1 : ℤ) (PowerSeries.mk 1) * (1 + PowerSeries.X)) *
            PowerSeries.invOfUnit (1 + PowerSeries.X) 1 := by rw [hmul]
      _ = PowerSeries.rescale (-1 : ℤ) (PowerSeries.mk 1) *
            ((1 + PowerSeries.X) * PowerSeries.invOfUnit (1 + PowerSeries.X) 1) := by ring
      _ = PowerSeries.rescale (-1 : ℤ) (PowerSeries.mk 1) * 1 := by rw [h]
      _ = PowerSeries.rescale (-1 : ℤ) (PowerSeries.mk 1) := mul_one _
  rw [heq, PowerSeries.coeff_rescale, PowerSeries.coeff_mk]
  simp

end NonsplitMultiplicative

section Additive

/-! **Branch 3 (`WAVE7-BSD-8`, additive reduction).** Falsifiable test: `W.localPowerSeries R = 1`
outright (the power series itself, not merely each coefficient). `if_neg hadd.not_hasGoodReduction`
eliminates the good-reduction branch; `HasAdditiveReduction.not_hasMultiplicativeReduction`
eliminates BOTH remaining branches -- the plain multiplicative branch directly, and (via
`HasSplitMultiplicativeReduction.toHasMultiplicativeReduction`, contraposed) the split-
multiplicative branch too, since split implies multiplicative -- leaving the final `else 1`
clause. `PowerSeries.mul_invOfUnit` alone then gives `invOfUnit 1 1 = 1` via `one_mul`. -/
theorem localPowerSeries_eq_one_of_hasAdditiveReduction
    (hadd : (W.minimal R).HasAdditiveReduction R) :
    W.localPowerSeries R = 1 := by
  unfold WeierstrassCurve.localPowerSeries WeierstrassCurve.localPolynomial
  rw [if_neg hadd.not_hasGoodReduction,
      if_neg (mt (fun hs => hs.toHasMultiplicativeReduction) hadd.not_hasMultiplicativeReduction),
      if_neg hadd.not_hasMultiplicativeReduction,
      show ((1 : Polynomial ℤ) : PowerSeries ℤ) = 1 by simp]
  have h : (1 : PowerSeries ℤ) * PowerSeries.invOfUnit (1 : PowerSeries ℤ) 1 = 1 :=
    PowerSeries.mul_invOfUnit _ 1 (by simp)
  rwa [one_mul] at h

end Additive

end BSD8LocalPowerSeriesBadReductionCoeffs

#print axioms BSD8LocalPowerSeriesBadReductionCoeffs.coeff_localPowerSeries_eq_one_of_hasSplitMultiplicativeReduction
#print axioms BSD8LocalPowerSeriesBadReductionCoeffs.coeff_localPowerSeries_eq_neg_one_pow_of_hasMultiplicativeReduction_of_not_hasSplitMultiplicativeReduction
#print axioms BSD8LocalPowerSeriesBadReductionCoeffs.localPowerSeries_eq_one_of_hasAdditiveReduction
