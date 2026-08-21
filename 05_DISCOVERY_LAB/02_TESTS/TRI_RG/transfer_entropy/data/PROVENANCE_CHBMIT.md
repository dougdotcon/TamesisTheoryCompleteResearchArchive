# Proveniência dos dados reais — CHB-MIT Scalp EEG, `chb01_03.edf`, canais `FP1-F7`/`T7-P7`

Dados baixados diretamente por fetch verificável (HTTPS, sem login/
token), nesta sessão, em 2026-08-21, via `data/prepare_chbmit.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado.

## Fonte

- **Base:** PhysioNet CHB-MIT Scalp EEG Database v1.0.0.
- **URL:** `https://physionet.org/files/chbmit/1.0.0/chb01/chb01_03.edf`
  (42.399.744 bytes) + `chb01-summary.txt` (5.355 bytes), ambos baixados
  e verificados nesta sessão.
- **`chb01-summary.txt` confirma, textualmente:** `File Name:
  chb01_03.edf`, `Seizure Start Time: 2996 seconds`, `Seizure End Time:
  3036 seconds` — batendo exatamente com o valor usado em
  `METHODOLOGY_NOTE.md`, verificado por `assert` no próprio script de
  preparação (não apenas lido visualmente).
- **Canais usados:** `FP1-F7` (X, frontal) e `T7-P7` (Y, temporal) —
  nomes de canal NATIVOS do EDF (montagem bipolar já embutida na
  gravação, não derivada nesta sessão). `256,0Hz`, `n=921.600` amostras
  por canal (3600,0s = 1h, batendo com o cabeçalho do arquivo).
- **Data de acesso:** 2026-08-21.

## Definição PRE/POST (domínio 1 de `METHODOLOGY_NOTE.md`)

Transição = onset da convulsão documentado em `chb01-summary.txt`,
`t=2996s` relativo ao início do arquivo — externo ao cálculo de TE.

- **PRE primária:** `t=[0,2996)s`, `n=766.976` amostras (2996,0s,
  ~49,9min) — pré-ictal + interictal.
- **POST primária:** `t=[2996,3600)s`, `n=154.624` amostras (604,0s) —
  até o final do registro contínuo do arquivo (nenhum outro evento
  documentado dentro deste arquivo; desenho de arquivo único, ver
  `METHODOLOGY_NOTE.md`).
- **PRE robustez:** 50% mais recentes do PRE primária, `n=383.488`
  (1498,0s).
- **POST robustez:** 50% mais próximos da transição do POST primária,
  `n=77.312` (302,0s).

Todas as 4 contagens batem exatamente com as regras já travadas em
`METHODOLOGY_NOTE.md` antes de qualquer cálculo de TE.

## Arquivos locais

- `chbmit_pre_x_primary.npy`, `chbmit_pre_y_primary.npy`,
  `chbmit_post_x_primary.npy`, `chbmit_post_y_primary.npy`,
  `chbmit_pre_x_robust.npy`, `chbmit_pre_y_robust.npy`,
  `chbmit_post_x_robust.npy`, `chbmit_post_y_robust.npy` — segmentos
  derivados em resolução nativa (256Hz, NÃO pré-decimados aqui — a
  subamostragem/teto computacional acontece dentro do pipeline,
  `te_common.MAX_N_PER_SEGMENT`). X = `FP1-F7`, Y = `T7-P7` em todos os
  arquivos.
- `chbmit_segments_meta.json` — metadados completos da preparação.
- O download bruto (`.edf`) NÃO foi salvo no diretório do repositório —
  reproduzível integralmente reexecutando `python3 prepare_chbmit.py`.
