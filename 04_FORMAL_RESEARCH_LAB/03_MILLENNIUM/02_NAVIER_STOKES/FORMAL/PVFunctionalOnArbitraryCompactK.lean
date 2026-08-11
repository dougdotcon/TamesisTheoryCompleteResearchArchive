/-
NS-4A (Wave-4, item WAVE4-NS-4A) — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`CalderonZygmundKernelDefinitions.lean`, `CalderonZygmundLocalPVExistence.lean`
(NS-1, Wave-1), `K_LipschitzDifference_HasLocalPV.lean` (NS-2a, Wave-2),
`PVDistributionOnCompactK.lean` (NS-2b, Wave-2) e
`RadiusIndependencePVLipschitz.lean` (NS-3a, Wave-3), mesma pasta:
arquivo Lean autônomo, verificado via `lake env lean` diretamente contra
o mesmo projeto Mathlib, fora da árvore de import compartilhada. Wave-4
é follow-on direto de Wave-3 (15 itens fechados) e Waves 1-2 antes dela;
item NS-4a do plano `01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md`.

## O que esta frente tenta, e por que

`PVDistributionOnCompactK.lean` (NS-2b) constrói `pvKCLM e2 e3 R hR :
𝓓^{1}_{K}(E, ℝ) →L[ℝ] ℝ` para UM único compacto FIXO `K = closedBall 0
R`. A própria seção "O que NÃO é afirmado" de NS-2b nomeia dois gaps
explícitos para estender isso a um `TestFunction.mkCLM` genuíno: (i)
independência do valor de `pvK` em relação ao raio `R` escolhido, para
DOIS raios distintos simultaneamente; (ii) estender a construção de
`K = closedBall 0 R` para um compacto GENÉRICO `K'` (não necessariamente
uma bola), usando (i) para reduzir ao caso de uma bola que contém `K'`.
`RadiusIndependencePVLipschitz.lean` (NS-3a, Wave-3) já fechou o gap (i)
(`pv_value_radius_independent`, para `g` Lipschitz eventualmente
constante além de um raio `R1`). Esta frente (NS-4a) fecha o gap (ii)
sozinho: para um compacto ARBITRÁRIO `K' : Compacts E`, compor `pvKCLM`
(sobre uma bola-envelope `closedBall 0 R` que contém `K'`) com
`ContDiffMapSupportedIn.monoCLM` (Mathlib, a inclusão contínua-linear de
`𝓓^{n₁}_{K₁}(E,F)` dentro de `𝓓^{n₂}_{K₂}(E,F)` quando `n₂ ≤ n₁` e
`K₁ ≤ K₂`) para obter um funcional p.v. contínuo-linear sobre `K'`
propriamente dito, `𝓓^{1}_{K'}(E, ℝ) →L[ℝ] ℝ` — não é literalmente um
NOVO `ContinuousLinearMap` primitivo, mas a COMPOSIÇÃO
`pvKCLM e2 e3 R hR ∘L monoCLM ℝ`, cuja continuidade linear vem de graça
(composição de `ContinuousLinearMap`s) — e então mostrar que o VALOR
desse composto não depende da escolha do raio-envelope `R` (para
quaisquer dois raios `R1, R2 > 0` tais que `K' ⊆ closedBall 0 R1` e
`K' ⊆ closedBall 0 R2`), via `pv_value_radius_independent` de NS-3a
aplicado com `(min R1 R2, max R1 R2)` (pois esse lema exige raio-menor
`<` raio-maior estrito, então é preciso um `wlog`/case-split sobre qual
dos dois raios envolventes é o menor).

Isso fecha o gap (ii) da seção "O que NÃO é afirmado" de NS-2b, mas NÃO
monta a construção completa via `TestFunction.mkCLM`/`TestFunction.limitCLM`
(o "gap (iii)" nomeado no plano de ataque da Onda 4: montagem GLOBAL de
um elemento de `𝓓'^{1}(E,ℝ) →L[ℝ] ℝ` usando a família compatível
`{pvK' : K' compacto}` construída aqui como as peças — a obrigação de
prova exata de `TestFunction.mkCLM`/`toFun_eq_T` para reunir essas peças
em UM único funcional sobre TODO `𝓓^{1}(E,ℝ)` não é tentada nesta
sessão). Ver bloco final "O que NÃO é afirmado" para o registro preciso
desse escopo.

## Restatação verbatim (ver nota de isolamento em cada arquivo irmão)

