# Fase 0.7 — nova busca de candidatos para `DISC-TRI-RG-001` (2026-08-20)

Usuário pediu uma nova rodada de busca (`"nova busca de candidatos"`) logo
após a linha ter sido pausada (`DISC-DEC-008`, "suficientemente explorada
por ora") ao concluir os 11 candidatos anteriores (3 da Fase 0 original + 4
da Fase 0.5 + 4 da Fase 0.6), todos NEGATIVOS ou fechados na etapa de
validação. Isto reabre a linha na prática (mesmo padrão já visto 3x nesta
linha: `DISC-DEC-005`/`006`/`007` foram todas revertidas quando o usuário
pediu retomada/nova busca) — `status` permanece `CANDIDATE_FORMULATING`,
nenhum novo `DISC-DEC-00N` é registrado agora; o registro formal da
reabertura fica para quando a rodada atual for encerrada (mesmo padrão que
`DISC-DEC-008` seguiu para toda a saga desde `DISC-DEC-007`).

5 agentes independentes em paralelo investigaram 5 candidatos genuinamente
novos (nenhuma reformulação leve de nenhum dos 11 anteriores), cada um com
instrução explícita de (a) verificar dado real por download/fetch direto,
não só citar; (b) avaliar risco de identificabilidade contra TODOS os 11
candidatos já fechados, não só o mais óbvio; (c) reportar um veredito
`viable: true/false` honesto, sem inflar viabilidade.

**Resultado: 3 `viable=true`, 2 `viable=false` — ambos os `false` por
motivo analítico/de literatura rigoroso (equivalência matemática provada
com estatísticas já fechadas negativas), não por dado indisponível.**

## 1. Complexidade de Lempel-Ziv (LZC) — `viable: true`

`R_lambda`: binarização por limiar de mediana (Aboy, Hornero, Abásolo &
Álvarez 2006, *IEEE Trans. Biomed. Eng.* 53:2282) + normalização de
Kaspar & Schuster 1987 (`b(n)=n/log2(n)`) — a regra mais simples e livre
de parâmetro desta linha até agora: **sem embedding, sem dimensão, sem
delay, sem grade de escalas** — evita estruturalmente o "poço" de
não-resolução de embedding que já matou `RQA` e quase matou `homologia
persistente` na etapa de validação.

`I(X)`: LZC normalizada sobre a série binarizada por mediana (primário) +
LZC normalizada sobre quantização ternária (Kamath 2016, companheiro,
relevante especificamente ao domínio de marcha/Parkinson abaixo).

**2 domínios novos verificados por download real:** (a) Daphnet
Freezing-of-Gait (UCI, acelerometria tri-axial de marcha em Parkinson,
64Hz, 10 pacientes, transições reais de congelamento anotadas por vídeo
sincronizado — sujeito `S01R01` tem 18 transições reais dentro de um único
registro contínuo, desenho multi-transição comparável ao `vfdb` do
Kramers-Moyal); (b) erupção do Kilauea 2018 (Lower East Rift Zone,
sismicidade vulcânica via IRIS FDSN, estação `HV.HAT..HHZ`, 100Hz) — LZC
computada diretamente como checagem de sanidade de computabilidade:
PRE=0,116, POST=0,259, não-degenerada, dobrando de valor.

