/-
  WAVE5-RH-6B — Cross-consistency bridge: `unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)` for
  `Lam ≥ 0` (Onda-5 task RH-6b).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-5
  task instructions on build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/Wave-2/Wave-3/Wave-4/
  other-Wave-5 file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`,
  `dseq`, `e`, `T`, `hasEigenvalue_T`, `eigenvalue_mem_range`, `exists_ne_zero_coord`, `eigCount`,
  `eigCount_def` exactly as-is (all REGISTERED, so imported directly — no reproduction needed for
  that half).

  WHY THIS FILE REPRODUCES (RATHER THAN `import`-ING) THE `Tp`/`IsEigenvalue`/`eigenvalue_bridge`/
  `eig_norm_transport_nat`/`eigenvalue_set_eq_preimage`/`unboundedEigCount` BLOCK. This file's
  falsifiable target needs, on its LHS, `unboundedEigCount` (WAVE3-RH-3,
  `UnboundedEigCountFloorLaw.lean`) and, as its main compositional step,
  `eigenvalue_set_eq_preimage` (WAVE4-RH-5, `EigenvalueSetBridgeRestricted.lean`), both same
  directory `03_MILLENNIUM/01_RIEMANN/FORMAL/`. Those files live OUTSIDE the `05_FORMAL/lean` Lake
  project root, are themselves declared "free-standing: NOT registered in `TamesisLab.lean`" in
  their own headers, and have no compiled `.olean` anywhere in `.lake/build/lib/lean` (checked
  directly this session: zero hits for `UnboundedEigCount` or `EigenvalueSetBridgeRestricted`
  under `.lake/build`). There is consequently no module import path that resolves to them. Rather
  than fabricate an ad hoc `.olean` placement in the shared, gitignored build cache used
  concurrently by 14 other Wave-5 sessions (a real option per the task instructions for a
  genuinely MISSING dependency, but one this file avoids for the same reason its own siblings
  give: minimizing interference with concurrent sessions writing into the same cache directory),
  this file follows the established sibling convention set by `UnboundedEigCountWeylLimitLaw.lean`
  (Wave-4 RH-4) and `EigenvalueSetBridgeRestricted.lean` (Wave-4 RH-5, same directory) for exactly
  this situation: it reproduces, BYTE-IDENTICAL, the full block of `EigenvalueSetBridgeRestricted
  .lean` through `eigenvalue_set_eq_preimage` — copied verbatim from that file's lines 118–316
  (§0 "the domain", §1 "the unbounded toy diagonal operator `Tp`", §2 "the falsifiable target:
  eigenvalue characterization", §3 "`Tp` has an eigenvector `e i` at every natural number `i`",
  §4 "THE BRIDGE `eigenvalue_bridge`", §5 "the restricted transport lemma and the eigenvalue-set
  bridge") — PLUS the `unboundedEigCount` definition from `UnboundedEigCountFloorLaw.lean` line
  245 (§4 there), under a fresh namespace (`RH6B.UnboundedEigCountEigCountBridge`) so no name
  clashes with either original file (neither of which this file ever touches) nor with the other
  Wave-3/Wave-4/Wave-5 siblings' own separate reproductions (each in its own distinct namespace —
  `RH3.UnboundedEigCountFloorLaw`, `RH4.UnboundedEigCountWeylLimitLaw`,
  `RH5.EigenvalueSetBridgeRestricted`, `RH6A.UnboundedEigCountRateBound`). The reproduced block is
  NOT reproved or reinterpreted — every line is copied as-is, including its own original doc
  comments (some of which reference "route-b", "the task", "WAVE4-RH-5" — those refer to the
  ORIGINAL Wave-4 RH-5 task, not this file's task; kept verbatim per the copy-exactly instruction
  rather than edited, to avoid any risk of silently introducing a divergence from the cited source
  during transcription).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-5 RH-6b task statement, nothing broader):

  > (i) `{nu:C | HasEigenvalue T nu ∧ (Lam+1)⁻¹ ≤ ‖nu‖} = (Complex.ofReal) ''
  >   {mu:R | (Lam+1)⁻¹ ≤ |mu| ∧ HasEigenvalue T (mu:C)}`, via `Complex.norm_real` + `ext`;
  > (ii) tomar `ncard` de ambos os lados via `Set.ncard_image_of_injective` +
  >   `Complex.ofReal_injective` para obter `S.ncard = eigCount T ((Lam+1)⁻¹)`;
  > (iii) compor com `eigenvalue_set_eq_preimage` (RH-5) via
  >   `Set.ncard_preimage_of_injective_subset_range` para fechar
  >   `unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)` para `Lam ≥ 0`.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §6 below — everything before
  §6 is the verbatim reproduction described above, plus the direct, read-only reuse of `eigCount`/
  `eigCount_def`/`eigenvalue_mem_range`/`hasEigenvalue_T` from the imported registered module).

  * `inv_shift_injective : Function.Injective (fun mu : ℂ => (mu + 1)⁻¹)` — the map `f mu = (mu+1)
    ⁻¹` is injective on ALL of `ℂ` (not just the restricted domain needed by
    `eigenvalue_set_eq_preimage`): `(a+1)⁻¹ = (b+1)⁻¹ → a+1 = b+1` via `inv_inj` (valid in any
    `GroupWithZero`, in particular `ℂ`, since `x ↦ x⁻¹` is literally injective there —
    `Mathlib/Algebra/Group/Basic.lean:296`, instantiated at the `GroupWithZero` level for `ℂ`),
    then `add_right_cancel`.
  * `inv_shift_surjective : Function.Surjective (fun mu : ℂ => (mu + 1)⁻¹)` — for ANY `nu:ℂ`
    (including `nu = 0`), `mu := nu⁻¹ - 1` satisfies `(mu+1)⁻¹ = nu`: `mu + 1 = nu⁻¹` by `ring`
    (pure commutative-ring rewriting, needs no case split on `nu = 0`), then `inv_inv` (valid
    unconditionally in a `GroupWithZero`, including at the junk value `0⁻¹⁻¹ = 0⁻¹ = 0`). Hence
    `f`'s range is ALL of `ℂ` — stronger than what step (iii) needs (`s ⊆ range f`), but the
    cleanest way to discharge that hypothesis.
  * `complex_eigenvalue_band_eq_image` — **STEP (i), CLOSED.** Exactly the target set equality:
    `{nu:ℂ | HasEigenvalue T nu ∧ (Lam+1)⁻¹ ≤ ‖nu‖} = Complex.ofReal ''
    {mu:ℝ | (Lam+1)⁻¹ ≤ |mu| ∧ HasEigenvalue T (mu:ℂ)}`, proved by `ext nu` in two symmetric
    halves. Forward: `eigenvalue_mem_range` (imported, registered) forces `nu = (dseq i : ℂ)` for
    some `i`, giving the real witness `mu := dseq i`; `Complex.norm_real` (`‖(r:ℂ)‖ = ‖r‖`) plus
    `Real.norm_eq_abs` transport the norm bound `(Lam+1)⁻¹ ≤ ‖nu‖` to `(Lam+1)⁻¹ ≤ |mu|`. Backward:
    direct from `Complex.norm_real`/`Real.norm_eq_abs` again, no further lemma needed.
  * `real_eigenvalue_band_ncard_eq_eigCount` — **STEP (ii), CLOSED.**
    `{mu:ℝ | (Lam+1)⁻¹ ≤ |mu| ∧ HasEigenvalue T (mu:ℂ)}.ncard = eigCount T ((Lam+1)⁻¹)`, literally
    `(eigCount_def ((Lam+1)⁻¹)).symm` (imported, registered — `eigCount_def` states exactly this
    set as the definitional unfolding of `eigCount`, `SpectralCountingInstance.lean` §8).
  * `complex_eigenvalue_band_ncard_eq_eigCount` — the two steps above composed with
    `Set.ncard_image_of_injective _ Complex.ofReal_injective`:
    `{nu:ℂ | HasEigenvalue T nu ∧ (Lam+1)⁻¹ ≤ ‖nu‖}.ncard = eigCount T ((Lam+1)⁻¹)`.
  * `unboundedEigCount_eq_eigCount` — **THE FALSIFIABLE TARGET, CLOSED.**
    `unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)` for every `Lam ≥ 0` — step (iii): unfold
    `unboundedEigCount`, rewrite along `eigenvalue_set_eq_preimage Lam hLam` (RH-5, reproduced
    above), apply `Set.ncard_preimage_of_injective_subset_range inv_shift_injective` (subset-of-
    range hypothesis discharged by `inv_shift_surjective.range_eq` making the range all of `ℂ`),
    then close with `complex_eigenvalue_band_ncard_eq_eigCount`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching the Wave-5 task
  instructions). This file says nothing about, and does not approximate, a solution to the Riemann
  Hypothesis or any Clay Millennium Prize problem: `Tp` remains a hand-built, purely algebraic toy
  `LinearPMap` on `ℓ²(ℕ,ℂ)` with no topology, no self-adjointness claim, and no connection
  whatsoever to `riemannZeta`/`N_zeta`/any spectral interpretation of the zeta zeros; `T` remains
  the same hand-built compact diagonal toy operator already registered in Wave-1. No mathematical
  novelty is claimed: showing that two DIFFERENT eigenvalue-counting conventions (one for an
  unbounded toy operator with an inverse-shifted diagonal, one for its bounded resolvent-like
  cousin) agree after the change of variables `nu = (mu+1)⁻¹` already forced by
  `eigenvalue_bridge`/`eigenvalue_set_eq_preimage` is an elementary bookkeeping fact about
  cardinalities of finite sets under bijections, not a new mathematical result.

  Every Mathlib name used below was checked by direct read/grep against the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in addition to compiling cleanly
  via `lake env lean` (see the file's own build log for the exact command/exit code, reported
  alongside this file).
-/
import Mathlib
import TamesisLab.Foundations.SpectralCountingInstance

open scoped ENNReal lp InnerProductSpace
open Filter Topology
open TamesisLab.Foundations.SpectralCounting
open TamesisLab.Foundations.SpectralCounting.InfDim

namespace RH6B.UnboundedEigCountEigCountBridge

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`.

