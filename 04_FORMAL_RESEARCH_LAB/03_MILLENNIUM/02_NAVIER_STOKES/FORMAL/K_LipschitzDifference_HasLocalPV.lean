/-
NS-2A (Wave-2, item WAVE2-NS-2A) — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`CalderonZygmundKernelDefinitions.lean`, `CalderonZygmundLocalPVExistence.lean`
(NS-1, Wave-1) e `ConstantinFeffermanDepletionKernel.lean` (mesma pasta):
arquivo Lean autônomo, verificado via `lake env lean` diretamente contra o
mesmo projeto Mathlib, fora da árvore de import compartilhada. Wave-2 é
follow-on direto de Wave-1 (27 itens fechados mais cedo hoje); item NS-2a
do plano `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`.

## O que esta frente tenta, e por que

`CalderonZygmundLocalPVExistence.lean` (NS-1) prova `hasLocalPV_K_mul_phi`:
`HasLocalPV (fun y => K e2 e3 y * φ y) 0 R L` para UMA função-teste
concreta e fixa `φ(y) = 1 - ‖y‖` (Lipschitz de constante `1`), usando no
passo central (`K_diff_integrableOn_closedBall`) a IGUALDADE EXATA
`φ y - φ 0 = -‖y‖` (consequência de `φ` ser radial e afim em `‖y‖`).

Esta frente (NS-2a) pergunta se essa igualdade exata pode ser relaxada
para uma DESIGUALDADE de Lipschitz genérica: substituir `φ` por
qualquer `g : E → ℝ` Lipschitz de constante `L ≥ 0`
(`hg : LipschitzWith L.toNNReal g`), e a igualdade `hphidiff` pelo
limitante `|g y - g 0| ≤ L * ‖y‖` (via `LipschitzWith.dist_le_mul`
reescrito por `dist_eq_norm`), reconstruindo toda a cadeia de
desigualdades (`hnormeq`/`hdecay` de NS-1) como uma cadeia de `≤`
terminando em `C * L * ‖y‖ ^ (-2)` em vez da igualdade original. O
`φ` concreto de NS-1 é mantido apenas como INSTÂNCIA de sanidade do
teorema genérico (via `phi_lipschitz`, reaproveitada só para
mensurabilidade/continuidade, exatamente como pedido pelo teste).

## Restatação verbatim (ver nota de isolamento em cada arquivo irmão)

Por ser um arquivo autônomo fora da árvore `05_FORMAL/lean/`, este
arquivo NÃO pode `import` `CalderonZygmundLocalPVExistence.lean` (sem
`.olean` em `LEAN_PATH`). Todo o conteúdo até a seção "NOVO NESTA FRENTE
(NS-2a)" é uma restatação VERBATIM (mesma definição, mesma prova) do
conteúdo já fechado e independentemente verificado em NS-1
(`tripleProduct`, `D`, `HasLocalPV`, `sphereSurfaceMeasure`, `K`, `yHat`,
`K_homogeneous`, `K_bounded_unit_sphere`, `K_abs_le_div_norm_pow`,
`K_shell_integral_eq_zero`, `phi`/`phi_lipschitz`/`phi_zero`,
`tendsto_setIntegral_annulus_of_integrableOn_closedBall`). NÃO é uma
nova alegação matemática. A seção "NOVO NESTA FRENTE (NS-2a)" é o único
conteúdo genuinamente novo desta sessão: a generalização de
`K_diff_integrableOn_closedBall` e de `hasLocalPV_K_mul_phi` de `φ`
concreta para `g` Lipschitz genérica.
-/

import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Angle.Unoriented.CrossProduct
import Mathlib.LinearAlgebra.CrossProduct
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Normed.Lp.MeasurableSpace
import Mathlib.MeasureTheory.Measure.Haar.OfBasis
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Analysis.Normed.Lp.PiLp
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Analysis.SpecialFunctions.Pow.Integral
import Mathlib.Topology.Order.AtTopBotIxx
import Mathlib.Tactic

namespace TamesisNSLocalPVLipschitz

open Matrix InnerProductGeometry MeasureTheory Set Filter Topology
open scoped Pointwise

/-! ## Parte 0 — restatação verbatim de `D` (núcleo de Constantin-Fefferman)

Cópia verbatim de `tripleProduct` e `D`, ver nota do cabeçalho. -/

noncomputable def tripleProduct (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 (WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3))

noncomputable def D (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 e3 * tripleProduct e1 e2 e3

/-! ## Parte 1 — restatação verbatim: `HasLocalPV` (definição do escopo) -/

def HasLocalPV (f : EuclideanSpace ℝ (Fin 3) → ℝ) (x0 : EuclideanSpace ℝ (Fin 3))
    (R L : ℝ) : Prop :=
  Filter.Tendsto
    (fun ε : ℝ => ∫ y in (Metric.closedBall x0 R \ Metric.closedBall x0 ε), f y)
    (nhdsWithin 0 (Set.Ioi 0)) (nhds L)

theorem HasLocalPV.unique {f : EuclideanSpace ℝ (Fin 3) → ℝ}
    {x0 : EuclideanSpace ℝ (Fin 3)} {R L L' : ℝ}
    (h : HasLocalPV f x0 R L) (h' : HasLocalPV f x0 R L') : L = L' := by
  unfold HasLocalPV at h h'
  exact tendsto_nhds_unique h h'

theorem hasLocalPV_zero (x0 : EuclideanSpace ℝ (Fin 3)) (R : ℝ) :
    HasLocalPV (fun _ : EuclideanSpace ℝ (Fin 3) => (0 : ℝ)) x0 R 0 := by
  have hzero : (fun ε : ℝ =>
      ∫ y in (Metric.closedBall x0 R \ Metric.closedBall x0 ε),
        (fun _ : EuclideanSpace ℝ (Fin 3) => (0 : ℝ)) y) = fun _ : ℝ => (0 : ℝ) := by
    funext ε
    simp
  unfold HasLocalPV
  rw [hzero]
  exact tendsto_const_nhds

/-! ## Parte 2 — restatação verbatim: `sphereSurfaceMeasure`, classe CZ -/

noncomputable def sphereSurfaceMeasure :
    MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3)) :=
  MeasureTheory.Measure.map
    ((↑) : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) →
      EuclideanSpace ℝ (Fin 3))
    (MeasureTheory.volume.toSphere)

/-! ## Parte 3 — restatação verbatim: `K` (peça de coeficiente congelado) -/

noncomputable def yHat (y : EuclideanSpace ℝ (Fin 3)) : EuclideanSpace ℝ (Fin 3) :=
  ‖y‖⁻¹ • y

noncomputable def K (e2 e3 y : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  D (yHat y) e2 e3 / ‖y‖ ^ 3

theorem yHat_smul_of_pos (y : EuclideanSpace ℝ (Fin 3)) (hy : y ≠ 0)
    (t : ℝ) (ht : 0 < t) : yHat (t • y) = yHat y := by
  have hty : ‖t • y‖ = t * ‖y‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos ht]
  unfold yHat
  rw [hty, mul_inv, smul_smul]
  congr 1
  field_simp

theorem K_homogeneous (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (y : EuclideanSpace ℝ (Fin 3)) (hy : y ≠ 0) (t : ℝ) (ht : 0 < t) :
    t ^ 3 * K e2 e3 (t • y) = K e2 e3 y := by
  have hty : ‖t • y‖ = t * ‖y‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos ht]
  have hyhat : yHat (t • y) = yHat y := yHat_smul_of_pos y hy t ht
  have hynorm : ‖y‖ ≠ 0 := norm_ne_zero_iff.mpr hy
  have ht0 : t ≠ 0 := ht.ne'
  unfold K
  rw [hyhat, hty, mul_pow]
  field_simp

theorem contDiff_D_fst (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ContDiff ℝ ⊤ (fun e1 : EuclideanSpace ℝ (Fin 3) => D e1 e2 e3) := by
  unfold D tripleProduct
  exact (contDiff_id.inner ℝ contDiff_const).mul (contDiff_id.inner ℝ contDiff_const)

theorem contDiffAt_yHat (y : EuclideanSpace ℝ (Fin 3)) (hy : y ≠ 0) :
    ContDiffAt ℝ ⊤ yHat y := by
  unfold yHat
  have hnorm : ContDiffAt ℝ (⊤ : WithTop ℕ∞) (‖·‖ : EuclideanSpace ℝ (Fin 3) → ℝ) y :=
    contDiffAt_norm (𝕜 := ℝ) hy
  have hinv : ContDiffAt ℝ (⊤ : WithTop ℕ∞)
      (fun z : EuclideanSpace ℝ (Fin 3) => ‖z‖⁻¹) y :=
    hnorm.inv (norm_ne_zero_iff.mpr hy)
  exact hinv.smul contDiffAt_id

theorem contDiffAt_K (e2 e3 : EuclideanSpace ℝ (Fin 3)) {y : EuclideanSpace ℝ (Fin 3)}
    (hy : y ≠ 0) : ContDiffAt ℝ ⊤ (K e2 e3) y := by
  have hD : ContDiffAt ℝ (⊤ : WithTop ℕ∞) (fun e1 : EuclideanSpace ℝ (Fin 3) => D e1 e2 e3)
      (yHat y) := (contDiff_D_fst e2 e3).contDiffAt
  have hcomp : ContDiffAt ℝ (⊤ : WithTop ℕ∞)
      (fun z : EuclideanSpace ℝ (Fin 3) => D (yHat z) e2 e3) y :=
    hD.comp y (contDiffAt_yHat y hy)
  have hnorm3 : ContDiffAt ℝ (⊤ : WithTop ℕ∞)
      (fun z : EuclideanSpace ℝ (Fin 3) => ‖z‖ ^ 3) y :=
    (contDiffAt_norm (𝕜 := ℝ) hy).pow 3
  have hne : ‖y‖ ^ 3 ≠ 0 := pow_ne_zero 3 (norm_ne_zero_iff.mpr hy)
  exact hcomp.div hnorm3 hne

/-! ## Parte 4 — restatação verbatim: fechamento de `mean_zero` (Parte 4 de
`FOUND-CZ-MEAN-ZERO-001`) -/

