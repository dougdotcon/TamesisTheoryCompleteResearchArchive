# Changelog do laboratório formal

## Unreleased

### Added

- Camada isolada `04_FORMAL_RESEARCH_LAB`.
- Estado canônico de retomada, governança, fila e mapas.
- Esqueletos formais Lean/Python sem alegações novas.
- Ferramenta de continuidade `labctl`.
- Especificação e estado de fases de `LAB-BENCH-001`.
- Benchmark documental de rastreabilidade de Poincaré.

### Changed

- O diagnóstico Lean separa smoke build de disponibilidade reprodutível.
- O benchmark de Poincaré está limitado a documentação histórica.

### Corrected

- `LAB-BENCH-001` deixou de ser classificado como `VERIFIED`: somente o smoke
  build passou.
- O `active_work_item` voltou de `RH-NOGO-001` para `LAB-BENCH-001`.
- A autorização foi reconciliada para
  `LAB_BENCHMARK_FORMALIZATION_PREPARATION_AUTHORIZED`.
- Um diretório `.tmp` deixou de ser tratado como toolchain canônico.
- A autoridade de documentos históricos permanece subordinada à precedência
  documental e às auditorias canônicas.

### Retracted

- Foi retirada a inferência operacional de que o smoke build concluiu
  `LAB-BENCH-001`.
- Nenhuma retratação matemática nova foi criada.

### Verified

- `LEAN_ENVIRONMENT_DISCOVERY: PASS`.
- `LEAN_SMOKE_BUILD: PASS` com 12 jobs usando Lean 4.32.2.
- O LAB-0 técnico e seus validadores permanecem `PASS`.

### Blocked

- `LEAN_TOOLCHAIN_AVAILABILITY: PARTIAL`: o toolchain definitivo não existe.
- `LAB_BENCHMARK_PREPARATION: PARTIAL`: revisão Mathlib ainda não fixada.
- `LAB_BENCHMARK_EXECUTION` e `LAB_BENCHMARK_VERIFICATION`: `NOT_STARTED`.
- `RH-NOGO-001`: `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- LAB-0.6 interrompido por `LAB06_RECONCILIATION_DIFF_UNRESOLVED`: o HEAD
  inicial não contém o laboratório e o resultado histórico do LAB-0 não pode
  ser recuperado por Git.
- Um processo externo criou `363be8a`; ele contém a camada formal e o artefato
  LAB-0.5, mas não é um commit exclusivo desta sessão.
- LAB-0.6 interrompido por `LAB_LEAN_TOOLCHAIN_INSTALLATION_FAILED` após o
  comando oficial do Elan expirar em 184 segundos.
- A instalação foi posteriormente concluída pelo Elan; o toolchain agora é
  definitivo e Mathlib está fixada no commit v4.32.2.
- O smoke import Mathlib excedeu 600 segundos em compilação local e o gate
  terminou como `LAB_MATHLIB_SMOKE_BUILD_FAILED`.
