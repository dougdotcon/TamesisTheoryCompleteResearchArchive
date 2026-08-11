/-
  WAVE4-RH-4 — Weyl-type limit law for the unbounded eigenvalue counting function:
  `Tendsto (fun Lam => (unboundedEigCount Lam : ℝ) / Lam) atTop (nhds 1)` (Onda-4 task RH-4).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-4
  task instructions on build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/Wave-2/Wave-3/other-
  Wave-4 file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`, `e`,
  `e_apply`, `e_ne_zero` exactly as-is.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING `UnboundedEigCountFloorLaw.lean` DIRECTLY.
  The task instructions ask this file to reuse `unboundedEigCount` /
  `unboundedEigCount_eq_floor` "exactly" from the WAVE3-RH-3 output file
  `UnboundedEigCountFloorLaw.lean` (same directory, `03_MILLENNIUM/01_RIEMANN/FORMAL/`). That file
  lives OUTSIDE the `05_FORMAL/lean` Lake project root, is itself declared "free-standing: NOT
  registered in `TamesisLab.lean`" in its own header, and has no compiled `.olean` anywhere in
  `.lake/build/lib/lean` (checked directly this session: zero hits for `UnboundedEigCount` under
  `.lake/build`). There is consequently no module import path that resolves to it. Rather than
  fabricate an ad hoc `.olean` placement in the shared, gitignored build cache used concurrently
  by 14 other Wave-4 sessions (a real option per the task instructions for a genuinely MISSING
  dependency, but one this file avoids to minimize any chance of interfering with those sessions
  writing into the same cache directory — the same reasoning `UnboundedEigCountFloorLaw.lean`
  itself gives for avoiding it, in its own header), this file follows the established sibling
  convention set by `UnboundedEigCountFloorLaw.lean` (Wave-3 RH-3, same directory) for exactly
  this situation: it reproduces, BYTE-IDENTICAL, the minimal self-contained block needed —
  everything through `unboundedEigCount_eq_floor` — copied verbatim from
  `UnboundedEigCountFloorLaw.lean` lines 118–280 (§0 "the domain", §1 "the unbounded toy diagonal
  operator `Tp`", §2 "the falsifiable target: eigenvalue characterization", §3 "`Tp` has an
  eigenvector `e i` at every natural number `i`", §4 "the unbounded eigenvalue counting function
  and its floor law"), under a fresh namespace (`RH4.UnboundedEigCountWeylLimitLaw`) so no name
  clashes with the original file (which this file never touches). The reproduced block is NOT
  reproved or reinterpreted — every line is copied as-is, including its own original doc comments
  (some of which reference "the task"/"route (a)" — that refers to the ORIGINAL Wave-3 RH-3 task,
  not this file's task; kept verbatim per the copy-exactly instruction rather than edited, to
  avoid any risk of silently introducing a divergence from the cited source during transcription).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-4 RH-4 task statement, nothing broader):

  > Provar `Tendsto (fun Lam => (unboundedEigCount Lam : R)/Lam) atTop (nhds 1)`, via
  > `unboundedEigCount_eq_floor` (congr'ado eventualmente em `Lam >= 0` via `eventually_ge_atTop`),
  > reescrito como `(floor Lam + 1)/Lam = floor Lam/Lam + 1/Lam`, fechando com `Tendsto.add`
  > contra `tendsto_nat_floor_div_atTop` (limite 1) e `tendsto_inv_atTop_zero` (limite 0).
  > `#print axioms` só com os 3 axiomas padrão.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §5 below — everything before
  §5 is the verbatim reproduction described above).
  * `unboundedEigCount_eventually_eq_floor_add_one_div` — the eventual (`Lam ≥ 0`, via
    `Filter.eventually_ge_atTop`) rewrite `(unboundedEigCount Lam : ℝ) / Lam
    = (⌊Lam⌋₊ : ℝ) / Lam + 1 / Lam`, obtained from `unboundedEigCount_eq_floor` by casting the
    `ℕ`-equation `unboundedEigCount Lam = ⌊Lam⌋₊ + 1` to `ℝ` (`push_cast`) and splitting the
    resulting fraction with `add_div`.
  * `unboundedEigCount_weyl_limit` — **THE FALSIFIABLE TARGET, CLOSED.**
    `Tendsto (fun Lam : ℝ => (unboundedEigCount Lam : ℝ) / Lam) atTop (nhds 1)`, exactly the
    strategy specified: `Tendsto.add` combines `tendsto_nat_floor_div_atTop`
    (`Mathlib/Analysis/SpecificLimits/Basic.lean:739`, `Tendsto (fun x ↦ (⌊x⌋₊ : R) / x) atTop
    (𝓝 1)`) with `tendsto_inv_atTop_zero`
    (`Mathlib/Topology/Algebra/Order/Field.lean:74`, `Tendsto (fun r : 𝕜 => r⁻¹) atTop (𝓝 0)`,
    rewritten to the `1 / Lam` shape via `one_div`) to get `Tendsto (fun Lam => (⌊Lam⌋₊:ℝ)/Lam +
    1/Lam) atTop (nhds (1+0))`, `nhds (1+0)` normalized to `nhds 1` by `simpa`, then
    `Filter.Tendsto.congr'` transports this along the eventual equality above to the actual goal
    about `unboundedEigCount`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly). Nothing here says anything about,
  or approximates, a solution to the Riemann Hypothesis or any Clay Millennium Prize problem: `Tp`
  remains a hand-built, purely algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)` with no topology, no
  self-adjointness claim, and no connection whatsoever to `riemannZeta`/`N_zeta`/any spectral
  interpretation of the zeta zeros. No mathematical novelty is claimed: the asymptotic
  `(⌊Lam⌋₊ + 1)/Lam → 1` as `Lam → ∞` is an elementary, classical fact about the naturals — indeed
  already available verbatim as `tendsto_nat_floor_div_atTop` in Mathlib — merely transported here
  through a toy operator's eigenvalue-counting function via the WAVE3-RH-3 floor law.

  Every Mathlib name used below was checked by direct read/grep against the vendored snapshot at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`, in addition to compiling cleanly
  via `lake env lean` (see the file's own build log for the exact command/exit code, reported
  alongside this file).
