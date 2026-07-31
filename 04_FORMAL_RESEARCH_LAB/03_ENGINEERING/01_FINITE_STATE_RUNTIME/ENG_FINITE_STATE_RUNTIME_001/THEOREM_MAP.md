---
document_id: RT-THEOREM-MAP
structures: 2
inductives: 1
definitions: 9
instances: 1
theorems: 18
private: 1
lines: 869
---

# Mapa dos teoremas formalizados

## `RawTable.lean`

| Objeto | Tipo | Hipóteses |
|---|---|---|
| `RawTransitionTable` | `structure` | nenhuma |
| `RawTransitionTable.Valid` | `def ... : Prop` | nenhuma |
| `RawTransitionTable.decidableValid` | `instance` | nenhuma |
| `ValidatedTransitionTable` | `structure` | nenhuma |
| `ValidatedTransitionTable.toRaw` | `def` | nenhuma |
| `ValidatedTransitionTable.toRaw_valid` | `theorem` | nenhuma |

`decidableValid` por `unfold; infer_instance` — a forma testada na
revisão. `toRaw_valid` fecha por `t.closed` **diretamente**.

## `Validation.lean`

| Objeto | Rota |
|---|---|
| `RuntimeCycleError` | `inductive`, `deriving DecidableEq, Repr, BEq` |
| `validateTransitionTable` | `dite` sobre `Valid` |
| `validateTransitionTable_sound` | `by_cases` + `dif_pos/neg` + `Except.ok.inj` |
| `validateTransitionTable_complete` | termo: `⟨⟨raw.next, h⟩, dif_pos h⟩` |
| `validateStart` | `dite` sobre `<` |
| `validateStart_sound` | mesma rota; **teorema anti-clamp** |
| `validateStart_complete` | termo: `⟨⟨start, h⟩, dif_pos h⟩` |
| `valid_empty` | `intro i; exact absurd i.isLt (by simp)` |

Os dois `_complete` são **termos**, não táticas — uma linha cada.

## `Execution.lean`

| Objeto | Rota |
|---|---|
| `ValidatedTransitionTable.step` | `fun i => ⟨t.next[i], t.closed i⟩` |
| `step_val` | `rfl`, `@[simp]` |
| `RawTransitionTable.step?` | `t.next[state]?` |
| `RawTransitionTable.run?` | recursão com `bind` |
| `step?_eq_some_step` | `show` + `getElem?_pos t.next (i : Nat) i.isLt` |
| `run?_eq_iterate_step` | indução + dois `show` + `Function.iterate_succ_apply` |

## `DetectorAdapter.lean`

| Objeto | Rota | Prova nova |
|---|---|---|
| `detectCycle?` | `detectCycleWitness? t.step start` | — |
| `detectCycle?_sound` | `detectCycleWitness?_sound h` | **nenhuma** |
| `detectCycle?_complete` | `detectCycleWitness?_complete t.step start` | **nenhuma** |
| `detectCycle?_raw_repeat` | `sound` + `run?_eq_iterate_step` ×2 + `hw.2.2.2` | três linhas |

Os dois primeiros teoremas são **termos de uma linha**. A enumeração, a
busca e a casa dos pombos do detector não aparecem.

## `DynamicAnalysis.lean`

| Objeto | Rota |
|---|---|
| `analyzeTransitionTable` | `do` sobre `Except`, dois `←` e um `match` |
| `analyze_reduce` | **privado**; `unfold` + dois `rw [show ... from dif_pos]` + `show` + `rfl` |
| `analyzeTransitionTable_invalid_table` | `unfold` + `rw [show ... from dif_neg]` + `rfl` |
| `analyzeTransitionTable_invalid_start` | `unfold` + `rw` + `show ... .bind _` + `rw` + `rfl` |
| `analyzeTransitionTable_sound` | `by_cases` ×2 + `analyze_reduce` + `cases` no detector |
| `analyzeTransitionTable_complete` | `detectCycle?_complete` + `analyze_reduce` + `rw` |
| `analyzeTransitionTable_ne_internalFailure` | `intro` + `complete` + `rw` + `absurd` |

### O auxiliar privado

`analyze_reduce` isola, de uma vez, as **duas** reduções que a notação
`do` esconde:

```lean
private theorem analyze_reduce (hRaw : raw.Valid) (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start =
      (match ValidatedTransitionTable.detectCycle? ⟨raw.next, hRaw⟩ ⟨start, hStart⟩ with
        | some witness => .ok witness
        | none => .error .internalDetectorFailure)
```

É ele que torna soundness e completeness curtas — sete e quatro linhas,
respectivamente — e que evita transporte dependente: a tabela concreta
`⟨raw.next, hRaw⟩` tem `next` **sintaticamente** igual a `raw.next`, de
modo que `Fin validated.next.size` e `Fin raw.next.size` são o mesmo
tipo. Nenhum `cast`, `Eq.ndrec` ou recast manual foi necessário.

## Camadas de hipótese, verificadas

```text
camada 0   Raw, Valid, decidableValid, step?, run?     nenhuma typeclass
camada 1   Validated, toRaw, validacoes                nenhuma typeclass
camada 2   step, step_val, pontes de execucao          nenhuma typeclass
camada 3   detectCycle? e herdeiros                    Fintype/DecidableEq de Fin n, INFERIDAS
camada 4   analyzeTransitionTable e teoremas           nenhuma do chamador
```

**O consumidor fornece `Array Nat` e `Nat`.** Nada mais.

## Ordem de declaração

Os dois teoremas de erro foram declarados **antes** de
`analyzeTransitionTable_sound`, invertendo a ordem sugerida no gate. A
razão é técnica: a soundness os usa nos ramos negativos do `by_cases`.
Registrado como escolha deliberada, não como desvio silencioso.