theorem tripleProduct_self_left (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    tripleProduct e3 e2 e3 = 0 := by
  unfold tripleProduct
  rw [EuclideanSpace.inner_eq_star_dotProduct]
  simp [dotProduct_comm, dot_cross_self]

def IsotropicSecondMoment (μ : MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3))) (c : ℝ) : Prop :=
  (∀ i j : Fin 3, Integrable (fun θ : EuclideanSpace ℝ (Fin 3) => θ i * θ j) μ) ∧
  (∀ i j : Fin 3, ∫ θ, θ i * θ j ∂μ = c * (if i = j then (1:ℝ) else 0))

theorem integral_D_eq_zero_of_isotropicSecondMoment
    {μ : MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3))} {c : ℝ}
    (hiso : IsotropicSecondMoment μ c) (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∫ θ, D θ e2 e3 ∂μ = 0 := by
  obtain ⟨hint, hval⟩ := hiso
  set w : EuclideanSpace ℝ (Fin 3) := WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3) with hw
  have hDeq : ∀ θ : EuclideanSpace ℝ (Fin 3),
      D θ e2 e3 = ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * (θ p.1 * θ p.2) := by
    intro θ
    unfold D tripleProduct
    rw [EuclideanSpace.inner_eq_star_dotProduct, EuclideanSpace.inner_eq_star_dotProduct]
    unfold dotProduct
    simp [Fin.sum_univ_three, Fintype.sum_prod_type]
    ring
  have hintg : ∀ p : Fin 3 × Fin 3,
      Integrable (fun θ : EuclideanSpace ℝ (Fin 3) => (e3 p.1 * w p.2) * (θ p.1 * θ p.2)) μ :=
    fun p => (hint p.1 p.2).const_mul _
  calc ∫ θ, D θ e2 e3 ∂μ
      = ∫ θ, ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * (θ p.1 * θ p.2) ∂μ := by
        simp_rw [hDeq]
    _ = ∑ p : Fin 3 × Fin 3, ∫ θ, (e3 p.1 * w p.2) * (θ p.1 * θ p.2) ∂μ :=
        integral_finsetSum Finset.univ (fun p _ => hintg p)
    _ = ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * ∫ θ, θ p.1 * θ p.2 ∂μ := by
        simp_rw [integral_const_mul]
    _ = ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * (c * (if p.1 = p.2 then (1:ℝ) else 0)) := by
        simp_rw [hval]
    _ = c * ∑ i : Fin 3, e3 i * w i := by
        simp [Fintype.sum_prod_type, Fin.sum_univ_three]
        ring
    _ = c * tripleProduct e3 e2 e3 := by
        congr 1
        unfold tripleProduct
        rw [EuclideanSpace.inner_eq_star_dotProduct]
        unfold dotProduct
        simp [Fin.sum_univ_three]
        ring
    _ = 0 := by rw [tripleProduct_self_left]; ring

