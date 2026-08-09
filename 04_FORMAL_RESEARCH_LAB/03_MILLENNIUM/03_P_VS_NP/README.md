# P versus NP — PVSNP-PHYS-001

Separar complexidade física de complexidade de máquinas de Turing.

## Auditoria `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09`

Alvo: definir `P_phys`/`NP_phys` sem alegar que isso decide `P` vs `NP`
clássico. Produto: `RESULTS/TECHNICAL_NOTE.md` (nota técnica principal),
com o detalhamento em `DEFINITIONS.md`, `ASSUMPTIONS.md`,
`KNOWN_RESULTS_MATRIX.md`, `PROOF_SKETCH.md`, `GAP_REGISTER.yaml` e
`REVIEWS/AUDIT_REPORT.md` (seções "Verificado"/"Aproximado" separadas).
Rascunho Lean não integrado em `FORMAL/PvsNPPhys.lean`.

**Condição de parada atingida e reportada, não forçada**: nem uma ponte
universal de simulação para máquinas de Turing, nem uma codificação
canônica `(E,M,R)`, existem na literatura pesquisada nesta sessão — ver
`PROOF_SKETCH.md` seção 3. Nenhum Problema do Milênio é declarado
resolvido, aproximado ou alcançável por esta auditoria.
