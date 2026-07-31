---
document_id: FCD-THEOREM-MAP
structures: 1
definitions: 3
instances: 1
theorems: 8
---

# Mapa dos teoremas formalizados

Tudo o que foi de fato construído, com o arquivo e a rota de prova.

## `Witness.lean`

| Objeto | Tipo | Hipóteses |
|---|---|---|
| `CycleWitness` | `structure` | nenhuma |
| `CycleWitness.Valid` | `def ... : Prop` | `[Fintype X]` |
| `CycleWitness.decidableValid` | `instance` | `[Fintype X]`, `[DecidableEq X]` |

`CycleWitness` deriva `DecidableEq`, `Repr` e `BEq`. A instância decidível
foi construída por `inferInstanceAs` sobre a conjunção expandida — sem ela
o `decide` do detector não elabora, achado registrado no gate de revisão.

## `Candidates.lean`

| Teorema | Rota |
|---|---|
| `cycleCandidates_zero` | `rfl` |
| `cycleCandidates_one` | `rfl` |
| `mem_cycleCandidates_iff` | `rcases`, `simp only [cycleCandidates, List.mem_flatMap, List.mem_map, List.mem_range, CycleWitness.mk.injEq]`, `constructor`, `omega` nos dois lados |

Os dois primeiros são `@[simp]`. `mem_cycleCandidates_iff` **não** tem
`Fintype`, `DecidableEq`, `Classical`, `f` nem `x` — confirmado pela
assinatura impressa.

## `Detector.lean`

```lean
def detectCycleWitness? {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : Option CycleWitness :=
  (cycleCandidates (Fintype.card X)).find? fun w =>
    decide (CycleWitness.Valid f x w)
```

Único ponto da frente em que `DecidableEq X` entra numa **definição**.

## `Correctness.lean`

| Teorema | Rota | Reutiliza |
|---|---|---|
| `detectCycleWitness?_sound` | `unfold`, `List.find?_some` com o predicado explícito, `of_decide_eq_true` | — |
| `detectCycleWitness?_complete` | `exists_bounded_iterate_collision` → `CycleWitness` → `mem_cycleCandidates_iff` → `List.find?_isSome` → `Option.isSome_iff_exists` | **`exists_bounded_iterate_collision`** |

A soundness **não** depende de `mem_cycleCandidates_iff`: as três cotas
vivem dentro de `Valid`. Foi preciso passar o predicado explicitamente a
`List.find?_some` — sem isso a unificação de ordem superior escolhia
`@decide (Valid f x w)` como função constante e falhava.

## `Periodicity.lean`

| Teorema | Rota | Prova nova |
|---|---|---|
| `CycleWitness.isPeriodicPt` | `periodic_tail_of_collision f x h.2.2.2` | **nenhuma** |
| `CycleWitness.mem_periodicPts` | `Function.mk_mem_periodicPts h.2.1 (isPeriodicPt h)` | **nenhuma** |
| `CycleWitness.propagates` | `collision_propagates f x h.2.2.2 k` | **nenhuma** |

Três aplicações de uma linha cada. Nenhuma aritmética de iteradas foi
reprovada; `Function.iterate_add_apply` não aparece em arquivo algum desta
frente.

## `Audit.lean`

Somente `#check`. Nenhuma definição, nenhum teorema.

## Agregadores

`TamesisLab/Foundations/CycleDetection.lean` importa os cinco módulos do
núcleo. `TamesisLab/Foundations.lean` importa esse agregador e o `Audit`;
`TamesisLab.lean` importa os três testes. Sem esses dois registros, o alvo
padrão do `lake build` não alcançaria a frente.

## Camadas de hipótese, verificadas

```text
camada 0   cycleCandidates, mem_cycleCandidates_iff
           sem X, sem Fintype, sem DecidableEq

camada 1   CycleWitness.Valid
           Fintype pela cota, SEM DecidableEq

camada 2   detectCycleWitness?, _sound, _complete
           Fintype e DecidableEq

camada 3   isPeriodicPt, mem_periodicPts, propagates
           Fintype (herdado de Valid), SEM DecidableEq
```