theorem volume_image_linearIsometryEquiv (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (B : Set (EuclideanSpace ℝ (Fin 3))) :
    (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) (T '' B) = MeasureTheory.volume B := by
  have hmp : Measure.map (⇑T) (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) =
      MeasureTheory.volume := (LinearIsometryEquiv.measurePreserving T).map_eq
  have h1 : Measure.map (⇑T.toMeasurableEquiv)
      (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) (T '' B) = MeasureTheory.volume (T '' B) := by
    rw [LinearIsometryEquiv.coe_toMeasurableEquiv, hmp]
  rw [MeasurableEquiv.map_apply] at h1
  rw [LinearIsometryEquiv.coe_toMeasurableEquiv, Set.preimage_image_eq B T.injective] at h1
  exact h1.symm

theorem image_smul_Ioo_linearIsometryEquiv
    (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) (A : Set (EuclideanSpace ℝ (Fin 3))) :
    T '' (Set.Ioo (0:ℝ) 1 • A) = Set.Ioo (0:ℝ) 1 • (T '' A) := by
  rw [← iUnion_smul_set, ← iUnion_smul_set, Set.image_iUnion₂]
  simp_rw [image_smul_set (F := EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) T]

theorem mapsTo_sphere (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Set.MapsTo T (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) := by
  intro x hx
  simp only [Metric.mem_sphere, dist_zero_right] at hx ⊢
  rw [LinearIsometryEquiv.norm_map]
  exact hx

noncomputable def sphereMap (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) → (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) :=
  (mapsTo_sphere T).restrict T _ _

theorem sphereMap_continuous (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Continuous (sphereMap T) :=
  Continuous.subtype_mk (T.continuous.comp continuous_subtype_val) _

theorem sphereMap_measurable (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Measurable (sphereMap T) := (sphereMap_continuous T).measurable

theorem image_val_preimage_sphereMap (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (s : Set (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1)) :
    ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) '' ((sphereMap T) ⁻¹' s)
      = T ⁻¹' (((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) '' s) := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    refine ⟨sphereMap T x, hx, ?_⟩
    show ((sphereMap T x : EuclideanSpace ℝ (Fin 3))) = T (x : EuclideanSpace ℝ (Fin 3))
    exact (Set.MapsTo.val_restrict_apply (mapsTo_sphere T) x)
  · rintro hy
    rw [Set.mem_preimage] at hy
    obtain ⟨x', hx', hx'eq⟩ := hy
    have hyS : y ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 := by
      have hx'2 : ‖(x' : EuclideanSpace ℝ (Fin 3))‖ = 1 := by
        have hx'3 := x'.2
        simp only [Metric.mem_sphere, dist_zero_right] at hx'3
        exact hx'3
      have hty : ‖T y‖ = 1 := by rw [← hx'eq]; exact hx'2
      simpa [Metric.mem_sphere, dist_zero_right, LinearIsometryEquiv.norm_map] using hty
    refine ⟨⟨y, hyS⟩, ?_, rfl⟩
    show sphereMap T ⟨y, hyS⟩ ∈ s
    have hval : ((sphereMap T ⟨y, hyS⟩ : EuclideanSpace ℝ (Fin 3))) = T y :=
      Set.MapsTo.val_restrict_apply (mapsTo_sphere T) ⟨y, hyS⟩
    have heq : sphereMap T ⟨y, hyS⟩ = x' := by
      apply Subtype.ext
      rw [hval, hx'eq]
    rwa [heq]

theorem preimage_eq_image_symm (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (A : Set (EuclideanSpace ℝ (Fin 3))) : T ⁻¹' A = T.symm '' A := by
  ext y
  simp only [Set.mem_preimage, Set.mem_image]
  constructor
  · intro h; exact ⟨T y, h, T.symm_apply_apply y⟩
  · rintro ⟨a, ha, rfl⟩; simpa using ha

theorem toSphere_map_sphereMap (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Measure.map (sphereMap T) (MeasureTheory.volume.toSphere) = MeasureTheory.volume.toSphere := by
  apply Measure.ext
  intro s hs
  rw [Measure.map_apply (sphereMap_measurable T) hs]
  rw [Measure.toSphere_apply' _ hs, Measure.toSphere_apply' _ (hs.preimage (sphereMap_measurable T))]
  rw [image_val_preimage_sphereMap T s, preimage_eq_image_symm T]
  rw [← image_smul_Ioo_linearIsometryEquiv T.symm]
  rw [volume_image_linearIsometryEquiv T.symm]

theorem sphereSurfaceMeasure_map_linearIsometryEquiv
    (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Measure.map T sphereSurfaceMeasure = sphereSurfaceMeasure := by
  unfold sphereSurfaceMeasure
  rw [Measure.map_map T.continuous.measurable measurable_subtype_coe]
  have hcomm : (T : EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 3)) ∘
        ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3))
      = ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) ∘ (sphereMap T) :=
    (Set.MapsTo.restrict_commutes T _ _ (mapsTo_sphere T)).symm
  rw [hcomm, ← Measure.map_map measurable_subtype_coe (sphereMap_measurable T),
    toSphere_map_sphereMap]

theorem ae_mem_sphere_sphereSurfaceMeasure :
    ∀ᵐ θ ∂sphereSurfaceMeasure, θ ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 := by
  rw [ae_iff]
  have hmeas : MeasurableSet {x : EuclideanSpace ℝ (Fin 3) | ¬ x ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1} :=
    (Metric.isClosed_sphere).measurableSet.compl
  unfold sphereSurfaceMeasure
  rw [Measure.map_apply measurable_subtype_coe hmeas]
  have hempty : ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) ⁻¹'
      {x : EuclideanSpace ℝ (Fin 3) | ¬ x ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1} = ∅ := by
    ext x; simp
  rw [hempty]; simp

instance instIsFiniteMeasure_sphereSurfaceMeasure : IsFiniteMeasure sphereSurfaceMeasure := by
  unfold sphereSurfaceMeasure
  infer_instance

theorem integrable_coord_mul_sphereSurfaceMeasure (i j : Fin 3) :
    Integrable (fun θ : EuclideanSpace ℝ (Fin 3) => θ i * θ j) sphereSurfaceMeasure := by
  apply Integrable.mono' (integrable_const (1:ℝ))
  · fun_prop
  · filter_upwards [ae_mem_sphere_sphereSurfaceMeasure] with θ hθ
    have hθ' : ‖θ‖ = 1 := by simpa [Metric.mem_sphere, dist_zero_right] using hθ
    have hi : ‖θ i‖ ≤ 1 := by rw [← hθ']; exact PiLp.norm_apply_le θ i
    have hj : ‖θ j‖ ≤ 1 := by rw [← hθ']; exact PiLp.norm_apply_le θ j
    calc ‖θ i * θ j‖ = ‖θ i‖ * ‖θ j‖ := norm_mul _ _
      _ ≤ 1 * 1 := mul_le_mul hi hj (norm_nonneg _) (by norm_num)
      _ = 1 := by ring

noncomputable def flipCoord (k : Fin 3) :
    EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3) :=
  LinearIsometryEquiv.piLpCongrRight 2
    (fun i => if i = k then LinearIsometryEquiv.neg ℝ else LinearIsometryEquiv.refl ℝ ℝ)

theorem flipCoord_apply_self (k : Fin 3) (θ : EuclideanSpace ℝ (Fin 3)) :
    (flipCoord k θ) k = - θ k := by
  unfold flipCoord
  rw [LinearIsometryEquiv.piLpCongrRight_apply]
  simp

theorem flipCoord_apply_other (k i : Fin 3) (θ : EuclideanSpace ℝ (Fin 3)) (h : i ≠ k) :
    (flipCoord k θ) i = θ i := by
  unfold flipCoord
  rw [LinearIsometryEquiv.piLpCongrRight_apply]
  simp [h]

noncomputable def permCoord (σ : Equiv.Perm (Fin 3)) :
    EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3) :=
  LinearIsometryEquiv.piLpCongrLeft 2 ℝ ℝ σ

theorem permCoord_apply (σ : Equiv.Perm (Fin 3)) (θ : EuclideanSpace ℝ (Fin 3)) (i : Fin 3) :
    (permCoord σ θ) i = θ (σ.symm i) := by
  unfold permCoord
  rw [LinearIsometryEquiv.piLpCongrLeft_apply]
  simp [Equiv.piCongrLeft']

theorem integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
    (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) (g : EuclideanSpace ℝ (Fin 3) → ℝ) :
    ∫ θ, g (T θ) ∂sphereSurfaceMeasure = ∫ θ, g θ ∂sphereSurfaceMeasure := by
  have hMP : MeasurePreserving T.toMeasurableEquiv sphereSurfaceMeasure sphereSurfaceMeasure := by
    refine ⟨T.toMeasurableEquiv.measurable, ?_⟩
    rw [LinearIsometryEquiv.coe_toMeasurableEquiv]
    exact sphereSurfaceMeasure_map_linearIsometryEquiv T
  have hcomp := hMP.integral_comp' g
  simpa [LinearIsometryEquiv.coe_toMeasurableEquiv] using hcomp

theorem integral_offdiag_eq_zero_sphereSurfaceMeasure (i j : Fin 3) (h : i ≠ j) :
    ∫ θ, θ i * θ j ∂sphereSurfaceMeasure = 0 := by
  have hkey := integral_comp_linearIsometryEquiv_sphereSurfaceMeasure (flipCoord i)
    (fun θ => θ i * θ j)
  have hpt : ∀ θ : EuclideanSpace ℝ (Fin 3),
      (flipCoord i θ) i * (flipCoord i θ) j = - (θ i * θ j) := by
    intro θ
    rw [flipCoord_apply_self, flipCoord_apply_other i j θ (Ne.symm h)]
    ring
  simp_rw [hpt] at hkey
  rw [integral_neg] at hkey
  linarith

theorem integral_diag_eq_sphereSurfaceMeasure (i j : Fin 3) :
    ∫ θ, θ i * θ i ∂sphereSurfaceMeasure = ∫ θ, θ j * θ j ∂sphereSurfaceMeasure := by
  have hkey := integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
    (permCoord (Equiv.swap i j)) (fun θ => θ i * θ i)
  have hpt : ∀ θ : EuclideanSpace ℝ (Fin 3),
      (permCoord (Equiv.swap i j) θ) i * (permCoord (Equiv.swap i j) θ) i = θ j * θ j := by
    intro θ
    rw [permCoord_apply]
    simp [Equiv.symm_swap, Equiv.swap_apply_left]
  simp_rw [hpt] at hkey
  linarith

theorem sphereSurfaceMeasure_isotropicSecondMoment :
    IsotropicSecondMoment sphereSurfaceMeasure (∫ θ, θ 0 * θ 0 ∂sphereSurfaceMeasure) := by
  refine ⟨integrable_coord_mul_sphereSurfaceMeasure, ?_⟩
  intro i j
  by_cases h : i = j
  · subst h
    simp only [mul_one, ite_true]
    exact integral_diag_eq_sphereSurfaceMeasure i 0
  · simp only [if_neg h, mul_zero]
    exact integral_offdiag_eq_zero_sphereSurfaceMeasure i j h

theorem K_mean_zero_sphereSurfaceMeasure (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∫ y in Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1, K e2 e3 y ∂sphereSurfaceMeasure = 0 := by
  have heq : Set.EqOn (K e2 e3) (fun y => D y e2 e3) (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) := by
    intro y hy
    have hynorm : ‖y‖ = 1 := by simpa [Metric.mem_sphere, dist_zero_right] using hy
    show D (yHat y) e2 e3 / ‖y‖ ^ 3 = D y e2 e3
    unfold yHat
    rw [hynorm]
    simp
  rw [setIntegral_congr_fun Metric.isClosed_sphere.measurableSet heq]
  show ∫ y, D y e2 e3 ∂(sphereSurfaceMeasure.restrict (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1)) = 0
  rw [Measure.restrict_eq_self_of_ae_mem ae_mem_sphere_sphereSurfaceMeasure]
  exact integral_D_eq_zero_of_isotropicSecondMoment sphereSurfaceMeasure_isotropicSecondMoment e2 e3

/-! ## NOVO NESTA FRENTE (NS-1)

Tudo abaixo desta linha é conteúdo genuinamente novo desta sessão --
não é restatação de nada anteriormente fechado. Ver o resumo do
cabeçalho e o bloco final "O que NÃO é afirmado" para o escopo exato. -/

/-! ### Parte 5 — `K e2 e3` é limitado na esfera unitária

Consequência de `contDiffAt_K` (item já fechado, restatado acima) mais
compacidade da esfera unitária (`isCompact_sphere`, Mathlib). -/

theorem K_bounded_unit_sphere (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∃ C : ℝ, ∀ θ : EuclideanSpace ℝ (Fin 3), ‖θ‖ = 1 → |K e2 e3 θ| ≤ C := by
  have hcompact : IsCompact (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) := isCompact_sphere _ _
  have hcont : ContinuousOn (K e2 e3) (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) := by
    intro y hy
    have hyne : y ≠ 0 := by
      intro h; rw [h] at hy; simp at hy
    exact (contDiffAt_K e2 e3 hyne).continuousAt.continuousWithinAt
  obtain ⟨C, hC⟩ := hcompact.exists_bound_of_continuousOn hcont
  refine ⟨C, fun θ hθ => ?_⟩
  have hmem : θ ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 := by
    simp [Metric.mem_sphere, dist_zero_right, hθ]
  have := hC θ hmem
  simpa [Real.norm_eq_abs] using this

/-- Consequência direta de `K_bounded_unit_sphere` e `K_homogeneous`:
`|K e2 e3 y| ≤ C / ‖y‖^3` para TODO `y ≠ 0`, com uma constante `C ≥ 0`
uniforme (não depende de `y`). Reaproveitada tanto pela integrabilidade
absoluta da peça de diferença (Parte 7) quanto pela integrabilidade de
`K` sobre uma casca compacta (Parte 9). -/
theorem K_abs_le_div_norm_pow (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ y : EuclideanSpace ℝ (Fin 3), y ≠ 0 → |K e2 e3 y| ≤ C / ‖y‖ ^ 3 := by
  obtain ⟨C₀, hC₀⟩ := K_bounded_unit_sphere e2 e3
  refine ⟨max C₀ 0, le_max_right _ _, ?_⟩
  intro y hy
  have hC : ∀ θ : EuclideanSpace ℝ (Fin 3), ‖θ‖ = 1 → |K e2 e3 θ| ≤ max C₀ 0 :=
    fun θ hθ => le_trans (hC₀ θ hθ) (le_max_left _ _)
  have hynorm : (0:ℝ) < ‖y‖ := norm_pos_iff.mpr hy
  have hyhat_norm : ‖yHat y‖ = 1 := by
    unfold yHat
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hynorm)]
    field_simp
  have hyhat_ne : yHat y ≠ 0 := by
    intro h; rw [h, norm_zero] at hyhat_norm; norm_num at hyhat_norm
  have hsmul_eq : ‖y‖ • yHat y = y := by
    unfold yHat
    rw [smul_smul, mul_inv_cancel₀ hynorm.ne', one_smul]
  have hKhom2 := K_homogeneous e2 e3 (yHat y) hyhat_ne ‖y‖ hynorm
  rw [hsmul_eq] at hKhom2
  have hy3pos : (0:ℝ) < ‖y‖ ^ 3 := by positivity
  rw [le_div_iff₀ hy3pos]
  calc |K e2 e3 y| * ‖y‖ ^ 3 = |K e2 e3 y * ‖y‖ ^ 3| := by
        rw [abs_mul, abs_of_nonneg (by positivity : (0:ℝ) ≤ ‖y‖ ^ 3)]
    _ = |‖y‖ ^ 3 * K e2 e3 y| := by ring_nf
    _ = |K e2 e3 (yHat y)| := by rw [hKhom2]
    _ ≤ max C₀ 0 := hC _ hyhat_norm

/-! ### Parte 6 — extensão de `mean_zero` para uma casca esférica genérica

**Item central desta frente**: `K_mean_zero_sphereSurfaceMeasure` (Parte
4, restatada acima) só dá média zero na esfera de raio `1`. O passo
conectivo genuinamente faltante -- identificado pela revisão adversarial
-- é estender isso para o volume da integral de `K` sobre QUALQUER
casca esférica `{a ≤ ‖y‖ ≤ b}`, `0 < a < b`. Isso é feito aqui via a
ponte polar/Fubini construída a partir de
`measurePreserving_homeomorphUnitSphereProd` (Kudryashov) e
`integral_prod_symm` (Fubini), NÃO citada nem construída em nenhum
trabalho anterior deste laboratório. -/

/-- Restatação de `K_mean_zero_sphereSurfaceMeasure` (Parte 4) contra a
medida SUBTIPO `volume.toSphere` de Kudryashov, em vez da medida
empurrada `sphereSurfaceMeasure` em `E`. Ponte necessária porque a
maquinaria de coordenadas polares generalizadas
(`measurePreserving_homeomorphUnitSphereProd`) produz integrais sobre
`volume.toSphere`, não sobre `sphereSurfaceMeasure`. -/
theorem K_mean_zero_sphereSurfaceMeasure_via_toSphere (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∫ θ : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1), K e2 e3 (θ : EuclideanSpace ℝ (Fin 3))
      ∂(MeasureTheory.volume.toSphere) = 0 := by
  rw [← K_mean_zero_sphereSurfaceMeasure e2 e3]
  rw [show (∫ y in Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1, K e2 e3 y ∂sphereSurfaceMeasure) =
      ∫ y, K e2 e3 y ∂sphereSurfaceMeasure from by
    rw [Measure.restrict_eq_self_of_ae_mem ae_mem_sphere_sphereSurfaceMeasure]]
  rw [sphereSurfaceMeasure]
  exact ((MeasurableEmbedding.subtype_coe Metric.isClosed_sphere.measurableSet).integral_map (K e2 e3)).symm

theorem K_shell_integral_eq_zero (e2 e3 : EuclideanSpace ℝ (Fin 3)) (a b : ℝ)
    (ha : 0 < a) (hab : a < b) :
    ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) b \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) a), K e2 e3 y = 0 := by
  set S : Set (EuclideanSpace ℝ (Fin 3)) :=
    Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) b \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) a with hS
  have hSmeas : MeasurableSet S :=
    (Metric.isClosed_closedBall.measurableSet).diff (Metric.isClosed_closedBall.measurableSet)
  have hSform : S = {y : EuclideanSpace ℝ (Fin 3) | a < ‖y‖ ∧ ‖y‖ ≤ b} := by
    ext y
    simp only [hS, Set.mem_diff, Metric.mem_closedBall, dist_zero_right, Set.mem_setOf_eq, not_le]
    tauto
  -- Reduce to an integral over the whole space of the indicator function.
  have step1 : ∫ y in S, K e2 e3 y = ∫ y, S.indicator (K e2 e3) y :=
    (MeasureTheory.integral_indicator hSmeas).symm
  -- Reduce to an integral over `{0}ᶜ` via the subtype comap.
  have step2 : (∫ y, S.indicator (K e2 e3) y)
      = ∫ x : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))),
          S.indicator (K e2 e3) x.1
          ∂(MeasureTheory.volume.comap
            ((↑) : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) →
              EuclideanSpace ℝ (Fin 3))) := by
    rw [MeasureTheory.integral_subtype_comap (measurableSet_singleton (0 : EuclideanSpace ℝ (Fin 3))).compl
      (S.indicator (K e2 e3))]
    rw [restrict_compl_singleton]
  -- Transfer along the polar-coordinate homeomorphism.
  set g : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 × Set.Ioi (0 : ℝ)) → ℝ :=
    fun p => S.indicator (K e2 e3)
      (((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))).symm p : EuclideanSpace ℝ (Fin 3)))
    with hg
  have hcomp : ∀ x : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))),
      g ((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))) x) = S.indicator (K e2 e3) x.1 := by
    intro x
    simp only [hg, Homeomorph.symm_apply_apply]
  have step3 :
      (∫ x : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))),
        S.indicator (K e2 e3) x.1
        ∂(MeasureTheory.volume.comap
          ((↑) : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) →
            EuclideanSpace ℝ (Fin 3))))
      = ∫ x : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))),
          g ((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))) x)
          ∂(MeasureTheory.volume.comap
            ((↑) : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) →
              EuclideanSpace ℝ (Fin 3))) := by
    apply MeasureTheory.integral_congr_ae
    filter_upwards with x
    exact (hcomp x).symm
  have step4 : (∫ x : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))),
      g ((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))) x)
      ∂(MeasureTheory.volume.comap
        ((↑) : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) →
          EuclideanSpace ℝ (Fin 3)))) = ∫ p, g p ∂(MeasureTheory.volume.toSphere.prod
        (MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1))) := by
    exact (MeasureTheory.Measure.measurePreserving_homeomorphUnitSphereProd
      (E := EuclideanSpace ℝ (Fin 3)) MeasureTheory.volume).integral_comp
      (Homeomorph.measurableEmbedding _) g
  rw [step1, step2, step3, step4]
  have hsymm : ∀ p : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 × Set.Ioi (0 : ℝ)),
      ((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))).symm p : EuclideanSpace ℝ (Fin 3))
        = (p.2 : ℝ) • (p.1 : EuclideanSpace ℝ (Fin 3)) :=
    fun p => homeomorphUnitSphereProd_symm_apply_coe (EuclideanSpace ℝ (Fin 3)) p
  -- Pointwise formula for `g`: it factors through the indicator of `Ioc a b`
  -- in the radial variable times `K θ / r^3` (homogeneity), for each fixed θ.
  have hgpt : ∀ p : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 × Set.Ioi (0 : ℝ)),
      g p = (Set.Ioc a b).indicator (fun r' => K e2 e3 (p.1 : EuclideanSpace ℝ (Fin 3)) / r' ^ 3)
        (p.2 : ℝ) := by
    rintro ⟨θ, r, hr⟩
    have hrpos : 0 < r := hr
    have hθnorm : ‖(θ : EuclideanSpace ℝ (Fin 3))‖ = 1 := by
      have := θ.2
      simpa [Metric.mem_sphere, dist_zero_right] using this
    have hθne : (θ : EuclideanSpace ℝ (Fin 3)) ≠ 0 := by
      intro h; rw [h] at hθnorm; simp at hθnorm
    have hnormr : ‖r • (θ : EuclideanSpace ℝ (Fin 3))‖ = r := by
      rw [norm_smul, Real.norm_eq_abs, abs_of_pos hrpos, hθnorm, mul_one]
    have hmem : (r • (θ : EuclideanSpace ℝ (Fin 3))) ∈ S ↔ r ∈ Set.Ioc a b := by
      rw [hSform]
      simp only [Set.mem_setOf_eq, Set.mem_Ioc, hnormr]
    simp only [hg]
    rw [hsymm ⟨θ, r, hr⟩]
    show S.indicator (K e2 e3) (r • (θ : EuclideanSpace ℝ (Fin 3)))
      = (Set.Ioc a b).indicator (fun r' => K e2 e3 (θ : EuclideanSpace ℝ (Fin 3)) / r' ^ 3) r
    by_cases hcase : r ∈ Set.Ioc a b
    · rw [Set.indicator_of_mem (hmem.mpr hcase) (K e2 e3), Set.indicator_of_mem hcase]
      have hK := K_homogeneous e2 e3 (θ : EuclideanSpace ℝ (Fin 3)) hθne r hrpos
      have hr3 : r ^ 3 ≠ 0 := pow_ne_zero 3 hrpos.ne'
      field_simp
      linarith [hK]
    · rw [Set.indicator_of_notMem (fun h => hcase (hmem.mp h)),
        Set.indicator_of_notMem hcase]
  obtain ⟨C, hC⟩ := K_bounded_unit_sphere e2 e3
  set s' : Set (Set.Ioi (0 : ℝ)) := (Subtype.val) ⁻¹' (Set.Ioc a b) with hs'def
  have hs'meas : MeasurableSet s' := measurableSet_Ioc.preimage measurable_subtype_coe
  have hs'fin : (MeasureTheory.Measure.volumeIoiPow
      (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1)) s' ≠ ⊤ := by
    have hxpos : 0 < b + 1 := by linarith
    have hsub : s' ⊆ Set.Iio (⟨b + 1, hxpos⟩ : Set.Ioi (0 : ℝ)) := by
      intro x hx
      simp only [hs'def, Set.mem_preimage, Set.mem_Ioc] at hx
      show (x : ℝ) < b + 1
      linarith [hx.2]
    have hle : MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1) s'
        ≤ MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1)
            (Set.Iio (⟨b + 1, hxpos⟩ : Set.Ioi (0 : ℝ))) := MeasureTheory.measure_mono hsub
    rw [MeasureTheory.Measure.volumeIoiPow_apply_Iio] at hle
    exact ne_top_of_le_ne_top ENNReal.ofReal_ne_top hle
  have hIndInteg : Integrable (fun r : Set.Ioi (0 : ℝ) => s'.indicator (fun _ => C) r)
      (MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1)) := by
    rw [integrable_indicator_iff hs'meas]
    exact MeasureTheory.integrableOn_const hs'fin
  have hDomInteg : Integrable
      (fun p : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 × Set.Ioi (0 : ℝ)) =>
        s'.indicator (fun _ => C / a ^ 3) p.2)
      (MeasureTheory.volume.toSphere.prod
        (MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1))) := by
    have := (hIndInteg.div_const (a ^ 3)).comp_snd
      (MeasureTheory.volume.toSphere : MeasureTheory.Measure (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1))
    simpa [Set.indicator, div_eq_mul_inv, Function.comp_def] using this
  have hgmeas : Measurable g := by
    set φ : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 × Set.Ioi (0 : ℝ)) →
        EuclideanSpace ℝ (Fin 3) :=
      fun p => ((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))).symm p : EuclideanSpace ℝ (Fin 3))
      with hφdef
    have hcont : Continuous φ :=
      continuous_subtype_val.comp (homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))).symm.continuous
    -- The composite `K e2 e3 ∘ φ` is continuous EVERYWHERE on the domain: `φ`
    -- (the polar-coordinate inverse map) never hits `0` by construction (its
    -- codomain is literally the subtype `{0}ᶜ`), so the singularity of `K`
    -- at the origin is never reached and `contDiffAt_K` applies at every point.
    have hKcont0 : ContinuousOn (K e2 e3) ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ) := by
      intro y hy
      exact (contDiffAt_K e2 e3 hy).continuousAt.continuousWithinAt
    have hmaps : ∀ p : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 × Set.Ioi (0 : ℝ)),
        φ p ∈ ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) := by
      intro p
      show φ p ≠ 0
      rw [hφdef]
      exact ((homeomorphUnitSphereProd (EuclideanSpace ℝ (Fin 3))).symm p).2
    have hKphicont : Continuous (fun p => K e2 e3 (φ p)) :=
      hKcont0.comp_continuous hcont hmaps
    have hgeq : g = (φ ⁻¹' S).indicator (fun p => K e2 e3 (φ p)) := by
      ext p
      simp only [hg, hφdef]
      rfl
    rw [hgeq]
    exact hKphicont.measurable.indicator (hSmeas.preimage hcont.measurable)
  have hActualInteg : Integrable g
      (MeasureTheory.volume.toSphere.prod
        (MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) - 1))) := by
    apply hDomInteg.mono' hgmeas.aestronglyMeasurable
    filter_upwards with p
    rw [hgpt p]
    have hp1norm : ‖(p.1 : EuclideanSpace ℝ (Fin 3))‖ = 1 := by
      have := p.1.2
      simpa [Metric.mem_sphere, dist_zero_right] using this
    have hKle : |K e2 e3 (p.1 : EuclideanSpace ℝ (Fin 3))| ≤ C := hC (p.1 : EuclideanSpace ℝ (Fin 3)) hp1norm
    have hCnonneg : (0 : ℝ) ≤ C := le_trans (abs_nonneg _) hKle
    have ha3 : (0 : ℝ) < a ^ 3 := by positivity
    by_cases hcase : (p.2 : ℝ) ∈ Set.Ioc a b
    · rw [Set.indicator_of_mem hcase]
      have hp2mem : p.2 ∈ s' := by simpa [hs'def] using hcase
      rw [Set.indicator_of_mem hp2mem]
      have hrpos : (0 : ℝ) < p.2 := p.2.2
      have hrge : a ≤ (p.2 : ℝ) := hcase.1.le
      rw [Real.norm_eq_abs, abs_div, abs_pow, abs_of_pos hrpos]
      gcongr
    · rw [Set.indicator_of_notMem hcase]
      have hp2nmem : p.2 ∉ s' := by simpa [hs'def] using hcase
      rw [Set.indicator_of_notMem hp2nmem]
      simp
  rw [MeasureTheory.integral_prod_symm g hActualInteg]
  have hinner : ∀ r : Set.Ioi (0 : ℝ),
      (∫ θ, g (θ, r) ∂MeasureTheory.volume.toSphere) = 0 := by
    intro r
    simp_rw [hgpt]
    by_cases hcase : (r : ℝ) ∈ Set.Ioc a b
    · simp_rw [Set.indicator_of_mem hcase]
      rw [MeasureTheory.integral_div, K_mean_zero_sphereSurfaceMeasure_via_toSphere e2 e3]
      ring
    · simp_rw [Set.indicator_of_notMem hcase]
      simp
  simp_rw [hinner]
  simp

