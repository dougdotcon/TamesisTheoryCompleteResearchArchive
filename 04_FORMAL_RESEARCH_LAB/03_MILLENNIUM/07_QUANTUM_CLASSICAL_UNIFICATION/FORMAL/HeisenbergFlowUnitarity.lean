/-
  QF-7 -- Unitarity of the Heisenberg flow `exp(t • heisenbergGenerator)`,
  `t : ℝ` (revised, real-time-only scope; the originally floated "or ℂ"
  variant was discarded upfront as false in general -- see the HONESTY
  NOTE below). Sibling of WAVE2-QF-5 (`HeisenbergCommutatorFlowIdentity.lean`,
  this directory) and WAVE3-QF-6 (`EhrenfestExpectationValueIdentity.lean`,
  this directory). Wave-4 batch item WAVE4-QF-7.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-4 task instructions on
  build contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other file in this directory, none of which import each other -- only
  Mathlib. Consistent with that precedent, this file does NOT `import`
  `HeisenbergFlowDerivativeProbe.lean` / `HeisenbergCommutatorFlowIdentity.lean`
  / `EhrenfestExpectationValueIdentity.lean` as Lean modules; instead it
  re-declares the identical `heisenbergGenerator` definition locally (see
  below), citing its QF-4 origin.

  HONESTY NOTE (mandatory, per `../SCOPE.md` in this directory's parent).
  "Quantum-Classical Unification" (QCU-001) is a lab-internal extension,
  informally numbered "Problem 8", added at explicit user request. It is
  **not** one of the seven Clay Millennium Problems, has no official
  recognition, no $1,000,000 prize, and no single agreed formal
  statement. This file makes ZERO claim that any Millennium problem
  (Clay-official or otherwise) is solved, approximated, or reachable,
  and ZERO claim of mathematical novelty: unitarity of `exp(tH)` for a
  skew-adjoint `H` is one of the most standard facts in operator theory
  (a direct corollary of `star_exp` and `exp_add_of_commute`), assembled
  here from one existing Mathlib lemma applied at a concrete instance,
  not a new theorem.

  Why `t : ℝ` only, not `t : ℂ`. For `t : ℂ`, `t • heisenbergGenerator`
  is skew-adjoint only when `t` is real (`star (t • x) = conj t • star
  x`, and `conj t • (-x) = -x` forces `conj t = t` when `x ≠ 0`, i.e.
  `t ∈ ℝ`); e.g. at `t = i`, `star(i • H) = conj i • star H = -i • (-H)
  = i • H ≠ -(i • H)` in general, so `exp(i•H)` is generally NOT
  unitary. This was flagged and discarded during the Wave-4 adversarial
  planning review (see this item's plan-code note: "para t:R (NAO 'ou C'
  -- descartado, falso em geral)"), so this file attempts EXACTLY the
  `t : ℝ` statement below, nothing broader.

  MOTIVATION / WHAT THIS FILE DOES, exactly as scoped by the Wave-4 plan.
  QF-4 established `heisenbergGenerator = diag(i, -i)` is skew-Hermitian
  (`heisenbergGenerator_skewHermitian : heisenbergGenerator.conjTranspose
  = -heisenbergGenerator`, `HeisenbergFlowDerivativeProbe.lean`, this
  directory) and that its scalar flow `exp(u • heisenbergGenerator)` has
  a well-defined Fréchet derivative, but did not touch unitarity. This
  file closes exactly that one gap for the flow at real time `t : ℝ`,
  via the prescribed 2-step method:
    (a) `skewAdjoint.smul_mem` at `R := ℝ`, `A := Matrix (Fin 2) (Fin 2)
        ℂ`, fed by `TrivialStar ℝ` (`Real.instTrivialStar`,
        `Mathlib/Data/Real/Star.lean:21`) and `StarModule ℝ (Matrix
        (Fin 2) (Fin 2) ℂ)` (via the generic instance `StarModule α
        (Matrix n n β)` in `Mathlib/LinearAlgebra/Matrix/ConjTranspose.lean:427`,
        itself fed by `StarModule ℝ ℂ`, `Mathlib/Analysis/RCLike/Basic.lean:570`,
        the generic `StarModule ℝ K` instance for any `RCLike K`) --
        applied to the local re-proof of `heisenbergGenerator ∈
        skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ)`, gives `t •
        heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ)` for
        every `t : ℝ`;
    (b) `exp_mem_unitary_of_mem_skewAdjoint`
        (`Mathlib/Analysis/Normed/Algebra/Exponential.lean:539`), applied
        directly to the result of (a), gives `exp (t •
        heisenbergGenerator) ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ)`.
  RESULT: step (a) -- the falsifiable test's own named risk condition --
  went through with ZERO friction, exactly as anticipated: `TrivialStar
  ℝ` and the `StarModule ℝ (Matrix (Fin 2) (Fin 2) ℂ)` chain both
  resolve automatically. Step (b) hit ONE friction point NOT anticipated
  by the plan text (which named step (a) as the risk): see "UNANTICIPATED
  FRICTION POINT" below for the precise sub-step that failed and how it
  was resolved without weakening the statement. Step 2 of the wider
  Wave-4 plan (extension via the inner product, `unitary.mapEquiv` +
  `inner_map_map_of_mem_unitary`) is explicitly NOT attempted here, per
  the plan's own gating ("so only after Passo 1").

  UNANTICIPATED FRICTION POINT (honest report, since it is real even
  though the file closes). `exp_mem_unitary_of_mem_skewAdjoint` needs
  `[ContinuousStar 𝔸]` together with the `[NormedRing 𝔸] [NormedAlgebra
  ℚ 𝔸] [CompleteSpace 𝔸]` instances that `exp` itself needs. Under `open
  scoped Matrix.Norms.Operator` (the ℓ∞/L¹-row operator norm QF-4/QF-5/
  QF-6 all use, since none of them needed `star`-compatibility), this
  `ContinuousStar (Matrix (Fin 2) (Fin 2) ℂ)` instance search FAILED --
  confirmed directly via `set_option trace.Meta.synthInstance true`,
  which showed even a locally-supplied `ContinuousStar (Matrix (Fin 2)
  (Fin 2) ℂ)` hypothesis (proved by hand via `LinearMap.
  continuous_of_finiteDimensional` applied to `star` as an `ℝ`-linear
  map, mirroring QF-6's own technique) failing `tryResolve` against the
  goal despite Lean pretty-printing both sides identically. The
  diagnosis: `Matrix.Norms.Operator`'s norm instances
  (`Matrix.linftyOpSeminormedAddCommGroup` et al., `Mathlib/Analysis/
  Matrix/Normed.lean:238-` onward) do NOT force their embedded
  `TopologicalSpace (Matrix (Fin 2) (Fin 2) ℂ)` field to be
  definitionally the ambient default `Matrix.instTopologicalSpace`
  (`Mathlib/Topology/Instances/Matrix.lean:48`, the Pi-type instance)
  via `UniformSpace.replaceTopology`/`replaceUniformity`, unlike the ℓ²
  operator ("C⋆") norm instances in `Mathlib/Analysis/CStarAlgebra/
  Matrix.lean`, whose `Matrix.instL2OpMetricSpace`
  (`CStarAlgebra/Matrix.lean:174-183`) explicitly does exactly that
  ("We first replace the topology so that we can automatically replace
  the uniformity..."). This is a genuine, real Mathlib diamond specific
  to the `Matrix.Norms.Operator` scope, never exercised by QF-4/QF-5/
  QF-6 because none of them combined a Banach-algebra structure
  (needed for `exp`) with a `star`-continuity requirement in the same
  proof. FIX (not a weakening): switch the opened scope from
  `Matrix.Norms.Operator` to `Matrix.Norms.L2Operator`
  (`open scoped Matrix.Norms.L2Operator`), which supplies
  `Matrix.instCStarRing (Matrix n n 𝕜)` (`CStarAlgebra/Matrix.lean:287`)
  directly -- giving `ContinuousStar` via the two-step generic chain
  `CStarRing.to_normedStarGroup` then `NormedStarGroup.to_continuousStar`
  (`Mathlib/Analysis/CStarAlgebra/Basic.lean:114`, `:72`) -- with no
  diamond, since `instL2OpMetricSpace`'s `replaceTopology` guarantees
  everything (the `NormedRing` used by `exp` AND the `ContinuousStar`
  used by `star_exp`) shares the identical ambient topology. One further
  instance gap surfaced once this switch was made: `NormedAlgebra ℚ
  (Matrix (Fin 2) (Fin 2) ℂ)` (needed by the "Rat" section of
  `Exponential.lean` that `exp_mem_unitary_of_mem_skewAdjoint` lives in)
  is not registered as a global instance (to avoid yet another diamond
  risk), exactly mirroring the precedent at `Mathlib/Analysis/Normed/
  Algebra/Spectrum.lean:374` and `QuaternionExponential.lean:110`, both
  of which supply it by hand via `NormedAlgebra.restrictScalars ℚ 𝕜 A`;
  this file does the same, `NormedAlgebra.restrictScalars ℚ ℂ (Matrix
  (Fin 2) (Fin 2) ℂ)`, fed by `NormedAlgebra ℂ (Matrix (Fin 2) (Fin 2)
  ℂ)` (`Matrix.instL2OpNormedAlgebra`, `CStarAlgebra/Matrix.lean:270`)
  and the standard `NormedAlgebra ℚ ℂ`. With both of these two supplied,
  the file closes genuinely, using nothing beyond the four standard
  proof-kernel primitives (`#print axioms` below confirms this).

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  in addition to compiling cleanly via `lake env lean`):
    - `skewAdjoint.smul_mem`
      (`Mathlib/Algebra/Star/SelfAdjoint.lean:574`)
      `[Star R] [TrivialStar R] [AddCommGroup A] [StarAddMonoid A]
      [Monoid R] [DistribMulAction R A] [StarModule R A] (r : R) {x : A}
      (h : x ∈ skewAdjoint A) : r • x ∈ skewAdjoint A`, instantiated at
      `R := ℝ`, `A := Matrix (Fin 2) (Fin 2) ℂ`.
    - `Real.instTrivialStar` (`Mathlib/Data/Real/Star.lean:21`) supplies
      `TrivialStar ℝ` unconditionally.
    - The generic `StarModule α (Matrix n n β)` instance
      (`Mathlib/LinearAlgebra/Matrix/ConjTranspose.lean:427`)
      `[Star α] [Star β] [SMul α β] [StarModule α β] : StarModule α
      (Matrix n n β)`, chained from the generic `StarModule ℝ K`
      instance for `K` an `RCLike` field (`Mathlib/Analysis/RCLike/Basic.lean:570`)
      instantiated at `K := ℂ`, exactly as the falsifiable test's own
      description of the instance chain anticipates ("via StarModule R C
      encadeado pela instancia generica StarModule a (Matrix n n b)").
    - `Matrix.star_eq_conjTranspose`, `skewAdjoint.mem_iff`
      (`Mathlib/LinearAlgebra/Matrix/ConjTranspose.lean`,
      `Mathlib/Algebra/Star/SelfAdjoint.lean`) used to rephrase
      `heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ)` as
      the concrete conjugate-transpose computation, closed by the same
      `fin_cases`/`simp` proof QF-4 uses for
      `heisenbergGenerator_skewHermitian`
      (`HeisenbergFlowDerivativeProbe.lean`, this directory).
    - `Matrix.instCStarRing`, `Matrix.instL2OpNormedRing`,
      `Matrix.instL2OpNormedAlgebra`
      (`Mathlib/Analysis/CStarAlgebra/Matrix.lean:287,264,270`, all
      `scoped[Matrix.Norms.L2Operator] instance`, activated via `open
      scoped Matrix.Norms.L2Operator`) supply, on the SAME shared
      ℓ²-operator-norm topology (via `Matrix.instL2OpMetricSpace`'s
      explicit `replaceTopology`), everything `exp` and
      `exp_mem_unitary_of_mem_skewAdjoint` need: `NormedRing`,
      `NormedAlgebra ℂ`, `CompleteSpace` (from the default
      `Matrix.instUniformSpace`-matching uniformity), `StarRing`
      (unconditional, `ConjTranspose.lean:431`), and `ContinuousStar`
      (via `CStarRing.to_normedStarGroup` +
      `NormedStarGroup.to_continuousStar`,
      `Mathlib/Analysis/CStarAlgebra/Basic.lean:114,72`).
    - `NormedAlgebra.restrictScalars` (`Mathlib/Analysis/Normed/Algebra/
      Basic.lean`, exact precedent at `Spectrum.lean:374`,
      `QuaternionExponential.lean:110`), supplied by hand for `R := ℚ`,
      `𝕜 := ℂ`, `A := Matrix (Fin 2) (Fin 2) ℂ`, discharging the
      `[NormedAlgebra ℚ 𝔸]` hypothesis of `exp`'s "Rat" section.
    - `exp_mem_unitary_of_mem_skewAdjoint`
      (`Mathlib/Analysis/Normed/Algebra/Exponential.lean:539`, in
      `namespace NormedSpace`) `[StarRing 𝔸] [ContinuousStar 𝔸] {x : 𝔸}
      (h : x ∈ skewAdjoint 𝔸) : exp x ∈ unitary 𝔸`, instantiated at
      `𝔸 := Matrix (Fin 2) (Fin 2) ℂ` as above.

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST, exactly as specified. Fix
  the same `2 × 2` skew-Hermitian generator `heisenbergGenerator =
  diag(i, -i)` as QF-4/QF-5/QF-6. Prove
  `exp (t • heisenbergGenerator) ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ)`
  for every `t : ℝ` (NOT `t : ℂ`, which is false in general -- see the
  HONESTY NOTE above), via exactly the two-step method prescribed:
  `skewAdjoint.smul_mem` then `exp_mem_unitary_of_mem_skewAdjoint` (with
  the norm-scope substitution documented above as the one genuine,
  honestly-reported friction point, resolved without weakening the
  statement).

  WHAT IS STILL MISSING even on full success of this file (stated
  honestly, per the Wave-4 instructions, mirroring QF-4/QF-5/QF-6's own
  honesty sections). This file proves ONLY that the flow of the fixed
  toy generator `heisenbergGenerator` lands in `unitary (Matrix (Fin 2)
  (Fin 2) ℂ)` (the submonoid characterization `star U * U = 1 ∧ U * star
  U = 1`) at every real time `t`. It does **not**: (a) prove any
  Ehrenfest theorem, Schrödinger/Heisenberg equation of motion, or
  correspondence-principle statement -- those are the separate concerns
  of QF-5/QF-6 in this same directory, not reproven or re-used here
  beyond the shared `heisenbergGenerator` definition; (b) extend to
  `t : ℂ` (shown false above) or to any unbounded/physical
  position-momentum generator (per QF-2/QF-3 in this same directory,
  this bounded/finite-dimensional setting cannot even realize the
  canonical commutation relation, so `heisenbergGenerator` is explicitly
  NOT a physical Hamiltonian); (c) connect unitarity of the flow to
  preservation of any inner product / norm of a state vector -- the
  Wave-4 plan's own "Passo 2" (via `unitary.mapEquiv` and
  `inner_map_map_of_mem_unitary`) is explicitly NOT attempted here, only
  the gated "Passo 1" above; (d) connect to any `ħ → 0` classical limit
  or any physical interpretation of `unitary` membership beyond the bare
  algebraic submonoid condition; (e) claim that the `Matrix.Norms.Operator`
  scope (used by QF-4/QF-5/QF-6) can itself support this unitarity
  result -- it cannot, without separately bridging its topology to the
  default one, which this file does NOT attempt (out of scope; the
  `Matrix.Norms.L2Operator` substitution documented above is the
  complete fix used here instead).
-/
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Algebra.Star.Module
import Mathlib.Analysis.RCLike.Basic

open scoped Matrix.Norms.L2Operator
open NormedSpace

namespace QF7.HeisenbergFlowUnitarity

/-- The fixed generator for this probe, identical to QF-4's/QF-5's/QF-6's
`heisenbergGenerator`: `H = diag(i, -i)`, a concrete `2 × 2`
skew-Hermitian complex matrix. Re-declared locally rather than imported,
per this directory's established free-standing-file precedent (see the
header note above). Playing the role of a toy "Hamiltonian-like"
generator for the purposes of this single-identity feasibility test; NOT
claimed to be a physical Hamiltonian (real position/momentum generators
are unbounded, per QF-2 / QF-3 in this same directory). -/
noncomputable def heisenbergGenerator : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.I, 0; 0, -Complex.I]

