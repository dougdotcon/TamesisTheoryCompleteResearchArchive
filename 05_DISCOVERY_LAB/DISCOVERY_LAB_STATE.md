# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-22 (`DISC-DEC-031`: casos `K=3,4,5` do Lema Aberto de U₁/₂ agora PROVADOS incondicionalmente — técnica genuinamente diferente da onda 5 (matriz de transferência/cadeia de Markov uniforme em `K`, em vez de análise de casos manual): `ψ_n^{(3)}=16/35+12/(35n)+5/(28n²)+3/(70n³)`, taxa completa `φ_n^{(3)}=16/35+1/(14n)+11/(10n²)+23/(35n³)+6/(35n⁴)`, ambas provadas do zero; `K=4,5` provados como bônus pelo mesmo procedimento mecânico. Verificado por referee adversarial hostil separado (re-derivação completa por técnica diferente, força bruta própria, reexecução dos scripts originais) — veredito SOUND, zero erros. Padrão de taxa geral-`K` catalogado honestamente como CONJECTURA (verificado `K=1..5`, não provado). `K≥6` permanece aberto, obstrução precisa nomeada. Anterior: `DISC-DEC-030`: primeiro resultado real de `DISC-COGNITIVE-EEG-SPECTRAL-001` — braço depressão fechado `CLOSED_REFUTED`. `H_Tamesis` (entropia espectral MENOR em MDD) refutada na direção OPOSTA (`Ī(X)_MDD=0,7613>Ī(X)_HC=0,6558`, `t=5,268`, `p=3,97×10⁻⁶`, `d=1,447`), confirmado por reprodução adversarial independente do zero (todos os números de decisão batem a <10⁻⁹, mesmas 2 exclusões, mesmos 6 arquivos indisponíveis, mesmos 2 pares duplicados descobertos independentemente) — `DISC-CLAIM-007`. Braço ansiedade permanece bloqueado por acesso. Anterior: `DISC-DEC-026`: onda paralela de `DISC-DEC-023` integrada — (a) `SPARC-FMULTI-STAGE1`: pipeline de auto-calibração completa de `f_multi` de Chae (2023) implementado e validado 100% sobre dado sintético [7/7 critérios pré-declarados, 5 cenários], verificado adversarialmente por 2 agentes independentes [1 problema de disciplina documental + 1 lacuna de robustez em `fit_a0` encontrados e corrigidos, nenhum número já reportado alterado] — pronto para Estágio 2 [dado real de descoberta, ainda NÃO o holdout selado], que exige pré-registro e autorização próprios; (b) `DISC-COGNITIVE-EEG-SPECTRAL-001`: etapa de operacionalização concluída [`I(X)`=entropia espectral de Shannon normalizada, modelos concorrentes nomeados, regra de decisão a priori, poder estatístico calculado, acesso real VERIFICADO por download para Mumtaz/depressão, NÃO verificado para DASPS/ansiedade por bloqueio de login IEEE] — braço depressão pronto para um futuro `PREREGISTRATION.md`, 2 lacunas nomeadas pendentes de decisão. Anterior: `DISC-DEC-024`/`DISC-DEC-025`: onda 5 integrada — caso `K=2` do Lema Aberto de U₁/₂ agora PROVADO incondicionalmente [`φ_n^{(2)}=8/15+1/(30n)+7/(10n²)+1/(5n³)`, verificado por referee adversarial em 4 camadas, 0 erros, Lema Aberto restante estritamente `K≥3`]; mecanismo `M-WEIB(β)` de expoente intermediário `α∈(1/2,1)` encontrado e confirmado, com correção de enquadramento via adendo datado [membro da família `M-q` para `β<1`, não escape dela]; pacote `tamesis-cycle-survival/` atualizado e recompilado com o novo resultado. Levantamento arquivo-inteiro de candidatos (Fase 0, 19 candidatos/7 áreas, não restrito a TRI-RG) fechado `CLOSED_NULL` [18/19 rejeitados com razão concreta]; único lead imaturo [EEG cognitivo, depressão vs. ansiedade] promovido a nova linha candidata `DISC-COGNITIVE-EEG-SPECTRAL-001`, `CANDIDATE_FORMULATING`, autorizada apenas etapa de operacionalização. Anterior: `DISC-DEC-021` — `DISC-RH-NUMBER-VARIANCE-001` [item 12] fechado `CLOSED_INCONCLUSIVE`/`NEITHER_MODEL` — reprodução adversarial encontrou um TERCEIRO bug real no estimador primário [corrigido via adendo datado, texto original preservado], mudando o subcaso de `PARTIAL_DISAGREEMENT` para `NEITHER_MODEL`; componente de exclusão de GUE CONFIRMADO como achado real, mais forte do que reportado originalmente [z_A de -203 e -161, não -203 e -4]. Todos os 12 itens do levantamento original de `DISC-RH-REAL-001` agora têm disposição final)
**Arquitetura:** motor 1 de 3 — ver `00_GOVERNANCE/RESEARCH_PIPELINE.md`
(`05_DISCOVERY_LAB` → `03_REPLICATION_GATE` → `04_FORMAL_RESEARCH_LAB`,
adotada em `DISC-DEC-003`). `04_FORMAL_RESEARCH_LAB` não é mais um
laboratório paralelo desacoplado — é o destino de formalização para claims
que sobrevivem ao Gate de Replicação (ver `DEC-107` de lá, que reclassifica
as Ondas 1-7 como arquivo de calibração de capacidade formal, não pesquisa
sobre nenhum Problema do Millennium).

## Status atual

