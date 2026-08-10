/-
  QF-5 -- Heisenberg commutator-flow identity, direct follow-on to QF-4
  (`HeisenbergFlowDerivativeProbe.lean`, Wave-1 batch item, same
  directory). Wave-2 batch item WAVE2-QF-5.

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib
  cache, NOT a full `lake build` -- see the Wave-2 task instructions on
  build contention with 19 concurrent sibling agents). Not registered in
  `TamesisLab.lean`; free-standing, following the precedent of every
  other file in this directory (`CCRFiniteDimImpossibility.lean`,
  `GelfandSelfAdjointRealValued.lean`, `HeisenbergFlowDerivativeProbe.lean`),
  none of which import each other -- only Mathlib. Consistent with that
  precedent, this file does NOT `import` `HeisenbergFlowDerivativeProbe.lean`
  as a Lean module (no such cross-file module wiring exists anywhere in
  this lab's free-standing-probe pattern); instead it re-declares the
  identical `heisenbergGenerator` definition locally (see below), citing
  its QF-4 origin.

  HONESTY NOTE (mandatory, per `../SCOPE.md` in this directory's parent).
  "Quantum-Classical Unification" (QCU-001) is a lab-internal extension,
  informally numbered "Problem 8", added at explicit user request. It is
  **not** one of the seven Clay Millennium Problems, has no official
  recognition, no $1,000,000 prize, and no single agreed formal
  statement. This file makes ZERO claim that any Millennium problem
  (Clay-official or otherwise) is solved, approximated, or reachable,
  and ZERO claim of mathematical novelty: the identity proved here is a
  completely standard, textbook one-line computation (product rule +
  commutation of a generator with its own exponential), assembled here
  from existing Mathlib lemmas, not a new theorem.

  MOTIVATION / WHAT THIS FILE DOES, exactly as scoped by the Wave-2 plan.
  QF-4 established that `hasFDerivAt_exp_smul_const_of_mem_ball`
  instantiates cleanly for the toy skew-Hermitian generator
  `heisenbergGenerator = diag(i, -i)` on `Matrix (Fin 2) (Fin 2) ℂ`, but
  went no further than the single-factor derivative of `u ↦ exp(u • H)`.
  This file extends that one step to the classical "Heisenberg-picture
  flow" 3-factor conjugation `t ↦ exp(t • (-H)) * A * exp(t • H)` (i.e.
  `exp(-tH)·A·exp(tH)` for a fixed matrix `A`), and computes its
  derivative in `t` directly, via:
    (1) instantiating `hasFDerivAt_exp_smul_const_of_mem_ball` at
        `x := -heisenbergGenerator` (packaged as the scalar-valued
        corollary `hasDerivAt_exp_smul_const_of_mem_ball`, which Mathlib
        itself derives from `hasFDerivAt_exp_smul_const_of_mem_ball` in
        exactly one step -- see
        `Mathlib/Analysis/SpecialFunctions/Exponential.lean:327`) to get
        the derivative of `u ↦ exp(u • (-H))` at a point;
    (2) the same instantiation at `x := heisenbergGenerator` for the
        third factor `exp(t • H)`;
    (3) two applications of the noncommutative-ring product rule for
        `HasDerivAt` (`HasDerivAt.mul_const` then `HasDerivAt.mul`, both
        of which are themselves thin scalar-valued wrappers around
        `HasFDerivAt.mul'` -- see
        `Mathlib/Analysis/Calculus/Deriv/Mul.lean:261-266`, which proves
        `HasDerivAt.mul` literally `by rw [...]; exact
        HasFDerivWithinAt.mul' hc hd` up to the `univ`/`WithinAt`
        bookkeeping -- so this is `HasFDerivAt.mul'` applied twice at
        one remove, not a different, unrelated product rule);
    (4) `Commute.exp_right` to slide `heisenbergGenerator` through the
        third factor `exp(t₀ • heisenbergGenerator)` (`H` commutes with
        any scalar multiple of itself, hence with the exponential of
        any scalar multiple of itself);
    (5) `noncomm_ring` to close the resulting pure associative/
        distributive rearrangement into the target commutator form.
  RESULT: this assembly goes through with ZERO friction beyond the
  single `rw` needed to apply step (4) before `noncomm_ring` -- i.e. the
  falsifiable test's own risk condition ("if `HasFDerivAt.mul'` or
  `Commute.exp_right` don't apply the way expected, or the final algebra
  doesn't close via `noncomm_ring`, stop and write a gap note") is NOT
  triggered.

  MATHLIB TOOLS USED (verified present by direct read of the vendored
  snapshot at `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  in addition to compiling cleanly via `lake env lean`):
    - `hasDerivAt_exp_smul_const_of_mem_ball`
      (`Mathlib/Analysis/SpecialFunctions/Exponential.lean:327-330`)
      `HasDerivAt (fun u : 𝕂 => exp (u • x)) (exp (t • x) * x) t`, given
      `t • x ∈ Metric.eball 0 (expSeries 𝕂 𝔸).radius`. Its own one-line
      proof is `(hasStrictDerivAt_exp_smul_const_of_mem_ball x t
      htx).hasDerivAt`, and `hasStrictDerivAt_exp_smul_const_of_mem_ball`
      in turn is `simpa using (hasStrictFDerivAt_exp_smul_const_of_mem_ball
      𝕂 x t htx).hasStrictDerivAt` -- i.e. this scalar-valued corollary
      IS `hasFDerivAt_exp_smul_const_of_mem_ball` (the exact lemma named
      in the Wave-2 falsifiable-test description) instantiated and then
      converted from Fréchet-derivative to scalar-derivative form via
      the standard `smulRight`/`HasStrictFDerivAt.hasStrictDerivAt`
      machinery, not a separate result.
    - `expSeries_radius_eq_top`, `edist_lt_top`,
      `NormedField.toNormedCommRing`, `Matrix.Norms.Operator` scoped
      instances -- same roles as documented in the QF-4 header (see
      `HeisenbergFlowDerivativeProbe.lean` in this same directory for
      the full account); reused here unchanged to discharge the
      `Metric.eball` side condition for both `x := heisenbergGenerator`
      and `x := -heisenbergGenerator`.
    - `HasDerivAt.mul_const`, `HasDerivAt.mul`
      (`Mathlib/Analysis/Calculus/Deriv/Mul.lean:266,303`) the scalar
      noncommutative-ring product rule for `HasDerivAt`, requiring only
      `NormedRing 𝔸` + `NormedAlgebra 𝕜 𝔸` (no commutativity of `𝔸`
      needed) -- applicable to `Matrix (Fin 2) (Fin 2) ℂ` under the
      operator-norm instance activated below, exactly as it is to any
      Banach algebra.
    - `Commute.smul_right`, `Commute.exp_right`
      (`Mathlib/Algebra/Group/Action/Defs.lean:397-399`,
      `Mathlib/Analysis/Normed/Algebra/Exponential.lean:228-230`) used
      together as `(Commute.refl heisenbergGenerator).smul_right t₀
      |>.exp_right : Commute heisenbergGenerator (exp (t₀ •
      heisenbergGenerator))` -- `H` commutes with `t₀ • H` (trivially,
      any element commutes with any scalar multiple of itself), hence
      with `exp (t₀ • H)`.
    - `noncomm_ring` (tactic, `Mathlib/Tactic/NoncommRing.lean`) closes
      the final pure associativity/distributivity rearrangement (plus
      cancellation of `-1`) once the one genuinely noncommutative fact
      (`H` commuting with `exp(t₀ • H)`) has been supplied by hand via
      the `rw` in step (4) above; `noncomm_ring` itself assumes no
      commutativity of multiplication.

  WHAT THIS FILE DOES / THE FALSIFIABLE TEST, exactly as specified.
  Fix the same `2 × 2` skew-Hermitian generator `heisenbergGenerator =
  diag(i, -i)` as QF-4, and an arbitrary fixed matrix `A : Matrix (Fin 2)
  (Fin 2) ℂ`. Prove
  `HasDerivAt (fun t => exp (t • (-heisenbergGenerator)) * A *
  exp (t • heisenbergGenerator))
    (exp (t₀ • (-heisenbergGenerator)) *
      (A * heisenbergGenerator - heisenbergGenerator * A) *
      exp (t₀ • heisenbergGenerator)) t₀`
  for every base point `t₀ : ℂ` -- i.e. `d/dt[exp(-tH)·A·exp(tH)] =
  exp(-tH)·(AH - HA)·exp(tH)`, using `t • (-H) = -(t • H)` (an
  unconditional `smul_neg` fact, not separately invoked below since the
  statement is phrased directly in terms of `t • (-H)`) as the reading
  of `exp(-tH)`.

  WHAT IS STILL MISSING even on full success of this file (stated
  honestly, per the Wave-2 instructions, mirroring QF-4's own honesty
  section). This file proves ONLY the bare derivative identity for the
  fixed finite-dimensional, bounded-operator toy generator
  `heisenbergGenerator`. It does **not**: (a) prove any Ehrenfest
  theorem, correspondence-principle statement, or physical Heisenberg-
  picture equation of motion; (b) touch the inner-product expectation
  `⟨ψ, A(t) ψ⟩` or its derivative, which is what a genuine Ehrenfest
  identity requires (this file computes `d/dt A(t)` as an
  operator-valued curve, not `d/dt ⟨ψ, A(t) ψ⟩` as a scalar-valued
  curve -- connecting the two needs differentiating the sesquilinear
  pairing, not attempted here); (c) generalize beyond a fixed finite
  dimension / bounded operator (per QF-2 in this same directory, this
  bounded/finite-dimensional setting cannot even realize the canonical
  commutation relation, so `heisenbergGenerator` is explicitly NOT a
  physical position/momentum-type generator); (d) connect to any
  `ħ → 0` classical limit or any interpretation of `A*H - H*A` as
  `iħ⁻¹[A, H]` or similar -- the identity here is proved for the bare
  matrix commutator `A*H - H*A`, with no physical constants attached.
