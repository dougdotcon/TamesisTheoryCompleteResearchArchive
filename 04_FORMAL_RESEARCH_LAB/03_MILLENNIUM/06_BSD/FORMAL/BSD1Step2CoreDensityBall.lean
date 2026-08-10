/-
BSD-1-STEP2-CORE -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`BSD1Step1ComposeResidueField.lean`, `LFunctionMultiplicativity.lean`,
`BadReductionValuationBridge.lean`, `02_NAVIER_STOKES/FORMAL/`).

## What this file is

Wave-1 item BSD-1 (`../BSD-1_GAP_NOTE.md`) diagnosed a genuine gap in
proving `WeierstrassCurve.LFunction.IsMultiplicative`: no bridging lemma
in Mathlib shows that the `UniformSpace.Completion`-based construction
`v.adicCompletionIntegers K` has the same residue field as the
pre-completion valuation ring inside `K`. That note's "Where to pick
this up" section named step (2) of a would-be full proof as: "a
completion-invariance-of-residue-field lemma ... (dense image + open
maximal ideal ⟹ residue field bijection with the pre-completion residue
field)".

`BSD-1-STEP1-COMPOSE` (`BSD1Step1ComposeResidueField.lean`, this same
Wave-2 batch) closed step (1): identifying the pre-completion valuation
ring `valuationSubringAtPrime K v` with `(v.valuation K).valuationSubring`
and showing its residue field is `𝓞 K ⧸ v.asIdeal`.

This file, `BSD-1-STEP2-CORE`, is a narrowly-scoped follow-on that
attempts *exactly* the density-ball half of step (2)'s "dense image"
ingredient, and nothing else -- it does NOT attempt to produce an actual
`𝓞 K`-element `y` (only a `valuationSubringAtPrime K v`-element `k`), does
NOT attempt the "open maximal ideal" half (the fact that the maximal
ideal of `adicCompletionIntegers K v` is open, which is a separate,
harder ingredient needed to turn this ball-approximation into an actual
residue-field bijection), and does NOT compose this with STEP1's result.
Exactly per the Onda 2 planning workflow's narrowed instruction: "Nao
tentar produzir y : O_K diretamente nesta etapa."

The test, exactly as specified: for `K` a number field, `v :
HeightOneSpectrum (𝓞 K)`, `x : v.adicCompletionIntegers K`, prove there
exists `k : v.valuationSubringAtPrime K` with
`Valued.v ((x : v.adicCompletion K) - (k : v.adicCompletion K)) < 1`,
via `IsDedekindDomain.HeightOneSpectrum.denseRange_algebraMap` +
`Valued.isOpen_ball` (openness of the unit ball) +
`Valuation.mem_valuationSubring_iff`/`Valuation.map_add_le` (to certify
the dense-range witness itself lands in the valuation subring, not just
somewhere in `K`).

## Result: it closes, unconditionally, with no forbidden tactics used

Both the general-Dedekind-domain version (matching the generality of
`BSD1Step1ComposeResidueField.lean`) and the literal number-field
specialization asked for by the test are proved below. See the end of
this file for the `#print axioms` output actually observed.

## The actual proof shape (why `denseRange_algebraMap` alone is not enough)

`IsDedekindDomain.HeightOneSpectrum.denseRange_algebraMap` only gives
`DenseRange (algebraMap K (v.adicCompletion K))` -- density of *all* of
`K`, not of the valuation subring `valuationSubringAtPrime K v`. A priori
the point of `K` that density hands back for a given open neighbourhood
of `x` could have valuation `> 1` (i.e. not lie in the subring at all),
so producing `k : v.valuationSubringAtPrime K` (not just `k' : K`) is a
genuine extra step, not automatic from `denseRange_algebraMap` alone.
The extra step used here is the non-archimedean triangle inequality:
since `x` is already an integer (`Valued.v (x : v.adicCompletion K) ≤ 1`)
and the dense-range witness `y` satisfies `Valued.v (y - x) < 1` (hence
`≤ 1`), `Valuation.map_add_le` applied to `y = x + (y - x)` forces
`Valued.v y ≤ 1` as well -- so the *specific* witness density hands back
for *this* target `x` is automatically forced into the subring, even
though `denseRange_algebraMap`'s range is not restricted to it. This
`Valued.v y ≤ 1` is then transported back along
`HeightOneSpectrum.valuedAdicCompletion_eq_valuation'` and
`Valuation.mem_valuationSubring_iff` (composed with
`HeightOneSpectrum.valuationSubringAtPrime_eq_valuationSubring`, the same
identification lemma `BSD1Step1ComposeResidueField.lean` uses) to certify
`k' ∈ v.valuationSubringAtPrime K`.

