/-
WAVE6-BSD-7 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`BSD1Step5Compose.lean`, `BSD6LFunctionEqOnPrimePowers.lean`,
`HasseCoefficientRecursionBound.lean`, `02_NAVIER_STOKES/FORMAL/`).

## What this file is

This item, `WAVE6-BSD-7`, is explicitly EXPLORATORY with a bounded size
ceiling. The falsifiable test attempted (exactly, nothing broader):

  For `W` a Weierstrass curve over `K` and `p` a good-reduction place,
  express `PowerSeries.coeff n (W.localPowerSeries (p.adicCompletionIntegers K))`
  as `TamesisLab.BSD3.cSeq a q n`, where `a`/`q` are read off
  `WeierstrassCurve.localPolynomial` and `q := Nat.card` of the residue
  field -- a BARE identity, with NO Hasse hypothesis, NO bound
  application, NO summability claim.

This is a candidate "bridge" between two pieces of prior-wave
infrastructure that were never previously connected:
* `WeierstrassCurve.localPolynomial` / `.localPowerSeries`
  (`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean:39-54`), and
* `TamesisLab.BSD3.cSeq` (`HasseCoefficientRecursionBound.lean`, Wave 2,
  `WAVE2-BSD-3`), the two-term linear recursion `c 0 = 1`, `c 1 = a`,
  `c (n+2) = a * c (n+1) - q * c n` satisfied by the coefficients of
  `1 / (1 - a T + q T ^ 2)`.

`cSeq` was originally introduced (Wave 2) to study Hasse-bound-driven
*growth* of these coefficients (`cSeq_abs_le`, via a nontrivial
Chebyshev-polynomial argument); that growth machinery is NOT reproduced
or used here. This file only reproduces `cSeq`'s bare *definition* and
its three defining equations (`cSeq_zero`, `cSeq_one`,
`cSeq_succ_succ`), which are `rfl`-provable one-liners, not the ~200
lines of Chebyshev/trigonometric analysis from the original file.

## Result: CLOSED, within the bounded scope stated above

The identity holds unconditionally at a good-reduction place, proved by
matching two power-series coefficient recursions term by term (no
Hasse-bound hypothesis on `a`/`q` is used or needed for the identity
itself -- `cSeq` is defined for arbitrary reals, Hasse-boundedness only
matters for the *growth bound* `cSeq_abs_le`, which this file does not
invoke).

## Proof strategy

Step A (`AbstractRecursion` section): for `a q : ℤ`, let
`φZ a q : PowerSeries ℤ := ↑(1 - C a * X + C q * X ^ 2 : Polynomial ℤ)`
and `ψZ a q := PowerSeries.invOfUnit (φZ a q) 1`. From
`φZ a q * ψZ a q = 1` (`PowerSeries.mul_invOfUnit`), extract:
* `coeff 0 ψZ = 1` via `PowerSeries.constantCoeff_invOfUnit`;
* `coeff 1 ψZ = a` via `PowerSeries.coeff_one_mul`
  (`Mathlib/RingTheory/PowerSeries/Basic.lean:644-648`);
* `coeff (n+2) ψZ = a * coeff (n+1) ψZ - q * coeff n ψZ` by rewriting
  `φZ a q` as `1 - C a * X + C q * X ^ 2`, expanding the product, and
  using the *monomial-shift* lemmas `PowerSeries.coeff_succ_X_mul` and
  `PowerSeries.coeff_X_pow_mul` (NOT the general `Finset.antidiagonal`
  convolution form of `PowerSeries.coeff_mul`, which is unnecessary here
  since `φZ a q` is only ever multiplied by a monomial `X` / `X ^ 2` in
  this derivation, not by a general power series).

Step B: a two-step (paired) induction on `n`, structurally identical in
shape to the induction already used in `HasseCoefficientRecursionBound
.lean`'s `cSeq_eq_rpow_mul_U`, shows the integer sequence `coeff n ψZ`,
cast to `ℝ`, agrees with `TamesisLab.BSD3.cSeq (a : ℝ) (q : ℝ) n` for
every `n`, using only `cSeq_zero` / `cSeq_one` / `cSeq_succ_succ` from
Step A above and Step B itself -- no Hasse bound anywhere.

