---
document_id: ENC-METADATA-NORMALIZATION-RECORD
deviations: 3
---

# Registro das correções de metadados

## `META-ENC-001` — contagem da API

```yaml
metadata_deviation:
  id: META-ENC-001
  classification: ACKNOWLEDGED_NON_MATERIAL
  mathematical_impact: NONE
  api_impact: NONE
  correction: COUNT_ALIGNED_WITH_LIST
```

`FINAL_PUBLIC_API.md` declarava `public_declarations: 14` no cabeçalho e
listava **quinze** itens no corpo. A contagem foi alinhada à lista.

**Verificação independente feita nesta revisão**: as declarações foram
extraídas dos quatro módulos por expressão regular sobre
`^(private )?(structure|def|theorem|instance)`.

```text
publicas   15   = 1 structure + 4 def + 10 theorem
privadas    1   = 1 theorem
```

A lista derivada coincide item a item com a documentada. O número escrito
estava errado; a API nunca esteve.

## `META-ENC-002` — chaves duplicadas na fila

```yaml
metadata_deviation:
  id: META-ENC-002
  classification: ACKNOWLEDGED_NON_MATERIAL
  mathematical_impact: NONE
  governance_semantic_impact: NONE
  correction: DUPLICATE_KEYS_NORMALIZED
```

### Comparação semântica, `751cef8` contra o estado final

```text
campos removidos       nenhum
campos alterados       status              READY -> VERIFIED
                       formalization_status NOT_STARTED -> VERIFIED
                       authorized_next_gate FORMALIZATION -> RESULT_REVIEW
                       public_declarations  14 -> 15      (META-ENC-001)
campos acrescentados   9, todos de medicao
```

As quatro alterações são exatamente as que o gate de formalização devia
fazer. **Nenhuma** delas é efeito colateral da normalização.

### Invariantes de governança, conferidos um a um

```text
work_item_id, title, track, dependencies, priority_class,
mathematical_novelty, algorithmic_novelty, research_role,
target_statement, stop_condition, dependency_depth,
external_dependency, encoding_source_policy
```

Todos **IGUAIS**. A normalização não mudou o valor efetivo de nenhum
campo do item: as duplicatas remanescentes tinham valores idênticos, e a
remoção manteve a primeira ocorrência.

## `META-ENC-003` — achado novo, fora da frente

```yaml
metadata_finding:
  id: META-ENC-003
  scope: OUTSIDE_THIS_WORK_ITEM
  classification: PRE_EXISTING_DEFECT
  action_taken: NONE
  requires: EXPLICIT_CORRECTIVE_GATE
```

A varredura exaustiva da fila encontrou duplicatas em **três** itens:

```text
FOUND-CYCLE-DETECTION-001.total_wrapper_status   ['DEFERRED', 'DEFERRED']
ENG-FINITE-STATE-RUNTIME-001.tests_planned       ['9', '8']
ENG-FINITE-STATE-ENCODING-001.encoding_source_policy   identicas
```

A segunda é **divergente**: o parser YAML usa a última ocorrência, logo o
valor efetivo é `8`, enquanto `9` aparece antes e é silenciosamente
descartado. Qual das duas é correta não é decidível a partir da fila, e
`ENG-FINITE-STATE-RUNTIME-001` é frente **encerrada**.

Nenhuma foi alterada. O registro fica aberto para um gate corretivo
explícito.

Vale dizer com todas as letras: a verificação anterior declarou "sem
chaves duplicadas" tendo conferido **duas chaves nomeadas**, não todas.
Uma checagem parcial apresentada como completa é o mesmo defeito que
`ENC-VAL-001` — evidência mais fraca do que a afirmação que sustenta.
