# FOUND-SEMIGROUP-001 — Matriz de resultados conhecidos

Separação obrigatória entre álgebra padrão, propriedades do modelo finito e
vocabulário Tamesis ainda não justificado.

| Item | Classe | Fonte | Estado nesta frente |
|---|---|---|---|
| definição de semigrupo (operação associativa) | álgebra padrão | Mathlib `Semigroup` | reutilizada |
| definição de monoide (semigrupo com identidade) | álgebra padrão | Mathlib `Monoid` | instanciada para `Shift3` |
| ação de semigrupo (`mul_smul`, sem identidade) | álgebra padrão | Mathlib `SemigroupAction` | reutilizada; nenhuma duplicata local |
| ação de monoide (`one_smul` + `mul_smul`) | álgebra padrão | Mathlib `MulAction` | instanciada para `Shift3`/`Regime3` |
| modelo cíclico C3 e sua ação regular | exemplo padrão | qualquer texto introdutório de álgebra | formalizado localmente como `Shift3`/`Regime3` |
| fidelidade da ação regular de C3 | propriedade do exemplo | FOUND-SG-012 | provada por análise finita |
| transitividade da ação regular de C3 | propriedade do exemplo | FOUND-SG-013 | provada por análise finita; **não** vale para semigrupos em geral |
| cardinalidades 3/3 | propriedade do exemplo | FOUND-SG-007/008 | provadas |
| bibliografia primária de teoria de semigrupos | literatura | — | `NOT_AUDITED` nesta frente; os resultados usados são elementares e cobertos pela Mathlib |
| "regime" / "transição" como conceitos Tamesis (TRI/TDTR) | vocabulário não formalizado | claims `TRI-001`, `TDTR-001` (`PARTIAL_RESULT`, `F`) | **não usado como premissa**; no máximo `possible future modelling interface` |
| equivalência TRI/TDTR ⇔ teoria de semigrupos | não estabelecida | — | **não declarada**; nenhuma inferência é autorizada |

Registro explícito: este gate não declara que sistemas físicos,
informacionais ou computacionais são semigrupos de regimes. O modelo C3 é um
exemplo finito de referência; a única ponte permitida com o vocabulário
Tamesis é a anotação `possible future modelling interface`.
