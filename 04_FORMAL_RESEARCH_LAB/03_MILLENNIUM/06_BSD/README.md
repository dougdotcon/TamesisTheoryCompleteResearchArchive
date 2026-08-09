# Birch–Swinnerton-Dyer — BSD-HYP-MATRIX-001

Construir uma matriz verificável de hipóteses e casos cobertos.

## Status desta frente (sessão 2026-08-09, onda paralela)

`work_item_id: BSD-HYP-MATRIX-001`, autorizada por
`PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09` como uma das cinco
frentes de auditoria paralela (`01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`).

Esta é uma **auditoria de literatura**, não uma tentativa de resolver BSD.
Produto entregue: `KNOWN_RESULTS_MATRIX.md`, uma tabela de 13 linhas
particionando os principais teoremas publicados por hipótese exata,
curva/família, posto analítico coberto e primos excluídos/exigidos, sem
unir resultados de hipóteses distintas.

## Onde ler

- `KNOWN_RESULTS_MATRIX.md` — o produto principal (a matriz).
- `DEFINITIONS.md` — definições clássicas usadas na matriz.
- `ASSUMPTIONS.md` — hipóteses estruturais transversais e o que não foi
  confirmado contra fonte primária nesta sessão.
- `GAP_REGISTER.yaml` — seis lacunas registradas, todas `OPEN`.
- `PROOF_SKETCH.md` — por que não há esboço de prova aqui, e o que o
  único artefato Lean (`FORMAL/hypothesis_partition_guardrail.lean`) é
  (e não é).
- `REVIEWS/AUDIT_REPORT.md` — seção "Verificado" vs. "Aproximado",
  incluindo a análise explícita de por que o documento legado
  `RECURSOS_PARA_PESQUISA/.../ANALISE_CRITICA_BSD.md` comete o erro que
  o `stop_condition` desta frente proíbe repetir.

## O que esta frente não afirma

Nenhum Problema do Milênio é declarado resolvido, aproximado ou
"alcançável" por este trabalho (`AGENTS.md`).
