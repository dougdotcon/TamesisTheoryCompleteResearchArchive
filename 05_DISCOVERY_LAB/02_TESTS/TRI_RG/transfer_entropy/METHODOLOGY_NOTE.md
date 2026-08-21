# Nota de metodologia — `transfer_entropy` (Transferência de Entropia / fluxo de informação direcionado)

**Status: decisões metodológicas fixadas ANTES de qualquer cálculo real nos
2 domínios (CHB-MIT EEG multi-eletrodo, `chb01_03.edf`; par de terremotos
de Kahramanmaraş, Turquia, 06/02/2023).** Mesmo espírito de disciplina já
usado para os 14 candidatos anteriores desta linha, incluindo o mesmo
padrão de validação sintética obrigatória, PRÉ-dado-real, com gate
explícito de correção única e limitada (`largest_lyapunov_exponent`,
`rqa`).

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md`
seção 2 para o levantamento que identificou este candidato como
`viable: true` — ranqueado #1 de 2 candidatos novos da Fase 0.8, primeira
candidatura genuinamente BIVARIADA/DIRECIONAL de toda a linha (os 14
candidatos anteriores são todos estatísticas univariadas de um único
canal).

## O que este candidato testa, precisamente

Não uma estatística de UM canal observado, mas o FLUXO DE INFORMAÇÃO
DIRIGIDO entre DOIS canais gravados SIMULTANEAMENTE do mesmo sistema
físico — mudou o acoplamento direcional entre subsistemas ao redor de uma
transição documentada externamente? Isto exige dado genuinamente
multivariado sincronizado (não um canal partido em duas metades), o que
foi verificado por download real nos dois domínios abaixo antes de
qualquer cálculo.

## `R_lambda` — embedding de história própria e estimador

### Atraso `tau` por canal

Reaproveitado SEM modificação de `rqa/analysis/rqa_common.py::estimate_tau`
(primeiro mínimo local da informação mútua time-delayed, Fraser & Swinney
1986, 16 bins, `lag=1..min(200,floor(N/10))`; fallback de primeiro
cruzamento por zero da autocorrelação linear). **Fallback adicional,
declarado a priori e específico deste candidato:** se `estimate_tau`
retornar `tau_not_resolved` para um canal, usa-se `tau=1` para aquele
canal — decisão diferente da adotada por RQA/LLE (que travam
`embedding_not_resolved` e recusam o cálculo), justificada porque a
embedding de história própria para TE (Frenzel & Pompe 2007) é
estruturalmente mais tolerante que a reconstrução de atrator completo de
Takens: o objetivo aqui é só capturar memória de curto prazo suficiente
para condicionar a predição local, não reconstruir um atrator
topologicamente fiel — `tau=1` é a convenção padrão de várias
implementações de TE na literatura (p.ex. TRENTOOL/IDTxl usam `tau=1`
como padrão quando não há sinal claro de periodicidade). Isto é reportado
explicitamente (`tau_method: "mi_local_minimum"` ou
`"fallback_tau_1"`) — nunca escondido.

### Dimensão de embedding `m` por canal — Ragwitz & Kantz 2002

Critério de minimização de erro de predição local (Ragwitz & Kantz 2002,
*Phys. Rev. E* 65:056201) — **estruturalmente diferente do limiar de
percentual de FNN que travou `rqa`/`largest_lyapunov_exponent` na
validação**: para `tau` já fixado acima, varre-se `m=1..M_MAX=10`; para
cada `m`, constrói-se o vetor de atraso `X_i=(x_i,x_{i-tau},...,
x_{i-(m-1)tau})`, prediz-se `x_{i+1}` pela média dos valores seguintes dos
`k_NN=4` vizinhos mais próximos (norma Euclidiana, excluindo o próprio
ponto) de `X_i`, e calcula-se o erro quadrático médio normalizado pela
variância da série, `e(m) = <(x_{i+1}-hat{x}_{i+1})^2>/sigma_x^2`.
Escolhe-se `m* = argmin_m e(m)`. **Diferença estrutural favorável,
identificável a priori:** este critério é uma MINIMIZAÇÃO sobre uma grade
finita — sempre produz um argmin, não tem modo de falha de
"nunca-converge-abaixo-do-limiar" que caracterizou o FNN nesta linha.
Isto é uma expectativa a priori, verificada empiricamente na validação
sintética (não assumida).

**Convenção de reuso, idêntica em espírito à de RQA/LLE:** `(m,tau)` de
cada canal são estimados UMA VEZ a partir do segmento PRE real (após
subamostragem, ver Gap de custo computacional abaixo) daquele canal
específico, e os MESMOS valores são reaplicados ao POST e a TODOS os
substitutos (IAAFT e deslocamento circular) e a TODAS as subjanelas de
ambas as condições — nunca reestimados por subjanela/substituto/condição.
Evita confundir "acoplamento mudou" com "embedding escolhido mudou".

### Simplificação deliberada: sem janela de Theiler explícita no estimador KSG/Ragwitz-Kantz

Diferente de LLE (que usa período orbital médio) e RQA (que usa `w=tau`),
este candidato NÃO impõe exclusão de vizinhos temporalmente próximos além
da exclusão trivial do próprio ponto. Isto é uma escolha deliberada, não
um descuido: (a) reduz superfície de bug em um estimador já
estruturalmente mais complexo (CMI multivariado, não uma estatística
escalar) — risco explicitamente nomeado no levantamento da Fase 0.8 e nas
instruções desta etapa como prioridade ("implementar cuidadosamente e
validar contra caso analítico conhecido... para evitar o tipo de risco de
bug de implementação que quase descarrilou `kramers_moyal`"); (b) é a
convenção padrão em implementações de referência amplamente citadas de
TE via KSG (Frenzel & Pompe 2007 não impõem correção de Theiler explícita
na formulação original; JIDT/TRENTOOL não aplicam uma por padrão); (c) a
robustez contra estrutura serial espúria vem, neste desenho, do par de
nulos substitutos (IAAFT + deslocamento circular, ver abaixo), que é um
diagnóstico mais direto e mais específico ao risco real (acoplamento
espúrio de curto prazo) do que uma janela de Theiler genérica. Se a
validação sintética revelar viés sistemático ligado a este risco
especificamente, isso será reportado honestamente (ver Gap de validação).

### Estimador de TE — KSG-CMI (Kraskov-Stögbauer-Grassberger 2004, estendido por Frenzel & Pompe 2007)

Implementação própria desta linha (nenhuma biblioteca mantida disponível
neste ambiente — IDTxl não está no índice PyPI acessível pelo proxy desta
sessão, JIDT requer JVM/`jpype` também indisponível; verificado antes de
implementar, não assumido). `TE(X->Y)` no horizonte de predição `u=1`
(Schreiber 2000, valor padrão, NÃO varrido como parâmetro de ajuste) é a
informação mútua condicional `I(Y_{t+u}; X_t^{(m_X,tau_X)} |
Y_t^{(m_Y,tau_Y)})`, estimada pelo estimador KSG-CMI de vizinhos mais
próximos (Kraskov, Stögbauer & Grassberger 2004; extensão para
informação mútua condicional de Frenzel & Pompe 2007, eq. 8):

```
A = Y_{t+u} (futuro do alvo, escalar)
B = X_t^{(m_X,tau_X)} (história do canal fonte)
C = Y_t^{(m_Y,tau_Y)} (história própria do alvo)