(Verbatim reproduction of `EigenvalueSetBridgeRestricted.lean` §0, lines 118–146 — see file header
for why this file reproduces rather than imports.) -/

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
diagonal operator `T x_n = n * x_n`, distinct from the already-registered bounded diagonal
operator `TamesisLab.Foundations.SpectralCounting.InfDim.T` (opened above simply as `T`), which
plays the role of `R` in the Wave-2/Wave-3/Wave-4 sibling files.

(Verbatim reproduction of `EigenvalueSetBridgeRestricted.lean` §1, lines 156–177.) -/

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

`mu : ℂ` is characterized as an eigenvalue of a `LinearPMap T : H2 →ₗ.[ℂ] H2` via
`∃ v ∈ T.domain, v ≠ 0, T v = mu * v` (phrased over the subtype `T.domain`).

(Verbatim reproduction of `EigenvalueSetBridgeRestricted.lean` §2, lines 185–187.) -/

/-- **The falsifiable eigenvalue predicate for a `LinearPMap`.** -/
def IsEigenvalue (T : H2 →ₗ.[ℂ] H2) (mu : ℂ) : Prop :=
  ∃ v : T.domain, (v : H2) ≠ 0 ∧ T v = mu • (v : H2)

/-! ### §3 — `Tp` has an eigenvector `e i` at every natural number `i`, matching `R`'s own
`e i` eigenvector for `dseq i` in `InfDim` (imported, read-only).

