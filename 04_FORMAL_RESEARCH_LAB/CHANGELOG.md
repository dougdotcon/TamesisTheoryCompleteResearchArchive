# Changelog do laboratório formal

## FOUND-CYCLE-DETECTION-001-SPECIFICATION-REVIEW - 2026-07-31

### Renamed

- **`prefixIndex` -> `baseIndex`**, 40 ocorrencias em 8 documentos.
  `baseIndex` eh o **indice-base da igualdade**
  `f^[baseIndex + period] x = f^[baseIndex] x`, e nao o menor indice de
  entrada. Nomes proibidos: `prefixIndex`, `entryIndex`, `tailLength`,
  `cycleEntry`.
- **Registros historicos NAO foram reescritos.** O JSON do gate anterior,
  sua sessao e o changelog preservam `prefixIndex`; a decisao esta
  marcada como **superada** em `DATA_MODEL.md` e na tabela de
  renomeacoes. A governanca viva foi atualizada.

### Measured

- Probe descartavel em `/tmp`, 28 s, **zero erros**, removido ao final.
- **Os cinco casos obrigatorios bateram**: `Fin 1` id -> `<0,1>`;
  `Bool` id -> `<0,1>`; `Bool` not -> `<0,2>`; `Fin 3` cauda -> `<2,1>`;
  `Fin 4` cauda e ciclo de dois -> `<2,2>`. Nenhuma funcao e nenhuma
  ordem foi alterada para satisfazer expectativa.
- Enumeracao: `cycleCandidates 0 = []` e `1 = [<0,1>]` por `rfl`;
  comprimentos 6, 10 e 15 para n = 3, 4 e 5; fronteira de soma medida por
  filtro.

### Findings

- **A instancia `Decidable` precisa ser DECLARADA.** `Valid` eh um `def`
  e a resolucao de instancias nao o desdobra; sem
  `CycleWitness.decidableValid` o `decide` nao elabora. Ausente da
  especificacao inicial; acrescentada as assinaturas congeladas.
- **Pegada axiomatica NAO eh noncomputabilidade.**
  `detectCycleWitness?` carrega `[propext, Classical.choice, Quot.sound]`
  — origem localizada em `Fintype.card` e `Finset.univ`. `cycleCandidates`,
  `List.range`, `find?` e `Nat.iterate` nao dependem de axioma algum.
  Criterio reformulado: nao `noncomputable`, `#eval` funciona, nenhum
  `Classical.choose` produzindo dado. Os tres confirmados.
- **`ValidAt` nao resolveria** a pegada: o detector calcula
  `Fintype.card X` de qualquer modo. Permanece `DEFERRED`.
- `propagates` **alinhada** a ordem de argumentos de
  `collision_propagates`: hipotese primeiro, `k` depois.
- Rota unica de completude: `List.find?_isSome` + `Option.isSome_iff_exists`.

### Frozen

- `CycleWitness` com dois naturais; `Valid`; `cycleCandidates`;
  `mem_cycleCandidates_iff`; `detectCycleWitness?`; soundness;
  completeness; as tres pontes proposicionais. Doze assinaturas publicas
  mais uma instancia.
- `total_wrapper: DEFERRED`, `OPTIONAL_CORE_PENDING_EXECUTION_TEST`. Seis
  dos sete criterios confirmados; o setimo exigiria provar a completude no
  probe. API v1 permanece `Option`. `getD` com certificado falso
  **proibido**.

### Not done

- **0** arquivos Lean no repositorio, **0** provas, **0** implementacao
  permanente, **0** `lake build`, **0** claims (ledger em **19**), **0**
  legado, **0** de `RH-NOGO-001`, **0** matematicos das duas fundacoes
  encerradas. Probe **removido**.

### Changed

- `canonical_commit`: `ab79032` -> `03e1ec3`.
- `specification_status` -> `APPROVED`.
- `authorized_action` -> `FOUND_CYCLE_DETECTION_001_FORMALIZATION_AUTHORIZED`
  (`DEC-018`, uma entrada literal, sem wildcard).

### Result

- `FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_APPROVED`. Dezenove
  lacunas reclassificadas: 6 resolvidas, 5 prontas para formalizacao, 1
  para auditoria de viabilidade, 6 diferidas, 1 bibliografica.

## FOUND-CYCLE-DETECTION-001-SPECIFICATION - 2026-07-31

### Frozen

- **`BOUNDED_CERTIFICATE_SEARCH`** como algoritmo primario. **Nao eh
  Floyd.** O argumento decisivo: o contrato do certificado coincide
  TERMO A TERMO com a conclusao de `exists_bounded_iterate_collision`,
  ja `VERIFIED`. A completude deixa de ser prova nova e passa a ser
  transporte.
- **`CycleWitness`** com **dois** naturais, `prefixIndex` e `period`.
  `entryPoint` **rejeitado** — derivavel por `f^[prefixIndex] x0`. A
  estrutura NAO eh parametrizada por `X`.
- Semantica vinculante: `prefixIndex` eh **indice-base de colisao
  certificada**, NAO o menor indice de entrada — o nome `entryIndex` fica
  proibido. `period` eh **periodo positivo testemunhado**, NAO
  `minimalPeriod`.

### Audited

- **31 APIs confirmadas** com assinatura impressa pelo proprio Lean, via
  sonda temporaria em `/tmp` (removida ao final). **Dois nomes do gate
  divergiam do checkout**: `List.find?_eq_some` ->
  `List.find?_eq_some_iff_append`; `Function.iterate` -> `Nat.iterate`.
  `List.get?` e `List.getElem?` **nao existem** como constantes.
- Fronteira `mu + lam = n` verificada **por avaliacao**: `n = 3` produz
  `(0,3), (1,2), (2,1)`; `n = 1` produz `[(0,1)]`.
- Predicado executavel: **Opcao A**, `decide`. A instancia `Decidable` da
  conjuncao completa foi obtida por `inferInstance` para `X = Bool`.
  `Bool` e `Prop` **nao** ficam congelados simultaneamente.

### Deviations

- **`mem_cycleCandidates_iff` NAO eh dependencia da soundness** — as tres
  cotas vivem dentro de `Valid`. Fortificacao, nao lacuna: a soundness
  sobrevive a uma troca de algoritmo. O DAG do gate foi corrigido nesse
  ramo.
- **Totalizacao `DEFERRED`.** Quatro das cinco condicoes tem argumento
  favoravel; a quinta — `#eval` funcionar — so eh verificavel
  implementando. API v1 permanece baseada em `Option`.

### Boundary

- `DecidableEq X` eh sobre **estados**; `periodicOrbit` vive em
  `Cycle X`. Nenhuma decidibilidade sobre `Cycle X` eh assumida.
  `DecidableEq` fica SOMENTE na camada do detector — as tres pontes
  proposicionais nao a recebem.
- Terminacao **estrutural**: lista finita + `List.find?`. Sem `fuel`, sem
  recursao bem fundada, sem `Classical.choice`, sem `Classical.choose`.
- Casa dos pombos consumida **uma unica vez**, em `FOUND-SEMIGROUP-002`;
  `Fintype.exists_ne_map_eq_of_card_lt` NAO aparecera nesta frente.
- `complexity_status: NOT_FORMALIZED`; minimalidade de `mu` e de `lam`
  **nao autorizadas**; `mathematical_novelty` e `algorithmic_novelty`
  ambas `NONE`.

### Not done

- **0** arquivos Lean permanentes, **0** provas, **0** algoritmos
  implementados, **0** `lake build`, **0** claims (ledger em **19**),
  **0** arquivos de legado, **0** de `RH-NOGO-001`, **0** matematicos de
  `FOUND-SEMIGROUP-002` e de `FOUND-FUNCTIONAL-GRAPH-001`. Sonda
  temporaria **removida**.

### Changed

- `canonical_commit`: `49924c3` -> `ab79032`, no preflight.
- `work_status` -> `READY`; `specification_status: READY_FOR_REVIEW`.
- `authorized_action` ->
  `FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED`
  (`DEC-017`, uma entrada literal no allowlist, sem wildcard).

### Result

- `FOUND_CYCLE_DETECTION_001_SPECIFICATION_READY`. Vinte e um documentos,
  dezenove lacunas, sete casos de teste, dez teoremas `CORE` e tres
  `OPTIONAL_CORE`.

## PORTFOLIO-REVIEW-CYCLE-DETECTION - 2026-07-31

### Selected

- **`FOUND-CYCLE-DETECTION-001`** — *Executable Cycle Detection for
  Finite Deterministic Systems*, criado como `SCOPED`. Ataca a lacuna
  registrada no fechamento anterior: `periodicOrbit` eh **noncomputavel**,
  e o resultado proposicional nao entrega algoritmo, `mu`, `lambda`,
  ponto de entrada, lista do ciclo nem certificado computavel.
- **Duplicata: NAO encontrada.** Zero ocorrencias de `CYCLE-DETECTION` ou
  `detectCycle`. Floyd e Brent aparecem em tres documentos, e nos tres
  como material declarado **fora de escopo**.

### Audited

