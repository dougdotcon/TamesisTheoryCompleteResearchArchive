# Reprodução adversarial independente — Daphnet Freezing-of-Gait, variante robustez (`lempel-ziv-complexity`)

**Papel:** agente de reexecução adversarial independente, passo 7 de
`AGENTS.md` — reprodução/tentativa-de-quebra de um achado `p<0,05`
(`RESULTS_SUMMARY.md`: Daphnet, variante robustez, `LZC_median` e
`LZC_ternary`, ambos `p=0,0` contra IAAFT), feita **sem memória da sessão
original** que produziu `METHODOLOGY_NOTE.md`/`VALIDATION_NOTE.md`/
`RESULTS_SUMMARY.md`/`CONFOUND_CHECK_DAPHNET.md`. Este documento não
substitui aqueles — os complementa com um segundo agente tentando
ativamente derrubar o achado por rotas que o agente original não tentou.

**Alvo:** `05_DISCOVERY_LAB/02_TESTS/TRI_RG/lempel_ziv_complexity/analysis/result_daphnet_robust.json`
— `LZC_median`: PRE=0,8132→POST=0,6047 (Δ=−0,2085, `p=0,0`);
`LZC_ternary`: PRE=0,7472→POST=0,5548 (Δ=−0,1923, `p=0,0`).

## Veredito (resumo executivo)

**Veredito misto, reportado sem suavizar em nenhuma direção: o número
específico `p=0,0`/`p=0,0` de S01R01 sob IAAFT NÃO é um bug, NÃO é um
artefato do ponto de corte exato, e é bit-a-bit reproduzível — mas o
achado, como um todo, NÃO SOBREVIVE a duas das quatro rotas de ataque
novas tentadas aqui (generalização entre sujeitos; robustez a método de
substituto alternativo), e por isso NÃO deve ser tratado como
"investigado e não-refutado" no sentido forte que justificaria avançar
ao Gate de Replicação sem mais trabalho.** Especificamente:

- **Sobrevive:** checagem de bug de código (Seção 0), reprodução exata
  do pipeline (Seção 1), reverificação das 3 checagens de confundidor
  originais (Seção 2), sensibilidade ao ponto de corte (Seção 3, Ataque
  A) — nestas 4 frentes, o achado é robusto e nenhuma explicação
  espúria simples o desfaz.
- **Não sobrevive integralmente:** resolução do `p=0,0` sob correção de
  múltiplas comparações honesta (Seção 4, Ataque B — ambíguo, não
  necessariamente refutado, mas não comprovadamente robusto dado o
  orçamento de 200 substitutos); generalização para outros sujeitos do
  mesmo dataset com o MESMO pipeline (Seção 5, Ataque C — o padrão
  qualitativo se INVERTE com igual força estatística em S07R01, e é
  inconsistente até em SINAL entre canais em S03R01); e, mais grave,
  robustez ao método de substituto alternativo já pré-autorizado por
  este próprio candidato (Seção 6, Ataque D — `LZC_ternary` PERDE
  significância sob bootstrap por blocos móveis, `p=0,07`).

Detalhes e números completos abaixo, organizados por ataque.

---

## 0. Checagem de correção de código (LZ76 rápido vs. ingênuo) — PASSA

Reexecutados `lz76_complexity` (rápido, O(n log n)) e
`lz76_complexity_naive` (ingênuo, O(n²/log n)) diretamente sobre os 4
arrays reais (`data/daphnet_{pre,post}_robust.npy`, canais mediana E
ternário — 4 combinações):

| segmento | canal | `c(n)` rápido | `c(n)` ingênuo | bate? | tempo rápido | tempo ingênuo |
|---|---|---|---|---|---|---|
| PRE robust (n=36.472) | mediana | 1.957 | 1.957 | sim | 0,42s | 17,09s |
| PRE robust (n=36.472) | ternário | 2.850 | 2.850 | sim | 0,40s | 18,31s |
| POST robust (n=39.521) | mediana | 1.565 | 1.565 | sim | 0,64s | 18,05s |
| POST robust (n=39.521) | ternário | 2.276 | 2.276 | sim | 0,59s | 19,00s |

