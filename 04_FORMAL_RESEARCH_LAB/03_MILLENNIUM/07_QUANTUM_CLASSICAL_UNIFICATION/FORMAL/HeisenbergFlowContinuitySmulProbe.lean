/-
  QF-11 -- Isolated probe: does `Continuous (fun t : ℝ => t •
  heisenbergGenerator)` typecheck under `open scoped
  Matrix.Norms.L2Operator`, via `Continuous.smul` / `continuous_smul` or
  the `NormedSpace.exp_continuous` pattern? A pre-requisite check before
  attempting a full `ContinuousMonoidHom` packaging of the Heisenberg
  flow (NOT attempted here -- see "WHAT IS STILL MISSING" below). Direct
  extension of Wave-4 batch item WAVE4-QF-7 (`HeisenbergFlowUnitarity.lean`,
  this directory, unitarity of the flow under `Matrix.Norms.L2Operator`),
  Wave-5 batch item WAVE5-QF-8 (`HeisenbergFlowNormPreservation.lean`,
  this directory) and WAVE5-QF-9 (`HeisenbergFlowGroupLaw.lean`, this
  directory, the bare pointwise addition law `heisenbergFlow_add`).
  Sibling also of Wave-6 batch item WAVE6-QF-10
  (`HeisenbergFlowMonoidHom.lean`, this directory, the algebraic
  `MonoidHom` packaging of the same flow, which this file's own falsifiable
  test description names as the NEXT step this probe is deliberately
  gating). Wave-6 batch item WAVE6-QF-11.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-6 task instructions on
  build contention with 13 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other file in this directory, none of which import each other -- only
  Mathlib. Consistent with that precedent, this file does NOT `import`
  `HeisenbergFlowUnitarity.lean` / `HeisenbergFlowGroupLaw.lean` /
  `HeisenbergFlowMonoidHom.lean` as Lean modules; instead it re-declares
  the identical `heisenbergGenerator` definition locally (see below),
  citing its QF-4 origin.

  HONESTY NOTE (mandatory, per `../SCOPE.md` in this directory's parent).
  "Quantum-Classical Unification" (QCU-001) is a lab-internal extension,
  informally numbered "Problem 8", added at explicit user request. It is
  **not** one of the seven Clay Millennium Problems, has no official
  recognition, no $1,000,000 prize, and no single agreed formal
  statement. This file makes ZERO claim that any Millennium problem
  (Clay-official or otherwise) is solved, approximated, or reachable,
  and ZERO claim of mathematical novelty: that scalar multiplication
  `t ↦ t • x` by a fixed vector `x` in a normed space is continuous is
  one of the most elementary facts in analysis, checked here purely as
  an isolated instance-synthesis feasibility probe for this specific
  concrete matrix type under this specific scoped norm instance -- not a
  new theorem.

  MOTIVATION / WHAT THIS FILE DOES, exactly as scoped by the Wave-6 plan.
  This is deliberately a narrow, isolated pre-requisite check, NOT an
  attempt at the full `ContinuousMonoidHom` packaging of QF-10's
  `heisenbergFlowHom`. The falsifiable test as specified: verify in
  isolation whether `Continuous (fun t : ℝ => t • heisenbergGenerator)`
  typechecks (i.e. is provable) under `open scoped
  Matrix.Norms.L2Operator`, via `Continuous.smul` / `continuous_smul` or
  the `NormedSpace.exp_continuous` pattern -- and if the instance
  synthesis of `ContinuousSMul ℝ (Matrix (Fin 2) (Fin 2) ℂ)` needed to
  discharge it FAILS under that scope, report BLOCKED and do not attempt
  the full `ContinuousMonoidHom` packaging.

  RESULT (the answer to the falsifiable test): **it typechecks with
  ZERO friction.** `ContinuousSMul ℝ (Matrix (Fin 2) (Fin 2) ℂ)`
  synthesizes automatically via `inferInstance` under the
  `Matrix.Norms.L2Operator` scope, and `Continuous (fun t : ℝ => t •
  heisenbergGenerator)` closes by the one-line composition
  `continuous_id.smul continuous_const`, exactly the `Continuous.smul`
  route the falsifiable test names as the primary candidate. This is NOT
  the friction point anticipated by the plan text; see "WHY THIS CLOSES
  WITH NO FRICTION" below for the precise instance chain, which differs
  structurally from the `NormedAlgebra ℚ` friction QF-7/QF-9/QF-10 each
  had to work around by hand.

  WHY THIS CLOSES WITH NO FRICTION (the genuine technical finding of this
  probe). The naive worry -- that discharging `ContinuousSMul ℝ (Matrix
  (Fin 2) (Fin 2) ℂ)` under `Matrix.Norms.L2Operator` would hit the same
  kind of "scalar restriction is not a global instance, to avoid a
  diamond" friction that QF-7/QF-9/QF-10 each hit for `NormedAlgebra ℚ
  (Matrix (Fin 2) (Fin 2) ℂ)` (see QF-7's header, "UNANTICIPATED
  FRICTION POINT") -- does NOT materialize here, for a structurally
  different reason specific to the `ℝ ⊆ ℂ` pair (as opposed to the
  general `ℚ ⊆ 𝕜` pair): Mathlib registers `NormedSpace.complexToReal`
  (`Mathlib/Analysis/Complex/Basic.lean:80`) as an UNCONDITIONAL, GLOBAL
  (lower-priority-900, but still automatically found) instance
  `[SeminormedAddCommGroup E] [NormedSpace ℂ E] : NormedSpace ℝ E` --
  unlike the `ℚ`-scalar-restriction case (`NormedAlgebra.restrictScalars
  ℚ 𝕜 A`, deliberately NOT made a global instance, per QF-7's header,
  "to avoid yet another diamond risk"). The comment directly above that
  instance in the Mathlib source explains why the `ℝ`/`ℂ` pair is safe
  to register globally where the general case is not: `ℝ` is THE
  canonical base field underlying every complex normed space in
  Mathlib's hierarchy, so there is no second, competing "real structure"
  a diamond could arise against, whereas an arbitrary `𝕜' ⊇ 𝕜` pair
  (e.g. `ℚ ⊆ ℂ`) has no such canonicity and is deliberately left
  instance-off. Concretely: under `Matrix.Norms.L2Operator`,
  `Matrix.instL2OpNormedAlgebra` (`Mathlib/Analysis/CStarAlgebra/
  Matrix.lean:270`) supplies `NormedAlgebra ℂ (Matrix (Fin 2) (Fin 2)
  ℂ)`, hence `NormedSpace ℂ (Matrix (Fin 2) (Fin 2) ℂ)`;
  `NormedSpace.complexToReal` then supplies `NormedSpace ℝ (Matrix (Fin
  2) (Fin 2) ℂ)` automatically; and the standard generic fact that a
  `NormedSpace` over a `NormedField` has continuous scalar action
  (`NormedSpace.toModule` chained through the library's standard
  `ContinuousSMul` instance for normed spaces) supplies `ContinuousSMul
  ℝ (Matrix (Fin 2) (Fin 2) ℂ)` -- all without any hand-supplied
  `haveI`, unlike every other file in this Wave-6/Wave-5/Wave-4 QF
  sub-sequence, each of which needed to hand-supply `NormedAlgebra ℚ
  (Matrix (Fin 2) (Fin 2) ℂ)` for the SAME underlying reason
  (`exp`/`exp_continuous` living in a "Rat section" requiring
  `NormedAlgebra ℚ 𝔸`, which the `ℚ`-general case does not auto-derive).
  This probe's own third example (below) confirms that the
  `NormedSpace.exp_continuous` pattern for the FULL flow `t ↦ exp (t •
  heisenbergGenerator)` still needs that same hand-supplied
  `NormedAlgebra ℚ` instance (exactly as QF-7/QF-9/QF-10 each already
  document) -- only the bare `t • heisenbergGenerator` continuity named
  by this probe's exact falsifiable-test statement is friction-free.

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  in addition to compiling cleanly via `lake env lean`):
    - `Matrix.instCStarRing`, `Matrix.instL2OpNormedRing`,
      `Matrix.instL2OpNormedAlgebra`
      (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:287,264,270`, all
      `scoped[Matrix.Norms.L2Operator] instance`, activated via `open
      scoped Matrix.Norms.L2Operator`) -- reused verbatim from
      QF-7/QF-9/QF-10 in this directory, supplying `NormedRing` /
      `NormedAlgebra ℂ` for `Matrix (Fin 2) (Fin 2) ℂ` on the shared
      ℓ²-operator-norm topology.
    - `NormedSpace.complexToReal` (`Mathlib/Analysis/Complex/Basic.lean:80`)
      `[SeminormedAddCommGroup E] [NormedSpace ℂ E] : NormedSpace ℝ E`, an
      unconditional global instance (priority 900), instantiated at
      `E := Matrix (Fin 2) (Fin 2) ℂ` -- the key instance-chain step this
      probe's falsifiable test asked to verify the presence of.
    - `Continuous.smul` (`Mathlib/Topology/Algebra/Module/Basic.lean` and
      generic `Mathlib/Topology/Algebra/MulAction.lean`), the primary
      route the falsifiable test names, applied to `continuous_id` and
      `continuous_const`.
    - `continuous_smul` (`Mathlib/Topology/Algebra/MulAction.lean:49`,
      the `ContinuousSMul` class field itself, `Continuous (fun p : M ×
      X => p.1 • p.2)`), the secondary route the falsifiable test names,
      confirmed directly instantiable at `M := ℝ`, `X := Matrix (Fin 2)
      (Fin 2) ℂ`.
    - `NormedSpace.exp_continuous`
      (`Mathlib/Analysis/Normed/Algebra/Exponential.lean`), the third
      route the falsifiable test names, confirmed to typecheck for the
      FULL flow `t ↦ exp (t • heisenbergGenerator)` -- but, unlike the
      bare `t • heisenbergGenerator` continuity, only after hand-supplying
      `NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2) ℂ)` via
      `NormedAlgebra.restrictScalars ℚ ℂ (Matrix (Fin 2) (Fin 2) ℂ)`,
      exactly as QF-7/QF-9/QF-10 each already document for their own use
      of `exp`.
    - `NormedAlgebra.restrictScalars` (`Mathlib/Analysis/Normed/Algebra/
      Basic.lean`, exact precedent at `Spectrum.lean:374`,
      `QuaternionExponential.lean:110`, reused verbatim from QF-7/QF-9/
      QF-10), supplied by hand ONLY for the third (bonus) example below,
      not for the falsifiable test's own primary statement.

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST, exactly as specified. Fix
  the same `2 × 2` skew-Hermitian generator `heisenbergGenerator =
  diag(i, -i)` as QF-4/.../QF-10. Under `open scoped
  Matrix.Norms.L2Operator`, verify (a) `ContinuousSMul ℝ (Matrix (Fin 2)
  (Fin 2) ℂ)` synthesizes via `inferInstance`; (b) `Continuous (fun t :
  ℝ => t • heisenbergGenerator)` closes via `Continuous.smul`; (c) the
  same statement closes via a manual `continuous_smul` composition; and
  (d, bonus, beyond the letter of the test but directly relevant to the
  probe's stated purpose of gating a future `ContinuousMonoidHom`
  packaging) `Continuous (fun t : ℝ => exp (t • heisenbergGenerator))`
  closes via the `NormedSpace.exp_continuous` pattern once
  `NormedAlgebra ℚ` is hand-supplied exactly as QF-7/QF-9/QF-10 already
  do. All four close with the reported friction profile above -- NONE of
  them are `BLOCKED`.

  WHAT IS STILL MISSING even on full success of this file (stated
  honestly, per the Wave-6 instructions, mirroring QF-4/.../QF-10's own
  honesty sections). This file proves ONLY the four bare continuity
  statements (a)-(d) listed above, each concerning the SCALAR function
  of `t : ℝ` alone (either the linear map `t ↦ t • heisenbergGenerator`
  or its composite with `exp`). It does **not**: (a) assemble
  `heisenbergFlowHom` (QF-10, `HeisenbergFlowMonoidHom.lean`, this
  directory) into a bundled `ContinuousMonoidHom (Multiplicative ℝ)
  (unitary (Matrix (Fin 2) (Fin 2) ℂ))` or any other topological
  one-parameter-group structure -- that packaging step is explicitly
  the NEXT gated step this probe exists to de-risk, not attempted here,
  per this file's own falsifiable-test description ("pre-requisito antes
  do empacotamento ContinuousMonoidHom completo"); (b) prove continuity
  of `heisenbergFlowHom` as a map INTO the `unitary` subtype with its
  subtype topology (only continuity into the ambient `Matrix (Fin 2)
  (Fin 2) ℂ)` is checked here); (c) prove any Ehrenfest theorem,
  Schrödinger/Heisenberg equation of motion, or correspondence-principle
  statement -- those are the separate concerns of QF-5/QF-6 in this same
  directory; (d) extend to `t : ℂ` (shown false for the *unitarity* of
  the flow in QF-7's header; continuity of `t • heisenbergGenerator`
  itself would hold for `t : ℂ` too, but that variant is not attempted,
  since it plays no role in gating the `ContinuousMonoidHom` packaging
  over `Multiplicative ℝ`) or to any unbounded/physical position-momentum
  generator (per QF-2/QF-3 in this same directory, this
  bounded/finite-dimensional setting cannot even realize the canonical
  commutation relation, so `heisenbergGenerator` is explicitly NOT a
  physical Hamiltonian); (e) connect to QF-8's norm/inner-product
  preservation results; (f) connect to any `ħ → 0` classical limit or any
  physical interpretation beyond the bare continuity facts checked.
-/
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.Star.Module
import Mathlib.Analysis.RCLike.Basic

open scoped Matrix.Norms.L2Operator
open NormedSpace

namespace QF11.HeisenbergFlowContinuitySmulProbe

/-- The fixed generator for this probe, identical to QF-4's/.../QF-10's
`heisenbergGenerator`: `H = diag(i, -i)`, a concrete `2 × 2`
skew-Hermitian complex matrix. Re-declared locally rather than imported,
per this directory's established free-standing-file precedent (see the
header note above). Playing the role of a toy "Hamiltonian-like"
generator for the purposes of this single-identity feasibility test; NOT
claimed to be a physical Hamiltonian (real position/momentum generators
are unbounded, per QF-2 / QF-3 in this same directory). -/
noncomputable def heisenbergGenerator : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.I, 0; 0, -Complex.I]

/-- **Instance-synthesis check (the falsifiable test's own named risk
condition).** `ContinuousSMul ℝ (Matrix (Fin 2) (Fin 2) ℂ)` synthesizes
automatically under `Matrix.Norms.L2Operator`, via
`NormedSpace.complexToReal` chained from `Matrix.instL2OpNormedAlgebra`
-- see the file header's "WHY THIS CLOSES WITH NO FRICTION" section for
the full chain. This is the instance whose FAILURE the falsifiable test
asks to be reported as `BLOCKED`; it does not fail. -/
example : ContinuousSMul ℝ (Matrix (Fin 2) (Fin 2) ℂ) := inferInstance

/-- **Main result (QF-11), the falsifiable test's primary statement,
via the `Continuous.smul` route it names first.** The scalar-multiplication
map `t ↦ t • heisenbergGenerator` is continuous on `ℝ`, under the
`Matrix.Norms.L2Operator` scope. -/
theorem continuous_smul_heisenbergGenerator :
    Continuous (fun t : ℝ => t • heisenbergGenerator) :=
  continuous_id.smul continuous_const

/-- **Same statement, via the falsifiable test's secondary named route**
(`continuous_smul`, the defining field of the `ContinuousSMul` class
applied at `M := ℝ`, `X := Matrix (Fin 2) (Fin 2) ℂ`, composed with the
pairing `t ↦ (t, heisenbergGenerator)`), confirming the route is not
merely inferrable as an instance but genuinely usable in a proof term. -/
theorem continuous_smul_heisenbergGenerator_via_continuous_smul :
    Continuous (fun t : ℝ => t • heisenbergGenerator) :=
  show Continuous ((fun p : ℝ × Matrix (Fin 2) (Fin 2) ℂ => p.1 • p.2) ∘
      fun t : ℝ => (t, heisenbergGenerator)) from
    continuous_smul.comp (Continuous.prodMk continuous_id continuous_const)

/-- **Bonus check, beyond the letter of the falisfiable test but directly
relevant to its stated purpose of gating a future `ContinuousMonoidHom`
packaging: continuity of the FULL flow** `t ↦ exp (t •
heisenbergGenerator)`, via the falsifiable test's third named route
(`NormedSpace.exp_continuous`). Unlike the bare `t • heisenbergGenerator`
continuity above, this needs `NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2)
ℂ)` hand-supplied (the same instance QF-7/QF-9/QF-10 each already
hand-supply for their own uses of `exp` -- see the file header). -/
theorem continuous_exp_smul_heisenbergGenerator :
    Continuous (fun t : ℝ => exp (t • heisenbergGenerator)) :=
  haveI : NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2) ℂ) :=
    NormedAlgebra.restrictScalars ℚ ℂ (Matrix (Fin 2) (Fin 2) ℂ)
  NormedSpace.exp_continuous.comp continuous_smul_heisenbergGenerator

end QF11.HeisenbergFlowContinuitySmulProbe

#print axioms QF11.HeisenbergFlowContinuitySmulProbe.continuous_smul_heisenbergGenerator
#print axioms QF11.HeisenbergFlowContinuitySmulProbe.continuous_smul_heisenbergGenerator_via_continuous_smul
#print axioms QF11.HeisenbergFlowContinuitySmulProbe.continuous_exp_smul_heisenbergGenerator
