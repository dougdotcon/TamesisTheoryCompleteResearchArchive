# Proveniência dos dados reais — Daphnet Freezing-of-Gait, sujeito `S01R01`

Dados baixados diretamente por fetch verificável (HTTPS, sem login/
token), nesta sessão, em 2026-08-20, via `data/prepare_daphnet.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado. **Re-verificado nesta sessão** (contagens re-conferidas contra
`METHODOLOGY_NOTE.md`, não apenas confiadas do levantamento da Fase 0.7).

## Fonte

- **Base de dados:** UCI ML Repository, Daphnet Freezing-of-Gait Dataset
  (Bächlin et al. 2010, *IEEE Trans. Info. Technol. Biomed.* 14(2):436).
- **URL:** `https://archive.ics.uci.edu/ml/machine-learning-databases/00245/dataset_fog_release.zip`
  (~21,4MB, download completo confirmado nesta sessão: 21.443.961 bytes).
- **Registro usado:** `dataset_fog_release/dataset/S01R01.txt`.
- **Data de acesso:** 2026-08-20.

## Verificação do registro (re-verificada nesta sessão)

`S01R01`: 151.987 amostras, 11 colunas, `fs=64Hz` (confirmado por
`documentation.html` do próprio pacote, re-lido diretamente nesta
sessão). Colunas: `0`=tempo(ms), `1-3`=aceleração do tornozelo (fwd/
vertical/lateral, mg), `4-6`=aceleração da coxa, `7-9`=aceleração do
tronco, `10`=anotação (`0`=fora de protocolo, `1`=caminhando/sem
congelamento, `2`=congelamento). Rótulos únicos confirmados:
`{0: 59.185, 1: 87.655, 2: 5.147}` amostras.

**18 episódios de congelamento** (runs contíguos de rótulo `2`)
confirmados por contagem direta de transições — bate exatamente com o
número já citado em `METHODOLOGY_NOTE.md`.

## Transição escolhida (Gap (c), fixada a priori)

**Onset do PRIMEIRO episódio de congelamento:** amostra `72.944`
(0-indexado), `t=1.139,765s` — bate EXATAMENTE com o valor travado em
`METHODOLOGY_NOTE.md` (`amostra 72.944, t=1.139,75s`, diferença de
arredondamento apenas). Rótulo imediatamente antes do onset: `1`
(caminhando); no onset: `2` (congelamento) — transição limpa, confirmada.

## Canal usado

Aceleração vertical do tornozelo, coluna 2 (0-indexada) do arquivo — o
sensor/eixo primário de Bächlin et al. 2010, per `METHODOLOGY_NOTE.md`
Gap (c) (fundamentado na literatura, não escolhido por inspeção do
resultado).

## Definição PRE/POST (Gap (c))

- **PRE primária** = sinal completo do início do registro até o onset →
  `n=72.944` (`1.139,75s`).
- **POST primária** = sinal completo do onset até o FIM do registro →
  `n=79.043` (`1.235,05s`) — necessariamente contém os outros 17
  episódios de congelamento subsequentes mais caminhada intercalada;
  interpretado honestamente como "regime pós-início-de-congelamento", não
  "um único episódio isolado" (per `METHODOLOGY_NOTE.md`).
- **PRE robustez** = 50% mais recentes do PRE primária → `n=36.472`.
- **POST robustez** = 50% mais próximos da transição do POST primária →
  `n=39.521`.

Todas as 4 contagens batem exatamente com as já travadas em
`METHODOLOGY_NOTE.md` antes de qualquer cálculo de LZC.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=200.000` — não acionado em nenhum segmento deste
domínio (todos os 4 segmentos ficam abaixo do teto), aplicado dentro de
`lzc_common.run_lzc_analysis` (não manualmente aqui), mesma convenção do
resto da linha. `fs=64Hz` preservado integralmente em todos os 4
segmentos.

## Arquivos locais

- `daphnet_pre_primary.npy`, `daphnet_post_primary.npy`,
  `daphnet_pre_robust.npy`, `daphnet_post_robust.npy` — segmentos
  derivados (já filtrados por amostra/evento), pequenos (< 1MB no
  total).
- `daphnet_segments_meta.json` — metadados completos da preparação.
- **O download bruto (`dataset_fog_release.zip`, ~21MB) NÃO foi
  commitado** — reproduzível integralmente reexecutando
  `python3 prepare_daphnet.py`.
