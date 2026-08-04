import TamesisLab.Engineering.FiniteStateRuntime.DetectorAdapter

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-RUNTIME-001 — API dinâmica

```lean
analyzeTransitionTable : RawTransitionTable → Nat →
    Except RuntimeCycleError CycleWitness
```

O consumidor fornece um `Array Nat` e um `Nat`. **Nada mais.** Sem
finitude, sem igualdade decidível, sem `Fin`, sem provas, sem funções
Lean — as estruturas finitas são construídas internamente.

Precedência vinculante dos erros, garantida pela ordem do `do`:

```text
1. tabela invalida
2. estado inicial invalido
3. falha interna impossivel
4. sucesso
```

O ramo `internalDetectorFailure` permanece na função executável, e um
teorema demonstra que ele é inalcançável sob as pré-condições formais.
Provar que um ramo é impossível é diferente de eliminá-lo — e é a
diferença entre documentar uma impossibilidade e totalizar uma função.
-/

namespace TamesisLab.Engineering.FiniteStateRuntime

open TamesisLab.Foundations.CycleDetection

/-- Analisa uma tabela recebida em tempo de execução. -/
def analyzeTransitionTable (raw : RawTransitionTable) (start : Nat) :
    Except RuntimeCycleError CycleWitness := do
  let validated ← validateTransitionTable raw
  let typedStart ← validateStart validated start
  match validated.detectCycle? typedStart with
  | some witness => .ok witness
  | none => .error .internalDetectorFailure

/-- Redução da análise quando ambas as validações passam.

Isola, de uma vez, as duas reduções que o `do` esconde, e é o que torna
soundness e completeness curtas.

**Pública desde ENG-RUNTIME-SOUNDNESS-002.** Enquanto era privada, quatro
frentes distintas reproduziram esta mesma redução em auxiliares próprios.
Publicá-la é o que elimina as quatro cópias. -/
theorem analyzeTransitionTable_reduce {raw : RawTransitionTable} (hRaw : raw.Valid)
    {start : Nat} (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start =
      (match ValidatedTransitionTable.detectCycle?
          ⟨raw.next, hRaw⟩ ⟨start, hStart⟩ with
        | some witness => .ok witness
        | none => .error .internalDetectorFailure) := by
  unfold analyzeTransitionTable
  rw [show validateTransitionTable raw = .ok ⟨raw.next, hRaw⟩ from dif_pos hRaw]
  show (validateStart ⟨raw.next, hRaw⟩ start).bind _ = _
  rw [show validateStart ⟨raw.next, hRaw⟩ start = .ok ⟨start, hStart⟩
      from dif_pos hStart]
  rfl

/-- Tabela inválida vence qualquer outro erro. -/
theorem analyzeTransitionTable_invalid_table (raw : RawTransitionTable)
    (start : Nat) (h : ¬raw.Valid) :
    analyzeTransitionTable raw start =
      .error .transitionDestinationOutOfBounds := by
  unfold analyzeTransitionTable
  rw [show validateTransitionTable raw
      = .error .transitionDestinationOutOfBounds from dif_neg h]
  rfl

/-- Com a tabela válida, o índice fora do domínio produz o erro de
consulta — com o valor pedido e a cardinalidade, sem correção. -/
theorem analyzeTransitionTable_invalid_start (raw : RawTransitionTable)
    (start : Nat) (hRaw : raw.Valid) (hStart : ¬start < raw.next.size) :
    analyzeTransitionTable raw start =
      .error (.initialStateOutOfBounds start raw.next.size) := by
  unfold analyzeTransitionTable
  rw [show validateTransitionTable raw = .ok ⟨raw.next, hRaw⟩ from dif_pos hRaw]
  show (validateStart ⟨raw.next, hRaw⟩ start).bind _ = _
  rw [show validateStart ⟨raw.next, hRaw⟩ start
      = .error (.initialStateOutOfBounds start raw.next.size)
      from dif_neg hStart]
  rfl

/-- **Correção da análise.**

Se a análise devolve um certificado, então a tabela era válida, o índice
estava no domínio, e a repetição vale **sobre o array original**.

Nada é afirmado sobre minimalidade. -/
theorem analyzeTransitionTable_sound {raw : RawTransitionTable} {start : Nat}
    {w : CycleWitness} (h : analyzeTransitionTable raw start = .ok w) :
    raw.Valid ∧
    start < raw.next.size ∧
    raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start := by
  by_cases hRaw : raw.Valid
  · by_cases hStart : start < raw.next.size
    · rw [analyzeTransitionTable_reduce hRaw hStart] at h
      cases hd : ValidatedTransitionTable.detectCycle?
          (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
      | none => rw [hd] at h; exact absurd h (by simp)
      | some w' =>
          rw [hd] at h
          have hww : w' = w := Except.ok.inj h
          subst hww
          exact ⟨hRaw, hStart,
            ValidatedTransitionTable.detectCycle?_raw_repeat hd⟩
    · rw [analyzeTransitionTable_invalid_start raw start hRaw hStart] at h
      exact absurd h (by simp)
  · rw [analyzeTransitionTable_invalid_table raw start hRaw] at h
    exact absurd h (by simp)

/-- **Soundness alargada: o contrato inteiro.**

`analyzeTransitionTable_sound` devolve três cláusulas e perde o resto de
`CycleWitness.Valid`. Esta devolve as quatro, sobre a tabela bruta.

A cláusula `w.baseIndex < raw.next.size` nunca havia sido exposta a
consumidor algum — sai de graça junto com as outras.

`analyzeTransitionTable_sound` **permanece**: alargar não é substituir. -/
theorem analyzeTransitionTable_rawValid {raw : RawTransitionTable} {start : Nat}
    {w : CycleWitness} (h : analyzeTransitionTable raw start = .ok w) :
    w.baseIndex < raw.next.size ∧ 0 < w.period ∧
      w.baseIndex + w.period ≤ raw.next.size ∧
        raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start := by
  obtain ⟨hRaw, hStart, hrun⟩ := analyzeTransitionTable_sound h
  rw [analyzeTransitionTable_reduce hRaw hStart] at h
  cases hd : ValidatedTransitionTable.detectCycle?
      (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
  | none => rw [hd] at h; exact absurd h (by simp)
  | some w' =>
      rw [hd] at h
      have hww : w' = w := Except.ok.inj h
      subst hww
      have hv := ValidatedTransitionTable.detectCycle?_sound hd
      exact ⟨by simpa using hv.1, hv.2.1, by simpa using hv.2.2.1, hrun⟩

/-- **Completude da análise.**

Para toda tabela válida e todo índice no domínio, a análise devolve um
certificado. O ramo `none` do detector nunca é alcançado. -/
theorem analyzeTransitionTable_complete (raw : RawTransitionTable)
    (start : Nat) (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    ∃ w, analyzeTransitionTable raw start = .ok w := by
  obtain ⟨w, hw⟩ :=
    ValidatedTransitionTable.detectCycle?_complete
      (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩
  refine ⟨w, ?_⟩
  rw [analyzeTransitionTable_reduce hRaw hStart, hw]

/-- O ramo defensivo é **inalcançável** sob as pré-condições formais.

O construtor permanece na função executável; o que se demonstra é que ele
nunca ocorre para entradas válidas. -/
theorem analyzeTransitionTable_ne_internalFailure (raw : RawTransitionTable)
    (start : Nat) (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure := by
  intro hFailure
  obtain ⟨w, hw⟩ := analyzeTransitionTable_complete raw start hRaw hStart
  rw [hw] at hFailure
  exact absurd hFailure (by simp)

end TamesisLab.Engineering.FiniteStateRuntime