/-! ### Parte 7 — a função-teste concreta e sua parte de diferença

`φ(y) := 1 - ‖y‖`: Lipschitz de constante `1` (consequência direta de
`norm` ser `1`-Lipschitz), com `φ 0 = 1`. Concreta, radial, não-trivial
(não é a função constante) -- exatamente o tipo de função-teste pedido
pelo escopo original. -/

noncomputable def phi (y : EuclideanSpace ℝ (Fin 3)) : ℝ := 1 - ‖y‖

theorem phi_lipschitz : LipschitzWith 1 phi := by
  apply LipschitzWith.of_dist_le_mul
  intro x y
  unfold phi
  rw [Real.dist_eq, NNReal.coe_one, one_mul]
  have heq : (1 - ‖x‖) - (1 - ‖y‖) = ‖y‖ - ‖x‖ := by ring
  rw [heq]
  calc |‖y‖ - ‖x‖| = |‖x‖ - ‖y‖| := abs_sub_comm _ _
    _ ≤ ‖x - y‖ := abs_norm_sub_norm_le x y
    _ = dist x y := (dist_eq_norm x y).symm

theorem phi_zero : phi (0 : EuclideanSpace ℝ (Fin 3)) = 1 := by unfold phi; simp

/-! ### Parte 8 — convergência da integral de coroa, para uma função
absolutamente integrável na bola fechada

