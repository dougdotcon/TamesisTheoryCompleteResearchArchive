---
document_id: PORTFOLIO-REVIEW-CYCLE-DETECTION
gate: PORTFOLIO_REVIEW
reviewed_at: 2026-07-31
reviewed_commit: 49924c3fe9b5cc2eab0cdea12c3554fc537c051d
decision: A_PORTFOLIO_REVIEW_APPROVED_CYCLE_DETECTION_SELECTED
selected_work_item: FOUND-CYCLE-DETECTION-001
duplicate_found: false
lean_files_created: 0
---

# Revisão de portfólio — detecção executável de ciclos

Revisão do estado do portfólio após o encerramento de
`FOUND-FUNCTIONAL-GRAPH-001`. **Nenhuma pesquisa matemática das frentes
rejeitadas foi iniciada. Nenhum arquivo Lean foi criado.**

## Frentes encerradas e congeladas

```yaml
FOUND-SEMIGROUP-002:
  work_status: VERIFIED
  result_review: APPROVED
  extension_status: NOT_AUTHORIZED

FOUND-FUNCTIONAL-GRAPH-001:
  work_status: VERIFIED
  specification_status: APPROVED
  formalization_status: VERIFIED
  result_review: APPROVED
  extension_status: NOT_AUTHORIZED
  mathematical_novelty: NONE

RH-NOGO-001:
  work_status: FROZEN_PARTIAL_RESULT
  authorization_state: NOT_AUTHORIZED
  execution_state: NO_EXECUTION
  concrete_layer_status: DEFERRED
```

Nenhum `extension_status` foi alterado. Nenhum módulo matemático dessas
frentes foi tocado. O novo item é **independente** e reutiliza APIs
verificadas; não é extensão de nenhuma delas.

## Itens ainda não executados

Seis itens permanecem na fila sem execução. Todos foram reavaliados.

### NS-PRESSURE-001

```yaml
work_item: NS-PRESSURE-001
scientific_value: alto — auditoria de um lema quantitativo real
formalization_cost: high
mathlib_readiness: baixa — EDP e fluidos praticamente ausentes
dependency_risk: alto — depende de análise de EDP externa
counterexample_access: medium
software_reuse: nenhum
poc_30_day_feasibility: NO
reason_selected_or_rejected: >
  Rejeitado. Problema Clay; a Mathlib não sustenta a camada de EDP
  necessária, e o item cai integralmente na lista de evitar já usada nos
  dois gates de seleção anteriores.
```

### PVSNP-PHYS-001

```yaml
work_item: PVSNP-PHYS-001
scientific_value: médio — definições novas, sem teorema forte à vista
formalization_cost: medium
mathlib_readiness: parcial — complexidade não é área madura na Mathlib
dependency_risk: alto — a ponte física/computacional é o próprio risco
counterexample_access: high
software_reuse: nenhum
poc_30_day_feasibility: NO
reason_selected_or_rejected: >
  Rejeitado. Vizinho de problema Clay, e o valor esperado concentra-se em
  definições cuja adequação não é verificável dentro do laboratório.
```

### YM-LIMIT-001

```yaml
work_item: YM-LIMIT-001
scientific_value: alto em tese
formalization_cost: very_high
mathlib_readiness: nenhuma — QFT construtiva ausente
dependency_risk: muito alto
counterexample_access: medium
software_reuse: nenhum
poc_30_day_feasibility: NO
reason_selected_or_rejected: >
  Rejeitado. Custo desproporcional e infraestrutura formal inexistente.
```

### HODGE-CDK-001

```yaml
work_item: HODGE-CDK-001
scientific_value: médio — auditoria bibliográfica
formalization_cost: high
mathlib_readiness: parcial em geometria algébrica, insuficiente para o alvo
dependency_risk: alto
counterexample_access: medium
software_reuse: nenhum
poc_30_day_feasibility: NO
reason_selected_or_rejected: >
  Rejeitado. Custo bibliográfico muito alto e nenhum produto formal
  pequeno identificável.
```

### BSD-HYP-MATRIX-001

