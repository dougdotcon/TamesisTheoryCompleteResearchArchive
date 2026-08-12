/-
  WAVE7-RH-7C — `Tp`, the toy unbounded diagonal `LinearPMap` on its finite-support domain
  (the SAME `Tp` used throughout `UnboundedEigCountFloorLaw.lean` (RH-3, Wave 3),
  `UnboundedEigCountWeylLimitLaw.lean` (RH-4, Wave 4), `EigenvalueSetBridgeRestricted.lean`
  (RH-5, Wave 4), `UnboundedEigCountRateBound.lean` (RH-6A, Wave 5),
  `UnboundedEigCountEigCountBridge.lean` (RH-6B, Wave 5), `TpUnboundedNormProbe.lean`
  (RH-6C, Wave 5), and `TpFormalAdjointProbe.lean` (RH-7B, Wave 6)), satisfies
  `Tp ≤ Tp.adjoint` (Onda-7 plan code `RH-7c`, work item `WAVE7-RH-7C`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-7
  task instructions on build contention with 13 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1..Wave-6 file, nor any
  other Wave-7 item's file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`
  exactly as-is — the identical read-only import already used by `TpFormalAdjointProbe.lean`.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING A PRIOR-WAVE FILE DIRECTLY (the same
  situation, and the same resolution, as every RH-3..RH-7B sibling in this directory, most
  recently `TpFormalAdjointProbe.lean`, whose own header explains this in full — see that file for
  the complete rationale re: `LinearPMapEigenvalueBridge.lean` living outside the Lake project
  root). This file reproduces, BYTE-IDENTICAL, the block `finiteSupport`, `memℓp_of_finiteSupport`,
  `TpFun`, `Tp`, `Tp_apply` from `TpFormalAdjointProbe.lean` lines 119–175, PLUS the theorem
  `Tp_isFormalAdjoint` from that same file's lines 188–202 (RH-7B, Onda 6 — the formal-symmetry
  witness this item's falsifiable target is built on), all copied as-is under a fresh namespace
  (`RH7C.TpLeAdjointProbe`) so no name clashes with any prior-wave reproduction. NONE of this
  reproduced block is reproved or reinterpreted; every line is copied verbatim. It is EXCLUDED
  from this item's 50-line new-content budget, exactly as the Wave-7 task instructions permit
  ("reproduced/inlined boilerplate from prior-wave files is EXCLUDED from this count"). Only §2
  below (`single_mem_finiteSupport`, `finiteSupport_dense`, `Tp_le_adjoint`) is this item's own new
  content.

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-7 RH-7c task statement, nothing broader):

  > Reproduzir o bloco minimo finiteSupport/TpFun/Tp; provar densidade de finiteSupport em H2 (via
  > lp.single, trivial); fechar `Tp ≤ Tp.adjoint` via `LinearPMap.IsFormalAdjoint.le_adjoint`
  > aplicado a `Tp_isFormalAdjoint` (RH-7B, Onda 6) mais a densidade. NAO tentar `IsSelfAdjoint`
  > neste item.

  WHY THIS TEST IS A GENUINE (NOT COSMETIC) GAP TO CLOSE. `TpFormalAdjointProbe.lean` (Wave-6,
  RH-7B) proves only the purely algebraic termwise identity `Tp.IsFormalAdjoint Tp`; it explicitly
  does NOT touch `Tp.adjoint` (the actual `LinearPMap` built from the Riesz-representation /
  continuous-extension machinery in `Mathlib.Analysis.InnerProductSpace.LinearPMap`) nor the
  order relation `≤` on `LinearPMap`s at all. `LinearPMap.IsFormalAdjoint.le_adjoint` is the
  Mathlib bridge from a purely algebraic symmetry witness to the genuine operator-theoretic
  statement `Tp ≤ Tp.adjoint`, but it has a real, non-trivial extra hypothesis beyond
  `Tp_isFormalAdjoint`: `Dense (Tp.domain : Set H2)`, i.e. density of the finite-support submodule
  in `H2` for the ambient `ℓ²` topology. This density fact is proved nowhere in the prior six
  RH-3..RH-7B files, so this item supplies exactly that missing piece and then invokes the bridge
  lemma; the resulting `Tp ≤ Tp.adjoint` is a strictly stronger operator-theoretic fact than
  `Tp_isFormalAdjoint` alone (it says `Tp.adjoint` genuinely *extends* `Tp`, domain and action both,
  not just that the two sides of the inner-product identity match on `Tp.domain × Tp.domain`).

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §2 below).
  * `single_mem_finiteSupport` — every `lp.single 2 i a` lies in `finiteSupport`: its support is
    contained in `{i}` (`lp.single_apply_ne`, `Mathlib/Analysis/Normed/Lp/lpSpace.lean:1030`), so
    `N := i + 1` witnesses membership.
  * `finiteSupport_dense` — **THE FIRST HALF OF THE FALSIFIABLE TARGET, CLOSED.**
    `Dense (finiteSupport : Set H2)`. Proved via `lp.hasSum_single`
    (`Mathlib/Analysis/Normed/Lp/lpSpace.lean:1171`: for `p ≠ ⊤`, every `f : lp E p` is the
    unconditional limit, over the `atTop` filter of finite subsets, of its own canonical
    finitely-supported partial sums `∑ i ∈ s, lp.single p i (f i)`) together with the general
    topological fact `mem_closure_of_tendsto`
    (`Mathlib/Topology/Neighborhoods.lean:357`: a net valued in `s` that tends to `x` has
    `x ∈ closure s`) applied with `s := finiteSupport`, using `Submodule.sum_mem`
    (`Mathlib/Algebra/Module/Submodule/Basic.lean:73`) plus `single_mem_finiteSupport` to see that
    EVERY finite partial sum already lies in `finiteSupport` (not merely eventually).
  * `Tp_le_adjoint` — **THE SECOND HALF OF THE FALSIFIABLE TARGET, CLOSED.** `Tp ≤ Tp.adjoint`.
    Proved exactly via the strategy specified: `Tp_isFormalAdjoint.le_adjoint finiteSupport_dense`,
    i.e. one direct application of `LinearPMap.IsFormalAdjoint.le_adjoint`
    (`Mathlib/Analysis/InnerProductSpace/LinearPMap.lean:195`) to the RH-7B witness
    `Tp_isFormalAdjoint : Tp.IsFormalAdjoint Tp` and the density fact just proved.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, as instructed by the Onda-7 plan for
  this exact item). This file says nothing about, and does not approximate, a solution to the
  Riemann Hypothesis or any Clay Millennium Prize problem: `Tp` remains a hand-built, purely
  algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)`. `Tp ≤ Tp.adjoint` is the "easy," always-true-for-
  densely-defined-symmetric-operators half of self-adjointness; it does NOT establish
  `IsSelfAdjoint Tp` or `Tp.adjoint = Tp` (the reverse inclusion `Tp.adjoint ≤ Tp`), which is
  explicitly NOT attempted here, per the task's own falsifiable-test statement. As
  `TpFormalAdjointProbe.lean`'s header already records, that reverse inclusion is in fact FALSE
  for `Tp` as defined (`finiteSupport` is a proper dense subspace of the true maximal domain on
  which the diagonal action stays in `ℓ²`), so `IsSelfAdjoint Tp` is not a nearby, harder version
  of this fact — it is a different and false claim for this particular toy operator. No
  mathematical novelty is claimed: that a densely-defined formally-symmetric operator is contained
  in its own adjoint is a completely standard, classical fact of unbounded operator theory, already
  packaged as `LinearPMap.IsFormalAdjoint.le_adjoint` in Mathlib.

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

namespace RH7C.TpLeAdjointProbe

/-! ### §0 — the domain: finitely-supported vectors of `H2`

(Verbatim reproduction of `TpFormalAdjointProbe.lean` §0, lines 119–131 — see file header for why
this file reproduces rather than imports. EXCLUDED from this item's new-content line count.) -/

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

/-- A finitely-supported sequence, multiplied pointwise by ANY coefficient sequence, is still in
`ℓ²` — its own support stays finite. -/
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

/-! ### §1 — the unbounded toy diagonal operator `Tp`, and RH-7B's `Tp_isFormalAdjoint`.

(Verbatim reproduction of `TpFormalAdjointProbe.lean` §1–§2, lines 155–202. EXCLUDED from this
item's new-content line count.) -/

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

/-- `Tp` is a formal adjoint of itself (RH-7B, Wave 6). -/
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

/-! ### §2 — NEW (WAVE7-RH-7C): density of `finiteSupport` in `H2`, and `Tp ≤ Tp.adjoint`.

This section is NOT a reproduction of anything: it is this file's own new content, the falsifiable
target for WAVE7-RH-7C. Explicitly NOT attempted: `IsSelfAdjoint Tp` — see the file header. -/

/-- Every `lp.single` vector lies in `finiteSupport`: its support is contained in `{i}`. -/
lemma single_mem_finiteSupport (i : ℕ) (a : ℂ) :
    lp.single (E := fun _ : ℕ => ℂ) 2 i a ∈ finiteSupport := by
  refine ⟨i + 1, fun j hj => ?_⟩
  have hij : j ≠ i := by omega
  exact lp.single_apply_ne (E := fun _ : ℕ => ℂ) 2 i a hij

/-- **THE FALSIFIABLE TARGET, PART 1, CLOSED.** `finiteSupport` is dense in `H2`: every vector is
the unconditional limit of its own canonical finitely-supported partial sums. -/
lemma finiteSupport_dense : Dense (finiteSupport : Set H2) := fun f =>
  mem_closure_of_tendsto (lp.hasSum_single (by norm_num) f)
    (Eventually.of_forall fun s =>
      Submodule.sum_mem _ fun i _ => single_mem_finiteSupport i (f i))

/-- **THE FALSIFIABLE TARGET, PART 2, CLOSED.** `Tp ≤ Tp.adjoint`, via
`LinearPMap.IsFormalAdjoint.le_adjoint` applied to `Tp_isFormalAdjoint` (RH-7B) and the density of
`Tp.domain = finiteSupport` in `H2` just established. -/
theorem Tp_le_adjoint : Tp ≤ Tp.adjoint :=
  Tp_isFormalAdjoint.le_adjoint finiteSupport_dense

end RH7C.TpLeAdjointProbe

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH7C.TpLeAdjointProbe.single_mem_finiteSupport
#print axioms RH7C.TpLeAdjointProbe.finiteSupport_dense
#print axioms RH7C.TpLeAdjointProbe.Tp_le_adjoint