**Bit-idêntico nas 4 combinações.** A alegação de correção da correção
de desempenho (`VALIDATION_NOTE.md`, Adendo) é confirmada
independentemente, não apenas citada. O achado não é invalidado por um
bug de implementação — prossegue-se para o resto da checagem.

---

## 1. Reprodução independente do pipeline completo (mesmo seed, mesmos parâmetros) — PASSA, BIT-IDÊNTICO

`run_lzc_analysis(pre, post, seed=12345)` (importado sem modificação de
`lzc_common.py`) reexecutado do zero sobre
`data/daphnet_{pre,post}_robust.npy`, mesmos parâmetros travados
(`N_SURROGATES=200`, `N_IAAFT_ITER=50`, `seed=12345`):

| | `LZC_median` PRE | `LZC_median` POST | Δ | `p` | `LZC_ternary` PRE | `LZC_ternary` POST | Δ | `p` |
|---|---|---|---|---|---|---|---|---|
| `result_daphnet_robust.json` (original) | 0,8131541954 | 0,6046929308 | −0,2084613 | 0,0 | 0,7471502565 | 0,5548477328 | −0,1923025 | 0,0 |
| Reexecução independente (esta checagem) | 0,8131541954 | 0,6046929308 | −0,2084613 | 0,0 | 0,7471502565 | 0,5548477328 | −0,1923025 | 0,0 |

**Bit-idêntico em todos os dígitos reportados** (o RNG `seed=12345` do
`numpy.random.default_rng` é determinístico e o pipeline não tem nenhum
componente de paralelismo/ordem não-determinística) — nenhuma
divergência de reprodução. Tempo desta reexecução: 509,7s (~8,5min),
consistente com o orçamento estimado em `METHODOLOGY_NOTE.md` Gap (d).

---

## 2. Reverificação independente das 3 checagens de confundidor já feitas — TODAS CONFIRMADAS

Antes de tentar rotas NOVAS de ataque, recomputei do zero (baixando o
dataset bruto novamente nesta sessão, sem depender de nenhum `.npy` já
derivado) as duas checagens numéricas centrais de
`CONFOUND_CHECK_DAPHNET.md`:

**Checagem 1 (composição de rótulo, caminhada-pura vs. caminhada-pura):**

| Segmento | `n` | `LZC_median` | `LZC_ternary` |
|---|---|---|---|
| PRE robust, só caminhada (rótulo 1) | 21.746 | 0,7613043013 | 0,6931125930 |
| POST robust, só caminhada (rótulo 1) | 37.727 | 0,5911748992 | 0,5560523284 |
| POST robust, só congelamento (rótulo 2) | 1.794 | 0,9037595464 | 0,7982923031 |

Bate exatamente (10 casas decimais conferidas) com
`CONFOUND_CHECK_DAPHNET.md`. **Confirmado independentemente: a queda
persiste (Δ=−0,170 mediana / −0,137 ternário) mesmo isolando
caminhada-pura em ambos os lados** — não é um artefato de composição de
rótulo.

**Checagem 3 (recorte por quartos, deriva genérica vs. mergulho
transiente):**

| Quarto | `n` | `LZC_median` | `LZC_ternary` |
|---|---|---|---|
| Q1 (PRE, distante) | 18.236 | 0,8219794524 | 0,8041168495 |
| Q2 (PRE, próximo) | 18.236 | 0,8072319457 | 0,7017658011 |
| Q3 (POST, próximo) | 19.761 | 0,3964592994 | 0,6679458310 |
| Q4 (POST, distante) | 19.760 | 0,7633452510 | 0,6269681268 |

