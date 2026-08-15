# Descoberta adversarial de nulos — `DISC-TRI-RG-001`, candidato `dfa-multiscale-entropy`, domínio PhysioNet Apnea-ECG `a04`

**Papel:** agente de destruição (Extensão de Metodologia 5). Objetivo: tentar
explicar o achado (`alpha` cai ~0,94→0,81; `alpha1` sobe ~0,76→1,33; `alpha2`
cai ~1,01→0,65; 6/6 testes de bootstrap por blocos `p<0,05`) por qualquer
mecanismo mundano, SEM invocar nenhum ingrediente de invariante cross-domain
via renormalização.

**Veredito resumido:** o achado ISOLADO em `a04` (fisiologia) **sobrevive**
a todas as tentativas de destruição por artefato que testei — não é
tamanho de amostra, não é contaminação por batimento ectópico/erro de QRS,
e não é uma deriva lenta monotônica de "mais tarde na noite". Mas ele
**não sobrevive como evidência de invariante cross-domain**: (a) o próprio
domínio pareado desta linha (GISP2/paleoclima, calculado com o MESMO
pipeline não modificado) não mostra efeito robusto — 5 de 6 testes de
bootstrap não significativos, e o único nominal (`p=0,042`) tem sinal
OPOSTO ao seu próprio par primário/robustez; e (b) existe um mecanismo
fisiológico específico, mundano e já bem documentado na literatura
(variação cíclica da frequência cardíaca — CVHR — durante apneia
obstrutiva) que explica a direção, e aproximadamente a escala, do efeito
inteiro sem qualquer ingrediente de RG. Ou seja: replicação de fisiologia
conhecida, não descoberta de física nova cross-domain — e o teste
cross-domain que a linha exige já falhou com os próprios dados que a
linha gerou.

---

## 1. Ataque por tamanho de amostra (rota 2 do mandato) — REJEITADO

`compute_alphas` de `dfa_common.py` (importado sem modificação) foi rodado
sobre pares PRE/POST sintéticos de fGn (gerador Davies-Harte de
`validate_synthetic.py`, também sem modificação) com o MESMO `H` fixo dos
dois lados (sorteios independentes — nulo verdadeiro, nenhuma mudança real
de correlação), usando os tamanhos de amostra EXATOS dos segmentos reais:
`N_pre=2747` / `N_post=9195` (primária) e `N_pre=1373` / `N_post=4597`
(robustez). 150 repetições por `H` ∈ {0,5; 0,70; 0,76; 0,87; 0,94}, cobrindo
o intervalo observado nos dados reais.

Resultado (script: `null_discovery_size_mismatch_test.py`, dados completos
em `null_discovery_size_mismatch_result.json`):

| Variante | Canal | `Delta` real | média do nulo (só desequilíbrio de N) | desvio do nulo | `z` |
|---|---|---:|---:|---:|---:|
| primária (2747 vs 9195) | `alpha` | -0,134 | ~-0,002 | ~0,03–0,04 | -3,2 a -4,4 |
| primária | `alpha1` | +0,569 | ~0,00–0,01 | ~0,02–0,03 | **+18,6 a +23,2** |
| primária | `alpha2` | -0,366 | ~0,00–0,01 | ~0,05–0,07 | -5,5 a -7,7 |
| robustez (1373 vs 4597) | `alpha` | -0,169 | ~0,00 | ~0,04–0,05 | -3,3 a -4,2 |
| robustez | `alpha1` | +0,334 | ~0,015–0,017 | ~0,03–0,04 | **+7,1 a +10,9** |
| robustez | `alpha2` | -0,346 | ~0,00–0,01 | ~0,06–0,08 | -4,2 a -5,6 |

(intervalo de `z` cobre os 5 valores de `H` testados; controle adicional
com `N` IGUAL dos dois lados, `H=0,87`, mostrou o mesmo padrão de nulo
centrado em zero com `std` pequeno — confirma que o desvio não é um
artefato genérico de estimação de `alpha`, mas especificamente NÃO
reproduzido por desequilíbrio de `N`).

**Conclusão desta rota:** o desequilíbrio de tamanho de amostra por si só
produz uma distribuição nula de `Delta alpha/alpha1/alpha2` centrada em
~0 com desvio padrão de poucas centésimas — muito menor que os deltas
reais observados (`z` de 3 a 23 dependendo do canal/variante, robusto à
escolha de `H` de referência). **A rota de tamanho de amostra não
sobrevive como explicação** — corrobora, por um método independente
(nulo sintético de forma explícita, não apenas o bootstrap já reportado
em `result_apnea_a04.json`), o mesmo veredito de significância que o
pipeline original já tinha calculado.

