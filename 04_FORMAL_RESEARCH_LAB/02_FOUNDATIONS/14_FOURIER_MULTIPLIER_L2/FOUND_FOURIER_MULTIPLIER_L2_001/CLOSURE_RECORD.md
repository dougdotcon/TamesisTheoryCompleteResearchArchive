---
document_id: FOUND-FOURIER-MULTIPLIER-L2-001-CLOSURE-RECORD
work_item_id: FOUND-FOURIER-MULTIPLIER-L2-001
work_status: VERIFIED
result_review: APPROVED
gate_combination_declared: true
corrects_own_specification: true
---

# Registro de encerramento

## A CORRECAO, que e o achado principal

A "Peca A" foi especificada por mim como *enfraquecer a hipotese
`HasTemperateGrowth` do lema de multiplicador*. **Essa especificacao era
vacua**, e a sondagem provou isso em Lean:

```lean
SchwartzMap.smulLeftCLM (g : E → 𝕜) : 𝓢(E, F) →L[𝕜] 𝓢(E, F) :=
  if hg : g.HasTemperateGrowth then bilinLeftCLM (…).flip hg else 0
```

E um **`dite` com valor-lixo `0`**. Consequencias, ambas provadas sem
`sorry`:

```text
fourierMultiplierCLM_eq_zero_of_not_temperate
    nao temperado  =>  o operador do Mathlib e LITERALMENTE 0

fourierMultiplierCLM_of_bounded_no_smoothness
    a hipotese HasTemperateGrowth pode ser APAGADA e o lema sai em
    5 linhas: by_cases, ramo temperado usa o lema do Mathlib, ramo
    nao-temperado o operador e 0 e usa memSobolev_fun_zero
```

Ou seja: enfraquecer a hipotese **nao diz nada** sobre o projetor de
Leray, porque sobre simbolos nao-temperados o operador ja e zero. **Era o
defeito de vacuidade outra vez**, desta vez na minha propria
especificacao.

A Peca A real e **construir um operador L2 novo**. E o que esta frente
entrega.

## O que foi construido

```lean
mulL2 (g : Lp ℂ ∞ volume) : Lp E F 2 →L[ℂ] Lp E F 2
norm_mulL2_le : ‖mulL2 F g‖ ≤ ‖g‖

fourierMulL2 (g : Lp ℂ ∞ volume) : Lp E F 2 →L[ℂ] Lp E F 2
norm_fourierMulL2_le : ‖fourierMulL2 F g‖ ≤ ‖g‖
```

Plancherel puro, **zero suavidade**. O Mathlib tinha as pecas
(`Lp.fourierTransformₗᵢ`, `Lp.norm_smul_le`, `HolderTriple ∞ 2 2`) mas
**nao tinha o CLM empacotado**.

## Compatibilidade: estende, nao substitui

```lean
toTemperedDistribution_fourierMulL2_eq (hg₁ : g.HasTemperateGrowth) :
    ↑(fourierMulL2 F (ofBounded hm C hC) u)
      = TemperedDistribution.fourierMultiplierCLM F g ↑u
```

Na sobreposicao temperada os dois operadores coincidem. O novo nao e
objeto solto.

## A forma canonica em Sobolev

```lean
MemSobolev.existsUnique_fourierMulL2 (hf : MemSobolev s 2 f)
    (g : Lp ℂ ∞ volume) :
    ∃! v, MemSobolev s 2 v ∧ ∃ u, besselPotential E F s f = ↑u ∧
      besselPotential E F s v = ↑(fourierMulL2 F g u) ∧
      ‖fourierMulL2 F g u‖ ≤ ‖g‖ * ‖u‖
```

`∃!`, apoiada em duas injetividades provadas
(`toTemperedDistribution_injective`, `besselPotential_injective`).

## Instancia positiva com o simbolo de Leray DE VERDADE

```lean
lerayComponent (m n : E) : E → ℂ := fun x ↦ (⟪x,m⟫ * ⟪x,n⟫ / ‖x‖^2 : ℝ)
norm_lerayComponent_le : ‖lerayComponent m n x‖ ≤ ‖m‖ * ‖n‖
not_hasTemperateGrowth_lerayComponent (hm : m ≠ 0)
positive_instance_leray
```

`positive_instance_leray` e uma conjuncao tripla: o simbolo **nao** e
temperado, **e** o operador do Mathlib nele e exatamente `0`, **e** o
operador novo da `∃!` solucao com cota de Plancherel.

Nao e brinquedo: e o `ξ_j ξ_k / |ξ|²` do projetor de Leray.

## Numeros

```text
linhas                345
declaracoes            38   (31 teoremas, 7 definicoes)
sorry / axioma local    0
pegada                 propext, Classical.choice, Quot.sound
lake build             exit 0, 8813 jobs
```

## Veredito revisto: LOW, nao high

Eu estimei `high`. Foi **uma sessao**, e o trabalho foi **montagem, nao
descoberta** — todas as pecas criticas ja estavam no Mathlib. O unico
atrito real foram dois timeouts de `whnf` resolvidos por reestruturacao.

## O que fica aberto

```text
FM-GAP-001  O Mathlib NAO TEM TIPO de espaco de Sobolev. MemSobolev e
            um Prop, nao um espaco normado, e grep -rl MemSobolev
            retorna UM arquivo. Logo
            fourierMultiplierSobolevCLM : H^s →L[ℂ] H^s
            NAO E SEQUER ENUNCIAVEL hoje. A forma ∃! entregue e a mais
            forte enunciavel no vocabulario atual. Fechar isso e
            engenharia de biblioteca: definir H^s como pullback de Lp
            pela isometria de Bessel.
FM-GAP-002  O simbolo aqui e ESCALAR (Lp ℂ ∞). O projetor de Leray e
            MATRICIAL. Exige Lp (F →L[ℂ] F) ∞ ou soma finita de
            componentes. Direto, so volume.
```

## Desvio de protocolo, declarado

Quatro gates combinados num commit, como em
`FOUND-SPECTRAL-COUNTING-001`. Nenhuma verificacao pulada; a separacao em
quatro commits foi.

## O que NAO e afirmado

```text
que o projetor de Leray esteja construido   -- falta o caso matricial
que Navier-Stokes tenha ficado alcancavel
que exista espaco de Sobolev como TIPO
```

**Nenhum problema de milenio foi atacado.**
