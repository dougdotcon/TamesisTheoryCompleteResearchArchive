/-
  WAVE6-RH-7B — `Tp`, the toy unbounded diagonal `LinearPMap` on its finite-support domain
  (the SAME `Tp` used throughout `UnboundedEigCountFloorLaw.lean` (RH-3, Wave 3),
  `UnboundedEigCountWeylLimitLaw.lean` (RH-4, Wave 4), `EigenvalueSetBridgeRestricted.lean`
  (RH-5, Wave 4), `UnboundedEigCountRateBound.lean` (RH-6A, Wave 5),
  `UnboundedEigCountEigCountBridge.lean` (RH-6B, Wave 5), and `TpUnboundedNormProbe.lean`
  (RH-6C, Wave 5)), is formally SELF-ADJOINT IN THE FORMAL sense, i.e. SYMMETRIC:
  `Tp.IsFormalAdjoint Tp` (Onda-6 plan code `RH-7b`, work item `WAVE6-RH-7B`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-6
  task instructions on build contention with 13 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1..Wave-5 file, nor any
  other Wave-6 item's file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`, `e`,
  `e_apply` exactly as-is — the identical read-only import already used by `TpUnboundedNormProbe.lean`.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING A PRIOR-WAVE FILE DIRECTLY (the same
  situation, and the same resolution, as every RH-3..RH-6C sibling in this directory, most
  recently `TpUnboundedNormProbe.lean`, whose own header explains this in full). The Wave-2
  shared-infra source `LinearPMapEigenvalueBridge.lean`
  (`03_MILLENNIUM/_SHARED_INFRA/FORMAL/LinearPMapEigenvalueBridge.lean`) lives OUTSIDE the
  `05_FORMAL/lean` Lake project root, is itself declared free-standing/unregistered, and has no
  compiled `.olean` in `.lake/build/lib/lean`. There is consequently no module import path that
  resolves to it, and this file follows the established sibling convention instead: it reproduces,
  BYTE-IDENTICAL, only the MINIMAL block actually needed for THIS test —
  `finiteSupport`, `memℓp_of_finiteSupport`, `TpFun`, `Tp`, `Tp_apply` — copied verbatim from
  `TpUnboundedNormProbe.lean` lines 104–165 (itself a verbatim copy of
  `LinearPMapEigenvalueBridge.lean` §0–§1), under a fresh namespace (`RH7B.TpFormalAdjointProbe`)
  so no name clashes with the original file, `TpUnboundedNormProbe.lean`, nor any other Wave-3/4/5/6
  sibling's own separate reproduction. This file's reproduction is DELIBERATELY SMALLER than
  `TpUnboundedNormProbe.lean`'s: it omits `e_mem_finiteSupport`, `eDom`, `eDom_coe`, `Tp_eDom`
  (the eigenvector-witness machinery `TpUnboundedNormProbe.lean` needed for its norm-unboundedness
  argument), since the falsifiable target below is a purely algebraic termwise-inner-product
  identity that never mentions eigenvectors or norms — it needs only the domain and the map itself.
  The reproduced block is NOT reproved or reinterpreted — every line is copied as-is.

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-6 RH-7b task statement, nothing broader):

  > Reproduzir o bloco minimo finiteSupport/TpFun/Tp/Tp_apply, entao provar
  > `Tp_isFormalAdjoint : Tp.IsFormalAdjoint Tp` via `lp.hasSum_inner` em ambos os lados + `funext`
  > + `Complex.conj_natCast` + `ring`, fechado por `HasSum.unique`. NAO tentar
  > `IsSelfAdjoint`/`T.adjoint=T` neste item.

  WHY THIS TEST IS A GENUINE (NOT COSMETIC) GAP TO CLOSE. `DiagonalSelfAdjointOperatorProbe.lean`
  (Wave-1, RH-3 in that file's own internal numbering) already proves both `T_isFormalAdjoint` and
  the FULL `T_isSelfAdjoint` — but for a DIFFERENT operator: `T` there lives on
  `H := lp (fun _:ℕ => ℝ) 2` (real scalars, not the complex `H2` used by every RH-3..RH-6C file in
  THIS directory) with the MAXIMAL domain `Dom = {x ∈ ℓ² | (n ↦ n·x_n) ∈ ℓ²}`, not the
  finite-support submodule `finiteSupport` that `Tp` (the operator actually used throughout
  RH-3..RH-6C) is restricted to. Neither `DiagonalSelfAdjointOperatorProbe.lean` nor any of the six
  RH-3..RH-6C files proves any adjointness fact whatsoever about `Tp` itself — this file supplies
  exactly that missing formal witness, restricted honestly (see below) to the SYMMETRIC half only.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §2 below — everything before
  §2 is the verbatim reproduction described above).
  * `Tp_isFormalAdjoint` — **THE FALSIFIABLE TARGET, CLOSED.**
    `Tp.IsFormalAdjoint Tp`, i.e. `∀ x y : Tp.domain, ⟪Tp x, (y:H2)⟫ = ⟪(x:H2), Tp y⟫`
    (`LinearPMap.IsFormalAdjoint`, `Mathlib/Analysis/InnerProductSpace/LinearPMap.lean:74-75`),
    proved exactly via the strategy specified: apply `lp.hasSum_inner`
    (`Mathlib/Analysis/InnerProductSpace/l2Space.lean:150`) to both sides, giving
    `HasSum (fun i => ⟪(Tp x:H2) i, (y:H2) i⟫) ⟪Tp x, (y:H2)⟫` and
    `HasSum (fun i => ⟪(x:H2) i, (Tp y:H2) i⟫) ⟪(x:H2), Tp y⟫`; show the two summand functions are
    equal by `funext` + unfolding `Tp_apply` on each side + the scalar inner-product formula
    `RCLike.inner_apply' (a b : ℂ) : ⟪a,b⟫ = conj a * b`
    (`Mathlib/Analysis/InnerProductSpace/Basic.lean:915`) + `map_mul` (distributing `conj` over the
    product `(i:ℂ) * x_i`) + `Complex.conj_natCast` (`Mathlib/Data/Complex/Basic.lean:481`,
    `conj (n:ℂ) = n` for `n:ℕ`, killing the spurious conjugate on the real diagonal weight `i`) +
    `ring` (closing the resulting commutative rearrangement); rewrite one `HasSum` term along that
    functional equality, then close by `HasSum.unique`
    (`Mathlib/Topology/Algebra/InfiniteSum/Defs.lean:327`, `to_additive`'d from `HasProd.unique`,
    itself `tendsto_nhds_unique` under `[T2Space α]` — `H2 = lp (fun _ => ℂ) 2` is Hausdorff,
    inherited automatically from its `NormedAddCommGroup` instance).

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, as instructed by the Onda-6 plan for
  this exact item). This file says nothing about, and does not approximate, a solution to the
  Riemann Hypothesis or any Clay Millennium Prize problem: `Tp` remains a hand-built, purely
  algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)`, and this file establishes only SYMMETRY
  (`IsFormalAdjoint`), the "easy half" of self-adjointness. It explicitly does NOT attempt
  `IsSelfAdjoint Tp` or `Tp.adjoint = Tp` — that is a strictly harder, SEPARATE claim, NOT
  attempted here. The reason it is harder: `finiteSupport` is a proper, non-maximal dense subspace
  of `H2` (unlike `Dom` in `DiagonalSelfAdjointOperatorProbe.lean`, which is already the MAXIMAL
  domain on which the diagonal action stays in `ℓ²`), so `Tp.adjoint.domain` is provably strictly
  larger than `Tp.domain = finiteSupport` (the adjoint's domain is exactly the maximal domain,
  `{x ∈ ℓ² | (n ↦ n·x_n) ∈ ℓ²}`, which properly contains `finiteSupport` — e.g. `x_n = 1/(n+1)^2`
  lies in the former but is not finitely supported) — so `Tp ≤ Tp.adjoint` strictly, and
  `IsSelfAdjoint Tp` (which needs the reverse inclusion too) is simply FALSE for `Tp` as defined,
  not merely unproved. Establishing self-adjointness for the toy operator used by RH-3..RH-6C would
  require first enlarging its domain to the maximal one (as
  `DiagonalSelfAdjointOperatorProbe.lean` already does for the real-scalar case), a materially
  different and larger undertaking than this file's scope. No mathematical novelty is claimed: that
  a diagonal map is formally symmetric under the standard `ℓ²` inner product is a completely
  elementary, classical fact about diagonal operators.

  Every Mathlib name used below was checked by direct read/grep against the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in addition to compiling cleanly
  via `lake env lean` (see the file's own build log for the exact command/exit code, reported
  alongside this file).
-/
import Mathlib
import TamesisLab.Foundations.SpectralCountingInstance

open scoped ENNReal lp InnerProductSpace ComplexConjugate LinearPMap
open Filter Topology
open TamesisLab.Foundations.SpectralCounting.InfDim

namespace RH7B.TpFormalAdjointProbe

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`.

