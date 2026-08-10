/-
BSD-1-STEP1-COMPOSE -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`LFunctionMultiplicativity.lean`, `BadReductionValuationBridge.lean`,
`CalderonZygmundKernelDefinitions.lean`, `02_NAVIER_STOKES/FORMAL/`).

## What this file is

Wave-1 item BSD-1 (`../BSD-1_GAP_NOTE.md`) diagnosed a genuine gap in
proving `WeierstrassCurve.LFunction.IsMultiplicative`: the residue field
of the `v`-adic completion `v.adicCompletionIntegers K` is not (yet)
known in Mathlib to agree with the residue field `𝓞 K ⧸ v.asIdeal` of
the localization of `𝓞 K` at `v`. That gap note explicitly listed, as
its step (1) of a would-be full proof, the sub-task:

  "A `RingEquiv` (or at least a residue-field-inducing map) between the
  localization of `𝓞 K` at `v` (whose residue field is `𝓞 K ⧸ v.asIdeal`,
  known finite) and `(v.valuation K).integer`/`valuationSubring` -- the
  pre-completion valuation ring inside `K` itself."

This file is a narrowly-scoped Wave-2 follow-on (`BSD-1-STEP1-COMPOSE`)
that attempts *exactly* that sub-task, and nothing else -- it does NOT
touch `adicCompletionIntegers`, `UniformSpace.Completion`, or any of the
harder completion-invariance step (2)/(3) machinery the gap note flagged
as the genuinely open, multi-day part of the problem.

The test: compose two already-proved Mathlib lemmas --
* `IsLocalization.AtPrime.equivQuotMaximalIdeal`
  (`Mathlib/RingTheory/Localization/AtPrime/Basic.lean:559`), instantiated
  with `Rₚ := IsDedekindDomain.HeightOneSpectrum.valuationSubringAtPrime K v`,
  giving `𝓞 K ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField Rₚ`;
* `IsDedekindDomain.HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring`
  (`Mathlib/RingTheory/DedekindDomain/AdicValuation.lean:504-506`),
  `valuationSubringAtPrime K v = (v.valuation K).valuationSubring`;

to transport the first isomorphism along the second equation and obtain
`𝓞 K ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField (v.valuation K).valuationSubring`
-- i.e. the residue field of the *actual* `v`-adic valuation subring of
`K` (not just the localization-at-`v` presentation of it) agrees with
`𝓞 K ⧸ v.asIdeal`.

## Result: it closes, unconditionally, with no forbidden tactics used

Both the direct instantiation and the composed/transported version below
are fully proved. See the end of this file for the `#print axioms`
output actually observed.

## Prerequisites confirmed (matching the adversarial reviewer's narrowed
verdict on this candidate in the Onda 2 planning workflow)

* `Rₚ := valuationSubringAtPrime K v` is a local ring: any
  `ValuationSubring K` (as a type, via its `CoeSort`) carries a generic
  `IsLocalRing` instance (`Mathlib/RingTheory/Valuation/ValuationSubring.lean:148`).
* `Rₚ` carries `IsLocalization (v.asIdeal.primeCompl) Rₚ`
  (`AdicValuation.lean:497`), which is *definitionally* the same
  typeclass as `IsLocalization.AtPrime Rₚ v.asIdeal` (an `abbrev`,
  `Localization/AtPrime/Basic.lean:52`) -- exactly what
  `equivQuotMaximalIdeal` needs.
* `v.asIdeal.IsMaximal` is an existing instance
  (`Mathlib/RingTheory/DedekindDomain/Ideal/Lemmas.lean:504`,
  `HeightOneSpectrum.isMaximal`, from `v.isPrime.isMaximal v.ne_bot` in a
  Dedekind domain) -- exactly what `equivQuotMaximalIdeal` needs for its
  ideal argument `p`.
* `IsLocalRing.ResidueField R := R ⧸ maximalIdeal R` literally, by
  definition (`Mathlib/RingTheory/LocalRing/ResidueField/Defs.lean:30-31`)
  -- so `equivQuotMaximalIdeal`'s codomain `Rₚ ⧸ maximalIdeal Rₚ` is the
  same object as `IsLocalRing.ResidueField Rₚ`, no separate reconciliation
  lemma needed.

## What is honestly still NOT done (do not overstate this)

* This file says nothing about `v.adicCompletionIntegers K`,
  `UniformSpace.Completion`, or finiteness/`IsPrimePow` of any residue
  field. The harder open step from `BSD-1_GAP_NOTE.md` -- showing that
  *completion* (not just localization) preserves the residue field -- is
  **not** attempted here; it remains exactly as open as that note
  describes (see its "Where to pick this up" section, step (2)).
* This file makes **zero** claim of novelty and **zero** claim of
  progress toward the Birch and Swinnerton-Dyer conjecture (a Clay
  Millennium Problem). It is reusable, honestly-scoped plumbing
  connecting the "localization at a prime" and "valuation subring"
  presentations of the same local ring inside a number field, nothing
  more.
-/

import Mathlib.RingTheory.DedekindDomain.AdicValuation
import Mathlib.RingTheory.Localization.AtPrime.Basic

open IsDedekindDomain

namespace BSD1Step1Compose

variable {R K : Type*} [CommRing R] [IsDedekindDomain R] [Field K] [Algebra R K]
  [IsFractionRing R K] (v : HeightOneSpectrum R)

/-- **Direct instantiation.** `IsLocalization.AtPrime.equivQuotMaximalIdeal`, applied with
`Rₚ := HeightOneSpectrum.valuationSubringAtPrime K v`. This alone requires no new work: `Rₚ` is
already known local (`ValuationSubring.isLocalRing`) and already carries the required
`IsLocalization.AtPrime` instance (`AdicValuation.lean:497`, definitionally an
`IsLocalization (v.asIdeal.primeCompl) Rₚ` instance since `IsLocalization.AtPrime` is an
`abbrev` for exactly that), and `v.asIdeal.IsMaximal` is an existing instance. -/
noncomputable def equivResidueField_valuationSubringAtPrime :
    R ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField (v.valuationSubringAtPrime K) :=
  IsLocalization.AtPrime.equivQuotMaximalIdeal v.asIdeal (v.valuationSubringAtPrime K)

/-- **Composed/transported version**, the actual `BSD-1-STEP1-COMPOSE` target: transport
`equivResidueField_valuationSubringAtPrime` along
`HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring` (`valuationSubringAtPrime K v =
(v.valuation K).valuationSubring`) to land on the residue field of the *actual* `v`-adic valuation
subring of `K`, closing exactly the sub-task step (1) that `../BSD-1_GAP_NOTE.md` flagged as
needed for a full proof of the finiteness side condition. -/
noncomputable def equivResidueField_valuationSubring :
    R ⧸ v.asIdeal ≃+* IsLocalRing.ResidueField (v.valuation K).valuationSubring := by
  rw [← HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring (R := R) (K := K) v]
  exact equivResidueField_valuationSubringAtPrime v

end BSD1Step1Compose

#print axioms BSD1Step1Compose.equivResidueField_valuationSubringAtPrime
#print axioms BSD1Step1Compose.equivResidueField_valuationSubring