- **Seis** itens nao executados reavaliados com os nove campos exigidos.
  Todos rejeitados. `TOE-INTERFACE-001` por motivo estrutural: depende de
  `RH-NOGO-001`, congelada — dependencia **bloqueante**.
- Nenhuma pesquisa matematica das frentes rejeitadas foi iniciada.

### Planned, not built

- Estrutura candidata `CycleDetectionResult` com seis invariantes,
  **nao congelada**.
- Algoritmos comparados: `PRIMARY: FLOYD_WITH_FUEL`,
  `REFERENCE_BASELINE: VISITED_TABLE`, `DEFERRED: BRENT`. **Nenhum
  implementado.**
- Risco principal: **terminacao**. Quatro camadas que a especificacao deve
  manter separadas — terminacao, correcao, complexidade e equivalencia
  com a API proposicional.
- Seis casos de teste (`CD-CE-001..006`) com valores **candidatos**;
  dezesseis lacunas (`CD-GAP-001..016`), **nenhuma fechada**.

### Boundary

- `DecidableEq X` eh sobre **estados**; `periodicOrbit` vive em
  `Cycle X`, e nenhuma decidibilidade sobre `Cycle X` eh assumida,
  requerida ou construida. A ponte eh **proposicional**.
- Minimalidade de `mu` e de `lambda`, complexidade assintotica formal,
  bacia completa e enumeracao global: **nao autorizadas**.
- `mathematical_novelty: NONE`. Deteccao de ciclos em sistemas
  deterministicos finitos eh material classico.

### Governance

- Tres edicoes minimas e literais em `10_TOOLS/labctl.py`, **sem
  wildcard**: `DEC-014` (gate sequence), `DEC-015` (dependencia de
  `FOUND-FUNCTIONAL-GRAPH-001` VERIFIED) e `DEC-016` (entrada de
  allowlist). `PORTFOLIO_REVIEW_AUTHORIZED` ja existia.
- `canonical_commit`: `3f6d7e7` -> `49924c3`, no preflight.
- `authorized_action` ->
  `FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
  Formalizacao, extracao e integracao permanecem **nao autorizadas**.

### Not done

- **0** arquivos Lean, **0** provas, **0** algoritmos, **0** `lake build`,
  **0** claims promovidas (ledger em **19**), **0** arquivos de legado,
  **0** de `RH-NOGO-001`, **0** matematicos de `FOUND-SEMIGROUP-002` e de
  `FOUND-FUNCTIONAL-GRAPH-001`. Pasta de especificacao **nao** criada.

### Result

- `PORTFOLIO_REVIEW_APPROVED_CYCLE_DETECTION_SELECTED`.

## FOUND-FUNCTIONAL-GRAPH-001-RESULT-REVIEW - 2026-07-31

### Reviewed

- `FGR-001` a `FGR-008`: **todos CONFIRMADOS**. Transitividade revisada
  linha a linha, com o mapa `mx/ny/my/nz` e as testemunhas `(d + mx, nz)`
  e `(mx, d + nz)`.
- **Caso infinito**: `EventuallyMeets` continua relacao de equivalencia
  para tipos infinitos; a existencia de ponto periodico eh FALSA em geral
  (`X = N`, `f n = n + 1`). Nenhum teorema Lean criado para isso.
  `[Fintype X]` aparece SOMENTE em `ComponentCycle.lean`.
- **Caso vazio**: os teoremas recebem `x : X`; com `X` vazio nao existe tal
  termo. Zero hipoteses de `Nonempty`, `Inhabited`, `Finite` ou
  `DecidableEq`.

### Binding caveat

- **A reciproca EXIGE ambos os pontos periodicos.** Dois pontos NAO
  periodicos tem, ambos, `periodicOrbit = Cycle.nil`; as orbitas vazias
  sao iguais SEM que as trajetorias se encontrem. As hipoteses `hp` e `hq`
  permanecem visiveis na assinatura, e o teste de auditoria verifica
  concretamente `periodicOrbit CE002.f a = Cycle.nil`.
- **Nao formalizado**: nenhum dos seis contraexemplos exibe dois pontos
  nao periodicos que NAO se encontram — em `CE-002` e `CE-004` os
  transitorios SE ENCONTRAM. Construi-lo exigiria um setimo modelo, isto
  eh, matematica nova, proibida neste gate. Registrado como observacao
  estrutural, NAO como fato formalizado.

### API and instance audit

- **16 declaracoes publicas**, exatamente a lista minima. Um unico
  auxiliar, `minimalPeriod_eq_two`, confirmado `private`.
- **5 instancias, ZERO no nucleo matematico.** Todas `Fintype` de
  contraexemplo, em cinco namespaces; `CE005` nao declara instancia.
- **0 conflitos**, zero `Setoid`, zero import de `SimpleGraph`, zero
  `Quotient`. Umbrella nao ambiguo.
- Wrappers relacionais usam `Std.Refl` e `Std.Symm`, os nomes **nao
  depreciados**; `IsTrans` tambem nao esta depreciado. Nenhum exigiu API
  depreciada.
- Novo teste `Tests/FoundFunctionalGraph001InstanceAudit.lean` (exit 0),
  que **nao altera modulo matematico algum** e verifica que, com todas as
  instancias em escopo, a API continua se aplicando a `Bool`.

### Limits

- **`periodicOrbit` eh noncomputavel**: o resultado NAO fornece algoritmo
  executavel de enumeracao de componentes, calculo de `mu` ou deteccao de
  ciclo. Registrado em `REUSE_MATRIX.md`, que separa uso proposicional de
  uso computacional.
- Matriz de reutilizacao: **1** `DIRECT_REUSE`, **7** `REQUIRES_ADAPTER`,
  **2** `CONCEPTUAL_ONLY`. Nenhuma integracao criada.

### Gaps

- **Onze resolvidos, quatro abertos** (`006`, `007`, `012` diferidos;
  `014` bibliografico). Nenhum fechado sem evidencia.

### Not done

- **0** teoremas novos, **0** modulos matematicos alterados, **0** claims
  novas (ledger em **19**), **0** arquivos de legado, **0** de
  `RH-NOGO-001`, **0** de `FOUND-SEMIGROUP-002`.

### Changed

- `canonical_commit`: `f8ccc02` -> `3f6d7e7`, no preflight.
- `result_review: APPROVED`; `extension_status: NOT_AUTHORIZED`.
- `authorized_action` -> `PORTFOLIO_REVIEW_REQUIRED`, que eh **trava de
  governanca**, nao acao autorizada. `NO_ACTION_AUTHORIZED` NAO foi usado.
  Nenhuma entrada nova no allowlist.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_APPROVED`. A frente fica
  encerrada. **O laboratorio nao tem frente ativa.**

## FOUND-FUNCTIONAL-GRAPH-001-FORMALIZATION - 2026-07-31

### Added

- Nucleo Lean em
  `05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/`:
  `Relations`, `PeriodicOrbits`, `ComponentCycle`, `Counterexamples`,
  `Audit`, agregador e dois testes isolados.
  **8 definicoes, 44 teoremas, 5 indutivos, 5 instancias, 0 estruturas.**
- Teorema principal `exists_component_cycle_with_entry_bound`: toda
  trajetoria alcanca um ponto periodico antes de `card X` passos, e todos
  os pontos periodicos do mesmo componente determinam a **mesma orbita
  periodica**. Prova por composicao de cinco passos.
- Corolario opcional `eventuallyMeets_of_periodicOrbit_eq`: **formalizado**,
  nao adiado.
- Seis contraexemplos `FFG-CE-001..006`, todos em Lean.
- `THEOREM_MAP.md`, `PROOF_AUDIT.md`, `COUNTEREXAMPLE_AUDIT.md`,
  `RESULT_BOUNDARY.md`.
- Claim `FUNCTIONAL-GRAPH-COMPONENT-FORMAL-001` (`F`, VERIFIED,
  `mathematical_novelty: NONE`). Ledger: **19 claims**.

### Verified

- `lake build` PASS com **8.726 jobs** em 96 s; dois testes isolados exit 0.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0`.
- `#print axioms`: `iterReachable_trans` **nao depende de axioma algum**;
  `eventuallyMeets_trans` usa apenas `propext` e `Quot.sound`; os demais
  ficam em `propext, Classical.choice, Quot.sound`. Sem `sorryAx`.
- **Arquitetura por hipoteses confirmada pelas assinaturas**:
  `eventuallyMeets_trans` e `periodicOrbit_eq_of_eventuallyMeets` **nao**
  exigem `Fintype X`; `DecidableEq X` **ausente de todos** os teoremas.
- **Zero instancias no nucleo matematico**; as 5 sao `Fintype` dos
  contraexemplos. Zero `Setoid`, zero import de `SimpleGraph`, zero
  `Quotient`.
- Pigeonhole **nao reaplicado** — consumido em `FOUND-SEMIGROUP-002`.
- `decide` **nao** usado sobre igualdade de `periodicOrbit`
  (noncomputavel); `CE003.orbit_eq` sai de
  `periodicOrbit_apply_iterate_eq`. Zero `native_decide`.
- Auditoria de whitespace executada **antes** do `git add`; **um unico
  commit**, sem commit corretivo posterior.

### Corrected

