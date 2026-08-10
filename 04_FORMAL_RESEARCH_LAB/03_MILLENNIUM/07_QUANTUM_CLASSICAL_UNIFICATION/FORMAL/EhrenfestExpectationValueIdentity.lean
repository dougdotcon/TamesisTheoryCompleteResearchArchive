/-
  QF-6 -- Ehrenfest-theorem expectation-value identity, pairing WAVE2-QF-5's
  operator-flow commutator identity (`HeisenbergCommutatorFlowIdentity.lean`,
  this directory) with a fixed state vector. Wave-3 batch item WAVE3-QF-6.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` -- see the Wave-3 task instructions on build
  contention with 14 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every other
  file in this directory, none of which import each other -- only Mathlib.
  Consistent with that precedent, this file does NOT `import`
  `HeisenbergCommutatorFlowIdentity.lean` as a Lean module; instead it
  re-declares the identical `heisenbergGenerator` definition locally (see
  below) and redoes QF-5's product-rule derivative computation with the time
  parameter `t : ℝ` instead of `t : ℂ` (QF-5 used `t : ℂ` throughout), which
  turns out to be the crux of why this file works at all -- see the HONESTY
  NOTE and MOTIVATION sections below.

  HONESTY NOTE (mandatory, per `../SCOPE.md` in this directory's parent).
  "Quantum-Classical Unification" (QCU-001) is a lab-internal extension,
  informally numbered "Problem 8", added at explicit user request. It is
  **not** one of the seven Clay Millennium Problems, has no official
  recognition, no $1,000,000 prize, and no single agreed formal statement.
  This file makes ZERO claim that any Millennium problem (Clay-official or
  otherwise) is solved, approximated, or reachable, and ZERO claim of
  mathematical novelty: the identity proved here is a completely standard,
  textbook computation (product rule for the Heisenberg-picture flow,
  composed with the derivative of the sesquilinear inner-product pairing at
  a fixed vector), assembled here from existing Mathlib lemmas, not a new
  theorem.

  MOTIVATION / WHAT THIS FILE DOES, exactly as scoped by the Wave-3 plan.
  QF-5 proved the *operator*-valued identity
  `d/dt[exp(-tH)·A·exp(tH)] = exp(-tH)·(AH-HA)·exp(tH)` for `t : ℂ`, but
  explicitly stopped short of the inner-product expectation value
  `⟨ψ, A(t) ψ⟩` (see QF-5's own "WHAT IS STILL MISSING" section, item (b)).
  This file closes exactly that one remaining gap for a *fixed* state vector
  `ψ`, using the falsifiable test's prescribed 4-step method:
    (1) confirm `NormedAlgebra ℝ (Matrix (Fin 2) (Fin 2) ℂ)` resolves (via
        `Matrix.linftyOpNormedAlgebra` instantiated at the base field
        `R := ℝ`, using `NormedAlgebra ℝ ℂ` -- the latter is the automatic
        instance `Complex.instNormedAlgebra` for any `NormedAlgebra R ℝ`,
        here trivially `R := ℝ` itself, registered in
        `Mathlib/Analysis/Complex/Basic.lean` -- see the MATHLIB TOOLS
        section for the exact instance);
    (2) rerun `hasDerivAt_exp_smul_const_of_mem_ball` -- and hence QF-5's
        entire product-rule derivative computation -- with the *scalar*
        type instantiated at `𝕂 := ℝ` (so `t₀ : ℝ`) instead of `𝕂 := ℂ`.
        This is not cosmetic: Mathlib's `HasDerivAt.inner`
        (`Mathlib/Analysis/InnerProductSpace/Calculus.lean:109`) is stated
        ONLY for curves `f g : ℝ → E`, because the inner product
        `(x, y) ↦ ⟪x, y⟫` on a complex inner-product space is only
        `ℝ`-bilinear (it is conjugate-linear, not linear, in its first
        argument), so there is no complex-differentiability statement for
        it to plug into -- `t : ℂ` as in QF-5 would make step (4) below
        inapplicable;
    (3) build the fixed ℂ-linear "evaluate at ψ" map
        `A ↦ (Matrix.toEuclideanLin A) ψ` (via `LinearMap.applyₗ` composed
        with `Matrix.toEuclideanLin`), restrict its scalars to `ℝ` via
        `LinearMap.restrictScalars`, and promote it to a continuous ℝ-linear
        map using `LinearMap.continuous_of_finiteDimensional`
        (`Mathlib/Topology/Algebra/Module/FiniteDimension.lean:277`) --
        every ℝ-linear map out of the (finite-dimensional, Hausdorff) real
        vector space `Matrix (Fin 2) (Fin 2) ℂ` is automatically continuous;
    (4) chain the operator-valued derivative from step (2) through this
        continuous linear map via `HasFDerivAt.comp_hasDerivAt`
        (`Mathlib/Analysis/Calculus/Deriv/Comp.lean:389`), then combine with
        the constant curve `t ↦ ψ` via `HasDerivAt.inner`
        (`Mathlib/Analysis/InnerProductSpace/Calculus.lean:109`), and close
        the final commutator-form rearrangement -- both the QF-5-style
        product-rule algebra and a small extra step re-expressing the
        result via `A t₀` itself rather than the raw exponentials -- with
        `noncomm_ring` plus one `Commute.exp_right`-derived rewrite, exactly
        mirroring QF-5's own closing step.
  RESULT: this assembly goes through with ZERO friction beyond the changes
  already anticipated by the falsifiable test itself (the `𝕂 := ℝ`
  reinstantiation of step (2), and the `LinearMap.applyₗ` /
  `LinearMap.restrictScalars` / `LinearMap.continuous_of_finiteDimensional`
  chain of step (3)) -- i.e. the falsifiable test's own risk condition ("if
  any of the 4 steps doesn't apply the way expected, stop and report which
  one") is NOT triggered. All 4 steps closed.

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  in addition to compiling cleanly via `lake env lean`):
    - `Matrix.linftyOpNormedAlgebra`
      (`Mathlib/Analysis/Matrix/Normed.lean:401-403`)
      `[NormedField R] [SeminormedRing α] [NormedAlgebra R α] [DecidableEq n]
      → NormedAlgebra R (Matrix n n α)`, a scoped instance activated (along
      with the underlying norm/ring instances) via
      `open scoped Matrix.Norms.Operator`, exactly as in QF-4/QF-5.
      Instantiated here at `R := ℝ`, `α := ℂ`, `n := Fin 2`.
    - `Complex.instNormedAlgebra`-style instance
      (`Mathlib/Analysis/Complex/Basic.lean`, the unnamed instance
      `instance {R : Type*} [NormedField R] [NormedAlgebra R ℝ] :
      NormedAlgebra R ℂ`) supplying `NormedAlgebra ℝ ℂ` from the trivial
      `NormedAlgebra ℝ ℝ`, feeding `Matrix.linftyOpNormedAlgebra` above.
    - `hasDerivAt_exp_smul_const_of_mem_ball`
      (`Mathlib/Analysis/SpecialFunctions/Exponential.lean:327-330`), same
      lemma QF-4/QF-5 used, but with its scalar type `𝕂` instantiated at
      `ℝ` (inferred from `t₀ : ℝ`) instead of `ℂ`. Crucially, the
      exponential map `NormedSpace.exp` itself is defined independently of
      `𝕂` (as the sum of `expSeries ℚ 𝔸`, see
      `Mathlib/Analysis/Normed/Algebra/Exponential.lean:107-130`), so the
      `exp` produced here is the literal same function as QF-4/QF-5's,
      not a different `𝕂`-dependent variant -- no diamond between the
      `𝕂 := ℝ` and `𝕂 := ℂ` instantiations of this lemma.
    - `expSeries_radius_eq_top`
      (`Mathlib/Analysis/Normed/Algebra/Exponential.lean:451`), same
      unconditional fact as QF-4/QF-5, re-invoked at `𝕂 := ℝ` (needs only
      `NontriviallyNormedField ℝ`, `CharZero ℝ`, `ContinuousSMul ℚ ℝ`, all
      automatic).
    - `HasDerivAt.mul_const`, `HasDerivAt.mul`
      (`Mathlib/Analysis/Calculus/Deriv/Mul.lean:266,303`), same
      noncommutative-ring product rule as QF-5, re-invoked over `𝕜 := ℝ`
      instead of `𝕜 := ℂ` (needs `NormedAlgebra ℝ (Matrix (Fin 2) (Fin 2)
      ℂ)`, confirmed by step (1) above).
    - `Commute.smul_right`, `Commute.exp_right` -- same as QF-5, unchanged.
    - `noncomm_ring` (tactic) -- same as QF-5, unchanged.
    - `Matrix.toEuclideanLin`
      (`Mathlib/Analysis/InnerProductSpace/PiL2.lean:1242`)
      `Matrix m n 𝕜 ≃ₗ[𝕜] EuclideanSpace 𝕜 n →ₗ[𝕜] EuclideanSpace 𝕜 m`, a
      shorthand for `Matrix.toLpLin 2 2`; its `.toLinearMap` coercion is
      composed with `LinearMap.applyₗ` below.
    - `LinearMap.applyₗ`
      (`Mathlib/Algebra/Module/LinearMap/End.lean:387`)
      `M →ₗ[R] (M →ₗ[R] M₂) →ₗ[R] M₂`, "evaluate the linear-map argument at
      a fixed point of `M`", used at `R := ℂ`, `M := EuclideanSpace ℂ
      (Fin 2)`, `M₂ := EuclideanSpace ℂ (Fin 2)`, fixed point `ψ`.
    - `LinearMap.restrictScalars`
      (`Mathlib/Algebra/Module/LinearMap/Defs.lean`) turns the composed
      `ℂ`-linear map `A ↦ (Matrix.toEuclideanLin A) ψ` into an `ℝ`-linear
      map on the same underlying function, via the scalar tower `ℝ ≤ ℂ`.
    - `LinearMap.continuous_of_finiteDimensional`
      (`Mathlib/Topology/Algebra/Module/FiniteDimension.lean:277`)
      `[T2Space E] [FiniteDimensional 𝕜 E] → (E →ₗ[𝕜] F') → Continuous f`,
      instantiated at `𝕜 := ℝ`, `E := Matrix (Fin 2) (Fin 2) ℂ` (Hausdorff
      as a metric space; finite-dimensional over `ℝ` since it is
      finite-dimensional over `ℂ`, which is itself finite-dimensional over
      `ℝ`), `F' := EuclideanSpace ℂ (Fin 2)` (as an `ℝ`-module via
      restriction of scalars). Used to package the restricted-scalars
      linear map above as a `ContinuousLinearMap`.
    - `ContinuousLinearMap.hasFDerivAt`
      (`Mathlib/Analysis/Calculus/FDeriv/Linear.lean:57`) any continuous
      linear map is its own Fréchet derivative at every point.
    - `HasFDerivAt.comp_hasDerivAt`
      (`Mathlib/Analysis/Calculus/Deriv/Comp.lean:389`) chains the
      operator-curve derivative from the QF-5-style computation through the
      continuous linear "evaluate at ψ" map.
    - `HasDerivAt.inner`
      (`Mathlib/Analysis/InnerProductSpace/Calculus.lean:109`)
      `{f g : ℝ → E} → HasDerivAt f f' x → HasDerivAt g g' x →
      HasDerivAt (fun t => ⟪f t, g t⟫) (⟪f x, g'⟫ + ⟪f', g x⟫) x` -- the
      one lemma in this whole chain that forces `t : ℝ` rather than `t : ℂ`
      (see MOTIVATION above). Applied with `f` the constant curve `ψ`
      (`hasDerivAt_const`, giving `f' = 0`) and `g` the composed curve from
      the previous step.
    - `inner_zero_left` (simp lemma) discharges the `⟪0, _⟫ = 0` term left
      over from `f' = 0` in the `HasDerivAt.inner` output.

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST, exactly as specified. Fix the
  same `2 × 2` skew-Hermitian generator `heisenbergGenerator = diag(i, -i)`
  as QF-4/QF-5, an arbitrary fixed matrix `A : Matrix (Fin 2) (Fin 2) ℂ`, and
  an arbitrary fixed vector `ψ : EuclideanSpace ℂ (Fin 2)`. Writing
  `A t := exp (t • (-heisenbergGenerator)) * A * exp (t • heisenbergGenerator)`
  for the Heisenberg-picture flow of `A` (real time parameter `t : ℝ` this
  time, not complex), prove
  `HasDerivAt (fun t : ℝ => ⟪ψ, Matrix.toEuclideanLin (A t) ψ⟫)
    ⟪ψ, Matrix.toEuclideanLin (A t₀ * heisenbergGenerator -
      heisenbergGenerator * A t₀) ψ⟫ t₀`
  for every base point `t₀ : ℝ` -- i.e. the Ehrenfest expectation-value
  identity `d/dt ⟨ψ, A(t) ψ⟩ = ⟨ψ, (A(t) H - H A(t)) ψ⟩`.

  WHAT IS STILL MISSING even on full success of this file (stated honestly,
  per the Wave-3 instructions, mirroring QF-4's and QF-5's own honesty
  sections). This file proves ONLY the bare expectation-value derivative
  identity for the fixed finite-dimensional, bounded-operator toy generator
  `heisenbergGenerator`, a fixed constant matrix `A`, and a fixed constant
  vector `ψ` (none of `A`, `ψ`, `heisenbergGenerator` themselves evolve
  under any equation of motion beyond the flow `A t` already defined by
  QF-5's construction). It does **not**: (a) prove any physical Ehrenfest
  theorem, correspondence-principle statement, or general Heisenberg
  equation of motion -- "Ehrenfest" is used here only as the informal name
  for this specific finite-dimensional bare-commutator identity, per QF-5's
  and QF-4's own honesty conventions; (b) attach any physical constant
  (`ħ`, `i`, or similar) to the commutator `A t₀ * H - H * A t₀` -- the
  identity is proved for the bare matrix commutator, exactly as QF-5 left
  it; (c) generalize beyond a fixed finite dimension / bounded operator /
  fixed state vector (per QF-2/QF-3 in this same directory, this
  bounded/finite-dimensional setting cannot even realize the canonical
  commutation relation, so `heisenbergGenerator` is explicitly NOT a
  physical position/momentum-type generator, and `ψ` here is not evolving
  under any Schrödinger equation); (d) connect to any `ħ → 0` classical
  limit or any interpretation of the commutator as a Poisson bracket.
-/
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Topology.Algebra.Module.FiniteDimension

open scoped Matrix.Norms.Operator
open NormedSpace

namespace QF6.EhrenfestExpectationValueIdentity

/-- The fixed generator for this probe, identical to QF-4's and QF-5's
`heisenbergGenerator`: `H = diag(i, -i)`, a concrete `2 × 2` skew-Hermitian
complex matrix. Re-declared locally rather than imported, per this
directory's established free-standing-file precedent (see the header note
above). Playing the role of a toy "Hamiltonian-like" generator for the
purposes of this single-identity feasibility test; NOT claimed to be a
physical Hamiltonian (real position/momentum generators are unbounded, per
QF-2 / QF-3 in this same directory). -/
noncomputable def heisenbergGenerator : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.I, 0; 0, -Complex.I]

