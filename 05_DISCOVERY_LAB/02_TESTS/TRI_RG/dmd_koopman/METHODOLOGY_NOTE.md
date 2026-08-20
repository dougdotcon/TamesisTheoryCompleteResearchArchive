# Nota de metodologia — `dmd_koopman` (Decomposição em Modos Dinâmicos / espectro de Koopman)

**Status: decisões metodológicas fixadas ANTES de qualquer cálculo real nos
2 domínios (Itália, primeira onda de COVID-19, lockdown de 09/03/2020;
Kīlauea 2018, abertura da primeira fissura em 03/05/2018).** Mesmo padrão
de disciplina já usado para os 12 candidatos anteriores desta linha — em
particular mesmo espírito de "canal primário revisado a priori, citações
de redundância documentadas antes de qualquer cálculo" já usado por
`kramers_moyal/kappa` e `visibility_graph/d_B`, e mesmo espírito de gate
de validação sintética obrigatória, PRÉ-real-data, já usado por `rqa` e
`largest_lyapunov_exponent` (ambos fechados na etapa de validação por um
gate de embedding compartilhado — ver seção própria abaixo sobre por que
o gate deste candidato é estruturalmente diferente, não uma repetição
cega).

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md`
seção 3 para o levantamento que identificou este candidato como
`viable=true, com canal primário revisado` — ranqueado #3 de 3 candidatos
novos da Fase 0.7, o único cujo canal primário original foi encontrado
redundante DURANTE a própria investigação (antes de qualquer dado real),
não depois.

Este é o 14º candidato identificado nesta linha ao todo (3º e último dos 3
`viable=true` da Fase 0.7, depois de `lempel_ziv_complexity` e
`largest_lyapunov_exponent`). Nenhum `PREREGISTRATION.md` é escrito para
esta linha — este documento cumpre esse papel.

## 0. Por que o canal mais natural foi rebaixado a priori (redundância com `critical_slowing_down`)

O canal originalmente mais óbvio para um candidato baseado em DMD/Koopman
seria a taxa de crescimento/decaimento do autovalor de Koopman dominante
(o único autovalor real de maior módulo). **Este canal foi encontrado,
DURANTE a própria sondagem da Fase 0.7 (não depois de gastar cômputo em
dado real), como matematicamente idêntico ao AC1/variância de
`critical_slowing_down` (candidato #1, já fechado NEGATIVO nesta linha)**
no regime linear/quase-estacionário — não uma semelhança conceitual, uma
equivalência algébrica provada por 2 artigos independentes de 2025-2026:

- **arXiv:2608.14716** ("Koopman early warning signals for bifurcation and
  rate-induced tipping") — valida esta equivalência em dado real de
  blackout de rede elétrica de 1996, mostrando que o sinal de alerta
  precoce baseado no autovalor de Koopman dominante rastreia literalmente
  a mesma informação que AC1/variância nesse regime.
- **arXiv:2508.19655** (*Nonlinear Dynamics*) — deriva diretamente
  `Corr(z_t, z_{t+1}) = λ_{J,1}(β)`: o AC1 escalar é literalmente igual ao
  autovalor dominante do Jacobiano/Koopman no regime próximo ao ponto
  fixo.

Esta é uma redundância MAIS FORTE e MAIS BEM DOCUMENTADA do que qualquer
uma que já sobreviveu até `viable: true` nesta linha antes deste
candidato. **Portanto, por decisão a priori, ANTES de qualquer cálculo,
o canal primário deste candidato é obrigatoriamente a frequência e a
razão de amortecimento do par de autovalores complexos conjugados MENOS
amortecido** (alvo: bifurcações do tipo Hopf/Neimark-Sacker, uma classe
de instabilidade OSCILATÓRIA que a própria literatura de CSD documenta
como ponto cego estrutural do AC1/variância escalar:
**arXiv:2605.28260** — "conventional early warning signals may fail to
distinguish the onset of oscillations... spectral early warning signals
rely upon spectral reddening, which does not occur prior to critical
transitions with an oscillatory component"). O autovalor real dominante é
REBAIXADO a diagnóstico-only desde o início — não é um canal de decisão,
apenas um checador de consistência com a literatura de CSD.

## 1. `R_lambda` — embedding de Hankel + truncamento de posto ótimo

### 1.1. Pré-processamento

Cada segmento (PRE ou POST, real ou substituto) é destendenciado
(remoção de tendência linear por mínimos quadrados, mesma convenção já
usada por DFA/wavelet nesta linha) e padronizado (média zero, variância
unitária) ANTES de qualquer passo abaixo — evita que o DMD confunda
escala de amplitude bruta com estrutura dinâmica, e mantém `I(X)`
comparável entre domínios de unidades físicas completamente diferentes
(casos cumulativos de COVID vs. velocidade sísmica).

### 1.2. Atraso `tau`

**Reaproveitado sem modificação** de `rqa_common.estimate_tau` (primeiro
mínimo local da informação mútua com atraso temporal, Fraser & Swinney
1986, *Phys. Rev. A* 33:1134; 16 bins, `lag=1..min(200, floor(N/10))`,
fallback de primeiro cruzamento por zero da autocorrelação linear) — o
mesmo código, importado diretamente de `rqa/analysis/rqa_common.py`, já
auditado 2x nesta linha (`rqa`, `largest_lyapunov_exponent`). `tau` define
o espaçamento ENTRE coordenadas sucessivas dentro de cada vetor-linha de
atraso do Hankel (convenção padrão de Hankel-DMD/Takens): a linha
`(x_i, x_{i+tau}, ..., x_{i+(d-1)*tau})`.

### 1.3. Dimensão de atraso `d` — regra operacional exata, não-arbitrária

Diferente de `rqa`/`largest_lyapunov_exponent` (que usam Falsos Vizinhos
Mais Próximos, FNN, para escolher a dimensão de embedding `m`), este
candidato usa uma regra MECÂNICA e diferente para `d`, porque o objeto
matemático subsequente (truncamento de posto via SVD, Gavish & Donoho
2014) não precisa — e não deveria — de uma dimensão de embedding
"minimamente suficiente" no sentido de FNN: a teoria de convergência do
Hankel-DMD (**Arbabi & Mezić 2017**, arXiv:1611.06664, "Ergodic theory,
dynamic mode decomposition, and computation of spectral properties of the
Koopman operator") prova que os autovalores/autofunções de Koopman
recuperados por DMD sobre observáveis-instantâneos embarcados em atraso
convergem para os verdadeiros autovalores/autofunções de Koopman à medida
que `d→∞`, via o teorema ergódico de Birkhoff — ou seja, a teoria
recomenda `d` GRANDE, não um `d` mínimo que "resolve" alguma coisa. A
regra abaixo opera nesse espírito ("tão grande quanto praticável"),
balanceado contra a necessidade de manter colunas suficientes no Hankel
para uma regressão de posto `r` bem-condicionada e contra um teto de
cômputo fixado a priori (mesmo espírito do teto `FNN_M_MAX=10`/`K_MAX=200`
de RQA/LLE — nenhum destes é escolhido depois de ver um domínio):

```
d = clip( floor(N / HANKEL_D_DIVISOR), D_MIN, D_MAX )
HANKEL_D_DIVISOR = 10   # ~10% do comprimento do segmento vira dimensão de atraso
D_MIN = 10              # piso: precisa de espaço suficiente para resolver
                        # ao menos alguns pares complexo-conjugados (cada
                        # par consome 2 dimensões reais) além do modo real
                        # dominante -- não um limiar de "resolução" como o
                        # de FNN, um piso de expressividade mínima