- `le_total` desconhecido sob imports minimos -> `Nat.le_total` (core).
- `Symmetric` **depreciado** -> `Std.Symm`, cujo construtor tem os dois
  elementos **explicitos** (`⟨fun _ _ h => …⟩`).
- `rw` nao fechava por `rfl` em cinco lemas de iteracao: o `rfl` automatico
  usa transparencia reduzivel e nao desdobra funcoes por casamento de
  padrao. `rfl` explicito acrescentado.
- `Mathlib.Tactic.Omega` **nao existe** nesta revisao; o import sugerido
  pelo gate foi omitido. `omega` eh do core.

### Not deferred

- **`FFG-CE-006` na versao FORTE.** O gate permitia adiar a igualdade dos
  periodos minimos; nao foi necessario. `minimalPeriod f a0 =
  minimalPeriod f b0 = 2` provado via `IsPeriodicPt.minimalPeriod_dvd`,
  `minimalPeriod_pos_of_mem_periodicPts`, `Nat.le_of_dvd`,
  `minimalPeriod_eq_one_iff_isFixedPt` e `omega`.

### Blocked

- **A unicidade eh da ORBITA**, nao do ponto (`FFG-CE-005` refuta), nao do
  representante, nao de `mu`, nao do periodo, nao de um ciclo global
  (`FFG-CE-001` refuta).
- Diferidos: ponte `SimpleGraph` (`FFG-GAP-012`), arvores (`FFG-GAP-007`),
  distancia minima (`FFG-GAP-006`), tempo minimo, representante canonico,
  quociente, classificacao completa.
- `FFG-GAP-014` permanece `OPEN_BIBLIOGRAPHIC`.
- `mathematical_novelty: NONE`.
- `RH-NOGO-001` e os arquivos matematicos de `FOUND-SEMIGROUP-002`:
  **0 tocados**.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_VERIFIED`.

## FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION-REVIEW - 2026-07-31

### Corrected

- **`MutuallyReachable`**: retirada a formulacao imprecisa "identifica o
  ciclo, nao o componente". Adotada a formulacao por classes: em pontos
  periodicos expressa pertencimento a mesma trajetoria ciclica; no dominio
  total, a classe de `p` periodico tem `minimalPeriod f p` elementos e cada
  ponto transitorio forma classe unitaria. Argumento de isolamento escrito.
  **Refinamento acrescentado pela revisao**: "classe unitaria" NAO distingue
  transitorio de ponto fixo — um ponto fixo tambem tem classe unitaria.
- **`IsRecurrent` RETIRADO.** "Recorrencia" tem significados mais amplos em
  dinamica. Estrategia A com a clausula condicional resolvida
  negativamente: os teoremas publicos usam `x ∈ Function.periodicPts f`
  diretamente; `IsCyclePoint`/`IsTransientPoint` NAO criados, porque a
  lista CORE nao os usa. Nessa resolucao A coincide com B.
- **Testemunhas da transitividade corrigidas.** A auditoria confirmou
  `iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)` — a
  contagem EXTERNA vem a esquerda. Formas naturais: `d + mx` e `d + nz`,
  nao `mx + d` e `nz + d`. Novo gap `FFG-GAP-015`.
- **`FFG-MAIN-001` e `FFG-MAIN-002` COLAPSADOS** em
  `exists_component_cycle_with_entry_bound`: o `p` existencial era sempre
  `f^[mu] x`, logo redundante. `FFG-REC-001` tambem removido.

### Added

- `SPECIFICATION_REVIEW.md`, `FINAL_DEFINITIONS.md`, `FINAL_SIGNATURES.md`,
  `API_NAMING_DECISION.md`, `REVIEW_DECISION.md` — **congelados**.
- Nucleo: 3 definicoes e **9 teoremas**; 2 corolarios opcionais.

### Verified

- Probe descartavel em `/tmp`, somente `import` e `#check`, exit **0**,
  **removido**. Zero `theorem`/`example`/`axiom`/`sorry`/`admit`.
  **0 arquivos `.lean` no repositorio; nenhum `lake build`.**
- `periodicPts` exige periodo positivo; `IsPeriodicPt f 0 x` eh sempre
  verdadeiro e nao serve sozinha.
- `periodicOrbit : Cycle X`, sem `DecidableEq`, **noncomputavel** — nao
  impede provas proposicionais, impede `decide` sobre igualdade de orbitas.
- Hipoteses: nenhuma finitude nas relacoes e na igualdade de orbitas;
  `[Fintype X]` so na existencia e no principal; `DecidableEq X` ausente.
- pytest 9 passed; `labctl validate` PASS.

### Blocked

- `componentSet` `DEFERRED_API_ALIAS` — sem uso na API publica.
- `Setoid`, `SimpleGraph`, arvores, distancia minima, representante
  canonico, classificacao completa: **DEFERRED**. A ponte com `SimpleGraph`
  fica como **conjectura futura**, nao como claim.
- `FFG-GAP-014` permanece `OPEN_BIBLIOGRAPHIC`.
- `mathematical_novelty: NONE`; ledger em **18** claims.
- `RH-NOGO-001` e os arquivos matematicos de `FOUND-SEMIGROUP-002`:
  **0 tocados**.

### Changed

- `canonical_commit`: `df6adb9` -> `90fb4e2`, no preflight.
- `specification_status`: `READY_FOR_REVIEW` -> `APPROVED`.
- `authorized_action` -> `FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_AUTHORIZED`.
- `DEFINITIONS.md` e `THEOREM_CANDIDATES.md` marcados **historicos**, com as
  decisoes superadas preservadas e a correcao anexada.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED`.

## FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION - 2026-07-31

### Decided

- **Componente funcional := classe de `EventuallyMeets`**
  (`∃ m n, f^[m] x = f^[n] y`). **NAO** `MutuallyReachable`.
  Contraexemplo decisivo `FFG-CE-004`: em `a→c, b→c, c→c`, os estados `a` e
  `b` estao no mesmo componente e nenhum alcanca o outro;
  `MutuallyReachable` separaria em tres classes o que eh uma estrutura so.
- **Um unico nome**: `EventuallyMeets`. `SameFunctionalComponent` rejeitado
  como segundo nome, **inclusive na forma `abbrev`**.
- **Unicidade = igualdade de `Function.periodicOrbit`**, nao existencia de
  um unico ponto periodico (`FFG-CE-005` refuta) nem representante
  canonico. O objeto unico eh a ORBITA.
- **Orientacao fixada**: o primeiro argumento de `EventuallyMeets` vai para
  o lado esquerdo da igualdade de orbitas. Consistente em `FFG-CYCLE-001` e
  `FFG-MAIN-001`.
- Alvo `CORE_UNIQUE_CYCLE_WITH_ENTRY_BOUND`, com `mu < Fintype.card X`.

### Added

- Especificacao em
  `02_FOUNDATIONS/04_FUNCTIONAL_GRAPHS/FOUND_FUNCTIONAL_GRAPH_001/`,
  **16 artefatos**. Quinze teoremas candidatos, seis contraexemplos,
  catorze gaps, catorze stop conditions.
- `COMPONENT_NOTIONS.md` e `NOVELTY_BOUNDARY.md` sao **vinculantes**.

### Verified (auditoria da Mathlib, por leitura da fonte)

- `periodicPts f = { x | ∃ n > 0, IsPeriodicPt f n x }` — periodo positivo
  **por definicao**, o que resolve a armadilha de `n = 0`.
- `periodicOrbit : Cycle α` **SEM `DecidableEq`** — bloco de variaveis em
  `Dynamics/PeriodicPts/Defs.lean:57`.
- **`periodicOrbit` eh NONCOMPUTAVEL** (`noncomputable section`, 240-490):
  `decide` indisponivel para igualdade de orbitas. Afeta os contraexemplos,
  nao o nucleo. `FFG-GAP-011`.
- `periodicOrbit_apply_iterate_eq` da `FFG-CYCLE-001` em **tres passos**,
  sem aritmetica modular.
- `mk_mem_periodicPts` eh o adaptador exato de `exists_eventual_period`.
- **Zero `NOT_FOUND`**: toda a maquinaria de ciclos ja existe. O conteudo
  matematico proprio desta frente eh menor que o da anterior; o valor eh de
  API e integracao.

### Corrected

- **Previsao refutada**: `FFG-GAP-008` previa que `DecidableEq X`
  provavelmente seria necessaria aqui. A leitura da fonte mostrou que
  **nao eh** — o nucleo exige apenas `[Fintype X]`. Registrado como
  refutacao explicita.
- **Assinatura rejeitada**: a forma `∃ μ p : ℕ × X` de
  `exists_recurrent_reachable` foi descartada por ser par artificial;
  adotada a forma limpa recomendada pelo proprio gate.

### Blocked

- **Formalizacao NAO autorizada.** A proxima etapa eh a REVISAO da
  especificacao, para que uma definicao inadequada de componente nao seja
  congelada em Lean.
- Diferidos: ponte `SimpleGraph` (`FFG-GAP-012`), arvores de entrada,
  distancia minima, unicidade de `mu`, contagem de componentes.
- `mathematical_novelty: NONE`. Decomposicao "forma rho" eh material padrao.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`; **0** arquivos tocados.
- `FOUND-SEMIGROUP-002.extension_status` permanece `NOT_AUTHORIZED`.

