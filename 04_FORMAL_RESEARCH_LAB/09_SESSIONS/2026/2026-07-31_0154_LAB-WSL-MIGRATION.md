---
session_id: 2026-07-31_0154_LAB-WSL-MIGRATION
started_at: 2026-07-31T00:58:00-03:00
ended_at: 2026-07-31T01:54:32-03:00
agent: claude-opus-5
git_commit_before: 634de1c3aa915fcb0ccc5f27d6fe6194368535a4
git_commit_after: null
active_work_item: LAB-BENCH-001
authorized_action: LAB_BENCHMARK_EXECUTION_AUTHORIZED
result_status: LAB_WSL_REPOSITORY_MIGRATION_PASS
files_created:
  - "04_FORMAL_RESEARCH_LAB/lab-wsl-migration-result.json"
  - "04_FORMAL_RESEARCH_LAB/09_SESSIONS/2026/2026-07-31_0154_LAB-WSL-MIGRATION.md"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/LAB-WSL-cache-get.log"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/LAB-WSL-lake-build.log"
files_modified:
  - "04_FORMAL_RESEARCH_LAB/LAB_STATE.md"
  - "04_FORMAL_RESEARCH_LAB/CHANGELOG.md"
  - "04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/LEAN_ENVIRONMENT.md"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/lean-toolchain"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/lakefile.toml"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/lake-manifest.json"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/specifications/LAB-BENCH-001.md"
  - "04_FORMAL_RESEARCH_LAB/05_FORMAL/specifications/LAB-BENCH-001_STATUS.yaml"
  - "04_FORMAL_RESEARCH_LAB/06_COMPUTATION/python/pyproject.toml"
  - "04_FORMAL_RESEARCH_LAB/10_TOOLS/labctl.py"
commands_executed:
  - "git status --short / git rev-parse HEAD / git tag --list (em /mnt/d)"
  - "git diff --ignore-cr-at-eol --stat (em /mnt/d)"
  - "git clone /mnt/d/TamesisTheoryCompleteResearchArchive /home/linuxdev/projects/TamesisTheoryCompleteResearchArchive"
  - "git switch -c lab/wsl-lean-migration"
  - "lake update mathlib"
  - "lake exe cache get"
  - "lake env lean TamesisLab/Tests/MathlibMinimalSmoke.lean"
  - "lake env lean TamesisLab/Tests/MathlibTacticSmoke.lean"
  - "lake env lean TamesisLab/Tests/MathlibSmoke.lean"
  - "lake build"
  - "grep -RInE '\\b(sorry|admit|axiom|unsafe)\\b' --include='*.lean' --exclude-dir='.lake' ."
  - "python3 -m pytest -q (em 06_COMPUTATION/python)"
  - "python3 10_TOOLS/labctl.py status"
  - "python3 10_TOOLS/labctl.py validate"
tests_executed:
  - "MathlibMinimalSmoke: exit 0"
  - "MathlibTacticSmoke: exit 0"
  - "MathlibSmoke: exit 0"
  - "lake build: exit 0, 8670 jobs"
  - "pytest: 2 passed"
  - "labctl validate: PASS, errors []"
claims_changed: []
gaps_opened: []
gaps_closed:
  - "LAB011_NO_CACHE_BACKED_PAIR_FOUND"
next_single_action: "Executar o benchmark formal LAB-BENCH-001 conforme sua especificação canônica."
---

## Objetivo autorizado

Migrar o repositório Tamesis congelado do disco Windows para o filesystem
Linux do WSL, alinhar o projeto Lean ao par já validado e preparar
`LAB-BENCH-001` para execução. Nenhuma hipótese científica, benchmark, Clay ou
Riemann foi executada.

## Estado inicial

`LAB-BENCH-001` estava `BLOCKED` desde LAB-0.6. O bloqueio final registrado era
`LAB011_NO_CACHE_BACKED_PAIR_FOUND`: sob o runtime Windows nativo, o cache
Mathlib deixava 2.583 objetos em estado `.part`/404 e a transferência nunca
concluía. O par declarado era Lean/Mathlib `v4.32.2`.

Um smoke test descartável em `/home/linuxdev/projects/tamesis-lean-smoke` já
havia comprovado que Lean, Lake e Mathlib funcionam nativamente no Ubuntu
24.04 sob WSL2, com o par `v4.33.0-rc1`.

