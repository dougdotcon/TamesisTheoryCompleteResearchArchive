import TamesisLab.Engineering.FiniteStateRuntime

set_option autoImplicit false

/-!
# Testes executáveis de ENG-FINITE-STATE-RUNTIME-001

Dez casos, avaliados por `#eval` **e** provados por `decide` ou `rfl`.
Sem `native_decide`.

Os valores de `CycleWitness` são **regressões da ordem do detector**, não
teoremas gerais de minimalidade.
-/

namespace TamesisLab.Tests.EngFiniteStateRuntime001Execution

open TamesisLab.Engineering.FiniteStateRuntime

/-! ## TEST-001 — tabela vazia: válida, mas sem consulta possível -/

#eval (validateTransitionTable ⟨#[]⟩).isOk
#eval analyzeTransitionTable ⟨#[]⟩ 0

example : (validateTransitionTable ⟨#[]⟩).isOk = true := by decide

example : analyzeTransitionTable ⟨#[]⟩ 0
    = .error (.initialStateOutOfBounds 0 0) := by decide

/-! ## TEST-002 — destino inválido vence, mesmo com início inválido -/

#eval analyzeTransitionTable ⟨#[1]⟩ 0
#eval analyzeTransitionTable ⟨#[1]⟩ 100

example : analyzeTransitionTable ⟨#[1]⟩ 0
    = .error .transitionDestinationOutOfBounds := by decide

example : analyzeTransitionTable ⟨#[1]⟩ 100
    = .error .transitionDestinationOutOfBounds := by decide

/-! ## TEST-003 — início inválido -/

#eval analyzeTransitionTable ⟨#[0]⟩ 1

example : analyzeTransitionTable ⟨#[0]⟩ 1
    = .error (.initialStateOutOfBounds 1 1) := by decide

/-! ## TEST-004 — ponto fixo -/

#eval analyzeTransitionTable ⟨#[0]⟩ 0

example : analyzeTransitionTable ⟨#[0]⟩ 0 = .ok ⟨0, 1⟩ := by decide

/-! ## TEST-005 — ciclo de dois -/

#eval analyzeTransitionTable ⟨#[1, 0]⟩ 0

example : analyzeTransitionTable ⟨#[1, 0]⟩ 0 = .ok ⟨0, 2⟩ := by decide

/-! ## TEST-006 — cauda para ponto fixo -/

#eval analyzeTransitionTable ⟨#[1, 2, 2]⟩ 0

example : analyzeTransitionTable ⟨#[1, 2, 2]⟩ 0 = .ok ⟨2, 1⟩ := by decide

/-! ## TEST-007 — cauda para ciclo de dois -/

#eval analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 0

example : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 0 = .ok ⟨2, 2⟩ := by decide

/-! ## TEST-008 — outros estados do mesmo modelo

O `period` testemunhado coincide dentro do componente; o `baseIndex`
**não** — depende do estado inicial. -/

#eval analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 1
#eval analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 2
#eval analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 3

example : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 1 = .ok ⟨1, 2⟩ := by decide
example : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 2 = .ok ⟨0, 2⟩ := by decide
example : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 3 = .ok ⟨0, 2⟩ := by decide

/-! ## TEST-009 — dois componentes na mesma tabela

`0` é ponto fixo; `1` e `2` formam um ciclo de dois. **Não** é
enumeração global de componentes: são três consultas independentes. -/

#eval analyzeTransitionTable ⟨#[0, 2, 1]⟩ 0
#eval analyzeTransitionTable ⟨#[0, 2, 1]⟩ 1
#eval analyzeTransitionTable ⟨#[0, 2, 1]⟩ 2

example : analyzeTransitionTable ⟨#[0, 2, 1]⟩ 0 = .ok ⟨0, 1⟩ := by decide
example : analyzeTransitionTable ⟨#[0, 2, 1]⟩ 1 = .ok ⟨0, 2⟩ := by decide
example : analyzeTransitionTable ⟨#[0, 2, 1]⟩ 2 = .ok ⟨0, 2⟩ := by decide

/-! ## TEST-010 — execução bruta parcial

`run? 0` não valida o estado; `run?` com um passo devolve `none` fora dos
limites. Sem fallback. -/

#eval (RawTransitionTable.mk #[]).run? 0 999
#eval (RawTransitionTable.mk #[]).run? 1 999
#eval (RawTransitionTable.mk #[1, 2, 3, 2]).run? 4 0

example : (RawTransitionTable.mk #[]).run? 0 999 = some 999 := rfl
example : (RawTransitionTable.mk #[]).run? 1 999 = none := rfl
example : (RawTransitionTable.mk #[1, 2, 3, 2]).run? 4 0 = some 2 := rfl

/-! ## Encadeamento: certificado computado, interpretado sobre o array -/

example :
    (RawTransitionTable.mk #[1, 2, 3, 2]).run? (2 + 2) 0 =
      (RawTransitionTable.mk #[1, 2, 3, 2]).run? 2 0 :=
  (analyzeTransitionTable_sound
    (by decide : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 0 = .ok ⟨2, 2⟩)).2.2

example : (⟨#[1, 2, 3, 2]⟩ : RawTransitionTable).Valid := by decide

example : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 0
    ≠ .error .internalDetectorFailure :=
  analyzeTransitionTable_ne_internalFailure ⟨#[1, 2, 3, 2]⟩ 0
    (by decide) (by decide)

end TamesisLab.Tests.EngFiniteStateRuntime001Execution
