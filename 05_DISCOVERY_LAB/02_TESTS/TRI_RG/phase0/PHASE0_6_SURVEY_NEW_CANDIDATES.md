# Fase 0.6 — nova busca de candidatos para `DISC-TRI-RG-001` (2026-08-18)

Usuário pediu uma nova rodada de busca após os 7 candidatos anteriores
(3 da Fase 0 original + 4 da Fase 0.5) serem todos fechados sem produzir
um invariante cross-domain confiável. 5 agentes independentes em
paralelo investigaram 5 candidatos genuinamente novos (nenhuma
reformulação leve de nenhum dos 7 anteriores), cada um com instrução
explícita de verificar dado real (não só citar) e avaliar risco de
identificabilidade contra TODOS os 7 candidatos já testados, não só o
mais óbvio.

**Resultado: 4 `viable=true`, 1 `viable=false`.**

## 1. Entropia de permutação + plano complexidade-entropia — `viable: true`

`R_lambda`: embedding ordinal de Bandt-Pompe (mapa de padrão de posto,
Bandt & Pompe 2002, *PRL* 88:174102) — projeta cada janela de `m` pontos
consecutivos (delay `tau`) no seu padrão de ORDEM relativa (permutação
`π∈S_m`), descartando toda informação métrica/de amplitude. Sem
propriedade de semigrupo estabelecida na escala base (mesma fraqueza
formal já identificada no embedding de Takens do RQA) — mitigado
recomendando reaproveitar o `R_lambda` já auditado de `mse_multiscale_entropy`
(coarse-graining de blocos de Costa, `R_2λ=R_λ'∘R_λ`) e computar `I(X)`
em cima dele (Entropia de Permutação Multiescala, Aziz & Arif 2005;
Morabito et al. 2012).

`I(X)`: `H_S` (entropia de Shannon normalizada da distribuição de
padrões ordinais) + `C_JS` (complexidade estatística de Jensen-Shannon,
Rosso et al. 2007, *PRL* 99:154102) — o plano complexidade-entropia.

**Regras de parâmetro não-arbitrárias, as melhores desta linha depois do
RQA:** `m∈{3,...,7}` (Bandt & Pompe 2002); `N>=5·m!` (Riedl, Müller &
Wessel 2013); `tau` via mínimo de informação mútua (Fraser & Swinney
1986 — mesma regra já implementada e auditada em `rqa/`).

**2 domínios novos verificados por download real:** (a) VitalDB (Seoul
National University, indução de anestesia, EEG bruto 128Hz, rótulo
externo `anestart` do sistema clínico hospitalar — caso 1 baixado,
1.477.269 amostras reais, 3,2h); (b) PhysioNet European ST-T Database,
onset de episódio isquêmico transitório dentro do mesmo registro
contínuo de 2h, anotado por cardiologista (Taddei et al. 1992),
verificado por fetch direto (registro `e0103`).

**Risco de identificabilidade central, documentado na literatura:**
Zunino et al. 2008 (*Phys. Lett. A* 372:4768) deriva uma relação quase
monótona entre `H_S` normalizado e o expoente de Hurst para fGn/fBm —
`H_S` sozinho corre risco real de ser reparametrização de `alpha`(DFA)/
`h(2)`(wavelet), ambos já fechados negativos nesta linha. **Discriminador
proposto:** `C_JS` é projetado especificamente para separar ruído
colorido linear de dinâmica caótica/determinística — mesmo papel que o
IAAFT já validou com sucesso para `CI`/`beta`(MSE). Nenhum artigo
publicado testou IAAFT contra `C_JS` especificamente (verificado por
busca) — seria um teste genuinamente novo desta linha, não replicação de
resultado já conhecido.

## 2. Kramers-Moyal / Friedrich-Peinke (reconstrução de Fokker-Planck) — `viable: true`

`R_lambda`: a escala de Markov-Einstein `tau_ME` — o menor `Delta tau`
em que a equação de Chapman-Kolmogorov se sustenta empiricamente
(testável, falsificável, não uma janela escolhida) — **a regra de seleção
de `lambda` mais principiada encontrada em toda esta linha até agora**,
já que é um teste orientado a dado, não uma convenção arbitrária.

`I(X)`: dois canais recomendados juntos — (1) taxa de decaimento local
`kappa=-D1'(x*)` no ponto fixo reconstruído; (2) forma GLOBAL do
potencial `U(x)=-∫(D1(x)/D2(x))dx` (número de poços/bimodalidade) mais a
dependência de estado de `D2(x)` (ruído multiplicativo vs. aditivo).

**2 domínios novos verificados por download real:** (a) FX tick-a-tick
EUR/CHF, choque de despeg do Banco Nacional Suíço em 15/01/2015 (dado
Dukascopy real decodificado, formato binário `.bi5`, preço grudado em
1,2009-1,2010 antes, colapso e oscilação violenta entre ~1,00-1,03
depois — bate com o horário documentado externamente do anúncio do
SNB); (b) PhysioNet MIT-BIH Malignant Ventricular Arrhythmia (`vfdb`),
registro 418 — 121 anotações reais de ritmo, ~10 transições N→VFL→N
DENTRO do mesmo registro contínuo de 35min de um único sujeito (desenho
mais forte que a maioria dos domínios já usados nesta linha, que
tipicamente têm só 1 transição por registro).