Fato genérico (não específico a `K`/`φ`): se `h` é integrável em
`closedBall 0 R`, então a integral de coroa `∫_{ε≤‖y‖≤R} h` converge,
quando `ε → 0⁺`, à integral sobre `closedBall 0 R \ {0}`. Via
`tendsto_setIntegral_of_monotone` (Mathlib) aplicado ao índice invertido
`(Ioi 0)ᵒᵈ` (a família de coroas CRESCE quando `ε` decresce) e
`tendsto_comp_coe_Ioi_atBot` (Mathlib,
`Topology.Order.AtTopBotIxx`) para converter o filtro de ordem `atBot`
no filtro topológico `nhdsWithin 0 (Ioi 0)` exigido por `HasLocalPV`. -/
theorem tendsto_setIntegral_annulus_of_integrableOn_closedBall
    (R : ℝ) (hR : 0 < R) (h : EuclideanSpace ℝ (Fin 3) → ℝ)
    (hint : IntegrableOn h (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R)) :
    Filter.Tendsto
      (fun ε : ℝ => ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) ε), h y)
      (nhdsWithin 0 (Set.Ioi 0))
      (nhds (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}), h y)) := by
  rw [← tendsto_comp_coe_Ioi_atBot (a := (0:ℝ))]
  set s : (Set.Ioi (0:ℝ)) → Set (EuclideanSpace ℝ (Fin 3)) :=
    fun ε => Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) (ε:ℝ) with hsdef
  show Filter.Tendsto (fun ε : Set.Ioi (0:ℝ) => ∫ y in s ε, h y) atBot (nhds _)
  have hAnti : Antitone s := by
    intro ε₁ ε₂ hle
    apply Set.sdiff_subset_sdiff_right
    exact Metric.closedBall_subset_closedBall hle
  set s' : (Set.Ioi (0:ℝ))ᵒᵈ → Set (EuclideanSpace ℝ (Fin 3)) := fun n => s (OrderDual.ofDual n)
    with hs'def
  have hMono : Monotone s' := fun n m hnm => hAnti hnm
  have hUnion : ⋃ n : (Set.Ioi (0:ℝ))ᵒᵈ, s' n =
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \ {(0 : EuclideanSpace ℝ (Fin 3))} := by
    ext y
    simp only [hs'def, hsdef, Set.mem_iUnion, Set.mem_diff, Metric.mem_closedBall,
      Set.mem_singleton_iff, dist_zero_right]
    constructor
    · rintro ⟨n, hy1, hy2⟩
      refine ⟨hy1, ?_⟩
      intro h0
      rw [h0, norm_zero] at hy2
      exact hy2 (OrderDual.ofDual n).2.le
    · rintro ⟨hyR, hy0⟩
      have hypos : 0 < ‖y‖ := lt_of_le_of_ne (norm_nonneg y) (fun heq => hy0 (by simpa using heq.symm))
      refine ⟨OrderDual.toDual ⟨‖y‖ / 2, half_pos hypos⟩, hyR, ?_⟩
      simp only [OrderDual.ofDual_toDual]
      exact not_le.mpr (by linarith)
  have hIonU : IntegrableOn h (⋃ n : (Set.Ioi (0:ℝ))ᵒᵈ, s' n) := by
    rw [hUnion]
    exact hint.mono_set (fun y hy => hy.1)
  have hmeasS : ∀ n : (Set.Ioi (0:ℝ))ᵒᵈ, MeasurableSet (s' n) := by
    intro n
    exact (Metric.isClosed_closedBall.measurableSet).diff (Metric.isClosed_closedBall.measurableSet)
  have hconv := tendsto_setIntegral_of_monotone hmeasS hMono hIonU
  rw [hUnion] at hconv
  exact hconv

/-! ## NOVO NESTA FRENTE (NS-2a)

Tudo abaixo desta linha é conteúdo genuinamente novo desta sessão -- não
é restatação de nada anteriormente fechado. Generaliza `φ` concreta
(NS-1) para `g` Lipschitz genérica, substituindo a igualdade exata
`φ y - φ 0 = -‖y‖` por um limitante de Lipschitz `|g y - g 0| ≤ L * ‖y‖`.
Ver o resumo do cabeçalho e o bloco final "O que NÃO é afirmado" para o
escopo exato. -/

/-! ### Parte 7' — a peça de diferença para uma `g` Lipschitz genérica

Generalização direta de `K_diff_integrableOn_closedBall` (NS-1, Parte 7):
em vez da igualdade exata `φ y - φ 0 = -‖y‖`, usamos apenas o limitante
de Lipschitz `|g y - g 0| ≤ L * ‖y‖`, obtido de
`LipschitzWith.dist_le_mul` reescrito via `Real.dist_eq`/`dist_eq_norm`.
A cadeia de desigualdades de `hdecay` (antes uma igualdade seguida de um
`≤`) vira uma cadeia de `≤` pura terminando em `C * L * ‖y‖ ^ (-2)`
(`Lr` abaixo denota `(L.toNNReal : ℝ)`, a constante de Lipschitz
efetiva usada por `LipschitzWith`). -/
theorem K_diff_integrableOn_closedBall_lipschitz (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (g : EuclideanSpace ℝ (Fin 3) → ℝ) (L : ℝ) (hg : LipschitzWith L.toNNReal g)
    (R : ℝ) (hR : 0 < R) :
    IntegrableOn (fun y => K e2 e3 y * (g y - g 0)) (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) := by
  obtain ⟨C₀, hC₀⟩ := K_bounded_unit_sphere e2 e3
  set C : ℝ := max C₀ 0 with hCdef
  have hCnonneg : (0:ℝ) ≤ C := le_max_right _ _
  have hC : ∀ θ : EuclideanSpace ℝ (Fin 3), ‖θ‖ = 1 → |K e2 e3 θ| ≤ C :=
    fun θ hθ => le_trans (hC₀ θ hθ) (le_max_left _ _)
  set Lr : ℝ := (L.toNNReal : ℝ) with hLrdef
  have hLrnonneg : (0:ℝ) ≤ Lr := L.toNNReal.coe_nonneg
  -- Measurability: `K e2 e3` is continuous away from `0` (`contDiffAt_K`),
  -- hence measurable everywhere; `g` is globally Lipschitz hence continuous.
  have hKmeas : Measurable (K e2 e3) := by
    apply measurable_of_continuousOn_compl_singleton (0 : EuclideanSpace ℝ (Fin 3))
    intro y hy
    exact (contDiffAt_K e2 e3 hy).continuousAt.continuousWithinAt
  have hmeas : AEStronglyMeasurable (fun y => K e2 e3 y * (g y - g 0))
      (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) :=
    (hKmeas.aestronglyMeasurable).mul
      ((hg.continuous.sub continuous_const).aestronglyMeasurable)
  -- Pointwise Lipschitz bound on the difference piece: `|g y - g 0| ≤ Lr * ‖y‖`.
  have hgdiff : ∀ y : EuclideanSpace ℝ (Fin 3), |g y - g 0| ≤ Lr * ‖y‖ := by
    intro y
    have hd := hg.dist_le_mul y 0
    rw [Real.dist_eq, dist_eq_norm, sub_zero] at hd
    exact hd
  -- Pointwise decay bound, valid for EVERY `y` (not just a.e.): at `y = 0`
  -- both sides are literally `0`; away from `0`, `K_homogeneous` converts
  -- `|K e2 e3 y|` into `|K e2 e3 (yHat y)| / ‖y‖^3 ≤ C / ‖y‖^3`, and the
  -- Lipschitz bound gives `|g y - g 0| ≤ Lr * ‖y‖`, so the PRODUCT is
  -- bounded by `(C / ‖y‖^3) * (Lr * ‖y‖) = C * Lr * ‖y‖^(-2)` -- a `≤`
  -- chain throughout, in place of NS-1's equality-based chain.
  have hdecay : ∀ y : EuclideanSpace ℝ (Fin 3),
      ‖K e2 e3 y * (g y - g 0)‖ ≤ C * Lr * ‖y‖ ^ (-(2:ℝ)) := by
    intro y
    by_cases hy : y = 0
    · subst hy
      simp only [sub_self, mul_zero, norm_zero]
      have : (0:ℝ) ≤ C * Lr * (0:ℝ) ^ (-(2:ℝ)) := by positivity
      exact this
    · have hynorm : (0:ℝ) < ‖y‖ := norm_pos_iff.mpr hy
      have hyhat_norm : ‖yHat y‖ = 1 := by
        unfold yHat
        rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hynorm)]
        field_simp
      have hyhat_ne : yHat y ≠ 0 := by
        intro h; rw [h, norm_zero] at hyhat_norm; norm_num at hyhat_norm
      have hsmul_eq : ‖y‖ • yHat y = y := by
        unfold yHat
        rw [smul_smul, mul_inv_cancel₀ hynorm.ne', one_smul]
      have hKhom2 := K_homogeneous e2 e3 (yHat y) hyhat_ne ‖y‖ hynorm
      rw [hsmul_eq] at hKhom2
      -- `hKhom2 : ‖y‖ ^ 3 * K e2 e3 y = K e2 e3 (yHat y)`
      have hKle : |K e2 e3 y| ≤ C / ‖y‖ ^ 3 := by
        have hy3pos : (0:ℝ) < ‖y‖ ^ 3 := by positivity
        rw [le_div_iff₀ hy3pos]
        calc |K e2 e3 y| * ‖y‖ ^ 3 = |K e2 e3 y * ‖y‖ ^ 3| := by
              rw [abs_mul, abs_of_nonneg (by positivity : (0:ℝ) ≤ ‖y‖ ^ 3)]
          _ = |‖y‖ ^ 3 * K e2 e3 y| := by ring_nf
          _ = |K e2 e3 (yHat y)| := by rw [hKhom2]
          _ ≤ C := hC _ hyhat_norm
      have hrpow : (C / ‖y‖ ^ 3) * (Lr * ‖y‖) = C * Lr * ‖y‖ ^ (-(2:ℝ)) := by
        rw [Real.rpow_neg (norm_nonneg y), show (2:ℝ) = ((2:ℕ):ℝ) from by norm_num,
          Real.rpow_natCast]
        have hy3ne : (‖y‖ ^ 3 : ℝ) ≠ 0 := by positivity
        have hy2ne : (‖y‖ ^ 2 : ℝ) ≠ 0 := by positivity
        field_simp
      calc ‖K e2 e3 y * (g y - g 0)‖ = |K e2 e3 y| * |g y - g 0| := by
            rw [Real.norm_eq_abs, abs_mul]
        _ ≤ (C / ‖y‖ ^ 3) * (Lr * ‖y‖) := by
            apply mul_le_mul hKle (hgdiff y) (abs_nonneg _)
            positivity
        _ = C * Lr * ‖y‖ ^ (-(2:ℝ)) := hrpow
  have hint_bigger : IntegrableOn (fun y => K e2 e3 y * (g y - g 0))
      (Metric.ball (0 : EuclideanSpace ℝ (Fin 3)) (R + 1)) MeasureTheory.volume :=
    MeasureTheory.integrableOn_ball_of_norm_le_rpow (E := EuclideanSpace ℝ (Fin 3))
      (μ := MeasureTheory.volume) (by simp) (by norm_num : (2:ℝ) < (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) : ℝ))
      (Filter.Eventually.of_forall (fun y => hdecay y)) hmeas
  exact hint_bigger.mono_set (Metric.closedBall_subset_ball (by linarith))

/-! ### Parte 9' — o teorema-alvo generalizado: `HasLocalPV` para `K e2 e3 · g`,
`g` Lipschitz genérica

**Item central desta frente**: mesma combinação de NS-1 Partes 6
(`K_shell_integral_eq_zero`, cancelamento exato em toda coroa), 7'
(`K_diff_integrableOn_closedBall_lipschitz`, integrabilidade absoluta da
diferença -- agora via desigualdade de Lipschitz, não igualdade exata) e
8 (`tendsto_setIntegral_annulus_of_integrableOn_closedBall`, convergência
genérica da integral de coroa), mas para QUALQUER `g` Lipschitz (não só
a `φ` concreta de NS-1). A prova é idêntica à de `hasLocalPV_K_mul_phi`
na estrutura; a única mudança é que `hKdiffIntS` agora vem de
`K_diff_integrableOn_closedBall_lipschitz` em vez de
`K_diff_integrableOn_closedBall`. -/
theorem hasLocalPV_K_mul_lipschitz (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (g : EuclideanSpace ℝ (Fin 3) → ℝ) (L : ℝ) (hg : LipschitzWith L.toNNReal g)
    (R : ℝ) (hR : 0 < R) :
    HasLocalPV (fun y => K e2 e3 y * g y) (0 : EuclideanSpace ℝ (Fin 3)) R
      (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * (g y - g 0)) := by
  unfold HasLocalPV
  have heventually : ∀ᶠ ε in nhdsWithin (0:ℝ) (Set.Ioi 0),
      (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) ε), K e2 e3 y * g y)
      = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) ε), K e2 e3 y * (g y - g 0) := by
    have hmemIoo : Set.Ioo (0:ℝ) R ∈ nhdsWithin (0:ℝ) (Set.Ioi 0) :=
      Ioo_mem_nhdsGT hR
    filter_upwards [hmemIoo] with ε hε
    have hεpos : 0 < ε := hε.1
    have hεR : ε < R := hε.2
    set S : Set (EuclideanSpace ℝ (Fin 3)) := Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) ε with hS
    have hSmeas : MeasurableSet S :=
      (Metric.isClosed_closedBall.measurableSet).diff (Metric.isClosed_closedBall.measurableSet)
    have hsplit : ∀ y, K e2 e3 y * g y
        = K e2 e3 y * (g y - g 0) + g 0 * K e2 e3 y := by
      intro y; ring
    have hSsub : S ⊆ Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R := fun y hy => hy.1
    have hKcont0 : ContinuousOn (K e2 e3) ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ) := by
      intro y hy
      exact (contDiffAt_K e2 e3 hy).continuousAt.continuousWithinAt
    have hSsub0compl : S ⊆ ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) := by
      intro y hy
      show y ≠ 0
      intro h0
      rw [hS, h0] at hy
      exact absurd (Metric.mem_closedBall_self hεpos.le) hy.2
    have hSvol : (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) S ≠ ⊤ :=
      (lt_of_le_of_lt (MeasureTheory.measure_mono hSsub) measure_closedBall_lt_top).ne
    have hKintS : IntegrableOn (K e2 e3) S := by
      obtain ⟨C, hCnonneg, hCbound⟩ := K_abs_le_div_norm_pow e2 e3
      have hconstInt : IntegrableOn (fun _ : EuclideanSpace ℝ (Fin 3) => C / ε ^ 3) S := by
        exact MeasureTheory.integrableOn_const hSvol
      apply hconstInt.mono' ((hKcont0.mono hSsub0compl).aestronglyMeasurable hSmeas)
      filter_upwards [ae_restrict_mem hSmeas] with y hy
      have hy0 : y ≠ 0 := hSsub0compl hy
      have hynorm : ε < ‖y‖ := by
        have := hy.2
        rw [hS] at hy
        simp only [Set.mem_diff, Metric.mem_closedBall, dist_zero_right, not_le] at hy
        exact hy.2
      have hεnn : (0:ℝ) < ε ^ 3 := by positivity
      have hynn : (0:ℝ) < ‖y‖ ^ 3 := by positivity
      rw [Real.norm_eq_abs]
      calc |K e2 e3 y| ≤ C / ‖y‖ ^ 3 := hCbound y hy0
        _ ≤ C / ε ^ 3 := by gcongr
    have hKdiffIntS : IntegrableOn (fun y => K e2 e3 y * (g y - g 0)) S :=
      (K_diff_integrableOn_closedBall_lipschitz e2 e3 g L hg R hR).mono_set hSsub
    have hgKIntS : IntegrableOn (fun y => g 0 * K e2 e3 y) S := hKintS.const_mul (g 0)
    calc (∫ y in S, K e2 e3 y * g y)
        = ∫ y in S, (K e2 e3 y * (g y - g 0) + g 0 * K e2 e3 y) := by
          apply setIntegral_congr_fun hSmeas
          intro y _
          exact hsplit y
      _ = (∫ y in S, K e2 e3 y * (g y - g 0)) + ∫ y in S, g 0 * K e2 e3 y :=
          MeasureTheory.integral_add hKdiffIntS hgKIntS
      _ = (∫ y in S, K e2 e3 y * (g y - g 0)) + g 0 * ∫ y in S, K e2 e3 y := by
          rw [MeasureTheory.integral_const_mul]
      _ = (∫ y in S, K e2 e3 y * (g y - g 0)) + g 0 * 0 := by
          rw [hS, K_shell_integral_eq_zero e2 e3 ε R hεpos hεR]
      _ = ∫ y in S, K e2 e3 y * (g y - g 0) := by ring
  have hlim := tendsto_setIntegral_annulus_of_integrableOn_closedBall R hR
    (fun y => K e2 e3 y * (g y - g 0))
    (K_diff_integrableOn_closedBall_lipschitz e2 e3 g L hg R hR)
  exact Filter.Tendsto.congr' (heventually.mono (fun ε h => h.symm)) hlim