Step C (`Connect` section): unfolds `WeierstrassCurve.localPolynomial`
under the hypothesis `(W.minimal R).HasGoodReduction R` (`if_pos`
against the good-reduction branch of the `if`/`else` chain in the
Mathlib definition) to identify `W.localPolynomial R` with exactly
`1 - C a * X + C q * X ^ 2` for `a`, `q` matching the Mathlib
docstring's own description (`q := Nat.card` of the residue field,
`a := q + 1 - Nat.card` of the reduced curve's point group), hence
`W.localPowerSeries R = ψZ a q` (`rfl`, since both sides literally unfold
to `PowerSeries.invOfUnit` of the same polynomial with the same unit
`1`), hence the coefficient identity via Step B.

A final `NumberFieldInstance` section specializes Step C's generic `R`
to `R := p.adicCompletionIntegers K` for `p : HeightOneSpectrum (𝓞 K)`
and `W` to `Wamb.baseChange (p.adicCompletion K)` for an ambient curve
`Wamb : WeierstrassCurve K`, matching the literal
`W.localPowerSeries (p.adicCompletionIntegers K)` shape named in this
item's falsifiable test -- a direct one-line application of the generic
`Connect`-section result, not independent new content.

## What this file does NOT prove (honest scope)

This is a purely algebraic/combinatorial fact about how the coefficients
of `1 / (1 - a T + q T ^ 2)` are indexed, specialized to the good-
reduction branch of `WeierstrassCurve.localPolynomial`. It does **not**:
touch `BSD-GAP-008` (Mordell-Weil, unrelated, still `OPEN`); invoke or
depend on the Hasse bound `|a| <= 2 sqrt q` in any way (the identity
holds for the literal integers `a`, `q` produced by `localPolynomial`,
whatever their size -- Hasse-boundedness is a separate, extremely
classical fact about actual traces of Frobenius that this file neither
proves nor assumes); make any summability or `LSeriesSummable` claim;
touch multiplicative/split/nonsplit-multiplicative/additive reduction
(only the good-reduction `if`-branch is unfolded); or make any claim of
mathematical novelty. Matching a generating function to its own
coefficient recursion is one of the most elementary facts possible about
formal power series. This file makes **zero** claim of progress toward,
or reachability of, the Birch and Swinnerton-Dyer conjecture (a Clay
Millennium Problem).
-/

import Mathlib.AlgebraicGeometry.EllipticCurve.LFunction

open Polynomial

/- Reproduced (bare definition + defining equations only, NOT the growth-bound
machinery) from `HasseCoefficientRecursionBound.lean` (Wave 2, `WAVE2-BSD-3`),
via the same "sibling files can't `import` each other" convention documented
there and in `BSD6LFunctionEqOnPrimePowers.lean`'s docstring: none of the
`03_MILLENNIUM/06_BSD/FORMAL/*.lean` files live under the `05_FORMAL/lean/`
project root, so a plain `import` of a sibling file does not resolve. -/
namespace TamesisLab.BSD3

/-- `cPair a q n = (c n, c (n+1))` for the recursion `c 0 = 1`, `c 1 = a`,
`c (n+2) = a * c (n+1) - q * c n`, packaged as a pair so the two-term
recursion becomes ordinary structural recursion on `ℕ`. Byte-identical to
`HasseCoefficientRecursionBound.lean`. -/
noncomputable def cPair (a q : ℝ) : ℕ → ℝ × ℝ
  | 0 => (1, a)
  | n + 1 => let p := cPair a q n; (p.2, a * p.2 - q * p.1)

/-- The Dirichlet coefficients of the formal power series `1 / (1 - a T + q T^2)`.
Byte-identical to `HasseCoefficientRecursionBound.lean`. -/
noncomputable def cSeq (a q : ℝ) (n : ℕ) : ℝ := (cPair a q n).1

theorem cSeq_zero (a q : ℝ) : cSeq a q 0 = 1 := rfl
theorem cSeq_one (a q : ℝ) : cSeq a q 1 = a := rfl
theorem cSeq_succ_succ (a q : ℝ) (n : ℕ) :
    cSeq a q (n + 2) = a * cSeq a q (n + 1) - q * cSeq a q n := rfl

end TamesisLab.BSD3

/-! ## `WAVE6-BSD-7` -- the actual new content of this item -/

namespace BSD7CoeffCSeqBridge

section AbstractRecursion

/-! Step A: the integer coefficient-recursion satisfied by the reciprocal of
`1 - C a * X + C q * X ^ 2`, derived directly from `φZ a q * ψZ a q = 1` via
monomial-shift lemmas -- no `Finset.antidiagonal` convolution bookkeeping
needed since `φZ a q` is only ever multiplied by `X` / `X ^ 2` below. -/

variable (a q : ℤ)

