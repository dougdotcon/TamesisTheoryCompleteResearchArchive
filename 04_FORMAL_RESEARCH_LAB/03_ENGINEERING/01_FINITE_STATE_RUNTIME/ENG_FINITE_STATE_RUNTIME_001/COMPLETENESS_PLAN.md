---
document_id: RT-COMPLETENESS-PLAN
pigeonhole_repeated: false
---

# Plano de completude

## Validação da tabela

```lean
theorem validateTransitionTable_complete (raw : RawTransitionTable)
    (h : raw.Valid) :
    ∃ validated, validateTransitionTable raw = .ok validated
```

Rota: `dif_pos h`. A testemunha é `⟨raw.next, h⟩`.

## Validação do início

```lean
theorem validateStart_complete (t : ValidatedTransitionTable) {start : Nat}
    (h : start < t.next.size) :
    ∃ s, validateStart t start = .ok s
```

Idem, com testemunha `⟨start, h⟩`.

## Detector adaptado

```lean
theorem ValidatedTransitionTable.detectCycle?_complete
    (t : ValidatedTransitionTable) (start : Fin t.next.size) :
    ∃ w, t.detectCycle? start = some w
```

**Reutilização direta** de `detectCycleWitness?_complete`, instanciado com
`X := Fin t.next.size`, `f := t.step`, `x := start`. As instâncias
`Fintype` e `DecidableEq` de `Fin n` são inferidas.

```text
NAO repetir a teoria de ciclos;
NAO repetir Fintype.exists_ne_map_eq_of_card_lt;
NAO repetir a enumeracao de candidatos.
```

A frente inteira consome a completude do detector como caixa-preta. Isso
deve ser verificável por `grep`: nenhuma menção ao lema de contagem nos
módulos desta frente.

## API dinâmica

```lean
theorem analyzeTransitionTable_complete (raw : RawTransitionTable)
    (start : Nat) (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    ∃ w, analyzeTransitionTable raw start = .ok w
```

Fluxo obrigatório:

```text
validateTransitionTable_complete   ->  o primeiro <- passa
validateStart_complete             ->  o segundo <- passa
detectCycle?_complete              ->  o match cai em some
                                       logo o ramo none nao ocorre
```

O `hStart` precisa ser transportado para a tabela **validada**: como
`validateTransitionTable_sound` dá `validated.toRaw = raw`, os tamanhos
coincidem, e `start < validated.next.size` segue.

## O corolário defensivo

```lean
theorem analyzeTransitionTable_ne_internalFailure
    (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start ≠ .error .internalDetectorFailure
```

Derivado da completude: se a análise devolve `.ok w`, ela não devolve
`.error _`, porque `Except` é um tipo indutivo com construtores
disjuntos.

```text
NAO eliminar o construtor de erro da API executavel nesta versao.
```

O teorema prova que o ramo é inalcançável para entradas válidas; ele
**não** o remove do código. Essa é exatamente a diferença entre
documentar uma impossibilidade e totalizar uma função.