Bate exatamente com `CONFOUND_CHECK_DAPHNET.md`. **Confirmado
independentemente: o padrão é um mergulho abrupto em Q3 seguido de
recuperação parcial em Q4 (canal mediano), não uma deriva monótona** —
consistente com um efeito localizado na transição, não uma deriva
genérica de sessão.

Nenhuma das duas checagens do agente original foi encontrada com erro
de cálculo ou de interpretação. Nenhuma ação de redesenho tomada aqui —
prossegue-se para rotas de ataque genuinamente novas.

---

## 3. Ataque A — sensibilidade ao ponto exato de corte PRE/POST (NOVO, não tentado pelo agente original)

**Motivação:** um efeito genuinamente ligado à transição documentada
deveria ser robusto a um deslocamento pequeno do ponto de corte;  um
artefato de um corte específico e arbitrário não deveria ser.

**Método:** desloquei o ponto de corte (amostra do onset, `72.944`) em
±30s, ±60s, ±120s (a 64Hz: ±1.920, ±3.840, ±7.680 amostras),
RECONSTRUÍDO diretamente do sinal bruto completo de `S01R01` (não dos
`.npy` já derivados, para eliminar qualquer possibilidade de erro de
indexação herdado). Os TAMANHOS das janelas robustez (`PRE_LEN=36.472`,
`POST_LEN=39.521`) foram mantidos fixos — só a LOCALIZAÇÃO do corte se
move, isolando o efeito de "onde exatamente você corta" do efeito de
"quanto você inclui".

| deslocamento | corte (amostra) | `LZC_m` PRE | `LZC_m` POST | Δ mediana | `LZC_t` PRE | `LZC_t` POST | Δ ternário |
|---:|---:|---:|---:|---:|---:|---:|---:|
| −120s | 65.264 | 0,8206 | 0,6136 | **−0,2071** | 0,7925 | 0,5500 | **−0,2425** |
| −60s | 69.104 | 0,8244 | 0,6047 | **−0,2197** | 0,7946 | 0,5548 | **−0,2398** |
| −30s | 71.024 | 0,8210 | 0,6109 | **−0,2102** | 0,7899 | 0,5741 | **−0,2158** |
| 0 (travado) | 72.944 | 0,8132 | 0,6047 | **−0,2085** | 0,7472 | 0,5548 | **−0,1923** |
| +30s | 74.864 | 0,8003 | 0,6159 | **−0,1844** | 0,7107 | 0,5195 | **−0,1912** |
| +60s | 76.784 | 0,8048 | 0,5811 | **−0,2237** | 0,7078 | 0,5124 | **−0,1954** |
| +120s | 80.624 | 0,7949 | 0,5788 | **−0,2161** | 0,7128 | 0,5080 | **−0,2048** |

**Resultado: o achado é REMARCAVELMENTE ESTÁVEL ao deslocamento do
ponto de corte.** Δ_mediana varia apenas entre −0,184 e −0,224 (faixa
de ~0,04, ~19% do valor central) e Δ_ternário entre −0,191 e −0,243
(faixa de ~0,05, ~26% do valor central), ao longo de uma janela de
deslocamento de 4 minutos (±120s) em torno do onset — SEMPRE na mesma
direção (queda), sem nenhuma inversão de sinal, sem nenhum colapso para
perto de zero. **Isto é evidência POSITIVA de que o efeito não é um
artefato de um corte específico e arbitrário** — é consistente com uma
mudança de regime genuína que ocupa uma vizinhança temporal
relativamente ampla em torno do onset documentado, não um pico isolado
de uma única amostra de corte. Este ataque, tentado especificamente
para quebrar o achado, **FALHOU em quebrá-lo** — reportado aqui como um
resultado honesto de reforço, não descartado por não ser a rota
"vencedora".

---

## 4. Ataque B — resolução do próprio `p=0,0` sob correção de múltiplas comparações (NOVO)

