/-
  WAVE3-RH-3 — `unboundedEigCount Lam = ⌊Lam⌋₊ + 1` for the toy unbounded diagonal `LinearPMap`
  `Tp`, direct route (Onda-3 task RH-3, route (a)).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-3
  task instructions on build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/Wave-2/other-Wave-3
  file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`, `e`,
  `e_apply`, `e_ne_zero` exactly as-is.

  WHY THIS FILE IS SELF-CONTAINED RATHER THAN `import`-ing `LinearPMapEigenvalueBridge.lean`
  DIRECTLY. The Wave-2 shared-infra source `LinearPMapEigenvalueBridge.lean`
  (`03_MILLENNIUM/_SHARED_INFRA/FORMAL/LinearPMapEigenvalueBridge.lean`) lives OUTSIDE the
  `05_FORMAL/lean` Lake project root, is itself declared "free-standing: NOT registered in
  `TamesisLab.lean`" in its own header, and has no compiled `.olean` anywhere in
  `.lake/build/lib/lean` (checked directly this session: zero hits for `LinearPMap` or
  `SHARED2C` under `.lake/build`). There is consequently no module import path that resolves to
  it. Rather than fabricate an ad hoc `.olean` placement in the shared, gitignored build cache
  (a real option per the Wave-3 task instructions for a genuinely MISSING dependency, but one
  this file avoids to minimize any chance of interfering with the 14 other concurrent sessions
  writing into the same cache directory), this file follows the established sibling convention
  set by `DiagonalSelfAdjointOperatorProbe.lean` (Wave-1 RH-3, same directory) for exactly this
  situation: it reproduces, BYTE-IDENTICAL, the minimal self-contained block of
  `LinearPMapEigenvalueBridge.lean` needed for route (a) of the falsifiable test — the
  definitions `finiteSupport`, `memℓp_of_finiteSupport`, `TpFun`, `Tp`, `Tp_apply`,
  `IsEigenvalue`, `e_mem_finiteSupport`, `eDom`, `eDom_coe`, `Tp_eDom`, and the theorems
  `Tp_isEigenvalue`, `Tp_eigenvalue_mem_range` — copied verbatim from
  `LinearPMapEigenvalueBridge.lean` lines 154–261 (§0 "the domain", §1 "the unbounded toy
  diagonal operator `Tp`", §2 "the falsifiable target: eigenvalue characterization", §3 "`Tp`
  has an eigenvector `e i` at every natural number `i`"), under a fresh namespace
  (`RH3.UnboundedEigCountFloorLaw`) so no name clashes with the original file (which this file
  never touches). The reproduced block is NOT reproved or reinterpreted — every line is copied
  as-is, including its own original doc comments (some of which reference "part (1)"/"part (2)
  of the task" — that refers to the ORIGINAL Wave-2 SHARED-2C task, not this file's task; kept
  verbatim per the copy-exactly instruction rather than edited, to avoid any risk of silently
  introducing a divergence from the cited source during transcription).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-3 RH-3 task statement, route (a), the one
  explicitly endorsed by the Onda-3 planning review as valid and SIMPLER than route (b)
  `eigenvalue_bridge`/`eigCount_eq_floor`, since `Tp`'s eigenvalue set is already known —
  `Tp_isEigenvalue`/`Tp_eigenvalue_mem_range` above — to be exactly `{(n:ℂ) : n ∈ ℕ}`, with no
  need to detour through the bounded resolvent operator `R`/`eigCount` at all):

  > Provar `unboundedEigCount Lam = Nat.floor Lam + 1` para `0 ≤ Lam`, via `Tp_isEigenvalue` +
  > `Tp_eigenvalue_mem_range`, bijetando o conjunto de autovalores com `{n : ℕ | n ≤ Lam}` via
  > `Nat.cast`.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §4 below — everything before
  §4 is the verbatim reproduction described above).
  * `unboundedEigCount (Lam : ℝ) : ℕ := {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}.ncard` — an
    UNBOUNDED-operator-style eigenvalue counting function, counting `Tp`'s eigenvalues with norm
    AT MOST `Lam` (growing as `Lam → ∞`), in explicit contrast to the bounded-operator `eigCount`
    of `SpectralCountingInstance.lean`/`SpectralCounting.lean`, which counts eigenvalues ABOVE a
    threshold and is finite for every threshold precisely because the underlying operator there
    is compact. `‖·‖` (the ambient `ℂ` norm) is used for "`Complex.abs`" from the task's own
    phrasing: this vendored Mathlib snapshot (`v4.33.0-rc1`) has no `Complex.abs` declaration at
    all (checked directly: zero hits under `Mathlib/Analysis/Complex/` and
    `Mathlib/Analysis/SpecialFunctions/Complex/`) — the modern replacement, confirmed present and
    used identically for this purpose, is the ordinary norm `‖·‖` on `ℂ`
    (`Complex.norm_natCast : ‖(n:ℂ)‖ = n`, `Mathlib/Analysis/Complex/Norm.lean:113`).
  * `eigenvalues_below_eq_image` — THE BIJECTION (the direct route the task asks for): the
    eigenvalue-band-below-`Lam` set equals the image of `{n : ℕ | (n:ℝ) ≤ Lam}` under
    `Nat.cast : ℕ → ℂ`. Forward: `Tp_eigenvalue_mem_range` forces `mu = (n:ℂ)`, then
    `Complex.norm_natCast` transports `‖mu‖ ≤ Lam` to `(n:ℝ) ≤ Lam`. Backward: `Tp_isEigenvalue n`
    plus `Complex.norm_natCast` again.
  * `nat_le_Lam_eq_range` — `{n : ℕ | (n:ℝ) ≤ Lam} = ↑(Finset.range (⌊Lam⌋₊ + 1))` for `0 ≤ Lam`,
    via `Nat.le_floor_iff` (`Mathlib/Algebra/Order/Floor/Defs.lean:140`) and
    `Nat.lt_add_one_iff` — the exact same shape of threshold lemma as
    `SpectralCountingInstance.InfDim.le_dseq_iff` (§9 of that file), which this file's proof
    otherwise does NOT depend on (route (a) never touches `eigCount`, `dseq`, or the bounded
    resolvent operator `R := InfDim.T` at all).
  * `unboundedEigCount_eq_floor` — **THE FALSIFIABLE TARGET, CLOSED.**
    `unboundedEigCount Lam = ⌊Lam⌋₊ + 1` for every `Lam ≥ 0`, by combining the two lemmas above
    with `Set.ncard_image_of_injective` (injectivity of `Nat.cast : ℕ → ℂ` via
    `Nat.cast_injective`, `Mathlib/Algebra/CharZero/Defs.lean:63`, since `ℂ` is `CharZero`),
    `Set.ncard_coe_finset`, and `Finset.card_range` — the same three-lemma closing combo already
    used successfully by `SpectralCountingInstance.eigCount_eq_floor`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly). Route (b) of the task
  (`eigenvalue_bridge` + `eigCount_eq_floor`, connecting `Tp`'s counting function to the BOUNDED
  resolvent operator `R`'s `eigCount`, with an explicit named inequality-transport lemma
  `‖mu‖ ≤ Lam ↔ (Lam+1)⁻¹ ≤ ‖(mu+1)⁻¹‖`) is NOT attempted here — the Onda-3 planning review
  explicitly endorsed route (a) alone as sufficient and noted route (b) requires an extra,
  separately-named transport step not needed by the simpler direct bijection. Nothing here says
  anything about, or approximates, a solution to the Riemann Hypothesis or any Clay Millennium
  Prize problem: `Tp` remains a hand-built, purely algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)`
  with no topology, no self-adjointness claim, and no connection whatsoever to
  `riemannZeta`/`N_zeta`/any spectral interpretation of the zeta zeros. No mathematical novelty
  is claimed: counting how many natural numbers `n` satisfy `n ≤ Lam` (namely `⌊Lam⌋₊ + 1` of
  them) is an elementary, classical fact about the naturals, merely transported here through a
  toy operator's eigenvalue set.

  Every Mathlib name used below was checked by direct read/grep against the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in addition to compiling
  cleanly via `lake env lean` (see the file's own build log for the exact command/exit code,
  reported alongside this file).
