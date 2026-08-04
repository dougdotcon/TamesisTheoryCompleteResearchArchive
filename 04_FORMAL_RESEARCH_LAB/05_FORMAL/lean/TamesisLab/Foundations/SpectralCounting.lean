/-
  Tamesis formal lab -- Piece B key theorem.
  Eigenvalues of a compact symmetric operator do not accumulate away from 0.
  NO sorry / NO admit / NO local axiom.
-/

import Mathlib.Analysis.InnerProductSpace.Spectrum
import Mathlib.Analysis.Normed.Operator.Compact.Basic
import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.Topology.MetricSpace.Sequences

/-!
# FOUND-SPECTRAL-COUNTING-001 — nao-acumulacao espectral

O teorema-chave: **os autovalores de um operador compacto autoadjunto nao
se acumulam fora de zero.**

O Mathlib nao tem nenhum lema de espectro discreto fora de 0 — so
`antilipschitz_of_not_hasEigenvalue`, `hasEigenvalue_or_mem_resolventSet`
e `hasEigenvalue_iff_mem_spectrum`, em `FredholmAlternative`. Frente
genuinamente nova.

## O que torna N(lambda) nao-vacuo

`Set.ncard` devolve `0` tambem para conjuntos **infinitos**. Sem a
finitude provada, `eigCount T lam = 0` seria demonstravel e vazio — o
mesmo defeito que derrubou `FOUND-MONOVARIANT-DESCENT-001`.
`eigCount_eq_zero_iff` so vale porque a finitude vem antes.

## A prova evita Pitagoras

O argumento classico usa `‖Tv - Tw‖^2 = mu^2 + nu^2`. Aqui usa-se
Cauchy-Schwarz contra o proprio autovetor:

```text
<v, Tv - Tw> = mu ‖v‖^2 - nu <v,w> = mu
logo |mu| <= ‖v‖ ‖Tv - Tw‖ = ‖Tv - Tw‖
```

Separacao `lam` em vez de `sqrt 2 * lam`, e **sem `Real.sqrt`**.

`CompleteSpace H` **nao e necessario** — o enunciado provado e mais forte
que o alvo.
-/

open Module.End Filter Topology
open scoped InnerProductSpace

namespace TamesisLab.Foundations.SpectralCounting

variable {𝕜 : Type*} {H : Type*} [RCLike 𝕜] [NormedAddCommGroup H]
  [InnerProductSpace 𝕜 H]

/-! ### Step 1 -- unit eigenvectors -/

/-- Every eigenvalue admits a unit eigenvector. -/
theorem exists_unit_eigenvector {T : H →ₗ[𝕜] H} {μ : 𝕜}
    (h : HasEigenvalue T μ) : ∃ v : H, ‖v‖ = 1 ∧ T v = μ • v := by
  obtain ⟨v, hv₁, hv₂⟩ := h.exists_hasEigenvector
  refine ⟨(‖v‖⁻¹ : 𝕜) • v, norm_smul_inv_norm hv₂, ?_⟩
  rw [mem_eigenspace_iff] at hv₁
  rw [map_smul, hv₁, smul_comm]

/-! ### Step 2 -- separation estimate -/

/-- For a symmetric operator, unit eigenvectors attached to distinct real eigenvalues
have images at distance at least the modulus of the first eigenvalue.
Proved by Cauchy-Schwarz against the first eigenvector, using orthogonality of
eigenspaces; no Pythagoras needed. -/
theorem sep_of_ne {T : H →ₗ[𝕜] H} (hs : T.IsSymmetric) {μ ν : ℝ} (hμν : μ ≠ ν)
    {v w : H} (hv : ‖v‖ = 1)
    (hTv : T v = (μ : 𝕜) • v) (hTw : T w = (ν : 𝕜) • w) :
    |μ| ≤ ‖T v - T w‖ := by
  have hne : (μ : 𝕜) ≠ (ν : 𝕜) := by simpa using hμν
  have horth : ⟪v, w⟫_𝕜 = 0 := by
    have := hs.orthogonalFamily_eigenspaces hne ⟨v, mem_eigenspace_iff.mpr hTv⟩
      ⟨w, mem_eigenspace_iff.mpr hTw⟩
    simpa using this
  have hkey : ⟪v, T v - T w⟫_𝕜 = (μ : 𝕜) := by
    rw [hTv, hTw, inner_sub_right, inner_smul_right, inner_smul_right, horth,
      inner_self_eq_norm_sq_to_K, hv]
    simp
  have hCS := norm_inner_le_norm (𝕜 := 𝕜) v (T v - T w)
  rw [hkey, hv, one_mul] at hCS
  simpa using hCS

