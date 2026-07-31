import TamesisLab.Foundations.CycleDetection

set_option autoImplicit false

/-!
# Testes executáveis de FOUND-CYCLE-DETECTION-001

Cinco modelos concretos, avaliados de verdade.

Os valores abaixo são **testes de regressão para a ordem da enumeração**.
**Não** são teoremas de minimalidade: nada aqui afirma que o `baseIndex`
devolvido é o menor possível, nem que o `period` devolvido é o período
mínimo.

Se a ordem de `cycleCandidates` mudar, estes valores mudam — e é
exatamente para detectar isso que os testes existem.
-/

namespace TamesisLab.Tests.FoundCycleDetection001Execution

open TamesisLab.Foundations.CycleDetection

/-! ## TEST-001 — tipo unitário, `a → a` -/

def f1 : Fin 1 → Fin 1 := id

#eval detectCycleWitness? f1 0

example : detectCycleWitness? f1 0 = some ⟨0, 1⟩ := by decide

/-! ## TEST-002 — identidade em `Bool` -/

def fId : Bool → Bool := id

#eval detectCycleWitness? fId false
#eval detectCycleWitness? fId true

example : detectCycleWitness? fId false = some ⟨0, 1⟩ := by decide
example : detectCycleWitness? fId true = some ⟨0, 1⟩ := by decide

/-! ## TEST-003 — alternância em `Bool` -/

def fNot : Bool → Bool := fun b => !b

#eval detectCycleWitness? fNot false
#eval detectCycleWitness? fNot true

example : detectCycleWitness? fNot false = some ⟨0, 2⟩ := by decide
example : detectCycleWitness? fNot true = some ⟨0, 2⟩ := by decide

/-! ## TEST-004 — cauda e ponto fixo, `0 → 1 → 2 → 2` -/

def f3 : Fin 3 → Fin 3
  | 0 => 1
  | 1 => 2
  | 2 => 2

#eval detectCycleWitness? f3 0

example : detectCycleWitness? f3 0 = some ⟨2, 1⟩ := by decide

/-! ## TEST-005 — cauda e ciclo de dois, `0 → 1 → 2 → 3 → 2` -/

def f4 : Fin 4 → Fin 4
  | 0 => 1
  | 1 => 2
  | 2 => 3
  | 3 => 2

#eval detectCycleWitness? f4 0

example : detectCycleWitness? f4 0 = some ⟨2, 2⟩ := by decide

/-! ## TEST-006 — demais estados dos mesmos modelos

O `period` testemunhado coincide dentro do componente; o `baseIndex`
**não** — ele depende do estado inicial. -/

#eval detectCycleWitness? f3 1
#eval detectCycleWitness? f3 2
#eval detectCycleWitness? f4 1
#eval detectCycleWitness? f4 2
#eval detectCycleWitness? f4 3

example : detectCycleWitness? f3 1 = some ⟨1, 1⟩ := by decide
example : detectCycleWitness? f3 2 = some ⟨0, 1⟩ := by decide
example : detectCycleWitness? f4 1 = some ⟨1, 2⟩ := by decide
example : detectCycleWitness? f4 2 = some ⟨0, 2⟩ := by decide
example : detectCycleWitness? f4 3 = some ⟨0, 2⟩ := by decide

/-! ## Enumeração concreta -/

#eval cycleCandidates 0
#eval cycleCandidates 1
#eval cycleCandidates 3
#eval cycleCandidates 4

example : cycleCandidates 0 = [] := rfl
example : cycleCandidates 1 = [⟨0, 1⟩] := rfl

/-! ## O certificado devolvido é válido, e o ponto-base é periódico -/

example : CycleWitness.Valid f4 0 ⟨2, 2⟩ :=
  detectCycleWitness?_sound (by decide : detectCycleWitness? f4 0 = some ⟨2, 2⟩)

example : f4^[2] 0 ∈ Function.periodicPts f4 :=
  CycleWitness.mem_periodicPts
    (detectCycleWitness?_sound (by decide : detectCycleWitness? f4 0 = some ⟨2, 2⟩))

end TamesisLab.Tests.FoundCycleDetection001Execution