D_MAX = 100             # teto de cômputo, fixado a priori (mesmo espírito
                        # do K_MAX=200 de LLE/RQA), evita SVD/regressão
                        # sobre uma matriz de atraso desnecessariamente
                        # grande
```

Número de colunas do Hankel resultante: `T = N - (d-1)*tau`. **Se
`floor(N/HANKEL_D_DIVISOR) < D_MIN` (segmento curto demais para sequer
atingir o piso de expressividade) OU `T - 1 < MIN_HANKEL_COLS=50`
(colunas insuficientes para uma SVD/regressão minimamente estável — mesmo
piso de 50 já usado por `D2_MIN_PAIRS` de LLE e `MIN_THEILER_POINTS`
correlato de RQA/LLE): status `hankel_insufficient_length`.**

**Distinção honesta e central, nomeada explicitamente:** este NÃO é o
mesmo tipo de gate que o `embedding_not_resolved` de FNN em RQA/LLE. O
gate de FNN é um teste de RESOLUBILIDADE DINÂMICA — ele pode falhar
mesmo com dado abundante, porque mede se a geometria do atrator
reconstruído é consistente (fração de falsos vizinhos cai abaixo de um
limiar), e ruído branco/fGn de baixo `H` estruturalmente nunca resolve
esse teste não importa quantas amostras existam. O gate acima é apenas um
teste de SUFICIÊNCIA DE COMPRIMENTO — ele sempre resolve para qualquer
segmento longo o bastante, independentemente de a dinâmica subjacente ser
ruído branco ou um oscilador genuíno, porque o truncamento de posto de
Gavish-Donoho sempre retorna algum posto `r>=1` (não há noção de
"convergência" que possa falhar estruturalmente do jeito que FNN falha).
**Isto é precisamente por que a validação sintética obrigatória da seção 4
não pode simplesmente reproduzir o desenho de validação de RQA/LLE
(testar se o gate "resolve") — ela precisa testar algo genuinamente
diferente: se o canal de frequência/amortecimento do modo complexo
recuperado tem PODER DISCRIMINATIVO real (sobrevive ao IAAFT), não se o
embedding "resolve" num sentido binário.** Ver seção 4.

### 1.4. Truncamento de posto — threshold ótimo de Gavish & Donoho (2014)

Para a matriz de dados `X1` (as primeiras `T-1` colunas do Hankel, shape
`d x (T-1)`), o posto de truncamento `r` é escolhido pelo threshold ótimo
de **Gavish & Donoho 2014** (*IEEE Trans. Info. Theory* 60:5040,
"The Optimal Hard Threshold for Singular Values is 4/√3"), caso de RUÍDO
DESCONHECIDO (o caso praticamente relevante para dado real, onde a
variância do ruído de medição não é conhecida a priori):

```
beta = min(d, T-1) / max(d, T-1)                    # razão de aspecto
omega(beta) = 0.56*beta^3 - 0.95*beta^2 + 1.82*beta + 1.43   # eq. (5) do artigo,
                                                     # aproximação a <1% do valor exato