/-! ### Step 3 -- the key theorem -/

/-- **Key theorem.** For a compact symmetric operator `T`, the set of real eigenvalues of
modulus at least `lam > 0` is finite: the eigenvalues do not accumulate away from `0`.
Note: `CompleteSpace H` is NOT needed. -/
theorem finite_eigenvalues_above {T : H →L[𝕜] H}
    (hc : IsCompactOperator T) (hs : (T : H →ₗ[𝕜] H).IsSymmetric)
    {lam : ℝ} (hlam : 0 < lam) :
    {μ : ℝ | lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)}.Finite := by
  by_contra hfin
  have hinf : {μ : ℝ | lam ≤ |μ| ∧
      HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)}.Infinite := hfin
  set f := hinf.natEmbedding _ with hfdef
  have hex : ∀ n : ℕ, ∃ v : H, ‖v‖ = 1 ∧
      (T : H →ₗ[𝕜] H) v = (((f n : ℝ)) : 𝕜) • v := fun n =>
    exists_unit_eigenvector (f n).2.2
  choose e he₁ he₂ using hex
  have hK : IsCompact (closure (Set.image (T : H →ₗ[𝕜] H) (Metric.closedBall (0 : H) 1))) :=
    hc.isCompact_closure_image_closedBall 1
  have hmem : ∀ n : ℕ, (T : H →ₗ[𝕜] H) (e n) ∈
      closure (Set.image (T : H →ₗ[𝕜] H) (Metric.closedBall (0 : H) 1)) := fun n =>
    subset_closure ⟨e n, by simp [Metric.mem_closedBall, he₁ n], rfl⟩
  obtain ⟨a, -, φ, hφ, hlim⟩ :=
    hK.tendsto_subseq (x := fun n => (T : H →ₗ[𝕜] H) (e n)) hmem
  rw [Metric.tendsto_atTop] at hlim
  obtain ⟨N, hN⟩ := hlim (lam / 2) (by linarith)
  have h1 := hN N le_rfl
  have h2 := hN (N + 1) (Nat.le_succ N)
  simp only [Function.comp_apply] at h1 h2
  have hne : ((f (φ N) : ℝ)) ≠ ((f (φ (N + 1)) : ℝ)) := by
    intro h
    exact (hφ (Nat.lt_succ_self N)).ne (f.injective (Subtype.coe_injective h))
  have hsep : |((f (φ N) : ℝ))| ≤
      ‖(T : H →ₗ[𝕜] H) (e (φ N)) - (T : H →ₗ[𝕜] H) (e (φ (N + 1)))‖ :=
    sep_of_ne hs hne (he₁ _) (he₂ _) (he₂ _)
  have hlow : lam ≤ ‖(T : H →ₗ[𝕜] H) (e (φ N)) - (T : H →ₗ[𝕜] H) (e (φ (N + 1)))‖ :=
    le_trans (f (φ N)).2.1 hsep
  have hup : ‖(T : H →ₗ[𝕜] H) (e (φ N)) - (T : H →ₗ[𝕜] H) (e (φ (N + 1)))‖ < lam := by
    have htri := dist_triangle ((T : H →ₗ[𝕜] H) (e (φ N))) a
      ((T : H →ₗ[𝕜] H) (e (φ (N + 1))))
    rw [dist_eq_norm] at htri
    rw [dist_comm] at h2
    linarith
  linarith

/-- The requested statement, verbatim (with the extra `[CompleteSpace H]`). -/
theorem finite_eigenvalues_above_target {𝕜 H} [RCLike 𝕜] [NormedAddCommGroup H]
    [InnerProductSpace 𝕜 H] [CompleteSpace H] {T : H →L[𝕜] H}
    (hc : IsCompactOperator T) (hs : (T : H →ₗ[𝕜] H).IsSymmetric)
    {lam : ℝ} (hlam : 0 < lam) :
    {μ : ℝ | lam ≤ |μ| ∧ Module.End.HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)}.Finite :=
  finite_eigenvalues_above hc hs hlam

