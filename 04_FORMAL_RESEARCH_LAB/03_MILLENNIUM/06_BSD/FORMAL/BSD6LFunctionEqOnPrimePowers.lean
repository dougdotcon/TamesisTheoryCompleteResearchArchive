/-
WAVE5-BSD-6 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`BSD1Step5Compose.lean`, `BSD1Step4ResidueBijection.lean`,
`LFunctionMultiplicativity.lean`, `02_NAVIER_STOKES/FORMAL/`).

## What this file is

`BSD-GAP-007` closed genuinely in Wave 4 (`BSD1Step5Compose.lean`,
`WeierstrassCurve.LFunction_isMultiplicative`, lines 370-372 of that
file, re-checked here directly via `lake env lean` before writing this
file): for any Weierstrass curve `W` over a number field `K`,
`W.LFunction.IsMultiplicative` holds unconditionally, no hypothesis.

This Wave-5 item, `WAVE5-BSD-6`, is a single, minimal, purely
structural corollary of that result: any two multiplicative arithmetic
functions that agree on all prime powers are equal
(`ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers`,
`Mathlib/NumberTheory/ArithmeticFunction/Defs.lean:564-573`, inside
`namespace IsMultiplicative`, requiring only `[CommMonoidWithZero R]`
-- satisfied by `R = ℤ`, the codomain of `WeierstrassCurve.LFunction`,
`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean:79-80`).
Specializing the generic lemma's `f` argument to `W.LFunction` and
feeding it `LFunction_isMultiplicative` gives, for one fixed `W`:
`W.LFunction` is determined by (equal to any other multiplicative
arithmetic function agreeing with it on) its values at prime powers.

This file makes **zero** claim of novelty, **zero** claim of progress
toward, or reachability of, the Birch and Swinnerton-Dyer conjecture (a
Clay Millennium Problem), and does **not** touch `BSD-GAP-008`
(Mordell-Weil, unrelated, still `OPEN`). `IsMultiplicative.eq_iff_
eq_on_prime_powers` is one of the most elementary structural facts
about multiplicative arithmetic functions in general; nothing here
concerns convergence of `LSeries`, analytic continuation, a functional
equation, a conductor, or Mordell-Weil rank.

## Falsifiable test attempted (exactly, nothing broader)

Minimal scope (this file's main, reported result):
`theorem LFunction_eq_iff_eq_on_prime_powers ... :=
  (LFunction_isMultiplicative W).eq_iff_eq_on_prime_powers ...`

Optional extension (separate declaration, own check -- per the task's
explicit instruction NOT to claim both closed unless both individually
pass `lake env lean` + `#print axioms` cleanly):
`LFunction_apply_eq_prod_prime_powers` via `.multiplicative_factorization`.

## Reproduction convention (same as `BSD1Step5Compose.lean`)

None of the sibling `03_MILLENNIUM/06_BSD/FORMAL/*.lean` files live
under the `05_FORMAL/lean/` project root, so a plain `import` of a
sibling file does not resolve, and `lake env lean <file> -o <olean>`
(to place a sibling file's compiled output into the shared build cache
so it could be imported) is refused by `lake` itself with "input file
... must be contained in root directory" (confirmed directly against
`BSD1Step5Compose.lean` while preparing this file -- same failure mode
`BSD1Step4ResidueBijection.lean` and `BSD1Step5Compose.lean` already
document for plain `import`). Consequently this file reproduces,
byte-identical, the full Wave-2/Wave-3/Wave-4 chain from
`BSD1Step5Compose.lean` needed to reach the unconditional
`WeierstrassCurve.LFunction_isMultiplicative` theorem (which itself
already reproduces from `BSD1Step1ComposeResidueField.lean`,
`BSD1Step4ResidueBijection.lean`, and `LFunctionMultiplicativity.lean`
-- see that file's own docstring for the detailed attribution chain),
with this note as attribution. Nothing below is independently
re-derived beyond what those Wave-2/3/4 files already closed; the only
new content of this item is `LFunction_eq_iff_eq_on_prime_powers`
(minimal scope) and, reported separately,
`LFunction_apply_eq_prod_prime_powers` (optional extension), both in
the final `WAVE5BSD6` section at the bottom of this file.

## Result

Both the minimal-scope declaration and the optional-extension
declaration typecheck cleanly, using no tactic or construct from this
lab's forbidden-token list (see the lab's governance scanner policy),
and leave no unproved side gaps -- see the `#print axioms` output at
the bottom of this file.
-/

