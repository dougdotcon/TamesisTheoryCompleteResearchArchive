---
document_id: RT-FINAL-ERROR-MODEL
frozen: true
---

# Modelo de erros e precedência — congelado

## API dinâmica

```lean
def analyzeTransitionTable (raw : RawTransitionTable) (start : Nat) :
    Except RuntimeCycleError CycleWitness := do
  let validated ← validateTransitionTable raw
  let typedStart ← validateStart validated start
  match validated.detectCycle? typedStart with
  | some witness => .ok witness
  | none => .error .internalDetectorFailure
```

## Precedência vinculante

```text
1. tabela invalida
2. estado inicial invalido
3. falha interna impossivel
4. sucesso
```

Medida no probe, com o teste decisivo exigido pelo gate:

```text
analyzeT ⟨#[1]⟩ 0     ->  transitionDestinationOutOfBounds
analyzeT ⟨#[1]⟩ 100   ->  transitionDestinationOutOfBounds
```

No segundo caso a tabela é inválida **e** o início é inválido. O erro de
**tabela** vence. A ordem do `do` é a garantia: `validateStart` nunca é
alcançado.

## Teoremas que congelam a precedência

```lean
theorem analyzeTransitionTable_invalid_table (raw) (start)
    (h : ¬raw.Valid) :
    analyzeTransitionTable raw start =
      .error .transitionDestinationOutOfBounds := by
  unfold analyzeTransitionTable validateTransitionTable
  rw [dif_neg h]
  rfl

theorem analyzeTransitionTable_invalid_start (raw) (start)
    (hRaw : raw.Valid) (hStart : ¬start < raw.next.size) :
    analyzeTransitionTable raw start =
      .error (.initialStateOutOfBounds start raw.next.size) := by
  unfold analyzeTransitionTable validateTransitionTable
  rw [dif_pos hRaw]
  show (validateStart ⟨raw.next, hRaw⟩ start).bind _ = _
  rw [show validateStart ⟨raw.next, hRaw⟩ start
        = .error (.initialStateOutOfBounds start raw.next.size)
      from dif_neg hStart]
  rfl
```

**Ambos compilam.** Note que o primeiro precisa de `rfl` ao final e o
segundo de um `show` — ver o achado técnico abaixo.

### Achado técnico congelado

Três abordagens **falham** e não devem ser tentadas de novo:

```text
simp [analyze, validate, dif_neg h, Except.bind]  ->  unsolved goals
split                                              ->  "Could not split"
simp only [...] ; simp [hStart]                    ->  "made no progress"
```

Motivo: depois de `dif_pos hRaw`, a condição interna é
`start < validated.next.size` com `validated` ainda **ligado pelo `do`**.
`(⟨raw.next, hRaw⟩ : ValidatedTransitionTable).next.size` é *defeq* a
`raw.next.size`, mas não sintaticamente igual, e `rw` opera
sintaticamente. O `show` resolve porque opera a menos de definicional.

## `internalDetectorFailure`

```text
mantido na funcao executavel;
proposicionalmente impossivel para entradas validas;
NAO mascara os dois primeiros erros;
NAO eh substituido por certificado falso.
```

A impossibilidade vira corolário:

```lean
theorem analyzeTransitionTable_ne_internalFailure (raw) (start)
    (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure
```

derivado de `analyzeTransitionTable_complete`: se a análise devolve
`.ok w`, ela não devolve `.error _`, por construtores disjuntos.

**O construtor defensivo não é removido da função.** Provar que um ramo é
inalcançável é diferente de eliminá-lo — e é a diferença entre documentar
uma impossibilidade e totalizar uma função.

## Soundness e completeness da análise

```lean
theorem analyzeTransitionTable_sound
    {raw} {start} {w} (h : analyzeTransitionTable raw start = .ok w) :
    raw.Valid ∧ start < raw.next.size ∧
    raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start

theorem analyzeTransitionTable_complete (raw) (start)
    (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    ∃ w, analyzeTransitionTable raw start = .ok w
```

### Transporte dependente — auditado

A revisão examinou o risco de recast entre `Fin validated.next.size` e
`Fin raw.next.size`. **A estratégia preferida evita o problema**: obter a
tabela validada **diretamente da redução** de `validateTransitionTable`,
isto é, trabalhar com `⟨raw.next, hRaw⟩`, cujo `next` é sintaticamente
`raw.next`. Assim os dois `Fin` são o mesmo tipo, e nenhum recast é
necessário.

```text
NAO adicionar equality recasts complexos sem necessidade.
```

A terceira conjunção da soundness é enunciada sobre `raw` — e é
exatamente por isso que `validateTransitionTable_sound` precisa devolver
`validated.toRaw = raw`, e não apenas a validade.
