---
schema: tamesis-formal-lab-state/1
updated_at: 2026-07-28T20:10:00-03:00
canonical_commit: "4b314d7360404385a91366449087779cccf87d4d"
repository_clean: false
active_track: "formal_infrastructure"
active_work_item: "LAB-BENCH-001"
work_status: "BLOCKED"
evidence_level: "F"
last_verified_artifact: "lab0.5-result.json"
current_blocker: "O HEAD não contém 04_FORMAL_RESEARCH_LAB; o diff não pode ser atribuído exclusivamente à reconciliação LAB-0.5."
next_single_action: "Resolver a ausência do commit-base do LAB-0 e reabrir o LAB-0.6."
authorized_action: "LAB_BENCHMARK_FORMALIZATION_PREPARATION_AUTHORIZED"
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

## Onde paramos

O LAB-0 técnico passou, mas a transição de fila foi promovida indevidamente
quando o smoke build foi tratado como conclusão de `LAB-BENCH-001`.
O gate LAB-0.5 restaurou a sequência:

```text
LAB-0
→ LAB-BENCH-001
→ somente posteriormente RH-NOGO-001
```

## Estado do benchmark

| Etapa | Estado |
|---|---|
| `LEAN_ENVIRONMENT_DISCOVERY` | `PASS` |
| `LEAN_TOOLCHAIN_AVAILABILITY` | `PARTIAL` |
| `LEAN_SMOKE_BUILD` | `PASS` |
| `LAB_BENCHMARK_PREPARATION` | `PARTIAL` |
| `LAB_BENCHMARK_EXECUTION` | `NOT_STARTED` |
| `LAB_BENCHMARK_VERIFICATION` | `NOT_STARTED` |

A especificação canônica está em
`05_FORMAL/specifications/LAB-BENCH-001.md`. Ela não autoriza a criação dos
módulos Lean previstos nem a execução do benchmark completo.

## Ambiente Lean verificado

- Elan: `4.2.3`.
- Lean no diretório temporário: `4.32.2`.
- Lake no diretório temporário: `5.0.0-src+f3b06c7`.
- Toolchain declarado: `leanprover/lean4:v4.32.2`.
- `elan toolchain list`: `leanprover/lean4:v4.32.tmp`.
- `elan which lean` e `elan which lake`: falham para o destino definitivo.
- Shims `elan`, `lean` e `lake`: não estão no PATH desta sessão.
- Mathlib: não configurado; revisão exata não resolvida.
- `lake-manifest.json` SHA-256:
  `F61F111EEE3C5856DD6187087B1574BDCB8A52B817F28EAD5254962EDC6C0D73`.

O smoke build passou com 12 jobs pelo caminho `.tmp`, mas o ambiente ainda não
é classificado como reprodutível.

## Bloqueio LAB-0.6

O commit `4b314d7360404385a91366449087779cccf87d4d` não contém
`04_FORMAL_RESEARCH_LAB/`; o diretório inteiro aparece como não rastreado.
Consequentemente, `git show HEAD:04_FORMAL_RESEARCH_LAB/lab0-result.json`
falha e não existe uma versão histórica congelável desse artefato no Git.
O protocolo exige parar antes de criar o commit da reconciliação.

## Estado de RH-NOGO-001

```text
SCOPED
NOT_AUTHORIZED
NO_EXECUTION
```

Nenhuma sessão de Riemann foi aberta e nenhuma análise espectral foi iniciada.

## Próxima ação única

Resolver a ausência do commit-base do LAB-0 e reabrir o LAB-0.6.

## Ações proibidas

- abrir ou executar `RH-NOGO-001`;
- construir operadores ou pesquisar no-go theorems;
- criar os módulos Lean do benchmark antes do gate de execução;
- usar o diretório `.tmp` como localização canônica;
- alterar qualquer arquivo fora de `04_FORMAL_RESEARCH_LAB/`;
- usar `sorry`, `admit`, axioma local ou `unsafe`;
- interpretar smoke build como verificação do benchmark;
- iniciar automaticamente a etapa seguinte.

## Ordem de retomada

1. `LAB_STATE.md`
2. `AGENTS.md`
3. `05_FORMAL/specifications/LAB-BENCH-001_STATUS.yaml`
4. `05_FORMAL/specifications/LAB-BENCH-001.md`
5. `01_PORTFOLIO/RESEARCH_QUEUE.yaml`
6. último arquivo em `09_SESSIONS/`

## Histórico recente

- `2026-07-28`: LAB-0 técnico passou.
- `2026-07-28`: smoke build passou com Lean 4.32.2 pelo caminho `.tmp`.
- `2026-07-28`: `LAB-BENCH-001` foi incorretamente marcado `VERIFIED`.
- `2026-07-28`: LAB-0.5 corrigiu o gate para `LAB-BENCH-001 / BLOCKED`.
- `2026-07-28`: nenhuma frente Clay foi iniciada.
- `2026-07-28`: LAB-0.6 interrompido por `LAB06_RECONCILIATION_DIFF_UNRESOLVED`;
  o HEAD não contém o laboratório e `lab0-result.json` não tem versão histórica
  em `git show HEAD`.
