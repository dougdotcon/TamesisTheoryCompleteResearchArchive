/-
BSD-MW-DESCENT-GAP-001 -- standalone probe, NOT integrated into `TamesisLab.lean`.
Verified in isolation via `lake env lean` directly against the project's Mathlib
checkout, outside the shared import tree (same convention as
`LFunctionMultiplicativity.lean`, `BadReductionValuationBridge.lean`).

## What this file is

This is a **reconnaissance-only** probe, not a formalization attempt. Its purpose
is to pin down, in checkable Lean, exactly which pieces of the standard proof of
the Mordell-Weil theorem (finite generation of `E(K)` for `K` a number field) are
already available in Mathlib's abstract descent machinery
(`Mathlib/GroupTheory/Descent.lean`, `AddCommGroup.fg_of_descent'`) versus which
pieces are still missing. Per the task's explicit scope, **no attempt is made
here to prove Mordell-Weil, weak Mordell-Weil, or any other new mathematical
fact** -- every declaration below either already exists in Mathlib (confirmed via
`#check`/`infer_instance`) or is a `#check` of an existing Mathlib statement's
type, used only to display the exact shape of its hypotheses. This file uses
none of the tactics or declaration forms forbidden by the lab's governance
scanner, and did not need to: the honest scoping result (see
`../BSD-4_GAP_NOTE.md`) is that the remaining gap is real and does not collapse
to a single missing lemma.

## The target statement being scoped (for reference, not attempted)

`AddCommGroup.fg_of_descent' {G : Type*} [AddCommGroup G] {h : G → ℝ} {C : ℝ}
    (H₁ : (zsmulAddMonoidHom (α := G) 2).range.FiniteIndex) (H₂ : ∀ x, 0 ≤ h x)
    (H₃ : ∀ x y, |h (x + y) + h (x - y) - 2 * (h x + h y)| ≤ C) [Northcott h] :
    AddGroup.FG G`

applied to `G := WeierstrassCurve.Affine.Point W` for `W` an elliptic curve over
`K := ℚ`. See `../BSD-4_GAP_NOTE.md` for the full gap analysis; this file only
records the individual instance/type checks that back that note's claims.
-/

import Mathlib.GroupTheory.Descent
import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.AddSubMap
import Mathlib.NumberTheory.Height.EllipticCurve
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.RingTheory.DedekindDomain.SelmerGroup

namespace BSDMordellWeilGapProbe

/-! ### Piece 1 (available): `E(K)` is an additive commutative group.

`WeierstrassCurve.Affine.Point.instAddCommGroup`
(`Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.lean:771`) already gives
Mathlib's `E(K)` the group structure `AddCommGroup.fg_of_descent'` needs its `G`
to carry. This is the one piece of the abstract group-theoretic side that is
fully in place. -/
example {K : Type*} [Field K] [DecidableEq K] (W : WeierstrassCurve.Affine K)
    [W.IsElliptic] : AddCommGroup (WeierstrassCurve.Affine.Point W) := by
  infer_instance

/-! ### Piece 2 (available): the abstract descent theorem itself.

`AddCommGroup.fg_of_descent'` (the `to_additive` form of `CommGroup.fg_of_descent'`,
`Mathlib/GroupTheory/Descent.lean:150`) exists with exactly the hypothesis shape
the docstring advertises. Displaying its type here (not applying it) records the
precise Prop-level obligations that would need to be discharged for
`G := W.Point`: finite index of `2 • G` in `G`, nonnegativity of the height,
the approximate parallelogram law, and a `Northcott h` instance. -/
#check @AddCommGroup.fg_of_descent'

/-! ### Piece 3 (available, but one abstraction layer short): the height
inequality proved in `Height/EllipticCurve.lean`.

`abs_logHeight_addSubMap_sub_two_mul_logHeight_le`
(`Mathlib/NumberTheory/Height/EllipticCurve.lean:45-52`) is a real, checked
Mathlib theorem -- but note its statement quantifies over `x : Fin 3 → K`
(bare coordinate vectors fed through the `addSubMap` polynomial map on `ℙ²`),
**not** over pairs of points `P Q : W.Point`. This is exactly the gap the
adversarial reviewer flagged: it is not yet the parallelogram law
`H₃` in `fg_of_descent'` needs, which must be a statement about `h (P + Q)`,
`h (P - Q)`, `h P`, `h Q` for actual points of the group `W.Point`. -/
#check @WeierstrassCurve.abs_logHeight_addSubMap_sub_two_mul_logHeight_le

/-! ### Piece 4 (missing): no naïve height on `E(K)` is defined.

`Height/EllipticCurve.lean`'s own header TODO (lines 26-29) lists, as still
outstanding: "Define the naïve height", "Add the further ingredients needed for
the approximate parallelogram law", and "Add the statement and proof of the
approximate parallelogram law". Consequently there is no candidate `h : W.Point
→ ℝ` in Mathlib to even plug into `fg_of_descent'` as its `h` argument. This
file does not (and per the task's scope, must not) supply one. -/

/-! ### Piece 5 (missing): the `addSubMap` correctness TODO.

`WeierstrassCurve.addSubMap` (`AddSubMap.lean:46-49`) is the coordinate-level
map used to prove Piece 3, but the file's own TODO (line 21) reads exactly:
"Show that the map really does what it is claimed to do" -- i.e. that
`addSubMap` really computes `(x(P+Q) * x(P-Q) : x(P+Q) + x(P-Q) : 1)` from
`(x(P) * x(Q) : x(P) + x(Q) : 1)`. Without this correctness lemma, Piece 3's
inequality (which is about the *map*, unconditionally) cannot be transported to
an inequality about *points* `P + Q`, `P - Q` even once Piece 4 supplies a
height on `W.Point`. -/

/-! ### Piece 6 (missing): weak Mordell-Weil, `E(K) / 2 • E(K)` finite.

This is `H₁` in `fg_of_descent'`. Mathlib has a *generic* Dedekind-domain
Selmer group (`IsDedekindDomain.selmerGroup`,
`Mathlib/RingTheory/DedekindDomain/SelmerGroup.lean`), imported above to confirm
directly that it type-checks and is available -- but grep across all of Mathlib
(run separately, recorded in `../BSD-4_GAP_NOTE.md`) confirms it is never
instantiated for, or connected to, `WeierstrassCurve`/`EllipticCurve`, and no
`n`-multiplication isogeny map, Kummer map, or elliptic-curve Selmer group
exists anywhere in Mathlib. This file imports the generic construction only to
demonstrate that fact by contrast; it proves nothing new about it. -/
#check @IsDedekindDomain.selmerGroup

end BSDMordellWeilGapProbe
