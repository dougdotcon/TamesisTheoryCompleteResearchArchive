/-
BSD-1-STEP3-HASEXTENSION -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`BSD1Step1ComposeResidueField.lean`, `BSD1Step2CoreDensityBall.lean`,
`LFunctionMultiplicativity.lean`, `BadReductionValuationBridge.lean`,
`02_NAVIER_STOKES/FORMAL/`).

## What this file is

Wave-1 item BSD-1 (`../BSD-1_GAP_NOTE.md`) diagnosed a genuine gap
(BSD-GAP-007) in proving `WeierstrassCurve.LFunction.IsMultiplicative`:
no bridging lemma in Mathlib shows that the `UniformSpace.Completion`-
based construction `v.adicCompletionIntegers K` has the same residue
field as the pre-completion valuation ring inside `K`. Wave-2 items
`BSD-1-STEP1-COMPOSE` (`BSD1Step1ComposeResidueField.lean`) and
`BSD-1-STEP2-CORE` (`BSD1Step2CoreDensityBall.lean`) each closed one
sub-ingredient of that gap note's step (2)/(3) plan, but explicitly did
**not** compose with each other or attempt the "open maximal ideal" /
residue-field-bijection machinery.

This Wave-3 item, `BSD-1-STEP3-HASEXTENSION`, attacks a different,
narrower ingredient identified by the Onda 3 planning workflow: the
generic `Valuation.HasExtension` typeclass from
`Mathlib/RingTheory/Valuation/Extension.lean`, instantiated for the
concrete pair `(v.valuation K, Valued.v : Valuation (v.adicCompletion K)
ℤᵐ⁰)`. Once available, `HasExtension` unlocks (via
`Valuation.HasExtension.instIsLocalHomValuationInteger`, `Extension.lean:
154-164`, an `@[instance]`-tagged theorem) an `IsLocalHom` instance
between the two valuations' `.integer` subrings -- a prerequisite the
Onda 3 recon flagged as needed for any future residue-field-bijection
step, but which is **not itself** attempted here.

The test, exactly as specified: prove
`(v.valuation K).HasExtension (Valued.v : Valuation (v.adicCompletion K)
ℤᵐ⁰)`, with a preliminary 30-second probe confirming
`IsLocalHom (algebraMap K (v.adicCompletion K))` resolves via
`inferInstance` alone (needed silently by `instIsLocalHomValuationInteger`
alongside `HasExtension` itself).

## Result: it closes, unconditionally, with no forbidden tactics used

Both the probe and the `HasExtension` instance are fully proved below,
in the same general-Dedekind-domain generality as
`BSD1Step1ComposeResidueField.lean` and `BSD1Step2CoreDensityBall.lean`
(`R` a Dedekind domain, `K` its fraction field, `v : HeightOneSpectrum
R`), plus a number-field specialization matching `BSD1Step2CoreDensityBall.lean`'s
pattern. See the end of this file for the `#print axioms` output
actually observed.

## The actual proof shape

`Valuation.HasExtension` (`Extension.lean:66`) unfolds to a single field:
`val_isEquiv_comap : vR.IsEquiv (vA.comap (algebraMap R A))`. Here
`vR := v.valuation K`, `vA := (Valued.v : Valuation (v.adicCompletion K)
ℤᵐ⁰)`, and `algebraMap K (v.adicCompletion K)` is definitionally the
coercion `(↑) : K → v.adicCompletion K`
(`Mathlib/RingTheory/DedekindDomain/AdicValuation.lean`'s
`algebraMap_adicCompletion`, specialized at `S := K` where
`algebraMap K K = RingHom.id K`; this is exactly the fact
`BSD1Step2CoreDensityBall.lean` already isolated and used, verbatim, as
its `halg : algebraMap K (v.adicCompletion K) k' = (k' : v.adicCompletion K) := rfl`).
So `vA.comap (algebraMap K (v.adicCompletion K)) x = Valued.v (x : v.adicCompletion K)`
for every `x : K` (via `Valuation.comap_apply`, itself `rfl`), and this
is *equal* (not merely equivalent) to `v.valuation K x` by
`HeightOneSpectrum.valuedAdicCompletion_eq_valuation'`
(`AdicValuation.lean:945-948`, cited by the Onda 3 recon). Since the two
valuations are literally equal as functions, `Valuation.ext` gives
equality of valuations, and `Valuation.IsEquiv.of_eq` upgrades that
equality to the required `IsEquiv` -- no genuine equivalence-but-not-
equality subtlety arises here, only the pointwise identity already
established for other purposes by `BSD1Step2CoreDensityBall.lean`.

