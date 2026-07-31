---
document_id: FCD-FINAL-GAP-STATUS
total: 19
resolved: 10
open: 9
---

# Estado final das lacunas

## Resolvidas — dez

| Gap | Estado | Evidência |
|---|---|---|
| `CD-GAP-001` | `RESOLVED_BY_DESIGN` | busca limitada congelada e formalizada |
| `CD-GAP-002` | `RESOLVED_FORMALLY` | `CycleWitness` com dois naturais |
| `CD-GAP-003` | `RESOLVED_FORMALLY` | terminação estrutural por `List.find?` |
| `CD-GAP-004` | `RESOLVED_FORMALLY` | `DecidableEq` só na camada executável |
| `CD-GAP-005` | `RESOLVED_FORMALLY` | cota `Fintype.card X`, fronteira incluída |
| `CD-GAP-006` | `RESOLVED_FORMALLY` | `detectCycleWitness?_sound` |
| `CD-GAP-007` | `RESOLVED_FORMALLY` | `CycleWitness.isPeriodicPt` |
| `CD-GAP-008` | `RESOLVED_FORMALLY` | `0 < period` consumido por `mk_mem_periodicPts` |
| `CD-GAP-011` | `RESOLVED_FORMALLY` | `CycleWitness.mem_periodicPts` |
| `CD-GAP-015` | `RESOLVED_BY_BOUNDARY` | novidade matemática e algorítmica `NONE` |

## Abertas — nove

| Gap | Estado | Por que continua aberta |
|---|---|---|
| `CD-GAP-009` | `OPEN_DEFERRED` | minimalidade de `baseIndex` **não** provada |
| `CD-GAP-010` | `OPEN_DEFERRED` | minimalidade de `period` **não** provada |
| `CD-GAP-012` | `OPEN_DEFERRED` | adaptador de componente deliberadamente omitido |
| `CD-GAP-013` | `OPEN_DEFERRED` | nenhum modelo formal de custo |
| `CD-GAP-014` | `READY_FOR_FEASIBILITY_AUDIT` | `#eval` confirmado; extração **não** realizada |
| `CD-GAP-016` | `OPEN_BIBLIOGRAPHIC` | Floyd e Brent seguem sem fonte primária |
| `CD-GAP-017` | `OPEN_DEFERRED` | função total **não** formalizada; API é `Option` |
| `CD-GAP-018` | `OPEN_DEFERRED` | ordem sustenta regressão, não minimalidade |
| `CD-GAP-019` | `OPEN_DEFERRED` | recomputação de iteradas, sem memoização |

```text
fechadas por expectativa: 0
```

Nenhuma das nove abertas impede o encerramento: todas são **extensões**,
não defeitos. As três que mais pesam — minimalidade, complexidade e
extração — foram mantidas fora do escopo desde a especificação, e não por
falha de execução.
