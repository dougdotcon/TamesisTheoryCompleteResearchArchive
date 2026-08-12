/-
  WAVE7-RH-7D — the quadratic form `⟪Tp x, x⟫` of the toy unbounded diagonal `LinearPMap` `Tp`
  (the SAME `Tp` used throughout `UnboundedEigCountFloorLaw.lean` (RH-3, Wave 3),
  `UnboundedEigCountWeylLimitLaw.lean` (RH-4, Wave 4), `EigenvalueSetBridgeRestricted.lean`
  (RH-5, Wave 4), `UnboundedEigCountRateBound.lean` (RH-6A, Wave 5),
  `UnboundedEigCountEigCountBridge.lean` (RH-6B, Wave 5), `TpUnboundedNormProbe.lean` (RH-6C,
  Wave 5), and `TpFormalAdjointProbe.lean` (RH-7B, Wave 6)) is REAL and NONNEGATIVE for every
  `x` in `Tp.domain` (Onda-7 plan code `RH-7d`, work item `WAVE7-RH-7D`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-7
  task instructions on build contention with 13 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1..Wave-6 file, nor any
  other Wave-7 item's file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`,
  `e`, `e_apply` exactly as-is — the identical read-only import already used by
  `TpUnboundedNormProbe.lean` and `TpFormalAdjointProbe.lean`.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING A PRIOR-WAVE FILE DIRECTLY (the same
  situation, and the same resolution, as every RH-3..RH-7B sibling in this directory, most
  recently `TpFormalAdjointProbe.lean`, whose own header explains this in full). This file
  reproduces, BYTE-IDENTICAL, only the MINIMAL block actually needed for THIS test —
  `finiteSupport`, `memℓp_of_finiteSupport`, `TpFun`, `Tp`, `Tp_apply` — copied verbatim from
  `TpFormalAdjointProbe.lean` lines 119–175 (itself a verbatim copy of
  `TpUnboundedNormProbe.lean` §0–§1, itself a verbatim copy of
  `LinearPMapEigenvalueBridge.lean` §0–§1), under a fresh namespace (`RH7D.TpInnerSelfNonnegProbe`)
  so no name clashes with any prior-wave file's own separate reproduction. The reproduced block is
  NOT reproved or reinterpreted — every line is copied as-is.

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-7 RH-7d task statement, nothing broader):

  > Reproduzir o bloco minimo finiteSupport/TpFun/Tp; provar
  > `Tp_inner_self_real_nonneg : ∀ x ∈ Tp.domain, (inner (Tp x) x : ℂ).im = 0 ∧
  > 0 ≤ (inner (Tp x) x : ℂ).re`, via `RCLike.inner_apply'` + `lp.hasSum_inner` + `funext` +
  > `Complex.conj_natCast` reduzindo a `Sum i*normSq(x_i)`, fechado por
  > `Complex.normSq_nonneg`.

  WHY THIS TEST IS A GENUINE (NOT COSMETIC) GAP TO CLOSE. `TpFormalAdjointProbe.lean` (Wave-6,
  RH-7B) already proves `Tp.IsFormalAdjoint Tp`, i.e. `⟪Tp x, y⟫ = ⟪x, Tp y⟫` for all
  `x y : Tp.domain` — but that is the "off-diagonal" symmetry statement. It says nothing about the
  DIAGONAL quadratic form `⟪Tp x, x⟫` being real-valued or of a definite sign; a symmetric formal
  adjoint alone does not by itself hand you either fact syntactically. This file supplies exactly
  that missing witness: `⟪Tp x, x⟫` is real (zero imaginary part) and nonnegative, for every
  `x ∈ Tp.domain`.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §2 below — everything before
  §2 is the verbatim reproduction described above).
  * `Tp_inner_self_real_nonneg` — **THE FALSIFIABLE TARGET, CLOSED.**
    `∀ x : Tp.domain, (⟪Tp x, (x:H2)⟫ : ℂ).im = 0 ∧ 0 ≤ (⟪Tp x, (x:H2)⟫ : ℂ).re`, proved exactly
    via the strategy specified: apply `lp.hasSum_inner` (`Mathlib/Analysis/InnerProductSpace/
    l2Space.lean:150`) to get `HasSum (fun i => ⟪(Tp x:H2) i, (x:H2) i⟫) ⟪Tp x, (x:H2)⟫`; rewrite
    the summand function, termwise, via `funext` + unfolding `Tp_apply` + the scalar inner-product
    formula `RCLike.inner_apply' (a b : ℂ) : ⟪a,b⟫ = conj a * b`
    (`Mathlib/Analysis/InnerProductSpace/Basic.lean:915`) + `map_mul` (distributing `conj` over the
    product `(i:ℂ) * x_i`) + `Complex.conj_natCast` (`Mathlib/Data/Complex/Basic.lean`, `conj
    (n:ℂ) = n` for `n:ℕ`, killing the spurious conjugate on the real diagonal weight `i`) +
    `Complex.normSq_eq_conj_mul_self` (`(normSq z : ℂ) = conj z * z`) to rewrite each summand as
    the real-cast complex number `((i:ℝ) * Complex.normSq (x_i) : ℝ)`; then split into real and
    imaginary parts via `Complex.hasSum_im`/`Complex.hasSum_re`
    (`Mathlib/Analysis/Complex/Basic.lean:608`/`605`) applied to the rewritten `HasSum`. The
    imaginary-part `HasSum` becomes `HasSum (fun _ => 0) ⟪Tp x,x⟫.im`, closed by
    `HasSum.unique` against `hasSum_zero`. The real-part `HasSum` becomes
    `HasSum (fun i => (i:ℝ) * Complex.normSq (x_i)) ⟪Tp x,x⟫.re`, whose limit is nonnegative
    because every summand is (`Nat.cast_nonneg` times `Complex.normSq_nonneg`), closed by
    `HasSum.nonneg`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, as instructed by the Onda-7 plan
  for this exact item). This file says nothing about, and does not approximate, a solution to the
  Riemann Hypothesis or any Clay Millennium Prize problem: `Tp` remains a hand-built, purely
  algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)`, and this file establishes only that its diagonal
  quadratic form is real and nonnegative on its own (non-maximal, finitely-supported) domain — an
  entirely expected, elementary fact about a diagonal operator with nonnegative-integer weights
  (`⟪Tp x, x⟫ = Σ i·|x_i|²` termwise), not a spectral-gap or self-adjointness result. It does NOT
  establish `IsSelfAdjoint Tp` (see `TpFormalAdjointProbe.lean`'s header for why that is a
  separate, strictly harder, unattempted claim: `Tp.domain = finiteSupport` is a proper
  non-maximal dense subspace of `H2`). No mathematical novelty is claimed: that a diagonal operator
  with nonnegative real weights has a nonnegative real quadratic form is a completely elementary,
  classical fact about diagonal operators.

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

namespace RH7D.TpInnerSelfNonnegProbe

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`.

