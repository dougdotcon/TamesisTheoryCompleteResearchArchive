import TamesisLab.Engineering.FiniteStateRuntime.RawTable

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-RUNTIME-001 — Validação

Duas validações **separadas**, com erros distintos:

```text
validateTransitionTable   valida o DADO
validateStart             valida a CONSULTA
```

Colapsá-las num único booleano destruiria a informação mais útil para
quem chama: **qual** validação falhou.

A proibição central desta frente vive aqui: destinos inválidos são
**rejeitados**, nunca corrigidos. Um ajuste silencioso de índice
transformaria uma tabela errada em um sistema diferente, e o certificado
devolvido seria correto sobre um sistema que o usuário nunca descreveu.

A lista completa de proibições literais está em
`ENG_FINITE_STATE_RUNTIME_001/COMPUTABILITY_RESULT.md`, fora dos arquivos
Lean, para que a auditoria de tokens possa exigir contagem zero.
-/

namespace TamesisLab.Engineering.FiniteStateRuntime

/-- Erros da camada dinâmica.

`transitionDestinationOutOfBounds` é genérico na v1: localizar o primeiro
destino inválido exigiria uma segunda busca e uma prova adicional, sem
afetar segurança nem correção.

`internalDetectorFailure` é **defesa operacional**; ele é
proposicionalmente impossível para entradas válidas, e existe um teorema
que o demonstra. -/
inductive RuntimeCycleError
  | transitionDestinationOutOfBounds
  | initialStateOutOfBounds (start : Nat) (stateCount : Nat)
  | internalDetectorFailure
deriving DecidableEq, Repr, BEq

/-- Valida a tabela, sem tocar no array.

O ramo positivo devolve a tabela validada com a própria hipótese como
campo `closed`. O ramo negativo devolve erro — jamais um valor
corrigido. -/
def validateTransitionTable (raw : RawTransitionTable) :
    Except RuntimeCycleError ValidatedTransitionTable :=
  if h : raw.Valid then
    .ok ⟨raw.next, h⟩
  else
    .error .transitionDestinationOutOfBounds

/-- Se a validação aceita, a tabela devolvida é a original e ela é válida.

A igualdade não envolve transporte dependente: `toRaw` descarta o campo
proposicional, de modo que a comparação é entre duas tabelas brutas com o
mesmo array. -/
theorem validateTransitionTable_sound {raw : RawTransitionTable}
    {validated : ValidatedTransitionTable}
    (h : validateTransitionTable raw = .ok validated) :
    validated.toRaw = raw ∧ raw.Valid := by
  unfold validateTransitionTable at h
  by_cases hv : raw.Valid
  · rw [dif_pos hv] at h
    have : validated = ⟨raw.next, hv⟩ := by
      exact (Except.ok.inj h).symm
    subst this
    exact ⟨rfl, hv⟩
  · rw [dif_neg hv] at h
    exact absurd h (by simp)

/-- Se a tabela é válida, a validação aceita. -/
theorem validateTransitionTable_complete (raw : RawTransitionTable)
    (h : raw.Valid) :
    ∃ validated, validateTransitionTable raw = .ok validated :=
  ⟨⟨raw.next, h⟩, dif_pos h⟩

/-- Valida a consulta, preservando `start` **exatamente**.

Nenhum módulo, nenhum clamp, nenhum zero padrão. Com `next.size = 0`
nenhum `start` passa, e o erro sai naturalmente — sem hipótese extra de
tabela não vazia. -/
def validateStart (t : ValidatedTransitionTable) (start : Nat) :
    Except RuntimeCycleError (Fin t.next.size) :=
  if h : start < t.next.size then
    .ok ⟨start, h⟩
  else
    .error (.initialStateOutOfBounds start t.next.size)

/-- O índice tipado devolvido tem exatamente o valor pedido.

Este é o teorema **anti-clamp**: qualquer ajuste silencioso do índice o
quebraria. -/
theorem validateStart_sound {t : ValidatedTransitionTable} {start : Nat}
    {typedStart : Fin t.next.size}
    (h : validateStart t start = .ok typedStart) :
    (typedStart : Nat) = start := by
  unfold validateStart at h
  by_cases hs : start < t.next.size
  · rw [dif_pos hs] at h
    have : typedStart = ⟨start, hs⟩ := (Except.ok.inj h).symm
    subst this
    rfl
  · rw [dif_neg hs] at h
    exact absurd h (by simp)

/-- Se o índice está no domínio, a validação da consulta aceita. -/
theorem validateStart_complete (t : ValidatedTransitionTable) (start : Nat)
    (h : start < t.next.size) :
    ∃ typedStart, validateStart t start = .ok typedStart :=
  ⟨⟨start, h⟩, dif_pos h⟩

/-- A tabela vazia é **estruturalmente válida**, por vacuidade. -/
theorem valid_empty : RawTransitionTable.Valid ⟨#[]⟩ := by
  intro i
  exact absurd i.isLt (by simp)

end TamesisLab.Engineering.FiniteStateRuntime
