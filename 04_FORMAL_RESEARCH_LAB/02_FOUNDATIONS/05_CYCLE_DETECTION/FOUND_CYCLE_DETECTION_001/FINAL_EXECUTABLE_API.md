---
document_id: FCD-FINAL-EXECUTABLE-API
frozen: true
---

# API executável final — congelada

## `PUBLIC_EXECUTABLE_CORE`

```lean
structure CycleWitness where
  baseIndex : ℕ
  period : ℕ

def cycleCandidates (n : ℕ) : List CycleWitness :=
  (List.range n).flatMap fun m =>
    (List.range (n - m)).map fun k =>
      ⟨m, k + 1⟩

def detectCycleWitness?
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    (f : X → X)
    (x : X) :
    Option CycleWitness :=
  (cycleCandidates (Fintype.card X)).find? fun w =>
    decide (CycleWitness.Valid f x w)
```

A ordem dos argumentos foi conferida no probe: `List.find?` recebe o
predicado primeiro, e a forma com ponto — `lista.find? pred` — elabora
corretamente.

## Predicado executável

Uma **única** representação proposicional, `CycleWitness.Valid`, decidida
por `decide`. **Não** foram criados `validB`, `isValid` nem
`checkWitness`.

Lemas de ponte confirmados no checkout:

```text
decide_eq_true_eq       : (decide p = true) = p
of_decide_eq_true       : decide p = true -> p
decide_eq_false_iff_not : decide p = false <-> ¬p
```

Os três existem. `of_decide_eq_true` é a forma direta e provavelmente a
mais conveniente na soundness.

## Exigências confirmadas

```text
computable            SIM — #eval em cinco modelos
sem noncomputable     SIM
sem Classical.choose  SIM
sem periodicOrbit     SIM
sem SimpleGraph       SIM
```

Sobre `Classical`: ver o achado de pegada axiomática em
`COMPUTABILITY_REVIEW.md`. Resumidamente, `Classical.choice` aparece na
pegada por causa de `Fintype.card`, e isso **não** afeta a
executabilidade.

## `PUBLIC_SPECIFICATION_CORE`

```text
CycleWitness.Valid
mem_cycleCandidates_iff
detectCycleWitness?_sound
detectCycleWitness?_complete
CycleWitness.isPeriodicPt
CycleWitness.mem_periodicPts
CycleWitness.propagates
```

## `OPTIONAL_CORE`

```text
detectCycleWitness
detected_cycle_is_component_cycle
```

## `DEFERRED`

```text
Floyd
Brent
tabela visitada
minimalidade
complexidade formal
extracao
integracao
enumeracao global de componentes
```

## Ordem determinística

```text
baseIndex crescente; dentro dele, period crescente.
```

Confirmada por avaliação. Autoriza **testes de regressão**. **Não**
autoriza teorema de `baseIndex` mínimo, de `period` mínimo, nem
equivalência com `minimalPeriod`. `CD-GAP-018` permanece aberto.