(Verbatim reproduction of `TpUnboundedNormProbe.lean` §0, lines 104–116, itself a verbatim copy of
`LinearPMapEigenvalueBridge.lean` §0 — see file header for why this file reproduces rather than
imports.) -/

/-- The submodule of `H2` consisting of finitely-supported sequences. -/
noncomputable def finiteSupport : Submodule ℂ H2 where
  carrier := {f : H2 | ∃ N : ℕ, ∀ i, N ≤ i → (f : ∀ _ : ℕ, ℂ) i = 0}
  zero_mem' := ⟨0, fun i _ => by simp⟩
  add_mem' := by
    rintro f g ⟨Nf, hf⟩ ⟨Ng, hg⟩
    refine ⟨max Nf Ng, fun i hi => ?_⟩
    rw [lp.coeFn_add, Pi.add_apply, hf i (le_trans (le_max_left _ _) hi),
      hg i (le_trans (le_max_right _ _) hi), add_zero]
  smul_mem' := by
    rintro c f ⟨N, hf⟩
    refine ⟨N, fun i hi => ?_⟩
    rw [lp.coeFn_smul, Pi.smul_apply, hf i hi, smul_zero]

/-- A finitely-supported sequence, multiplied pointwise by ANY coefficient sequence (in
particular the UNBOUNDED sequence `c i = i` used by `Tp` below), is still in `ℓ²` — its own
support stays finite. -/
lemma memℓp_of_finiteSupport (c : ℕ → ℂ) (f : H2) (N : ℕ)
    (hf : ∀ i, N ≤ i → (f : ∀ _ : ℕ, ℂ) i = 0) :
    Memℓp (fun i => c i * (f : ∀ _ : ℕ, ℂ) i) 2 := by
  have hfin : Set.Finite {i : ℕ | (fun i => c i * (f : ∀ _ : ℕ, ℂ) i) i ≠ 0} := by
    apply Set.Finite.subset (Set.finite_Iio N)
    intro i hi
    simp only [Set.mem_setOf_eq] at hi
    by_contra hc
    exact hi (by rw [hf i (not_lt.mp hc), mul_zero])
  exact (memℓp_zero hfin).of_exponent_ge (by norm_num : (0 : ℝ≥0∞) ≤ 2)

