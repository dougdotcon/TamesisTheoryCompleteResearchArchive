# Proveniência dos dados reais — Kilauea 2018 LERZ, estação `HV.HAT..HHZ`

Dados baixados diretamente por fetch verificável (HTTPS, sem login/
token), nesta sessão, em 2026-08-20, via `data/prepare_kilauea.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado.

## Fonte

- **Serviço:** IRIS/EarthScope FDSN dataselect web service.
- **URL base:** `https://service.iris.edu/fdsnws/dataselect/1/query`
  (redireciona automaticamente, `307`, para
  `https://service.earthscope.org/fdsnws/dataselect/1/query` — mesmo
  backend, confirmado nesta sessão; a URL original `service.iris.edu`
  usada na query é a mesma já citada em `METHODOLOGY_NOTE.md`).
- **Estação/canal:** `net=HV sta=HAT loc=-- cha=HHZ` (velocidade
  sismométrica vertical, 100Hz).
- **Data de acesso:** 2026-08-20.

## Janelas baixadas

- **PRE:** `2018-05-02T18:00:00` a `2018-05-03T18:00:00 UTC` — 1 traço
  contínuo confirmado (`obspy.Stream.get_gaps()` retorna `[]`),
  `HV.HAT..HHZ 2018-05-02T18:00:00.005Z - 2018-05-03T17:59:59.995Z,
  100.0Hz, 8.640.000 amostras` — bate EXATAMENTE com
  `METHODOLOGY_NOTE.md` (`N=8.640.000`).
- **POST:** `2018-05-03T18:00:00` a `2018-05-04T22:32:54 UTC` (limite =
  terremoto M6,9 do flanco sul, USGS) — 1 traço contínuo confirmado
  (`get_gaps()=[]`), `HV.HAT..HHZ 2018-05-03T18:00:00.005Z -
  2018-05-04T22:32:53.995Z, 100.0Hz, 10.277.400 amostras` — bate
  EXATAMENTE com `METHODOLOGY_NOTE.md` (`N=10.277.400`).

## Definição PRE/POST (Gap (c))

- **PRE primária:** `n=8.640.000` (24,00h).
- **POST primária:** `n=10.277.400` (28,55h).
- **PRE robustez:** 50% mais recentes (últimas 12h) → `n=4.320.000`.
- **POST robustez:** 50% mais próximos da transição (primeiras ~14,27h)
  → `n=5.138.700`.

Todas as 4 contagens batem exatamente com as já travadas em
`METHODOLOGY_NOTE.md` antes de qualquer cálculo de LZC.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=200.000` — ACIONADO nos 4 segmentos deste domínio
(todos `N>200.000`), aplicado automaticamente dentro de
`lzc_common.run_lzc_analysis` (decimação por stride uniforme, não
manualmente aqui). Fator de decimação exato reportado em
`config.pre_subsample_info`/`post_subsample_info` de cada
`result_kilauea_*.json` (esperado ≈43 para PRE primária, ~100Hz→~2,3Hz
efetivo, per o cálculo já feito em `METHODOLOGY_NOTE.md` Gap (d)).

## Arquivos locais

- `kilauea_pre_primary.npy`, `kilauea_post_primary.npy`,
  `kilauea_pre_robust.npy`, `kilauea_post_robust.npy` — segmentos
  derivados em RESOLUÇÃO NATIVA (100Hz, NÃO pré-decimados aqui -- a
  decimação acontece dentro do pipeline, per Gap (d)) — por isso
  GRANDES (≈150MB combinados, ao contrário da convenção "pequeno" de
  outros domínios desta linha; consequência inevitável da resolução
  nativa de 100Hz sobre janelas de ~24-28h, não um desvio de
  disciplina). **NÃO commitados** (tamanho), per instrução explícita da
  sessão orquestradora de não commitar nesta etapa de qualquer forma —
  reproduzíveis integralmente reexecutando `python3 prepare_kilauea.py`.
- `kilauea_segments_meta.json` — metadados completos da preparação.
- Os downloads brutos (`.mseed`) NÃO foram salvos no diretório do
  repositório (baixados para um diretório de trabalho temporário fora
  do repositório e descartados) — reproduzíveis integralmente
  reexecutando o script de preparação.
