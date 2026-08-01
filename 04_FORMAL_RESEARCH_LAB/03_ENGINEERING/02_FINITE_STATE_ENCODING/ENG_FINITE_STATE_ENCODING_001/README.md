---
work_item_id: ENG-FINITE-STATE-ENCODING-001
title: Certified Finite-State Encoding and Table Construction
stage: SPECIFICATION
status: READY_FOR_REVIEW
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
---

# ENG-FINITE-STATE-ENCODING-001

## O que a frente faz

```text
sistema deterministico tipado
        |  codificacao certificada FORNECIDA
Fin n -> Fin n
        |  Array.ofFn
ValidatedTransitionTable
        |  runtime adapter existente
analyzeTransitionTable
        |  interpretacao
repeticao PROVADA no sistema tipado original
```

O consumidor fornece três coisas e nada mais:

```text
CertifiedFiniteEncoding S n
stepS : S -> S
start : S
```

**Zero typeclasses.** Sem `Fintype S`, sem `DecidableEq S`, sem
`Nonempty`, sem `Inhabited`.

## O que muda em relação à frente anterior

`ENG-FINITE-STATE-RUNTIME-001` provou algo sobre **a tabela**. Esta
frente prova algo sobre **a relação entre a tabela e o sistema**.

A soundness anterior termina numa igualdade entre resultados de `run?`
sobre um `Array Nat`. A soundness desta frente termina numa igualdade
**em `S`**:

```lean
stepS^[w.baseIndex + w.period] start = stepS^[w.baseIndex] start
```

## Estado da especificação

Todos os treze resultados `ENC-CORE` foram **demonstrados em probe
descartável**, não apenas planejados. Dois probes, ambos exit `0`, ambos
removidos ao final.

```text
probe 1   estrutura, tabela, tamanho, indice, comutacoes, run?
probe 2   analise dinamica, soundness, completeness, oito testes
```

## Ordem de leitura

```text
SPECIFICATION_DECISION.md
DATA_MODEL.md
ENCODING_LAWS.md
ENCODED_STEP.md
TABLE_CONSTRUCTION.md
ARRAY_SIZE_AND_CAST_POLICY.md
TABLE_INDEX.md
STEP_COMMUTATION.md
SEMICONJUGATION.md
ITERATION_COMMUTATION.md
RAW_RUN_CORRESPONDENCE.md
DYNAMIC_ANALYSIS_BRIDGE.md
SOUNDNESS_PLAN.md
COMPLETENESS_PLAN.md
EMPTY_TYPE_POLICY.md
COMPUTABILITY_BOUNDARY.md
AXIOM_BOUNDARY.md
IMPORT_PLAN.md
LEAN_API_AUDIT.md
TEST_PLAN.md
THEOREM_MAP.md
GAP_REGISTER.yaml
STOP_CONDITIONS.md
CLAIM_BOUNDARY.md
RESULT_BOUNDARY.md
REVIEW_CHECKLIST.md
```

## O que esta frente **não** faz

```text
nao prova que um servico, programa, workflow, agente ou processo
fisico foi modelado corretamente;
nao cria CLI, parser, JSON, extracao ou integracao;
nao modifica o runtime adapter nem o detector;
nao apresenta algoritmo novo;
nao apresenta novidade matematica.
```


---

## Revisão — `2066edc`

`specification_status: APPROVED`. Documentos da frente: **39**.

Ordem de leitura vigente após a revisão: começar por
`SPECIFICATION_REVIEW.md` e `REVIEW_DECISION.md`, depois os seis
`FINAL_*`, e só então os documentos de especificação, que permanecem como
registro histórico.
