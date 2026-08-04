---
document_id: FOUND-UNIFORM-PRIMREC-001-SPECIFICATION-REVIEW
work_item_id: FOUND-UNIFORM-PRIMREC-001
review_start_head: e219927b574588cf83926b00aebe3b421cdaa7a1
decision: FOUND_UNIFORM_PRIMREC_001_SPECIFICATION_REVIEW_APPROVED
defects_found: 1
defects_corrected: 1
---

# Revisao de especificacao

## Reexecucao

Probe rodado de novo neste gate: `exit 0`, `0` linhas `error:`,
`git_dirty=0`.

## O defeito

```text
primrec_run?_gen   {α : Type}     restrito ao universo 0
flatMap_eq_foldr   {α β : Type}   restrito ao universo 0
```

Os dois lemas **gerais** da frente estavam presos ao universo `0` **sem
motivo**. `flatMap_eq_foldr` e um lema puro de listas; `primrec_run?_gen`
so exige `[Primcodable α]`, que e universo-polimorfico.

Nao era erro de prova — era generalidade jogada fora por descuido de
assinatura. Corrigido para `Type*`, e o probe recompila com `exit 0`.

Hipoteses estritamente mais fracas, mesma conclusao, mesmo numero de
declaracoes: `31` publicas.

## Os oito itens

| # | Item | Veredito |
|---|---|---|
| 1 | `Primrec₂ analyzeTransitionTable` compila | CONFIRMADO |
| 2 | `run?_eq_iterate` e a peca que destrava | CONFIRMADO |
| 3 | O casamento nao reimplementa o detector | CONFIRMADO |
| 4 | `RawValid` espelha `CycleWitness.Valid` clausula a clausula | CONFIRMADO |
| 5 | Instancia positiva avaliada por `decide` | CONFIRMADO |
| 6 | `Primrec` NAO e apresentado como eficiencia | CONFIRMADO |
| 7 | Nenhuma frente encerrada tocada | CONFIRMADO |
| 8 | Universo dos lemas gerais | **CORRIGIDO** |

## O item 6, que a revisao existia para proteger

A frente anterior teve de dizer que `Primrec` **nao mede nada** por ser
vacuo sobre dominio finito. Esta poderia soar como se, deixando de ser
vacuo, passasse a medir. **Nao passa.**

`Primrec` contem torres de exponenciais. O revisor procurou, em
`README.md`, `SPECIFICATION_DECISION.md` e `STOP_CONDITIONS.md`, qualquer
frase que sugerisse eficiencia. Nao ha nenhuma, e `STOP-UP-002` existe
exatamente para isso.

## Decisao

`FOUND_UNIFORM_PRIMREC_001_SPECIFICATION_REVIEW_APPROVED`. Segue para
formalizacao.
