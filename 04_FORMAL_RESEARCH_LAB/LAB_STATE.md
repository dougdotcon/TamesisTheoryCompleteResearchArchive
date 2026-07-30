---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-30T09:51:00-03:00
canonical_commit: "0bce2ff08d8dd370279445ac878ddc2570588deb"
canonical_commit_policy: "aponta para o commit finalizado do gate; a atualização deste campo ocorre no commit de fechamento seguinte"
repository_clean: true
active_track: "formal_infrastructure"
active_work_item: "LAB-BENCH-001"
work_status: "BLOCKED"
evidence_level: "F"
last_verified_artifact: "lab0.10-cache-network-result.json"
current_blocker: "O cURL moderno transfere parcialmente, mas 2.583 objetos legacy permanecem .part/404 e o processo paralelo não conclui."
next_single_action: "Investigar o endpoint legacy que deixa 2.583 objetos em estado .part/404 e impede a conclusão do curl paralelo."
authorized_action: "LAB_CACHE_NETWORK_RECOVERY_AUTHORIZED"
prohibited_actions:
  - "Não iniciar RH-NOGO-001 ou qualquer frente Clay"
  - "Não executar a formalização completa do benchmark neste gate"
  - "Não modificar legado"
  - "Não declarar descoberta"
  - "Não promover evidência automaticamente"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "05_FORMAL/specifications/LAB-BENCH-001_STATUS.yaml"
  - "05_FORMAL/specifications/LAB-BENCH-001.md"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

O LAB-0 técnico passou e o LAB-0.5 corrigiu a sequência para manter
LAB-BENCH-001 antes de qualquer frente Clay.

## Estado do benchmark

| Etapa | Estado |
|---|---|
| LEAN_ENVIRONMENT_DISCOVERY | PASS |
| LEAN_TOOLCHAIN_AVAILABILITY | PASS |
| LEAN_SMOKE_BUILD | PASS para o smoke core anterior |
| LAB_BENCHMARK_PREPARATION | PARTIAL |
| LAB_BENCHMARK_EXECUTION | NOT_STARTED |
| LAB_BENCHMARK_VERIFICATION | NOT_STARTED |

A especificação canônica está em
05_FORMAL/specifications/LAB-BENCH-001.md. A preparação permanece parcial
porque o smoke de importação Mathlib ainda não terminou.

## Ambiente Lean e Mathlib

- Elan: 4.2.3.
- Lean: 4.32.2, commit f3b06c705e6c85f5314019d5d3baab0fec5b580c.
- Lake: 5.0.0-src+f3b06c7.
- Toolchain declarado e resolvido: leanprover/lean4:v4.32.2.
- elan which lean/lake: caminhos definitivos, sem .tmp.
- Mathlib: commit 905b95818eb32af7874a58b427f50c1711a5e96c, tag v4.32.2.
- Manifesto SHA-256: 4BB811C39DA9FBFF3CE2D6BD9B947AF0A4266D865608EA83A66A5A9B97C453B9.
- Cache remoto Mathlib: indisponível; compilação local tentada.
- Smoke import Mathlib: timeout após 600 segundos; sem PASS reivindicado.

## Commit observado

Um processo externo criou 363be8ad18083c8dc54c3b9d42c47cfd5bb954c8, que
contém a camada formal e lab0.5-result.json. O commit não foi criado por esta
sessão e o lab0-result.json nele contido já traz avisos posteriores; ele
permanece congelado e não é tratado como snapshot histórico puro.

## Estado de RH-NOGO-001

SCOPED
NOT_AUTHORIZED
NO_EXECUTION

Nenhuma sessão de Riemann foi aberta.

## Próxima ação única

Concluir o smoke test Mathlib compilando localmente o alvo MathlibSmoke.

## Ações proibidas

- abrir ou executar RH-NOGO-001;
- criar teoremas do benchmark além do smoke de infraestrutura;
- alterar qualquer arquivo fora de 04_FORMAL_RESEARCH_LAB/;
- usar sorry, admit, axioma local ou unsafe;
- interpretar smoke incompleto como verificação;
- iniciar automaticamente a etapa seguinte.

## Histórico recente

- 2026-07-28: LAB-0 técnico passou.
- 2026-07-28: LAB-0.5 corrigiu o gate.
- 2026-07-28: commit externo 363be8a congelou a camada formal.
- 2026-07-28: toolchain definitivo e Mathlib foram resolvidos.
- 2026-07-28: LAB-0.6 interrompido por LAB_MATHLIB_SMOKE_BUILD_FAILED.
- 2026-07-28: nenhuma frente Clay foi iniciada.