The probe closes via the generic, unconditional instance
`Mathlib/RingTheory/LocalRing/RingHom/Basic.lean:141`: any ring hom out
of a `DivisionRing` into a `Nontrivial` ring is automatically a local
ring hom (`map_nonunit` follows from `isUnit_iff_ne_zero` and injectivity
of the zero-preimage under a division-ring hom). `K` is a `Field` hence
`DivisionRing`, and `v.adicCompletion K` is a `Field` (hence
`Nontrivial`), so `inferInstance` finds it with zero bespoke work, as the
Onda 3 recon predicted.

## What is honestly still NOT done (do not overstate this)

* This file does NOT attempt `BSD-1-STEP4-RESIDUE-BIJECTION` (the
  residue-field surjectivity/bijectivity argument gated on this item),
  nor any composition with `BSD1Step1ComposeResidueField.lean` or
  `BSD1Step2CoreDensityBall.lean`. It only "unblocks"
  `instIsLocalHomValuationInteger` in the sense of making its
  `[vR.HasExtension vS]` hypothesis dischargeable by `inferInstance`; it
  does not itself invoke that instance for any further downstream
  purpose beyond a demonstration `example`.
* This file says nothing about finiteness or `IsPrimePow` of any residue
  field, nor about the "open maximal ideal" half of `BSD-1_GAP_NOTE.md`'s
  step (2). Those remain exactly as open as that note and
  `BSD1Step2CoreDensityBall.lean`'s docstring describe.
* This file makes **zero** claim of novelty and **zero** claim of
  progress toward the Birch and Swinnerton-Dyer conjecture (a Clay
  Millennium Problem). It is reusable, honestly-scoped plumbing
  instantiating a generic Mathlib typeclass for one concrete valuation
  pair, nothing more.
-/

import Mathlib.RingTheory.DedekindDomain.AdicValuation
import Mathlib.RingTheory.Valuation.Extension
import Mathlib.NumberTheory.NumberField.Basic

open IsDedekindDomain NumberField WithZero

namespace BSD1Step3HasExtension

section GeneralDedekindDomain

variable {R K : Type*} [CommRing R] [IsDedekindDomain R] [Field K] [Algebra R K]
  [IsFractionRing R K] (v : HeightOneSpectrum R)

/-- **Preliminary probe**, exactly as recommended by the Onda 3 planning workflow:
`IsLocalHom (algebraMap K (v.adicCompletion K))` resolves via `inferInstance` alone, using the
generic division-ring instance (`Mathlib/RingTheory/LocalRing/RingHom/Basic.lean:141`) and
requiring no bespoke work. Needed silently, alongside `HasExtension` itself, by
`Valuation.HasExtension.instIsLocalHomValuationInteger`. -/
example : IsLocalHom (algebraMap K (v.adicCompletion K)) := inferInstance

/-- **The `BSD-1-STEP3-HASEXTENSION` target.** The `v`-adic valuation `Valued.v` on the
completion `v.adicCompletion K` is an extension (in the `Valuation.HasExtension` sense) of the
pre-completion valuation `v.valuation K` on `K`: pulling `Valued.v` back along the (coercion)
algebra map `K → v.adicCompletion K` recovers `v.valuation K` exactly, not merely up to
equivalence. -/
instance hasExtension :
    (v.valuation K).HasExtension (Valued.v : Valuation (v.adicCompletion K) ℤᵐ⁰) where
  val_isEquiv_comap := Valuation.IsEquiv.of_eq <| Valuation.ext fun x => by
    rw [Valuation.comap_apply]
    exact (HeightOneSpectrum.valuedAdicCompletion_eq_valuation' v x).symm

/-- **Demonstration that this genuinely unblocks `instIsLocalHomValuationInteger`**: with
`hasExtension` and the probe instance above both in scope, the `IsLocalHom` instance between the
two valuations' `.integer` subrings (`Valuation.HasExtension.instIsLocalHomValuationInteger`,
`Extension.lean:154-164`) is now dischargeable by `inferInstance`, with no further hypotheses
supplied by hand. -/
example : IsLocalHom (algebraMap (v.valuation K).integer
    (Valued.v : Valuation (v.adicCompletion K) ℤᵐ⁰).integer) := inferInstance

end GeneralDedekindDomain

section NumberFieldSpecialization

/-- **Literal specialization of the `BSD-1-STEP3-HASEXTENSION` test**, `K` a number field and
`v : HeightOneSpectrum (𝓞 K)`, matching the test statement word for word. Direct corollary of
`hasExtension` above, instantiated at `R := 𝓞 K`. -/
instance hasExtension_numberField {K : Type*} [Field K] [NumberField K]
    (v : HeightOneSpectrum (𝓞 K)) :
    (v.valuation K).HasExtension (Valued.v : Valuation (v.adicCompletion K) ℤᵐ⁰) :=
  hasExtension v

end NumberFieldSpecialization

end BSD1Step3HasExtension

#print axioms BSD1Step3HasExtension.hasExtension
#print axioms BSD1Step3HasExtension.hasExtension_numberField