**Risco de identificabilidade central, confirmado analiticamente:**
Ritchie & Sieber 2016 (arXiv:1609.07271) mostra que, para a linearização
Ornstein-Uhlenbeck ao redor de um ponto fixo, tanto AC1 quanto variância
(a base de `critical_slowing_down`, já fechado negativo) são funções
algébricas da MESMA taxa de decaimento que `kappa=-D1'(x*)` — o canal (1)
sozinho corre risco real de ser `critical_slowing_down` reformulado.
**Discriminador proposto:** o canal (2), forma global do potencial, tem
precedente real e citável (Livina & Lenton 2007, *GRL* 34:L03712; Livina,
Kwasniok & Lenton 2010, *Climate of the Past* 6:77 — "análise de
potencial" aplicada a transições paleoclimáticas, incluindo eventos de
Dansgaard-Oeschger) mostrando que rastrear o NÚMERO DE POÇOS do potencial
captura informação que AC1/variância, calculados perto de um único
atrator, estruturalmente não conseguem ver.

**Restrição computacional/de densidade de amostra real e verificada:**
o próprio artigo fundador (Renner, Peinke & Friedrich 2001) precisou de
suavização de 44s e `tau_min=4min` efetivos por causa de ruído de
microestrutura — implica poucas amostras independentes por hora de dado
FX de alta frequência, um risco concreto para a estimativa de `D1(x)`/
`D2(x)` binada.

## 3. Homologia persistente / Análise Topológica de Dados (TDA) — `viable: true`

`R_lambda`: embedding de Takens (mesma regra FNN/informação mútua já
auditada em RQA) → complexo de Vietoris-Rips sobre a nuvem de pontos
embedded → diagrama de persistência em H1 (Perea & Harer 2015,
*Found. Comput. Math.* 15:799).

`I(X)`: persistência máxima ou total de H1 (assinatura de
periodicidade/ciclo-limite), ou norma-Lp da paisagem de persistência
(Gidea & Katz 2018, *Physica A* 491:820 — precedente direto de detecção
de transição de regime: aplicado a 4 índices financeiros americanos,
mostrou tendência crescente ~250 dias antes das quebras de 2000 e 2008).

**2 domínios novos verificados por download real:** (a) deformação de
onda gravitacional do LIGO, evento GW150914 (dado de tensão real
decodificado via API GWOSC, 131.072 amostras a 4096Hz, sha256
registrado — domínio genuinamente inédito nesta arquitetura de
laboratório, nunca usado por nenhum dos 7 candidatos anteriores); (b)
S&P500 ao redor da falência do Lehman Brothers (15/09/2008, dado real
via API do Yahoo Finance) — mesmo tipo de domínio (índice financeiro) já
usado por `critical_slowing_down` (NASDAQ 2000-2002), mas evento e série
distintos, e é o precedente de literatura mais direto para este
candidato especificamente.

**Risco de identificabilidade — o único candidato desta rodada com
checagem empírica PRÓPRIA rodada nesta sessão (não só teórica):** o
agente instalou `ripser`/`gudhi` e testou uma senoide ruidosa em 9 níveis
de ruído, correlacionando persistência máxima de H1 com um análogo de
`%DET`(RQA) — **correlação de Pearson r≈0,92** no regime de degradação de
estrutura mais relevante para detectar transição (atrator se
degradando rumo a ruído). Achado concreto e reproduzível (não uma
suposição), indicando risco substancial de redundância com RQA — que já
fechou nesta linha sem sequer alcançar dado real.

**Restrição computacional real, medida diretamente:** custo pior que
O(N²) na prática — janelas acima de algumas centenas de pontos ficam
caras rápido (medido: 3.240 pontos = 16,4s por diagrama, single-core),
forçando janelas pequenas incompatíveis com a taxa de amostragem nativa
de vários domínios (4096Hz do LIGO, 250Hz de ECG) sem uma etapa de
subamostragem adicional — outro parâmetro não-arbitrário a resolver.

## 4. Índice de cauda via Teoria de Valores Extremos (estimador de Hill) — `viable: true`

`R_lambda`: seleção de limiar `u` (fração amostral `k`) via método
duplo-bootstrap que minimiza o erro quadrático médio assintótico do
estimador de Hill (Danielsson, de Haan, Peng & de Vries 2001, *J.
Multivariate Analysis* 76:226) ou via teste sequencial de qualidade de
ajuste GPD (Bader, Yan & Zhang 2018, *Annals of Applied Statistics*
12:310) — ambos automatizados, sem etapa visual/subjetiva.

`I(X)`: índice de cauda `xi` (parâmetro de forma GPD) via estimador de
Hill ou ajuste de máxima verossimilhança, aplicado DIRETAMENTE às
flutuações extremas da série contínua (não a tamanhos de eventos
discretos extraídos, diferente de SOC).

