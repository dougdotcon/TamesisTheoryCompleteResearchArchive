import TamesisLab.Foundations.FunctionalGraphs.Counterexamples

set_option autoImplicit false

/-!
# FOUND-FUNCTIONAL-GRAPH-001 — Audit

Registro de assinaturas. Nenhum resultado novo.

Os `#check` tornam visíveis na saída do build as hipóteses efetivamente
exigidas — em particular a **ausência** de `Fintype X` e `DecidableEq X`
nas relações e na igualdade de órbitas.
-/

namespace TamesisLab.Foundations.FunctionalGraphs.Audit

section Local

#check @TamesisLab.Foundations.FunctionalGraphs.IterReachable
#check @TamesisLab.Foundations.FunctionalGraphs.MutuallyReachable
#check @TamesisLab.Foundations.FunctionalGraphs.EventuallyMeets

#check @TamesisLab.Foundations.FunctionalGraphs.iterReachable_refl
#check @TamesisLab.Foundations.FunctionalGraphs.iterReachable_trans
#check @TamesisLab.Foundations.FunctionalGraphs.IterReachable.eventuallyMeets

#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_refl
#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_symm
#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_trans

#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_isRefl
#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_isSymm
#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_isTrans

#check @TamesisLab.Foundations.FunctionalGraphs.periodicOrbit_eq_of_eventuallyMeets
#check @TamesisLab.Foundations.FunctionalGraphs.eventuallyMeets_of_periodicOrbit_eq

#check @TamesisLab.Foundations.FunctionalGraphs.exists_cyclePoint_reachable_with_bound
#check @TamesisLab.Foundations.FunctionalGraphs.exists_component_cycle_with_entry_bound

end Local

section MathlibReuse

-- Reutilizados sem redefinicao, revisao v4.33.0-rc1
-- (rev 79d0395a1825a6264ad5d269e35e60537518955e).
#check @Function.periodicPts
#check @Function.mem_periodicPts
#check @Function.mk_mem_periodicPts
#check @Function.periodicOrbit
#check @Function.periodicOrbit_apply_iterate_eq
#check @Function.mem_periodicOrbit_iff
#check @Function.self_mem_periodicOrbit
#check @Function.iterate_add_apply
#check @Function.IsPeriodicPt.minimalPeriod_dvd
#check @Function.minimalPeriod_eq_one_iff_isFixedPt
#check @Function.minimalPeriod_pos_of_mem_periodicPts

-- Reutilizado de FOUND-SEMIGROUP-002, VERIFIED.
#check @TamesisLab.Foundations.FiniteDynamics.exists_eventual_period

end MathlibReuse

section Counterexamples

#check @Counterexamples.CE001.not_meets
#check @Counterexamples.CE002.a_not_periodic
#check @Counterexamples.CE003.orbit_eq
#check @Counterexamples.CE004.not_mutually_reachable
#check @Counterexamples.CE005.distinct_points_same_orbit
#check @Counterexamples.CE006.same_period_different_component

end Counterexamples

end TamesisLab.Foundations.FunctionalGraphs.Audit