(Verbatim reproduction of `TpFormalAdjointProbe.lean` §0, lines 119–131, itself a verbatim copy of
`TpUnboundedNormProbe.lean` §0, itself a verbatim copy of `LinearPMapEigenvalueBridge.lean` §0 —
see file header for why this file reproduces rather than imports.) -/

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
throughout RH-3..RH-7B.

(Verbatim reproduction of `TpFormalAdjointProbe.lean` §1, lines 155–175.) -/

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

/-! ### §2 — NEW (WAVE7-RH-7D): `⟪Tp x, x⟫` is real and nonnegative for every `x ∈ Tp.domain`.

This section is NOT a reproduction of anything: it is this file's own new content, the falsifiable
target for WAVE7-RH-7D. -/

/-- **THE FALSIFIABLE TARGET, CLOSED.** The diagonal quadratic form `⟪Tp x, x⟫` of `Tp` is real
(zero imaginary part) and nonnegative, for every `x : Tp.domain`. Proved exactly via the strategy
specified: `lp.hasSum_inner`, termwise rewriting of the summand via `Tp_apply` +
`RCLike.inner_apply'` + `map_mul` + `Complex.conj_natCast` + `Complex.normSq_eq_conj_mul_self` to
`(i:ℝ) * normSq(x_i)` cast to `ℂ`, then `Complex.hasSum_im`/`Complex.hasSum_re` closed by
`HasSum.unique hasSum_zero` (imaginary part) and `HasSum.nonneg` using `Complex.normSq_nonneg`
(real part). -/
theorem Tp_inner_self_real_nonneg (x : Tp.domain) :
    (inner (𝕜 := ℂ) (Tp x : H2) (x : H2)).im = 0 ∧
      0 ≤ (inner (𝕜 := ℂ) (Tp x : H2) (x : H2)).re := by
  have hL : HasSum (fun i => inner (𝕜 := ℂ) ((Tp x : H2) i) ((x : H2) i))
      (inner (𝕜 := ℂ) (Tp x : H2) (x : H2)) := lp.hasSum_inner (Tp x : H2) (x : H2)
  have hfun : (fun i => inner (𝕜 := ℂ) ((Tp x : H2) i) ((x : H2) i))
      = (fun i : ℕ => (((i : ℝ) * Complex.normSq ((x : H2) i) : ℝ) : ℂ)) := by
    funext i
    simp only [Tp_apply]
    rw [RCLike.inner_apply', map_mul, Complex.conj_natCast, mul_assoc,
      ← Complex.normSq_eq_conj_mul_self]
    push_cast
    ring
  rw [hfun] at hL
  have him := Complex.hasSum_im hL
  have hre := Complex.hasSum_re hL
  simp only [Complex.ofReal_im] at him
  simp only [Complex.ofReal_re] at hre
  exact ⟨him.unique hasSum_zero,
    hre.nonneg (fun i => mul_nonneg (Nat.cast_nonneg i) (Complex.normSq_nonneg _))⟩

end RH7D.TpInnerSelfNonnegProbe

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH7D.TpInnerSelfNonnegProbe.Tp_inner_self_real_nonneg