/-! ### §1 — the unbounded toy diagonal operator `Tp`, as a `LinearPMap`.

`Tp` is defined only on `finiteSupport`, and acts as `(Tp x)_i = i * x_i` — the SAME `Tp` used
throughout RH-3..RH-6C.

(Verbatim reproduction of `TpUnboundedNormProbe.lean` §1, lines 144–165, itself a verbatim copy of
`LinearPMapEigenvalueBridge.lean` §1.) -/

/-- The underlying (everywhere-defined-on-its-domain) linear map of `Tp`. -/
noncomputable def TpFun : finiteSupport →ₗ[ℂ] H2 where
  toFun x := ⟨fun i => (i : ℂ) * (x : H2) i, by
    obtain ⟨N, hN⟩ := x.2
    exact memℓp_of_finiteSupport (fun i => (i : ℂ)) (x : H2) N hN⟩
  map_add' x y := by
    ext i
    show (i : ℂ) * ((x : H2) + (y : H2)) i = (i : ℂ) * (x : H2) i + (i : ℂ) * (y : H2) i
    rw [lp.coeFn_add, Pi.add_apply, mul_add]
  map_smul' c x := by
    ext i
    show (i : ℂ) * (c • (x : H2)) i = c • ((i : ℂ) * (x : H2) i)
    rw [lp.coeFn_smul, Pi.smul_apply, smul_eq_mul, smul_eq_mul]
    ring

