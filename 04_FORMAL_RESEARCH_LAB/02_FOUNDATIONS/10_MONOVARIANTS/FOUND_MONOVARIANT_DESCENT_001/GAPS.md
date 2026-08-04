---
document_id: FOUND-MONOVARIANT-DESCENT-001-GAPS
work_item_id: FOUND-MONOVARIANT-DESCENT-001
gaps_opened: 8
gaps_closed_at_specification: 0
---

# Lacunas, declaradas antes de começar

| id | conteúdo | estado |
|---|---|---|
| `MON-GAP-001` | existe monovariante sempre que não há ciclo? | **ABERTA** |
| `MON-GAP-002` | medidas em ordens gerais e ordinais | ABERTA |
| `MON-GAP-003` | monovariantes não estritos, com descida eventual | ABERTA |
| `MON-GAP-004` | terminação de programas | ABERTA |
| `MON-GAP-005` | combinação de invariante com monovariante | ABERTA |
| `MON-GAP-006` | sistemas não determinísticos | ABERTA |
| `MON-GAP-007` | cota quantitativa no número de passos | ABERTA |
| `MON-GAP-008` | bibliografia de argumentos de monovariante | **DELIBERADAMENTE ABERTA** |

## `MON-GAP-001`, a honesta

Para sistemas **finitos** sem ciclo, a distância até o fim da órbita é um
monovariante, e a recíproca vale trivialmente. Para `C` infinito **não é
óbvio**, e a frente não trata. Afirmar necessidade está proibido.

## `MON-GAP-005`, a que aponta para a frente seguinte

Invariante e monovariante compõem: separar por invariante e decrescer por
monovariante são obrigações independentes. Combiná-las é a peça natural
seguinte, e **não** é feita aqui.

## `MON-GAP-007`, que a frente deliberadamente não toca

`Monovariant.iterate_lt` dá descida estrita, e sobre `Nat` isso implica
uma cota no número de passos. A frente **não** enuncia essa cota: seria
uma afirmação quantitativa, e `LAB_STATE.md` proíbe afirmação de custo
sem modelo.