/-- The local Euler-factor-shaped polynomial `1 - C a * X + C q * X ^ 2`, as a
power series (coercion `Polynomial ℤ → PowerSeries ℤ`). -/
noncomputable def φZ : PowerSeries ℤ :=
  (1 - Polynomial.C a * Polynomial.X + Polynomial.C q * Polynomial.X ^ 2 : Polynomial ℤ)

/-- Its multiplicative inverse as a power series (constant coefficient `1` is
always a unit). -/
noncomputable def ψZ : PowerSeries ℤ := PowerSeries.invOfUnit (φZ a q) 1

theorem constantCoeff_φZ : PowerSeries.constantCoeff (φZ a q) = 1 := by
  unfold φZ; push_cast; simp

theorem mul_ψZ : φZ a q * ψZ a q = 1 :=
  PowerSeries.mul_invOfUnit (φZ a q) 1 (by rw [constantCoeff_φZ]; rfl)

theorem φZ_eq :
    φZ a q = 1 - PowerSeries.C a * PowerSeries.X + PowerSeries.C q * PowerSeries.X ^ 2 := by
  unfold φZ; push_cast; ring

theorem constantCoeff_ψZ : PowerSeries.constantCoeff (ψZ a q) = 1 := by
  unfold ψZ; rw [PowerSeries.constantCoeff_invOfUnit]; rfl

theorem coeff_zero_ψZ : PowerSeries.coeff 0 (ψZ a q) = 1 := by
  rw [PowerSeries.coeff_zero_eq_constantCoeff, constantCoeff_ψZ]

theorem coeff_one_ψZ : PowerSeries.coeff 1 (ψZ a q) = a := by
  have h := mul_ψZ a q
  have hc := congrArg (PowerSeries.coeff 1) h
  rw [PowerSeries.coeff_one_mul, constantCoeff_φZ, constantCoeff_ψZ] at hc
  have hφ1 : PowerSeries.coeff 1 (φZ a q) = -a := by
    unfold φZ; rw [Polynomial.coeff_coe]; simp [Polynomial.coeff_one]
  rw [hφ1] at hc
  simp only [PowerSeries.coeff_one, if_neg (one_ne_zero)] at hc
  linarith [hc]

/-- The recursion step, extracted by rewriting `φZ a q` as `1 - C a * X + C q
* X ^ 2`, expanding the product `φZ a q * ψZ a q = 1`, and using the
monomial-shift lemmas `PowerSeries.coeff_succ_X_mul` /
`PowerSeries.coeff_X_pow_mul` to read off `coeff (n+2) (X * ψZ) = coeff (n+1)
ψZ` and `coeff (n+2) (X ^ 2 * ψZ) = coeff n ψZ`. -/
theorem coeff_succ_succ_ψZ (n : ℕ) :
    PowerSeries.coeff (n + 2) (ψZ a q) =
      a * PowerSeries.coeff (n + 1) (ψZ a q) - q * PowerSeries.coeff n (ψZ a q) := by
  have h := mul_ψZ a q
  have hc := congrArg (PowerSeries.coeff (n + 2)) h
  rw [φZ_eq] at hc
  simp only [sub_mul, add_mul, one_mul, map_sub, map_add] at hc
  rw [show PowerSeries.C a * PowerSeries.X * ψZ a q
        = PowerSeries.C a * (PowerSeries.X * ψZ a q) by ring,
      show PowerSeries.C q * PowerSeries.X ^ 2 * ψZ a q
        = PowerSeries.C q * (PowerSeries.X ^ 2 * ψZ a q) by ring] at hc
  rw [PowerSeries.coeff_C_mul, PowerSeries.coeff_C_mul] at hc
  have hshift1 : PowerSeries.coeff (n + 2) (PowerSeries.X * ψZ a q) =
      PowerSeries.coeff (n + 1) (ψZ a q) := by
    simpa using PowerSeries.coeff_succ_X_mul (n + 1) (ψZ a q)
  have hshift2 : PowerSeries.coeff (n + 2) (PowerSeries.X ^ 2 * ψZ a q) =
      PowerSeries.coeff n (ψZ a q) := by
    simpa using PowerSeries.coeff_X_pow_mul (ψZ a q) 2 n
  rw [hshift1, hshift2] at hc
  have h1 : PowerSeries.coeff (n + 2) (1 : PowerSeries ℤ) = 0 := by simp
  rw [h1] at hc
  linarith [hc]

/-! Step B: paired (two-step) induction matching `cSeq`'s own recursion,
same shape as `HasseCoefficientRecursionBound.lean`'s `cSeq_eq_rpow_mul_U`
induction -- no Hasse bound involved anywhere in this step. -/

