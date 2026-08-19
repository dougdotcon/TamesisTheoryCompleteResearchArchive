# Proveniência dos dados reais — PhysioNet MIT-BIH Malignant Ventricular Arrhythmia Database (`vfdb`)

Dados baixados diretamente por fetch verificável (`wfdb`/HTTPS, sem
login/token), nesta sessão, em 2026-08-19, via `data/prepare_vfdb.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado. **Re-verificado nesta sessão, não confiado no cache de uma
sessão anterior** (instrução explícita da sessão orquestradora — o
levantamento da Fase 0.6 não commitou nenhum artefato reutilizável).

## Fonte

- **Base de dados:** PhysioNet MIT-BIH Malignant Ventricular Arrhythmia
  Database (`vfdb`) 1.0.0.
- **URL base:** `https://physionet.org/files/vfdb/1.0.0/`
- **Registro:** `418` (`418.hea`, `418.dat`, `418.atr`), baixado via
  biblioteca `wfdb` (`wfdb.rdrecord`/`wfdb.rdann`, `pn_dir="vfdb/1.0.0"`).
- **Data de acesso:** 2026-08-19.

## Verificação do registro (re-verificada nesta sessão)

Registro `418`: **35 minutos contínuos (2100s), 2 canais, ambos
rotulados genericamente `ECG` (sem nome de derivação individual, ao
contrário de EDB), `fs=250Hz`, ganho ADC=200, `525.000` amostras por
canal.** Canal 0 tem faixa dinâmica maior (`std=0,527mV`) que o canal 1
(`std=0,219mV`) — **canal 0 usado como canal de análise primário**,
escolha simples e documentada (não rederivada a partir da própria
transição). **121 anotações no total, com apenas DOIS valores de
`aux_note` em todo o registro: `(N` (ritmo normal) e `(VFL` (flutter/
fibrilação ventricular)** — confirmado por inspeção direta, não
assumido. **60 onsets `(VFL` no total no registro** (mais que as "~10
transições" estimadas no levantamento da Fase 0.6/`METHODOLOGY_NOTE.md`
— provavelmente porque alguns episódios têm múltiplas anotações `(VFL`
internas; não investigado further pois só a PRIMEIRA transição é usada
nesta rodada, per Gap (c)).

## Transição escolhida como PRE/POST primária (per Gap (c): só a primeira, não todas ~10)

**Primeiro onset `(VFL` cronológico:** amostra 99.624 (398,496s).
**Offset (retorno a `(N`):** amostra 101.499 (405,996s) — episódio de
**7,5s (1.875 amostras)**, curto, mas é o que a "primeira transição
documentada" fornece; usado como especificado, não substituído por um
episódio mais longo posterior.

**Verificado explicitamente (não assumido) que o segmento PRE é
genuinamente limpo:** a ÚNICA anotação antes da amostra 99.624 é `(N`
na amostra 18 (marca o início do ritmo normal no começo do registro) —
nenhum outro confundidor entre o início do registro e o onset escolhido.

## Definição PRE/POST (Gap (c))

- **PRE** = ECG (canal 0) antes do onset anotado → **n=99.624 amostras**
  (398,5s ≈ 6,6 min).
- **POST** = ECG durante o episódio, até o offset anotado → **n=1.875
  amostras** (7,5s).

## Variantes de robustez (Gap (c), reaproveitada sem modificação)

- **PRE robustez:** os 50% mais recentes (por contagem) do PRE primário
  → `n=49.812`.
- **POST robustez:** os 50% mais próximos da transição do POST primário
  → `n=937`.

## Nota honesta sobre tamanho de amostra do POST

O episódio POST primário (1.875 amostras) e robustez (937 amostras) são
BEM menores que os segmentos de outros domínios já usados nesta linha —
consequência direta de usar a PRIMEIRA transição documentada (per Gap
(c)), que aqui é um episódio curto de VFL (7,5s), não uma escolha desta
sessão. Isso pode limitar o alcance da grade de lags do teste de
Chapman-Kolmogorov no segmento POST especificamente (o piso de blocos
não-sobrepostos exige `>= MIN_SAMPLES_PER_BIN*N_BINS_X=300` blocos
válidos por lag) — reportado honestamente no resultado, não escondido
nem contornado trocando de episódio.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=50.000` — não acionado em nenhum segmento deste
domínio (todos `n<50.000`), aplicado dentro de `km_common.run_km_
analysis` (não manualmente aqui), mesma convenção do resto da linha.

## Arquivos locais

- `vfdb_pre_primary.npy`, `vfdb_post_primary.npy`,
  `vfdb_pre_robust.npy`, `vfdb_post_robust.npy` — segmentos derivados
  (já filtrados por amostra/evento) — commitados neste diretório
  (pequenos, < 1MB no total).
- `vfdb_segments_meta.json` — metadados completos da preparação,
  incluindo os valores de `aux_note` únicos e a lista de eventos antes
  do onset escolhido (verificação de "PRE limpo").
- **Os downloads brutos (`418.dat`, `418.hea`, `418.atr`) NÃO foram
  commitados** — `wfdb` os busca diretamente do PhysioNet em memória
  (nunca grava um arquivo bruto local); reproduzíveis integralmente
  reexecutando `python3 prepare_vfdb.py`.