-/
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Calculus.Deriv.Mul

open scoped Matrix.Norms.Operator
open NormedSpace

namespace QF5.HeisenbergCommutatorFlowIdentity

/-- The fixed generator for this probe, identical to QF-4's
`heisenbergGenerator` in `HeisenbergFlowDerivativeProbe.lean` (this
directory): `H = diag(i, -i)`, a concrete `2 × 2` skew-Hermitian complex
matrix. Re-declared locally rather than imported, per this directory's
established free-standing-file precedent (see the header note above).
Playing the role of a toy "Hamiltonian-like" generator for the purposes
of this single-identity feasibility test; NOT claimed to be a physical
Hamiltonian (real position/momentum generators are unbounded, per QF-2
/ QF-3 in this same directory). -/
noncomputable def heisenbergGenerator : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.I, 0; 0, -Complex.I]

/-- The exponential-series ball-membership side condition, discharged
exactly as in QF-4: a complete normed algebra has infinite radius of
convergence (`expSeries_radius_eq_top`), so every point is (trivially,
via `edist_lt_top`) inside the ball of that radius. Stated once here and
reused for both `x := heisenbergGenerator` and `x :=
-heisenbergGenerator` below. -/
theorem mem_eball (x : Matrix (Fin 2) (Fin 2) ℂ) (t : ℂ) :
    t • x ∈ Metric.eball (0 : Matrix (Fin 2) (Fin 2) ℂ)
      (expSeries ℂ (Matrix (Fin 2) (Fin 2) ℂ)).radius :=
  (expSeries_radius_eq_top ℂ (Matrix (Fin 2) (Fin 2) ℂ)).symm ▸ edist_lt_top _ _

