---
document_id: FCD-COMPUTABILITY-BOUNDARY
---

# Fronteira de computabilidade

## O que é computável

```text
CycleWitness                 par de naturais
cycleCandidates              List.range / flatMap / map
CycleWitness.Valid           proposicional, mas DECIDIVEL com DecidableEq X
detectCycleWitness?          List.find? sobre lista finita
```

## O que **não** é, e permanece proposicional

```text
Function.periodicOrbit       noncomputavel — vive em Cycle X
Function.periodicPts         Set X — nao eh dado
EventuallyMeets              proposicao existencial sobre dois naturais
IterReachable                idem
```

## A distinção que evita o erro de categoria

```text
DecidableEq X  eh sobre ESTADOS, elementos de X.
periodicOrbit  vive em Cycle X, quociente por rotacao.
```

Nenhuma decidibilidade sobre `Cycle X` é assumida, requerida ou
construída. O detector nunca compara órbitas; compara `f^[a] x` com
`f^[b] x`, que são elementos de `X`.

## Onde `DecidableEq X` entra e onde não entra

| Objeto | `Fintype X` | `DecidableEq X` |
|---|---|---|
| `CycleWitness` | não | não |
| `cycleCandidates` | não | não |
| `mem_cycleCandidates_iff` | não | não |
| `CycleWitness.Valid` | **sim** | **não** |
| `detectCycleWitness?` | **sim** | **sim** |
| `detectCycleWitness?_sound` | sim | sim (herdado da assinatura do detector) |
| `detectCycleWitness?_complete` | sim | sim (idem) |
| `CycleWitness.isPeriodicPt` | **não** | **não** |
| `CycleWitness.mem_periodicPts` | **não** | **não** |
| `CycleWitness.propagates` | **não** | **não** |

As três pontes proposicionais recebem a colisão `f^[μ+λ] x = f^[μ] x` como
hipótese e não precisam de finitude nem de decidibilidade — exatamente como
`periodic_tail_of_collision` e `collision_propagates`, que também não as
exigem. **`DecidableEq` não será propagada para teoremas que não a
necessitam.**

## Justificativa de `DecidableEq X`

A comparação executável é

```text
f^[mu + lam] x = f^[mu] x
```

entre dois elementos de `X`. Sem `DecidableEq X` não existe instância
`Decidable` para essa igualdade e `decide` não elabora. A necessidade é
**real e verificada** na sonda: a instância para o predicado completo foi
obtida por `inferInstance` no caso `X = Bool`.

Isto **não contradiz** as frentes anteriores.
`FOUND-SEMIGROUP-002` e `FOUND-FUNCTIONAL-GRAPH-001` registraram que
`DecidableEq X` não era necessária — e não era, porque aquelas camadas são
**puramente proposicionais**: afirmar que dois estados são iguais não
exige poder decidir se são. Executar uma comparação exige.

`LAB_STATE.md` proíbe acrescentar `DecidableEq X` "sem necessidade
verificada". A necessidade está verificada, e apenas onde ela existe.
