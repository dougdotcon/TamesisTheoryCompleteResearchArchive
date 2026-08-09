/-
BSD-BAD-PRIMES-FINITE-001 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's Mathlib
checkout, outside the shared import tree (same convention as
`LFunctionMultiplicativity.lean`, `CalderonZygmundKernelDefinitions.lean`,
`02_NAVIER_STOKES/FORMAL/`).

## What this file is

The original goal behind this item was the finiteness of the bad-reduction locus
of a Weierstrass curve over a number field `K`: for all but finitely many
`p : IsDedekindDomain.HeightOneSpectrum (𝓞 K)`, the base change of `W` to the
`p`-adic completion has good reduction, in the sense of
`WeierstrassCurve.HasGoodReduction` from
`Mathlib/AlgebraicGeometry/EllipticCurve/Reduction.lean:281-282` (Bryan Wang,
2025), which is stated over an *abstract* discrete valuation ring `R` via
`valuation K (maximalIdeal R) W.Δ = 1` -- `maximalIdeal R` here being
`IsDiscreteValuationRing.maximalIdeal R : HeightOneSpectrum R`, the *reconstructed*
`HeightOneSpectrum` of the abstract DVR `R` itself (see
`Mathlib/RingTheory/Valuation/Discrete/IsDiscreteValuationRing.lean:41`).

