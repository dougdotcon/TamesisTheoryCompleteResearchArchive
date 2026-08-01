import TamesisLab.Engineering.FiniteStateEncoding

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — teste formal

`#check` de todas as declarações públicas, mais a confirmação, por
exemplo genérico, de que **nenhuma** delas exige typeclass sobre `S`.

O auxiliar privado de leitura não é alcançável daqui — e é assim que se
verifica que ele é mesmo interno.
-/

namespace TamesisLab.Tests.EngFiniteStateEncoding001

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

#check @CertifiedFiniteEncoding
#check @CertifiedFiniteEncoding.encode_injective
#check @CertifiedFiniteEncoding.encodedStep
#check @buildTransitionTable
#check @buildTransitionTable_size
#check @CertifiedFiniteEncoding.tableIndex
#check @CertifiedFiniteEncoding.tableIndex_val
#check @CertifiedFiniteEncoding.tableIndex_semiconj
#check @CertifiedFiniteEncoding.table_step_commutes
#check @CertifiedFiniteEncoding.table_iterate_commutes
#check @CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
#check @analyzeEncodedSystem
#check @analyzeEncodedSystem_sound
#check @analyzeEncodedSystem_complete
#check @analyzeEncodedSystem_ne_error

/-! ## Nenhuma typeclass sobre `S`

Cada exemplo abaixo é genérico em `S` e `n`, **sem** `Fintype`,
`DecidableEq`, `Nonempty` ou `Inhabited`. Se qualquer uma delas fosse
exigida, a elaboração falharia por instância ausente. -/

example {S : Type} {n : Nat} (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) : ValidatedTransitionTable :=
  buildTransitionTable encoding stepS

example {S : Type} {n : Nat} (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (s : S) : Fin (buildTransitionTable encoding stepS).next.size :=
  encoding.tableIndex stepS s

example {S : Type} {n : Nat} (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) : Except RuntimeCycleError CycleWitness :=
  analyzeEncodedSystem encoding stepS start

example {S : Type} {n : Nat} (encoding : CertifiedFiniteEncoding S n) :
    Function.Injective encoding.encode :=
  encoding.encode_injective

example {S : Type} {n : Nat} (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) :
    Function.Semiconj (encoding.tableIndex stepS) stepS
      (buildTransitionTable encoding stepS).step :=
  encoding.tableIndex_semiconj stepS

example {S : Type} {n : Nat} (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (start : S) :
    ∃ witness, analyzeEncodedSystem encoding stepS start = .ok witness :=
  analyzeEncodedSystem_complete encoding stepS start

/-! ## A soundness é enunciada no tipo de estados -/

example {S : Type} {n : Nat} {encoding : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {witness : CycleWitness}
    (h : analyzeEncodedSystem encoding stepS start = .ok witness) :
    stepS^[witness.baseIndex + witness.period] start = stepS^[witness.baseIndex] start :=
  analyzeEncodedSystem_sound h

end TamesisLab.Tests.EngFiniteStateEncoding001
