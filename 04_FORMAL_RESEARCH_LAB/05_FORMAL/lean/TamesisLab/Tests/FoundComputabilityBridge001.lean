import TamesisLab.Foundations.ComputabilityBridge

set_option autoImplicit false

/-!
# Testes de FOUND-COMPUTABILITY-BRIDGE-001

Sete testes. A instância positiva exigida pela governança, o caso vácuo
que a delimita, e o par que mostra que a conclusão **não depende da
codificação escolhida**.
-/

namespace TamesisLab.Tests.FoundComputabilityBridge001

open TamesisLab.Foundations.ComputabilityBridge
open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.CycleDetection

/-- O tipo da instância positiva é habitado. -/
theorem boolEncoding_nonempty : Nonempty Bool := ⟨true⟩

/-- **A instância positiva.** Não é hipótese assumida satisfazível: é o
valor calculado por avaliação. -/
theorem boolEncoding_analysis_concrete :
    analyzeEncodedSystem boolEncoding not true = .ok ⟨0, 2⟩ := by decide

/-- A cota, exercitada de verdade.

Quantificada sobre `w`, logo **não** decidível por avaliação: este
enunciado falha se `analyzeEncodedSystem_bound` sair do arquivo. A
primeira versão enunciava `0 + 2 ≤ 2` e passaria sem o teorema. -/
theorem boolEncoding_bound_applies :
    ∀ w : CycleWitness, analyzeEncodedSystem boolEncoding not true = .ok w →
      w.baseIndex + w.period ≤ 2 :=
  fun _ h => analyzeEncodedSystem_bound h

/-- `Primrec` sob a instância **induzida pela codificação**. -/
theorem boolEncoding_primrec :
    haveI := encodingPrimcodable boolEncoding
    Primrec (analyzeEncodedSystem boolEncoding not) :=
  primrec_analyzeEncodedSystem boolEncoding not

/-- **A instância induzida não é canônica, e não precisa ser.**

`Primcodable Bool` já existe no Mathlib e é diferente de
`encodingPrimcodable boolEncoding`. Sob a canônica a conclusão é a mesma,
pela mesma linha de prova — porque quem faz o trabalho é a **finitude**,
não a codificação.

Um caso não é uma invariância: afirmá-la está proibido por
`STOP-CB-013`, e fechá-la é `CB-GAP-010`. -/
theorem boolEncoding_primrec_canonical :
    Primrec (analyzeEncodedSystem boolEncoding not) :=
  Primrec.dom_finite _

/-- `Computable` segue de `Primrec`. -/
theorem boolEncoding_computable :
    haveI := encodingPrimcodable boolEncoding
    Computable (analyzeEncodedSystem boolEncoding not) :=
  computable_analyzeEncodedSystem boolEncoding not

/-- O caso vácuo, que delimita a instância positiva. -/
theorem emptyEncoding_isEmpty : IsEmpty Empty :=
  isEmpty_of_encoding_zero emptyEncoding

end TamesisLab.Tests.FoundComputabilityBridge001
