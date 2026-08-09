/-
  Tamesis formal lab -- Wave-1 item RH-4 (RH-NOGO-001 front, formal
  reconnaissance pass, NOT a Millennium-problem attack).

  Extends the already-VERIFIED FOUND-SPECTRAL-COUNTING-001 fixed-threshold
  `eigCount` (TamesisLab/Foundations/SpectralCounting.lean) with the correct
  direction of the limit statement.

  Prova completa: nenhuma lacuna, nenhum axioma local, nenhum escape hatch
  de prova.
-/

import Mathlib
import TamesisLab.Foundations.SpectralCounting
import TamesisLab.Foundations.SpectralCountingInstance

/-!
# RH-4 -- `eigCount` diverge quando o patamar tende a `0⁺`

## Contexto

`FOUND-SPECTRAL-COUNTING-001` (VERIFIED) prova que, para um operador
compacto autoadjunto `T`, o conjunto `{μ : lam ≤ |μ| ∧ HasEigenvalue T μ}`
é **finito** para todo `lam > 0` (`finite_eigenvalues_above`), e que
`eigCount T lam := esse_conjunto.ncard` é **antítono** em `lam`
(`eigCount_antitone`, `lam₁ ≤ lam₂ → eigCount T lam₂ ≤ eigCount T lam₁`).

O teste originalmente proposto para este item pedia
`Tendsto (fun L => N L) atTop atTop` -- ou seja, o patamar `L` crescendo.
Isso está **matematicamente errado**: como `eigCount_antitone` já mostra que
a contagem é não-crescente em `lam`, ela não pode divergir quando `lam → +∞`
(pelo contrário, ela some para `lam` grande, como ilustra
`SpectralCountingInstance.eigCount_two = 0`). A revisão adversarial apontou
exatamente isso e forneceu a direção correta: os autovalores de um operador
compacto só se acumulam em `0`, logo a contagem acima do patamar diverge
quando o patamar **encolhe para `0`**, não quando cresce.

Este arquivo prova a versão corrigida:

```
Tendsto (fun lam : ℝ => (eigCount T lam : ℝ)) (𝓝[>] 0) atTop
```

sob a hipótese adicional (necessária: sem ela `eigCount T lam` seria
eventualmente constante em `0`, e o teste seria vazio) de que `T` possui um
conjunto **infinito** de autovalores reais **não-nulos**.

## O que este arquivo NÃO prova (leia antes de citar)

* **Nada sobre GLOBAL_WEYL_BRIDGE.** O `N(Λ)` que GWB-002/GWB-003 precisam é
  a contagem de autovalores de um operador **não-limitado** com resolvente
  compacto, crescendo quando `Λ → +∞`. O `eigCount T lam` aqui é a cauda
  *acima* de um patamar de um operador **limitado**, e diverge quando o
  patamar **encolhe para `0`**. Ligar as duas noções exige uma inversão
  espectral (`Λ_não-limitado = 1/μ_resolvente-compacto`) que **não** está
  formalizada aqui -- é uma obrigação nova, separada, não coberta por este
  arquivo, e permanece como lacuna explícita para trabalho futuro.
* **Nada sobre a lei de potência `N(Λ) ~ C·Λ^(d/m)`** (GWB-006/GWB-009):
  isso exige cálculo simbólico e integração em variedades, ausentes da
  Mathlib.
* **Nada sobre GWB-001** (discreticidade para operadores pseudodiferenciais
  não-limitados numa variedade): esse é um `EXPLICIT_CLASS_ASSUMPTION`
  citado em `DISCRETENESS_CLASSIFICATION.md`, não um teorema, e permanece
  inalterado por este arquivo.
* **Nenhuma alegação de progresso sobre a Hipótese de Riemann** ou qualquer
  outro problema do Millennium Prize. Este é puramente um fato de
  escalonamento (scaffolding) sobre operadores compactos autoadjuntos
  limitados, reutilizável fora desta frente.

## Ingredientes reutilizados (sem reprovar nada)

