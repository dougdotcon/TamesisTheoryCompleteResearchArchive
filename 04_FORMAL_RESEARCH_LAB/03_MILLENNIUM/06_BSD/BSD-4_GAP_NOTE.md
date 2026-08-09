# BSD-4 gap note: pinning down Mathlib's Mordell-Weil descent gap

Item: **BSD-MW-DESCENT-GAP-001** (Wave-1 batch, code `BSD-4`).
File produced alongside this note: `FORMAL/MordellWeilGapProbe.lean`.

## What kind of item this is

This item is **reconnaissance-only, by design**, per its own falsifiable test:
read `Mathlib/GroupTheory/Descent.lean`,
`Mathlib/NumberTheory/Height/EllipticCurve.lean`, and
`Mathlib/AlgebraicGeometry/EllipticCurve/Affine/AddSubMap.lean` closely enough
to write out the exact remaining Prop-level statement list needed to invoke
`AddCommGroup.fg_of_descent'` for `E(ℚ)`. No proof of Mordell-Weil, weak
Mordell-Weil, or the parallelogram law was attempted or is claimed. The one
Lean file accompanying this note contains no new mathematical result: every
declaration in it is either an `example` confirming an *existing* Mathlib
instance resolves, or a `#check` displaying the type of an *existing* Mathlib
declaration, exactly as the task's own test description allows ("no new Lean
code required, or at most a stub example").

## The target being scoped

`AddCommGroup.fg_of_descent'` (`Mathlib/GroupTheory/Descent.lean:150`, the
`to_additive` form of `CommGroup.fg_of_descent'`) has signature:

```
theorem AddCommGroup.fg_of_descent' {G : Type*} [AddCommGroup G] {h : G → ℝ} {C : ℝ}
    (H₁ : (nsmulAddMonoidHom (α := G) 2).range.FiniteIndex) (H₂ : ∀ x, 0 ≤ h x)
    (H₃ : ∀ x y, |h (x + y) + h (x - y) - 2 * (h x + h y)| ≤ C) [Northcott h] :
    AddGroup.FG G
```

(the additive name `nsmulAddMonoidHom` was confirmed directly by `#check`,
not assumed — see `FORMAL/MordellWeilGapProbe.lean`). Applying this with
`G := WeierstrassCurve.Affine.Point W` for a Weierstrass model `W` of an
elliptic curve `E/ℚ` would give finite generation of `E(ℚ)`, i.e. the group
side of Mordell-Weil. The docstring of `Descent.lean` itself (lines 45-47)
states this is "one of the main ingredients of the standard proof of the
Mordell-Weil Theorem."

## Piece-by-piece gap list

**(0) The group structure `G := E(ℚ)` itself — available.**
`WeierstrassCurve.Affine.Point` (`Mathlib/AlgebraicGeometry/EllipticCurve/
Affine/Point.lean:771`) already has an `AddCommGroup` instance, for any field
`K` with `DecidableEq K` and `W.IsElliptic`. Confirmed directly: `example {K}
[Field K] [DecidableEq K] (W : WeierstrassCurve.Affine K) [W.IsElliptic] :
AddCommGroup (WeierstrassCurve.Affine.Point W) := by infer_instance` type-checks
in `MordellWeilGapProbe.lean`. This is the only piece of the five below that is
fully closed.

**(1) `H₁`: weak Mordell-Weil, `E(ℚ) / 2•E(ℚ)` finite — entirely absent.**
Three independent searches across the full Mathlib checkout, all negative:
* `grep -rli mordell .` (case-insensitive) returns exactly one file,
  `Mathlib/GroupTheory/Descent.lean` itself — the word appears only in that
  file's own docstring, motivating the descent theorem; there is no
  `MordellWeil`/`weakMordellWeil` declaration anywhere.
* `grep -rli selmer .` returns three files: `RingTheory/Polynomial/Selmer.lean`
  (irreducibility of the unrelated Selmer *polynomials* `Xⁿ - X - 1`, Thomas
  Browning 2022 — a name collision, not Selmer-*group* material) and
  `RingTheory/DedekindDomain/SelmerGroup.lean` (`IsDedekindDomain.selmerGroup`,
  David Kurniadi Angdinata 2022), which is a **generic** Dedekind-domain Kummer
  theory Selmer group `K(S, n) ≤ Kˣ ⧸ (Kˣ)ⁿ`, built from an arbitrary Dedekind
  domain and a set `S` of primes. `grep -n "EllipticCurve\|WeierstrassCurve"`
  against that file returns nothing: it is never instantiated for, or
  connected to, elliptic curves.
