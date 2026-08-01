import TamesisLab

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — auditoria de cobertura pelo agregador raiz

Importa **apenas** `TamesisLab` e alcança as quinze declarações públicas da
frente por nome totalmente qualificado. Se qualquer uma deixasse de ser
exportada pela cadeia
`TamesisLab → TamesisLab.Engineering → ...FiniteStateEncoding`, este
arquivo falharia.

Ele **não** é registrado em `TamesisLab.lean`: importa a raiz, e
registrá-lo criaria ciclo de imports. É executado explicitamente.
-/

namespace TamesisLab.Tests.EngFiniteStateEncoding001UmbrellaAudit

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

/-! ## As quinze declarações públicas, pela raiz -/

#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding
#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.encodedStep
#check TamesisLab.Engineering.FiniteStateEncoding.buildTransitionTable
#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.tableIndex
#check TamesisLab.Engineering.FiniteStateEncoding.analyzeEncodedSystem

#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.encode_injective
#check TamesisLab.Engineering.FiniteStateEncoding.buildTransitionTable_size
#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.tableIndex_val
#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.tableIndex_semiconj
#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.table_iterate_commutes
#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
#check TamesisLab.Engineering.FiniteStateEncoding.analyzeEncodedSystem_sound
#check TamesisLab.Engineering.FiniteStateEncoding.analyzeEncodedSystem_complete

#check TamesisLab.Engineering.FiniteStateEncoding.CertifiedFiniteEncoding.table_step_commutes
#check TamesisLab.Engineering.FiniteStateEncoding.analyzeEncodedSystem_ne_error

/-! ## As frentes anteriores continuam alcançadas pela mesma raiz -/

#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_sound
#check TamesisLab.Engineering.FiniteStateRuntime.ValidatedTransitionTable.run?_eq_iterate_step
#check TamesisLab.Foundations.CycleDetection.CycleWitness

/-! ## Exemplo executável, pela raiz -/

/-- `Bool` com negação, codificação `false ↔ 0`, `true ↔ 1`. -/
def boolEnc : CertifiedFiniteEncoding Bool 2 where
  encode := fun b => if b then ⟨1, by decide⟩ else ⟨0, by decide⟩
  decode := fun i => decide (i.val = 1)
  decode_encode := by decide
  encode_decode := by decide

example : (buildTransitionTable boolEnc not).next = #[1, 0] := by decide

example : analyzeEncodedSystem boolEnc not true = .ok ⟨0, 2⟩ := by decide

/-- A conclusão semântica, no tipo original, alcançada pela raiz. -/
example : not^[0 + 2] true = not^[0] true :=
  analyzeEncodedSystem_sound
    (show analyzeEncodedSystem boolEnc not true = .ok ⟨0, 2⟩ by decide)

end TamesisLab.Tests.EngFiniteStateEncoding001UmbrellaAudit
