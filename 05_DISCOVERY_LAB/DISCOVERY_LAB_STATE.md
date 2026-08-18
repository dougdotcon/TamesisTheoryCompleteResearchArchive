# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-18 (fechamento de `grafo-de-visibilidade`, `DISC-TRI-RG-001`)
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
| Teste ativo | Nenhum. `DISC-COSMOLOGY-MOND-SPARC-004` encerrado (`CLOSED_INCONCLUSIVE`, 2026-08-18, ver seção própria abaixo — redesenho de SPARC-003 com desprojeção Monte Carlo completa; confundidor de multiplicidade oculta plausivelmente suficiente para explicar todo o sinal residual). `DISC-COSMOLOGY-MOND-SPARC-003` encerrado (`CLOSED_INCONCLUSIVE` — estatística pré-registrada estruturalmente incapaz de produzir veredito válido, não erro nem falta de dado). `DISC-RH-ZERO-GAP-RUNS-001` encerrado (`REPLICATION_PASSED`). `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` encerrado (`REPLICATION_FAILED` — inconclusivo por falta de poder no dataset reservado, achado primário NÃO contradito). `DISC-COSMOLOGY-MOND-SPARC-002` encerrado (`REPLICATION_FAILED`). `DISC-COSMOLOGY-MOND-SPARC-001` encerrado (`CLOSED_INCONCLUSIVE`). `DISC-TRI-RG-001` retomada em 2026-08-18 a pedido do usuário para fechar o candidato `grafo-de-visibilidade` (rank #3) — resultado NEGATIVO (ver seção própria abaixo); 6 dos 7 candidatos identificados na linha agora têm resultado completo, os 6 NEGATIVO; resta apenas RQA não fechado |
| Fase | RH-REAL: dois sub-testes concluídos, ambos com Gate de Replicação completo acionado. (1) `DISC-RH-ZERO-GAP-RUNS-001`: `INVERSE_SIGNAL` `REPLICATION_PASSED` — gaps grandes consecutivos são menos comuns que sob reordenação aleatória, confirmado em 3 regimes de altura (~75.000, ~10¹², ~10²¹). (2) `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`: gap mínimo escala como `N^(-1/3)` (GUE), exclui `N^(-1)` (Poisson) e `N^(-1/2)` (GOE) — `β̂=-0,3395` vs. previsão `-0,3333`, `evidence_level: preregistered_confirmed` sobre o dataset primário; Gate no terceiro dataset reservado (`zeros5.txt`, #10²²) resultou `REPLICATION_FAILED` por amostra pequena demais para a grade travada (0 blocos possíveis em N=10.000) — inconclusivo, não contraditório. TRI-RG: os 3 candidatos viáveis da Fase 0 agora testados com rigor completo, os 3 NEGATIVO para invariante cross-domain — `critical-slowing-down` (GISP2/SDDB/NASDAQ), `wavelet-multiresolution-scaling` (Tohoku/CHB-MIT), `dfa-multiscale-entropy` (Apneia-ECG/GISP2, achado forte de 1 domínio explicado por mecanismo fisiológico já conhecido — CVHR — e não replicado no segundo domínio); mais 3 candidatos novos fechados NEGATIVO (`soc-avalanches`, `mse-multiscale-entropy`, `grafo-de-visibilidade` — este último com achado adicional decisivo: `d_B`, o canal originalmente primário, é estruturalmente não computável para séries estocásticas, small-world por construção; `C`, promovido a canal único ANTES de dado real, validado com poder real mas sem sinal em nenhum dos 2 domínios). Resta apenas RQA não fechado nesta linha. SPARC-003: pré-registro travado como réplica independente do veredito de SPARC-002 via binárias largas Gaia reais (43.147 sistemas pós-corte); modelo MOND pré-registrado tem imagem `(1,+∞)` mas as 5 medianas empíricas reais são todas `<1` — ajuste estruturalmente impossível (diluição por projeção). `CLOSED_INCONCLUSIVE`. SPARC-004: redesenho de SPARC-003 com desprojeção 3D via Monte Carlo (método primário de Chae 2023, estatística `δ_obs-newt`); `a0_fit=1,657×10⁻¹⁰` (IC95% `[1,232×10⁻¹⁰;2,181×10⁻¹⁰]`) após correção de um bug de assimetria de ruído astrométrico encontrado pela descoberta adversarial de nulos; veredito bruto `BOTH_FALSIFIED`, mas a checagem adversarial de multiplicidade oculta (gatilho pré-declarado) mostrou que companheiras não resolvidas, em magnitude plausível pela literatura, são sozinhas suficientes para explicar todo o sinal — `CLOSED_INCONCLUSIVE`, nenhum veredito H_A/H_B aceito |
| Próxima ação obrigatória | Nenhuma — todas as quatro linhas cosmológicas SPARC/MOND (001-004) encerradas; `DISC-TRI-RG-001` com 6 de 7 candidatos identificados agora fechados (todos NEGATIVO), resta só RQA. Aguardando próxima direção do usuário: (a) implementar a auto-calibração completa de `f_multi` de Chae (Eqs. 11-13) e reabrir a linha SPARC com um pré-registro genuinamente novo sobre o holdout selado; (b) investigar o achado de integridade de `gaia_real_analysis.py`; (c) nova linha inteiramente distinta; (d) fechar gaps de RQA (único candidato formalizado restante em `DISC-TRI-RG-001`), nova busca, revisitar candidatos já testados com dados diferentes, ou considerar a linha suficientemente explorada (6/6 negativos) |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto), `DISC-DEC-003` (arquitetura de três motores + seis extensões), `DISC-DEC-004` (pivô de SPARC-002 + pré-registro do teste de derivação de a₀), `DISC-DEC-005` (1ª pausa de `DISC-TRI-RG-001`, revertida em 2026-08-14), `DISC-DEC-006` (2ª pausa, revertida em 2026-08-15), `DISC-DEC-007` (3ª pausa de `DISC-TRI-RG-001` a pedido do usuário, 2026-08-15, após 5 dos 6 candidatos considerados na nova busca resultarem NEGATIVO) |
| Claims fechados/registrados | 6 (`DISC-CLAIM-001`, `preregistered_inconclusive`; `DISC-CLAIM-002`, `preregistered_inconclusive` após Gate, `replication_status: REPLICATION_FAILED`; `DISC-CLAIM-003`, `preregistered_falsified` [direção de H, efeito real na direção oposta], `replication_status: REPLICATION_PASSED`; `DISC-CLAIM-004`, `preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`, `replication_status: REPLICATION_FAILED` [inconclusivo por falta de poder no dataset reservado, não contradição]; `DISC-CLAIM-005`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [estatística estruturalmente incapaz de produzir veredito válido, não erro de implementação]; `DISC-CLAIM-006`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [confundidor de multiplicidade oculta plausivelmente suficiente para explicar o sinal residual, não erro de implementação — o bug de assimetria de ruído foi corrigido antes de catalogar]) |
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
