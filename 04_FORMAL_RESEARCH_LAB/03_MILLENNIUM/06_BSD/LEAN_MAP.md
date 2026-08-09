# Mapa Lean

Curvas elípticas, funções L, grupos de Selmer, e Sha seguem
`NOT_FORMALIZED` — a matriz é uma auditoria de literatura, não uma
formalização de aritmética de curvas elípticas.

Um rascunho autocontido foi escrito e compilado nesta rodada (auditoria
`BSD-HYP-MATRIX-001`, 2026-08-09):

- `FORMAL/hypothesis_partition_guardrail.lean` — em lógica pura, sem
  Mathlib: `union_of_covered_cases` (o que uma matriz de teoremas
  condicionais realmente dá) e um contraexemplo concreto de dois
  elementos mostrando que essa união não é cobertura universal sem uma
  hipótese de exaustividade adicional (`BSD-GAP-005`) — o formato exato
  da falácia que `ANALISE_CRITICA_BSD.md` comete. Compilado
  (`lake env lean`, `exit 0`) na integração serial. **Não** registrado em
  `TamesisLab.lean`. `Curve`, `H`, `P` são parâmetros opacos — nada aqui
  prova algo sobre curvas elípticas reais.
