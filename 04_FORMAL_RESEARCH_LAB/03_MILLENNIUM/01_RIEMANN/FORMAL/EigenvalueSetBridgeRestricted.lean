/-
  WAVE4-RH-5 — Route-b set bridge (revised): eigenvalue set equality via `eigenvalue_bridge`,
  transport lemma RESTRICTED to `mu = (n:C)`, `n:N` (Onda-4 task RH-5).

  STATUS: drafted and self-checked with `lake env lean` by the authoring session (single-file
  typecheck against the existing built Mathlib cache, NOT a full `lake build` — see the Wave-4
  task instructions on build contention with 14 concurrent sibling agents). Free-standing: NOT
  registered in `TamesisLab.lean`, and this file does not modify any Wave-1/Wave-2/Wave-3/other-
  Wave-4 file. It only *imports* (read-only) the registered Wave-1 module
  `TamesisLab.Foundations.SpectralCountingInstance`
  (`05_FORMAL/lean/TamesisLab/Foundations/SpectralCountingInstance.lean`), reusing its `H2`,
  `dseq`, `e`, `T`, `hasEigenvalue_T`, `eigenvalue_mem_range`, `exists_ne_zero_coord` exactly as-is.

  WHY THIS FILE REPRODUCES RATHER THAN `import`-ING `LinearPMapEigenvalueBridge.lean` DIRECTLY
  (the same situation, and the same resolution, as the Wave-3 sibling
  `UnboundedEigCountFloorLaw.lean`, same directory). The Wave-2 shared-infra source
  `LinearPMapEigenvalueBridge.lean` (`03_MILLENNIUM/_SHARED_INFRA/FORMAL/
  LinearPMapEigenvalueBridge.lean`) lives OUTSIDE the `05_FORMAL/lean` Lake project root, is
  itself declared "free-standing: NOT registered in `TamesisLab.lean`" in its own header, and has
  no compiled `.olean` anywhere in `.lake/build/lib/lean` (checked directly this session: zero
  hits for `LinearPMap` under `.lake/build`). There is consequently no module import path that
  resolves to it. Rather than fabricate an ad hoc `.olean` placement in the shared, gitignored
  build cache (a real option per the Wave-4 task instructions for a genuinely MISSING dependency,
  but one this file avoids to minimize any chance of interfering with the 14 other concurrent
  sessions writing into the same cache directory), this file follows the established sibling
  convention set by `UnboundedEigCountFloorLaw.lean` (Wave-3 RH-3, same directory): it reproduces,
  BYTE-IDENTICAL, the block of `LinearPMapEigenvalueBridge.lean` needed for this test — the
  definitions `finiteSupport`, `memℓp_of_finiteSupport`, `TpFun`, `Tp`, `Tp_apply`, `IsEigenvalue`,
  `e_mem_finiteSupport`, `eDom`, `eDom_coe`, `Tp_eDom`, and the theorems `Tp_isEigenvalue`,
  `Tp_eigenvalue_mem_range`, `eigenvalue_bridge` — copied verbatim from
  `LinearPMapEigenvalueBridge.lean` lines 154–300 (§0 "the domain", §1 "the unbounded toy diagonal
  operator `Tp`", §2 "the falsifiable target: eigenvalue characterization", §3 "`Tp` has an
  eigenvector `e i` at every natural number `i`", §4 "THE BRIDGE"), under a fresh namespace
  (`RH5.EigenvalueSetBridgeRestricted`) so no name clashes with the original file (which this file
  never touches) nor with the Wave-3 sibling's own separate reproduction (a different namespace,
  `RH3.UnboundedEigCountFloorLaw`). The reproduced block is NOT reproved or reinterpreted — every
  line is copied as-is, including its own original doc comments (some of which reference "part
  (1)"/"part (2) of the task" — that refers to the ORIGINAL Wave-2 SHARED-2C task, not this file's
  task; kept verbatim per the copy-exactly instruction rather than edited).

  THE FALSIFIABLE TEST ATTEMPTED (exactly the Wave-4 RH-5 task statement, nothing broader — in
  particular, NOT the unconditional version, which the task itself flags as FALSE, counterexample
  `mu = i`, `Lam = 0.5`):

  > Para `Lam ≥ 0`, provar
  >   `{mu : C | IsEigenvalue Tp mu ∧ ‖mu‖ ≤ Lam}`
  >     `= (fun mu => (mu+1)⁻¹) ⁻¹' {nu : C | Module.End.HasEigenvalue T nu ∧ (Lam+1)⁻¹ ≤ ‖nu‖}`,
  > construído ponto a ponto via `eigenvalue_bridge` composto com o lema de transporte RESTRITO a
  > `mu = (n:C)`, `n:N`:
  >   `∀ n:N, (n:R) ≤ Lam ↔ (Lam+1)⁻¹ ≤ ‖((n:C)+1)⁻¹‖`
  > (via `norm_inv` + `Complex.norm_natCast` + a real inverse-monotonicity lemma).

  WHY THE RESTRICTED TRANSPORT LEMMA IS ENOUGH (this is the whole point of route-b "revised",
  distinguishing it from the abandoned unconditional attempt). The transport lemma
  `eig_norm_transport_nat` below is proved ONLY for `mu` of the form `(n:C)`, `n:N` — it is
  actually FALSE for general `mu:C` (task's own counterexample: `mu = i`, `Lam = 0.5`; `‖i‖ = 1 >
  0.5 = Lam`, yet `‖(i+1)⁻¹‖ = 1/√2 ≈ 0.707 ≥ (0.5+1)⁻¹ = 2/3 ≈ 0.667`, so the "‖mu‖ ≤ Lam ↔
  (Lam+1)⁻¹ ≤ ‖(mu+1)⁻¹‖" implication fails at `mu=i`: RHS holds, LHS does not). But this
  restricted domain is exactly ALL that the set-equality proof ever needs: on the LHS of the
  target equality, `IsEigenvalue Tp mu` already forces `mu = (n:C)` for some `n:N`
  (`Tp_eigenvalue_mem_range`); on the RHS, `Module.End.HasEigenvalue T (mu+1)⁻¹` combined with
  `eigenvalue_bridge` ALSO forces `IsEigenvalue Tp mu`, hence again `mu = (n:C)`. So both
  directions of the set-equality proof reduce, before ever invoking the norm transport, to the
  case `mu = (n:C)` — exactly the domain on which the restricted lemma holds. `eigenvalue_bridge`
  itself (the `IsEigenvalue Tp mu ↔ HasEigenvalue T (mu+1)⁻¹` biconditional) IS unconditional in
  `mu` and is reused as-is; only the NORM half of the target biconditional needs restricting.

  WHAT WAS ACTUALLY BUILT, PRECISELY (the NEW content of this file, §5 below — everything before
  §5 is the verbatim reproduction described above).
  * `eig_norm_transport_nat (Lam : R) (hLam : 0 ≤ Lam) (n : N) : (n:R) ≤ Lam ↔ (Lam+1)⁻¹ ≤
    ‖((n:C)+1)⁻¹‖` — THE RESTRICTED TRANSPORT LEMMA, exactly as specified: `((n:C)+1) =
    ((n+1:N):C)` by `push_cast`, then `norm_inv` (`‖a⁻¹‖ = ‖a‖⁻¹`,
    `Mathlib/Analysis/Normed/Field/Basic.lean:77`) + `Complex.norm_natCast` (`‖(n:C)‖ = n`,
    `Mathlib/Analysis/Complex/Norm.lean:113`) turn the goal into a purely real inequality between
    inverses, closed by `inv_le_inv₀` (`Mathlib/Algebra/Order/GroupWithZero/Basic.lean:1218`,
    `0 < a → 0 < b → (a⁻¹ ≤ b⁻¹ ↔ b ≤ a)`) plus `linarith`/`positivity` for the positivity side
    conditions (`Lam + 1 > 0` from `hLam : 0 ≤ Lam`; `(n:R) + 1 > 0` from `n.cast_nonneg`).
  * `eigenvalue_set_eq_preimage` — **THE FALSIFIABLE TARGET, CLOSED.** The set equality exactly as
    stated, proved pointwise (`ext mu`) in two symmetric halves, each reducing `mu` to `(n:C)` via
    `Tp_eigenvalue_mem_range` (forward: directly from the membership hypothesis; backward: from
    `eigenvalue_bridge.mpr` applied to the `HasEigenvalue` hypothesis) before combining
    `eigenvalue_bridge` (for the `IsEigenvalue`/`HasEigenvalue` half) with
    `eig_norm_transport_nat` (for the norm half).

  WHAT THIS FILE DOES NOT DO / STILL MISSING (stated honestly, matching Wave-4 instructions). The
  unconditional version of the transport lemma (`∀ mu:C, ‖mu‖ ≤ Lam ↔ (Lam+1)⁻¹ ≤ ‖(mu+1)⁻¹‖`) is
  NOT attempted, is NOT true, and is explicitly not needed — see above. This file says nothing
  about, and does not approximate, a solution to the Riemann Hypothesis or any Clay Millennium
  Prize problem: `Tp` remains a hand-built, purely algebraic toy `LinearPMap` on `ℓ²(N,C)` with no
  topology, no self-adjointness claim, and no connection whatsoever to `riemannZeta`/`N_zeta`/any
  spectral interpretation of the zeta zeros. No mathematical novelty is claimed: relating two
  elementary real-number inequalities about `n ≤ Lam` versus `1/(Lam+1) ≤ 1/(n+1)` through a toy
  operator's eigenvalue set is a completely classical, elementary observation.

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

namespace RH5.EigenvalueSetBridgeRestricted

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

/-- **The falsifiable eigenvalue predicate for a `LinearPMap`** (part (1) of the original task). -/
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
not reproduced, for `R`'s own side of the bridge theorem below; `Tp`'s analogous fact is proved
fresh here since `Tp` itself is new). -/
theorem Tp_eigenvalue_mem_range {mu : ℂ} (h : IsEigenvalue Tp mu) : ∃ n : ℕ, mu = (n : ℂ) := by
  obtain ⟨v, hv0, hveq⟩ := h
  obtain ⟨i, hi⟩ := exists_ne_zero_coord hv0
  refine ⟨i, ?_⟩
  have hcoord := congrArg (fun g : H2 => (g : ∀ _ : ℕ, ℂ) i) hveq
  simp only [Tp_apply, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul] at hcoord
  exact (mul_right_cancel₀ hi hcoord).symm

/-! ### §4 — THE BRIDGE: connecting `IsEigenvalue Tp mu` (the unbounded `LinearPMap`) BY HAND to
`Module.End.HasEigenvalue` of the bounded operator `R := InfDim.T`. `R`'s diagonal `1/(n+1)` is
the explicit inverse-shift of `Tp`'s diagonal `n`: on the shared eigenvector `e n`,
`(Tp + 1) (e n) = (n + 1) • e n` while `R (e n) = (1/(n+1)) • e n`.

(Verbatim reproduction of `LinearPMapEigenvalueBridge.lean` §4, lines 268–300.) -/

/-- **`eigenvalue_bridge`.** `mu` is an eigenvalue of the unbounded toy `LinearPMap` `Tp` iff
`(mu + 1)⁻¹` is an eigenvalue (in the `Module.End.HasEigenvalue` sense) of the bounded operator
`R := InfDim.T` (`TamesisLab.Foundations.SpectralCounting.InfDim.T`, opened above as `T`), i.e.
the explicit diagonal operator `1/(n+1)` already registered in the lab. No side condition on `mu`
is needed: both sides are automatically false at the ℂ-inverse junk value `mu = -1` (there
`(mu+1)⁻¹ = 0`, and `0` is never one of `Tp`'s or `R`'s eigenvalues — every eigenvalue of `Tp` is
a nonneg integer cast, and every eigenvalue of `R` is `dseq i = 1/(i+1) ≠ 0`), so the `↔` holds
unconditionally, though the two "always false at `mu = -1`" side facts are not separately proved
here — only the `↔` itself, which does not need them. -/
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

/-! ### §5 — NEW (WAVE4-RH-5): the restricted transport lemma and the eigenvalue-set bridge

This section is NOT a reproduction of anything: it is this file's own new content, the
falsifiable target for WAVE4-RH-5. -/

/-- **The restricted transport lemma** (deliberately restricted to `mu = (n:ℂ)`, `n:ℕ` — the
UNRESTRICTED version, `∀ mu:ℂ, ‖mu‖ ≤ Lam ↔ (Lam+1)⁻¹ ≤ ‖(mu+1)⁻¹‖`, is FALSE: counterexample
`mu = i`, `Lam = 0.5`, see file header). For `Lam ≥ 0` and `n : ℕ`, `(n:ℝ) ≤ Lam` iff
`(Lam+1)⁻¹ ≤ ‖((n:ℂ)+1)⁻¹‖`. -/
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

/-- **THE FALSIFIABLE TARGET, CLOSED.** For `Lam ≥ 0`, the `Tp`-eigenvalue band `{mu | IsEigenvalue
Tp mu ∧ ‖mu‖ ≤ Lam}` equals the preimage, under `mu ↦ (mu+1)⁻¹`, of the `R`-eigenvalue band
`{nu | HasEigenvalue T nu ∧ (Lam+1)⁻¹ ≤ ‖nu‖}` — built pointwise via `eigenvalue_bridge` composed
with `eig_norm_transport_nat`, exactly as the task specifies (route-b "revised": the restricted
transport lemma suffices because `IsEigenvalue Tp mu`, on either side of the biconditional
`eigenvalue_bridge`, already forces `mu = (n:ℂ)` for some `n:ℕ` via `Tp_eigenvalue_mem_range` —
see file header for why this makes the restricted lemma enough). -/
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

end RH5.EigenvalueSetBridgeRestricted

/-! ### Axiom audit (verification-protocol requirement, not part of the mathematical content).
Confirms every new declaration above depends only on the standard three Lean/Mathlib axioms. -/

#print axioms RH5.EigenvalueSetBridgeRestricted.Tp_isEigenvalue
#print axioms RH5.EigenvalueSetBridgeRestricted.Tp_eigenvalue_mem_range
#print axioms RH5.EigenvalueSetBridgeRestricted.eigenvalue_bridge
#print axioms RH5.EigenvalueSetBridgeRestricted.eig_norm_transport_nat
#print axioms RH5.EigenvalueSetBridgeRestricted.eigenvalue_set_eq_preimage