(Verbatim reproduction of `EigenvalueSetBridgeRestricted.lean` §3, lines 194–230.) -/

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
`Tp` is a natural number, by looking at a nonzero coordinate of the eigenvector. -/
theorem Tp_eigenvalue_mem_range {mu : ℂ} (h : IsEigenvalue Tp mu) : ∃ n : ℕ, mu = (n : ℂ) := by
  obtain ⟨v, hv0, hveq⟩ := h
  obtain ⟨i, hi⟩ := exists_ne_zero_coord hv0
  refine ⟨i, ?_⟩
  have hcoord := congrArg (fun g : H2 => (g : ∀ _ : ℕ, ℂ) i) hveq
  simp only [Tp_apply, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul] at hcoord
  exact (mul_right_cancel₀ hi hcoord).symm

/-! ### §4 — THE BRIDGE: connecting `IsEigenvalue Tp mu` (the unbounded `LinearPMap`) BY HAND to
`Module.End.HasEigenvalue` of the bounded operator `R := InfDim.T`.

(Verbatim reproduction of `EigenvalueSetBridgeRestricted.lean` §4, lines 239–269.) -/

/-- **`eigenvalue_bridge`.** `mu` is an eigenvalue of the unbounded toy `LinearPMap` `Tp` iff
`(mu + 1)⁻¹` is an eigenvalue (in the `Module.End.HasEigenvalue` sense) of the bounded operator
`R := InfDim.T`. -/
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