* `finite_eigenvalues_above`, `eigCount`, `eigCount_antitone` -- de
  `TamesisLab.Foundations.SpectralCounting` (linhas 92-192 daquele
  arquivo), já VERIFIED.
* `Set.Infinite.exists_subset_card_eq` (Mathlib,
  `Mathlib/Data/Set/Finite/Basic.lean`) -- de um conjunto infinito extrai-se
  um `Finset` de cardinalidade arbitrária.
* `Ioo_mem_nhdsGT` (Mathlib, dual automático de `Ioo_mem_nhdsLT` em
  `Mathlib/Topology/Order/OrderClosed.lean`) -- vizinhança à direita de `0`
  contém um intervalo `Ioo 0 ε`.
* Para a instância positiva de não-vacuidade (seção final): o operador
  diagonal `T` de `TamesisLab.Foundations.SpectralCounting.InfDim`
  (arquivo `SpectralCountingInstance.lean`, também já VERIFIED), com
  diagonal `1/(i+1)`.
-/

open Module.End Filter Topology
open scoped InnerProductSpace

namespace TamesisLab.Foundations.SpectralCounting.Limit

variable {𝕜 : Type*} {H : Type*} [RCLike 𝕜] [NormedAddCommGroup H]
  [InnerProductSpace 𝕜 H]

section Abstract

variable {T : H →L[𝕜] H}

