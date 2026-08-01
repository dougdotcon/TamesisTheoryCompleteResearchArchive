---
document_id: ENC-THEOREM-MAP
core_results: 13
probe_status_summary: "13 PROBE_PROVED"
---

# Mapa de teoremas

| Id | Declaração | Categoria | Estado no probe |
|---|---|---|---|
| `ENC-CORE-001` | `CertifiedFiniteEncoding` | `PUBLIC_EXECUTABLE_CORE` | `PROBE_PROVED` |
| `ENC-CORE-002` | `CertifiedFiniteEncoding.encode_injective` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-003` | `CertifiedFiniteEncoding.encodedStep` | `PUBLIC_EXECUTABLE_CORE` | `PROBE_PROVED` |
| `ENC-CORE-004` | `buildTransitionTable` | `PUBLIC_EXECUTABLE_CORE` | `PROBE_PROVED` |
| `ENC-CORE-005` | `buildTransitionTable_size` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-005b` | `buildTransitionTable_getElem` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-006` | `CertifiedFiniteEncoding.tableIndex` | `PUBLIC_EXECUTABLE_CORE` | `PROBE_PROVED` |
| `ENC-CORE-007` | `tableIndex_val` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED`, por `rfl` |
| `ENC-CORE-008` | `table_step_commutes` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-008b` | `tableIndex_semiconj` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-009` | `table_iterate_commutes` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-010` | `run?_corresponds_to_typed_iterate` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-011` | `analyzeEncodedSystem` | `PUBLIC_EXECUTABLE_CORE` | `PROBE_PROVED` |
| `ENC-CORE-012` | `analyzeEncodedSystem_sound` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| `ENC-CORE-013` | `analyzeEncodedSystem_complete` | `PUBLIC_SPECIFICATION_CORE` | `PROBE_PROVED` |
| — | `analyzeEncodedSystem_ne_error` | `PUBLIC_COROLLARY` | `PROBE_PROVED` |
| — | `CertifiedFiniteEncoding.decode_surjective` | `OPTIONAL_ADAPTER` | `PROBE_PROVED` |

`ENC-CORE-005b` e `ENC-CORE-008b` são subdivisões declaradas dos itens
`005` e `008` da lista do portfólio, mantendo rastreabilidade.

## DAG global

```text
CertifiedFiniteEncoding
  ├─ encode_injective ──────────────────────────────┐
  └─ encodedStep                                    │
       └─ buildTransitionTable                      │
            ├─ buildTransitionTable_size            │
            │    ├─ buildTransitionTable_getElem    │
            │    └─ tableIndex                      │
            │         └─ tableIndex_val ────────┐   │
            └─ (campo closed) ─ toRaw_valid     │   │
                                                │   │
  table_step_commutes  ◄────────────────────────┘   │
       └─ tableIndex_semiconj                       │
            └─ table_iterate_commutes               │
                 └─ run?_corresponds_to_typed_iterate
                      ├─ analyzeEncodedSystem_sound ┘
                      └─ (via toRaw_valid + size)
                           └─ analyzeEncodedSystem_complete
                                └─ analyzeEncodedSystem_ne_error
```

## Herdado das frentes anteriores, sem uma linha nova

```text
ValidatedTransitionTable, .step, .step_val, .toRaw, .toRaw_valid
RawTransitionTable.run?
ValidatedTransitionTable.run?_eq_iterate_step
analyzeTransitionTable
analyzeTransitionTable_sound
analyzeTransitionTable_complete
RuntimeCycleError
CycleWitness
detectCycle? e seus tres teoremas
```

## Tamanho estimado

```text
estruturas    1
definicoes    4
teoremas     12
linhas       cerca de 260, contra 869 da frente anterior
```
