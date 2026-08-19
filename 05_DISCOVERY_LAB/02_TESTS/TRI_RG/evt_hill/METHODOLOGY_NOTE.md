# Nota de metodologia — fechamento dos gaps de `evt-hill` (Dinâmica do Índice de Cauda via Teoria de Valores Extremos)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (onda de calor de 2021 no Pacífico Noroeste, NOAA/PDX;
furacão Florence, Rio Cape Fear, USGS). Mesmo espírito de disciplina já
usado para os 9 candidatos anteriores desta linha.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md`
(candidato 4) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #4 (último) entre os 4 novos candidatos da Fase
0.6 — bem fundamentado (seleção de limiar automatizada publicada), 2
domínios novos verificados por download real, mas com um risco de
identificabilidade real (não eliminado) contra `soc-avalanches`, e
confundidores mundanos adicionais já nomeados em ambos os domínios.

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.6): 2 domínios reais com dado baixado/inspecionado
— (a) NOAA NCEI GHCN-Daily, estação PDX (USW00024229), onda de calor de
junho/2021 (pico de 46,7°C, recorde histórico documentado); (b) USGS
NWIS, estação 02105769 (Rio Cape Fear em Lock 1, próximo a Kelly, NC),
furacão Florence (setembro/2018) — gauge DIFERENTE do já usado pelo
furacão Harvey em `grafo-de-visibilidade`. Nenhum `Delta I` calculado
ainda. Faltam: (a) regra de seleção de limiar não-arbitrária,
implementável sem risco de bug (declarando honestamente uma
simplificação do método completo da literatura); (b) definição de
`I(X)` e canal companheiro; (c) checagem de redundância com SOC,
barata e decisiva, usando dado JÁ commitado nesta linha; (d) definição
de PRE/POST SEM o risco de circularidade já nomeado na Fase 0.6, e
confundidores mundanos declarados a priori; (e) piso de amostra; (f)
**protocolo de significância — que precisa ser DIFERENTE do IAAFT
padrão desta linha, por um motivo matemático concreto explicado
abaixo, não uma escolha arbitrária.**

## Gap (a): seleção de limiar/`k` — `R_lambda`

**Regra, simplificação declarada honestamente do método completo de
Danielsson, de Haan, Peng & de Vries (2001, *J. Multivariate Analysis*
76:226):** o método original usa bootstrap DUPLO com correção de viés
via um parâmetro de segunda ordem `rho` estimado separadamente — **essa
correção de viés de segunda ordem NÃO é implementada aqui**, declarado
como simplificação explícita, análoga em espírito à simplificação WCM já
usada em `wavelet-multiresolution-scaling` ou à omissão de `f_multi` em
SPARC-004. Em vez disso, usa-se minimização de MSE via bootstrap SIMPLES
(um único nível), ainda um critério automatizado, sem etapa
visual/subjetiva:

1. Grade de `k` candidato: 30 valores inteiros log-espaçados entre
   `k_min=10` e `k_max=floor(n/4)`.
2. Estimador de Hill em cada `k`: `H(k) = (1/k) * sum_{i=1}^{k}
   log(X_(n-i+1)/X_(n-k))`, sobre as estatísticas de ordem da CAUDA
   SUPERIOR da série bruta (não incrementos absolutos — os 2 domínios
   desta rodada são naturalmente unidirecionais: temperatura mais alta e
   altura de régua mais alta são os extremos de interesse).
3. `B=200` reamostras bootstrap COM reposição do array completo de
   estatísticas de ordem; `Var_boot(k)` = variância das 200 reestimativas
   de `H(k)`.
4. `H_ref` = mediana de `H(k)` sobre o terço central da grade de `k`
   (aproximação determinística do "platô estável" que a inspeção visual
   de um gráfico de Hill tradicionalmente busca a olho).
5. `MSE(k) = Var_boot(k) + (H(k)-H_ref)^2`; `k* = argmin MSE(k)`.
6. `xi = H(k*)`.

**Diferença deliberada da convenção já usada em VG/RQA/Kramers-Moyal
("estimar do PRE, reaplicar sem recálculo"):** aqui `k*`/limiar é
REESTIMADO independentemente em CADA segmento (PRE, POST, e cada
segmento de cada randomização do Gap (f)) — porque o próprio `xi` é uma
propriedade da distribuição marginal daquele segmento específico, e
`k*` é o limiar que melhor resolve ESSA distribuição. Forçar o limiar de
um segmento sobre outro repetiria exatamente o problema estrutural que
já quebrou `PKS` no POST de `kramers-moyal`/EUR-CHF (bins do PRE não
cobrindo uma distribuição POST muito diferente) — lição já aprendida
nesta linha, aplicada aqui a priori.

## Gap (b): `I(X)` e canal companheiro

**`I(X)` primário:** `xi_Hill` (índice de cauda via estimador de Hill,
Gap (a)).

**`I(X)` companheiro:** `xi_MLE` — parâmetro de forma GPD ajustado por
máxima verossimilhança às excedências acima do MESMO limiar `u=X_(n-k*)`
já selecionado no Gap (a) (de Haan & Ferreira 2006) — um estimador
MECANISTICAMENTE DIFERENTE do mesmo índice de cauda (verossimilhança vs.
momento de log-razão de Hill), dando uma forma de validação cruzada
interna: se os dois discordarem substancialmente, isso já é informativo
por si só.

## Gap (c): checagem de redundância com SOC — barata, decisiva, ANTES de qualquer dado NOVO

**Risco de identificabilidade já nomeado na Fase 0.6:** o "princípio do
grande salto único" (Embrechts-Klüppelberg-Mikosch 1997) implica que,
para variáveis de cauda pesada somadas, a soma herda o mesmo índice de
cauda dos termos — risco real (mitigado mas não eliminado pelo fato de
`soc_avalanches` usar CONTAGEM de eventos discretos, não soma de
magnitude).

**Checagem obrigatória, ANTES de tocar qualquer dado novo desta rodada:**
reaproveitar os dados JÁ commitados de `soc_avalanches` (Ridgecrest,
GOES — `02_TESTS/TRI_RG/soc_avalanches/data/`), calcular `xi_Hill` (Gap
a) sobre os MESMOS segmentos PRE/POST já travados por aquele candidato,
e comparar com os valores de `tau`(SOC) JÁ publicados em
`soc_avalanches/RESULTS_SUMMARY.md`/`analysis/result_*.json`. Se
`xi_Hill` e `tau` se moverem juntos (correlacionados) nos mesmos
segmentos, isso é evidência concreta de redundância — declarado
honestamente, mesmo que enfraqueça a candidatura. Se desacoplados,
reforça a distinção teórica já argumentada na Fase 0.6.

## Gap (d): definição de PRE/POST — SEM o risco de circularidade já nomeado

Regra domain-agnostic REAPROVEITADA (mesma convenção já usada 9x nesta
linha), com uma nota explícita sobre por que ISSO evita a circularidade
já identificada na Fase 0.6: PRE (primária) = todo o registro contínuo
disponível anterior à transição documentada; POST (primária) = todo o
registro contínuo disponível POSTERIOR à transição, até o PRÓXIMO
evento/confundidor documentado — **não apenas os dias/horas de pico do
próprio evento extremo**. Usar a janela completa "até o próximo evento"
(tipicamente semanas, não dias) evita medir `xi` só sobre os pontos que,
por definição, já são os mais extremos — o mesmo raciocínio de janela já
usado em todos os candidatos anteriores, aplicado aqui explicitamente
contra o risco já nomeado.

- **Onda de calor (PDX):** transição = início do evento, aviso de calor
  excessivo do NWS para a região de Portland, 25/06/2021. PRE = TMAX
  diário de junho/2021 antes do aviso (mais histórico disponível para
  amostra maior, se necessário). POST = TMAX diário de 25/06/2021 até o
  próximo evento de calor documentado ou final de julho/2021 (o que
  vier primeiro) — várias semanas, não só os 3-4 dias de pico.
- **Furacão Florence (Cape Fear):** transição = landfall categoria 4
  documentado pelo NHC, 14/09/2018. PRE = altura de régua diária/
  instantânea antes do landfall (anos de histórico já verificados
  acessíveis, 2000-2018). POST = altura de régua desde o landfall até a
  recessão de volta à linha de base ou o próximo evento documentado.

**Confundidor mundano já nomeado, checagem obrigatória SE houver
achado:** a estação USGS 02105769 fica em "Lock 1" (comporta/represa) —
mudanças de operação da comporta podem alterar mecanicamente a
estatística de excedência sem refletir nada climático genuíno. Se
`xi_Hill`/`xi_MLE` mostrar mudança significativa neste domínio, checagem
adversarial obrigatória de registros de operação da comporta (se
publicamente disponíveis) ANTES de aceitar o achado como genuíno — mesmo
espírito de "checagem condicional ao achado" já usado em SOC/STAI.

## Gap (e): piso de amostra e teto computacional

`MIN_N_PER_SEGMENT=200` (necessário para uma grade de `k` até `n/4`
fazer sentido com `k_min=10`). `MAX_N_PER_SEGMENT=100.000` — custo
computacional baixo (ordenação O(N log N) + bootstrap O(N) por réplica),
sem necessidade de subamostragem agressiva como em VG/RQA.

## Gap (f): protocolo de significância — TESTE DE RANDOMIZAÇÃO, NÃO IAAFT (desvio deliberado e justificado da convenção padrão desta linha)

**Por que IAAFT é matematicamente INADEQUADO aqui, não uma escolha
estilística:** o IAAFT (Schreiber & Schmitz 1996), por construção,
preserva a distribuição marginal EXATA da série original — a etapa de
ajuste de amplitude gera substitutos cujos VALORES são uma permutação
exata dos valores reais, só reordenados no tempo. O estimador de Hill
(Gap a) depende SOMENTE das estatísticas de ordem/valores da série — não
da ordem temporal. Logo, TODO substituto IAAFT de um segmento real teria
`xi` IDÊNTICO (bit a bit, a menos de ruído numérico do algoritmo
iterativo) ao `xi` do próprio segmento real — a distribuição nula de
`Delta_xi` construída por IAAFT seria degenerada (variância ~0,
centrada exatamente no `Delta_xi` real), tornando qualquer teste de
significância baseado nisso sem sentido (p sempre ~1,0,
independentemente de haver ou não uma mudança genuína). **Este problema
é específico de estatísticas puramente baseadas em valores/marginal
(como `xi`) — não afeta os candidatos anteriores desta linha, cujos
`I(X)` (entropia, recorrência, box-covering, etc.) dependem da ORDEM
temporal, não só dos valores.**

**Substituto adotado — teste de randomização do ponto de corte:**

1. Série combinada = PRE+POST concatenados NA ORDEM TEMPORAL ORIGINAL
   (preserva toda a estrutura de autocorrelação real dos dados — não é
   um embaralhamento).
2. `N_RANDOMIZATIONS=200`. Em cada réplica: sorteia um ponto de corte
   `s` uniformemente entre `MIN_SEG_FRACTION=0,2` e `0,8` do comprimento
   total combinado (evita cortes degenerados perto das bordas); atribui
   os primeiros `s` pontos como "antes" e o restante como "depois";
   recalcula `xi_Hill`/`xi_MLE` em cada lado (Gaps a-b, limiar
   reestimado independentemente em cada lado, mesma regra do dado real).
3. `Delta_xi_aleatorio = xi(depois) - xi(antes)` por réplica.
4. `p = fração de réplicas com |Delta_xi_aleatorio| >= |Delta_xi_real|`
   (bicaudal).

Isso testa a pergunta certa — "o corte na data REAL da transição produz
uma mudança de `xi` mais extrema do que um corte aleatório em outro
ponto da mesma série combinada?" — sem a degenerescência do IAAFT para
esta estatística específica. Mesmo orçamento computacional (200
réplicas) da convenção padrão desta linha, por consistência.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado (mesmo padrão já usado nos 9 candidatos anteriores). A
metodologia acima foi fixada ANTES de qualquer cálculo, incluindo a
substituição do protocolo de significância padrão desta linha (IAAFT)
por um teste de randomização — uma correção justificada por um argumento
matemático concreto sobre a própria natureza do estimador, decidida
antes de ver qualquer resultado real, não uma reformulação posterior.
