---
document_id: RT-STOP-CONDITIONS
count: 21
---

# Condições de parada

`NEEDS_REFINEMENT` se qualquer uma ocorrer:

```text
 1. size armazenado redundantemente;
 2. tabela vazia misturada com tabela invalida;
 3. destinos invalidos corrigidos por modulo;
 4. estado inicial invalido corrigido por modulo;
 5. fallback silencioso;
 6. ValidatedTransitionTable nao garantindo fechamento;
 7. step podendo sair de Fin n;
 8. run? usando valor padrao;
 9. correspondencia de iteracoes sem plano coerente;
10. o detector anterior copiado;
11. o pigeonhole repetido;
12. analyzeTransitionTable escondendo erros de validacao;
13. internalDetectorFailure mascarando tabela ou inicio invalidos;
14. o ramo none substituido por witness falso;
15. escolha classica produzindo dados;
16. o objeto de orbita quociente no codigo executavel;
17. parsing JSON no nucleo;
18. Floyd ou Brent como dependencia;
19. correcao da abstracao externa assumida;
20. complexidade afirmada sem modelo;
21. novidade matematica ou algoritmica reivindicada.
```

## Estado nesta especificação

| # | Estado |
|---|---|
| 1 | **não ocorre** — `stateCount` foi considerado e recusado |
| 2 | **não ocorre** — erros distintos, teoremas distintos, testes distintos |
| 3 | **não ocorre** — `dite` sobre `Valid`, sem tocar no array |
| 4 | **não ocorre** — `validateStart_sound` prova preservação exata |
| 5 | **não ocorre** — nenhum `getD`, nenhum default |
| 6 | **não ocorre** — `closed` é campo da estrutura |
| 7 | **não ocorre** — o tipo de `step` não admite escape |
| 8 | **não ocorre** — `run?` devolve `none`, verificado no probe |
| 9 | **não ocorre** — indução com a variante de `iterate` **auditada** |
| 10 | **não ocorre** — `detectCycle?` é aplicação de uma linha |
| 11 | **não ocorre** — consumido via `exists_bounded_iterate_collision` |
| 12 | **não ocorre** — a ordem do `do` garante precedência dos erros |
| 13 | **não ocorre** — os dois teoremas de erro esperado fixam qual sai |
| 14 | **não ocorre** — `none` vira erro, nunca certificado |
| 15 | **não ocorre** — nenhum `Classical.choose` |
| 16 | **não ocorre** — não aparece na frente |
| 17 | **não ocorre** — o núcleo recebe `Array Nat`, não texto |
| 18 | **não ocorre** — ambos `NOT_AUTHORIZED` |
| 19 | **não ocorre** — registrado como responsabilidade externa, `RT-GAP-017` |
| 20 | **não ocorre** — `RT-GAP-019` aberto |
| 21 | **não ocorre** — `NONE` / `NONE` |

## Herdadas

```text
nao estender as tres fundacoes encerradas;
nao totalizar detectCycleWitness?;
nao registrar testes que importam a raiz dentro de TamesisLab.lean;
parar com POST_COMMIT_VALIDATION_FAILED se uma auditoria falhar depois
  do commit e ambas as correcoes estiverem proibidas;
nao assumir sucesso a partir de saida truncada;
nao operar a partir de /mnt/d.
```
