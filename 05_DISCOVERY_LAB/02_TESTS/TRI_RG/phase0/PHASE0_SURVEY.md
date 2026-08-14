# DISC-TRI-RG-001 — Fase 0: levantamento de candidatos (R_lambda, I(X))

**Data:** 2026-08-14. **Método:** workflow com 5 agentes de pesquisa
independentes em paralelo (um por candidato) + 1 agente de síntese/ranking.
Cada agente teve acesso a WebSearch/WebFetch/curl e instrução explícita de
NUNCA fabricar citações, URLs ou resultados de acesso — declarar
honestamente quando algo não foi verificado de verdade. Resultado bruto
completo (JSON, ~515 linhas, todas as citações e notas de verificação) em
`workflow_raw_output.json` neste diretório.

**Objetivo desta fase:** cumprir o `next_action` de `DISC-TRI-RG-001` em
`01_PORTFOLIO/TEST_QUEUE.yaml` — nomear um mapa de coarse-graining/
renormalização `R_lambda` candidato e identificar pelo menos DOIS domínios
reais com dado público onde uma quantidade `I(X)` seja computável de forma
IDÊNTICA (mesma fórmula, sem reajuste por domínio), antes de qualquer
pré-registro.

## Os 5 candidatos avaliados

### 1. Critical Slowing Down (variância/autocorrelação lag-1 crescentes) — `viable: true`, **rank 1**

`R_lambda`: coarse-graining temporal por janela deslizante de tamanho
lambda + destendenciamento fixo. `I(X)`: autocorrelação lag-1 (AC1) e
variância dos resíduos, mesma fórmula em todo domínio. Fundamentação real
e verificada (Scheffer et al. 2009 *Nature*; Dakos et al. 2008 *PNAS*,
2012 *Ecology*; Lenton et al. 2012 *Phil. Trans. R. Soc. A* — perto de uma
bifurcação o autovalor dominante da dinâmica linearizada tende a zero,
conexão direta com tempo de relaxação divergente perto de um ponto fixo de
RG). Modelo concorrente nomeado e real: taxonomia B-tipping vs.
R-tipping/N-tipping (Ashwin et al. 2012) — não é espantalho, é o outro
ramo da mesma literatura.

**3 domínios com dado real baixado e verificado nesta sessão** (não apenas
citado): (a) GISP2 (NOAA, núcleo de gelo da Groenlândia) — transição
Younger Dryas→Preboreal, ~11.500 anos AP, rótulo dentro do próprio artigo
de origem (Alley 2000); (b) PhysioNet SDDB (Holter cardíaco) — onset de
fibrilação ventricular, timestamp anotado dentro do próprio arquivo
(`#vfon: 07:54:33`); (c) NASDAQ Composite (FRED) — bolha/crash pontocom
2000-2002, rótulo mais fraco (consenso histórico externo, não anotação
embutida no CSV).