### Not done

- **0** arquivos Lean, **0** provas, **0** `lake build`, **0** experimentos
  Python, **0** claims promovidas (ledger em 18), **0** arquivos de legado.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_READY`.

## PORTFOLIO-REVIEW - 2026-07-31

### Lock transition

- **`NO_ACTION_AUTHORIZED` -> `PORTFOLIO_REVIEW_REQUIRED`**, atomicamente,
  nos cinco pontos de governanca viva: allowlist do `labctl.py`,
  `LAB_STATE`, `RESEARCH_QUEUE`, `STATUS.yaml` e `CLOSURE_RECORD.md` de
  `FOUND-SEMIGROUP-002`. Motivo: o sufixo `_AUTHORIZED` convidava a ler a
  trava como autorizacao.
- **Registros historicos NAO foram reescritos** —
  `found-semigroup-002-result-review.json`, `09_SESSIONS/` e este
  changelog documentam o que aquele gate decidiu, com o nome que a trava
  tinha entao. Uma busca futura ainda encontrara o nome antigo neles, e
  isso eh correto.
- A trava foi **satisfeita** neste mesmo gate, pela emissao explicita de
  uma revisao de portfolio.

### Decided

- **`FOUND-FUNCTIONAL-GRAPH-001` selecionado** (Finite Functional Graph
  Decomposition), track `foundations`, status `SCOPED`. Busca por
  duplicata: **0 ocorrencias**.
- Os seis itens `SCOPED` remanescentes foram reavaliados; **nenhum**
  satisfaz simultaneamente infraestrutura Mathlib pronta, acesso alto a
  contraexemplos e PoC em 30 dias. `TOE-INTERFACE-001` esta **bloqueado**:
  depende formalmente de `RH-NOGO-001`, congelado.
- **Resultado forte NAO autorizado**: a unicidade do ciclo por componente
  depende de qual nocao de componente for adotada (`FFG-GAP-002`,
  `FFG-GAP-004`). `strong_result_status:
  NOT_AUTHORIZED_BEFORE_SPECIFICATION`.

### Added

- `01_PORTFOLIO/PORTFOLIO_REVIEW_2026_07_31.md` e
  `01_PORTFOLIO/NEXT_WORK_ITEM_DECISION.md`.
- Entrada `FOUND-FUNCTIONAL-GRAPH-001` em `RESEARCH_QUEUE.yaml` e cadeia
  de fundacoes finitas em `GLOBAL_DEPENDENCY_GRAPH.md`.
- Dez gaps iniciais `FFG-GAP-001..010` e cinco contraexemplos planejados
  `FFG-CE-001..005`.

### Changed

- `canonical_commit`: `b4ce2551` -> `3f72ad0`, no preflight.
- `active_work_item`: `FOUND-SEMIGROUP-002` -> `FOUND-FUNCTIONAL-GRAPH-001`.
- `authorized_action` -> `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `labctl`: sequencia de gates admite o novo item, com pre-condicao
  `FOUND-SEMIGROUP-002 VERIFIED`.

### Blocked

- **`FOUND-FUNCTIONAL-GRAPH-001` NAO eh extensao de `FOUND-SEMIGROUP-002`**,
  cujo `extension_status` permanece `NOT_AUTHORIZED`. A relacao eh de
  reutilizacao de API verificada.
- `mathematical_novelty: NONE`. Decomposicao "rho shape" de iteracao
  finita eh material padrao.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`; **0** arquivos tocados.

### Not done

- **0** arquivos Lean, **0** provas, **0** `lake build`, **0** claims
  promovidas, **0** arquivos de legado, **0** arquivos matematicos de
  `FOUND-SEMIGROUP-002`, **0** pastas de especificacao da nova frente.

### Result

- `PORTFOLIO_REVIEW_APPROVED_FUNCTIONAL_GRAPH_SELECTED`.

## FOUND-SEMIGROUP-002-RESULT-REVIEW - 2026-07-31

### Reviewed

- `FRR-001` a `FRR-007`: **todos CONFIRMADOS**. Verificado por inspecao
  que a reciproca de `IsInvariant.under` NAO eh afirmada, e que a palavra
  "periodo" nunca significa periodo minimo.
- **Caso `card X = 0`**: o teorema recebe `x : X`, logo no ponto de
  aplicacao `X` eh habitado. Sem contradicao escondida. Zero instancias de
  `Nonempty`/`Inhabited`.
- **Casa dos pombos**: 1 uso real (3 ocorrencias textuais: uso, docstring,
  `#check`). Nao reprovada no teorema principal, no corolario de acao nem
  na propagacao.
- **`minimalPeriod`**: 4 mencoes, **todas em comentario**; 0 usos.
  `MulAction.period`: 0 ocorrencias.

### API and instance audit

- **API publica: 17 declaracoes**, exatamente a lista minima esperada.
  Um unico auxiliar, `eventual_period_of_lt`, e ele eh `private`.
- **11 instancias, ZERO no nucleo matematico.** Todas em
  `Counterexamples`, sob cinco namespaces: `CE001` 4, `CE002` 4,
  `CE003` 1, `CE004` 2, `CE005` 0.
- **0 conflitos.** `CE004` reutiliza `CE001.Tr` sobre outro espaco de
  estados; os pares sao distintos e ambos `•` resolvem corretamente.
- **Nenhuma instancia de `Preorder`** (1 ocorrencia da palavra, num
  comentario que declara a exclusao).
- Novo teste `Tests/FoundSemigroup002InstanceAudit.lean` (exit 0), que
  **nao altera modulo matematico algum**: onze `#synth`, desambiguacao do
  `•`, e a verificacao decisiva de que `exists_eventual_period` continua
  se aplicando a `Bool` com todas as instancias em escopo.

### Gaps

- Nove resolvidos, tres abertos. **`FSG2-GAP-007` NAO fechado** (negativa
  sobre o periodo continua sem contraexemplo); **`FSG2-GAP-009` NAO
  fechado** (sem auditoria bibliografica).

### Reuse

- Um unico `DIRECT_REUSE`: testes de alcancabilidade — a parte da API que
  **nao exige finitude**. Seis `REQUIRES_ADAPTER`, tres `CONCEPTUAL_ONLY`.
  Nenhuma integracao criada.

### Not done

- **0** teoremas novos, **0** modulos matematicos alterados, **0** claims
  novas, **0** claims fisicas ou de novidade, **0** arquivos de legado,
  **0** arquivos de `RH-NOGO-001` tocados.

### Changed

- `canonical_commit`: `2b86a880` -> `b4ce2551`, no preflight.
- `result_review: APPROVED`; `extension_status: NOT_AUTHORIZED`.
- `authorized_action` -> `NO_ACTION_AUTHORIZED`, que eh **trava, nao
  autorizacao de execucao**.

### Result

- `FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED`. A frente fica **encerrada
  como fundacao formal reutilizavel**, sem autorizacao ativa. O
  laboratorio nao tem frente ativa: a escolha do proximo trabalho exige um
  gate separado de revisao de portfolio.

## FOUND-SEMIGROUP-002-FORMALIZATION - 2026-07-31

### Corrected

- **5.1 Invariancia sob um elemento.** Retirada a afirmacao de que
  `IsInvariantUnder a` seria *universalmente* mais fraca que
  `IsInvariant`. O que vale e foi formalizado eh apenas a implicacao
  `IsInvariant I -> IsInvariantUnder a I` (`IsInvariant.under`). A estrita
  fraqueza PODE ocorrer, mas nao uniformemente: se `a` gera `M`, as duas
  nocoes coincidem.
- **5.2 Contraexemplo de alcancabilidade.** `CE-001` reconstruido como
  **acao genuina de monoide** (`{idT, collapse}` sobre `{zero, one}`), com
  as leis verificadas antes da instanciacao. O grafo de uma funcao isolada
  refutaria apenas a alcancabilidade por aquele gerador, nao a simetria de
  `Reachable`, que eh definida pela acao COMPLETA.

### Added

- Nucleo Lean em `05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/`:
  `Reachability`, `Invariants`, `EventualPeriodicity`, `MonoidIteration`,
  `Counterexamples`, `Audit`, agregador e dois testes isolados.
  **41 teoremas, 10 defs, 6 indutivos, 11 instancias.**
- Teorema principal `exists_eventual_period`: toda trajetoria de
  `f : X -> X` com `X` finito eh eventualmente periodica, com
  `mu < card X`, `0 < lam`, `mu + lam <= card X`, ponto periodico na cauda
  e propagacao a todos os indices posteriores.
- Corolarios de acao `monoid_element_eventually_periodic` e
  `..._propagates`, **derivados** via `smul_iterate_apply`.
- Cinco contraexemplos formais (`CE-001..CE-005`), todos em Lean, **sem
  Python** e **sem `native_decide`**.
- `THEOREM_MAP.md`, `PROOF_AUDIT.md`, `COUNTEREXAMPLE_AUDIT.md`,
  `RESULT_BOUNDARY.md`, `C3_BOUNDARY.md`.
- Claim `FINITE-DYNAMICS-FORMAL-001` (`F`, VERIFIED,
  `mathematical_novelty: NONE`).

