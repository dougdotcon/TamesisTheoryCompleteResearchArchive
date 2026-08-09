# Mapa Lean

O Teorema de Cattani-Deligne-Kaplan, transversalidade de Griffiths, e
qualquer geometria algébrica/teoria de Hodge seguem `NOT_FORMALIZED` —
Mathlib não tem variações de estrutura de Hodge nem domínios de período.

Um rascunho autocontido foi escrito e compilado nesta rodada (auditoria
`HODGE-CDK-001`, 2026-08-09):

- `FORMAL/hodge_locus_fallacy_sketch.lean` — formaliza só a *estrutura
  lógica* da falácia identificada (`HODGE-GAP-002`): uma propriedade
  estrutural forte do locus (aqui, finitude, substituto formal de
  algebricidade) não implica sobrejetividade do mapa. Compilado
  (`lake env lean`, `exit 0`) na integração serial. **Não** registrado
  em `TamesisLab.lean`, e **não** é uma formalização de CDK, Griffiths,
  ou Lefschetz (1,1) — é uma analogia abstrata sobre tipos arbitrários.