| Campo | Valor |
|---|---|
| Teste ativo | Nenhum. `DISC-COSMOLOGY-MOND-SPARC-004` encerrado (`CLOSED_INCONCLUSIVE`, 2026-08-18, ver seção própria abaixo — redesenho de SPARC-003 com desprojeção Monte Carlo completa; confundidor de multiplicidade oculta plausivelmente suficiente para explicar todo o sinal residual). `DISC-COSMOLOGY-MOND-SPARC-003` encerrado (`CLOSED_INCONCLUSIVE` — estatística pré-registrada estruturalmente incapaz de produzir veredito válido, não erro nem falta de dado). `DISC-RH-ZERO-GAP-RUNS-001` encerrado (`REPLICATION_PASSED`). `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` encerrado (`REPLICATION_FAILED` — inconclusivo por falta de poder no dataset reservado, achado primário NÃO contradito). `DISC-COSMOLOGY-MOND-SPARC-002` encerrado (`REPLICATION_FAILED`). `DISC-COSMOLOGY-MOND-SPARC-001` encerrado (`CLOSED_INCONCLUSIVE`). `DISC-TRI-RG-001` retomada em 2026-08-18 a pedido do usuário, completou os 11/11 candidatos identificados (Fase 0.6 incluída), foi PAUSADA (`DISC-DEC-008`, 2026-08-20), reaberta na prática no mesmo dia por nova busca (Fase 0.7), completou os 3/3 candidatos novos (`complexidade-de-lempel-ziv` NEGATIVO após reexecução adversarial; `largest_lyapunov_exponent` fechado na validação; `dmd_koopman` NEGATIVO — 1 domínio `NOT_COMPUTABLE`, achado do outro refutado por 4 checagens adversariais), foi PAUSADA novamente (`DISC-DEC-009`, 2026-08-20), reaberta na prática no mesmo dia por nova busca (Fase 0.8), completou os 2/2 candidatos novos (`transfer_entropy` NEGATIVO após reprodução adversarial descobrir um artefato instrumental de baixa frequência; `epsilon-machine-complexity` fechado na etapa de validação), foi ENCERRADA FORMALMENTE (`DISC-DEC-010`, 2026-08-21, `status: CLOSED_NULL`) — os 16 candidatos identificados em 5 rodadas de busca têm resultado completo, nenhum produziu invariante cross-domain sobrevivente — foi REABERTA (`DISC-DEC-011`, mesmo dia) com escopo estritamente delimitado (revisitar `epsilon-machine-complexity` com CSSR incremental completo), e ENCERRADA NOVAMENTE (`DISC-DEC-012`, mesmo dia) após a revisão concluir: a implementação corrigida foi verificada como correta (recupera exatamente um processo de ordem finita com solução teórica exata) e AINDA ASSIM não mostrou poder discriminativo para `C_mu` — a ambiguidade original está resolvida a favor de fragilidade genuína do estimador, não limitação de implementação. Dado real (Old Faithful, La Palma 2021) nunca tocado. Ver `02_TESTS/TRI_RG/CLOSURE_SUMMARY.md` (síntese original) e `02_TESTS/TRI_RG/epsilon_machine_complexity/RESULTS_SUMMARY_V2.md` (revisão) |
| Fase | RH-REAL: dois sub-testes concluídos, ambos com Gate de Replicação completo acionado. (1) `DISC-RH-ZERO-GAP-RUNS-001`: `INVERSE_SIGNAL` `REPLICATION_PASSED` — gaps grandes consecutivos são menos comuns que sob reordenação aleatória, confirmado em 3 regimes de altura (~75.000, ~10¹², ~10²¹). (2) `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`: gap mínimo escala como `N^(-1/3)` (GUE), exclui `N^(-1)` (Poisson) e `N^(-1/2)` (GOE) — `β̂=-0,3395` vs. previsão `-0,3333`, `evidence_level: preregistered_confirmed` sobre o dataset primário; Gate no terceiro dataset reservado (`zeros5.txt`, #10²²) resultou `REPLICATION_FAILED` por amostra pequena demais para a grade travada (0 blocos possíveis em N=10.000) — inconclusivo, não contraditório. TRI-RG: os 3 candidatos viáveis da Fase 0 agora testados com rigor completo, os 3 NEGATIVO para invariante cross-domain — `critical-slowing-down` (GISP2/SDDB/NASDAQ), `wavelet-multiresolution-scaling` (Tohoku/CHB-MIT), `dfa-multiscale-entropy` (Apneia-ECG/GISP2, achado forte de 1 domínio explicado por mecanismo fisiológico já conhecido — CVHR — e não replicado no segundo domínio); mais 3 candidatos novos fechados NEGATIVO (`soc-avalanches`, `mse-multiscale-entropy`, `grafo-de-visibilidade` — este último com achado adicional decisivo: `d_B`, o canal originalmente primário, é estruturalmente não computável para séries estocásticas, small-world por construção; `C`, promovido a canal único ANTES de dado real, validado com poder real mas sem sinal em nenhum dos 2 domínios); e o 7º e último candidato, `RQA`, fechado na própria etapa de validação (identificabilidade nunca estabelecida, mesmo após uma correção de desenho pré-autorizada — dado real nunca tocado). Linha `DISC-TRI-RG-001` agora completa, 7/7 candidatos com resultado final. SPARC-003: pré-registro travado como réplica independente do veredito de SPARC-002 via binárias largas Gaia reais (43.147 sistemas pós-corte); modelo MOND pré-registrado tem imagem `(1,+∞)` mas as 5 medianas empíricas reais são todas `<1` — ajuste estruturalmente impossível (diluição por projeção). `CLOSED_INCONCLUSIVE`. SPARC-004: redesenho de SPARC-003 com desprojeção 3D via Monte Carlo (método primário de Chae 2023, estatística `δ_obs-newt`); `a0_fit=1,657×10⁻¹⁰` (IC95% `[1,232×10⁻¹⁰;2,181×10⁻¹⁰]`) após correção de um bug de assimetria de ruído astrométrico encontrado pela descoberta adversarial de nulos; veredito bruto `BOTH_FALSIFIED`, mas a checagem adversarial de multiplicidade oculta (gatilho pré-declarado) mostrou que companheiras não resolvidas, em magnitude plausível pela literatura, são sozinhas suficientes para explicar todo o sinal — `CLOSED_INCONCLUSIVE`, nenhum veredito H_A/H_B aceito |
| Próxima ação obrigatória | Nenhuma obrigatória. `DISC-CORE-NUMERICS-001` está com a consolidação matemática de U₁/₂ ainda mais avançada (onda 5): Teorema 1 provado e verificado por referee adversarial sem erros; ponte `n→∞` provada de forma exata para `K=0,1,2` (fórmula completa `φ_n^{(2)}=8/15+1/(30n)+7/(10n²)+1/(5n³)`), reduzida a um Lema Aberto estritamente mais estreito para `K≥3`, honestamente documentado; generalização U_α derivada e confirmada (`α∈[1/2,1]` para toda a classe), mecanismo `M-WEIB(β)` de expoente intermediário confirmado; pacote `tamesis-cycle-survival/` (recompilado com o resultado K=2) e `FAILED_HYPOTHESES.md` publicados. Reaberturas futuras legítimas: nova técnica para o Lema Aberto K≥3; fechar a lacuna de rigor do sombreamento M-CLUST(b grande); só depois disso considerar testar U_α em sistemas empíricos reais (explicitamente adiado pelo usuário). `SPARC-FMULTI-STAGE1` concluído e verificado adversarialmente (auto-calibração de `f_multi`, validação sintética apenas, pronto para Estágio 2, holdout selado intocado, Estágio 2 exige pré-registro/autorização próprios). `DISC-COGNITIVE-EEG-SPECTRAL-001` (`CANDIDATE_FORMULATING`) tem etapa de operacionalização concluída — braço depressão (Mumtaz) pronto para um futuro `PREREGISTRATION.md`; braço ansiedade (DASPS) bloqueado por acesso (exige signup IEEE humano); nenhum dado real ainda computado. `DISC-TRI-RG-001` permanece `CLOSED_NULL` (`DISC-DEC-012`). A revisão delimitada de `epsilon-machine-complexity` (CSSR incremental completo) concluiu com veredito mais decisivo que o original — fragilidade genuína do estimador `C_mu` confirmada, não limitação de implementação (verificado via um diagnóstico de ordem finita recuperado exatamente, e via uma prova analítica original sobre a estrutura período-2 do Processo Even). 16/16 candidatos permanecem com resultado final. Uma reabertura futura exigiria nova justificativa explícita; uma revisita legítima a `epsilon-machine-complexity` exigiria uma medida de complexidade fundamentalmente diferente de `C_mu` (nova candidatura), não mais uma correção de implementação. Ver `02_TESTS/TRI_RG/epsilon_machine_complexity/RESULTS_SUMMARY_V2.md` |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto), `DISC-DEC-003` (arquitetura de três motores + seis extensões), `DISC-DEC-004` (pivô de SPARC-002 + pré-registro do teste de derivação de a₀), `DISC-DEC-005` (1ª pausa de `DISC-TRI-RG-001`, revertida em 2026-08-14), `DISC-DEC-006` (2ª pausa, revertida em 2026-08-15), `DISC-DEC-007` (3ª pausa, revertida em 2026-08-18), `DISC-DEC-008` (4ª pausa, revertida no mesmo dia por nova busca — Fase 0.7), `DISC-DEC-009` (5ª pausa, revertida no mesmo dia por nova busca — Fase 0.8), `DISC-DEC-010` (ENCERRAMENTO FORMAL de `DISC-TRI-RG-001`, 2026-08-21, `status: CANDIDATE_FORMULATING -> CLOSED_NULL`, após os 16/16 candidatos resultarem sem invariante cross-domain sobrevivente), `DISC-DEC-011` (REABERTURA delimitada, mesmo dia, `status: CLOSED_NULL -> CANDIDATE_FORMULATING`, escopo restrito a revisitar `epsilon-machine-complexity` com CSSR incremental completo), `DISC-DEC-012` (ENCERRAMENTO FORMAL novamente, mesmo dia, `status: CANDIDATE_FORMULATING -> CLOSED_NULL`, após a revisão delimitada confirmar de forma mais decisiva a ausência de invariante), `DISC-DEC-013` (criação de `DISC-CORE-NUMERICS-001`, 4 frentes de adjudicação numérica interna + triagem RH itens 5/6/10, 5 agentes paralelos, 2026-08-21), `DISC-DEC-014` (integração da onda 1 + autorização da onda 2: caracterização da função-limite U₁/₂ + pré-registro FHK item 10; diretriz permanente de README atualizado a cada onda, 2026-08-21), `DISC-DEC-015` (autorização da onda 3: prioridade de literatura, teorema rigoroso, generalização U_α, pacote standalone, 2026-08-22), `DISC-DEC-016` (fechamento de `DISC-RH-FHK-SHORT-INTERVAL-MAX-001`, `CLOSED_INCONCLUSIVE`, confirmado adversarialmente, 2026-08-22), `DISC-DEC-017` (integração completa da onda 3: teorema + referee + generalização U_α + adversarial + pacote standalone, 2026-08-22), `DISC-DEC-018` (autorização da onda 4: itens RH-REAL não-tentados + rigor M-CLUST, 2026-08-22), `DISC-DEC-019` (integração da revisão RH-REAL + autorização do pré-registro do item 12, 2026-08-22), `DISC-DEC-020` (integração da correção de rigor M-CLUST, PARCIALMENTE CORRIGIDO, 2026-08-22), `DISC-DEC-021` (fechamento de `DISC-RH-NUMBER-VARIANCE-001` com correção pós-adversarial de um bug real, `NEITHER_MODEL`, 2026-08-22), `DISC-DEC-022` (autorização da onda 5: tentativa delimitada do Lema Aberto K≥2 + busca de mecanismo de α intermediário, 2 frentes matemáticas puras, 2026-08-22), `DISC-DEC-023` (adoção de paralelismo multi-linha como modo padrão de operação; autorização de 2 frentes paralelas independentes da onda 5 — `SPARC-FMULTI-STAGE1` e `ARCHIVE-WIDE-PHASE0-SURVEY`, 2026-08-22), `DISC-DEC-024` (integração da onda 5: caso K=2 do Lema Aberto PROVADO incondicionalmente com referee adversarial de 4 camadas; mecanismo M-WEIB(β) de α intermediário encontrado e confirmado com correção de enquadramento, 2026-08-22), `DISC-DEC-025` (fechamento de `DISC-ARCHIVE-PHASE0-SURVEY-001` como `CLOSED_NULL`, 18/19 candidatos rejeitados; autorização de `DISC-COGNITIVE-EEG-SPECTRAL-001` como nova linha candidata, etapa de operacionalização apenas, 2026-08-22), `DISC-DEC-026` (integração da onda paralela de `DISC-DEC-023`: `SPARC-FMULTI-STAGE1` concluído e verificado adversarialmente, pronto para Estágio 2; operacionalização de `DISC-COGNITIVE-EEG-SPECTRAL-001` concluída, braço depressão pronto para pré-registro, braço ansiedade bloqueado por acesso, 2026-08-22), `DISC-DEC-027` (autorização de rascunhos NÃO travados para SPARC-004 Estágio 2 e braço depressão EEG, mais nova tentativa K3 do Lema Aberto, 2026-08-22), `DISC-DEC-028` (lock do pré-registro do braço depressão EEG, 2026-08-22), `DISC-DEC-029` (lock do pré-registro de `SPARC-FMULTI-STAGE2`, correção de robustez em `calibrate_f_multi()`, 2026-08-22), `DISC-DEC-030` (fechamento `CLOSED_REFUTED` do braço depressão EEG com reprodução adversarial confirmada, `DISC-CLAIM-007`, 2026-08-22), `DISC-DEC-031` (casos `K=3,4,5` do Lema Aberto provados por matriz de transferência uniforme em `K`, verificado por referee adversarial hostil separado, veredito SOUND, 2026-08-22) |
| Claims fechados/registrados | 7 (`DISC-CLAIM-001`, `preregistered_inconclusive`; `DISC-CLAIM-002`, `preregistered_inconclusive` após Gate, `replication_status: REPLICATION_FAILED`; `DISC-CLAIM-003`, `preregistered_falsified` [direção de H, efeito real na direção oposta], `replication_status: REPLICATION_PASSED`; `DISC-CLAIM-004`, `preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`, `replication_status: REPLICATION_FAILED` [inconclusivo por falta de poder no dataset reservado, não contradição]; `DISC-CLAIM-005`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [estatística estruturalmente incapaz de produzir veredito válido, não erro de implementação]; `DISC-CLAIM-006`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [confundidor de multiplicidade oculta plausivelmente suficiente para explicar o sinal residual, não erro de implementação — o bug de assimetria de ruído foi corrigido antes de catalogar]; `DISC-CLAIM-007`, `preregistered_falsified` [entropia espectral EEG em depressão na direção OPOSTA à prevista, `d=1,447`], `adversarial_review_verdict: CONFIRMED`) |
| Claims em andamento | 0 |

## Resultado do piloto (DISC-COSMOLOGY-MOND-SPARC-001)

