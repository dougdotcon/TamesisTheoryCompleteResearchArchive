---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-31T01:54:32-03:00
canonical_commit: "634de1c3aa915fcb0ccc5f27d6fe6194368535a4"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "formal_infrastructure"
active_work_item: "LAB-BENCH-001"
work_status: "READY"
evidence_level: "F"
last_verified_artifact: "lab-wsl-migration-result.json"
current_blocker: null
next_single_action: "Executar o benchmark formal LAB-BENCH-001 conforme sua especificação canônica."
authorized_action: "LAB_BENCHMARK_EXECUTION_AUTHORIZED"
prohibited_actions:
  - "Não iniciar RH-NOGO-001 ou qualquer frente Clay"
  - "Não modificar legado"
  - "Não declarar descoberta"
  - "Não promover evidência automaticamente"
  - "Não retomar a rota nativa Windows"
  - "Não operar a partir de /mnt/d"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "05_FORMAL/LEAN_ENVIRONMENT.md"
  - "05_FORMAL/specifications/LAB-BENCH-001_STATUS.yaml"
  - "05_FORMAL/specifications/LAB-BENCH-001.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

A infraestrutura formal está encerrada. O runtime canônico do laboratório
migrou para Ubuntu 24.04 no WSL2 e o par Lean/Mathlib `v4.33.0-rc1` compila,
com cache disponível e smokes concluídos. O bloqueio que persistiu de LAB-0.6
a LAB-0.11 era específico do runtime Windows nativo e deixou de existir.

## Estado do benchmark

| Etapa | Estado |
|---|---|
| LEAN_ENVIRONMENT_DISCOVERY | PASS |
| LEAN_TOOLCHAIN_AVAILABILITY | PASS |
| LEAN_SMOKE_BUILD | PASS |
| LAB_BENCHMARK_PREPARATION | PASS |
| LAB_BENCHMARK_EXECUTION | NOT_STARTED |
| LAB_BENCHMARK_VERIFICATION | NOT_STARTED |

A especificação canônica está em
`05_FORMAL/specifications/LAB-BENCH-001.md`. A preparação está completa: o
toolchain é definitivo, a revisão Mathlib está fixada e os três smokes de
importação concluíram.

## Runtime e ambiente Lean

- Runtime canônico: Ubuntu 24.04 no WSL2, usuário `linuxdev`, host `linux-dev`.
- Diretório canônico: `/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive`.
- Elan: 4.2.3.
- Lean: 4.33.0-rc1, commit `62eed1db4d67327ec8120be05f1a1b0847d74561`.
- Lake: 5.0.0-src+62eed1d.
- Toolchain declarado e resolvido: `leanprover/lean4:v4.33.0-rc1`.
- Mathlib: tag `v4.33.0-rc1`, revisão `79d0395a1825a6264ad5d269e35e60537518955e`.
- Cache Mathlib: `lake exe cache get` exit 0; 8.643 arquivos descomprimidos.
- Smokes `Mathlib.Data.Nat.Basic`, `Mathlib.Tactic` e `Mathlib`: PASS.
- `lake build`: PASS, 8.670 jobs.

O detalhamento está em `05_FORMAL/LEAN_ENVIRONMENT.md`.

## Rota nativa Windows

`FROZEN / HISTORICAL / NOT_OPERATIONAL`

Congelada na tag `lab-native-windows-paused`, commit
`634de1c3aa915fcb0ccc5f27d6fe6194368535a4`. O par Lean/Mathlib `v4.32.2`
associado a ela não é ressuscitado. `/mnt/d/TamesisTheoryCompleteResearchArchive`
serve apenas como origem histórica do clone.

## Estado de RH-NOGO-001

SCOPED
NOT_AUTHORIZED
NO_EXECUTION

Nenhuma sessão de Riemann foi aberta.

## Próxima ação única

Executar o benchmark formal LAB-BENCH-001 conforme sua especificação canônica.

## Ações proibidas

- abrir ou executar RH-NOGO-001;
- alterar qualquer arquivo fora de `04_FORMAL_RESEARCH_LAB/`;
- usar sorry, admit, axioma local ou unsafe;
- interpretar smoke de infraestrutura como verificação matemática;
- promover evidência automaticamente;
- retomar a rota nativa Windows ou operar a partir de `/mnt/d`.

## Histórico recente

- 2026-07-28: LAB-0 técnico passou.
- 2026-07-28: LAB-0.5 corrigiu o gate.
- 2026-07-28: commit externo 363be8a congelou a camada formal.
- 2026-07-28: LAB-0.6 interrompido por LAB_MATHLIB_SMOKE_BUILD_FAILED.
- 2026-07-28: LAB-0.7 terminou como LAB07_CACHE_UNAVAILABLE_FOR_REVISION.
- 2026-07-28: LAB-0.8 terminou como LAB08_NO_REPRODUCIBLE_PAIR_FOUND.
- 2026-07-30: LAB-0.9 terminou como LAB09_CAUSE_STILL_UNRESOLVED.
- 2026-07-30: LAB-0.10 terminou como LAB010_CACHE_TRANSFER_STALLED.
- 2026-07-30: LAB-0.11 terminou como LAB011_NO_CACHE_BACKED_PAIR_FOUND.
- 2026-07-31: LAB-WSL-MIGRATION migrou o runtime canônico para o WSL2,
  alinhou o par a `v4.33.0-rc1` e encerrou a infraestrutura.
- Nenhuma frente Clay foi iniciada.
