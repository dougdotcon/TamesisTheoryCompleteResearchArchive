---
schema: tamesis-formal-lab-state/1
schema_extension_note: >
  Esta sessão usou temporariamente um campo aditivo active_work_items
  (lista) sob o schema/1 existente (additionalProperties: true) para
  registrar execução paralela. A onda fechou nesta mesma sessão — as
  cinco frentes migraram para closed_work_items abaixo, e o campo foi
  removido. Mudança pedida explicitamente na sessão 2026-08-09,
  autorizada por PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09.
updated_at: 2026-08-11T00:00:00-03:00
canonical_commit: "920be31ffe0ccd5171b15c5b0a35ce8826dcc569"
canonical_commit_policy: >
  Aponta para o último commit canônico integralmente encerrado
  antes da sessão atual. Deve existir e ser ancestral do HEAD.
  Igualdade com o HEAD é válida no começo de uma sessão; a
  ancestralidade NÃO é estrita.
repository_clean: true
active_track: "multi (millennium + toe_synthesis)"
active_work_item: "WAVE5-BATCH-001"
work_status: "VERIFIED"
specification_status: "APPROVED"
specification_review: "N_A_SELF_SPECIFIED"
formalization_status: "VERIFIED"
result_review: "APPROVED"
extension_status: "NOT_AUTHORIZED"
external_integration_status: "NOT_AUTHORIZED"
relational_bisimulation_status: "NOT_AUTHORIZED"
nondeterministic_systems_status: "NOT_AUTHORIZED"
bisimulation_status: "NOT_AUTHORIZED"
quotient_status: "NOT_AUTHORIZED"
extraction_status: "NOT_AUTHORIZED"
cli_status: "NOT_AUTHORIZED"
parser_status: "NOT_AUTHORIZED"
integration_status: "NOT_AUTHORIZED"
evidence_level: "F"
formalized_at_commit: "this integration commit (Wave 5 batch, 14 new files committed together)"
last_verified_artifact: "14 Wave-5 Lean files across 8 research lines + shared infrastructure (see RESEARCH_QUEUE.yaml WAVE5-* entries for exact paths) -- each independently recompiled by this session directly (lake env lean, foreground, exit 0 on all 14, one file re-run standalone after a batch timeout), zero forbidden tokens (sorry/admit/axiom/unsafe) via independent grep -nw on all 14, axiom footprints reconstructed independently from the raw log output (not from report transcriptions) for every declaration -- subset of [propext, Classical.choice, Quot.sound] in 100% of cases, zero sorryAx -- one central full lake build after all 14 landed (exit 0, 8825 jobs, unchanged job count confirming standalone/unregistered status, identical to Waves 1-4), zero modification to any pre-existing tracked file (git status confirmed: exactly 14 new untracked files) -- on top of each item's own implementer self-check and independent adversarial reviewer pass within the workflow (28 agents total across the batch). First wave with a full 14/14 CLOSED result (10 VERIFIED + 4 VERIFIED_WITH_NOTES, 0 GAP_DIAGNOSED, 0 REJECTED). RH-6C closes a genuine honesty gap (Tp_unbounded, never proved by Wave-3/4 siblings despite prose calling Tp \"unbounded\"). HG-4F's own formalizer independently re-verified HG-4E's closure before attempting the gated Estagio 2. BSD-6 reported minimal scope and optional extension as separate individually-verified results, touching neither BSD-GAP-008 nor the BSD conjecture."
current_blocker: null
next_single_action: >
  WAVE5-BATCH-001 (14 itens da Onda 5 do plano de ataque de portfólio,
  DEC-097/DEC-098) fechou VERIFIED / result_review APPROVED (DEC-099).
  14 de 14 CLOSED (10 VERIFIED, 4 VERIFIED_WITH_NOTES -- RH-6a, RH-6b,
  RH-6c, YM-CAPSTONE-EIGVAL-DICHOTOMY, todas notas menores/cosméticas,
  sem problema de corretude), 0 GAP_DIAGNOSED, 0 REJECTED -- primeiro
  fechamento total 14/14 do ciclo de ondas. **ACHADO NOTÁVEL:** `RH-6c`
  formaliza pela primeira vez que `Tp` é genuinamente não limitado
  (`¬ ∃ C : ℝ, ∀ x : Tp.domain, ‖(Tp x : H2)‖ ≤ C * ‖(x : H2)‖`) --
  nenhum irmão das Ondas 3-4 provava isso apesar de chamar `Tp` de
  "operador não limitado" em prosa repetidamente. Classificado como
  resultado de esclarecimento sobre um operador de brinquedo, **não**
  como progresso sobre a Hipótese de Riemann (reafirmado em
  `prohibited_claims`). `HG-4F` executou corretamente seu próprio gate
  interno de dois estágios: o agente formalizador re-verificou de forma
  independente (recompilação + `#print axioms` próprios) que `HG-4E`
  havia genuinamente fechado antes de tentar o Estágio 2 gated. `BSD-6`
  reportou escopo mínimo e extensão opcional como resultados
  SEPARADOS, ambos individualmente verificados; não toca `BSD-GAP-008`
  (que permanece `OPEN`) nem alega progresso sobre a conjectura BSD.
  Linha `PN` confirmada formalmente esgotada nesta onda (0 candidatos).
  Verificação em quatro camadas idêntica às Ondas 1-4 para todos os 14
  itens: `lake env lean` exit 0 em todos, zero token proibido via
  `grep -nw` independente, axiomas reconstruídos a partir do log bruto
  para cada declaração (zero `sorryAx`), `lake build` central sem
  regressão (8825 jobs). `git status` confirmou que NENHUM arquivo
  pré-existente foi tocado -- apenas 14 arquivos `.lean` novos. Ver
  `09_SESSIONS/2026/2026-08-11_WAVE5_EXECUTION.md` para detalhe
  completo por item. `authorized_action` volta a
  `PORTFOLIO_REVIEW_REQUIRED`. Próximo passo: decisão de portfólio
  pendente sobre encerramento formal da linha `PN` como sub-frente
  esgotada, e sobre se/quando `BSD-GAP-008` vira projeto dedicado
  separado fora do ciclo de ondas (ambas ainda não decididas, apenas
  nomeadas pelo plano da Onda 5) -- ou continuação do ciclo de ondas no
  mesmo modo para as linhas que ainda produzem candidatos
  (RH/HG/QF/YM/SHARED-INFRA).
  ---
  (histórico anterior preservado abaixo)
  ---
  WAVE5-BATCH-001 (14 itens da Onda 5 do plano de ataque de portfólio,
  DEC-097/DEC-098) registrado e o gate de execução aberto. Pedido
  explícito do usuário ("Siga para onda 5"), continuação direta do
  ciclo. Plano da Onda 5 produzido por workflow de 19 agentes
  fundamentado nos arquivos reais da Onda 4 (incluindo o fechamento de
  BSD-GAP-007). 14 candidatos revisados, 14 formam a lista de execução
  -- mesma contagem numérica que a Onda 4, mas por composição diferente:
  PN caiu de 1 para 0 (primeira linha a esgotar genuinamente em cinco
  ondas, recomendada para encerramento formal como sub-frente de
  cobertura de construtor), enquanto RH cresceu de 2 para 3 e QF de 1
  para 2. Zero candidato REFUTED nesta rodada. O documento nomeia
  `BSD-GAP-008` (Mordell-Weil fraco, 5 lacunas formais separadas) como o
  candidato mais maduro para projeto dedicado de escala própria -- mais
  maduro agora que `BSD-GAP-007` provou que uma cadeia longa de
  composição pode fechar neste laboratório -- mas nenhum item desta
  onda toca `BSD-GAP-008`. `authorized_action` -> `FORMALIZATION`.
  Próximo passo: dispatch do workflow de execução, depois verificação
  independente completa desta sessão antes de qualquer integração.
  ---
  (histórico anterior preservado abaixo)
  ---
  WAVE4-BATCH-001 (14 itens da Onda 4 do plano de ataque de portfólio,
  DEC-094/DEC-095) fechou VERIFIED / result_review APPROVED (DEC-096).
  14 de 14 CLOSED (10 VERIFIED, 4 VERIFIED_WITH_NOTES -- RH-4, RH-5,
  YM-CAPSTONE-FULL, HG-1E, todas notas menores/cosméticas, sem problema
  de corretude), 0 GAP_DIAGNOSED, 0 REJECTED. **ACHADO CENTRAL:**
  `WAVE4-BSD-1-STEP5-COMPOSE` fechou genuinamente `BSD-GAP-007` (aberto
  desde a Onda 1) -- STEP5a produz
  `IsLocalRing.ResidueField (v.adicCompletionIntegers K) ≃+*
  (𝓞 K ⧸ v.asIdeal)`, comparado letra por letra e confirmado idêntico ao
  alvo nomeado em `BSD-1_GAP_NOTE.md` linha 95; STEP5b usa isso para
  provar `WeierstrassCurve.LFunction_isMultiplicative` SEM hipótese,
  universalmente sobre TODO lugar `v`, exatamente o "alvo incondicional"
  que a linha 134 do gap note dizia permanecer não-provado. Verificado
  com escrutínio extra por esta sessão (não apenas autorrelato):
  recompilação própria, leitura integral do arquivo de 389 linhas,
  comparação byte a byte contra os três arquivos-fonte citados como
  "reproduzidos". Rota diferente da originalmente prevista pelo gap note
  (via `Valuation.HasExtension` do próprio Mathlib), mas entrega
  exatamente o mesmo objeto e teorema-alvo. **O que isso NÃO significa:**
  nenhum progresso sobre a conjectura de Birch e Swinnerton-Dyer --
  `IsMultiplicative` de coeficientes de Dirichlet é propriedade
  estrutural básica, não toca `LSeries`/continuação analítica/equação
  funcional/posto de Mordell-Weil. `BSD-GAP-008` permanece `OPEN`.
  Verificação em quatro camadas idêntica às Ondas 1-3 para os outros 13
  itens: lake env lean exit 0 em todos os 14, zero token proibido,
  axiomas reconstruídos para os 2 arquivos sem `#print axioms` embutido
  (zero sorryAx em todos os 14), lake build central sem regressão (8825
  jobs). git status confirmou que NENHUM arquivo pré-existente foi
  tocado -- apenas 14 arquivos `.lean` novos. Ver
  09_SESSIONS/2026/2026-08-11_WAVE4_EXECUTION.md para detalhe completo
  por item. `authorized_action` volta a `PORTFOLIO_REVIEW_REQUIRED`.
  ---
  (histórico anterior preservado abaixo)
  ---
  WAVE4-BATCH-001 (14 itens da Onda 4 do plano de ataque de portfólio,
  DEC-094/DEC-095) registrado e o gate de execução aberto. Usuário
  respondeu explicitamente "1" a uma pergunta de três opções levantada
  nesta sessão (continuar o ciclo de ondas no mesmo modo vs. pausar para
  um gate dedicado `TOE_INTERFACE_EXECUTION` vs. modo híbrido com um
  projeto dedicado para `BSD-GAP-007`) -- opção 1 escolhida: continuar o
  ciclo de ondas. Plano da Onda 4 produzido por workflow de 19 agentes
  fundamentado nos arquivos reais da Onda 3, com atenção especial à
  pergunta central sobre BSD: revisão adversarial confirmou que
  `BSD-1-STEP3`/`STEP4` (Onda 3), embora por rota diferente da
  originalmente prevista, alcançam o mesmo objeto que `BSD-1_GAP_NOTE.md`
  pedia -- mas compor isso (`STEP5a`) ainda não foi tentado, e mesmo se
  fechar, alimentar isso na versão incondicional de
  `WeierstrassCurve.LFunction.IsMultiplicative` (`STEP5b`) é checkpoint
  separado não verificado. Nomeado com precisão como
  `BSD-GAP-007-RESIDUAL`, não declarado fechado. 15 candidatos revisados,
  14 formam a lista de execução (contagem caindo estruturalmente onda a
  onda: 25 -> 20 -> 15 -> 14); zero REFUTED nesta rodada -- primeira onda
  desde a Onda 2 com essa característica, mas a revisão adversarial
  efetivamente recompilou dois candidatos inteiros e encontrou/corrigiu
  um erro matemático substantivo (hipótese route-b incondicional falsa em
  RH-5, contraexemplo mu=i, Lam=0.5, antes do despacho). O documento
  também recomenda um modo híbrido para o futuro (não adotado nesta
  rodada): abrir projeto dedicado para `BSD-GAP-007` em vez de tratá-lo
  como item de onda. `authorized_action` -> `FORMALIZATION`. Próximo
  passo: dispatch do workflow de execução, depois verificação
  independente completa desta sessão antes de qualquer integração.
  ---
  (histórico anterior preservado abaixo)
  ---
  WAVE3-BATCH-001 (15 itens da Onda 3 do plano de ataque de portfólio,
  DEC-091/DEC-092) fechou VERIFIED / result_review APPROVED (DEC-093).
  15 de 15 CLOSED (12 VERIFIED, 3 VERIFIED_WITH_NOTES -- PN-6, HG-1D,
  TOE-3E, todas notas menores/cosméticas, sem problema de corretude), 0
  GAP_DIAGNOSED, 0 REJECTED. Verificação em quatro camadas idêntica às
  Ondas 1-2: implementador auto-verifica -> revisor adversarial
  independente recompila -> esta sessão recompila TODOS os 15 arquivos
  por conta própria (lake env lean, exit 0 em todos), reconstrói axiomas
  para os 2 arquivos sem #print axioms embutido (zero sorryAx em todos
  os 15) -> uma lake build central confirma zero regressão (8825 jobs,
  mesma contagem de antes). git status confirmou que NENHUM arquivo
  pré-existente foi tocado -- apenas 15 arquivos .lean novos (13 em
  diretórios FORMAL/ já existentes + 2 em TamesisLab/TOE/). `NS-GAP-001`
  e os demais gaps centrais de cada Problema do Milênio permanecem
  abertos -- nenhuma linha destas 15 toca o problema central de forma
  alguma. Ver 09_SESSIONS/2026/2026-08-10_WAVE3_EXECUTION.md para
  detalhe completo por item. `authorized_action` volta a
  `PORTFOLIO_REVIEW_REQUIRED`.
  ---
  (histórico anterior preservado abaixo)
  ---
  WAVE2-BATCH-001 (20 itens da Onda 2 do plano de ataque de portfólio,
  DEC-088/DEC-089) fechou VERIFIED / result_review APPROVED (DEC-090).
  20 de 20 CLOSED (18 VERIFIED, 2 VERIFIED_WITH_NOTES -- RH-1, HG-1B,
  ambas notas menores/cosméticas, sem problema de corretude), 0
  GAP_DIAGNOSED, 0 REJECTED -- melhor taxa de fechamento que a Onda 1
  (25/27). Verificação em quatro camadas idêntica à Onda 1: implementador
  auto-verifica -> revisor adversarial independente recompila -> esta
  sessão recompila TODOS os 20 arquivos por conta própria (lake env
  lean, exit 0 em todos), reconstrói axiomas para os 2 arquivos sem
  #print axioms embutido (zero sorryAx em todos os 20) -> uma lake build
  central confirma zero regressão (8825 jobs, mesma contagem de antes).
  git status confirmou que NENHUM arquivo pré-existente foi tocado --
  apenas 20 arquivos .lean novos (17 em diretórios FORMAL/ já existentes
  + 3 no novo diretório 03_MILLENNIUM/_SHARED_INFRA/FORMAL/).
  Peculiaridade técnica diagnosticada e corrigida: RVMLimit.lean (saída
  da Onda 1) nunca fora compilado no cache .lake/ compartilhado por não
  ser importado por nenhum arquivo registrado -- esta sessão compilou-o
  diretamente para dentro do cache de build (artefato gitignored, não
  arquivo fonte) para que RH-1 recompile com exit 0 de forma
  reprodutível. `NS-GAP-001` e os demais gaps centrais de cada Problema
  do Milênio (incluindo BSD-GAP-007/008, abertos na Onda 1) permanecem
  abertos -- nenhuma linha destas 20 toca o problema central de forma
  alguma. Ver 09_SESSIONS/2026/2026-08-10_WAVE2_EXECUTION.md para
  detalhe completo por item. `authorized_action` volta a
  `PORTFOLIO_REVIEW_REQUIRED`.
  ---
  (histórico anterior preservado abaixo)
  ---
  WAVE1-BATCH-001 (27 itens da Onda 1 do plano de ataque de portfólio,
  DEC-085/DEC-086) fechou VERIFIED / result_review APPROVED. Pedido
  explícito do usuário ("Onda 1 completa, todas as 24" -- contagem real
  27, corrigida) após apresentação do plano de ataque completo. Cada um
  dos 27 itens: implementador formaliza + auto-verifica no primeiro
  plano -> revisor adversarial independente recompila e re-verifica
  citações -> esta sessão recompila TODOS os 27 arquivos por conta
  própria (lake env lean, exit 0 em todos), reconstrói o footprint de
  axiomas para os 6 arquivos sem #print axioms embutido (zero sorryAx em
  todos os 27), roda UMA lake build central (exit 0, 8825 jobs, mesma
  contagem de antes -- confirma que os novos arquivos standalone não
  entraram no build registrado), e confirma via git status que NENHUM
  arquivo pré-existente foi tocado. Resultado: 25 de 27 CLOSED
  (18 VERIFIED, 7 VERIFIED_WITH_NOTES), 2 de 27 GAP_DIAGNOSED com nota de
  gap exaustiva e honesta (BSD-1: multiplicatividade condicional de
  WeierstrassCurve.LFunction provada, mas o lado incondicional trava numa
  lacuna genuína de compatibilidade de corpo de resíduo entre dois
  frameworks de completação do Mathlib nunca conectados; BSD-4:
  levantamento dos 5 gaps reais que faltam para invocar
  AddCommGroup.fg_of_descent' e obter Mordell-Weil fraco, maior e mais
  espalhado do que a recon original supôs). ZERO REJECTED. `NS-GAP-001`
  e os demais gaps centrais de cada Problema do Milênio permanecem
  abertos -- nenhuma linha destas 27 toca o problema central de forma
  alguma; são todas peças de infraestrutura auxiliar ou resultados
  negativos/de esclarecimento, exatamente como o plano prometeu. Ver
  09_SESSIONS/2026/2026-08-09_WAVE1_EXECUTION.md para detalhe completo
  por item. `authorized_action` volta a `PORTFOLIO_REVIEW_REQUIRED`.
  ---
  (histórico anterior preservado abaixo)
  ---
  FOUND-DIRICHLET-OSCILLATORY-INTEGRAL-001 fechou VERIFIED / result_review
  APPROVED (revisão adversarial: zero problemas, incluindo re-verificação
  da citação de Grafakos contra o OCR em cache da fonte primária).
  Integral de Dirichlet integral(0,infinity) sin(x)/x dx = pi/2 provada
  em Lean (tendsto_integral_sin_div_atTop), item standalone de
  fundamentos gerais, escolhido pelo usuário após a terceira checagem de
  exaustão do dia (PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09_EVE.md) e
  a pesquisa de escopo (RESEARCH_SCOPING_SINGULAR_INTEGRAL_INFRASTRUCTURE_2026_08_09.md)
  que identificou esta integral como a menor unidade irredutível de
  trabalho em qualquer rota rumo a limitação L²/L^p do núcleo
  Constantin-Fefferman. Lema 5.2.5 completo de Grafakos NÃO tentado --
  decisão de escopo deliberada, documentada honestamente no próprio
  arquivo, com o achado de que sua parte real é independente desta
  integral (tarefa futura separada, tamanho comparável). NENHUMA conexão
  a CZKernelClass/fourierMulL2/distribuições p.v. feita. Um usuário
  pediu, à parte, um inventário completo do que falta (infraestrutura
  CZ/integral singular ausente do Mathlib, e as cinco condições de
  reativação de RH-NOGO-001) — respondido diretamente na conversa, não
  como documento de governança separado. `authorized_action` volta a
  `PORTFOLIO_REVIEW_REQUIRED`. Próxima frente exige revisão de
  portfólio: candidatos honestos incluem (a) o Lema 5.2.5 completo de
  Grafakos como continuação direta, (b) o construtor de distribuições de
  valor principal necessário para a Proposição 5.2.3, ou (c) qualquer
  uma das três condições já nomeadas em ciclos anteriores (reativação de
  RH-NOGO-001, decisão do usuário sobre investimento maior, colaborador
  especializado).
  ---
  (histórico anterior preservado abaixo)
  ---
  FOUND-CZ-KERNEL-DEFINITIONS-001 fechou VERIFIED / result_review
  APPROVED_WITH_NOTES (revisão adversarial com escrutínio reforçado:
  0 problemas de solidez matemática; 1 citação Mathlib fabricada
  encontrada e corrigida — não usada em nenhuma prova, apenas em prosa
  de docstring). Camada definicional de Calderón-Zygmund formalizada:
  integral de valor principal local (com instância positiva), classe
  estrutural CZKernelClass (parametrizada por medida μ arbitrária —
  sphereSurfaceMeasure oferecida como instanciação concreta), e
  homogeneidade de grau -3 + suavidade C^∞ fora da origem PROVADAS para
  a peça de coeficiente congelado K(y):=D(ŷ,e2,e3)/‖y‖³. Média zero para
  esse K concreto NÃO foi tentada — registrada honestamente como
  intratável nesta janela de escopo. NS-GAP-001 permanece OPEN, anotado
  com cross-referência. Fila volta a exigir revisão de portfólio antes
  de qualquer frente nova.
  ---
  (histórico anterior preservado abaixo, por política de não reescrever
  next_single_action retroativamente)
  ---
  FOUND-CZ-KERNEL-DEFINITIONS-001 aberta (SCOPED), extensão nomeada da
  exceção de DEC-076 via DEC-078. Escopo (camada definicional apenas,
  escolhido explicitamente pelo usuário diante do achado de que o
  Mathlib não tem nenhuma infraestrutura de Calderón-Zygmund/BMO/
  maximal/interpolação/p.v.): (1) integral de valor principal LOCAL em
  R^3; (2) classe estrutural de núcleo Calderón-Zygmund (homogêneo grau
  -3, suave fora da origem, média zero sobre a esfera unitária); (3)
  verificação de homogeneidade (e, se tratável, média zero — não
  forçada, gap nomeado se intratável) da peça de coeficiente congelado
  K(y):=D(ŷ,e2,e3)/|y|³, reusando D já formalizado em
  FOUND-CF-DEPLETION-KERNEL-001. NENHUMA limitação L^p, NENHUM teorema
  CZ completo, NENHUMA estimativa sobre a integral p.v. real aplicada a
  campo de vorticidade genuíno, NENHUM progresso em NS-GAP-001/004.
  Próximo passo: dispatchar formalização Lean, verificar build de forma
  independente, revisão adversarial com escrutínio reforçado (mesma
  classe de sensibilidade da frente anterior).
  ---
  Contexto: pedido explícito do usuário de reavaliar a governança para
  continuar atacando, fundamentado exclusivamente em fontes reais
  verificadas. Exploração completa de cinco clusters do corpus Tamesis
  (09_SESSIONS/2026/2026-08-09_TAMESIS_CORPUS_EXPLORATION.md) não
  encontrou nenhuma alavanca de análise harmônica/Calderón-Zygmund
  utilizável — confirmado pelas próprias autoauditorias do corpus.
  Direção escolhida pelo usuário: formalizar Constantin-Fefferman 1993
  (fonte real, citável). DEC-076 abriu uma exceção NOMEADA e DELIMITADA
  ao stop_condition de NS-PRESSURE-001: FOUND-CF-DEPLETION-KERNEL-001,
  o núcleo algébrico de depleção geométrica
  D(e1,e2,e3):=(e1·e3)·det(e1,e2,e3) — NÃO o teorema completo, que
  continua fora de escopo. Formalização concluída e fechada
  (FOUND-CF-DEPLETION-KERNEL-001, VERIFIED/APPROVED_WITH_NOTES). Usuário
  pediu "vamos construir a teoria de operadores"; avaliação honesta
  (busca exaustiva no Mathlib) mostrou zero infraestrutura CZ existente
  — um programa de meses/anos se atacado por inteiro. Usuário escolheu,
  diante dessa realidade, a camada definicional apenas para este ciclo
  (ver início deste campo).
