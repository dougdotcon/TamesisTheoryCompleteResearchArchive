---
document_id: RT-RESULT-REVIEW
gate: ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW
reviewed_commit: 746102fa458fe7ccda6d8939bb3f8834a8ac0dc4
decision: A_RESULT_REVIEW_APPROVED
new_theorems: 0
math_modules_modified: 0
---

# Revisão do resultado

Revisão do que já está verificado. **Nenhum teorema novo, nenhum módulo
matemático alterado, nenhuma implementação nova.** A única alteração de
conteúdo é a correção documental do cabeçalho de gaps.

## Confirmação item a item

### RTR-001 — representação bruta `CONFIRMADO`

```lean
structure RawTransitionTable where
  next : Array Nat
deriving DecidableEq, Repr, BEq
```

Um campo. `size`, `stateCount`, `proof`, `start` e `fallback` ausentes;
nenhum accessor `stateCount` existe. `raw.next.size` é o único nome
público do número de estados.

### RTR-002 — validade estrutural `CONFIRMADO`

```lean
∀ i : Fin raw.next.size, raw.next[i] < raw.next.size
```

Confirmado que **não** exige estado inicial, **não** exige tabela não
vazia, e **não** afirma alcançabilidade, componente único ou ciclo único.

### RTR-003 — decidibilidade `CONFIRMADO`

`by unfold; infer_instance`. Sem `Classical`, `Classical.choose`,
`Classical.decEq` ou marca de não-computabilidade. Síntese confirmada em
`#[]`, `#[0]` e `#[1]`.

### RTR-004 — tabela vazia `CONFIRMADO`

`valid_empty` provado; `validateTransitionTable ⟨#[]⟩` devolve `ok`;
`analyzeTransitionTable ⟨#[]⟩ 0` devolve
`initialStateOutOfBounds 0 0`. **Nenhum erro `emptyTable` existe.**

### RTR-005 — tabela validada `CONFIRMADO`

Dois campos, `next` e `closed`. Sem campos redundantes, sem `deriving`.

### RTR-006 — conversão `CONFIRMADO`

`toRaw` devolve `⟨t.next⟩` — o array é preservado literalmente.
`toRaw_valid` fecha por `t.closed`.

### RTR-007 — erros `CONFIRMADO`

Exatamente três construtores. Tabela inválida e início inválido **não**
colapsados: erros distintos, teoremas distintos, testes distintos.

## Validação — auditada

`validateTransitionTable` tem o comportamento de duas linhas exigido, e a
busca por `%`, `mod`, `clamp`, `min`, `max`, `getD` e `fallback` no código
retornou **zero**. As duas únicas ocorrências textuais estão em
documentação: a própria lista de proibições e o nome "anti-clamp".

`validateTransitionTable_sound` prova as duas conjunções exigidas;
`_complete` aceita toda tabela válida. Nenhum diagnóstico do primeiro
destino inválido é exigido — `RT-GAP-022` segue diferido.

`validateStart` preserva exatamente o `Nat` fornecido, e
`validateStart_sound` o prova. Sem módulo, clamp, zero padrão, fallback
ou escolha arbitrária.

## Execução — auditada

`step` devolve `⟨t.next[i], t.closed i⟩` e **não pode sair de `Fin n`**;
`step_val` fecha por `rfl`.

A semântica bruta foi confirmada e **não alterada**:

```text
run? 0 999 = some 999      inclusive fora dos limites
run? 1 999 = none          primeiro lookup invalido
```

```text
run? eh semantica bruta parcial;
validateStart eh a barreira da API segura.
```

## As duas pontes

`step?_eq_some_step` relaciona o lookup opcional sobre `Nat` com o `step`
total sobre `Fin n`, via `getElem?_pos`, sem fallback.

`run?_eq_iterate_step` foi auditado linha por linha: indução em `k` com o
quantificador **no enunciado**, hipótese válida para todo `start`, passo
externo executado primeiro, `Function.iterate_succ_apply`, **nenhuma
orientação inversa**. Axiomas `[propext, Quot.sound]`.

**Nenhuma segunda semântica paralela de execução existe.**

## Reutilização do detector

`detectCycle?` é exatamente `detectCycleWitness? t.step start`;
`_sound` e `_complete` são reutilizações diretas, termos de uma linha.

```text
cycleCandidates                     0 ocorrencias
exists_ne_map_eq_of_card_lt         0 ocorrencias
exists_bounded_iterate_collision    0 ocorrencias
```

O detector **não** foi copiado, e o pigeonhole **não** foi repetido.

## Interpretação do witness

`detectCycle?_raw_repeat` afirma a igualdade entre
`t.toRaw.run? (baseIndex + period) start` e
`t.toRaw.run? baseIndex start`, pelo DAG exigido. Nada é afirmado sobre
minimalidade, `minimalPeriod` ou entrada canônica.

## Decisão

```text
A. ENG_FINITE_STATE_RUNTIME_001_RESULT_REVIEW_APPROVED
```

Os dezesseis critérios de aprovação foram atendidos, incluindo o
primeiro: **o cabeçalho dos gaps foi corrigido**.
