# Proveniência dos dados reais — EUR/CHF tick-a-tick, choque de despeg do SNB (15/01/2015)

Dados baixados diretamente por fetch verificável (HTTP direto ao feed
público da Dukascopy, sem login/token), nesta sessão, em 2026-08-19, via
`data/prepare_eurchf.py` (re-executável, baixa e reprocessa do zero).
Nenhum dado embutido/fabricado. **Re-verificado nesta sessão, não
confiado no cache não-commitado da sessão da Fase 0.6** (instrução
explícita da sessão orquestradora).

## Fonte

- **Provedor:** Dukascopy, feed histórico de tick-a-tick público.
- **URL (padrão, uma por hora UTC):**
  `https://datafeed.dukascopy.com/datafeed/EURCHF/2015/00/15/{HH}h_ticks.bi5`
  (mês indexado a partir de 0 na convenção da Dukascopy — Janeiro = `00`).
- **Par:** `EURCHF`. **Data:** 2015-01-15 (UTC), as 24 horas do dia.
- **Formato:** binário `.bi5`, comprimido LZMA. Registro de 20 bytes por
  tick, big-endian `>iiiff`: offset de tempo em ms desde o início da
  hora do arquivo (`int32`), `ask*10^5` (`int32`), `bid*10^5` (`int32`),
  volume ask/bid em milhões da moeda-base (`float32` cada). Ponto
  decimal EUR/CHF = `10^5` (5 casas), confirmado empiricamente (preços
  decodificados batem com o piso conhecido de 1,2009-1,2010).
- **Data de acesso:** 2026-08-19.

## Confiabilidade do download — observado empiricamente nesta sessão

O host da Dukascopy reseta a conexão TLS intermitentemente após um
request bem-sucedido em condições normais (`Connection reset by peer`)
e retorna `503 Service Unavailable` esporadicamente — observado de
forma não-determinística, não ligado a nenhuma URL/hora específica (a
mesma URL que falhou funciona ao tentar de novo depois). **Nenhuma hora
falhou definitivamente** — todas as 24 horas de 2015-01-15 foram
baixadas com sucesso, algumas precisando de até 7 tentativas (hora=19,
6 falhas 503 consecutivas antes de suceder na 7ª). Retry com backoff
exponencial + jitter implementado em `prepare_eurchf.py::fetch_hour`
(até 8 tentativas por hora); uma falha genuína após esgotar as
tentativas teria sido reportada como falha, nunca mascarada.

## Verificação do registro (re-verificada nesta sessão)

**24/24 horas de 2015-01-15 UTC baixadas com sucesso, 78.333 ticks no
total** (nenhuma hora vazia). Contagem de ticks por hora:

| Hora UTC | Ticks | Hora UTC | Ticks | Hora UTC | Ticks |
|---|---|---|---|---|---|
| 00 | 319 | 08 | 949 | 16 | 8.358 |
| 01 | 379 | 09 | 973 | 17 | 5.701 |
| 02 | 250 | 10 | 5.301 | 18 | 6.271 |
| 03 | 189 | 11 | 6.457 | 19 | 4.131 |
| 04 | 227 | 12 | 5.925 | 20 | 3.209 |
| 05 | 238 | 13 | 6.851 | 21 | 3.034 |
| 06 | 240 | 14 | 6.379 | 22 | 723 |
| 07 | 618 | 15 | 9.962 | 23 | 1.649 |

Liquidez extremamente baixa nas horas pré-anúncio (dezenas a poucas
centenas de ticks/hora, mercado "grudado" no piso), salto brutal de
volume a partir da hora 10 (>5.000 ticks/hora) — consistente com o
choque documentado.

**Checagem empírica direta (não apenas assumida da documentação
externa) de que a quebra estrutural de preço ocorre perto do horário
assumido do anúncio (09:30 UTC = 10:30 CET, Suíça em CET/UTC+1 em
janeiro, sem horário de verão):**

- Preço 5min antes do anúncio: **1,200975**
- Preço logo antes do split: **1,200975**
- Preço logo depois do split: **1,200965**
- Preço 5min depois do anúncio: **1,020855**
- Salto máximo de 1 tick numa janela de ±5min ao redor do split:
  **0,136765**

Confirma o colapso real e documentado (de ~1,2010 para ~1,02, ~15% num
único dia) exatamente na janela assumida — não um artefato de escolha
de horário.

## Definição PRE/POST (Gap (c))

Transição = anúncio do SNB, 2015-01-15 09:30 UTC (`ms=34.200.000` desde
meia-noite UTC). Série de análise = **preço médio (mid = (ask+bid)/2)**
por tick.

- **PRE** = todos os ticks de 00:00 UTC até o anúncio → **n=3.836**
  (≈9,5h, mercado extremamente ilíquido/grudado no piso).
