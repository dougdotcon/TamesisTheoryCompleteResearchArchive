---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T02:54:50-03:00
canonical_commit: "95e5865e174e77b19a56e6a3c1c243ef4c64a6c1"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "millennium"
active_work_item: "RH-NOGO-001"
work_status: "SCOPED"
evidence_level: "F"
last_verified_artifact: "found-semigroup-001-result.json"
current_blocker: "Especificação formal e auditoria bibliográfica ainda não executadas."
next_single_action: "Preparar o enunciado formal, as dependências e a auditoria bibliográfica de RH-NOGO-001 sem iniciar sua prova."
authorized_action: "RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED"
prohibited_actions:
  - "Não executar a prova de RH-NOGO-001 (RH_NOGO_PROOF_EXECUTION não autorizado)"
  - "Não usar os zeros como entrada para construir o espectro que depois os explica"
  - "Não usar evidência numérica como prova da RH"
  - "Não usar linguagem Tamesis no lugar do enunciado clássico"
  - "Não modificar legado"
  - "Não declarar descoberta"
  - "Não promover evidência automaticamente"
  - "Não retomar a rota nativa Windows nem operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "00_GOVERNANCE/CLAIM_LEDGER.yaml (RH-NOGO-001)"
  - "03_MILLENNIUM/01_RIEMANN/"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

FOUND-SEMIGROUP-001 foi executado e verificado: o modelo finito de três
regimes e três transições está formalizado como monoide cíclico com ação
fiel e transitiva, sob a interface oficial da Mathlib
(`SemigroupAction`/`MulAction`), com auditoria computacional e
contraexemplos que impedem generalização indevida. Valor científico:
`FOUNDATIONAL_FORMALIZATION_ONLY` — o modelo não valida TRI, TDTR ou
qualquer claim histórica.

## Work items verificados

| Item | Estado | Evidência |
|---|---|---|
| LAB-ARCH-001 | VERIFIED | governança e labctl |
| LAB-BENCH-001 | VERIFIED | lab-bench-001-result.json |
| FOUND-SEMIGROUP-001 | VERIFIED | found-semigroup-001-result.json; FOUND-SG-001..013 |

## Frente ativa

`RH-NOGO-001` — `SCOPED`, com autorização exclusiva de **preparação de
especificação** (`RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED`).

A execução da prova (`RH_NOGO_PROOF_EXECUTION`) permanece
`NOT_AUTHORIZED / NO_EXECUTION`. A preparação exige, antes de qualquer
prova: enunciado exato da classe de operadores, hipóteses espectrais
explícitas, auditoria de não circularidade (separação de GUE e dados
definidos pelos próprios zeros), bibliografia primária, matriz de
resultados conhecidos, gaps, contraexemplos, Lean map e critério de
novidade.

## Runtime e ambiente Lean

- Runtime canônico: Ubuntu 24.04 no WSL2, usuário `linuxdev`, host `linux-dev`.
- Diretório canônico: `/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive`.
- Lean: 4.33.0-rc1; Lake: 5.0.0-src+62eed1d; Elan: 4.2.3.
- Mathlib: tag `v4.33.0-rc1`, revisão `79d0395a1825a6264ad5d269e35e60537518955e`.
- Detalhamento em `05_FORMAL/LEAN_ENVIRONMENT.md`.

## Rota nativa Windows

`FROZEN / HISTORICAL / NOT_OPERATIONAL` — tag `lab-native-windows-paused`,
commit `634de1c3aa915fcb0ccc5f27d6fe6194368535a4`.

## Próxima ação única

Preparar o enunciado formal, as dependências e a auditoria bibliográfica de
RH-NOGO-001 sem iniciar sua prova.

## Ações proibidas

- executar a prova de RH-NOGO-001 ou qualquer frente Clay;
- alterar qualquer arquivo fora de `04_FORMAL_RESEARCH_LAB/`;
- usar sorry, admit, axioma local ou unsafe;
- promover computação, simulação ou modelo finito a teorema universal;
- interpretar FOUND-SEMIGROUP-001 como validação de TRI, TDTR ou TOE;
- retomar a rota nativa Windows ou operar a partir de `/mnt/d`.

## Histórico recente

- 2026-07-28 a 2026-07-30: LAB-0.x bloqueados pelo cache Mathlib no Windows.
- 2026-07-31: LAB-WSL-MIGRATION migrou o runtime canônico para o WSL2
  (`v4.33.0-rc1`).
- 2026-07-31: LAB-BENCH-001 executado e verificado
  (`LAB_BENCH_001_VERIFIED`).
- 2026-07-31: FOUND-SEMIGROUP-001 executado e verificado
  (`FOUND_SEMIGROUP_001_VERIFIED`); modelo C3 formalizado; claim
  FOUND-SG-FORMAL-001 registrada em `F`.
- Nenhuma prova de Riemann foi aberta; nenhuma frente Clay foi executada.
