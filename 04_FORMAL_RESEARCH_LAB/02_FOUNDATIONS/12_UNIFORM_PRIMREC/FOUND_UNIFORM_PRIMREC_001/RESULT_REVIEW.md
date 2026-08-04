---
document_id: FOUND-UNIFORM-PRIMREC-001-RESULT-REVIEW
work_item_id: FOUND-UNIFORM-PRIMREC-001
review_start_head: 9d3f936989383753ac13a8209b3bf8d414fea50b
decision: FOUND_UNIFORM_PRIMREC_001_RESULT_REVIEW_APPROVED
defects_found: 0
defects_corrected: 0
---

# Revisao de resultado

## Reexecucao

```text
lake build      exit 0, 8811 jobs, 0 error, 0 sorry
declaracoes     36 derivadas da arvore instalada
publicas        31  (4 def, 27 teoremas)
tokens          0
```

Bate com a especificacao congelada. Nenhum defeito novo.

## Os sete itens

| # | Item | Veredito |
|---|---|---|
| 1 | `Primrec₂ analyzeTransitionTable` compila na arvore | CONFIRMADO |
| 2 | `CB-GAP-001` fecha com prova, nao com declaracao | CONFIRMADO |
| 3 | A prova consulta o algoritmo, nao a finitude | CONFIRMADO |
| 4 | O detector nao foi reimplementado | CONFIRMADO |
| 5 | Instancia positiva avaliada nos dois lados | CONFIRMADO |
| 6 | `Primrec` NAO e apresentado como eficiencia | CONFIRMADO |
| 7 | Nenhuma frente encerrada tocada | CONFIRMADO |

## O item 3, que e a diferenca entre as duas frentes

```text
ponte      Primrec f  para TODA f       porque o dominio e FINITO
uniforme   Primrec2 analyzeTransitionTable   porque run? e uma ITERADA
```

Na ponte, a prova era `Primrec.dom_finite f` e nunca olhava `f`. Aqui a
prova passa por `run?_eq_iterate`, `Primrec.nat_iterate`,
`primrec_cycleCandidates` e `primrec_find` — **cada uma delas so existe
por causa do que a funcao faz**.

## O item 6, e por que ele nao e formalidade

Sao **dois limites diferentes**, e os dois valem:

```text
ponte      Primrec nao mede nada    porque e VACUO sobre dominio finito
uniforme   Primrec nao mede custo   porque a CLASSE e enorme
```

`Primrec` contem torres de exponenciais. Fechar o nivel uniforme
**nao** aproximou o laboratorio de um resultado de eficiencia, e a claim
promovida carrega esse qualificador como obrigatorio.

## Decisao

`FOUND_UNIFORM_PRIMREC_001_RESULT_REVIEW_APPROVED`. Claim
`UNIFORM-ANALYSIS-PRIMREC-FORMAL-001` promovida, nivel `F`.
