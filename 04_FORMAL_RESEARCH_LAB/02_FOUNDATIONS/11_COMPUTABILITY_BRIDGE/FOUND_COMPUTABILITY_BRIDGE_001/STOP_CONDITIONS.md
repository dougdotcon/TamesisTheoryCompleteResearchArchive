---
document_id: FOUND-COMPUTABILITY-BRIDGE-001-STOP-CONDITIONS
work_item_id: FOUND-COMPUTABILITY-BRIDGE-001
stop_conditions_declared: 13
tested_by_anticipation: 13
triggered: 0
---

# Condições de parada

Todas testadas por antecipação no probe. Nenhuma disparou.

| # | Condição | Testada |
|---|---|---|
| STOP-CB-001 | Definir classe de complexidade | sim |
| STOP-CB-002 | Afirmar custo ou complexidade assintótica | sim |
| STOP-CB-003 | Afirmar qualquer coisa sobre P vs NP | sim |
| STOP-CB-004 | Apresentar a ponte como se certificasse o algoritmo | sim |
| STOP-CB-005 | Tratar `baseIndex + period ≤ n` como cota de recursos | sim |
| STOP-CB-006 | Provar ou afirmar o enunciado uniforme | sim |
| STOP-CB-007 | Fechar sem instância positiva em tipo habitado | sim |
| STOP-CB-008 | Modificar arquivo de frente encerrada | sim |
| STOP-CB-009 | Registrar `encodingPrimcodable` como `instance` global | sim |
| STOP-CB-010 | Usar `sorry`, `admit` ou axioma local no lugar do uniforme | sim |
| STOP-CB-011 | Conectar a Clay, TOE, física ou Riemann | sim |
| STOP-CB-012 | Novidade ≠ `NONE` | sim |
| STOP-CB-013 | Tratar a `Primcodable` induzida como canônica | sim |

## STOP-CB-004, que é a armadilha real desta frente

A tentação é escrever "o detector do laboratório é primitivo recursivo"
e seguir como se isso dissesse algo sobre a busca limitada. **Não diz.**
`primrec_of_encoding` prova o mesmo para toda função que sai do tipo, e
seu corpo nunca consulta a definição de `f`.

A frente inteira só é honesta se essa frase estiver escrita no lugar mais
visível — e está, no `README.md`, na `SPECIFICATION_DECISION.md` e aqui.

## STOP-CB-005, que separa certificado de recurso

```text
w.baseIndex + w.period <= n     o TESTEMUNHO cabe em n
                                 PROVADO

a computacao custa n passos      AFIRMACAO DE CUSTO
                                 PROIBIDA, sem modelo
```

A primeira é teorema. A segunda exige um modelo de máquina que o
laboratório não tem e esta frente não constrói.

## STOP-CB-006 e STOP-CB-010, que andam juntas

`UniformPrimrecStatement` é `def : Prop`. Ela demonstra que o enunciado
**elabora** e nada mais. Provar `Primrec₂ analyzeTransitionTable` exige
mostrar que a busca limitada é primitiva recursiva sobre um domínio
infinito — trabalho real, de gate próprio.

Preencher a lacuna com `sorry` ou axioma local produziria a aparência do
resultado sem o resultado. Está proibido pelo `AGENTS.md`, e a `def :
Prop` é a alternativa que não mente.

## STOP-CB-013, aberta pela revisão

A instância induzida **não** é canônica: `Primcodable Bool` já existe no
Mathlib. Afirmar que a classificação independe da codificação exigiria um
teorema de invariância que esta frente não prova — `CB-GAP-010`.

O que existe é um caso: `boolEncoding_primrec_canonical`. Um caso não é
uma invariância, e a diferença entre as duas coisas é exatamente o que
esta condição de parada protege.

## STOP-CB-007, herdada do defeito anterior

`FOUND-MONOVARIANT-DESCENT-001` fechou com hipótese vácua e teve de ser
corrigido. A regra `positive_instance_required` nasceu daí.

Esta frente exibe `boolEncoding` — `Bool`, `n = 2`, tipo habitado — e
`boolEncoding_analysis_concrete` é decidida por **avaliação**, não
assumida. `isEmpty_of_encoding_zero` está enunciada como teorema público
para que o caso vácuo (`n = 0`) fique nomeado em vez de esquecido.