-/
import Mathlib
import TamesisLab.Foundations.SpectralCountingInstance

open scoped ENNReal lp InnerProductSpace
open Filter Topology
open TamesisLab.Foundations.SpectralCounting.InfDim

namespace RH4.UnboundedEigCountWeylLimitLaw

/-! ### §0 — the domain: finitely-supported vectors of `H2`

`H2 := TamesisLab.Foundations.SpectralCounting.InfDim.H2 = ℓ²(ℕ, ℂ)`, opened above (read-only
import), the SAME ambient Hilbert space already used by the registered bounded operator `R`.

(Verbatim reproduction of `UnboundedEigCountFloorLaw.lean` §0, lines 118–146 — see file header
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
plays the role of `R` in the Wave-2/Wave-3 sibling files.

(Verbatim reproduction of `UnboundedEigCountFloorLaw.lean` §1, lines 157–177.) -/

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

(Verbatim reproduction of `UnboundedEigCountFloorLaw.lean` §2, lines 186–188.) -/

/-- **The falsifiable eigenvalue predicate for a `LinearPMap`.** -/
def IsEigenvalue (T : H2 →ₗ.[ℂ] H2) (mu : ℂ) : Prop :=
  ∃ v : T.domain, (v : H2) ≠ 0 ∧ T v = mu • (v : H2)

/-! ### §3 — `Tp` has an eigenvector `e i` at every natural number `i`, matching `R`'s own
`e i` eigenvector for `dseq i` in `InfDim` (imported, read-only).

(Verbatim reproduction of `UnboundedEigCountFloorLaw.lean` §3, lines 195–231.) -/

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

/-! ### §4 — the unbounded eigenvalue counting function and its floor law (WAVE3-RH-3, reused
by name in this file's own falsifiable test).

(Verbatim reproduction of `UnboundedEigCountFloorLaw.lean` §4, lines 245–280.) -/

/-- **The unbounded-operator-style eigenvalue counting function** (contrast with the
bounded-operator `eigCount` of `SpectralCounting.lean`/`SpectralCountingInstance.lean`, which
counts ABOVE a threshold and is finite because its operator is compact): counts `Tp`'s
eigenvalues with norm AT MOST `Lam`, growing as `Lam → ∞`. `‖·‖` stands in for `Complex.abs`,
which does not exist in this vendored Mathlib snapshot. -/
noncomputable def unboundedEigCount (Lam : ℝ) : ℕ :=
  {mu : ℂ | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}.ncard

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
point for this file's own falsifiable target below. `unboundedEigCount Lam = ⌊Lam⌋₊ + 1` for
every `Lam ≥ 0`. -/
theorem unboundedEigCount_eq_floor {Lam : ℝ} (hLam : 0 ≤ Lam) :
    unboundedEigCount Lam = ⌊Lam⌋₊ + 1 := by
  unfold unboundedEigCount
  rw [eigenvalues_below_eq_image, nat_le_Lam_eq_range hLam,
    Set.ncard_image_of_injective _ Nat.cast_injective, Set.ncard_coe_finset, Finset.card_range]

/-! ### §5 — NEW (WAVE4-RH-4): the Weyl-type limit law

This section is NOT a reproduction of anything: it is this file's own new content, the
falsifiable target for WAVE4-RH-4. `unboundedEigCount Lam / Lam → 1` as `Lam → ∞`, since
`unboundedEigCount Lam = ⌊Lam⌋₊ + 1` eventually (`Lam ≥ 0`), and `(⌊Lam⌋₊ + 1)/Lam
= ⌊Lam⌋₊/Lam + 1/Lam → 1 + 0 = 1`. -/

/-- **Eventual rewrite** (the exact strategy specified by the task): for `Lam ≥ 0`,
`(unboundedEigCount Lam : ℝ) / Lam = (⌊Lam⌋₊ : ℝ) / Lam + 1 / Lam`, via
`unboundedEigCount_eq_floor` cast to `ℝ` and split with `add_div`. -/
theorem unboundedEigCount_eventually_eq_floor_add_one_div :
    (fun Lam : ℝ => (⌊Lam⌋₊ : ℝ) / Lam + 1 / Lam)
      =ᶠ[atTop] (fun Lam : ℝ => (unboundedEigCount Lam : ℝ) / Lam) := by
  filter_upwards [eventually_ge_atTop (0 : ℝ)] with Lam hLam
  show (⌊Lam⌋₊ : ℝ) / Lam + 1 / Lam = (unboundedEigCount Lam : ℝ) / Lam
  rw [unboundedEigCount_eq_floor hLam]
  push_cast
  rw [add_div]

/-- **THE FALSIFIABLE TARGET, CLOSED.** `Tendsto (fun Lam => (unboundedEigCount Lam : ℝ) / Lam)
atTop (nhds 1)` — exactly the strategy the task specifies: `unboundedEigCount_eq_floor`,
congr'd eventually in `Lam ≥ 0` via `eventually_ge_atTop`, rewritten as `⌊Lam⌋₊/Lam + 1/Lam`,
closed with `Tendsto.add` against `tendsto_nat_floor_div_atTop` (limit `1`) and
`tendsto_inv_atTop_zero` (limit `0`). -/
theorem unboundedEigCount_weyl_limit :
    Tendsto (fun Lam : ℝ => (unboundedEigCount Lam : ℝ) / Lam) atTop (nhds 1) := by
  have h1 : Tendsto (fun Lam : ℝ => (⌊Lam⌋₊ : ℝ) / Lam) atTop (nhds 1) :=
    tendsto_nat_floor_div_atTop
  have h2 : Tendsto (fun Lam : ℝ => (1 : ℝ) / Lam) atTop (nhds 0) := by
    simpa [one_div] using (tendsto_inv_atTop_zero (𝕜 := ℝ))
  have hSum : Tendsto (fun Lam : ℝ => (⌊Lam⌋₊ : ℝ) / Lam + 1 / Lam) atTop (nhds 1) := by
    simpa using h1.add h2
  exact hSum.congr' unboundedEigCount_eventually_eq_floor_add_one_div

end RH4.UnboundedEigCountWeylLimitLaw

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH4.UnboundedEigCountWeylLimitLaw.Tp_isEigenvalue
#print axioms RH4.UnboundedEigCountWeylLimitLaw.Tp_eigenvalue_mem_range
#print axioms RH4.UnboundedEigCountWeylLimitLaw.eigenvalues_below_eq_image
#print axioms RH4.UnboundedEigCountWeylLimitLaw.nat_le_Lam_eq_range
#print axioms RH4.UnboundedEigCountWeylLimitLaw.unboundedEigCount_eq_floor
#print axioms RH4.UnboundedEigCountWeylLimitLaw.unboundedEigCount_eventually_eq_floor_add_one_div
#print axioms RH4.UnboundedEigCountWeylLimitLaw.unboundedEigCount_weyl_limit