### Verified

- `lake build` PASS com **8.717 jobs** em 117 s; dois testes isolados
  exit 0. Build final **sem avisos**.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0`.
- `#print axioms` nos 8 objetos: **quatro nao dependem de axioma algum**;
  os demais usam apenas `propext`, `Classical.choice`, `Quot.sound`.
- Casa dos pombos usada **uma unica vez**; `minimalPeriod` **nunca** usado;
  **nenhuma** instancia global de `Preorder`.
- Hipoteses ociosas confirmadas e removidas: `exists_eventual_period` exige
  **somente** `[Fintype X]`; o corolario de acao nao exige `Fintype M`,
  `DecidableEq X` nem `Group M`. `FSG2-GAP-004c` fechado.
- pytest 9 passed; `labctl validate` PASS com `canonical_commit_check` PASS.

### Changed

- `canonical_commit`: `39e3d95` -> `2b86a880`, no preflight.
- `FOUND-SEMIGROUP-002`: `READY` -> `VERIFIED`.
- `authorized_action` -> `FOUND_SEMIGROUP_002_RESULT_REVIEW_AUTHORIZED`
  (entrada literal unica).

### Blocked

- **Novidade matematica: NONE.** Periodicidade eventual em conjunto finito
  eh o principio da casa dos pombos.
- NAO provados: unicidade da cauda, minimalidade do periodo, decomposicao
  canonica, classificacao de acoes finitas, sistemas infinitos, qualquer
  resultado fisico, TRI, TDTR.
- `C3_BOUNDARY.md` (vinculante): "propriedades de C3 falham em geral"
  significa que para CADA UMA existe contraexemplo, **nao** que todas
  falhem simultaneamente em toda acao. Nenhum teorema de
  `FOUND-SEMIGROUP-001` foi alterado.
- `FSG2-GAP-007`: a negativa "o periodo depende do estado inicial"
  continua sem contraexemplo e **nao eh afirmada**.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`; **0** arquivos tocados.

### Result

- `FOUND_SEMIGROUP_002_FORMALIZATION_VERIFIED`.

## FOUND-SEMIGROUP-002-SPECIFICATION - 2026-07-31

### Preflight

- `canonical_commit` atualizado de `c186ab59` para `39e3d95` **antes** de
  qualquer trabalho de especificacao; politica textual substituida por
  "ultimo commit canonico integralmente encerrado antes da sessao atual;
  deve existir e ser ancestral do HEAD".
- Commits `1576cf1` e `39e3d95` fazem parte obrigatoria do estado de
  retomada.

### Added

- Validacao nao destrutiva de `canonical_commit` em `labctl.py`
  (`check_canonical_commit`, funcao pura com `runner` injetavel):
  `cat-file` ausente -> `CANONICAL_COMMIT_UNAVAILABLE` com recomendacao de
  completar o historico; `is-ancestor` exit 0 -> PASS (igualdade aceita);
  exit 1 -> `CANONICAL_COMMIT_NOT_ANCESTOR`; outro exit ->
  `CANONICAL_COMMIT_GIT_ERROR`. Severidade **erro**, nunca warning.
- `tests/test_canonical_commit.py`: 7 testes cobrindo os cinco casos
  pedidos, **sem criar branch nem reescrever historico**. O teste de
  igualdade afirma que nao ha `rev-parse` extra, travando a ancestralidade
  nao estrita.
- Especificacao `FOUND-SEMIGROUP-002` em
  `02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/` (13 artefatos).
  Onze teoremas candidatos, cinco contraexemplos, doze gaps.

### Decided

- Meta principal: **`C. CORE_BOUNDS_AND_PROPAGATION`**. Os tres limitantes
  foram verificados como simultaneamente alcancaveis ANTES da escolha.
  **`DECOMPOSITION` excluida** apos analise de custo (`FSG2-GAP-004b`).
- Tres camadas separadas: acao completa / gerador / funcao finita.
  Periodicidade eventual pertence a Camada C e **nao** menciona monoide.
- Sem instancia global `Preorder` para alcancabilidade (`FSG2-GAP-006`).

### Verified

- `smul_iterate_apply` **existe** na Mathlib fixada: `FSG2-GAP-003`
  resolvido pela API, nao por prova.
- `mem_orbit_iff` eh `Iff.rfl`: a ponte alcancabilidade/orbita custa zero.
- Periodicidade eventual **ausente** do Mathlib (zero ocorrencias de
  `preperiodic`/`eventuallyPeriodic`): o enunciado sera local.
- **Armadilha registrada**: `minimalPeriod` e `MulAction.period` devolvem 0
  fora de `periodicPts`; `CE-003` a torna detectavel (`FSG2-GAP-002b`).
- pytest **9 passed**; `labctl validate` PASS com `canonical_commit_check`
  PASS.

### Not done

- **0** arquivos Lean, **0** provas, **0** `lake build`, **0** experimentos
  Python, **0** claims cientificas promovidas, **0** arquivos de legado
  modificados, **0** arquivos de `RH-NOGO-001` tocados.

### Blocked

- Novidade matematica: **NONE**. Periodicidade eventual em conjunto finito
  eh o principio da casa dos pombos. `NOVELTY_BOUNDARY.md` eh vinculante.
- Bibliografia primaria `NOT_AUDITED` (`FSG2-GAP-009`): nenhuma afirmacao
  de prioridade historica eh permitida.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT` / `NOT_AUTHORIZED` /
  `NO_EXECUTION`.

### Result

- `FOUND_SEMIGROUP_002_SPECIFICATION_READY`.
  `authorized_action` -> `FOUND_SEMIGROUP_002_FORMALIZATION_AUTHORIZED`.

## APPROVAL RECORD - 2026-07-31

### Approved

- **`DEC-012` aprovado apos revisao.** As quatro alteracoes em
  `labctl.py` sao minimas, literais e deflacionarias, e preservam
  `RH-NOGO-001` como `NOT_AUTHORIZED` / `NO_EXECUTION`. Nao houve
  relaxamento material do guardrail.
- **`DEC-013` aprovado apos revisao.** `FOUND-SEMIGROUP-002` eh aceito
  como novo work item `SCOPED`, porque os itens remanescentes da fila
  canonica eram incompativeis com os criterios de custo e dependencia da
  revisao. A criacao **nao** eh uma descoberta cientifica: o item deve
  investigar propriedades padrao de acoes finitas de monoides - orbitas,
  alcancabilidade, invariantes, periodicidade eventual e contraexemplos.
- Escopo da aprovacao: **apenas preparacao da especificacao**.

### Added

- `DEC-014`: endurecimento futuro de governanca para
  `FROZEN_PARTIAL_RESULT`, registrado como `PENDING_NOT_IMPLEMENTED`.
  Todo item nesse estado deveria exigir `freeze_record`,
  `result_boundary`, `reactivation_criteria` e `concrete_layer_status`.
  **Nao implementado em `labctl.py`** neste gate.
- `RESEARCH_QUEUE.yaml`: `concrete_layer_status: DEFERRED` em
  `RH-NOGO-001`, que passa a conter os quatro campos propostos - o
  endurecimento futuro sera um no-op para o estado atual.

### Unchanged

- Commit `1576cf1` **nao foi reescrito**.
- `active_work_item: FOUND-SEMIGROUP-002`, `work_status: SCOPED`,
  `authorized_action: FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED`.
- Nenhum teorema Lean, nenhuma claim promovida, nenhuma especificacao
  iniciada.

## RH-NOGO-RESEARCH-REVIEW - 2026-07-31

### Decided

- **`RH-NOGO-001` CONGELADO** como resultado parcial formal
  (`A_FREEZE_AS_PARTIAL_FORMAL_RESULT`, `DEC-012`). Congelado, **nao
  descartado**: a camada abstrata eh verificada e reutilizavel.
- Opcoes B (continuar), C (colaboracao externa) e D (rejeitar) descartadas
  com motivo registrado.
- `FOUND-SEMIGROUP-002` selecionado como proximo work item (`DEC-013`),
  **apenas para especificacao**. Nenhum dos seis itens remanescentes da
  fila satisfazia os criterios do gate.

### Added

- `RH_NOGO_FINAL_RESEARCH_REVIEW.md`, `RH_NOGO_FREEZE_RECORD.md`,
  `RH_NOGO_REACTIVATION_CRITERIA.md`, `RH_NOGO_RESULT_BOUNDARY.md`.
- `RESEARCH_QUEUE.yaml`: item `FOUND-SEMIGROUP-002` (algebra finita e
  dinamica discreta; `Fintype`/`Decidable`/`decide` ja disponiveis).

### Changed

- `RH-NOGO-001`: `SCOPED` -> `FROZEN_PARTIAL_RESULT` na fila e em
  `STATUS.yaml`. `authorization_state` e `execution_state` **inalterados**.
- `active_work_item`: `RH-NOGO-001` -> `FOUND-SEMIGROUP-002`.
- `authorized_action`: `RH_NOGO_RESEARCH_REVIEW_AUTHORIZED` ->
  `FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED`.
