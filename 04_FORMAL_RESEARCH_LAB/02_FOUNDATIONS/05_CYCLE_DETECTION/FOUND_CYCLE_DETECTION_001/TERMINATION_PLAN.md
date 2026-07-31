---
document_id: FCD-TERMINATION-PLAN
termination: STRUCTURAL
---

# Plano de terminação

## Argumento

```text
cycleCandidates (card X) eh uma lista finita;
List.find? termina estruturalmente sobre a lista;
logo o detector termina por construcao.
```

Não há obrigação de prova: a terminação é **reconhecida pelo elaborador**,
porque `List.find?` é uma função total da biblioteca sobre um argumento
`List`, e `cycleCandidates` é construída por `List.range`, `List.flatMap` e
`List.map` — todas totais.

## O que **não** é usado

```text
fuel recursivo sobre estados;
recursao bem fundada;
while sem cota;
StateM com condicao sem prova;
Classical.choice.
```

Isto é a diferença central em relação a Floyd. Floyd é um laço cuja
terminação depende de um argumento matemático — a tartaruga e a lebre se
encontram porque a trajetória é eventualmente periódica —, e em Lean esse
argumento precisa virar `fuel` ou recursão bem fundada, com invariantes.
A busca limitada não tem laço: tem uma lista.

## Finitude da lista

`List.range n` tem comprimento `n` (`List.length_range`, confirmado no
checkout). `flatMap` e `map` de listas finitas são finitas. Nenhum lema
adicional é necessário para a terminação — o comprimento exato só
interessaria a uma análise de complexidade, que **não** está autorizada.

## Comparação registrada

| Estratégia | Terminação | Custo formal |
|---|---|---|
| busca limitada por certificado | **estrutural**, sem prova | mínimo |
| tabela visitada | estrutural com acumulador | invariante de acumulador |
| Floyd com `fuel` | por cota `fuel` | invariantes de duas velocidades |
| Floyd com recursão bem fundada | por medida decrescente | medida + prova de decrescimento |
| Brent | por dobramento de blocos | invariantes de bloco |
