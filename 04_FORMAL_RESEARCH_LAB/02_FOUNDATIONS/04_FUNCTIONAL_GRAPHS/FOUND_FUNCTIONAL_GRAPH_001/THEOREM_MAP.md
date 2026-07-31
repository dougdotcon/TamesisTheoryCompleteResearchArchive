---
artifact_id: FOUND-FUNCTIONAL-GRAPH-001
status: VERIFIED
lean_root: "05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/"
---

# FOUND-FUNCTIONAL-GRAPH-001 — Mapa de teoremas

## Arquitetura por hipóteses

```text
Relations.lean        sem finitude   IterReachable, MutuallyReachable, EventuallyMeets
PeriodicOrbits.lean   sem finitude   igualdade de orbitas periodicas
ComponentCycle.lean   [Fintype X]    existencia limitada e teorema principal
Counterexamples.lean  modelos finitos
Audit.lean            somente #check
```

`Fintype X` aparece em **um único arquivo**.

## Definições

| Lean | Enunciado | Arquivo |
|---|---|---|
| `IterReachable f x y` | `∃ n, f^[n] x = y` | `Relations` |
| `MutuallyReachable f x y` | `IterReachable f x y ∧ IterReachable f y x` | `Relations` |
| `EventuallyMeets f x y` | `∃ m n, f^[m] x = f^[n] y` | `Relations` |

Não criados: `SameFunctionalComponent`, `componentSet`, `IsRecurrent`,
`IsTransient`, `IsCyclePoint`, `IsTransientPoint`.

## Alcance dirigido

| ID | Lean | Testemunha |
|---|---|---|
| `FFG-REACH-001` | `iterReachable_refl` | `0` |
| `FFG-REACH-002` | `iterReachable_trans` | **`b + a`** |
| `FFG-MEET-004` | `IterReachable.eventuallyMeets` | `(n, 0)` |

### Orientação

```lean
Function.iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)
```

A contagem **externa** fica à **esquerda**. Daí `b + a` e não `a + b`:
`f^[b + a] x = f^[b] (f^[a] x) = f^[b] y = z`.

## Encontro eventual

| ID | Lean | Testemunhas |
|---|---|---|
| `FFG-MEET-001` | `eventuallyMeets_refl` | `(0, 0)` |
| `FFG-MEET-002` | `eventuallyMeets_symm` | troca |
| `FFG-MEET-003` | `eventuallyMeets_trans` | dois casos |

### Transitividade — mapa de índices

```text
hxy da  mx, ny   com  f^[mx] x = f^[ny] y
hyz da  my, nz   com  f^[my] y = f^[nz] z
```

Separação por `Nat.le_total ny my`.

```text
caso ny ≤ my,  d = my - ny   testemunhas  (d + mx, nz)
caso my ≤ ny,  d = ny - my   testemunhas  (mx, d + nz)
```

Cada caso é um `calc` de cinco passos, com `Function.iterate_add_apply`
**explicitamente instanciado** e as igualdades de índices por `omega`.

## Empacotamento relacional — sem instâncias

| Lean | Tipo |
|---|---|
| `eventuallyMeets_isRefl` | `Std.Refl (EventuallyMeets f)` |
| `eventuallyMeets_isSymm` | `Std.Symm (EventuallyMeets f)` |
| `eventuallyMeets_isTrans` | `IsTrans X (EventuallyMeets f)` |

Os três são `theorem`, **nenhum é `instance`**. Nenhuma `Setoid`.

Nota de revisão: `IsRefl` e `Symmetric` estão **depreciados** nesta revisão,
em favor de `Std.Refl` e `Std.Symm`; `IsTrans` não está. Daí a assimetria.

## Órbitas periódicas

| ID | Lean | Classificação |
|---|---|---|
| `FFG-CYCLE-001` | `periodicOrbit_eq_of_eventuallyMeets` | `CORE` |
| `FFG-CYCLE-002` | `eventuallyMeets_of_periodicOrbit_eq` | `OPTIONAL` — **formalizado** |

`FFG-CYCLE-001`, três passos, sem aritmética modular:

```text
periodicOrbit f p = periodicOrbit f (f^[m] p)   (lema hp m).symm
                  = periodicOrbit f (f^[n] q)   rw [hmn]
                  = periodicOrbit f q           lema hq n
```

`FFG-CYCLE-002`, quatro passos: `self_mem_periodicOrbit hp`, reescrita por
`← hOrbit`, `mem_periodicOrbit_iff hq`, testemunhas `(0, n)`.

## Existência e teorema principal

| ID | Lean |
|---|---|
| `FFG-REC-002` | `exists_cyclePoint_reachable_with_bound` |
| `FFG-MAIN-001` | `exists_component_cycle_with_entry_bound` |

```lean
exists_cyclePoint_reachable_with_bound :
  ∀ {X} [Fintype X] (f : X → X) (x : X),
    ∃ mu < Fintype.card X, f^[mu] x ∈ Function.periodicPts f

exists_component_cycle_with_entry_bound :
  ∀ {X} [Fintype X] (f : X → X) (x : X),
    ∃ mu < Fintype.card X,
      f^[mu] x ∈ Function.periodicPts f ∧
      ∀ q ∈ Function.periodicPts f,
        EventuallyMeets f x q →
        Function.periodicOrbit f (f^[mu] x) = Function.periodicOrbit f q
```

### Composição do principal

```text
1. exists_cyclePoint_reachable_with_bound        da mu e hp
2. IterReachable f x (f^[mu] x)                  testemunha mu
3. IterReachable.eventuallyMeets                 EventuallyMeets f x (f^[mu] x)
4. eventuallyMeets_symm                          EventuallyMeets f (f^[mu] x) x
5. eventuallyMeets_trans com hxq                 EventuallyMeets f (f^[mu] x) q
6. periodicOrbit_eq_of_eventuallyMeets hp hq     conclusao
```

**Nenhum pigeonhole, nenhuma indução nova, nenhum `∃!`.**

## Hipóteses efetivamente exigidas

Impressas pelo build:

```text
@eventuallyMeets_trans :
  ∀ {X : Type u_1} {f : X → X} {x y z : X}, ...

@periodicOrbit_eq_of_eventuallyMeets :
  ∀ {X : Type u_1} {f : X → X} {p q : X}, ...

@exists_component_cycle_with_entry_bound :
  ∀ {X : Type u_1} [inst : Fintype X] (f : X → X) (x : X), ...
```

`Fintype X` **ausente** dos dois primeiros. `DecidableEq X` **ausente de
todos**.

## Inventário

```text
arquivos do nucleo        5   (+ agregador + 2 testes)
definicoes                8   (3 relacoes + 5 funcoes de contraexemplo)
auxiliares private        1   (minimalPeriod_eq_two)
teoremas                 44
estruturas                0
indutivos                 5
instancias                5   (Fintype dos contraexemplos)
instancias no nucleo      0
```

## Contraexemplos

| ID | Lean | Refuta |
|---|---|---|
| `FFG-CE-001` | `CE001.not_meets` | ciclo global único |
| `FFG-CE-002` | `CE002.a_not_periodic` | todo estado periódico |
| `FFG-CE-003` | `CE003.not_fixed`, `CE003.orbit_eq` | todo ciclo é ponto fixo |
| `FFG-CE-004` | `CE004.not_mutually_reachable` | componente = alcance mútuo |
| `FFG-CE-005` | `CE005.distinct_points_same_orbit` | um ponto periódico por componente |
| `FFG-CE-006` | `CE006.same_period_different_component` | mesmo período ⟹ mesmo componente |
