# Resultado primário — Pico espectral da ressonância de Schumann na estação ELF de Sierra Nevada

**Test ID:** `DISC-SCHUMANN-RESONANCE-001`
**Pré-registro (LOCKED):** `PREREGISTRATION.md`, travado em 2026-08-27
(`DISC-DEC-102`). Este documento reporta o resultado exatamente como saiu
da execução da análise pré-registrada — nenhuma reformulação de hipótese,
estatística de teste, banda de tolerância, ou critério de falsificação foi
feita depois de ver o dado real.
**Data de execução:** 2026-08-27.
**Código:**
- `analysis/range_zip.py` — leitor HTTP Range seekable para `zipfile`.
- `analysis/download_segments.py` — seleção e extração do subconjunto real.
- `analysis/compute_psd.py` — análise pré-registrada (Welch PSD + critério
  de decisão da Seção 5).
**Resultados numéricos completos:** `data/results_primary.json`.
**Proveniência completa:** `data/PROVENANCE.md`. **Dado bruto local:**
`data/raw/<segmento>/<NS|EW>/` (144 arquivos binários + 144 `_info.txt`).
**Manifesto de download (offsets, CRC32, sha256, texto integral de cada
`_info.txt`):** `data/manifest.json`.
**Gráficos:** `data/plots/psd_<segmento>_<canal>.png` (6 arquivos).

> **Este é o resultado da análise primária (não-adversarial), executado por
> um único agente.** Por `00_GOVERNANCE/AGENTS.md` passo 7, ele **não pode**
> ser catalogado como fechado até que um segundo agente, instruído a tentar
> refutá-lo, reexecute a análise de forma independente (código próprio,
> mesma proveniência de dado) — essa reexecução **não** foi feita por este
> agente/sessão.

---

## Veredito

```
VEREDITO (todos os 3 segmentos × 2 canais): NÃO DISTINGUE
```

