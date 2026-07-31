---
document_id: RT-THEOREM-CANDIDATES
core: 23
optional_corollary: 5
---

# Candidatos

## `CORE`

```text
RawTransitionTable
RawTransitionTable.Valid
RawTransitionTable.decidableValid

ValidatedTransitionTable
ValidatedTransitionTable.toRaw

RuntimeCycleError

validateTransitionTable
validateTransitionTable_sound
validateTransitionTable_complete

validateStart
validateStart_sound
validateStart_complete

ValidatedTransitionTable.step
ValidatedTransitionTable.step_val

RawTransitionTable.step?
RawTransitionTable.run?

ValidatedTransitionTable.step?_eq_some_step
ValidatedTransitionTable.run?_eq_iterate_step

ValidatedTransitionTable.detectCycle?
ValidatedTransitionTable.detectCycle?_sound
ValidatedTransitionTable.detectCycle?_complete
ValidatedTransitionTable.detectCycle?_raw_repeat

analyzeTransitionTable
analyzeTransitionTable_sound
analyzeTransitionTable_complete
```

### Promoção de `step?_eq_some_step`

O gate pediu para avaliar se `step?_eq_some_step` é, na prática,
dependência necessária de `run?_eq_iterate_step`; se for, promovê-la a
`CORE`.

**É.** O caso sucessor da indução precisa reescrever
`t.toRaw.step? (state : Nat)` como `some (t.step state)` para que o `bind`
do `do` reduza e a hipótese de indução se aplique. Sem esse lema, o passo
teria de ser reprovado inline a cada uso.

```text
step?_eq_some_step: promovido a CORE.
```

Também `ValidatedTransitionTable.toRaw_valid` é `CORE`, por ser o que
permite reentrar na camada bruta preservando a garantia.

## `OPTIONAL_COROLLARY`

```text
validateTransitionTable_error_iff
analyzeTransitionTable_invalid_table
analyzeTransitionTable_invalid_start
analyzeTransitionTable_ne_internalFailure
RawTransitionTable.stateCount
```

O último aparece aqui **não** como recomendação, mas como registro de que
foi considerado e recusado — ver `RAW_DATA_MODEL.md`.

Os três do meio são baratos e valiosos: eles fixam **qual** erro sai em
cada situação, e é isso que impede `internalDetectorFailure` de mascarar
falha de validação. Recomendação: formalizá-los, mesmo sendo opcionais.

## `DEFERRED`

```text
diagnostico detalhado do destino invalido    RT-GAP-022
CLI                                          RT-GAP-014
JSON, CSV, arquivo                           RT-GAP-015
API web, banco de dados                      fora de escopo
Floyd, Brent, tabela visitada                NOT_AUTHORIZED
totalizacao do detector anterior             CD-GAP-017
minimalidade                                 CD-GAP-009, CD-GAP-010
complexidade formal                          RT-GAP-019
benchmark                                    fora de escopo
integracao com sistemas reais                RT-GAP-017
prova de correcao da abstracao externa       RT-GAP-017
```

## Hipóteses por camada

```text
RawTransitionTable.Valid    nenhuma typeclass externa
validateTransitionTable     nenhuma typeclass externa
ValidatedTransitionTable    nenhuma typeclass externa
step                        nenhuma typeclass externa
step?, run?                 nenhuma typeclass externa
detectCycle?                Fintype e DecidableEq de Fin n, INFERIDAS
analyzeTransitionTable      nenhuma fornecida pelo chamador
```

O consumidor fornece `Array Nat` e `Nat`. Nada mais.

## Custo estimado

```text
estruturas       3
definicoes       7
instancias       1
teoremas CORE   12
corolarios       4
```

Nenhum teorema exige teoria nova. Os quatro mais caros são
`run?_eq_iterate_step` (indução com generalização do estado),
`analyzeTransitionTable_sound` (desmontar o `do`),
`detectCycle?_raw_repeat` (composição de três lemas) e
`analyzeTransitionTable_complete` (transporte do limite entre `raw` e
`validated`).
