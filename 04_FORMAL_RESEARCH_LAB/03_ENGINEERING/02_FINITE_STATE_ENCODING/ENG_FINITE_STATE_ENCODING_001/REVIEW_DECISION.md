---
document_id: ENC-REVIEW-DECISION
decision: A_ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_APPROVED
reviewed_at_commit: 2066edc165ace0fbf4e183303e30c4ced246aaaa
stop_conditions_triggered: 0
---

# Decisão da revisão

```text
A. ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_APPROVED
```

## Critérios de aprovação, um a um

| Critério | Evidência |
|---|---|
| codificação fornecida e executável | quatro campos; `#eval` em sete modelos |
| duas leis com papéis claros | `decode_encode` = dependência de prova; `encode_decode` = contrato, medido pela seção `WeakEncoding` |
| nenhum `Fintype S` | zero ocorrências nas 14 declarações |
| nenhum `DecidableEq S` | zero ocorrências |
| construção pública única | `buildTransitionTable`; nenhuma concorrente |
| tabela validada por construção | campo `closed`; `validateTransitionTable` não é chamada |
| igualdade de tamanho congelada | `size = n`, orientação única |
| casts centralizados | **dois** pontos, um em cada direção |
| `tableIndex_val` preserva o `Nat` | `rfl`, e `@[simp]`; conferido por `decide` sob permutação |
| o passo comuta | `tableIndex_semiconj`, seis linhas |
| semiconjugação orientada corretamente | orientação registrada; comutação é o `.symm` |
| iteradas comutam | `Semiconj.iterate_right`, um termo |
| `run?` corresponde à dinâmica tipada | lado bruto começa em `encode`, não em `tableIndex` |
| soundness termina em `S` | `encode_injective` é a última seta do DAG |
| completeness reutiliza o adapter | `analyzeTransitionTable_complete`; sem pré-condições |
| nenhuma escolha clássica produz dado | `grep` zero; `#eval` funciona |
| caso vazio coerente | tabela `#[]`; chamada de análise não habitada |
| invariância do witness concreto **não** afirmada | `ENC-GAP-020`, `STOP-ENC-019` |
| limites externos explícitos | `RESULT_BOUNDARY.md` preservado; `RT-GAP-017` intacto |
| probes compilam integralmente | probe principal exit `0`, zero erros |

**Zero stop conditions disparadas.**

## As três decisões pedidas

```yaml
encode_decode:
  decision: KEEP
  role: PUBLIC_CONTRACT, nao dependencia de prova

encodedStep:
  decision: PUBLIC_EXECUTABLE_CORE
  reason: unico nome publico do conteudo da tabela, apos o auxiliar virar interno

axiom_footprint:
  decision: ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT
  reason: rota leve inviavel para n generico; o adapter reutilizado ja carrega os tres axiomas
```

## Correções aplicadas

```text
1. tableIndex_semiconj passa a teorema semantico principal
2. table_step_commutes passa a PUBLIC_COROLLARY
3. buildTransitionTable_getElem passa a INTERNAL_HELPER
4. tableIndex_val recebe @[simp]
5. declaracoes movidas para o namespace CertifiedFiniteEncoding
```

Declarações públicas: **16 → 14**.

## Autorização

```yaml
authorized_action: ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED
```

Uma entrada literal, sem wildcard. Extração, CLI, parser e integração
permanecem **não autorizadas**, e nenhuma frente encerrada foi tocada.

## O que a formalização deve preservar

```text
uma unica tabela publica;
dois pontos controlados de transporte;
zero escolha classica produzindo dado executavel.
```

Este é o critério decisivo declarado pelo gate, e é o que o probe
demonstrou ser alcançável.


---

## Correção de validação — `ENC-VAL-001`

A decisão permanece:

```text
A. ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_APPROVED
```

Um dos vinte critérios — *"os probes compilam integralmente"* — foi
declarado satisfeito indevidamente: o probe de axiomas havia terminado
com `exit 1`. O gate corretivo separou os experimentos negativos e
reexecutou ambos os arquivos com `exit 0`.

```text
a decisao A so se tornou integralmente valida apos o gate corretivo.
```

Entre `751cef8` e o commit corretivo, a autorização de formalização
esteve **suspensa**.