**Gaps concretos ainda não resolvidos:** nenhum `Delta I` foi de fato
calculado nesta sessão (só o acesso ao dado foi verificado); falta uma
regra ÚNICA de seleção de `lambda` que funcione através de escalas de
amostragem radicalmente diferentes (núcleo de gelo ~15-20 anos de
espaçamento vs. ECG 250Hz vs. NASDAQ diário) — sem isso, risco real de
violar o próprio `stop_condition` já declarado na fila ("redefinir I(X)
ou R_lambda por domínio... vira dois modelos separados fingindo ser um");
protocolo de teste contra nulo substituto (AR(1) de parâmetro constante,
método Dakos et al.) ainda não implementado. Um resultado positivo aqui
replicaria majoritariamente uma literatura já estabelecida há 15+ anos —
valor principal seria de infraestrutura (um pipeline único cross-domain
sem reformulação), não física nova, e isso precisa estar dito
explicitamente em qualquer pré-registro futuro.

### 2. Wavelet multiresolution / WTMM (expoente de Hurst generalizado, largura multifractal) — `viable: true`, **rank 2**

`R_lambda`: projeção wavelet multirresolução, `R_2λ = R_λ' ∘ R_λ` POR
CONSTRUÇÃO (subespaços aninhados V_j) — o `R_lambda` mais rigoroso
matematicamente dos 5 candidatos. `I(X)`: expoente de Hurst generalizado
h(q) ou largura do espectro multifractal `Δα` via WTMM. Fundamentação
real (Muzy/Bacry/Arneodo 1991-1995; Kantelhardt et al. 2002). Modelo
concorrente nomeado e real: ruído/movimento Browniano fracionário
monofractal (fGn/fBm de H único) — disputa histórica genuína (Leland et
al. 1994/95 vs. Riedi et al. 1999).

**Domínios:** sismologia (IRIS/EarthScope, estação IU.ANMO em torno do
mainshock de Tohoku 2011, rótulo USGS/GCMT completamente externo — o
exemplo mais limpo de transição real dos 15 domínios apresentados em
todos os 5 candidatos) é o único que satisfaz plenamente "transição real
dentro do mesmo sistema, com rótulo externo". Fisiologia (PhysioNet CHF
vs. NSR) é comparação de CLASSE entre pacientes diferentes, não uma
transição temporal. Tráfego de rede (Bellcore/LBL) tem rótulo de regime
fraco/autorreferencial (sem anotação de ataque externa nesta trace
específica); MAWI/MAWILab identificado como alternativa mais forte mas
não teve conteúdo efetivamente baixado/verificado. Turbulência — domínio
historicamente bandeira do método — buscada e NÃO encontrada acessível
sem conta nesta sessão (lacuna honesta, não escondida).

**Gaps:** hoje só 1 domínio robusto o suficiente (sismologia); falta um
segundo domínio limpo. Nenhuma computação real do método WTMM/
wavelet-leader foi executada nesta sessão (só um proxy informal de
variância Haar no tráfego de rede). A própria literatura documenta que
WTMM produz multifractalidade espúria mesmo para fBm exatamente
monofractal sob amostra finita — controle por dados substitutos
(surrogates IAAFT) é obrigatório, não opcional.

### 3. DFA / Multiscale Entropy — `viable: true`, **rank 3**

`R_lambda`: procedimento DFA padrão (Peng et al. 1994/1995 — nota: o
artigo de batimento cardíaco é *Chaos* 5:82-87 (1995), não PRL como uma
formulação inicial supôs; corrigido pelo próprio agente via checagem
cruzada em 3 fontes). `I(X)`: expoente de escala `alpha(n)`. Execução
empírica a mais séria dos 5 candidatos: algoritmo implementado do zero,
validado contra nulos sintéticos batendo exatamente com a teoria (ruído
branco alpha=0,53≈0,5; passeio aleatório alpha=1,50≈1,5), rodado sobre
dado PhysioNet real decodificado via biblioteca `wfdb` (106-112 mil
batimentos anotados reais por registro, metadados clínicos reais no
cabeçalho) e sobre os gaps de zeros de zeta já usados em
`DISC-RH-GAP-EXTREME-VALUE-SCALING-001` (alpha=0,138, anti-persistente,
consistente com a correlação serial negativa GUE já documentada nesse
outro teste do laboratório).

**Problema estrutural não detectado pelo próprio agente, mas identificado
pela síntese ao aplicar a mesma régua usada para rejeitar o candidato
box-covering:** os dois domínios usados (saudável vs. insuficiência
cardíaca; continental vs. oceânico) são comparações de CLASSE entre
sistemas/sujeitos diferentes, não transições de um mesmo sistema
evoluindo no tempo — o que a descrição literal de `DISC-TRI-RG-001` pede
("uma variação Delta I preveja uma transição de regime"). Precisa de
reformulação (ex.: progressão NYHA dentro do mesmo paciente ao longo do
tempo) antes de contar como teste de transição. Além disso, o cálculo
climático de fato não foi executado (só acesso verificado), e a checagem
fisiológica usou N=1 registro por grupo (não a coorte completa de 54+29),
com direção OPOSTA à literatura de grupo — relatado honestamente pelo
próprio agente, esperado com amostra N=1.