tau* = omega(beta) * median(valores singulares de X1)
r = #{valores singulares de X1 > tau*}, com r >= 1 forçado
```

`omega(beta)` reduz-se a `omega(1) = 0,56 - 0,95 + 1,82 + 1,43 = 2,86 ≈
2,858` no caso de matriz quadrada (`beta=1`) — o valor citado
literalmente na instrução da tarefa e o mais comumente citado na
literatura de Gavish-Donoho. Aqui usa-se a fórmula geral dependente de
`beta` (também do mesmo artigo, eq. 5), porque as matrizes de Hankel
`d x (T-1)` deste candidato tipicamente NÃO são quadradas (`d<=100`,
`T-1` tipicamente muito maior) — uma generalização correta, não um desvio
da instrução, que reduz-se exatamente ao caso citado quando `d ≈ T-1`.
Este é o `R_lambda` genuinamente livre de sintonia humana: nenhum posto é
escolhido visualmente ou por domínio.

### 1.5. Decomposição em Modos Dinâmicos (exact DMD, Tu et al. 2014)

Com `X1` = colunas `0..T-2`, `X2` = colunas `1..T-1` do Hankel (o operador
de Koopman avança o índice de COLUNA em 1 amostra nativa da série já
processada — não em `tau` — convenção padrão de Hankel-DMD/HAVOK):

```
U, S, Vh = SVD(X1)                    # completa
U_r, S_r, V_r = truncar em r (Gavish-Donoho, seção 1.4)
Atilde = U_r^H @ X2 @ V_r @ diag(1/S_r)     # operador de Koopman reduzido, r x r
autovalores lambda_k, autovetores W = eig(Atilde)
```

(Tu, Rowley, Luchtenburg, Brunton & Kutz 2014, *J. Comput. Dyn.* 1:391,
"On Dynamic Mode Decomposition: Theory and Applications" — formulação
padrão do DMD exato usada aqui.)

### 1.6. Convenção de embedding/posto compartilhado (mesma lógica de RQA/LLE)

`tau` e `d` são estimados/fixados UMA VEZ a partir do segmento PRE de cada
domínio/variante; o MESMO `(tau, d)` é aplicado ao POST correspondente e a
cada substituto de ambos. O posto `r` (Gavish-Donoho), ao contrário, **é
recalculado independentemente por condição** (PRE real, POST real, cada
substituto) — decisão análoga à janela de Theiler do LLE (`w`) e ao
`epsilon` do RQA: `r` é uma característica dos valores singulares
daquela série específica (proporcional ao nível de ruído/estrutura
daquele segmento), não um parâmetro dinâmico compartilhado como `tau`/`d`.
Isto é nomeado explicitamente porque é uma decisão que afeta diretamente
se `Delta`(frequência)/`Delta`(amortecimento) pode refletir mudança de
posto entre PRE e POST — um risco reportado honestamente na validação
(seção 4) e nos resultados, não escondido.

## 2. `I(X)`

### 2.1. Seleção do par de autovalores complexos conjugados menos amortecido

Dos `r` autovalores de `Atilde`:

1. Cada autovalor é classificado como REAL (`|Im(lambda)| < EPS_IMAG *
   |lambda|`, `EPS_IMAG=1e-6`, tolerância relativa fixada a priori) ou
   COMPLEXO.
2. Autovalores complexos são agrupados em pares conjugados (já que
   `Atilde` é real, autovalores complexos aparecem em pares conjugados
   exatos a menos de precisão de ponto flutuante — pareamento por parte
   real mais próxima e parte imaginária de sinal oposto).
3. Entre todos os pares complexo-conjugados, o par PRIMÁRIO é o de MAIOR
   `|lambda|` (mais próximo do círculo unitário = menos amortecido = mais
   perto da fronteira de instabilidade oscilatória).
4. **Se nenhum par complexo-conjugado existir** (todos os `r` autovalores
   efetivamente reais dentro da tolerância): canal primário reportado como
   `no_complex_mode` para aquele segmento — uma falha honesta e
   diagnóstica, não um valor fabricado.

**Primário:**
- `f_dom = arg(lambda) / (2*pi*dt)` — frequência de oscilação do par
  primário. `dt=1` (uma amostra da série JÁ processada por `R_lambda`,
  mesma convenção "sem renormalização específica de domínio" já usada
  pelo `lambda_1` do LLE) — unidades: ciclos por amostra de `R_lambda`.
- `zeta = -ln|lambda| / sqrt(ln(|lambda|)^2 + arg(lambda)^2)` — razão de
  amortecimento do par primário. Adimensional, comparável entre domínios.

Ambas as fórmulas são citadas literalmente da tarefa/da conversão padrão
autovalor-discreto -> par polo-contínuo-equivalente (frequência natural
amortecida e razão de amortecimento de um par de polos complexos
conjugados) usada em identificação de sistemas/engenharia estrutural.

### 2.2. Companheiro — gap espectral entre modos

`|lambda_1| - |lambda_2|`: os autovalores são primeiro colapsados em
MODOS distintos (cada par complexo-conjugado conta como 1 modo, de
magnitude `|lambda|`; cada autovalor real conta como 1 modo, de magnitude
`|lambda|`) — evita o problema trivial de comparar as duas metades do
MESMO par complexo-conjugado (que têm `|lambda|` idêntico por
construção, dando gap=0 vazio). Os modos distintos são ordenados por
magnitude decrescente; `lambda_1`/`lambda_2` aqui são os 2 modos de maior
magnitude (podendo ser o par complexo primário e o modo real dominante,
ou dois pares complexos distintos, dependendo do segmento). Mede quão
"limpo" é o domínio de um único modo sobre a dinâmica reconstruída.

**Diagnóstico secundário, não usado na decisão:** resíduo de
reconstrução de posto finito, `||X2 - Atilde-projetado(X1)||_F /
||X2||_F` — quão bem o modelo Koopman de posto `r` reconstrói a dinâmica
observada.

### 2.3. Diagnóstico-only (rebaixado a priori, seção 0) — autovalor real dominante

`lambda_real_dominant`: o autovalor REAL de maior `|lambda|` (se existir
algum). Reportado como `ln|lambda_real_dominant|/dt` (taxa de
crescimento/decaimento, mesmas unidades de "por amostra de `R_lambda`")
— retido APENAS para checar consistência direcional com a literatura de
CSD (arXiv:2608.14716, arXiv:2508.19655), explicitamente NÃO tratado
como evidência de um invariante novo (ver seção 0).

## 3. Riscos de identificabilidade (documentados, citados, não re-derivados)

1. **Vs. `critical_slowing_down` (#1):** endereçado integralmente na
   seção 0 — canal primário redesenhado especificamente para escapar
   desta redundância, decisão tomada a priori.
2. **Vs. `kramers_moyal` (#9):** `kappa` (canal também demovido do
   Kramers-Moyal, Ritchie & Sieber 2016, ver `kramers_moyal/
   METHODOLOGY_NOTE.md`) é uma função algébrica da MESMA taxa de
   decaimento de Ornstein-Uhlenbeck que o AC1/variância do CSD — e o
   autovalor real demovido deste candidato (seção 2.3) é, pela mesma
   cadeia de identidades da seção 0, ESSA MESMA taxa. Isto forma um
   **cluster de 3 vias, todas equivalentes à mesma taxa de decaimento**:
   AC1/variância(CSD) ≈ `kappa`(Kramers-Moyal) ≈ autovalor real
   demovido(DMD). Nomeado explicitamente aqui, por completude, porque a
   instrução exige checagem contra TODOS os candidatos anteriores, não só
   o óbvio. **Isto NÃO afeta o canal primário real deste candidato**
   (frequência/amortecimento do modo complexo) — o canal de escape do
   próprio Kramers-Moyal (forma global do potencial/número de poços) é
   informação estruturalmente diferente, sem colisão aí também.
3. **Vs. `rqa`/`persistent_homology`/`largest_lyapunov_exponent` (#7,
   #11, e o candidato mais recente de LLE):** ancestralidade
   compartilhada de embedding de atraso (Hankel/Takens); risco de base
   real de não-resolução de embedding em segmento real quase-aleatório —
   ENDEREÇADO via o gate de validação obrigatório da seção 4, desenhado
   especificamente porque o modo de falha deste candidato é
   estruturalmente diferente do FNN (seção 1.3).
4. **Vs. wavelet, DFA (#2, #3):** forma funcional diferente (invariância
   de escala tipo lei de potência vs. decomposição modal
   exponencial/oscilatória) — risco baixo.
5. **Vs. SOC, EVT/Hill (#4, #10):** estatística de valor
   extremo/limiar, não relacionada ao espectro de um operador linear —
   risco baixo.
6. **Vs. MSE, grafo de visibilidade, entropia de permutação (#5, #6,
   #8):** construtos de taxa de entropia/topologia de grafo/padrão
   ordinal — risco baixo.
7. **Vs. `lempel_ziv_complexity` (#12, fechado nesta linha imediatamente
   antes deste candidato):** paradigma diferente (complexidade
   algorítmica/compressão vs. espectro de operador linear) — risco baixo,
   sem necessidade de elaborar mais.

## 4. Validação sintética obrigatória — desenho (fixado ANTES de qualquer cálculo)

Conforme exigido pela seção 1.3 acima: o desenho de validação de
RQA/LLE (testar se um gate binário de resolubilidade converge) NÃO se
aplica aqui do mesmo jeito, porque o gate deste candidato (seção 1.3) é
uma condição de comprimento, não de resolubilidade dinâmica — ele sempre
passa para segmentos longos o bastante, independentemente do conteúdo. A
pergunta relevante e genuinamente testável é outra: **o canal de
frequência/amortecimento do modo complexo recuperado tem PODER
DISCRIMINATIVO real (sobrevive ao IAAFT) quando a dinâmica real muda de
regime (fixo/foco estável -> ciclo-limite), ou o truncamento de posto de
Gavish-Donoho simplesmente devolve ruído sem sinal para segmentos
realisticamente curtos/ruidosos?** Este é exatamente o controle positivo
nomeado pela sondagem da Fase 0.7: um **oscilador de Hopf ajustável**
(sistema de Stuart-Landau).

### 4.0. Diagnóstico de correção de código (não é a validação de identificabilidade em si)

Senoide pura determinística, `x(t) = sin(2*pi*f0*t)`, `f0=0,05`
ciclos/amostra (período 20 amostras), `N=2.000`, dither de `1e-6` (mesma
técnica/razão já usada por RQA/LLE — quebra recorrências exatas de ponto
flutuante). Espera-se: par complexo-conjugado recuperado com `|lambda|`
próximo de 1 (não-amortecido) e `f_dom` próximo de `0,05` ciclos/amostra,
`zeta` próximo de 0. Confirma que Hankel + Gavish-Donoho + DMD exato +
extração de frequência/amortecimento produzem um valor sensato antes de
testar em dinâmica estocástica genuinamente ambígua.

### 4.1. Controle positivo — oscilador de Stuart-Landau com parâmetro de bifurcação de Hopf ajustável

Sistema (forma normal de Stuart-Landau, com ruído aditivo — mesmo
espírito da literatura de sinais de alerta precoce pré-Hopf citada na
seção 0, arXiv:2605.28260, que usa exatamente este tipo de sistema
ruidoso para testar detecção de bifurcação oscilatória):

```
dx = (mu*x - omega*y - (x^2+y^2)*x) dt + sigma*dW_x
dy = (mu*y + omega*x - (x^2+y^2)*y) dt + sigma*dW_y
```

Observável escalar: `x(t)` (parte real de `z=x+iy`) — consistente com o
resto desta linha operar sobre séries escalares univariadas.

- **PRE:** `mu_pre = -0,3` (foco estável — trajetória decai ao ponto fixo,
  com flutuações contínuas induzidas pelo ruído aditivo em torno dele,
  oscilação amortecida).
- **POST:** `mu_post = +0,3` (ciclo-limite — oscilação auto-sustentada de
  amplitude `sqrt(mu_post)`).
- `omega = 1,0`, `sigma = 0,05` (ruído aditivo fraco), integração
  Euler-Maruyama, `dt_internal=0,01`, subamostragem para `sample_dt=0,1`
  (fator 10, mesmo espírito de `dt_internal`/`sample_dt` já usado nas
  validações de Rössler de RQA/LLE), transiente inicial descartado
  (2.000 passos internos = 20 unidades de tempo, ~3 tempos de decaimento
  de `1/|mu_pre|` ou várias voltas do ciclo-limite) antes de manter
  `N=4.000` amostras por segmento. Sementes de ruído independentes por
  segmento/substituto.

**Achado honesto esperado a priori, nomeado antes de rodar:** a forma
normal cúbica literal de Stuart-Landau usada aqui NÃO tem acoplamento
amplitude-frequência (a frequência do ciclo-limite permanece `~omega`,
sem "amolecimento" de frequência) — o sinal mais robusto e
teoricamente esperado é o COLAPSO da razão de amortecimento `zeta` (de
positivo, no foco estável, para próximo de zero, no ciclo-limite), não
necessariamente um deslocamento de `f_dom`. Isto é consistente com a
literatura mais ampla de sinais de alerta precoce para Hopf (o
amortecimento colapsando é a assinatura central; o "amolecimento de
frequência" citado na tarefa é uma assinatura adicional possível em
sistemas com acoplamento amplitude-frequência mais geral, não garantida
neste sistema específico). Reportado honestamente nos resultados,
qualquer que seja o padrão observado — sem reformular a hipótese depois
de ver o resultado.

### 4.2. Controle negativo

Duas realizações INDEPENDENTES (sementes de ruído diferentes) do MESMO
processo, `mu_pre = mu_post = -0,3` (sem bifurcação) — mesmos `omega`,
`sigma`, `dt_internal`, `sample_dt`, `N` do controle positivo. Testa
diretamente a taxa de falso-positivo do canal complexo sob o protocolo
IAAFT completo, quando não há mudança de regime genuína.

### 4.3. Gatilho de correção pré-declarado, ÚNICO e limitado

Mesma disciplina desta linha inteira: se o controle positivo (seção 4.1)
não mostrar poder real (`p>=0,05` em `f_dom` E `zeta`) mas o problema for
de BAIXO PODER (não de não-computabilidade estrutural — aqui não há
`hankel_insufficient_length`/`no_complex_mode` bloqueando o cálculo, já
que o oscilador de Stuart-Landau tem `N=4.000 >> D_MAX=100`), **UM ÚNICO
ajuste pré-autorizado é permitido:** aumentar `sigma` do ruído aditivo
para `sigma=0,15` (aproximando-se mais do regime realisticamente
ruidoso de dado real observado nesta linha, sem alterar `R_lambda`,
`I(X)`, a regra de PRE/POST, ou o protocolo de significância) e
re-rodar UMA vez. **Se ainda assim nenhum canal mostrar poder real:
candidato `dmd_koopman` é FECHADO NA ETAPA DE VALIDAÇÃO**, sem tocar dado
real — resultado honesto e completo, 3º candidato consecutivo desta linha
(depois de `rqa`, `largest_lyapunov_exponent`) a fechar assim, se for o
caso. **Nenhuma segunda correção será feita.**

## 5. Convenção de PRE/POST (regra domain-agnostic, reaproveitada sem modificação)

Mesma convenção já usada 7x nesta linha: PRE (primária) = todo o registro
contínuo disponível antes da transição documentada; PRE (robustez) = os
50% mais recentes desse PRE. POST (primária) = todo o registro contínuo
disponível depois da transição, até o próximo evento/confundidor
documentado; POST (robustez) = os 50% mais próximos da transição desse
POST.

### 5.1. Itália, primeira onda de COVID-19 — lockdown nacional "Io resto a casa", 09/03/2020

- **Fonte:** JHU CSSE `time_series_covid19_confirmed_global.csv`
  (`https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv`),
  linha da Itália (`Country/Region=Italy`), contagem cumulativa diária de
  casos confirmados.
- **Transição:** decreto de lockdown nacional "Io resto a casa",
  09/03/2020 (Decreto do Presidente do Conselho de Ministros, DPCM,
  amplamente documentado).
- **PRE:** toda a série cumulativa disponível a partir do primeiro caso
  registrado até 08/03/2020 (inclusive).
- **POST:** toda a série disponível a partir de 09/03/2020 até o próximo
  confundidor de política documentado de mesma magnitude nacional
  (fechamento total de todas as atividades produtivas não-essenciais,
  DPCM de 22/03/2020) — evita misturar múltiplas mudanças de política
  distintas no mesmo segmento POST.
- Domínio genuinamente novo para esta linha (dinâmica populacional de
  epidemia — nenhum candidato anterior usou este tipo de domínio).
- **Nota honesta a priori sobre resolução temporal:** a série é diária
  (uma amostra/dia), então PRE tem tipicamente ~45-50 amostras e POST
  ~13-14 amostras até o próximo confundidor — MUITO curto para os pisos
  `D_MIN=10`/`MIN_HANKEL_COLS=50` da seção 1.3 quando aplicados
  diretamente à contagem cumulativa bruta. Por isso a série trabalhada é
  a INCIDÊNCIA diária (primeira diferença da contagem cumulativa, `Delta
  casos/dia`), não a contagem cumulativa em si (mesma convenção padrão
  de epidemiologia de séries temporais, evita a autocorrelação trivial
  de uma série monotonicamente crescente); mesmo assim, o número de
  amostras continua pequeno em termos absolutos e este risco é nomeado
  aqui a priori para ser reportado honestamente no resultado, não
  descoberto e escondido depois.

### 5.2. Kīlauea 2018 — abertura da primeira fissura, 03/05/2018

- **Fonte:** IRIS/EarthScope FDSN dataselect
  (`https://service.iris.edu/fdsnws/dataselect/1/query`), estação
  `HV.BYL..HHZ` (velocidade sismométrica vertical, 100Hz) — ou estação HV
  próxima se `BYL` não estiver disponível para a janela necessária
  (decisão de fallback documentada em `data/PROVENANCE_KILAUEA.md` com o
  resultado real da tentativa, não decidida por conveniência depois de
  ver o dado).
