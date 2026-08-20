# Nota de metodologia — fechamento dos gaps de `lempel-ziv-complexity`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (congelamento de marcha em Parkinson, Daphnet FoG; erupção
do Kilauea 2018, Lower East Rift Zone). Esta nota faz o papel do
`PREREGISTRATION.md` para esta linha de candidatos (`DISC-TRI-RG-001`) —
nenhum `PREREGISTRATION.md` é escrito nesta linha, por convenção já usada
nos 9 candidatos anteriores. Uma vez travada, esta nota só pode ser
corrigida por um bug de implementação genuíno descoberto na validação —
nunca por redefinição de `I(X)` ou `R_lambda` depois de ver resultado
real.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md`
(candidato 1) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #1 entre os 3 novos candidatos da Fase 0.7 — o
`R_lambda` mais simples e livre de parâmetro de toda a linha até agora
(sem embedding, sem dimensão, sem delay, sem grade de escalas), evitando
estruturalmente o modo de falha de não-resolução de embedding que já
fechou `RQA` na validação e quase fechou `homologia persistente`.

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.7): 2 domínios reais com dado baixado/inspecionado
diretamente NESTA sessão (re-verificação, não apenas re-citação da
Fase 0.7) — (a) Daphnet Freezing-of-Gait (UCI ML repository, acelerometria
tri-axial de marcha em Parkinson, 64Hz, sujeito `S01R01` confirmado com 18
transições reais caminhada→congelamento dentro de um único registro
contínuo de 151.987 amostras); (b) sismicidade vulcânica do Kilauea 2018,
estação `HV.HAT..HHZ` via IRIS/EarthScope FDSN dataselect, 100Hz,
disponibilidade contínua confirmada para a janela necessária (sem gaps).
Nenhum `Delta_LZC` calculado ainda. Faltam: (a) definição exata do
algoritmo LZ76 + regra de normalização + `I(X)` primário/companheiro; (b)
declaração de identificabilidade e fraqueza estrutural; (c) definição
exata de segmento PRE/POST em cada domínio (incluindo a regra de seleção
de transição/canal, decidida ANTES de qualquer cálculo de LZC); (d)
protocolo de significância e orçamento computacional.

## Gap (a): `R_lambda` e `I(X)`

**`R_lambda` primário — binarização por limiar de mediana** (Aboy,
Hornero, Abásolo & Álvarez 2006, *IEEE Trans. Biomed. Eng.* 53:2282):

```
s(i) = 0  se x(i) <  mediana(X)
s(i) = 1  se x(i) >= mediana(X)
```

calculada UMA VEZ sobre cada segmento (PRE e POST têm cada um sua própria
mediana — a regra de coarse-graining é reaplicada por segmento, não uma
mediana global compartilhada, seguindo a mesma disciplina já usada para
`r` em MSE e `epsilon`/`RR_target` em RQA: o limiar é reestimado
localmente a cada segmento, nunca herdado do PRE para o POST).

**`R_lambda` companheiro — quantização ternária por tercis** (Kamath
2016, *Cogent Engineering* 3(1):1177924): os limiares são o tercil 1/3 e
o tercil 2/3 da distribuição empírica do PRÓPRIO segmento (mesma
disciplina "reestimado por segmento" acima), mapeando cada amostra para
`{0,1,2}`.

**Normalização de Kaspar & Schuster 1987** (*Phys. Rev. A* 36:842),
aplicada à contagem bruta de parsing LZ76 (Lempel & Ziv 1976, *IEEE
Trans. Info. Theory* 22:75) de um scan guloso da string simbólica:

```
b(n) = n / log_alpha(n)      (alpha = tamanho do alfabeto: 2 para
                               binário, 3 para ternário)