* `grep -rli isogeny .` returns **zero** files anywhere in Mathlib: there is no
  multiplication-by-`n` isogeny on `WeierstrassCurve.Affine.Point`, hence no
  candidate map whose kernel/cokernel a Selmer-group argument would even act
  on. Building weak Mordell-Weil from scratch would require, at minimum, an
  `n`-isogeny on `E(ℚ)`, the Kummer sequence `0 → E(ℚ)/nE(ℚ) → Sel⁽ⁿ⁾(E/ℚ) →
  Ш(E/ℚ)[n] → 0` via Galois cohomology of the `n`-torsion, and a bound on the
  Selmer group — a self-contained arithmetic-geometry project, not a short
  gap-filling lemma.

**(2) `H₃`: the approximate parallelogram law for points of `E(ℚ)` —
absent, and further from done than the recon's framing suggested.**
The adversarial reviewer's revised expectation for this test (which this probe
confirms rather than merely repeats) is that this side has *at least three*
distinct outstanding sub-gaps, not one:

* **(2a) `AddSubMap.lean:21` correctness TODO.** The literal text is: "TODO:
  Show that the map really does what it is claimed to do." `addSubMap`
  (lines 46-49) is asserted, not proved, to compute
  `(x(P+Q)·x(P-Q) : x(P+Q)+x(P-Q) : 1)` from `(x(P)·x(Q) : x(P)+x(Q) : 1)` on
  the level of `ℙ²` coordinate vectors. Nothing in the file connects
  `addSubMap` back to the actual group operations `P + Q`, `P - Q` on
  `WeierstrassCurve.Affine.Point`.
* **(2b) No naïve height on `E(K)` is defined.** `Height/EllipticCurve.lean`'s
  own header TODO (lines 26-29) lists as still outstanding, verbatim: "Define
  the naïve height", "Add the further ingredients needed for the approximate
  parallelogram law", and "Add the statement and proof of the approximate
  parallelogram law." There is consequently no candidate `h : W.Point → ℝ` in
  Mathlib today to supply as `fg_of_descent'`'s `h` argument at all.
* **(2c) The one theorem that *is* proved in that file is one abstraction
  layer short of a statement about points.**
  `abs_logHeight_addSubMap_sub_two_mul_logHeight_le`
  (`Height/EllipticCurve.lean:45-52`) is genuinely proved and does check
  (confirmed again here via `#check`), but its statement is
  `∃ C, ∀ x : Fin 3 → K, |logHeight (addSubMap-image of x) - 2 * logHeight x| ≤
  C` — a coordinate-level inequality about the polynomial map `addSubMap`
  acting on **arbitrary vectors** `x : Fin 3 → K`, universally quantified, with
  no reference to `W.Point`, to a point `P`, or to the curve equation being
  satisfied at all. Turning this into `H₃`'s actual required statement,
  `∀ P Q : W.Point, |h (P+Q) + h (P-Q) - 2*(h P + h Q)| ≤ C`, needs (2a) *and*
  (2b) *and* a proof that the naïve height of a point equals
  `logHeight` of its (normalized) coordinate vector, none of which exist yet.

So the honest count is (2a) + (2b) + (2c)'s remaining composition step = at
least three separate un-discharged sub-gaps on the height/parallelogram-law
side, not a "nearly closed" single missing link — matching the reviewer's
independent re-read of the same file rather than the original recon's more
optimistic phrasing.

