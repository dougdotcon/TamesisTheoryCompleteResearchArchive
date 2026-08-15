# DISC-TRI-RG-001 — Nova rodada de busca de candidatos (2026-08-15)

**Contexto:** após os 3 candidatos viáveis da Fase 0 original (`critical-slowing-down`,
`wavelet-multiresolution-scaling`, `dfa-multiscale-entropy`) serem testados com
rigor completo e todos resultarem NEGATIVO (incluindo a revisita com registros
de backup do Apnea-ECG), a linha foi pausada (`DISC-DEC-006`). Restava, das 3
rotas de retomada listadas naquela pausa, apenas uma não exercida: nova
rodada de busca por candidatos ainda não considerados. Usuário pediu
explicitamente para executar essa rota.

**Método:** 5 agentes de pesquisa independentes em paralelo, cada um com
instrução explícita de (a) ler os 3 `RESULTS_SUMMARY.md` dos candidatos já
testados para não repetir os mesmos erros estruturais; (b) formalizar um
`R_lambda`/`I(X)` genuinamente diferente dos 5 candidatos da Fase 0 original;
(c) evitar o erro estrutural já identificado duas vezes nesta linha (tratar
comparação ESTÁTICA de classe entre sistemas diferentes como se fosse
transição de regime); (d) buscar pelo menos 2 domínios físicos distintos com
dado real verificado por download, cada um com transição documentada por
fonte EXTERNA dentro do MESMO sistema no tempo; (e) declarar honestamente
gaps e riscos, sem forçar `viable=true`. Nenhum agente teve acesso ao
trabalho dos outros 4 (paralelo, sem coordenação).

## Candidatos investigados

### 1. Entropia Multiescala (Multiscale Sample Entropy, MSE) — `viable: true`

`R_lambda`: coarse-graining de blocos NÃO sobrepostos (Costa, Goldberger &
Peng 2002/2005) — literalmente um mapa de bloco-spin/renormalização, com
fundamentação formal mais forte que qualquer candidato já testado nesta
linha (conexão direta com o Teorema Central do Limite visto como fluxo de
RG — Jona-Lasinio 2001, *Physics Reports* 352). `I(X)`: índice de
complexidade (soma de `SampEn(tau)`) ou inclinação `beta` da curva
`SampEn` vs. `log(tau)`. Classificação relevante/marginal/irrelevante
proposta com precedente real (ruído branco = irrelevante/CLT; processo
1/f = marginal/ponto fixo não-trivial; processo integrado = relevante).

**2 domínios novos verificados por download real:** (a) índice geomagnético
Dst/SYM-H, tempestade de março de 1989 ("Quebec Blackout", SYM-H mínimo
−714 nT, ano completo 1989 baixado do NASA/SPDF OMNIweb, 34,4MB, sha256
registrado); (b) vibração de rolamento até falha (FEMTO/PRONOSTIA, IEEE PHM
2012 Data Challenge, critério de fim-de-vida >20g definido pelos
organizadores, externo ao cálculo de entropia — o caso mais limpo de
não-circularidade dos dois).

**Risco central declarado pelo próprio agente:** para processos gaussianos
autossimilares puros, `beta` (MSE) pode ser essencialmente um reparâmetro do
expoente de Hurst `H` — mesma família estatística já testada 2x nesta linha
(DFA-alpha, wavelet-C2) com resultado negativo. Discriminador proposto: MSE
é sensível a estrutura NÃO-linear que substitutos IAAFT (que preservam o
espectro linear) não reproduzem — ao contrário de DFA-alpha, que a própria
linha já descobriu ser quase puramente espectral (baixo poder do IAAFT). Se
esse discriminador se confirmar, MSE testaria algo genuinamente diferente
de DFA; se não, colapsa na mesma redundância.

**Gaps:** regra de `tau` cross-domain ainda mais desafiadora que nos outros
candidatos (convenção original de Costa usa `tau` inteiro absoluto,
incompatível entre 25,6kHz e 5min); nenhum `Delta I` calculado ainda;
ambiguidade de direção já documentada na própria literatura de
entropia-magnetosfera (sinal de alerta igual ao que já fez CSD errar).

### 2. Expoentes de criticalidade auto-organizada (SOC) / avalanches — `viable: true`

`R_lambda`: binning temporal diádico de eventos (composição formal
`R_2λ=R_λ'∘R_λ`, mesma propriedade rigorosa do candidato wavelet). `I(X)`:
expoente `tau` da lei de potência de tamanho de avalanche, e/ou razão de
ramificação `sigma`. Classificação relevante/marginal/irrelevante com
precedente real (Bak-Tang-Wiesenfeld 1987; Sethna, Dahmen & Myers 2001).

**2 domínios novos verificados por download real:** (a) sequência sísmica de
Ridgecrest 2019 (API FDSN do USGS, 30.131 eventos M≥0,5 reais, foreshock
M6.4→mainshock M7.1→decaimento de réplicas); (b) flares solares (GOES XRS,
NOAA/NCEI, arquivo real inspecionado, transição de mínimo/máximo de ciclo
solar determinada externamente pelo painel NASA/NOAA, independente da
própria estatística de flares).