/-- **The toy unbounded diagonal `LinearPMap`.** Domain = finitely-supported vectors of `H2`;
`Tp x_n = n * x_n`. -/
noncomputable def Tp : H2 →ₗ.[ℂ] H2 := ⟨finiteSupport, TpFun⟩

@[simp] lemma Tp_apply (x : Tp.domain) (i : ℕ) :
    ((Tp x : H2) : ∀ _ : ℕ, ℂ) i = (i : ℂ) * (x : H2) i := rfl

/-! ### §2 — NEW (WAVE6-RH-7B): `Tp` is formally symmetric, i.e. `Tp.IsFormalAdjoint Tp`.

This section is NOT a reproduction of anything: it is this file's own new content, the falsifiable
target for WAVE6-RH-7B. Explicitly NOT attempted: `IsSelfAdjoint Tp` / `Tp.adjoint = Tp` — see the
file header for why that is a separate, harder, unattempted claim. -/

/-- **THE FALSIFIABLE TARGET, CLOSED.** `Tp` is a formal adjoint of itself, i.e. symmetric under
the `H2` inner product: `∀ x y : Tp.domain, ⟪Tp x, (y:H2)⟫ = ⟪(x:H2), Tp y⟫`
(`LinearPMap.IsFormalAdjoint`). Proved exactly via the strategy specified: `lp.hasSum_inner` on
both sides, termwise equality of the summand functions via `funext` + `Tp_apply` +
`RCLike.inner_apply'` + `map_mul` + `Complex.conj_natCast` + `ring`, closed by `HasSum.unique`. -/
theorem Tp_isFormalAdjoint : Tp.IsFormalAdjoint Tp := by
  intro x y
  show inner (𝕜 := ℂ) (Tp x : H2) (y : H2) = inner (𝕜 := ℂ) (x : H2) (Tp y : H2)
  have hL : HasSum (fun i => inner (𝕜 := ℂ) ((Tp x : H2) i) ((y : H2) i))
      (inner (𝕜 := ℂ) (Tp x : H2) (y : H2)) := lp.hasSum_inner (Tp x : H2) (y : H2)
  have hR : HasSum (fun i => inner (𝕜 := ℂ) ((x : H2) i) ((Tp y : H2) i))
      (inner (𝕜 := ℂ) (x : H2) (Tp y : H2)) := lp.hasSum_inner (x : H2) (Tp y : H2)
  have hfun : (fun i => inner (𝕜 := ℂ) ((Tp x : H2) i) ((y : H2) i))
      = (fun i => inner (𝕜 := ℂ) ((x : H2) i) ((Tp y : H2) i)) := by
    funext i
    simp only [Tp_apply]
    rw [RCLike.inner_apply', RCLike.inner_apply', map_mul, Complex.conj_natCast]
    ring
  rw [hfun] at hL
  exact hL.unique hR

end RH7B.TpFormalAdjointProbe

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH7B.TpFormalAdjointProbe.Tp_isFormalAdjoint
