---
document_id: FCD-STOP-CONDITIONS
count: 16
---

# Condições de parada

Decisão `NEEDS_REFINEMENT` se qualquer uma ocorrer:

```text
1.  Floyd permanecer obrigatorio na primeira versao;
2.  o detector usar periodicOrbit como dado computavel;
3.  a estrutura armazenar entryPoint redundantemente sem razao;
4.  prefixIndex ser chamado de minimo sem prova;
5.  period ser chamado de minimalPeriod sem prova;
6.  a terminacao depender de uma busca nao limitada;
7.  o algoritmo usar Classical.choose;
8.  a funcao principal ser marcada noncomputable;
9.  a completude repetir a casa dos pombos;
10. cycleCandidates omitir o caso mu + lam = card X;
11. o total wrapper impedir #eval;
12. DecidableEq ser propagada para teoremas que nao a necessitam;
13. a complexidade ser afirmada sem modelo de custo;
14. SimpleGraph ser introduzido;
15. uma claim de novidade matematica ser criada;
16. uma conexao com fisica, TRI, TDTR, TOE ou Clay ser aberta.
```

## Estado de cada uma nesta especificação

| # | Estado |
|---|---|
| 1 | **não ocorre** — Floyd é `DEFERRED_OPTIMIZATION` |
| 2 | **não ocorre** — `periodicOrbit` só aparece em enunciado proposicional |
| 3 | **não ocorre** — `entryPoint` foi rejeitado do modelo de dados |
| 4 | **não ocorre** — o nome `entryIndex` foi proibido; `prefixIndex` é "índice-base de colisão certificada" |
| 5 | **não ocorre** — `period` é "período positivo testemunhado"; `minimalPeriod` marcado `NOT_NEEDED` |
| 6 | **não ocorre** — busca sobre `cycleCandidates (card X)`, lista finita |
| 7 | **não ocorre** — `Classical.choose` proibido explicitamente |
| 8 | **não ocorre** — nenhuma definição marcada `noncomputable` |
| 9 | **não ocorre** — pigeonhole consumido via `exists_bounded_iterate_collision` |
| 10 | **não ocorre** — fronteira verificada por avaliação: `(0,3),(1,2),(2,1)` em `n=3` |
| 11 | **prevenido** — o total wrapper está `DEFERRED` justamente por não poder ser verificado aqui |
| 12 | **não ocorre** — `DecidableEq` fica só na camada 2; as três pontes não a recebem |
| 13 | **não ocorre** — `complexity_status: NOT_FORMALIZED` |
| 14 | **não ocorre** — zero menções a `SimpleGraph` na especificação |
| 15 | **não ocorre** — ledger em 19; nenhuma claim criada |
| 16 | **não ocorre** — nenhuma conexão aberta |

## Condições herdadas das frentes anteriores

```text
nao estender FOUND-SEMIGROUP-002 nem FOUND-FUNCTIONAL-GRAPH-001;
nao aplicar a reciproca de periodicOrbit a pontos nao periodicos;
nao criar instancia global de Setoid para EventuallyMeets;
nao operar a partir de /mnt/d;
nao modificar legado.
```