Em nenhum dos 6 pares canal×segmento testados o pico dominante da PSD na
janela 5–10 Hz atinge o limiar de proeminência ≥3× exigido pela Seção 5 do
pré-registro para SUPORTA. Ao mesmo tempo, em todos os 6 pares existe um
máximo local genuíno (um "morro" real na PSD, não um artefato de borda de
janela) dentro da banda de tolerância `[6.70, 8.35]` Hz — portanto o
critério textual de FALSIFICA ("nenhum pico distinguível... existe dentro
de [6.70, 8.35] Hz") também não se aplica literalmente. O resultado cai na
**zona de "não distingue"** explicitamente prevista na Seção 5 do
pré-registro: *"um pico existe mas sua proeminência acima do ruído de
fundo local... é inferior a 3× — registrado como tal, não reinterpretado
como suporte ou refutação."*

Isto **não** é lido aqui como "Tamesis confirmado", "Schumann detectado",
nem "Schumann refutado" — apenas como o resultado deste teste único,
pré-registrado, sobre este dataset específico, nesta estação, com este N.
Ver Seção 4 abaixo para a leitura alternativa mais estrita (que colapsaria
o resultado para FALSIFICA) e por que ela não foi adotada como o veredito
primário — ambas as leituras, com todos os números brutos, estão expostas
para o revisor adversarial julgar de forma independente.

| Segmento | Estação | Veredito |
|---|---|---|
| `2014-01-15` | verão austral / inverno boreal | NÃO DISTINGUE |
| `2014-04-15` | primavera boreal | NÃO DISTINGUE |
| `2014-07-15` | verão boreal | NÃO DISTINGUE |

---

## 1. Proveniência e acesso ao dado (resumo — detalhe completo em `data/PROVENANCE.md`)

- **Fonte:** Zenodo, registro `10.5281/zenodo.6348691` ("Four-year
  measurements from Sierra Nevada ELF station. Year 2014"), CC-BY-4.0,
  acessado em 2026-08-27.
- **Sem baixar os 26,7 GB completos:** o suporte a HTTP Range requests do
  servidor Zenodo (`206 Partial Content`, confirmado por `curl`) foi usado
  para ler apenas o diretório central do ZIP (1 requisição, últimos 12 MB)
  e depois extrair, uma requisição por vez, exatamente os 144 arquivos de
  dado horário + 144 `_info.txt` necessários — nunca o arquivo completo.
  **Total transferido pela rede nesta sessão: 240,8 MB** (0,9% dos 26,7
  GB do arquivo completo), em 289 requisições HTTP, todas com verificação
  TLS padrão. O CRC32 de cada arquivo extraído foi validado automaticamente
  pelo módulo `zipfile` contra o diretório central do ZIP; nenhuma
  divergência ocorreu.
- **Subconjunto (Seção 6 do pré-registro, N=3):** três dias completos de
  24h (`2014-01-15`, `2014-04-15`, `2014-07-15`), cada um com exatamente 24
  arquivos horários × 2 canais (NS = `sensor_0`, EW = `sensor_1`) —
  254 MB descomprimidos em `data/raw/`.
- **Taxa de amostragem real, lida do próprio dado (não assumida):**
  `sampling period (usec): 3906.000000` em **todos** os 144 arquivos
  `_info.txt` inspecionados ⇒ `fs = 1e6/3906 = 256,0163850486431 Hz`.
  Ligeiramente diferente dos 256 Hz nominais da literatura secundária
  (diferença ≈ 64 ppm) — a diferença em si é pequena o suficiente para não
  afetar a banda de busca 5–10 Hz de forma material, mas o valor usado em
  todo o pipeline é o real, lido do metadado, nunca o nominal assumido.
- **Formato binário:** inteiros de 16 bits sinalizados (`file_size` =
  2×`number_of_samples` em todos os arquivos, confirmando 16 bits/amostra),
  convertidos para volts pelo fator `10/2^15` V/LSB (±10 V de saturação,
  16 bits: 1 bit de sinal + 15 de amplitude — Salinas et al. 2022). A
  **ordem de bytes (little-endian) foi determinada empiricamente** nesta
  sessão (nenhum link de repositório de código companheiro está presente
  no registro Zenodo, e o texto completo do artigo está bloqueado por
  paywall): decodificar como little-endian produz um sinal com
  estatísticas de um sinal analógico real (desvio-padrão ≈0,23 V, bem
  dentro do trilho ±10 V); decodificar como big-endian produz
  desvio-padrão ≈5,77 V ≈ 10/√3, a assinatura de ruído uniforme de bytes
  trocados, com mínimo/máximo batendo exatamente na saturação ±10 V —
  evidência decisiva a favor de little-endian. Detalhe completo, incluindo
  os números lado a lado, em `data/PROVENANCE.md`.

## 2. Metodologia da análise (exatamente como especificado na Seção 4 do pré-registro)

Para cada um dos 6 pares canal×segmento:

1. Carregar os 24 arquivos horários em ordem cronológica (por índice de
   hora extraído do nome do arquivo), decodificar cada um como `int16`
   little-endian, escalar por `10/2^15` V/LSB, concatenar em uma única
   série temporal contínua (~24h + ~1,4s, já que cada arquivo cobre
   3600,0576 s reais, não exatamente 3600 s).
2. `scipy.signal.welch(samples, fs=fs, window='hann', nperseg=round(64×fs),
   noverlap=nperseg//2, detrend='constant', scaling='density')` — `fs` é o
   valor real confirmado acima, não 256 Hz nominal. `nperseg = 16385`
   amostras (64,00 s exatos na taxa real) em todos os 6 casos.
   Número de segmentos de Welch efetivamente promediados: **2698** por
   canal×segmento (alta resolução estatística — o espectro é suave, não
   ruído de poucas médias).
3. Identificar o pico de maior potência dentro de 5–10 Hz (o "pico
   dominante").
4. Calcular a proeminência do pico dominante: `potência_do_pico /
   mediana(potência na vizinhança ±1 Hz)`.
5. Aplicar o critério de decisão da Seção 5 (ver discussão de leitura
   textual na Seção 4 abaixo deste documento).

Nenhum filtro, detrend além da remoção de média por segmento (padrão do
`scipy.signal.welch`, não uma escolha adicional desta análise), ou outra
etapa de pré-processamento foi aplicado — a Seção 4 do pré-registro não
especifica nenhum, e nenhum foi adicionado após ver o dado.

## 3. Resultados numéricos por canal×segmento

| Segmento | Canal | Pico dominante 5–10Hz (Hz) | Dentro de `[6.70,8.35]`? | Proeminência (×mediana ±1Hz) | Suporta este canal? |
|---|---|---|---|---|---|
| `2014-01-15` | NS | 8,0313 | Sim | 1,221× | Não |
| `2014-01-15` | EW | 7,8125 | Sim | 1,334× | Não |
| `2014-04-15` | NS | 7,9063 | Sim | 1,319× | Não |
| `2014-04-15` | EW | 7,8750 | Sim | 1,442× | Não |
| `2014-07-15` | NS | 7,9375 | Sim | 1,325× | Não |
| `2014-07-15` | EW | 8,5000 | **Não** (fora por 0,15 Hz) | 1,360× | Não |

Em nenhum caso a proeminência atinge 3×. Note a **consistência forte de
localização**: em 5 dos 6 pares o pico dominante cai entre 7,81–8,03 Hz —
bem dentro da banda de tolerância e muito próximo do valor nominal de
7,83 Hz da literatura; no 6º caso (verão, EW) o pico dominante cai a
8,50 Hz, apenas 0,15 Hz além do limite superior de tolerância (8,35 Hz),
com um segundo máximo local mais fraco a 7,95 Hz dentro da banda (ver
tabela de máximos locais completa em `data/results_primary.json`, campo
`tolerance_band_best_local_peak.all_local_maxima_in_band`).

Contexto (potência nos modos 2 e 3, ~14 Hz e ~21 Hz, para o critério
qualitativo "claramente separado dos harmônicos" da Seção 5): em todos os
6 casos a potência perto de 14 Hz e 21 Hz é de **2 a 15 vezes maior** que a
potência no pico do modo 1 identificado — ou seja, o modo 1 (quando existe
como morro distinguível) NÃO está sendo confundido com um harmônico mais
forte vazando para dentro da janela 5–10 Hz; os harmônicos são
inequivocamente mais fortes e ficam fora da janela de busca, como esperado
fisicamente. Números exatos em `data/results_primary.json` →
`harmonics_check`.

> **[Correção datada, 2026-08-27 — revisão adversarial, `DISC-DEC-104`,
> Issue 1, severidade BAIXA.]** A faixa "2 a 15 vezes" está incorreta —
> recalculando diretamente de `data/results_primary.json`, a faixa real é
> **2,31×–18,43×** (2 dos 6 casos, `2014-01-15/EW` e `2014-04-15/EW`,
> excedem o "15" citado). Não afeta nenhum número da tabela principal
> nem o veredito de nenhum canal/segmento — imprecisão de arredondamento
> na prosa de contexto.
>
> **[Correção datada, 2026-08-27 — revisão adversarial, `DISC-DEC-104`,
> Issue 2, severidade MODERADA.]** O método usado acima (potência no bin
> mais próximo de 14,000/21,000 Hz exatos) é mais fraco e metodologicamente
> inconsistente com o método usado para achar o próprio pico do modo 1
> (busca de máximo numa janela, não um bin fixo). Refazendo com o mesmo
> método de janela (±2 Hz em torno de 14/21 Hz), o referee encontrou, nos
> 6 casos, uma feição espectral muito mais estreita e muito mais forte
> perto de **15,1–15,2 Hz** (não 14 Hz), com razão contra o pico do modo 1
> chegando a 161,7× em um caso. A largura (~1–2 bins, ≈0,03–0,05 Hz) é
> inconsistente com um "morro largo" físico de Schumann e mais consistente
> com uma linha de interferência de banda estreita (elétrica ou
> instrumental), não relacionada à ressonância de Schumann — possíveis
> candidatos não confirmados: subarmônico de rede elétrica de 50 Hz
> (~16,67 Hz≈50/3, coincidência numérica não confirmada) ou efeito de
> borda de filtro/calibração do instrumento perto de 24,9–25,0 Hz. **Isto
> não contamina o resultado primário** — a banda de busca pré-registrada
> (5–10 Hz) foi verificada explicitamente como livre desse tipo de feição
> estreita nos 6 casos, e a checagem de harmônicos é declarada pelo
> próprio pré-registro apenas como contexto qualitativo, não parte do
> critério numérico da Seção 5. Fica registrado como observação aberta
> para investigação futura caso este dataset seja reutilizado (ex. um
> teste dedicado ao 2º modo de Schumann).

### Forma espectral (por que "não distingue", não "falsifica")

Inspecionando o formato bruto da PSD (ver os 6 gráficos em `data/plots/`,
ex. `psd_2014-01-15_NS.png`): existe um morro largo e inequívoco — a
potência sobe suavemente de ~3,4×10⁻⁵ V²/Hz em 5 Hz até um platô de
~1,2–1,3×10⁻⁴ V²/Hz entre 7,5–8,3 Hz, e desce de volta a ~7×10⁻⁵ V²/Hz por
volta de 10 Hz, antes de subir novamente em direção aos modos 2/3 mais
fortes acima de 14 Hz. Esse envelope (morro largo no modo 1, vale, subida
para o modo 2) é qualitativamente a forma clássica de um espectro de
ressonância de Schumann de baixo Q. O problema não é ausência de
estrutura — é que o morro é **largo** (≈3–4 Hz de largura), então a
janela de ±1 Hz usada como "ruído de fundo local" pela métrica de
proeminência do pré-registro captura, em grande parte, o próprio ombro do
morro, não um piso de ruído verdadeiramente plano — o que mecanicamente
achata a razão pico/mediana medida, mesmo quando o morro em si é
visualmente inconfundível.

## 4. Aplicação do critério de decisão (Seção 5) — leitura adotada e leitura alternativa

O texto da Seção 5 faz uma distinção de três vias que este relatório
aplica literalmente, sem adicionar nem remover nenhum critério:

- **SUPORTA:** pico dominante de 5–10 Hz dentro de `[6.70,8.35]` Hz **e**
  proeminência ≥3×.
- **FALSIFICA:** *"nenhum pico distinguível de ruído de fundo existe
  dentro de [6.70, 8.35] Hz, em NENHUM dos dois canais"*.
- **Não distingue:** *"um pico existe mas sua proeminência... é inferior a
  3× — registrado como tal, não reinterpretado como... refutação."*

A cláusula de "não distingue" só faz sentido como categoria distinta de
FALSIFICA se "pico existe" (checável por um máximo local genuíno na PSD
discretizada — um bin estritamente maior que seus dois vizinhos imediatos)
for uma condição logicamente mais fraca do que "pico com proeminência
≥3×"; caso contrário as duas cláusulas colidiriam e a zona de "não
distingue" nunca poderia ser alcançada por construção. **Leitura adotada
como veredito primário:** FALSIFICA exige ausência de qualquer máximo
local genuíno dentro da banda de tolerância, em nenhum canal; "não
distingue" cobre o caso, encontrado aqui em todos os 6 pares, de um
máximo local genuíno mas com proeminência <3×. Esta leitura foi
implementada em `analysis/compute_psd.py::genuine_local_maxima_in_band()`
e `classify_segment()`, com docstring explicando a mesma lógica.

**Leitura alternativa (mais estrita), exposta para o revisor adversarial:**
se "pico distinguível de ruído de fundo" na cláusula de FALSIFICA for lido
como sinônimo de "proeminência ≥3×" (colapsando as duas cláusulas), então
os mesmos números brutos acima produziriam veredito **FALSIFICA** para os
3 segmentos (nenhum canal atinge proeminência ≥3× em nenhum lugar da
banda de tolerância). Nenhuma das duas leituras muda qualquer número
(frequência do pico, proeminência, potência) — apenas o rótulo de decisão
aplicado aos mesmos números. Ambas as leituras concordam que **SUPORTA não
se aplica em nenhum caso**. Esta ambiguidade textual do pré-registro em si
(não uma reformulação feita por este agente) é reportada explicitamente
aqui, não escondida, para julgamento pelo revisor adversarial do passo 7
(`00_GOVERNANCE/AGENTS.md`).

> **[Nota datada, 2026-08-27 — revisão adversarial, `DISC-DEC-104`.]** O
> referee hostil reproduziu os 6 casos de forma bit-a-bit idêntica e deu
> seu próprio veredito de leitura sobre a ambiguidade acima: pende
> levemente para a leitura adotada aqui (NÃO DISTINGUE) ser a mais
> textualmente fiel ao pré-registro (linguagem deliberadamente diferente
> nas duas cláusulas). **Mas** identificou um problema real na redação do
> próprio pré-registro (não deste resultado): sob médias pesadas de Welch
> (2698 segmentos), "existe um bin estritamente maior que os dois
> vizinhos imediatos" é uma condição quase trivial de satisfazer em
> qualquer banda com dezenas de bins — a banda `[6,70,8,35]` Hz tem ~106
> bins, e 20–27 "máximos locais genuínos" foram encontrados por caso
> (~1 em cada 4–5 bins), consistente com o que ruído residual de
> estimação produziria mesmo sem nenhuma ressonância real. Sob a leitura
> adotada, o ramo FALSIFICA fica quase inatingível para qualquer dataset
> real minimamente ruidoso — uma fraqueza de desenho do critério em si,
> não uma manipulação de nenhum agente, registrada aqui para julgamento
> futuro sem reformular o critério retroativamente. Adicionalmente
> (Tarefa 4 do referee, teste de robustez além do texto travado): sob uma
> janela de Welch de 32s (não sancionada nem proibida pelo pré-registro,
> que especifica 64s sem ambiguidade prática), o único caso fora da banda
> de tolerância (`2014-07-15/EW`, 8,50 Hz) migra para dentro dela
> (7,97 Hz) — o caso limítrofe do resultado primário está "em cima do
> fio", o que **reforça**, não enfraquece, o enquadramento "não distingue"
> (um resultado robustamente SUPORTA ou FALSIFICA não deveria virar de
> lado com uma escolha razoável de parâmetro não travada).

## 5. Gráficos

Um PSD por canal×segmento (banda de tolerância sombreada em verde, pico
dominante marcado), salvos em:

- `data/plots/psd_2014-01-15_NS.png`, `data/plots/psd_2014-01-15_EW.png`
- `data/plots/psd_2014-04-15_NS.png`, `data/plots/psd_2014-04-15_EW.png`
- `data/plots/psd_2014-07-15_NS.png`, `data/plots/psd_2014-07-15_EW.png`

## 6. O que este resultado NÃO é (Seção 7 do pré-registro)

Idêntico ao escopo travado no pré-registro, reafirmado aqui sem adição:
nenhuma alegação de conexão neural, telepatia, ou transmissão de
consciência via ressonância de Schumann; nenhuma alegação teórica
específica do arcabouço Tamesis; nenhuma generalização para outras
estações/instrumentos a partir deste resultado nesta estação específica;
nenhuma alegação sobre a causa física exata da variação diurna/sazonal
observada. Este é, exclusivamente, um teste de reprodutibilidade
instrumental de um fenômeno físico de 70+ anos de literatura estabelecida,
neste dataset específico.

## 7. Reexecução adversarial

**Pendente.** Por `00_GOVERNANCE/AGENTS.md` passo 7, este resultado não
pode ser catalogado como fechado em `01_PORTFOLIO/TEST_QUEUE.yaml` /
`00_GOVERNANCE/CLAIM_LEDGER.yaml` até que um segundo agente, instruído a
tentar refutá-lo (não confirmá-lo), reexecute a análise de forma
independente sobre a mesma proveniência de dado, com código próprio.
