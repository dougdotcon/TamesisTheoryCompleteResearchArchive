# Changelog do laboratório formal

## FOUND-SEMIGROUP-001 — 2026-07-31

### Added

- Frente de semigrupos formalizada:
  `TamesisLab/Foundations/Semigroups/{Basic,Regime3,Theorems,Action,Audit}.lean`,
  agregador `Semigroups.lean` e teste `Tests/FoundSemigroup001.lean`.
- Modelo C3: `Regime3` (3 regimes), `Shift3` (3 transições),
  `Shift3.apply`, `Shift3.comp`; 12 teoremas FOUND-SG-002..013
  (associatividade, identidades, lei da ação, ciclo, cardinalidades,
  distinção, fidelidade, transitividade); FOUND-SG-001 (fechamento)
  registrado como garantido por construção.
- Instâncias `Monoid Shift3` e `MulAction Shift3 Regime3` criadas após as
  leis; camada abstrata reutiliza `SemigroupAction`/`MulAction` da Mathlib
  — nenhuma duplicata local (stop condition respeitada).
- Documentação da frente `02_FOUNDATIONS/03_SEMIGROUPS/`:
  TARGET_RESULT, DEFINITIONS (convenção de composição explícita),
  ASSUMPTIONS, KNOWN_RESULTS_MATRIX (separação álgebra padrão / modelo C3 /
  vocabulário Tamesis não justificado), DEPENDENCY_DAG, GAP_REGISTER,
  LEAN_MAP, THEOREM_MAP.
- Auditoria computacional
  `06_COMPUTATION/python/experiments/found_semigroup_001_audit.py`
  (`COMPUTATIONAL_FINITE_CROSS_CHECK_ONLY`): 7 verificações exaustivas PASS
  e 4 fixtures negativas com falha esperada observada (não associatividade,
  ação incompatível, não transitividade, não fidelidade).
- Claim `FOUND-SG-FORMAL-001` (`F`, `formal_foundations`, VERIFIED); nenhuma
  claim científica promovida.

### Changed

- `FOUND-SEMIGROUP-001`: `READY` → `VERIFIED`.
- `active_work_item`: `FOUND-SEMIGROUP-001` → `RH-NOGO-001` (`SCOPED`), com
  autorização exclusiva de preparação
  (`RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED`); a execução da prova
  permanece `NOT_AUTHORIZED / NO_EXECUTION`.
- `labctl`: entradas literais `RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED`
  no allowlist e `RH-NOGO-001` como item ativo condicionado a
  `FOUND-SEMIGROUP-001` `VERIFIED`; sem wildcard.
- Instâncias `Fintype` de `Regime3`/`Shift3` escritas manualmente: o derive
  handler da revisão fixada falha sob imports mínimos (registrado em
  `LEAN_MAP.md`).

### Verified

- `lake build` PASS, 8.683 jobs; teste isolado PASS; tokens proibidos zero.
- Auditoria Python PASS; pytest 2 passed; `labctl validate` PASS.
- `FOUND_SEMIGROUP_001_VERIFIED`.

### Blocked

- `RH-NOGO-001`: somente preparação autorizada; prova não autorizada.

## LAB-BENCH-001 — 2026-07-31

### Added

- Módulos Lean do benchmark: `TamesisLab/Benchmark/{Core,Structures,Relations,MathlibInterop}.lean`,
  agregador `TamesisLab/Benchmark.lean` e teste
  `TamesisLab/Tests/BenchmarkSmoke.lean` — 11 definições e 15 teoremas
  elementares conhecidos, todos referenciados no teste.
- Matriz de rastreabilidade `05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md`
  ligando cada requisito BENCH-* a arquivo, assinatura e método de prova.
- Claim de infraestrutura `BENCH-INFRA-001` (`evidence_level: F`,
  `domain: formal_infrastructure`); nenhuma claim científica criada ou
  promovida.
- Skills locais de agente copiadas de `AJUSTE_FINO/` para `.claude/skills`
  (24 operacionais, 1 incompleta), fora do controle de versão via
  `.git/info/exclude`.

### Changed

- `LAB-BENCH-001`: `READY` → `VERIFIED`; todas as seis fases `PASS`.
- `active_work_item`: `LAB-BENCH-001` → `FOUND-SEMIGROUP-001` (`READY`);
  autorização passou a `FOUNDATIONS_EXECUTION_AUTHORIZED`.
- `labctl` atualizado para o novo estágio do gate: entrada literal
  `FOUNDATIONS_EXECUTION_AUTHORIZED` no allowlist; `FOUND-SEMIGROUP-001`
  aceito como item ativo somente com `LAB-BENCH-001` `VERIFIED`; `VERIFIED`
  do benchmark exige fases de execução e verificação `PASS`; fases de
  execução/verificação aceitam `NOT_STARTED` ou `PASS`, com verificação
  condicionada à execução.

### Verified