/-- **Skew-adjoint membership**, the reformulation of QF-4's
`heisenbergGenerator_skewHermitian` needed to feed `skewAdjoint.smul_mem`
below: `heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ)`,
i.e. `star heisenbergGenerator = -heisenbergGenerator`, proved by the
same concrete entrywise computation QF-4 uses for its
`.conjTranspose = -·` statement (`star` on matrices is definitionally
`Matrix.conjTranspose`, via `Matrix.star_eq_conjTranspose`). -/
theorem heisenbergGenerator_mem_skewAdjoint :
    heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ) := by
  rw [skewAdjoint.mem_iff, Matrix.star_eq_conjTranspose]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [heisenbergGenerator, Matrix.conjTranspose_apply]

/-- **Falsifiable-test step (a).** `t • heisenbergGenerator ∈ skewAdjoint
(Matrix (Fin 2) (Fin 2) ℂ)` for every `t : ℝ`, via `skewAdjoint.smul_mem`
instantiated at `R := ℝ`, `A := Matrix (Fin 2) (Fin 2) ℂ` -- fed by
`TrivialStar ℝ` and `StarModule ℝ (Matrix (Fin 2) (Fin 2) ℂ)` (the latter
via the generic `StarModule α (Matrix n n β)` instance chained through
`StarModule ℝ ℂ`), exactly as the falsifiable test prescribes. Both
instances resolve automatically (no friction); the sub-step this file's
falsification condition names did NOT fail -- see the file header's
"UNANTICIPATED FRICTION POINT" note for where the real (different)
friction point turned out to be. -/
theorem smul_heisenbergGenerator_mem_skewAdjoint (t : ℝ) :
    t • heisenbergGenerator ∈ skewAdjoint (Matrix (Fin 2) (Fin 2) ℂ) :=
  skewAdjoint.smul_mem t heisenbergGenerator_mem_skewAdjoint