## Trabalho executado

### 1. Validação do repositório congelado

HEAD `634de1c3aa915fcb0ccc5f27d6fe6194368535a4`, branch `complete-archive-v1`,
tag `lab-native-windows-paused` apontando para o mesmo commit.

Sob git Linux em DrvFs, 2454 arquivos apareceram como modificados. O diff
acusou 2.178.795 inserções contra 2.178.795 deleções — contagem idêntica,
reescrita integral de cada arquivo. `git diff --ignore-cr-at-eol --stat`
produziu saída vazia, provando que a diferença é apenas de terminador de linha:
a worktree Windows está em CRLF e os blobs em LF, e o `core.autocrlf` do git
Windows não se aplica ao git do WSL. Nenhum arquivo estava staged.

O repositório foi classificado como **content-clean**. O clone lê o object
database, não a worktree, e portanto não é afetado.

### 2. Clone para o filesystem Linux

4.063 arquivos em 24,875 s, contra vários minutos que o mero `git status`
levava em `/mnt/d`. O clone nasceu com working tree limpo
(`git status --short` retornou zero linhas), confirmando o diagnóstico CRLF de
forma independente.

Os diretórios não-rastreados `.claude/` e `AJUSTE_FINO/` não migraram, por
não estarem sob controle de versão.

Branch `lab/wsl-lean-migration` criada.

### 3. Alinhamento do projeto Lean

`lean-toolchain` passou a declarar `leanprover/lean4:v4.33.0-rc1`.
`lakefile.toml` passou a requerer Mathlib pela tag `v4.33.0-rc1`, no formato de
escopo `leanprover-community` usado pelo projeto oficial validado.

`lake update mathlib` concluiu com exit 0 em 35m37s, incluindo o clone completo
do `mathlib4`. O manifesto resolveu a revisão
`79d0395a1825a6264ad5d269e35e60537518955e`, idêntica à do smoke test.

Nenhum artefato de build foi copiado do projeto descartável.

### 4. Cache

O hook pós-update do `lake update` já descomprimiu 8.642 arquivos em 223.499 ms
sem nenhum download, porque o cache global `~/.cache/mathlib` já continha os
`.ltar` da mesma revisão. O `lake exe cache get` explícito confirmou o estado em
6,581 s: exit 0, "No files to download", 8.643 arquivos já descomprimidos.

Nenhum timeout, nenhum erro de curl, uname, chmod ou leantar.

### 5. Smokes e build

| Arquivo | Import | Exit | Duração |
|---|---|---|---|
| `MathlibMinimalSmoke.lean` | `Mathlib.Data.Nat.Basic` | 0 | 3,975 s |
| `MathlibTacticSmoke.lean` | `Mathlib.Tactic` | 0 | 25,834 s |
| `MathlibSmoke.lean` | `Mathlib` | 0 | 16,957 s |

Nenhum smoke precisou ser criado: os três já existiam e ambos os módulos
Mathlib importados continuam presentes em `v4.33.0-rc1`.

`lake build` concluiu 8.670 jobs com exit 0 em 46,755 s. O alvo `TamesisLab`
importa `TamesisLab.Tests.MathlibSmoke`, portanto o build exercita Mathlib
integralmente.

### 6. Defeitos de ferramenta corrigidos

Quatro defeitos pré-existentes impediam o gate de fechar. Nenhum é
consequência da migração; três são artefatos da rota Windows.

1. **`labctl.lean_check` usava `USERPROFILE`**, variável exclusiva do Windows.
   Sob Linux, `Path(os.environ.get("USERPROFILE", ""))` produz caminho relativo
   inexistente, `installed_toolchains` fica vazio e a função retorna `BLOCKED`.
   Passou a resolver `ELAN_HOME`, depois `USERPROFILE`, depois `HOME`.

2. **`labctl validate` não podia retornar `PASS` em nenhuma circunstância.**
   `validate()` exige `lean_result["status"] == "PASS"`, mas `lean_check()` só
   retornava `"BLOCKED"` ou `"NOT_RUN"`. O registro histórico
   `lab0-result.json` confirma: `LAB0_LEAN_ENVIRONMENT_FAILED` com `errors: []`.
   `lean_check` passa a retornar `PASS` quando há toolchain estável não-`.tmp`
   resolvido no PATH. A função continua sem jamais invocar `lake build`.

