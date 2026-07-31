---
document_id: FCD-COMPUTABILITY-REVIEW
stage: RESULT_REVIEW
verdict: COMPUTABLE
---

# Revisão de computabilidade

> Este documento foi iniciado no gate de revisão de especificação, quando
> a evidência era de sonda descartável. Agora registra o estado
> **medido sobre os módulos permanentes**.

## Classificação confirmada

```text
CycleWitness         computavel
cycleCandidates      computavel
detectCycleWitness?  computavel e avaliavel
CycleWitness.Valid   proposicional, decidivel com DecidableEq X
```

```text
nenhuma definicao marcada como nao computavel;
nenhuma escolha classica no codigo;
nenhum dado produzido por escolha classica explicita.
```

Verificado por `grep` sobre os seis módulos, o agregador da frente e os
cinco testes: **zero** ocorrências dos tokens proibidos.

## Pegada axiomática, medida

```text
cycleCandidates                does not depend on any axioms
mem_cycleCandidates_iff        [propext, Classical.choice, Quot.sound]
detectCycleWitness?            [propext, Classical.choice, Quot.sound]
detectCycleWitness?_sound      [propext, Classical.choice, Quot.sound]
detectCycleWitness?_complete   [propext, Classical.choice, Quot.sound]
CycleWitness.isPeriodicPt      [propext, Classical.choice, Quot.sound]
CycleWitness.mem_periodicPts   [propext, Classical.choice, Quot.sound]
CycleWitness.propagates        [propext, Classical.choice, Quot.sound]

sorryAx          0
axiomas locais   0
```

`cycleCandidates` é o **único** objeto da frente que não menciona
`Fintype` — e é exatamente o único sem pegada. A coincidência não é
acidental: ela localiza a origem em `Fintype.card` e `Finset.univ`.

## A leitura correta, reafirmada

```text
A pegada de Classical.choice NAO eh prova de nao computabilidade.
```

A infraestrutura de `Finset` da Mathlib usa escolha dentro de **provas**,
que são apagadas na compilação. `Fintype.card` é computável, e o detector
que a usa também é — demonstrado por `#eval` em cinco modelos e por
dezesseis teoremas verificados pelo kernel via `decide`.

Exigir pegada vazia seria inatingível para qualquer detector cuja cota
venha da cardinalidade.

## Fronteira entre executar e extrair

```text
#eval eh evidencia operacional DENTRO do Lean.
NAO eh ainda extracao de produto.
```

Nenhum binário, alvo executável do Lake, API externa ou integração foi
criado. `extraction_status` permanece `READY_FOR_FEASIBILITY_AUDIT`, e
`extraction_authorized` permanece `false`.

## O que permanece proposicional

```text
Function.periodicOrbit    noncomputavel, e ausente do nucleo
Function.periodicPts      Set X, interface proposicional
EventuallyMeets           proposicional, e nem sequer importado
```

O detector devolve um par de naturais. A pertinência a `periodicPts` é um
**teorema sobre esse par**, não um cálculo.
