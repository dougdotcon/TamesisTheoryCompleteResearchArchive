import TamesisLab

set_option autoImplicit false

/-!
# Auditoria de cobertura do agregador raiz — ENG-FINITE-STATE-RUNTIME-001

Importa **apenas** `TamesisLab` e referencia a frente por nome totalmente
qualificado. Falha se a trilha de engenharia deixar de ser alcançada pelo
agregador raiz.

Não é registrado em `TamesisLab.lean`: ele importa a raiz, e registrá-lo
criaria um ciclo. É executado explicitamente.
-/

namespace TamesisLab.Tests.EngFiniteStateRuntime001UmbrellaAudit

#check TamesisLab.Engineering.FiniteStateRuntime.RawTransitionTable
#check TamesisLab.Engineering.FiniteStateRuntime.RawTransitionTable.Valid
#check TamesisLab.Engineering.FiniteStateRuntime.RawTransitionTable.decidableValid
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.toRaw
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.toRaw_valid
#check TamesisLab.Engineering.FiniteStateRuntime.RuntimeCycleError
#check TamesisLab.Engineering.FiniteStateRuntime.validateTransitionTable
#check TamesisLab.Engineering.FiniteStateRuntime.validateTransitionTable_sound
#check TamesisLab.Engineering.FiniteStateRuntime.validateTransitionTable_complete
#check TamesisLab.Engineering.FiniteStateRuntime.validateStart
#check TamesisLab.Engineering.FiniteStateRuntime.validateStart_sound
#check TamesisLab.Engineering.FiniteStateRuntime.validateStart_complete
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.step
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.step_val
#check TamesisLab.Engineering.FiniteStateRuntime.RawTransitionTable.step?
#check TamesisLab.Engineering.FiniteStateRuntime.RawTransitionTable.run?
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.step?_eq_some_step
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.run?_eq_iterate_step
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.detectCycle?
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.detectCycle?_sound
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.detectCycle?_complete
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.detectCycle?_raw_repeat
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_sound
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_complete
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_invalid_table
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_invalid_start
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_ne_internalFailure

/-! ## Exemplo executável alcançado pela raiz -/

#eval TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable
  ⟨#[1, 2, 3, 2]⟩ 0

example :
    TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable
      ⟨#[1, 2, 3, 2]⟩ 0 = .ok ⟨2, 2⟩ := by
  decide

example :
    TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable
      ⟨#[1]⟩ 100
      = .error .transitionDestinationOutOfBounds := by
  decide

/-! ## As quatro fundações anteriores continuam alcançadas pela mesma raiz -/

#check @TamesisLab.Foundations.FiniteDynamics.exists_bounded_iterate_collision
#check @TamesisLab.Foundations.FunctionalGraphs.exists_component_cycle_with_entry_bound
#check @TamesisLab.Foundations.CycleDetection.detectCycleWitness?
#check @TamesisLab.Foundations.CycleDetection.detectCycleWitness?_complete

end TamesisLab.Tests.EngFiniteStateRuntime001UmbrellaAudit
