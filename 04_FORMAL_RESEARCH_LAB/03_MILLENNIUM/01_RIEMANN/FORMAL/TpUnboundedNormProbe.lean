/-
  WAVE5-RH-6C — Formally confirm the toy unbounded diagonal `LinearPMap` `Tp` is genuinely
  unbounded, as an operator-norm statement (Onda-5 task RH-6c, plan code `RH-6c`).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-5
  task instructions on build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/Wave-2/Wave-3/Wave-4/
  other-Wave-5 file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`, `e`,
  `e_apply`, `e_ne_zero` exactly as-is.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING `LinearPMapEigenvalueBridge.lean` DIRECTLY
  (the same situation, and the same resolution, as the Wave-3/Wave-4 siblings
  `UnboundedEigCountFloorLaw.lean`, `UnboundedEigCountWeylLimitLaw.lean`,
  `EigenvalueSetBridgeRestricted.lean`, all in this same directory). The Wave-2 shared-infra
  source `LinearPMapEigenvalueBridge.lean`
  (`03_MILLENNIUM/_SHARED_INFRA/FORMAL/LinearPMapEigenvalueBridge.lean`) lives OUTSIDE the
  `05_FORMAL/lean` Lake project root, is itself declared "free-standing: NOT registered in
  `TamesisLab.lean`" in its own header, and has no compiled `.olean` anywhere in
  `.lake/build/lib/lean` (checked directly this session: zero hits for `LinearPMap` under
  `.lake/build`). There is consequently no module import path that resolves to it. Rather than
  fabricate an ad hoc `.olean` placement in the shared, gitignored build cache used concurrently
  by 14 other Wave-5 sessions (a real option per the task instructions for a genuinely MISSING
  dependency, but one this file avoids for the same reason its Wave-3/Wave-4 siblings avoid it),
  this file follows the established sibling convention: it reproduces, BYTE-IDENTICAL, only the
  MINIMAL block actually needed for THIS test — `finiteSupport`, `memℓp_of_finiteSupport`,
  `TpFun`, `Tp`, `Tp_apply`, `e_mem_finiteSupport`, `eDom`, `eDom_coe`, `Tp_eDom` — copied verbatim
  from `LinearPMapEigenvalueBridge.lean` lines 154–300 (§0 "the domain", §1 "the unbounded toy
  diagonal operator `Tp`", §3 "`Tp` has an eigenvector `e i` at every natural number `i`"), under
  a fresh namespace (`RH6C.TpUnboundedNormProbe`) so no name clashes with the original file (which
  this file never touches) nor with any Wave-3/4/5 sibling's own separate reproduction. This file's
  reproduction is DELIBERATELY SMALLER than the Wave-3/Wave-4/Wave-5 siblings': it omits `§2`
  (`IsEigenvalue`) and the theorems `Tp_isEigenvalue`/`Tp_eigenvalue_mem_range`, since the
  falsifiable target below never mentions eigenvalues at all — it is a pure operator-norm
  statement about `Tp` and needs only the domain, the map, and one eigenvector family (`eDom`/
  `Tp_eDom`) as an explicit unboundedness witness. The reproduced block is NOT reproved or
  reinterpreted — every line is copied as-is, including its own original doc comments (some of
  which reference "part (1)"/"part (2) of the task" — that refers to the ORIGINAL Wave-2
  SHARED-2C task, not this file's task; kept verbatim per the copy-exactly instruction rather than
  edited, to avoid any risk of silently introducing a divergence from the cited source during
  transcription).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-5 RH-6c task statement, nothing broader):

  > Provar `¬ (∃ C:ℝ, ∀ x:Tp.domain, ‖(Tp x:H2)‖ ≤ C * ‖(x:H2)‖)` usando `Tp_eDom`,
  > `lp.norm_single`, `norm_smul`, `Complex.norm_natCast` e `exists_nat_gt`. `#print axioms` limpo
  > (3 axiomas padrão).

  WHY THIS TEST IS A GENUINE (NOT COSMETIC) GAP TO CLOSE. Neither the Wave-4 RH-4 file
  (`UnboundedEigCountWeylLimitLaw.lean`) nor the Wave-4 RH-5 file
  (`EigenvalueSetBridgeRestricted.lean`) — nor the underlying Wave-3 RH-3 file
  (`UnboundedEigCountFloorLaw.lean`) — actually PROVES anywhere in their bodies that `Tp` is
  unbounded as an operator; all three merely construct `Tp` as a `LinearPMap` (which carries no
  boundedness/continuity annotation either way) and refer to it in prose as "the unbounded toy
  diagonal operator". This file supplies the missing formal witness: an explicit `#print axioms`
  clean proof that no real constant `C` bounds `‖Tp x‖` by `C * ‖x‖` uniformly over `Tp.domain`.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §2 below — everything before
  §2 is the verbatim reproduction described above).
  * `Tp_unbounded` — **THE FALSIFIABLE TARGET, CLOSED.**
    `¬ ∃ C : ℝ, ∀ x : Tp.domain, ‖(Tp x : H2)‖ ≤ C * ‖(x : H2)‖`, exactly the strategy specified:
    assume such a `C` exists; pick (`exists_nat_gt`) a natural `n` with `C < n`; instantiate the
    hypothesis at `x := eDom n`; rewrite `Tp (eDom n) = (n:ℂ) • e n` (`Tp_eDom`) and
    `(eDom n : H2) = e n` (`eDom_coe`); split the smul norm on the left with `norm_smul`
    (`‖(n:ℂ) • e n‖ = ‖(n:ℂ)‖ * ‖e n‖`); compute `‖e n‖ = 1` directly from `e n = lp.single 2 n 1`
    via `lp.norm_single` (`Mathlib/Analysis/Normed/Lp/lpSpace.lean:1099`) plus `norm_one`; cancel
    the `* 1` on both sides; rewrite `‖(n:ℂ)‖ = (n:ℝ)` via `Complex.norm_natCast`
    (`Mathlib/Analysis/Complex/Norm.lean:113`); this leaves `(n:ℝ) ≤ C`, contradicting `C < n` by
    `linarith`.

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly). This file says nothing about, and
  does not approximate, a solution to the Riemann Hypothesis or any Clay Millennium Prize problem:
  `Tp` remains a hand-built, purely algebraic toy `LinearPMap` on `ℓ²(ℕ,ℂ)` with no topology beyond
  the ambient Hilbert-space norm, no self-adjointness claim, and no connection whatsoever to
  `riemannZeta`/`N_zeta`/any spectral interpretation of the zeta zeros. No mathematical novelty is
  claimed: that a diagonal map `x_n ↦ n·x_n` fails to be norm-bounded on a dense domain of
  finitely-supported sequences, witnessed by the unit basis vectors `e n` alone, is a completely
  elementary, classical fact about unbounded operators.

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

