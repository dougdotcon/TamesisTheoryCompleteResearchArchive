import TamesisLab.Engineering.FiniteStateRuntime

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-RUNTIME-001 — auditoria de assinaturas

Somente `#check`. Nenhuma definição, nenhum teorema.

O que esta auditoria torna visível:

```text
camada bruta e validacao   nenhuma typeclass do chamador
step, step?, run?          nenhuma typeclass do chamador
detectCycle?               Fintype e DecidableEq de Fin n, INFERIDAS
analyzeTransitionTable     assinatura sem typeclass alguma
```
-/

namespace TamesisLab.Engineering.FiniteStateRuntime

#check @RawTransitionTable
#check @RawTransitionTable.next
#check @RawTransitionTable.Valid
#check @RawTransitionTable.decidableValid

#check @ValidatedTransitionTable
#check @ValidatedTransitionTable.closed
#check @ValidatedTransitionTable.toRaw
#check @ValidatedTransitionTable.toRaw_valid

#check @RuntimeCycleError

#check @validateTransitionTable
#check @validateTransitionTable_sound
#check @validateTransitionTable_complete
#check @valid_empty

#check @validateStart
#check @validateStart_sound
#check @validateStart_complete

#check @ValidatedTransitionTable.step
#check @ValidatedTransitionTable.step_val
#check @RawTransitionTable.step?
#check @RawTransitionTable.run?
#check @ValidatedTransitionTable.step?_eq_some_step
#check @ValidatedTransitionTable.run?_eq_iterate_step

#check @ValidatedTransitionTable.detectCycle?
#check @ValidatedTransitionTable.detectCycle?_sound
#check @ValidatedTransitionTable.detectCycle?_complete
#check @ValidatedTransitionTable.detectCycle?_raw_repeat

#check @analyzeTransitionTable
#check @analyzeTransitionTable_sound
#check @analyzeTransitionTable_complete
#check @analyzeTransitionTable_invalid_table
#check @analyzeTransitionTable_invalid_start
#check @analyzeTransitionTable_ne_internalFailure

-- reutilizados, nao reimplementados
#check @TamesisLab.Foundations.CycleDetection.detectCycleWitness?
#check @TamesisLab.Foundations.CycleDetection.detectCycleWitness?_sound
#check @TamesisLab.Foundations.CycleDetection.detectCycleWitness?_complete

end TamesisLab.Engineering.FiniteStateRuntime
