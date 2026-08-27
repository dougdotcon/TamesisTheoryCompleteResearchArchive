# Relatório adversarial — reexecução independente (passo 7, `AGENTS.md`)

**Test ID:** `DISC-SCHUMANN-RESONANCE-001`
**Papel:** revisor adversarial, agente separado do que produziu
`RESULTS_PRIMARY.md` (`00_GOVERNANCE/AGENTS.md` §"Separação de papéis").
Instruído explicitamente a tentar refutar o achado, não confirmá-lo.
**Data:** 2026-08-27.
**Disciplina seguida:** todo código deste relatório foi escrito do zero.
`analysis/compute_psd.py`, `analysis/download_segments.py` e
`analysis/range_zip.py` (o código da frente original) **não foram lidos**
em nenhum momento desta revisão — nem antes, nem depois de produzir meus
próprios resultados. Onde meus números batem com os da frente, é
reprodução independente genuína, não cópia.
**Artefatos deste relatório** (todos em `adversarial/`):
- `referee_byte_order_check.py` + saída — tarefa 1.
- `referee_psd.py` + `referee_run.log` + `referee_results.json` — tarefa 3
  (reprodução completa dos 6 casos) e tarefa 4 (sensibilidade a `nperseg`).
- `referee_extra_checks.py` + `referee_extra_checks.log` — tarefas 6, 7, 8.
- `referee_provenance_spotcheck.py` — re-download independente de 2
  arquivos brutos diretamente do Zenodo (implementação própria de leitor
  HTTP Range + `zipfile`, escrita do zero) — tarefa 8 (spot-check de
  proveniência). Requer rede e o pacote `requests` para reexecutar.

---

## Veredito

```
VEREDITO ADVERSARIAL: SOUND WITH NAMED ISSUES
```

Reproduzi do zero, com código próprio, os 6 pares canal×segmento e obtive
**concordância exata** (frequência do pico, potência do pico, contagem e
lista de máximos locais genuínos na banda de tolerância, e proeminência —
esta última batendo a 4 casas decimais assim que adoto a leitura literal
"mediana da vizinhança ±1 Hz" incluindo o próprio bin do pico, que é a
convenção que a frente de fato usou). **Não encontrei nenhum erro
numérico, nenhum dado fabricado, e nenhuma violação de proveniência.** A
determinação de little-endian é sólida e não-circular; a taxa de
amostragem e o formato binário (16 bits) são verificados por evidência
interna do próprio dado (não dependem de nenhuma fonte externa); e o único
parâmetro não-verificável nesta revisão (a escala ±10 V, citada de um
resumo de artigo pago) provei ser **irrelevante ao resultado** — o teste
pré-registrado é invariante a essa escolha de escala (Tarefa 8).

Dois problemas reais, não-fatais, nenhum deles tocando o critério travado
nem os números da tabela principal, foram encontrados e são registrados
como "named issues" abaixo — daí `SOUND WITH NAMED ISSUES`, não `CONFIRMED`
sem ressalvas. Além disso, dou meu próprio veredito de leitura sobre a
ambiguidade textual NÃO DISTINGUE vs. FALSIFICA que a própria
`RESULTS_PRIMARY.md` já expõe (Tarefa 5) — é uma questão de interpretação
sobre um documento que nem eu nem o agente da análise primária escrevemos,
não um erro numérico de nenhum dos lados.

---

## Tarefa 1 — Determinação de byte order (little-endian vs. big-endian)

**Método:** decodifiquei `data/raw/2014-01-15/NS/smplGRTU1_sensor_0_1401150054`
(921.600 amostras, 1.843.200 bytes) das duas formas com `numpy.frombuffer`,
sem depender de nenhuma lógica do código da frente.

| | LE (meu) | LE (frente) | BE (meu) | BE (frente) |
|---|---|---|---|---|
| média (V) | −0,287254 | ≈−0,287 | 0,022103 | ≈0,022 |
| desvio (V) | 0,233618 | ≈0,234 | 5,768616 | ≈5,769 |
| min/max (V) | −7,3715/7,3270 | — | **−10,0000/9,9997** | — |
| fração no limite ±32767/−32768 | 0,0000% | — | 0,0322% | — |