Reduction theory is applied to `R := p.adicCompletionIntegers K` (the valuation
subring of `p`'s adic completion `p.adicCompletion K`), which Mathlib already
knows is a discrete valuation ring
(`Mathlib/NumberTheory/NumberField/Completion/FinitePlace.lean:76`) with fraction
field `p.adicCompletion K`
(`Mathlib/RingTheory/Valuation/ValuationSubring.lean:153`, the generic
`IsFractionRing` instance for any `ValuationSubring`). The global finiteness
statement, however, needs to talk about divisibility of `W.Δ` by `p` as a prime
of the *global* ring `𝓞 K` (so that
`Mathlib/RingTheory/DedekindDomain/Factorization.lean`'s finite-support machinery
applies) -- i.e. it needs the reconstructed *local* valuation
`(IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K)).valuation
(p.adicCompletion K)` used by `HasGoodReduction` to agree with plain ideal
membership `_ ∈ p.asIdeal` in `𝓞 K`. Per the adversarial reviewer's verdict, this
compatibility is not glue code -- it is a genuine bridge between two
independently-built corners of Mathlib (the abstract-DVR reduction-theory
valuation vs. the Dedekind-domain/adic-completion global valuation), and the
reviewer's narrowed instruction was to attempt **only this bridge lemma**, fully
decoupled from `HasGoodReduction`/`Reduction.lean`, before attempting anything
about `WeierstrassCurve` or bad-reduction loci at all.

## Result: the bridge closes, unconditionally, with no forbidden tactics or
declarations used (checked directly, see the end of this file)

Three lemmas below, chained together, give exactly the compatibility the
reviewer asked to be tested in isolation:

1. `global_bridge`: `Valued.v (y : p.adicCompletion K) < 1 ↔ y ∈ p.asIdeal`, for
   `y : 𝓞 K` -- the `Valued` instance on the completion (built into
   `p.adicCompletion K` itself, `Mathlib/RingTheory/DedekindDomain/
   AdicValuation.lean:708`) agrees with plain divisibility of `y` by `p` in
   `𝓞 K`. Proof: `HeightOneSpectrum.valuedAdicCompletion_eq_valuation'`
   (`AdicValuation.lean:945`) plus `HeightOneSpectrum.valuation_of_algebraMap`
   and `HeightOneSpectrum.intValuation_lt_one_iff_mem`
   (`AdicValuation.lean:341,357`) applied to the *global* `p : HeightOneSpectrum
   (𝓞 K)`.
2. `local_bridge`: for `y : 𝓞 K` and a proof `hy` that its image lands in
   `p.adicCompletionIntegers K`, the *reconstructed* local valuation
   `(IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K)).valuation
   (p.adicCompletion K)` agrees with `Valued.v` on that element. Proof: chains
   the *generic* fact that any DVR's reconstructed `HeightOneSpectrum.valuation`
   detects membership in its own maximal ideal
   (`HeightOneSpectrum.valuation_lt_one_iff_mem`, general for any DVR, applied
   here with the DVR instantiated as `p.adicCompletionIntegers K`) together with
   the *generic* `ValuationSubring` fact that "non-unit of `v.valuationSubring`"
   is equivalent to "`v _ < 1`" (`Valuation.mem_maximalIdeal_iff`,
   `Mathlib/RingTheory/Valuation/ValuationSubring.lean:882`), using that
   `p.adicCompletionIntegers K` unfolds to `Valued.v.valuationSubring`
   (`AdicValuation.lean:804`) definitionally.
3. `finiteness_bridge` / `finiteness_bridge'`: the composition of (1) and (2),
   discharging the side condition `hy` automatically via
   `HeightOneSpectrum.coe_mem_adicCompletionIntegers`
   (`AdicValuation.lean:812`, "a global integer is in the local integers") so
   that the final statement needs no hypothesis beyond `y : 𝓞 K`.

Nothing here required `IsIntegral (𝓞 K) W)`, `nonzero`, or characteristic
hypotheses -- the chain works for every `y : 𝓞 K` including `y = 0` (both
`intValuation_lt_one_iff_mem` and membership in `p.asIdeal` are trivially true
there), which is what one wants for a compatibility lemma meant to be plugged
into `W.Δ` later without extra side conditions.

## What is honestly still NOT done (do not overstate this)

* **The original finiteness theorem itself is NOT proved here.** This file says
  nothing about `WeierstrassCurve`, `HasGoodReduction`, `W.Δ`, or
  `HasFiniteMulSupport`/`Ideal.finite_factors`
  (`Mathlib/RingTheory/DedekindDomain/Factorization.lean:84,112`). Finishing the
  original goal would still require: (a) instantiating `y := W.Δ` (or rather the
  numerator of an integral model's discriminant) in `finiteness_bridge'`, (b)
  relating `HasGoodReduction R W ↔ ¬ p ∣ (Δ)` using this bridge plus
  `hasGoodReduction_iff` from `Reduction.lean`, and (c) invoking
  `HasFiniteMulSupport`/`Ideal.finite_factors` on `Ideal.span {Δ_numerator}`.
  None of (a)-(c) is attempted here; per the task's explicit scope limit, this
  file attempts *only* the isolated bridge lemma the reviewer asked for.
* This file makes **zero** claim of novelty and **zero** claim of progress
  toward the Birch and Swinnerton-Dyer conjecture (a Clay Millennium Problem).
  It says nothing about conductors, analytic continuation, functional
  equations, or Mordell-Weil rank. It is reusable, honestly-scoped plumbing
  connecting two corners of Mathlib's valuation theory, nothing more.
-/

import Mathlib.RingTheory.DedekindDomain.AdicValuation
import Mathlib.RingTheory.Valuation.Discrete.IsDiscreteValuationRing
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace
import Mathlib.NumberTheory.NumberField.Basic

open IsDedekindDomain NumberField

namespace BSDBadPrimesFinite

variable {K : Type*} [Field K] [NumberField K] (p : HeightOneSpectrum (𝓞 K))

/-- **Global half of the bridge.** The `Valued` instance carried by the adic
completion `p.adicCompletion K` (built into the completion itself, not
reconstructed) agrees with plain ideal membership of `y` at `p` in `𝓞 K`.
This is essentially already-available Mathlib API
(`valuedAdicCompletion_eq_valuation'` + `intValuation_lt_one_iff_mem`), recorded
here as one clean statement for use in `finiteness_bridge`. -/
theorem global_bridge (y : 𝓞 K) :
    Valued.v (y : p.adicCompletion K) < 1 ↔ y ∈ p.asIdeal := by
  have h := HeightOneSpectrum.valuedAdicCompletion_eq_valuation' (R := 𝓞 K) (K := K) p
    (algebraMap (𝓞 K) K y)
  have hcoe : ((algebraMap (𝓞 K) K y : K) : p.adicCompletion K) = (y : p.adicCompletion K) := by
    simp
  rw [hcoe] at h
  rw [h, HeightOneSpectrum.valuation_of_algebraMap]
  exact HeightOneSpectrum.intValuation_lt_one_iff_mem p y

/-- **Local half of the bridge.** This is the genuinely non-trivial compatibility
the adversarial reviewer flagged: the *reconstructed* `HeightOneSpectrum`
valuation of the discrete valuation ring `p.adicCompletionIntegers K`
(`IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K)`, exactly
what `WeierstrassCurve.HasGoodReduction` uses when instantiated at this DVR)
agrees with the completion's own `Valued.v` instance on elements of that DVR.
These are, a priori, two independently-constructed valuations on
`p.adicCompletion K` that merely happen to share the same valuation subring; the
proof goes through the generic facts that (i) any DVR's reconstructed valuation
detects its own maximal ideal, and (ii) a `Valuation`'s own valuation subring's
non-units are exactly the elements of valuation `< 1`. -/
theorem local_bridge (y : 𝓞 K)
    (hy : (y : p.adicCompletion K) ∈ p.adicCompletionIntegers K) :
    (IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K)).valuation
        (p.adicCompletion K) (⟨(y : p.adicCompletion K), hy⟩ : p.adicCompletionIntegers K) < 1
      ↔ Valued.v (y : p.adicCompletion K) < 1 :=
  (HeightOneSpectrum.valuation_lt_one_iff_mem
      (IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K))
      (⟨(y : p.adicCompletion K), hy⟩ : p.adicCompletionIntegers K)).trans
    (Valuation.mem_maximalIdeal_iff (v := Valued.v)
      (a := (⟨(y : p.adicCompletion K), hy⟩ : p.adicCompletionIntegers K)))

