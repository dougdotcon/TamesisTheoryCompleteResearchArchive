---
document_id: FOUND-BISIMULATION-BOUNDARY-001-STOP-CONDITIONS
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
stop_conditions_declared: 10
stop_conditions_triggered: 0
---

# Stop conditions

```text
STOP-BIS-001  o colapso e enunciado ou usado fora do recorte
              deterministico total e funcional
STOP-BIS-002  Reflects e definido de forma ja resolvida, tornando o
              colapso uma tautologia disfarcada de teorema
STOP-BIS-003  a frente afirma que bissimulacao reflete ciclos
STOP-BIS-004  a frente afirma que bissimulacao e inutil em geral
STOP-BIS-005  bissimulacao relacional, acoes rotuladas ou coinducao
              entram no escopo
STOP-BIS-006  sistemas nao deterministicos ou funcoes parciais entram
              no escopo
STOP-BIS-007  o contraexemplo BOOL_TO_UNIT e modificado
STOP-BIS-008  qualquer frente encerrada e modificada
STOP-BIS-009  probe obrigatorio com exit diferente de zero
STOP-BIS-010  novidade inflada: o colapso e classico
```

## As duas mais prováveis

`STOP-BIS-001` e `STOP-BIS-002` são os riscos reais desta frente.

O primeiro porque colapsos se generalizam sozinhos na escrita: basta
escrever "bissimulação é semiconjugação" sem qualificador, e a afirmação
passa a ser falsa exatamente na teoria onde a palavra nasceu.

O segundo porque a tentação de simplificar `Reflects` é forte — a
existencial parece redundante justamente **porque** o teorema é
verdadeiro. Simplificá-la destruiria o conteúdo do resultado.

## Testadas por antecipação

```text
STOP-BIS-002  a definicao com ∃ foi compilada, e reflects_iff_simulates
              precisou de prova em duas direcoes, nao de Iff.rfl
STOP-BIS-003  as duas negacoes compilam
STOP-BIS-009  probe terminou com REAL_EXIT_CODE 0
```

O contraste com `simulates_iff_semiconj`, que **é** `Iff.rfl`, é a
evidência de que `Reflects` não foi trivializado.
