/-
  SHARED-2C — Spectral bridge probe: `LinearPMap` eigenvalue vs
  `Module.End.HasEigenvalue`, on a toy diagonal operator (Wave-2 batch,
  shared-infrastructure item, relevant to RH-4 and generically to any line
  that needs to talk about unbounded operators via `LinearPMap`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring
  session (single-file typecheck against the existing built Mathlib cache,
  NOT a full `lake build` — see the Wave-2 task instructions on build
  contention with 19 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any
  Wave-1 or other Wave-2 file. It only *imports* (read-only) the
  registered Wave-1/foundations module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`),
  reusing its `H2`, `dseq`, `e`, `T`, `hasEigenvalue_T`,
  `eigenvalue_mem_range`, `exists_ne_zero_coord` rather than redeclaring
  them. (Unlike the Wave-2 sibling `HermitianComplexEmbeddingRange.lean`,
  which had to reproduce a matrix verbatim because its Wave-1 source lives
  outside the `TamesisLab` module graph, `SpectralCountingInstance.lean`
  IS part of the registered `lean_lib "TamesisLab"` graph — confirmed
  directly this session: it is `import`ed by `TamesisLab/Foundations.lean`
  and has a built `.olean` — so ordinary `import
  TamesisLab.Foundations.SpectralCountingInstance` resolves cleanly via
  `lake env lean` from this file's own directory, with no build-system
  workaround needed.)

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-2 task statement,
  nothing broader). Two parts:

  (1) Characterize `mu : ℂ` as an eigenvalue of a `LinearPMap`
      `T : H2 →ₗ.[ℂ] H2` directly via
      `∃ v ∈ T.domain, v ≠ 0 ∧ T v = mu • v`
      (below: `IsEigenvalue`), matching the task's literal phrasing
      "exists v in T.domain, v != 0, T v = mu * v".

  (2) Build a genuinely UNBOUNDED toy `LinearPMap` `Tp`, diagonal on the
      dense domain of finitely-supported sequences of the SAME space
      `H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2` (`ℓ²(ℕ,ℂ)`)
      already used by the registered bounded operator, with
      `Tp x_n = n * x_n` (`n` UNBOUNDED as `n → ∞`, in contrast to the
      registered bounded diagonal operator
      `R := TamesisLab.Foundations.SpectralCounting.InfDim.T`, whose
      diagonal `dseq n = 1/(n+1)` IS bounded by `1`). Then connect
      `IsEigenvalue Tp mu` BY HAND to `Module.End.HasEigenvalue` of `R`,
      via the explicit inverse-shift relationship the task specifies:
      `R` is the diagonal operator `1/(n+1)`, i.e. (on the shared
      eigenvector `e n`) `R` acts as the inverse of `Tp + 1`. The main
      theorem `eigenvalue_bridge` makes this precise and UNCONDITIONAL:
      `IsEigenvalue Tp mu ↔ Module.End.HasEigenvalue (R : Module.End ℂ H2)
      (mu + 1)⁻¹`, for every `mu : ℂ` (no side condition on `mu` needed —
      see the theorem's own docstring for why the `ℂ`-inverse junk value
      at `mu = -1` does not break the `↔`).

  WHAT WAS ACTUALLY BUILT, PRECISELY.
  * `finiteSupport : Submodule ℂ H2` — the finitely-supported vectors of
    `H2`, i.e. `{f | ∃ N, ∀ i ≥ N, f i = 0}`. `smul_/add_/zero_mem'`
    proved directly.
  * `memℓp_of_finiteSupport` — a finitely-supported sequence, multiplied
    pointwise by ANY coefficient sequence (in particular the unbounded
    `c i = i`), is still in `ℓ²`, because its own support stays finite.
    Proved via `memℓp_zero` (`Memℓp f 0 ↔ Set.Finite {i | f i ≠ 0}`,
    `Mathlib/Analysis/Normed/Lp/lpSpace.lean`) followed by
    `Memℓp.of_exponent_ge` (`Memℓp f q → q ≤ p → Memℓp f p`, same file) at
    `q := 0 ≤ p := 2` — this is exactly what makes the UNBOUNDED diagonal
    `n * x_n` well-defined as a genuine (everywhere-defined-on-its-own
    domain) linear map into `H2`, without needing any boundedness
    argument (contrast with the registered `R`, whose own construction in
    `SpectralCountingInstance.lean` needs `mulLin`/`mkContinuous` with an
    explicit bound `C`, precisely BECAUSE its domain is all of `H2`, not
    just the finite-support subspace).
  * `Tp : H2 →ₗ.[ℂ] H2 := ⟨finiteSupport, TpFun⟩` — the toy unbounded
    `LinearPMap`, `(Tp x)_i = i * x_i`.
  * `IsEigenvalue (T : H2 →ₗ.[ℂ] H2) (mu : ℂ) : Prop := ∃ v : T.domain,
    (v : H2) ≠ 0 ∧ T v = mu • (v : H2)` — part (1) of the test, the
    `LinearPMap`-level eigenvalue predicate, phrased exactly as specified.
  * `Tp_isEigenvalue (n : ℕ) : IsEigenvalue Tp (n : ℂ)` — every natural
    number is an eigenvalue of `Tp`, eigenvector `e n` (the standard basis
    vector already defined in `SpectralCountingInstance.lean`, reused
    as-is; it is finitely supported, hence lies in `Tp.domain`).
  * `Tp_eigenvalue_mem_range {mu} (h : IsEigenvalue Tp mu) : ∃ n : ℕ, mu =
    n` — the converse: `Tp`'s eigenvalue set is EXACTLY `ℕ`, proved by
    the same "look at a nonzero coordinate" argument as the registered
    `InfDim.eigenvalue_mem_range` for the bounded operator `R` (that
    lemma is reused, not reproduced, for `R`'s own side of the bridge
    below; `Tp`'s analogous fact has to be proved fresh here since `Tp`
    itself is new).
  * `eigenvalue_bridge (mu : ℂ) : IsEigenvalue Tp mu ↔
    Module.End.HasEigenvalue (T : Module.End ℂ H2) (mu + 1)⁻¹` — part (2)
    of the test, THE ACTUAL HAND-BUILT CONNECTION. (Here `T` inside the
    statement is `TamesisLab.Foundations.SpectralCounting.InfDim.T`,
    opened unqualified at the top of the file — i.e. exactly `R` from the
    task description; `Tp` is this file's own new toy operator, kept
    under a different name specifically to avoid clashing with the
    already-registered `T`.) Forward direction: from an eigenvector of
    `Tp` at `mu`, `Tp_eigenvalue_mem_range` forces `mu = (n : ℂ)` for some
    `n`; the cast identity `((n:ℂ)+1)⁻¹ = (dseq n : ℂ)` (`push_cast` +
    `one_div`) then transports the already-registered `hasEigenvalue_T n`
    (an `R`-fact) into the goal. Backward direction: from `R` having
    eigenvalue `(mu+1)⁻¹`, the already-registered `eigenvalue_mem_range`
    (an `R`-fact) gives `dseq i = (mu+1)⁻¹` for some `i`; the same cast
    identity plus `inv_inj` (`Mathlib/Algebra/Group/Basic.lean`,
    unconditional — no nonzero side hypothesis needed, since inversion is
    involutive even at the junk value `0⁻¹ = 0`) plus `add_right_cancel`
    solves `mu = (i : ℂ)` exactly, and `Tp_isEigenvalue i` closes the
    goal on the `Tp` side.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching
  Wave-2 instructions). `Tp` is a genuinely toy, hand-built unbounded
  operator on `ℓ²(ℕ,ℂ)`, used ONLY to instantiate the `IsEigenvalue`
  predicate against something not artificially bounded; no attempt is
  made here to relate `Tp`/`IsEigenvalue` to closedness, self-adjointness
  in the unbounded sense, deficiency indices, or any other piece of
  genuine unbounded-operator theory (`Tp` is not shown to be a *closed*
  operator, and no claim of self-adjointness for `Tp` is made or needed).
  `IsEigenvalue` itself is a bespoke ad hoc `Prop`, not a Mathlib
  primitive and not claimed to be — Mathlib has no ready-made
  "`LinearPMap` eigenvalue" API as of the vendored snapshot (searched
  directly: no `HasEigenvalue`/`eigenvalue` declarations anywhere under
  `Mathlib/LinearAlgebra/LinearPMap.lean` or
  `Mathlib/Analysis/InnerProductSpace/LinearPMap.lean`), so the falsifiable
  test's own phrasing (the raw existential) is exactly what gets
  formalized, with no upstream lemma reused for it. Nothing here computes
  a "spectrum" of `Tp` in the `spectrum`/`resolventSet` sense (no
  topology or continuity is placed on `Tp` at all — it is a bare algebraic
  `LinearPMap`). Nothing here is about Yang-Mills, Riemann Hypothesis, the
  RH-4 line, or any Millennium problem; it says nothing about, and does
  not approximate, a solution to any Clay problem. No mathematical
  novelty is claimed: relating the eigenvalues of a diagonal operator
  `n ↦ n` to those of its diagonal "resolvent-at-`-1`" `n ↦ 1/(n+1)` is a
  completely elementary, classical observation about diagonal operators.

  Every Mathlib name used below was checked by direct read/grep against
  the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in
  addition to compiling cleanly via `lake env lean` (see the file's own
  build log for the exact command/exit code, reported alongside this
  file).
-/
import Mathlib
import TamesisLab.Foundations.SpectralCountingInstance

open scoped ENNReal lp InnerProductSpace
open Filter Topology
open TamesisLab.Foundations.SpectralCounting.InfDim

namespace SHARED2C.LinearPMapEigenvalueBridge

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`. -/

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
support stays finite. This is exactly what lets the unbounded diagonal `n * x_n` land in `H2`
without any boundedness argument, unlike the registered bounded `R` (`InfDim.mulOp`/`mulLin`),
whose construction needs an explicit bound because its domain is all of `H2`. -/
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

/-! ### §1 — the unbounded toy diagonal operator `Tp`, as a `LinearPMap`

`Tp` is defined only on `finiteSupport`, and acts as `(Tp x)_i = i * x_i` — the toy unbounded
diagonal operator `T x_n = n * x_n` from the task statement, distinct from the already-registered
bounded diagonal operator `TamesisLab.Foundations.SpectralCounting.InfDim.T` (opened above simply
as `T`), which plays the role of `R` below. -/

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
`Tp x_n = n * x_n`, unbounded (no continuity claim is made, nor needed). -/
noncomputable def Tp : H2 →ₗ.[ℂ] H2 := ⟨finiteSupport, TpFun⟩

@[simp] lemma Tp_apply (x : Tp.domain) (i : ℕ) :
    ((Tp x : H2) : ∀ _ : ℕ, ℂ) i = (i : ℂ) * (x : H2) i := rfl

/-! ### §2 — the falsifiable target: eigenvalue characterization for a `LinearPMap`

`mu : ℂ` is characterized as an eigenvalue of a `LinearPMap T : H2 →ₗ.[ℂ] H2` exactly as stated
in the task: `∃ v ∈ T.domain, v ≠ 0, T v = mu * v` (phrased over the subtype `T.domain`). -/

/-- **The falsifiable eigenvalue predicate for a `LinearPMap`** (part (1) of the task). -/
def IsEigenvalue (T : H2 →ₗ.[ℂ] H2) (mu : ℂ) : Prop :=
  ∃ v : T.domain, (v : H2) ≠ 0 ∧ T v = mu • (v : H2)

/-! ### §3 — `Tp` has an eigenvector `e i` at every natural number `i`, matching `R`'s own
`e i` eigenvector for `dseq i` in `InfDim` (imported, read-only). -/

lemma e_mem_finiteSupport (i : ℕ) : e i ∈ finiteSupport := by
  refine ⟨i + 1, fun j hj => ?_⟩
  rw [e_apply]
  have : j ≠ i := by omega
  simp [this]

/-- `e i`, viewed as an element of `Tp.domain`. -/
noncomputable def eDom (i : ℕ) : Tp.domain := ⟨e i, e_mem_finiteSupport i⟩

@[simp] lemma eDom_coe (i : ℕ) : (eDom i : H2) = e i := rfl

lemma Tp_eDom (i : ℕ) : Tp (eDom i) = (i : ℂ) • e i := by
  ext j
  rw [Tp_apply, eDom_coe, lp.coeFn_smul]
  simp only [Pi.smul_apply, smul_eq_mul, e_apply]
  by_cases hij : j = i
  · subst hij; simp
  · simp [hij]

/-- **`Tp` has eigenvalue `n` for every natural `n`**, with eigenvector `e n`. -/
theorem Tp_isEigenvalue (n : ℕ) : IsEigenvalue Tp (n : ℂ) :=
  ⟨eDom n, by
    show (e n : H2) ≠ 0
    exact e_ne_zero n, Tp_eDom n⟩

/-- **Converse (spectrum of the unbounded toy operator is exactly `ℕ`).** Every eigenvalue of
`Tp` is a natural number, by looking at a nonzero coordinate of the eigenvector — the same
argument as the registered `InfDim.eigenvalue_mem_range` for the bounded operator `R` (reused,
not reproduced, for `R`'s own side of the bridge theorem below; `Tp`'s analogous fact is proved
fresh here since `Tp` itself is new). -/
theorem Tp_eigenvalue_mem_range {mu : ℂ} (h : IsEigenvalue Tp mu) : ∃ n : ℕ, mu = (n : ℂ) := by
  obtain ⟨v, hv0, hveq⟩ := h
  obtain ⟨i, hi⟩ := exists_ne_zero_coord hv0
  refine ⟨i, ?_⟩
  have hcoord := congrArg (fun g : H2 => (g : ∀ _ : ℕ, ℂ) i) hveq
  simp only [Tp_apply, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul] at hcoord
  exact (mul_right_cancel₀ hi hcoord).symm

/-! ### §4 — THE BRIDGE (part (2) of the task): connecting `IsEigenvalue Tp mu` (the unbounded
`LinearPMap`) BY HAND to `Module.End.HasEigenvalue` of the bounded operator `R := InfDim.T`.
`R`'s diagonal `1/(n+1)` is the explicit inverse-shift of `Tp`'s diagonal `n`: on the shared
eigenvector `e n`, `(Tp + 1) (e n) = (n + 1) • e n` while `R (e n) = (1/(n+1)) • e n`. -/

/-- **SHARED-2C main bridge theorem — the falsifiable test.** `mu` is an eigenvalue of the
unbounded toy `LinearPMap` `Tp` iff `(mu + 1)⁻¹` is an eigenvalue (in the
`Module.End.HasEigenvalue` sense) of the bounded operator `R := InfDim.T`
(`TamesisLab.Foundations.SpectralCounting.InfDim.T`, opened above as `T`), i.e. the explicit
diagonal operator `1/(n+1)` already registered in the lab. No side condition on `mu` is needed:
both sides are automatically false at the ℂ-inverse junk value `mu = -1` (there `(mu+1)⁻¹ = 0`,
and `0` is never one of `Tp`'s or `R`'s eigenvalues — every eigenvalue of `Tp` is a nonneg
integer cast, and every eigenvalue of `R` is `dseq i = 1/(i+1) ≠ 0`), so the `↔` holds
unconditionally, though the two "always false at `mu = -1`" side facts are not separately proved
here — only the `↔` itself, which does not need them. This is the hand-built connection between
the `LinearPMap`-level characterization and `Module.End.HasEigenvalue`. -/
theorem eigenvalue_bridge (mu : ℂ) :
    IsEigenvalue Tp mu ↔ Module.End.HasEigenvalue (T : Module.End ℂ H2) (mu + 1)⁻¹ := by
  constructor
  · intro h
    obtain ⟨n, rfl⟩ := Tp_eigenvalue_mem_range h
    have hcast : ((n : ℂ) + 1)⁻¹ = ((dseq n : ℝ) : ℂ) := by
      unfold dseq
      push_cast
      rw [one_div]
    rw [hcast]
    exact hasEigenvalue_T n
  · intro h
    obtain ⟨i, hi⟩ := eigenvalue_mem_range h
    have hcast : ((dseq i : ℝ) : ℂ) = ((i : ℂ) + 1)⁻¹ := by
      unfold dseq
      push_cast
      rw [one_div]
    rw [hcast] at hi
    have hmu_eq : (i : ℂ) + 1 = mu + 1 := inv_inj.mp hi
    have hmu : mu = (i : ℂ) := (add_right_cancel hmu_eq).symm
    rw [hmu]
    exact Tp_isEigenvalue i

end SHARED2C.LinearPMapEigenvalueBridge

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms SHARED2C.LinearPMapEigenvalueBridge.Tp_isEigenvalue
#print axioms SHARED2C.LinearPMapEigenvalueBridge.Tp_eigenvalue_mem_range
#print axioms SHARED2C.LinearPMapEigenvalueBridge.eigenvalue_bridge
