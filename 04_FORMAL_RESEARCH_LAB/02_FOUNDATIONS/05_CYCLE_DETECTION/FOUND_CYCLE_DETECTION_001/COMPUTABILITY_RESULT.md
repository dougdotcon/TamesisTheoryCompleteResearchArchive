---
document_id: FCD-COMPUTABILITY-RESULT
verdict: COMPUTABLE
---

# Resultado de computabilidade

## O registro vinculante

```text
A presenca de Classical.choice em #print axioms NAO significa que a
funcao esteja marcada como nao computavel.

A definicao foi avaliada por #eval e nao usa escolha classica para
CONSTRUIR o certificado.
```

## Pegada axiomática medida

```text
cycleCandidates                does not depend on any axioms
mem_cycleCandidates_iff        [propext, Classical.choice, Quot.sound]
detectCycleWitness?            [propext, Classical.choice, Quot.sound]
detectCycleWitness?_sound      [propext, Classical.choice, Quot.sound]
detectCycleWitness?_complete   [propext, Classical.choice, Quot.sound]
CycleWitness.isPeriodicPt      [propext, Classical.choice, Quot.sound]
CycleWitness.mem_periodicPts   [propext, Classical.choice, Quot.sound]
CycleWitness.propagates        [propext, Classical.choice, Quot.sound]

sorryAx                        0
axiomas locais                 0
```

`cycleCandidates` é o único objeto da frente que não menciona `Fintype`, e
é exatamente o único sem pegada. Isso confirma a origem localizada no gate
de revisão: `Fintype.card` e `Finset.univ`, cuja infraestrutura usa
escolha dentro de **provas**, apagadas na compilação.

## Critério operacional aplicado

```text
1. nenhuma definicao marcada como nao computavel;
2. #eval funciona em cinco modelos concretos;
3. nenhuma escolha classica CONSTRUINDO dado.
```

Os três confirmados. Exigir pegada axiomática vazia seria inatingível para
qualquer detector cuja cota venha da cardinalidade.

## Proibições, registradas fora dos arquivos Lean

Mantidas aqui de propósito: escrevê-las nos módulos faria as auditorias de
tokens e de imports proibidos encontrarem as próprias menções documentais
e reportarem falso positivo.

O núcleo desta frente **não** contém, e a auditoria exige contagem zero
para: os quatro tokens de prova incompleta, a marca de não-computabilidade,
o combinador de escolha que extrai dado de um existencial, importações de
grafos simples, topologia, medida, análise ou das frentes de Riemann, e o
objeto de órbita quociente da Mathlib.

O lema de contagem que implementa a casa dos pombos também tem contagem
zero exigida — ela foi consumida uma única vez em `FOUND-SEMIGROUP-002`.

## Imports efetivos

```text
Mathlib.Data.Fintype.Card
Mathlib.Data.List.Range
Mathlib.Logic.Function.Iterate
TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity
```

Quatro. `FunctionalGraphs` **não** é importado — o adaptador de componente
foi omitido, e importá-lo seria dependência ociosa.
