---
document_id: META-ENC-003-CORRECTION-RECORD
deviation_id: META-ENC-003
classification: GOVERNANCE_DATA_AMBIGUITY
status: CORRECTED
corrected_at_commit: e9e2ce7e3ba589425942efd5b551cf03570334bc
---

# Registro da correção de `META-ENC-003`

```yaml
metadata_deviation:
  id: META-ENC-003
  classification: GOVERNANCE_DATA_AMBIGUITY
  source: RESEARCH_QUEUE.yaml
  duplicate_scope: REPOSITORY_WIDE_AUDIT_REQUIRED
  mathematical_impact: NONE
  formal_proof_impact: NONE
  parser_behavior: SILENT_LAST_VALUE_WINS
  portfolio_review_blocked: true
```

## O problema, enunciado corretamente

```text
O problema nao eh apenas a existencia de um valor aparentemente
incorreto.

O problema eh que um mapa YAML possui mais de uma definicao para a
mesma chave e o parser descarta silenciosamente parte do documento.

Enquanto isso for permitido, a representacao textual da governanca nao
possui semantica univoca.
```

## Inventário — a varredura integral

```yaml
yaml_files_scanned: 55
documents_scanned: 55
mappings_scanned: 470
sequences_scanned: 320
scalars_scanned: 3471
unparsable_files: 0
duplicate_occurrences: 8
files_with_duplicates: 3
identical_duplicates: 5
divergent_duplicates: 3
```

O relatório anterior falava em duplicatas em **três itens**, todos dentro
de `RESEARCH_QUEUE.yaml`. A varredura integral encontrou **oito
ocorrências em três arquivos**, e duas divergências que ninguém havia
visto — porque a busca anterior olhou apenas a fila.

### Tabela completa

| Arquivo | Caminho | Chave | Linhas | Valores | Classificação |
|---|---|---|---|---|---|
| `RESEARCH_QUEUE.yaml` | `queue[12]` | `total_wrapper_status` | 402 / 409 | `DEFERRED` / `DEFERRED` | `IDENTICAL` |
| `RESEARCH_QUEUE.yaml` | `queue[13]` | `tests_planned` | 505 / 518 | `9` / `8` | **`DIVERGENT`** |
| `RESEARCH_QUEUE.yaml` | `queue[14]` | `extraction_status` | 572 / 603 | `NOT_AUTHORIZED` / idem | `IDENTICAL` |
| `RESEARCH_QUEUE.yaml` | `queue[14]` | `cli_status` | 573 / 604 | `NOT_AUTHORIZED` / idem | `IDENTICAL` |
| `RESEARCH_QUEUE.yaml` | `queue[14]` | `parser_status` | 574 / 605 | `NOT_AUTHORIZED` / idem | `IDENTICAL` |
| `RESEARCH_QUEUE.yaml` | `queue[14]` | `integration_status` | 575 / 606 | `NOT_AUTHORIZED` / idem | `IDENTICAL` |
| `FOUND_CYCLE_DETECTION_001/STATUS.yaml` | `<root>` | `extraction_status` | 11 / 72 | `NOT_AUTHORIZED` / `READY_FOR_FEASIBILITY_AUDIT` | **`DIVERGENT`** |
| `ENG_FINITE_STATE_ENCODING_001/STATUS.yaml` | `<root>` | `documents` | 56 / 76 | `39` / `65` | **`DIVERGENT`** |

## `tests_planned` — resolvido por fonte de verdade

```yaml
field: tests_planned
duplicate_values: [9, 8]
parser_effective_value_before: 8
field_semantics: >
  numero de casos de teste CONGELADOS na especificacao da frente, no
  TEST_PLAN.md. Nao eh o numero de casos executados, nem de arquivos de
  teste Lean, nem de teoremas de regressao.
authoritative_source:
  - 03_ENGINEERING/01_FINITE_STATE_RUNTIME/ENG_FINITE_STATE_RUNTIME_001/TEST_PLAN.md
  - 03_ENGINEERING/01_FINITE_STATE_RUNTIME/ENG_FINITE_STATE_RUNTIME_001/STATUS.yaml
authoritative_value: 9
correction: B_UPDATED_TO_SOURCE_OF_TRUTH
semantic_change_from_parser_effective_value: true
classification: NON_MATHEMATICAL_GOVERNANCE_SEMANTIC_CORRECTION
mathematical_impact: NONE
test_artifact_impact: NONE
```