/-! ### Parte 10' — instância de sanidade: recupera o resultado de NS-1
como caso particular

`φ` (`y ↦ 1 - ‖y‖`) é Lipschitz de constante `1`
(`phi_lipschitz : LipschitzWith 1 phi`, restatada verbatim acima).
`(1:ℝ).toNNReal = 1`, então `hasLocalPV_K_mul_lipschitz` instanciada em
`g := phi`, `L := 1` reproduz exatamente a conclusão de
`hasLocalPV_K_mul_phi` (NS-1) -- confirmando que a generalização desta
frente não perdeu o caso concreto já fechado. `phi_lipschitz` é
reaproveitada aqui SOMENTE para fornecer a hipótese de Lipschitz (o
papel de mensurabilidade/continuidade que o teste pedia). -/
theorem hasLocalPV_K_mul_phi_via_lipschitz (e2 e3 : EuclideanSpace ℝ (Fin 3)) (R : ℝ) (hR : 0 < R) :
    HasLocalPV (fun y => K e2 e3 y * phi y) (0 : EuclideanSpace ℝ (Fin 3)) R
      (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * (phi y - phi 0)) := by
  have hg : LipschitzWith (1:ℝ).toNNReal phi := by
    rw [Real.toNNReal_one]
    exact phi_lipschitz
  exact hasLocalPV_K_mul_lipschitz e2 e3 phi 1 hg R hR

