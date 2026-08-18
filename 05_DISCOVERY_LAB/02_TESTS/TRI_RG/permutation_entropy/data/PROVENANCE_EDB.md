# Proveniência dos dados reais — PhysioNet European ST-T Database (episódio isquêmico transitório)

Dados baixados diretamente por fetch verificável (`wfdb`/HTTPS, sem
login/token), nesta sessão, em 2026-08-18, via `data/prepare_edb.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado.

## Fonte

- **Base de dados:** PhysioNet European ST-T Database (EDB) 1.0.0
  (Taddei et al. 1992, *European Heart Journal* 13:1164).
- **URL base:** `https://physionet.org/files/edb/1.0.0/`
- **Registro:** `e0103` (`e0103.hea`, `e0103.dat`, `e0103.atr`), baixado
  via biblioteca `wfdb` (`wfdb.rdrecord`/`wfdb.rdann`,
  `pn_dir="edb/1.0.0"`).
- **Data de acesso:** 2026-08-18.
- **Convenção de anotação de episódios ST verificada por fetch direto
  de** `https://physionet.org/files/edb/1.0.0/annotations.shtml` (não
  assumida de memória): anotações de episódio ST carregam texto
  `(ST<sinal><sinal_de_desvio>` no INÍCIO do episódio,
  `AST<sinal><sinal_de_desvio><magnitude>` no PICO, e
  `ST<sinal><sinal_de_desvio>)` no FIM — o dígito identifica em qual dos
  2 canais do registro o episódio foi medido.

## Verificação do registro (re-verificada nesta sessão, não assumida do levantamento da Fase 0.6)

O registro `e0103`, citado pelo levantamento da Fase 0.6 apenas como
"cabeçalho verificado", foi baixado e suas anotações efetivamente
inspecionadas nesta sessão: **2 horas, 2 canais (`V4`, `MLIII`),
`fs=250Hz`, `1.800.000` amostras por canal**. Paciente com angina mista,
doença de 1 vaso (artéria coronária direita), medicado com nitratos e
diltiazem — perfil clínico diretamente consistente com episódios
isquêmicos reais documentados. **5 episódios ST anotados por
cardiologista, todos no canal `MLIII` (índice de sinal 1):**

| # | Início (amostra / s) | Fim (amostra / s) | Duração (s) | `aux_note` de início |
|---|---|---|---|---|
| 1 | 214.719 / 858,9 | 255.059 / 1020,2 | 161,4 | `(ST1+` |
| 2 | 397.333 / 1589,3 | 435.369 / 1741,5 | 152,1 | `(ST1+` |
| 3 | 575.587 / 2302,3 | 613.796 / 2455,2 | 152,8 | `(ST1+` |
| 4 | 727.684 / 2910,7 | 759.225 / 3036,9 | 126,2 | `(ST1+` |
| 5 | 1.702.273 / 6809,1 | 1.739.121 / 6956,5 | 147,4 | `(ST1+` |

## Episódio escolhido como transição PRE/POST primária

**Episódio 1** (o primeiro cronologicamente) — onset em amostra 214.719
(858,9s), offset em amostra 255.059 (1.020,2s). Escolhido por ser o mais
limpo/menos confundido disponível: **verificado explicitamente (não
assumido) que NENHUMA outra anotação não-batimento (mudança de ritmo,
outro episódio ST/T, troca de qualidade de sinal) ocorre entre o início
do registro e este onset** — a única anotação não-batimento antes da
amostra 214.719 é `(N` (ritmo sinusal normal) na amostra 15, ou seja, o
segmento PRE inteiro é ritmo sinusal normal contínuo, sem confundidor.

Canal usado: `MLIII` (índice de sinal 1 — o canal em que este registro
tem seus episódios ST efetivamente anotados).

## Definição PRE/POST (Gap (c), regra específica de EDB)

- **PRE** = ECG (canal MLIII) antes do onset anotado → **n=214.719
  amostras** (858,9s ≈ 14,3 min).
- **POST** = ECG durante o episódio, até o offset anotado → **n=40.340
  amostras** (161,4s ≈ 2,7 min).

## Variantes de robustez (Gap (c), reaproveitada sem modificação)

- **PRE robustez:** os 50% mais recentes (por contagem) do PRE primário
  → `n=107.360`.
- **POST robustez:** os 50% mais próximos da transição do POST primário
  → `n=20.170`.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=20.000`, decimação por *stride* uniforme, aplicada
DENTRO de `pe_common.run_pe_analysis` (não manualmente aqui) —
identicamente às 2 variantes deste domínio e ao domínio VitalDB. Ver
`edb_segments_meta.json` para os `n` brutos de cada segmento antes da
subamostragem; os `stride`/`n_used` efetivamente aplicados por
`run_pe_analysis` ficam registrados em `config.pre_subsample_info` /
`config.post_subsample_info` de cada `result_edb_*.json`.

## Arquivos locais

- `edb_pre_primary.npy`, `edb_post_primary.npy`, `edb_pre_robust.npy`,
  `edb_post_robust.npy` — segmentos derivados (já filtrados por
  amostra/evento, ANTES da subamostragem Gap (d), aplicada
  automaticamente dentro do pipeline em tempo de execução) —
  commitados neste diretório.
- `edb_segments_meta.json` — metadados completos da preparação,
  incluindo os 5 episódios ST detectados e a lista de eventos antes do
  onset escolhido (verificação de "PRE limpo").
- **Os downloads brutos (`e0103.dat` ~5,4MB, `e0103.hea`, `e0103.atr`)
  NÃO foram commitados** — reproduzíveis integralmente reexecutando
  `python3 prepare_edb.py` (instrução explícita da sessão orquestradora
  para este passo: documentar via URL/proveniência em vez de commitar
  arquivos brutos grandes).
