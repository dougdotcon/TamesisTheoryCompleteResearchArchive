---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-GAP-STATUS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
gaps_total: 20
gaps_closed: 15
gaps_open: 5
---

# Estado final dos gaps

Contagens derivadas da tabela abaixo, não escritas à mão.

## Fechados — 15

| Gap | Título | Fechado por |
|---|---|---|
| ABS-GAP-001 | representação da abstração | `Abstraction.lean`, dois campos |
| ABS-GAP-002 | orientação da semiconjugação | `Iff.rfl`, `ABS-TEST-001` |
| ABS-GAP-003 | correspondência de iteradas | `iterate_commutes` |
| ABS-GAP-004 | integração com `CertifiedFiniteEncoding` | argumento separado |
| ABS-GAP-005 | análise do sistema abstrato | `analyzeAbstractSystem` |
| ABS-GAP-006 | soundness observacional | conclui em `A` |
| ABS-GAP-007 | formulação de `OrbitSeparating` | não tautológica, provado |
| ABS-GAP-008 | relação com `Set.InjOn` | equivalência medida, `DEFERRED_OPTIONAL` |
| ABS-GAP-009 | reflexão da repetição | hipótese explícita |
| ABS-GAP-010 | contraexemplo `BOOL_TO_UNIT` | `Counterexample.lean` |
| ABS-GAP-011 | necessidade de `DecidableEq C` | nenhuma, verificado por varredura |
| ABS-GAP-012 | necessidade de finitude de `C` | nenhuma, `ABS-TEST-006` |
| ABS-GAP-013 | completude abstrata | `analyzeAbstractSystem_complete` |
| ABS-GAP-014 | ciclos espúrios | exibidos em `BOOL_TO_UNIT` e na paridade |
| ABS-GAP-019 | bibliografia e terminologia | ver abaixo |

### Sobre `ABS-GAP-019`

Fechado **por delimitação, não por revisão bibliográfica**. A frente
declara `mathematical_novelty: NONE` e não reivindica prioridade sobre
resultado algum: semiconjugação, abstração e injetividade restrita a uma
órbita são clássicas. Nenhuma fonte primária foi consultada, e nenhuma
era necessária, porque nenhuma afirmação de originalidade foi feita.

Se algum gate futuro quiser reivindicar posição na literatura, o gap
deve ser **reaberto**.

## Abertos — 5

| Gap | Título | Estado |
|---|---|---|
| ABS-GAP-015 | bissimulação | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| ABS-GAP-016 | quocientes | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| ABS-GAP-017 | correção da abstração externa | `OPEN_PERMANENT` |
| ABS-GAP-018 | extração | `OPEN_DEFERRED`, `NOT_AUTHORIZED` |
| ABS-GAP-020 | complexidade | `OPEN_DEFERRED`, sem modelo de custo |

### `ABS-GAP-017` é permanente

Nenhuma frente formal pode decidir se um sistema externo real foi
corretamente modelado por `C`, `stepC` e `abstract`. Isso é obrigação
do adaptador da aplicação, e continua fora do alcance de qualquer prova
neste repositório.

## Contagem

```text
total     20
fechados  15
abertos    5
```