LZC   = c(n) / b(n)
```

onde `c(n)` é a contagem bruta de subsequências distintas produzidas pelo
algoritmo de parsing LZ76 padrão (implementação clássica de Kaspar &
Schuster, validada nesta sessão contra o caso de teste do próprio artigo
original: string binária `1001111011000010`, `c` esperado `=6`,
confirmado bit a bit antes de qualquer uso real).

**`I(X)` primário:** `LZC_median` — LZC normalizada sobre a série
binarizada por mediana.

**`I(X)` companheiro:** `LZC_ternary` — LZC normalizada sobre a série
quantizada por tercis (`b(n)=n/log3(n)`), especialmente relevante ao
domínio de marcha/Parkinson abaixo (Kamath 2016 desenvolveu a variante
ternária especificamente para sinais fisiológicos de marcha).

`Delta_LZC_median = LZC_median(POST) - LZC_median(PRE)`,
`Delta_LZC_ternary = LZC_ternary(POST) - LZC_ternary(PRE)`, ambos
testados bicaudalmente contra substitutos IAAFT (Gap (d)).

**Nota de notação:** este candidato é o primeiro desta linha SEM
embedding, SEM ordem `m`, SEM delay `tau`, e SEM grade de escalas — não
há Gap de "regra de escala cross-domain" análogo ao de MSE/PE/DFA/wavelet
porque `R_lambda` aqui não depende do domínio de forma alguma além da
reestimação de mediana/tercis por segmento (que é automática, não
requer nenhuma escolha de parâmetro humana).

## Gap (b): declaração de identificabilidade e fraqueza estrutural

**Risco central, já documentado na literatura, não hipotético:** Ziv &
Lempel 1978 (*IEEE Trans. Info. Theory* 24:530) provam que LZC converge
assintoticamente para a taxa de entropia de uma fonte estacionária
ergódica — o MESMO alvo teórico assintótico de `CI`/`beta` (MSE, já
fechado NEGATIVO nesta linha) e, possivelmente por extensão via a família
de Hurst, de `alpha`(DFA)/`h(2)`(wavelet) (ambos também já fechados
NEGATIVOS), mesmo risco genérico de parentesco com Hurst já documentado
para `H_S`(entropia de permutação) por Zunino, Pérez, Martín, Garavaglia,
Plastino & Rosso 2008.

**Contra-evidência real e concreta de não-redundância em amostra finita,
já encontrada na literatura (não uma esperança vaga):**

- Villazana, Seijas & Caralli 2015 mostram LZC e entropia de Shannon
  NÃO-monotonicamente relacionadas em registros REAIS do MIT-BIH
  Arrhythmia Database (registro 109: entropia alta, LZC baixa) — a
  relação assintótica teórica (Ziv & Lempel 1978) não se manifesta como
  monotonicidade estrita em amostra finita/dado real.
- Mateos, Zozor & Olivares 2017/2020 constroem um plano LZC-permutação
  vs. entropia-de-Shannon-permutação e o mostram COMPLEMENTAR, não
  redundante, separando fBm de fGn de ruído-K apesar de espectros médios
  idênticos entre as classes.

**Discriminador desta linha:** sobrevivência ao teste de substitutos
IAAFT (Schreiber & Schmitz 1996) — o próprio teste de falsificação já
usado com sucesso para separar candidatos redundantes (ex. `alpha` DFA,
sem poder) dos genuinamente não-redundantes (ex. `CI` MSE, `C_JS`
entropia de permutação, com poder real) nesta linha. **Nenhum artigo
publicado testou IAAFT contra LZC especificamente em nenhum dos 2
domínios desta rodada** (verificado por busca dedicada na Fase 0.7) — o
teste de validação sintética abaixo (Gap (d)/`validate_synthetic.py`) é
genuinamente novo, não uma replicação de resultado já conhecido na
literatura.

**Fraqueza estrutural nomeada honestamente, ANTES de qualquer resultado
(não descoberta defensivamente depois de um nulo):** ao contrário de
`C_JS` (complexidade estatística de Jensen-Shannon, entropia de
permutação), que foi PROJETADO especificamente por Rosso et al. 2007 para
separar caos determinístico de ruído estocástico correlacionado, LZC
como formulado aqui NÃO tem um segundo canal projetado especificamente
para essa discriminação — limitação documentada na literatura por
Nagarajan 2002 (*IEEE Trans. Biomed. Eng.* 49:1371). O canal ternário
(`LZC_ternary`) é um DIAGNÓSTICO DE ROBUSTEZ (mesma pergunta, alfabeto
mais fino), não um discriminador caos-vs-ruído — isso é dito aqui
explicitamente, não inventado um substituto agora. Se a validação
sintética abaixo mostrar que nenhum dos dois canais tem poder real contra
um controle positivo de caos determinístico genuíno, essa fraqueza
estrutural é a explicação a priori mais provável, não uma surpresa.

**Modelo concorrente nomeado:** processo gaussiano autossimilar de `H`
único (fGn/fBm) — mesmo concorrente já usado por
`wavelet-multiresolution-scaling`, `dfa-multiscale-entropy`,
`mse-multiscale-entropy`, `grafo-de-visibilidade` e `entropia-de-
permutação`.

## Gap (c): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada em todos os candidatos anteriores desta linha): PRE (primária) =
todo o registro contínuo disponível anterior à transição documentada;
PRE (robustez) = os 50% mais recentes (por CONTAGEM de amostras) desse
PRE. POST (primária) = todo o registro contínuo disponível posterior à
transição, até o próximo evento/confundidor documentado; POST
(robustez) = os 50% mais próximos da transição desse POST.

### Domínio 1 — Daphnet Freezing-of-Gait, sujeito `S01R01`

**Regra de seleção do sujeito/registro (fixada a priori):** primeiro
sujeito/registro com >=1 transição caminhada→congelamento anotada E
>=5.000 amostras disponíveis tanto antes quanto depois da transição
escolhida (piso adaptado do exemplo dado na instrução da tarefa) —
`S01R01` (18 transições, N=151.987 amostras totais, ~2.375s) satisfaz
isso trivialmente e é o registro já verificado na Fase 0.7; nenhum outro
sujeito foi inspecionado (sujeitos 4 e 10 não têm nenhum evento de
congelamento, per o próprio README do dataset — excluídos por desenho,
não por falha).

**Regra de seleção de canal (fixada a priori, fundamentada na
literatura, não escolhida por explorar o dado):** aceleração vertical do
tornozelo (coluna 3 do arquivo, índice 2 em array 0-indexado) — o sensor
e eixo primário usados por Bächlin et al. 2010 (o próprio artigo que
define este dataset) no algoritmo de índice de congelamento
(*freeze index*), fundamentado na literatura do domínio, não em
inspeção do resultado.

**Regra de seleção de transição e definição de PRE/POST (fixada a
priori, ANTES de qualquer cálculo de LZC):** como o registro contém
múltiplas transições (18 no total), episódios de congelamento
individuais são fisiologicamente breves por natureza (documentado:
34–973 amostras = 0,5–15,2s cada, mediana ~2s) — abaixo de qualquer piso
razoável de amostra para uma estimativa de LZC minimamente confiável se
usados isoladamente como janela POST. Este candidato, ao contrário de
`kramers-moyal`/`vfdb` (que usou APENAS a primeira transição isolada,
janela POST curta mas aceitável para aquele pipeline), define a
transição documentada como o ONSET do PRIMEIRO episódio de congelamento
anotado por vídeo no registro (amostra 72.944, `t=1.139,75s`) — o
primeiro instante em que o comportamento de congelamento se manifesta
nesta sessão, um evento clinicamente significativo e documentado por
vídeo sincronizado (Bächlin et al. 2010). **PRE = sinal contínuo
completo do início do registro até esse onset (amostras `[0,
72944)`, mistura de rótulos "fora de protocolo"/"caminhando", sem
filtragem por rótulo intra-segmento — mesma convenção já usada em outros
domínios desta linha, onde o rótulo delimita apenas a fronteira PRE/POST,
não filtra amostras dentro de cada segmento). POST = sinal contínuo
completo desse onset até o FIM do registro (amostras `[72944, 151987)`)
— não há nenhum "próximo evento documentado" mais específico disponível
neste dataset além do fim do arquivo (a sessão termina sem nenhum
protocolo externo de encerramento anotado), então "fim do registro
contínuo disponível" desempenha o papel do próximo evento documentado,
exatamente como a convenção já prevê para esse caso.** Este POST
necessariamente contém uma mistura de caminhada normal e mais 17
episódios de congelamento subsequentes — isso é dito aqui explicitamente
como a interpretação correta do achado (se houver): "regime pós-início-
de-congelamento" (que inclui episódios repetidos de FoG), não "um único
episódio de congelamento isolado". PRE: N=72.944 (~1.139,75s). POST:
N=79.043 (~1.235,05s) — ambos grandes o suficiente para computação
robusta, ordem de grandeza comparável entre si.

Robustez: PRE = últimas 36.472 amostras (50% mais recentes) antes do
onset; POST = primeiras 39.521 amostras (50% mais próximas da transição)
depois do onset.

### Domínio 2 — Kilauea 2018, Lower East Rift Zone, estação `HV.HAT..HHZ`

**Transição documentada:** abertura da primeira fissura eruptiva em
Leilani Estates, ~03/05/2018 (USGS Hawaiian Volcano Observatory) —
travada aqui em `2018-05-03T18:00:00 UTC`, o mesmo horário já usado como
início de janela POST de exemplo na Fase 0.7 (verificado nesta sessão:
LZC não-degenerada em torno desse horário na checagem de sanidade
original).

**Definição de PRE (fixada a priori, com limitação nomeada
explicitamente):** ao contrário de domínios com um início natural
limitado (ex. início de caso clínico, início de teste de rolamento), a
estação `HV.HAT` opera continuamente há anos — "todo o registro contínuo
disponível" literalmente seria multi-anual e diluiria completamente
qualquer contraste de regime com atividade de fundo não relacionada.
PRE é travado aqui a uma janela de 24h imediatamente anterior à
transição: `2018-05-02T18:00:00` a `2018-05-03T18:00:00 UTC`
(confirmado nesta sessão: traço único contínuo, sem gaps, 8.640.000
amostras a 100Hz). **Limitação honesta, nomeada agora, não escondida:**
a cronologia pública do USGS/HVO indica que a atividade sísmica/de
intrusão precursora na Lower East Rift Zone já vinha se intensificando
desde ~30/04/2018 (colapso do piso da cratera do Puʻu ʻŌʻō) — esta
janela de 24h portanto não é necessariamente "fundo sísmico de longo
prazo completamente limpo", mas é o "fundo imediatamente anterior à
abertura da fissura", que é a interpretação honesta reportada, não
inflada.

**Definição de POST — "próximo evento documentado" usado explicitamente
como fronteira (fixada a priori):** o terremoto M6,9 do flanco sul do
Kilauea, `2018-05-04T22:32:54 UTC` (USGS — o maior terremoto no Havaí
desde 1975), é o próximo evento sismológico de grande magnitude e
independentemente documentado após a abertura da fissura — usado aqui
como a fronteira POST, exatamente o papel de "próximo evento documentado"
que a convenção desta linha já usa (ex. `aneend` em MSE/VitalDB). Isso
evita misturar na mesma janela POST dois regimes fisicamente distintos
(a abertura efusiva da fissura vs. a resposta sismológica de um grande
terremoto tectônico + sua sequência de réplicas). POST =
`2018-05-03T18:00:00` a `2018-05-04T22:32:54 UTC` (confirmado nesta
sessão: traço único contínuo, sem gaps, 10.277.400 amostras a 100Hz).
PRE: N=8.640.000 (24h). POST: N=10.277.400 (~28,55h).

Robustez: PRE = últimas 4.320.000 amostras (50% mais recentes, últimas
12h) antes da transição; POST = primeiras 5.138.700 amostras (50% mais
próximas da transição, primeiras ~14,27h) depois da transição.

## Gap (d): orçamento computacional e protocolo de significância

**Subamostragem (gap de orçamento computacional, mesma disciplina já
usada em VG/RQA/PE):** `MAX_N_PER_SEGMENT=200000`, decimação por *stride*
uniforme se excedido — teto maior que o `20000` usado em PE/VG porque o
próprio parsing LZ76 é O(N) e barato (sem embedding); o custo dominante é
IAAFT (FFT por iteração). Benchmark medido nesta sessão (`numpy`
`rfft`/`irfft`, 50 iterações IAAFT, máquina desta sessão): `N=20000` →
~0,15s/substituto: `N=200000` → ~1,30s/substituto → 200 substitutos ≈
260s por série. Com PRE+POST computados independentemente, isso dá
≈260s×2≈9min por combinação domínio×variante — 4 combinações no total
(2 domínios × 2 variantes) ≈36min de IAAFT, orçamento aceitável para
esta tarefa. `N=500000` já chegaria a ≈24min só de IAAFT por combinação
(~96min total) — não escolhido por desnecessário face ao teto de
200.000, que já é grande o bastante para preservar estrutura de baixa
frequência relevante nos dois domínios (Kilauea: 200.000 amostras a partir
de PRE=8,64M dá fator de decimação ~43, de 100Hz para ~2,3Hz efetivo —
ainda captura sismicidade de banda relativamente baixa; Daphnet: PRE e
POST já ficam abaixo do teto sem decimação nenhuma, 64Hz preservado
integralmente).

**Piso mínimo de computabilidade:** `MIN_N_SEGMENT=50` — abaixo disso o
pipeline retorna `status="insufficient_samples"` explicitamente, nunca
um valor calculado silenciosamente sobre uma amostra patologicamente
pequena (nenhum dos segmentos reais definidos no Gap (c) chega perto
desse piso — o menor é PRE robustez do Daphnet POST-robustez,
N=39.521 — mas o piso protege qualquer uso futuro deste pipeline).

**Protocolo de significância — IAAFT como teste PRIMÁRIO:** mesmo
protocolo já usado com sucesso em MSE/VG/RQA/PE/Kramers-Moyal:
`N_SURROGATES=200`, `N_IAAFT_ITER=50`, substitutos de PRE e POST gerados
INDEPENDENTEMENTE cada um da sua própria série real, `seed=12345`. Teste
BICAUDAL: `p = fração de substitutos com |Delta_LZC_substituto| >=
|Delta_LZC_real|`, aplicado independentemente a `LZC_median` e
`LZC_ternary`.

**Fallback pré-autorizado (Gap (e) da convenção geral desta linha):** se
a validação sintética mostrar baixo poder do IAAFT para QUALQUER canal
(`LZC_median` e/ou `LZC_ternary`), bootstrap por blocos móveis (Kunsch
1989) é adicionado como teste PRIMÁRIO complementar para esse canal,
ANTES de tocar dado real — mesma correção já aplicada em DFA, SOC, RQA
(tentado, não ajudou lá por motivo estrutural distinto) e disponibilizada
para PE. Esta é a ÚNICA correção pré-autorizada (per a disciplina de
escalonamento desta linha) — se o fallback também não resolver, o
candidato é fechado na etapa de validação, sem uma segunda tentativa de
redesenho.

**Se a validação mostrar que um canal genuinamente não tem poder
discriminativo além do que a família Hurst já testou:** esse canal pode
ser rebaixado a diagnóstico-only (nunca removido/apagado), mesma
disciplina já aplicada a `kappa`/`beta_D2` em Kramers-Moyal e `d_B` em
grafo-de-visibilidade — decisão de governança tomada pela sessão
orquestradora após ver o resultado, não pelo agente que executa a
validação.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi ou será travado para esta linha (esta nota desempenha esse papel,
per convenção já estabelecida). A metodologia acima foi fixada ANTES de
qualquer cálculo de LZC — os dados reais já foram baixados/inspecionados
para verificar acessibilidade, contagens de amostra e estrutura de
anotação (mesma reconhecimento básico já feito nos scripts `prepare_*.py`
de todos os candidatos anteriores desta linha, ex. `kramers_moyal/data/
prepare_vfdb.py` inspecionando `aux_note` ANTES de calcular qualquer
`PKS`), mas NENHUM valor de LZC, `Delta_LZC`, ou p-valor foi calculado
sobre dado real até este ponto.
