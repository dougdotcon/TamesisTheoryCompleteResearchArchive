---
document_id: FOUND-UNIFORM-PRIMREC-001-STOP-CONDITIONS
work_item_id: FOUND-UNIFORM-PRIMREC-001
stop_conditions_declared: 9
tested_by_anticipation: 9
triggered: 0
---

# Condicoes de parada

| # | Condicao | Testada |
|---|---|---|
| STOP-UP-001 | Afirmar custo ou complexidade assintotica | sim |
| STOP-UP-002 | Tratar `Primrec` como sinonimo de eficiente | sim |
| STOP-UP-003 | Definir classe de complexidade | sim |
| STOP-UP-004 | Alegar qualquer coisa sobre P vs NP | sim |
| STOP-UP-005 | Misturar `decide` e `if` no mesmo predicado | sim |
| STOP-UP-006 | Reimplementar o detector em vez de casar com ele | sim |
| STOP-UP-007 | Modificar arquivo de frente encerrada | sim |
| STOP-UP-008 | Fechar sem instancia positiva avaliada | sim |
| STOP-UP-009 | Novidade != `NONE` | sim |

## STOP-UP-002, a armadilha desta frente

`Primrec` contem torres de exponenciais. "A analise e primitiva
recursiva" **nao** e um resultado de eficiencia, e a frase so e honesta
acompanhada disso.

A frente anterior teve de dizer que `Primrec` nao mede nada por ser
vacuo sobre dominio finito. Esta tem de dizer que, mesmo **nao** sendo
vacuo, continua sem medir custo. Sao dois limites diferentes, e os dois
valem.

## STOP-UP-005, que quase custou a frente

`PrimrecPred p` carrega a sua propria instancia de `DecidablePred`.
Construir um `Primrec fun a => decide (p a)` por fora e entrega-lo onde
se espera `PrimrecPred p` **falha**, porque as instancias nao coincidem,
e nenhuma tatica desfaz isso.

A saida foi escrever os predicados com `if ... then true else false` e
usar `Primrec.ite`, que aceita `PrimrecPred` diretamente. Onde um Bool
era inevitavel, `Primrec.eq.comp ... (const true)` produz o
`PrimrecPred` ja no formato certo.

## STOP-UP-006, que separa casar de reimplementar

`detectCycle?_eq_raw` **nao** reimplementa o detector: ele mostra que o
detector ja existente, aplicado a tabela validada, e igual a um `find?`
sobre a mesma lista de candidatos com um predicado equivalente. O
detector permanece onde foi provado.
