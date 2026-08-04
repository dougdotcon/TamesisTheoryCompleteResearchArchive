import TamesisLab.Foundations.FiniteStateAbstraction.AbstractAnalysis

set_option autoImplicit false

/-!
# FOUND-MONOVARIANT-DESCENT-001 — a cláusula recuperada

`CycleWitness.Valid` garante `0 < period`, e
`ValidatedTransitionTable.detectCycle?_sound` entrega esse contrato
inteiro. Mas `analyzeTransitionTable_sound` devolve apenas três
cláusulas, e **a positividade se perde ali**, antes de chegar a
`analyzeEncodedSystem_sound` e a `analyzeAbstractSystem`.

Este módulo a recupera, **sem tocar em nenhuma frente encerrada**: a
redução do bloco `do` é reproduzida aqui a partir de API exclusivamente
pública.

A linha vale a pena ficar escrita. Reproduzir uma redução curta a partir
de API pública é permitido; reimplementar o detector, ou a casa dos
pombos, não é — e nada disso é feito aqui.
-/

namespace TamesisLab.Foundations.Monovariants

open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.FiniteStateAbstraction
open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime

variable {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}

/-- Redução do bloco `do` quando as duas validações passam.

Auxiliar **privado**. Reproduz, com API pública, o que a frente do
runtime mantém privado. -/
private theorem analyze_reduce_public {raw : RawTransitionTable} (hRaw : raw.Valid)
    {start : Nat} (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start =
      (match ValidatedTransitionTable.detectCycle?
          (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
        | some witness => .ok witness
        | none => .error .internalDetectorFailure) := by
  unfold analyzeTransitionTable
  rw [show validateTransitionTable raw = .ok ⟨raw.next, hRaw⟩ from dif_pos hRaw]
  show (validateStart ⟨raw.next, hRaw⟩ start).bind _ = _
  rw [show validateStart ⟨raw.next, hRaw⟩ start = .ok ⟨start, hStart⟩
      from dif_pos hStart]
  rfl

/-- **A positividade, recuperada no nível da tabela.** -/
theorem analyzeTransitionTable_period_pos {raw : RawTransitionTable} {start : Nat}
    {w : CycleWitness} (h : analyzeTransitionTable raw start = .ok w) :
    0 < w.period := by
  obtain ⟨hRaw, hStart, -⟩ := analyzeTransitionTable_sound h
  rw [analyze_reduce_public hRaw hStart] at h
  cases hd : ValidatedTransitionTable.detectCycle?
      (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
  | none => rw [hd] at h; exact absurd h (by simp)
  | some w' =>
      rw [hd] at h
      have hww : w' = w := Except.ok.inj h
      subst hww
      exact (ValidatedTransitionTable.detectCycle?_sound hd).2.1

/-- **A positividade, no nível da análise abstrata.**

É o que torna o teorema negativo desta frente livre de hipótese que o
consumidor precise inventar. -/
theorem analyzeAbstractSystem_period_pos
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C} {witness : CycleWitness}
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    0 < witness.period :=
  analyzeTransitionTable_period_pos h

end TamesisLab.Foundations.Monovariants
