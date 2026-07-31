---
document_id: RT-FINAL-GAP-STATUS
total: 22
---

# Estado final das lacunas

## Resolvidas — quatorze

| Gap | Estado | Evidência |
|---|---|---|
| `RT-GAP-001` | `RESOLVED_BY_DESIGN` | `RawTransitionTable` com um campo |
| `RT-GAP-002` | `RESOLVED_FORMALLY` | `Valid` formalizado e decidível |
| `RT-GAP-003` | `RESOLVED_FORMALLY` | `validateTransitionTable` + `_sound` + `_complete` |
| `RT-GAP-004` | `RESOLVED_FORMALLY` | `ValidatedTransitionTable`, `toRaw`, `toRaw_valid` |
| `RT-GAP-005` | `RESOLVED_FORMALLY` | `valid_empty`; consulta rejeitada |
| `RT-GAP-006` | `RESOLVED_FORMALLY` | `validateStart` + anti-clamp + `_complete` |
| `RT-GAP-007` | `RESOLVED_FORMALLY` | `step`, total por construção |
| `RT-GAP-008` | `RESOLVED_FORMALLY` | `step_val` e `step?_eq_some_step` |
| `RT-GAP-009` | `RESOLVED_FORMALLY` | `run?_eq_iterate_step` |
| `RT-GAP-010` | `RESOLVED_FORMALLY` | `detectCycle?` e os dois teoremas herdados |
| `RT-GAP-011` | `RESOLVED_BY_BOUNDARY` | `Option` preservado; detector não totalizado |
| `RT-GAP-012` | `RESOLVED_FORMALLY` | `RuntimeCycleError` e a precedência provada |
| `RT-GAP-016` | `RESOLVED_FORMALLY` | `detectCycle?_raw_repeat` e a soundness da análise |
| `RT-GAP-020` | `RESOLVED_BY_BOUNDARY` | novidade `NONE` / `NONE` |

## Abertas — oito

| Gap | Estado | Por que continua aberta |
|---|---|---|
| `RT-GAP-013` | `OPEN_DEFERRED` | nenhuma execução nativa via Lake |
| `RT-GAP-014` | `OPEN_DEFERRED` | nenhuma CLI |
| `RT-GAP-015` | `OPEN_DEFERRED` | nenhum parsing externo |
| `RT-GAP-017` | `OPEN_DEFERRED` | a correção da abstração externa **não** é fornecida |
| `RT-GAP-018` | `OPEN_DEFERRED` | testes que importam a raiz seguem fora do build |
| `RT-GAP-019` | `OPEN_DEFERRED` | nenhum modelo formal de custo |
| `RT-GAP-021` | `OPEN_BIBLIOGRAPHIC` | nenhuma fonte primária consultada |
| `RT-GAP-022` | `OPEN_DEFERRED` | diagnóstico detalhado do destino inválido |

## Contagens finais — corrigidas neste gate

```yaml
resolved_by_design: 1
resolved_formally: 11
resolved_by_boundary: 2
open_deferred: 7
open_bibliographic: 1
total: 22
```

Soma: `1 + 11 + 2 + 7 + 1 = 22`. O cabeçalho declarava `10` e `8`; a
correção está registrada em `METADATA_CORRECTION_RECORD.md`.

```text
fechados por expectativa: 0
```

Nenhuma das oito abertas impede o encerramento: todas são **extensões**,
não defeitos. Sete dependem de autorizações que a frente deliberadamente
não pediu; a oitava, `RT-GAP-017`, é uma obrigação que pertence a quem
produz a abstração.