**2 domínios novos verificados por download real:** (a) onda de calor de
2021 no Pacífico Noroeste dos EUA (NOAA NCEI, estação PDX, pico
documentado de 46,7°C em 28/06 — recorde histórico externo); (b)
furacão Florence, Rio Cape Fear (estação USGS 02105769, diferente do
gauge do furacão Harvey já usado por `grafo-de-visibilidade`).

**Risco de identificabilidade, honesto e não trivial:** o "princípio do
grande salto único" (Embrechts-Klüppelberg-Mikosch 1997) implica que,
para variáveis de cauda pesada somadas, a soma herda o mesmo índice de
cauda dos termos individuais — se o tamanho de avalanche do SOC fosse
definido como soma de magnitudes contínuas, isso forçaria redundância
teórica direta com `xi`. Mitigado parcialmente (SOC usa CONTAGEM de
eventos discretos, não soma de magnitude), mas não eliminado — risco
moderado-a-alto, barato de checar cedo (calcular `tau`(SOC) e `xi`(EVT)
nas mesmas janelas já travadas de Ridgecrest/GOES antes de qualquer
pré-registro). Confundidores mundanos adicionais já nomeados: operação
de reservatório/comporta na régua do Cape Fear; risco de circularidade
janela-evento na onda de calor.

## 5. RG de block-spin literal sobre série binarizada — `viable: false`

Investigado como a realização mais literal possível de "R_lambda =
mapa de coarse-graining" (decimação de Kadanoff/Ising 1D sobre uma
versão binarizada da série). Duas das três escolhas de parâmetro têm
fundamentação real e não-arbitrária na literatura (limiar de
binarização via sinal de incremento; regra de decimação via majority-rule
ou decimação de sítio único, ambas convenções clássicas citáveis) —
melhor fundamentado nesses dois eixos que os 2 candidatos originalmente
inviáveis da Fase 0. **Mas falha por um motivo analítico, não
empírico:** a solubilidade exata da decimação de Ising 1D
(`tanh K'=(tanh K)^b`) implica que QUALQUER processo de correlação de
curto alcance flui trivialmente para acoplamento zero sob decimações
repetidas — o observável de fluxo de RG, quando tem algum poder
discriminativo, colapsa numa versão mais ruidosa (binarização destrói
informação) do que o expoente de Hurst já testado 2x negativo (DFA,
wavelet). Reforçado por uma patologia real e citada da mecânica
estatística (van Enter, Fernández & Sokal 1993, *J. Stat. Phys.* 72:879
— transformações majority-rule podem produzir uma medida não-Gibbsiana,
tornando a própria linguagem de "acoplamento efetivo" formalmente
malposta). Nenhum precedente de literatura foi encontrado aplicando essa
maquinaria exata a dado real para detecção de transição de regime.
Fechado por identificabilidade, sem tocar dado real — mesmo espírito já
usado para `spacing-statistics-rmt-non-zeta` na Fase 0 original.

## Ranking honesto (não travado — decisão de qual perseguir fica com o usuário)

1. **Entropia de permutação + plano complexidade-entropia** — melhores
   regras de parâmetro não-arbitrárias desta rodada, semigroup corrigido
   por reaproveitar o `R_lambda` já auditado do MSE, 2 domínios muito
   fortes com transições nitidamente documentadas, e um discriminador
   (`C_JS`) com argumento mecanístico claro e NUNCA testado na
   literatura — mesmo padrão de sucesso que já validou MSE nesta linha.
2. **Kramers-Moyal / Friedrich-Peinke** — regra de seleção de `lambda`
   mais principiada (teste de Markov-Einstein orientado a dado, não
   janela escolhida) de toda a linha até agora; domínio `vfdb` com ~10
   transições dentro do mesmo registro é um desenho mais forte que a
   maioria dos domínios já usados; risco de redundância com CSD
   claramente diagnosticado E com canal de escape real e citado
   (forma do potencial, não só taxa de decaimento local).
3. **Homologia persistente / TDA** — matemática mais distinta de todas
   (topologia algébrica), domínio inédito genuinamente novo (LIGO), mas
   é o único candidato com uma checagem de redundância EMPÍRICA própria
   já rodada nesta sessão mostrando risco concreto (r≈0,92) contra RQA
   — que nem chegou a tocar dado real. Custo computacional real também
   força janelas pequenas.
4. **Índice de cauda EVT/Hill** — solidamente fundamentado e com bons
   domínios novos, mas risco de redundância com SOC é real (mesmo que
   parcialmente mitigado) e ambos os domínios têm confundidores mundanos
   adicionais já nomeados que precisam de mais desenho antes da
   validação.

Nenhum candidato foi travado. `DISC-TRI-RG-001` permanece
`CANDIDATE_FORMULATING`. Toda a infraestrutura desta busca (URLs
verificadas, dados reais efetivamente baixados e inspecionados por cada
agente, checagens exploratórias) fica documentada neste arquivo para
reaproveitamento futuro sem precisar de nova busca do zero.
