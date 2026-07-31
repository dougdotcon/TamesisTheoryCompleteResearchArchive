import TamesisLab.Engineering.FiniteStateRuntime

set_option autoImplicit false

/-!
# Teste da API formal de ENG-FINITE-STATE-RUNTIME-001

Verifica as assinaturas públicas e, sobretudo, que a API dinâmica
**não exige typeclass alguma do consumidor**.
-/

namespace TamesisLab.Tests.EngFiniteStateRuntime001

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

#check @RawTransitionTable
#check @RawTransitionTable.Valid
#check @RawTransitionTable.decidableValid
#check @ValidatedTransitionTable
#check @ValidatedTransitionTable.toRaw
#check @ValidatedTransitionTable.toRaw_valid
#check @RuntimeCycleError
#check @validateTransitionTable
#check @validateTransitionTable_sound
#check @validateTransitionTable_complete
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

/-! ## O consumidor fornece apenas `Array Nat` e `Nat` -/

example (next : Array Nat) (start : Nat) :
    Except RuntimeCycleError CycleWitness :=
  analyzeTransitionTable ⟨next⟩ start

/-! ## A instância decidível resolve -/

#synth Decidable (RawTransitionTable.Valid ⟨#[]⟩)
#synth Decidable (RawTransitionTable.Valid ⟨#[0]⟩)
#synth Decidable (RawTransitionTable.Valid ⟨#[1]⟩)

example (t : RawTransitionTable) : Decidable t.Valid := inferInstance

/-! ## As camadas proposicionais não exigem typeclass -/

example (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    (t.step i : Nat) = t.next[i] :=
  t.step_val i

example (t : ValidatedTransitionTable) (k : Nat) (start : Fin t.next.size) :
    t.toRaw.run? k (start : Nat) =
      some (((t.step)^[k] start : Fin t.next.size) : Nat) :=
  t.run?_eq_iterate_step k start

/-! ## Encadeamento completo, do array ao certificado -/

example (next : Array Nat) (start : Nat) (w : CycleWitness)
    (h : analyzeTransitionTable ⟨next⟩ start = .ok w) :
    (⟨next⟩ : RawTransitionTable).run? (w.baseIndex + w.period) start =
      (⟨next⟩ : RawTransitionTable).run? w.baseIndex start :=
  (analyzeTransitionTable_sound h).2.2

example (next : Array Nat) (start : Nat)
    (hRaw : (⟨next⟩ : RawTransitionTable).Valid)
    (hStart : start < next.size) :
    ∃ w, analyzeTransitionTable ⟨next⟩ start = .ok w :=
  analyzeTransitionTable_complete ⟨next⟩ start hRaw hStart

end TamesisLab.Tests.EngFiniteStateRuntime001