/-- **Full bridge**, conditional on the (always-true, see `finiteness_bridge'`)
side fact that `y`'s image lies in the local integers. Composes `local_bridge`
and `global_bridge`: the reduction-theory valuation used by `HasGoodReduction`
at `p` agrees, on global integers, with plain divisibility by `p` in `𝓞 K`. -/
theorem finiteness_bridge (y : 𝓞 K)
    (hy : (y : p.adicCompletion K) ∈ p.adicCompletionIntegers K) :
    (IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K)).valuation
        (p.adicCompletion K) (⟨(y : p.adicCompletion K), hy⟩ : p.adicCompletionIntegers K) < 1
      ↔ y ∈ p.asIdeal :=
  (local_bridge p y hy).trans (global_bridge p y)

/-- **Unconditional final form.** Same statement as `finiteness_bridge`, with the
side hypothesis discharged automatically via
`HeightOneSpectrum.coe_mem_adicCompletionIntegers` ("a global integer is in the
local integers"), so no hypothesis beyond `y : 𝓞 K` remains. This is the exact
compatibility fact that would let a future `HasGoodReduction`-based finiteness
theorem for the bad-reduction locus reduce to
`Mathlib.RingTheory.DedekindDomain.Factorization`'s `Ideal.finite_factors` /
`HasFiniteMulSupport`, once `y` is instantiated to (the numerator of) a
Weierstrass discriminant -- that instantiation is NOT carried out in this file
(see the file docstring). -/
theorem finiteness_bridge' (y : 𝓞 K) :
    (IsDiscreteValuationRing.maximalIdeal (p.adicCompletionIntegers K)).valuation
        (p.adicCompletion K)
        (⟨(y : p.adicCompletion K),
          HeightOneSpectrum.coe_mem_adicCompletionIntegers (R := 𝓞 K) p y⟩ :
          p.adicCompletionIntegers K) < 1
      ↔ y ∈ p.asIdeal :=
  finiteness_bridge p y (HeightOneSpectrum.coe_mem_adicCompletionIntegers (R := 𝓞 K) p y)

end BSDBadPrimesFinite

#print axioms BSDBadPrimesFinite.global_bridge
#print axioms BSDBadPrimesFinite.local_bridge
#print axioms BSDBadPrimesFinite.finiteness_bridge
#print axioms BSDBadPrimesFinite.finiteness_bridge'