### A evidência

```text
TEST_PLAN.md, front matter        tests: 9
TEST_PLAN.md, secoes              RT-TEST-001 a RT-TEST-009  = 9 casos
STATUS.yaml da frente             tests_planned: 9
fila, linha 505                   9      escrita no gate de especificacao
fila, linha 518                   8      escrita no gate de formalizacao
portfolio-review-...-result.json  lista de 8 nomes, RT-TEST-001..008
```

O `8` é a contagem da **seleção de portfólio**, anterior ao congelamento
da especificação, que acrescentou `RT-TEST-009 — dois componentes`. Ela
foi copiada para a fila num gate posterior e passou a coexistir com o
`9`.

A comparação com a frente vizinha confirma a semântica: em
`FOUND-CYCLE-DETECTION-001`, a fila, o `TEST_PLAN.md` e o `STATUS.yaml`
dizem `7`, os três de acordo.

E a distinção que o gate pediu está registrada: a formalização do
runtime executou **10** casos concretos e o `STATUS.yaml` da frente traz
`tests_formalized: 10`. `tests_planned` e `tests_formalized` são campos
diferentes, com números diferentes, e nenhum dos dois é o número de
arquivos `.lean` (que são 4).

### A honestidade exigida

O valor final, `9`, **difere** do valor que o parser vinha usando, `8`.
Isto não é correção cosmética: é
`NON_MATHEMATICAL_GOVERNANCE_SEMANTIC_CORRECTION`. Nenhum teorema,
nenhuma prova e nenhum artefato de teste muda; o que muda é o que a fila
**diz** sobre a frente.

## `FOUND_CYCLE_DETECTION_001.extraction_status` — a divergência mais séria

```yaml
duplicate_values: [NOT_AUTHORIZED, READY_FOR_FEASIBILITY_AUDIT]
parser_effective_value_before: READY_FOR_FEASIBILITY_AUDIT
authoritative_source:
  - FOUND_CYCLE_DETECTION_001/CLOSURE_RECORD.md
  - LAB_STATE.md, closed_work_items
authoritative_value: NOT_AUTHORIZED
correction: B_UPDATED_TO_SOURCE_OF_TRUTH
semantic_change_from_parser_effective_value: true
```

O `STATUS.yaml` de uma frente **encerrada** vinha sendo lido como
`READY_FOR_FEASIBILITY_AUDIT` — uma trava **mais fraca** do que a que a
governança de fato mantém. `CLOSURE_RECORD.md` e `LAB_STATE.md` dizem
`NOT_AUTHORIZED`, e é esse o valor que fica.

O valor de estágio de especificação não foi apagado da história: ele
permanece registrado em `COMPUTABILITY_REVIEW.md` daquela frente, que é
onde pertence.

Nenhum estado em `LAB_STATE.md` mudou — ele já dizia `NOT_AUTHORIZED`. O
que mudou foi o arquivo parar de se contradizer.

## `ENG_FINITE_STATE_ENCODING_001.documents`

```yaml
duplicate_values: [39, 65]
parser_effective_value_before: 65
authoritative_source: contagem real do diretorio, por script
authoritative_value: 65
correction: A_SINGLE_DOCUMENTED_VALUE_PRESERVED
semantic_change_from_parser_effective_value: false
```

O `39` era do gate de revisão; o `65`, do encerramento. A contagem real,
verificada, é `65`.

## As cinco duplicatas idênticas

```text
IDENTICAL_DUPLICATE_NORMALIZED, mantida a primeira ocorrencia
```

`total_wrapper_status` em `queue[12]`; `extraction_status`, `cli_status`,
`parser_status` e `integration_status` em `queue[14]`. Nenhuma mudança de
valor efetivo.

## Resultado

```yaml
META-ENC-003:
  status: CORRECTED
  repository_wide_scan: PASS
  duplicate_keys_remaining: 0
  permanent_validator: ACTIVE
  regression_tests: PASS
```

```text
varredura depois:  55 arquivos, 0 duplicatas, 0 arquivos afetados
labctl validate:   PASS
pytest:            21 testes, todos PASS   (eram 9)
claims:            22, inalteradas
work items:        15, inalterados
arquivos Lean:     0 criados, 0 modificados
```