/-! ### Step 4 -- the counting function N(lam) is no longer junk -/

/-- The eigenvalue counting function above level `lam`. -/
noncomputable def eigCount (T : H →L[𝕜] H) (lam : ℝ) : ℕ :=
  {μ : ℝ | lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)}.ncard

section Counting
variable {T : H →L[𝕜] H}

/-- `eigCount` is a genuine cardinality: realised by an explicit `Finset` whose
elements are exactly the eigenvalues above `lam`. -/
theorem eigCount_eq_finset_card (hc : IsCompactOperator T)
    (hs : (T : H →ₗ[𝕜] H).IsSymmetric) {lam : ℝ} (hlam : 0 < lam) :
    ∃ F : Finset ℝ, (↑F : Set ℝ) =
      {μ : ℝ | lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)} ∧
      F.card = eigCount T lam := by
  have hfin := finite_eigenvalues_above hc hs hlam
  refine ⟨hfin.toFinset, by simp, ?_⟩
  rw [eigCount, Set.ncard_eq_toFinset_card _ hfin]

/-- Non-junk: `eigCount T lam = 0` really means there are NO eigenvalues above `lam`.
For an infinite set `Set.ncard` would also return `0`; that is the junk value. -/
theorem eigCount_eq_zero_iff (hc : IsCompactOperator T)
    (hs : (T : H →ₗ[𝕜] H).IsSymmetric) {lam : ℝ} (hlam : 0 < lam) :
    eigCount T lam = 0 ↔
      ∀ μ : ℝ, lam ≤ |μ| → ¬ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜) := by
  rw [eigCount, Set.ncard_eq_zero (finite_eigenvalues_above hc hs hlam),
    Set.eq_empty_iff_forall_notMem]
  simp only [Set.mem_setOf_eq, not_and]

/-- Non-junk, positive form: a positive count exhibits an actual eigenvalue. -/
theorem exists_of_eigCount_pos (hc : IsCompactOperator T)
    (hs : (T : H →ₗ[𝕜] H).IsSymmetric) {lam : ℝ} (hlam : 0 < lam)
    (h : 0 < eigCount T lam) :
    ∃ μ : ℝ, lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜) := by
  by_contra hcon
  push Not at hcon
  exact absurd ((eigCount_eq_zero_iff hc hs hlam).mpr fun μ hμ hev => hcon μ hμ hev) h.ne.symm

/-- `eigCount` is antitone in `lam` -- a statement that fails for the junk value. -/
theorem eigCount_antitone (hc : IsCompactOperator T)
    (hs : (T : H →ₗ[𝕜] H).IsSymmetric) {lam₁ lam₂ : ℝ} (hlam₁ : 0 < lam₁)
    (h : lam₁ ≤ lam₂) : eigCount T lam₂ ≤ eigCount T lam₁ :=
  Set.ncard_le_ncard (fun μ hμ => ⟨le_trans h hμ.1, hμ.2⟩)
    (finite_eigenvalues_above hc hs hlam₁)