- **Transição:** abertura da primeira fissura eruptiva do Lower East Rift
  Zone (LERZ) em Leilani Estates, 03/05/2018, ~16h50 HST (~02h50 UTC de
  04/05/2018) — travada em `2018-05-03T18:00:00 UTC` como convenção
  operacional simples (mesma convenção de hora cheia já usada por
  `lempel_ziv_complexity/data/prepare_kilauea.py` para este EXATO evento,
  reaproveitada aqui por consistência, não redecidida).
- **PRE:** 24h imediatamente antes da transição
  (`2018-05-02T18:00:00`–`2018-05-03T18:00:00 UTC`).
- **POST:** da transição até o próximo evento de grande magnitude
  independentemente documentado, o terremoto M6,9 de flanco sul de
  04/05/2018 (`2018-05-04T22:32:54 UTC`, USGS) — mesmo limite POST já
  usado por `lempel_ziv_complexity` para este domínio.
- **Distinção explícita de transparência (instrução explícita da
  tarefa):** esta é a transição de 03/05/2018 (abertura de fissura +
  terremoto M6,9), **DIFERENTE e NÃO-SOBREPOSTA** da transição de
  17/05/2018 (início explosivo) usada por
  `largest_lyapunov_exponent/METHODOLOGY_NOTE.md` — e é a MESMA transição
  que `rqa/METHODOLOGY_NOTE.md` havia originalmente pré-selecionado mas
  NUNCA tocou (RQA fechou na validação, antes de qualquer dado real).
  Não há conflito real de dado com RQA (RQA nunca calculou nada nesta
  janela). **Nota honesta adicional, não escondida:** esta é a MESMA
  transição/janela temporal (mas estação sismológica potencialmente
  diferente, `BYL` vs. `HAT`) já usada por `lempel_ziv_complexity` neste
  exato domínio — LZC já tocou dado real nesta janela usando a estação
  `HAT`. Isto não é um problema de disciplina desta linha (candidatos
  diferentes podem legitimamente usar a mesma transição documentada, como
  já ocorre explicitamente entre `rqa` e `largest_lyapunov_exponent` no
  Kīlauea), mas é nomeado aqui por transparência total.

