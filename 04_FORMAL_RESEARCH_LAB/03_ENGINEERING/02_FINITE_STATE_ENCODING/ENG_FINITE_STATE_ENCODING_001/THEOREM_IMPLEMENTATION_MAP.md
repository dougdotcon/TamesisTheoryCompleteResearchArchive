---
document_id: ENC-THEOREM-IMPLEMENTATION-MAP
---

# Mapa de implementação

| Id | Declaração | Módulo | Categoria | Forma |
|---|---|---|---|---|
| `ENC-CORE-001` | `CertifiedFiniteEncoding` | `Encoding.lean` | `PUBLIC_EXECUTABLE_CORE` | estrutura, 4 campos |
| `ENC-CORE-002` | `CertifiedFiniteEncoding.encode_injective` | `Encoding.lean` | `PUBLIC_SPECIFICATION_CORE` | termo, 1 linha |
| `ENC-CORE-003` | `CertifiedFiniteEncoding.encodedStep` | `Encoding.lean` | `PUBLIC_EXECUTABLE_CORE` | definição, 1 linha |
| `ENC-CORE-004` | `buildTransitionTable` | `TableConstruction.lean` | `PUBLIC_EXECUTABLE_CORE` | `Array.ofFn` + `closed` |
| `ENC-CORE-005` | `buildTransitionTable_size` | `TableConstruction.lean` | `PUBLIC_SPECIFICATION_CORE` | `@[simp]`, termo |
| `ENC-CORE-005b` | `buildTransitionTable_getElem` | `Commutation.lean` | `INTERNAL_HELPER` | `private`, termo |
| `ENC-CORE-006` | `CertifiedFiniteEncoding.tableIndex` | `TableConstruction.lean` | `PUBLIC_EXECUTABLE_CORE` | `Fin.cast` |
| `ENC-CORE-007` | `CertifiedFiniteEncoding.tableIndex_val` | `TableConstruction.lean` | `PUBLIC_SPECIFICATION_CORE` | `@[simp]`, `rfl` |
| `ENC-CORE-008b` | `CertifiedFiniteEncoding.tableIndex_semiconj` | `Commutation.lean` | `PUBLIC_SPECIFICATION_CORE` | 6 linhas |
| `ENC-CORE-008` | `CertifiedFiniteEncoding.table_step_commutes` | `Commutation.lean` | `PUBLIC_COROLLARY` | `.symm`, 1 linha |
| `ENC-CORE-009` | `CertifiedFiniteEncoding.table_iterate_commutes` | `Commutation.lean` | `PUBLIC_SPECIFICATION_CORE` | termo, 1 linha |
| `ENC-CORE-010` | `CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate` | `Commutation.lean` | `PUBLIC_SPECIFICATION_CORE` | 3 linhas |
| `ENC-CORE-011` | `analyzeEncodedSystem` | `DynamicAnalysis.lean` | `PUBLIC_EXECUTABLE_CORE` | definição, 1 linha |
| `ENC-CORE-012` | `analyzeEncodedSystem_sound` | `DynamicAnalysis.lean` | `PUBLIC_SPECIFICATION_CORE` | 4 linhas |
| `ENC-CORE-013` | `analyzeEncodedSystem_complete` | `DynamicAnalysis.lean` | `PUBLIC_SPECIFICATION_CORE` | 5 linhas |
| — | `analyzeEncodedSystem_ne_error` | `DynamicAnalysis.lean` | `PUBLIC_COROLLARY` | 4 linhas |

Treze resultados CORE, todos implementados. Nenhum foi enfraquecido em
relação à especificação revisada.

## DAG realizado

```text
CertifiedFiniteEncoding
  ├─ encode_injective ─────────────────────────────┐
  └─ encodedStep                                   │
       └─ buildTransitionTable  (campo closed)     │
            ├─ buildTransitionTable_size           │
            │    ├─ buildTransitionTable_getElem   │
            │    └─ tableIndex                     │
            │         └─ tableIndex_val ───────┐   │
            └─ toRaw_valid                     │   │
                                               │   │
  tableIndex_semiconj  ◄───────────────────────┘   │
       ├─ table_step_commutes                      │
       └─ table_iterate_commutes                   │
            └─ run?_corresponds_to_typed_iterate   │
                 ├─ analyzeEncodedSystem_sound ────┘
                 └─ analyzeEncodedSystem_complete
                      └─ analyzeEncodedSystem_ne_error
```

## Consumido das frentes anteriores, sem uma linha nova

```text
ValidatedTransitionTable, .step, .step_val, .toRaw, .toRaw_valid
ValidatedTransitionTable.run?_eq_iterate_step
RawTransitionTable.run?
analyzeTransitionTable
analyzeTransitionTable_sound
analyzeTransitionTable_complete
RuntimeCycleError
CycleWitness
```

Medido: `analyzeTransitionTable` 4 ocorrências, `_sound` 2, `_complete` 1,
`run?_eq_iterate_step` 1, `toRaw_valid` 2, `step_val` 1.
