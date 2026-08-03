---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-REUSE-MATRIX
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Matriz de reutilização

## O que foi consumido, sem alteração

| API | Origem | Papel nesta frente |
|---|---|---|
| `CertifiedFiniteEncoding` | ENG-FINITE-STATE-ENCODING-001 | finitude executável de `A` |
| `analyzeEncodedSystem` | ENG-FINITE-STATE-ENCODING-001 | corpo de `analyzeAbstractSystem` |
| `analyzeEncodedSystem_sound` | ENG-FINITE-STATE-ENCODING-001 | base da soundness observacional |
| `analyzeEncodedSystem_complete` | ENG-FINITE-STATE-ENCODING-001 | base da completeness abstrata |
| `CycleWitness` | FOUND-CYCLE-DETECTION-001 | tipo do certificado |
| `RuntimeCycleError` | ENG-FINITE-STATE-RUNTIME-001 | tipo de erro do `Except` |
| `Function.Semiconj` | Mathlib | campo `commutes` |
| `Function.Semiconj.iterate_right` | Mathlib | `iterate_commutes` |
| `Function.Injective` | Mathlib | teste de instanciação |

## O que NÃO foi copiado

```text
detector de ciclos            nao copiado
runtime adapter               nao copiado
casa dos pombos               nao reaplicada
construcao da tabela          nao reaberta
semantica de execucao         nao duplicada
construtores de erro          nao criados nem removidos
segundo transporte Fin n      nao criado
```

## Arquivos de frentes encerradas tocados

```text
TamesisLab/Engineering/FiniteStateEncoding/     0
TamesisLab/Engineering/FiniteStateRuntime/      0
TamesisLab/Foundations/CycleDetection/          0
TamesisLab/Foundations/FunctionalGraphs/        0
TamesisLab/Foundations/Semigroups/              0
TamesisLab/Foundations/FiniteDynamics/          0
TamesisLab/RHNogo/                              0
```

Os únicos arquivos preexistentes modificados são os dois agregadores,
`TamesisLab/Foundations.lean` e `TamesisLab.lean`, que ganharam linhas
de `import`. Nenhuma declaração anterior foi alterada.

## Razão de custo

```text
declaracoes novas de matematica propria    0
lemas reprovados de Mathlib                0
lemas reprovados de frentes anteriores     0
```

A frente inteira é composição. É por isso que
`mathematical_novelty: NONE` não é modéstia, e sim a descrição exata do
que aconteceu.
