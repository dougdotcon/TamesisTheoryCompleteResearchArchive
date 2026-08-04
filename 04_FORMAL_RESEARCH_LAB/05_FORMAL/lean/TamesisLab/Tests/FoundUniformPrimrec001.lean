import TamesisLab.Foundations.UniformPrimrec

set_option autoImplicit false

/-!
# Testes de FOUND-UNIFORM-PRIMREC-001

Instancia positiva **por avaliacao**: os dois lados do casamento sao
calculados e coincidem.
-/

namespace TamesisLab.Tests.FoundUniformPrimrec001

open TamesisLab.Foundations.UniformPrimrec
open TamesisLab.Engineering.FiniteStateRuntime

/-- A tabela de dois estados e valida. -/
theorem twoCycle_valid : twoCycle.Valid := by decide

/-- A funcao do laboratorio, avaliada. -/
theorem twoCycle_analysis :
    analyzeTransitionTable twoCycle 0 = .ok ⟨0, 2⟩ := by decide

/-- A reformulacao nao dependente, avaliada. **O mesmo valor.** -/
theorem twoCycle_analyzeRaw : analyzeRaw twoCycle 0 = .ok ⟨0, 2⟩ := by decide

end TamesisLab.Tests.FoundUniformPrimrec001
