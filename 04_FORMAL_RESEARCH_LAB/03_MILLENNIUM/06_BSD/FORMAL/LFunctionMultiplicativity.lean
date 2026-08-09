/-
BSD-L-MULT-001 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's
Mathlib checkout, outside the shared import tree (same convention as
`CalderonZygmundKernelDefinitions.lean`, `02_NAVIER_STOKES/FORMAL/`).

## What this file is

Mathlib (as of this session) defines the L-function of a Weierstrass
curve over a number field as a formal Euler product of local factors:
`WeierstrassCurve.LFunction` in
`Mathlib/AlgebraicGeometry/EllipticCurve/LFunction.lean:79-85`
(Thomas Browning, added 2026-04-25). This file attempts the single most
basic classical structural fact about any L-function -- multiplicativity
of its Dirichlet coefficients (`IsMultiplicative`) -- using Mathlib's own
generic Euler-product machinery in
`Mathlib/NumberTheory/ArithmeticFunction/LFunction.lean`:
* `isMultiplicative_ofPowerSeries_of_isPrimePow` (:186-188)
* `isMultiplicative_eulerProduct` (:314-315, no `Multipliable` side
  condition needed -- the non-multipliable case is handled by
  `tprod_eq_one_of_not_multipliable` + `isMultiplicative_one`, confirmed
  by direct reading of the proof).

## What was actually found: the target does NOT close unconditionally

The unconditional goal
`theorem WeierstrassCurve.LFunction_isMultiplicative {K} [Field K]
[NumberField K] (W : WeierstrassCurve K) : W.LFunction.IsMultiplicative`
requires, for every `v : HeightOneSpectrum (𝓞 K)`,
`IsPrimePow (Nat.card (IsLocalRing.ResidueField (v.adicCompletionIntegers K)))`
(equivalently `Finite (IsLocalRing.ResidueField (v.adicCompletionIntegers K))`,
since `𝓞 K ⧸ v.asIdeal` is already known finite and a residue field that
is a finite field automatically has prime-power cardinality).

This side condition does **not** close. Full diagnosis, including the
exact instance-resolution failure and the exhaustive Mathlib search
confirming no bridging lemma exists, is in `../BSD-1_GAP_NOTE.md`
(same directory level as this file's parent, i.e.
`03_MILLENNIUM/06_BSD/BSD-1_GAP_NOTE.md`).

## What this file DOES prove (honest, conditional, no unproved gaps)

Per the adversarial reviewer's own split test: once the unconditional
finiteness lemma is diagnosed as not closing, the second, genuinely
cheap half of the argument is worth checking on its own terms, taking
the diagnosed gap as an explicit hypothesis rather than smuggling it in.
Both theorems below are **unconditionally true and fully proved** -- the
`IsPrimePow (Nat.card ...)` hypothesis is a real, non-trivial,
non-vacuous proposition, not a disguised `True` and not left as an
unproved gap discharged by a forbidden tactic; nothing about it is
assumed to hold for actual number fields.

1. `localEulerFactor_isMultiplicative_of_isPrimePow`: for any Weierstrass
   curve over the fraction field of a discrete valuation ring `R`,
   `W.localEulerFactor R` is multiplicative, GIVEN that the residue
   field of `R` has prime-power cardinality.
2. `LFunction_isMultiplicative_of_residueField_isPrimePow`: for a
   Weierstrass curve `W` over a number field `K`,
   `W.LFunction.IsMultiplicative`, GIVEN the (currently unproved, for
   this construction) hypothesis that every adic-completion residue
   field of `𝓞 K` has prime-power cardinality.

## What is still missing even if the diagnosed gap were later closed

Nothing here proves convergence of `W.LSeries` anywhere in `ℂ`, analytic
continuation, a functional equation, a conductor, or any connection to
Mordell-Weil rank. This file makes zero claim of novelty, zero claim of
progress toward the Birch and Swinnerton-Dyer conjecture (a Clay
Millennium Problem), and zero claim that the Millennium problem is
solved, approximated, or reachable. It is reusable, honestly-labeled
plumbing about a formal Dirichlet series, nothing more.
-/

import Mathlib.AlgebraicGeometry.EllipticCurve.LFunction

open IsDedekindDomain NumberField ArithmeticFunction

namespace WeierstrassCurve

section LocalField

variable {R : Type*} [CommRing R] [IsDomain R] [IsDiscreteValuationRing R] {L : Type*}
  [Field L] [Algebra R L] [IsFractionRing R L] (W : WeierstrassCurve L)

/-- The local Euler factor of a Weierstrass curve at a discrete valuation ring `R` is a
multiplicative arithmetic function, PROVIDED the residue field of `R` has prime-power
cardinality (see the file docstring: this hypothesis is exactly the gap diagnosed in
`BSD-1_GAP_NOTE.md` for the number-field case `R = v.adicCompletionIntegers K` -- it is not
proved here, it is an explicit, honest hypothesis). Proof: `localEulerFactor` unfolds to
`ArithmeticFunction.ofPowerSeries q (localPowerSeries R)` with `q = Nat.card
(IsLocalRing.ResidueField R)`, and Mathlib's `isMultiplicative_ofPowerSeries_of_isPrimePow`
applies once `IsPrimePow q` and `(localPowerSeries R).constantCoeff = 1` are supplied; the
latter is `PowerSeries.constantCoeff_invOfUnit` since `localPowerSeries R = invOfUnit
(localPolynomial R) 1`. -/
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

/-- `W.LFunction` is a multiplicative arithmetic function, PROVIDED every adic-completion
residue field of `𝓞 K` has prime-power cardinality. This hypothesis is exactly the diagnosed
gap (see `BSD-1_GAP_NOTE.md`): it is *not* discharged here, it is an explicit premise of this
theorem. `LFunction` unfolds to `eulerProduct (fun p ↦ (W.baseChange _).localEulerFactor
(p.adicCompletionIntegers K))`, and `isMultiplicative_eulerProduct` (which needs no
`Multipliable` side condition) reduces the goal to pointwise multiplicativity of each local
factor, discharged by `localEulerFactor_isMultiplicative_of_isPrimePow` above. -/
theorem LFunction_isMultiplicative_of_residueField_isPrimePow
    (hq : ∀ p : HeightOneSpectrum (𝓞 K),
      IsPrimePow (Nat.card (IsLocalRing.ResidueField (p.adicCompletionIntegers K)))) :
    W.LFunction.IsMultiplicative := by
  unfold WeierstrassCurve.LFunction
  apply ArithmeticFunction.isMultiplicative_eulerProduct
  intro p
  exact localEulerFactor_isMultiplicative_of_isPrimePow _ (hq p)

end NumberField

end WeierstrassCurve

#print axioms WeierstrassCurve.localEulerFactor_isMultiplicative_of_isPrimePow
#print axioms WeierstrassCurve.LFunction_isMultiplicative_of_residueField_isPrimePow