eps_i = distância (norma de Chebyshev/máximo, padrão KSG) ao k_NN=4-ésimo
        vizinho mais próximo de i no espaço conjunto completo (A,B,C)
n_AC(i) = # pontos j!=i com distância_max((A,C)) < eps_i
n_BC(i) = # pontos j!=i com distância_max((B,C)) < eps_i
n_C(i)  = # pontos j!=i com distância_max(C) < eps_i

TE(X->Y) = psi(k_NN) - <psi(n_AC+1)> - <psi(n_BC+1)> + <psi(n_C+1)>
```

`k_NN=4` fixo (valor padrão da literatura, nunca ajustado por domínio,
igual ao `k_NN` usado no critério de Ragwitz-Kantz acima para
consistência interna). `psi` = função digamma. Norma de Chebyshev
(máximo por coordenada) no espaço conjunto, convenção padrão KSG que
garante o cancelamento de viés entre os 4 termos — distinta,
deliberadamente, da norma Euclidiana usada no passo de seleção de `m`
acima (dois papéis diferentes: seleção de embedding vs. estimação de
informação).

### Estimador de robustez — Transferência de Entropia Simbólica (Staniek & Lehnertz 2008)

Reaproveita DIRETAMENTE `permutation_entropy/analysis/pe_common.py::
ordinal_pattern_codes` (import, não reimplementação), `m=4` FIXO,
`tau_BP=1` FIXO — mesma convenção já auditada nesta linha. Cada canal
vira uma sequência de símbolos (24 padrões ordinais possíveis). TE
discreta padrão (Schreiber 2000) aplicada aos símbolos, com histórico de
comprimento 1 em unidades de símbolo (o próprio símbolo já codifica `m=4`
amostras brutas de história, convenção de Staniek & Lehnertz 2008 —
horizonte `u=1` PASSO DE SÍMBOLO, unidade diferente do `u=1` AMOSTRA
BRUTA do estimador KSG, nomeado explicitamente para não confundir):
estimador plug-in (contagens empíricas, sem suavização) de
`sum p(y_{t+1},y_t,x_t) * log2[p(y_{t+1}|y_t,x_t)/p(y_{t+1}|y_t)]`. Este
estimador é SEMPRE computável para qualquer `N>=m!=24` (nenhum risco de
não-convergência tipo FNN), mas sofre de esparsidade combinatória em
segmentos curtos (espaço conjunto de `24^3=13.824` estados) — **risco
nomeado a priori, não descoberto post-hoc:** o domínio sísmico (Gap de
janelas abaixo) produz segmentos de ordem `10^2`-`10^3` pontos após
o *binning*, tornando a TE simbólica ali estruturalmente ruidosa/pouco
confiável por esparsidade — reportada mesmo assim (protocolo não muda
por domínio), mas com esta ressalva explícita carregada para
`RESULTS_SUMMARY.md` se materializar.

## Sub-janelamento para não-estacionariedade (decisão de desenho FIXADA a priori, Gap central desta candidatura)

TE assume (quase-)estacionariedade formalmente (Vicente, Wibral, Lindner
& Pompe 2011, *J. Comput. Neurosci.* 30:45) — ambos os domínios são
fortemente não-estacionários perto da transição (crise convulsiva; par de
terremotos). Mitigação: computar TE em SUBJANELAS curtas dentro de cada
segmento PRE/POST, depois agregar por MEDIANA (robusta a subjanelas
atípicas, escolha pré-declarada em vez de média) — em vez de uma única
estimativa gigante e não-estacionária.

**Regra domain-agnostic, fixada a priori:** para um segmento de `N`
amostras (já subamostrado, ver Gap de custo computacional):
- `N < N_ABS_MIN=30`: `insufficient_samples`, nenhum cálculo.
- `N_ABS_MIN <= N < N_MIN_SUBWINDOW=200`: uma única "subjanela" = o
  segmento inteiro (`n_subwindows=1`) — colapso honesto e reportado como
  tal (`n_subwindows_achieved=1`), não um erro.
- `N >= N_MIN_SUBWINDOW=200`: `L_SUB = max(N_MIN_SUBWINDOW,
  floor(N/N_SUBWINDOWS_TARGET=8))`, `n_subwindows = floor(N/L_SUB)`,
  blocos contíguos NÃO sobrepostos (resto final descartado).

`N_MIN_SUBWINDOW=200` é o piso prático citado na literatura de TE sobre
dado fisiológico real para o KSG-CMI permanecer razoavelmente estável com
`k_NN=4` e dimensionalidade conjunta modesta (Vicente et al. 2011).
`N_SUBWINDOWS_TARGET=8` é uma meta, não uma garantia — domínios com
poucas amostras totais (o domínio sísmico após *binning*, ver Gap
abaixo) podem colapsar para `n_subwindows=1` mesmo nesta regra, uma
CONSEQUÊNCIA PREVISÍVEL e aceita a priori do desenho, não uma falha.

TE por subjanela é computada de forma IDÊNTICA (mesmo `(m,tau)` por
canal, já fixado do PRE completo) para real, substitutos IAAFT e
substitutos de deslocamento circular — os substitutos são gerados no
segmento COMPLETO (preservando a estrutura global que cada método de
nulo se propõe a preservar) e DEPOIS particionados no MESMO esquema de
subjanelas do dado real correspondente, garantindo comparação
"maçãs-com-maçãs" entre real e nulo.

## `I(X)`

**Primário:** `TE_net(X->Y) = TE(X->Y) - TE(Y->X)` — fluxo direcionado
líquido, mediana das subjanelas de cada direção, agregado por segmento.

**Companheiro:** `TE_sum(X,Y) = TE(X->Y) + TE(Y->X)` — magnitude total de
acoplamento bidirecional (agnóstico a direção).

Ambos calculados DUAS VEZES por segmento/condição: uma vez via KSG-CMI
(estimador primário contínuo) e uma vez via TE Simbólica (estimador de
robustez, Staniek & Lehnertz 2008) — `STE_net`, `STE_sum`. Nenhum dos
dois é redefinido por domínio; a mesma fórmula e os mesmos parâmetros
fixos são aplicados aos dois domínios sem ajuste.

`Delta_TE_net = mediana(TE_net_POST_subjanelas) - mediana(TE_net_PRE_subjanelas)`
(e igualmente para `TE_sum`, `STE_net`, `STE_sum`).

## Protocolo de nulo substituto DUPLO — território genuinamente novo nesta linha

### Primário: IAAFT por canal, independente (Schreiber & Schmitz 1996)

Reimplementação própria desta linha (mesmo padrão de "nova implementação
por candidatura" já usado em `pe_common.py`/`dmd_common.py`, não
reaproveitamento direto de código). `N_SURROGATES=200`,
`N_IAAFT_ITER=50`, `seed=12345`, bicaudal. Cada canal é fase-randomizado
INDEPENDENTEMENTE do outro (destrói a relação cruzada temporal entre X e
Y, preserva o espectro linear/distribuição de amplitude PRÓPRIOS de cada
canal) — convenção padrão para estatísticas de acoplamento (Papana,
Kyrtsou, Kugiumtzis & Diks 2013), testando a hipótese nula "o acoplamento
observado excede o que se espera da estrutura linear/espectral de cada
canal isoladamente". Substitutos de PRE e POST gerados
INDEPENDENTEMENTE, cada um a partir da sua própria série real — mesmo
protocolo já usado 14x nesta linha (`p = fração de substitutos com
|Delta_substituto| >= |Delta_real|`).

### Companheiro (não fallback — rodado desde o início): deslocamento circular (Quian Quiroga, Kraskov, Kreuz & Grassberger 2002)

Pré-autorizado como companheiro, não gatilho de baixo poder. Um único
deslocamento circular aleatório é aplicado ao canal `Y` relativamente a
`X` (canal `X` mantido EXATAMENTE inalterado — decisão simétrica: para
`TE(X->Y)` e `TE(Y->X)` usa-se o MESMO par deslocado nesta iteração,
evitando duas convenções de deslocamento diferentes por direção),
preservando EXATAMENTE a forma de onda/espectro de cada canal (ao
contrário do IAAFT, que gera um substituto novo cada vez) e destruindo
SOMENTE a relação cruzada temporal fixa entre os dois canais. Deslocamento
sorteado uniformemente em `[min_shift, N-min_shift]` amostras, com
`min_shift = max(N//10, m_X*tau_X, m_Y*tau_Y, 10)` — evita deslocamentos
triviais próximos de 0/N que, dada a suavidade/autocorrelação de curto
prazo de sinais fisiológicos e sísmicos reais, deixariam a relação
cruzada quase intacta. `N_SURROGATES=200`, `seed=67890` (stream separado
do IAAFT, fixo e distinto, documentado explicitamente — evita
correlacionar os dois fluxos de números aleatórios). Bicaudal, mesma
fórmula de `p`. Aplicado a PRE e POST independentemente (deslocamentos
sorteados separadamente para cada condição).

**Ambos os métodos são reportados lado a lado para os 4 canais (`TE_net`,
`TE_sum`, `STE_net`, `STE_sum`) em cada domínio/variante — nenhum é
descartado a priori.**

## Riscos de identificabilidade (documentados, não hipotéticos)

1. **Risco de redundância matemática vs. os 14 candidatos anteriores:
   BAIXO.** Nenhuma identidade algébrica encontrada (Fase 0.8) — esta é a
   primeira candidatura bivariada/direcional de toda a linha; os 14
   anteriores são estatísticas univariadas.
2. **Viés de amostra finita do KSG** — conhecido na literatura (Kraskov
   et al. 2004), tipicamente decai com `N` mas não é zero para `N`
   finito. Mitigado (não eliminado) porque `Delta=POST-PRE` cancela um
   viés aproximadamente constante entre condições de tamanho amostral
   comparável — mesma lógica já usada implicitamente por outros
   candidatos desta linha para vieses de estimador. Não elimina viés se
   PRE e POST tiverem `N` efetivo (após sub-janelamento) MUITO diferente
   — nomeado como limitação a ser observada, não escondida.
3. **Não-estacionariedade dentro de PRE/POST** — mitigada pelo desenho de
   sub-janelamento acima, FIXADO a priori (não uma correção post-hoc).
4. **Confundidor de fonte comum (James, Barnett & Crutchfield 2016,
   *Phys. Rev. Lett.* 116:238701)** — TE pode ser dirigida por uma fonte
   externa compartilhada, não por transferência genuína X->Y. Risco REAL
   e nomeado especificamente para os 2 domínios (mitigação de desenho
   abaixo, não descoberta post-hoc) — E checagem adversarial obrigatória
   se qualquer achado `p<0,05` sobreviver (ver Gap de reprodução
   adversarial, item 7 da tarefa orquestradora).

## Domínio 1 — CHB-MIT EEG, `chb01_03.edf`, canais `FP1-F7` (frontal) e `T7-P7` (temporal)

**Fonte:** PhysioNet CHB-MIT Scalp EEG Database
(`https://physionet.org/files/chbmit/1.0.0/chb01/`), 256Hz, montagem
bipolar (nomes de canal já são pares bipolares nativos do EDF, não
derivados por esta sessão). `chb01-summary.txt` confirmado por fetch
direto nesta sessão: `chb01_03.edf`, início 13:43:04, convulsão
documentada em `[2996s, 3036s]` relativa ao início do arquivo, 1 hora de
duração total do arquivo (3600s).

**Escolha de desenho, decidida e documentada (instrução explícita da
tarefa permite ambas as opções):** design de UM ÚNICO arquivo/episódio
(`chb01_03.edf` sozinho), NÃO estendendo para `chb01_04.edf`. Motivo:
evita (a) ter que assumir/verificar continuidade sem lacunas entre dois
arquivos EDF gravados separadamente, (b) misturar dois episódios
convulsivos distintos (com seus próprios períodos pré/pós-ictais) dentro
de uma única condição POST não-estacionária de forma ainda mais severa
do que o já esperado, (c) mantém a interpretação de `Delta` limpa: UMA
transição real, não duas.

**PRE/POST (transição = onset da convulsão, `t=2996s`, documentado no
`summary.txt`, externo ao cálculo de TE):**
- PRE primária: `t=[0, 2996)` s dentro de `chb01_03.edf` (pré-ictal +
  interictal, ~49,9min, `n~=767.096` amostras a 256Hz).
- POST primária: `t=[2996, 3600)` s dentro de `chb01_03.edf` — até o
  final do registro contínuo disponível no arquivo (não há outro evento
  documentado dentro deste arquivo) — inclui os 40s ictais documentados
  mais ~564s pós-ictais (`n~=154.624` amostras).
- PRE robustez: 50% mais recentes (por contagem de amostras) do PRE
  primária.
- POST robustez: 50% mais próximos da transição do POST primária.

**Direção pré-declarada, testada bicaudalmente de qualquer forma
(Wilke, Worrell & He 2011, *IEEE Trans. Biomed. Eng.*; literatura de
sincronização ictal em geral):** acoplamento AUMENTA ao redor do onset,
frequentemente com fluxo de saída (outflow) da zona de início ictal.
Não presumimos aqui qual dos dois canais (`FP1-F7` frontal, `T7-P7`
temporal) é a zona de início sem evidência adicional — ambas as direções
de `TE_net` são reportadas e testadas.

**Risco nomeado e mitigação, carregado para o resultado final
independentemente do veredito (Nolte, Ziehe, Nikulin, Schlögl, Krämer,
Brismar & Müller 2008, *PRL* 100:234101):** condução de volume entre
eletrodos próximos pode produzir "acoplamento" espúrio de fase zero.
Parcialmente mitigado por (a) montagem BIPOLAR (já usada, não
referência comum, reduz mas não elimina condução de volume compartilhada
entre pares de eletrodo espacialmente próximos) e (b) a própria
construção de TE, que é estritamente defasada no tempo (`u=1` amostra à
frente, não fase zero) — mas NÃO totalmente eliminado; nomeado como
ressalva real em `RESULTS_SUMMARY.md` independentemente do resultado.
**Checagem adversarial adicional específica deste domínio, pré-declarada
para o caso de achado significativo:** comparar pares de eletrodo
fisicamente PRÓXIMOS vs. DISTANTES — se o efeito aparecer igualmente
forte independentemente da relevância fisiológica/distância entre
eletrodos, é evidência de artefato de condução de volume, não de
sincronização ictal genuína.

## Domínio 2 — Terremotos de Kahramanmaraş, Turquia, 06/02/2023, estações IRIS `KO.GAZ..HHZ` e `KO.BNN..HHZ`

**Fonte:** IRIS/EarthScope FDSN dataselect + station web services
(`https://service.iris.edu/fdsnws/...`), verificado por fetch direto
nesta sessão: `KO|GAZ||HHZ` (37,17°N 37,21°E, 100Hz, ativa desde
2022-02-03) e `KO|BNN||HHZ` (38,85°N 35,85°E, 100Hz, ativa desde
2022-11-29) — ambas cobrindo integralmente a janela necessária.
Transições (USGS, catálogo externo): M7,8 Pazarcık em
`2023-02-06T01:17:34Z`, M7,5 Elbistan em `2023-02-06T10:24:48Z`
(~9h07min depois).

**Mitigação OBRIGATÓRIA contra o artefato de propagação de onda
compartilhada (mesmo modo de falha que enganou `dmd_koopman` em
Kīlauea) — NÃO alimentar forma de onda bruta de 100Hz ao estimador de
TE.** Distância `GAZ`-`BNN` implica atraso de propagação de onda
sísmica da ordem de dezenas de segundos entre as duas estações — se
alimentada bruta, a TE detectaria trivialmente esse atraso de
propagação físico como "acoplamento", não uma covariação genuína do
PROCESSO de disparo de tensão/réplicas (Freed 2005, *Annu. Rev. Earth
Planet. Sci.* 33:335). **Pré-processamento fixado a priori, ANTES de
qualquer cálculo:** taxa de energia sísmica local (RMS) em blocos NÃO
sobrepostos de largura fixa `BIN_WIDTH_S=120s` (2 minutos) — dentro da
faixa sugerida de 1-10min, e comodamente (3x) maior que o atraso de
propagação de onda entre as duas estações, garantindo que qualquer
acoplamento detectado reflita covariação estação-a-estação do PROCESSO
de disparo de tensão em escala de minutos, não a chegada compartilhada
da mesma onda:
```
rms_bin_j = sqrt( (1/n_bin) * sum_{i em bloco j} x_i^2 )
```
aplicado à forma de onda BRUTA (contagens do instrumento, sem remoção de
resposta instrumental — comparação relativa de energia, convenção já
usada por outros candidatos sísmicos desta linha, p.ex. Kīlauea em
`dmd_koopman`/`largest_lyapunov_exponent`, não um limite novo).

**PRE/POST (transição = M7,8, `2023-02-06T01:17:34Z`):**
- PRE primária: 24h imediatamente antes da transição
  (`2023-02-05T01:17:34Z` a `2023-02-06T01:17:34Z`) — janela de fundo
  operacional fixada a priori (não há outro evento de magnitude
  comparável documentado imediatamente antes nesta região que forneça um
  limite natural mais curto; mesma convenção de janela de fundo de 24h já
  usada para segmentos PRE sísmicos nesta linha, p.ex. Kīlauea).
  `~288` blocos de 2min.
- POST primária: da transição M7,8 até a transição M7,5
  (`2023-02-06T01:17:34Z` a `2023-02-06T10:24:48Z`, ~9,12h — convenção
  "até o próximo evento documentado" desta linha). `~273` blocos de
  2min.
- PRE robustez: 50% mais recentes (últimas 12h) do PRE primária.
- POST robustez: 50% mais próximos da transição (~4,56h) do POST
  primária.

**Consequência a priori explícita do sub-janelamento (Gap acima) para
este domínio, declarada ANTES de rodar:** com `N` da ordem de `10^2`-`10^3`
blocos, a regra de sub-janelamento provavelmente colapsa para
`n_subwindows=1` ou poucas subjanelas em várias das 4 combinações
segmento×variante — isto é esperado e aceito, não uma falha de desenho a
corrigir depois.

**Direção pré-declarada, testada bicaudalmente de qualquer forma
(literatura de transferência de tensão/gatilho de réplicas):**
acoplamento AUMENTA na sequência de réplicas em relação ao fundo.

**Risco nomeado e mitigação — confundidor de magnitude/processo comum
(análogo ao que refutou o achado de `dmd_koopman` em Kīlauea):**
**Checagem adversarial obrigatória, pré-declarada, se `p<0,05` em
qualquer canal/variante deste domínio:** divisão "placebo" inteiramente
dentro do PRE (sem transição real nenhuma) — se a mesma "significância"
aparecer numa divisão arbitrária sem evento real, é evidência de
sensibilidade genérica do domínio/pipeline a qualquer corte de sismo de
fundo, não uma assinatura genuína de disparo de tensão — mesmo desenho
adversarial que refutou com sucesso o achado espúrio de `dmd_koopman`
em Kīlauea.

## Gap de custo computacional (fixado a priori)

`MAX_N_PER_SEGMENT=4000` amostras por segmento (aplicado IGUALMENTE aos
dois canais de um mesmo par — decimação por *stride* uniforme, UMA
decisão de *stride* por segmento aplicada aos DOIS canais simultaneamente
para preservar o pareamento temporal exato entre X e Y; diferente da
subamostragem independente por canal usada em candidatos univariados
desta linha). `k_NN=4` fixo em todo o pipeline (KSG-CMI e Ragwitz-Kantz).
`M_MAX=10` (grade de busca de `m`). Estes tetos equilibram o protocolo de
200 substitutos IAAFT + 200 substitutos de deslocamento circular × 50
iterações IAAFT × até 8 subjanelas × 2 direções × 2 estimadores (KSG +
Simbólico) × 2 domínios × 2 variantes — mesma disciplina de orçamento já
usada nesta linha (RQA, VG, LLE), fixada antes de saber se algum segmento
excede o limite.

## Disciplina de escalonamento (reafirmada, aplicável a esta candidatura)

Um ÚNICO passo de correção pré-declarado e mecânico é autorizado se a
validação sintética obrigatória revelar um problema genuíno de desenho
(não uma reformulação de hipótese) — especificado no protocolo de
validação sintética (`analysis/validate_synthetic.py`/
`VALIDATION_NOTE.md`). Depois disso, o candidato DEVE ser fechado,
positivo ou negativo, honestamente. Nenhuma sintonia aberta.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
é escrito para esta linha (mesmo padrão já usado nos 14 candidatos
anteriores — este é o 15º candidato identificado nesta linha ao todo, 1º
dos 2 genuinamente novos encontrados na sondagem da Fase 0.8 de
2026-08-20). A metodologia acima foi fixada ANTES de qualquer cálculo
real, precisamente para que o resultado da validação sintética
obrigatória — fechamento na validação ou passagem para dado real — seja
reportado como o resultado honesto que é.