Por ser um arquivo autônomo fora da árvore `05_FORMAL/lean/`, este
arquivo NÃO pode `import` `PVDistributionOnCompactK.lean` nem
`RadiusIndependencePVLipschitz.lean` (sem `.olean` em `LEAN_PATH`). Todo
o conteúdo até a seção "NOVO NESTA FRENTE (NS-4a)" é uma restatação
VERBATIM (mesma definição, mesma prova) do conteúdo já fechado e
independentemente verificado em NS-1/NS-2a/NS-2b/NS-3a
(`tripleProduct`, `D`, `sphereSurfaceMeasure`, `K`, `yHat`,
`K_homogeneous`, `K_bounded_unit_sphere`, `K_abs_le_div_norm_pow`,
`K_shell_integral_eq_zero`, `K_diff_integrableOn_closedBall_lipschitz`,
toda a maquinaria de `mean_zero` que os sustenta
(`tripleProduct_self_left`, `IsotropicSecondMoment`,
`integral_D_eq_zero_of_isotropicSecondMoment`, os lemas de isometria
linear/mapa de esfera, `flipCoord`/`permCoord`, e
`K_mean_zero_sphereSurfaceMeasure(_via_toSphere)`),
`lipschitzWith_seminorm_of_contDiffMapSupportedIn`,
`const_mul_rpow_neg_two_integrableOn_closedBall`, `pvKCompact`,
`pvKLM`/`pvKLM_apply`, `pvKCLM`/`pvKCLM_apply` (de NS-2b), e
`K_diff_shell_integral_eq_zero`/`pv_value_radius_independent` (de
NS-3a). NÃO é uma nova alegação matemática. As partes específicas de
`HasLocalPV` (definição, `HasLocalPV.unique`, `hasLocalPV_zero`,
`hasLocalPV_K_mul_lipschitz`, `tendsto_setIntegral_annulus_of_...`) e a
função-teste concreta `φ` de NS-1 são OMITIDAS aqui pelo mesmo motivo
que em NS-3a: não são necessárias ao conteúdo novo desta frente — nem
`pvKCLM`, nem `pvKCLM_apply`, nem `pv_value_radius_independent`
referenciam `HasLocalPV` em sua prova (verificado linha a linha contra
os arquivos-fonte antes de omitir). A seção "NOVO NESTA FRENTE (NS-4a)"
é o único conteúdo genuinamente novo desta sessão:
`pvKCLM_comp_monoCLM_eq_integral` (a composição reproduz a mesma fórmula
integral) e `pvKCLM_comp_monoCLM_radius_independent` (o teorema-alvo,
independência do valor do composto em relação ao raio-envelope
escolhido).
-/

import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Angle.Unoriented.CrossProduct
import Mathlib.LinearAlgebra.CrossProduct
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Normed.Lp.MeasurableSpace
import Mathlib.MeasureTheory.Measure.Haar.OfBasis
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Analysis.Normed.Lp.PiLp
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Analysis.SpecialFunctions.Pow.Integral
import Mathlib.Topology.Order.AtTopBotIxx
import Mathlib.Analysis.Distribution.TestFunction
import Mathlib.Tactic

namespace TamesisNSPVFunctionalOnArbitraryK

open Matrix InnerProductGeometry MeasureTheory Set Filter Topology TopologicalSpace WithSeminorms
open scoped Pointwise Distributions

/-! ## Parte 0 — restatação verbatim de `D` (núcleo de Constantin-Fefferman) -/

noncomputable def tripleProduct (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 (WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3))

noncomputable def D (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 e3 * tripleProduct e1 e2 e3

/-! ## Parte 1 — restatação verbatim: `sphereSurfaceMeasure` -/

noncomputable def sphereSurfaceMeasure :
    MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3)) :=
  MeasureTheory.Measure.map
    ((↑) : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) →
      EuclideanSpace ℝ (Fin 3))
    (MeasureTheory.volume.toSphere)

/-! ## Parte 2 — restatação verbatim: `K` (peça de coeficiente congelado) -/

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

/-! ## Parte 3 — restatação verbatim: fechamento de `mean_zero` -/

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

/-! ## Parte 4 — restatação verbatim: `K e2 e3` é limitado na esfera unitária -/

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

/-! ## Parte 5 — restatação verbatim: cancelamento de casca esférica genérica -/

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
  have step1 : ∫ y in S, K e2 e3 y = ∫ y, S.indicator (K e2 e3) y :=
    (MeasureTheory.integral_indicator hSmeas).symm
  have step2 : (∫ y, S.indicator (K e2 e3) y)
      = ∫ x : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))),
          S.indicator (K e2 e3) x.1
          ∂(MeasureTheory.volume.comap
            ((↑) : ({(0 : EuclideanSpace ℝ (Fin 3))}ᶜ : Set (EuclideanSpace ℝ (Fin 3))) →
              EuclideanSpace ℝ (Fin 3))) := by
    rw [MeasureTheory.integral_subtype_comap (measurableSet_singleton (0 : EuclideanSpace ℝ (Fin 3))).compl
      (S.indicator (K e2 e3))]
    rw [restrict_compl_singleton]
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