## 6. Regra de subamostragem para custo computacional

`MAX_N_PER_SEGMENT=200.000` amostras (mesmo teto já usado por
`lempel_ziv_complexity` para o Kīlauea 2018, domínio sismológico
compartilhado, 100Hz sobre janelas de ~24-28h), decimação por *stride*
uniforme se excedido — aplicado igualmente a todos os domínios via
`rqa_common.subsample_segment` (reaproveitado sem modificação), decidido
antes de saber se algum segmento excede o limite. Para o Hankel/DMD, o
custo dominante é a SVD de `X1` (`d x (T-1)`, `d<=D_MAX=100`) — O(d²·T),
linear em `T` para `d` fixo, tratável mesmo em `T~200.000`.

## 7. Protocolo de significância — IAAFT como teste PRIMÁRIO

Mesmo protocolo já usado nesta linha: `N_SURROGATES=200`,
`N_IAAFT_ITER=50`, substitutos de PRE e POST gerados INDEPENDENTEMENTE
cada um da sua própria série real, `seed=12345`. Teste BICAUDAL. Cada
substituto passa pela MESMA pipeline completa (`(tau, d)` JÁ FIXADOS da
série real correspondente — não reestimados por substituto; posto `r`
recalculado por substituto via Gavish-Donoho, análogo à janela de Theiler
do LLE/`epsilon` do RQA). `p = fração de substitutos com |Delta_canal
substituto| >= |Delta_canal real|`, calculado separadamente para
`f_dom`, `zeta`, e o gap espectral companheiro. Substitutos onde o canal
primário é `no_complex_mode` contam como INDEFINIDOS (excluídos do
denominador da fração, não tratados como zero) — mesma convenção de
"indefinido != não-significativo" já usada por RQA/LLE.

