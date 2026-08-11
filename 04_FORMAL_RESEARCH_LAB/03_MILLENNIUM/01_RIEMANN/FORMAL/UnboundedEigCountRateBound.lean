/-
  WAVE5-RH-6A — Non-asymptotic rate bound for the Weyl-type limit law of `unboundedEigCount`:
  for `Lam > 0`, `0 < (unboundedEigCount Lam : R)/Lam - 1` AND
  `(unboundedEigCount Lam : R)/Lam - 1 ≤ 1/Lam` (Onda-5 task RH-6a).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-5
  task instructions on build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/Wave-2/Wave-3/Wave-4/
  other-Wave-5 file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`, `e`,
  `e_apply`, `e_ne_zero` exactly as-is.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING `UnboundedEigCountFloorLaw.lean` DIRECTLY.
  The task instructions ask this file to build directly on `unboundedEigCount_eq_floor`, exactly
  as reused by the Wave-3/Wave-4 siblings `UnboundedEigCountFloorLaw.lean` (WAVE3-RH-3) and
  `UnboundedEigCountWeylLimitLaw.lean` (WAVE4-RH-4), same directory,
  `03_MILLENNIUM/01_RIEMANN/FORMAL/`. Those files live OUTSIDE the `05_FORMAL/lean` Lake project
  root, are themselves declared "free-standing: NOT registered in `TamesisLab.lean`" in their own
  headers, and have no compiled `.olean` anywhere in `.lake/build/lib/lean` (checked directly this
  session: zero hits for `UnboundedEigCount` under `.lake/build`). There is consequently no module
  import path that resolves to them. Rather than fabricate an ad hoc `.olean` placement in the
  shared, gitignored build cache used concurrently by 14 other Wave-5 sessions (a real option per
  the task instructions for a genuinely MISSING dependency, but one this file avoids to minimize
  any chance of interfering with those sessions writing into the same cache directory — the same
  reasoning the Wave-3/Wave-4 siblings themselves give for avoiding it, in their own headers),
  this file follows the established sibling convention set by `UnboundedEigCountWeylLimitLaw.lean`
  (Wave-4 RH-4, same directory) for exactly this situation: it reproduces, BYTE-IDENTICAL, the
  minimal self-contained block needed — everything through `unboundedEigCount_eq_floor` — copied
  verbatim from `UnboundedEigCountFloorLaw.lean` lines 118–280 (§0 "the domain", §1 "the unbounded
  toy diagonal operator `Tp`", §2 "the falsifiable target: eigenvalue characterization", §3 "`Tp`
  has an eigenvector `e i` at every natural number `i`", §4 "the unbounded eigenvalue counting
  function and its floor law"), under a fresh namespace (`RH6A.UnboundedEigCountRateBound`) so no
  name clashes with the original file (which this file never touches) nor with the Wave-3/Wave-4
  siblings' own separate reproductions. The reproduced block is NOT reproved or reinterpreted —
  every line is copied as-is, including its own original doc comments (some of which reference
  "the task"/"route (a)" — that refers to the ORIGINAL Wave-3 RH-3 task, not this file's task;
  kept verbatim per the copy-exactly instruction rather than edited, to avoid any risk of silently
  introducing a divergence from the cited source during transcription).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-5 RH-6a task statement, nothing broader):

  > Para Lam>=1 (ou Lam>0), provar `0 < (unboundedEigCount Lam : R)/Lam - 1` /\
  > `(unboundedEigCount Lam : R)/Lam - 1 <= 1/Lam`, diretamente de `unboundedEigCount_eq_floor` +
  > `Nat.floor_le` + `Nat.lt_floor_add_one`. `#print axioms` limpo.

  This file takes the weaker, still-sufficient hypothesis `Lam > 0` (the task's own parenthetical
  alternative to `Lam ≥ 1`) — the proof below never actually needs `Lam ≥ 1`, only `Lam > 0`
  (for `Nat.floor_le` — which itself only needs `0 ≤ Lam` — and to divide by `Lam` at all).

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §5 below — everything before
  §5 is the verbatim reproduction described above).
  * `unboundedEigCount_rate_bound` — **THE FALSIFIABLE TARGET, CLOSED.** For `Lam > 0`,
    `0 < (unboundedEigCount Lam : ℝ)/Lam - 1 ∧ (unboundedEigCount Lam : ℝ)/Lam - 1 ≤ 1/Lam`,
    exactly the strategy specified: `unboundedEigCount_eq_floor` (cast to `ℝ`) rewrites
    `unboundedEigCount Lam` as `⌊Lam⌋₊ + 1`; `div_sub_one` turns `(⌊Lam⌋₊+1)/Lam - 1` into
    `(⌊Lam⌋₊+1-Lam)/Lam`; then the strict lower bound is `div_pos` fed by `Nat.lt_floor_add_one`
    (`Lam < ⌊Lam⌋₊ + 1`, giving a positive numerator), and the upper bound is
    `div_le_div_of_nonneg_right` fed by `Nat.floor_le` (`⌊Lam⌋₊ ≤ Lam`, giving numerator `≤ 1`)
    against the shared denominator `Lam`.

    Mathematically this is the familiar non-asymptotic sandwich `⌊Lam⌋₊ ≤ Lam < ⌊Lam⌋₊ + 1`
    (`Nat.floor_le` / `Nat.lt_floor_add_one`) divided through by `Lam > 0` and re-centered at `1`:
    it makes the WAVE4-RH-4 limit `(unboundedEigCount Lam : ℝ)/Lam → 1` quantitative with an
    explicit, elementary `O(1/Lam)` two-sided error bound, valid for EVERY `Lam > 0` (not just
    asymptotically), rather than adding any new information about `unboundedEigCount` itself.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly). Nothing here says anything about,
  or approximates, a solution to the Riemann Hypothesis or any Clay Millennium Prize problem: `Tp`
  remains a hand-built, purely algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)` with no topology, no
  self-adjointness claim, and no connection whatsoever to `riemannZeta`/`N_zeta`/any spectral
  interpretation of the zeta zeros. No mathematical novelty is claimed: the bound
  `⌊Lam⌋₊ ≤ Lam < ⌊Lam⌋₊ + 1` is the elementary defining property of `Nat.floor` itself
  (`Nat.floor_le`/`Nat.lt_floor_add_one`, both already in Mathlib) — this file merely divides that
  classical two-sided inequality through by `Lam > 0` and transports it, via the WAVE3-RH-3 floor
  law, to a statement about a toy operator's eigenvalue-counting function.

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

namespace RH6A.UnboundedEigCountRateBound

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
plays the role of `R` in the Wave-2/Wave-3/Wave-4 sibling files.

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

/-! ### §5 — NEW (WAVE5-RH-6A): the non-asymptotic rate bound

This section is NOT a reproduction of anything: it is this file's own new content, the
falsifiable target for WAVE5-RH-6A. The WAVE4-RH-4 sibling proved the asymptotic limit
`unboundedEigCount Lam / Lam → 1` as `Lam → ∞`; this file instead makes that limit QUANTITATIVE:
for every `Lam > 0` (not merely eventually), the ratio `unboundedEigCount Lam / Lam` overshoots
`1` by a strictly positive amount that is at most `1 / Lam`. The whole content is the classical
floor sandwich `⌊Lam⌋₊ ≤ Lam < ⌊Lam⌋₊ + 1` (`Nat.floor_le` / `Nat.lt_floor_add_one`), transported
through `unboundedEigCount_eq_floor` and divided by `Lam`. -/

/-- **THE FALSIFIABLE TARGET, CLOSED.** For `Lam > 0`, the ratio `unboundedEigCount Lam / Lam`
lies strictly above `1`, and exceeds it by at most `1 / Lam` — a two-sided, non-asymptotic rate
bound for the WAVE4-RH-4 Weyl-type limit law, valid at every positive `Lam`, not just eventually.
Direct from `unboundedEigCount_eq_floor` (cast to `ℝ`), `Nat.floor_le`, and
`Nat.lt_floor_add_one`, exactly as the task specifies. -/
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

end RH6A.UnboundedEigCountRateBound

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH6A.UnboundedEigCountRateBound.Tp_isEigenvalue
#print axioms RH6A.UnboundedEigCountRateBound.Tp_eigenvalue_mem_range
#print axioms RH6A.UnboundedEigCountRateBound.eigenvalues_below_eq_image
#print axioms RH6A.UnboundedEigCountRateBound.nat_le_Lam_eq_range
#print axioms RH6A.UnboundedEigCountRateBound.unboundedEigCount_eq_floor
#print axioms RH6A.UnboundedEigCountRateBound.unboundedEigCount_rate_bound
