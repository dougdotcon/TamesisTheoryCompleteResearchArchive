---
document_id: PORTFOLIO-REVIEW-DUHAMEL-SKELETON-2026-08-09
reviewed_at: 2026-08-09
conclusion: FOUND-DUHAMEL-SKELETON-001_AUTHORIZED
---

# Revisão de portfólio — esqueleto de Duhamel

## Onde a cadeia está

`HEAT-GAP-001` fechou por completo na frente anterior
(`FOUND-HEAT-SEMIGROUP-LAW-001`, DEC-068): o semigrupo do calor
`heatOpL2` é agora contração, simétrico via produto interno, satisfaz a
lei de semigrupo, e é fortemente contínuo para `t₀ ≥ 0` arbitrário.
Composto com o projetor de Leray já caracterizado, dá o operador de
Stokes `P·e^{tΔ}`.

## Por que o esqueleto de Duhamel é o próximo passo honesto

A fórmula de Duhamel/solução branda `u(t) = S(t)u₀ + ∫₀ᵗ S(t-s)B(u(s))ds`
é o objeto padrão da literatura (Fujita-Kato, Cannone) para formular
existência local de Navier-Stokes via ponto fixo. **Esta frente NÃO
tenta esse ponto fixo.** O termo `B` (a não-linearidade, tipicamente
`B(u) = -P·∇·(u⊗u)` para Navier-Stokes) fica **completamente abstrato**
— apenas contínuo, sem nenhuma estimativa. O que se constrói é a
infraestrutura de tipo: que a integral de Bochner que define o termo de
Duhamel está bem definida (integrável) dado `u` contínua e `B` contínua,
usando a continuidade forte de `heatOpL2` que acabou de ser provada. Sem
essa peça, nem sequer o ENUNCIADO de "solução branda" é expressável em
Lean neste laboratório.

## O que isso NÃO ataca

`NS-GAP-001`/`004` (a estimativa não-local do Hessiano de pressão) é
exatamente o que daria a `B` suas propriedades quantitativas
(Lipschitz/bilinear estimate) necessárias para rodar um ponto fixo de
Banach. Essa estimativa não é tentada aqui, nem em nenhuma frente
autônoma futura sem justificativa explícita nova.

## Alternativas consideradas e descartadas

```text
Reabrir SC-GAP-002/ENC-GAP-020/RT-GAP-017/YM-GAP-007 como frente de
  construcao -- ja reavaliados em STRATEGIC_REVIEW_BATTLE_MAP_2026_08_09.md,
  nenhum justificado.
Tentar NS-GAP-001 diretamente -- proibido por stop_condition em
  NS-PRESSURE-001 e pela avaliação estrutural registrada (dificuldade
  comparável a criterios de regularidade condicional nunca verificados
  a priori).
```

## Registro

`FOUND-DUHAMEL-SKELETON-001` registrado em `RESEARCH_QUEUE.yaml`, escopo
delimitado por `stop_condition` explícito.

## Trava

`authorized_action: FORMALIZATION`. Revisão de portfólio consumida ao
fechar a frente.
