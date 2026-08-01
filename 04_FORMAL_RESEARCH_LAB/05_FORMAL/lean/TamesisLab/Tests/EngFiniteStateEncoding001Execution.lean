import TamesisLab.Engineering.FiniteStateEncoding

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — testes executáveis

Oito casos, com codificações explícitas. Por `decide` e `rfl`, sem
`native_decide`.

O caso decisivo é `ENC-TEST-006`: sob a codificação permutada os
**números da tabela mudam** e a validade semântica do certificado no
tipo original **não** muda. A coincidência dos witnesses concretos é
observação de teste, e não teorema — ver `ENC-GAP-020`.
-/

namespace TamesisLab.Tests.EngFiniteStateEncoding001Execution

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

/-! ## ENC-TEST-001 — tipo unitário -/

/-- Codificação identidade sobre `Fin 1`. -/
def unitEnc : CertifiedFiniteEncoding (Fin 1) 1 where
  encode := id
  decode := id
  decode_encode := by decide
  encode_decode := by decide

example : (buildTransitionTable unitEnc id).next = #[0] := by decide

example : analyzeEncodedSystem unitEnc id ⟨0, by decide⟩
    = .ok ⟨0, 1⟩ := by decide

/-! ## ENC-TEST-002 e ENC-TEST-003 — `Bool` -/

/-- `false ↔ 0`, `true ↔ 1`. -/
def boolEnc : CertifiedFiniteEncoding Bool 2 where
  encode := fun b => if b then ⟨1, by decide⟩ else ⟨0, by decide⟩
  decode := fun i => decide (i.val = 1)
  decode_encode := by decide
  encode_decode := by decide

example : (buildTransitionTable boolEnc id).next = #[0, 1] := by decide

example : analyzeEncodedSystem boolEnc id false = .ok ⟨0, 1⟩ := by decide
example : analyzeEncodedSystem boolEnc id true = .ok ⟨0, 1⟩ := by decide

example : (buildTransitionTable boolEnc not).next = #[1, 0] := by decide

example : analyzeEncodedSystem boolEnc not false = .ok ⟨0, 2⟩ := by decide
example : analyzeEncodedSystem boolEnc not true = .ok ⟨0, 2⟩ := by decide

/-! ## ENC-TEST-004 — três estados, cauda para ponto fixo -/

/-- `0 → 1 → 2 → 2`. -/
def fixStep : Fin 3 → Fin 3
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | _ => ⟨2, by decide⟩

/-- Codificação identidade sobre `Fin 3`. -/
def idEnc3 : CertifiedFiniteEncoding (Fin 3) 3 where
  encode := id
  decode := id
  decode_encode := by decide
  encode_decode := by decide

example : (buildTransitionTable idEnc3 fixStep).next = #[1, 2, 2] := by decide

example : analyzeEncodedSystem idEnc3 fixStep ⟨0, by decide⟩
    = .ok ⟨2, 1⟩ := by decide

/-! ## ENC-TEST-005 e ENC-TEST-006 — quatro estados, cauda para ciclo de dois -/

/-- `0 → 1 → 2 → 3 → 2`. -/
def tailStep : Fin 4 → Fin 4
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩
  | ⟨2, _⟩ => ⟨3, by decide⟩
  | _ => ⟨2, by decide⟩

/-- Codificação identidade sobre `Fin 4`. -/
def idEnc4 : CertifiedFiniteEncoding (Fin 4) 4 where
  encode := id
  decode := id
  decode_encode := by decide
  encode_decode := by decide

/-- Codificação **permutada**: `i ↦ 3 - i`, involutiva. -/
def permEnc : CertifiedFiniteEncoding (Fin 4) 4 where
  encode := fun i => ⟨3 - i.val, by omega⟩
  decode := fun i => ⟨3 - i.val, by omega⟩
  decode_encode := by decide
  encode_decode := by decide

example : (buildTransitionTable idEnc4 tailStep).next = #[1, 2, 3, 2] := by decide

example : analyzeEncodedSystem idEnc4 tailStep ⟨0, by decide⟩
    = .ok ⟨2, 2⟩ := by decide