### 4. Box-covering / renormalização de redes (Song-Havlin-Makse) — `viable: false`, rank 4

`R_lambda` mais rigoroso e literal de todos os 5 (renormalização real em
blocos sobre grafos, iterável, com classificação relevante/marginal/
irrelevante extraída diretamente do texto primário, PDFs lidos nesta
sessão). 4 datasets de rede reais verificados via download+descompressão
byte a byte (SNAP/CAIDA). **Rejeitado corretamente pelo próprio agente:**
toda evidência de "transição fractal↔não-fractal" na literatura vem de
modelos SINTÉTICOS com parâmetro de mistura artificial ajustado
manualmente — nenhum sistema real observado atravessando essa transição
no tempo foi encontrado. O que existe em dado real é uma classificação
ESTÁTICA (WWW/PIN=fractal; Internet AS-level=não-fractal), não uma
transição — e mesmo essa classificação está sob disputa metodológica
ativa (arXiv:2501.16030, 2025, reclassifica a Internet como fractal).

### 5. Estatística de espaçamento de níveis / parâmetro de Brody, fora de zeta — `viable: false`, rank 5

Dados reais baixados e computação real executada (níveis nucleares
RIPL-3/ENSDF; autovalores de rede de coautoria SNAP ca-GrQc) — `I(X)=⟨r⟩`
calculado com a mesma fórmula (Atas et al. 2013) nos dois domínios.
**Rejeitado corretamente:** falha em identificabilidade (a previsão
testada é idêntica à de Bohigas-Giannoni-Schmit 1984 + RMT padrão, já
confirmada há décadas nos dois domínios exatos usados aqui — não há
discriminador Tamesis-específico) e em RG/EFT (nenhum `R_lambda` genuíno
foi implementado; a única proposta — janela espectral como parâmetro de
escala — foi corretamente identificada como subamostragem, não
coarse-graining real).

## Achado transversal da síntese

Aplicando a MESMA régua a todos os 5 candidatos, a síntese identificou que
dois candidatos (`dfa-multiscale-entropy` e o domínio de fisiologia de
`wavelet-multiresolution-scaling`) cometem o mesmo erro estrutural que
corretamente derrubou `box-covering`: tratar uma comparação ESTÁTICA de
classe entre sistemas diferentes como se fosse uma transição de regime.
Isso não havia sido detectado pelos próprios agentes desses dois
candidatos — só emergiu ao comparar os 5 resultados lado a lado.

## Recomendação (síntese, não travada)

Nenhum dos 5 candidatos está pronto para `CANDIDATE_LOCKED`/pré-registro
hoje. `critical-slowing-down` é o mais próximo — único cujos 3 domínios
verificados são transições genuínas dentro do mesmo sistema ao longo do
tempo, com pelo menos 2 dos 3 rótulos vindos da própria fonte — mas de
forma CONDICIONAL: faltam (a) regra única de seleção de `lambda`
cross-domain, (b) protocolo de nulo substituto (Dakos et al.), (c) cálculo
real de `Delta I` nos 3 domínios já verificados (hoje só o acesso ao dado
foi confirmado). `wavelet-multiresolution-scaling` fica em segundo lugar,
efetivamente com 1 domínio robusto (sismologia/Tohoku) — precisaria de um
segundo domínio tão limpo quanto esse antes de avançar. `dfa-multiscale-
entropy` tem a execução técnica mais sólida mas precisa de reformulação
em torno de uma transição temporal genuína. Os dois inviáveis
(`box-covering`, `spacing-statistics-rmt-non-zeta`) têm infraestrutura de
dado real reaproveitável e rotas alternativas identificadas (percolação
sob ataque a hubs; teoria de escala de Anderson) — anotadas como sementes
futuras, não descartadas do laboratório.
