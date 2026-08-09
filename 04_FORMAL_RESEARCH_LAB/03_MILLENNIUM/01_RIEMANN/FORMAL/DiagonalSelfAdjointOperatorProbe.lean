/-
RH-3 — standalone draft, NOT integrated into `TamesisLab.lean` or any shared aggregator.
Follows the same convention as `DirichletOscillatoryIntegral.lean`
(02_FOUNDATIONS/21_DIRICHLET_OSCILLATORY_INTEGRAL/) and
`CalderonZygmundKernelDefinitions.lean` (03_MILLENNIUM/02_NAVIER_STOKES/FORMAL/): a
self-contained Lean file, verified directly via `lake env lean` against the same
vendored Mathlib, outside the shared import tree. This file is a Wave-1 formal
reconnaissance item, not a natural extension of the `TamesisLab.RHNogo.*` chain
(it shares no definitions with `AsymptoticCore`/`Bridge`/`Geometry`/`Composition`
and does not touch the counting-law / abstract-composition no-go argument at all),
so it does not follow that chain's registered-module convention.

## What this file is

A single, narrow, falsifiable formal test of REACT-001 from
`03_MILLENNIUM/01_RIEMANN/RH_NOGO_REACTIVATION_CRITERIA.md`:

> Uma biblioteca Lean fornecer infraestrutura adequada para operadores auto-adjuntos
> NAO LIMITADOS e resolvente compacto. Verification required: localizar a API,
> compilar um exemplo minimo contra a revisao fixada e registrar os nomes dos
> teoremas.

