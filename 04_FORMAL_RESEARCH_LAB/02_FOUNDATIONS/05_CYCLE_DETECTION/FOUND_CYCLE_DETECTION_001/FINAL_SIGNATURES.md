---
document_id: FCD-FINAL-SIGNATURES
frozen: true
count_public: 12
---

# Assinaturas congeladas

Desviar de qualquer uma delas exige gate próprio.

## Executáveis

```lean
structure CycleWitness where
  baseIndex : ℕ
  period : ℕ

def cycleCandidates (n : ℕ) : List CycleWitness

def detectCycleWitness?
    {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : Option CycleWitness
```

## Predicado e instância

```lean
def CycleWitness.Valid
    {X : Type*} [Fintype X]
    (f : X → X) (x : X) (w : CycleWitness) : Prop

instance CycleWitness.decidableValid
    {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) (w : CycleWitness) :
    Decidable (CycleWitness.Valid f x w)
```

## Enumeração

```lean
theorem mem_cycleCandidates_iff
    {n : ℕ} {w : CycleWitness} :
    w ∈ cycleCandidates n ↔
      w.baseIndex < n ∧
      0 < w.period ∧
      w.baseIndex + w.period ≤ n
```

Sem `Fintype`, sem `DecidableEq`, sem `Classical`, sem `f`, sem `x`.

## Correção e completude

```lean
theorem detectCycleWitness?_sound
    {X : Type*} [Fintype X] [DecidableEq X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : detectCycleWitness? f x = some w) :
    CycleWitness.Valid f x w

theorem detectCycleWitness?_complete
    {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) :
    ∃ w : CycleWitness, detectCycleWitness? f x = some w
```

## Pontes proposicionais

```lean
theorem CycleWitness.isPeriodicPt
    {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) :
    Function.IsPeriodicPt f w.period (f^[w.baseIndex] x)

theorem CycleWitness.mem_periodicPts
    {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) :
    f^[w.baseIndex] x ∈ Function.periodicPts f

theorem CycleWitness.propagates
    {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) (k : ℕ) :
    f^[w.baseIndex + k + w.period] x =
      f^[w.baseIndex + k] x
```

**Nenhuma** das três recebe `DecidableEq`.

`propagates` foi alinhada à assinatura já verificada, lida do fonte neste
gate:

```lean
theorem collision_propagates {X : Type*} (f : X → X) (x : X) {mu lam : ℕ}
    (h : f^[mu + lam] x = f^[mu] x) (k : ℕ) :
    f^[mu + k + lam] x = f^[mu + k] x
```

Mesma forma, mesma ordem de argumentos: hipótese primeiro, `k` depois.
Nenhuma chamada extra a `Nat.add_comm` será necessária, e
`Function.iterate_add_apply` **não** será reprovado.

## Opcionais

```lean
def detectCycleWitness
    {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : CycleWitness

theorem detectCycleWitness_valid
    {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) :
    CycleWitness.Valid f x (detectCycleWitness f x)

theorem detected_cycle_is_component_cycle
    {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) :
    ∀ q ∈ Function.periodicPts f,
      EventuallyMeets f x q →
        Function.periodicOrbit f (f^[w.baseIndex] x) =
          Function.periodicOrbit f q
```

As duas primeiras dependem da totalização, `DEFERRED`. A terceira é
proposicional e pode ser omitida da primeira formalização — ver
`REVIEW_DECISION.md`.

## Contagem

```text
PUBLIC_EXECUTABLE_CORE        3
PUBLIC_SPECIFICATION_CORE     7  (+1 instancia)
OPTIONAL_CORE                 3
```