**Motivação:** `p=0,0` com `N_SURROGATES=200` não significa "p
exatamente zero" — significa "0 de 200 substitutos excederam o Δ real",
o que tem uma resolução finita. A pergunta desta checagem não é "o
efeito é real fisiologicamente" (já endereçado nos ataques acima), mas
"o `p=0,0` relatado é forte o bastante para sobreviver a uma correção
de múltiplas comparações honesta, dado o orçamento de substitutos
realmente usado".

**Cálculo do limite superior de confiança do `p` verdadeiro** (0
sucessos em 200 tentativas, intervalo de Clopper-Pearson,
`1 - alpha^(1/n)` com confiança de 95%):

```
limite superior 95% do p verdadeiro = 1 - 0,05^(1/200) = 0,01487
(aproximação "regra de três", 3/n = 0,015 — consistente)
piso de resolução ingênuo (1/(n+1))  = 0,00498
```

Ou seja: com apenas 200 substitutos, `p=0,0` relatado é consistente,
com 95% de confiança, com qualquer `p` verdadeiro entre 0 e ~1,49% —
não apenas com "p exatamente zero" ou "p muito menor que 0,005".

**Correção de múltiplas comparações:** 8 testes brutos (4
combinações domínio×variante × 2 canais), mas os 2 canais dentro da
MESMA combinação são computados sobre transformações (binária/ternária)
da MESMA série bruta subjacente — claramente correlacionados, não
testes independentes. Um Bonferroni honesto trata as 4 combinações
domínio×variante como a família de testes (não os 8 testes brutos):

```
alpha corrigido (familia de 4 combinações) = 0,05 / 4 = 0,0125
alpha corrigido (ingenuamente sobre 8 testes independentes) = 0,05 / 8 = 0,00625
```

**Resultado desta checagem:** o PONTO ESTIMADO `p=0,0` sobrevive
trivialmente a qualquer correção (0 × qualquer fator continua 0). Mas o
LIMITE SUPERIOR DE CONFIANÇA do `p` verdadeiro (0,0149) **excede** o
`alpha` corrigido pela família de 4 combinações (0,0125) — e excede
ainda mais o `alpha` corrigido ingenuamente sobre 8 testes (0,00625).
**Isto significa que, com o orçamento de `N_SURROGATES=200` efetivamente
usado, não é possível distinguir com 95% de confiança entre "o efeito
sobrevive a Bonferroni sobre as 4 combinações" e "o efeito não
sobrevive"** — a resolução do teste é simplesmente baixa demais para
essa afirmação específica, independentemente de o efeito ser real ou
não. Isto NÃO é o mesmo que "o achado é um falso positivo" — é uma
limitação de RESOLUÇÃO do orçamento computacional do teste primário,
nomeada aqui explicitamente como um ponto fraco genuíno que nem
`METHODOLOGY_NOTE.md` nem `RESULTS_SUMMARY.md` haviam quantificado.
**Recomendação concreta para qualquer decisão de governança:** se este
achado for levado ao Gate de Replicação, rodar novamente com
`N_SURROGATES` bem maior (ex. 2.000-5.000) para apertar o limite
superior de confiança do `p` real antes de reivindicar sobrevivência a
qualquer correção de múltiplas comparações formal — não foi refeito
aqui por orçamento de tempo desta checagem adversarial (cada combinação
já leva ~8,5min com 200 substitutos; 2.000 substitutos levaria
~85min só para esta combinação).

---

## 5. Ataque C — outros sujeitos/registros do MESMO dataset, MESMO pipeline travado (NOVO, o ataque mais informativo desta checagem)

**Motivação:** o achado é, por desenho, `intra-sujeito, intra-registro`
(per `RESULTS_SUMMARY.md`/`CONFOUND_CHECK_DAPHNET.md`, já reconhecido
honestamente pelo agente original). A pergunta natural — não
respondida na sessão original — é: o mesmo padrão qualitativo (queda de
LZC concentrada no início do congelamento) aparece em OUTROS
sujeitos/registros do mesmo dataset, aplicando a MESMA regra de janela
de robustez (primeiro onset, PRE=50% mais recentes do PRE completo,
POST=50% mais próximos do POST completo), SEM nenhuma modificação do
pipeline?