`10/√3 = 5,773503` — o desvio BE (5,7686) bate com a assinatura de ruído
uniforme de bytes trocados, exatamente como alegado. O mín/máx BE batendo
em −10,0000 exato e +9,9997 (= 32767×10/32768, o valor máximo
representável em complemento de dois assimétrico — não uma imprecisão, é
o que "saturação de 16 bits assimétrica" deveria produzir) confirma
clipping genuíno sob BE, ausente sob LE.

**Diagnóstico adicional, não usado pela frente (verificação não-circular
própria):** autocorrelação lag-1. Um sinal analógico real de banda
5–10 Hz amostrado a 256 Hz deve ter autocorrelação lag-1 alta (amostras
adjacentes, separadas por ~3,9 ms, devem ser fortemente correlacionadas);
ruído de bytes trocados não deve ter nenhuma. Resultado (2 arquivos,
2 segmentos/canais distintos):

| Arquivo | LE lag-1 autocorr | BE lag-1 autocorr |
|---|---|---|
| `2014-01-15/NS/…0054` | **0,6819** | 0,0005 |
| `2014-07-15/EW/…0057` | **0,8417** | −0,0017 |

Isto é um critério totalmente independente das estatísticas de
amplitude já citadas pela frente, e aponta na mesma direção com folga
enorme (0,68–0,84 vs. ~0,0). **Conclusão da tarefa 1:** a determinação de
little-endian é sólida, não-circular, e agora corroborada por um segundo
critério estrutural independente. Nenhum problema encontrado.

---

## Tarefa 2 — Taxa de amostragem

Inspecionei os 144 arquivos `_info.txt` (cobertura completa, não amostra):
**todos os 144** têm `sampling period (usec): 3906.000000` e
`number of samples: 921600`; **todos** os 144 arquivos de dado binário têm
exatamente 1.843.200 bytes = 2×921.600 (confirma 16 bits/amostra
independentemente de qualquer alegação de literatura — é aritmética pura
sobre o tamanho do arquivo). `fs = 1e6/3906 = 256,0163850486431 Hz`
(verificado em Python com `repr()` de ponto flutuante — bate dígito a
dígito com `PROVENANCE.md`). `64×fs = 16385,0486…` — `round()` e `floor()`
dão ambos `16385`; `ceil()` dá `16386`. **Conclusão da tarefa 2: correto,
sem ressalvas, com cobertura 100% (não apenas amostragem) dos arquivos.**

---

## Tarefa 3 — Reprodução independente completa dos 6 casos (`referee_psd.py`)

Script próprio (`analysis/{compute_psd,download_segments,range_zip}.py` da
frente **não lidos** antes nem depois): carrega os 24 arquivos/canal em
ordem cronológica (ordenação lexicográfica do nome do arquivo — verificado
manualmente que produz ordem cronológica correta em todos os 6 casos, já
que o minuto inicial é fixo dentro de cada mês), decodifica `int16`
little-endian, escala por `10/2^15` V/LSB, concatena, roda
`scipy.signal.welch(..., window='hann', nperseg=round(64×fs),
noverlap=nperseg//2, detrend='constant', scaling='density')`.

**Resultado — meus números vs. os da frente (`data/results_primary.json`):**

| Segmento | Canal | Pico (Hz) — meu | Pico (Hz) — frente | Dentro da banda? | Proeminência — meu | Proeminência — frente |
|---|---|---|---|---|---|---|
| 2014-01-15 | NS | 8,03127384284422 | 8,03127384284422 | Sim / Sim | 1,2213 | 1,221 |
| 2014-01-15 | EW | 7,81252319342823 | 7,81252319342823 | Sim / Sim | 1,3344 | 1,334 |
| 2014-04-15 | NS | 7,90627347174937 | 7,90627347174937 | Sim / Sim | 1,3194 | 1,319 |
| 2014-04-15 | EW | 7,87502337897566 | 7,87502337897566 | Sim / Sim | 1,4415 | 1,442 |
| 2014-07-15 | NS | 7,93752356452308 | 7,93752356452308 | Sim / Sim | 1,3251 | 1,325 |
| 2014-07-15 | EW | 8,50002523444992 | 8,50002523444992 | **Não** / **Não** | 1,3595 | 1,360 |

