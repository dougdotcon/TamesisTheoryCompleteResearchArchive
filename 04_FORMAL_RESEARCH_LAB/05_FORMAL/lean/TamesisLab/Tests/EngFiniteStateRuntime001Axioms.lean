import TamesisLab.Engineering.FiniteStateRuntime

set_option autoImplicit false

/-!
# Auditoria de axiomas de ENG-FINITE-STATE-RUNTIME-001

Registro vinculante:

```text
A presenca de Classical.choice em #print axioms NAO significa que a
definicao esteja marcada como nao computavel.
```

A expectativa é que a camada de validação e a execução bruta **não**
dependam de escolha, e que a pegada apareça apenas onde o detector entra,
por `Fintype.card`.

Permitidos: `propext`, `Classical.choice`, `Quot.sound`.
Proibidos: `sorryAx` e axiomas locais.
-/

namespace TamesisLab.Tests.EngFiniteStateRuntime001Axioms

open TamesisLab.Engineering.FiniteStateRuntime

/-! ## Camada de validação -/

#print axioms RawTransitionTable.Valid
#print axioms validateTransitionTable
#print axioms validateTransitionTable_sound
#print axioms validateTransitionTable_complete
#print axioms validateStart
#print axioms validateStart_sound
#print axioms validateStart_complete
#print axioms valid_empty

/-! ## Execução bruta e ponte de iterações -/

#print axioms ValidatedTransitionTable.step
#print axioms RawTransitionTable.step?
#print axioms RawTransitionTable.run?
#print axioms ValidatedTransitionTable.step?_eq_some_step
#print axioms ValidatedTransitionTable.run?_eq_iterate_step

/-! ## Camada do detector -/

#print axioms ValidatedTransitionTable.detectCycle?
#print axioms ValidatedTransitionTable.detectCycle?_raw_repeat

/-! ## API dinâmica -/

#print axioms analyzeTransitionTable
#print axioms analyzeTransitionTable_sound
#print axioms analyzeTransitionTable_complete
#print axioms analyzeTransitionTable_invalid_table
#print axioms analyzeTransitionTable_invalid_start
#print axioms analyzeTransitionTable_ne_internalFailure

end TamesisLab.Tests.EngFiniteStateRuntime001Axioms