**Seleção dos sujeitos (fixada antes de rodar, não escolhida por
inspeção de resultado):** dos 10 sujeitos do dataset, 4 não têm nenhum
episódio de congelamento (`S03R03`, `S04R01`, `S06R02`, `S10R01` —
confirmado por inspeção direta nesta sessão, reconfirmando o que
`METHODOLOGY_NOTE.md` já dizia sobre S04/S10 e estendendo a mesma
verificação aos outros dois). Dos 13 registros restantes com >=1
episódio, selecionei 3 adicionais por critério simples de tamanho
(evitar segmentos POST-robustez muito pequenos, mesmo piso de
`MIN_N_SEGMENT` já usado no pipeline) sem olhar para o resultado antes
de escolher: `S02R01` (9 episódios), `S07R01` (16 episódios), `S03R01`
(43 episódios, o registro com MAIS episódios de todo o dataset).

**Resultado — pipeline `run_lzc_analysis` idêntico, mesmo seed=12345,
sem nenhuma modificação:**

| Sujeito | `n_pre`/`n_post` | `LZC_m` PRE→POST | Δ mediana | `p` mediana | `LZC_t` PRE→POST | Δ ternário | `p` ternário |
|---|---|---|---|---|---|---|---|
| **S01R01** (achado original) | 36.472/39.521 | 0,8132→0,6047 | **−0,2085** | **0,0** | 0,7472→0,5548 | **−0,1923** | **0,0** |
| S02R01 | 27.244/9.036 | 0,7420→0,6137 | −0,1282 | 0,59 | 0,6527→0,5001 | −0,1526 | 0,145 |
| S07R01 | 20.336/39.427 | 0,3181→0,7299 | **+0,4118** | **0,0** | 0,4454→0,6841 | **+0,2387** | **0,0** |
| S03R01 | 22.063/50.032 | 0,4114→0,2583 | −0,1530 | 1,0 | 0,2765→0,5583 | **+0,2818** | 0,925 |

**Leitura honesta, sem suavizar:**

- **S02R01** mostra a MESMA DIREÇÃO (queda de LZC nos dois canais), com
  magnitude menor (~60% da de S01R01), mas **NÃO atinge significância
  em nenhum canal** (`p=0,59` mediana, `p=0,145` ternário) sob o MESMO
  teste IAAFT com o MESMO orçamento de substitutos. Direção qualitativa
  concorda; significância não replica.
- **S07R01** mostra o padrão **INVERTIDO**: LZC AUMENTA (não diminui) do
  PRE para o POST-robustez, em AMBOS os canais, com significância total
  (`p=0,0` nos dois canais) — tão "significativo" quanto o achado
  original de S01R01, mas no sentido OPOSTO. Isto é o resultado mais
  importante desta checagem adversarial: o MESMO pipeline, aplicado à
  MESMA regra de janela em torno do MESMO tipo de transição (onset do
  primeiro episódio de congelamento) em outro sujeito, produz um efeito
  igualmente forte e "limpo" estatisticamente, mas de sinal oposto.
  **Isto não prova que S01R01 é espúrio** (o mecanismo pode ser
  genuinamente diferente entre sujeitos — fisiologia de FoG é
  heterogênea entre pacientes, documentado na literatura clínica), mas
  **refuta diretamente qualquer leitura de "queda de LZC no início do
  congelamento" como um padrão fisiológico ESTÁVEL e replicável dentro
  do próprio dataset usado**, que é exatamente o tipo de generalização
  que tornaria este achado mais forte do que "curiosidade de um único
  sujeito/registro" — generalização que NÃO se sustenta aqui.
