# Proveniência dos dados reais — Terremotos de Kahramanmaraş, Turquia, 06/02/2023, estações `KO.GAZ..HHZ`/`KO.BNN..HHZ`

Dados baixados diretamente por fetch verificável (HTTPS, sem login/
token), nesta sessão, em 2026-08-21, via `data/prepare_turkey_eq.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado.

## Fonte

- **Serviço:** IRIS/EarthScope FDSN dataselect web service.
- **URL base:** `https://service.iris.edu/fdsnws/dataselect/1/query`.
- **Estações/canal:** `net=KO sta=GAZ loc=-- cha=HHZ` (X, Gaziantep,
  37,17°N 37,21°E, ~20km do epicentro M7,8, 100Hz, ativa desde
  2022-02-03) e `net=KO sta=BNN loc=-- cha=HHZ` (Y, Kayseri, 38,85°N
  35,85°E, ~230km, 100Hz, ativa desde 2022-11-29) — ambas verificadas
  disponíveis nesta sessão via consulta de metadados de estação/canal
  ANTES do download completo (`service.iris.edu/fdsnws/station/1/query`).
- **Transições (USGS, catálogo externo):** M7,8 Pazarcık,
  `2023-02-06T01:17:34Z`; M7,5 Elbistan, `2023-02-06T10:24:48Z`
  (~9,12h depois).
- **Data de acesso:** 2026-08-21.

## Robustez do download (nomeada honestamente)

A primeira tentativa de download do PRE/BNN falhou com
`http.client.IncompleteRead` (falha transitória de rede/proxy no meio de
uma transferência *chunked* de ~9.6MB) — `data/prepare_turkey_eq.py`
inclui `n_retries=4` com nova tentativa completa por estação/janela; a
segunda tentativa (rodada nesta sessão) teve sucesso em todas as 4
buscas na primeira tentativa. Nenhum dado foi editado/completado
manualmente — a falha e o retry estão registrados nos logs desta sessão.

## Lacunas reais nos dados e preenchimento (nomeado a priori em
`METHODOLOGY_NOTE.md`, não descoberto post-hoc)

O fluxo bruto do FDSN veio fragmentado em múltiplos traços contíguos
curtos com pequenas lacunas entre eles (ordem de segundos, típico de
telemetria sismológica real, especialmente na janela POST que contém a
própria sequência de terremotos): `PRE/GAZ` 6 traços brutos / 5 lacunas;
`PRE/BNN` 4 traços / 3 lacunas; `POST/GAZ` 10 traços / 9 lacunas;
`POST/BNN` 10 traços / 9 lacunas. Preenchidas por **interpolação linear**
(`obspy.Stream.merge(method=1, fill_value='interpolate')`) ANTES do
cálculo de RMS — prática padrão de sismologia para lacunas curtas reais,
verificado programaticamente (`assert` sobre `np.ma.is_masked`) que
nenhuma amostra ficou sem preenchimento após o merge. Contagem exata de
lacunas por segmento/canal em `turkeyeq_segments_meta.json`
(`n_gaps_*`).

## Mitigação obrigatória contra propagação de onda compartilhada (já travada em `METHODOLOGY_NOTE.md`)

A forma de onda bruta de 100Hz NUNCA foi alimentada ao estimador de TE.
`data/prepare_turkey_eq.py` calcula a taxa de energia sísmica local (RMS)
em blocos NÃO sobrepostos de `BIN_WIDTH_S=120s` (2min) **ANTES de salvar
os `.npy`** — os arquivos `.npy` já contêm a série de energia
coarse-grained, não a forma de onda bruta.

## Definição PRE/POST (domínio 2 de `METHODOLOGY_NOTE.md`)

- **PRE primária:** `2023-02-05T01:17:34Z` a `2023-02-06T01:17:34Z`
  (24h de fundo antes do M7,8) — `n_bins=720` (24,00h).
- **POST primária:** `2023-02-06T01:17:34Z` a `2023-02-06T10:24:48Z`
  (do M7,8 até o M7,5, ~9,12h) — `n_bins=273` (9,10h).
- **PRE robustez:** 50% mais recentes (últimas 12h) — `n_bins=360`.
- **POST robustez:** 50% mais próximos da transição (~4,55h) —
  `n_bins=136`.

Todas as 4 contagens batem com as janelas de tempo já travadas em
`METHODOLOGY_NOTE.md`; pequenas diferenças de `n_bins` vs. o cálculo
ingênuo `duração/BIN_WIDTH_S` são esperadas e explicadas pelo
truncamento de blocos parciais no fim de cada janela (convenção "sem
preenchimento de bloco parcial", igual à usada por `mse`/`permutation
_entropy` para *coarse-graining* nesta linha).

**Consequência a priori já nomeada em `METHODOLOGY_NOTE.md`:** com
`N` da ordem de centenas de *blocos*, a regra de sub-janelamento de
`te_common.py` provavelmente colapsa para poucas subjanelas (ou uma só)
em várias combinações segmento×variante deste domínio — verificado nos
resultados (`analysis/result_turkeyeq_*.json`), não uma falha de
desenho.

## Arquivos locais

- `turkeyeq_pre_x_primary.npy`, `turkeyeq_pre_y_primary.npy`,
  `turkeyeq_post_x_primary.npy`, `turkeyeq_post_y_primary.npy`,
  `turkeyeq_pre_x_robust.npy`, `turkeyeq_pre_y_robust.npy`,
  `turkeyeq_post_x_robust.npy`, `turkeyeq_post_y_robust.npy` — séries de
  RMS já coarse-grained (`BIN_WIDTH_S=120s`), X=`GAZ`, Y=`BNN`.
- `turkeyeq_segments_meta.json` — metadados completos da preparação
  (inclui contagem de lacunas por segmento/canal).
- Os downloads brutos (`.mseed`) NÃO foram salvos no diretório do
  repositório — reproduzíveis integralmente reexecutando
  `python3 prepare_turkey_eq.py`.
