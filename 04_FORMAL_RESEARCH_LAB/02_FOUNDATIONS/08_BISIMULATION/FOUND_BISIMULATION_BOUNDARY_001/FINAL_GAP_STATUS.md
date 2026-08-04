---
document_id: FOUND-BISIMULATION-BOUNDARY-001-FINAL-GAP-STATUS
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
gaps_total: 10
gaps_closed: 5
gaps_open: 5
---

# Estado final dos gaps

## Fechados — 5

| Gap | Título | Fechado por |
|---|---|---|
| BIS-GAP-001 | definição das duas metades | `Definitions.lean` |
| BIS-GAP-002 | colapso | `bisimulation_iff_semiconj` |
| BIS-GAP-003 | o contraexemplo já é bissimulação | `boolToUnit_bisimulation` |
| BIS-GAP-004 | sobrejetividade não resgata | `surjective_bisimulation_does_not_reflect_cycles` |
| BIS-GAP-005 | fronteira do recorte | `SCOPE_BOUNDARY.md`, por design |

`BIS-GAP-005` é fechado **por documentação, não por formalização**. O
recorte não é um teorema: é a delimitação de onde os teoremas valem.
Formalizar a falha do colapso em sistemas não determinísticos exigiria
modelar sistemas não determinísticos, que é `BIS-GAP-007` e está fora de
escopo.

## Abertos — 5

| Gap | Título | Estado |
|---|---|---|
| BIS-GAP-006 | bissimulação relacional | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| BIS-GAP-007 | sistemas não determinísticos | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| BIS-GAP-008 | ações rotuladas | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| BIS-GAP-009 | coindução | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| BIS-GAP-010 | bibliografia | `OPEN_BIBLIOGRAPHIC` |

`BIS-GAP-010` permanece **aberto**, ao contrário do gap bibliográfico da
frente anterior. Aqui a diferença importa: o resultado toca uma noção —
bissimulação — que tem literatura própria e extensa em semântica de
concorrência. Declarar `mathematical_novelty: NONE` cobre a
originalidade, mas não substitui uma revisão de terminologia. Fechá-lo
por delimitação seria mais frágil do que foi na frente anterior, e por
isso não foi feito.

## Contagem

```text
total     10
fechados   5
abertos    5
```