## 2. Ataque por contaminação de batimento ectópico/erro de QRS (rota 3) — REJEITADO, e na direção ERRADA

Inspeção direta dos RR brutos extraídos via `wfdb` (script
`null_discovery_rr_diagnostics.py`, rodado sobre `a04.qrs`/`a04.apn` reais,
sem modificar `dfa_common.py`):

- **PRE** (N=2747): fração de saltos sucessivos de RR >20% = **2,69%**;
  saltos >50% = **1,64%**.
- **POST** (N=9195): fração de saltos >20% = **1,06%**; saltos >50% =
  **0,69%**.
- Checagem de duplicação de batimento perdido (RR próximo de 2× a
  mediana local, assinatura clássica de falha de detecção): **zero**
  ocorrências em ambos os segmentos. Checagem de detecção espúria (RR
  próximo de 0,5× a mediana): PRE=0,36% (10/2747), POST=0,076% (7/9195) —
  **PRE tem mais**, não menos.

Ou seja: **o segmento PRE tem MAIS saltos grandes e MAIS candidatos a
detecção espúria que o POST**, o oposto do que a hipótese de "apneia
causa mais erro de detecção de QRS, inflando `alpha1`" precisaria para
ser verdadeira.

Corroborado de forma independente por um teste computacional já presente
no repositório (`result_apnea_a04_adversarial.json`,
`adversarial_2_winsorized`, winsorização de 1% nos extremos de RR — uma
forma padrão de neutralizar exatamente esse tipo de contaminação por
outlier): winsorizar **NÃO reduz** o efeito — ele fica mais forte:

| | `alpha1` PRE | `alpha1` POST | `Delta alpha1` |
|---|---:|---:|---:|
| sem winsorização (resultado primário) | 0,760 | 1,328 | +0,569 |
| winsorizado 1% | 0,796 | **1,488** | **+0,692** |

Se o salto de `alpha1` fosse artefato de outliers/ectópicos, removê-los
deveria ATENUAR o efeito. Ele se INTENSIFICA. **Esta rota está morta.**

## 3. Ataque por tendência lenta/hora da noite (rota 4) — parcialmente rejeitado, mas com uma lacuna estrutural genuína não resolvida

### 3a. O efeito aparece quase imediatamente após o início da apneia, não como deriva lenta

Já presente no repositório (`result_apnea_a04_adversarial.json`,
`adversarial_1_truncated_post`): truncar o POST para apenas os **primeiros
12 minutos** após o início do rótulo de apneia (N=794, vs. 140 min/N=9195
do primário) já reproduz a maior parte do efeito:

| | PRE (N=2747) | POST truncado a 12 min (N=794) | POST completo (N=9195, referência) |
|---|---:|---:|---:|
| `alpha1` | 0,760 | **1,239** | 1,328 |
| `alpha2` | 1,013 | **0,574** | 0,648 |

E a decomposição em 4 sub-blocos não sobrepostos de ~35 min cada dentro do
POST (`adversarial_3_boundary_subblocks`) mostra o efeito estável ao
longo de toda a janela de 140 min, sem tendência monotônica clara de
"aprofundamento" com o tempo:

| sub-bloco (min desde início da noite) | `alpha1` | `alpha2` |
|---|---:|---:|
| [35,70] | 1,148 | 0,724 |
| [70,105] | 1,393 | 0,410 |
| [105,140] | 1,360 | 0,457 |
| [140,175] | 1,312 | 0,653 |

Isso pesa CONTRA uma deriva circadiana lenta e monotônica como explicação
única: o salto já está quase completo nos primeiros 12 minutos, e não
cresce de forma monotônica pelo resto da noite.

### 3b. Mas: não existe controle "mais tarde na noite, ainda sem apneia" dentro deste registro — e a literatura mostra que estágio do sono, por si só, já é um confundidor forte e documentado para DFA

Levantamento completo dos rótulos minuto-a-minuto de `a04.apn`
(`null_discovery_rr_diagnostics.py`):

```
N  [0, 34]     35 min   <- PRE
A  [35, 174]  140 min   <- POST
N  [175, 176]   2 min
A  [177, 461] 285 min
N  [462, 463]   2 min
A  [464, 491]  28 min
```