/-! ### §5 — the restricted transport lemma and the eigenvalue-set bridge (WAVE4-RH-5).

(Verbatim reproduction of `EigenvalueSetBridgeRestricted.lean` §5, lines 276–316.) -/

/-- **The restricted transport lemma** (deliberately restricted to `mu = (n:ℂ)`, `n:ℕ` — the
UNRESTRICTED version is FALSE, counterexample `mu = i`, `Lam = 0.5`, see the RH-5 file header).
For `Lam ≥ 0` and `n : ℕ`, `(n:ℝ) ≤ Lam` iff `(Lam+1)⁻¹ ≤ ‖((n:ℂ)+1)⁻¹‖`. -/
theorem eig_norm_transport_nat (Lam : ℝ) (hLam : 0 ≤ Lam) (n : ℕ) :
    (n : ℝ) ≤ Lam ↔ (Lam + 1)⁻¹ ≤ ‖((n : ℂ) + 1)⁻¹‖ := by
  have hcast : ((n : ℂ) + 1) = ((n + 1 : ℕ) : ℂ) := by push_cast; ring
  rw [norm_inv, hcast, Complex.norm_natCast]
  push_cast
  constructor
  · intro h
    exact (inv_le_inv₀ (by linarith) (by positivity)).mpr (by linarith)
  · intro h
    have h' := (inv_le_inv₀ (by linarith) (by positivity)).mp h
    linarith