end TamesisNSLocalPVLipschitz

/-! ## O que NÃO é afirmado

```text
NÃO prova nenhuma limitação L^p de operador integral singular
NÃO prova nenhum teorema de Calderón-Zygmund (decomposição, tipo-fraco,
  interpolação de Marcinkiewicz)
NÃO constrói nenhuma distribuição de valor principal (nenhuma
  continuidade-em-topologia, nenhuma reivindicação de linearidade como
  operador em 𝓓' -- `HasLocalPV` é apenas uma Prop sobre um limite
  pontual real, não um termo do framework `Mathlib.Analysis.Distribution`)
NÃO trata uma função-teste genérica de Schwartz/C^∞_c -- só funções
  `g` GLOBALMENTE Lipschitz de constante `L` finita (`e2`, `e3`
  continuam fixos, "coeficientes congelados", exatamente como em
  NS-1/`FOUND-CZ-KERNEL-DEFINITIONS-001`/`FOUND-CZ-MEAN-ZERO-001`)
NÃO prova nada sobre a integral p.v. real das equações (2.1)/(2.2) de
  Constantin-Fefferman aplicada a um campo de vorticidade genuíno
NÃO prova NS-GAP-001/004 nem qualquer regularidade condicional real
NÃO afirma que Navier-Stokes ficou alcançável, aproximável, ou resolvido
NÃO afirma novidade matemática -- a generalização de uma igualdade
  exata (válida só para `φ(y) = 1 - ‖y‖`) para uma desigualdade de
  Lipschitz genérica é um relaxamento de hipótese completamente
  padrão em análise (o mesmo argumento clássico de Calderón-Zygmund,
  ver Grafakos, agora aplicado à classe MAIOR das funções Lipschitz
  em vez de a uma única função-teste concreta); a única coisa nova é a
  formalização Lean desse relaxamento
```