**Concordância bit-a-bit** em frequência do pico, potência do pico,
determinação dentro/fora da banda, e na lista completa + contagem de
"máximos locais genuínos" (bin estritamente maior que os dois vizinhos
imediatos) em todos os 6 casos — comparação automatizada
(`referee_results.json` vs. `data/results_primary.json`) confirma 6/6 sem
nenhuma divergência acima de `1e-9`. A proeminência bate a 3–4 casas
decimais assim que adoto a convenção "mediana do bin do pico + vizinhos
±1 Hz, **incluindo** o próprio bin do pico" (testei explicitamente:
excluir o próprio bin dá 1,2270 em vez de 1,2213 para o primeiro caso —
diferença de ~0,5%, não muda nenhum veredito, mas a convenção
**inclusiva** é a que reproduz os números publicados exatamente, e é
também a leitura mais literal de "mediana da vizinhança ±1 Hz" no texto
do pré-registro, que não menciona excluir o pico da própria vizinhança).

**Conclusão da tarefa 3:** reprodução independente bem-sucedida e exata
em todos os 6 casos. Não consegui refutar nenhum número da tabela
principal apesar de tentar ativamente (código novo, convenção de
proeminência testada nos dois sentidos, contagem completa de máximos
locais).

---

## Tarefa 4 — Sensibilidade a `nperseg`

**Leitura textual:** "`nperseg` = amostras equivalentes a 64 segundos na
taxa real confirmada" não especifica arredondamento. Testei `round`,
`floor` e `ceil`:

- `round(64×fs) = floor(64×fs) = 16385` (a parte fracionária 0,0486 já
  arredonda para baixo) — **não há ambiguidade prática aqui**: as duas
  leituras mais naturais do texto ("arredondar" e "tomar quantas amostras
  cabem inteiras em 64s") convergem para o mesmo `nperseg`.
- `ceil(64×fs) = 16386` (1 amostra a mais): recomputei os 6 casos —
  frequência do pico desloca no máximo 0,0005 Hz, proeminência muda no
  máximo ~1% relativo, **nenhum veredito muda de lado da banda de
  tolerância ou do limiar de 3×**.

**Teste de robustez adicional, além do pedido (não uma leitura textual
válida de "64 segundos" — um estresse deliberado com janela de 32s, metade
do valor travado, para checar se o resultado é frágil a escolhas de
parâmetro em geral):** com `nperseg = round(32×fs) = 8193`, 5 dos 6 casos
não mudam de lado da banda; mas o **único caso fora da banda no resultado
primário** (`2014-07-15/EW`, 8,50 Hz) **muda para dentro da banda**
(7,9683 Hz) sob essa janela mais curta. Isto **não é uma violação do
pré-registro** — 64s está inequivocamente especificado e as duas leituras
textualmente válidas (`round`/`floor`) concordam exatamente — mas é um
achado de robustez relevante: o único caso "fora da tolerância" do
resultado primário está em cima do fio, sensível a uma escolha de janela
que o pré-registro não sanciona. Isto **reforça**, não enfraquece, a
leitura de que o conjunto de 6 casos deveria ser tratado como "não
resolvido" — um resultado robustamente `SUPORTA` ou robustamente
`FALSIFICA` não deveria virar de lado com uma mudança razoável (mas não
pré-registrada) de parâmetro.

**Conclusão da tarefa 4:** nenhuma ambiguidade real em `nperseg=16385`
dado o texto travado; a única fragilidade encontrada (o caso limítrofe
`2014-07-15/EW`) é evidência a favor, não contra, do enquadramento "não
distingue" da frente.

---

## Tarefa 5 — Adjudicação da ambiguidade textual (NÃO DISTINGUE vs. FALSIFICA)

A frente já expôs a ambiguidade de forma honesta (`RESULTS_PRIMARY.md`
§4) — não a inventou, e a apresentou como questão aberta para este
revisor, com ambos os números crus dados. Meu papel aqui é dar um
veredito de leitura próprio, deixando claro que é uma interpretação de um
documento que nenhum de nós dois escreveu (a sessão orquestradora
escreveu), não um erro numérico.

**Leitura adotada pela frente:** FALSIFICA exige ausência de **qualquer**
máximo local genuíno na banda; "não distingue" cobre "máximo local existe,
mas proeminência <3×". Isto faz do critério de três vias uma partição
bem-fundada (existência de pico × limiar de proeminência, duas condições
ortogonais).

**Leitura alternativa (mais estrita):** "pico distinguível de ruído de
fundo" na cláusula de FALSIFICA é sinônimo de "proeminência ≥3×" (a
mesma métrica operacionalizada na cláusula seguinte), colapsando as duas
cláusulas.