**Risco de identificabilidade central, honesto:** LZC converge
assintoticamente para a taxa de entropia (Ziv & Lempel 1978) — o mesmo
alvo teórico de `CI`/`beta`(MSE, já fechado negativo) e, por extensão via
a família de Hurst, possivelmente de `alpha`(DFA)/`h(2)`(wavelet)
(mesmo risco genérico já identificado para `H_S`(entropia de permutação)
por Zunino et al. 2008). **Contra-evidência real e concreta encontrada:**
Villazana, Seijas & Caralli 2015 mostram LZC e entropia de Shannon
NÃO-monotonicamente relacionadas em registros reais do MIT-BIH Arrhythmia
(registro 109: entropia alta, LZC baixa); Mateos, Zozor & Olivares
2017/2020 constroem um plano LZC-permutação vs. entropia-de-Shannon-
permutação e o mostram COMPLEMENTAR, não redundante, separando fBm de
fGn de ruído-K apesar de espectros médios idênticos. Plano de
discriminador: sobrevivência ao IAAFT (o próprio teste de falsificação
desta linha) — nenhum artigo publicado testou IAAFT contra LZC
especificamente em nenhum dos 2 domínios (verificado por busca dedicada).
**Fraqueza estrutural nomeada honestamente:** ao contrário de `C_JS`
(entropia de permutação), LZC não tem um segundo canal projetado
especificamente para separar caos determinístico de ruído correlacionado
(limitação documentada por Nagarajan 2002) — o canal ternário é um
diagnóstico de robustez, não um discriminador desse tipo.

## 2. Maior expoente de Lyapunov (LLE, algoritmo de Rosenstein) — `viable: true`

`R_lambda`: embedding de Takens reaproveitando as regras já auditadas
desta linha (FNN de Kennel et al. 1992 para `m`, informação mútua de
Fraser & Swinney 1986 para `tau`) + janela de Theiler via período médio
(convenção original de Rosenstein et al. 1993) + critério de convergência
de Kantz & Schreiber 2004 para a região de ajuste linear da curva de
divergência (automatizado, não escolhido visualmente).

`I(X)`: `lambda_1` (inclinação da região linear de `<ln d_j(i)>`,
primário) + dimensão de correlação `D2` (Grassberger & Procaccia 1983,
companheiro/diagnóstico).

**2 domínios novos verificados por download real:** (a) Kilauea 2018,
início explosivo do dia 17/05 (distinto da transição de 3-4/05 já
pré-selecionada — mas nunca tocada — pelo RQA) — salto real de ~100x na
envoltória RMS de 1 minuto, batendo com o horário documentado pelo
USGS/HVO; (b) MIT-BIH Atrial Fibrillation Database (`afdb`, novo
subbanco do PhysioNet), registro `04936` — salto real de 4,6x no CV do
intervalo RR exatamente na fronteira anotada por cardiologista.

**Risco de identificabilidade central, concreto e não-hipotético:** LLE
reusa o MESMO gatilho de FNN que já travou o `RQA` estruturalmente (nunca
converge abaixo de 1% para ruído branco/fGn com `H<0,3`, confirmado em 5
seeds). Pior que o `RQA`: o ajuste bruto de Rosenstein NÃO falha de forma
limpa em ruído — ainda retorna um número espúrio e documentado
(Provenzale, Smith, Vio & Murante 1992), então o gate de FNN precisa ser
um REJEITE pré-registrado e obrigatório (nunca um `m` padrão forçado), ou
o candidato arrisca fabricar uma "detecção" falsa que escapa do IAAFT —
um modo de falha estritamente pior que o `NOT_COMPUTABLE` honesto do RQA.
**Validação sintética de duas etapas (o mesmo redesenho que o RQA já
correu — ruído branco/fGn no PRE, mapa logístico depois sistema de
Rössler no POST) é OBRIGATÓRIA antes de qualquer dado real.** Riscos
adicionais nomeados: co-variação direcional (não identidade) com
`%DET`(RQA) via Trulla et al. 1996; parentesco formal mais fraco com
`H_S`(entropia de permutação) via o teorema de Pesin (KS-entropia = soma
dos expoentes de Lyapunov positivos).

## 3. Decomposição em Modos Dinâmicos / espectro de Koopman (DMD) — `viable: true`, com canal primário revisado

`R_lambda`: embedding de Hankel (atraso temporal) + truncamento de posto
ótimo de Gavish & Donoho 2014 (regra de threshold automática, sem
sintonia humana) — um dos `R_lambda` mais bem fundamentados desta
rodada.