authorized_action: "PORTFOLIO_REVIEW_REQUIRED"
attack_plan_document: "01_PORTFOLIO/PLANO_DE_ATAQUE_PORTFOLIO_COMPLETO_2026_08_09.md"
wave1_batch_authorization: "DEC-086, 27 itens WAVE1-*, escolhido pelo usuario via AskUserQuestion"
wave2_attack_plan_document: "01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md"
wave2_batch_authorization: "DEC-089, 20 itens WAVE2-*, continuacao direta do ciclo pedida explicitamente pelo usuario"
wave2_closure: "DEC-090, 20/20 CLOSED (18 VERIFIED + 2 VERIFIED_WITH_NOTES), 0 GAP_DIAGNOSED, 0 REJECTED"
wave3_attack_plan_document: "01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_3_2026_08_10.md"
wave3_batch_authorization: "DEC-092, 15 itens WAVE3-*, pedido explicito do usuario (\"Siga para onda 3\")"
wave3_closure: "DEC-093, 15/15 CLOSED (12 VERIFIED + 3 VERIFIED_WITH_NOTES), 0 GAP_DIAGNOSED, 0 REJECTED"
wave4_attack_plan_document: "01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_4_2026_08_10.md"
wave4_batch_authorization: "DEC-095, 14 itens WAVE4-*, usuario escolheu opcao 1 (continuar ciclo de ondas) entre 3 apresentadas"
wave4_closure: "DEC-096, 14/14 CLOSED (10 VERIFIED + 4 VERIFIED_WITH_NOTES), 0 GAP_DIAGNOSED, 0 REJECTED"
wave4_bsd_gap_007_status: "CLOSED por WAVE4-BSD-1-STEP5-COMPOSE (DEC-096) -- ver GAP_REGISTER.yaml para detalhe completo e prohibited_claims_reaffirmed"
wave5_attack_plan_document: "01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md"
wave5_batch_authorization: "DEC-098, 14 itens WAVE5-*, pedido explicito do usuario (\"Siga para onda 5\")"
wave5_pn_line_status: "esgotada genuinamente segundo a revisao adversarial -- recomendada para encerramento formal como sub-frente de cobertura de construtor, nao mais reavaliada onda a onda"
wave5_bsd_gap_008_status: "OPEN, nomeado como candidato maduro a projeto dedicado de escala propria -- NAO incluido nesta onda"
wave5_closure: "DEC-099, 14/14 CLOSED (10 VERIFIED + 4 VERIFIED_WITH_NOTES), 0 GAP_DIAGNOSED, 0 REJECTED -- primeiro fechamento total 14/14 do ciclo"
pn_line_wave_rotation_status: "RETIRADA da rotacao de reconhecimento a partir da Onda 6 (DEC-100), por escolha explicita do usuario apos esgotamento genuino na Onda 5 (0 candidatos, apos 1 na Onda 4). Retirada operacional/reversivel -- P vs NP NAO declarado fechado, PNP-GAP-001..004 permanecem OPEN, linha pode ser reativada por decisao de portfolio futura."
portfolio_review_document_dirichlet_oscillatory_integral: "01_PORTFOLIO/PORTFOLIO_REVIEW_DIRICHLET_OSCILLATORY_INTEGRAL_2026_08_09.md"
portfolio_review_document_queue_exhausted_eve: "01_PORTFOLIO/PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09_EVE.md"
portfolio_review_document_cz_mean_zero: "01_PORTFOLIO/PORTFOLIO_REVIEW_CZ_MEAN_ZERO_2026_08_09.md"
portfolio_review_document_cz_kernel_definitions: "01_PORTFOLIO/PORTFOLIO_REVIEW_CZ_KERNEL_DEFINITIONS_2026_08_09.md"
portfolio_review_document_cf_depletion_kernel: "01_PORTFOLIO/PORTFOLIO_REVIEW_CF_DEPLETION_KERNEL_2026_08_09.md"
portfolio_review_document_queue_exhausted_pm: "01_PORTFOLIO/PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09_PM.md"
portfolio_review_document_duhamel_fixedpoint_instance: "01_PORTFOLIO/PORTFOLIO_REVIEW_DUHAMEL_FIXEDPOINT_INSTANCE_2026_08_09.md"
portfolio_review_document_abstract_wellposedness: "01_PORTFOLIO/PORTFOLIO_REVIEW_ABSTRACT_WELLPOSEDNESS_2026_08_09.md"
portfolio_review_status: "CONSUMED"
portfolio_review_document_duhamel_skeleton: "01_PORTFOLIO/PORTFOLIO_REVIEW_DUHAMEL_SKELETON_2026_08_09.md"
portfolio_review_document_parallel_wave_002: "01_PORTFOLIO/PORTFOLIO_REVIEW_PARALLEL_WAVE_002_2026_08_09.md"
portfolio_review_document_heat_semigroup: "01_PORTFOLIO/STRATEGIC_REVIEW_BATTLE_MAP_2026_08_09.md"
portfolio_review_document_leray_orthogonal_sobolev: "01_PORTFOLIO/PORTFOLIO_REVIEW_LERAY_ORTHOGONAL_SOBOLEV_2026_08_09.md"
portfolio_review_document_leray_sobolev: "01_PORTFOLIO/PORTFOLIO_REVIEW_LERAY_SOBOLEV_2026_08_09.md"
portfolio_review_document: "01_PORTFOLIO/PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09.md"
frontmatter_scan_coverage: "FULL"
yaml_scan_files_covered: 390
yaml_scan_markdown_front_matter_covered: 333
yaml_duplicate_key_status: "VERIFIED_CLEAN"
consumed_authorizations: ["LAB_GOV_YAML_DUPLICATE_KEYS_CORRECTION_AUTHORIZED", "LAB_GOV_FRONTMATTER_SCAN_CORRECTION_AUTHORIZED", "LAB_GOV_DECISION_LEDGER_CORRECTION_AUTHORIZED"]
decision_ledger_integrity: "VERIFIED_CLEAN"
decision_citations_unregistered: 0
closed_work_items:
  FOUND-UNIFORM-PRIMREC-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    closes_gap: CB-GAP-001
    cost_model_status: NOT_AUTHORIZED
    complexity_class_status: NOT_AUTHORIZED
    efficiency_claim_status: FORBIDDEN
    proof_consults_algorithm: true
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-COMPUTABILITY-BRIDGE-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    uniform_level_status: STATED_NOT_PROVED
    cost_model_status: NOT_AUTHORIZED
    complexity_class_status: NOT_AUTHORIZED
    canonicity_status: ONE_CASE_NOT_AN_INVARIANCE
    central_result_sign: NEGATIVE
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-MONOVARIANT-DESCENT-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    general_orders_status: NOT_AUTHORIZED
    ordinals_status: NOT_AUTHORIZED
    program_termination_status: NOT_AUTHORIZED
    quantitative_bound_status: NOT_AUTHORIZED
    nondeterministic_systems_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-INVARIANT-UNREACHABILITY-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    relational_invariants_status: NOT_AUTHORIZED
    monovariant_status: NOT_AUTHORIZED
    termination_status: NOT_AUTHORIZED
    complete_invariant_status: NOT_AUTHORIZED
    nondeterministic_systems_status: NOT_AUTHORIZED
    classical_choice_present: false
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-BISIMULATION-BOUNDARY-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    relational_bisimulation_status: NOT_AUTHORIZED
    nondeterministic_systems_status: NOT_AUTHORIZED
    labelled_actions_status: NOT_AUTHORIZED
    coinduction_status: NOT_AUTHORIZED
    quotient_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    axiom_footprint: NONE
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-FINITE-STATE-ABSTRACTION-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    bisimulation_status: NOT_AUTHORIZED
    quotient_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    cli_status: NOT_AUTHORIZED
    parser_status: NOT_AUTHORIZED
    external_integration_status: NOT_AUTHORIZED
    external_abstraction_correctness: PERMANENTLY_OUT_OF_SCOPE
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  FOUND-SEMIGROUP-002:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
  FOUND-FUNCTIONAL-GRAPH-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
  FOUND-CYCLE-DETECTION-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    totalization_status: DEFERRED
    extraction_status: NOT_AUTHORIZED
    optimization_status: NOT_AUTHORIZED
    minimality_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  ENG-FINITE-STATE-RUNTIME-001:
    work_status: VERIFIED
    specification_status: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    cli_status: NOT_AUTHORIZED
    external_format_status: NOT_AUTHORIZED
    integration_status: NOT_AUTHORIZED
    detailed_diagnostics_status: NOT_AUTHORIZED
    external_abstraction_correctness: DEFERRED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  ENG-FINITE-STATE-ENCODING-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: APPROVED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    reencoding_invariance_status: NOT_AUTHORIZED
    extraction_status: NOT_AUTHORIZED
    cli_status: NOT_AUTHORIZED
    parser_status: NOT_AUTHORIZED
    integration_status: NOT_AUTHORIZED
    external_abstraction_correctness: DEFERRED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
  ENG-RUNTIME-SOUNDNESS-002:
    work_status: VERIFIED
    specification_status: APPROVED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    algorithmic_novelty: NONE
    backfilled_at_gate: LAB-CORR-VALIDATION-BLINDNESS-001
  FOUND-SPECTRAL-COUNTING-001:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    closes_gap: SC-GAP-001
    open_gap: SC-GAP-002
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
    backfilled_at_gate: LAB-CORR-VALIDATION-BLINDNESS-001
  FOUND-FOURIER-MULTIPLIER-L2-001:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
    backfilled_at_gate: LAB-CORR-VALIDATION-BLINDNESS-001
  FOUND-ELLIPTIC-HEIGHT-001:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
    backfilled_at_gate: LAB-CORR-VALIDATION-BLINDNESS-001
  FOUND-LERAY-PROJECTOR-001:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    closes_gap: LP-GAP-003
    open_gap: LP-GAP-004
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
    decision_ref: DEC-056, DEC-057
    backfilled_at_gate: LAB-CORR-VALIDATION-BLINDNESS-001
  FOUND-SOBOLEV-SPACE-001:
    work_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
    backfilled_at_gate: LAB-CORR-VALIDATION-BLINDNESS-001
  NS-PRESSURE-001:
    work_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    audit_outcome: REFUTED_NAIVE_FORM_STRENGTHENED_OPEN
    execution_mode: PARALLEL_AUDIT_WAVE
    mathematical_novelty: NONE
    research_role: LITERATURE_AUDIT
    decision_ref: DEC-059, DEC-060, DEC-061
  PVSNP-PHYS-001:
    work_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    audit_outcome: NO_UNIVERSAL_BRIDGE_FOUND
    execution_mode: PARALLEL_AUDIT_WAVE
    mathematical_novelty: NONE
    research_role: LITERATURE_AUDIT
    decision_ref: DEC-059, DEC-060, DEC-061
  YM-LIMIT-001:
    work_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    audit_outcome: INSUFFICIENCY_THEOREM_PROVED
    execution_mode: PARALLEL_AUDIT_WAVE
    mathematical_novelty: NONE
    research_role: LITERATURE_AUDIT
    external_claim_watch: YM-GAP-007
    decision_ref: DEC-059, DEC-060, DEC-061
  HODGE-CDK-001:
    work_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    audit_outcome: SCOPE_DELINEATED_WORKED_CASE
    execution_mode: PARALLEL_AUDIT_WAVE
    mathematical_novelty: NONE
    research_role: LITERATURE_AUDIT
    decision_ref: DEC-059, DEC-060, DEC-061
  BSD-HYP-MATRIX-001:
    work_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    audit_outcome: MATRIX_BUILT_NO_PROOF
    execution_mode: PARALLEL_AUDIT_WAVE
    mathematical_novelty: NONE
    research_role: LITERATURE_AUDIT
    decision_ref: DEC-059, DEC-060, DEC-061
  FOUND-LERAY-PROJECTOR-SOBOLEV-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    closes_gap: LP-GAP-004
    open_gap: LP-GAP-005
    unblocked_by: FOUND-SOBOLEV-SPACE-001
    self_adjoint_claim: FORBIDDEN
    orthogonal_projection_claim: FORBIDDEN
    note: >
      Auto-adjuncao/ortogonalidade FORBIDDEN dentro do escopo desta
      frente especificamente. LP-GAP-005 fechou depois, na frente
      seguinte, via pareamento pullback explicito (nao a API
      IsSelfAdjoint do Mathlib) — ver FOUND-LERAY-PROJECTOR-SOBOLEV-ORTHOGONAL-001.
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-LERAY-PROJECTOR-SOBOLEV-ORTHOGONAL-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    closes_gap: LP-GAP-005
    predecessor: FOUND-LERAY-PROJECTOR-SOBOLEV-001
    scope_note: >
      Auto-adjuncao/ortogonalidade/Pitagoras provados via pareamento
      pullback explicito hsInner (funcao comum), NAO via instancia
      global InnerProductSpace (Hs E F s) nem via
      IsSelfAdjoint/ContinuousLinearMap.adjoint do Mathlib — risco de
      diamante de tipo com a norma ja instalada, evitado por decisao
      deliberada de escopo.
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-HEAT-SEMIGROUP-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    open_gap: HEAT-GAP-001
    strategic_direction_source: STRATEGIC_REVIEW_BATTLE_MAP_2026_08_09.md, DEC-065
    scope_note: >
      Contracao (norma <= 1) e simetria via produto interno
      (inner_heatOpL2_symm, reusando inner_fourierMulL2_symm ja
      verificado) provadas para o semigrupo do calor e^{tDelta} em L^2;
      composto com o projetor de Leray ja caracterizado no operador de
      Stokes P*e^{tDelta}. IsSelfAdjoint/ContinuousLinearMap.adjoint do
      Mathlib NAO foram provados — incompatibilidade de instancia
      Module (Lp.instModule vs InnerProductSpace.toNormedSpace.toModule)
      encontrada ao tentar, nao forcada. Lei de semigrupo
      S(t+r)=S(t)S(r) e continuidade forte em t NAO demonstradas —
      HEAT-GAP-001, aberto de proposito.
    self_adjoint_instance_claim: FORBIDDEN
    semigroup_law_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
    open_gap_closed_by: >
      FOUND-HEAT-SEMIGROUP-LAW-001 (mesma sessao, onda PARALLEL-WAVE-002).
      Este registro nao e reescrito, apenas anotado.
  FOUND-HEAT-SEMIGROUP-LAW-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    closes_gap: HEAT-GAP-001
    predecessor: FOUND-HEAT-SEMIGROUP-001
    parallel_wave: PARALLEL-WAVE-002
    scope_note: >
      Lei de semigrupo (heatOpL2_add/heatOpL2_add', S(t+r)=S(t)∘S(r)) E
      continuidade forte (heatOpL2_continuousAt, para t0 >= 0 arbitrario,
      via convergencia dominada com cota fixa independente do parametro
      variavel) — ambas provadas, nao apenas uma. Revisao adversarial
      corrigiu uma imprecisao factual de contagem de linhas
      (256->408 alegado, 201->408 real); nenhum problema de solidez.
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  NS-GAP-005-RECHECK:
    action_type: BIBLIOGRAPHIC_VERIFICATION
    parent_work_item: NS-PRESSURE-001
    verdict: CONFIRMED_CONDITIONAL
    note: >
      "Seregin-Sverak: Type I blow-up excluido" (citado sem qualificacao
      no documento legado) confirmado CONDICIONAL, nao incondicional:
      ARMA 2002 e criterio de regularidade condicional (hipotese de
      controle de pressao); Comm.PDE 2009 restrito a solucoes
      axissimetricas sob "certas hipoteses naturais" nao detalhadas;
      Acta Math. 2009 (Liouville) reporta o caso 3D geral como "fora de
      alcance das tecnicas existentes". Achado adicional: preprint nao
      verificado (Cheskidov-Dai-Palasek, arXiv:2511.09556, nov. 2025)
      alega CONSTRUIR blow-up Tipo I via nao-unicidade -- registrado como
      claim externa, nao endossada nem refutada.
      Ver 03_MILLENNIUM/02_NAVIER_STOKES/GAP_REGISTER.yaml, campo
      recheck_2026_08_09_parallel_wave_002 em NS-GAP-005.
    research_role: LITERATURE_AUDIT
  YM-GAP-007-RECHECK:
    action_type: BIBLIOGRAPHIC_VERIFICATION
    parent_work_item: YM-LIMIT-001
    verdict: STATUS_UPDATED
    note: >
      arXiv:2506.00284 continua retirada (motivo generico de padrao de
      qualidade do arXiv, sem refutacao matematica especifica
      encontrada). arXiv:2606.19362 ganhou journal-ref desde a ultima
      checagem (Fortschr. Phys. 74(2026)4, e70097) -- status atualizado
      para "publicamente verificavel como publicada em revista com
      revisao por pares"; este laboratorio continua sem avaliar se essa
      revisao foi adequada ao escopo da alegacao. Nenhuma nova preprint
      2026 relevante encontrada.
      Ver 03_MILLENNIUM/04_YANG_MILLS/GAP_REGISTER.yaml, campo
      recheck_2026_08_09_parallel_wave_002 em YM-GAP-007.
    research_role: LITERATURE_AUDIT
  FOUND-DUHAMEL-SKELETON-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    predecessor: FOUND-HEAT-SEMIGROUP-LAW-001
    scope_note: >
      Termo de Duhamel bem definido (integral de Bochner integravel)
      para B completamente abstrato (apenas Continuous B, sem
      Lipschitz/estimativa bilinear), via continuidade CONJUNTA de
      heatOpL2 em (t,f) — fortalecimento genuino sobre
      heatOpL2_continuousAt, provado por argumento de sanduiche
      triangular usando a cota de contracao uniforme. Caso de saneamento
      B=0 reduz a evolucao linear pura. Nenhum ponto fixo, existencia ou
      unicidade de solucao branda tentados ou afirmados.
    bilinear_estimate_claim: FORBIDDEN
    existence_uniqueness_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-ABSTRACT-DUHAMEL-FIXEDPOINT-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    predecessor: FOUND-DUHAMEL-SKELETON-001
    scope_note: >
      exists_unique_mild_solution: dado B GLOBALMENTE Lipschitz
      (hipotese explicita LipschitzWith L B, nunca derivada nem
      afirmada para o B real de Navier-Stokes) e T*L < 1, existe
      solucao branda UNICA local em [0,T], via ContractingWith/teorema
      do ponto fixo de Banach aplicado ao mapa de Duhamel totalizado em
      BoundedContinuousFunction. Correcao de redacao: alvo original
      previa B Lipschitz numa bola; entregue foi B Lipschitz global
      (hipotese mais forte, nao overclaiming, caso particular do que
      seria provado com a hipotese na bola).
    concrete_B_lipschitz_claim: FORBIDDEN
    global_existence_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-DUHAMEL-FIXEDPOINT-INSTANCE-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    predecessor: FOUND-ABSTRACT-DUHAMEL-FIXEDPOINT-001
    scope_note: >
      concrete_mild_solution_instance: instancia concreta e
      nao-degenerada de exists_unique_mild_solution, em E3/F3 (R³
      concreto, mesmo par de concrete_stokesOpL2_R3), com concreteB :=
      (1/2:C)•id (nao-nulo), L=1/2 provado > 0 a partir da norma real do
      operador (nao afirmado), T=1, u0=0. Corrige a unica lacuna
      deixada por FOUND-ABSTRACT-DUHAMEL-FIXEDPOINT-001 (ausencia de
      instancia positiva).
    concrete_B_navier_stokes_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-CF-DEPLETION-KERNEL-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    track: millennium
    governance_exception: DEC-076
    scope_note: >
      Nucleo algebrico isolado D(e1,e2,e3):=(e1.e3)*det(e1,e2,e3) do
      mecanismo de Constantin-Fefferman 1993 (Indiana Univ. Math. J. 42,
      775-789; eq. 2.1-2.3 via Li 2020, arXiv:1712.00551): depleção
      exata D(e1,e2,e2)=0, cota quantitativa |D|<=||e2-e3|| (constante
      1) para vetores unitarios, instancia concreta nao-degenerada
      (D=588/15625, triplas racionais 3-4-5/7-24-25). Revisao
      adversarial com escrutinio reforcado (primeira frente ligada
      diretamente a NS-GAP-001): APPROVED_WITH_NOTES, zero problemas de
      solidez, uma frase reformulada por precaucao de leitura ("mesma
      forma qualitativa", nao "conectando diretamente").
    integral_pv_representation_claim: FORBIDDEN
    full_constantin_fefferman_theorem_claim: FORBIDDEN
    real_ns_solution_estimate_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-CZ-KERNEL-DEFINITIONS-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED_WITH_NOTES
    extension_status: NOT_AUTHORIZED
    track: millennium
    governance_exception: DEC-078
    predecessor: FOUND-CF-DEPLETION-KERNEL-001
    scope_note: >
      Camada definicional de Calderon-Zygmund em R^3: (1) integral de
      valor principal LOCAL (HasLocalPV/localPV, unicidade via
      tendsto_nhds_unique, instancia positiva nao-degenerada para a
      funcao nula); (2) CZKernelClass (mu K), parametrizada por medida
      mu arbitraria fornecida pelo chamador -- Mathlib nao tem medida de
      superficie canonica pronta em EuclideanSpace R (Fin 3);
      sphereSurfaceMeasure oferecida como instanciacao concreta
      nao-degenerada via pushforward de Measure.toSphere; (3)
      homogeneidade de grau -3 PROVADA (K_homogeneous) e suavidade
      C^infinito fora da origem PROVADA (contDiffAt_K, alem do minimo do
      escopo) para K(y):=D(y-hat,e2,e3)/||y||^3. mean_zero para esse K
      NAO tentada -- registrada como intratavel nesta janela de escopo,
      exige calculo analitico de integral de superficie sem atalho
      algebrico. Revisao adversarial com escrutinio reforcado (segunda
      frente ligada a NS-GAP-001): APPROVED_WITH_NOTES -- 0 problemas de
      solidez, 1 citacao Mathlib fabricada encontrada
      (contDiffOn_of_forall_contDiffAt, nao usada em nenhuma prova) e
      corrigida para ContDiffAt.contDiffWithinAt.
    lp_boundedness_claim: FORBIDDEN
    calderon_zygmund_theorem_claim: FORBIDDEN
    integral_pv_representation_claim: FORBIDDEN
    real_ns_solution_estimate_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-CZ-MEAN-ZERO-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    track: millennium
    governance_exception: DEC-080
    predecessor: FOUND-CZ-KERNEL-DEFINITIONS-001
    scope_note: >
      Fecha o campo mean_zero de CZKernelClass para K(y):=
      D(y-hat,e2,e3)/||y||^3, deixado em aberto pela frente anterior.
      Parte A: prova condicional integral_D_eq_zero_of_isotropicSecondMoment
      -- isotropia do tensor de segundo momento de uma medida implica
      media zero de D, via D(theta,e2,e3)=(theta.e3)(theta.w),
      w:=e2xe3, e a identidade de argumento repetido e3.(e2xe3)=0
      (tripleProduct_self_left, via dot_cross_self do Mathlib). Parte B:
      isotropia de sphereSurfaceMeasure PROVADA EM GERAL -- invariancia
      sob TODO LinearIsometryEquiv de E (via
      LinearIsometryEquiv.measurePreserving do Mathlib propagada pela
      formula de cone de toSphere), mais forte que o subgrupo finito de
      permutacao/troca-de-sinal originalmente sugerido como alternativa
      tratavel. Resultado: czKernelClass_sphereSurfaceMeasure_K, o
      primeiro termo COMPLETO de CZKernelClass no laboratorio (384->865
      linhas). Revisao adversarial com escrutinio reforcado (terceira
      frente ligada a NS-GAP-001, a mais sofisticada matematicamente):
      APPROVED, sem ressalvas -- recompilou de forma independente no
      primeiro plano, leu o conteudo matematico completo (nao so as
      assinaturas), confirmou uso genuino da hipotese de isotropia,
      confirmou flipCoord/permCoord como isometrias genuinas nao-
      degeneradas, verificou cada citacao Mathlib contra o codigo-fonte,
      auditou toda a prosa contra overclaiming (nenhum encontrado).
    l2_boundedness_claim: FORBIDDEN
    lp_boundedness_claim: FORBIDDEN
    calderon_zygmund_theorem_claim: FORBIDDEN
    integral_pv_representation_claim: FORBIDDEN
    real_ns_solution_estimate_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
  FOUND-DIRICHLET-OSCILLATORY-INTEGRAL-001:
    work_status: VERIFIED
    specification_status: APPROVED
    specification_review: N_A_SELF_SPECIFIED
    formalization_status: VERIFIED
    result_review: APPROVED
    extension_status: NOT_AUTHORIZED
    track: FOUNDATIONS
    governance_exception: DEC-082
    predecessor: null
    scope_note: >
      Prova a integral de Dirichlet classica
      integral(0,infinity) sin(x)/x dx = pi/2 (tendsto_integral_sin_div_atTop),
      item standalone de fundamentos gerais, escolhido apos a pesquisa
      de escopo que identificou esta integral como a menor unidade
      irredutivel de trabalho em qualquer rota rumo a limitacao L^2/L^p
      do nucleo Constantin-Fefferman. Rota: truque de Feynman
      reorganizado para evitar diferenciacao sob integral impropria, via
      troca de uma integral dupla genuinamente finita (retangulo
      compacto, sem Fubini improprio), convergencia dominada, limitante
      explicito O(1/N). Lema 5.2.5 completo de Grafakos NAO tentado --
      decisao de escopo deliberada, documentada honestamente no proprio
      arquivo, com o achado de que sua parte real (5.2.10)/(5.2.11) e
      independente desta integral (prova FTC autonoma; tarefa futura
      separada, tamanho comparavel) -- so a parte complexa (5.2.12)/
      (5.2.13) a consome, e mesmo assim falta um lema de limitacao
      uniforme adicional. Revisao adversarial: APPROVED, sem ressalvas
      -- recompilou de forma independente (log vazio, zero avisos),
      reconstruiu por conta propria o footprint de axiomas (18
      declaracoes, so [propext, Classical.choice, Quot.sound]),
      re-derivou a mao cada passo matematico nao-trivial, verificou cada
      citacao Mathlib contra o codigo-fonte, e re-verificou a citacao de
      Grafakos contra o OCR em cache da fonte primaria.
    l2_boundedness_claim: FORBIDDEN
    lp_boundedness_claim: FORBIDDEN
    calderon_zygmund_theorem_claim: FORBIDDEN
    integral_pv_representation_claim: FORBIDDEN
    real_ns_solution_estimate_claim: FORBIDDEN
    navier_stokes_reachable_claim: FORBIDDEN
    ns_gap_001_progress_claim: FORBIDDEN
    cz_kernel_connection_claim: FORBIDDEN
    grafakos_lemma_525_complete_claim: FORBIDDEN
    mathematical_novelty: NONE
    research_role: FORMAL_FOUNDATION
frozen_work_items:
  RH-NOGO-001:
    work_status: FROZEN_PARTIAL_RESULT
    authorization_state: NOT_AUTHORIZED
    execution_state: NO_EXECUTION
    concrete_layer_status: DEFERRED
governance_lock_renamed:
  from: NO_ACTION_AUTHORIZED
  to: PORTFOLIO_REVIEW_REQUIRED
  reason: "o sufixo _AUTHORIZED convidava a ler a trava como autorização"
  satisfied_by: PORTFOLIO_REVIEW
governance_rules:
  validate_status_must_be_read: >
    Nenhum gate pode encerrar sem que o campo status de labctl validate
    seja LIDO e reportado. Proibido pipe para head, tail ou qualquer
    truncagem sobre a saida do validador — head -2 do JSON imprime a
    chave de abertura e o schema, nunca o status. A forma canonica
    extrai o campo por parser. Seis gates consecutivos encerraram cegos
    por causa disso.
  queue_registration_required: >
    Nenhuma frente pode ser encerrada sem estar registrada na
    RESEARCH_QUEUE.yaml. Quatro frentes foram fechadas com CLOSURE_RECORD
    e STATUS.yaml sem jamais existirem na fila.
  axiom_scan_scope: >
    Uma varredura de pegada axiomática só pode ser publicada como
    integral se cobrir TODAS as declarações do artefato, incluindo
    auxiliares privados, TEST_ONLY e testes. O relatório publica
    axiom_scan_declarations_covered para que a palavra "medida" seja
    conferível sem reexecutar o probe. A primeira medição desta
    frente cobriu 20 de 28 e seria publicada como integral.
  positive_instance_required: >
    Toda frente que introduz uma hipotese deve exibir uma INSTANCIA
    POSITIVA que a satisfaca, num tipo habitado, ou declarar
    explicitamente que a hipotese e vacua. Contagem derivada, pegada
    medida e tokens varridos verificam FORMA; satisfazibilidade e
    CONTEUDO, e cinco gates passaram sem verifica-la.
  post_commit_validation: >
    Quando uma auditoria obrigatória falhar depois do primeiro commit e
    amend e commit corretivo estiverem ambos proibidos, parar com
    GATE_POST_COMMIT_VALIDATION_FAILED e aguardar gate corretivo explícito.
  truncated_output: >
    Não assumir sucesso a partir de saída truncada. Toda etapa de patch
    termina com verificação independente do efeito.
  yaml_scan_scope: >
    A varredura de chaves duplicadas cobre arquivos .yaml e .yml E o front
    matter YAML de todo documento Markdown versionado sob o laboratorio. O
    relatorio publica yaml_files_scanned e markdown_front_matter_scanned
    para que a palavra "integral" seja conferivel sem ler o codigo.
  yaml_duplicate_keys: >
    Cada chave de um mapa YAML ocorre exatamente uma vez. Duplicatas
    idênticas também são proibidas. "Último valor vence" não é semântica
    de governança, e a ausência de erro no parser não demonstra
    integridade. labctl validate rejeita qualquer duplicata em todo YAML
    versionado sob o laboratório, com o código DUPLICATE_YAML_KEY.
  aggregate_counts: >
    Contagens agregadas de declarações, gaps, arquivos, claims, testes e
    estados não são fonte primária. Toda contagem agregada deve ser
    derivada ou conferida automaticamente contra as entradas individuais
    antes do commit, e a conferência deve percorrer TODAS as entradas, não
    um subconjunto nomeado.
  mandatory_probe_exit_code: >
    Experimentos negativos, provas exploratórias destinadas a falhar e
    testes de impossibilidade não podem compartilhar arquivo com probes
    obrigatórios cujo contrato exige exit 0. Validações obrigatórias
    devem terminar com código de saída zero. Resultados negativos são
    preservados em documentação, nunca reexecutados como validação.
    Um processo Lean com exit 1 nunca é evidência de PASS.
prohibited_actions:
  - "Não usar Set.ncard_coe_Finset: o nome é ncard_coe_finset, f minúsculo"
  - "Não buscar Nontrivial (lp …) para infinito-dimensionalidade: sai de autovetores independentes"
  - "Não ler a isometria de todos os Hs entre si como degenerescência: a dependência em s vive em toDist"
  - "Não declarar Hs como abbrev: a topologia de subtipo colidiria com a da norma"
  - "Não afirmar que existe teoria de EDP no laboratório"
  - "Não citar a proibição revogada: lerayOpL2 É projeção ortogonal desde DEC-056, provado"
  - "Não citar a cota como 2n²: é exatamente 1, e atingida, desde DEC-056"
  - "Não afirmar que a pressão de Navier-Stokes foi recuperada: o projetor é peça, não solução"
  - "Não prever field_simp; ring para addSubMap: falha; usar linear_combination com certificados de ideal"
  - "Não afirmar Mordell-Weil provado: falta F, e F é escala de meses"
  - "Não apresentar o probe promovido como PR ao Mathlib: namespaces e linear_combination não estão em forma"
  - "Não enfraquecer HasTemperateGrowth achando que resolve Leray: smulLeftCLM é dite com lixo 0"
  - "Não afirmar que o projetor de Leray está construído: falta o caso matricial"
  - "Não citar MemSobolev como espaço: é Prop, não tipo normado"
  - "Não fechar contagem espectral com N(λ) ainda junk: Nat.card devolve 0 em conjunto infinito"
  - "Não abrir a enumeração ℕ → ℝ monótona: é SC-GAP-002, e não é necessária para N(λ)"
  - "Não citar TamesisLab/TOE.lean ou YangMills.lean como conteúdo: são esqueletos de 8 linhas"
  - "Não tratar toe_smoke : True como afirmação: é o caso-limite da vacuidade"
  - "Não dizer que falta toolchain a TOE-INTERFACE-001: a base categorial é 15 de 15"
  - "Não reduzir a lacuna de RH-NOGO-001 a pseudodiferencial: falta Weyl espectral inteiro"
  - "Não repetir que o primeiro passo de NS-PRESSURE-001 é bibliográfico: medido, é formal"
  - "Não tratar TM2ComputableInPolyTime como aplicável: o limite polinomial é não-teorema no Mathlib"
  - "Não citar ToPartrec como ponte para FinTM2: Fintype Λ' é FALSE, medido"
  - "Não afirmar que falta modelo de custo ao toolchain: TM2ComputableInPolyTime elabora"
  - "Não confundir existir com ser barato: instanciar o custo exige construir um FinTM2"
  - "Não tratar acúmulo de pré-requisitos como aproximação de um ataque"
  - "Não escrever linha iniciada por theorem ou def dentro de docstring: o contador a lê como declaração"
  - "Não prender lema geral a um universo sem motivo: Type* custa o mesmo"
  - "Não tratar Primrec como sinônimo de eficiente: a classe contém torres de exponenciais"
  - "Não misturar decide e if no mesmo predicado: PrimrecPred carrega instância própria"
  - "Não reimplementar o detector: detectCycle?_eq_raw é casamento, não reescrita"
  - "Não declarar o nível uniforme provado antes de lake build fechar sobre ele"
  - "Não confundir o obstáculo: é tipo dependente Fin t.next.size, não computabilidade"
  - "Não tratar o fechamento do nível uniforme como definição de classe de complexidade"
  - "Não escrever sorry, admit ou axioma em docstring Lean: a varredura de tokens acha a própria documentação"
  - "Não tratar a Primcodable induzida como canônica: Primcodable Bool já existe no Mathlib"
  - "Não afirmar invariância da classificação sob recodificação: há um caso, não um teorema"
  - "Não publicar afirmação de primazia sem derivá-la: a biblioteca já tinha 22 instâncias"
  - "Não aceitar teste cujo enunciado passe com o teorema removido do arquivo"
  - "Não apresentar a ponte de computabilidade como se ela certificasse o algoritmo"
  - "Não usar Primrec do detector como degrau para classe de complexidade: é verdade por finitude"
  - "Não tratar baseIndex + period <= n como cota de recursos: é cota do certificado"
  - "Não afirmar o nível uniforme: Primrec₂ analyzeTransitionTable elabora e NÃO está provado"
  - "Não preencher a lacuna uniforme com sorry, admit ou axioma local"
  - "Não registrar encodingPrimcodable como instance global: ela toma argumento explícito"
  - "Não publicar varredura de pegada axiomática sem cobrir todas as declarações"
  - "Não definir classe de complexidade antes da ponte de computabilidade existir"
  - "Não afirmar custo ou complexidade assintótica sem modelo de máquina declarado"
  - "Não tratar disponibilidade de riemannZeta como prontidão para RH"
  - "Não declarar teoria ausente sem tentar elaborar: Bochner era nome obsoleto, não lacuna"
  - "Não fechar frente que introduz hipótese sem exibir instância positiva em tipo habitado"
  - "Não tratar falha de instância como limite honesto sem testar satisfazibilidade"
  - "Não usar Monovariant: a definição é vácua, implica IsEmpty C"
  - "Não usar ordem geral ou WellFoundedRelation: a medida vive em Nat"
  - "Não afirmar que boa fundação basta: k - 1 falha em zero"
  - "Não afirmar que monovariante é necessário para ausência de ciclo"
  - "Não abrir terminação de programas nem ordinais"
  - "Não escrever contagem agregada sem derivá-la por script no mesmo gate"
  - "Não afirmar que um invariante separador é necessário para inalcançabilidade: é suficiente"
  - "Não usar invariante para certificar recorrência: só vale em ponto fixo"
  - "Não abrir monovariantes, boa ordem ou terminação nesta frente"
  - "Não conectar invariantes a Clay, TOE, física ou Riemann"
  - "Não atacar problema de milênio antes de a ferramenta estar encerrada"
  - "Não citar DEC-NNN como autoridade sem entrada correspondente no DECISION_LEDGER"
  - "Não reutilizar um decision_id já emitido para uma decisão diferente"
  - "Não reescrever entrada histórica do CHANGELOG para corrigir citação"
  - "Não tratar a janela limitada como hipótese mais fraca que OrbitSeparating"
  - "Não afirmar custo menor que busca concreta direta: não há modelo de custo"
  - "Não usar processo com exit diferente de zero como evidência de PASS"
  - "Não tratar igualdade abstrata como igualdade concreta sem hipótese de reflexão"
  - "Não afirmar que abstrações finitas não produzem ciclos espúrios"
  - "Não assumir bissimulação onde só há semiconjugação"
  - "Não aceitar duas definições da mesma chave YAML, ainda que os valores coincidam"
  - "Não adotar o valor efetivo do parser como fonte de verdade ao resolver divergência"
  - "Não afirmar invariância do witness concreto sob recodificação"
  - "Não estender ENG-FINITE-STATE-ENCODING-001 nem abrir 002 sem gate próprio"
  - "Não conferir contagem agregada por amostragem: a varredura deve cobrir todas as entradas"
  - "Não expor buildTransitionTable_getElem: é private e vive em Commutation.lean"
  - "Não provar table_step_commutes diretamente: é o .symm de tableIndex_semiconj"
  - "Não criar segundo tableIndex sobre Fin n: esse papel já é de encode"
  - "Não estender ENG-FINITE-STATE-ENCODING-001 nem abrir 002 sem gate próprio"
  - "Não misturar experimento negativo com probe obrigatório no mesmo arquivo"
  - "Não desviar das assinaturas congeladas nos documentos FINAL_* sem gate próprio"
  - "Não afirmar invariância do witness concreto sob recodificação: ENC-GAP-020"
  - "Não tornar buildTransitionTable_getElem público: é INTERNAL_HELPER"
  - "Não provar table_step_commutes diretamente: ele é o .symm da semiconjugação"
  - "Não abrir frente para remover propext, Classical.choice ou Quot.sound infraestruturais"
  - "Não derivar a codificação de Fintype: equivFin é noncomputable e truncEquivFin não produz dado"
  - "Não criar um terceiro ponto de transporte Fin n ↔ Fin table.next.size"
  - "Não usar encode_decode onde decode_encode é a lei semanticamente necessária"
  - "Não reprovar a comutação de iteradas por indução manual: Semiconj.iterate_right resolve"
  - "Não enunciar a soundness sobre a tabela: ela deve terminar em igualdade sobre S"
  - "Não alterar retroativamente RT-GAP-017 nem tocar a frente do runtime adapter"
  - "Não derivar encode de Fintype.equivFin: é noncomputable e não pode produzir dado"
  - "Não modificar ENG-FINITE-STATE-RUNTIME-001 ao construir a codificação certificada"
  - "Não declarar RT-GAP-017 fechado no caso geral: a frente cobre apenas o recorte tipado"
  - "Não iniciar a formalização de ENG-FINITE-STATE-ENCODING-001 sem gate próprio"
  - "Não desviar das assinaturas congeladas em FINAL_SIGNATURES.md sem gate próprio"
  - "Não criar CLI, parser, JSON, CSV, rede ou integração externa sem gate próprio"
  - "Não derivar contagens agregadas à mão: verificar cabeçalho contra as entradas por script"
  - "Não remover o ramo internalDetectorFailure — sua impossibilidade é teorema, não motivo de remoção"
  - "Não estender ENG-FINITE-STATE-RUNTIME-001 nem abrir 002 sem gate próprio"
  - "Não alterar a semântica de zero passos de run? — run? 0 state = some state"
  - "Não alterar a precedência dos erros: tabela, depois consulta, depois execução"
  - "Não renomear 03_ENGINEERING — a duplicação de prefixo é cosmética e reconhecida"
  - "Não desviar das assinaturas congeladas em SPECIFICATION_DECISION.md sem gate próprio"
  - "Não criar RawTransitionTable.stateCount — duplicaria next.size"
  - "Não trocar ValidatedTransitionTable por Subtype nem manter ambos"
  - "Não colapsar erro de tabela e erro de estado inicial num único construtor"
  - "Não remover o ramo internalDetectorFailure da função executável"
  - "Não corrigir destinos inválidos por módulo, clamp ou fallback silencioso"
  - "Não converter estado inicial inválido por módulo"
  - "Não permitir que a tabela validada aponte para fora do domínio"
  - "Não usar Classical.choose para produzir dados"
  - "Não depender de Function.periodicOrbit na execução"
  - "Não reimplementar o detector nem a casa dos pombos"
  - "Não misturar parsing JSON, CSV, arquivo ou rede com o núcleo formal"
  - "Não incluir servidor, banco de dados ou interface web na primeira versão"
  - "Não tornar Floyd, Brent ou a totalização dependências obrigatórias"
  - "Não declarar automaticamente correta a abstração de um sistema real em estados finitos"
  - "Não afirmar complexidade sem modelo de custo"
  - "Não formalizar Floyd, Brent ou tabela visitada — todos NOT_AUTHORIZED"
  - "Não estender FOUND-CYCLE-DETECTION-001 nem abrir FOUND-CYCLE-DETECTION-002 sem gate próprio"
  - "Não estender FOUND-FUNCTIONAL-GRAPH-001 nem FOUND-SEMIGROUP-002 sem gate próprio"
  - "Não reabrir RH-NOGO-001 sem que uma condição de RH_NOGO_REACTIVATION_CRITERIA.md ocorra e seja verificada"
  - "Não registrar testes que importam TamesisLab dentro de TamesisLab.lean — import circular"
  - "Não conectar a nova frente a TRI, TDTR, teoria de tudo, física, Hipótese de Riemann ou conjectura Clay"
  - "Não afirmar novo modelo de computação, novo algoritmo, nova teoria de autômatos ou descoberta"
  - "Não tratar reutilização em software como descoberta científica"
  - "Não modificar legado nem operar a partir de /mnt/d"
  - "Não afirmar que bissimulação reflete ciclos: BOOL_TO_UNIT já é uma bissimulação sobrejetiva"
  - "Não definir Reflects já resolvido: a existencial do zag é o conteúdo do colapso"
  - "Não escrever \"bissimulação é semiconjugação\" sem o qualificador determinístico total e funcional"
  - "Não afirmar que bissimulação é inútil: o resultado vale só neste recorte"
  - "Não estender o colapso zig/zag para sistemas não determinísticos ou bissimulação relacional"
  - "Não estender FOUND-FINITE-STATE-ABSTRACTION-001 nem abrir 002 sem gate próprio"
  - "Não declarar uma varredura integral sem publicar quantos arquivos ela abriu"
  - "Não fechar front matter com o delimitador --- na mesma linha do corpo"
  - "Não usar yaml.safe_load em front matter sem antes rejeitar chaves duplicadas"
  - "Não usar código de saída capturado através de fronteira de shell como evidência"
  - "Não declarar PASS quando a saída contiver linha error: ainda que o exit seja zero"
  - "Não registrar FoundFiniteStateAbstraction001UmbrellaAudit em TamesisLab.lean"
  - "Não usar lake env lean isolado antes do build: sem .olean das dependências dá exit 1 falso"
  - "Não usar FOUND-FINITE-ABSTRACTION-001 como item ativo: é nome candidato anterior"
  - "Não concluir igualdade em C a partir da soundness observacional sem OrbitSeparating"
  - "Não descrever a completeness abstrata como completeness concreta"
  - "Não esconder OrbitSeparating dentro de CertifiedFiniteAbstraction"
  - "Não armazenar encoding, witness, tabela ou estado inicial na estrutura da abstração"
  - "Não afirmar que lerayOpHs é auto-adjunto ou projeção ortogonal em H^s: Hs E F s não tem produto interno, isso é LP-GAP-005"
  - "Não citar RH_NOGO_REACTIVATION_CRITERIA.md como regra que rege FOUND-LERAY-PROJECTOR-SOBOLEV-001: está escopado a RH-NOGO-001, é analogia, não autoridade"
  - "Não confiar no código de saída de um pipe truncado por head/tail: conferir o exit code do processo lean separadamente"
resume_read_order:
  - "LAB_STATE.md"
  - "AGENTS.md"
  - "01_PORTFOLIO/PORTFOLIO_REVIEW_LERAY_SOBOLEV_2026_08_09.md"
  - "02_FOUNDATIONS/16_LERAY_PROJECTOR/FOUND_LERAY_PROJECTOR_SOBOLEV_001/STATUS.yaml"
  - "01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md"
  - "03_MILLENNIUM/02_NAVIER_STOKES/STATUS.yaml"
  - "03_MILLENNIUM/03_P_VS_NP/STATUS.yaml"
  - "03_MILLENNIUM/04_YANG_MILLS/STATUS.yaml"
  - "03_MILLENNIUM/05_HODGE/STATUS.yaml"
  - "03_MILLENNIUM/06_BSD/STATUS.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "último relatório em 09_SESSIONS/"
---

# Estado atual

```text
LAB-ARCH-001                        VERIFIED                ENCERRADO
LAB-BENCH-001                       VERIFIED                ENCERRADO
FOUND-SEMIGROUP-001                 VERIFIED                ENCERRADO
FOUND-SEMIGROUP-002                 VERIFIED / APPROVED     ENCERRADO
FOUND-FUNCTIONAL-GRAPH-001          VERIFIED / APPROVED     ENCERRADO
FOUND-CYCLE-DETECTION-001           VERIFIED / APPROVED     ENCERRADO
ENG-FINITE-STATE-RUNTIME-001        VERIFIED / APPROVED     ENCERRADO
ENG-FINITE-STATE-ENCODING-001       VERIFIED / APPROVED     ENCERRADO
FOUND-FINITE-STATE-ABSTRACTION-001  VERIFIED / APPROVED     ENCERRADO
FOUND-BISIMULATION-BOUNDARY-001     VERIFIED / APPROVED     ENCERRADO
FOUND-INVARIANT-UNREACHABILITY-001  VERIFIED / APPROVED     ENCERRADO
FOUND-MONOVARIANT-DESCENT-001       VERIFIED / APPROVED     ENCERRADO

FOUND-COMPUTABILITY-BRIDGE-001      VERIFIED / APPROVED     ENCERRADO

FOUND-UNIFORM-PRIMREC-001           VERIFIED / APPROVED     ENCERRADO

ENG-RUNTIME-SOUNDNESS-002           VERIFIED / APPROVED     ENCERRADO

FOUND-SPECTRAL-COUNTING-001         VERIFIED / APPROVED     ENCERRADO
FOUND-FOURIER-MULTIPLIER-L2-001     VERIFIED / APPROVED     ENCERRADO
FOUND-ELLIPTIC-HEIGHT-001           VERIFIED / APPROVED     ENCERRADO
FOUND-LERAY-PROJECTOR-001           VERIFIED / APPROVED     ENCERRADO
FOUND-SOBOLEV-SPACE-001             VERIFIED / APPROVED     ENCERRADO

RH-NOGO-001                         FROZEN_PARTIAL_RESULT   congelado

NS-PRESSURE-001                     VERIFIED / APPROVED_WITH_NOTES  ENCERRADO
PVSNP-PHYS-001                      VERIFIED / APPROVED_WITH_NOTES  ENCERRADO
YM-LIMIT-001                        VERIFIED / APPROVED_WITH_NOTES  ENCERRADO
HODGE-CDK-001                       VERIFIED / APPROVED_WITH_NOTES  ENCERRADO
BSD-HYP-MATRIX-001                  VERIFIED / APPROVED_WITH_NOTES  ENCERRADO
TOE-INTERFACE-001                   SCOPED                  bloqueado: dep RH-NOGO-001 nao satisfeita (as outras duas ja sao VERIFIED)

LAB-GOV-DECISION-LEDGER-001         VERIFIED                ENCERRADO
LAB-CORR-VALIDATION-BLINDNESS-001   VERIFIED                ENCERRADO

FOUND-LERAY-PROJECTOR-SOBOLEV-001            VERIFIED / APPROVED_WITH_NOTES  ENCERRADO
FOUND-LERAY-PROJECTOR-SOBOLEV-ORTHOGONAL-001 VERIFIED / APPROVED             ENCERRADO

authorized_action: PORTFOLIO_REVIEW_REQUIRED   (trava, nao execucao)
```

**Fila esgotada em 2026-08-09** para as 28 frentes antigas (ver
`01_PORTFOLIO/PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09.md`) — mas duas
frentes novas surgiram depois, em cadeia justificada: `LP-GAP-004`
(versão H^s do projetor de Leray) estava bloqueada por `FM-GAP-001`, e
`FM-GAP-001` tinha acabado de fechar nesta mesma sessão via
`FOUND-SOBOLEV-SPACE-001`. Não é invenção de trabalho — é o
reconhecimento de que um bloqueador especificamente nomeado deixou de
existir (ver `01_PORTFOLIO/PORTFOLIO_REVIEW_LERAY_SOBOLEV_2026_08_09.md`).
`FOUND-LERAY-PROJECTOR-SOBOLEV-001` fechou `VERIFIED` com revisão
adversarial `APPROVED_WITH_NOTES`, abrindo `LP-GAP-005`
(auto-adjunção/projeção ortogonal em H^s) de propósito. A frente seguinte,
`FOUND-LERAY-PROJECTOR-SOBOLEV-ORTHOGONAL-001`, fechou esse gap via um
pareamento pullback explícito (não a API `IsSelfAdjoint` do Mathlib, por
risco de diamante de tipo) — revisão adversarial `APPROVED`, sem
ressalvas. **Nenhum gap conhecido do projetor de Leray permanece aberto.**
`RH-NOGO-001` e `TOE-INTERFACE-001` continuam sem condição de reativação
satisfeita — isto não muda a conclusão de esgotamento sobre eles.

**Onda concluída, integrada e revisada: cinco frentes em paralelo no
track `millennium`** — `NS-PRESSURE-001`, `PVSNP-PHYS-001`,
`YM-LIMIT-001`, `HODGE-CDK-001`, `BSD-HYP-MATRIX-001`. Vinte e quatro
frentes encerradas antes desta onda. Autorizada por
`PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09`, que também corrigiu
`closed_work_items` faltando seis entradas (a mesma classe de defeito
prosa/YAML que `LAB-CORR-VALIDATION-BLINDNESS-001` já havia corrigido
uma vez). `TOE-INTERFACE-001` fica fora desta onda: duas de suas três
dependências não estão satisfeitas.

**Integração (sessão orquestradora, mesmo ciclo):** os cinco rascunhos
Lean escritos em paralelo corretamente NÃO rodaram `lake build` (regra
da onda, para não corromper o cache compartilhado). Na integração serial,
dois deles falharam ao compilar de primeira — `NS-PRESSURE-001` (faltava
`import Mathlib.Tactic.Linarith`; `ring` falhou em `Matrix n n ℝ`, que
não é comutativa, corrigido para `noncomm_ring`) e `PVSNP-PHYS-001`
(`omega` não reduzia uma aplicação de lambda sob um `def` não
desdobrado). `YM-LIMIT-001` teve três correções menores (mesma classe de
problema de redução de lambda, mais uma `def` que precisava de
`noncomputable`). `HODGE-CDK-001` e `BSD-HYP-MATRIX-001` tiveram um erro
cada (`BSD`: doc-comment `/-- -/` antes de `section`, que não é uma
declaração; `Decidable` não sintetizado através de um `def` não
desdobrado). Os cinco compilam agora com `exit 0`; nenhum está registrado
em `TamesisLab.lean`. Adicionalmente, todos os cinco continham a palavra
literal `sorry`/`admit` dentro de docstrings alegando sua ausência — o
mesmo padrão que `LAB-CORR-VALIDATION-BLINDNESS-001` já havia proibido
duas vezes antes; corrigido proativamente nesta integração, antes de
qualquer gate acusar.

**Revisão adversarial (mesmo ciclo):** cinco agentes independentes,
cada um revendo uma frente diferente da que formalizou, com instrução
explícita de tentar refutar antes de aprovar. Veredito: `APPROVED_WITH_NOTES`
nas cinco — nenhum stop_condition violado, nenhuma citação fabricada,
nenhuma linguagem inflada, nenhum conteúdo Lean mais fraco que o
alegado. Achados corrigidos nesta integração: intervalo de página de
Cantwell 1992 (782–792 → 782–793); `LEAN_MAP.md` desatualizado em
quatro frentes (ainda dizia `NOT_FORMALIZED` apesar do rascunho Lean já
compilado); uma citação do PDF do Clay/Deligne que fundia duas cláusulas
distintas numa só (corrigida com o texto exato, re-extraído do PDF
primário — a correção na verdade reforça a tese central de
`HODGE-CDK-001`, já que a cláusula perdida cita CDK 1995 como a fonte da
parte "conhecida"); cinco entradas pré-existentes em `CLAIM_LEDGER.yaml`
(datadas de 2026-07-28, antes desta sessão) que ainda diziam `SCOPED`.
**Achado que não foi apenas corrigido, mas registrado como observação
externa** (`YM-GAP-007`, ver `GAP_REGISTER.yaml` de `YM-LIMIT-001`): duas
preprints de 2025/2026 alegam prova construtiva completa de existência e
mass gap de Yang-Mills 4D — uma (arXiv:2506.00284, SU(3)) foi **retirada
pelo arXiv admin**; a outra (arXiv:2606.19362, SU(N) geral) permanece
publicada, sem revisão por pares confirmada. Este laboratório não
verifica, endossa nem refuta nenhuma das duas — registrado só para
rastreabilidade.

## Por que este bloco existe

Ele esteve **desatualizado por seis gates**, descrevendo
`FOUND-FUNCTIONAL-GRAPH-001` como estado corrente enquanto o front matter
já registrava dez frentes encerradas. O YAML é a fonte de verdade e
sempre esteve correto; a prosa não. Como `resume_read_order` manda ler
este arquivo primeiro, a prosa obsoleta enganava exatamente na retomada.

E **aconteceu de novo**: entre a correção acima e este gate, a prosa
voltou a dizer "Nenhuma frente ativa" enquanto três frentes eram abertas
e duas encerradas. A reincidência está registrada aqui em vez de apagada.

## O que a cadeia de dez frentes estabeleceu

```text
semiconjugacao             NAO reflete recorrencia
bissimulacao funcional     NAO reflete   (e a mesma coisa, no caso total)
bissimulacao sobrejetiva   NAO reflete
OrbitSeparating            REFLETE
injetividade global        REFLETE  (forte demais)
```

Abstração entrega **observação**, não reflexão. Reforçar a relação de
simulação não atravessa essa fronteira; o que atravessa é **separação de
estados**.

## Limite computacional que permanece

`periodicOrbit` é **noncomputável**. `OrbitSeparating` é obrigação do
consumidor, por órbita, e **não** foi tornada decidível — a tentativa foi
formalizada em probe, compilou, e foi rejeitada por não comprar nada que
a equação única já não comprasse.

## O que a ponte de computabilidade estabeleceu

```text
CertifiedFiniteEncoding induz Primcodable        SIM, direto (nao canonica)
analyzeEncodedSystem e Computable e Primrec      SIM, POR FINITUDE
a busca limitada importa para essa conclusao     NAO
baseIndex + period <= n e cota de recursos       NAO, e do CERTIFICADO
custo formalizavel sem modelo de maquina         NAO neste nivel
```

`Primrec.dom_finite` prova que **toda** função que sai de um tipo finito
codificável é primitiva recursiva, sem consultar a função. A
classificação é **constante** sobre o domínio do laboratório: ela não
distingue o detector de uma tabela de consulta.

A pergunta só readquire conteúdo no nível **uniforme**, sobre
`RawTransitionTable × Nat`, onde o domínio é infinito. O enunciado
`UniformPrimrecStatement` elabora; a prova **não é tentada** —
`CB-GAP-001`.

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_BRIDGE
```

## Próxima ação

As cinco frentes da onda paralela (`NS-PRESSURE-001`, `PVSNP-PHYS-001`,
`YM-LIMIT-001`, `HODGE-CDK-001`, `BSD-HYP-MATRIX-001`) reportaram e foram
integradas nesta sessão. Nenhuma está `VERIFIED`: todas `PARTIAL_RESULT`
com `result_review: PENDING`. Próxima ação: revisão adversarial
independente de cada resultado, uma por vez — ver
`PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md` para as condições de
paralelismo que continuam valendo. O texto abaixo é histórico, da frente
`FOUND-COMPUTABILITY-BRIDGE-001`, preservado por política do laboratório
de não reescrever entradas antigas.

```text
ponte      Primrec nao mede nada    porque e VACUO sobre dominio finito
uniforme   Primrec nao mede custo   porque a CLASSE e enorme
```

São **dois limites diferentes**, e os dois valem.

O modelo de custo **existe no toolchain** — `TM2ComputableInPolyTime`
elabora. O que custa é instanciá-lo: exige construir um `FinTM2` para
`analyzeTransitionTable`, e o único exemplo trabalhado do Mathlib é a
identidade. E mesmo instanciado, o produto seria uma **definição de
classe**, não um ataque.