- **POST** = todos os ticks do anúncio até o fim do dia UTC documentado
  (23:59:59 UTC) → **n=74.497** (≈14,5h, inclui o colapso e a
  volatilidade extrema subsequente).

## Variantes de robustez (Gap (c), reaproveitada sem modificação)

- **PRE robustez:** os 50% mais recentes (por contagem) do PRE primário
  → `n=1.918`.
- **POST robustez:** os 50% mais próximos da transição do POST primário
  → `n=37.248`.

## `dt` usado pelo pipeline (nota honesta sobre amostragem irregular)

Tick-a-tick é amostrado IRREGULARMENTE no tempo (intervalos entre ticks
variam de ms a minutos, dependendo da liquidez). `km_common.run_km_
analysis` exige um único `dt` nativo escalar. Escolha: **mediana do
intervalo entre ticks consecutivos, calculada sobre o dia completo**
(`dt≈0,302s`, ver `eurchf_segments_meta.json` campo `median_inter_tick_
dt_seconds_full_day`) — a série é tratada em "tempo de tick" (índice de
tick, não relógio), convenção já padrão em boa parte da literatura de
microestrutura de mercado. **Nota técnica importante:** essa escolha NÃO
afeta o canal de decisão `PKS` numericamente — `D1(x)`/`D2(x)` escalam
igualmente por `1/tau` e `1/(2*tau)`, então a razão `2*D1/D2` usada na
reconstrução de `p_st(x)` (e, portanto, `PKS`) é invariante a uma
reescala uniforme de `tau`/`dt`; `dt` só afeta os valores ABSOLUTOS
reportados de `D1`..`D4`/`tau_ME` (em unidades de tempo) e o corte de
5% do comprimento do segmento na grade de lags do CK (que, por
construção em `km_common.lag_grid_samples`, já opera inteiramente em
unidades de AMOSTRA, então nem esse corte depende do valor de `dt`).

## Achado estrutural honesto — `PKS` indefinido no POST em AMBAS as variantes

O choque do SNB é um dos movimentos de câmbio mais violentos já
documentados (~15% num único dia, de um regime de câmbio fixo). Os
`N_BINS_X=10` bins de quantil são calculados UMA VEZ a partir do PRE
(per Gap (a), regra travada — o PRE é o período pré-choque, faixa de
preço extremamente estreita ~1,2009-1,2010) e reaplicados SEM
recálculo ao POST. Como o POST inclui o colapso a ~1,02, quase TODO
tick do POST cai abaixo do menor quantil observado no PRE — **37.239
de 74.497 ticks do POST primário (≈50%) caem no bin 0 sozinho**, e os 9
bins restantes ficam com 0-2 amostras cada, muito abaixo do piso
`MIN_SAMPLES_PER_BIN=30`. Resultado: 9 de 10 bins ficam indefinidos
para `D1(x)`/`D2(x)` no POST, `reconstruct_stationary_density` retorna
`insufficient_defined_bins` (`n_defined=1 < 3`), e `PKS_post=None` —
**não um p-valor não-significativo, um resultado literalmente
INDEFINIDO** para o canal de decisão. Mesmo padrão em ambas as
variantes (primária e robustez). Isso é uma consequência honesta e
esperada de aplicar a regra já travada ("bins do PRE, reaplicados sem
recálculo") a um domínio com uma ruptura estrutural desse porte —
reportado como está, não contornado recalculando bins ou trocando a
regra.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=50.000` — acionado APENAS no POST primário
(`n=74.497 > 50.000`), decimação por *stride* uniforme aplicada dentro
de `km_common.run_km_analysis` (não manualmente aqui); todos os outros
3 segmentos ficam abaixo do teto. Ver `config.pre_subsample_info`/
`config.post_subsample_info` em cada `result_eurchf_*.json` para o
`stride`/`n_used` efetivo.

## Arquivos locais

- `eurchf_pre_primary.npy`, `eurchf_post_primary.npy`,
  `eurchf_pre_robust.npy`, `eurchf_post_robust.npy` — série de preço
  médio (mid) derivada, já filtrada por tick/horário (ANTES da
  subamostragem Gap (d), aplicada automaticamente dentro do pipeline)
  — commitados neste diretório (pequenos, ≈940KB no total).
- `eurchf_segments_meta.json` — metadados completos da preparação,
  incluindo contagem de ticks por hora e a checagem de quebra
  estrutural de preço.
- **Os downloads brutos (24 arquivos `.bi5`, ~poucos KB a ~50KB cada,
  comprimidos) NÃO foram commitados** — buscados e decodificados em
  memória por `prepare_eurchf.py`, nunca gravados em disco como
  arquivo intermediário; reproduzíveis integralmente reexecutando
  `python3 prepare_eurchf.py`.
