/-
HG-4e -- Packaging the mul/inv closure of `IsHolomorphicTransition` as a
`Subgroup` of `(ℂ → ℂ)ˣ` (Wave-5 item WAVE5-HG-4E, Hodge line /
03_MILLENNIUM/05_HODGE)

STATUS: BUILT (`lake env lean`, exit 0), single-file check against the
already-built Mathlib cache. Not imported by TamesisLab.lean, not
registered anywhere else. Touches no file other than this one.

BACKGROUND (the exact residual gap this item closes):
Wave-1's `HolomorphicTransitionProbe.lean` (this directory) built a
predicate `IsHolomorphicTransition g := MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g`
for line-bundle transition functions and the bridge lemma
`isHolomorphicTransition_iff_differentiable : IsHolomorphicTransition g ↔
Differentiable ℂ g`. Wave-4's `HolomorphicTransitionMulInvClosureProbe.lean`
(HG-4d, this directory) then proved the predicate is closed under pointwise
multiplication (`isHolomorphicTransition_mul`) and, for everywhere-
nonvanishing functions, pointwise inversion (`isHolomorphicTransition_inv`).
Neither of those two files packages this mul/inv closure as an actual
algebraic substructure: line-bundle transition functions are precisely the
`Cˣ`-valued (everywhere-invertible) holomorphic maps, and the natural home
for "the holomorphic transition functions" as a single algebraic object is
a `Subgroup` of the unit group `(ℂ → ℂ)ˣ` of the pointwise-multiplication
monoid `ℂ → ℂ` -- NOT a sub-monoid of `ℂ → ℂ` itself, because inversion
(reversing a trivialization) needs a genuine group-theoretic inverse, and
plain `ℂ → ℂ` under pointwise multiplication has zero divisors and is not
a group. This Wave-5 item (HG-4e) closes exactly that packaging step: build
`HolomorphicTransitionSubgroup : Subgroup (ℂ → ℂ)ˣ` whose carrier is the set
of units `u` whose underlying function `(u : ℂ → ℂ)` is holomorphic in the
HG-4/HG-4d sense, and verify it satisfies the three `Subgroup` obligations
(`one_mem'`, `mul_mem'`, `inv_mem'`). Nothing broader.

THE TEST, AND THE RESULT: CLOSED, exactly as scoped by the Wave-5 plan.
This file is a new, standalone file (outside the lakefile package, exactly
like its Wave-1/Wave-4 sources) that inlines, byte-identical, the
`IsHolomorphicTransition` definition and `isHolomorphicTransition_iff_
differentiable` bridge lemma from `HolomorphicTransitionProbe.lean`
(namespace `HG4HolomorphicTransitionProbe`), and the two closure corollaries
`isHolomorphicTransition_mul` / `isHolomorphicTransition_inv` from
`HolomorphicTransitionMulInvClosureProbe.lean` (namespace
`HG4dHolomorphicTransitionMulInvClosureProbe`). It then builds

  `HolomorphicTransitionSubgroup : Subgroup (ℂ → ℂ)ˣ`

with carrier `{u | IsHolomorphicTransition (u : ℂ → ℂ)}`, proving:
  - `one_mem'` via `Units.val_one` (the coercion of `(1 : (ℂ → ℂ)ˣ)` is the
    constant function `1`) plus `differentiable_const`;
  - `mul_mem'` via `Units.val_mul` (the coercion of a product of units is the
    pointwise product of the coercions) plus `isHolomorphicTransition_mul`
    (HG-4d);
  - `inv_mem'` via `Units.val_inv_eq_inv_val` (`↑u⁻¹ = (↑u)⁻¹`, valid because
    `ℂ → ℂ` is a `DivisionMonoid` under the `Pi.divisionMonoid` instance,
    since `ℂ` itself is one) plus `isHolomorphicTransition_inv` (HG-4d),
    whose nonvanishing hypothesis `∀ x, (u : ℂ → ℂ) x ≠ 0` is supplied by
    `Pi.isUnit_iff` (a function `ℂ → ℂ` is a unit of the pointwise monoid
    iff it is pointwise a unit) composed with `isUnit_iff_ne_zero` (a unit
    of the field `ℂ` is exactly a nonzero element) applied to `u.isUnit`.