3. **`LAB_STATE.canonical_commit` continha SHA de 7 caracteres**, violando o
   padrão `^[0-9a-f]{40}$` de `lab-state.schema.json`. Substituído pelo SHA
   completo do commit congelado.

4. **O allowlist de `authorized_action` não continha
   `LAB_BENCHMARK_EXECUTION_AUTHORIZED`.** A entrada literal foi acrescentada,
   sem wildcard nem relaxamento genérico, sob autorização explícita do
   mantenedor.

Além disso, **o pacote Python não era importável**: `tamesis_lab` usa layout
`src/` e só era alcançável por um install editable não versionado na máquina
Windows. `python3 -m pytest` a partir da raiz do laboratório falhava com
`ModuleNotFoundError`. Corrigido de forma reproduzível com
`pythonpath = ["src"]` em `06_COMPUTATION/python/pyproject.toml`; a invocação
canônica passa a ser `python3 -m pytest` executado em `06_COMPUTATION/python`.

### 7. Validação final

`pytest`: 2 passed, exit 0 — igual ao registro histórico do LAB-0.

`labctl validate`: `PASS`, `errors: []`, `warnings: []`. As 12 mudanças do
working tree estão todas sob `04_FORMAL_RESEARCH_LAB/`. `legacy_files_modified`
0, `research_claims_promoted` 0, `new_mathematical_proofs_executed` 0.
`RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

Tokens proibidos nos fontes do laboratório: `sorry` 0, `admit` 0, `axiom` 0,
`unsafe` 0.

## Evidências

`04_FORMAL_RESEARCH_LAB/lab-wsl-migration-result.json`
`04_FORMAL_RESEARCH_LAB/05_FORMAL/LEAN_ENVIRONMENT.md`
`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/LAB-WSL-cache-get.log`
`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/LAB-WSL-lake-build.log`

## Falhas

Uma falha real ocorreu e foi corrigida dentro do gate: `python3 -m pytest`
executado a partir de `04_FORMAL_RESEARCH_LAB` retornou exit 2 com
`ModuleNotFoundError: No module named 'tamesis_lab'`. A causa é o layout `src/`
combinado à ausência de install versionado, não a migração.

Nenhuma outra falha ocorreu. Nenhum comando foi repetido após falha.

## Decisões

- O par Lean/Mathlib canônico passou de `v4.32.2` para `v4.33.0-rc1`. Nenhuma
  formalização científica dependia do par anterior, então nada foi perdido.
  `v4.32.2` não é ressuscitado.
- A rota nativa Windows fica `FROZEN / HISTORICAL / NOT_OPERATIONAL`.
- `/mnt/d/TamesisTheoryCompleteResearchArchive` permanece apenas como origem
  histórica do clone e não recebe execução.
- Correções de ferramenta foram tratadas como parte da migração do runtime, e
  não como um novo gate de depuração de ambiente.

## O que não foi feito

- Nenhum arquivo `Benchmark/*.lean` foi criado.
- O benchmark `LAB-BENCH-001` não foi executado.
- `RH-NOGO-001` não foi aberto.
- Nenhum arquivo fora de `04_FORMAL_RESEARCH_LAB/` foi modificado.
- Nenhuma claim foi promovida e nenhuma prova matemática nova foi produzida.
- As skills de `AJUSTE_FINO/` não foram importadas; isso pertence ao gate
  separado `LAB-AGENT-SKILLS-IMPORT`.

## Próxima ação única

Executar o benchmark formal LAB-BENCH-001 conforme sua especificação canônica.

## Handoff

A infraestrutura está encerrada. O runtime canônico é Ubuntu 24.04 no WSL2, em
`/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive`, com Lean
`v4.33.0-rc1`, Lake `5.0.0-src+62eed1d` e Mathlib
`79d0395a1825a6264ad5d269e35e60537518955e`. Cache, três smokes, build completo,
testes Python e validador estruturais passam. `LAB-BENCH-001` está `READY` com
`LAB_BENCHMARK_EXECUTION_AUTHORIZED`. A próxima sessão é de formalização.
