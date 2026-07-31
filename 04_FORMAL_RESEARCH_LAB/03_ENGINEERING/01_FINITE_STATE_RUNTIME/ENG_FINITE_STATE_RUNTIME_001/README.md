---
document_id: RT-README
work_item_id: ENG-FINITE-STATE-RUNTIME-001
specification_status: READY_FOR_REVIEW
lean_files_created: 0
---

# ENG-FINITE-STATE-RUNTIME-001 — especificação

*Certified Runtime Adapter for Finite Deterministic Systems.*

> **Especificação apenas.** Nenhum módulo Lean permanente, nenhuma prova
> permanente, nenhum adaptador, nenhum binário, nenhum `lake build`.

## A ponte

```text
dados dinamicos          sistema formal
Array Nat        ---->   Fin n -> Fin n
```

para permitir a aplicação segura do detector já verificado
`FOUND-CYCLE-DETECTION-001.detectCycleWitness?`.

## As quatro decisões congeladas

```text
entrada bruta        Array Nat
tabela vazia         estruturalmente valida
destino invalido     erro, nunca modulo/clamp/fallback
resultado dinamico   Except RuntimeCycleError CycleWitness
```

O `CycleWitness` é devolvido diretamente pela camada dinâmica, **sem**
totalizar o detector anterior: o eventual `none` vira
`internalDetectorFailure`, ramo defensivo que a correção prova impossível
para entradas válidas.

## Ordem de leitura

```text
TARGET_RESULT.md             o que se quer
RAW_DATA_MODEL.md            RawTransitionTable
VALIDITY_MODEL.md            Valid e as formulacoes alternativas
VALIDATED_DATA_MODEL.md      ValidatedTransitionTable
ERROR_MODEL.md               RuntimeCycleError
VALIDATION_API.md            validateTransitionTable
START_STATE_VALIDATION.md    validateStart
TYPED_TRANSITION_API.md      step e step_val
RAW_EXECUTION_SEMANTICS.md   step? e run?
ITERATION_CORRESPONDENCE.md  run?_eq_iterate_step
DETECTOR_ADAPTER.md          detectCycle?
DYNAMIC_ANALYSIS_API.md      analyzeTransitionTable
CORRECTNESS_PLAN.md          soundness
COMPLETENESS_PLAN.md         completeness
COMPUTABILITY_BOUNDARY.md    o que executa e o que nao
LEAN_API_AUDIT.md            APIs auditadas no checkout
TEST_PLAN.md                 nove casos
THEOREM_CANDIDATES.md        CORE e OPTIONAL_COROLLARY
THEOREM_DEPENDENCY_MAP.md    o DAG
GAP_REGISTER.yaml            vinte e duas lacunas
STOP_CONDITIONS.md           vinte e uma condicoes
NOVELTY_BOUNDARY.md          novidade zero
SPECIFICATION_DECISION.md    a decisao
```

## Limites

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

## Nota sobre a localização

Esta pasta vive em `03_ENGINEERING/`, ao lado de `03_MILLENNIUM/`. O
prefixo numérico repetido segue o caminho literal fixado pelo gate; há
precedente no próprio repositório, onde `02_FOUNDATIONS/` contém
`04_FUNCTIONAL_GRAPHS/` e `04_MONOTONES/`.
