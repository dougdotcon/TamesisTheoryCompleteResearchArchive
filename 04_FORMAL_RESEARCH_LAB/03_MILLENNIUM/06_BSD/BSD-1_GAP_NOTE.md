# BSD-1 gap note: `WeierstrassCurve.LFunction.IsMultiplicative`

Item: **BSD-L-MULT-001** (Wave-1 batch, code `BSD-1`).
File produced alongside this note: `FORMAL/LFunctionMultiplicativity.lean`.

## What was attempted

Per the adversarial reviewer's narrowed test, the isolated side-condition
lemma was attempted **first, in isolation, before touching
`IsMultiplicative`**:

```
example {K} [Field K] [NumberField K] (v : IsDedekindDomain.HeightOneSpectrum (𝓞 K)) :
    Finite (IsLocalRing.ResidueField (v.adicCompletionIntegers K)) := by
  infer_instance
```

(equivalently `IsPrimePow (Nat.card (IsLocalRing.ResidueField (v.adicCompletionIntegers K)))`).

## Result: it does not close

`infer_instance` fails with:

```
failed to synthesize instance of type class
  Finite (IsLocalRing.ResidueField ↥(HeightOneSpectrum.adicCompletionIntegers K v))
```

This is a genuine, reproducible failure (checked directly with
`lake env lean` against the project's Mathlib, exit code 1 for the probe
file), not a speculation. It confirms the reviewer's independent
re-verification of the recon's flagged "connective step."

## Why: exhaustive search confirms no bridging lemma exists

Three independent checks, all negative:

1. **Direct grep for any co-occurrence.** Across the entire Mathlib
   checkout, the only `.lean` file that mentions both `adicCompletion`
   and `ResidueField`/`residue` is
   `Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean` itself (the
   file whose definition this item is trying to reason about). No
   supporting lemma exists anywhere else in the library.

2. **The one candidate transport lemma is for a different completion
   construction.** `AdicCompletion.residueField_map_bijective` in
   `Mathlib/RingTheory/AdicCompletion/LocalRing.lean:151-154` proves
   residue-field invariance for the *module-theoretic*
   `AdicCompletion (maximalIdeal R) R` construction (Noetherian local
   ring `R`, `I`-adic completion as an inverse limit of `R ⧸ I^n`). The
   construction actually used by `WeierstrassCurve.LFunction` is a
   different one: `v.adicCompletionIntegers K = Valued.v.valuationSubring`,
   built from `UniformSpace.Completion` of the valued field `K` at the
   `v`-adic valuation (`Mathlib/RingTheory/DedekindDomain/AdicValuation.lean`).
   These are genuinely different bundled objects (inverse limit of
   quotients vs. uniform-space completion of a field), and no bridging
   `RingEquiv`/`IsLocalRing.ResidueField` compatibility lemma between
   them was found.

3. **The nearest thematically-relevant file assumes what we need, it
   does not prove it.** `Mathlib/Topology/Algebra/Valued/LocallyCompact.lean`
   has a `FiniteResidueField` section (`𝓀[K]` notation for
   `IsLocalRing.ResidueField 𝒪[K]` where `𝒪[K] := Valued.integer K`, a
   `Subring`, not the `ValuationSubring` used by `adicCompletionIntegers`).
   Every lemma there (`finite_quotient_maximalIdeal_pow_of_finite_residueField`,
   `totallyBounded_iff_finite_residueField`) takes `Finite 𝓀[K]` as an
   explicit **hypothesis** and derives consequences from it; none of them
   establish finiteness itself. There is also no `CompactSpace`/`IsCompact`
   instance anywhere in Mathlib for `v.adicCompletionIntegers K` (checked
   directly) that could have supplied finiteness via
   `totallyBounded_iff_finite_residueField` the other way.

## What a full proof of the side condition would require

The mathematically true fact is standard (a discrete valuation ring's
residue field is unchanged by completion, because the maximal ideal is
open and the original ring is dense, so the residue field is already
"complete" i.e. discrete/finite quotient survives verbatim), and
`𝓞 K ⧸ v.asIdeal` is already known finite in Mathlib
(`v.asIdeal.finiteQuotientOfFreeOfNeBot`, used in
`Completion/FinitePlace.lean:126`). But turning this into a Lean proof
for the *specific* bundled objects `WeierstrassCurve.LFunction` uses
requires building, essentially from scratch:

1. A `RingEquiv` (or at least a residue-field-inducing map) between the
   localization of `𝓞 K` at `v` (whose residue field is `𝓞 K ⧸ v.asIdeal`,
   known finite) and `(v.valuation K).integer`/`valuationSubring` — the
   pre-completion valuation ring inside `K` itself.
2. A completion-invariance-of-residue-field lemma for the
   `UniformSpace.Completion`-based construction specifically (dense
   image + open maximal ideal ⟹ residue field bijection with the
   pre-completion residue field), since no such generic lemma exists for
   this construction in Mathlib.
3. Composing (1) and (2) to conclude
   `IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃ 𝓞 K ⧸ v.asIdeal`,
   then transporting finiteness and (via `Nat.card` of a finite field)
   prime-power cardinality across that equivalence.

None of steps (1)-(3) are one-line instance lookups; each is a genuine
new lemma bridging two independently-developed corners of Mathlib
(Dedekind-domain adic valuations vs. `Valued`-field completion API vs.
the Noetherian-module `AdicCompletion` API). This matches the
reviewer's estimate of a multi-step, plausibly half-day-to-multi-day
side quest, not a same-session closure — so, per the task's explicit
stop condition, it was not forced.

## What was still proved (the other half of the split test)

Per the reviewer's own instruction ("only then is the full
`IsMultiplicative` theorem ... worth attempting"), the second half of
the split test was carried out with the diagnosed gap made an explicit,
honest hypothesis rather than assumed silently. Both results below are
fully proved, checked with `lake env lean`, zero forbidden tokens, and
`#print axioms` shows only `[propext, Classical.choice, Quot.sound]`:

* `WeierstrassCurve.localEulerFactor_isMultiplicative_of_isPrimePow` —
  the local Euler factor is multiplicative, given prime-power residue
  cardinality at that one place.
* `WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow` —
  `W.LFunction.IsMultiplicative`, given prime-power residue cardinality
  at every place of `𝓞 K`.

This validates the reviewer's claim that, *given* the side condition,
the algebraic argument really is cheap (a few lines, composing two
existing Mathlib lemmas). The bottleneck is entirely the finiteness
side condition diagnosed above.

## What is NOT claimed

No claim of novelty. No claim of progress toward the Birch and
Swinnerton-Dyer conjecture (a Clay Millennium Problem) — the conditional
results above say nothing about convergence of `LSeries`, analytic
continuation, functional equation, conductor, or Mordell-Weil rank, and
the unconditional target (`W.LFunction.IsMultiplicative` with no
hypothesis) remains unproved. This is a scoped, honest negative result
for the finiteness side condition plus an honest conditional positive
result for the algebraic reduction, nothing more.

## Where to pick this up

Anyone continuing this should start at step (2) above: proving that
`UniformSpace.Completion`-based adic completions of a discrete valuation
preserve the residue field. If a general lemma of that shape already
exists (or gets added) elsewhere in Mathlib under a name not covered by
the searches above, steps (1) and (3) are short, and the unconditional
`LFunction_isMultiplicative` then follows immediately from
`LFunction_isMultiplicative_of_residueField_isPrimePow` in
`FORMAL/LFunctionMultiplicativity.lean` with no further algebraic work.