import Mathlib.RingTheory.DedekindDomain.AdicValuation
import Mathlib.RingTheory.Localization.AtPrime.Basic
import Mathlib.RingTheory.Valuation.Extension
import Mathlib.RingTheory.SimpleRing.Basic
import Mathlib.AlgebraicGeometry.EllipticCurve.LFunction

open IsDedekindDomain NumberField WithZero Valuation ArithmeticFunction

namespace BSD1Step5Compose

section STEP1ComposeReproduced

/- Reproduced byte-identical from `BSD1Step1ComposeResidueField.lean`'s
`BSD1Step1Compose.equivResidueField_valuationSubringAtPrime` and
`BSD1Step1Compose.equivResidueField_valuationSubring`, via
`BSD1Step5Compose.lean`'s own `STEP1ComposeReproduced` section (see this
file's docstring above for attribution). -/

variable {R K : Type*} [CommRing R] [IsDedekindDomain R] [Field K] [Algebra R K]
  [IsFractionRing R K] (v : HeightOneSpectrum R)

/-- **Direct instantiation.** `IsLocalization.AtPrime.equivQuotMaximalIdeal`, applied with
`Rₚ := HeightOneSpectrum.valuationSubringAtPrime K v`. -/
noncomputable def equivResidueField_valuationSubringAtPrime :
    R ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField (v.valuationSubringAtPrime K) :=
  IsLocalization.AtPrime.equivQuotMaximalIdeal v.asIdeal (v.valuationSubringAtPrime K)

/-- **Composed/transported version**, transport
`equivResidueField_valuationSubringAtPrime` along
`HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring` to land on the residue field of
the *actual* `v`-adic valuation subring of `K`. -/
noncomputable def equivResidueField_valuationSubring :
    R ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField (v.valuation K).valuationSubring := by
  rw [← HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring (R := R) (K := K) v]
  exact equivResidueField_valuationSubringAtPrime v

end STEP1ComposeReproduced

section STEP4ResidueBijectionReproduced