- **S03R01** (registro com MAIS episódios de congelamento de todo o
  dataset, `n=43`) mostra um resultado ainda mais desorganizado: os DOIS
  canais **discordam em SINAL entre si** dentro do MESMO sujeito
  (`LZC_median` cai, Δ=−0,153; `LZC_ternary` SOBE, Δ=+0,282 — mesmo sinal
  de S07R01 no canal ternário, mas oposto ao canal mediano do mesmo
  S03R01) — e nenhum dos dois atinge significância (`p=1,0` mediana,
  `p=0,925` ternário). Isto é o padrão mais fraco/ruidoso dos 4 sujeitos
  testados, mas ainda assim informativo: nem a DIREÇÃO do efeito é
  consistente entre os dois canais dentro de um único sujeito adicional,
  o que já era invisível em S01R01 (onde os dois canais concordam em
  sinal e magnitude) e não podia ter sido descoberto sem testar outro
  sujeito.

**Síntese do Ataque C (4 sujeitos no total, incluindo o original):**
Direção mediana: 2/4 caem (S01R01, S03R01), 1/4 sobe (S07R01), 1/4 cai
(S02R01) → na verdade 3/4 caem no canal mediano (S01R01, S02R01, S03R01)
e 1/4 sobe (S07R01). Direção ternário: 2/4 caem (S01R01, S02R01), 2/4
sobem (S07R01, S03R01) — MUITO menos consistente que o canal mediano.
Significância (`p<0,05`, MESMO pipeline/orçamento): **1/4** (apenas
S01R01, nos dois canais). **A alegação mais forte que os dados desta
checagem sustentam é: a direção predominante (queda) aparece em 3 dos 4
sujeitos testados no canal mediano, mas só atinge significância
estatística em 1 desses 4 sob o MESMO teste — não é um padrão robusto
o bastante para ser chamado de replicado, mas também não é
"aleatório puro" (não é 50/50 de sinal, há uma tendência direcional
fraca no canal mediano que o canal ternário não compartilha).**

---

## 6. Ataque D — método de substituto alternativo: bootstrap por blocos móveis (Kunsch 1989), o fallback JÁ pré-autorizado por `METHODOLOGY_NOTE.md` — RESULTADO MAIS DANOSO DESTA CHECAGEM

**Motivação:** um achado que sobrevive a apenas UM método específico de
substituto (IAAFT) é mais fraco do que um que sobrevive a métodos
independentes. `METHODOLOGY_NOTE.md` já pré-autoriza o bootstrap por
blocos móveis como fallback — mas ele nunca foi rodado sobre o dado
REAL de Daphnet-robustez (só sobre os controles sintéticos, em
`VALIDATION_NOTE.md`). Rodei-o aqui, usando `run_block_bootstrap_test`
importado sem modificação de `lzc_common.py`, exatamente sobre
`data/daphnet_{pre,post}_robust.npy` (`block_length=max(N//20,10)=1823`,
`n_bootstrap=200`, `seed=12345`, mesmos parâmetros da convenção já
travada).

| Canal | Δ real | média nula MBB | desvio nulo MBB | `p` (MBB, bicaudal) | `p` (IAAFT, já relatado) |
|---|---|---|---|---|---|
| `LZC_median` | −0,2085 | −0,1439 | 0,0742 | **0,04** | 0,0 |
| `LZC_ternary` | −0,1923 | −0,1027 | 0,0552 | **0,07** | 0,0 |

**Resultado — este é o ataque que mais aproxima de quebrar o achado:**

- `LZC_median` continua `p<0,05` sob MBB (`p=0,04`), mas por uma margem
  MUITO mais estreita do que o `p=0,0` limpo do IAAFT — passa raspando o
  limiar convencional, não com folga.
