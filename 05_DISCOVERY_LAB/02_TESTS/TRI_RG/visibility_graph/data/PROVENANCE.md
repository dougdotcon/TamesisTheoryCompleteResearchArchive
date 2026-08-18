# Proveniência dos dados reais — `grafo-de-visibilidade`

Dados baixados diretamente por fetch verificável (curl, HTTPS, sem login/token),
nesta sessão, em 2026-08-18. Nenhum dado embutido/fabricado.

## Domínio 1 — Geomagnetismo (índice SYM-H, tempestade de 17/03/2015)

- **Fonte:** NASA/SPDF OMNIweb, High Resolution OMNI (HRO), dados 5-min, ano completo 2015.
- **URL exata:** `https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_5min2015.asc`
- **Formato:** `https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/hroformat.txt`
  (mesmo formato já usado e verificado em `mse_multiscale_entropy/data/hroformat.txt`
  para o ano de 1989; reaproveitado sem modificação). Campo SYM/H = coluna 42
  (1-indexado, separado por espaço em branco), confirmado batendo a fórmula de
  Fortran `(2I4,4I3,3I4,2I7,F6.2,I7,8F8.2,4F8.1,F7.2,F9.0,F6.2,2F7.2,F6.1,6F8.2,7I6,F7.2,F5.1)`
  + 3 campos extras de fluxo de prótons GOES para dado de 5-min = 49 campos totais.
- **Arquivo local:** `data/omni_5min2015.asc` (34.374.240 bytes, 105.120 linhas =
  365 dias × 288 intervalos de 5 min, ano completo sem lacunas — 2015 não é bissexto).
- **Verificação de sanidade:** SYM-H mínimo no arquivo = −233 nT, batendo com o
  valor documentado na literatura (SYM/H mínimo = −234 nT; Dst mínimo = −223 nT
  durante a tempestade de 17/03/2015 — Kamide & Kusano 2015; verificado por busca
  web independente nesta sessão).
- **SSC (Sudden Storm Commencement), transição PRE/POST:** 2015-03-17 04:45 UT
  — Kamide & Kusano 2015 (*Space Weather*), verificado por busca web direta
  nesta sessão (múltiplas fontes independentes convergindo no mesmo horário:
  choque interplanetário chegou à Wind às 03:59 UT, SSC observado em solo às
  04:45 UT em 17/03/2015).
- **Próximo evento geomagnético documentado (fronteira POST):** tempestade de
  22-25/06/2015 (Dst mínimo entre −204 e −208 nT, segunda tempestade mais forte
  de 2015), verificado por busca web direta nesta sessão. POST = 2015-03-17
  04:45 UT até 2015-06-21 23:55 UT (última amostra de 5 min antes do início
  documentado da próxima tempestade).
- **PRE:** todo o registro contínuo disponível do ARQUIVO 2015 anterior ao SSC
  (2015-01-01 00:00 UT a 2015-03-17 04:40 UT) — mesma convenção prática já usada
  em `mse_multiscale_entropy` para dado OMNI (um ano-arquivo por vez, não
  concatenando múltiplos anos anteriores; ver `METHODOLOGY_NOTE.md` Gap (c),
  regra domain-agnostic geral "todo o registro contínuo disponível", aplicada
  aqui de forma consistente com o precedente já estabelecido nesta linha para
  este mesmo tipo de dado).

## Domínio 2 — Hidrologia (altura de régua, furacão Harvey/2017)

- **Fonte:** USGS National Water Information System (NWIS), serviço de valores
  instantâneos (IV), estação **USGS 08074500, Whiteoak Bayou at Houston, TX**
  (29.775228°N, −95.397161°W), parâmetro **00065 (gage height, ft)**.
- **Identificação da estação:** localizada por busca direta a partir do pico
  documentado citado em `METHODOLOGY_NOTE.md` ("pico real de 44,31 pés") —
  consultado o serviço oficial de picos anuais (`peak` service) da USGS para
  múltiplas estações candidatas na bacia de Houston (Buffalo Bayou, Brays Bayou,
  Sims Bayou, Whiteoak Bayou, Cypress Creek, Vince Bayou, Greens Bayou) até
  encontrar a correspondência EXATA: `USGS 08074500` registrou pico de vazão de
  50.600 cfs em 2017-08-27, com **gage_ht = 44,31 pés** (código de qualificação
  "9,C" = vazão devida a furacão; registro afetado por urbanização/canalização)
  — URL exata usada para a verificação:
  `https://nwis.waterdata.usgs.gov/nwis/peak?site_no=08074500&agency_cd=USGS&format=rdb`.