/-! ## Parte 6 — restatação verbatim: integrabilidade da peça de diferença
para `g` Lipschitz genérica (NS-2a, Parte 7') -/

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
  have hKmeas : Measurable (K e2 e3) := by
    apply measurable_of_continuousOn_compl_singleton (0 : EuclideanSpace ℝ (Fin 3))
    intro y hy
    exact (contDiffAt_K e2 e3 hy).continuousAt.continuousWithinAt
  have hmeas : AEStronglyMeasurable (fun y => K e2 e3 y * (g y - g 0))
      (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) :=
    (hKmeas.aestronglyMeasurable).mul
      ((hg.continuous.sub continuous_const).aestronglyMeasurable)
  have hgdiff : ∀ y : EuclideanSpace ℝ (Fin 3), |g y - g 0| ≤ Lr * ‖y‖ := by
    intro y
    have hd := hg.dist_le_mul y 0
    rw [Real.dist_eq, dist_eq_norm, sub_zero] at hd
    exact hd
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

/-! ## Parte 7 — restatação verbatim (NS-2b): empacotamento como
`ContinuousLinearMap` para um único compacto FIXO `K = closedBall 0 R` -/

open ContDiffMapSupportedIn in
/-- Restatação verbatim de NS-2b: qualquer `f ∈ 𝓓^{1}_{K}(E, ℝ)` (C¹,
globalmente, anulando-se fora do compacto `K`) é globalmente Lipschitz em
`E`, com constante de Lipschitz efetiva limitada pela seminorma
`N[ℝ]_{K, 1, 1} f`. Já genérica em QUALQUER compacto `K` -- não só bolas
-- o que esta frente reaproveita diretamente para `K'` arbitrário. -/
theorem lipschitzWith_seminorm_of_contDiffMapSupportedIn
    {K : Compacts (EuclideanSpace ℝ (Fin 3))}
    (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K) :
    LipschitzWith (Real.toNNReal (N[ℝ]_{K, (1:ℕ∞), 1} f)) (f : EuclideanSpace ℝ (Fin 3) → ℝ) := by
  have hdiff : Differentiable ℝ (f : EuclideanSpace ℝ (Fin 3) → ℝ) :=
    f.contDiff.differentiable (one_ne_zero)
  have hbound : ∀ x : EuclideanSpace ℝ (Fin 3),
      ‖fderiv ℝ (f : EuclideanSpace ℝ (Fin 3) → ℝ) x‖ ≤ N[ℝ]_{K, (1:ℕ∞), 1} f := by
    intro x
    by_cases hx : x ∈ (K : Set (EuclideanSpace ℝ (Fin 3)))
    · rw [← norm_iteratedFDeriv_one]
      exact ContDiffMapSupportedIn.norm_iteratedFDeriv_apply_le_seminorm ℝ (le_refl (1 : ℕ∞))
    · have hKopen : IsOpen (K : Set (EuclideanSpace ℝ (Fin 3)))ᶜ :=
        K.isCompact.isClosed.isOpen_compl
      have hnhds : (K : Set (EuclideanSpace ℝ (Fin 3)))ᶜ ∈ nhds x := hKopen.mem_nhds hx
      have heqnear : (f : EuclideanSpace ℝ (Fin 3) → ℝ) =ᶠ[nhds x] (0 : EuclideanSpace ℝ (Fin 3) → ℝ) :=
        Filter.eventually_of_mem hnhds (fun y hy => f.zero_on_compl hy)
      have hfd0 : fderiv ℝ (f : EuclideanSpace ℝ (Fin 3) → ℝ) x = fderiv ℝ (0 : EuclideanSpace ℝ (Fin 3) → ℝ) x :=
        Filter.EventuallyEq.fderiv_eq heqnear
      rw [hfd0, fderiv_zero]
      simpa using apply_nonneg (N[ℝ]_{K, (1:ℕ∞), 1}) f
  have hboundnn : ∀ x : EuclideanSpace ℝ (Fin 3),
      ‖fderiv ℝ (f : EuclideanSpace ℝ (Fin 3) → ℝ) x‖₊ ≤ Real.toNNReal (N[ℝ]_{K, (1:ℕ∞), 1} f) := by
    intro x
    rw [← NNReal.coe_le_coe]
    push_cast
    rw [Real.coe_toNNReal _ (apply_nonneg _ f)]
    exact hbound x
  exact lipschitzWith_of_nnnorm_fderiv_le hdiff hboundnn

/-- Restatação verbatim de NS-2b: domínio da função-Lipschitz de decaimento
constante `C * ‖y‖^(-2)` sobre `closedBall 0 R`. -/
theorem const_mul_rpow_neg_two_integrableOn_closedBall (C : ℝ) (hC : 0 ≤ C) (R : ℝ) (hR : 0 < R) :
    IntegrableOn (fun y : EuclideanSpace ℝ (Fin 3) => C * ‖y‖ ^ (-(2:ℝ)))
      (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) := by
  have hmeas : AEStronglyMeasurable (fun y : EuclideanSpace ℝ (Fin 3) => C * ‖y‖ ^ (-(2:ℝ)))
      (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) := by
    apply Measurable.aestronglyMeasurable
    exact (measurable_norm.pow_const _ |>.const_mul C : Measurable
      (fun y : EuclideanSpace ℝ (Fin 3) => C * ‖y‖ ^ (-(2:ℝ))))
  have hbig : IntegrableOn (fun y : EuclideanSpace ℝ (Fin 3) => C * ‖y‖ ^ (-(2:ℝ)))
      (Metric.ball (0 : EuclideanSpace ℝ (Fin 3)) (R + 1)) MeasureTheory.volume :=
    MeasureTheory.integrableOn_ball_of_norm_le_rpow (E := EuclideanSpace ℝ (Fin 3))
      (μ := MeasureTheory.volume) (by simp)
      (by norm_num : (2:ℝ) < (Module.finrank ℝ (EuclideanSpace ℝ (Fin 3)) : ℝ))
      (Filter.Eventually.of_forall (fun y => le_of_eq (by
        rw [Real.norm_eq_abs, abs_of_nonneg (by positivity : (0:ℝ) ≤ C * ‖y‖ ^ (-(2:ℝ)))])))
      hmeas
  exact hbig.mono_set (Metric.closedBall_subset_ball (by linarith))

variable (e2 e3 : EuclideanSpace ℝ (Fin 3)) (R : ℝ) (hR : 0 < R)

/-- Restatação verbatim de NS-2b: o compacto fixo `K = closedBall 0 R`
usado como a bola-envelope para `pvKCLM`. -/
noncomputable def pvKCompact : Compacts (EuclideanSpace ℝ (Fin 3)) :=
  ⟨Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R, isCompact_closedBall _ _⟩

/-- Restatação verbatim de NS-2b: o funcional linear subjacente a
`pvKCLM`. -/
noncomputable def pvKLM :
    ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R) →ₗ[ℝ] ℝ where
  toFun f := ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
      {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0)
  map_add' f g := by
    have hIf : IntegrableOn (fun y => K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0))
        (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) :=
      K_diff_integrableOn_closedBall_lipschitz e2 e3 f (N[ℝ]_{pvKCompact R, (1:ℕ∞), 1} f)
        (lipschitzWith_seminorm_of_contDiffMapSupportedIn f) R hR
    have hIg : IntegrableOn (fun y => K e2 e3 y * ((g : EuclideanSpace ℝ (Fin 3) → ℝ) y - g 0))
        (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) :=
      K_diff_integrableOn_closedBall_lipschitz e2 e3 g (N[ℝ]_{pvKCompact R, (1:ℕ∞), 1} g)
        (lipschitzWith_seminorm_of_contDiffMapSupportedIn g) R hR
    have hIf' := hIf.mono_set (diff_subset (t := ({(0 : EuclideanSpace ℝ (Fin 3))} :
      Set (EuclideanSpace ℝ (Fin 3)))))
    have hIg' := hIg.mono_set (diff_subset (t := ({(0 : EuclideanSpace ℝ (Fin 3))} :
      Set (EuclideanSpace ℝ (Fin 3)))))
    show (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}),
        K e2 e3 y * ((f + g : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞)
          (pvKCompact R)) y - (f + g) 0))
        = (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
            {(0 : EuclideanSpace ℝ (Fin 3))}),
            K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0))
          + ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
            {(0 : EuclideanSpace ℝ (Fin 3))}),
            K e2 e3 y * ((g : EuclideanSpace ℝ (Fin 3) → ℝ) y - g 0)
    rw [← MeasureTheory.integral_add hIf' hIg']
    apply MeasureTheory.setIntegral_congr_fun
      ((Metric.isClosed_closedBall.measurableSet).diff
        (measurableSet_singleton (0 : EuclideanSpace ℝ (Fin 3))))
    intro y _
    simp only [ContDiffMapSupportedIn.toContDiffMapSupportedInClass]
    show K e2 e3 y * (f y + g y - (f 0 + g 0)) =
        K e2 e3 y * (f y - f 0) + K e2 e3 y * (g y - g 0)
    ring
  map_smul' c f := by
    have hIf : IntegrableOn (fun y => K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0))
        (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) :=
      K_diff_integrableOn_closedBall_lipschitz e2 e3 f (N[ℝ]_{pvKCompact R, (1:ℕ∞), 1} f)
        (lipschitzWith_seminorm_of_contDiffMapSupportedIn f) R hR
    have hIf' := hIf.mono_set (diff_subset (t := ({(0 : EuclideanSpace ℝ (Fin 3))} :
      Set (EuclideanSpace ℝ (Fin 3)))))
    show (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}),
        K e2 e3 y * ((c • f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞)
          (pvKCompact R)) y - (c • f) 0))
        = c * ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
            {(0 : EuclideanSpace ℝ (Fin 3))}),
            K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0)
    rw [← MeasureTheory.integral_const_mul]
    apply MeasureTheory.setIntegral_congr_fun
      ((Metric.isClosed_closedBall.measurableSet).diff
        (measurableSet_singleton (0 : EuclideanSpace ℝ (Fin 3))))
    intro y _
    show K e2 e3 y * (c * f y - c * f 0) = c * (K e2 e3 y * (f y - f 0))
    ring

