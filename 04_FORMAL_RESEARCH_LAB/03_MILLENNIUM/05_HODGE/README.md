# Hodge — HODGE-CDK-001

Auditar a inferência entre loci de Hodge e existência de ciclos algébricos.

## Rodada `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09` (auditoria de literatura)

Produto desta rodada: reconstrução, com citação de fonte primária onde
possível, do que o Teorema de Cattani–Deligne–Kaplan (1995) prova sobre
o locus de Hodge e do que ele explicitamente não prova sobre a
Conjectura de Hodge geral, mais um caso especial (Noether–Lefschetz,
codimensão de ciclo 1) auditado passo a passo.

Ler nesta ordem:

1. `REVIEWS/AUDIT_REPORT.md` — nota crítica, seções "Verificado" e
   "Aproximado" separadas.
2. `DEFINITIONS.md` — definições citadas (classe de Hodge, locus de
   Hodge, transversalidade de Griffiths, teorema CDK, Lefschetz (1,1)).
3. `ASSUMPTIONS.md` — a distinção auditada e onde a inferência proibida
   entraria.
4. `RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md` — caso especial verificável,
   auditado passo a passo.
5. `KNOWN_RESULTS_MATRIX.md`, `GAP_REGISTER.yaml`, `PROOF_SKETCH.md`.
6. `FORMAL/hodge_locus_fallacy_sketch.lean` — rascunho Lean isolado,
   não compilado nesta sessão, formalizando apenas a estrutura lógica
   da falácia auditada (não CDK, nem Hodge, nem Lefschetz).

Nenhum resultado aqui declara, aproxima, ou sugere resolução da
Conjectura de Hodge — proibição de `../../AGENTS.md`.