- **`labctl.py`, quatro alteracoes minimas e literais** (registradas em
  `DEC-012`): `ALLOWED_WORK_STATUS += FROZEN_PARTIAL_RESULT`; checagem de
  `RH-NOGO-001` aceita `{SCOPED, FROZEN_PARTIAL_RESULT}` (deflacionaria,
  segue bloqueando `READY`/`IN_PROGRESS`/`VERIFIED`); sequencia de gates
  admite `FOUND-SEMIGROUP-002`; allowlist +1 entrada literal.
  As travas `NOT_AUTHORIZED` / `NO_EXECUTION` **nao foram tocadas**.

### Verified

- Teoremas Lean novos: **0**. Claims promovidas: **0**. No-go executado:
  **nao**. Legado modificado: **0**.
- pytest 2 passed; `labctl validate` PASS.

### Blocked

- `GLOBAL-WEYL-BRIDGE-SCALAR`: 9 obrigacoes, **0 provadas**.
- Riemann-von Mangoldt: **nao formalizada**.
- Reativacao so por `REACT-001..005`. Mais capacidade computacional ou um
  modelo de IA mais forte **nao** sao criterio.

### Result

- `RH_NOGO_FROZEN_AS_PARTIAL_FORMAL_RESULT`.
  `spectral_nogo: NOT_ESTABLISHED`; `hilbert_polya: NOT_EXCLUDED`;
  `riemann_hypothesis: NO_RESULT`.

## ABSTRACT-COUNTING-NOGO - 2026-07-31

### Added

- `ABSTRACT-NOGO-001` formalizado em
  `05_FORMAL/lean/TamesisLab/RHNogo/Composition/`: `AbstractNogo.lean`,
  `Corollaries.lean`, `Audit.lean`, agregador `Composition.lean` e teste
  `Tests/RHNogoAbstractComposition.lean`. **5 teoremas**, 1 estrutura,
  1 definicao.
- Teorema principal `abstract_power_tlog_incompatibility`: uma lei de
  potencia positiva para `NTarget`, uma lei positiva `T log T` para
  `NBase` e `NTarget - NBase = o(T log T)` sao simultaneamente
  insatisfaziveis. Prova em DUAS LINHAS: composicao de
  `COUNTING-LAW-BRIDGE` com `ASYM-NOGO-001`.
- Estrutura `AbstractCountingNogoData` (nao eh `class`) e o teorema
  `.false` de inabitabilidade.
- Corolarios `ABSTRACT-NOGO-E0-001` (igualdade eventual) e
  `ABSTRACT-NOGO-E1-001` (diferenca limitada), reutilizando conversoes ja
  verificadas.
- `ABSTRACT_COMPOSITION_THEOREM_MAP.md` e
  `ABSTRACT_COMPOSITION_PROOF_AUDIT.md`.
- Claim `ABSTRACT-COUNTING-NOGO-FORMAL-001` (`F`, `formal_asymptotics`,
  VERIFIED).

### Verified

- `lake build` PASS com **8.708 jobs** em 129 s; teste isolado exit 0.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0` na arvore inteira.
- `#print axioms` nos 7 objetos: apenas `propext`, `Classical.choice`,
  `Quot.sound`.
- Imports da pasta `Composition/`: **apenas** `AsymptoticCore` e `Bridge`.
  **`Geometry/` NAO importado.**
- Vocabulario proibido na pasta: 7 ocorrencias, **todas em comentarios que
  declaram a exclusao**; nenhuma em identificador, tipo ou termo de prova.
- Direcao da diferenca confirmada por `Iff.rfl`: `SubdominantTLog X Y` eh
  literalmente `X - Y = o(T log T)`. Opcao C (documentar a convencao
  existente); nenhum lema de sinal foi necessario.
- pytest 2 passed; `labctl validate` PASS.
- Nenhuma falha de compilacao: os cinco arquivos passaram de primeira.

### Changed

- `authorized_action`: `RH_NOGO_ABSTRACT_COMPOSITION_FORMALIZATION_AUTHORIZED`
  -> `RH_NOGO_RESEARCH_REVIEW_AUTHORIZED` (entrada literal unica).
- `STATUS.yaml`: `abstract_layer: COMPLETE`.

### Blocked

- **Nenhuma instancia de `PowerCountingLaw` vinda de operador** — exigiria
  `GWB-001..009`, zero provadas.
- **Nenhuma instancia de `TLogCountingLaw` vinda da zeta** — exigiria
  Riemann-von Mangoldt (`SB-GAP-010B`).
- `E3` nao formalizado (`SB-GAP-011`).
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

### Result

- `RH_NOGO_ABSTRACT_COMPOSITION_VERIFIED`. A camada analitica abstrata
  esta COMPLETA. O resultado **nao eh novidade matematica**.

## RH-NOGO-GEOMETRIC-GAP-RESOLUTION - 2026-07-31

### Added

- `W_ELLIPTIC_SCALAR_V3.md`: classe dividida em
  **W-ELLIPTIC-SCALAR-SOURCE** (6 condicoes literais de Coriasco-Doll p.1)
  e **W-ELLIPTIC-SCALAR-BRIDGE** (mais 6 acrescimos deste laboratorio,
  cada um marcado `EXPLICIT_BRIDGE_ASSUMPTION`). Metade da classe eh
  deste laboratorio, e isso agora esta numa tabela.
- Condicoes novas e explicitas: `M` nao vazia (B3), `d >= 1` (B4) e
  simbolo principal real, positivo fora da secao nula e homogeneo de
  grau `m > 0` (B5). B5 estava sendo usada TACITAMENTE.
- `WEYL_COEFFICIENT_POSITIVITY.md`: argumento em seis passos para
  `C_P > 0`, com o estado de cada passo.
- `GLOBAL_WEYL_DATA_BRIDGE.md`: instanciacao de `PowerCountingLaw`
  campo a campo, com fornecedor e evidencia.
- `DISCRETENESS_CLASSIFICATION.md`, `GEOMETRIC_LEAN_SCOPE.md`,
  `GEOMETRIC_GAP_RESOLUTION_AUDIT.md`.
- Nucleo Lean em `05_FORMAL/lean/TamesisLab/RHNogo/Geometry/`:
  5 teoremas, 1 estrutura, 1 construtor. Teoria da medida elementar.
- Claim `WEYL-COEFFICIENT-INTERFACE-001` (`F`,
  `spectral_interface_governance`).

### Changed

- **`GWB-008` dividida em tres**: `008A` (positividade da medida no
  espaco de fases, `DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE`),
  `008B` (`C_P > 0`, `ELEMENTARY_COROLLARY_WITH_FORMALIZED_CORE`) e
  `008C` (`C_P < infinito`, `DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE`).
- **Discretude classificada sem inflacao**: `GWB-001` eh
  `EXPLICIT_CLASS_ASSUMPTION`; `GWB-002` eh `SOURCE_CITED_RESULT`.
- `GAP-RH-014` -> `RESOLVED_DOCUMENTALLY_FOR_SCALAR_BRIDGE_CLASS_ONLY`.
  NAO eh `CLOSED`: o argumento foi ESCRITO, nao provado.
- `GAP-RH-012` -> `EXPLICIT_CLASS_ASSUMPTION_CLASSIFIED`.
- `GAP-RH-009` -> `OPEN_SYSTEMS_DEFERRED`. **NAO fechado.**
- `authorized_action`: `RH_NOGO_GEOMETRIC_GAP_RESOLUTION_AUTHORIZED`
  -> `RH_NOGO_ABSTRACT_COMPOSITION_FORMALIZATION_AUTHORIZED`
  (entrada literal unica, sem wildcard).

### Verified

- `lake build` PASS com **8.703 jobs**; teste isolado exit 0.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0`.
- `#print axioms` nos 7 objetos: apenas `propext`, `Classical.choice`,
  `Quot.sound`.
- Auditoria de escopo em `Geometry/`: nenhuma definicao de variedade,
  fibrado cotangente, operador pseudodiferencial, simbolo principal,
  medida de Liouville ou coeficiente de Weyl concreto. As unicas
  ocorrencias desse vocabulario sao os avisos que declaram a exclusao.
- pytest 2 passed; `labctl validate` PASS.

### Blocked

- **As onze obrigacoes `GWB-001..009` continuam NAO PROVADAS.**
- `GAP-RH-015` (finitude de `C_P`) aberto; `SB-GAP-012` (seis acrescimos
  de ponte sem fonte) aberto; `SB-GAP-001` dividido em `001A/001B/001C`.
- `ASYM-NOGO-001` NAO aplicado. Nenhum operador construido ou excluido.
  Hilbert-Polya NAO excluido. Nada afirmado sobre a Hipotese de Riemann.

### Result

- `RH_NOGO_SCALAR_GEOMETRIC_INTERFACE_READY`. A entrada geometrica foi
  resolvida em nivel de INTERFACE e de REGISTRO, nao de prova.

## COUNTING-LAW-BRIDGE — 2026-07-31

### Added

- Ponte de contagem formalizada em
  `05_FORMAL/lean/TamesisLab/RHNogo/Bridge/`: `Definitions.lean`,
  `TLogScale.lean`, `LittleOTransfer.lean`, `CountingLawBridge.lean`,
  `StrongAsymptoticCorollary.lean`, `Audit.lean`, agregador `Bridge.lean`
  e teste `Tests/RHNogoCountingBridge.lean`. **15 teoremas**, 9 definicoes.
