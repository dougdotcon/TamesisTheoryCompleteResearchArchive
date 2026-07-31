---
artifact_id: FOUND-FUNCTIONAL-GRAPH-001
audit_status: PASS
---

# FOUND-FUNCTIONAL-GRAPH-001 — Auditoria de prova

## Axiomas

```text
iterReachable_trans                      does not depend on any axioms
eventuallyMeets_trans                    [propext, Quot.sound]
periodicOrbit_eq_of_eventuallyMeets      [propext, Classical.choice, Quot.sound]
eventuallyMeets_of_periodicOrbit_eq      [propext, Classical.choice, Quot.sound]
exists_cyclePoint_reachable_with_bound   [propext, Classical.choice, Quot.sound]
exists_component_cycle_with_entry_bound  [propext, Classical.choice, Quot.sound]
```

`iterReachable_trans` **não depende de axioma algum**.
`eventuallyMeets_trans` usa apenas `propext` e `Quot.sound`, sem
`Classical.choice` — a escolha entra só pela cadeia de `periodicOrbit` e do
pigeonhole herdado. **Sem `sorryAx`, sem axioma local.**

## Tokens proibidos

```bash
grep -RInE '\b(sorry|admit|axiom|unsafe)\b' --include='*.lean' --exclude-dir='.lake' .
```

```text
sorry=0  admit=0  axiom=0  unsafe=0
```

`native_decide`: **3 ocorrências textuais, todas em docstrings** declarando
que **não** é usado — duas nesta frente, uma herdada de
`FOUND-SEMIGROUP-002`. Zero invocações.

## Imports do núcleo

```text
Relations.lean        Mathlib.Logic.Function.Iterate
                      Mathlib.Order.Defs.Unbundled
PeriodicOrbits.lean   TamesisLab...FunctionalGraphs.Relations
                      Mathlib.Dynamics.PeriodicPts.Defs
ComponentCycle.lean   TamesisLab...FunctionalGraphs.PeriodicOrbits
                      TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity
                      Mathlib.Data.Fintype.Card
```

**Zero imports** de `SimpleGraph`, `Setoid`, `Quotient`, análise,
topologia, medida, PDE, geometria, `RH-NOGO` ou legado. O umbrella
`Mathlib.Tactic` **não** foi necessário.

`Mathlib.Tactic.Omega` **não existe** nesta revisão — `omega` é tática do
core. O import sugerido pelo gate foi corretamente omitido.

`Cycle` aparece apenas através da API de `periodicOrbit`; nenhuma
manipulação interna do quociente.

### Menções em prosa

`SimpleGraph` aparece 2 vezes e `Setoid` 1 vez nos arquivos do núcleo,
**todas em docstrings** que declaram a exclusão. `Quotient`: zero
ocorrências.

## Instâncias

```text
Relations.lean        0
PeriodicOrbits.lean   0
ComponentCycle.lean   0
Audit.lean            0
Counterexamples.lean  5   (Fintype de CE001, CE002, CE003, CE004, CE006)
```

**Zero instâncias no núcleo matemático.** Nenhuma `Setoid`, nenhuma
instância global de equivalência, nenhuma instância de `Preorder`. `CE005`
não declara instância: reutiliza o modelo de `CE003`.

## Uso único do pigeonhole

`Fintype.exists_ne_map_eq_of_card_lt` **não aparece** nesta frente. O
princípio foi consumido uma única vez em `FOUND-SEMIGROUP-002`, dentro de
`exists_bounded_iterate_collision`, e aqui apenas se reutiliza
`exists_eventual_period` via `Function.mk_mem_periodicPts`.

## `decide` e noncomputabilidade

`Function.periodicOrbit` é noncomputável. Nenhuma igualdade de órbitas é
provada por `decide`:

```text
CE003.orbit_eq                       periodicOrbit_apply_iterate_eq a_periodic 1
CE005.distinct_points_same_orbit     reutiliza CE003.orbit_eq
```

`decide` é usado apenas sobre tabelas finitas, desigualdade de estados e
proposições decidíveis transparentes.

## Falhas durante a execução

Três, todas corrigidas sem token proibido:

1. **`le_total` desconhecido** no contexto de imports mínimos. Trocado por
   `Nat.le_total`, que é do core.
2. **`Symmetric` depreciado** em favor de `Std.Symm`, com `α` implícito —
   mesmo padrão de `IsRefl`/`Std.Refl` já encontrado em
   `FOUND-SEMIGROUP-002`. Enunciado e teste trocados. O construtor de
   `Std.Symm` tem os dois elementos **explícitos**, exigindo
   `⟨fun _ _ h => …⟩`.
3. **`rw` não fechava por `rfl`** em cinco lemas de iteração dos
   contraexemplos: o `rfl` automático de `rw` usa transparência reducível e
   não desdobra as funções definidas por casamento de padrão. Corrigido com
   `rfl` explícito.

Nenhuma exigiu enfraquecer enunciado.

## Build

```text
lake build TamesisLab.Foundations.FunctionalGraphs   PASS, 752 jobs
lake build (completo)                                PASS, 8726 jobs, 96 s
Tests/FoundFunctionalGraph001.lean                   exit 0, 27 s
Tests/FoundFunctionalGraph001Counterexamples.lean    exit 0, 2 s
```

Nenhum teste foi removido para fazer o build passar; ambos permanecem
importados por `TamesisLab.lean`.

## O que **não** foi provado

```text
ponte com conectividade de SimpleGraph;
decomposicao em arvores;
distancia minima ao ciclo;
tempo minimo de entrada;
periodo minimo no teorema principal;
representante canonico;
quociente formal dos componentes;
classificacao completa;
qualquer resultado sobre sistemas infinitos.
```