example : (buildTransitionTable permEnc tailStep).next = #[1, 0, 1, 2] := by decide

example : analyzeEncodedSystem permEnc tailStep ⟨0, by decide⟩
    = .ok ⟨2, 2⟩ := by decide

/-- O transporte preserva o valor natural, também sob permutação. -/
example : ((permEnc.tableIndex tailStep ⟨0, by decide⟩ :
    Fin (buildTransitionTable permEnc tailStep).next.size) : Nat) = 3 := by decide

/-- A comutação de um passo, instanciada. -/
example : (buildTransitionTable permEnc tailStep).step
      (permEnc.tableIndex tailStep ⟨0, by decide⟩)
    = permEnc.tableIndex tailStep (tailStep ⟨0, by decide⟩) :=
  permEnc.table_step_commutes tailStep ⟨0, by decide⟩

/-- A comutação de iteradas, instanciada em `k = 4`. -/
example : ((buildTransitionTable permEnc tailStep).step)^[4]
      (permEnc.tableIndex tailStep ⟨0, by decide⟩)
    = permEnc.tableIndex tailStep (tailStep^[4] ⟨0, by decide⟩) :=
  permEnc.table_iterate_commutes tailStep 4 ⟨0, by decide⟩

/-! ## ENC-TEST-007 — tipo vazio

A tabela é construída e é vazia. `analyzeEncodedSystem` exige
`start : Empty`, que não existe — a ausência de chamada é garantida pelo
sistema de tipos, e não por uma verificação em tempo de execução. -/

/-- `Empty ↔ Fin 0`. -/
def emptyEnc : CertifiedFiniteEncoding Empty 0 where
  encode := fun s => s.elim
  decode := fun i => absurd i.isLt (Nat.not_lt_zero _)
  decode_encode := fun s => s.elim
  encode_decode := fun i => absurd i.isLt (Nat.not_lt_zero _)

example : (buildTransitionTable emptyEnc (fun s => s.elim)).next = #[] := by decide

/-! ## ENC-TEST-008 — exclusão de erro, concreta -/

example : analyzeEncodedSystem permEnc tailStep ⟨0, by decide⟩
    ≠ .error RuntimeCycleError.internalDetectorFailure :=
  analyzeEncodedSystem_ne_error permEnc tailStep ⟨0, by decide⟩ _

example : analyzeEncodedSystem permEnc tailStep ⟨0, by decide⟩
    ≠ .error RuntimeCycleError.transitionDestinationOutOfBounds :=
  analyzeEncodedSystem_ne_error permEnc tailStep ⟨0, by decide⟩ _

example (err : RuntimeCycleError) :
    analyzeEncodedSystem boolEnc not true ≠ .error err :=
  analyzeEncodedSystem_ne_error boolEnc not true err

/-! ## Interpretação semântica

Os dois exemplos abaixo obtêm o witness concreto por `decide` e
concluem uma igualdade **entre iteradas de `stepS`, no tipo original**.
Nenhuma conclusão menciona `Array` ou `Fin n`.

A codificação permutada produz uma tabela diferente e a mesma conclusão
semântica. Isso é o que a frente prova; a coincidência dos witnesses
concretos, não. -/

example : tailStep^[2 + 2] ⟨0, by decide⟩ = tailStep^[2] ⟨0, by decide⟩ :=
  analyzeEncodedSystem_sound
    (show analyzeEncodedSystem idEnc4 tailStep ⟨0, by decide⟩ = .ok ⟨2, 2⟩ by decide)

example : tailStep^[2 + 2] ⟨0, by decide⟩ = tailStep^[2] ⟨0, by decide⟩ :=
  analyzeEncodedSystem_sound
    (show analyzeEncodedSystem permEnc tailStep ⟨0, by decide⟩ = .ok ⟨2, 2⟩ by decide)

example : not^[0 + 2] true = not^[0] true :=
  analyzeEncodedSystem_sound
    (show analyzeEncodedSystem boolEnc not true = .ok ⟨0, 2⟩ by decide)

end TamesisLab.Tests.EngFiniteStateEncoding001Execution