**Fallback pré-autorizado (não usado a menos que a validação sintética
mostre um padrão de baixo poder, não de não-computabilidade
estrutural):** bootstrap por blocos móveis (Kunsch 1989), mesma máquina
reaproveitada de `rqa_common.py`
(`moving_block_bootstrap_resample`/`run_block_bootstrap_test`),
comprimento de bloco ligado à escala temporal do embedding (`L=max(2*tau,
10)`).

## 8. Disciplina de escalonamento (aplicável a esta linha inteira, reafirmada aqui)

Um ÚNICO passo de correção pré-declarado é autorizado se a validação
revelar um problema genuíno de desenho (não uma reformulação de
hipótese) — já especificado na seção 4.3 (aumentar `sigma` do ruído do
controle positivo, mantendo `R_lambda`/`I(X)`/regras de PRE-POST/
protocolo de significância intactos). Depois disso, o candidato DEVE ser
fechado, positivo ou negativo, honestamente. Nenhuma sintonia aberta.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
é escrito para esta linha (mesmo padrão já usado nos 13 candidatos
anteriores — este é o 14º candidato identificado nesta linha ao todo, 3º
e último dos 3 genuinamente novos encontrados na sondagem da Fase 0.7 de
2026-08-20). A metodologia acima foi fixada ANTES de qualquer cálculo
real, precisamente para que o resultado da validação sintética
obrigatória — seja ele um fechamento na validação (como RQA/LLE) ou uma
passagem para dado real — seja reportado como o resultado honesto que é.
