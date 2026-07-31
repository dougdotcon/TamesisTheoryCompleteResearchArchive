---
document_id: RT-FINAL-VALIDATION-API
frozen: true
---

# API de validação — congelada

## Tabela

```lean
def validateTransitionTable (raw : RawTransitionTable) :
    Except RuntimeCycleError ValidatedTransitionTable :=
  if h : raw.Valid then
    .ok ⟨raw.next, h⟩
  else
    .error .transitionDestinationOutOfBounds
```

Confirmado: array preservado sem alteração, nenhum módulo, nenhum clamp,
nenhum fallback, nenhuma escolha explícita, definição computável.

Pegada axiomática medida: **`[propext, Quot.sound]`** — a validação,
isolada, **não** depende de `Classical.choice`.

```lean
theorem validateTransitionTable_sound
    {raw : RawTransitionTable} {validated : ValidatedTransitionTable}
    (h : validateTransitionTable raw = .ok validated) :
    validated.toRaw = raw ∧ raw.Valid

theorem validateTransitionTable_complete (raw : RawTransitionTable)
    (h : raw.Valid) :
    ∃ validated, validateTransitionTable raw = .ok validated
```

### Auditoria da igualdade dependente

A revisão examinou se a soundness é simples por casos no `if`. **É.** O
`dite` tem exatamente dois ramos; no ramo `.error` a hipótese `h` é
impossível por construtores disjuntos de `Except`, e no ramo `.ok` o valor
devolvido é literalmente `⟨raw.next, _⟩`, cujo `toRaw` é `⟨raw.next⟩`.

A igualdade `validated.toRaw = raw` **não** envolve transporte
dependente: `toRaw` descarta o campo `Prop`, de modo que a comparação é
entre duas `RawTransitionTable`, ambas com o mesmo `next`. É a razão de
`toRaw` existir.

`validateTransitionTable_error_iff` permanece **opcional**.

## Estado inicial

```lean
def validateStart (t : ValidatedTransitionTable) (start : Nat) :
    Except RuntimeCycleError (Fin t.next.size) :=
  if h : start < t.next.size then
    .ok ⟨start, h⟩
  else
    .error (.initialStateOutOfBounds start t.next.size)

theorem validateStart_sound
    {t : ValidatedTransitionTable} {start : Nat}
    {typedStart : Fin t.next.size}
    (h : validateStart t start = .ok typedStart) :
    (typedStart : Nat) = start

theorem validateStart_complete (t : ValidatedTransitionTable) (start : Nat)
    (h : start < t.next.size) :
    ∃ typedStart, validateStart t start = .ok typedStart
```

Confirmado: `validateStart` não altera `start`, não usa módulo, não usa
clamp, não escolhe zero. Pegada: `[propext, Quot.sound]`.

`validateStart_sound` é o **teorema anti-clamp** — se alguma
implementação futura ajustar o índice, esta prova quebra.
