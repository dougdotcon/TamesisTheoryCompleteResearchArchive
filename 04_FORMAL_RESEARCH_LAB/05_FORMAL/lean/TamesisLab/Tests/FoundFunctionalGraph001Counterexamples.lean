import TamesisLab.Foundations.FunctionalGraphs

set_option autoImplicit false

/-!
# Teste isolado — FOUND-FUNCTIONAL-GRAPH-001 (contraexemplos)

Seis modelos, seis afirmações refutadas distintas.

Nenhum `native_decide`. `decide` **não** é usado sobre igualdade de
`Function.periodicOrbit`, que é noncomputável.
-/

namespace TamesisLab.Tests.FoundFunctionalGraph001Counterexamples

open TamesisLab.Foundations.FunctionalGraphs
open TamesisLab.Foundations.FunctionalGraphs.Counterexamples

/-! ## CE-001 — dois ciclos globais distintos -/

example : CE001.St.a ∈ Function.periodicPts CE001.f := CE001.a_periodic
example : CE001.St.b ∈ Function.periodicPts CE001.f := CE001.b_periodic
example : ¬ EventuallyMeets CE001.f CE001.St.a CE001.St.b := CE001.not_meets

/-! ## CE-002 — cauda antes do ciclo -/

example : CE002.St.a ∉ Function.periodicPts CE002.f := CE002.a_not_periodic
example : CE002.St.c ∈ Function.periodicPts CE002.f := CE002.c_periodic
example : IterReachable CE002.f CE002.St.a CE002.St.c := CE002.reach_a_c
example : EventuallyMeets CE002.f CE002.St.a CE002.St.c := CE002.meets_a_c

/-- O teorema principal se aplica ao modelo com cauda. -/
example :
    ∃ mu : ℕ,
      mu < Fintype.card CE002.St ∧
      CE002.f^[mu] CE002.St.a ∈ Function.periodicPts CE002.f ∧
      ∀ q : CE002.St,
        q ∈ Function.periodicPts CE002.f →
        EventuallyMeets CE002.f CE002.St.a q →
        Function.periodicOrbit CE002.f (CE002.f^[mu] CE002.St.a) =
          Function.periodicOrbit CE002.f q :=
  exists_component_cycle_with_entry_bound CE002.f CE002.St.a

/-! ## CE-003 — ciclo de comprimento maior que um -/

example : CE003.St.a ∈ Function.periodicPts CE003.f := CE003.a_periodic
example : CE003.St.b ∈ Function.periodicPts CE003.f := CE003.b_periodic
example : CE003.St.a ≠ CE003.St.b := CE003.a_ne_b
example : CE003.f CE003.St.a ≠ CE003.St.a := CE003.not_fixed

/-- Igualdade de órbitas provada **sem** `decide`. -/
example :
    Function.periodicOrbit CE003.f CE003.St.b =
      Function.periodicOrbit CE003.f CE003.St.a :=
  CE003.orbit_eq

/-! ## CE-004 — mesmo componente sem alcance mútuo

O contraexemplo decisivo: refuta `MutuallyReachable` como componente. -/

example : EventuallyMeets CE004.f CE004.St.a CE004.St.b := CE004.meets_a_b
example : ¬ IterReachable CE004.f CE004.St.a CE004.St.b := CE004.not_reach_a_b
example : ¬ IterReachable CE004.f CE004.St.b CE004.St.a := CE004.not_reach_b_a
example : ¬ MutuallyReachable CE004.f CE004.St.a CE004.St.b :=
  CE004.not_mutually_reachable

/-! ## CE-005 — vários pontos cíclicos, uma única órbita -/

example :
    CE003.St.a ≠ CE003.St.b ∧
      CE003.St.a ∈ Function.periodicPts CE003.f ∧
      CE003.St.b ∈ Function.periodicPts CE003.f ∧
      Function.periodicOrbit CE003.f CE003.St.b =
        Function.periodicOrbit CE003.f CE003.St.a :=
  CE005.distinct_points_same_orbit

/-! ## CE-006 — mesmo período mínimo, componentes distintos -/

example : Function.minimalPeriod CE006.f CE006.St.a0 = 2 := CE006.a0_minimalPeriod
example : Function.minimalPeriod CE006.f CE006.St.b0 = 2 := CE006.b0_minimalPeriod

example :
    Function.minimalPeriod CE006.f CE006.St.a0 =
        Function.minimalPeriod CE006.f CE006.St.b0 ∧
      ¬ EventuallyMeets CE006.f CE006.St.a0 CE006.St.b0 :=
  CE006.same_period_different_component

end TamesisLab.Tests.FoundFunctionalGraph001Counterexamples