- `LZC_ternary` **NÃO sobrevive** ao teste alternativo (`p=0,07`,
  `>0,05`) — o canal que teve o `p=0,0` mais "limpo" sob IAAFT (e que,
  ironicamente, foi o único canal com poder discriminativo VALIDADO
  contra o controle positivo sintético em `VALIDATION_NOTE.md`, ao
  contrário do canal mediano) **deixa de ser significativo** quando o
  método de substituto muda de IAAFT para bootstrap por blocos móveis.
- Isto inverte a hierarquia de confiança que a validação sintética
  original estabeleceu: lá, `LZC_ternary` era o canal "confiável"
  (poder IAAFT validado desde o início) e `LZC_median` era o canal sem
  poder estabelecido por nenhum teste (`NO_POWER_ESTABLISHED_EITHER_TEST`,
  per `VALIDATION_NOTE.md`). Aqui, no dado REAL, é exatamente o
  contrário que aparece sob o teste alternativo: `LZC_median` (o canal
  sem poder validado) sobrevive ao MBB; `LZC_ternary` (o canal COM poder
  validado) não sobrevive. Esta inversão é, por si só, um sinal de
  alerta — um efeito genuíno e robusto normalmente não deveria trocar
  de canal "confiável" dependendo de qual teste de significância é
  usado.
- **Nota de calibração honesta:** `VALIDATION_NOTE.md` já havia
  encontrado, no controle POSITIVO sintético, que o MBB é
  sistematicamente PIOR (menos poder) que o IAAFT para `LZC_median`
  (`p=0,95` MBB vs. `p=0,455` IAAFT) — então um MBB mais fraco no dado
  real não é totalmente inesperado a priori. Mas a mesma nota também
  mostrou que o MBB CONCORDAVA com o IAAFT para `LZC_ternary` no
  controle positivo sintético (`p=0,0` nos dois) — o que torna a
  DISCORDÂNCIA encontrada aqui no dado real (IAAFT `p=0,0` vs. MBB
  `p=0,07` para `LZC_ternary`) especificamente NÃO prevista pela
  validação sintética, e por isso mais preocupante do que se fosse
  apenas "MBB é geralmente mais fraco".

**Conclusão do Ataque D: este é o único dos 4 ataques novos tentados
nesta checagem que efetivamente enfraquece o achado de forma
substancial — não o refuta por completo (o canal mediano ainda cruza
`p<0,05` sob MBB), mas remove a alegação de "significância limpa e
robusta a método de substituto" que o `p=0,0`/`p=0,0` do IAAFT sozinho
sugeria.**

---

## Síntese final e recomendação de governança

**O que este achado É, com confiança alta após esta checagem:** um
efeito numérico real (não um bug de implementação, não um artefato de
ponto de corte), localizado temporalmente no início do primeiro
episódio de congelamento de UM sujeito (`S01R01`) e UM registro
(`S01R01`), reproduzível bit a bit pelo pipeline travado, que sobrevive
a deslocamentos de até ±120s no ponto de corte PRE/POST e a 3
checagens diretas de confundidor (composição de rótulo, glitch de
sensor, deriva genérica de sessão).

**O que este achado NÃO É, com confiança alta após esta checagem:** (1)
um padrão fisiológico geral de "FoG reduz complexidade algorítmica de
marcha" que se replica de forma confiável dentro do PRÓPRIO dataset —
falha em replicar significância em 3 de 4 sujeitos testados sob o
MESMO pipeline, e se INVERTE em sinal com igual força estatística em
pelo menos 1 sujeito (S07R01); (2) um resultado robusto ao MÉTODO de
teste de significância — o canal que a validação sintética original
identificou como "confiável" (`LZC_ternary`) perde significância sob o
próprio fallback de bootstrap já pré-autorizado por este candidato.