theorem coeff_ψZ_cast_pair (n : ℕ) :
    ((PowerSeries.coeff n (ψZ a q) : ℤ) : ℝ) = TamesisLab.BSD3.cSeq (a : ℝ) (q : ℝ) n ∧
    ((PowerSeries.coeff (n + 1) (ψZ a q) : ℤ) : ℝ) =
      TamesisLab.BSD3.cSeq (a : ℝ) (q : ℝ) (n + 1) := by
  induction n with
  | zero =>
    refine ⟨?_, ?_⟩
    · rw [coeff_zero_ψZ]; simp [TamesisLab.BSD3.cSeq_zero]
    · rw [coeff_one_ψZ]; simp [TamesisLab.BSD3.cSeq_one]
  | succ n ih =>
    obtain ⟨ih0, ih1⟩ := ih
    refine ⟨ih1, ?_⟩
    rw [coeff_succ_succ_ψZ]
    push_cast
    rw [ih1, ih0, TamesisLab.BSD3.cSeq_succ_succ]

/-- **Step A+B combined.** The integer coefficients of `ψZ a q` (the
reciprocal, as a power series, of `1 - C a * X + C q * X ^ 2`), cast to `ℝ`,
agree pointwise with `TamesisLab.BSD3.cSeq (a : ℝ) (q : ℝ)`. No Hasse-bound
hypothesis on `a q : ℤ` anywhere. -/
theorem coeff_ψZ_cast_eq_cSeq (n : ℕ) :
    ((PowerSeries.coeff n (ψZ a q) : ℤ) : ℝ) = TamesisLab.BSD3.cSeq (a : ℝ) (q : ℝ) n :=
  (coeff_ψZ_cast_pair a q n).1

end AbstractRecursion

section Connect

/-! Step C: identify `WeierstrassCurve.localPolynomial` / `.localPowerSeries`
at a good-reduction place with `φZ` / `ψZ` above (same variables as Mathlib's
own `LocalField` section in `Mathlib/AlgebraicGeometry/EllipticCurve
/LFunction.lean:35-36`). -/

variable {R : Type*} [CommRing R] [IsDomain R] [IsDiscreteValuationRing R] {K : Type*}
  [Field K] [Algebra R K] [IsFractionRing R K] (W : WeierstrassCurve K)

/-- Unfolding `WeierstrassCurve.localPolynomial` on the good-reduction branch
of its `if`/`else` chain: `if_pos hgood` selects exactly the
`1 - C a * X + C q * X ^ 2` clause, with `a`, `q` matching the Mathlib
docstring's own description of the good-reduction case. -/
theorem localPolynomial_eq_of_hasGoodReduction (hgood : (W.minimal R).HasGoodReduction R) :
    W.localPolynomial R =
      1 - Polynomial.C ((Nat.card (IsLocalRing.ResidueField R) : ℤ) + 1
            - Nat.card ((W.minimal R).reduction R).toAffine.Point) * Polynomial.X
        + Polynomial.C (Nat.card (IsLocalRing.ResidueField R) : ℤ) * Polynomial.X ^ 2 := by
  unfold WeierstrassCurve.localPolynomial
  rw [if_pos hgood]

/-- `W.localPowerSeries R` literally unfolds to `PowerSeries.invOfUnit` of the
same polynomial (via `localPolynomial_eq_of_hasGoodReduction`) with the same
unit `1` used to define `ψZ`, so the two agree by `rfl` once the polynomials
are equated. -/
theorem localPowerSeries_eq_ψZ_of_hasGoodReduction (hgood : (W.minimal R).HasGoodReduction R) :
    W.localPowerSeries R =
      BSD7CoeffCSeqBridge.ψZ ((Nat.card (IsLocalRing.ResidueField R) : ℤ) + 1
            - Nat.card ((W.minimal R).reduction R).toAffine.Point)
        (Nat.card (IsLocalRing.ResidueField R) : ℤ) := by
  unfold WeierstrassCurve.localPowerSeries
  rw [localPolynomial_eq_of_hasGoodReduction W hgood]
  rfl