- `lake build` PASS com 8.676 jobs; `BenchmarkSmoke` PASS individual.
- Tokens proibidos: zero nos fontes do laboratório.
- pytest: 2 passed; `labctl validate`: PASS sem erros.
- `LAB_BENCH_001_VERIFIED`.

### Blocked

- `FOUND-SEMIGROUP-001`: `READY`, não executado nesta sessão.
- `RH-NOGO-001`: `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

## LAB-WSL-MIGRATION — 2026-07-31

### Changed

- O runtime canônico do laboratório passou de Windows nativo para Ubuntu 24.04
  no WSL2. Diretório canônico:
  `/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive`.
- O par Lean/Mathlib canônico passou de `v4.32.2` para `v4.33.0-rc1`. Mathlib
  fixada em `79d0395a1825a6264ad5d269e35e60537518955e`. Nenhuma formalização
  científica dependia do par anterior.
- `05_FORMAL/lean/lean-toolchain` e `05_FORMAL/lean/lakefile.toml` foram
  alinhados ao par validado; `lake update mathlib` regenerou o manifesto.
- `LAB-BENCH-001` passou de `BLOCKED` para `READY`; a autorização passou a
  `LAB_BENCHMARK_EXECUTION_AUTHORIZED`.

### Corrected

- `labctl.lean_check` usava `USERPROFILE`, variável exclusiva do Windows, e não
  localizava o diretório de toolchains sob Linux. Passou a resolver
  `ELAN_HOME`, depois `USERPROFILE`, depois `HOME`.
- `labctl validate` não podia retornar `PASS` em nenhuma circunstância, porque
  exigia `lean_check()["status"] == "PASS"` e essa função só retornava
  `BLOCKED` ou `NOT_RUN`. O registro histórico `lab0-result.json` mostra
  `LAB0_LEAN_ENVIRONMENT_FAILED` com `errors: []`. `lean_check` passa a
  retornar `PASS` quando há toolchain estável não-`.tmp` resolvido no PATH,
  sem jamais invocar build.
- `LAB_STATE.canonical_commit` continha um SHA abreviado de 7 caracteres,
  violando o padrão de 40 exigido por `lab-state.schema.json`.
- O allowlist de `authorized_action` em `labctl` recebeu a entrada literal
  `LAB_BENCHMARK_EXECUTION_AUTHORIZED`, sem wildcard nem relaxamento genérico.

### Verified

- `LEAN_ENVIRONMENT_DISCOVERY: PASS`.
- `LEAN_TOOLCHAIN_AVAILABILITY: PASS` com toolchain definitivo.
- `LEAN_SMOKE_BUILD: PASS`: os três smokes de Mathlib compilaram.
- `LAB_BENCHMARK_PREPARATION: PASS`.
- `lake build` concluiu 8.670 jobs.
- Tokens proibidos nos fontes do laboratório: zero.

### Blocked

- `LAB_BENCHMARK_EXECUTION` e `LAB_BENCHMARK_VERIFICATION`: `NOT_STARTED`.
- `RH-NOGO-001`: `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- A rota nativa Windows fica `FROZEN / HISTORICAL / NOT_OPERATIONAL` na tag
  `lab-native-windows-paused`.

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
- LAB-0.7 confirmou checkout Mathlib compatível com o manifesto, mas o comando
  oficial `cache get` falhou com recurso ausente; o smoke direto acusou
  `MISSING_OLEAN` e o alvo isolado excedeu 600 segundos.
- LAB-0.7 terminou como `LAB07_CACHE_UNAVAILABLE_FOR_REVISION`; nenhum benchmark
  ou problema Clay foi executado.
- LAB-0.8 confirmou que `v4.32.2` é tag Mathlib oficial e compatível com o
  toolchain declarado, mas o cache falha com exceção Windows de processo antes
  de informar URL/HTTP. O probe isolado de `v4.32.1` reproduziu a falha.
- LAB-0.8 terminou como `LAB08_NO_REPRODUCIBLE_PAIR_FOUND`; nenhuma migração
  canônica foi executada.
- LAB-0.9 identificou que o erro Windows 2 vinha da chamada interna a
  `uname.exe`, ausente no PATH enquanto o cache avaliava curl 7.55.1.
- A precedência temporária de `Git/usr/bin` removeu o erro de criação de
  processo, mas os downloads curl permaneceram presos por 600 segundos; o gate
  terminou como `LAB09_CAUSE_STILL_UNRESOLVED`.
- LAB-0.10 separou o cURL Windows 7.55.1 do cURL Git 8.21.0 e confirmou que
  `Git/usr/bin` sozinho não altera a seleção do cURL.
- A precedência interna do cache passou a usar o cURL Git verificado; 398
  `.ltar` foram transferidos e a contagem `.olean` subiu para 1.173, mas 2.583
  objetos permaneceram `.part`/404 e a transferência não concluiu.
- LAB-0.10 terminou como `LAB010_CACHE_TRANSFER_STALLED`.