**Meu veredito de leitura:** por pura fidelidade textual — o que as
palavras mais plausivelmente significam, isoladas de considerações de
utilidade estatística — eu pendo levemente para a leitura **adotada pela
frente** ser a mais textualmente coerente. Razão principal: o documento
usa deliberadamente uma linguagem diferente nas duas cláusulas ("pico
distinguível de ruído de fundo" vs. "proeminência... é inferior a 3×") —
se o autor quisesse que FALSIFICA fosse "proeminência <3× em todo lugar",
já tinha o vocabulário exato disponível na cláusula seguinte e não o
usou. Uma leitura que colapsa as duas cláusulas em uma única condição
quantitativa torna a cláusula de "não distingue" logicamente inatingível
por construção (nunca haveria um caso em que "existe pico mas
proeminência <3×" fosse uma categoria distinta de FALSIFICA) — o que é
estranho para um documento que se deu ao trabalho de escrever três
categorias paralelas e nomeadas.

**Mas** — e isto é um problema real na redação do pré-registro em si, não
no resultado da frente — a leitura adotada tem uma fraqueza séria que a
`RESULTS_PRIMARY.md` não menciona: sob médias pesadas (aqui, 2698
segmentos de Welch por caso), "existe um bin estritamente maior que os
dois vizinhos imediatos" é uma condição estatisticamente **quase trivial**
de satisfazer em qualquer banda com dezenas de bins, mesmo sob um fundo
puramente monótono ou 1/f sem nenhuma ressonância real — basta ruído
residual de estimação suficiente para criar ondulações locais. Verifiquei
isto empiricamente: a banda `[6,70, 8,35]` Hz tem ~106 bins
(`(8,35−6,70)/0,015625`), e a frente encontrou entre 20 e 27 "máximos
locais genuínos" por caso — cerca de 1 em cada 4–5 bins, consistente com o
que ruído residual sobreposto a **qualquer** tendência suave produziria,
com ou sem ressonância real. Sob a leitura adotada, FALSIFICA fica quase
impossível de disparar para qualquer dataset real minimamente ruidoso —
um critério de falsificação que quase nunca pode ser acionado é uma
fraqueza de desenho, não uma vantagem. Isto não é uma crítica ao trabalho
da frente (nem meu, nem dela — nenhum de nós escreveu o pré-registro),
mas é uma observação que deveria ir para o registro: **a Seção 5 do
pré-registro, como escrita, tem uma zona cinzenta genuína entre suas
próprias cláusulas, e a leitura mais textualmente defensável é também a
que deixa o ramo FALSIFICA quase vazio de conteúdo operacional.** Reporto
isto explicitamente para julgamento futuro, sem reformular o critério
retroativamente (o que seria uma violação de `AGENTS.md`).

**Resumo da tarefa 5:** ambas as leituras concordam que SUPORTA não se
aplica em nenhum dos 6 casos — isto não é uma questão de interpretação, é
aritmética (nenhuma proeminência atinge 3×). A escolha entre NÃO DISTINGUE
e FALSIFICA é genuinamente uma questão de interpretação textual do
pré-registro, não um erro de nenhum dos dois agentes; minha leitura pessoal
pende para NÃO DISTINGUE ser a mais fiel ao texto como escrito, mas
reconheço que a leitura estrita (FALSIFICA) tem um argumento de fundo
igualmente sério a seu favor, ligado a uma fraqueza pré-existente na
redação do critério, não a uma manipulação por parte de nenhum agente.

---

## Tarefa 6 — Sanity check do "morro largo" (`referee_extra_checks.py`)

Método independente, não usado pela frente: ajustei uma lei de potência
suave em log-log (`log(psd) ~ a·log(f) + b`) usando **apenas** pontos
claramente fora do "morro" alegado (2,0–5,3 Hz e 10,7–13,0 Hz), e comparei
o valor real da PSD em ~7,83 Hz e no vale (~10–11 Hz) contra essa
extrapolação suave.

| Segmento/Canal | Excesso @7,83Hz vs. fundo suave | Vale vs. fundo suave |
|---|---|---|
| 2014-01-15 NS | 2,032× | 0,820× (abaixo do fundo) |
| 2014-01-15 EW | 2,578× | 0,601× |
| 2014-04-15 NS | 2,924× | 0,752× |
| 2014-04-15 EW | 2,681× | 0,476× |
| 2014-07-15 NS | 3,222× | 0,814× |
| 2014-07-15 EW | 2,136× | 0,658× |

Em todos os 6 casos: (a) a PSD real em ~7,83 Hz excede a extrapolação de
um fundo suave por 2,0×–3,2×, e (b) o vale logo depois cai **abaixo** do
mesmo fundo suave extrapolado (0,48×–0,82×). Um fundo puramente monótono
ou de lei de potência pura não produziria esse padrão de subida-acima e
queda-abaixo — é a assinatura clássica de uma feição espectral localizada
genuína sobreposta/entalhada no contínuo, não um artefato de vazamento
espectral ou tendência 1/f. Isto é evidência independente **a favor** da
caracterização qualitativa "morro largo real" de `RESULTS_PRIMARY.md` §3,
por um método diferente do usado por qualquer um dos dois agentes.

Nota adicional: o excesso medido por este método (2,0×–3,2×) é maior que
a proeminência ±1 Hz medida pela frente (1,22×–1,44×) — exatamente
consistente com a própria explicação da frente de que a janela ±1 Hz
mecanicamente capta o ombro do próprio morro, achatando a razão medida.
Meu método, com uma janela de "ruído de fundo" mais distante e mais larga,
recupera um excesso maior, sem usar nenhuma lógica do pré-registro para
isso. **Conclusão da tarefa 6:** a caracterização "morro largo real, não
artefato" se sustenta sob um método de verificação independente.

---

## Tarefa 7 — Checagem dos harmônicos (`referee_extra_checks.py`)

**Reprodução exata dos números da frente:** recalculando
`potência(bin mais próximo de 14,000/21,000 Hz) / potência(pico modo 1)`
a partir de `data/results_primary.json`, obtenho a faixa real
**2,31×–18,43×** (não "2 a 15×" como o texto de `RESULTS_PRIMARY.md` §3
afirma — ver Issue 1 abaixo).

**Achado adverso real:** ao fazer uma busca de máximo local **na mesma
janela** que o método do pico primário usa (janela de ±2 Hz em torno de
14/21 Hz, em vez de olhar só o bin mais próximo de um número redondo), a
potência encontrada nas regiões 12–16 Hz e 19–23 Hz é, em vários casos,
**muito maior** e concentrada em um pico extremamente estreito perto de
~15,14–15,20 Hz (não 14,0 Hz), presente **nos 6 casos**, com razão contra
o modo 1 variando de 6,6× a **161,7×** (`2014-07-15/EW`). Inspecionei a
forma bruta dessa feição (`data/raw`, PSD em torno de 15,0–15,3 Hz): é um
pico de 1–2 bins de largura (≈0,03–0,05 Hz), consistente com um tom de
banda estreita genuíno, não ruído de estimação — muito mais estreito que
o "morro largo" físico de baixa qualidade esperado para o modo 2 de
Schumann (que na literatura tem largura de alguns Hz, como o modo 1).
Também há uma subida acentuada perto de 16,67 Hz (≈50/3 Hz, possível
subarmônico de rede elétrica de 50 Hz — não confirmado, reportado apenas
como coincidência numérica sugestiva) e uma subida acentuada perto da
borda superior da banda calibrada (24,9–25,0 Hz, borda declarada de
calibração do instrumento no pré-registro) em quase todos os casos — mais
plausivelmente um efeito de borda de filtro/calibração do que sinal real.

**Isto não contamina o resultado primário** — verifiquei explicitamente
que a banda de busca 5–10 Hz (a única usada pelo critério travado) não
tem nenhuma feição espectral tão estreita quanto essas (os "máximos
locais genuínos" na tabela da frente sobem e descem suavemente, sem saltos
de bin-a-bin de 5–150× como os vistos em 15,1–15,2 Hz). Mas significa que
a checagem de contexto "harmônicos claramente mais fortes, como esperado
fisicamente" de `RESULTS_PRIMARY.md` §3 é construída sobre um método
(bin mais próximo de um número redondo) inconsistente com o método usado
para o pico primário (busca de máximo em janela), e não menciona a
existência de uma feição de interferência muito mais forte e estreita
perto de 15,1–15,2 Hz que — se fosse tratada com o mesmo método de busca
usado para o modo 1 — dominaria qualquer caracterização de "modo 2". Ver
Issue 2 abaixo.

**Conclusão da tarefa 7:** a afirmação qualitativa "modo 1 não é confundido
com harmônicos mais fortes" continua verdadeira (a banda 5–10 Hz está
limpa dessas feições estreitas), mas a checagem de harmônicos como
apresentada é mais fraca e menos completa do que o texto sugere, e contém
uma inconsistência numérica com o próprio JSON (Issue 1).

---

## Tarefa 8 — Proveniência, integridade, e o parâmetro não-verificável (±10 V)

**Spot-check de re-download independente** (script próprio, HTTP Range +
`zipfile` sobre um `io.RawIOBase` customizado, escrito do zero sem ler
`analysis/range_zip.py`): busquei o diretório central do `2014.zip`
diretamente do Zenodo (`https://zenodo.org/api/records/6348691/files/2014.zip/content`,
`Content-Length` confirmado = 26.697.876.825 bytes, batendo com
`PROVENANCE.md`), localizei e baixei **dois** arquivos específicos
independentemente (um de `2014-01-15/NS`, um de `2014-07-15/EW`), e
comparei byte-a-byte com as cópias locais em `data/raw/`:

| Arquivo | CRC32 remoto (novo download) | CRC32 local | SHA256 idênticos? |
|---|---|---|---|
| `.../1401150054` | `aff253f9` | `aff253f9` | **Sim** |
| `.../1407151257` | `0605ecb2` | `0605ecb2` | **Sim** |

33.815 entradas no diretório central confirmadas, batendo com
`PROVENANCE.md`. **Nenhum dado fabricado — os bytes locais são
genuinamente os bytes do Zenodo.**

**Metadados do registro Zenodo, confirmados por fetch direto próprio (API
JSON):** título "Four-year measurements from Sierra Nevada ELF station.
Year 2014", DOI `10.5281/zenodo.6348691`, licença `cc-by-4.0`,
`access_right: open`, tamanho do arquivo e MD5 batendo exatamente com
`PROVENANCE.md`. A descrição do registro (buscada nesta revisão)
confirma independentemente "0 for NS, 1 for EW" e "~1,8 MB por arquivo
horário" — bate com a alegação da frente.

**Tabela 1 do Toledo-Redondo et al. (2022), JGR Atmospheres — a âncora
numérica de toda a banda de tolerância:** busquei via `WebFetch`
independentemente (não confiando na alegação de "verificado por fetch
direto" do pré-registro) e confirmei: NS = "6.80" a "8.35" Hz, EW = "6.70"
a "8.22" Hz — bate exatamente com `[6,70, 8,35]` Hz travado na Seção 5.
**Não é um número inventado.**

**Bloqueio de paywall genuíno, não uma desculpa:** tentei eu mesmo acessar
o ScienceDirect (Salinas et al. 2022) e o mirror `digibug.ugr.es` — recebi
`403 Forbidden` e timeout, respectivamente, os mesmos obstáculos
declarados por `PROVENANCE.md`. **O parâmetro de escala ±10 V (16 bits,
1 bit de sinal + 15 de amplitude) permanece não-verificável nesta revisão
por essa mesma razão.**

**Achado tranquilizador, verificado empiricamente (não pedido
explicitamente, mas necessário para avaliar o risco real desse parâmetro
não-verificado):** recomputei os 6 casos usando as contagens brutas do
ADC (`int16`, sem nenhuma conversão para volts) em vez da série escalada
por `10/2^15`. **Frequência do pico e razão de proeminência são idênticas
bit-a-bit** nos 6 casos — esperado, já que a busca de pico dominante e a
proeminência (razão pico/mediana) são invariantes a qualquer reescala
positiva uniforme do sinal. **Ou seja: o único parâmetro desta análise
sourced de uma fonte não-verificável (o valor exato ±10 V) não pode, por
construção matemática, afetar o resultado do teste pré-registrado** — só
afeta a unidade (V) dos números de potência reportados, não a frequência
do pico nem se ela cai dentro da banda, nem a proeminência. O único
parâmetro que de fato importa e não vem de literatura (byte order) foi
verificado de forma independente e não-circular na Tarefa 1; o único
parâmetro que vem de literatura (escala em volts) foi verificado como
irrelevante ao resultado nesta tarefa.

**Ordem trava-antes-de-rodar:** `git diff ec42b65 -- PREREGISTRATION.md`
retorna vazio — o pré-registro não foi alterado desde o commit de trava
(`ec42b65`, 2026-08-27 13:58:19 UTC). `RESULTS_PRIMARY.md`, `analysis/` e
`data/` estão não-commitados (`git status`), consistente com trabalho
aguardando integração pela sessão orquestradora.

**Consistência JSON ↔ prosa:** conferida campo a campo para os 6 casos
(frequência, potência, proeminência, `in_tolerance_band`,
`all_local_maxima_in_band`) — **nenhuma divergência**, exceto a já citada
na Tarefa 7/Issue 1 (faixa de harmônicos "2 a 15×" vs. faixa real
2,31×–18,43×).

**Conclusão da tarefa 8:** nenhuma lacuna de proveniência real
encontrada. O único gap genuíno (escala ±10 V não-confirmável por
paywall) é honestamente declarado pela frente **e** provado nesta revisão
como irrelevante ao resultado do teste.

---

## Issues nomeados

### Issue 1 — Faixa de razão de harmônicos na prosa não bate com o próprio JSON (Severidade: LOW)

`RESULTS_PRIMARY.md` §3 afirma "a potência perto de 14 Hz e 21 Hz é de
**2 a 15 vezes** maior que a potência no pico do modo 1". Recalculando
diretamente de `data/results_primary.json` (`harmonics_check`/
`global_dominant_peak_5_10Hz`), a faixa real é **2,31×–18,43×** — dois dos
6 casos (`2014-01-15/EW`: 16,32×; `2014-04-15/EW`: 18,43×) excedem o "15"
citado no texto.

**Por que é LOW:** não afeta nenhum número da tabela principal, nem o
veredito de nenhum canal/segmento — é puramente uma imprecisão de
arredondamento na prosa de contexto, provavelmente um "quase 15,
arredondado para baixo" sem checagem final contra o JSON.
**Recomendação:** corrigir a frase para "2 a 18 vezes" ou citar a faixa
exata.

### Issue 2 — Checagem de harmônicos usa método mais fraco que o do pico primário e não menciona uma feição de interferência mais forte perto de 15,1–15,2 Hz (Severidade: MODERATE)

O "harmonics_check" da frente mede a potência no bin **mais próximo de
14,000 Hz e 21,000 Hz exatos** — não uma busca de máximo em janela, ao
contrário do método usado para achar o próprio pico do modo 1 (que
percorre toda a banda 5–10 Hz). Refazendo com o mesmo método de busca de
janela (±2 Hz em torno de 14/21 Hz), encontrei, nos 6 casos, uma feição
espectral **muito mais estreita e muito mais forte** perto de
15,1–15,2 Hz (não 14 Hz), com razão contra o pico do modo 1 chegando a
**161,7×** em um caso (`2014-07-15/EW`) — bem acima da faixa "2–15×"/
"2,3–18,4×" citada para o bin fixo. A largura (~1–2 bins, ≈0,03–0,05 Hz) é
inconsistente com um "morro largo" físico de Schumann (que deveria ter
alguns Hz de largura, como o próprio modo 1) e mais consistente com uma
linha de interferência de banda estreita (elétrica ou instrumental) não
relacionada à ressonância de Schumann. Também há indícios de uma subida
acentuada perto de ~16,67 Hz (coincidência numérica com 50/3 Hz, não
confirmada como causa) e perto da borda superior da banda calibrada do
instrumento (24,9–25,0 Hz, plausivelmente um efeito de borda de
filtro/calibração).

**Por que é MODERATE e não invalida o veredito travado:** (a) a banda de
busca pré-registrada é exclusivamente 5–10 Hz, e verifiquei explicitamente
que essa banda está livre desse tipo de feição estreita em todos os 6
casos — a comparação pico-a-pico da Tarefa 3 usa o método correto e já
está bit-a-bit reproduzida; (b) a checagem de harmônicos em si é
declarada pelo próprio pré-registro apenas como contexto qualitativo
("claramente separado... dos picos do 2º/3º modo"), não como parte do
critério numérico de decisão da Seção 5. **Recomendação:** se
`RESULTS_PRIMARY.md` §3 for citado no futuro, qualificar a checagem de
harmônicos como um "bin único perto de um número redondo", não uma
varredura completa da região 12–25 Hz, e nomear explicitamente a
existência de uma feição de interferência não-Schumann mais forte
próxima — que não ameaça o resultado primário, mas merece investigação
própria se este dataset for reutilizado (ex. para um futuro teste sobre o
2º modo de Schumann especificamente).

### Issue 3 (informativo, não um erro) — O único caso "fora da banda" é sensível a uma escolha de janela não travada pelo pré-registro (Severidade: LOW, reforça o veredito "não distingue" em vez de contradizê-lo)

Ver Tarefa 4: `2014-07-15/EW` (8,50 Hz, fora de `[6,70, 8,35]` por
0,15 Hz sob a janela de 64s travada) move-se para dentro da banda
(7,97 Hz) sob uma janela de 32s — uma escolha que o pré-registro não
sanciona nem proíbe explicitamente, mas que também não é a leitura mais
natural de "64 segundos". Não é uma violação de proveniência nem um erro
de cálculo (a janela de 64s travada foi implementada corretamente e sem
ambiguidade prática, como mostrado na Tarefa 4) — é registrado aqui como
contexto de robustez, não como problema a corrigir.

---

## Resumo para `TEST_QUEUE.yaml` / `CLAIM_LEDGER.yaml`

- **Critério travado (Seção 5 do pré-registro): números da tabela
  principal CONFIRMADOS**, reproduzidos independentemente do zero,
  bit-a-bit idênticos em frequência de pico, potência, determinação
  dentro/fora da banda de tolerância, e lista completa de máximos locais
  genuínos, nos 6/6 pares canal×segmento. Nenhuma proeminência atinge o
  limiar de 3× em nenhum caso — confirmado independentemente. SUPORTA não
  se aplica em nenhum caso sob nenhuma leitura textual.
- **Veredito geral da revisão adversarial: `SOUND WITH NAMED ISSUES`** —
  1 issue LOW (Issue 1, faixa de harmônicos imprecisa na prosa), 1 issue
  MODERATE (Issue 2, checagem de harmônicos metodologicamente mais fraca
  que o método primário e não menciona uma interferência de banda
  estreita mais forte perto de 15,1–15,2 Hz — não toca o critério
  travado), 1 nota informativa (Issue 3, robustez do caso limítrofe).
- **Byte order, taxa de amostragem, formato binário e proveniência do
  download:** todos verificados independentemente nesta revisão, com
  métodos e/ou re-downloads próprios não usados pela frente. Nenhum dado
  fabricado, nenhuma citação inventada, nenhuma violação de proveniência.
- **O único parâmetro não-verificável nesta revisão (escala ±10 V,
  sourced de resumo de artigo pago) foi provado matematicamente
  irrelevante ao resultado do teste pré-registrado** (invariância de
  escala confirmada empiricamente nos 6 casos).
- **Ambiguidade textual NÃO DISTINGUE vs. FALSIFICA (Seção 5): genuína,
  não inventada por nenhum agente.** Meu veredito de leitura pessoal
  pende levemente para NÃO DISTINGUE como a leitura mais textualmente
  coerente (Tarefa 5), mas nomeio explicitamente que a leitura estrita
  (FALSIFICA) tem um argumento de fundo sério a seu favor — a leitura
  adotada deixa o ramo FALSIFICA quase inatingível sob médias pesadas de
  Welch, uma fraqueza de desenho do pré-registro em si, não do agente que
  o executou nem desta revisão. Ambas as leituras concordam, sem
  ambiguidade, que **SUPORTA não se aplica** em nenhum dos 6 casos.
- Ordem trava-antes-de-rodar confirmada (`git diff` vazio contra o commit
  de trava). Nenhum sinal de reformulação de critério pós-hoc.