namespace RH6C.TpUnboundedNormProbe

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

/-! ### §1 — the unbounded toy diagonal operator `Tp`, as a `LinearPMap`, plus its `e n`
eigenvector witnesses `eDom n` / `Tp_eDom`.

`Tp` is defined only on `finiteSupport`, and acts as `(Tp x)_i = i * x_i` — the toy unbounded
diagonal operator `T x_n = n * x_n`, distinct from the already-registered bounded diagonal
operator `TamesisLab.Foundations.SpectralCounting.InfDim.T` (opened above simply as `T`).

(Verbatim reproduction of `LinearPMapEigenvalueBridge.lean` §1 and part of §3, lines 191–211 and
225–261 minus the `IsEigenvalue`-specific material this file does not need.) -/

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
`Tp x_n = n * x_n`, unbounded — THE FACT THIS FILE FORMALLY CONFIRMS BELOW (§2), rather than
merely asserting in prose as the Wave-3/Wave-4 siblings do. -/
noncomputable def Tp : H2 →ₗ.[ℂ] H2 := ⟨finiteSupport, TpFun⟩

@[simp] lemma Tp_apply (x : Tp.domain) (i : ℕ) :
    ((Tp x : H2) : ∀ _ : ℕ, ℂ) i = (i : ℂ) * (x : H2) i := rfl

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

/-! ### §2 — NEW (WAVE5-RH-6C): `Tp` is genuinely unbounded, as an operator-norm statement.

This section is NOT a reproduction of anything: it is this file's own new content, the
falsifiable target for WAVE5-RH-6C. No real `C` bounds `‖Tp x‖ ≤ C * ‖x‖` uniformly over
`Tp.domain` — witnessed by the unit basis vectors `e n = eDom n` alone: `‖Tp (eDom n)‖ = n` while
`‖(eDom n : H2)‖ = 1`, and `n` is unbounded (`exists_nat_gt`). -/

/-- `‖e n‖ = 1` for every `n`, directly from `e n = lp.single 2 n 1`
(`SpectralCountingInstance.lean:107`) via `lp.norm_single`
(`Mathlib/Analysis/Normed/Lp/lpSpace.lean:1099`) and `norm_one`. -/
lemma norm_e (n : ℕ) : ‖(e n : H2)‖ = 1 := by
  unfold e
  rw [lp.norm_single (by norm_num : (0 : ℝ≥0∞) < 2)]
  exact norm_one

/-- **THE FALSIFIABLE TARGET, CLOSED.** No real constant `C` bounds `‖Tp x‖ ≤ C * ‖x‖` uniformly
over `Tp.domain` — exactly the strategy the task specifies: assume such a `C`, pick
(`exists_nat_gt`) a natural `n` with `C < n`, instantiate the bound at `x := eDom n`, rewrite via
`Tp_eDom` + `eDom_coe` + `norm_smul` + `norm_e` + `Complex.norm_natCast` to get `(n : ℝ) ≤ C`,
contradicting `C < n`. -/
theorem Tp_unbounded :
    ¬ ∃ C : ℝ, ∀ x : Tp.domain, ‖(Tp x : H2)‖ ≤ C * ‖(x : H2)‖ := by
  rintro ⟨C, hC⟩
  obtain ⟨n, hn⟩ := exists_nat_gt C
  have h := hC (eDom n)
  rw [Tp_eDom, eDom_coe, norm_smul, norm_e, mul_one, mul_one, Complex.norm_natCast] at h
  linarith

end RH6C.TpUnboundedNormProbe

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH6C.TpUnboundedNormProbe.norm_e
#print axioms RH6C.TpUnboundedNormProbe.Tp_unbounded