Mathlib (pinned `v4.33.0-rc1`, see `05_FORMAL/lean/lakefile.toml`) carries genuine
definitional infrastructure for unbounded operators via `LinearPMap`
(`Mathlib/Topology/Algebra/Module/LinearPMap.lean`: `IsClosed`, `IsClosable`,
`closure`, `HasCore`, citing Weidmann's *Linear Operators in Hilbert Spaces*) and,
specifically for Hilbert spaces, a genuine formal adjoint and self-adjointness
notion (`Mathlib/Analysis/InnerProductSpace/LinearPMap.lean`: `IsFormalAdjoint`,
`adjoint` (notation `T†`), `isSelfAdjoint_def : IsSelfAdjoint A ↔ A† = A`,
`IsSelfAdjoint.dense_domain`, `IsSelfAdjoint.isClosed`). This had never been
probed by this lab before; every citation above was independently re-read from
source, not merely inherited from a description, before this file was written.

**The test attempted here**: exhibit the simplest genuine instance of an
*unbounded* self-adjoint operator and drive Mathlib's `LinearPMap.adjoint` /
`IsFormalAdjoint` / `IsSelfAdjoint` machinery end to end, all the way to a fully
closed `IsSelfAdjoint T` proof — not merely the easy "symmetric" half
(`T ≤ T.adjoint`, which any densely-defined `T` with `T.IsFormalAdjoint T`
gets for free from `LinearPMap.IsFormalAdjoint.le_adjoint`), but genuine equality
`T.adjoint = T`, which requires separately showing `T.adjoint.domain ≤ T.domain`.
That second inclusion is exactly the classical fact that makes self-adjointness a
strictly stronger, harder statement than mere symmetry for unbounded operators,
and there is no Mathlib lemma that hands it to us — it had to be proved by hand
below (`adjoint_domain_le`), by extracting a bound from continuity of the adjoint
functional and testing it against finitely-supported truncations. That is the
genuine, non-trivial content of this file.

**The instance**: the diagonal ("multiplication") operator on the real sequence
Hilbert space `H := lp (fun _ : ℕ => ℝ) 2` (Mathlib's `ℓ²(ℕ, ℝ)`, an
`InnerProductSpace ℝ` instance via `lp.instInnerProductSpace`, `l2Space.lean`),

  `(T x)_n = n * x_n`,  with maximal domain  `Dom = {x ∈ ℓ² | (n ↦ n·x_n) ∈ ℓ²}`.

This is the standard textbook example of an unbounded self-adjoint operator
(diagonal operators with real eigenvalue sequence on their maximal domain), chosen
over the originally-proposed real-line multiplication operator `M_f` on `L²(ℝ)`
specifically to avoid measure-theoretic domain-density/integrability plumbing:
density of `Dom` here reduces to `lp.hasSum_single` (finitely-supported
truncations of any `f : ℓ²` converge to `f`), a purely combinatorial fact, rather
than a simple-function density argument in `L²(ℝ)`.

## What this file does NOT do (read before citing this result)

* It does **not** define `spectrum`, `resolvent`, `resolventSet`, or
  `compactResolvent` for `LinearPMap` — confirmed absent from every one of the 8
  Mathlib files that reference `LinearPMap` before this file was written, and
  still absent afterwards; nothing here adds any of that machinery. REACT-001
  explicitly demands *compact resolvent*, not merely self-adjointness, so this
  file narrows but does **not** close REACT-001, and by itself gives no grounds
  to reopen `RH-NOGO-001`.
* It proves self-adjointness for one hand-picked diagonal operator with an
  elementary (linear, real) eigenvalue sequence, on a sequence space, not for any
  differential operator, not on any function space relevant to a spectral
  interpretation of the Riemann zeta zeros, and not for any operator with a
  discrete or compact-resolvent spectrum in any sense formalized here.
* It makes no claim of mathematical novelty (this is a 1930s-vintage textbook
  fact) and no claim that any Millennium Prize problem is solved, approximated,
  or newly reachable.
* It does not touch `TamesisLab.lean`, `TamesisLab/RHNogo/*`, or any other file
  in this lab.

## Verification

```
cd 05_FORMAL/lean
lake env lean ../../03_MILLENNIUM/01_RIEMANN/FORMAL/DiagonalSelfAdjointOperatorProbe.lean
```
Exit code 0. No incomplete-proof placeholder, no locally introduced primitive
assumption, and no memory-unchecked declaration appears anywhere in this file.
Printing the trusted foundations of every declaration below shows only
`[propext, Classical.choice, Quot.sound]`.
-/

import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.l2Space

namespace TamesisRH3DiagonalSelfAdjointProbe

open scoped LinearPMap ComplexConjugate ENNReal
noncomputable section

/-- The real Hilbert space `ℓ²(ℕ, ℝ)`. -/
abbrev H : Type := lp (fun _ : ℕ => ℝ) 2

example : InnerProductSpace ℝ H := inferInstance
example : CompleteSpace H := inferInstance

/-- The multiplier sequence `(mulSeq x) n = n * x n`. -/
def mulSeq (x : H) (n : ℕ) : ℝ := (n : ℝ) * x n

/-- The maximal domain on which the diagonal action `n ↦ n * x_n` stays in `ℓ²`. -/
def Dom : Submodule ℝ H where
  carrier := {x : H | Memℓp (mulSeq x) 2}
  zero_mem' := by
    have : mulSeq (0 : H) = (0 : ∀ _ : ℕ, ℝ) := by funext n; simp [mulSeq]
    rw [Set.mem_setOf_eq, this]
    exact zero_memℓp (E := fun _ : ℕ => ℝ) (p := 2)
  add_mem' := by
    intro x y hx hy
    have heq : mulSeq (x + y) = mulSeq x + mulSeq y := by
      funext n; simp only [mulSeq, lp.coeFn_add, Pi.add_apply]; ring
    rw [Set.mem_setOf_eq, heq]
    exact Memℓp.add hx hy
  smul_mem' := by
    intro c x hx
    have heq : mulSeq (c • x) = c • mulSeq x := by
      funext n; simp only [mulSeq, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul]; ring
    rw [Set.mem_setOf_eq, heq]
    exact Memℓp.const_smul hx c

/-- Every finitely-supported basis vector `lp.single 2 i a` lies in `Dom`: multiplying by `n`
just rescales the single nonzero coordinate. -/
theorem single_mem_dom (i : ℕ) (a : ℝ) : lp.single 2 i a ∈ Dom := by
  have hmem : Memℓp (⇑(lp.single 2 i ((i : ℝ) * a) : H)) 2 :=
    lp.memℓp (lp.single 2 i ((i : ℝ) * a) : H)
  have heq : mulSeq (lp.single 2 i a) = ⇑(lp.single 2 i ((i : ℝ) * a) : H) := by
    funext n
    simp only [mulSeq, lp.single_apply, Pi.single_apply]
    by_cases h : n = i
    · subst h; simp
    · simp [h]
  show Memℓp (mulSeq (lp.single 2 i a)) 2
  rw [heq]; exact hmem

/-- `Dom` is dense: every `f : H` is the limit (`lp.hasSum_single`) of its finitely-supported
truncations, each of which lies in `Dom` since `Dom` is a submodule containing every
`lp.single`. Purely combinatorial — no measure theory, unlike the `L²(ℝ)` case this instance
was chosen to avoid. -/
theorem dom_dense : Dense (Dom : Set H) := by
  intro f
  have hsum : HasSum (fun i : ℕ => lp.single 2 i (f i : ℝ)) f := lp.hasSum_single (by norm_num) f
  refine mem_closure_of_tendsto hsum ?_
  filter_upwards with s
  exact Submodule.sum_mem Dom (fun i _ => single_mem_dom i (f i))

/-- The diagonal operator `(T x)_n = n * x_n`, as a linear map on `Dom`. -/
def Tlin : Dom →ₗ[ℝ] H where
  toFun x := ⟨mulSeq (x : H), x.2⟩
  map_add' x y := by
    ext n; simp only [mulSeq, lp.coeFn_add, Pi.add_apply, Submodule.coe_add]; ring
  map_smul' c x := by
    ext n
    simp only [mulSeq, SetLike.val_smul, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul,
      RingHom.id_apply]
    ring

/-- The diagonal multiplication operator `T : H →ₗ.[ℝ] H`, `(T x)_n = n * x_n`, with domain
`Dom = {x ∈ ℓ² | (n ↦ n * x_n) ∈ ℓ²}` — the classical minimal example of an unbounded
self-adjoint operator. -/
def T : H →ₗ.[ℝ] H where
  domain := Dom
  toFun := Tlin

@[simp] theorem T_domain : T.domain = Dom := rfl

@[simp] theorem T_apply (x : T.domain) : T x = ⟨mulSeq (x : H), x.2⟩ := rfl

theorem T_apply_coe (x : T.domain) (n : ℕ) : (T x : H) n = mulSeq (x : H) n := rfl

local notation "⟪" x ", " y "⟫" => inner (𝕜 := ℝ) x y

theorem inner_eq_tsum (f g : H) : ⟪f, g⟫ = ∑' n : ℕ, f n * g n := by
  show (∑' n : ℕ, (inner (𝕜 := ℝ) (f n) (g n))) = ∑' n : ℕ, f n * g n
  simp [RCLike.inner_apply, mul_comm]

/-- `T` is (formally) symmetric: `⟪T x, y⟫ = ⟪x, T y⟫` for `x, y` in its domain. This is the
easy, purely algebraic half of self-adjointness — commutativity of real multiplication under
the `ℓ²` inner product — and by itself only gives `T ≤ T.adjoint`
(`LinearPMap.IsFormalAdjoint.le_adjoint`), not the equality `IsSelfAdjoint` demands. -/
theorem T_isFormalAdjoint : T.IsFormalAdjoint T := by
  intro x y
  show ⟪T x, y⟫ = ⟪(x : H), T y⟫
  rw [inner_eq_tsum, inner_eq_tsum]
  refine tsum_congr fun n => ?_
  show mulSeq (x : H) n * (y : H) n = (x : H) n * mulSeq (y : H) n
  simp only [mulSeq]; ring

/-- **The hard direction.** Every `y` in the domain of `T.adjoint` already lies in `Dom`. This
is the genuine analytic content of self-adjointness for the maximal-domain diagonal operator,
and the one part no Mathlib lemma supplies: a bounded linear functional on the dense subspace
`Dom` (`ContinuousLinearMap.bound`), tested against finitely-supported truncations
`∑_{i∈s} lp.single 2 i (n·y_n)` of `(n ↦ n * y n)` (`memℓp_gen'`, `lp.norm_sum_single`), forces
that sequence to be square-summable — i.e. forces `y` back into `Dom`. Without this direction one
only has symmetry (`T ≤ T.adjoint`), not self-adjointness. -/
theorem adjoint_domain_le : T.adjoint.domain ≤ Dom := by
  intro y hy
  rw [LinearPMap.mem_adjoint_domain_iff] at hy
  set clm : T.domain →L[ℝ] ℝ := ⟨(innerₛₗ ℝ y).comp T.toFun, hy⟩ with hclm_def
  obtain ⟨C, hC0, hCle⟩ := clm.bound
  apply memℓp_gen' (p := 2) (C := C ^ 2)
  intro s
  set xs : H := ∑ i ∈ s, lp.single 2 i (mulSeq y i) with hxs_def
  have hxs_dom : xs ∈ T.domain := by
    rw [T_domain]
    exact Submodule.sum_mem Dom (fun i _ => single_mem_dom i (mulSeq y i))
  have hxs_coe : ∀ n : ℕ, xs n = if n ∈ s then mulSeq y n else 0 := by
    intro n
    simp only [hxs_def, lp.coeFn_sum, Finset.sum_apply, lp.single_apply, Finset.sum_pi_single]
  have hclm_val : clm ⟨xs, hxs_dom⟩ = ∑ n ∈ s, (mulSeq y n) ^ 2 := by
    have hclm_eq : clm ⟨xs, hxs_dom⟩ = ⟪y, T (⟨xs, hxs_dom⟩ : T.domain)⟫ := by
      show (innerₛₗ ℝ y) (T ⟨xs, hxs_dom⟩) = _
      rw [coe_innerₛₗ_apply]
    rw [hclm_eq, inner_eq_tsum]
    have hterm : ∀ n : ℕ, (y : H) n * (T (⟨xs, hxs_dom⟩ : T.domain) : H) n
        = if n ∈ s then (mulSeq y n) ^ 2 else 0 := by
      intro n
      have hcoe : (T (⟨xs, hxs_dom⟩ : T.domain) : H) n = mulSeq xs n := rfl
      rw [hcoe, mulSeq, hxs_coe n]
      by_cases h : n ∈ s
      · simp only [h, if_true, mulSeq]; ring
      · simp [h]
    simp_rw [hterm]
    refine (tsum_eq_sum (s := s) fun n hn => ?_).trans (Finset.sum_congr rfl fun n hn => ?_)
    · simp [hn]
    · simp [hn]
  have hnorm_sq : ∀ n : ℕ, ‖mulSeq y n‖ ^ (2 : ℝ≥0∞).toReal = (mulSeq y n) ^ 2 := by
    intro n
    rw [show (2 : ℝ≥0∞).toReal = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast,
      Real.norm_eq_abs, sq_abs]
  simp_rw [hnorm_sq]
  have hnn : 0 ≤ ∑ n ∈ s, (mulSeq y n) ^ 2 := Finset.sum_nonneg fun n _ => sq_nonneg _
  -- `‖xs‖ ^ 2` equals the very sum we are trying to bound.
  have hxsnormsq : ‖xs‖ ^ 2 = ∑ n ∈ s, (mulSeq y n) ^ 2 := by
    have h2 : ‖xs‖ ^ (2 : ℝ≥0∞).toReal = ∑ i ∈ s, ‖mulSeq y i‖ ^ (2 : ℝ≥0∞).toReal :=
      lp.norm_sum_single (by norm_num) (mulSeq y) s
    rw [show (2 : ℝ≥0∞).toReal = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast] at h2
    simp_rw [Real.rpow_natCast] at h2
    rw [h2]
    exact Finset.sum_congr rfl fun n _ => by rw [Real.norm_eq_abs, sq_abs]
  -- The subtype norm on `T.domain` is, by construction, the ambient norm.
  have hnorm_coe : ‖(⟨xs, hxs_dom⟩ : T.domain)‖ = ‖xs‖ := rfl
  have hb : (∑ n ∈ s, (mulSeq y n) ^ 2) ≤ C * ‖xs‖ := by
    have hb0 := hCle ⟨xs, hxs_dom⟩
    rw [hclm_val, Real.norm_eq_abs, abs_of_nonneg hnn, hnorm_coe] at hb0
    exact hb0
  -- `∑(n y_n)² ≤ C·‖xs‖` and `‖xs‖² = ∑(n y_n)²` force `∑(n y_n)² ≤ C²`.
  nlinarith [hb, hxsnormsq, norm_nonneg xs, hC0.le, sq_nonneg (‖xs‖ - C)]

/-- **Main result.** `T`, the diagonal operator `(T x)_n = n * x_n` on its maximal domain
`Dom = {x ∈ ℓ² | (n ↦ n * x_n) ∈ ℓ²}`, is self-adjoint in the `LinearPMap` sense: `T† = T`.
This meets REACT-001's "compile a minimal example" bar for the self-adjointness layer of
unbounded-operator infrastructure. It does **not** touch the compact-resolvent half of
REACT-001 — see the file header. -/
theorem T_isSelfAdjoint : IsSelfAdjoint T := by
  rw [LinearPMap.isSelfAdjoint_def]
  have hle : T ≤ T.adjoint := T_isFormalAdjoint.le_adjoint dom_dense
  have hdom_eq : T.domain = T.adjoint.domain := le_antisymm hle.1 adjoint_domain_le
  exact (LinearPMap.eq_of_le_of_domain_eq hle hdom_eq).symm

end

end TamesisRH3DiagonalSelfAdjointProbe