theorem pvKLM_apply (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R)) :
    pvKLM e2 e3 R hR f = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
      {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0) :=
  rfl

/-- Restatação verbatim de NS-2b: `pvKLM e2 e3 R hR` é CONTÍNUO, isto é,
um `ContinuousLinearMap` `𝓓^{1}_{K}(E, ℝ) →L[ℝ] ℝ` para o compacto FIXO
`K = closedBall 0 R`. -/
noncomputable def pvKCLM :
    ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R) →L[ℝ] ℝ where
  toLinearMap := pvKLM e2 e3 R hR
  cont := by
    obtain ⟨C₀, hC₀nonneg, hC₀bound⟩ := K_abs_le_div_norm_pow e2 e3
    set CR : ℝ := ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
      {(0 : EuclideanSpace ℝ (Fin 3))}), C₀ * ‖y‖ ^ (-(2:ℝ)) with hCRdef
    have hCRnonneg : (0:ℝ) ≤ CR := by
      rw [hCRdef]
      apply MeasureTheory.integral_nonneg
      intro y
      positivity
    refine continuous_of_isBounded (ContDiffMapSupportedIn.withSeminorms ℝ
      (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R))
      (norm_withSeminorms ℝ ℝ) (pvKLM e2 e3 R hR)
      (.of_real fun _ ↦ ⟨{1}, CR, fun f ↦ ?_⟩)
    simp only [Finset.sup_singleton]
    show ‖pvKLM e2 e3 R hR f‖ ≤ CR * N[ℝ]_{pvKCompact R, (1:ℕ∞), 1} f
    set Lr : ℝ := N[ℝ]_{pvKCompact R, (1:ℕ∞), 1} f with hLrdef
    have hLrnonneg : (0:ℝ) ≤ Lr := apply_nonneg _ f
    have hgLip : LipschitzWith Lr.toNNReal (f : EuclideanSpace ℝ (Fin 3) → ℝ) :=
      lipschitzWith_seminorm_of_contDiffMapSupportedIn f
    have hInt : IntegrableOn (fun y => K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0))
        (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) :=
      K_diff_integrableOn_closedBall_lipschitz e2 e3 f Lr hgLip R hR
    have hIntDiff := hInt.mono_set (diff_subset (t := ({(0 : EuclideanSpace ℝ (Fin 3))} :
      Set (EuclideanSpace ℝ (Fin 3)))))
    have hDom : IntegrableOn (fun y : EuclideanSpace ℝ (Fin 3) => Lr * (C₀ * ‖y‖ ^ (-(2:ℝ))))
        (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R) :=
      (const_mul_rpow_neg_two_integrableOn_closedBall C₀ hC₀nonneg R hR).const_mul Lr
    have hDomDiff := hDom.mono_set (diff_subset (t := ({(0 : EuclideanSpace ℝ (Fin 3))} :
      Set (EuclideanSpace ℝ (Fin 3)))))
    have hpointwise : ∀ᵐ y ∂(MeasureTheory.volume.restrict
        (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \ {(0 : EuclideanSpace ℝ (Fin 3))})),
        ‖K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0)‖ ≤ Lr * (C₀ * ‖y‖ ^ (-(2:ℝ))) := by
      filter_upwards [ae_restrict_mem ((Metric.isClosed_closedBall.measurableSet).diff
        (measurableSet_singleton (0 : EuclideanSpace ℝ (Fin 3))))] with y hy
      have hy0 : y ≠ 0 := by
        intro h; rw [h] at hy; exact hy.2 rfl
      have hynorm : (0:ℝ) < ‖y‖ := norm_pos_iff.mpr hy0
      have hKle : |K e2 e3 y| ≤ C₀ / ‖y‖ ^ 3 := hC₀bound y hy0
      have hgdiff : |(f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0| ≤ Lr * ‖y‖ := by
        have hd := hgLip.dist_le_mul y 0
        rw [Real.dist_eq, dist_eq_norm, sub_zero, Real.coe_toNNReal Lr hLrnonneg] at hd
        exact hd
      have hrpow : (C₀ / ‖y‖ ^ 3) * (Lr * ‖y‖) = Lr * (C₀ * ‖y‖ ^ (-(2:ℝ))) := by
        rw [Real.rpow_neg (norm_nonneg y), show (2:ℝ) = ((2:ℕ):ℝ) from by norm_num,
          Real.rpow_natCast]
        have hy3ne : (‖y‖ ^ 3 : ℝ) ≠ 0 := by positivity
        have hy2ne : (‖y‖ ^ 2 : ℝ) ≠ 0 := by positivity
        field_simp
      calc ‖K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0)‖
          = |K e2 e3 y| * |(f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0| := by
            rw [Real.norm_eq_abs, abs_mul]
        _ ≤ (C₀ / ‖y‖ ^ 3) * (Lr * ‖y‖) := by
            apply mul_le_mul hKle hgdiff (abs_nonneg _)
            positivity
        _ = Lr * (C₀ * ‖y‖ ^ (-(2:ℝ))) := hrpow
    have hnormle : ‖pvKLM e2 e3 R hR f‖ ≤ ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}), Lr * (C₀ * ‖y‖ ^ (-(2:ℝ))) := by
      rw [pvKLM_apply]
      exact MeasureTheory.norm_integral_le_of_norm_le hDomDiff hpointwise
    have hfinal : (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
        {(0 : EuclideanSpace ℝ (Fin 3))}), Lr * (C₀ * ‖y‖ ^ (-(2:ℝ)))) = Lr * CR := by
      rw [hCRdef, MeasureTheory.integral_const_mul]
    rw [hfinal] at hnormle
    calc ‖pvKLM e2 e3 R hR f‖ ≤ Lr * CR := hnormle
      _ = CR * Lr := by ring
      _ = CR * N[ℝ]_{pvKCompact R, (1:ℕ∞), 1} f := by rw [hLrdef]

