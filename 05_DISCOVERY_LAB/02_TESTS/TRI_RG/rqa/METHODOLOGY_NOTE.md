# Nota de metodologia — fechamento dos gaps de `RQA` (Análise de Quantificação de Recorrência)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (rolamento IMS/Rexnord run-to-failure, sismologia vulcânica
de Kīlauea 2018). Mesmo espírito de disciplina já usado para os 6
candidatos anteriores desta linha (`critical-slowing-down`,
`wavelet-multiresolution-scaling`, `dfa-multiscale-entropy`,
`soc-avalanches`, `mse-multiscale-entropy`, `grafo-de-visibilidade`).

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`
(candidato 4) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #4 (último) entre os 4 novos candidatos — única
vantagem real: regras de seleção de parâmetro NÃO-arbitrárias e
publicadas (nenhum outro candidato desta linha teve isso). Mas com um
**sinal de alerta empírico já observado na própria sondagem exploratória**,
mais concreto que um risco puramente teórico: a mesma fórmula, mesma
convenção, aplicada informalmente aos 2 domínios (1 segmento por
condição, sem rigor) produziu comportamento DOMAIN-INCONSISTENTE — sinal
direcionalmente robusto no vulcão (9/9 combinações de parâmetro),
ausente/instável no rolamento (7/9 positivo mas magnitudes ínfimas, sinal
invertido em 2/9) — o MESMO padrão de falha que já derrubou
`critical-slowing-down` (achado em 1 de 3 domínios, direção oposta nos
outros).

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.5, sondagem exploratória própria não pré-
registrada): 2 domínios novos reais com dado baixado/inspecionado — (a)
engenharia mecânica (rolamento IMS/Rexnord run-to-failure, NASA PCoE, 984
arquivos reais, falha de pista externa documentada pelo próprio dataset);
(b) sismologia vulcânica (Kīlauea 2018, IRIS/EarthScope, abertura de
fissura + terremoto M6,9 de 04/05/2018 documentados pelo USGS/HVO).
Sondagem informal (1 segmento por condição, parâmetros não travados)
sugeriu sinal no vulcão mas não no rolamento — precisamente o padrão que
precisa ser testado com rigor, não assumido. Faltam: (a) regras exatas e
travadas de `m` (dimensão de embedding), `tau` (atraso), `epsilon`
(limiar de recorrência); (b) declaração de identificabilidade; (c) regra
de PRE/POST; (d) regra de subamostragem para custo O(N²); (e) protocolo
de significância.

## Gap (a): reconstrução do espaço de fase (`R_lambda`) — regras de parâmetro NÃO-arbitrárias

**Embedding de Takens:** `y_i = (x_i, x_{i+tau}, x_{i+2*tau}, ..., x_{i+(m-1)*tau})`.

**Atraso `tau`:** primeiro mínimo local da informação mútua média
time-delayed (Fraser & Swinney 1986, *Phys. Rev. A* 33:1134) — histograma
de 16 bins (convenção padrão da literatura), varredura de `lag=1` até
`lag=min(200, floor(N/10))`. Se nenhum mínimo local for encontrado nessa
faixa, usa-se o PRIMEIRO CRUZAMENTO POR ZERO da autocorrelação linear
como fallback documentado (convenção padrão quando a MI é monótona
decrescente sem mínimo, ex. processos muito curtos) — decisão fixada a
priori, não escolhida depois de ver qual domínio precisa do fallback.

**Dimensão de embedding `m`:** falsos vizinhos mais próximos (FNN, Kennel,
Brown & Abarbanel 1992, *Phys. Rev. A* 45:3403) com os parâmetros
originais do artigo: `R_tol=10`, `A_tol=2`. Varre `m=1` até `m=10`
(teto a priori, faixa padrão para séries geofísicas/mecânicas), para no
primeiro `m` cuja fração de falsos vizinhos cai abaixo de `1%`. Se nenhum
`m<=10` atingir esse limiar, o domínio é REJEITADO por embedding não
resolvido — declarado honestamente, não forçado a um `m` arbitrário.

**Convenção para comparação justa PRE vs. POST (decisão explícita,
evita confundir "dinâmica mudou" com "embedding escolhido mudou"):** `m`
e `tau` são estimados UMA VEZ a partir do segmento PRE (linha de base) de
cada domínio/variante, e os MESMOS `(m,tau)` são aplicados ao POST
correspondente — nunca reestimados separadamente por condição.

**Limiar de recorrência `epsilon`:** taxa de recorrência fixa (RR,
Marwan et al. 2007, *Physics Reports* 438:237) — `RR_target=0,05` (5%,
convenção padrão da literatura de RQA), `epsilon` calculado
independentemente para CADA condição (PRE, POST, e cada substituto) de
modo que a matriz de recorrência daquela condição específica atinja
`RR_target` — isso é uma normalização de limiar, não um parâmetro
dinâmico estimado, portanto reestimar por condição não introduz o mesmo
viés que reestimar `(m,tau)` separadamente introduziria.

**Métrica de distância:** norma de Chebyshev (máximo), convenção padrão
da literatura de RQA (Marwan et al. 2007).

**Janela de Theiler:** `w=tau` (exclui da contagem de recorrência os
pares de pontos cuja proximidade temporal, não dinâmica, os tornaria
trivialmente "recorrentes" — convenção padrão, evita inflar `%DET`/`%LAM`
por autocorrelação de curto alcance).

## Gap (b): `I(X)` e declaração de identificabilidade

**`I(X)` primário:** `%DET` (determinismo) — fração de pontos
recorrentes que pertencem a linhas diagonais de comprimento `>=l_min=2`:
`DET = sum_{l>=l_min} l*P(l) / sum_l l*P(l)`, onde `P(l)` é o histograma
de comprimentos de linha diagonal (Marwan et al. 2007, fórmula original).

**`I(X)` secundário (canal companheiro):** `ENTR` (entropia de Shannon
da distribuição `P(l)` de comprimentos de linha diagonal) — informação
distinta de `%DET` por construção (mede a DIVERSIDADE de estrutura
determinística, não só sua fração total; um sistema pode ter `%DET` alto
com poucas linhas muito longas, `ENTR` baixa, ou `%DET` similar com
muitas linhas curtas variadas, `ENTR` alta).

**Declaração de identificabilidade — dois riscos distintos, ambos
nomeados explicitamente:**

1. **Risco espectral/linear (mecanismo já conhecido na literatura de
   RQA, Zbilut & Webber):** `%DET`/`ENTR` respondem a QUALQUER estrutura
   de correlação temporal, incluindo processos lineares Gaussianos
   autocorrelacionados (AR/fGn) — não é automaticamente evidência de
   determinismo não-linear genuíno. Discriminador, mesma lógica já usada
   com sucesso em `mse-multiscale-entropy` e `grafo-de-visibilidade`:
   substituto IAAFT como teste PRIMÁRIO de significância — preserva o
   espectro linear de cada série, mas destrói qualquer estrutura de
   recorrência determinística genuína que vá além disso. **Validação
   obrigatória de PODER, ANTES de qualquer dado real** (mesma exigência
   já usada em MSE/VG): controle positivo sintético — PRE = ruído branco
   Gaussiano; POST = mapa logístico caótico (`r=4`) com marginal e
   espectro casados por remapeamento de posto — verificar que
   `%DET`/`ENTR` reais caem fora da distribuição nula IAAFT.
2. **Risco de inconsistência cross-domain (o risco CENTRAL e já
   OBSERVADO empiricamente nesta candidatura específica, não hipotético):**
   a sondagem exploratória informal já sugeriu sinal robusto num domínio
   (vulcão) e ausente/instável no outro (rolamento) — o mesmo padrão de
   falha que já derrubou `critical-slowing-down`. Este pré-registro NÃO
   assume que esse padrão vai se repetir sob rigor completo (parâmetros
   travados, protocolo IAAFT, variantes de robustez) — mas é o resultado
   mais honesto a esperar e reportar caso se confirme, não uma surpresa a
   ser escondida.

**Se a validação repetir o padrão de baixo poder já visto em DFA-alpha:**
adicionar teste complementar de bootstrap por blocos móveis (Kunsch
1989) como PRIMÁRIO, mesma correção já aplicada 2x nesta linha (DFA,
SOC), ANTES de tocar dado real. **Se a validação repetir o padrão de
`grafo-de-visibilidade` (canal estruturalmente não computável, não um
problema de poder):** documentar honestamente e decidir ANTES de dado
real se algum canal precisa ser retirado do critério, sem forçar.

## Gap (c): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada 5x nesta linha — CSD, DFA, SOC, MSE, VG): PRE (primária) = todo o
registro contínuo disponível anterior à transição documentada; PRE
(robustez) = os 50% mais recentes (por CONTAGEM de amostras) desse PRE.
POST (primária) = todo o registro contínuo disponível posterior à
transição, até o próximo evento/confundidor documentado; POST (robustez)
= os 50% mais próximos da transição desse POST.

- **Engenharia mecânica (rolamento IMS/Rexnord):** transição = primeiro
  instante de falha de pista externa documentado pelo próprio dataset
  (Qiu et al. 2006, NASA PCoE, critério do experimento original, externo
  a qualquer cálculo de RQA). PRE = dado disponível antes desse instante;
  POST = dado disponível depois, até o fim do registro.
- **Sismologia vulcânica (Kīlauea 2018):** transição = início da
  sequência eruptiva de 03/05/2018 (abertura de fissura na Lower East
  Rift Zone, documentado pelo USGS/HVO) até o terremoto M6,9 de
  04/05/2018 (colapso da caldeira). PRE = tremor de fundo pré-erupção
  disponível. POST = sequência eruptiva + sismicidade associada até o
  final do registro contínuo disponível da estação usada.

## Gap (d): regra de subamostragem para custo O(N²) — declarada a priori para TODOS os domínios

Construção da matriz de recorrência é O(N²) por segmento (mesmo custo
estrutural já enfrentado por `grafo-de-visibilidade`). **Reaproveitado
sem modificação:** `MAX_N_PER_SEGMENT=5000` amostras, decimação por
*stride* uniforme se excedido, aplicada IGUALMENTE aos 2 domínios desta
rodada, decidida antes de saber se algum segmento realmente excede o
limite.

## Gap (e): protocolo de significância — IAAFT como teste PRIMÁRIO

Mesmo protocolo já usado com sucesso em MSE/VG: `N_SURROGATES=200`,
`N_IAAFT_ITER=50`, substitutos de PRE e POST gerados INDEPENDENTEMENTE
cada um da sua própria série real, `seed=12345`. Teste BICAUDAL. Cada
substituto passa pela MESMA pipeline completa (embedding com `(m,tau)`
JÁ FIXADO da série real correspondente — não reestimado por substituto,
já que `(m,tau)` é propriedade da série original que o substituto tenta
imitar; `epsilon` recalculado por substituto via `RR_target` fixo). `p =
fração de substitutos com |Delta_DET_substituto| >= |Delta_DET_real|`
(e igualmente para `Delta_ENTR`).

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado (mesmo padrão já usado nos 6 candidatos anteriores desta
linha de fechamento exploratório de gaps). A metodologia acima foi
fixada ANTES de qualquer cálculo, precisamente para que o padrão de
inconsistência cross-domain já sugerido pela sondagem informal — se
confirmado sob rigor completo — seja reportado como o resultado honesto
que é, não uma falha a esconder nem uma surpresa.
