# Nota de metodologia — `largest_lyapunov_exponent` (Maior Expoente de Lyapunov, algoritmo de Rosenstein)

**Status: decisões metodológicas fixadas ANTES de qualquer cálculo real nos
2 domínios (Kīlauea 2018, início explosivo de 17/05; MIT-BIH Atrial
Fibrillation Database, registro `04936`).** Mesmo espírito de disciplina já
usado para os 7 candidatos anteriores desta linha, e em particular mesmo
padrão de validação sintética obrigatória, PRÉ-real-data, já usado por `RQA`
(`02_TESTS/TRI_RG/rqa/METHODOLOGY_NOTE.md`) — que este candidato reproduz
quase literalmente porque herda o mesmo risco estrutural de embedding.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md`
seção 2 para o levantamento que identificou este candidato como `viable=true`
— ranqueado #2 de 3 candidatos novos, com uma exigência explícita de gate de
validação obrigatório ANTES de qualquer dado real, dado o precedente concreto
e já observado (não hipotético) de `RQA`.

## Contexto herdado de `RQA` — por que este candidato tem um gate mais rígido que qualquer outro desta linha

`RQA` (candidato #7, `02_TESTS/TRI_RG/rqa/`) usa a MESMA maquinaria de
embedding (Falsos Vizinhos Mais Próximos/FNN de Kennel, Brown & Abarbanel
1992 para `m`; informação mútua de Fraser & Swinney 1986 para `tau`) que este
candidato também usa. A própria validação sintética de `RQA`
(`rqa/VALIDATION_NOTE.md`) encontrou, de forma robusta e confirmada (5
sementes, ambas as marginais Gaussiana e uniforme, `N=2.000` e `N=5.000`,
imune ao fallback de bootstrap por blocos móveis pré-autorizado): **o gate de
FNN estruturalmente NUNCA converge abaixo de 1% de fração de falsos vizinhos
para `m<=10`** em ruído branco puro, AR(1) com `phi<0,95`, ou ruído
Gaussiano fracionário (fGn) com `H<0,3`. `RQA` foi fechado NA ETAPA DE
VALIDAÇÃO — dado real nunca tocado — após DUAS tentativas de controle
positivo (mapa logístico, depois sistema de Rössler), nenhuma estabelecendo
poder real do IAAFT.

**Este candidato herda esse risco integralmente** (mesmo código de FNN/MI,
reaproveitado — não reimplementado — de `rqa/analysis/rqa_common.py`) — mas
com um modo de falha **pior**, documentado explicitamente na literatura
(Provenzale, Smith, Vio & Murante 1992, *Physica D* 58:31, "Distinguishing
between low-dimensional dynamics and randomness in measured time series"):
ao contrário de `%DET`/`ENTR` do RQA (que simplesmente não são computáveis —
`NOT_COMPUTABLE` — quando FNN não converge), o ajuste bruto de inclinação de
Rosenstein da curva de divergência **não falha de forma limpa em ruído** —
ele retorna um número espúrio, plausível, e sem aviso, mesmo quando o
embedding subjacente é dinamicamente sem sentido.

## REGRA OBRIGATÓRIA, NÃO-NEGOCIÁVEL — gate de FNN como REJEITE forçado

> **Se FNN não convergir abaixo do limiar de 1% para nenhum `m<=10`, a
> pipeline DEVE retornar `status: NOT_COMPUTABLE` (especificamente
> `embedding_not_resolved`) para aquele segmento, e NÃO PODE cair de volta
> para um `m` padrão/forçado.** Esta regra é idêntica em espírito à de `RQA`
> Gap (a), mas aqui é ainda mais crítica: um `lambda_1` calculado
> silenciosamente sobre um embedding não resolvido seria um modo de falha
> estritamente PIOR que o `NOT_COMPUTABLE` honesto do RQA, porque poderia
> produzir uma "detecção" de mudança falsa-positiva que sobrevive ao IAAFT
> sem que ninguém perceba que o embedding nunca foi de fato estabelecido.
> Esta regra é implementada em código (`analysis/lle_common.py`,
> `run_lle_analysis`) como um `return` explícito antes de qualquer cálculo de
> `lambda_1`/`D2` — nunca como um aviso posterior ignorável.

## `R_lambda` — embedding e estimação do expoente de Lyapunov

**Atraso `tau`:** primeiro mínimo local da informação mútua time-delayed
(Fraser & Swinney 1986, *Phys. Rev. A* 33:1134) — **reaproveitando sem
modificação** `rqa_common.estimate_tau` (16 bins, `lag=1..min(200,
floor(N/10))`, fallback de primeiro cruzamento por zero da autocorrelação
linear se nenhum mínimo local for encontrado). Código idêntico, importado
diretamente de `rqa/analysis/rqa_common.py`, não reimplementado.

**Dimensão de embedding `m`:** Falsos Vizinhos Mais Próximos (Kennel, Brown
& Abarbanel 1992), `R_tol=10`, `A_tol=2`, varredura `m=1..10`, parada no
primeiro `m` cuja fração de falsos vizinhos cai abaixo de 1% — **reaproveitando
sem modificação** `rqa_common.estimate_m`/`rqa_common.fnn_fraction`. **HARD
REJECT se nenhum `m<=10` resolver** (ver regra obrigatória acima) —
`status="embedding_not_resolved"`, nenhum `lambda_1`/`D2` calculado, nenhum
fallback forçado.

**Convenção de embedding compartilhado (mesma lógica de `RQA` Gap (a)):**
`m` e `tau` são estimados UMA VEZ a partir do segmento PRE de cada
domínio/variante, e os MESMOS `(m,tau)` são aplicados ao POST correspondente
e a cada substituto de ambos — nunca reestimados por condição. Evita
confundir "dinâmica mudou" com "embedding escolhido mudou".

**Janela de Theiler (convenção DIFERENTE da de `RQA` — decisão explícita,
não conflação):** `RQA` usa `w=tau` (exclui pares temporalmente próximos por
uma heurística simples ligada ao atraso de embedding). Este candidato usa a
convenção ORIGINAL de Rosenstein et al. 1993: **período orbital médio**,
estimado como o recíproco da frequência média do espectro de potência da
série (periodograma via FFT, frequência média ponderada pela potência em
cada frequência positiva, `w = round(1 / f_mean)`). Esta é uma escolha
diferente e deliberada — não um erro de conflação com a convenção do RQA —
porque a janela de Theiler no algoritmo de Rosenstein existe especificamente
para excluir vizinhos que são próximos por causa de estarem na MESMA órbita
(não por proximidade temporal arbitrária ligada a `tau`), e o período
orbital médio é a estimativa canônica dessa escala na literatura de
Rosenstein. **Decisão adicional, fixada a priori:** a janela de Theiler é
calculada INDEPENDENTEMENTE por condição (PRE real, POST real, cada
substituto) — não compartilhada como `(m,tau)` — porque é derivada das
características espectrais daquela série específica, exatamente como o
`epsilon` do RQA é recalculado por condição (normalização, não parâmetro
dinâmico estimado).

**Distância para busca de vizinho mais próximo:** norma Euclidiana no espaço
reconstruído (convenção padrão de Rosenstein et al. 1993 — distinta da
norma de Chebyshev usada pelo RQA para a matriz de recorrência, que é um
objeto matemático diferente).

**Curva de divergência e região de ajuste linear:** para cada ponto de
referência `i` no espaço reconstruído, encontra-se o vizinho mais próximo
`j` (excluindo `|i-j|<=w`, janela de Theiler) e rastreia-se
`d_j(k) = ||Y_{i+k} - Y_{j+k}||` para `k=0..K_max` (`K_max = min(200,
floor(M/2))`, teto a priori análogo ao teto de `lag_max` do RQA). A curva
`<ln d_j(k)>` é a média sobre todos os pontos de referência válidos
(excluindo `d_j(0)=0`). **Região de ajuste automatizada via o critério de
convergência de Kantz & Schreiber (2004, *Nonlinear Time Series Analysis*,
2ª ed.):** a curva de divergência é recomputada em `m*`, `m*+1`, `m*+2`
(onde `m*` é o `m` resolvido por FNN — os dois valores adicionais servem
SÓ para testar a estabilidade da inclinação, não redefinem `m*`). Para cada
janela contígua candidata `[k1,k2]` (comprimento mínimo 5 amostras) dentro
de `[1,K_max]`, ajusta-se a inclinação (regressão linear) da curva em cada
um dos 3 `m`. A janela é declarada "estável" se a mudança relativa de
inclinação entre `m*`→`m*+1` E entre `m*+1`→`m*+2` for ambas `<10%`
(tolerância fixa, pré-declarada). Entre todas as janelas estáveis, escolhe-se
a MAIOR (maior comprimento; empate resolvido pela de início mais cedo). Esta
regra é inteiramente mecânica/automatizável — nenhuma região é escolhida
visualmente. **Se nenhuma janela for estável:** o canal `lambda_1` para
aquele segmento é reportado como `linear_region_not_resolved` — uma falha de
diagnóstico honesta, distinta do `embedding_not_resolved` do gate de FNN
(este ocorre DEPOIS de o embedding ter sido resolvido).

## `I(X)`

**Primário:** `lambda_1` — a inclinação da região linear identificada acima,
computada especificamente em `m=m*` (o `m` auditado pelo gate de FNN; `m*+1`
e `m*+2` servem apenas para CONFIRMAR a estabilidade da região, não para
recalcular o valor reportado). Mesmas unidades (nats por amostra de
`R_lambda`, isto é, por passo de índice da série JÁ processada por cada
domínio — sem renormalização específica de domínio) em todos os domínios.

**Companheiro/diagnóstico:** dimensão de correlação `D2` (Grassberger &
Procaccia 1983, *Phys. Rev. Lett.* 50:346) — integral de correlação `C(r)`
sobre pares `|i-j|>w` (mesma janela de Theiler), com a MESMA regra
automatizada de região de escala (estabilidade de inclinação `<10%` através
de `m*, m*+1, m*+2` consecutivos, aplicada a `log C(r)` vs `log r`) usada
para `lambda_1` — mesmo espírito de regra, aplicada a um objeto matemático
diferente (curva log-log em vez de semi-log).

**Diagnóstico de baixo peso (NÃO um canal de decisão):** `R²` do ajuste
linear da região identificada de `lambda_1` em `m=m*` — sinalizado quando a
curva de divergência não é bem descrita por uma única exponencial, sem
afetar a decisão de significância por si só.

## Riscos de identificabilidade (já documentados, citados, não re-derivados)

1. **Vs. `RQA` (#7):** maquinaria de embedding compartilhada (FNN/MI), risco
   real e concreto de não-computabilidade — endereçado acima via o gate
   obrigatório de FNN. Este é o risco CENTRAL desta candidatura, já
   confirmado empiricamente no contexto do RQA antes mesmo de qualquer
   cálculo deste candidato.
2. **Vs. `%DET`/`ENTR` do RQA:** existe uma co-variação empírica REAL e
   DIRECIONAL (não uma identidade matemática) — Trulla, Giuliani, Zbilut &
   Webber 1996 (*Phys. Lett. A* 223:255) mostram `%DET` rastreando a rota de
   duplicação de período para o caos no mapa logístico, a MESMA cascata de
   bifurcação que o LLE classicamente rastreia. Nomeado explicitamente, não
   escondido.
3. **Vs. `persistent_homology` (#11):** compartilha ancestralidade de
   embedding de Takens, mas é um objeto matemático genuinamente diferente
   (uma TAXA de divergência vs. uma estatística de persistência
   topológica) — nenhuma redundância medida existe ainda (diferente da
   redundância medida r≈0,92 do próprio TDA com o RQA).
4. **Vs. `permutation_entropy`/`H_S` (#8):** risco mais brando e formal, via
   o teorema de Pesin (entropia de Kolmogorov-Sinai = soma dos expoentes de
   Lyapunov positivos, para sistemas bem-comportados) — `H_S` foi
   explicitamente motivada na literatura fundadora como um proxy barato para
   a taxa de entropia KS. Prioridade mais baixa que o risco de embedding do
   RQA, já que `H_S` é limitada/adimensional e `lambda_1` não é.
5. **Vs. `visibility_graph`/`C` (#6):** risco mais estreito — Lacasa & Toral
   2010 (*Phys. Rev. E* 82:036120) ligam o DECAIMENTO DA DISTRIBUIÇÃO DE
   GRAU do grafo de visibilidade horizontal ao expoente de Lyapunov, para
   famílias específicas de mapas caóticos 1-D. O canal real do candidato VG
   foi o coeficiente de clusterização `C`, não o decaimento de grau — risco
   estreito, não direto.
6. **Candidatos restantes (CSD, wavelet, DFA, SOC, MSE, EVT/Hill,
   Kramers-Moyal):** nenhuma relação formal/documentada encontrada, risco
   baixo.

## Validação sintética obrigatória — protocolo (fixado ANTES de qualquer cálculo)

Mesmo desenho de duas etapas já usado por `RQA` (`rqa/VALIDATION_NOTE.md`),
reaproveitando a técnica de remapeamento por posto (rank-remap) já validada
nesta linha:

0. **Diagnóstico de correção de código** (não faz parte da validação de
   identificabilidade em si): trajetória determinística com expoente de
   Lyapunov conhecido (mapa logístico `r=4`, `lambda_1` teórico = `ln(2) ≈
   0,693` nats/iteração) — confirma que o código de embedding + Rosenstein +
   Kantz-Schreiber produz um valor sensato antes de testar em dado
   genuinamente ambíguo.

1. **Controle positivo, tentativa 1 (especificação literal):** PRE = ruído
   branco Gaussiano iid. POST = mapa logístico caótico (`r=4`) remapeado por
   posto sobre o PRE. Verifica se FNN sequer resolve `m<=10` para o PRE —
   dado o precedente do RQA, é esperado (mas testado, não assumido) que
   NÃO resolva.

2. **Controle negativo:** PRE e POST = duas realizações independentes do
   MESMO processo linear (fGn-like, `H=0,7` fixo, sementes independentes) —
   sonda diretamente o risco espectral/linear, exercitando a pipeline
   completa quando o embedding É computável.

3. **Gatilho de correção pré-declarado, ÚNICO e limitado (disciplina de
   escalonamento desta linha):** se o controle positivo da tentativa 1 falhar
   por `embedding_not_resolved` (mesmo modo de falha exato já visto no RQA),
   **redesenhar a fonte do sinal caótico de POST** — do mapa logístico
   (espectro banda-larga/quase-branco) para o **sistema de Rössler**
   (Rössler 1976, *Phys. Lett. A* 57:397; espectro naturalmente
   colorido/banda-limitada, mais compatível com um PRE fGn `H=0,7`) —
   mantendo PRE = fGn-like `H=0,7` (já validado, resolve FNN) e a mesma
   técnica de remapeamento por posto. Esta é uma correção de DESENHO de
   validação (qual processo caótico usar como fonte de POST), não uma
   reformulação de `R_lambda`, `I(X)`, regra de PRE/POST, ou protocolo de
   significância — nenhum desses é alterado. Mesmo protocolo mecânico de
   decisão do RQA:
   - Se `lambda_1` e/ou `D2` mostrarem poder real (`p<0,05` com separação
     clara da nula IAAFT): validação PASSA, segue-se para dado real com a
     pipeline travada, sem modificação.
   - Se NENHUM dos dois canais mostrar poder real sob este segundo desenho:
     candidato `largest_lyapunov_exponent` é FECHADO NA ETAPA DE VALIDAÇÃO,
     sem tocar dado real — resultado honesto e completo, não uma falha.
     **Nenhuma terceira tentativa será feita.**

4. **Caveat adicional, específico deste candidato, nomeado a priori:**
   diferente do RQA (cujos canais `%DET`/`ENTR` dependem de contagens de
   recorrência relativas, mais tolerantes a distorções de amplitude), o
   Rosenstein LLE depende da GEOMETRIA de distância exata no espaço
   reconstruído — o remapeamento por posto, sendo uma transformação
   monótona não-linear da amplitude, pode distorcer a geometria local do
   atrator reconstruído de forma mais severa para `lambda_1`/`D2` do que
   distorceu para `%DET`/`ENTR` do RQA. Isso é nomeado aqui como um risco
   adicional a ser reportado honestamente se observado — não uma razão para
   alterar o desenho de validação antes de rodá-lo (o desenho continua
   sendo o mesmo já auditado nesta linha).

## Convenção de PRE/POST (regra domain-agnostic, reaproveitada sem modificação)

Mesma convenção já usada 6x nesta linha (CSD, DFA, SOC, MSE, VG, RQA): PRE
(primária) = todo o registro contínuo disponível antes da transição
documentada; PRE (robustez) = os 50% mais recentes (por contagem de
amostras) desse PRE. POST (primária) = todo o registro contínuo disponível
depois da transição, até o próximo evento/confundidor documentado; POST
(robustez) = os 50% mais próximos da transição desse POST.

- **Kīlauea 2018, início explosivo de 17/05 (Neal et al. 2019, *Science*
  363:367):** transição = ~4:15 da manhã HST = 14:15 UTC, 17/05/2018 (início
  da atividade explosiva documentada pelo USGS/HVO). Estação `HV.RIMD..HHZ`
  (100Hz) via IRIS FDSN dataselect, ou estação HV próxima se `RIMD` não
  estiver disponível para a janela necessária. **Distinção explícita de
  transparência (instrução explícita da tarefa):** esta é uma transição
  DIFERENTE e NÃO-SOBREPOSTA daquela pré-selecionada (mas nunca calculada —
  `RQA` nunca tocou dado real) pelo `RQA/METHODOLOGY_NOTE.md` (abertura de
  fissura de 03/05/2018 + terremoto M6,9 de 04/05/2018, colapso de caldeira).
  Não há conflito real de dado (RQA nunca calculou nada), mas a distinção é
  nomeada aqui por transparência, conforme instruído. PRE = tremor de fundo
  disponível antes de 14:15 UTC de 17/05; POST = sequência explosiva e
  sismicidade associada depois, até o final do registro contínuo disponível
  da estação usada ou até o próximo evento documentado.
- **MIT-BIH Atrial Fibrillation Database (`afdb`), registro `04936`:**
  2 canais de ECG a 250Hz, ~9,2M amostras (~10,2h), anotações de ritmo
  revisadas por cardiologista. Trabalho sobre o tacograma de intervalos RR
  derivado (representação padrão para análise não-linear de VFC nesta linha,
  consistente com como DFA/MSE/entropia de permutação trataram o Apneia-ECG).
  Transição = primeira ocorrência documentada `(N -> (AFIB`, amostra 413.691
  (t=1654,76s). PRE = tacograma RR disponível antes dessa amostra; POST =
  tacograma RR disponível depois, até a próxima transição de ritmo anotada
  (evitando misturar múltiplos episódios de FA/ritmo normal no mesmo
  segmento).

## Regra de subamostragem para custo O(N²) (D2) / O(N log N) (Rosenstein via KD-tree)

`MAX_N_PER_SEGMENT=5000` amostras, decimação por *stride* uniforme se
excedido — mesmo teto já usado por `RQA`/`grafo-de-visibilidade`, aplicado
igualmente a todos os domínios, decidido antes de saber se algum segmento
excede o limite. A busca de vizinho mais próximo do Rosenstein usa
`cKDTree` (O(N log N)); a integral de correlação de `D2` é O(N²) por par de
raios e é o motivo principal do teto.

## Protocolo de significância — IAAFT como teste PRIMÁRIO

Mesmo protocolo já usado nesta linha: `N_SURROGATES=200`, `N_IAAFT_ITER=50`,
substitutos de PRE e POST gerados INDEPENDENTEMENTE cada um da sua própria
série real, `seed=12345`. Teste BICAUDAL. Cada substituto passa pela MESMA
pipeline completa (embedding com `(m,tau)` JÁ FIXADO da série real
correspondente — não reestimado por substituto; janela de Theiler
recalculada por substituto, análoga ao `epsilon` do RQA). `p = fração de
substitutos com |Delta_lambda1_substituto| >= |Delta_lambda1_real|` (e
igualmente para `Delta_D2`).

**Fallback pré-autorizado (não usado a menos que a validação mostre o
mesmo padrão de baixo poder já visto em DFA-alpha, não o padrão de
não-computabilidade estrutural já visto no RQA):** bootstrap por blocos
móveis (Kunsch 1989), mesma máquina reaproveitada de `rqa_common.py`
(`moving_block_bootstrap_resample`, `run_block_bootstrap_test`), comprimento
de bloco ligado à escala temporal do embedding (`L=max(2*tau,10)`).

## Disciplina de escalonamento (aplicável a esta linha inteira, reafirmada aqui)

Um ÚNICO passo de correção pré-declarado é autorizado se a validação revelar
um problema genuíno de desenho (não uma reformulação de hipótese) — já
especificado acima (troca de mapa logístico para Rössler no controle
positivo, mantendo `R_lambda`/`I(X)`/regras de PRE-POST/protocolo de
significância intactos). Depois disso, o candidato DEVE ser fechado,
positivo ou negativo, honestamente. Nenhuma sintonia aberta.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md` é
escrito para esta linha (mesmo padrão já usado nos 12 candidatos anteriores
— este é o 13º candidato identificado nesta linha ao todo, 2º dos 3
genuinamente novos encontrados na sondagem da Fase 0.7 de 2026-08-20).
A metodologia acima foi fixada ANTES de qualquer cálculo real, precisamente
para que o resultado da validação sintética obrigatória — seja ele um
fechamento na validação (como `RQA`) ou uma passagem para dado real — seja
reportado como o resultado honesto que é.
