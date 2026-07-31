---
document_id: RT-FINAL-COMPUTABILITY-REVIEW
stage: RESULT_REVIEW
supersedes: RT-COMPUTABILITY-REVIEW
verdict: COMPUTABLE
---

# Revisão final de computabilidade

`COMPUTABILITY_REVIEW.md` já existia, criado em `6c3b837` no gate de
revisão da especificação. Ele **não** foi sobrescrito: este documento é o
sucessor de estágio, no mesmo padrão dos seis `FINAL_*` já presentes na
frente. A revisão da especificação media **treze** casos e antecipava a
pegada axiomática; esta mede o resultado formalizado.

## Confirmado

```text
RawTransitionTable                    computavel
RawTransitionTable.Valid              decidivel
validateTransitionTable               computavel
validateStart                         computavel
ValidatedTransitionTable.step         computavel
RawTransitionTable.step?              computavel
RawTransitionTable.run?               computavel
ValidatedTransitionTable.detectCycle? computavel
analyzeTransitionTable                computavel
```

Todos avaliados por `#eval` nos testes de execução.

## Tokens proibidos

```text
sorry, admit, axiom, unsafe, noncomputable,
Classical.choose, Classical.decEq
```

**Zero ocorrências** nos seis módulos, nos dois agregadores e nos quatro
testes.

## Pegada axiomática, por camada

```text
SEM AXIOMA
  RawTransitionTable.step?
  RawTransitionTable.run?

SEM Classical.choice
  RawTransitionTable.Valid
  validateTransitionTable e seus dois teoremas
  validateStart e seus dois teoremas
  valid_empty
  ValidatedTransitionTable.step
  step?_eq_some_step
  run?_eq_iterate_step

COM Classical.choice, herdado de Fintype.card
  detectCycle? e seus tres teoremas
  analyzeTransitionTable e seus cinco teoremas

sorryAx          0
axiomas locais   0
```

O padrão é exatamente o previsto na especificação e confirmado na
revisão: **a ponte `Array → Fin` é axiomaticamente mais leve que o
detector que ela alimenta**, e as duas funções de execução bruta não
dependem de axioma nenhum.

## `internalDetectorFailure`

```text
eh erro explicito;
NAO eh witness padrao;
NAO eh correcao silenciosa.
```

Ele aparece no tipo `Except` ao lado dos dois erros de validação, e um
teorema prova que é inalcançável sob entradas válidas.

## Imports

```text
Mathlib.Data.Fintype.Card
Mathlib.Logic.Function.Iterate
TamesisLab.Foundations.CycleDetection
```

Três externos. Zero de grafos simples, topologia, medida, EDP, das
frentes de Riemann, de JSON, de parser, de entrada e saída ou de rede.
**A API dinâmica é uma função pura.**

## `#eval` não é extração

```yaml
extraction_status: NOT_AUTHORIZED
cli_status: NOT_AUTHORIZED
external_format_status: NOT_AUTHORIZED
integration_status: NOT_AUTHORIZED
```

Nenhum binário, alvo Lake, CLI, parser, JSON, CSV, arquivo, rede ou banco
foi criado.