```yaml
work_item: BSD-HYP-MATRIX-001
scientific_value: médio — matriz de hipóteses é produto documental
formalization_cost: high
mathlib_readiness: parcial — curvas elípticas existem, Iwasawa não
dependency_risk: alto
counterexample_access: medium
software_reuse: nenhum
poc_30_day_feasibility: NO
reason_selected_or_rejected: >
  Rejeitado. O produto seria essencialmente bibliográfico, e o custo de
  leitura primária excede o orçamento de um ciclo.
```

### TOE-INTERFACE-001

```yaml
work_item: TOE-INTERFACE-001
scientific_value: declarado alto, não verificável
formalization_cost: very_high
mathlib_readiness: baixa
dependency_risk: BLOQUEANTE
counterexample_access: medium
software_reuse: nenhum
poc_30_day_feasibility: NO
reason_selected_or_rejected: >
  Rejeitado, e por motivo estrutural: depende de RH-NOGO-001, que está
  FROZEN_PARTIAL_RESULT com camada concreta diferida. A dependência é
  bloqueante e não pode ser removida por este gate.
```

## Alvo avaliado

```yaml
work_item: FOUND-CYCLE-DETECTION-001
title: Executable Cycle Detection for Finite Deterministic Systems
scientific_value: nulo em novidade, alto em valor formal
formalization_cost: moderate
mathlib_readiness: ALTA — Fintype, DecidableEq, Nat, List/Finset, well-founded recursion
dependency_risk: baixo — depende só de material VERIFIED do próprio laboratório
counterexample_access: HIGH — modelos finitos explícitos, avaliação por decide
software_reuse: VERY_HIGH
poc_30_day_feasibility: YES
reason_selected_or_rejected: >
  Selecionado. Ataca uma lacuna concreta e registrada do resultado
  imediatamente anterior, reutiliza APIs verificadas sem estendê-las,
  é finito e decidível, e não toca em física, EDP, análise espectral nem
  em qualquer conjectura Clay.
```

## Verificação de duplicata

Busca no laboratório inteiro por alvo semanticamente equivalente:

```text
CYCLE-DETECTION / CYCLE_DETECTION   0 ocorrencias como work item
detectCycle / cycleDetect           0 ocorrencias
Floyd / Brent / tortoise            aparecem SOMENTE como material
                                    explicitamente declarado FORA de escopo
```

As três ocorrências relevantes são declarações de fronteira, não trabalho
executado:

| Arquivo | Registro |
|---|---|
| `FOUND_SEMIGROUP_002/KNOWN_RESULTS_MATRIX.md` | "Detecção de ciclo (tortoise and hare) — algoritmo clássico — **fora de escopo**" |
| `FOUND_SEMIGROUP_002/REUSE_MATRIX.md` | "executável (Floyd, Brent) exigiria construção computacional que está [fora]" |
| `FOUND_FUNCTIONAL_GRAPH_001/REUSE_MATRIX.md` | `computational_use: "NÃO — o algoritmo (Floyd, Brent) teria de ser escrito à parte"` |

```text
duplicata: NAO ENCONTRADA
```

O novo item não duplica: ele executa exatamente o que as duas frentes
anteriores registraram como não feito.

Confirmado também que **nenhuma** definição executável de detecção de
ciclo existe no núcleo Lean: os únicos `def` em `Foundations/` são as três
relações proposicionais de `FunctionalGraphs/Relations.lean`, `Reachable`,
`IsInvariant` e as funções de transição dos contraexemplos.

## Critérios de rejeição do alvo

Nenhum ocorreu.

| Critério de rejeição | Verificado |
|---|---|
| item equivalente já concluído | não existe |
| dependência formal material ausente | `exists_eventual_period` e `exists_bounded_iterate_collision` estão `VERIFIED` |
| algoritmo incompatível com o Lean fixado | Floyd, tabela visitada e Brent são exprimíveis em Lean 4.33.0-rc1 |
| custo estimado desproporcional | `MODERATE`, com PoC de 30 dias viável |
| resultado pretendido falso | o resultado é clássico e verdadeiro para tipos finitos |

## Decisão

```text
A. PORTFOLIO_REVIEW_APPROVED_CYCLE_DETECTION_SELECTED
```

Item criado como `SCOPED`. Autorizada **apenas** a preparação da
especificação.