- Teorema principal `counting_law_bridge`: se `N_base/(T log T) -> c` e
  `N_target - N_base = o(T log T)`, entao `N_target/(T log T) -> c`.
- Versao estrutural `TLogCountingLaw.transfer`, com preservacao da
  constante provada por `rfl`.
- `STRONG-TLOG-COROLLARY` (`tendsto_tLog_of_eq_main_add_littleO`):
  "formula forte implica limite", **sem mencionar zeta**.
- Hierarquia `E0 => E1 => E2` formalizada.
- `COUNTING_BRIDGE_THEOREM_MAP.md` e `COUNTING_BRIDGE_PROOF_AUDIT.md`.
- Claim `COUNTING-BRIDGE-FORMAL-001` (`F`, `formal_asymptotics`, VERIFIED).

### Corrected

- **`SB-GAP-010` dividido e parcialmente fechado.** A afirmacao anterior de
  que formalizar `RVM-LIMIT` exigiria definir a funcao zeta estava ERRADA
  para a parte generica. `SB-GAP-010A` (corolario generico)
  `CLOSED_BY_FORMALIZATION`; `SB-GAP-010B` (Riemann-von Mangoldt concreto)
  `OUT_OF_CURRENT_SCOPE`; `SB-GAP-010` `SUPERSEDED`.
- **Hipotese ociosa removida:** `0 < c` nao eh necessaria em
  `counting_law_bridge` e foi retirada do teorema tecnico; a positividade
  permanece apenas na interface `TLogCountingLaw`.
- `Bridge/SignatureProbe.lean` reduzido a registro historico: as definicoes
  foram promovidas para `Bridge/Definitions.lean`.

### Verified

- `lake build` PASS com **8.699 jobs**; teste isolado exit 0; tokens
  proibidos zero.
- `#print axioms` nos 13 objetos rastreaveis: apenas `propext`,
  `Classical.choice`, `Quot.sound`.
- Auditoria de escopo: imports da pasta `Bridge/` sao apenas `Log.Basic`,
  `Pow.Real` e `Asymptotics.Lemmas`; busca por `zeta`, `Riemann`, `Weyl`,
  `Complex`, `spectral`, `operator`, `Polya`: **nenhuma ocorrencia**.
- pytest 2 passed; `labctl validate` PASS.
- `ASYM-NOGO-001` **nao** aplicado.

### Changed

- `authorized_action`: `RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED`
  -> `RH_NOGO_GEOMETRIC_GAP_RESOLUTION_AUTHORIZED` (entrada literal unica).

### Blocked

- `GWB-008` (`C_P > 0`): obrigacao GEOMETRICA; nao bloqueou este gate.
- `GAP-RH-012` (discretude), `GAP-RH-009` (fibrados, NAO fechado),
  `SB-GAP-010B`, `SB-GAP-011` (nivel E3 nao formalizado).
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

### Result

- `RH_NOGO_COUNTING_BRIDGE_VERIFIED`. Componentes analiticos abstratos
  verificados: `COUNTING-LAW-BRIDGE` -> `ASYM-NOGO-001`.

## RH-NOGO-001 — especificacao da ponte de contagem — 2026-07-31

### Added

- Especificacao completa da ponte em `03_MILLENNIUM/01_RIEMANN/`:
  `SOURCE_BRIDGE_SPECIFICATION.md` (indice), `W_ELLIPTIC_SCALAR_V2.md`,
  `W_ELLIPTIC_SYSTEM_DEFERRED.md`, `GLOBAL_WEYL_BRIDGE_OBLIGATIONS.md`
  (GWB-001..009), `RVM_LIMIT_BRIDGE.md`, `COUNTING_LAW_RELATIONS.md`
  (E0-E3), `COUNTING_LAW_BRIDGE_SPEC.md`, `NARROW_NOGO_STATEMENT.md`,
  `SPECTRAL_MATCH_CONVENTIONS.md` (SMC-001..007),
  `SOURCE_BRIDGE_DEPENDENCY_DAG.yaml`, `SOURCE_BRIDGE_GAP_REGISTER.yaml`
  (SB-GAP-001..010), `SOURCE_BRIDGE_LEAN_FEASIBILITY.md`.
- `05_FORMAL/lean/TamesisLab/RHNogo/Bridge/SignatureProbe.lean`: oito
  assinaturas elaboradas (`PowerCountingLaw`, `TLogCountingLaw`,
  `SubdominantDifference`, `EventualEquality`, `BoundedDifference`,
  `RatioEquivalence`, `CountingLawBridgeStatement`,
  `NarrowSpectralNogoStatement`), `set_option autoImplicit false`,
  **nenhuma prova**.

### Changed

- **Alvo migrado de igualdade espectral exata para `N_P(T) - N_zeta(T) =
  o(T log T)` (nivel E2)**, que cobre E0, E1, E2 e E3 com um unico lema.
- `W-ELLIPTIC-SCALAR` v2: bordo e sistemas/fibrados **excluidos**
  deliberadamente. `GAP-RH-009` NAO foi fechado - foi contornado por
  estreitamento (`SB-GAP-006`).
- Regra de quantificacao fixada: "para todo operador REALIZADO P que
  satisfaca INDIVIDUALMENTE as hipoteses". A forma "para todas as
  realizacoes de uma expressao formal" esta proibida.
- `authorized_action`: `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED` ->
  `RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED` (entrada literal
  unica).

### Verified

- `lake build` PASS com 8.692 jobs; probe isolado exit 0; tokens proibidos
  zero; `ASYM-NOGO-001` **nao** aplicado.
- pytest 2 passed; `labctl validate` PASS.

### Blocked

- `SB-GAP-001` / `GAP-RH-014`: **`C_P > 0` nao eh afirmado por nenhuma
  fonte obtida** - bloqueante para `POWER-LAW-FOR-NP`.
- `SB-GAP-002` / `GAP-RH-012`: discretude eh hipotese incorporada.
- `SB-GAP-003`: convencoes de fronteira (`<` vs `<=`) nao reconciliadas.
- `SB-GAP-010`: `RVM-LIMIT` fora de alcance de formalizacao.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

### Result

- `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_READY`.

## RH-NOGO-001 — fonte global e reformulação da classe — 2026-07-31

### Added

- Separação arquitetural em duas classes: `W_POWER_CLASS.md` (assintótica
  abstrata; nenhuma EDP) e `W_ELLIPTIC_CLASS.md` (v2: pseudodiferencial
  clássico, positivo, auto-adjunto, ordem `m > 0`, variedade compacta).
- `HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md`: as sete etapas A–G com estado e
  fonte de cada uma, mais os cinco pontos que o gate proibiu chamar de
  triviais.
- `GLOBAL_WEYL_THEOREM_CANDIDATES.md`, `GLOBAL_WEYL_CONSTANT.md`,
  `CLASS_W_V2_DECISION.md`, `SELF_ADJOINT_REALIZATION_DECISION.md`,
  `ORDER_PARITY_AUDIT.md`, `ADDITIONAL_SOURCE_AUDIT.md`.
- Fontes obtidas por acesso público (arXiv), com `sha256`: Ivrii 2016
  (*100 years of Weyl's law*, 90 pp.) e Coriasco–Doll 2020 (*Weyl Law on
  Asymptotically Euclidean Manifolds*, 26 pp.).

### Verified

- **A lei de Weyl global existe com hipóteses precisas.** Coriasco–Doll
  p. 1: *"positive elliptic self-adjoint classical pseudodifferential
  operator of order `m > 0` on a compact manifold"*,
  `N(λ) = #{j : λ_j < λ}`, `N(λ) = γλ^{d/m} + O(λ^{(d−1)/m})`.
- Ivrii (3.1.3) dá a constante correta para **sistemas**:
  `κ₀ = (2π)^{−d}∬ n(x,ξ)dxdξ`, `n` = nº de autovalores do símbolo
  principal em `(0,1)` — não um volume escalar.
- Ivrii (3.1.11) escreve a identidade local→global
  `N⁻(λ) = ∫ e(x,x,λ)dx`, que era a etapa ausente.
- Ivrii 3.1.1(iv): a assintótica de **um termo** vale sem hipótese de não
  degenerescência — suficiente para `W-POWER`.

### Corrected

- **Atribuição bibliográfica (GAP-RH-013).** Coriasco–Doll atribuem a lei
  global a "Hörmander [15]" = Acta Math. 121 (1968), 193–218, artigo que
  enuncia apenas a lei **local**. Regra adotada: citar Hörmander pelo
  resultado local; a lei global por Coriasco–Doll/Ivrii ou pela ponte
  explícita. Hörmander 1968 **não** foi reclassificado.
- `GAP-RH-010` (auto-adjunção) e `GAP-RH-011` (paridade da ordem)
  fechados **por reformulação**, não por prova. `OPERATOR_CLASS.md` (v1)
  não foi editado: permanece como registro do que a auditoria refutou.

### Changed

