---
document_id: RT-COMPUTABILITY-RESULT
verdict: COMPUTABLE
---

# Resultado de computabilidade

## Registro vinculante

```text
A presenca de Classical.choice em #print axioms NAO significa que a
definicao esteja marcada como nao computavel.
```

## Pegada medida, por camada

```text
CAMADA BRUTA — sem axioma algum
  RawTransitionTable.step?        does not depend on any axioms
  RawTransitionTable.run?         does not depend on any axioms

CAMADA DE VALIDACAO E EXECUCAO — sem Classical.choice
  RawTransitionTable.Valid                [propext, Quot.sound]
  validateTransitionTable                 [propext, Quot.sound]
  validateTransitionTable_sound           [propext, Quot.sound]
  validateTransitionTable_complete        [propext, Quot.sound]
  validateStart                           [propext, Quot.sound]
  validateStart_sound                     [propext, Quot.sound]
  validateStart_complete                  [propext, Quot.sound]
  valid_empty                             [propext, Quot.sound]
  ValidatedTransitionTable.step           [propext, Quot.sound]
  step?_eq_some_step                      [propext, Quot.sound]
  run?_eq_iterate_step                    [propext, Quot.sound]

CAMADA DO DETECTOR — heranca por Fintype.card
  detectCycle? e todos os herdeiros       [propext, Classical.choice, Quot.sound]

sorryAx          0
axiomas locais   0
```

O resultado é nítido e vale a pena registrar: **as duas definições de
execução bruta não dependem de axioma nenhum**, e toda a camada de
validação e da ponte de iterações dispensa `Classical.choice`. A pegada
entra exatamente onde o detector entra.

## Critério operacional aplicado

```text
1. nenhuma definicao marcada como nao computavel;
2. #eval funciona — dezenove avaliacoes;
3. nenhuma escolha classica CONSTRUINDO dado.
```

Os três confirmados.

## Proibições — registradas fora dos arquivos Lean

Mantidas aqui de propósito: escrevê-las nos módulos faria a auditoria de
tokens encontrar as próprias menções documentais.

O núcleo desta frente **não** contém, e a auditoria exige contagem zero
para: os quatro tokens de prova incompleta, a marca de
não-computabilidade, o combinador de escolha que extrai dado de um
existencial, o combinador de igualdade decidível clássica, importações de
grafos simples, topologia, medida, análise, parser, JSON ou entrada e
saída, e o objeto de órbita quociente da Mathlib.

Também têm contagem zero exigida: o lema de contagem do pigeonhole, o
teorema de colisão limitada e a enumeração de candidatos do detector — a
frente os consome **através** de `detectCycleWitness?`, sem mencioná-los.

## Imports efetivos

```text
Mathlib.Data.Fintype.Card
Mathlib.Logic.Function.Iterate
TamesisLab.Foundations.CycleDetection
```

Três, mais os internos da própria frente. Nenhum umbrella de táticas,
nenhum módulo de entrada e saída, nenhuma rede. **A API dinâmica é uma
função pura.**

## `#eval` não é extração

`extraction_status` permanece `READY_FOR_FEASIBILITY_AUDIT` e
`extraction_authorized` permanece `false`. Nenhum binário, alvo Lake,
CLI, parser, JSON, CSV, arquivo, rede ou banco pertence a esta frente.