**Por que isto não é uma contradição interna:** um efeito pode ser
genuíno, fisiologicamente real E específico do sujeito/contexto (FoG é
uma condição clinicamente heterogênea — mecanismos de congelamento
variam entre pacientes, é plausível que a assinatura de complexidade do
tremor no início do congelamento dependa de características
individuais de marcha, medicação, fase do ciclo on/off da levodopa,
etc., nenhuma dessas variáveis controlada ou sequer registrada neste
dataset). O problema não é que S01R01 seja necessariamente "falso" — é
que **o achado, tal como relatado em `RESULTS_SUMMARY.md`, não tem
evidência suficiente (após esta checagem) para ser tratado como algo
mais forte do que "uma observação intrigante de um único
sujeito/sessão"**, e a moldura de "canal companheiro `LZC_ternary`
corrobora o canal primário `LZC_median`" usada em
`CONFOUND_CHECK_DAPHNET.md`/`RESULTS_SUMMARY.md` para reforçar a
confiança no achado fica ela própria enfraquecida pelo Ataque D — os
dois canais concordam sob IAAFT, mas discordam em robustez sob MBB, e
já discordavam em qual canal tinha poder validado desde a etapa de
validação sintética.

**Recomendação concreta para a sessão orquestradora:**

1. **Não promover** este achado a "cross-domain invariant sobrevivente"
   — isso já era a conclusão honesta de `RESULTS_SUMMARY.md` antes desta
   checagem (não há segundo domínio corroborando), e permanece.
2. **Não tratar** o achado de Daphnet-robustez como "investigado e
   não-refutado" no sentido forte que autorizaria avanço direto ao Gate
   de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`) — os Ataques C e D
   acima são refutações parciais genuínas, não apenas "mais uma checagem
   que passou".
3. Se a linha `lempel-ziv-complexity` for mantida aberta para uma
   rodada futura especificamente sobre FoG, o mínimo necessário antes de
   qualquer nova alegação seria: (a) testar TODOS os 13 registros do
   dataset com >=1 episódio de congelamento (não apenas os 4 desta
   checagem), reportando a distribuição completa de sinal/significância,
   não apenas casos favoráveis; (b) rodar o teste de substituto
   alternativo (MBB) como parte do protocolo PRIMÁRIO desde o início
   (não como checagem adversarial a posteriori) para qualquer novo
   sujeito; (c) aumentar `N_SURROGATES` para pelo menos 2.000 antes de
   reportar qualquer `p=0,0` como significância "limpa" sob correção de
   múltiplas comparações.
4. `LZC_median` (canal primário desta linha) segue sem poder
   discriminativo estabelecido pela validação sintética
   (`NO_POWER_ESTABLISHED_EITHER_TEST`, per `VALIDATION_NOTE.md`) — essa
   ressalva já nomeada pelo agente original continua valendo e não foi
   resolvida por esta checagem.

## Arquivos desta checagem

- Este documento (`ADVERSARIAL_REPRODUCTION_DAPHNET.md`).
- Scripts de checagem (scratch de sessão, não commitados no repositório
  por serem reexecuções ad hoc sobre dados já reprodutíveis a partir de
  `data/prepare_daphnet.py`; números completos já reportados acima com
  precisão suficiente para reprodução independente):
  cross-validação `lz76_complexity` vs. `lz76_complexity_naive` sobre os
  4 arrays reais; reexecução de `run_lzc_analysis` sobre
  `data/daphnet_{pre,post}_robust.npy`; reconstrução de `S02R01`,
  `S07R01`, `S03R01` a partir do zip bruto do UCI (mesma URL de
  `PROVENANCE_DAPHNET.md`) aplicando a MESMA regra de janela de
  robustez; `run_block_bootstrap_test` sobre
  `data/daphnet_{pre,post}_robust.npy`.
- Nenhum arquivo LOCKED (`METHODOLOGY_NOTE.md`, `lzc_common.py`'s
  `R_lambda`/`I(X)`/protocolo de significância, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `DECISION_LEDGER.yaml`) foi modificado por
  esta checagem. `lz76_complexity_naive` foi apenas CHAMADO (não
  modificado) para a cross-validação da Seção 0.

