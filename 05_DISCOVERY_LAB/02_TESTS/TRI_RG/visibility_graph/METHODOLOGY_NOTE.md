# Nota de metodologia — fechamento dos gaps de `grafo-de-visibilidade`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (tempestade geomagnética de 17/03/2015, evento de
inundação do furacão Harvey/2017). Mesmo espírito de disciplina já usado
para os 5 candidatos anteriores desta linha (`critical-slowing-down`,
`wavelet-multiresolution-scaling`, `dfa-multiscale-entropy`,
`soc-avalanches`, `mse-multiscale-entropy`).

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`
(candidato 3) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #3 entre os 4 novos candidatos — reaproveita o
box-covering já verificado (mas nunca implementado em código) do
candidato inviável `box-covering-network-renorm` da Fase 0 original, mas
com dois riscos concretos já nomeados: (1) redundância com a família
Hurst (Xie & Zhou 2011; Liu, Zhou & Yuan 2010; Fan, Guo & Zha — a
dimensão fractal de box-covering do grafo de visibilidade pode ser
reparametrização monótona do expoente de Hurst); (2) custo computacional
O(N²) real e mensurável.

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.5, sondagem exploratória própria não pré-
registrada): 2 domínios reais com dado baixado/inspecionado — (a) índice
geomagnético (NASA OMNI, tempestade "St. Patrick's Day" de 17/03/2015,
SSC documentado externamente); (b) altura de régua hidrológica (USGS
NWIS, furacão Harvey, pico real de 44,31 pés). Sondagem confirmou
tratabilidade computacional em janelas moderadas, mas custo O(N²)
mensurável para janelas grandes. Nenhum `Delta I` calculado com protocolo
travado ainda. Faltam: (a) convenção de box-covering (a disputa
node-covering vs. edge-covering já documentada na literatura, que este
pré-registro precisa resolver DECLARANDO uma convenção única a priori,
não escolhendo depois de ver o resultado); (b) declaração de
identificabilidade + teste de poder contra o risco de redundância com
Hurst; (c) regra de PRE/POST; (d) regra de subamostragem para o custo
O(N²); (e) protocolo de significância.

## Gap (a): construção do grafo de visibilidade e convenção de box-covering (`R_lambda`)

**Grafo de visibilidade natural** (Lacasa et al. 2008, PNAS 105:4972,
algoritmo original, não modificado): para uma série temporal
`(t_a, y_a)`, dois nós `a<b` têm aresta se e somente se, para todo `c`
com `a<c<b`:

$$y_c < y_b + (y_a-y_b)\frac{t_b-t_c}{t_b-t_a}$$

Grafo NÃO-direcionado, NÃO-ponderado — convenção original de Lacasa,
não nenhuma variante (horizontal visibility graph, ponderado por
inclinação, etc.).

**Box-covering:** algoritmo de Song, Havlin & Makse (2005, *Nature*
433:392) por NODE-COVERING (não edge-covering) — declarado a priori
precisamente porque a literatura (Xie & Zhou 2011; Liu, Zhou & Yuan
2010) documenta que o rótulo fractal/não-fractal muda entre as duas
convenções; usar node-covering elimina essa ambiguidade por construção,
sem escolher depois de ver o resultado. Uma "caixa" de tamanho `l_B` é um
conjunto de nós tal que a distância de caminho mais curto entre QUAISQUER
dois nós da caixa é `<l_B` (estritamente). `N_B(l_B)` = número mínimo de
caixas para cobrir todos os nós do grafo — cobertura mínima exata é
NP-difícil, usado o algoritmo guloso padrão *compact-box-burning* (CBB,
Song et al. 2007, *Journal of Statistical Mechanics*, mesmo algoritmo
usado na literatura de renormalização de redes), com ordem de nós
sorteada aleatoriamente e resultado MEDIANO sobre `R_REPEATS=50`
sementes independentes por `l_B` (reduz viés de ordem de cobertura,
prática padrão da literatura de box-covering).

**`I(X)` primário:** `d_B` (dimensão fractal de box-covering), ajuste
OLS de `log(N_B(l_B))` vs. `log(l_B)` em escala log-log:
`N_B(l_B) ~ l_B^{-d_B}`.

**`I(X)` secundário (canal companheiro):** `C` (coeficiente de
clustering médio do grafo de visibilidade) — canal distinto de `d_B`
(Lacasa & Toral 2010, *Phys. Rev. E* 82:036120, mostra que clustering do
grafo de visibilidade carrega informação dinâmica complementar à
dimensão de box-covering, não redundante com ela por construção).

**Grade de `l_B` domain-agnostic (fixada a priori):** inteiros
log-espaçados entre `l_B_min=2` e `l_B_max=floor(diam(G)/4)` — piso de 4
no denominador garante que a caixa maior ainda é uma fração pequena do
diâmetro do grafo, necessário para o regime de escala da renormalização
fazer sentido (mesma lógica de "grade ligada ao que é de fato estimável"
já usada em MSE para `tau_max`). `N_SCALES=min(15,l_B_max-l_B_min+1)`
valores únicos. **Se `l_B_max` render menos de 4 valores distintos de
`l_B`**, o domínio é REJEITADO por sub-potência insuficiente para um
ajuste log-log confiável — declarado honestamente antes de qualquer
cálculo, não forçado.

## Gap (b): declaração de identificabilidade — risco de redundância com Hurst

**Risco central, já nomeado na Fase 0.5, não escondido:** `d_B` do grafo
de visibilidade pode ser reparametrização monótona do expoente de Hurst
`H` de uma série gaussiana autossimilar, redundante com `alpha` (DFA,
NEGATIVO nesta linha) e `C2` (wavelet, NEGATIVO nesta linha). **Modelo
concorrente nomeado e real:** processo gaussiano autossimilar de `H`
único (fGn/fBm) — mesmo concorrente já usado por
`wavelet-multiresolution-scaling` e `dfa-multiscale-entropy`.

**Discriminador, mesma lógica já validada com sucesso em
`mse-multiscale-entropy`:** substituto IAAFT (Schreiber & Schmitz 1996)
como teste PRIMÁRIO de significância — preserva o espectro linear
(portanto a estrutura de Hurst) de cada série, mas destrói qualquer
estrutura topológica não-linear genuína do grafo de visibilidade que vá
além disso. Se `Delta d_B`/`Delta C` sobreviverem ao IAAFT, isso é
evidência de estrutura além do que DFA/wavelet já testaram e refutaram —
o próprio teste de identificabilidade desta linha, mesmo raciocínio já
aplicado com sucesso em MSE.

**Validação obrigatória de PODER, ANTES de qualquer dado real (mesma
exigência já usada para MSE, porque aqui também o IAAFT é o teste
PRIMÁRIO, não secundário):** controle positivo sintético — PRE = ruído
branco Gaussiano; POST = mapa logístico caótico (`r=4`) com marginal e
espectro casados ao PRE via remapeamento de posto (rank-remap, mesma
técnica já usada e validada em MSE) — verificar que `d_B`/`C` real
recuperado cai fora da distribuição nula dos 200 substitutos IAAFT
(mesmo padrão de sucesso já visto em MSE: ~19 desvios-padrão da
distribuição nula). **Se a validação repetir o padrão de baixo poder já
visto em DFA-alpha** (substitutos preservando o espectro linear
reproduzindo quase exatamente o valor real): adicionar teste
complementar de bootstrap por blocos móveis (Kunsch 1989) como PRIMÁRIO,
mesma correção já aplicada 2x nesta linha (DFA, SOC), ANTES de tocar
dado real.

## Gap (c): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada 4x nesta linha — CSD, DFA, SOC, MSE): PRE (primária) = todo o
registro contínuo disponível anterior à transição documentada; PRE
(robustez) = os 50% mais recentes (por CONTAGEM de amostras) desse PRE.
POST (primária) = todo o registro contínuo disponível posterior à
transição, até o próximo evento/confundidor documentado; POST (robustez)
= os 50% mais próximos da transição desse POST.

- **Geomagnetismo:** transição = SSC (storm sudden commencement) de
  17/03/2015 ("tempestade de St. Patrick's Day"), documentado
  externamente (Kamide & Kusano 2015, *Earth, Planets and Space* 67:187).
  PRE = período quieto anterior ao SSC. POST = fase principal + fase de
  recuperação após o SSC, até o próximo evento geomagnético documentado.
- **Hidrologia (furacão Harvey):** transição = início da precipitação
  extrema do landfall de categoria 4 documentado pelo NHC (25/08/2017).
  PRE = nível de régua de baseline anterior ao landfall. POST = subida
  até o pico documentado de 44,31 pés e além, até o final do registro
  contínuo disponível da estação.

## Gap (d): regra de subamostragem para custo O(N²) — declarada a priori para TODOS os domínios

Construção do grafo de visibilidade é O(N²) por segmento; box-covering
por CBB adiciona custo adicional não-trivial por `l_B` e por repetição.
**`MAX_N_PER_SEGMENT=5000`** amostras, fixado a priori (não ajustado
depois de ver qual domínio precisa) — se um segmento (PRE ou POST, em
qualquer variante) exceder esse limite, decimado por *stride* uniforme
até `MAX_N_PER_SEGMENT` exatas (mesmo tipo de desvio já declarado
honestamente para o domínio de rolamento em MSE — risco explícito de
atenuar estrutura fina, não escondido). Essa regra se aplica
IGUALMENTE aos 2 domínios desta rodada, decidida antes de saber se algum
segmento realmente excede o limite.

## Gap (e): protocolo de significância — IAAFT como teste PRIMÁRIO

**Decisão, mesmo espírito de MSE (mas diferente de CSD/DFA original/SOC,
onde IAAFT ou Poisson foi secundário):** aqui o substituto IAAFT é o
teste PRIMÁRIO, porque é literalmente o discriminador de
identificabilidade declarado no Gap (b).

Protocolo: `N_SURROGATES=200` pares, `N_IAAFT_ITER=50`, substitutos de
PRE e POST gerados INDEPENDENTEMENTE cada um da sua própria série real,
`seed=12345`. Teste BICAUDAL (sem previsão direcional a priori, mesma
disciplina já usada em CSD/MSE). `p = fração de substitutos com
|Delta_d_B_substituto| >= |Delta_d_B_real|` (e igualmente para
`Delta_C`).

## Adendo — `d_B` estruturalmente NÃO COMPUTÁVEL sob a grade a priori; `C` promovido a discriminador único (fixado ANTES de qualquer dado real)

A validação sintética obrigatória do Gap (b) (`analysis/validate_synthetic.py`,
`analysis/validation_synthetic.json`) revelou que `d_B`, o `I(X)` primário
originalmente declarado no Gap (a), é **estruturalmente NÃO COMPUTÁVEL**
para séries temporais estocásticas típicas sob a própria grade a priori
já declarada (`l_B_max=floor(diam(G)/4)`, mínimo de 4 escalas
distintas, ou seja `diam(G)>=20`). Isso não é um bug de implementação:
o diagnóstico de correção do código (`box_covering_code_diagnostic`) usa
uma rampa linear determinística quase-colinear e produz `d_B=1,899`
corretamente (diâmetro 89, grade de 13 escalas) — o algoritmo de
box-covering/CBB/ajuste OLS funciona quando a grade é atingível.

**O problema é estrutural do próprio grafo de visibilidade sob dado
estocástico:** ruído branco Gaussiano e um processo tipo-fGn (`H=0,7`)
produzem grafos de visibilidade com diâmetro pequeno (~9-14) e CRESCIMENTO
EXTREMAMENTE LENTO com `N` — verificado empiricamente, sem custo de
box-covering/IAAFT, até o teto declarado `MAX_N_PER_SEGMENT=5000`:

| processo | N=500 | N=1000 | N=2000 | N=3500 | N=5000 |
|---|---|---|---|---|---|
| ruído branco | diam=10 | diam=9 | diam=11 | diam=12 | diam=14 |
| fGn-símile H=0,7 | diam=8 | diam=9 | diam=14 | diam=12 | diam=14 |

Mesmo no TETO de tamanho de segmento já declarado a priori (5.000
amostras — o maior que esta linha jamais permitiria usar, por custo
O(N²)), o diâmetro nunca se aproxima de 20. Isso bate com a propriedade
de "mundo pequeno" (*small-world*) já bem documentada na literatura de
grafos de visibilidade (Lacasa et al. 2008/2010) — e está em tensão
direta e conhecida com a própria premissa do box-covering fractal de
Song-Havlin-Makse (2005), que só produz um expoente bem-definido para
redes NÃO-mundo-pequeno. Ou seja: **não é uma limitação de amostra
pequena, corrigível com mais dado** — é uma incompatibilidade estrutural
entre o candidato `grafo-de-visibilidade + box-covering` e qualquer
série temporal estocástica real de tamanho tratável, generalizável a
QUALQUER domínio desta linha, não específica de nenhum dos 2 dominios
alvo.

**Decisão, fixada ANTES de qualquer dado real (nenhuma razão de aceleração,
razão de escala, ou dado observacional real foi tocado até este ponto):**
honrar a própria regra já pré-declarada no Gap (a) ("se `l_B_max` render
menos de 4 valores distintos de `l_B`, o domínio é REJEITADO... declarado
honestamente... não forçado") em vez de afrouxar o divisor ou o piso de
escalas agora que o resultado desfavorável foi visto — isso seria
precisamente o tipo de ajuste de metodologia após ver resultado que esta
disciplina proíbe, mesmo sendo ainda dado sintético. `d_B` é **retirado
do critério de decisão** desta rodada de fechamento de gaps — mantido no
código apenas como diagnóstico reportável quando (raramente) computável,
nunca como parte de um veredito de significância.

`C` (coeficiente de clustering médio, canal companheiro já declarado no
Gap (a) como informação distinta de `d_B` por construção, Lacasa & Toral
2010) é **promovido a `I(X)` único** desta rodada: a validação mostrou
poder real e decisivo contra o risco de identificabilidade nomeado no
Gap (b) — controle positivo (ruído branco vs. mapa logístico caótico,
marginal/espectro casados por remapeamento de posto) recuperou `Delta C`
fora da distribuição nula IAAFT por **~14,5 desvios-padrão equivalentes**
(`p_C=0,0`, `n=200` substitutos); controle negativo (dois processos
lineares idênticos, sementes independentes) corretamente NÃO significativo
(`p_C=0,25`). Isso resolve — para o canal `C` especificamente — o mesmo
risco de redundância com Hurst já nomeado na Fase 0.5 (se `C` fosse mera
reparametrização de `H`, o IAAFT teria o mesmo problema de baixo poder já
visto para `alpha`/DFA nesta linha; não teve).

Todas as referências a `I(X)=d_B+C` no restante deste documento devem ser
lidas, a partir deste ponto, como `I(X)=C` (único, decisivo); `d_B`
permanece reportado nos resultados apenas como diagnóstico, nunca como
parte do critério de significância ou do veredito cross-domain.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml` (pausada por
`DISC-DEC-007`, retomada agora a pedido do usuário para fechar
especificamente este candidato), nenhum `PREREGISTRATION.md` foi
travado. A metodologia acima foi fixada ANTES de qualquer cálculo,
precisamente para que, se um pré-registro for escrito depois, ele possa
declarar honestamente que a convenção de box-covering, a definição de
`I(X)`, a regra de subamostragem e o protocolo de significância já
existiam antes de qualquer resultado real ser visto.