**Terceiro domínio corretamente rejeitado:** avalanches neuronais sob
anestesia (Curic, Ashby & McGirr 2024) — vigília e anestesia gravadas como
sessões distintas em animais diferentes, repetindo o erro estrutural já
identificado 2x nesta linha (comparação de classe, não transição temporal).

**Mecanismos mundanos já identificados a priori (positivo — exatamente a
disciplina que a Extensão de Metodologia 5 pede fazer ANTES, não depois):**
incompletude de curto prazo pós-mainshock (STAI) distorce o expoente
medido logo após a transição sismológica, sem qualquer criticalidade
genuína; viés de detecção dependente do fluxo de fundo em flares solares
menores durante o máximo solar.

**Gaps:** nenhum `tau`/`sigma` calculado ainda; falta regra única de
`lambda` cross-domain (spikes em ms vs. sismicidade em min vs. flares em
horas); nenhum protocolo de nulo substituto implementado; troca de
satélite GOES não resolvida se a transição de dez/2019 for usada.

### 3. Grafo de visibilidade + renormalização de box-covering — `viable: true`

`R_lambda`: grafo de visibilidade natural (Lacasa et al. 2008) seguido de
box-covering renormalization (Song-Havlin-Makse, o mesmo método já
verificado — mas nunca implementado em código — no candidato inviável
`box-covering-network-renorm` da Fase 0 original). `I(X)`: dimensão fractal
`d_B` do grafo.

**2 domínios novos verificados por download real:** (a) geomagnetismo (NASA
OMNI, tempestade de 17/03/2015, SSC documentado externamente); (b)
hidrologia (USGS NWIS, altura de régua do Furacão Harvey, pico real de
44,31 pés). Sondagem exploratória (implementação própria, não
pré-registrada) confirmou tratabilidade computacional em janelas moderadas,
mas custo O(N²) real e mensurável (risco concreto para janelas grandes tipo
ECG plena resolução).

**Risco central e decisivo, achado na literatura:** três artigos reais
(Xie & Zhou 2011; Liu, Zhou & Yuan 2010; Fan, Guo & Zha) mostram que o
rótulo fractal/não-fractal do grafo de visibilidade depende da convenção
de box-covering (node vs. edge-covering) — a MESMA fraqueza que já
reprovou `box-covering-network-renorm` original — e que `d_B(VG)` pode ser
uma reparametrização monótona do expoente de Hurst na mesma série, o que
tornaria este candidato redundante com os 2 candidatos Hurst-adjacentes já
testados e negativos (DFA, wavelet). Sondagem exploratória própria (não
pré-registrada) mostrou `Delta d_B` pequeno e ajuste power-law vs.
exponencial ambíguo nos dois domínios — mesmo padrão de fragilidade que já
derrubou `wavelet-multiresolution-scaling`.

### 4. Análise de Quantificação de Recorrência (RQA) — `viable: true`

`R_lambda`: embedding de Takens (reconstrução de espaço de fase) seguido de
threshold de distância (matriz de recorrência). Formalmente mais fraco que
wavelet/MSE (sem propriedade de semigrupo natural entre embeddings), mas
com uma vantagem real que nenhum outro candidato desta linha teve: regras
de seleção de parâmetro NÃO-arbitrárias e publicadas (falsos vizinhos mais
próximos para `m` — Kennel et al. 1992; informação mútua para `tau` —
Fraser & Swinney 1986; taxa de recorrência fixa para `epsilon` — Marwan et
al. 2007). `I(X)`: `%DET` (determinismo), com `%LAM`/`TT`/`ENTR` como
canais secundários.

**2 domínios novos verificados por download real:** (a) engenharia mecânica
(rolamento IMS/Rexnord run-to-failure, NASA PCoE, 984 arquivos reais,
falha de pista externa documentada pelo próprio dataset); (b) sismologia
vulcânica (Kīlauea 2018, IRIS/EarthScope, abertura de fissura + terremoto
M6,9 documentados pelo USGS/HVO).

**Sinal de alerta empírico já observado na própria sondagem exploratória
(mais forte que um risco puramente teórico):** a mesma fórmula, mesma
convenção, aplicada sem modificação aos 2 domínios, produziu comportamento
DOMAIN-INCONSISTENTE — sinal direcionalmente robusto no vulcão (9/9
combinações de parâmetro), ausente/instável no rolamento (7/9 positivo mas
magnitudes ínfimas, sinal invertido em 2/9) — o MESMO padrão de falha que
já derrubou `critical-slowing-down` (achado em 1 de 3 domínios, direção
oposta nos outros).

**Mecanismos mundanos já identificados a priori:** tremor harmônico
vulcânico (McNutt 1992; Julian 1994, fenômeno estabelecido há décadas,
mais periódico/espectralmente estreito que sismicidade de fundo — poderia
por si só elevar `%DET`); assinatura impulsiva de defeito de pista de
rolamento (padrão-ouro de manutenção preditiva há décadas — análise de
envelope, curtose).