Depois da transição em 35 min, o resto da noite (mais de 7 horas) é quase
inteiramente rotulado `A`, com apenas dois blocos `N` de 2 minutos —
curtos demais para um DFA independente confiável. **Não há como construir,
dentro de `a04`, um segmento "mais tarde na noite, ainda sem apneia" para
isolar hora-da-noite de apneia como variável.** Essa é uma limitação
estrutural genuína do registro escolhido, não resolvida por nenhum teste
computacional possível sobre este único registro.

Mais importante: Penzel, Kantelhardt, Becker, Peter, Bunde (2003),
*"Detrended Fluctuation Analysis and Spectral Analysis of Heart Rate
Variability for Sleep Stage and Sleep Apnea Identification"*, Computers in
Cardiology 30:307-310 — o artigo-irmão do IEEE TBME 50(10):1143-51 citado
no `METHODOLOGY_NOTE.md`, mesmo grupo, mesmos parâmetros DFA (`alpha1`,
`alpha2`, chamados `c1`/`c2` no texto) — relatou que **os parâmetros de DFA
separam ESTÁGIO DO SONO melhor do que separam SEVERIDADE DE APNEIA**:
78,4% de acerto para estágio do sono (85,0% com medidas de domínio do
tempo) contra apenas 60,1% para severidade de apneia (74,4% com domínio
do tempo). Ou seja, a própria literatura fundadora deste método mostra que
mudança de estágio do sono (leve→profundo→REM→acordado) é, no mínimo, um
confundidor tão forte quanto apneia para `alpha1`/`alpha2`.

**Consequência direta:** a base PhysioNet Apnea-ECG (usada aqui) não tem
NENHUMA anotação de estágio do sono (só rótulo `N`/`A` derivado de
respiração/SpO2). A transição PRE→POST em `a04` é, com altíssima
probabilidade fisiológica, TAMBÉM uma transição de estágio/profundidade do
sono (os primeiros 35 min de uma noite tipicamente incluem o início do
sono/estágios mais leves; 140 min de apneia severa contínua tipicamente
vêm acompanhados de repetidos micro-despertares e fragmentação de sono que
alteram a composição de estágio). **Isso não pode ser separado de "efeito
específico de apneia" usando somente `a04`** — é uma lacuna honesta, não
uma refutação, mas deveria estar declarada explicitamente ao lado do
resultado, não apenas implícita na limitação de "apneia é um processo
cíclico" já registrada no `METHODOLOGY_NOTE.md`.

## 4. Mecanismo mundano específico encontrado: variação cíclica da frequência cardíaca (CVHR) contaminando exatamente a faixa de escala do DFA

Análise espectral direta dos intervalos RR brutos (FFT do RR centrado na
média, banda de período 15-200 batimentos — a mesma vizinhança onde
`alpha1`/`alpha2` são calculados, fronteira em `n=16`):

| | Período dominante (batimentos) | Período (segundos, RR médio do segmento) | Potência na banda [15,200] / potência total |
|---|---:|---:|---:|
| PRE | ~70–153 (fraco, disperso) | ~53–116 s | **18,3%** |
| POST | **~41–48** (pico dominante, muito nítido) | **~38–44 s** | **73,7%** |

A potência absoluta do pico dominante do POST é ~100-150× maior que
qualquer pico equivalente no PRE. O período (~40 s) é consistente com a
frequência de eventos documentada do próprio registro: AHI=77,4/h implica
um evento de apneia/hipopneia a cada **~46,5 s em média** — exatamente na
mesma vizinhança do período espectral dominante medido diretamente na
série de RR do POST.

Isto é a assinatura clássica de **variação cíclica da frequência cardíaca
(cyclical variation of heart rate, CVHR)**, descrita originalmente por
Guilleminault et al. (1984, *Lancet* 1:126-131 — citada como referência
[5] no próprio Penzel et al. 2003) e usada há décadas como método clínico
independente de detecção de apneia obstrutiva a partir do próprio ECG.
Fisiologicamente: bradicardia durante a apneia seguida de taquicardia no
despertar/retomada da respiração, repetindo a cada ciclo apneia-hipopneia.

