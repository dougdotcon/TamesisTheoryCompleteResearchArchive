---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T02:24:40-03:00
canonical_commit: "dc43bec5209be77ad227383d1405c33e4dc71484"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "foundations"
active_work_item: "FOUND-SEMIGROUP-001"
work_status: "READY"
evidence_level: "F"
last_verified_artifact: "lab-bench-001-result.json"
current_blocker: null
next_single_action: "Preparar e executar FOUND-SEMIGROUP-001 conforme seu enunciado canônico."
authorized_action: "FOUNDATIONS_EXECUTION_AUTHORIZED"
prohibited_actions:
  - "Não iniciar RH-NOGO-001 ou qualquer frente Clay"
  - "Não modificar legado"
  - "Não declarar descoberta"
  - "Não promover evidência automaticamente"
  - "Não retomar a rota nativa Windows"
  - "Não operar a partir de /mnt/d"
  - "Não tratar o benchmark de infraestrutura como resultado científico"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "05_FORMAL/LEAN_ENVIRONMENT.md"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

O benchmark formal LAB-BENCH-001 foi executado e verificado no runtime
canônico Ubuntu 24.04/WSL2. A infraestrutura Lean/Mathlib compila matemática
elementar conhecida com rastreabilidade completa e zero tokens proibidos.
O benchmark mede o processo; nenhum item dele é resultado científico.

## Estado do benchmark LAB-BENCH-001

`VERIFIED`

| Etapa | Estado |
|---|---|
| LEAN_ENVIRONMENT_DISCOVERY | PASS |
| LEAN_TOOLCHAIN_AVAILABILITY | PASS |
| LEAN_SMOKE_BUILD | PASS |
| LAB_BENCHMARK_PREPARATION | PASS |
| LAB_BENCHMARK_EXECUTION | PASS |
| LAB_BENCHMARK_VERIFICATION | PASS |

Evidências: `lab-bench-001-result.json`,
`05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md` (11 definições,
15 teoremas, todos elementares e conhecidos), `lake build` PASS com 8.676
jobs, `TamesisLab/Tests/BenchmarkSmoke.lean` PASS individual, pytest PASS,
`labctl validate` PASS.

## Runtime e ambiente Lean

- Runtime canônico: Ubuntu 24.04 no WSL2, usuário `linuxdev`, host `linux-dev`.
- Diretório canônico: `/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive`.
- Lean: 4.33.0-rc1; Lake: 5.0.0-src+62eed1d; Elan: 4.2.3.
- Mathlib: tag `v4.33.0-rc1`, revisão `79d0395a1825a6264ad5d269e35e60537518955e`.
- Detalhamento em `05_FORMAL/LEAN_ENVIRONMENT.md`.

## Rota nativa Windows

`FROZEN / HISTORICAL / NOT_OPERATIONAL` — tag `lab-native-windows-paused`,
commit `634de1c3aa915fcb0ccc5f27d6fe6194368535a4`.

## Estado de RH-NOGO-001

SCOPED
NOT_AUTHORIZED
NO_EXECUTION

Nenhuma sessão de Riemann foi aberta.

## Próxima ação única

Preparar e executar FOUND-SEMIGROUP-001 conforme seu enunciado canônico.

FOUND-SEMIGROUP-001 definirá com precisão regime, transição e composição em
um exemplo finito, antes de qualquer frente Clay. Não foi executado nesta
sessão.

## Ações proibidas

- abrir ou executar RH-NOGO-001;
- alterar qualquer arquivo fora de `04_FORMAL_RESEARCH_LAB/`;
- usar sorry, admit, axioma local ou unsafe;
- interpretar o benchmark de infraestrutura como validação de TRI, TDTR, TOE
  ou qualquer claim histórica;
- promover evidência automaticamente;
- retomar a rota nativa Windows ou operar a partir de `/mnt/d`.

## Histórico recente

- 2026-07-28: LAB-0 técnico passou; LAB-0.5 corrigiu o gate.
- 2026-07-28 a 2026-07-30: LAB-0.6 a LAB-0.11 bloqueados pelo cache Mathlib
  sob o runtime Windows nativo.
- 2026-07-31: LAB-WSL-MIGRATION migrou o runtime canônico para o WSL2 e
  alinhou o par Lean/Mathlib a `v4.33.0-rc1`.
- 2026-07-31: LAB-BENCH-001 executado e verificado
  (`LAB_BENCH_001_VERIFIED`); skills locais de agente disponibilizadas em
  `.claude/skills` fora do controle de versão.
- Nenhuma frente Clay foi iniciada.