`I(X)` **teve que ser revisado durante a própria investigação, não após
dado real** (mesmo espírito do EVT/Hill trocando IAAFT por randomização
ANTES de qualquer cálculo): o canal originalmente proposto (taxa de
crescimento/decaimento do autovalor de Koopman dominante) foi encontrado
como **matematicamente idêntico** ao AC1/variância do `critical-slowing-
down` (já fechado negativo) — não apenas conceitualmente parecido, mas
provado por 2 artigos independentes de 2025-2026 (Koopman early-warning-
signals, arXiv:2608.14716, validado em dado real de blackout de rede
elétrica de 1996; e uma segunda prova de identidade algébrica direta,
arXiv:2508.19655/*Nonlinear Dynamics*). **Canal primário revisado**:
frequência e razão de amortecimento do par de autovalores complexos
conjugados menos amortecido — alvo de bifurcações OSCILATÓRIAS
(Hopf/Neimark-Sacker), uma classe que a literatura de CSD documenta
explicitamente como um ponto cego estrutural do AC1/variância escalar
(arXiv:2605.28260). Canal real (autovalor único) REBAIXADO a
diagnóstico-only a priori, com as citações de redundância documentadas
ANTES de qualquer cálculo — mesmo padrão de `kappa`(Kramers-Moyal) e
`d_B`(grafo de visibilidade).

**2 domínios novos verificados por download real:** (a) Itália, primeira
onda de COVID-19, lockdown nacional de 09/03/2020 (JHU CSSE, contagem
cumulativa real de casos); (b) Kilauea 2018, sismicidade contínua de
2018-05-03 (IRIS FDSN, estação `BYL`, forma de onda real decodificada via
ObsPy).

**Risco de identificabilidade adicional, honesto:** compartilha
ancestralidade de embedding (Hankel/Takens) com `RQA` e `homologia
persistente`, ambos fechados na etapa de validação — checagem de
controle positivo (oscilador com bifurcação de Hopf ajustável) deve ser
rodada ANTES de qualquer dado real, mesmo padrão já usado para embeddings
nesta linha. Terceiro achado: `kappa`(Kramers-Moyal), o autovalor real
demovido deste candidato, e o AC1/variância do CSD formam um cluster de
3 vias todas equivalentes à mesma taxa de decaimento — nomeado
explicitamente porque a instrução pedia checagem contra TODOS os 11, não
só o óbvio.

## 4. Largura do espectro multifractal (MF-DFA) — `viable: false`

Investigado como estatística de ORDEM SUPERIOR (largura `Delta h` do
espectro de singularidade, não o expoente único `h(2)`) sobre o mesmo
formalismo de escala já usado por DFA e wavelet. **Fecha por
identificabilidade, não por dado indisponível ou `R_lambda`/`I(X)` fracos
— na verdade os mais fortes desta rodada:** `Delta h`(MF-DFA) e
`ΔC2`(wavelet, candidato #2, já fechado negativo) são duas
ESTATÍSTICAS DIFERENTES DA MESMA CURVA `tau(q)`/`h(q)` subjacente — uma
relação padrão de livro-texto na literatura de formalismo multifractal
(Wendt, Abry & Jaffard 2007; Wendt, Roux, Jaffard & Abry 2009: `Delta
alpha ∝ sqrt(-c2)`), não uma correlação meramente empírica. O próprio
`RESULTS_SUMMARY.md` do wavelet já nomeia `ΔC2` como "a estatística que
de fato indica mudança de estrutura multifractal" — e essa estatística
já falhou adversarialmente (inverteu sinal sob winsorização de 1%,
explodiu 6,5x sob truncamento de janela). Um risco estrutural adicional,
independente, foi encontrado na própria literatura de MF-DFA: `Delta
h≠0` surge espuriamente de comprimento finito de série combinado com
persistência de longo alcance, mesmo para um processo genuinamente
monofractal (Grech & Pamula). 2 domínios novos foram verificados por
download real mesmo assim (MIT-BIH `afdb` registro `08215`; Bitcoin,
crash de 10-11/10/2025) e ficam como infraestrutura reaproveitável para
um candidato futuro genuinamente distinto.

## 5. EMD / Transformada de Hilbert-Huang (HHT) — `viable: false`

Investigado como decomposição adaptativa não-linear (Modos Intrínsecos)
alternativa ao wavelet linear de base fixa já testado. **Fecha por
identificabilidade, mesmo padrão do MF-DFA:** as duas operacionalizações
mais naturais de "distribuição de energia/frequência instantânea entre
IMFs" são PROVADAS equivalentes, por 2 grupos de pesquisa independentes
(Flandrin, Rilling & Gonçalves 2004 — EMD é um banco de filtros diádico
adaptativo com propriedades de escala compartilhadas com wavelet-MRA; e
o próprio grupo de Huang, Wu & Huang 2004, confirma de forma
independente) — o EMD reduz-se estruturalmente à mesma quantidade Hurst-
like já testada 2x negativa nesta linha (DFA, wavelet), e possivelmente
uma 3a via, via o parentesco de `H_S`(entropia de permutação) com Hurst
já documentado por Zunino et al. A única rota de escape encontrada
(`NDD`, grau de modulação de frequência intra-onda, Wang, Wang & Zhang
2012) tem base de literatura fina demais para o padrão desta linha (1
artigo de revista menor, validado só em modelo sintético de alto-falante,
nunca testado contra substitutos IAAFT). 2 domínios novos foram
verificados por download real mesmo assim (SCADA de turbina eólica
Kelmarsh, com falha mecânica real datada; extensão de gelo marinho
ártico, mínimo recorde de 2007 via NSIDC) e ficam como infraestrutura
reaproveitável.

## Ranking honesto (não travado — decisão de qual perseguir fica com o usuário)

1. **Complexidade de Lempel-Ziv** — `R_lambda` mais simples e livre de
   parâmetro de toda a linha (sem embedding, evitando estruturalmente o
   modo de falha que já matou/quase matou 2 dos últimos 3 candidatos
   baseados em embedding), risco de identificabilidade real mas com
   contra-evidência empírica concreta de não-redundância em dado real já
   publicado, e um teste de discriminador (IAAFT vs. LZC) genuinamente
   nunca tentado na literatura. Fraqueza: nenhum segundo canal
   discriminador tipo `C_JS`.
2. **Maior expoente de Lyapunov** — matematicamente o mais distinto dos
   3 (taxa de divergência exponencial, não densidade de recorrência nem
   estatística de persistência), 2 domínios fortes e genuinamente novos,
   mas herda o MESMO risco de não-convergência de FNN que já fechou o
   RQA na validação — e falha de forma pior (número espúrio, não
   `NOT_COMPUTABLE` limpo) se o gate não for pré-registrado como
   obrigatório. Validação sintética de 2 etapas é inegociável antes de
   qualquer dado real.
3. **DMD / espectro de Koopman** — `R_lambda` muito bem fundamentado,
   mas o canal mais natural e citável foi encontrado, DURANTE esta
   própria investigação, matematicamente idêntico ao `critical-slowing-
   down` já fechado (confirmado em dado real de blackout por um grupo
   independente) — o canal de escape (frequência/amortecimento
   complexo) tem precedente de engenharia real mas nunca foi testado
   para este propósito específico de detecção cross-domain, e o
   candidato herda o mesmo risco de embedding do RQA/TDA.

Nenhum candidato foi travado. `DISC-TRI-RG-001` permanece
`CANDIDATE_FORMULATING`. Toda a infraestrutura desta busca (domínios
verificados, achados de identificabilidade, e os 2 candidatos `viable:
false` com sua infraestrutura de domínio reaproveitável) fica commitada
e disponível para retomada futura.
