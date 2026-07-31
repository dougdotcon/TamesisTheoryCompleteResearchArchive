---
document_id: FCD-CLOSURE-RECORD
work_item_id: FOUND-CYCLE-DETECTION-001
closed_at: 2026-08-01
closed_at_commit: d9d672caf817fdb6d0b2dd27a6bf5355bc8739fe
result_review: APPROVED
extension_status: NOT_AUTHORIZED
---

# Registro de encerramento

## O que a frente entregou

**A primeira fundação algorítmica executável do laboratório.**

```text
teorema existencial ja verificado
        |
enumeracao executavel
        |
detector Option CycleWitness
        |
soundness + completeness
        |
certificado de periodicidade
```

Um programa Lean que, para qualquer estado inicial de um sistema
determinístico finito com igualdade decidível, devolve um par
`⟨baseIndex, period⟩` — e está **provado** que esse par satisfaz o
contrato e que ele sempre existe.

## Números

```text
estruturas      1
definicoes      3
instancias      1
teoremas        8
testes          5, todos exit 0
regressoes      16, por decide, sem native_decide
linhas Lean     609 no nucleo e nos tres testes originais
documentos      43
lacunas         19: 10 resolvidas, 9 abertas
claims          1, a vigesima do ledger
```

## O que **não** foi entregue

```text
funcao total sem Option
minimalidade de baseIndex ou de period
Floyd, Brent, tabela visitada
complexidade formal
extracao de binario
integracao externa
adaptador de componente funcional
periodicOrbit computavel
novidade matematica ou algoritmica
```

## Estado de encerramento

```yaml
work_status: VERIFIED
specification_status: APPROVED
formalization_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED

totalization_status: DEFERRED
extraction_status: NOT_AUTHORIZED
optimization_status: NOT_AUTHORIZED
minimality_status: NOT_AUTHORIZED
```

## Desvio de governança

```text
GOV-CD-001: ACKNOWLEDGED_NON_MATERIAL
```

Ver `GOVERNANCE_DEVIATION_REVIEW.md`. O desvio foi real; o dano, nulo. A
regra normativa futura — parar com `GATE_POST_COMMIT_VALIDATION_FAILED`
quando ambas as correções estiverem proibidas — passa a valer a partir
deste gate.

## Condições de reabertura

A frente só volta a ser tocada por um gate explícito. Em particular,
**nada** do seguinte está autorizado por consequência deste encerramento:

```text
totalizacao
Floyd, Brent ou tabela visitada
minimalidade
complexidade formal
extracao
integracao
FOUND-CYCLE-DETECTION-002
```

## Valor registrado

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```

A busca limitada por certificado é a implementação ingênua contra a qual
Floyd e Brent foram propostos como melhorias. O valor está na execução
verificada dentro do Lean, na correção e na completude formais, nos
certificados produzidos, e na reutilização de duas fundações anteriores
sem repetir nenhuma delas.
