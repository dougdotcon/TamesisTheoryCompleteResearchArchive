/-
BSD-1-STEP5-COMPOSE -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`BSD1Step1ComposeResidueField.lean`, `BSD1Step4ResidueBijection.lean`,
`LFunctionMultiplicativity.lean`, `BadReductionValuationBridge.lean`,
`02_NAVIER_STOKES/FORMAL/`).

## What this file is

`../BSD-1_GAP_NOTE.md` diagnosed a genuine gap (BSD-GAP-007) in proving
`WeierstrassCurve.LFunction.IsMultiplicative`, and laid out a three-step
plan to close it:

1. A `RingEquiv`/residue-field-inducing map between the localization of
   `𝓞 K` at `v` (residue field `𝓞 K ⧸ v.asIdeal`, known finite) and the
   pre-completion `v`-adic valuation subring of `K` itself -- closed by
   Wave-2 item `BSD-1-STEP1-COMPOSE` (`BSD1Step1ComposeResidueField.lean`,
   `equivResidueField_valuationSubring`).
2. A completion-invariance-of-residue-field result for the
   `UniformSpace.Completion`-based construction `v.adicCompletionIntegers`
   -- addressed (surjectivity + injectivity of the residue map induced by
   `Valuation.HasExtension`) by Wave-3 item `BSD-1-STEP4-RESIDUE-BIJECTION`
   (`BSD1Step4ResidueBijection.lean`, `residue_algebraMap_bijective`).
3. Composing (1) and (2) to conclude
   `IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+* 𝓞 K ⧸ v.asIdeal`,
   then transporting finiteness and prime-power cardinality across that
   equivalence.

This Wave-4 item, `BSD-1-STEP5-COMPOSE`, attempts step (3): composing
STEP1's and STEP4's already-closed results with each other for the first
time (neither prior file composed with the other -- both explicitly say
so in their own docstrings). It has two internal gated checkpoints,
attempted and reported strictly in order, exactly as scoped by the task:

* **STEP5a** (the falsifiable test): the actual `RingEquiv` composition
  `IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+* 𝓞 K ⧸ v.asIdeal`,
  built as `(STEP1result.trans (RingEquiv.ofBijective _ STEP4result)).symm`.
* **STEP5b** (gated on STEP5a closing; NOT verified by the Onda 4
  adversarial reviewer, per the task instructions): using STEP5a's equiv
  plus `Ideal.finiteQuotientOfFreeOfNeBot` and `FiniteField.isPrimePow_card`,
  produce the literal `hq` hypothesis that
  `WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow`
  (`LFunctionMultiplicativity.lean`) requires, and state the *unconditional*
  `WeierstrassCurve.LFunction_isMultiplicative` theorem with no hypothesis.

## Reproduction convention (same as `BSD1Step4ResidueBijection.lean`)