Essa oscilação quase-periódica, ao contaminar exatamente a janela de
escala `n~20-60` usada pelo DFA (fronteira `alpha1`/`alpha2` em `n=16`, e
`alpha2` primário cobrindo `n` de 21 a 2298), é um mecanismo MUNDANO
conhecido e suficiente, por si só, para produzir o padrão observado: em
escalas curtas (`alpha1`, `n<=16`, bem menor que o período de ~44
batimentos), a série parece localmente lisa/persistente dentro de uma
única rampa do ciclo — inflando `alpha1` para bem acima de 1; em escalas
que cruzam ou excedem o período do ciclo (`alpha2`, `n>=20`), a
recorrência do ciclo introduz um platô/crossover no ajuste log-log que
reduz a inclinação ajustada — depressão de `alpha2`. Este é exatamente o
padrão qualitativo observado (`alpha1` sobe fortemente, `alpha2` cai).
Nenhum ingrediente de renormalização cross-domain é necessário para essa
explicação — é fisiologia cardiorrespiratória já documentada há 40 anos.

## 5. Checagem cross-domain (o que a linha `DISC-TRI-RG-001` realmente exige) — FALHA, com os próprios dados já calculados pela linha

O ponto anterior por si só já reduziria o achado a "replicação de
fisiologia conhecida". Mas o teste mais direto contra a alegação de
INVARIANTE CROSS-DOMAIN é comparar com o segundo domínio já calculado
pela mesma linha, com o MESMO pipeline não modificado:
`result_gisp2_dfa.json` (paleoclima GISP2, transição Younger
Dryas→Preboreal).

| GISP2 | `Delta alpha` | `p_bootstrap_alpha` | `Delta alpha1` | `p_bootstrap_alpha1` | `Delta alpha2` | `p_bootstrap_alpha2` |
|---|---:|---:|---:|---:|---:|---:|
| primária | +0,362 | **0,126** (n.s.) | +0,082 | **0,466** (n.s.) | +0,538 | **0,506** (n.s.) |
| robustez | +0,196 | **0,458** (n.s.) | -0,030 | **0,042** (sig., mas sinal OPOSTO ao primário) | +0,011 | **0,996** (n.s.) |

Comparando com fisiologia (`a04`, todos 6 testes `p<0,05`, maioria
`p<0,001`, mesmo sinal em primária e robustez para cada canal): o domínio
pareado GISP2 mostra **5 de 6 testes de bootstrap não significativos**, e
o único nominalmente significativo (`alpha1` robustez, `p=0,042`) tem
sinal invertido em relação ao seu próprio par primário (não significativo)
— exatamente o padrão que se espera de ruído cruzando `p=0,05` por acaso
em múltiplas comparações, não de um efeito real e replicável.

**Isso é decisivo para o objetivo desta linha especificamente.**
`DISC-TRI-RG-001` não está testando "será que DFA muda com apneia" (já
sabido) — está testando se a MESMA fórmula `I(X)`, aplicada sem
reformulação em domínios fisicamente distintos, revela um invariante
comum via a lente de renormalização. Um efeito forte e consistente em UM
domínio e ausente/não replicável no outro domínio já calculado pela
própria linha é, por definição, o oposto de um invariante cross-domain —
é evidência de um efeito específico de domínio (fisiologia
cardiorrespiratória), não de física de RG universal.

## 6. Viés de seleção / look-elsewhere (rota 5) — não resolvido, honestamente sinalizado

`METHODOLOGY_NOTE.md` documenta que registros de backup (`a18`, `a14`,
`a01`) foram "mapeados para replicação futura" mas — até onde os arquivos
neste diretório mostram — nenhum deles foi de fato levado a um cálculo
final. Isto significa que:

- Apenas UM registro fisiológico (`a04`) foi computado até resultado
  final e reportado.
- O processo de busca que encontrou `a04` (agente de busca dedicado,
  conforme `METHODOLOGY_NOTE.md` "Contexto") plausivelmente inspecionou
  múltiplos registros candidatos antes de fixar este; não há um log
  quantitativo de quantos registros foram checados nem que critério de
  "transição limpa" foi aplicado ANTES de ver o resultado de `a04`
  especificamente.
- Isso não invalida o resultado em `a04` (que sobreviveu a todas as
  checagens de artefato acima), mas significa que a MAGNITUDE do efeito
  em `a04` não deve ser tratada como representativa sem replicação
  pré-registrada em pelo menos um dos registros de backup — exatamente
  o que o próprio `METHODOLOGY_NOTE.md` já promete e ainda não entregou.

## 7. Veredito final