-/
import Mathlib
import TamesisLab.Foundations.SpectralCountingInstance

open scoped ENNReal lp InnerProductSpace
open Filter Topology
open TamesisLab.Foundations.SpectralCounting.InfDim

namespace RH3.UnboundedEigCountFloorLaw

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`.

(Verbatim reproduction of `LinearPMapEigenvalueBridge.lean` §0, lines 154–182 — see file header
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
diagonal operator `T x_n = n * x_n` from the task statement, distinct from the already-registered
bounded diagonal operator `TamesisLab.Foundations.SpectralCounting.InfDim.T` (opened above simply
as `T`), which plays the role of `R` below.

(Verbatim reproduction of `LinearPMapEigenvalueBridge.lean` §1, lines 191–211.) -/

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
in the task: `∃ v ∈ T.domain, v ≠ 0, T v = mu * v` (phrased over the subtype `T.domain`).

(Verbatim reproduction of `LinearPMapEigenvalueBridge.lean` §2, lines 219–220.) -/

/-- **The falsifiable eigenvalue predicate for a `LinearPMap`** (part (1) of the task). -/
def IsEigenvalue (T : H2 →ₗ.[ℂ] H2) (mu : ℂ) : Prop :=
  ∃ v : T.domain, (v : H2) ≠ 0 ∧ T v = mu • (v : H2)

/-! ### §3 — `Tp` has an eigenvector `e i` at every natural number `i`, matching `R`'s own
`e i` eigenvector for `dseq i` in `InfDim` (imported, read-only).

(Verbatim reproduction of `LinearPMapEigenvalueBridge.lean` §3, lines 225–261.) -/

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
not reproduced, for `R`'s own side of the bridge theorem in `LinearPMapEigenvalueBridge.lean`;
`Tp`'s analogous fact is proved fresh there, and copied verbatim here). -/
theorem Tp_eigenvalue_mem_range {mu : ℂ} (h : IsEigenvalue Tp mu) : ∃ n : ℕ, mu = (n : ℂ) := by
  obtain ⟨v, hv0, hveq⟩ := h
  obtain ⟨i, hi⟩ := exists_ne_zero_coord hv0
  refine ⟨i, ?_⟩
  have hcoord := congrArg (fun g : H2 => (g : ∀ _ : ℕ, ℂ) i) hveq
  simp only [Tp_apply, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul] at hcoord
  exact (mul_right_cancel₀ hi hcoord).symm

/-! ### §4 — NEW (WAVE3-RH-3): the unbounded eigenvalue counting function and its floor law

This section is NOT a reproduction of anything: it is this file's own new content, the
falsifiable target for WAVE3-RH-3. `unboundedEigCount Lam` counts `Tp`'s eigenvalues of norm at
most `Lam`; since `Tp`'s eigenvalue set is exactly `{(n:ℂ) : n ∈ ℕ}` (§2–§3 above), this count is
exactly the number of naturals `n ≤ Lam`, i.e. `⌊Lam⌋₊ + 1`. -/

/-- **The unbounded-operator-style eigenvalue counting function** (contrast with the
bounded-operator `eigCount` of `SpectralCounting.lean`/`SpectralCountingInstance.lean`, which
counts ABOVE a threshold and is finite because its operator is compact): counts `Tp`'s
eigenvalues with norm AT MOST `Lam`, growing as `Lam → ∞`. `‖·‖` stands in for the task's
`Complex.abs`, which does not exist in this vendored Mathlib snapshot (see file header). -/
noncomputable def unboundedEigCount (Lam : ℝ) : ℕ :=
  {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}.ncard

/-- **The direct bijection** (route (a) of the task): the eigenvalue-band-below-`Lam` set is
exactly the image of `{n : ℕ | (n:ℝ) ≤ Lam}` under `Nat.cast : ℕ → ℂ`. -/
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

/-- `{n : ℕ | (n:ℝ) ≤ Lam} = ↑(Finset.range (⌊Lam⌋₊ + 1))` for `0 ≤ Lam` — the same shape of
threshold lemma as `SpectralCountingInstance.InfDim.le_dseq_iff` (§9 of that file), via
`Nat.le_floor_iff`. -/
theorem nat_le_Lam_eq_range {Lam : ℝ} (hLam : 0 ≤ Lam) :
    {n : ℕ | (n : ℝ) ≤ Lam} = ↑(Finset.range (⌊Lam⌋₊ + 1)) := by
  ext n
  simp only [Set.mem_setOf_eq, Finset.coe_range, Set.mem_Iio]
  rw [Nat.lt_add_one_iff, Nat.le_floor_iff hLam]

/-- **THE FALSIFIABLE TARGET, CLOSED.** `unboundedEigCount Lam = ⌊Lam⌋₊ + 1` for every `Lam ≥ 0`
— route (a) from the Onda-3 task statement, direct via `Tp_isEigenvalue` +
`Tp_eigenvalue_mem_range`, bijecting the eigenvalue set with `{n : ℕ | n ≤ Lam}` via `Nat.cast`. -/
theorem unboundedEigCount_eq_floor {Lam : ℝ} (hLam : 0 ≤ Lam) :
    unboundedEigCount Lam = ⌊Lam⌋₊ + 1 := by
  unfold unboundedEigCount
  rw [eigenvalues_below_eq_image, nat_le_Lam_eq_range hLam,
    Set.ncard_image_of_injective _ Nat.cast_injective, Set.ncard_coe_finset, Finset.card_range]

end RH3.UnboundedEigCountFloorLaw

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH3.UnboundedEigCountFloorLaw.Tp_isEigenvalue
#print axioms RH3.UnboundedEigCountFloorLaw.Tp_eigenvalue_mem_range
#print axioms RH3.UnboundedEigCountFloorLaw.eigenvalues_below_eq_image
#print axioms RH3.UnboundedEigCountFloorLaw.nat_le_Lam_eq_range
#print axioms RH3.UnboundedEigCountFloorLaw.unboundedEigCount_eq_floor