Auditoria do código legado (`AUDIT_LEGACY_MOND_EFE_SPARC.md`) confirmou que
o resultado "EFE CONFIRMED, p<0.000001" de
`01_TAMESIS_CORE/.../MOND_EFE/efe/README.md` vinha de curvas de rotação
digitadas à mão para 8 galáxias de Virgem que **não existem** no catálogo
SPARC público real — não apenas um fallback de emergência, mas o dado por
trás da manchete inteira.

Refeito com dado real (SPARC_Lelli2016c.mrt + Rotmod_LTG/*.dat, 175
galáxias, proveniência em `data/PROVENANCE.md`), pré-registro travado antes
de qualquer cálculo (`PREREGISTRATION.md`, commit `49867fa`), o teste
comparável disponível (aglomerado de Ursa Maior vs. campo, já que Virgem não
está representado na amostra real) deu p=0.049373 — cruza o limiar de 0.05
na direção prevista pelo EFE, mas cai exatamente na zona frágil (0.04–0.06)
que o próprio pré-registro já previa precisar declarar como tal.

Reexecução adversarial independente reproduziu os números exatamente (sem
bugs) e mostrou que excluir 4 galáxias de campo com ajuste de inclinação
baseado em apenas 2 pontos inverte o veredito (p sobe para 0.0635). Veredito
formal: **INCONCLUSIVE**. Registrado em `DISC-CLAIM-001`, sem nenhuma
linguagem "CONFIRMED"/"DETECTED".

Este é o resultado que a trilha foi desenhada para produzir: nem a manchete
inflada do código legado, nem uma negação categórica — um número real,
reproduzido de forma independente, e corretamente rotulado como frágil
demais para sustentar qualquer alegação de detecção.

## Resultado de DISC-COSMOLOGY-MOND-SPARC-002 (pivotado, encerrado)

`next_action` original (extrair de `01_TAMESIS_CORE` uma previsão Tamesis
distinta de MOND genérico) resolvido com achado **negativo**: essa
previsão não existe. Pivotado para testar qual das duas derivações
internas conflitantes de `a₀` sobrevive ao dado real — `a₀=cH₀/(2π)`
("Ponte Holográfica") vs. `a₀=cH₀` ("MOND Emergence", cuja própria
alegação numérica já é aritmeticamente incorreta por fator ~5,7,
independente de qualquer dado).

Na amostra de descoberta (120 galáxias), o resultado pareceu decisivo:
`H_A` sobrevive, `H_B` falsificada por fator ~2,5×, reproduzido de forma
independente com 0,004% de diferença. O Gate de Replicação (holdout de 55
galáxias, nunca antes visto, aberto por um terceiro agente independente)
**não confirmou** esse resultado — `g†` no holdout saiu 3,5× maior,
intervalo de confiança largo o suficiente para conter as duas hipóteses.
Um adversário de nulo dedicado mostrou que o achado sobrevive a
sistemáticas conhecidas do SPARC, mas seu peso evidencial específico para
Tamesis é mais fraco do que parecia (a0_A reproduz uma coincidência já
conhecida na literatura MOND padrão desde antes de Tamesis existir).
Achado lateral acionável: `MOND_Emergence/index.html:282` provavelmente
contém um erro de copy-paste, independente do veredito estatístico.

Veredito final: `DISC-CLAIM-002`, `evidence_level: preregistered_inconclusive`,
`replication_status: REPLICATION_FAILED` (inconclusivo, não contraditório).
Ver `09_SESSIONS/2026/2026-08-12_A0_DERIVATION_PIVOT.md` para o relato
completo em ordem cronológica.

## Fase 0 de `DISC-COSMOLOGY-MOND-SPARC-003` (2026-08-14)

Iniciada a pedido do usuário. Três agentes investigaram em paralelo:
(1) busca exaustiva por nova previsão Tamesis-específica em
`01_TAMESIS_CORE` — **negativa**, toda fórmula adicional encontrada ou
reproduz exatamente MOND padrão (a função de interpolação "derivada"
por unicidade holográfica é numericamente idêntica à "Simple" de
Milgrom/Famaey & Binney; a função "TAMESIS" é a própria curva empírica
de McGaugh et al. 2016 rebatizada), ou já foi auto-refutada dentro do
próprio corpus (correlação M/L-`g_ext`), ou duplicaria SPARC-001 (teste
EFE Ursa Maior), ou não é falsificável como está (lente de aglomerado);
(2) a discrepância de leverage do holdout de SPARC-002 como germe de
teste — **negativa**, Monte Carlo mostrou que é variância de amostragem
comum (percentil ~78, nada extremo), sem nenhuma alegação Tamesis sobre
comportamento em alta aceleração para dar um modelo concorrente nomeado;
(3) dataset independente para replicar o veredito de SPARC-002 —
**positiva**: binárias largas do Gaia (El-Badry, Rix & Heintz 2021,
MNRAS 506, 2269) são reais, públicas, volumosas (≈1,94 GB, 1.817.594
pares), o mesmo catálogo usado por Chae (2023) para testes de gravidade
em regime de aceleração ultra-baixa.

**Achado de integridade grave, descoberto no processo:**
`01_TAMESIS_CORE/.../lab_gravity/analysis/gaia_real_analysis.py` contém
uma lista `REAL_GAIA_BINARIES` rotulada como dado real de El-Badry/Chae,
mas com `source_id` sequenciais/artificiais e progressão de velocidades
monotônica demais — dado fabricado. O achado "MOND DETECTED"
(`RESEARCH_RESULTS.md:259-261`) descansa sobre esse dado — mesmo padrão
do achado original que motivou a criação desta trilha (curvas de
Virgem fabricadas, SPARC-001).

**Rota recomendada:** tratar SPARC-003 como réplica independente do
veredito ainda inconclusivo de SPARC-002 (`H_A: a0=cH0/2π` vs.
`H_B: a0=cH0`), substituindo o dataset fabricado pelo catálogo real
El-Badry et al. (2021). Nenhuma nova alegação — mesmas duas hipóteses já
travadas em SPARC-002, observável discriminador adaptado ao novo
sistema físico (binário Kepleriano, não disco rotativo). Antes de
qualquer pré-registro: verificar por fetch direto a fórmula exata do
estimador de Chae (2023), declarar corte de qualidade e split
discovery/holdout próprios. Detalhes completos em
`02_TESTS/COSMOLOGY_WIDE_BINARIES/phase0/PHASE0_SEARCH.md`.

## Pré-registro travado de `DISC-COSMOLOGY-MOND-SPARC-003` (2026-08-14)

A pedido do usuário, pré-registro escrito e travado
(`02_TESTS/COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md`). Metodologia de
Chae verificada por fetch direto de **dois** artigos primários (uma
confusão de arXiv ID entre o título/ApJ citado e o número arXiv
originalmente fornecido foi descoberta e corrigida: são dois artigos
reais e distintos do mesmo autor, "Artigo A" ApJ 952,128/arXiv:2305.04613
e "Artigo B" arXiv:2309.10404, artigo de acompanhamento). O método
primário de Chae (desprojeção 3D via Monte Carlo orbital, dependente de
excentricidades de Hwang et al. 2022 não verificadas nesta sessão) foi
declarado tratável demais para reproduzir diretamente — adotado em vez
disso o método de perfil de velocidade projetada do Artigo B (simplicação
honesta e declarada, ainda real/publicada, validada pelo próprio Chae
como correlacionada ao método completo).

Catálogo real El-Badry, Rix & Heintz (2021) baixado por completo
(1.937.351.290 bytes = 100% do esperado, sha256 verificado duas vezes,
1.817.594 pares, contagem exata batendo com o paper). Cortes de
qualidade REAIS de Chae aplicados (`R<0,01` — não `R<0,1` como suposto
inicialmente —, `200<sepAU<30.000`, `BinType==MSMS`, distância`<200pc`,
`4<M_G<14`): **43.147 sistemas** sobrevivem. Massa estelar derivada via
relação massa-luminosidade de Pecaut & Mamajek (2013), tabela de Mamajek
baixada diretamente (catálogo não traz massa). Split
discovery(**30.203**)/holdout(**12.944** selado) gerado com seed
determinístico. Bordas de 5 bins de `log(g_N)` calculadas somente de
massa+separação — `a0_A` e `a0_B` ambos caem dentro da faixa de dado
disponível, dando poder genuíno ao teste. H_A/H_B idênticas às já
travadas em SPARC-002, não reformuladas. Nenhuma razão de velocidade
observada foi calculada antes deste lock.

Status: `CANDIDATE_LOCKED`. Próximo passo: rodar a análise
pré-registrada, depois reexecução adversarial independente.

## Resultado final de `DISC-COSMOLOGY-MOND-SPARC-003` (2026-08-14) — `CLOSED_INCONCLUSIVE`

Análise pré-registrada rodada sobre os 30.203 sistemas de descoberta,
seguida de reexecução adversarial independente (segundo agente,
implementação do zero, sem ler o código/resultado primário antes de ter
o próprio pronto). **Concordância bit a bit** em toda a parte
determinística entre os dois agentes — nenhum bug de fórmula, unidade,
constante ou binagem em nenhum dos dois scripts.

**As 5 medianas empíricas de `v_p_obs/v_p_N` por bin** (0,6932; 0,6409;
0,6243; 0,6150; 0,5941) **são todas abaixo de 1** — mas o modelo MOND
pré-registrado, `(1-e^{-√(g_N/a0)})^{-1/2}`, tem imagem estritamente em
`(1,+∞)` para qualquer `a0>0` finito. **Não existe `a0` que alcance o
alvo.** Checagem de convergência e checagem de sanidade (Seção 3 do
pré-registro) — ambas já declaradas como salvaguardas — falharam:
ajustes de `x0=1` e `x0=5` divergem ~16%; `a0` ajustado sai ~2,4 ordens
de grandeza abaixo do valor de referência McGaugh.

**Causa raiz confirmada independentemente, não é bug:** o agente
adversarial rodou uma simulação Monte Carlo própria (N=200.000) de
binárias Keplerianas puramente Newtonianas (zero física MOND) e obteve
mediana(v_proj/v_circ)≈0,55 — mesma ordem de grandeza do observado no
dado real. É diluição por projeção, efeito conhecido na literatura
(Pittordis & Sutherland 2018; Banik & Zhao 2018), já antecipada no
preâmbulo da Seção 4 do pré-registro como limitação da estatística
simplificada adotada.

Por instrução explícita da própria Seção 3 ("o teste para até isso ser
resolvido, antes de aceitar qualquer veredito H_A/H_B"): **nenhum
veredito H_A/H_B é aceito.** Registrado como `DISC-CLAIM-005`,
`evidence_level: preregistered_inconclusive`,
`adversarial_review_verdict: METHODOLOGY_FLAW_FOUND`. Gate de
Replicação nunca acionado (teste já falhou sua própria checagem de
sanidade). Holdout (12.944 sistemas) permanece selado, disponível para
um teste futuro genuinamente redesenhado com desprojeção completa.
Lição de governança registrada em `METHODOLOGY_EXTENSIONS.md` Seção 1.
Detalhes completos: `09_SESSIONS/2026/2026-08-14_SPARC003_WIDE_BINARIES.md`.

## Resultado final de `DISC-COSMOLOGY-MOND-SPARC-004` (2026-08-18) — `CLOSED_INCONCLUSIVE`

Usuário pediu para redesenhar SPARC-003 com desprojeção Monte Carlo
completa (método primário de Chae 2023: desprojeção 3D orbital, não a
simplificação de velocidade projetada que matou SPARC-003 por restrição
de imagem). Pré-registro travado após validação sintética pré-lock
corrigir a estatística discriminadora para `δ_obs-newt` (real menos mock
Newtoniano casado por sistema), reaproveitando H_A/H_B, catálogo, cortes
e split de SPARC-002/003 sem modificação.

**Análise primária v1:** `δ_obs-newt=[+0,2274;+0,1723;+0,1313;+0,1027;
+0,0467]`, `a0_fit=3,634×10⁻¹⁰` (IC95% `[2,944×10⁻¹⁰;4,494×10⁻¹⁰]`),
`BOTH_FALSIFIED` bruto. A descoberta adversarial de nulos obrigatória
(`AGENTS.md` passo 7) achou um **bug de implementação real** (não
reformulação): o ramo mock não carregava ruído astrométrico Gaia,
enquanto o ramo real carrega — viés de Rice/Rayleigh não cancelado pela
subtração real-mock, provado decisivamente via teste 100% sintético.
Corrigido, revalidado, análise real re-executada.

**Análise primária v2 (corrigida):** `δ_obs-newt=[+0,1486;+0,1482;
+0,1150;+0,0949;+0,0430]` (~5× menor), `a0_fit=1,657×10⁻¹⁰` (IC95%
`[1,232×10⁻¹⁰;2,181×10⁻¹⁰]`) — `a0_A` cai logo abaixo do IC (margem
~0,057 dex), `a0_B` claramente fora. Reexecução adversarial confirmou v2
bit a bit.

**Achado decisivo:** o gatilho pré-declarado (`g/g_N` real bruto>1 no
bin 0) ativou a checagem adversarial obrigatória de multiplicidade
oculta (`f_multi`, Chae Eqs. 11-13, declarada NÃO implementada). Com o
sinal v2 corrigido, companheiras não resolvidas — sozinhas, em magnitude
inteiramente plausível pela literatura (`f_multi=0,25-0,47`) — cobrem de
23% a 146% do sinal por bin, a diferença RUWE-alto/baixo excede o sinal
real total em vários bins, e mesmo `f_multi=0,25` produz sinal sintético
(zero MOND) maior que o sinal real inteiro nos 5 bins.

Por instrução explícita da própria Seção 4 do pré-registro ("checagem
adversarial de multiplicidade oculta obrigatória se `g/g_N>1`, ANTES de
aceitar qualquer veredito"): **nenhum veredito H_A/H_B é aceito.**
Registrado como `DISC-CLAIM-006`, `evidence_level:
preregistered_inconclusive`, `adversarial_review_verdict:
METHODOLOGY_FLAW_FOUND`. Gate de Replicação não acionado. Holdout
(12.944 sistemas) permanece selado, disponível para uma tentativa futura
que implemente a auto-calibração completa de `f_multi`. Detalhes
completos: `02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/PREREGISTRATION.md`
Seção 7; `09_SESSIONS/2026/2026-08-18_SPARC004_MC_DEPROJECTION.md`.

## Resultado da linha RH-REAL (dois sub-testes, ambos com Gate acionado)

Motivada pela pesquisa de zeros de zeta da Anthropic, a linha `DISC-RH-REAL-001`
converteu duas afirmações de literatura não-testáveis com dado finito
(`liminf`/"infinitos") em perguntas proxy falsificáveis com modelo
concorrente nomeado, satisfazendo a exigência de discriminating observable.

**Sub-teste 1 — `DISC-RH-ZERO-GAP-RUNS-001`** (item 9, correlação sequencial
de gaps). Hipótese direcional original **errada** — previu mais runs de
gaps grandes consecutivos, achado real foi o oposto (`INVERSE_SIGNAL`,
reportado honestamente como tal, sem spin). Gate de Replicação com
`zeros4.txt` (regime #10²¹): `REPLICATION_PASSED`. Adversário de nulo
mostrou que o efeito é genérico a qualquer sequência com autocorrelação
serial negativa (confirmado via simulação sintética AR(1)) — isso não
enfraquece o achado, já que a alegação substantiva sempre foi "gaps de
zeta têm correlação serial negativa", não um mecanismo exclusivo de zeta.
Ver `09_SESSIONS/2026/` para o relato completo desta sessão.

**Sub-teste 2 — `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`** (item 7,
constante de gaps pequenos de Inoue 2026, arXiv:2604.05733). Pergunta
proxy via teoria de valores extremos: gap normalizado mínimo entre `N`
zeros escala como `N^(-1/3)` (GUE) ou `N^(-1)` (Poisson)? Resultado sobre
`zeros1.txt` (100k zeros): `β̂=-0,3395`, quase exatamente `-1/3=-0,3333`,
IC 95% bootstrap `[-0,3872;-0,2868]` — contém GUE folgadamente, exclui
Poisson e GOE (`-1/2`) com folga grande. `evidence_level:
preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`
(reprodução bit a bit por agente independente, três métodos de ajuste
concordantes). Gate de Replicação completo acionado sobre `zeros5.txt`
(regime #10²², nunca antes baixado): **`REPLICATION_FAILED` por falta de
poder estatístico**, não por contradição — o dataset reservado só tem
9.999 gaps, insuficiente para a grade travada (0 blocos possíveis em
N=10.000; só N=500/N=1.000 atingem a barra de ≥8 blocos declarada no
pré-registro, e restritos a esses dois pontos o IC vira
não-informativo). O achado primário sobre `zeros1.txt` permanece de pé,
apenas não pôde ser confirmado de forma independente numa terceira altura
com esta fonte específica. `promoted_to_formal_lab: false` — confirmação
numérica de universalidade GUE já conhecida na literatura, não descoberta
matemática nova. Lição de governança documentada em
`03_REPLICATION_GATE/PROTOCOL.md`: verificar A PRIORI que uma fonte
reservada tem amostra suficiente para a grade já travada, não apenas que
existe em regime diferente. Ver
`09_SESSIONS/2026/2026-08-12_RH_GAP_EXTREME_VALUE_SCALING.md` para o
relato completo.

Não há mais fonte adicional de Odlyzko disponível no regime #10²² para
resolver a falta de poder do sub-teste 2 sem consumir dado já usado.

## Resultado da Fase 0 de `DISC-TRI-RG-001` (2026-08-14)

5 candidatos de par `(R_lambda, I(X))` avaliados em paralelo por agentes
de pesquisa independentes, cada um obrigado a verificar dado real (baixar/
inspecionar, não só citar) antes de declarar um domínio utilizável. Relato
completo em `02_TESTS/TRI_RG/phase0/PHASE0_SURVEY.md`.

**3/5 `viable: true`**, ranqueados por uma síntese adversarial que aplicou
a mesma régua a todos: (1) **critical-slowing-down** — variância/
autocorrelação lag-1 crescentes perto de bifurcação (Scheffer 2009, Dakos
2008/2012, Lenton 2012); 3 domínios com transição REAL dentro do mesmo
sistema no tempo, dado verificado (GISP2/Younger Dryas, PhysioNet SDDB/
onset de fibrilação ventricular, NASDAQ/crash pontocom); modelo
concorrente nomeado real (B-tipping vs. R/N-tipping, Ashwin 2012); ainda
faltam regra de `lambda` cross-domain, protocolo de nulo substituto, e o
cálculo real de `Delta I` (só o acesso ao dado foi verificado). (2)
**wavelet-multiresolution-scaling** — `R_lambda` mais rigoroso
matematicamente dos 5 (`R_2λ=R_λ'∘R_λ` por construção via subespaços
aninhados), mas só 1 domínio robusto (sismologia, mainshock de Tohoku
2011, rótulo USGS/GCMT externo). (3) **dfa-multiscale-entropy** —
execução empírica mais sólida (DFA implementado do zero, validado contra
nulos teóricos, rodado sobre dado PhysioNet real decodificado E sobre os
gaps de zeta já usados em `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`), mas
os 2 domínios usados são comparações ESTÁTICAS de classe (saudável vs.
insuficiência cardíaca; continental vs. oceânico), não transições
temporais — mesmo defeito que corretamente derrubou o candidato (4)
abaixo, só detectado na síntese cross-candidato.

**2/5 `viable: false`**, corretamente rejeitados pelos próprios agentes:
(4) **box-covering-network-renorm** (Song-Havlin-Makse) — `R_lambda` mais
literal de todos, dado real de 4 redes verificado (SNAP/CAIDA), mas toda
"transição" fractal↔não-fractal na literatura vem de modelos sintéticos
com parâmetro artificial; dado real só mostra classificação estática, e
essa classificação está sob disputa ativa em 2025. (5)
**spacing-statistics-rmt-non-zeta** — dado real e computação real
executados (níveis nucleares RIPL-3, autovalores de rede SNAP), mas falha
em identificabilidade (previsão idêntica ao consenso BGS/RMT de 40 anos)
e em RG/EFT (nenhum `R_lambda` genuíno implementado).

**Nenhum candidato foi travado.** Decisão de qual (ou quais) perseguir
fica com o usuário.

## Fechamento dos 3 gaps de `critical-slowing-down` (2026-08-14) — resultado NEGATIVO

A pedido do usuário, os 3 gaps concretos do candidato `critical-slowing-
down` (rank 1 na Fase 0) foram fechados: (a) regra de `lambda`
cross-domain — todos os parâmetros de escala expressos como frações fixas
do comprimento do segmento (convenção Dakos et al. 2012), a mesma em
todo domínio; (b) protocolo de teste contra nulo substituto — AR(1) de
parâmetro constante, 1000 substitutos, teste unicaudal (Dakos et al. 2008
*PNAS*); (c) `Delta I` calculado de fato nos 3 domínios já verificados
(GISP2, PhysioNet SDDB, NASDAQ). Metodologia fixada e commitada (commit
`b43fde0`) ANTES de qualquer cálculo real; pipeline única
(`csd_common.py`) validada contra dado sintético primeiro (caso nulo:
sem tendência; caso com CSD injetado: `τ=1,000`, detectado), depois
chamada sem modificação por 3 agentes independentes.

**Resultado: NEGATIVO.** Das 12 combinações testadas (3 domínios × 2
variantes de janela × 2 canais — AC1 e variância), apenas 1 cruzou
`p<0,05` (GISP2, variante de 50% mais recente, canal AC1: `τ=0,848`,
`p=0,032`) — estatisticamente consistente com ruído puro sob 12
comparações múltiplas sem correção (esperado ~0,6 falsos positivos ao
acaso). Mais grave: em 2 dos 3 domínios (PhysioNet SDDB, NASDAQ variante
primária), o canal de AC1 mostrou tendência FORTEMENTE NEGATIVA
(`τ=-0,82`, `τ=-0,95`, `τ=-0,37`) — direção OPOSTA à prevista por CSD,
não apenas ausência de sinal. `critical-slowing-down`, formulado com uma
regra de `lambda` genuinamente cega ao domínio (exigência central de
`DISC-TRI-RG-001`), não produz um invariante cross-domain confiável
nestes 3 domínios/transições. Achado negativo honesto, catalogado com o
mesmo peso que um resultado positivo teria — não invalida CSD como
fenômeno geral na literatura (que usa janelas informadas por
conhecimento específico de cada sistema, não uma regra cega), apenas
mostra que esta instanciação específica cross-domain não sobrevive.
Nenhum `PREREGISTRATION.md` foi escrito — o próprio passo de fechamento
de gaps evitou travar um pré-registro fadado ao fracasso. Detalhes
completos em `02_TESTS/TRI_RG/critical_slowing_down/RESULTS_SUMMARY.md`.

## Busca de segundo domínio para `wavelet-multiresolution-scaling` (2026-08-14)

Com `critical-slowing-down` descartado, usuário pediu para buscar um
segundo domínio robusto para `wavelet-multiresolution-scaling` (que
tinha só sismologia/Tohoku 2011 na Fase 0). Três agentes investigaram em
paralelo três candidatos — relato completo em
`02_TESTS/TRI_RG/wavelet_multiresolution/SECOND_DOMAIN_SEARCH.md`.

**Recomendado: EEG de crise epiléptica (CHB-MIT, PhysioNet).** Banco
aberto (sem login), registro real de 42,4 MB baixado e parseado byte a
byte com parser EDF escrito do zero, rótulo de transição clínico
(onset/offset de crise em segundos, dentro do mesmo registro contínuo do
paciente) — mesma estrutura de rótulo já validada em sismologia e no
domínio cardíaco de `critical-slowing-down`. Ressalvas: só 1 crise/1
paciente verificada (182 crises/22 pacientes disponíveis para
replicação futura); EEG de escalpo é mais suscetível a artefato que
ECG/sismômetro.

**Domínio de apoio válido: turbulência de plasma no vento solar** (NASA
OMNI + catálogo independente CfA de choques interplanetários) —
transição real confirmada numericamente (velocidade do vento solar
400→729 km/s, `|B|` 7,7→30,5 nT no choque de 2024-10-10), mas domínio
FISICAMENTE DIFERENTE do WTMM hidrodinâmico histórico (que continua sem
fonte livremente acessível encontrada — lacuna honesta reconfirmada).

**Descartado: MAWI/MAWILab** — dado real verificado, rótulo genuíno para
fluxos isolados, mas falha estrutural (só captura amostras diárias de 15
min, nunca contínuas — eventos pequenos ficam invisíveis no agregado,
eventos grandes preenchem a janela toda sem baseline); também
descontinuado pelos mantenedores em dezembro/2024.

## Fechamento dos gaps de `wavelet-multiresolution-scaling` (2026-08-14) — resultado NEGATIVO

A pedido do usuário, os gaps restantes (regra de janela, cálculo real do
método, protocolo de substitutos) foram fechados nos 2 domínios acima.
Metodologia fixada e commitada (commit `6da7112`) ANTES de qualquer
cálculo real: `WTMM`/wavelet-leader completo substituído honestamente
por log-cumulantes de coeficientes wavelet (WCM — Castaing/Gagne/
Hopfinger 1990, Delbeke/Abry 2000, Wendt/Abry/Jaffard 2007), por
tratabilidade computacional; `R_lambda` continua a mesma projeção
multirresolução wavelet. Pipeline validada contra controle sintético
multifractal (ruído gaussiano modulado por cascata log-normal) antes de
tocar dado real.

**EEG (CHB-MIT, chb01_03):** variante primária com significância nominal
(`p=0,040` ΔC2; `p=0,015` ΔC1) desaparece por completo quando o PRE é
truncado ao mesmo tamanho do POST (`p=0,290`; `p=0,900`, ΔC1 chega a
inverter de sinal) — frágil, dependente do desenho do teste.

**Sismologia (Tohoku 2011, IU.ANMO/BHZ):** achado inicial muito
significativo (`ΔC2=+0,356 p=0,005`; `ΔC1=+0,942 p=0,000`) acionou
checagem adversarial completa. Hipótese de saturação/clipping do
sismômetro REJEITADA (pico usa só 31,3% da escala de 24 bits, sem
assinatura de clipping, sem relatos documentados para ANMO/GSN durante
Tohoku 2011). Mas o achado NÃO sobrevive a um truncamento genuíno
(`N=16.384`: `ΔC2` dispara para 2,30 mas é diagnosticado como artefato
de estimador de amostra pequena; `ΔC1` perde significância,
`p=0,595`) nem a aparar apenas 1% das amostras mais extremas do POST
(`ΔC2` inverte de sinal e perde toda significância, `p=0,990`) —
consistente com a limitação do próprio IAAFT sob marginais de cauda
pesada já documentada na validação sintética desta metodologia.

**Veredito: NEGATIVO nos 2 domínios.** Nenhuma variante tem `ΔC2` E
`ΔC1` simultaneamente significativos e estáveis.
`wavelet-multiresolution-scaling`, como `critical-slowing-down` antes
dele, não produz um invariante cross-domain confiável testado com
protocolo genuinamente cego ao domínio e checagem adversarial completa.
Nenhum `PREREGISTRATION.md` foi escrito. Detalhes completos em
`02_TESTS/TRI_RG/wavelet_multiresolution/RESULTS_SUMMARY.md`.

## Retomada de `DISC-TRI-RG-001` e fechamento dos gaps de `dfa-multiscale-entropy` (2026-08-14) — resultado NEGATIVO

Usuário pediu explicitamente para retomar a linha após a pausa
(`DISC-DEC-005`). Um agente de busca dedicado encontrou um domínio
fisiológico com transição temporal GENUÍNA (corrigindo o defeito da Fase
0, que usava comparações estáticas de classe): PhysioNet Apnea-ECG
Database, registro `a04` (AHI=77,4, apneia severa), 35 min de sono normal
seguidos imediatamente por 140 min contínuos de apneia dentro do mesmo
paciente/registro, rótulo clínico externo (Thomas Penzel). Segundo
domínio cross-domain: paleoclima GISP2, reaproveitado de
`critical-slowing-down` (mesma transição Younger Dryas→Preboreal).

Pipeline DFA-1 nova (`dfa_common.py`) validada contra dado sintético
ANTES de qualquer dado real — a validação revelou que o teste IAAFT
bicaudal originalmente especificado na metodologia tem baixo poder para
`alpha` (substitutos preservam o espectro linear, que é essencialmente o
que `alpha` mede: o controle positivo sintético, H=0,5→H=0,9, não atingiu
`p<0,05`). Corrigido ANTES de tocar dado real: adicionado um teste
complementar de bootstrap por blocos móveis (Künsch 1989), que passou a
ser o teste PRIMÁRIO de significância — mesma disciplina de
`METHODOLOGY_EXTENSIONS.md` Seção 1 (verificar comportamento da
estatística contra nulo/sintético antes de gastar tempo em dado real).

**Resultado: NEGATIVO cross-domain.** Apneia-ECG mostrou sinal forte nos
6 testes de bootstrap (`p<0,05`, maioria `p<0,001`), que sobreviveu à
reexecução adversarial cega (extração independente de RR bate ~byte a
byte) e à winsorização (não é artefato de outlier) — mas a descoberta
adversarial de nulos identificou um mecanismo fisiológico já conhecido há
40 anos (CVHR — Cyclical Variation of Heart Rate, Guilleminault et al.
1984) que explica o efeito por completo, batendo exatamente com o AHI
documentado do paciente. GISP2 não replicou o sinal (5 dos 6 testes de
bootstrap não significativos). `dfa-multiscale-entropy`, como os outros 2
candidatos antes dele, não produz um invariante cross-domain confiável.
Detalhes completos em
`02_TESTS/TRI_RG/dfa_multiscale_entropy/RESULTS_SUMMARY.md`.

**Estado final da linha:** os 3 candidatos viáveis da Fase 0
(`critical-slowing-down`, `wavelet-multiresolution-scaling`,
`dfa-multiscale-entropy`) testados com rigor completo — metodologia
pré-commitada, pipeline validada contra dado sintético, checagem
adversarial completa onde o efeito justificou — os 3 resultado NEGATIVO
para invariante cross-domain. Nenhum `PREREGISTRATION.md` foi escrito em
nenhum dos 3. Toda a infraestrutura (3 pipelines validadas, 9
domínios/variantes testados no total) fica commitada e reaproveitável.

## Revisita com registros de backup do Apnea-ECG (2026-08-15)

Usuário pediu para revisitar os candidatos com os registros de backup do
Apnea-ECG mapeados na busca de `dfa-multiscale-entropy` (`a18`, `a14`,
`a01`). Questionado sobre escopo, optou por tratar o banco como um
domínio fisiológico NOVO para os 3 candidatos (não só replicação de DFA).
3 agentes independentes baixaram os 3 registros e rodaram as 3 pipelines
já validadas sem modificação. Detalhes completos em
`02_TESTS/TRI_RG/APNEA_BACKUP_RECORDS_REVISIT.md`.

**Não resolve a exigência cross-domain** (os 3 registros são do MESMO
domínio já testado em `a04`). CSD: sem sinal em nenhum registro (mesmo
padrão de ausência já visto em todos os outros domínios). Wavelet
(primeira aplicação a apneia-ECG): `ΔC1` mostra padrão direcionalmente
consistente, mas é exatamente o canal que a própria linha já suspeitava
refletir amplitude, não estrutura multifractal genuína; `ΔC2` instável.
DFA: a direção de `Δalpha`/`Δalpha2` (queda) **replica nos 4 registros de
apneia** (`a18` é o mais fraco); `Δalpha1` (o canal mais dramático em
`a04`) é o menos replicável. Fortalece a leitura já registrada — efeito
fisiológico real que generaliza parcialmente entre pacientes, mas
continua sendo a mesma explicação mundana já identificada (CVHR). Checagem
adversarial adicional não foi acionada para os registros de backup
(efeitos mais modestos que o achado original, custo alto vs. valor
marginal baixo, declarado explicitamente).

## Nova rodada de busca de candidatos para `DISC-TRI-RG-001` (2026-08-15)

Após `DISC-DEC-006` (segunda pausa), usuário pediu a única rota de
retomada ainda não exercida: nova busca por candidatos ainda não
considerados. 5 agentes independentes em paralelo investigaram 6
candidatos genuinamente novos (não variações dos 5 originais). Detalhes
completos em `02_TESTS/TRI_RG/phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`.

**4 `viable=true`:** (1) **Entropia Multiescala (MSE)** — fundamentação
formal de `R_lambda` mais rigorosa já considerada nesta linha (conexão
direta com o Teorema Central do Limite via Jona-Lasinio 2001), 2 domínios
novos verificados (tempestade geomagnética 1989, rolamento FEMTO/PRONOSTIA
até falha), mas risco real de redundância com a família Hurst já testada
(DFA/wavelet). (2) **Expoentes de criticalidade auto-organizada (SOC)** —
matemática genuinamente distinta dos 3 já testados, 2 domínios novos
(sismicidade Ridgecrest 2019, flares solares GOES/NOAA), sem risco de
redundância identificado, mecanismos mundanos já mapeados e corrigíveis.
(3) **Grafo de visibilidade + box-covering** — reaproveita box-covering já
verificado (nunca implementado em código na Fase 0 original), 2 domínios
novos (geomagnetismo 2015, furacão Harvey), mas risco de redundância com
Hurst documentado DIRETAMENTE na literatura (Xie & Zhou 2011). (4) **RQA
(Recurrence Quantification Analysis)** — único candidato com regras de
parâmetro NÃO-arbitrárias publicadas, mas sondagem exploratória própria já
mostrou o MESMO padrão de inconsistência cross-domain que derrubou
`critical-slowing-down`.

**2 `viable=false`, corretamente rejeitados com justificativa concreta:**
percolação sob ataque a hubs (nenhum evento real tem simultaneamente
fragmentação genuína E reconstrução publicada de `S(f)`); escala de
Anderson (nenhuma generalização real se liberta de transporte de onda
quântico).

**Ranking honesto, não travado:** SOC > MSE > grafo de visibilidade > RQA.
Nenhum candidato foi travado — decisão de qual perseguir (se algum) fica
com o usuário.

## Fechamento de gaps de `soc-avalanches` (2026-08-15) — resultado NEGATIVO

Candidato ranqueado #1 na nova rodada de busca. Metodologia (binagem por
intervalo médio entre eventos, `I(X)`=`tau` via MLE + `sigma`, substituto
Poisson + bootstrap pareado após validação sintética revelar perda de
poder do Poisson sob desequilíbrio de taxa) fixada e pipeline validada
ANTES de qualquer dado real. Detalhes completos em
`02_TESTS/TRI_RG/soc_avalanches/RESULTS_SUMMARY.md`.

**Ridgecrest 2019 (sismicidade):** achado inicial na variante de robustez
(`p_bootstrap_tau=0,0`) acionou a escalada condicional já pré-declarada
(nulo ETAS subcrítico) — resultado `p_ETAS_tau=0,273`, NÃO significativo.
Descoberta adversarial de nulos reproduziu o mesmo "efeito" dividindo
apenas a janela POST (sem nenhuma transição envolvida) — decaimento
clássico de Omori-Utsu, não SOC/invariante novo. **Flares solares GOES:**
sem sinal em nenhuma variante, direção instável.

**Estado da linha:** 4 candidatos agora testados com rigor completo
(`critical-slowing-down`, `wavelet-multiresolution-scaling`,
`dfa-multiscale-entropy`, `soc-avalanches`) — os 4 NEGATIVO. Restam 3
candidatos da nova busca não fechados (MSE, grafo de visibilidade, RQA).

## Fechamento de gaps de `mse-multiscale-entropy` (2026-08-15) — resultado NEGATIVO

Candidato ranqueado #2 na nova rodada de busca. Validação sintética
confirmou o discriminador de identificabilidade central desta linha: ao
contrário de `alpha`/DFA, o IAAFT TEM poder real para `CI`/`beta`
(controle positivo com `p=0,0`), o que já resolve substancialmente o
risco de redundância com Hurst identificado na Fase 0.5. Detalhes
completos em `02_TESTS/TRI_RG/mse_multiscale_entropy/RESULTS_SUMMARY.md`.

**Resultado real:** sem sinal em nenhuma das 8 combinações testadas (2
domínios × 2 variantes × 2 canais) — geomagnetismo (SYM-H, tempestade de
março/1989) e rolamento (FEMTO/PRONOSTIA `Bearing1_1`, run-to-failure)
ambos completamente negativos. Nenhuma reexecução adversarial completa
foi acionada (proporcional — sem achado significativo a explicar, ao
contrário de DFA/apneia-ECG e SOC/Ridgecrest). Desvio metodológico
honesto no domínio de rolamento: PRE decimado por stride (fator 200) por
inviabilidade computacional, risco de ter atenuado sinal fino não
descartado.

**Estado da linha:** 5 candidatos agora testados com rigor completo
(`critical-slowing-down`, `wavelet-multiresolution-scaling`,
`dfa-multiscale-entropy`, `soc-avalanches`, `mse-multiscale-entropy`) —
os 5 NEGATIVO. Resta 1 candidato da nova busca não fechado (grafo de
visibilidade; RQA também não fechado).

## Fechamento de gaps de `grafo-de-visibilidade` (2026-08-18) — resultado NEGATIVO

Usuário pediu para retomar `DISC-TRI-RG-001`; escolhido o candidato
ranqueado #3 na busca de 2026-08-15 (grafo de visibilidade natural,
Lacasa et al. 2008, + box-covering, Song-Havlin-Makse 2005). Metodologia
fixada em `02_TESTS/TRI_RG/visibility_graph/METHODOLOGY_NOTE.md` ANTES
de qualquer cálculo real.

**Achado decisivo da validação sintética obrigatória:** `d_B` (dimensão
fractal de box-covering, canal primário originalmente declarado) é
ESTRUTURALMENTE NÃO COMPUTÁVEL para séries temporais estocásticas —
grafos de visibilidade são "small-world" (diâmetro cresce só como
`~log(N)`, medido entre 9 e 19 para `N` de 1.000 a 15.000), nunca
atingindo o piso de 20 exigido pela própria grade a priori, mesmo no
teto de 5.000 amostras já declarado. Não é bug (diagnóstico com série
determinística confirma o código correto) nem falta de poder estatístico
(bootstrap por blocos móveis testado e não resolve — 25/25 reamostras
continuam insuficientes). Decisão, fixada ANTES de dado real, honrando a
própria regra de rejeição já pré-declarada em vez de afrouxá-la: `d_B`
retirado do critério; `C` (clustering, canal companheiro) promovido a
`I(X)` único — validado com poder real forte (~14,55 desvios-padrão no
controle positivo sintético).

**Resultado real** (geomagnetismo — SYM-H, tempestade 17/03/2015, NASA
OMNI; hidrologia — régua, furacão Harvey, USGS 08074500, pico real
confirmado 44,31 pés): NEGATIVO limpo nas 4 combinações
(2 domínios × 2 variantes), `p_C` entre 0,595 e 0,995, sem consistência
direcional entre domínios. `d_B` não-computável nos 4 casos reais,
confirmando a previsão da validação. Reexecução adversarial NÃO
acionada por proporcionalidade (nada significativo a explicar, mesmo
princípio já usado em MSE). Detalhes completos:
`02_TESTS/TRI_RG/visibility_graph/RESULTS_SUMMARY.md`.

**Estado da linha:** 6 dos 7 candidatos identificados (3 da Fase 0
original + 4 da nova busca) agora têm resultado completo — os 6
NEGATIVO. Resta apenas 1 candidato formalizado não fechado: RQA (rank #4
— sondagem exploratória já mostrou o mesmo padrão de inconsistência
cross-domain que derrubou `critical-slowing-down`).

## Fechamento de gaps de `RQA` (2026-08-18) — fechado NA VALIDAÇÃO, dado real nunca tocado

Usuário pediu para fechar também o RQA — último candidato identificado
nesta linha (7 de 7 no total). Metodologia fixada em
`02_TESTS/TRI_RG/rqa/METHODOLOGY_NOTE.md` ANTES de qualquer cálculo real:
regras de parâmetro não-arbitrárias e publicadas (FNN para `m`,
informação mútua para `tau`, taxa de recorrência fixa para `epsilon`),
embedding compartilhado PRE/POST, `I(X)=%DET+ENTR`, IAAFT primário.

**Validação sintética, tentativa 1** (PRE=ruído branco, conforme
especificado): achado estrutural mais severo que o de
`grafo-de-visibilidade` — FNN nunca resolve `m<=10` para ruído branco
(nem AR(1) até `phi=0,9`, só a partir de `phi=0,95` ou `H(fGn)>=0,3`),
bloqueando `%DET` E `ENTR` simultaneamente (compartilham o mesmo passo de
embedding). Não é bug (diagnóstico determinístico confirma código
correto) nem falta de poder (bootstrap testado, 0/25 resolve).

**Correção de desenho, fixada ANTES de dado real, com protocolo de
decisão mecânico pré-declarado (nenhuma terceira tentativa autorizada):**
trocar a fonte caótica de POST do mapa logístico (espectro banda-larga,
causa de um descasamento espectral que confundiu uma tentativa informal
anterior) para o sistema de Rössler (espectro colorido, compatível com o
PRE `fGn H=0,7` já validado).

**Validação, tentativa 2 (Rössler):** embedding resolveu (`m=4, tau=40`),
bom casamento espectral — mas `p_DET=1,0`, `p_ENTR=1,0`, sem poder real
em nenhum canal. Aplicando o protocolo pré-fixado mecanicamente:
candidato **fechado na própria etapa de validação** — o dado real
(rolamento IMS/Rexnord, vulcão Kīlauea 2018) nunca foi tocado. Resultado
honesto e completo, distinto de "negativo no dado real" mas igualmente
definitivo para os propósitos desta linha. Detalhes completos:
`02_TESTS/TRI_RG/rqa/RESULTS_SUMMARY.md`.

## Estado final da linha `DISC-TRI-RG-001` — 7 de 7 candidatos identificados com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| `mse-multiscale-entropy` | Geomagnetismo (1989), rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |
| `grafo-de-visibilidade` | Geomagnetismo (2015), hidrologia/Harvey | NEGATIVO (sem achado em nenhum domínio) |
| `RQA` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |

Nenhum candidato produziu um invariante cross-domain confiável. Isso é um
prior forte e honesto contra a hipótese central desta linha tal como
formulada até aqui (um par `R_lambda`/`I(X)` genuinamente cego ao
domínio, aplicado sem reformulação, prevendo transições em domínios
físicos diferentes) — não uma prova de impossibilidade. Toda a
infraestrutura (7 `METHODOLOGY_NOTE.md`, 6 pipelines validadas e
aplicadas a dado real, domínios reais de 14+ fontes testadas no total)
fica commitada e reaproveitável.

## Fase 0.6 — nova busca de candidatos (2026-08-18)

Usuário pediu nova rodada de busca. 5 agentes independentes em paralelo
investigaram 5 candidatos genuinamente novos (nenhuma reformulação leve
dos 7 já testados), cada um com instrução de verificar dado real e
avaliar risco de identificabilidade contra todos os 7 candidatos já
fechados. **Resultado: 4 `viable=true`, 1 `viable=false`.**

1. **Entropia de permutação + plano complexidade-entropia** (Bandt-Pompe/
   Rosso) — melhores regras de parâmetro não-arbitrárias desta rodada
   (`m∈{3..7}`, `N>=5·m!`, `tau` via informação mútua), 2 domínios novos
   fortes (VitalDB indução de anestesia, PhysioNet European ST-T
   isquemia). `H_S` sozinho tem risco documentado de redundância com
   Hurst (Zunino et al. 2008); `C_JS` (complexidade de Jensen-Shannon) é
   o discriminador proposto, nunca testado na literatura contra IAAFT.
2. **Kramers-Moyal / Friedrich-Peinke** (reconstrução de Fokker-Planck)
   — regra de seleção de `lambda` mais principiada de toda a linha até
   agora (teste de Markov-Einstein/Chapman-Kolmogorov orientado a dado,
   não janela escolhida), 2 domínios novos (choque do SNB EUR/CHF
   tick-a-tick; `vfdb` com ~10 transições N→VFL→N dentro do mesmo
   registro). Risco de redundância com `critical_slowing_down`
   confirmado analiticamente (Ritchie & Sieber 2016), mas canal de
   escape real e citado (forma global do potencial, Livina & Lenton
   2007/2010).
3. **Homologia persistente / TDA** — matemática mais distinta de todas
   (topologia algébrica), domínio inédito genuinamente novo (deformação
   de onda gravitacional LIGO GW150914). Único candidato com checagem
   EMPÍRICA própria de redundância já rodada nesta sessão: correlação
   r≈0,92 entre persistência máxima de H1 e o `%DET` do RQA (que nem
   chegou a tocar dado real) no regime mais relevante para detectar
   transição. Custo computacional real força janelas pequenas.
4. **Índice de cauda EVT/Hill estimator** — bem fundamentado (seleção de
   limiar automatizada, Danielsson et al. 2001; Bader, Yan & Zhang
   2018), 2 domínios novos (onda de calor 2021 Pacífico Noroeste;
   furacão Florence/Rio Cape Fear, gauge diferente do Harvey). Risco de
   redundância com SOC via princípio do "grande salto único" — real,
   parcialmente mitigado, barato de checar cedo.
5. **RG de block-spin literal sobre série binarizada** — `viable: false`,
   fechado por identificabilidade ANALÍTICA (a decimação de Ising 1D
   força fluxo trivial para qualquer processo de correlação de curto
   alcance; quando tem poder discriminativo, colapsa numa versão mais
   ruidosa do Hurst já testado 2x negativo) — sem tocar dado real, mesmo
   espírito de `spacing-statistics-rmt-non-zeta` na Fase 0 original.

Nenhum candidato foi travado. Ranking honesto (não travado): permutação+
CECP > Kramers-Moyal > TDA > EVT/Hill. Detalhes completos:
`02_TESTS/TRI_RG/phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md`.

## Fechamento de gaps de `entropia-de-permutacao` (2026-08-18) — resultado NEGATIVO

Usuário pediu para fechar o candidato ranqueado #1 na Fase 0.6.
Metodologia (coarse-graining reaproveitado de MSE + embedding ordinal
Bandt-Pompe, `m=4` fixo; `I(X)=H_S`/`PCI`+`C_JS`/`MCI`) fixada em
`02_TESTS/TRI_RG/permutation_entropy/METHODOLOGY_NOTE.md` ANTES de
qualquer cálculo real.

**Validação sintética — o resultado mais limpo desta linha até agora:**
ao contrário da hipótese a priori (`C_JS` teria poder, `H_S` talvez não,
como `alpha` do DFA), **os DOIS canais mostraram poder real completo**
contra o controle positivo IAAFT (mapa logístico: `p_PCI=0,0`,
`p_MCI=0,0`, ambos com separação de ~10-12 desvios-padrão da nula). Um
controle adicional de Hurst diferencial (`H=0,3` vs. `H=0,9`, sem
conteúdo não-linear, pedido pela sessão orquestradora para testar
diretamente o risco de identificabilidade já nomeado — Zunino et al.
2008) confirmou que nenhum canal mostra significância espúria por mero
desvio linear de Hurst (`p=1,0` em ambos) — o risco foi resolvido ANTES
de tocar dado real, não descoberto depois.

**Resultado real** (VitalDB, indução de anestesia via EEG; PhysioNet
European ST-T, episódio isquêmico transitório): **sem sinal
significativo nas 8 combinações** (2 domínios × 2 variantes × 2 canais).
A variante primária do domínio isquêmico teve os `p` mais baixos da
linha inteira (`p_PCI=0,275`, `p_MCI=0,325`, direção qualitativamente
intuitiva para isquemia) mas não cruzou `p<0,05` e não se reproduziu na
variante de robustez — reportado honestamente como tendência sub-limiar,
não achado. Durante a etapa de dado real, um bug de desempenho real foi
encontrado e corrigido (subamostragem do Gap (d) não aplicada antes da
geração de substitutos IAAFT), com revalidação sintética confirmada
bit-idêntica após a correção. Reexecução adversarial completa não
acionada por proporcionalidade (nada significativo a explicar).

**Veredito honesto:** negativo, mas não por falta de poder do teste — é
o único candidato desta linha cuja validação sintética confirmou poder
completo em AMBOS os canais declarados, tornando este o resultado
negativo mais confiável (menos ambíguo) já obtido nesta linha. Detalhes
completos: `02_TESTS/TRI_RG/permutation_entropy/RESULTS_SUMMARY.md`.

**Estado da linha:** 8 dos 8 candidatos fechados até agora (7 da linha
original + este) sem invariante cross-domain sobrevivente. Restam 3
candidatos formalizados da Fase 0.6 ainda não fechados: Kramers-Moyal/
Friedrich-Peinke (rank #2), homologia persistente/TDA (rank #3), índice
de cauda EVT/Hill (rank #4).

## Fechamento de gaps de `kramers-moyal` (2026-08-19) — sem veredito computável, dois motivos estruturais honestos

Usuário pediu para fechar o candidato ranqueado #2 na Fase 0.6.
Metodologia (teste de Markov-Einstein/Chapman-Kolmogorov para `tau_ME`;
`I(X)=PKS`, curtose de forma do potencial reconstruído) fixada em
`02_TESTS/TRI_RG/kramers_moyal/METHODOLOGY_NOTE.md` ANTES de qualquer
cálculo real — incluindo uma decisão a priori incomum: `kappa`
(taxa de decaimento local) foi demovido a diagnóstico-apenas DESDE O
INÍCIO, com base numa prova algébrica publicada (Ritchie & Sieber 2016,
não uma correlação empírica) de que é identidade exata com a mesma
grandeza que `critical_slowing_down` já testou e refutou.

**Validação sintética:** `PKS` (canal primário) confirmado com poder
real e limpo (`p=0,005` no controle positivo de SDE biestável, `p=0,23`
no negativo). `beta_D2` (companheiro) não mostrou poder detectável em
nenhuma das duas variantes pré-autorizadas nem sob o fallback de
bootstrap — demovido também a diagnóstico por decisão da sessão
orquestradora (adendo, commit `9d35eeb`), ANTES de qualquer dado real.

**Resultado real, dois motivos estruturais distintos, nenhum deles
problema de poder do IAAFT:**
- **PhysioNet `vfdb`** (arritmia ventricular maligna, registro 418):
  propriedade de Markov NUNCA estabelecida — o teste de CK rejeita
  fortemente em quase todos os lags curtos testados, resultado
  teoricamente esperado para amplitude bruta de ECG sem informação de
  fase cardíaca. `tau_ME` não encontrado, `PKS` não computado.
- **EUR/CHF** (choque do SNB, 15/01/2015, confirmado empiricamente:
  preço caiu de 1,200975 para 1,020855 em 5min): `tau_ME` estabelecido
  normalmente no PRE, mas `PKS` fica ESTRUTURALMENTE INDEFINIDO no
  POST — o choque (~15% num dia) é grande demais para os 10 bins de
  quantil fixados do PRE resolverem o POST (~50% de todo o POST cai
  num único bin), consequência honesta da própria regra "bins fixados
  do PRE" (travada precisamente para evitar reestimação ad hoc)
  colidindo com um choque de magnitude extrema.

Reexecução adversarial não acionada (nenhum achado positivo computável
a explicar). Uma nota metodológica para tentativas futuras (bins sobre
a união PRE+POST, ou normalização por log-retorno) foi registrada, não
implementada. Detalhes completos:
`02_TESTS/TRI_RG/kramers_moyal/RESULTS_SUMMARY.md`.

**Estado da linha:** 9 dos 9 candidatos fechados até agora sem
invariante cross-domain sobrevivente. Restam 2 candidatos formalizados
da Fase 0.6 ainda não fechados: homologia persistente/TDA (rank #3),
índice de cauda EVT/Hill (rank #4).

## Fechamento de gaps de `evt-hill` (2026-08-19) — negativo/não testável

Usuário pediu para fechar o último candidato formalizado da Fase 0.6.
Metodologia fixada em `02_TESTS/TRI_RG/evt_hill/METHODOLOGY_NOTE.md`
ANTES de qualquer cálculo real, com um desvio deliberado da convenção
padrão desta linha: o protocolo de significância NÃO usa IAAFT (que
preserva a marginal exata por construção, tornando a nula degenerada
para um estimador puramente baseado em estatísticas de ordem como
Hill) — usa em vez disso um teste de randomização do ponto de corte.
`I(X)=xi_Hill` (primário, limiar REESTIMADO por segmento, não fixado do
PRE) + `xi_MLE` (companheiro, GPD/MLE).

**Validação sintética:** `xi_Hill` correto contra distribuições de
cauda conhecida; poder real do teste de randomização confirmado para
PRE/POST desbalanceado (o caso realista). Checagem obrigatória de
redundância com SOC (reaproveitando dado já commitado) ficou
inconclusiva por poder estatístico (`n=3`), levemente contra
redundância simples.

**Resultado real:** PDX (onda de calor 2021, NOAA GHCN-Daily)
ESTRUTURALMENTE NÃO TESTÁVEL — piso de amostra não atingido (POST=37
dias, resolução diária vs. janela de "semanas" exigida para evitar
circularidade). Cape Fear (furacão Florence 2018, USGS 02105769):
canal primário `xi_Hill` sem significância em nenhuma variante
(`p=0,185`/`0,22`); canal companheiro `xi_MLE` significativo só na
variante de robustez (`p=0,025`), investigado a fundo e explicado por
um platô de crista de cheia físico real e limitado (suporte GPD
finito, não cauda mais pesada), não um achado cross-domain genuíno.
Checagem de confundidor de comporta (Lock 1, gatilho pré-declarado)
acionada — evidência circunstancial pesa contra o confundidor
(estrutura submersa no pico). Detalhes completos:
`02_TESTS/TRI_RG/evt_hill/RESULTS_SUMMARY.md`.

**Estado da linha:** 10 dos 11 candidatos identificados fechados sem
invariante cross-domain sobrevivente. Resta apenas 1 candidato
formalizado não fechado: homologia persistente/TDA (rank #3).

## Fechamento de gaps de `homologia-persistente` (2026-08-20) — fechado NA VALIDAÇÃO, Fase 0.6 completa

Usuário pediu para fechar o último candidato formalizado da Fase 0.6
(rank #3, TDA via filtração de Vietoris-Rips sobre embedding de
Takens). Metodologia fixada em
`02_TESTS/TRI_RG/persistent_homology/METHODOLOGY_NOTE.md` ANTES de
qualquer cálculo real: embedding `m=3` FIXO (deliberadamente diferente
da regra de FNN do RQA, que já falhara estruturalmente para ruído
branco), desenho de sub-janelas (`N_WINDOW=200`, até 10 por segmento)
diretamente motivado pelo custo computacional já MEDIDO na Fase 0.6.

**Validação sintética — achado decisivo, respondendo diretamente ao
risco já medido na Fase 0.6** (correlação `r≈0,92` entre persistência
máxima de H1 e um análogo do `%DET`(RQA) num teste informal): os DOIS
canais (`I(X)`=persistência máxima e total de H1) mostraram
`IAAFT_LOW_POWER` contra o controle positivo não-linear (`p=0,355` e
`p=0,320`), e o fallback de bootstrap por blocos móveis pré-autorizado,
acionado automaticamente, TAMBÉM não mostrou poder (`p=0,454`/`0,368`).
Controle negativo corretamente não-significativo em ambos os testes.
Diagnóstico de correção de código passou limpo (onda senoidal traça um
laço inequívoco em espaço de fase).

**Mecanismo diferente de como o RQA falhou, resultado final igual:** o
embedding com `m=3` fixo resolveu perfeitamente em ~1.200 séries (zero
falhas de `tau`) — o problema não é resolução de embedding, é que a
própria estatística de persistência não separa sinal caótico genuíno de
ruído colorido de espectro casado, sob este desenho. Fechado NA ETAPA DE
VALIDAÇÃO, sem terceira tentativa de redesenho (mesma disciplina já
usada no RQA) — o dado real (LIGO GW150914, S&P500/Lehman) nunca foi
tocado. Detalhes completos:
`02_TESTS/TRI_RG/persistent_homology/RESULTS_SUMMARY.md`.

**Estado da linha:** Fase 0.6 completa — 4 de 4 candidatos formalizados
fechados, nenhum produziu invariante cross-domain sobrevivente. **11 de
11 candidatos identificados nesta linha, desde sua criação, têm
resultado final** (2 fechados na etapa de validação — RQA e
homologia-persistente —, 9 testados até dado real, todos negativos ou
estruturalmente não-testáveis). Nenhum invariante cross-domain
confiável foi encontrado por esta linha até agora.

## O que já foi feito nesta trilha

1. Governança criada: `00_GOVERNANCE/{AGENTS.md,DECISION_LEDGER.yaml,CLAIM_LEDGER.yaml,PREREGISTRATION_TEMPLATE.md}`.
2. Piloto escolhido (autorização explícita do usuário): auditar e refazer o
   teste EFE/SPARC de `01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE`.
3. Auditoria do código legado completa (`AUDIT_LEGACY_MOND_EFE_SPARC.md`,
   8 achados citados por arquivo:linha).
4. Dado real baixado e verificado (`data/PROVENANCE.md`).
5. Pré-registro travado (`PREREGISTRATION.md`, commit `49867fa`).
6. Análise pré-registrada executada sobre dado real
   (`analysis/run_preregistered_analysis.py`, `result_primary.json`).
7. Reexecução adversarial por agente independente
   (`analysis/adversarial_reproduction.py`, `result_adversarial.json`) —
   veredito INCONCLUSIVE.
8. Resultado registrado em `TEST_QUEUE.yaml` (status `CLOSED_INCONCLUSIVE`)
   e `CLAIM_LEDGER.yaml` (`DISC-CLAIM-001`).
9. Decisão de fechamento registrada (`DISC-DEC-002`).

## Arquitetura adotada em 2026-08-12 (`DISC-DEC-003`)

Revisão estratégica externa do usuário identificou que o laboratório
formal (Ondas 1-7, `04_FORMAL_RESEARCH_LAB`) provavelmente otimizava
probabilidade de fechamento (13/13 em três ondas seguidas) em vez de valor
científico esperado. Resposta: arquitetura de três motores
(`00_GOVERNANCE/RESEARCH_PIPELINE.md`) — descoberta de risco alto aqui,
Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`) de risco baixo no
meio, formalização Lean de risco baixíssimo só para quem sobrevive os dois.
Seis extensões técnicas de metodologia adotadas junto
(`00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md`): identificabilidade
(discriminating observable obrigatório), RG/EFT para TRI/TDTR, MDL/
complexidade algorítmica (`ΔJ`), descoberta automática de invariantes
antes de narrativa LLM, descoberta adversarial de nulos (debunker
convencional dedicado), holdout selado obrigatório para buscas amplas.

Três linhas candidatas registradas (`01_PORTFOLIO/TEST_QUEUE.yaml`,
status `CANDIDATE_FORMULATING`, nenhuma pré-registrada):
- `DISC-COSMOLOGY-MOND-SPARC-002` — SPARC como comparação preditiva de
  modelos nomeados, não confirmação/refutação de EFE isolada.
- `DISC-RH-REAL-001` — pesquisa real sobre `riemannZeta`, distinta do
  operador de brinquedo `Tp` (agora reclassificado em
  `04_FORMAL_RESEARCH_LAB` como teste unitário de maquinário, não
  caminho até RH — ver `DEC-107` de lá).
- `DISC-TRI-RG-001` — busca de invariante cross-domain via lente de
  renormalização/coarse-graining para a Theory of Regime Interfaces.

## O que ainda não foi feito

- Decisão do usuário sobre qual candidato de `DISC-TRI-RG-001` perseguir
  (ver seção própria acima) e fechamento dos gaps concretos do candidato
  escolhido antes de qualquer `PREREGISTRATION.md`.
- Fora do escopo desta trilha, mas acionável: reportar/corrigir o
  provável erro de copy-paste em
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Universe_Equation/02_MOND_Emergence/index.html:282`.

## Como continuar (para o próximo agente/sessão)

Ler `00_GOVERNANCE/RESEARCH_PIPELINE.md` e `METHODOLOGY_EXTENSIONS.md`
primeiro. Para `DISC-TRI-RG-001` ou uma nova linha, seguir
`00_GOVERNANCE/AGENTS.md` desde o passo 1 — mas o passo 3 exige declarar
o discriminating observable (e holdout selado, se aplicável) no
`PREREGISTRATION.md` antes do commit de lock, e ao reservar uma fonte de
dado adicional para o Gate, verificar A PRIORI que ela tem amostra
suficiente para a grade/estatística que será travada (lição de
`03_REPLICATION_GATE/PROTOCOL.md`, 2026-08-13). Não reabrir nem editar
`02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` (piloto 001),
`02_TESTS/COSMOLOGY_A0_DERIVATION/PREREGISTRATION.md` (teste 002),
`02_TESTS/RH_ZETA_ZEROS/PREREGISTRATION.md` (RH-REAL sub-teste 1) nem
`02_TESTS/RH_GAP_EXTREME_VALUE_SCALING/PREREGISTRATION.md` (RH-REAL
sub-teste 2) — todos fechados e travados, holdouts/fontes reservadas já
consumidos. Uma extensão de qualquer uma dessas linhas de investigação é
um novo teste com seu próprio pré-registro, não uma reabertura.
