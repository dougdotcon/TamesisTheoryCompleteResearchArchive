/-
  WAVE6-RH-7A — Composition of the WAVE5-RH-6A rate bound with the WAVE5-RH-6B `eigCount` bridge,
  under a single shared namespace (Onda-6 task RH-7a).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-6
  task instructions on build contention with 13 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/.../Wave-5 file nor
  any other Wave-6 item's file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`,
  `dseq`, `e`, `e_apply`, `e_ne_zero`, `T`, `hasEigenvalue_T`, `eigenvalue_mem_range`,
  `exists_ne_zero_coord`, `eigCount`, `eigCount_def` exactly as-is (all REGISTERED, so imported
  directly — no reproduction needed for that half).

  WHY THIS FILE REPRODUCES (RATHER THAN `import`-ING) BOTH SOURCE BLOCKS INTO ONE NAMESPACE. The
  Onda-6 task for RH-7A is EXACTLY to compose `UnboundedEigCountRateBound.lean`'s
  `unboundedEigCount_rate_bound` (WAVE5-RH-6A) with `UnboundedEigCountEigCountBridge.lean`'s
  `unboundedEigCount_eq_eigCount` (WAVE5-RH-6B) via
  `rw [← unboundedEigCount_eq_eigCount hLam.le]; exact unboundedEigCount_rate_bound hLam`. As the
  Onda-6 planning workflow diagnosed (`PLANO_DE_ATAQUE_ONDA_6_2026_08_11.md`, RH-7A section) this
  literal tactic script does NOT type-check as a cross-file composition of the two PRE-EXISTING
  lemma names, because they live in two DIFFERENT namespaces
  (`RH6A.UnboundedEigCountRateBound` vs. `RH6B.UnboundedEigCountEigCountBridge`), each with its
  OWN separately-declared `Tp`/`finiteSupport`/`unboundedEigCount` (confirmed by grep: `noncomputable
  def Tp` appears once per file, in 6 distinct namespaces across the RH FORMAL directory) — `rw`
  needs syntactic/constant identity, and `unboundedEigCount` in one file's namespace is a DIFFERENT
  constant from `unboundedEigCount` in the other's, even though both definitions are byte-identical.
  Neither source file is itself importable (both are free-standing, outside the `05_FORMAL/lean`
  Lake project root, with no compiled `.olean` in `.lake/build/lib/lean` — checked directly this
  session: zero hits for `UnboundedEigCountRateBound`/`UnboundedEigCountEigCountBridge` under
  `.lake/build`), so this file follows the convention already established by every RH-3..RH-6C
  sibling for exactly this situation: it reproduces, BYTE-IDENTICAL, both source blocks under ONE
  shared fresh namespace (`RH7A.UnboundedEigCountRateBoundEigCountBridge`), so that the SAME local
  `Tp`/`unboundedEigCount` constants back both derivations, and the closing `rw` chain becomes a
  literal, syntactically-valid rewrite against the file's own local lemma names.

  * Part (a), §0–§6 below: copied verbatim from `UnboundedEigCountEigCountBridge.lean` lines
    118–411 (§0 "the domain", §1 "the unbounded toy diagonal operator `Tp`", §2 "the falsifiable
    target: eigenvalue characterization", §3 "`Tp` has an eigenvector `e i` at every natural
    number `i`", §4 "THE BRIDGE `eigenvalue_bridge`", §5 "the restricted transport lemma and the
    eigenvalue-set bridge", §5b "`unboundedEigCount`", §6 "the cross-consistency bridge to
    `eigCount`") — through `unboundedEigCount_eq_eigCount`.
  * Part (b), §7 below: copied verbatim from `UnboundedEigCountRateBound.lean` lines 269–283 (§5
    "the non-asymptotic rate bound") — i.e. `unboundedEigCount_rate_bound` itself, WITHOUT its own
    copy of §0–§4 (the domain/`Tp`/eigenvector block), since that block is IDENTICAL to part (a)'s
    §0–§3 already present in this file and is reused rather than duplicated a second time (the
    task's "ambos sobre o MESMO Tp/unboundedEigCount local" requirement — a single shared `Tp` and
    a single shared `unboundedEigCount`, not two separate copies inside this one file).

  Both reproduced blocks are NOT reproved or reinterpreted — every line is copied as-is, including
  original doc comments (some reference "route-b", "the task", "WAVE4-RH-5", "WAVE5-RH-6A/6B" —
  those refer to the ORIGINAL Wave-4/Wave-5 tasks, not this file's task; kept verbatim per the
  copy-exactly instruction rather than edited, to avoid any risk of silently introducing a
  divergence from the cited sources during transcription).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Onda-6 RH-7a task statement, nothing broader):

  > Em arquivo novo (namespace unico), reproduzir byte-a-byte o bloco
  > UnboundedEigCountEigCountBridge ate unboundedEigCount_eq_eigCount e a derivacao de
  > piso-sanduiche de unboundedEigCount_rate_bound, ambos sobre o MESMO Tp/unboundedEigCount
  > local. Fechar, para Lam>0:
  > `0 < (eigCount T ((Lam+1)⁻¹):R)/Lam-1 ∧ (eigCount T ((Lam+1)⁻¹):R)/Lam-1 <= 1/Lam` via
  > `rw [← unboundedEigCount_eq_eigCount hLam.le]; exact unboundedEigCount_rate_bound hLam`,
  > usando os nomes locais do proprio arquivo. `#print axioms` limpo.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §8 below — everything before
  §8 is the verbatim reproduction described above).
  * `unboundedEigCount_rate_bound_via_eigCount` — **THE FALSIFIABLE TARGET, CLOSED.** For
    `Lam > 0`: `0 < (eigCount T ((Lam+1)⁻¹):ℝ)/Lam - 1 ∧ (eigCount T ((Lam+1)⁻¹):ℝ)/Lam - 1 ≤
    1/Lam`, proved EXACTLY via the two-line tactic script the task specifies:
    `rw [← unboundedEigCount_eq_eigCount hLam.le]; exact unboundedEigCount_rate_bound hLam` —
    both `unboundedEigCount_eq_eigCount` and `unboundedEigCount_rate_bound` are this file's OWN
    local lemma names (§6 and §7 respectively), backed by the SAME local `Tp` (§1) and the SAME
    local `unboundedEigCount` (§5b), so the `rw` is a literal syntactic match, not a cross-file
    coercion. Mathematically this is exactly the WAVE5-RH-6A non-asymptotic floor-sandwich rate
    bound `⌊Lam⌋₊ ≤ Lam < ⌊Lam⌋₊ + 1`, transported through the WAVE5-RH-6B change-of-variables
    `unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)` — nothing new is proved about either
    `unboundedEigCount`, `eigCount`, or the change of variables; this file only makes the
    COMPOSITION of the two pre-existing Onda-5 results type-check under a shared namespace, as
    diagnosed by the Onda-6 planning workflow.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching the Wave-6 task
  instructions). This file says nothing about, and does not approximate, a solution to the Riemann
  Hypothesis or any Clay Millennium Prize problem: `Tp` remains a hand-built, purely algebraic toy
  `LinearPMap` on `ℓ²(ℕ,ℂ)` with no topology, no self-adjointness claim, and no connection
  whatsoever to `riemannZeta`/`N_zeta`/any spectral interpretation of the zeta zeros; `T` remains
  the same hand-built compact diagonal toy operator already registered in Wave-1. No mathematical
  novelty is claimed: this file's ENTIRE new content is the observation that two ALREADY-PROVED
  Onda-5 facts (a change-of-variables identity and a floor-sandwich rate bound), both about the
  SAME underlying toy construction but declared in separate namespaces in separate files, compose
  by direct substitution once brought under one namespace — an elementary bookkeeping step, not a
  new mathematical result, and precisely the kind of "namespace-fragmentation" gap the Onda-6
  planning workflow flagged as `NEEDS_NARROWING` before narrowing it to this exact reproduction.

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