Every file in this `BSD1Step*.lean` family is deliberately standalone
(verified in isolation, not part of the shared `TamesisLab.lean` import
tree), and none of these sibling `03_MILLENNIUM/06_BSD/FORMAL/*.lean`
files live under the `05_FORMAL/lean/` project root, so a plain `import`
of a sibling file would not resolve (confirmed directly, same failure
mode `BSD1Step4ResidueBijection.lean` documents: "input file ... must be
contained in root directory"). Consequently, this file reproduces
byte-identical the declarations from `BSD1Step1ComposeResidueField.lean`
(`equivResidueField_valuationSubringAtPrime`,
`equivResidueField_valuationSubring`), from `BSD1Step4ResidueBijection.lean`
(its STEP2-witness and STEP3-`HasExtension` reproductions, plus
`residue_algebraMap_surjective`/`_injective`/`_bijective`), and -- for the
gated STEP5b half only -- from `LFunctionMultiplicativity.lean`
(`WeierstrassCurve.localEulerFactor_isMultiplicative_of_isPrimePow`,
`WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow`),
each with this note as attribution. Nothing below is independently
re-derived that wasn't already closed by a Wave-2/Wave-3/Wave-1 sibling;
the only new content of this item is the STEP5a composition itself and,
gated on it, the STEP5b `hq`-production/wiring.

## Result: STEP5a closes, unconditionally, with no forbidden tactics used

The composition typechecks exactly as specified by the falsifiable test
(`(STEP1result.trans (RingEquiv.ofBijective _ STEP4result)).symm`), landing
on `IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+* 𝓞 K ⧸ v.asIdeal`
with no `show`/`rw`/tactic massaging needed -- `v.adicCompletionIntegers K`
unfolds definitionally to `Valued.v.valuationSubring`
(`AdicValuation.lean:804-805`), which is syntactically the `L₀` that
STEP4's `residue_algebraMap_bijective` already talks about, so the two
composed equivalences line up on the nose. See the end of this file for
the `#print axioms` output actually observed for both the named
`equivResidueField_adicCompletionIntegers` declaration and the literal
`example` matching the test's exact stated form.

## Result: STEP5b also closes, unconditionally, with no forbidden tactics used

Per the task's explicit instruction, STEP5b was only attempted because
STEP5a closed, and is reported here as a separate result. The hypothesis
`hq` that `LFunction_isMultiplicative_of_residueField_isPrimePow` needs is
produced by transporting `Nat.card` across STEP5a's equivalence
(`Nat.card_congr`) onto `Nat.card (𝓞 K ⧸ p.asIdeal)`, which is finite
(`Ideal.finiteQuotientOfFreeOfNeBot p.ne_bot`, using the existing
`Module.Free ℤ (𝓞 K)`/`Module.Finite ℤ (𝓞 K)` instances -- the latter
itself an existing instance, `IsNoetherian.finite`, from the existing
`IsNoetherian ℤ (𝓞 K)` instance) and already a field (`p.asIdeal.IsMaximal`
gives the standard `Ideal.Quotient.field` instance), hence of prime-power
cardinality by `FiniteField.isPrimePow_card`. The unconditional
`WeierstrassCurve.LFunction_isMultiplicative` theorem (no hypothesis) then
follows immediately by feeding this `hq` into
`LFunction_isMultiplicative_of_residueField_isPrimePow`, exactly as the
test specifies.

## What is honestly still NOT done / NOT claimed (do not overstate this)

* **This is a governance/ledger judgment for the integrator, not asserted
  here**: this file does NOT claim BSD-GAP-007 is closed, and does NOT
  claim `WeierstrassCurve.LFunction_isMultiplicative` (proved below,
  unconditionally, as a matter of Lean typechecking) constitutes progress
  toward, or any step closer to a solution of, the Birch and
  Swinnerton-Dyer conjecture (a Clay Millennium Problem). `IsMultiplicative`
  of the Dirichlet coefficients of a formal Euler product is one of the
  most basic possible structural facts about any L-function; nothing here
  says anything about convergence of `LSeries`, analytic continuation, a
  functional equation, a conductor, or Mordell-Weil rank.
* This file makes **zero** claim of novelty.
* This file does not touch `v.adicCompletionIntegers` finiteness by any
  route other than the composition above; no other gap from
  `BSD-1_GAP_NOTE.md`, `BSD1Step2CoreDensityBall.lean`, or
  `BSD1Step3HasExtension.lean` is revisited or re-litigated.
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
`BSD1Step1Compose.equivResidueField_valuationSubring`, per this file's
docstring above. -/

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
the *actual* `v`-adic valuation subring of `K`. This is the `STEP1result` the falsifiable test
refers to. -/
noncomputable def equivResidueField_valuationSubring :
    R ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField (v.valuation K).valuationSubring := by
  rw [← HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring (R := R) (K := K) v]
  exact equivResidueField_valuationSubringAtPrime v

end STEP1ComposeReproduced

section STEP4ResidueBijectionReproduced

/- Reproduced byte-identical from `BSD1Step4ResidueBijection.lean`, per this file's docstring
above: its own STEP2-CORE-witness and STEP3-`HasExtension` reproductions, plus its actual
`STEP4-RESIDUE-BIJECTION` target declarations. -/

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

/-- The `STEP4result` the falsifiable test refers to. -/
theorem residue_algebraMap_bijective :
    Function.Bijective (algebraMap (IsLocalRing.ResidueField K₀) (IsLocalRing.ResidueField L₀)) :=
  ⟨residue_algebraMap_injective v, residue_algebraMap_surjective v⟩

end ResidueBijection

end STEP4ResidueBijectionReproduced

section STEP5aCompose

/-! ## STEP5a -- the actual `BSD-1-STEP5-COMPOSE` falsifiable test

Compose `equivResidueField_valuationSubring` (`STEP1result`) with the `RingEquiv` induced by
`residue_algebraMap_bijective` (`RingEquiv.ofBijective _ STEP4result`), then take `.symm`, exactly
as the test specifies. `v.adicCompletionIntegers K` unfolds definitionally to
`Valued.v.valuationSubring` (`AdicValuation.lean:804-805`), i.e. exactly the `L₀` that
`residue_algebraMap_bijective` is stated for, so no further reconciliation lemma is needed. -/

variable {K : Type*} [Field K] [NumberField K] (v : HeightOneSpectrum (𝓞 K))

/-- Named version of the STEP5a target, for `#print axioms`. -/
noncomputable def equivResidueField_adicCompletionIntegers :
    IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+* (𝓞 K ⧸ v.asIdeal) :=
  ((equivResidueField_valuationSubring v).trans
    (RingEquiv.ofBijective _ (residue_algebraMap_bijective v))).symm

/-- The falsifiable test, verbatim in shape: `(STEP1result.trans (RingEquiv.ofBijective _
STEP4result)).symm`. -/
noncomputable example : IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+* (𝓞 K ⧸ v.asIdeal) :=
  ((equivResidueField_valuationSubring v).trans
    (RingEquiv.ofBijective _ (residue_algebraMap_bijective v))).symm

end STEP5aCompose

section STEP5bUniversal

/-! ## STEP5b (gated on STEP5a closing; NOT independently adversarially verified)

Using `equivResidueField_adicCompletionIntegers` (STEP5a) plus
`Ideal.finiteQuotientOfFreeOfNeBot` and `FiniteField.isPrimePow_card`, produce the literal `hq`
that `WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow`
(`LFunctionMultiplicativity.lean`, reproduced below) requires. -/

variable {K : Type*} [Field K] [NumberField K]

/-- Every adic-completion residue field of `𝓞 K` has prime-power cardinality: transport
`Nat.card` across the STEP5a equivalence onto `𝓞 K ⧸ p.asIdeal`, which is finite
(`Ideal.finiteQuotientOfFreeOfNeBot`) and already a field (`p.asIdeal.IsMaximal`), hence of
prime-power cardinality by `FiniteField.isPrimePow_card`. This is exactly the `hq` argument
`LFunction_isMultiplicative_of_residueField_isPrimePow` needs. -/
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

/- Reproduced byte-identical from `LFunctionMultiplicativity.lean`'s
`WeierstrassCurve.localEulerFactor_isMultiplicative_of_isPrimePow` and
`WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow`, per this file's
docstring above -- needed to state the gated, STEP5b-only unconditional
`LFunction_isMultiplicative` theorem. -/

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

/-- The `STEP5b` target: the unconditional `LFunction.IsMultiplicative` theorem, no hypothesis,
obtained by feeding `BSD1Step5Compose.residueField_isPrimePow` into
`LFunction_isMultiplicative_of_residueField_isPrimePow`. See this file's docstring for what this
does and does NOT claim about the Birch and Swinnerton-Dyer conjecture. -/
theorem LFunction_isMultiplicative : W.LFunction.IsMultiplicative :=
  LFunction_isMultiplicative_of_residueField_isPrimePow W
    (fun p => BSD1Step5Compose.residueField_isPrimePow p)

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