theorem pvKCLM_apply (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R)) :
    pvKCLM e2 e3 R hR f = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
      {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0) :=
  rfl

/-! ## Parte 8 — restatação verbatim (NS-3a): independência do valor p.v.
local em relação ao raio de corte, para `g` eventualmente constante -/

theorem K_diff_shell_integral_eq_zero (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (g : EuclideanSpace ℝ (Fin 3) → ℝ) (c : ℝ) (R1 R2 : ℝ)
    (hR1 : 0 < R1) (hR1R2 : R1 < R2)
    (hsupp : ∀ y : EuclideanSpace ℝ (Fin 3), R1 < ‖y‖ → g y = c) :
    ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R1), K e2 e3 y * (g y - g 0) = 0 := by
  set B : Set (EuclideanSpace ℝ (Fin 3)) :=
    Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R1 with hB
  have hBmeas : MeasurableSet B :=
    (Metric.isClosed_closedBall.measurableSet).diff (Metric.isClosed_closedBall.measurableSet)
  have hEq : Set.EqOn (fun y => K e2 e3 y * (g y - g 0))
      (fun y => K e2 e3 y * (c - g 0)) B := by
    intro y hy
    have hyR1 : R1 < ‖y‖ := by
      rw [hB] at hy
      simp only [Set.mem_diff, Metric.mem_closedBall, dist_zero_right, not_le] at hy
      exact hy.2
    show K e2 e3 y * (g y - g 0) = K e2 e3 y * (c - g 0)
    rw [hsupp y hyR1]
  rw [setIntegral_congr_fun hBmeas hEq]
  rw [MeasureTheory.integral_mul_const]
  rw [hB, K_shell_integral_eq_zero e2 e3 R1 R2 hR1 hR1R2]
  ring

theorem pv_value_radius_independent (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (g : EuclideanSpace ℝ (Fin 3) → ℝ) (L : ℝ) (hg : LipschitzWith L.toNNReal g)
    (c : ℝ) (R1 R2 : ℝ) (hR1 : 0 < R1) (hR1R2 : R1 < R2)
    (hsupp : ∀ y : EuclideanSpace ℝ (Fin 3), R1 < ‖y‖ → g y = c) :
    (∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R1 \
        {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * (g y - g 0))
      = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
        {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * (g y - g 0) := by
  have hR2 : 0 < R2 := hR1.trans hR1R2
  set A : Set (EuclideanSpace ℝ (Fin 3)) :=
    Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R1 \ {(0 : EuclideanSpace ℝ (Fin 3))} with hA
  set B : Set (EuclideanSpace ℝ (Fin 3)) :=
    Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
      Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R1 with hB
  have hBmeas : MeasurableSet B :=
    (Metric.isClosed_closedBall.measurableSet).diff (Metric.isClosed_closedBall.measurableSet)
  have hDisj : Disjoint A B := by
    rw [Set.disjoint_left]
    intro y hyA hyB
    exact hyB.2 hyA.1
  have hUnion : A ∪ B = Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
      {(0 : EuclideanSpace ℝ (Fin 3))} := by
    ext y
    simp only [hA, hB, Set.mem_union, Set.mem_diff, Set.mem_singleton_iff,
      Metric.mem_closedBall, dist_zero_right]
    constructor
    · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩)
      · exact ⟨h1.trans hR1R2.le, h2⟩
      · refine ⟨h1, ?_⟩
        intro hy0
        apply h2
        rw [hy0, norm_zero]
        linarith
    · rintro ⟨h1, h2⟩
      by_cases hle : ‖y‖ ≤ R1
      · exact Or.inl ⟨hle, h2⟩
      · exact Or.inr ⟨h1, hle⟩
  have hIntA : IntegrableOn (fun y => K e2 e3 y * (g y - g 0)) A :=
    (K_diff_integrableOn_closedBall_lipschitz e2 e3 g L hg R1 hR1).mono_set Set.diff_subset
  have hIntB : IntegrableOn (fun y => K e2 e3 y * (g y - g 0)) B :=
    (K_diff_integrableOn_closedBall_lipschitz e2 e3 g L hg R2 hR2).mono_set Set.diff_subset
  have hBzero : ∫ y in B, K e2 e3 y * (g y - g 0) = 0 := by
    rw [hB]
    exact K_diff_shell_integral_eq_zero e2 e3 g c R1 R2 hR1 hR1R2 hsupp
  calc (∫ y in A, K e2 e3 y * (g y - g 0))
      = (∫ y in A, K e2 e3 y * (g y - g 0)) + ∫ y in B, K e2 e3 y * (g y - g 0) := by
        rw [hBzero]; ring
    _ = ∫ y in (A ∪ B), K e2 e3 y * (g y - g 0) :=
        (setIntegral_union hDisj hBmeas hIntA hIntB).symm
    _ = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
          {(0 : EuclideanSpace ℝ (Fin 3))}), K e2 e3 y * (g y - g 0) := by rw [hUnion]

/-! ## NOVO NESTA FRENTE (NS-4a)

Tudo abaixo desta linha é conteúdo genuinamente novo desta sessão -- não
é restatação de nada anteriormente fechado. Ver o resumo do cabeçalho e
o bloco final "O que NÃO é afirmado" para o escopo exato. -/

/-! ### Parte 9 — a composição `pvKCLM ∘ monoCLM` reproduz a mesma fórmula
integral, para qualquer compacto `K'` que caiba dentro da bola-envelope
`closedBall 0 R`

Consequência direta de `pvKCLM_apply` (Parte 7, restatada acima de NS-2b)
mais `ContDiffMapSupportedIn.monoCLM_apply` (Mathlib,
`Mathlib.Analysis.Distribution.ContDiffMapSupportedIn`, em torno da linha
817 no Mathlib vendorizado deste projeto): como `n₁ = n₂ = (1:ℕ∞)` e
`K' ≤ pvKCompact R` (hipótese `hK'`), a condição do `if` de
`monoCLM_apply` é verdadeira, logo a inclusão de `f : 𝓓^{1}_{K'}(E,ℝ)`
em `𝓓^{1}_{pvKCompact R}(E,ℝ)` via `monoCLM ℝ` é, como FUNÇÃO
subjacente, literalmente `f` (não um mapa diferente, não o mapa zero) --
por isso a composição `pvKCLM e2 e3 R hR ∘ (monoCLM ℝ)` calcula
EXATAMENTE a mesma fórmula integral p.v. que `pvKCLM` calcularia se `K'`
fosse `pvKCompact R` diretamente. -/
theorem pvKCLM_comp_monoCLM_eq_integral
    (e2 e3 : EuclideanSpace ℝ (Fin 3)) (K' : Compacts (EuclideanSpace ℝ (Fin 3)))
    (R : ℝ) (hR : 0 < R) (hK' : K' ≤ pvKCompact R)
    (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K') :
    pvKCLM e2 e3 R hR (ContDiffMapSupportedIn.monoCLM ℝ f)
      = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R \
          {(0 : EuclideanSpace ℝ (Fin 3))}),
          K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0) := by
  have hcond : (1 : ℕ∞) ≤ (1 : ℕ∞) ∧ K' ≤ pvKCompact R := ⟨le_refl _, hK'⟩
  have hmono_eq : ((ContDiffMapSupportedIn.monoCLM ℝ f :
      ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R)) :
      EuclideanSpace ℝ (Fin 3) → ℝ) = (f : EuclideanSpace ℝ (Fin 3) → ℝ) := by
    rw [ContDiffMapSupportedIn.monoCLM_apply, if_pos hcond]
  rw [pvKCLM_apply]
  simp only [hmono_eq]