- Decisões: classe `REFORMULATE_AS_CLASSICAL_PSEUDODIFFERENTIAL`; ordem
  `PSEUDODIFFERENTIAL_POSITIVE_ORDER`; auto-adjunção
  `positive_self_adjoint_operator` (uma realização).
- `authorized_action`: `RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED` →
  `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED` (entrada literal única).

### Blocked

- `RETRIEVAL_FAILED`: Safarov–Vassiliev, Shubin e a monografia de Ivrii —
  comerciais; nenhuma tentativa de burlar acesso. As **provas** da lei
  global permanecem em textos não lidos.
- Abertos: `GAP-RH-009` (fibrados/sistemas na etapa D — `UNRESOLVED`),
  `GAP-RH-012` (discretude, `PARTIALLY_SUPPORTED`), `GAP-RH-014`
  (positividade de `C_P`), bordo `AMBIGUOUS`.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
  `ASYM-NOGO-001` **não** aplicado; nenhum teorema Lean criado; nenhuma
  claim promovida.

### Result

- `RH_NOGO_LOCAL_TO_GLOBAL_BRIDGE_SUFFICIENT`.

## RH-NOGO-001 — auditoria de fontes primárias — 2026-07-31

### Added

- Acervo de fontes em `08_REVIEWS/SOURCES/RH_NOGO/`: quatro PDFs originais
  não modificados, com proveniência, tamanho e `sha256` em
  `SOURCE_MANIFEST.yaml`; extrações de texto marcadas como derivadas.
  Nenhuma OCR usada.
- Auditorias por documento: `VON_MANGOLDT_1905_AUDIT.md` (12 perguntas
  respondidas com citação de página), `HORMANDER_1968_AUDIT.md` (17
  perguntas), `RIEMANN_1859_AUDIT.md`, `BOMBIERI_CLAY_AUDIT.md`.
- `CLASS_W_SOURCE_MAPPING.md`: matriz W1–W8 contra fonte primária.
- `SOURCE_BRIDGE_REQUIREMENTS.md`: mapa lógico A–H, sem prova.
- `UNRESOLVED_SOURCE_QUESTIONS.md`: dez questões abertas.

### Verified

- **Pilar A sustentado.** von Mangoldt 1905 p. 19 prova, para `T > 28,558`,
  `N = (T/2π)l(T/2π) − T/2π + 7/8 + η(0,43200 lT + 1,91662 llT + 12,20373)`,
  `−1 < η < 1`. Contagem por parte real de `ξ(t)`, **com multiplicidade**
  ("jede so oft gezählt, als ihre Ordnungszahl angibt", p. 2), `T` escolhido
  fora de zeros, método do princípio do argumento — **incondicional**.
- Riemann 1859 (tradução Wilkins, lida integralmente) apenas esboça e
  declara faltar prova estrita; Bombieri/Clay confirma
  ("states, sketching a proof").

### Blocked

- **Pilar B parcialmente sustentado.** Hörmander 1968 prova a lei de Weyl
  **local** da função espectral (eq. 5.3, p. 215) mas **não enuncia** a
  contagem global `N_P(Λ) ~ C_P Λ^(d/m)`. Busca no texto integral por
  "number of eigenvalues" / "counting function" / `N(λ)`: nenhuma
  ocorrência.
- Classe W: apenas W4 e W6 `SUPPORTED_DIRECTLY`; W7 e W8 `NOT_SUPPORTED`;
  W5 `AMBIGUOUS` (Friedrichs vs. essencial auto-adjunção); W2 cobre apenas
  sistemas com autovalores distintos do símbolo principal.
- A cadeia da ponte quebra na etapa E de `SOURCE_BRIDGE_REQUIREMENTS.md`.

### Changed

- `authorized_action`: `RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED` →
  `RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED` (entrada literal única
  no allowlist). `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED` **não**
  foi concedida, por decisão B.
- `GAP-RH-002` → `AUDITED_INSUFFICIENT`; abertos `GAP-RH-009` a
  `GAP-RH-012`.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- Nenhum teorema Lean escrito, nenhuma claim criada ou promovida.

### Result

- `RH_NOGO_PRIMARY_SOURCES_PARTIALLY_SUFFICIENT`.

## ASYM-NOGO-001 — 2026-07-31

### Added

- Núcleo assintótico formalizado em
  `TamesisLab/RHNogo/AsymptoticCore/{Definitions,Normalization,PowerLog,Incompatibility,Audit}.lean`,
  agregador e teste `Tests/RHNogoAsymptotic001.lean`: 4 definições e 12
  teoremas rastreáveis (ASYM-NOGO-ALG/PL/AUX/CONTRA/PROBE).
- Teorema principal `asym_nogo_001`: nenhuma função real admite
  simultaneamente `N(T)/(T log T) → c > 0` e `N(T)/T^α → C > 0` com `α > 0`.
- `ASYM_NOGO_001_THEOREM_MAP.md` e `ASYM_NOGO_001_PROOF_AUDIT.md`
  (auditoria adversarial + `#print axioms`).
- `EPISTEMIC_CORRECTIONS.md` com os dois eixos separados
  (`source_retrieval_status` / `mathematical_claim_status`).
- Claim `ASYM-NOGO-FORMAL-001` (`F`, `formal_asymptotics`, VERIFIED).

### Corrected

- Afirmação de exaustividade sobre a literatura substituída por
  "amostra bibliográfica catalogada nesta sessão" em `DEFINITIONS.md` e
  `EXCLUSIONS.md`.
- `sources_audited` → `bibliographic_records_classified` em
  `rh-nogo-001-specification-result.json`; nenhuma obra está
  `CONTENT_AUDITED`. O relatório de sessão anterior não foi reescrito.
- `SignatureProbe.lean`: nota registrando que o enunciado, antes sem corpo
  probatório, passou a ser provado.

### Changed

- `authorized_action`: `RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED`
  → `RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED`; entrada literal acrescentada
  ao allowlist do `labctl`, sem wildcard.
- `GAP-RH-004` fechado (`CLOSED_BY_FORMALIZATION`).

### Verified

- `lake build` PASS (8.691 jobs); teste isolado PASS; tokens proibidos zero.
- `#print axioms`: apenas `propext`, `Classical.choice`, `Quot.sound`.
- pytest 2 passed; `labctl validate` PASS.
- `ASYM_NOGO_001_VERIFIED`.

### Blocked

- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`; a ponte
  para Riemann–von Mangoldt e para a lei de Weyl depende de leitura
  primária (GAP-RH-002, GAP-RH-003).
- Nenhuma claim sobre a Hipótese de Riemann foi promovida.

## RH-NOGO-001 (especificação) — 2026-07-31

### Added

- Especificação completa da frente em `03_MILLENNIUM/01_RIEMANN/`:
  `OPERATOR_CLASS.md` (Classe W, W1–W8), `TARGET_RESULT.md` (enunciado
  candidato em três níveis), `DEFINITIONS.md` (as 14 questões obrigatórias
  respondidas), `ASSUMPTIONS.md`, `ASYMPTOTIC_CORE.md` (sublema
  `ASYM-NOGO-001` com análise de casos e estratégia), `EXCLUSIONS.md`,
  `ESCAPE_ROUTES.md` (14 rotas não cobertas), `BIBLIOGRAPHY_AUDIT.md`
  (8 fontes classificadas), `CLAIM_MATRIX.md`
  (ESTABLISHED/CONDITIONAL/PROPOSED/OUT_OF_SCOPE), `LEAN_FEASIBILITY.md`,
  `STOP_CONDITIONS.md`, `GAP_REGISTER.yaml` (GAP-RH-001..008),
  `DEPENDENCY_DAG.yaml`, `LEAN_MAP.md`, `PROOF_SKETCH.md` (sem execução).
- `05_FORMAL/lean/TamesisLab/RHNogo/SignatureProbe.lean`: `Prop` do núcleo
  abstrato **sem corpo probatório** + `#check` das ferramentas Mathlib
  previstas. Compila (`lake build` 8.684 jobs).

### Changed

- `authorized_action`: `RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED` →
  `RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED` (entrada literal
  acrescentada ao allowlist do `labctl`; sem wildcard).
  `RH_NOGO_PROOF_EXECUTION` **não** foi autorizado.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`;
  acrescentado `specification_status: SPECIFICATION_READY` na fila.

### Verified

- Fontes: Riemann 1859, von Mangoldt 1905, Bombieri/Clay, Hörmander 1968,
  Berry–Keating 1999, Connes 1999, Bender–Brody–Müller 2017 e o preprint
  Hedenmalm 2026 (existência confirmada em listagem arXiv nesta sessão;
  classificado como preprint não revisado, em
  `CLAIMS_REQUIRING_INDEPENDENT_AUDIT`).
- Ferramentas assintóticas presentes na Mathlib fixada
  (`isLittleO_log_rpow_atTop`, `tendsto_log_atTop`, `rpow`, `IsLittleO`).
- `RH_NOGO_001_SPECIFICATION_READY`.

### Blocked

- Prova do no-go completo: bloqueada por GAP-RH-002 (transcrição da versão
  exata da lei de Weyl de Hörmander 1968) e sem autorização.
- Nenhuma claim científica foi criada ou promovida neste gate.

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