**(3) `[Northcott h]`: adjacent infrastructure that partially exists.**
Mathlib already has `Northcott (mulHeight₁ (K := K))` for any number field `K`
(`Height/NumberField.lean:395`, built from the product formula and finiteness
of bounded-height sets in `ℙ¹(K)`), and `ℚ` is confirmed a `NumberField`
(`NumberField/Basic.lean:422`, `instance numberField : NumberField ℚ`) via the
`AdmissibleAbsValues ℚ` instance chain
(`Height/NumberField.lean:77-83`, `instAdmissibleAbsValues`). This is real,
reusable Northcott-property infrastructure for heights on `K`-points of
projective space — but it is stated for `mulHeight₁ : K → ℝ` (points of
`ℙ¹(K)`/elements of `K`), not for any height on `E(K)`, so it cannot supply
`[Northcott h]` for `fg_of_descent'` until (2b) defines an `h : W.Point → ℝ`
whose Northcott property is then separately proved (presumably, but not yet
verified, by transport along whatever embedding of `E(K)` into a projective
space (2b) ends up using).

## Summary table

| Piece | Status | Where |
|---|---|---|
| `G := E(ℚ)` is an `AddCommGroup` | **done** | `Affine/Point.lean:771` |
| `AddCommGroup.fg_of_descent'` itself | **done** (abstract theorem) | `GroupTheory/Descent.lean:150` |
| `H₁`: weak Mordell-Weil (`E(ℚ)/2E(ℚ)` finite) | **absent** | no file anywhere |
| `H₃`(2a): `addSubMap` correctness | **absent** (open TODO) | `AddSubMap.lean:21` |
| `H₃`(2b): naïve height on `E(K)` defined | **absent** (open TODO) | `Height/EllipticCurve.lean:26-29` |
| `H₃`(2c): parallelogram law for actual points | **absent**; only a one-layer-removed coordinate inequality exists | `Height/EllipticCurve.lean:45-52` |
| `[Northcott h]` for `E(K)`'s height | **absent**, but adjacent `mulHeight₁` Northcott machinery for `ℙ¹(K)` exists and is reusable in principle | `Height/NumberField.lean:395` |

## Outcome, per the test's own telling criterion

The falsifiable test's stated criterion was: a short, enumerable gap list is a
meaningful scouting result worth flagging for a dedicated future front; if
stating the missing pieces reveals *additional* undocumented dependencies
beyond what was expected, that should lower confidence in near-term
tractability. The count above is five outstanding items (one absent
prerequisite entirely — weak Mordell-Weil — plus a three-way split of what the
recon had treated as a single "nearly closed" parallelogram-law gap), which is
larger and more structurally spread out than the original recon anticipated,
though smaller than "additional undocumented dependencies beyond the reviewer's
own re-check" — the reviewer's independent read had already anticipated
exactly this three-way split before this probe was written, and this probe's
direct file/line checks and Lean type-checks corroborate it with no further
surprises found. Per the task's explicit stop condition, this is reported as
an honest scoping result, not forced into a stronger claim.

## What is NOT claimed

No claim of novelty. No claim of progress toward the Birch and
Swinnerton-Dyer conjecture (a Clay Millennium Problem) or toward the
Mordell-Weil theorem itself. Nothing here proves finite generation of any
elliptic curve's rational points, defines a height on `E(K)`, proves the
parallelogram law, or establishes weak Mordell-Weil. This is a scoped,
citation-checked inventory of what Mathlib's own in-progress descent-theorem
chain still needs, useful only for deciding whether the lab should invest in a
dedicated future Mordell-Weil front (a substantial arithmetic-geometry project
in its own right, per gap (1) above) — not a step of that front itself.

## Where to pick this up

Anyone opening a dedicated Mordell-Weil front should expect to need, roughly in
increasing order of Galois-cohomology sophistication: (2a) the `addSubMap`
correctness proof (an explicit, if lengthy, polynomial-identity verification
using the Weierstrass relations already encoded in `W.b₂, W.b₄, W.b₆, W.b₈`);
(2b)+(2c) a height on `E(K)` defined via embedding into `ℙ²` (or `ℙ¹` via
`x`-coordinate) composed with the existing `logHeight`/`mulHeight` API, then
the parallelogram law for points assembled from (2a) and the already-proved
coordinate-level bound in `Height/EllipticCurve.lean:45-52`; and finally, as
the largest and separate piece, (1) weak Mordell-Weil via Galois cohomology of
the `n`-torsion, which has no present Mathlib scaffolding at all (no isogeny,
no Kummer map, no elliptic-curve-specific Selmer group) and should be treated
as its own multi-session project rather than a follow-on to this note.
