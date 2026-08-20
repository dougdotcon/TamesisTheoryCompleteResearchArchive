# Proveniência dos dados reais — Kīlauea 2018, abertura de fissura de 03/05, estação `HV.BYL..HHZ`

Dados baixados diretamente por fetch verificável (HTTPS, sem login/
token), nesta sessão, em 2026-08-20, via `data/prepare_kilauea.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado.

## Fonte

- **Serviço:** IRIS/EarthScope FDSN dataselect web service.
- **URL base:** `https://service.iris.edu/fdsnws/dataselect/1/query`
  (redireciona automaticamente, `307`, para
  `https://service.earthscope.org/fdsnws/dataselect/1/query`).
- **Estação/canal:** `net=HV sta=BYL loc=-- cha=HHZ` (velocidade
  sismométrica vertical, 100Hz) — **estação primária, USADA SEM
  fallback** (verificada disponível nesta sessão via consulta de
  metadados de estação/canal ANTES da tentativa de download completo:
  `HV|BYL|19.412087|-155.259877|1079.0|Byron's Ledge|1997-02-01|`, canal
  `HHZ` ativo `2015-11-02` a `2024-07-16`, cobrindo integralmente a
  janela necessária). `data/kilauea_segments_meta.json` confirma
  `station_fallback_used=false`.
- **Data de acesso:** 2026-08-20.

## Janelas baixadas

- **PRE:** `2018-05-02T18:00:00` a `2018-05-03T18:00:00 UTC` — 1 traço
  contínuo confirmado (`obspy.Stream.get_gaps()` retorna `[]`),
  `HV.BYL..HHZ`, 100,0Hz, `n=8.640.000` amostras (24,00h) — bate
  EXATAMENTE com `METHODOLOGY_NOTE.md`.
- **POST:** `2018-05-03T18:00:00` a `2018-05-04T22:32:54 UTC` (limite =
  terremoto M6,9 do flanco sul, USGS) — 1 traço contínuo confirmado
  (`get_gaps()=[]`), `HV.BYL..HHZ`, 100,0Hz, `n=10.277.400` amostras
  (28,55h) — bate EXATAMENTE com `METHODOLOGY_NOTE.md`.

## Definição PRE/POST (seção 5.2 de `METHODOLOGY_NOTE.md`)

- **PRE primária:** `n=8.640.000` (24,00h).
- **POST primária:** `n=10.277.400` (28,55h).
- **PRE robustez:** 50% mais recentes (últimas 12h) → `n=4.320.000`.
- **POST robustez:** 50% mais próximos da transição (primeiras ~14,27h)
  → `n=5.138.700`.

Todas as 4 contagens batem exatamente com as já travadas em
`METHODOLOGY_NOTE.md` antes de qualquer cálculo de DMD.

## Distinção explícita de transparência (já nomeada em `METHODOLOGY_NOTE.md`)

Esta é a MESMA janela temporal (03/05/2018, abertura de fissura +
terremoto M6,9 de 04/05) já usada por `lempel_ziv_complexity` para o
domínio Kīlauea — mas com estação DIFERENTE (`BYL` aqui, vs. `HAT` em
`lempel_ziv_complexity/data/PROVENANCE_KILAUEA.md`). É também a MESMA
janela originalmente pré-selecionada (mas nunca tocada — RQA fechou na
validação) por `rqa/METHODOLOGY_NOTE.md`. É DIFERENTE e NÃO-SOBREPOSTA da
transição de 17/05/2018 (início explosivo) usada por
`largest_lyapunov_exponent`.

## Subamostragem (Gap (d) desta linha)

`MAX_N_PER_SEGMENT=200.000` — ACIONADO nos 4 segmentos deste domínio
(todos `N>200.000`), aplicado automaticamente dentro de
`dmd_common.run_dmd_analysis` (decimação por *stride* uniforme, não
manualmente aqui). Fator de decimação exato reportado em
`config`/`diagnostics` de cada `result_kilauea_*.json`.

## Arquivos locais

- `kilauea_pre_primary.npy`, `kilauea_post_primary.npy`,
  `kilauea_pre_robust.npy`, `kilauea_post_robust.npy` — segmentos
  derivados em RESOLUÇÃO NATIVA (100Hz, NÃO pré-decimados aqui — a
  decimação acontece dentro do pipeline). **NÃO commitados** (tamanho,
  ~150MB combinados) — reproduzíveis integralmente reexecutando
  `python3 prepare_kilauea.py`.
- `kilauea_segments_meta.json` — metadados completos da preparação
  (inclui `station_fallback_used=false`, confirmando que `BYL` (estação
  primária) foi usada em ambas as janelas, sem necessidade do fallback
  `HAT`).
- Os downloads brutos (`.mseed`) NÃO foram salvos no diretório do
  repositório — reproduzíveis integralmente reexecutando o script de
  preparação.