namespace RH7A.UnboundedEigCountRateBoundEigCountBridge

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`.

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §0, lines 118–146.) -/

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
plays the role of `R` in the Wave-2/.../Wave-5 sibling files.

THIS `Tp` IS THE SINGLE SHARED CONSTANT reused below by BOTH part (a) (the `eigCount` bridge, §2–
§6) and part (b) (the rate bound, §7) — exactly what the task's "ambos sobre o MESMO
Tp/unboundedEigCount local" requires.

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §1, lines 170–190.) -/

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

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §2, lines 199–201.) -/

/-- **The falsifiable eigenvalue predicate for a `LinearPMap`.** -/
def IsEigenvalue (T : H2 →ₗ.[ℂ] H2) (mu : ℂ) : Prop :=
  ∃ v : T.domain, (v : H2) ≠ 0 ∧ T v = mu • (v : H2)

/-! ### §3 — `Tp` has an eigenvector `e i` at every natural number `i`, matching `R`'s own
`e i` eigenvector for `dseq i` in `InfDim` (imported, read-only).

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §3, lines 208–241.) -/

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

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §4, lines 248–272.) -/

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

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §5, lines 278–314.) -/

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

THIS IS THE SINGLE SHARED `unboundedEigCount` reused below by BOTH part (a) (§6, the `eigCount`
bridge) and part (b) (§7, the rate bound) — exactly what the task's "ambos sobre o MESMO
Tp/unboundedEigCount local" requires.

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §5b, lines 320–325.) -/

/-- **The unbounded-operator-style eigenvalue counting function** (contrast with the
bounded-operator `eigCount` of `SpectralCounting.lean`/`SpectralCountingInstance.lean`, which
counts ABOVE a threshold and is finite because its operator is compact): counts `Tp`'s
eigenvalues with norm AT MOST `Lam`, growing as `Lam → ∞`. -/
noncomputable def unboundedEigCount (Lam : ℝ) : ℕ :=
  {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}.ncard

/-! ### §6 — the cross-consistency bridge to `eigCount` (WAVE5-RH-6B, part (a) of this file's
composition).

(Verbatim reproduction of `UnboundedEigCountEigCountBridge.lean` §6, lines 335–411.) -/

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

/-- **`unboundedEigCount_eq_eigCount` — part (a)'s target, CLOSED.**
`unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)` for every `Lam ≥ 0` — step (iii): unfold
`unboundedEigCount`, rewrite along `eigenvalue_set_eq_preimage` (RH-5, reproduced above), apply
`Set.ncard_preimage_of_injective_subset_range` (using `inv_shift_injective` and the subset-of-
range fact from `inv_shift_range`), then close with `complex_eigenvalue_band_ncard_eq_eigCount`.
-/
theorem unboundedEigCount_eq_eigCount {Lam : ℝ} (hLam : 0 ≤ Lam) :
    unboundedEigCount Lam = eigCount T ((Lam + 1)⁻¹) := by
  unfold unboundedEigCount
  rw [eigenvalue_set_eq_preimage Lam hLam,
    Set.ncard_preimage_of_injective_subset_range inv_shift_injective
      (by rw [inv_shift_range]; exact Set.subset_univ _),
    complex_eigenvalue_band_ncard_eq_eigCount]

/-! ### §7 — the non-asymptotic floor-sandwich rate bound (WAVE5-RH-6A, part (b) of this file's
composition), reproduced against the SAME local `Tp`/`unboundedEigCount` declared above in §1/§5b
(NOT a second, separate copy — the whole point of putting both blocks in one namespace).

(Verbatim reproduction of `UnboundedEigCountRateBound.lean` §4 (lines 228–257, the direct-
bijection/floor-law steps needed to derive the rate bound) and §5 (lines 269–283, the rate bound
itself). `UnboundedEigCountRateBound.lean`'s OWN §0–§3 — domain/`Tp`/eigenvector — are NOT
reproduced a second time here: they are already present verbatim in this file's §0–§3 above, and
are IDENTICAL between the two source files (both are themselves verbatim reproductions of the same
original `UnboundedEigCountFloorLaw.lean` block), so reusing this file's own §0–§3 is the correct
reading of "sobre o MESMO Tp/unboundedEigCount local", not a divergence from either source.) -/

/-- **The direct bijection**: the eigenvalue-band-below-`Lam` set is exactly the image of
`{n : ℕ | (n:ℝ) ≤ Lam}` under `Nat.cast : ℕ → ℂ`. -/
theorem eigenvalues_below_eq_image (Lam : ℝ) :
    {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}
      = (fun n : ℕ => (n : ℂ)) '' {n : ℕ | (n : ℝ) ≤ Lam} := by
  ext mu
  simp only [Set.mem_setOf_eq, Set.mem_image]
  constructor
  · rintro ⟨hEig, hle⟩
    obtain ⟨n, rfl⟩ := Tp_eigenvalue_mem_range hEig
    refine ⟨n, ?_, rfl⟩
    rwa [Complex.norm_natCast] at hle
  · rintro ⟨n, hn, rfl⟩
    refine ⟨Tp_isEigenvalue n, ?_⟩
    rwa [Complex.norm_natCast]

/-- `{n : ℕ | (n:ℝ) ≤ Lam} = ↑(Finset.range (⌊Lam⌋₊ + 1))` for `0 ≤ Lam`, via
`Nat.le_floor_iff`. -/
theorem nat_le_Lam_eq_range {Lam : ℝ} (hLam : 0 ≤ Lam) :
    {n : ℕ | (n : ℝ) ≤ Lam} = ↑(Finset.range (⌊Lam⌋₊ + 1)) := by
  ext n
  simp only [Set.mem_setOf_eq, Finset.coe_range, Set.mem_Iio]
  rw [Nat.lt_add_one_iff, Nat.le_floor_iff hLam]

/-- **The WAVE3-RH-3 floor law**, reused (byte-identical statement and proof) as the starting
point for `unboundedEigCount_rate_bound` below. `unboundedEigCount Lam = ⌊Lam⌋₊ + 1` for
every `Lam ≥ 0`. -/
theorem unboundedEigCount_eq_floor {Lam : ℝ} (hLam : 0 ≤ Lam) :
    unboundedEigCount Lam = ⌊Lam⌋₊ + 1 := by
  unfold unboundedEigCount
  rw [eigenvalues_below_eq_image, nat_le_Lam_eq_range hLam,
    Set.ncard_image_of_injective _ Nat.cast_injective, Set.ncard_coe_finset, Finset.card_range]

/-- **`unboundedEigCount_rate_bound` — part (b)'s target, CLOSED.** For `Lam > 0`, the ratio
`unboundedEigCount Lam / Lam` lies strictly above `1`, and exceeds it by at most `1 / Lam` — a
two-sided, non-asymptotic rate bound for the WAVE4-RH-4 Weyl-type limit law, valid at every
positive `Lam`, not just eventually. Direct from `unboundedEigCount_eq_floor` (cast to `ℝ`),
`Nat.floor_le`, and `Nat.lt_floor_add_one`, exactly as the task specifies. -/
theorem unboundedEigCount_rate_bound {Lam : ℝ} (hLam : 0 < Lam) :
    0 < (unboundedEigCount Lam : ℝ) / Lam - 1 ∧
      (unboundedEigCount Lam : ℝ) / Lam - 1 ≤ 1 / Lam := by
  have hLam0 : (0 : ℝ) ≤ Lam := hLam.le
  have hcount : (unboundedEigCount Lam : ℝ) = (⌊Lam⌋₊ : ℝ) + 1 := by
    exact_mod_cast unboundedEigCount_eq_floor hLam0
  rw [hcount, div_sub_one hLam.ne']
  have hfl : (⌊Lam⌋₊ : ℝ) ≤ Lam := Nat.floor_le hLam0
  have hlt : Lam < (⌊Lam⌋₊ : ℝ) + 1 := Nat.lt_floor_add_one Lam
  refine ⟨div_pos (by linarith) hLam, div_le_div_of_nonneg_right (by linarith) hLam0⟩

/-! ### §8 — NEW (WAVE6-RH-7A): the composition itself

This section is NOT a reproduction of anything: it is this file's own new content, the falsifiable
target for WAVE6-RH-7A. Both `unboundedEigCount_eq_eigCount` (§6) and `unboundedEigCount_rate_bound`
(§7) are declared in THIS file's single namespace, backed by THIS file's single `Tp` (§1) and
single `unboundedEigCount` (§5b) — so the composing `rw` below is a literal, syntactically-valid
rewrite of one local lemma name against another, exactly as the task specifies. -/

/-- **THE FALSIFIABLE TARGET, CLOSED.** For `Lam > 0`:
`0 < (eigCount T ((Lam+1)⁻¹) : ℝ) / Lam - 1 ∧ (eigCount T ((Lam+1)⁻¹) : ℝ) / Lam - 1 ≤ 1 / Lam` —
the WAVE5-RH-6A rate bound, transported along the WAVE5-RH-6B change of variables
`unboundedEigCount Lam = eigCount T ((Lam+1)⁻¹)`, composed under this file's single shared
namespace exactly as the task's tactic script specifies. -/
theorem unboundedEigCount_rate_bound_via_eigCount {Lam : ℝ} (hLam : 0 < Lam) :
    0 < (eigCount T ((Lam + 1)⁻¹) : ℝ) / Lam - 1 ∧
      (eigCount T ((Lam + 1)⁻¹) : ℝ) / Lam - 1 ≤ 1 / Lam := by
  rw [← unboundedEigCount_eq_eigCount hLam.le]
  exact unboundedEigCount_rate_bound hLam

end RH7A.UnboundedEigCountRateBoundEigCountBridge

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.Tp_isEigenvalue
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.Tp_eigenvalue_mem_range
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.eigenvalue_bridge
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.eig_norm_transport_nat
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.eigenvalue_set_eq_preimage
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.inv_shift_injective
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.inv_shift_surjective
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.inv_shift_range
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.complex_eigenvalue_band_eq_image
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.real_eigenvalue_band_ncard_eq_eigCount
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.complex_eigenvalue_band_ncard_eq_eigCount
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.unboundedEigCount_eq_eigCount
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.eigenvalues_below_eq_image
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.nat_le_Lam_eq_range
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.unboundedEigCount_eq_floor
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.unboundedEigCount_rate_bound
#print axioms RH7A.UnboundedEigCountRateBoundEigCountBridge.unboundedEigCount_rate_bound_via_eigCount
