---
document_id: FCD-THEOREM-DEPENDENCY-MAP
pigeonhole_in_this_front: false
---

# Mapa de dependências

```text
cycleCandidates
      |
mem_cycleCandidates_iff
      |
detectCycleWitness?_sound

exists_bounded_iterate_collision
      |
detectCycleWitness?_complete

detectCycleWitness?_sound
      |
CycleWitness.Valid
      |
periodic_tail_of_collision
      |
CycleWitness.isPeriodicPt
      |
CycleWitness.mem_periodicPts

CycleWitness.Valid
      |
collision_propagates
      |
CycleWitness.propagates

CycleWitness.mem_periodicPts
      +
FOUND-FUNCTIONAL-GRAPH-001
      |
detected_cycle_is_component_cycle
```

## Correção registrada ao primeiro ramo

O DAG acima reproduz o mapa do gate. A auditoria de
`CORRECTNESS_PLAN.md` mostrou que a aresta

```text
mem_cycleCandidates_iff  ->  detectCycleWitness?_sound
```

**não é necessária**: as cotas estão dentro de `Valid`, e a soundness sai
de `List.find?_some` mais `decide_eq_true_eq`. O mapa efetivo é:

```text
cycleCandidates ---------------------> detectCycleWitness?
                     |
mem_cycleCandidates_iff --------------> detectCycleWitness?_complete

List.find?_some + decide_eq_true_eq --> detectCycleWitness?_sound
```

A dependência foi **removida**, não esquecida. O efeito é desejável: a
soundness sobrevive a uma troca de algoritmo.

## Fronteira do pigeonhole

```text
Fintype.exists_ne_map_eq_of_card_lt
      |
      +--> FOUND-SEMIGROUP-002 : exists_bounded_iterate_collision   [UMA VEZ]
                    |
                    +--> FOUND-FUNCTIONAL-GRAPH-001
                    |
                    +--> FOUND-CYCLE-DETECTION-001
```

A casa dos pombos permanece **somente** na fundação anterior. Esta frente
a consome através de `exists_bounded_iterate_collision` e **não** a
reimplementa.

## Camadas de hipótese

```text
camada 0   cycleCandidates, mem_cycleCandidates_iff
           sem X, sem Fintype, sem DecidableEq

camada 1   CycleWitness.Valid e as tres pontes proposicionais
           Fintype (pela cota), sem DecidableEq

camada 2   detectCycleWitness?, sound, complete
           Fintype e DecidableEq

camada 3   detected_cycle_is_component_cycle
           proposicional, reutiliza FOUND-FUNCTIONAL-GRAPH-001
```

`DecidableEq` aparece **apenas** na camada 2.
