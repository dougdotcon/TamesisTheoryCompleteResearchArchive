---
document_id: FCD-THEOREM-CANDIDATES
core: 10
optional_core: 3
---

# Teoremas candidatos

## `CORE`

```text
CycleWitness
CycleWitness.Valid

cycleCandidates
mem_cycleCandidates_iff

detectCycleWitness?
detectCycleWitness?_sound
detectCycleWitness?_complete

CycleWitness.isPeriodicPt
CycleWitness.mem_periodicPts
CycleWitness.propagates
```

Assinaturas candidatas:

```lean
structure CycleWitness where
  baseIndex : ℕ
  period : ℕ

def CycleWitness.Valid {X : Type*} [Fintype X]
    (f : X → X) (x : X) (w : CycleWitness) : Prop

def cycleCandidates (n : ℕ) : List CycleWitness

theorem mem_cycleCandidates_iff {n : ℕ} {w : CycleWitness} :
    w ∈ cycleCandidates n ↔
      w.baseIndex < n ∧ 0 < w.period ∧ w.baseIndex + w.period ≤ n

def detectCycleWitness? {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : Option CycleWitness

theorem detectCycleWitness?_sound {X : Type*} [Fintype X] [DecidableEq X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : detectCycleWitness? f x = some w) :
    CycleWitness.Valid f x w

theorem detectCycleWitness?_complete {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) :
    ∃ w : CycleWitness, detectCycleWitness? f x = some w

theorem CycleWitness.isPeriodicPt {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness} (h : CycleWitness.Valid f x w) :
    Function.IsPeriodicPt f w.period (f^[w.baseIndex] x)

theorem CycleWitness.mem_periodicPts {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness} (h : CycleWitness.Valid f x w) :
    f^[w.baseIndex] x ∈ Function.periodicPts f

theorem CycleWitness.propagates {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness} (h : CycleWitness.Valid f x w) :
    ∀ k : ℕ,
      f^[w.baseIndex + k + w.period] x = f^[w.baseIndex + k] x
```

Nota sobre os binders de `isPeriodicPt`, `mem_periodicPts` e `propagates`:
`[Fintype X]` aparece porque `Valid` o exige — não porque a matemática
precise dele. Se a formalização adotar o auxiliar `ValidAt n` registrado
como fallback em `DATA_MODEL.md`, as três podem perder `Fintype`. **Sem
`DecidableEq` em nenhuma das três.**

## `OPTIONAL_CORE`

```text
detectCycleWitness
detectCycleWitness_valid
detected_cycle_is_component_cycle
```

```lean
def detectCycleWitness {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : CycleWitness

theorem detectCycleWitness_valid {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) :
    CycleWitness.Valid f x (detectCycleWitness f x)

theorem detected_cycle_is_component_cycle {X : Type*} [Fintype X]
    {f : X → X} {x : X} {w : CycleWitness} (h : CycleWitness.Valid f x w) :
    ∀ q ∈ Function.periodicPts f,
      EventuallyMeets f x q →
        Function.periodicOrbit f (f^[w.baseIndex] x) =
          Function.periodicOrbit f q
```

As duas primeiras dependem da totalização, hoje `DEFERRED`. A terceira é
puramente proposicional e independe dela.

## `DEFERRED`

```text
minimalidade de baseIndex;
minimalidade de period;
Floyd;
Brent;
tabela visitada;
lista do ciclo;
enumeracao de componentes;
complexidade formal;
integracao externa.
```

## Reutilização por teorema

| Candidato | Reutiliza | Prova nova? |
|---|---|---|
| `mem_cycleCandidates_iff` | `List.mem_flatMap`, `List.mem_map`, `List.mem_range` | sim, mas elementar |
| `detectCycleWitness?_sound` | `List.find?_some`, `decide_eq_true_eq` | quase nenhuma |
| `detectCycleWitness?_complete` | **`exists_bounded_iterate_collision`**, `mem_cycleCandidates_iff`, `List.find?_isSome`, `Option.isSome_iff_exists` | transporte |
| `CycleWitness.isPeriodicPt` | **`periodic_tail_of_collision`** | **nenhuma** — aplicação direta |
| `CycleWitness.mem_periodicPts` | `Function.mk_mem_periodicPts` + a anterior | nenhuma |
| `CycleWitness.propagates` | **`collision_propagates`** | **nenhuma** — assinatura idêntica |
| `detected_cycle_is_component_cycle` | `periodicOrbit_eq_of_eventuallyMeets`, `IterReachable.eventuallyMeets`, `eventuallyMeets_symm`, `eventuallyMeets_trans` | nenhuma nova; espelha `exists_component_cycle_with_entry_bound` |

Três dos dez `CORE` não exigem matemática nova alguma: são aplicações
literais de teoremas já `VERIFIED`.