/-! ### Parte 10 — o teorema-alvo: a independência de raio do funcional
composto `pvKCLM ∘ monoCLM`, para qualquer compacto `K'` e quaisquer dois
raios-envelope `R1, R2 > 0` (em qualquer ordem)

**Item central desta frente**: para `K' : Compacts E` e `f ∈ 𝓓^{1}_{K'}(E,
ℝ)`, o valor de `pvKCLM e2 e3 R hR (monoCLM ℝ f)` NÃO depende da escolha
do raio-envelope `R`, contanto que `K' ⊆ closedBall 0 R` (hipóteses
`hK'1`/`hK'2` para `R1`/`R2` respectivamente -- juntas, equivalentes a
`K' ⊆ closedBall 0 (min R1 R2)`, exatamente a hipótese do teste
original). A prova reduz, via `pvKCLM_comp_monoCLM_eq_integral` (Parte
9), ao valor da integral p.v. de `K e2 e3 * f` (função subjacente a `f`,
esquecendo o empacotamento `ContDiffMapSupportedIn`), e então aplica
`pv_value_radius_independent` (Parte 8, restatada de NS-3a) com
`g := (f : E → ℝ)`, `L := N[ℝ]_{K',1,1} f`
(`lipschitzWith_seminorm_of_contDiffMapSupportedIn f`, restatada de
NS-2b -- já genérica em QUALQUER compacto `K`, não só bolas), `c := 0`
(pois `f` se anula fora de `K'`, `f.zero_on_compl`), com `(min R1 R2,
max R1 R2)` no lugar de `(R1, R2)` -- `wlog` sobre qual dos dois raios é
o menor, exigido porque `pv_value_radius_independent` exige `R1 < R2`
estrito -- fechado por um `rcases lt_trichotomy R1 R2` de três casos (o
caso `R1 = R2` é trivial por irrelevância de prova, `rfl`). `hsupp` (a
hipótese `∀ y, min R1 R2 < ‖y‖ → f y = 0`) é derivada diretamente de
`f.zero_on_compl`: se `‖y‖ > min R1 R2` mas `y ∈ K'`, então `‖y‖ ≤ R1`
(de `hK'1`, via `SetLike.coe_subset_coe`) e `‖y‖ ≤ R2` (de `hK'2`), logo
`‖y‖ ≤ min R1 R2`, contradizendo `‖y‖ > min R1 R2`; portanto `y ∉ K'`, e
`f.zero_on_compl` dá `f y = 0`. -/
theorem pvKCLM_comp_monoCLM_radius_independent
    (e2 e3 : EuclideanSpace ℝ (Fin 3)) (K' : Compacts (EuclideanSpace ℝ (Fin 3)))
    (R1 R2 : ℝ) (hR1 : 0 < R1) (hR2 : 0 < R2)
    (hK'1 : K' ≤ pvKCompact R1) (hK'2 : K' ≤ pvKCompact R2)
    (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K') :
    pvKCLM e2 e3 R1 hR1 (ContDiffMapSupportedIn.monoCLM ℝ f)
      = pvKCLM e2 e3 R2 hR2 (ContDiffMapSupportedIn.monoCLM ℝ f) := by
  rw [pvKCLM_comp_monoCLM_eq_integral e2 e3 K' R1 hR1 hK'1 f,
      pvKCLM_comp_monoCLM_eq_integral e2 e3 K' R2 hR2 hK'2 f]
  set Lr : ℝ := N[ℝ]_{K', (1 : ℕ∞), 1} f with hLrdef
  have hLip : LipschitzWith Lr.toNNReal (f : EuclideanSpace ℝ (Fin 3) → ℝ) :=
    lipschitzWith_seminorm_of_contDiffMapSupportedIn f
  have hsupp_min : ∀ y : EuclideanSpace ℝ (Fin 3),
      min R1 R2 < ‖y‖ → (f : EuclideanSpace ℝ (Fin 3) → ℝ) y = 0 := by
    intro y hy
    apply f.zero_on_compl
    show y ∉ (K' : Set (EuclideanSpace ℝ (Fin 3)))
    intro hmem
    have hyR1 : ‖y‖ ≤ R1 := by
      have hy' : y ∈ (pvKCompact R1 : Set (EuclideanSpace ℝ (Fin 3))) :=
        SetLike.coe_subset_coe.mpr hK'1 hmem
      simpa [pvKCompact, Metric.mem_closedBall, dist_zero_right] using hy'
    have hyR2 : ‖y‖ ≤ R2 := by
      have hy' : y ∈ (pvKCompact R2 : Set (EuclideanSpace ℝ (Fin 3))) :=
        SetLike.coe_subset_coe.mpr hK'2 hmem
      simpa [pvKCompact, Metric.mem_closedBall, dist_zero_right] using hy'
    exact absurd (le_min hyR1 hyR2) (not_le.mpr hy)
  rcases lt_trichotomy R1 R2 with hlt | heq | hlt
  · have hmineq : min R1 R2 = R1 := min_eq_left hlt.le
    have hsupp : ∀ y : EuclideanSpace ℝ (Fin 3),
        R1 < ‖y‖ → (f : EuclideanSpace ℝ (Fin 3) → ℝ) y = 0 := by
      rw [← hmineq]; exact hsupp_min
    exact pv_value_radius_independent e2 e3 (f : EuclideanSpace ℝ (Fin 3) → ℝ) Lr hLip
      0 R1 R2 hR1 hlt hsupp
  · subst heq
    rfl
  · have hmineq : min R1 R2 = R2 := min_eq_right hlt.le
    have hsupp : ∀ y : EuclideanSpace ℝ (Fin 3),
        R2 < ‖y‖ → (f : EuclideanSpace ℝ (Fin 3) → ℝ) y = 0 := by
      rw [← hmineq]; exact hsupp_min
    exact (pv_value_radius_independent e2 e3 (f : EuclideanSpace ℝ (Fin 3) → ℝ) Lr hLip
      0 R2 R1 hR2 hlt hsupp).symm

end TamesisNSPVFunctionalOnArbitraryK

/-! ## O que NÃO é afirmado

```text
NÃO constrói um membro de `𝓓^{1}(E, ℝ) →L[ℝ] ℝ` (dual topológico do
  espaço COMPLETO de funções-teste, via `TestFunction.mkCLM`/
  `TestFunction.limitCLM`) -- essa construção exigiria montar a família
  `{pvKCLM_comp_monoCLM : K' compacto}` fechada aqui em UM único
  funcional GLOBAL, satisfazendo a obrigação de prova exata de
  `TestFunction.mkCLM` (compatibilidade da família via `monoCLM` para
  TODO par de compactos, não só um par fixo por vez) -- o "gap (iii)"
  nomeado no plano de ataque da Onda 4, explicitamente fora do escopo
  desta sessão
NÃO prova nenhuma limitação L^p de operador integral singular
NÃO prova nenhum teorema de Calderón-Zygmund (decomposição, tipo-fraco,
  interpolação de Marcinkiewicz)
NÃO trata uma função-teste genérica de Schwartz/C^∞_c de ordem
  arbitrária -- só `𝓓^{1}_{K'}` (ordem exatamente `1`, `e2`, `e3`
  continuam fixos, "coeficientes congelados", exatamente como em
  NS-1/NS-2a/NS-2b/NS-3a)
NÃO prova nada sobre a integral p.v. real das equações (2.1)/(2.2) de
  Constantin-Fefferman aplicada a um campo de vorticidade genuíno
NÃO prova NS-GAP-001/004 nem qualquer regularidade condicional real
NÃO afirma que Navier-Stokes ficou alcançável, aproximável, ou resolvido
NÃO afirma novidade matemática -- compor um `ContinuousLinearMap` já
  fechado (`pvKCLM`, NS-2b) com a inclusão contínua-linear padrão de
  Mathlib entre espaços de funções-teste (`ContDiffMapSupportedIn.monoCLM`)
  é uma aplicação rotineira do maquinário de distribuições já presente em
  Mathlib; a independência de raio do valor resultante é uma consequência
  imediata de `pv_value_radius_independent` (já fechado em NS-3a) mais
  a observação elementar de que `f.zero_on_compl` fornece exatamente a
  hipótese `hsupp` (constância -- aqui, anulação -- além do raio menor)
  que aquele lema exige; a única coisa nova é a formalização Lean dessa
  composição e do case-split `min`/`max` sobre a ordem dos dois raios
```

## Resumo do que esta frente FECHOU

O teste (WAVE4-NS-4A) pedia: compor `pvKCLM` (bola) com `monoCLM`
(`K' -> bola`) para obter o funcional p.v. contínuo-linear sobre `K'`
arbitrário; fechar radius-independence via `pv_value_radius_independent`
aplicado com `(min R1 R2, max R1 R2)` (wlog sobre qual raio é menor);
derivar `hsupp` de `f.zero_on_compl` composto com `K' ≤ closedBall 0
(min R1 R2)`. Isso fechou sem obstáculo -- exatamente como o teste
antecipou, com o "gap cosmético" no enunciado (raio menor/maior via
`min`/`max`, não assumindo ordem `a priori`) resolvido por um
`rcases lt_trichotomy R1 R2` de três casos (o terceiro caso, `R1 = R2`,
fecha por `rfl` após `subst`, por irrelevância de prova em `Prop`).
`pvKCLM_comp_monoCLM_eq_integral` (Parte 9, novo) mostra que a composição
`pvKCLM e2 e3 R hR ∘ (ContDiffMapSupportedIn.monoCLM ℝ)` reproduz
EXATAMENTE a mesma fórmula integral p.v. que `pvKCLM` calcularia
diretamente sobre `K'` (via `ContDiffMapSupportedIn.monoCLM_apply` do
Mathlib, cuja condição `n₂ ≤ n₁ ∧ K₁ ≤ K₂` é verdadeira aqui pois
`n₁ = n₂ = 1` e `K' ≤ pvKCompact R`, hipótese `hK'`).
`pvKCLM_comp_monoCLM_radius_independent` (Parte 10, novo, o
teorema-alvo) mostra que esse valor composto é o MESMO para quaisquer
dois raios-envelope `R1, R2 > 0` tais que `K' ⊆ closedBall 0 R1` e
`K' ⊆ closedBall 0 R2` (hipóteses `hK'1`, `hK'2`), reduzindo (via a
Parte 9) ao caso já fechado por `pv_value_radius_independent` (NS-3a)
aplicado a `g := (f : E → ℝ)`, `L := N[ℝ]_{K',1,1} f`
(`lipschitzWith_seminorm_of_contDiffMapSupportedIn`, NS-2b, já genérica
em qualquer compacto), `c := 0`, e `hsupp` derivada diretamente de
`f.zero_on_compl` (`f` se anula fora de `K'`, e `K' ⊆ closedBall 0
(min R1 R2)` segue de `hK'1`/`hK'2` juntas via `le_min`).

Fontes citadas (mesmas de NS-1/NS-2a/NS-2b/NS-3a, mais o maquinário
específico de `monoCLM`):
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
- `LipschitzWith.dist_le_mul`, `Mathlib.Topology.MetricSpace.Lipschitz`.
- `lipschitzWith_of_nnnorm_fderiv_le`, `Mathlib.Analysis.Calculus.MeanValue`.
- `MeasureTheory.setIntegral_union`, `MeasureTheory.integral_mul_const`,
  `Mathlib.MeasureTheory.Integral.Bochner.Set` /
  `Mathlib.MeasureTheory.Integral.Bochner.Basic`.
- `ContDiffMapSupportedIn`, `ContDiffMapSupportedIn.seminorm`,
  `ContDiffMapSupportedIn.withSeminorms`, `Seminorm.IsBounded.of_real`,
  `Seminorm.continuous_of_isBounded`, `ContDiffMapSupportedIn.monoCLM`,
  `ContDiffMapSupportedIn.monoCLM_apply`, `ContDiffMapSupportedIn.zero_on_compl`,
  Anatole Dedecker, Luigi Massacci,
  `Mathlib.Analysis.Distribution.ContDiffMapSupportedIn`,
  `Mathlib.Analysis.LocallyConvex.WithSeminorms` (mecanismo novo desta
  frente: a composição de `pvKCLM` com a inclusão canônica `monoCLM`
  entre compactos, e o `wlog`/case-split via `SetLike.coe_subset_coe` e
  `PartialOrder.ofSetLike` que identifica `≤` em `Compacts` com inclusão
  de conjuntos).
-/

#print axioms TamesisNSPVFunctionalOnArbitraryK.tripleProduct
#print axioms TamesisNSPVFunctionalOnArbitraryK.D
#print axioms TamesisNSPVFunctionalOnArbitraryK.sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.yHat_smul_of_pos
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_homogeneous
#print axioms TamesisNSPVFunctionalOnArbitraryK.contDiff_D_fst
#print axioms TamesisNSPVFunctionalOnArbitraryK.contDiffAt_yHat
#print axioms TamesisNSPVFunctionalOnArbitraryK.contDiffAt_K
#print axioms TamesisNSPVFunctionalOnArbitraryK.tripleProduct_self_left
#print axioms TamesisNSPVFunctionalOnArbitraryK.integral_D_eq_zero_of_isotropicSecondMoment
#print axioms TamesisNSPVFunctionalOnArbitraryK.volume_image_linearIsometryEquiv
#print axioms TamesisNSPVFunctionalOnArbitraryK.image_smul_Ioo_linearIsometryEquiv
#print axioms TamesisNSPVFunctionalOnArbitraryK.mapsTo_sphere
#print axioms TamesisNSPVFunctionalOnArbitraryK.sphereMap
#print axioms TamesisNSPVFunctionalOnArbitraryK.sphereMap_continuous
#print axioms TamesisNSPVFunctionalOnArbitraryK.sphereMap_measurable
#print axioms TamesisNSPVFunctionalOnArbitraryK.image_val_preimage_sphereMap
#print axioms TamesisNSPVFunctionalOnArbitraryK.preimage_eq_image_symm
#print axioms TamesisNSPVFunctionalOnArbitraryK.toSphere_map_sphereMap
#print axioms TamesisNSPVFunctionalOnArbitraryK.sphereSurfaceMeasure_map_linearIsometryEquiv
#print axioms TamesisNSPVFunctionalOnArbitraryK.ae_mem_sphere_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.instIsFiniteMeasure_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.integrable_coord_mul_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.flipCoord
#print axioms TamesisNSPVFunctionalOnArbitraryK.flipCoord_apply_self
#print axioms TamesisNSPVFunctionalOnArbitraryK.flipCoord_apply_other
#print axioms TamesisNSPVFunctionalOnArbitraryK.permCoord
#print axioms TamesisNSPVFunctionalOnArbitraryK.permCoord_apply
#print axioms TamesisNSPVFunctionalOnArbitraryK.integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.integral_offdiag_eq_zero_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.integral_diag_eq_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.sphereSurfaceMeasure_isotropicSecondMoment
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_mean_zero_sphereSurfaceMeasure
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_bounded_unit_sphere
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_abs_le_div_norm_pow
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_mean_zero_sphereSurfaceMeasure_via_toSphere
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_shell_integral_eq_zero
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_diff_integrableOn_closedBall_lipschitz
#print axioms TamesisNSPVFunctionalOnArbitraryK.lipschitzWith_seminorm_of_contDiffMapSupportedIn
#print axioms TamesisNSPVFunctionalOnArbitraryK.const_mul_rpow_neg_two_integrableOn_closedBall
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKCompact
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKLM
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKLM_apply
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKCLM
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKCLM_apply
#print axioms TamesisNSPVFunctionalOnArbitraryK.K_diff_shell_integral_eq_zero
#print axioms TamesisNSPVFunctionalOnArbitraryK.pv_value_radius_independent

-- NOVO NESTA FRENTE (NS-4a) -- declarações novas desta sessão
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKCLM_comp_monoCLM_eq_integral
#print axioms TamesisNSPVFunctionalOnArbitraryK.pvKCLM_comp_monoCLM_radius_independent