- **URLs exatas dos dados de série temporal usados na análise (serviço `iv`,
  formato `rdb`, redirecionado por HTTP 301 de `waterservices.usgs.gov` para
  `nwis.waterservices.usgs.gov`, seguido via `curl -L`):**
  - PRE: `https://waterservices.usgs.gov/nwis/iv/?sites=08074500&parameterCd=00065&startDT=2007-10-01&endDT=2017-08-24&format=rdb`
  - POST: `https://waterservices.usgs.gov/nwis/iv/?sites=08074500&parameterCd=00065&startDT=2017-08-25&endDT=2026-08-17&format=rdb`
- **Arquivos locais:** `data/usgs_pre_raw.rdb` (14.096.902 bytes, 334.289
  leituras válidas de 15 min, 2007-10-01 01:00 a 2017-08-24 23:45, hora local
  CDT/CST conforme reportado pelo próprio serviço), `data/usgs_post_raw.rdb`
  (13.173.722 bytes, 313.063 leituras válidas, 2017-08-25 00:00 a 2026-08-17
  21:45).
- **Verificação de sanidade decisiva:** o valor MÁXIMO de altura de régua no
  segmento POST baixado é **44,31 pés exatos** (`argmax` em 2017-08-27,
  batendo com o registro oficial de pico anual da própria USGS) — confirma
  que a estação/parâmetro/período estão corretos, não é coincidência: bate
  dígito a dígito com o número já citado em `METHODOLOGY_NOTE.md` (obtido de
  forma independente na Fase 0.5, antes desta sessão).
- **Período de registro instantâneo (00065) disponível na estação, conforme
  serviço `seriesCatalogOutput`:** 2007-10-01 a presente (contínuo, sem
  lacuna multi-mês detectada nos dados baixados).
- **Transição PRE/POST:** 2017-08-25 (início da precipitação extrema do
  landfall de categoria 4 documentado pelo NHC, granularidade de dia inteiro
  conforme `METHODOLOGY_NOTE.md` Gap (c) — sem hora específica declarada na
  nota, usada a fronteira de dia civil em horário local da estação).
- **PRE:** todo o registro contínuo disponível do parâmetro 00065 na estação
  anterior à transição (2007-10-01, início do período de registro instantâneo
  documentado pelo próprio catálogo de séries da USGS, até 2017-08-24 23:45).
- **POST:** subida até o pico documentado de 44,31 pés e além, até o final do
  registro contínuo disponível da estação no momento desta sessão
  (2026-08-17 21:45 — última leitura disponível via o serviço `iv`), conforme
  `METHODOLOGY_NOTE.md` Gap (c) ("até o final do registro contínuo disponível
  da estação", fronteira aberta, deliberadamente distinta da regra genérica
  de "até o próximo evento documentado" usada no domínio geomagnético).
- **Leituras inválidas/faltantes:** descartadas por não serem conversíveis a
  float (ex. códigos de gelo/estimativa textual do NWIS), nunca substituídas
  por valor fabricado — contagem de linhas descartadas = diferença entre
  linhas de dado brutas do arquivo `.rdb` e `n` reportado em `segments_meta.json`.

## Variantes PRE/POST (Gap (c), aplicadas identicamente aos 2 domínios)

- **Robustez PRE:** os 50% mais recentes (por contagem de amostras) do PRE primário.
- **Robustez POST:** os 50% mais próximos da transição (por contagem de amostras) do POST primário.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=5000`, decimação por stride uniforme, aplicada
IDENTICAMENTE aos 2 domínios e às 2 variantes (primária/robustez) dentro de
`vg_common.run_vg_analysis` (não aplicada manualmente aqui — a função pública
já implementa a regra, ver `analysis/vg_common.py`).