/-- **Main result (`WAVE6-BSD-7`'s falsifiable test, minimal generic
form).** At a good-reduction place, the coefficients of `W.localPowerSeries
R`, cast to `ℝ`, are given by `TamesisLab.BSD3.cSeq a q n` with `a`, `q` read
off `WeierstrassCurve.localPolynomial`'s own good-reduction formula and `q :=
Nat.card` of the residue field, exactly as this item's falsifiable test
specifies. A bare identity: no Hasse hypothesis, no bound, no summability
claim. -/
theorem coeff_localPowerSeries_cast_eq_cSeq_of_hasGoodReduction
    (hgood : (W.minimal R).HasGoodReduction R) (n : ℕ) :
    ((PowerSeries.coeff n (W.localPowerSeries R) : ℤ) : ℝ) =
      TamesisLab.BSD3.cSeq
        (((Nat.card (IsLocalRing.ResidueField R) : ℤ) + 1
              - Nat.card ((W.minimal R).reduction R).toAffine.Point : ℤ) : ℝ)
        ((Nat.card (IsLocalRing.ResidueField R) : ℤ) : ℝ) n := by
  rw [localPowerSeries_eq_ψZ_of_hasGoodReduction W hgood]
  exact coeff_ψZ_cast_eq_cSeq _ _ n

end Connect

section NumberFieldInstance

/-! Specialization of the generic `Connect`-section result to `R :=
p.adicCompletionIntegers K`, `W := Wamb.baseChange (p.adicCompletion K)`,
matching the literal `W.localPowerSeries (p.adicCompletionIntegers K)` shape
named in this item's falsifiable test and in
`WeierstrassCurve.LFunction`'s own definition
(`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean:79-81`). A direct
one-line application of `coeff_localPowerSeries_cast_eq_cSeq_of_hasGoodReduction`
above, not independent new content. -/

open IsDedekindDomain NumberField

variable {K : Type*} [Field K] [NumberField K] (W : WeierstrassCurve K)
  (p : HeightOneSpectrum (𝓞 K))

/-- **Number-field-level instance of the main result**, matching the exact
`p.adicCompletionIntegers K` phrasing of this item's falsifiable test. -/
theorem coeff_localPowerSeries_adicCompletionIntegers_cast_eq_cSeq_of_hasGoodReduction
    (hgood : ((W.baseChange (p.adicCompletion K)).minimal (p.adicCompletionIntegers K)).HasGoodReduction
      (p.adicCompletionIntegers K)) (n : ℕ) :
    ((PowerSeries.coeff n
        ((W.baseChange (p.adicCompletion K)).localPowerSeries (p.adicCompletionIntegers K))
        : ℤ) : ℝ) =
      TamesisLab.BSD3.cSeq
        (((Nat.card (IsLocalRing.ResidueField (p.adicCompletionIntegers K)) : ℤ) + 1
              - Nat.card (((W.baseChange (p.adicCompletion K)).minimal
                  (p.adicCompletionIntegers K)).reduction
                    (p.adicCompletionIntegers K)).toAffine.Point : ℤ) : ℝ)
        ((Nat.card (IsLocalRing.ResidueField (p.adicCompletionIntegers K)) : ℤ) : ℝ) n :=
  coeff_localPowerSeries_cast_eq_cSeq_of_hasGoodReduction _ hgood n

end NumberFieldInstance

end BSD7CoeffCSeqBridge

#print axioms TamesisLab.BSD3.cSeq_zero
#print axioms TamesisLab.BSD3.cSeq_one
#print axioms TamesisLab.BSD3.cSeq_succ_succ
#print axioms BSD7CoeffCSeqBridge.constantCoeff_φZ
#print axioms BSD7CoeffCSeqBridge.mul_ψZ
#print axioms BSD7CoeffCSeqBridge.φZ_eq
#print axioms BSD7CoeffCSeqBridge.constantCoeff_ψZ
#print axioms BSD7CoeffCSeqBridge.coeff_zero_ψZ
#print axioms BSD7CoeffCSeqBridge.coeff_one_ψZ
#print axioms BSD7CoeffCSeqBridge.coeff_succ_succ_ψZ
#print axioms BSD7CoeffCSeqBridge.coeff_ψZ_cast_pair
#print axioms BSD7CoeffCSeqBridge.coeff_ψZ_cast_eq_cSeq
#print axioms BSD7CoeffCSeqBridge.localPolynomial_eq_of_hasGoodReduction
#print axioms BSD7CoeffCSeqBridge.localPowerSeries_eq_ψZ_of_hasGoodReduction
#print axioms BSD7CoeffCSeqBridge.coeff_localPowerSeries_cast_eq_cSeq_of_hasGoodReduction
#print axioms BSD7CoeffCSeqBridge.coeff_localPowerSeries_adicCompletionIntegers_cast_eq_cSeq_of_hasGoodReduction
