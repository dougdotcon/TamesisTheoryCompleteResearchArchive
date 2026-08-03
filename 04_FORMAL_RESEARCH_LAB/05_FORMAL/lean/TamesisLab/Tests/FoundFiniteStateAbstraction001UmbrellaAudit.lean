import TamesisLab

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — auditoria de cobertura pela raiz

Importa **apenas** `TamesisLab` e alcança as sete declarações públicas da
frente por nome totalmente qualificado. Se qualquer uma deixasse de ser
exportada pela cadeia
`TamesisLab → TamesisLab.Foundations → ...FiniteStateAbstraction`, este
arquivo falharia.

Ele **não** é registrado em `TamesisLab.lean`: importa a raiz, e
registrá-lo criaria ciclo de imports. É executado explicitamente.
-/

namespace TamesisLab.Tests.FoundFiniteStateAbstraction001UmbrellaAudit

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.FiniteStateAbstraction

/-! ## As duas declarações executáveis, pela raiz -/

#check TamesisLab.Foundations.FiniteStateAbstraction.CertifiedFiniteAbstraction
#check TamesisLab.Foundations.FiniteStateAbstraction.analyzeAbstractSystem

/-! ## As cinco declarações de especificação, pela raiz -/

#check TamesisLab.Foundations.FiniteStateAbstraction.CertifiedFiniteAbstraction.iterate_commutes
#check TamesisLab.Foundations.FiniteStateAbstraction.analyzeAbstractSystem_observational_sound
#check TamesisLab.Foundations.FiniteStateAbstraction.OrbitSeparating
#check TamesisLab.Foundations.FiniteStateAbstraction.analyzeAbstractSystem_reflected_sound
#check TamesisLab.Foundations.FiniteStateAbstraction.analyzeAbstractSystem_complete

/-! ## O contraexemplo, pela raiz -/

#check TamesisLab.Foundations.FiniteStateAbstraction.Counterexample.boolToUnit_semiconj
#check TamesisLab.Foundations.FiniteStateAbstraction.Counterexample.boolToUnit_not_orbitSeparating
#check TamesisLab.Foundations.FiniteStateAbstraction.Counterexample.naive_cycle_reflection_is_false

/-! ## As frentes anteriores continuam alcançadas pela mesma raiz -/

#check TamesisLab.Engineering.FiniteStateEncoding.analyzeEncodedSystem_sound
#check TamesisLab.Engineering.FiniteStateEncoding.analyzeEncodedSystem_complete
#check TamesisLab.Engineering.FiniteStateRuntime.analyzeTransitionTable_sound
#check TamesisLab.Foundations.CycleDetection.CycleWitness

/-! ## Cadeia completa, executada pela raiz

Uma abstração genuinamente muitos-para-um: `Fin 4 → Fin 2`, colapsando
pela paridade, sobre um passo que soma um. -/

/-- `i ↦ i + 1` em `Fin 4`. -/
def rotate4 : Fin 4 → Fin 4 := fun i => ⟨(i.val + 1) % 4, by omega⟩

/-- `i ↦ i + 1` em `Fin 2`. -/
def rotate2 : Fin 2 → Fin 2 := fun i => ⟨(i.val + 1) % 2, by omega⟩

/-- A paridade: dois estados concretos por estado abstrato. -/
def parity : Fin 4 → Fin 2 := fun i => ⟨i.val % 2, by omega⟩

/-- A abstração pela paridade comuta com as rotações. -/
def parityAbstraction : CertifiedFiniteAbstraction (Fin 4) (Fin 2) rotate4 rotate2 where
  abstract := parity
  commutes := by
    intro i
    revert i
    decide

/-- Codificação identidade sobre `Fin 2`. -/
def idEnc2 : CertifiedFiniteEncoding (Fin 2) 2 where
  encode := id
  decode := id
  decode_encode := by decide
  encode_decode := by decide

example : analyzeAbstractSystem parityAbstraction idEnc2 ⟨0, by decide⟩ = .ok ⟨0, 2⟩ := by decide

/-- A recorrência **observacional**, pela raiz: as paridades coincidem. -/
example : parity ((rotate4^[0 + 2]) ⟨0, by decide⟩) = parity ((rotate4^[0]) ⟨0, by decide⟩) :=
  analyzeAbstractSystem_observational_sound
    (show analyzeAbstractSystem parityAbstraction idEnc2 ⟨0, by decide⟩ = .ok ⟨0, 2⟩ by decide)

/-- E a recorrência **concreta** falha: `rotate4` só volta em quatro
passos, não em dois. A abstração pela paridade não separa a órbita. -/
example : (rotate4^[0 + 2]) ⟨0, by decide⟩ ≠ (rotate4^[0]) ⟨0, by decide⟩ := by decide

example : ¬ OrbitSeparating parity rotate4 ⟨0, by decide⟩ := by
  intro hsep
  exact absurd (hsep 2 0 (by decide)) (by decide)

end TamesisLab.Tests.FoundFiniteStateAbstraction001UmbrellaAudit