/-- **Falsifiable-test step (1).** `Matrix (Fin 2) (Fin 2) ℂ` is a normed
algebra over `ℝ`, not just over `ℂ`: via `Matrix.linftyOpNormedAlgebra`
(activated by `open scoped Matrix.Norms.Operator` above) instantiated at the
base field `R := ℝ`, fed by the automatic instance `NormedAlgebra ℝ ℂ`
(itself `NormedAlgebra R ℂ` at `R := ℝ`, from the trivial `NormedAlgebra ℝ
ℝ`). Stated here as an explicit sanity check, exactly as the falsifiable
test's step (1) prescribes. -/
noncomputable example : NormedAlgebra ℝ (Matrix (Fin 2) (Fin 2) ℂ) := inferInstance

/-- The exponential-series ball-membership side condition, discharged
exactly as in QF-4/QF-5 but at the base field `ℝ` instead of `ℂ`: a
complete normed algebra has infinite radius of convergence
(`expSeries_radius_eq_top`), so every point is (trivially, via
`edist_lt_top`) inside the ball of that radius. -/
theorem mem_eball (x : Matrix (Fin 2) (Fin 2) ℂ) (t : ℝ) :
    t • x ∈ Metric.eball (0 : Matrix (Fin 2) (Fin 2) ℂ)
      (expSeries ℝ (Matrix (Fin 2) (Fin 2) ℂ)).radius :=
  (expSeries_radius_eq_top ℝ (Matrix (Fin 2) (Fin 2) ℂ)).symm ▸ edist_lt_top _ _

