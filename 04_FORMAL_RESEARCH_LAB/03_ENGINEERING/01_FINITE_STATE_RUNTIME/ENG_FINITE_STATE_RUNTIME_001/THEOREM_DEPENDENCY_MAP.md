---
document_id: RT-THEOREM-DEPENDENCY-MAP
pigeonhole_in_this_front: false
---

# Mapa de dependências

```text
RawTransitionTable
      |
RawTransitionTable.Valid ------ decidableValid
      |                              |
      |                       validateTransitionTable
      |                          /            \
      |          validateTransitionTable_sound  validateTransitionTable_complete
      v
ValidatedTransitionTable
      |
      +--> toRaw ---> toRaw_valid
      |
      +--> validateStart ---> _sound, _complete
      |
      +--> step ---> step_val
                        |
RawTransitionTable.step? ---- step?_eq_some_step
      |                              |
RawTransitionTable.run? -------------+
      |                              |
      +------------------> run?_eq_iterate_step
                                     |
detectCycleWitness?  --------> detectCycle?
      |                          /        \
detectCycleWitness?_sound       /          \  detectCycleWitness?_complete
      |                        /            \        |
      +--> detectCycle?_sound              detectCycle?_complete
                   |                                 |
                   +---> detectCycle?_raw_repeat <---+
                                     |
                              analyzeTransitionTable
                                  /         \
              analyzeTransitionTable_sound   analyzeTransitionTable_complete
                                                     |
                                    analyzeTransitionTable_ne_internalFailure
```

## Camadas

```text
camada 0   dado bruto              RawTransitionTable, Valid, step?, run?
           sem typeclass, sem Fin

camada 1   validacao               validateTransitionTable, validateStart
           sem typeclass externa

camada 2   dominio tipado          ValidatedTransitionTable, step
           Fin construido internamente

camada 3   ponte                   step?_eq_some_step, run?_eq_iterate_step
           conecta 0 e 2

camada 4   detector                detectCycle? e herdeiros
           Fintype e DecidableEq INFERIDAS

camada 5   API dinamica            analyzeTransitionTable
           nenhuma hipotese do chamador
```

## Fronteira do pigeonhole

```text
Fintype.exists_ne_map_eq_of_card_lt
      |
      +--> FOUND-SEMIGROUP-002 : exists_bounded_iterate_collision   [UMA VEZ]
                 |
                 +--> FOUND-FUNCTIONAL-GRAPH-001
                 |
                 +--> FOUND-CYCLE-DETECTION-001
                            |
                            +--> ENG-FINITE-STATE-RUNTIME-001
```

Quarta frente a consumir a casa dos pombos **através** do teorema
original. Exigência de contagem zero para o lema nos módulos desta frente.

## O ramo que não existe

```text
analyzeTransitionTable
      |
      +-- .ok witness                    alcancavel
      |
      +-- error transitionDestination... alcancavel
      |
      +-- error initialStateOutOfBounds  alcancavel
      |
      +-- error internalDetectorFailure  INALCANCAVEL para entradas validas
                                          (analyzeTransitionTable_ne_internalFailure)
```

O quarto ramo existe no código e não existe na semântica. Essa assimetria
é deliberada e está documentada em `DYNAMIC_ANALYSIS_API.md`.