/-- **Teorema principal (RH-4, versão corrigida).** Se `T` é compacto e
autoadjunto, e possui um conjunto infinito de autovalores reais
**não-nulos**, então `eigCount T lam → +∞` quando `lam → 0⁺` (dentro de
`lam > 0`). Reusa apenas `finite_eigenvalues_above` (via
`Set.ncard_le_ncard`) e a estrutura de patamar de `eigCount`; não reprova
`eigCount_antitone`, mas é consistente com ela (o crescimento acontece na
direção oposta à do teste originalmente proposto). -/
theorem eigCount_tendsto_atTop_nhdsWithin_zero
    (hc : IsCompactOperator T) (hs : (T : H →ₗ[𝕜] H).IsSymmetric)
    (hinf : {μ : ℝ | μ ≠ 0 ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)}.Infinite) :
    Tendsto (fun lam : ℝ => (eigCount T lam : ℝ))
      (nhdsWithin (0 : ℝ) (Set.Ioi (0 : ℝ))) atTop := by
  rw [Filter.tendsto_atTop]
  intro b
  -- `m` é um natural que domina `b` e é `≥ 1`, garantindo um `Finset` não-vazio.
  set m : ℕ := max ⌈b⌉₊ 1 with hm_def
  have hbm : b ≤ (m : ℝ) :=
    le_trans (Nat.le_ceil b) (by exact_mod_cast (le_max_left ⌈b⌉₊ 1 : ⌈b⌉₊ ≤ m))
  have hm1 : 1 ≤ m := le_max_right _ _
  -- Extrai `m` autovalores não-nulos distintos do conjunto infinito.
  obtain ⟨F, hFsub, hFcard⟩ := hinf.exists_subset_card_eq m
  have hcard_pos : 0 < F.card := by rw [hFcard]; omega
  have hFne : F.Nonempty := Finset.card_pos.mp hcard_pos
  have hFnz : ∀ μ ∈ F, μ ≠ 0 := fun μ hμ => (hFsub (Finset.mem_coe.mpr hμ)).1
  have hFeig : ∀ μ ∈ F, HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜) :=
    fun μ hμ => (hFsub (Finset.mem_coe.mpr hμ)).2
  -- `lam0` = o menor `|μ|` sobre `F` (via a imagem `G`); é positivo pois todo
  -- `μ ∈ F` é não-nulo.
  set G : Finset ℝ := F.image (fun μ => |μ|) with hG_def
  have hGne : G.Nonempty := hFne.image _
  have hlam0_pos : 0 < G.min' hGne := by
    refine (Finset.lt_min'_iff G hGne).mpr (fun y hy => ?_)
    rw [hG_def, Finset.mem_image] at hy
    obtain ⟨μ, hμF, rfl⟩ := hy
    exact abs_pos.mpr (hFnz μ hμF)
  -- Para todo `lam` na vizinhança à direita `Ioo 0 lam0`, `F` inteiro fica
  -- contido na banda `{lam ≤ |μ|}`, logo `eigCount T lam ≥ F.card ≥ m ≥ b`.
  refine Filter.eventually_of_mem (Ioo_mem_nhdsGT hlam0_pos) (fun lam hlam => ?_)
  obtain ⟨hlam_pos, hlam_lt⟩ := hlam
  have hsub : (↑F : Set ℝ) ⊆
      {μ : ℝ | lam ≤ |μ| ∧ HasEigenvalue (T : Module.End 𝕜 H) (μ : 𝕜)} := by
    intro μ hμ
    have hμF : μ ∈ F := Finset.mem_coe.mp hμ
    refine ⟨?_, hFeig μ hμF⟩
    have hmem : |μ| ∈ G := by rw [hG_def]; exact Finset.mem_image_of_mem _ hμF
    calc lam ≤ G.min' hGne := le_of_lt hlam_lt
      _ ≤ |μ| := Finset.min'_le G (|μ|) hmem
  have hcard_le : F.card ≤ eigCount T lam := by
    have hle := Set.ncard_le_ncard hsub (finite_eigenvalues_above hc hs hlam_pos)
    rwa [Set.ncard_coe_finset] at hle
  have hm_le : m ≤ eigCount T lam := hFcard ▸ hcard_le
  exact le_trans hbm (by exact_mod_cast hm_le)

end Abstract

/-! ### Instância positiva (não-vacuidade)

A hipótese `hinf` (conjunto infinito de autovalores não-nulos) é
satisfazível: `SpectralCounting.InfDim.T`, o operador diagonal
`1/(i+1)` em `ℓ²(ℕ, ℂ)`, já tem `IsCompactOperator`, `IsSymmetric`, e
`infinite_eigenvalues` provados. Como toda `dseq i = 1/(i+1) ≠ 0`, o
conjunto de autovalores é automaticamente o mesmo conjunto "não-nulos". -/

section PositiveInstance

open TamesisLab.Foundations.SpectralCounting.InfDim

/-- Os autovalores de `SpectralCounting.InfDim.T` já formam, sem hipótese
adicional, um conjunto infinito de valores não-nulos (todo `dseq i > 0`). -/
theorem positiveInstance_infinite_nonzero_eigenvalues :
    {μ : ℝ | μ ≠ 0 ∧
      Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))}.Infinite := by
  apply Set.Infinite.mono
    (s := {μ : ℝ | Module.End.HasEigenvalue (T : Module.End ℂ H2) ((μ : ℂ))})
  · intro μ hμ
    obtain ⟨i, rfl⟩ := (real_hasEigenvalue_iff μ).mp hμ
    exact ⟨(dseq_pos i).ne', hμ⟩
  · exact infinite_eigenvalues

/-- **Instância não-vazia do teorema principal.** O teorema `RH-4` acima
tem hipóteses satisfazíveis por um exemplo já verificado nesta base: para
`T = SpectralCounting.InfDim.T`, `eigCount T lam → +∞` quando `lam → 0⁺`. -/
theorem positiveInstance_eigCount_tendsto_atTop_nhdsWithin_zero :
    Tendsto (fun lam : ℝ => (eigCount T lam : ℝ))
      (nhdsWithin (0 : ℝ) (Set.Ioi (0 : ℝ))) atTop :=
  eigCount_tendsto_atTop_nhdsWithin_zero
    T_isCompactOperator T_isSymmetric positiveInstance_infinite_nonzero_eigenvalues

end PositiveInstance

end TamesisLab.Foundations.SpectralCounting.Limit

#print axioms TamesisLab.Foundations.SpectralCounting.Limit.eigCount_tendsto_atTop_nhdsWithin_zero
#print axioms TamesisLab.Foundations.SpectralCounting.Limit.positiveInstance_infinite_nonzero_eigenvalues
#print axioms TamesisLab.Foundations.SpectralCounting.Limit.positiveInstance_eigCount_tendsto_atTop_nhdsWithin_zero