/-- `eigCount` agrees with `Nat.card` of the subtype. -/
theorem eigCount_eq_natCard (T : H →L[𝕜] H) (lam : ℝ) :
    eigCount T lam =
      Nat.card {μ : ℝ // lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)} :=
  (Nat.card_coe_set_eq _).symm

end Counting

/-! ### Step 5 -- POSITIVE INSTANCE (hypotheses satisfiable, conclusion non-empty) -/

/-- The rank-one operator sending `x` to `inner v x` times `v`. -/
noncomputable def rankOne (v : H) : H →L[𝕜] H := (innerSL 𝕜 v).smulRight v

theorem rankOne_isCompactOperator (v : H) (hv : ‖v‖ = 1) :
    IsCompactOperator (rankOne (𝕜 := 𝕜) v) := by
  have hcpt : IsCompact (Set.image (fun t : 𝕜 => t • v) (Metric.closedBall (0 : 𝕜) 1)) :=
    (isCompact_closedBall (0 : 𝕜) 1).image (by fun_prop)
  have key : IsCompactOperator
      (⇑((rankOne (𝕜 := 𝕜) v : H →L[𝕜] H) : H →ₗ[𝕜] H)) := by
    rw [isCompactOperator_iff_isCompact_closure_image_closedBall _ one_pos]
    refine IsCompact.closure_of_subset hcpt ?_
    rintro _ ⟨x, hx, rfl⟩
    refine ⟨⟪v, x⟫_𝕜, ?_, ?_⟩
    · simp only [Metric.mem_closedBall, dist_zero_right]
      calc ‖⟪v, x⟫_𝕜‖ ≤ ‖v‖ * ‖x‖ := norm_inner_le_norm v x
        _ ≤ 1 := by
            rw [hv, one_mul]
            simpa [Metric.mem_closedBall, dist_zero_right] using hx
    · simp [rankOne]
  exact key

theorem rankOne_isSymmetric (v : H) :
    ((rankOne (𝕜 := 𝕜) v : H →L[𝕜] H) : H →ₗ[𝕜] H).IsSymmetric := by
  intro x y
  simp [rankOne, inner_smul_left, inner_smul_right, inner_conj_symm]
  ring

theorem rankOne_hasEigenvalue_one (v : H) (hv : ‖v‖ = 1) :
    HasEigenvalue ((rankOne (𝕜 := 𝕜) v : H →L[𝕜] H) : Module.End 𝕜 H) (((1 : ℝ)) : 𝕜) := by
  have hv0 : v ≠ 0 := by
    rw [← norm_ne_zero_iff, hv]; norm_num
  refine hasEigenvalue_of_hasEigenvector (x := v) ⟨mem_eigenspace_iff.mpr ?_, hv0⟩
  simp [rankOne, inner_self_eq_norm_sq_to_K, hv]

/-- POSITIVE INSTANCE: for every unit vector `v` the hypotheses of the key theorem hold
for `rankOne v`, and the eigenvalue set above `lam = 1` is NON-EMPTY, so the count is
genuinely positive.  The theorem is therefore not vacuous. -/
theorem positive_instance (v : H) (hv : ‖v‖ = 1) :
    IsCompactOperator (rankOne (𝕜 := 𝕜) v) ∧
    ((rankOne (𝕜 := 𝕜) v : H →L[𝕜] H) : H →ₗ[𝕜] H).IsSymmetric ∧
    0 < eigCount (rankOne (𝕜 := 𝕜) v) 1 := by
  refine ⟨rankOne_isCompactOperator v hv, rankOne_isSymmetric v, ?_⟩
  rw [eigCount, Set.ncard_pos (finite_eigenvalues_above
    (rankOne_isCompactOperator v hv) (rankOne_isSymmetric v) one_pos)]
  exact ⟨1, by norm_num, rankOne_hasEigenvalue_one v hv⟩

/-- Fully concrete closed positive instance. -/
theorem positive_instance_concrete :
    0 < eigCount (𝕜 := ℝ) (rankOne (EuclideanSpace.single (0 : Fin 1) (1 : ℝ))) 1 :=
  (positive_instance (𝕜 := ℝ) (EuclideanSpace.single (0 : Fin 1) (1 : ℝ)) (by simp)).2.2

end TamesisLab.Foundations.SpectralCounting

#print axioms TamesisLab.Foundations.SpectralCounting.finite_eigenvalues_above
#print axioms TamesisLab.Foundations.SpectralCounting.finite_eigenvalues_above_target
#print axioms TamesisLab.Foundations.SpectralCounting.eigCount_eq_finset_card
#print axioms TamesisLab.Foundations.SpectralCounting.eigCount_eq_zero_iff
#print axioms TamesisLab.Foundations.SpectralCounting.exists_of_eigCount_pos
#print axioms TamesisLab.Foundations.SpectralCounting.eigCount_antitone
#print axioms TamesisLab.Foundations.SpectralCounting.eigCount_eq_natCard
#print axioms TamesisLab.Foundations.SpectralCounting.positive_instance
#print axioms TamesisLab.Foundations.SpectralCounting.positive_instance_concrete
