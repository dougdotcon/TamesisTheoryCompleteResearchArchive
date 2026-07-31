---
document_id: RT-ERROR-PRECEDENCE-REVIEW
precedence_proved: true
---

# Revisão da precedência dos erros

## Ordem vinculante

```text
1. tabela invalida
2. estado inicial invalido
3. falha interna impossivel
4. sucesso
```

Garantida pela ordem do `do`: cada `←` propaga o primeiro erro e para, de
modo que `validateStart` **nunca** é alcançado com tabela inválida, e o
detector **nunca** é alcançado com índice fora do domínio.

## `analyzeTransitionTable_invalid_table`

```lean
(h : ¬raw.Valid) :
    analyzeTransitionTable raw start = .error .transitionDestinationOutOfBounds
```

Note a hipótese: **apenas** `¬raw.Valid`. Nada é dito sobre `start`, e é
exatamente isso que faz a tabela inválida vencer **mesmo quando o início
também é inválido**. Medido:

```text
analyzeTransitionTable ⟨#[1]⟩ 0    ->  transitionDestinationOutOfBounds
analyzeTransitionTable ⟨#[1]⟩ 100  ->  transitionDestinationOutOfBounds
```

Em `#[1]`, o único estado tem destino `1`, fora do domínio; e `100` está
fora dos limites. O erro reportado é o da **tabela**.

## `analyzeTransitionTable_invalid_start`

```lean
(hRaw : raw.Valid) (hStart : ¬start < raw.next.size) :
    analyzeTransitionTable raw start =
      .error (.initialStateOutOfBounds start raw.next.size)
```

Exige **tabela válida** e início inválido — a hipótese `hRaw` é
indispensável, e é ela que impede este teorema de contradizer o
anterior. O erro carrega o `start` pedido e a cardinalidade real, sem
correção.

## `analyzeTransitionTable_ne_internalFailure`

```lean
(hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure
```

Sob as duas pré-condições, o erro interno é **impossível**. Derivado da
completude: se a análise devolve `.ok w`, ela não devolve `.error _`.

## O construtor permanece

```text
internalDetectorFailure continua na funcao executavel.
```

Três razões, registradas desde a especificação: não totalizar o detector;
honestidade da API, já que o `Except` existe de qualquer forma; e
robustez a uma futura troca do detector.

E a garantia de que ele **não mascara** falha de validação não é
retórica: são os dois teoremas de erro acima que a estabelecem, fixando
qual erro sai em cada situação.

## Modelo de erros

```text
transitionDestinationOutOfBounds        generico na v1 (RT-GAP-022 diferido)
initialStateOutOfBounds start count     carrega os dois numeros
internalDetectorFailure                 defensivo, impossivel sob validade
```

Tabela inválida e início inválido **não** colapsados.
