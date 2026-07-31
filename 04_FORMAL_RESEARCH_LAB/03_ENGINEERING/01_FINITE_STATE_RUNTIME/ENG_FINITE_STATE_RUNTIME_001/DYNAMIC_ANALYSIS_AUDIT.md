---
document_id: RT-DYNAMIC-ANALYSIS-AUDIT
soundness_proved: true
completeness_proved: true
---

# Auditoria da API dinâmica

As duas obrigações que **não** tinham evidência executável antes deste
gate — `analyzeTransitionTable_sound` e `_complete` — foram formalizadas
e compilaram.

## Precedência dos erros, provada

```lean
theorem analyzeTransitionTable_invalid_table (h : ¬raw.Valid) :
    analyzeTransitionTable raw start = .error .transitionDestinationOutOfBounds

theorem analyzeTransitionTable_invalid_start (hRaw : raw.Valid)
    (hStart : ¬start < raw.next.size) :
    analyzeTransitionTable raw start =
      .error (.initialStateOutOfBounds start raw.next.size)
```

Os dois **fixam qual erro sai em cada situação**, e é isso que impede
`internalDetectorFailure` de mascarar falha de validação. Medido:

```text
analyzeTransitionTable ⟨#[1]⟩ 0    ->  transitionDestinationOutOfBounds
analyzeTransitionTable ⟨#[1]⟩ 100  ->  transitionDestinationOutOfBounds
```

No segundo caso a tabela é inválida **e** o início é inválido. O erro de
**tabela** vence — a ordem do `do` garante que `validateStart` nunca é
alcançado.

## Soundness

```lean
theorem analyzeTransitionTable_sound
    (h : analyzeTransitionTable raw start = .ok w) :
    raw.Valid ∧ start < raw.next.size ∧
    raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start
```

Estratégia efetiva:

```text
by_cases hRaw    ramo negativo fecha por analyzeTransitionTable_invalid_table
by_cases hStart  ramo negativo fecha por analyzeTransitionTable_invalid_start
analyze_reduce   reduz a analise ao match do detector
cases no detector
  none  contradiz h
  some  Except.ok.inj identifica o witness
        detectCycle?_raw_repeat entrega a terceira conjuncao
```

**Nenhum transporte dependente foi necessário.** A tabela concreta é
`⟨raw.next, hRaw⟩`, cujo campo `next` é sintaticamente `raw.next`; logo
`Fin validated.next.size` e `Fin raw.next.size` são o mesmo tipo, e
`(⟨raw.next, hRaw⟩).toRaw` é definicionalmente `raw` por eta de
estruturas. Zero `cast`, zero `Eq.ndrec`.

A terceira conjunção é enunciada sobre `raw` — e é exatamente por isso
que `validateTransitionTable_sound` precisa devolver a igualdade das
tabelas, e não apenas a validade.

## Completeness

```lean
theorem analyzeTransitionTable_complete (hRaw : raw.Valid)
    (hStart : start < raw.next.size) :
    ∃ w, analyzeTransitionTable raw start = .ok w := by
  obtain ⟨w, hw⟩ :=
    ValidatedTransitionTable.detectCycle?_complete ⟨raw.next, hRaw⟩ ⟨start, hStart⟩
  refine ⟨w, ?_⟩
  rw [analyze_reduce hRaw hStart, hw]
```

Quatro linhas. O witness vem por **eliminação proposicional normal** do
existencial do detector — nenhum `Classical.choose`, nenhum
`Option.get`, nenhuma projeção para produzir dado executável.

A colisão limitada **não** é repetida: ela é consumida através de
`detectCycleWitness?_complete`.

## O ramo defensivo

```lean
theorem analyzeTransitionTable_ne_internalFailure (hRaw) (hStart) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure
```

Derivado da completude em três linhas. **O construtor permanece na
função executável.** Provar que um ramo é inalcançável é diferente de
eliminá-lo — e é a diferença entre documentar uma impossibilidade e
totalizar uma função.

`FOUND-CYCLE-DETECTION-001` **não** foi totalizado; seu
`totalization_status` permanece `DEFERRED`.

## Axiomas da camada dinâmica

```text
detectCycle?                          [propext, Classical.choice, Quot.sound]
detectCycle?_raw_repeat               [propext, Classical.choice, Quot.sound]
analyzeTransitionTable                [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_sound          [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_complete       [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_invalid_table  [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_invalid_start  [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_ne_internalFailure [propext, Classical.choice, Quot.sound]
```

A pegada entra exatamente onde o detector entra, por `Fintype.card`. Não
é marca de não-computabilidade: a função foi avaliada em dezenove casos.