### 5. Percolação sob ataque a hubs — `viable: false`

Investigação honesta de dois eventos reais candidatos (blecaute
Nordeste-EUA/Canadá 2003; nuvem de cinzas do Eyjafjallajökull 2010).
Rejeitado: o único evento que fragmentou de fato (blecaute 2003) não tem
reconstrução publicada de `S(f)` a partir do evento real (só simulações em
topologia sintética); o único evento com reconstrução de percolação
publicada sobre dado real (Eyjafjallajökull) explicitamente NÃO cruzou o
limiar de percolação, segundo os próprios autores (Woolley-Meza et al.
2013). Problema de identificabilidade adicional: literatura nomeada
(Hines/Dobson) já disputa se percolação-sobre-topologia é o mecanismo real
de cascata em redes elétricas. Infraestrutura real (FERC/NERC 2003, TADS)
anotada como semente reaproveitável para um projeto futuro dedicado de
reconstrução de topologia, não uma continuação leve.

### 6. Teoria de escala de Anderson (localização) — `viable: false`

Rejeitado de forma ainda mais categórica: nenhuma generalização real
encontrada na literatura (incluindo RG de Anderson em grafos aleatórios
regulares, Vanoni et al. 2024) se liberta do transporte de onda/condutância
quântica — permanece física de matéria condensada em todas as extensões
reais. A única rota de RG de rede genuinamente cross-domain encontrada
(Laplacian Renormalization Group, Villegas et al. 2022/2025) é fisicamente
diferente da função beta de Anderson — usá-la sob esse nome seria
reformulação disfarçada, o erro que esta linha já proíbe explicitamente.
Recomendação do próprio agente: se o laboratório quiser essa rota no
futuro, tratar LRG como sua própria linha nova, não como "Anderson
generalizado".

## Achado transversal da síntese

Aplicando a mesma régua aos 4 candidatos viáveis, dois padrões de risco já
conhecidos desta linha reaparecem, agora identificados ANTES de qualquer
investimento de rigor (exatamente o objetivo desta etapa de busca):

1. **Risco de redundância com a família Hurst/multifractal já testada**
   (MSE, grafo de visibilidade) — ambos podem estar medindo, no fundo, a
   mesma coisa que DFA-alpha/wavelet-C2 já testaram e refutaram, só que sob
   uma matemática de superfície diferente. Precisa ser resolvido cedo (ex.
   correlacionar `beta`(MSE)/`d_B`(VG) com `alpha`(DFA) nas MESMAS janelas)
   antes de qualquer investimento maior.
2. **Sinal de alerta empírico de inconsistência cross-domain já visível em
   sondagem exploratória** (RQA) — o mesmo padrão exato que derrubou
   `critical-slowing-down` (1 domínio robusto, 1 ausente/instável) já
   aparece numa sondagem informal de 1 segmento por condição, antes de
   qualquer rigor. Isso não desqualifica RQA automaticamente, mas é um
   prior desfavorável concreto, não hipotético.

Em contraste, **SOC/avalanches** é o único dos 4 sem nenhum sinal de alerta
equivalente nesta rodada — matemática genuinamente distinta dos 3
candidatos já testados (baseada em eventos discretos/leis de potência, não
em expoentes de escala de série contínua), sem risco de redundância
identificado, e com os mecanismos mundanos mais prováveis já mapeados e
concretamente checáveis (correção de STAI é procedimento padrão em
sismologia operacional; escolha de janela de fluxo solar estável evita o
viés de detecção).

## Ranking honesto (não travado — decisão de qual perseguir fica com o usuário)

1. **SOC/avalanches** — matemática mais distinta dos 3 já testados, sem
   risco de redundância identificado, 2 domínios sólidos, mecanismos
   mundanos concretos e corrigíveis já mapeados.
2. **MSE** — fundamentação formal de `R_lambda` mais rigorosa de todos os
   candidatos já considerados nesta linha (conexão direta com CLT/RG), mas
   com risco real de redundância com DFA que precisa ser resolvido primeiro.
3. **Grafo de visibilidade** — mesma força formal (reaproveita box-covering
   já verificado), mas risco de redundância com Hurst mais diretamente
   documentado na literatura (Xie & Zhou 2011) que o de MSE, mais um custo
   computacional real a resolver.
4. **RQA** — vantagem real de ter regras de parâmetro não-arbitrárias
   publicadas, mas já mostrou o padrão de inconsistência cross-domain que
   derrubou CSD, numa sondagem preliminar informal.

Nenhum candidato foi travado. `DISC-TRI-RG-001` permanece
`CANDIDATE_FORMULATING`. Toda a infraestrutura desta busca (URLs
verificadas, contagens de bytes, scripts exploratórios em scratchpad de
sessão, não commitados) fica documentada neste arquivo para reaproveitamento
futuro sem precisar de nova busca do zero.
