# Yang–Mills — YM-LIMIT-001

Separar rede, limite contínuo, axiomas, não trivialidade e gap uniforme.

## Auditoria 2026-08-09 (onda paralela `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09`)

Produto desta rodada: teorema de insuficiência (nível abstrato) mostrando
que "tightness + gap de volume finito positivo", sozinhas, não implicam
"teoria limite única com gap que sobrevive ao limite". Ver, nesta ordem:

1. `TARGET_RESULT.md` — enunciado clássico Clay (intacto) e escopo real
   desta auditoria.
2. `ASSUMPTIONS.md` — cadeia de hipóteses auditada, elo por elo.
3. `PROOF_SKETCH.md` — teorema de insuficiência e os dois contraexemplos.
4. `COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md` — os três contraexemplos
   em detalhe (dois formalizados em Lean, um em prosa).
5. `FORMAL/InsufficiencyToyModel.lean` — esboço Lean, não compilado nesta
   sessão, não integrado a `TamesisLab.lean`.
6. `RESULTS/INSUFFICIENCY_THEOREM.md` — enunciado final.
7. `REVIEWS/AUDIT_REPORT.md` — separação Verificado / Aproximado.
8. `GAP_REGISTER.yaml` — gaps `YM-GAP-001`..`YM-GAP-006`, todos `OPEN`.

Nenhum Problema do Milênio foi declarado resolvido, aproximado, ou
alcançável por esta auditoria.