/-- **`eigenvalue_set_eq_preimage` (WAVE4-RH-5, reused byte-identical as the starting point for
this file's own falsifiable target below).** For `Lam ≥ 0`, the `Tp`-eigenvalue band
`{mu | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}` equals the preimage, under `mu ↦ (mu+1)⁻¹`, of the
`R`-eigenvalue band `{nu | HasEigenvalue T nu ∧ (Lam+1)⁻¹ ≤ ‖nu‖}`. -/
theorem eigenvalue_set_eq_preimage (Lam : ℝ) (hLam : 0 ≤ Lam) :
    {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}
      = (fun mu : ℂ => (mu + 1)⁻¹) ⁻¹'
          {nu : ℂ | Module.End.HasEigenvalue (T : Module.End ℂ H2) nu ∧ (Lam + 1)⁻¹ ≤ ‖nu‖} := by
  ext mu
  simp only [Set.mem_setOf_eq, Set.mem_preimage]
  constructor
  · rintro ⟨hEig, hle⟩
    obtain ⟨n, rfl⟩ := Tp_eigenvalue_mem_range hEig
    refine ⟨(eigenvalue_bridge (n : ℂ)).mp hEig, ?_⟩
    rw [Complex.norm_natCast] at hle
    exact (eig_norm_transport_nat Lam hLam n).mp hle
  · rintro ⟨hHas, hle⟩
    have hEig : IsEigenvalue Tp mu := (eigenvalue_bridge mu).mpr hHas
    obtain ⟨n, rfl⟩ := Tp_eigenvalue_mem_range hEig
    refine ⟨hEig, ?_⟩
    rw [Complex.norm_natCast]
    exact (eig_norm_transport_nat Lam hLam n).mpr hle

/-! ### §5b — `unboundedEigCount` (WAVE3-RH-3, reused byte-identical).

(Verbatim reproduction of `UnboundedEigCountFloorLaw.lean` §4 (definition only), line 245.) -/

/-- **The unbounded-operator-style eigenvalue counting function** (contrast with the
bounded-operator `eigCount` of `SpectralCounting.lean`/`SpectralCountingInstance.lean`, which
counts ABOVE a threshold and is finite because its operator is compact): counts `Tp`'s
eigenvalues with norm AT MOST `Lam`, growing as `Lam → ∞`. -/
noncomputable def unboundedEigCount (Lam : ℝ) : ℕ :=
  {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}.ncard

/-! ### §6 — NEW (WAVE5-RH-6B): the cross-consistency bridge to `eigCount`

This section is NOT a reproduction of anything: it is this file's own new content, the
falsifiable target for WAVE5-RH-6B. Everything above `unboundedEigCount` is the verbatim
reproduction described in the file header; `eigCount`/`eigCount_def`/`eigenvalue_mem_range`/
`hasEigenvalue_T` below are the registered, imported originals from
`TamesisLab.Foundations.SpectralCounting.InfDim` (NOT reproduced — genuinely reused by name). -/

/-- `f mu = (mu+1)⁻¹` is injective on all of `ℂ` (stronger than the restricted-domain fact
`eigenvalue_bridge`/`eigenvalue_set_eq_preimage` need): `inv_inj` (valid in the `GroupWithZero`
`ℂ`) plus `add_right_cancel`. -/
theorem inv_shift_injective : Function.Injective (fun mu : ℂ => (mu + 1)⁻¹) := by
  intro a b hab
  simp only at hab
  exact add_right_cancel (inv_inj.mp hab)

/-- `f mu = (mu+1)⁻¹` is surjective on all of `ℂ`: for any `nu`, `mu := nu⁻¹ - 1` satisfies
`(mu+1)⁻¹ = nu`, via the ring identity `mu + 1 = nu⁻¹` (no case split on `nu = 0` needed) followed
by `inv_inv` (unconditional in a `GroupWithZero`, including at the junk value `0⁻¹⁻¹ = 0`). -/
theorem inv_shift_surjective : Function.Surjective (fun mu : ℂ => (mu + 1)⁻¹) := by
  intro nu
  refine ⟨nu⁻¹ - 1, ?_⟩
  show (nu⁻¹ - 1 + 1)⁻¹ = nu
  have hstep : nu⁻¹ - 1 + 1 = nu⁻¹ := by ring
  rw [hstep, inv_inv]

/-- Consequently the range of `f` is all of `ℂ`. -/
theorem inv_shift_range : Set.range (fun mu : ℂ => (mu + 1)⁻¹) = Set.univ :=
  inv_shift_surjective.range_eq

/-- **STEP (i), CLOSED.** For `Lam ≥ 0` (not actually needed here, kept for parallelism with the
task statement — the equality holds for every `Lam : ℝ`), the complex `R`-eigenvalue band above
`(Lam+1)⁻¹` equals the image, under `Complex.ofReal`, of the real `R`-eigenvalue band above
`(Lam+1)⁻¹` — every eigenvalue of `T` is real (`eigenvalue_mem_range`, registered), so the two
bands correspond exactly. Proved via `ext` + `Complex.norm_real`/`Real.norm_eq_abs`, exactly as
the task specifies. -/
theorem complex_eigenvalue_band_eq_image (Lam : ℝ) :
    {nu : ℂ | Module.End.HasEigenvalue (T : Module.End ℂ H2) nu ∧ (Lam + 1)⁻¹ ≤ ‖nu‖}
      = Complex.ofReal ''
          {mu : ℝ | (Lam + 1)⁻¹ ≤ |mu| ∧
            Module.End.HasEigenvalue (T : Module.End ℂ H2) (mu : ℂ)} := by
  ext nu
  simp only [Set.mem_setOf_eq, Set.mem_image]
  constructor
  · rintro ⟨hHas, hle⟩
    obtain ⟨i, hi⟩ := eigenvalue_mem_range hHas
    refine ⟨dseq i, ⟨?_, hasEigenvalue_T i⟩, hi⟩
    rw [← hi, Complex.norm_real, Real.norm_eq_abs] at hle
    exact hle
  · rintro ⟨mu, ⟨hmuAbs, hmuHas⟩, rfl⟩
    refine ⟨hmuHas, ?_⟩
    rw [Complex.norm_real, Real.norm_eq_abs]
    exact hmuAbs

/-- **STEP (ii), CLOSED.** The real `R`-eigenvalue band above `(Lam+1)⁻¹` has `ncard` exactly
`eigCount T ((Lam+1)⁻¹)` — literally the definitional unfolding `eigCount_def` (registered),
read backwards. -/
theorem real_eigenvalue_band_ncard_eq_eigCount (Lam : ℝ) :
    {mu : ℝ | (Lam + 1)⁻¹ ≤ |mu| ∧
      Module.End.HasEigenvalue (T : Module.End ℂ H2) (mu : ℂ)}.ncard
      = eigCount T ((Lam + 1)⁻¹) :=
  (eigCount_def ((Lam + 1)⁻¹)).symm

/-- Steps (i)+(ii) composed via `Set.ncard_image_of_injective` +
`Complex.ofReal_injective`: the complex `R`-eigenvalue band above `(Lam+1)⁻¹` has `ncard` exactly
`eigCount T ((Lam+1)⁻¹)`. -/
theorem complex_eigenvalue_band_ncard_eq_eigCount (Lam : ℝ) :
    {nu : ℂ | Module.End.HasEigenvalue (T : Module.End ℂ H2) nu ∧ (Lam + 1)⁻¹ ≤ ‖nu‖}.ncard
      = eigCount T ((Lam + 1)⁻¹) := by
  rw [complex_eigenvalue_band_eq_image,
    Set.ncard_image_of_injective _ Complex.ofReal_injective,
    real_eigenvalue_band_ncard_eq_eigCount]

/-- **THE FALSIFIABLE TARGET, CLOSED.** `unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)` for
every `Lam ≥ 0` — step (iii): unfold `unboundedEigCount`, rewrite along `eigenvalue_set_eq_preimage`
(RH-5, reproduced above), take `ncard` of the preimage via
`Set.ncard_preimage_of_injective_subset_range` (using `inv_shift_injective` and the subset-of-range
fact from `inv_shift_range`), then close with `complex_eigenvalue_band_ncard_eq_eigCount`. -/
theorem unboundedEigCount_eq_eigCount {Lam : ℝ} (hLam : 0 ≤ Lam) :
    unboundedEigCount Lam = eigCount T ((Lam + 1)⁻¹) := by
  unfold unboundedEigCount
  rw [eigenvalue_set_eq_preimage Lam hLam,
    Set.ncard_preimage_of_injective_subset_range inv_shift_injective
      (by rw [inv_shift_range]; exact Set.subset_univ _),
    complex_eigenvalue_band_ncard_eq_eigCount]

end RH6B.UnboundedEigCountEigCountBridge

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH6B.UnboundedEigCountEigCountBridge.Tp_isEigenvalue
#print axioms RH6B.UnboundedEigCountEigCountBridge.Tp_eigenvalue_mem_range
#print axioms RH6B.UnboundedEigCountEigCountBridge.eigenvalue_bridge
#print axioms RH6B.UnboundedEigCountEigCountBridge.eig_norm_transport_nat
#print axioms RH6B.UnboundedEigCountEigCountBridge.eigenvalue_set_eq_preimage
#print axioms RH6B.UnboundedEigCountEigCountBridge.inv_shift_injective
#print axioms RH6B.UnboundedEigCountEigCountBridge.inv_shift_surjective
#print axioms RH6B.UnboundedEigCountEigCountBridge.inv_shift_range
#print axioms RH6B.UnboundedEigCountEigCountBridge.complex_eigenvalue_band_eq_image
#print axioms RH6B.UnboundedEigCountEigCountBridge.real_eigenvalue_band_ncard_eq_eigCount
#print axioms RH6B.UnboundedEigCountEigCountBridge.complex_eigenvalue_band_ncard_eq_eigCount
#print axioms RH6B.UnboundedEigCountEigCountBridge.unboundedEigCount_eq_eigCount
