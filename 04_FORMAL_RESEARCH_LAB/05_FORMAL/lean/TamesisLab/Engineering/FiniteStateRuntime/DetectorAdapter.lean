import TamesisLab.Engineering.FiniteStateRuntime.Execution
import TamesisLab.Foundations.CycleDetection

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-RUNTIME-001 — Adaptador do detector

Uma linha de definição e três teoremas, todos por **reutilização**.

O detector de `FOUND-CYCLE-DETECTION-001` é consumido como caixa-preta:
sua enumeração, sua busca e a casa dos pombos que ele herda **não** são
repetidas aqui. As instâncias de finitude e igualdade decidível de
`Fin n` são inferidas — o chamador não fornece nenhuma.
-/

namespace TamesisLab.Engineering.FiniteStateRuntime

open TamesisLab.Foundations.CycleDetection

/-- O detector certificado, aplicado à função tipada da tabela. -/
def ValidatedTransitionTable.detectCycle? (t : ValidatedTransitionTable)
    (start : Fin t.next.size) : Option CycleWitness :=
  detectCycleWitness? t.step start

/-- O certificado devolvido satisfaz o contrato — herdado diretamente. -/
theorem ValidatedTransitionTable.detectCycle?_sound
    {t : ValidatedTransitionTable} {start : Fin t.next.size}
    {w : CycleWitness} (h : t.detectCycle? start = some w) :
    CycleWitness.Valid t.step start w :=
  detectCycleWitness?_sound h

/-- Algum certificado é sempre devolvido — herdado diretamente. -/
theorem ValidatedTransitionTable.detectCycle?_complete
    (t : ValidatedTransitionTable) (start : Fin t.next.size) :
    ∃ w, t.detectCycle? start = some w :=
  detectCycleWitness?_complete t.step start

/-- **O certificado, reinterpretado sobre a tabela original.**

Executar `baseIndex + period` passos e executar `baseIndex` passos levam
ao mesmo estado — afirmação sobre o `Array` que o chamador entregou, não
sobre um objeto interno.

Nada é afirmado sobre minimalidade. -/
theorem ValidatedTransitionTable.detectCycle?_raw_repeat
    {t : ValidatedTransitionTable} {start : Fin t.next.size}
    {w : CycleWitness} (h : t.detectCycle? start = some w) :
    t.toRaw.run? (w.baseIndex + w.period) (start : Nat) =
      t.toRaw.run? w.baseIndex (start : Nat) := by
  have hw : CycleWitness.Valid t.step start w := t.detectCycle?_sound h
  rw [t.run?_eq_iterate_step (w.baseIndex + w.period) start,
    t.run?_eq_iterate_step w.baseIndex start, hw.2.2.2]

end TamesisLab.Engineering.FiniteStateRuntime