/-- **Main result (QF-7), the falsifiable test exactly as specified.**
The Heisenberg flow `exp (t • heisenbergGenerator)` is unitary in
`Matrix (Fin 2) (Fin 2) ℂ` for every real time `t : ℝ` -- via
`exp_mem_unitary_of_mem_skewAdjoint` (falsifiable-test step (b)) applied
directly to step (a) above, under the `Matrix.Norms.L2Operator` scope
(see the file header's "UNANTICIPATED FRICTION POINT" note for why this
scope, rather than `Matrix.Norms.Operator`, is needed). NOT claimed, and
explicitly false in general, for `t : ℂ` -- see the file header's
HONESTY NOTE. -/
theorem exp_heisenbergFlow_mem_unitary (t : ℝ) :
    exp (t • heisenbergGenerator) ∈ unitary (Matrix (Fin 2) (Fin 2) ℂ) :=
  haveI : NormedAlgebra ℚ (Matrix (Fin 2) (Fin 2) ℂ) :=
    NormedAlgebra.restrictScalars ℚ ℂ (Matrix (Fin 2) (Fin 2) ℂ)
  exp_mem_unitary_of_mem_skewAdjoint (smul_heisenbergGenerator_mem_skewAdjoint t)

end QF7.HeisenbergFlowUnitarity

#print axioms QF7.HeisenbergFlowUnitarity.heisenbergGenerator_mem_skewAdjoint
#print axioms QF7.HeisenbergFlowUnitarity.smul_heisenbergGenerator_mem_skewAdjoint
#print axioms QF7.HeisenbergFlowUnitarity.exp_heisenbergFlow_mem_unitary