## Resumo do que esta frente FECHOU

O teste (WAVE2-NS-2A) pedia: declarar `hasLocalPV_K_mul_lipschitz` para
`g` Lipschitz genérica (`hg : LipschitzWith L.toNNReal g`), substituindo
a igualdade exata `hphidiff` (NS-1) pelo limitante
`|g y - g 0| ≤ L * ‖y‖` (via `LipschitzWith.dist_le_mul` +
`dist_eq_norm`), e reescrevendo `hnormeq`/o `calc` final de `hdecay`
como uma cadeia de `≤` terminando em `C * L * ‖y‖ ^ (-2)`, mantendo
`phi_lipschitz` apenas para mensurabilidade/continuidade. Isso fechou
sem obstáculo: a prova de NS-1 (`K_diff_integrableOn_closedBall`,
`hasLocalPV_K_mul_phi`) usava a igualdade exata só em DOIS pontos
localizados -- `hnormeq` (agora `hgdiff`/uma desigualdade) e o `calc`
final de `hdecay` (agora uma cadeia `≤` de três passos em vez de
igualdade-seguida-de-≤) -- e nenhuma outra parte da prova (medibilidade,
o limitante de `K`, `integrableOn_ball_of_norm_le_rpow`, o cancelamento
de casca via `K_shell_integral_eq_zero`, a convergência da integral de
coroa) dependia da igualdade exata. `K_diff_integrableOn_closedBall_lipschitz`
e `hasLocalPV_K_mul_lipschitz` (Partes 7'/9') são a generalização
completa; `hasLocalPV_K_mul_phi_via_lipschitz` (Parte 10') confirma que
o caso concreto de NS-1 é recuperado exatamente como corolário
(`L := 1`, `g := phi`, reaproveitando `phi_lipschitz` só como hipótese
de Lipschitz).

Fontes citadas (mesmas de NS-1, ver `CalderonZygmundLocalPVExistence.lean`):
- P. Constantin, C. Fefferman, "Direction of vorticity and the problem
  of global regularity for the Navier-Stokes equations", Indiana Univ.
  Math. J. 42 (1993), 775-789.
- Siran Li, "On Vortex Alignment and Boundedness of L^q Norm of
  Vorticity", Acta Math. Sci. 40(6) (2020), 1700-1708, arXiv:1712.00551,
  eq. 2.1-2.3.
- Loukas Grafakos, *Classical Fourier Analysis*, 3ª ed., Springer GTM
  249, 2014, §5.1.4 e §5.2.1-5.2.2.
- `MeasureTheory.Measure.toSphere`,
  `MeasureTheory.Measure.measurePreserving_homeomorphUnitSphereProd`,
  Yury Kudryashov, `Mathlib.MeasureTheory.Constructions.HaarToSphere`.
- `LinearIsometryEquiv.measurePreserving`, Sébastien Gouëzel,
  `Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace`.
- `MeasureTheory.integrableOn_ball_of_norm_le_rpow`, Kalle Kytölä,
  `Mathlib.Analysis.SpecialFunctions.Pow.Integral`.
- `tendsto_comp_coe_Ioi_atBot`, `Mathlib.Topology.Order.AtTopBotIxx`.
- `LipschitzWith.dist_le_mul`, `Mathlib.Topology.MetricSpace.Lipschitz`
  (mecanismo novo desta frente: a ponte entre a hipótese de Lipschitz
  genérica e o limitante pontual `|g y - g 0| ≤ L * ‖y‖`).
-/

#print axioms TamesisNSLocalPVLipschitz.tripleProduct
#print axioms TamesisNSLocalPVLipschitz.D
#print axioms TamesisNSLocalPVLipschitz.HasLocalPV.unique
#print axioms TamesisNSLocalPVLipschitz.hasLocalPV_zero
#print axioms TamesisNSLocalPVLipschitz.sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.yHat_smul_of_pos
#print axioms TamesisNSLocalPVLipschitz.K_homogeneous
#print axioms TamesisNSLocalPVLipschitz.contDiff_D_fst
#print axioms TamesisNSLocalPVLipschitz.contDiffAt_yHat
#print axioms TamesisNSLocalPVLipschitz.contDiffAt_K
#print axioms TamesisNSLocalPVLipschitz.tripleProduct_self_left
#print axioms TamesisNSLocalPVLipschitz.integral_D_eq_zero_of_isotropicSecondMoment
#print axioms TamesisNSLocalPVLipschitz.volume_image_linearIsometryEquiv
#print axioms TamesisNSLocalPVLipschitz.image_smul_Ioo_linearIsometryEquiv
#print axioms TamesisNSLocalPVLipschitz.mapsTo_sphere
#print axioms TamesisNSLocalPVLipschitz.sphereMap
#print axioms TamesisNSLocalPVLipschitz.sphereMap_continuous
#print axioms TamesisNSLocalPVLipschitz.sphereMap_measurable
#print axioms TamesisNSLocalPVLipschitz.image_val_preimage_sphereMap
#print axioms TamesisNSLocalPVLipschitz.preimage_eq_image_symm
#print axioms TamesisNSLocalPVLipschitz.toSphere_map_sphereMap
#print axioms TamesisNSLocalPVLipschitz.sphereSurfaceMeasure_map_linearIsometryEquiv
#print axioms TamesisNSLocalPVLipschitz.ae_mem_sphere_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.instIsFiniteMeasure_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.integrable_coord_mul_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.flipCoord
#print axioms TamesisNSLocalPVLipschitz.flipCoord_apply_self
#print axioms TamesisNSLocalPVLipschitz.flipCoord_apply_other
#print axioms TamesisNSLocalPVLipschitz.permCoord
#print axioms TamesisNSLocalPVLipschitz.permCoord_apply
#print axioms TamesisNSLocalPVLipschitz.integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.integral_offdiag_eq_zero_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.integral_diag_eq_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.sphereSurfaceMeasure_isotropicSecondMoment
#print axioms TamesisNSLocalPVLipschitz.K_mean_zero_sphereSurfaceMeasure
#print axioms TamesisNSLocalPVLipschitz.K_bounded_unit_sphere
#print axioms TamesisNSLocalPVLipschitz.K_abs_le_div_norm_pow
#print axioms TamesisNSLocalPVLipschitz.K_mean_zero_sphereSurfaceMeasure_via_toSphere
#print axioms TamesisNSLocalPVLipschitz.K_shell_integral_eq_zero
#print axioms TamesisNSLocalPVLipschitz.phi
#print axioms TamesisNSLocalPVLipschitz.phi_lipschitz
#print axioms TamesisNSLocalPVLipschitz.phi_zero
#print axioms TamesisNSLocalPVLipschitz.tendsto_setIntegral_annulus_of_integrableOn_closedBall

-- NOVO NESTA FRENTE (NS-2a) -- declarações novas desta sessão
#print axioms TamesisNSLocalPVLipschitz.K_diff_integrableOn_closedBall_lipschitz
#print axioms TamesisNSLocalPVLipschitz.hasLocalPV_K_mul_lipschitz
#print axioms TamesisNSLocalPVLipschitz.hasLocalPV_K_mul_phi_via_lipschitz