Openness of the unit ball `{y | Valued.v y < 1}` (needed to get an actual
`𝓝 x`-neighbourhood to feed to `DenseRange`/`mem_closure_iff_nhds`) comes
from `Valued.isOpen_ball (v.adicCompletion K) (1 : ValueGroup₀ ...)`,
which is stated in terms of the auxiliary `Valuation.restrict` used
internally for the topology; `Valuation.restrict_lt_one_iff` (a `simp`
lemma) reconciles it with the literal `Valued.v y < 1` statement the rest
of the proof works with. The shifted ball around `x` (rather than `0`) is
then obtained as the preimage of that ball under the continuous
subtraction map `fun y => y - x`.

## What is honestly still NOT done (do not overstate this)

* This file produces `k : v.valuationSubringAtPrime K` (a pre-completion,
  `K`-side object), exactly as the narrowed test asked. It does NOT
  produce `y : 𝓞 K` -- going from `valuationSubringAtPrime` (a
  localization of `𝓞 K` at `v`, i.e. a ring containing `𝓞 K` with
  finitely many extra inverted elements adjoined) down to an actual
  `𝓞 K`-element is a separate step, deliberately out of scope here per
  the Onda 2 planning workflow's instruction.
* This file says nothing about the maximal ideal of
  `v.adicCompletionIntegers K` being open (the other half of step (2)'s
  "dense image + open maximal ideal" recipe from `BSD-1_GAP_NOTE.md`), nor
  about turning this ball-approximation into an actual residue-field
  bijection/equivalence. Those remain exactly as open as
  `BSD-1_GAP_NOTE.md` describes.
* This file does NOT compose with `BSD1Step1ComposeResidueField.lean`'s
  result; the two are independent, narrowly-scoped Wave-2 items that
  happen to both bear on the same Wave-1 gap.
* This file makes **zero** claim of novelty and **zero** claim of
  progress toward the Birch and Swinnerton-Dyer conjecture (a Clay
  Millennium Problem). It is reusable, honestly-scoped plumbing about a
  density-ball approximation, nothing more.
-/

import Mathlib.RingTheory.DedekindDomain.AdicValuation
import Mathlib.NumberTheory.NumberField.Basic

open IsDedekindDomain NumberField

namespace BSD1Step2Core

section GeneralDedekindDomain

variable {R K : Type*} [CommRing R] [IsDedekindDomain R] [Field K] [Algebra R K]
  [IsFractionRing R K] (v : HeightOneSpectrum R)

/-- **The `BSD-1-STEP2-CORE` target, general-Dedekind-domain version** (matching the generality
of `BSD1Step1ComposeResidueField.lean`): every integral point `x` of the `v`-adic completion is
within an open unit ball of some point coming from the pre-completion valuation subring
`v.valuationSubringAtPrime K` (not merely from `K` at large -- see the file docstring for why
that extra containment is the actual content of this lemma, beyond bare density). -/
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

end GeneralDedekindDomain

section NumberFieldSpecialization

/-- **Literal specialization of the `BSD-1-STEP2-CORE` test**, `K` a number field and
`v : HeightOneSpectrum (𝓞 K)`, matching the test statement word for word. Direct corollary of
`exists_valuationSubringAtPrime_sub_lt_one` above, instantiated at `R := 𝓞 K`. -/
theorem exists_valuationSubringAtPrime_sub_lt_one_numberField {K : Type*} [Field K]
    [NumberField K] (v : HeightOneSpectrum (𝓞 K)) (x : v.adicCompletionIntegers K) :
    ∃ k : v.valuationSubringAtPrime K,
      Valued.v ((x : v.adicCompletion K) - ((k : K) : v.adicCompletion K)) < 1 :=
  exists_valuationSubringAtPrime_sub_lt_one v x

end NumberFieldSpecialization

end BSD1Step2Core

#print axioms BSD1Step2Core.exists_valuationSubringAtPrime_sub_lt_one
#print axioms BSD1Step2Core.exists_valuationSubringAtPrime_sub_lt_one_numberField
