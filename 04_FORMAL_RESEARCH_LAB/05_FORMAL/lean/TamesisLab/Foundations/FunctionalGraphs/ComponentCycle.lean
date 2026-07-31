import TamesisLab.Foundations.FunctionalGraphs.PeriodicOrbits
import TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity
import Mathlib.Data.Fintype.Card

set_option autoImplicit false

/-!
# FOUND-FUNCTIONAL-GRAPH-001 — Ciclo do componente

Único arquivo do núcleo que usa `Fintype X`.

O princípio da casa dos pombos **não** é reaplicado: ele foi consumido uma
única vez em `FOUND-SEMIGROUP-002`, dentro de
`exists_bounded_iterate_collision`, e aqui apenas se reutiliza
`exists_eventual_period`.

## Interpretação vinculante

A unicidade provada é da **órbita periódica** do componente definido por
`EventuallyMeets`.

Não é unicidade do ponto periódico, do índice de entrada, do período, do
representante do ciclo, nem de um ciclo global para toda a função. E não é
uma decomposição por `SimpleGraph`.
-/

namespace TamesisLab.Foundations.FunctionalGraphs

open TamesisLab.Foundations.FiniteDynamics

/-- FFG-REC-002 — toda trajetória num tipo finito alcança um ponto
periódico antes de `Fintype.card X` passos.

Adaptador de `exists_eventual_period` via `Function.mk_mem_periodicPts`.
Sem par artificial `ℕ × X`, sem `DecidableEq X`. -/
theorem exists_cyclePoint_reachable_with_bound {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu : ℕ, mu < Fintype.card X ∧ f^[mu] x ∈ Function.periodicPts f := by
  obtain ⟨mu, lam, hmu, hlam, _, hper, _⟩ := exists_eventual_period f x
  exact ⟨mu, hmu, Function.mk_mem_periodicPts hlam hper⟩

/-- **FFG-MAIN-001** — teorema principal.

A trajetória de `x` alcança um ponto periódico antes de `card X` passos, e
**qualquer** ponto periódico do mesmo componente funcional determina
exatamente a mesma órbita periódica.

Prova por composição: `exists_cyclePoint_reachable_with_bound`,
`IterReachable.eventuallyMeets`, `eventuallyMeets_symm`,
`eventuallyMeets_trans` e `periodicOrbit_eq_of_eventuallyMeets`. Nenhum
passo analítico novo, nenhum `∃!`. -/
theorem exists_component_cycle_with_entry_bound {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu : ℕ,
      mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f ∧
      ∀ q : X,
        q ∈ Function.periodicPts f →
        EventuallyMeets f x q →
        Function.periodicOrbit f (f^[mu] x) = Function.periodicOrbit f q := by
  obtain ⟨mu, hmu, hp⟩ := exists_cyclePoint_reachable_with_bound f x
  refine ⟨mu, hmu, hp, ?_⟩
  intro q hq hxq
  have hreach : IterReachable f x (f^[mu] x) := ⟨mu, rfl⟩
  have h1 : EventuallyMeets f x (f^[mu] x) := hreach.eventuallyMeets
  have h2 : EventuallyMeets f (f^[mu] x) x := eventuallyMeets_symm h1
  have h3 : EventuallyMeets f (f^[mu] x) q := eventuallyMeets_trans h2 hxq
  exact periodicOrbit_eq_of_eventuallyMeets hp hq h3

end TamesisLab.Foundations.FunctionalGraphs
