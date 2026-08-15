# Nota de metodologia — fechamento dos gaps de `soc-avalanches`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (sismicidade de Ridgecrest 2019, flares solares GOES).
Mesmo espírito de disciplina já usado para `critical-slowing-down`,
`wavelet-multiresolution-scaling` e `dfa-multiscale-entropy`.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`
(candidato 2) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #1 entre os 4 novos candidatos — matemática
genuinamente distinta dos 3 já testados (baseada em eventos discretos/leis
de potência, não em expoentes de escala de série contínua), sem risco de
redundância identificado, mecanismos mundanos já mapeados.

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.5): 2 domínios reais com dado baixado/inspecionado
(sismicidade de Ridgecrest via API FDSN do USGS, 30.131 eventos M≥0,5;
flares solares via GOES XRS/NOAA), transição documentada por fonte
externa em ambos (mainshock M7,1 em 06/07/2019 03:19 UTC; máximo/mínimo do
ciclo solar 24 datados pelo painel NASA/NOAA). Nenhum `tau`/`sigma` foi
calculado ainda. Faltam: (a) regra de binning temporal (`lambda`) e
definição operacional de avalanche; (b) definição exata de `I(X)` e
declaração de identificabilidade (distinguir de leis já conhecidas há
décadas nos 2 domínios); (c) protocolo de nulo substituto.

## Gap (a): regra de binning temporal (`R_lambda`) e definição de avalanche

**Decisão:** binning temporal em janelas NÃO sobrepostas de largura
`lambda`, seguindo a convenção padrão da literatura de avalanches
neuronais (Beggs & Plenz 2003; Priesemann et al. 2014): `lambda` = médio
INTERVALO ENTRE EVENTOS (mean inter-event interval, IEI) — não um valor
absoluto de tempo escolhido à mão, e não ajustado separadamente por
domínio além do que a própria taxa de eventos já determina.

**Regra crítica para não conflar mudança de TAXA com mudança de
ESTRUTURA:** `lambda` é calculado UMA VEZ, a partir do IEI médio de todo o
fluxo de eventos COMBINADO (PRE+POST concatenados, mesmo domínio), e
aplicado SEM MODIFICAÇÃO à binagem de PRE e de POST separadamente. Se
`lambda` fosse recalculado separadamente para cada segmento (IEI local),
uma mudança pura de taxa entre PRE e POST (que não é o que este candidato
quer testar) poderia mecanicamente induzir ou apagar qualquer diferença de
`I(X)` — o mesmo risco de viés de desenho já evitado em
`critical-slowing-down` (fração fixa do comprimento do segmento, não um
valor recalibrado por domínio).

**Definição de avalanche** (Beggs & Plenz 2003): uma avalanche é uma
sequência MÁXIMA de janelas (bins) consecutivas não-vazias, delimitada por
pelo menos uma janela vazia (ou pela borda do segmento) de cada lado.
`s` (tamanho) = soma da contagem de eventos em todas as janelas da
avalanche. `T` (duração) = número de janelas que ela ocupa.

**Robustez:** repetir com `lambda_robustez = 2 * lambda_primaria` e
`lambda_robustez_2 = lambda_primaria / 2` — checagem de sensibilidade à
escolha de escala, reportada junto com a primária, nunca escolhida a
posteriori pela mais favorável.

## Gap (b): definição de `I(X)` e declaração de identificabilidade

**`I(X)` primário:** `tau`, o expoente da lei de potência
`P(s) ~ s^{-tau}` da distribuição de tamanho de avalanche, estimado por
MÁXIMA VEROSSIMILHANÇA (Clauset, Shalizi & Newman 2009, *SIAM Review*
51:661 — método padrão-ouro, NÃO regressão OLS de `log P(s)` vs. `log s`,
que é um método enviesado e desaconselhado pela própria literatura de
leis de potência). `s_min` (limiar inferior do ajuste) determinado pelo
próprio método de Clauset et al. via minimização da estatística
Kolmogorov-Smirnov entre o ajuste e o dado empírico — não escolhido à
mão. Incerteza de `tau` estimada por bootstrap não-paramétrico (parte do
método original de Clauset et al.).

**`I(X)` secundário (canal companheiro):** razão de ramificação
`sigma = <n_{t+1}> / <n_t>`, média sobre pares de janelas consecutivas
DENTRO de avalanches (excluindo janelas de borda vazias), convenção de
Beggs & Plenz — `sigma≈1` no ponto crítico, `sigma<1` subcrítico,
`sigma>1` supercrítico.

`Delta_tau = tau(POST) - tau(PRE)`, `Delta_sigma = sigma(POST) -
sigma(PRE)`.

**Declaração de identificabilidade (Seção 1 de `METHODOLOGY_EXTENSIONS.md`,
obrigatória):** os dois domínios escolhidos têm leis de escala JÁ
estabelecidas há décadas que precisam ser distinguidas explicitamente do
que este candidato testa, para não redescobrir trivialmente algo já
conhecido:

- **Sismologia:** a lei de Gutenberg-Richter (1944) já descreve a
  distribuição de MAGNITUDE de terremotos individuais como lei de
  potência (valor-b). Isso é uma estatística DIFERENTE do que este
  candidato mede: `tau` aqui vem da distribuição de tamanho de
  AVALANCHES (clusters de eventos definidos por proximidade temporal via
  `lambda`), não da magnitude de eventos individuais — depende da
  estrutura de CLUSTERING/RAMIFICAÇÃO do processo pontual, não apenas da
  distribuição marginal de tamanho de cada evento. Um resultado positivo
  aqui não pode ser apresentado como "redescoberta de Gutenberg-Richter"
  nem pode ignorá-la — a checagem de robustez ao formato Omori-Utsu do
  decaimento de réplicas (ver Gap (c)) existe precisamente para isolar
  esse risco.
- **Flares solares:** existe precedente real de expoentes de lei de
  potência já medidos para energia/pico de fluxo de flares individuais
  (Lu & Hamilton 1991, `N(E)~E^-1,4`) — mesma distinção: aquilo é
  distribuição de flares individuais, este candidato mede clusters
  temporais de eventos.

**Modelo concorrente nomeado e real** (não espantalho): processo de
Poisson homogêneo (mesma taxa média, sem estrutura de clustering) — nulo
canônico da literatura de SOC desde Bak, Tang & Wiesenfeld (1987). Para
sismologia especificamente, um modelo concorrente mais forte e nomeado
existe (ETAS de parâmetro de ramificação subcrítico `n<1`, Ogata 1988;
Helmstetter & Sornette 2002) — **declarado aqui como limitação conhecida:
não implementado nesta rodada de fechamento de gaps** (custo de ajuste de
um modelo ETAS completo é desproporcional a esta etapa exploratória);
reservado como checagem adversarial de escalada SE o efeito em sismologia
for grande o suficiente para justificar, mesmo padrão já usado para o
achado inicial de Tohoku em `wavelet-multiresolution-scaling`.

## Gap (c): protocolo de nulo substituto

**Decisão primária:** substitutos de Poisson homogêneo. Para cada
segmento (PRE, POST), ajustar a taxa média de eventos `mu` do segmento
real; gerar `N_SURROGATES=1000` realizações independentes de um processo
de Poisson homogêneo com essa mesma taxa `mu` e o mesmo comprimento
temporal do segmento real (mesmo número esperado de eventos, contagem
exata sorteada de `Poisson(mu * duracao)`). Rodar a MESMA pipeline de
binagem/avalanche/MLE (Gaps (a) e (b), `lambda` fixo já calculado do dado
real combinado — reaproveitado sem recalibração por substituto) em cada
substituto, obtendo `tau_substituto`, `sigma_substituto`.

`Delta_tau_substituto = tau_substituto_POST - tau_substituto_PRE` (pareado
por índice de substituto `i`, cada `i` com seu próprio par PRE/POST
gerado independentemente da taxa real de cada segmento).

**Teste BICAUDAL** (mesmo raciocínio já usado em
`wavelet-multiresolution-scaling` e no adendo de
`dfa-multiscale-entropy`): a própria busca de Fase 0.5 já identificou
ambiguidade de direção na literatura (o próprio agente de busca achou
resultados conflitantes sobre se complexidade/criticalidade sobe ou desce
perto de tempestades geomagnéticas em candidatos correlatos) — declarar
bicaudal a priori em vez de escolher a direção depois de ver o resultado.
`p = fração de substitutos com |Delta_tau_substituto| >= |Delta_tau_real|`
(e igualmente para `sigma`). Semente fixa `seed=12345`.

**Escalada condicional ao tamanho do efeito (declarada a priori, não
decidida depois de ver o resultado):** se o resultado em SISMOLOGIA
mostrar `p<0,05` E o efeito sobreviver às checagens de robustez de STAI
(Gap (d) abaixo), um nulo ETAS subcrítico ajustado (Gap (b)) deve ser
implementado como checagem adversarial adicional antes de qualquer
conclusão — mesmo padrão de escalada proporcional ao efeito já usado 2x
nesta linha (Tohoku, apneia-ECG a04).

## Gap (d): definição de segmento PRE/POST e mitigação de STAI (mecanismo mundano já identificado a priori)

Regra domain-agnostic REAPROVEITADA sem modificação de
`critical-slowing-down`/`dfa-multiscale-entropy` (mesma convenção já usada
2x nesta linha, incluindo para os registros de backup do Apnea-ECG): PRE
(primária) = todo o registro contínuo disponível anterior à transição
documentada; PRE (robustez) = os 50% mais recentes (por CONTAGEM de
eventos) desse PRE. POST (primária) = todo o registro contínuo disponível
posterior à transição, até o próximo evento/confundidor documentado; POST
(robustez) = os 50% mais próximos da transição (por contagem) desse POST.

**Mitigação de STAI (incompletude de curto prazo pós-mainshock),
identificada a priori pelo agente de busca como o mecanismo mundano mais
provável em sismologia:** em vez de excluir uma janela temporal arbitrária
pós-mainshock (introduziria um segundo parâmetro livre não-principiado),
a magnitude de completude `Mc` é determinada EMPIRICAMENTE via técnica de
máxima curvatura (Wiemer & Wyss 2000) separadamente para PRE e para POST;
o `Mc` FINAL usado é `max(Mc_PRE, Mc_POST) + 0,2` (margem de segurança
padrão da literatura), aplicado como corte de magnitude mínima IDÊNTICO a
PRE e POST — nenhuma amostra é descartada por estar "perto demais" do
mainshock em tempo, só por estar abaixo do `Mc` conservador que garante
completude em TODO o período, incluindo a janela mais afetada por STAI.
Isso evita introduzir um buffer temporal arbitrário mantendo a mesma
disciplina domain-agnostic do resto desta nota.

**Transição de instrumento em flares solares (mecanismo mundano
identificado a priori pelo agente de busca):** a janela de flares solares
DEVE permanecer inteiramente dentro do arquivo homogêneo de um único
satélite/instrumento GOES (a Fase 0.5 já identificou risco de confundidor
se a transição de mínimo de dez/2019 for usada, cruzando a troca
GOES-15→GOES-16/17). Usar a fase de declínio do ciclo 24 (máximo em
~abril/2014, aproximando-se do mínimo em 2017), inteiramente dentro do
arquivo legado `goes-xrs-report_*.txt` já verificado — declarado
explicitamente como simplificação (não cobre o mínimo real de dez/2019),
mesmo espírito de simplificação declarada já usado em
`wavelet-multiresolution-scaling` (WCM em vez de WTMM completo).

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado. A metodologia acima foi fixada ANTES de qualquer cálculo,
precisamente para que, se um pré-registro for escrito depois, ele possa
declarar honestamente que a regra de escala, a definição de `I(X)` e o
protocolo de nulo já existiam antes de qualquer resultado ser visto.
