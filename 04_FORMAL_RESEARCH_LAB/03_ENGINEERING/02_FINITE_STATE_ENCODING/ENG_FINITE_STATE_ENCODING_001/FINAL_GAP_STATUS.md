---
document_id: ENC-FINAL-GAP-STATUS
total: 20
---

# Estado final das lacunas

## Resolvidas — quinze

| Gap | Estado | Evidência |
|---|---|---|
| `ENC-GAP-001` | `RESOLVED_BY_DESIGN` | estrutura de quatro campos, codificação fornecida |
| `ENC-GAP-002` | `RESOLVED_BY_DESIGN` | nada adicionado à estrutura; análise não habitada para `Empty` |
| `ENC-GAP-003` | `RESOLVED_BY_API_AUDIT` | `Array.ofFn` computável, sete tabelas por `decide` |
| `ENC-GAP-004` | `RESOLVED_BY_API_AUDIT` | `Array.size_ofFn` em modo termo; orientação `size = n` |
| `ENC-GAP-005` | `RESOLVED_FORMALLY` | campo `closed`; `toRaw_valid` reutilizado |
| `ENC-GAP-006` | `RESOLVED_BY_DESIGN` | exatamente dois pontos de transporte |
| `ENC-GAP-007` | `RESOLVED_FORMALLY` | `tableIndex_val`, `rfl`, `@[simp]` |
| `ENC-GAP-008` | `RESOLVED_FORMALLY` | `tableIndex_semiconj`, por `decode_encode` |
| `ENC-GAP-009` | `RESOLVED_FORMALLY` | semiconjugação principal; comutação como `.symm` |
| `ENC-GAP-010` | `RESOLVED_FORMALLY` | `iterate_right`, termo de uma linha |
| `ENC-GAP-011` | `RESOLVED_FORMALLY` | `run?_corresponds_to_typed_iterate` |
| `ENC-GAP-012` | `RESOLVED_FORMALLY` | soundness com igualdade em `S` |
| `ENC-GAP-013` | `RESOLVED_FORMALLY` | completeness sem pré-condições |
| `ENC-GAP-014` | `RESOLVED_FORMALLY` | exclusão universal de erros |
| `ENC-GAP-015` | `RESOLVED_BY_API_AUDIT` | pegada medida; `sorryAx 0` |

## Abertas — cinco

| Gap | Estado | Por que continua aberta |
|---|---|---|
| `ENC-GAP-016` | `OPEN_BIBLIOGRAPHIC` | nenhuma fonte primária consultada |
| `ENC-GAP-017` | `OPEN_DEFERRED` | nenhuma extração |
| `ENC-GAP-018` | `OPEN_DEFERRED` | nenhum parser externo |
| `ENC-GAP-019` | `OPEN_DEFERRED` | a correção da abstração concreta **não** é fornecida |
| `ENC-GAP-020` | `OPEN_DEFERRED` | invariância do witness concreto **não** é provada |

## Contagens

```yaml
resolved_by_design: 3
resolved_by_api_audit: 3
resolved_formally: 9
open_deferred: 4
open_bibliographic: 1
total: 20
```

Derivadas por script a partir das entradas, e conferidas contra o
cabeçalho. `3 + 3 + 9 + 4 + 1 = 20`.

```text
fechados por expectativa: 0
```

Nenhuma das cinco abertas impede o encerramento: quatro são extensões
não pedidas, e a quinta — `ENC-GAP-019` — é obrigação de quem produz a
abstração.