/- Reproduced byte-identical from `BSD1Step4ResidueBijection.lean`, via
`BSD1Step5Compose.lean`'s own `STEP4ResidueBijectionReproduced` section
(see this file's docstring above for attribution): its STEP2-CORE-witness
and STEP3-`HasExtension` reproductions, plus the `STEP4-RESIDUE-BIJECTION`
target declarations. -/

section STEP2CoreWitnessReproduced

variable {R K : Type*} [CommRing R] [IsDedekindDomain R] [Field K] [Algebra R K]
  [IsFractionRing R K] (v : HeightOneSpectrum R)

theorem exists_valuationSubringAtPrime_sub_lt_one (x : v.adicCompletionIntegers K) :
    ∃ k : v.valuationSubringAtPrime K,
      Valued.v ((x : v.adicCompletion K) - ((k : K) : v.adicCompletion K)) < 1 := by
  set x' : v.adicCompletion K := (x : v.adicCompletion K) with hx'
  -- The unit ball around `0` is open (`Valued.isOpen_ball`, reconciled with the literal
  -- `Valued.v _ < 1` statement via the `restrict_lt_one_iff` simp lemma).
  have hopen : IsOpen {y : v.adicCompletion K | Valued.v (y - x') < 1} := by
    have h : IsOpen {y : v.adicCompletion K | Valued.v y < 1} := by
      have heq : {y : v.adicCompletion K | Valued.v y < 1} = {y | Valued.v.restrict y < 1} := by
        ext y
        exact (Valuation.restrict_lt_one_iff (Valued.v) (x := y)).symm
      rw [heq]
      exact Valued.isOpen_ball (v.adicCompletion K) 1
    have hc : Continuous (fun y : v.adicCompletion K => y - x') := by fun_prop
    simpa [Set.preimage] using hc.isOpen_preimage _ h
  have hx_mem : x' ∈ {y : v.adicCompletion K | Valued.v (y - x') < 1} := by simp
  have hnhds := hopen.mem_nhds hx_mem
  -- Density of `K` inside the completion (the lemma named in the test).
  have hdense : DenseRange (algebraMap K (v.adicCompletion K)) :=
    HeightOneSpectrum.denseRange_algebraMap K v
  obtain ⟨y, hyU, hyrange⟩ := mem_closure_iff_nhds.mp (hdense x') _ hnhds
  obtain ⟨k', hk'⟩ := hyrange
  have hyU' : Valued.v (y - x') < 1 := hyU
  have hxle : Valued.v x' ≤ 1 := (HeightOneSpectrum.mem_adicCompletionIntegers R K v).mp x.2
  -- Non-archimedean triangle inequality: since `x' = y - (y - x') ...` equivalently
  -- `y = x' + (y - x')` with both summands of valuation `≤ 1`, so is `y`.
  have hyle : Valued.v y ≤ 1 := by
    have hsplit : y = x' + (y - x') := by ring
    rw [hsplit]
    exact Valuation.map_add_le _ hxle hyU'.le
  have halg : algebraMap K (v.adicCompletion K) k' = (k' : v.adicCompletion K) := rfl
  have hval : Valued.v y = v.valuation K k' := by
    rw [← hk', halg]
    exact HeightOneSpectrum.valuedAdicCompletion_eq_valuation' v k'
  have hk'le : v.valuation K k' ≤ 1 := hval ▸ hyle
  have hk'mem : k' ∈ v.valuationSubringAtPrime K := by
    rw [HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring]
    exact hk'le
  refine ⟨⟨k', hk'mem⟩, ?_⟩
  show Valued.v (x' - (algebraMap K (v.adicCompletion K) k')) < 1
  rw [hk', show x' - y = -(y - x') by ring, Valuation.map_neg]
  exact hyU'

end STEP2CoreWitnessReproduced

section STEP3HasExtensionReproduced

variable {R K : Type*} [CommRing R] [IsDedekindDomain R] [Field K] [Algebra R K]
  [IsFractionRing R K] (v : HeightOneSpectrum R)

instance hasExtension :
    (v.valuation K).HasExtension (Valued.v : Valuation (v.adicCompletion K) ℤᵐ⁰) where
  val_isEquiv_comap := Valuation.IsEquiv.of_eq <| Valuation.ext fun x => by
    rw [Valuation.comap_apply]
    exact (HeightOneSpectrum.valuedAdicCompletion_eq_valuation' v x).symm

end STEP3HasExtensionReproduced

section ResidueBijection

variable {K : Type*} [Field K] [NumberField K] (v : HeightOneSpectrum (𝓞 K))

local notation "K₀" => Valuation.valuationSubring (v.valuation K)
local notation "L₀" =>
  Valuation.valuationSubring (Valued.v : Valuation (v.adicCompletion K) ℤᵐ⁰)

theorem residue_algebraMap_surjective :
    Function.Surjective (algebraMap (IsLocalRing.ResidueField K₀) (IsLocalRing.ResidueField L₀)) := by
  intro b
  obtain ⟨x, rfl⟩ := IsLocalRing.residue_surjective b
  obtain ⟨k, hk⟩ := exists_valuationSubringAtPrime_sub_lt_one v x
  have hk0mem : (k : K) ∈ K₀ := by
    rw [show K₀ = v.valuationSubringAtPrime K from
      (HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring v).symm]
    exact k.2
  set k0 : K₀ := ⟨(k : K), hk0mem⟩ with hk0_def
  have hmem : x - algebraMap K₀ L₀ k0 ∈ IsLocalRing.maximalIdeal L₀ := by
    rw [Valuation.mem_maximalIdeal_iff]
    show Valued.v ((x : v.adicCompletion K) - (algebraMap K₀ L₀ k0 : v.adicCompletion K)) < 1
    have hcoe : (algebraMap K₀ L₀ k0 : v.adicCompletion K) = ((k : K) : v.adicCompletion K) := rfl
    rw [hcoe]
    exact hk
  have heq : IsLocalRing.residue L₀ x = IsLocalRing.residue L₀ (algebraMap K₀ L₀ k0) := by
    have hz : IsLocalRing.residue L₀ (x - algebraMap K₀ L₀ k0) = 0 :=
      (IsLocalRing.residue_eq_zero_iff _).mpr hmem
    rwa [_root_.map_sub, sub_eq_zero] at hz
  exact ⟨IsLocalRing.residue K₀ k0, by
    rw [IsLocalRing.ResidueField.algebraMap_residue, ← heq]⟩

theorem residue_algebraMap_injective :
    Function.Injective (algebraMap (IsLocalRing.ResidueField K₀) (IsLocalRing.ResidueField L₀)) :=
  RingHom.injective (algebraMap (IsLocalRing.ResidueField K₀) (IsLocalRing.ResidueField L₀))

theorem residue_algebraMap_bijective :
    Function.Bijective (algebraMap (IsLocalRing.ResidueField K₀) (IsLocalRing.ResidueField L₀)) :=
  ⟨residue_algebraMap_injective v, residue_algebraMap_surjective v⟩

end ResidueBijection

end STEP4ResidueBijectionReproduced

section STEP5aCompose

/- Reproduced byte-identical from `BSD1Step5Compose.lean`'s own STEP5a
composition (see this file's docstring above for attribution): compose
`equivResidueField_valuationSubring` with the `RingEquiv` induced by
`residue_algebraMap_bijective`, then take `.symm`. `v.adicCompletionIntegers K`
unfolds definitionally to `Valued.v.valuationSubring`, i.e. exactly the `L₀`
that `residue_algebraMap_bijective` is stated for. -/

variable {K : Type*} [Field K] [NumberField K] (v : HeightOneSpectrum (𝓞 K))

noncomputable def equivResidueField_adicCompletionIntegers :
    IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+* (𝓞 K ⧸ v.asIdeal) :=
  ((equivResidueField_valuationSubring v).trans
    (RingEquiv.ofBijective _ (residue_algebraMap_bijective v))).symm

end STEP5aCompose

section STEP5bUniversal

/- Reproduced byte-identical from `BSD1Step5Compose.lean`'s own STEP5b
section (see this file's docstring above for attribution). -/

variable {K : Type*} [Field K] [NumberField K]

theorem residueField_isPrimePow (p : HeightOneSpectrum (𝓞 K)) :
    IsPrimePow (Nat.card (IsLocalRing.ResidueField (p.adicCompletionIntegers K))) := by
  have hcard : Nat.card (IsLocalRing.ResidueField (p.adicCompletionIntegers K)) =
      Nat.card ((𝓞 K) ⧸ p.asIdeal) :=
    Nat.card_congr (equivResidueField_adicCompletionIntegers p).toEquiv
  rw [hcard]
  haveI : Finite ((𝓞 K) ⧸ p.asIdeal) := p.asIdeal.finiteQuotientOfFreeOfNeBot p.ne_bot
  haveI : Fintype ((𝓞 K) ⧸ p.asIdeal) := Fintype.ofFinite _
  haveI : Field ((𝓞 K) ⧸ p.asIdeal) := Ideal.Quotient.field p.asIdeal
  rw [Nat.card_eq_fintype_card]
  exact FiniteField.isPrimePow_card _

end STEP5bUniversal

end BSD1Step5Compose

namespace WeierstrassCurve

/- Reproduced byte-identical from `LFunctionMultiplicativity.lean` /
`BSD1Step5Compose.lean`'s `WeierstrassCurve` section (see this file's
docstring above for attribution) -- needed to state the unconditional
`LFunction_isMultiplicative` theorem this item's corollary depends on. -/

section LocalField

variable {R : Type*} [CommRing R] [IsDomain R] [IsDiscreteValuationRing R] {L : Type*}
  [Field L] [Algebra R L] [IsFractionRing R L] (W : WeierstrassCurve L)

theorem localEulerFactor_isMultiplicative_of_isPrimePow
    (hq : IsPrimePow (Nat.card (IsLocalRing.ResidueField R))) :
    (W.localEulerFactor R).IsMultiplicative := by
  unfold WeierstrassCurve.localEulerFactor
  apply ArithmeticFunction.isMultiplicative_ofPowerSeries_of_isPrimePow _ hq
  unfold WeierstrassCurve.localPowerSeries
  rw [PowerSeries.constantCoeff_invOfUnit]
  simp

end LocalField

section NumberField

variable {K : Type*} [Field K] [NumberField K] (W : WeierstrassCurve K)

theorem LFunction_isMultiplicative_of_residueField_isPrimePow
    (hq : ∀ p : HeightOneSpectrum (𝓞 K),
      IsPrimePow (Nat.card (IsLocalRing.ResidueField (p.adicCompletionIntegers K)))) :
    W.LFunction.IsMultiplicative := by
  unfold WeierstrassCurve.LFunction
  apply ArithmeticFunction.isMultiplicative_eulerProduct
  intro p
  exact localEulerFactor_isMultiplicative_of_isPrimePow _ (hq p)

/-- Reproduced from `BSD1Step5Compose.lean` (Wave-4, `WAVE4-BSD-1-STEP5-COMPOSE`): the
unconditional `LFunction.IsMultiplicative` theorem, no hypothesis, obtained by feeding
`BSD1Step5Compose.residueField_isPrimePow` into
`LFunction_isMultiplicative_of_residueField_isPrimePow`. This is the closed `BSD-GAP-007`
result this Wave-5 item's own new content (below) builds on. -/
theorem LFunction_isMultiplicative : W.LFunction.IsMultiplicative :=
  LFunction_isMultiplicative_of_residueField_isPrimePow W
    (fun p => BSD1Step5Compose.residueField_isPrimePow p)

end NumberField

end WeierstrassCurve

/-! ## `WAVE5-BSD-6` -- the actual new content of this item

Everything above this point is byte-identical reproduction (attributed above) of already-closed
Wave-2/3/4 results, needed only because sibling files in this directory cannot `import` each
other (see this file's docstring). The two declarations below are the falsifiable test this item
was tasked to attempt. -/

namespace WeierstrassCurve

section NumberField

variable {K : Type*} [Field K] [NumberField K] (W : WeierstrassCurve K)

/-- **Minimal scope (`WAVE5-BSD-6`, main reported result).** `W.LFunction` is equal to any other
`ℤ`-valued multiplicative arithmetic function `g` iff the two agree at every prime power. Direct
specialization of `ArithmeticFunction.IsMultiplicative.eq_iff_eq_on_prime_powers`
(`Mathlib/NumberTheory/ArithmeticFunction/Defs.lean:564-573`) to `f := W.LFunction`, discharging
its `hf` hypothesis with the already-closed (`BSD-GAP-007`, Wave-4) `LFunction_isMultiplicative`
above. Purely structural: says nothing about convergence, analytic continuation, a functional
equation, a conductor, or Mordell-Weil rank, and is not claimed as progress toward the Birch and
Swinnerton-Dyer conjecture. -/
theorem LFunction_eq_iff_eq_on_prime_powers (g : ArithmeticFunction ℤ)
    (hg : g.IsMultiplicative) :
    W.LFunction = g ↔ ∀ p i : ℕ, Nat.Prime p → W.LFunction (p ^ i) = g (p ^ i) :=
  IsMultiplicative.eq_iff_eq_on_prime_powers W.LFunction (LFunction_isMultiplicative W) g hg

/-- **Optional extension (`WAVE5-BSD-6`, SEPARATE declaration, own pass/fail check -- do not
claim closed jointly with `LFunction_eq_iff_eq_on_prime_powers` unless both individually pass).**
For `n ≠ 0`, `W.LFunction n` is the product, over the prime factorization of `n`, of
`W.LFunction` evaluated at each prime power factor. Direct specialization of
`ArithmeticFunction.IsMultiplicative.multiplicative_factorization`
(`Mathlib/NumberTheory/ArithmeticFunction/Defs.lean:546-549`) to `f := W.LFunction`, again
discharging `hf` with `LFunction_isMultiplicative`. Same scope disclaimer as above. -/
theorem LFunction_apply_eq_prod_prime_powers {n : ℕ} (hn : n ≠ 0) :
    W.LFunction n = n.factorization.prod fun p k => W.LFunction (p ^ k) :=
  (LFunction_isMultiplicative W).multiplicative_factorization W.LFunction hn

end NumberField

end WeierstrassCurve

#print axioms BSD1Step5Compose.equivResidueField_valuationSubringAtPrime
#print axioms BSD1Step5Compose.equivResidueField_valuationSubring
#print axioms BSD1Step5Compose.exists_valuationSubringAtPrime_sub_lt_one
#print axioms BSD1Step5Compose.hasExtension
#print axioms BSD1Step5Compose.residue_algebraMap_surjective
#print axioms BSD1Step5Compose.residue_algebraMap_injective
#print axioms BSD1Step5Compose.residue_algebraMap_bijective
#print axioms BSD1Step5Compose.equivResidueField_adicCompletionIntegers
#print axioms BSD1Step5Compose.residueField_isPrimePow
#print axioms WeierstrassCurve.localEulerFactor_isMultiplicative_of_isPrimePow
#print axioms WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow
#print axioms WeierstrassCurve.LFunction_isMultiplicative
#print axioms WeierstrassCurve.LFunction_eq_iff_eq_on_prime_powers
#print axioms WeierstrassCurve.LFunction_apply_eq_prod_prime_powers