| Rota de ataque | Resultado |
|---|---|
| (2) desequilíbrio de tamanho de amostra | **Rejeitada** — nulo sintético com N idêntico ao real não produz efeito comparável (z=3 a 23) |
| (3) contaminação por ectópico/erro de QRS | **Rejeitada, e invertida** — PRE tem mais saltos/outliers que POST; winsorização FORTALECE o efeito |
| (4a) deriva lenta monotônica | **Rejeitada** — efeito já quase completo em 12 min, sem tendência monotônica nos 140 min |
| (4b) confusão com estágio do sono | **Não resolvida — lacuna estrutural genuína**, sustentada pela própria literatura (Penzel 2003: DFA separa estágio do sono MELHOR que apneia) e pela ausência de qualquer segmento `N` longo tardio em `a04` para controle |
| Mecanismo mundano positivo (CVHR) | **Encontrado e quantificado** — oscilação de ~40 s domina 74% da potência espectral do POST na banda relevante para o DFA, consistente com AHI=77,4/h e com literatura de 1984 em diante |
| (1) já é conhecido, não é novidade | **Sim, como efeito fisiológico isolado** — mecanismo e direção plausivelmente explicados por CVHR já documentado; nenhuma citação encontrada replica exatamente estes números em `a04`, mas a CLASSE de efeito (DFA muda com apneia, direção de `alpha1`/`alpha2` já disputada por sub-banda na literatura, conforme o próprio `METHODOLOGY_NOTE.md` já reconhece ao declarar teste bicaudal) não é nova |
| Invariante cross-domain (o que `DISC-TRI-RG-001` exige) | **FALHA** — domínio pareado GISP2, mesmo pipeline, 5/6 testes de bootstrap não significativos e o único significativo com sinal invertido |
| (5) viés de seleção do registro | **Não resolvido** — apenas 1 registro computado até o fim; backups mapeados mas não rodados |

**Recomendação para a linha:** o resultado em `a04` pode continuar sendo
reportado honestamente como um resultado fisiológico robusto (sobrevive a
ataques de artefato), mas NÃO deveria ser usado, isoladamente, para
avançar `DISC-TRI-RG-001` rumo a `CANDIDATE_LOCKED`/pré-registro como
evidência de invariante cross-domain — o próprio segundo domínio já
calculado pela linha (GISP2) contradiz essa leitura. Qualquer síntese
futura desta linha precisa reportar a falha de replicação cross-domain
(`Seção 5` acima) com o mesmo peso dado ao sucesso do teste de bootstrap
em fisiologia, e precisa endereçar explicitamente o confundidor de
estágio do sono (`Seção 3b`) antes de qualquer alegação de que o efeito é
"apneia" e não "apneia + fragmentação do sono associada".

---

## Apêndice: proveniência dos artefatos computacionais

- `null_discovery_size_mismatch_test.py` — script que gera o nulo
  sintético de desequilíbrio de tamanho de amostra (Seção 1), importando
  `dfa_common.compute_alphas` e `validate_synthetic.davies_harte_fgn` sem
  modificação.
- `null_discovery_size_mismatch_result.json` — saída numérica completa do
  script acima (todos os `H`, ambas as variantes de tamanho, controle de
  tamanho igual).
- `null_discovery_rr_diagnostics.py` — script que extrai RR brutos de
  `a04.qrs`/`a04.apn` via `wfdb`, reconstrói a sequência completa de
  rótulos minuto-a-minuto (Seção 3b), calcula diagnóstico de saltos/
  duplicação de batimento (Seção 2) e a análise espectral de periodicidade
  CVHR (Seção 4).
- `result_apnea_a04_adversarial.json` — já presente no repositório antes
  desta sessão (reprodução independente/"cega" do resultado primário mais
  3 variantes adversariais: POST truncado a 12 min, winsorização 1%,
  decomposição em 4 sub-blocos); reutilizado aqui nas Seções 2 e 3a sem
  modificação, não gerado por este agente.
- `result_apnea_a04.json`, `result_gisp2_dfa.json`,
  `validation_synthetic.json` — resultados oficiais da linha, lidos mas
  não modificados; a Seção 5 é uma leitura adversarial nova destes
  arquivos já existentes (nenhum número novo foi calculado para o GISP2 —
  os `p_bootstrap_*` citados já estavam no JSON oficial, apenas não
  haviam sido comparados lado a lado com os 6/6 significativos da
  fisiologia em nenhum documento de síntese existente).
