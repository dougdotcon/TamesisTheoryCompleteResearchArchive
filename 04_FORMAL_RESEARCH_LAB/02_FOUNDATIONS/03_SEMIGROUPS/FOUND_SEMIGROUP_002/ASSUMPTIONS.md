# FOUND-SEMIGROUP-002 — Hipóteses

## Hipóteses assumidas

1. `X` é um tipo finito (`Fintype X`). A finitude é **essencial**: é dela
   que vem a periodicidade eventual, via casa dos pombos.
2. `f : X → X` é uma função total e determinística. Nenhum não
   determinismo, nenhuma probabilidade.
3. Na Camada A, `M` é um monoide e a ação satisfaz `MulAction` da Mathlib
   (`one_smul`, `mul_smul`).
4. A convenção de composição é a herdada de `FOUND-SEMIGROUP-001`:
   `a * b` aplica `b` primeiro.

## Hipóteses deliberadamente **não** assumidas

```text
Fintype M        a finitude de M NAO eh usada em lugar algum.
                 A periodicidade eventual vem da finitude de X.

DecidableEq X    nao aparece na prova esbocada de FSG2-PER-002.
                 Ver FSG2-GAP-004c: sera omitida salvo necessidade
                 demonstrada na execucao.

Group M          inversos nao sao usados. Monoide basta.

acao fiel        ver CE-004.

acao transitiva  ver CE-002.

comutatividade   nao usada.
```

## Propriedades que **não** são automáticas

Cada negativa abaixo tem um contraexemplo planejado em
`COUNTEREXAMPLE_PLAN.md`. **Nenhuma é afirmada sem exemplo.**

| Negativa | Contraexemplo |
|---|---|
| alcançabilidade não precisa ser simétrica | `CE-001` |
| uma ação finita não precisa ser transitiva | `CE-002` |
| uma ação finita não precisa ser fiel | `CE-004` |
| uma órbita pode ter uma cauda antes do ciclo | `CE-003` |
| periodicidade eventual não implica periodicidade desde `n = 0` | `CE-003` |
| ações diferentes podem induzir a mesma função em `X` | `CE-004` |
| um invariante pode ser constante em mais de uma órbita | `CE-005` |
| um invariante não precisa separar órbitas | `CE-005` |
| o período pode depender do estado inicial | **sem modelo planejado** — `FSG2-GAP-007` |

A última linha está registrada como pendência em vez de ser afirmada. O
modelo é trivial de construir, mas não foi incluído entre os cinco
contraexemplos pedidos pelo gate, e este documento não afirma negativas sem
exemplo.

## O que **não** é assumido como premissa

Nenhuma claim histórica do arquivo é usada:

```text
TRI
TDTR
Tamesis
Omega
teoria de tudo
resultados Clay
claims fisicas
documentos legados nao auditados
```

As skills orientam o método; **não** constituem fonte matemática.

## Fronteira de validade

Os teoremas da Camada C valem para qualquer `f : X → X` com `X` finito —
essa é a força do enunciado, e também o motivo de ele não ser novidade.

Os teoremas das Camadas A e B valem para qualquer monoide agindo sobre
qualquer tipo; a finitude só entra no corolário `FSG2-ACT-001`.

O modelo `C3` de `FOUND-SEMIGROUP-001` é **um** exemplo. Suas propriedades
atípicas — fidelidade (FOUND-SG-012) e transitividade (FOUND-SG-013) — são
propriedades **daquele** modelo, refutadas em geral por `CE-004` e `CE-002`
respectivamente.