The fallback named in the plan (proving `(u⁻¹ : ℂ → ℂ) = ((u : ℂ → ℂ))⁻¹`
pointwise via `funext` instead of through the `DivisionMonoid` chain) was
NOT needed: `Units.val_inv_eq_inv_val` applied directly with zero diamond
issues, because the ambient `Inv (ℂ → ℂ)` instance picked up by both the
`Subgroup`'s ambient group `(ℂ → ℂ)ˣ` and by `Units.val_inv_eq_inv_val`'s
`DivisionMonoid (ℂ → ℂ)` instance resolve to the same `Pi.instInv` /
`Pi.divisionMonoid` instances (there is only one `Inv (ℂ → ℂ)` instance in
scope, coming from `ℂ`'s own `Field`-derived `DivisionMonoid`), so no
`convert`/`show`-level instance mismatch arose.

WHAT THIS FILE DOES NOT DO (stop conditions):
- Does NOT modify `HolomorphicTransitionProbe.lean` or
  `HolomorphicTransitionMulInvClosureProbe.lean`; it inlines copies of the
  short relevant pieces into this new file instead, exactly as HG-4d did
  for HG-4.
- Does NOT define or touch any `VectorBundle`/`Bundle`/`HolomorphicLineBundle`
  API, and does NOT attempt any cocycle-condition bookkeeping for an actual
  line bundle -- only the algebraic closure-as-a-subgroup fact about the
  transition-function predicate itself.
- Does NOT prove or approach Lefschetz's theorem on (1,1)-classes, the
  Hodge Conjecture, or any Millennium Problem, and claims no progress
  toward any of them.
- Does NOT claim mathematical novelty: every lemma used (`Units.val_one`,
  `Units.val_mul`, `Units.val_inv_eq_inv_val`, `Pi.isUnit_iff`,
  `isUnit_iff_ne_zero`, `differentiable_const`, plus the pre-existing
  `Pi.divisionMonoid` instance) is pre-existing, proved Mathlib content;
  the only thing built here is packaging the already-closed HG-4/HG-4d
  facts as the three fields of a `Subgroup` structure.

VERIFICATION OF CITED NAMES (by grep against the vendored snapshot in
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib, and by this
file's own successful compilation):
  - `structure Subgroup (G : Type*) [Group G] extends Submonoid G where
       inv_mem' {x} : x ∈ carrier → x⁻¹ ∈ carrier`
                               Algebra/Group/Subgroup/Defs.lean:295-297
  - `structure Submonoid (M : Type*) [MulOneClass M] extends Subsemigroup M
       where one_mem' : (1 : M) ∈ carrier`
                               Algebra/Group/Submonoid/Defs.lean:89-91
       (`Subsemigroup` supplies `carrier` and
       `mul_mem' {a b} : a ∈ carrier → b ∈ carrier → a * b ∈ carrier`.)
  - `instance instCommGroupUnits {α} [CommMonoid α] : CommGroup αˣ`
                               Algebra/Group/Units/Defs.lean:265-267
       (so `(ℂ → ℂ)ˣ` is a `Group`, satisfying `Subgroup`'s hypothesis,
       since `ℂ → ℂ` is a `CommMonoid` under `Pi.instMul`/`Pi.instOne`.)
  - `lemma val_inv_eq_inv_val [DivisionMonoid α] (u : αˣ) : ↑u⁻¹ = (u⁻¹ : α)`
                               Algebra/Group/Units/Defs.lean:280-281
  - `instance Pi.divisionMonoid [∀ i, DivisionMonoid (f i)] :
       DivisionMonoid (∀ i, f i)`
                               Algebra/Group/Pi/Basic.lean:99
  - `lemma Pi.isUnit_iff : IsUnit x ↔ ∀ i, IsUnit (x i)`
                               Algebra/Group/Pi/Units.lean:31-33
  - `protected theorem Units.isUnit [Monoid M] (u : Mˣ) : IsUnit (u : M)`
                               Algebra/Group/Units/Defs.lean:384
  - `theorem isUnit_iff_ne_zero : IsUnit a ↔ a ≠ 0`
                               Algebra/GroupWithZero/Units/Basic.lean:264
  - `isHolomorphicTransition_mul`, `isHolomorphicTransition_inv` (HG-4d)
                               HolomorphicTransitionMulInvClosureProbe.lean
                               (this directory, Wave-4)
-/

import Mathlib

/- ============================================================
   PART 1 -- inlined verbatim from `HolomorphicTransitionProbe.lean`
   (HG-4, Wave-1): only the definition and bridge lemma needed below.
   ============================================================ -/

namespace HG4HolomorphicTransitionProbe

open scoped Manifold

/-- The candidate predicate: "the transition function `g` of a rank-1
trivial bundle over `M := ℂ` (single-chart model `𝓘(ℂ, ℂ)`) is
holomorphic," stated purely in terms of Mathlib's pre-existing manifold
complex-differentiability machinery. -/
def IsHolomorphicTransition (g : ℂ → ℂ) : Prop :=
  MDifferentiable 𝓘(ℂ, ℂ) 𝓘(ℂ, ℂ) g

/-- The predicate unfolds, with zero extra infrastructure, to Mathlib's
standard complex-differentiability. -/
theorem isHolomorphicTransition_iff_differentiable {g : ℂ → ℂ} :
    IsHolomorphicTransition g ↔ Differentiable ℂ g := by
  unfold IsHolomorphicTransition
  exact mdifferentiable_iff_differentiable

end HG4HolomorphicTransitionProbe

/- ============================================================
   PART 2 -- inlined verbatim from
   `HolomorphicTransitionMulInvClosureProbe.lean` (HG-4d, Wave-4): the two
   pointwise closure corollaries needed below.
   ============================================================ -/

namespace HG4dHolomorphicTransitionMulInvClosureProbe

open HG4HolomorphicTransitionProbe

/-- The HG-4d multiplicative closure: if two transition functions `g`, `h`
are holomorphic, so is their pointwise product `g * h`. -/
theorem isHolomorphicTransition_mul {g h : ℂ → ℂ}
    (hg : IsHolomorphicTransition g) (hh : IsHolomorphicTransition h) :
    IsHolomorphicTransition (g * h) :=
  isHolomorphicTransition_iff_differentiable.mpr
    ((isHolomorphicTransition_iff_differentiable.mp hg).mul
      (isHolomorphicTransition_iff_differentiable.mp hh))

/-- The HG-4d inverse closure: if a transition function `g` is holomorphic
and everywhere nonvanishing, so is its pointwise inverse `g⁻¹`. -/
theorem isHolomorphicTransition_inv {g : ℂ → ℂ} (hz : ∀ x, g x ≠ 0)
    (hg : IsHolomorphicTransition g) :
    IsHolomorphicTransition g⁻¹ :=
  isHolomorphicTransition_iff_differentiable.mpr
    ((isHolomorphicTransition_iff_differentiable.mp hg).inv hz)

end HG4dHolomorphicTransitionMulInvClosureProbe

/- ============================================================
   PART 3 -- HG-4e: the actual falsifiable test for this item. Package the
   mul/inv closure above as a `Subgroup (ℂ → ℂ)ˣ`. Nothing beyond this
   packaging (and the one small nonvanishing lemma it needs) is attempted.
   ============================================================ -/

namespace HG4eHolomorphicTransitionSubgroupProbe

open HG4HolomorphicTransitionProbe HG4dHolomorphicTransitionMulInvClosureProbe

/-- Every unit `u : (ℂ → ℂ)ˣ` of the pointwise-multiplication monoid is,
pointwise, a nonzero complex number: this is exactly what "unit" means for
a `Pi`-type target valued in a field, via `Pi.isUnit_iff` (unit of a
product = pointwise unit) and `isUnit_iff_ne_zero` (unit of a field =
nonzero element). This is the nonvanishing hypothesis `inv_mem'` needs to
invoke `isHolomorphicTransition_inv`. -/
theorem holomorphicTransitionUnit_val_ne_zero (u : (ℂ → ℂ)ˣ) :
    ∀ x, (u : ℂ → ℂ) x ≠ 0 := fun x =>
  isUnit_iff_ne_zero.mp (Pi.isUnit_iff.mp u.isUnit x)

/-- The Wave-5 HG-4e test itself: the holomorphic transition functions,
viewed as units of the pointwise-multiplication monoid `ℂ → ℂ` (i.e. the
everywhere-invertible transition functions, exactly the `Cˣ`-valued ones
an actual line bundle's transition functions must be), form a `Subgroup`
of `(ℂ → ℂ)ˣ`. This packages, in one algebraic object, the HG-4d closure
facts `isHolomorphicTransition_mul` / `isHolomorphicTransition_inv`
together with the trivial-transition-function case (`one_mem'`). -/
def HolomorphicTransitionSubgroup : Subgroup (ℂ → ℂ)ˣ where
  carrier := {u | IsHolomorphicTransition (u : ℂ → ℂ)}
  one_mem' := by
    show IsHolomorphicTransition ((1 : (ℂ → ℂ)ˣ) : ℂ → ℂ)
    rw [Units.val_one]
    exact isHolomorphicTransition_iff_differentiable.mpr (differentiable_const 1)
  mul_mem' {u v} hu hv := by
    show IsHolomorphicTransition ((u * v : (ℂ → ℂ)ˣ) : ℂ → ℂ)
    rw [Units.val_mul]
    exact isHolomorphicTransition_mul hu hv
  inv_mem' {u} hu := by
    show IsHolomorphicTransition ((u⁻¹ : (ℂ → ℂ)ˣ) : ℂ → ℂ)
    rw [Units.val_inv_eq_inv_val]
    exact isHolomorphicTransition_inv (holomorphicTransitionUnit_val_ne_zero u) hu

/-- Sanity re-statement: membership in the packaged subgroup is exactly
the HG-4/HG-4d predicate on the underlying function, definitionally. -/
theorem mem_holomorphicTransitionSubgroup_iff {u : (ℂ → ℂ)ˣ} :
    u ∈ HolomorphicTransitionSubgroup ↔ IsHolomorphicTransition (u : ℂ → ℂ) :=
  Iff.rfl

/-- Nontriviality witness: the unit `1 : (ℂ → ℂ)ˣ` genuinely belongs to the
subgroup (an instance of `one_mem'` above, stated standalone so the
subgroup is exhibited as inhabited by a concrete element, not merely
well-typed). -/
theorem one_mem_holomorphicTransitionSubgroup :
    (1 : (ℂ → ℂ)ˣ) ∈ HolomorphicTransitionSubgroup :=
  HolomorphicTransitionSubgroup.one_mem

#print axioms holomorphicTransitionUnit_val_ne_zero
#print axioms HolomorphicTransitionSubgroup
#print axioms mem_holomorphicTransitionSubgroup_iff
#print axioms one_mem_holomorphicTransitionSubgroup

end HG4eHolomorphicTransitionSubgroupProbe

/-
RESULT: CLOSED. `HolomorphicTransitionSubgroup : Subgroup (ℂ → ℂ)ˣ` is built
exactly as scoped by the Wave-5 HG-4e test, with carrier `{u |
IsHolomorphicTransition (u : ℂ → ℂ)}`, discharging `one_mem'` via
`Units.val_one` + `differentiable_const`, `mul_mem'` via `Units.val_mul` +
the HG-4d lemma `isHolomorphicTransition_mul`, and `inv_mem'` via
`Units.val_inv_eq_inv_val` (through the pre-existing `Pi.divisionMonoid`
instance on `ℂ → ℂ`, with no diamond issue -- the `DivisionMonoid`-chain
route from the plan worked directly, so the plan's pointwise-`funext`
fallback was not needed) + the HG-4d lemma `isHolomorphicTransition_inv`,
whose nonvanishing hypothesis is supplied by the new lemma
`holomorphicTransitionUnit_val_ne_zero` (via `Pi.isUnit_iff` +
`isUnit_iff_ne_zero`, exactly as scoped). This closes the packaging gap
neither HG-4 (Wave-1) nor HG-4d (Wave-4) addressed: the holomorphic,
everywhere-invertible transition functions form an actual algebraic
substructure (a subgroup of the unit group), not just a predicate closed
under two separate operations. No attempt is made here at the general
`VectorBundle`/`Bundle` API, at any actual cocycle condition, or at
Lefschetz (1,1), the Hodge Conjecture, or any Millennium Problem.
-/