/-- **Falsifiable-test step (2), the QF-5 commutator-flow identity rerun at
`𝕂 := ℝ`.** Identical proof to QF-5's `hasDerivAt_heisenbergCommutatorFlow`,
with `t₀ : ℝ` instead of `t₀ : ℂ` throughout (the change the falsifiable
test's step (2) asks for). This is the operator-valued half of the
Ehrenfest identity; the state-vector pairing is added below. -/
theorem hasDerivAt_heisenbergCommutatorFlow
    (A : Matrix (Fin 2) (Fin 2) ℂ) (t₀ : ℝ) :
    HasDerivAt
      (fun t : ℝ => exp (t • (-heisenbergGenerator)) * A *
        exp (t • heisenbergGenerator))
      (exp (t₀ • (-heisenbergGenerator)) *
        (A * heisenbergGenerator - heisenbergGenerator * A) *
        exp (t₀ • heisenbergGenerator))
      t₀ := by
  have hf1 : HasDerivAt (fun u : ℝ => exp (u • (-heisenbergGenerator)))
      (exp (t₀ • (-heisenbergGenerator)) * (-heisenbergGenerator)) t₀ :=
    hasDerivAt_exp_smul_const_of_mem_ball (-heisenbergGenerator) t₀
      (mem_eball (-heisenbergGenerator) t₀)
  have hf3 : HasDerivAt (fun u : ℝ => exp (u • heisenbergGenerator))
      (exp (t₀ • heisenbergGenerator) * heisenbergGenerator) t₀ :=
    hasDerivAt_exp_smul_const_of_mem_ball heisenbergGenerator t₀
      (mem_eball heisenbergGenerator t₀)
  have h12 : HasDerivAt (fun t : ℝ => exp (t • (-heisenbergGenerator)) * A)
      (exp (t₀ • (-heisenbergGenerator)) * (-heisenbergGenerator) * A) t₀ :=
    hf1.mul_const A
  have h123 := h12.mul hf3
  have hcommute : Commute heisenbergGenerator (exp (t₀ • heisenbergGenerator)) :=
    ((Commute.refl heisenbergGenerator).smul_right t₀).exp_right
  have hswap : exp (t₀ • heisenbergGenerator) * heisenbergGenerator
      = heisenbergGenerator * exp (t₀ • heisenbergGenerator) := hcommute.symm.eq
  rw [hswap] at h123
  have halgebra :
      exp (t₀ • (-heisenbergGenerator)) * (-heisenbergGenerator) * A *
          exp (t₀ • heisenbergGenerator) +
        exp (t₀ • (-heisenbergGenerator)) * A *
          (heisenbergGenerator * exp (t₀ • heisenbergGenerator)) =
      exp (t₀ • (-heisenbergGenerator)) *
        (A * heisenbergGenerator - heisenbergGenerator * A) *
        exp (t₀ • heisenbergGenerator) := by
    noncomm_ring
  rw [halgebra] at h123
  exact h123

/-- The Heisenberg-picture flow of a fixed matrix `A`, as a curve in `t`,
named for readability in the final statement below: `flow A t = exp(t•(-H))
* A * exp(t•H)`, matching QF-5's unnamed curve. -/
noncomputable def flow (A : Matrix (Fin 2) (Fin 2) ℂ) (t : ℝ) :
    Matrix (Fin 2) (Fin 2) ℂ :=
  exp (t • (-heisenbergGenerator)) * A * exp (t • heisenbergGenerator)

theorem hasDerivAt_flow (A : Matrix (Fin 2) (Fin 2) ℂ) (t₀ : ℝ) :
    HasDerivAt (flow A)
      (exp (t₀ • (-heisenbergGenerator)) *
        (A * heisenbergGenerator - heisenbergGenerator * A) *
        exp (t₀ • heisenbergGenerator))
      t₀ :=
  hasDerivAt_heisenbergCommutatorFlow A t₀

/-- **Falsifiable-test step (3).** The fixed `ℂ`-linear "evaluate
`Matrix.toEuclideanLin A` at `ψ`" map, built via `LinearMap.applyₗ` composed
with (the linear-map coercion of) `Matrix.toEuclideanLin`, exactly as
prescribed. -/
noncomputable def evalAtPsiₗ (ψ : EuclideanSpace ℂ (Fin 2)) :
    Matrix (Fin 2) (Fin 2) ℂ →ₗ[ℂ] EuclideanSpace ℂ (Fin 2) :=
  (LinearMap.applyₗ ψ).comp
    (Matrix.toEuclideanLin (𝕜 := ℂ) (m := Fin 2) (n := Fin 2)).toLinearMap

@[simp]
theorem evalAtPsiₗ_apply (ψ : EuclideanSpace ℂ (Fin 2)) (A : Matrix (Fin 2) (Fin 2) ℂ) :
    evalAtPsiₗ ψ A = Matrix.toEuclideanLin A ψ := rfl

/-- **Falsifiable-test step (3), continued.** `evalAtPsiₗ ψ`, restricted to
`ℝ`-linearity and promoted to a `ContinuousLinearMap` via
`LinearMap.continuous_of_finiteDimensional` (every `ℝ`-linear map out of the
finite-dimensional Hausdorff space `Matrix (Fin 2) (Fin 2) ℂ` is
automatically continuous). -/
noncomputable def evalAtPsiL (ψ : EuclideanSpace ℂ (Fin 2)) :
    Matrix (Fin 2) (Fin 2) ℂ →L[ℝ] EuclideanSpace ℂ (Fin 2) :=
  ⟨(evalAtPsiₗ ψ).restrictScalars ℝ,
    ((evalAtPsiₗ ψ).restrictScalars ℝ).continuous_of_finiteDimensional⟩

@[simp]
theorem evalAtPsiL_apply (ψ : EuclideanSpace ℂ (Fin 2)) (A : Matrix (Fin 2) (Fin 2) ℂ) :
    evalAtPsiL ψ A = Matrix.toEuclideanLin A ψ := rfl

/-- **Falsifiable-test step (4).** The composed curve `t ↦ Matrix.toEuclideanLin
(flow A t) ψ` has derivative `Matrix.toEuclideanLin A'(t₀) ψ` at `t₀`, via
`HasFDerivAt.comp_hasDerivAt` chaining `evalAtPsiL ψ`'s own derivative
(`ContinuousLinearMap.hasFDerivAt`) through `hasDerivAt_flow`. -/
theorem hasDerivAt_flow_apply_psi
    (A : Matrix (Fin 2) (Fin 2) ℂ) (ψ : EuclideanSpace ℂ (Fin 2)) (t₀ : ℝ) :
    HasDerivAt (fun t : ℝ => Matrix.toEuclideanLin (flow A t) ψ)
      (Matrix.toEuclideanLin
        (exp (t₀ • (-heisenbergGenerator)) *
          (A * heisenbergGenerator - heisenbergGenerator * A) *
          exp (t₀ • heisenbergGenerator)) ψ)
      t₀ := by
  have hcomp := (evalAtPsiL ψ).hasFDerivAt.comp_hasDerivAt t₀ (hasDerivAt_flow A t₀)
  exact hcomp

/-- Purely algebraic helper (holds in any, possibly noncommutative, ring):
if `e1` and `e2` both commute with `H`, then the derivative-of-conjugation
commutator `(e1*X*e2)*H - H*(e1*X*e2)` re-expresses as the conjugated bare
commutator `e1*(X*H-H*X)*e2`. This is exactly the extra algebraic step (on
top of QF-5's own closing step) needed to restate the Ehrenfest identity's
RHS in terms of `flow A t₀` itself rather than the raw exponentials. -/
private theorem conj_commutator_eq {R : Type*} [Ring R] (e1 e2 X H : R)
    (h1 : H * e1 = e1 * H) (h2 : e2 * H = H * e2) :
    (e1 * X * e2) * H - H * (e1 * X * e2) = e1 * (X * H - H * X) * e2 := by
  rw [mul_assoc (e1 * X) e2 H, h2, ← mul_assoc H (e1 * X) e2, ← mul_assoc H e1 X, h1]
  noncomm_ring

/-- The derivative value from `hasDerivAt_flow`, re-expressed via `flow A t₀`
itself (i.e. `flow A t₀ * H - H * flow A t₀`) rather than via the raw
exponentials, using `conj_commutator_eq` fed by two `Commute.exp_right`
facts (one of them, for `exp(t₀•(-H))`, is the mirror image of the one QF-5
uses for `exp(t₀•H)`). -/
theorem flow_mul_sub_mul_eq
    (A : Matrix (Fin 2) (Fin 2) ℂ) (t₀ : ℝ) :
    flow A t₀ * heisenbergGenerator - heisenbergGenerator * flow A t₀ =
      exp (t₀ • (-heisenbergGenerator)) *
        (A * heisenbergGenerator - heisenbergGenerator * A) *
        exp (t₀ • heisenbergGenerator) := by
  have hcommute : Commute heisenbergGenerator (exp (t₀ • heisenbergGenerator)) :=
    ((Commute.refl heisenbergGenerator).smul_right t₀).exp_right
  have hcommuteNeg : Commute heisenbergGenerator (exp (t₀ • (-heisenbergGenerator))) :=
    ((Commute.refl heisenbergGenerator).neg_right.smul_right t₀).exp_right
  show
    (exp (t₀ • (-heisenbergGenerator)) * A * exp (t₀ • heisenbergGenerator)) *
        heisenbergGenerator -
      heisenbergGenerator *
        (exp (t₀ • (-heisenbergGenerator)) * A * exp (t₀ • heisenbergGenerator)) =
    exp (t₀ • (-heisenbergGenerator)) *
      (A * heisenbergGenerator - heisenbergGenerator * A) *
      exp (t₀ • heisenbergGenerator)
  exact conj_commutator_eq (exp (t₀ • (-heisenbergGenerator))) (exp (t₀ • heisenbergGenerator))
    A heisenbergGenerator hcommuteNeg.eq hcommute.symm.eq

/-- **Main result (QF-6), the falsifiable test exactly as specified.** The
Ehrenfest expectation-value identity: the scalar-valued curve
`t ↦ ⟪ψ, Matrix.toEuclideanLin (flow A t) ψ⟫` (the expectation value of the
Heisenberg-picture-evolved observable `A` in the fixed state `ψ`) has
derivative `⟪ψ, Matrix.toEuclideanLin (flow A t₀ * H - H * flow A t₀) ψ⟫` at
every base point `t₀ : ℝ`, i.e.
`d/dt ⟨ψ, A(t) ψ⟩ = ⟨ψ, (A(t) H - H A(t)) ψ⟩`. -/
theorem hasDerivAt_ehrenfestExpectationValue
    (A : Matrix (Fin 2) (Fin 2) ℂ) (ψ : EuclideanSpace ℂ (Fin 2)) (t₀ : ℝ) :
    HasDerivAt
      (fun t : ℝ => (inner ℂ ψ (Matrix.toEuclideanLin (flow A t) ψ) : ℂ))
      (inner ℂ ψ (Matrix.toEuclideanLin
        (flow A t₀ * heisenbergGenerator - heisenbergGenerator * flow A t₀) ψ) : ℂ)
      t₀ := by
  have hconst : HasDerivAt (fun _ : ℝ => ψ) (0 : EuclideanSpace ℂ (Fin 2)) t₀ :=
    hasDerivAt_const t₀ ψ
  have hg := hasDerivAt_flow_apply_psi A ψ t₀
  have hpair := hconst.inner ℂ hg
  simp only [inner_zero_left, add_zero] at hpair
  -- `hpair : HasDerivAt (fun t => ⟪ψ, toEuclideanLin (flow A t) ψ⟫)
  --   ⟪ψ, toEuclideanLin (exp(t₀•(-H)) * (A*H - H*A) * exp(t₀•H)) ψ⟫ t₀`.
  rw [flow_mul_sub_mul_eq]
  exact hpair

end QF6.EhrenfestExpectationValueIdentity

#print axioms QF6.EhrenfestExpectationValueIdentity.mem_eball
#print axioms QF6.EhrenfestExpectationValueIdentity.hasDerivAt_heisenbergCommutatorFlow
#print axioms QF6.EhrenfestExpectationValueIdentity.hasDerivAt_flow
#print axioms QF6.EhrenfestExpectationValueIdentity.evalAtPsiₗ_apply
#print axioms QF6.EhrenfestExpectationValueIdentity.evalAtPsiL_apply
#print axioms QF6.EhrenfestExpectationValueIdentity.hasDerivAt_flow_apply_psi
#print axioms QF6.EhrenfestExpectationValueIdentity.conj_commutator_eq
#print axioms QF6.EhrenfestExpectationValueIdentity.flow_mul_sub_mul_eq
#print axioms QF6.EhrenfestExpectationValueIdentity.hasDerivAt_ehrenfestExpectationValue