/-- **Main result (QF-5), the falsifiable test exactly as specified.**
The Heisenberg-picture flow `t ↦ exp(t • (-H)) * A * exp(t • H)` (read
as `exp(-tH)·A·exp(tH)`, for a fixed matrix `A` and the fixed
skew-Hermitian generator `heisenbergGenerator`) has derivative
`exp(t₀ • (-H)) * (A*H - H*A) * exp(t₀ • H)` at every base point
`t₀ : ℂ` -- the Heisenberg commutator-flow identity
`d/dt[exp(-tH)·A·exp(tH)] = exp(-tH)·(AH - HA)·exp(tH)`.

Proof outline (matches the falsifiable test's prescribed method
exactly): instantiate `hasDerivAt_exp_smul_const_of_mem_ball` (itself a
one-step corollary of `hasFDerivAt_exp_smul_const_of_mem_ball`, see the
file header) at `x := -heisenbergGenerator` and separately at
`x := heisenbergGenerator`; combine via `HasDerivAt.mul_const` then
`HasDerivAt.mul` (the scalar-derivative repackaging of
`HasFDerivAt.mul'`, applied twice); slide `heisenbergGenerator` through
`exp (t₀ • heisenbergGenerator)` via `Commute.exp_right`; close the
resulting pure associative/distributive rearrangement with
`noncomm_ring`. -/
theorem hasDerivAt_heisenbergCommutatorFlow
    (A : Matrix (Fin 2) (Fin 2) ℂ) (t₀ : ℂ) :
    HasDerivAt
      (fun t : ℂ => exp (t • (-heisenbergGenerator)) * A *
        exp (t • heisenbergGenerator))
      (exp (t₀ • (-heisenbergGenerator)) *
        (A * heisenbergGenerator - heisenbergGenerator * A) *
        exp (t₀ • heisenbergGenerator))
      t₀ := by
  -- Step 1: instantiate `hasFDerivAt_exp_smul_const_of_mem_ball` (via its
  -- scalar-derivative corollary) at `x := -heisenbergGenerator`, giving
  -- the derivative of `u ↦ exp(u • (-H))` at `t₀` in one step.
  have hf1 : HasDerivAt (fun u : ℂ => exp (u • (-heisenbergGenerator)))
      (exp (t₀ • (-heisenbergGenerator)) * (-heisenbergGenerator)) t₀ :=
    hasDerivAt_exp_smul_const_of_mem_ball (-heisenbergGenerator) t₀
      (mem_eball (-heisenbergGenerator) t₀)
  -- Same instantiation at `x := heisenbergGenerator`, for the third factor.
  have hf3 : HasDerivAt (fun u : ℂ => exp (u • heisenbergGenerator))
      (exp (t₀ • heisenbergGenerator) * heisenbergGenerator) t₀ :=
    hasDerivAt_exp_smul_const_of_mem_ball heisenbergGenerator t₀
      (mem_eball heisenbergGenerator t₀)
  -- Step 2 (first application of the product rule, i.e. `HasFDerivAt.mul'`
  -- at one remove): differentiate `exp(t • (-H)) * A` (`A` constant).
  have h12 : HasDerivAt (fun t : ℂ => exp (t • (-heisenbergGenerator)) * A)
      (exp (t₀ • (-heisenbergGenerator)) * (-heisenbergGenerator) * A) t₀ :=
    hf1.mul_const A
  -- Step 3 (second application of the product rule): differentiate
  -- `(exp(t • (-H)) * A) * exp(t • H)`.
  have h123 := h12.mul hf3
  -- `h123 : HasDerivAt (fun t => exp(t•(-H)) * A * exp(t•H))
  --   (exp(t₀•(-H)) * (-H) * A * exp(t₀•H)
  --     + exp(t₀•(-H)) * A * (exp(t₀•H) * H)) t₀`.
  -- Step 4: slide `heisenbergGenerator` through `exp(t₀ • heisenbergGenerator)`
  -- via `Commute.exp_right` (`H` commutes with any scalar multiple of
  -- itself, hence with the exponential of any scalar multiple of itself).
  have hcommute : Commute heisenbergGenerator (exp (t₀ • heisenbergGenerator)) :=
    ((Commute.refl heisenbergGenerator).smul_right t₀).exp_right
  have hswap : exp (t₀ • heisenbergGenerator) * heisenbergGenerator
      = heisenbergGenerator * exp (t₀ • heisenbergGenerator) := hcommute.symm.eq
  rw [hswap] at h123
  -- Step 5: close the final pure associative/distributive rearrangement.
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

end QF5.HeisenbergCommutatorFlowIdentity

#print axioms QF5.HeisenbergCommutatorFlowIdentity.mem_eball
#print axioms QF5.HeisenbergCommutatorFlowIdentity.hasDerivAt_heisenbergCommutatorFlow
