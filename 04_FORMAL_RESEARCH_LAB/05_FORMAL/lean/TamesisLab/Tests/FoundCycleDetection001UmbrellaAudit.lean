import TamesisLab

set_option autoImplicit false

/-!
# Auditoria de cobertura do agregador raiz

Este teste existe por causa de um defeito real: na primeira passagem da
formalização os agregadores não foram atualizados, e o alvo padrão do
`lake build` passava **sem cobrir a frente**.

O teste importa **apenas** `TamesisLab` — a raiz — e referencia a frente
por nome totalmente qualificado. Ele falha se a frente deixar de ser
alcançada pelo agregador raiz.
-/

namespace TamesisLab.Tests.FoundCycleDetection001UmbrellaAudit

#check TamesisLab.Foundations.CycleDetection.CycleWitness
#check TamesisLab.Foundations.CycleDetection.CycleWitness.Valid
#check TamesisLab.Foundations.CycleDetection.CycleWitness.decidableValid
#check TamesisLab.Foundations.CycleDetection.cycleCandidates
#check TamesisLab.Foundations.CycleDetection.mem_cycleCandidates_iff
#check TamesisLab.Foundations.CycleDetection.detectCycleWitness?
#check TamesisLab.Foundations.CycleDetection.detectCycleWitness?_sound
#check TamesisLab.Foundations.CycleDetection.detectCycleWitness?_complete
#check TamesisLab.Foundations.CycleDetection.CycleWitness.isPeriodicPt
#check TamesisLab.Foundations.CycleDetection.CycleWitness.mem_periodicPts
#check TamesisLab.Foundations.CycleDetection.CycleWitness.propagates
#check TamesisLab.Foundations.CycleDetection.cycleCandidates_zero
#check TamesisLab.Foundations.CycleDetection.cycleCandidates_one

/-! ## Exemplo executável alcançado pela raiz -/

#eval TamesisLab.Foundations.CycleDetection.detectCycleWitness?
  (fun b : Bool => !b) true

example :
    TamesisLab.Foundations.CycleDetection.detectCycleWitness?
      (fun b : Bool => !b) true
      = some ⟨0, 2⟩ := by
  decide

example :
    TamesisLab.Foundations.CycleDetection.detectCycleWitness?
      (id : Bool → Bool) false
      = some ⟨0, 1⟩ := by
  decide

/-! ## As fundações anteriores continuam alcançadas pela mesma raiz -/

#check @TamesisLab.Foundations.FiniteDynamics.exists_bounded_iterate_collision
#check @TamesisLab.Foundations.FunctionalGraphs.exists_component_cycle_with_entry_bound

end TamesisLab.Tests.FoundCycleDetection001UmbrellaAudit
