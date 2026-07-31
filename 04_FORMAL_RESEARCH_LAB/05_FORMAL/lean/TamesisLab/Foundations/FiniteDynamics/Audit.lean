import TamesisLab.Foundations.FiniteDynamics.MonoidIteration
import TamesisLab.Foundations.FiniteDynamics.Counterexamples

set_option autoImplicit false

/-!
# FOUND-SEMIGROUP-002 — Audit

Registro de assinaturas. Nenhum resultado novo.

Os `#check` do teorema principal e do corolário de ação existem para tornar
**visíveis na saída do build** as hipóteses efetivamente exigidas — em
particular a ausência de `DecidableEq X`, `Fintype M` e `Group M`.
-/

namespace TamesisLab.Foundations.FiniteDynamics.Audit

section Local

-- Camada A
#check @TamesisLab.Foundations.FiniteDynamics.Reachable
#check @TamesisLab.Foundations.FiniteDynamics.reachable_refl
#check @TamesisLab.Foundations.FiniteDynamics.reachable_trans
#check @TamesisLab.Foundations.FiniteDynamics.reachable_isRefl
#check @TamesisLab.Foundations.FiniteDynamics.reachable_isTrans
#check @TamesisLab.Foundations.FiniteDynamics.reachable_iff_mem_orbit
#check @TamesisLab.Foundations.FiniteDynamics.IsInvariant
#check @TamesisLab.Foundations.FiniteDynamics.IsInvariantUnder
#check @TamesisLab.Foundations.FiniteDynamics.IsInvariant.under
#check @TamesisLab.Foundations.FiniteDynamics.IsInvariant.of_reachable
#check @TamesisLab.Foundations.FiniteDynamics.IsInvariantUnder.pow

-- Camada C
#check @TamesisLab.Foundations.FiniteDynamics.exists_bounded_iterate_collision
#check @TamesisLab.Foundations.FiniteDynamics.periodic_tail_of_collision
#check @TamesisLab.Foundations.FiniteDynamics.collision_propagates
#check @TamesisLab.Foundations.FiniteDynamics.exists_eventual_period

-- Camada B
#check @TamesisLab.Foundations.FiniteDynamics.monoid_element_eventually_periodic
#check @TamesisLab.Foundations.FiniteDynamics.monoid_element_eventual_period_propagates

end Local

section MathlibReuse

-- Reutilizados sem redefinicao, na revisao fixada v4.33.0-rc1
-- (rev 79d0395a1825a6264ad5d269e35e60537518955e).
#check @MulAction.orbit
#check @MulAction.mem_orbit_iff
#check @Fintype.exists_ne_map_eq_of_card_lt
#check @Function.iterate_add_apply
#check @Function.IsPeriodicPt
#check @smul_iterate_apply

end MathlibReuse

section Counterexamples

#check @Counterexamples.CE001.reachable_not_symmetric
#check @Counterexamples.CE002.not_transitive
#check @Counterexamples.CE003.s0_not_periodic
#check @Counterexamples.CE004.not_faithful
#check @Counterexamples.CE005.invariant_does_not_separate_orbits

end Counterexamples

end TamesisLab.Foundations.FiniteDynamics.Audit
