# Proveniência dos dados reais — Itália, primeira onda de COVID-19, lockdown de 09/03/2020

Dados baixados diretamente por fetch verificável (HTTPS, sem login/
token), nesta sessão, em 2026-08-20, via `data/prepare_covid_italy.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado.

## Fonte

- **Fonte:** JHU CSSE COVID-19 Data Repository,
  `time_series_covid19_confirmed_global.csv`.
- **URL:**
  `https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv`
  (`1.819.904` bytes baixados nesta sessão).
- **Linha usada:** `Country/Region=Italy` (`Province/State` vazio —
  série nacional agregada).
- **Data de acesso:** 2026-08-20.
- **Série trabalhada:** incidência diária (primeira diferença da
  contagem cumulativa de casos confirmados) — convenção padrão de
  epidemiologia de séries temporais, evita a autocorrelação trivial de
  uma série monotonicamente crescente e mantém o comprimento de amostra
  minimamente maior possível dado o comprimento absoluto curto da série
  bruta (ver risco nomeado a priori na seção 5.1 de
  `METHODOLOGY_NOTE.md`).

## Definição PRE/POST (seção 5.1 de `METHODOLOGY_NOTE.md`)

- **Transição:** decreto de lockdown nacional "Io resto a casa" (DPCM),
  09/03/2020.
- **Primeiro caso confirmado na Itália (JHU):** 31/01/2020 (2 casos
  cumulativos naquele dia).
- **PRE primária:** incidência diária de 31/01/2020 a 08/03/2020
  (inclusive), `n=38` amostras.
- **POST primária:** incidência diária de 09/03/2020 a 21/03/2020
  (inclusive — dia anterior ao próximo confundidor documentado, o DPCM
  de fechamento total de atividades produtivas não-essenciais de
  22/03/2020), `n=13` amostras.
- **PRE robustez:** 50% mais recentes → `n=19`.
- **POST robustez:** 50% mais próximos da transição → `n=6`.

Valores de incidência diária exatos (para auditabilidade, também salvos
em `covid_italy_segments_meta.json`):

- **PRE primária** (31/01–08/03/2020): `[2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 42, 93, 74, 93, 131, 202, 233, 240,
  566, 342, 466, 587, 769, 778, 1247, 1492]`
- **POST primária** (09–21/03/2020): `[1797, 977, 2313, 2651, 2547,
  3497, 3590, 3233, 3526, 4207, 5322, 5986, 6557]`

## Achado honesto crítico, nomeado a priori e confirmado após rodar a pipeline travada

**Como já antecipado explicitamente em `METHODOLOGY_NOTE.md` seção 5.1
("MUITO curto para os pisos `D_MIN=10`/`MIN_HANKEL_COLS=50`"), a
resolução diária deste domínio produz segmentos curtos demais para a
pipeline travada — mas a falha real observada ocorre um passo ANTES do
que a nota de metodologia havia antecipado: não no gate de `d` (seção
1.3), mas já no primeiro passo, a estimativa de `tau` (informação mútua,
reaproveitada de `rqa_common.estimate_tau`):**

- **PRE primária** (`n=38`): `lag_max = min(200, floor(38/10)) = 3` —
  curva de MI (`[1,0309, 0,8933, 0,8675]`) monotonicamente decrescente,
  sem mínimo local, E o fallback de cruzamento-por-zero da autocorrelação
  também não encontra cruzamento em `lag<=3` → `status=tau_not_resolved`.
- **POST primária** (`n=13`): `lag_max = min(200, floor(13/10)) = 1` —
  curva de MI vazia (não há sequer 2 lags para comparar) →
  `status=tau_not_resolved` (`reason=lag_max_too_small`).
- **PRE robustez** (`n=19`) e **POST robustez** (`n=6`): mesmo padrão,
  ainda mais curtas (`lag_max=1` para ambas).

**Todas as 4 combinações PRE/POST × primária/robustez deste domínio
retornam `status="tau_not_resolved"` na pipeline travada
(`analysis/dmd_common.run_dmd_analysis`), ANTES de qualquer cálculo de
`d`/posto/DMD** — não um bug: o mesmo tipo de gate de suficiência de
dado (aqui, na estimativa de `tau` compartilhada com RQA/LLE, não no
gate de `d` específico deste candidato) funcionando exatamente como
desenhado, mecanicamente, sem exceção para este domínio. Resultado
completo em `analysis/result_covid_italy_primary.json` /
`analysis/result_covid_italy_robust.json`, discutido honestamente em
`RESULTS_SUMMARY.md`. **Nenhuma tentativa de afrouxar `lag_max`/
`D_MIN`/`HANKEL_D_DIVISOR` post-hoc foi feita** — isso seria exatamente o
tipo de sintonia após ver o dado que esta linha proíbe; todas essas
regras foram travadas em `METHODOLOGY_NOTE.md` ANTES de qualquer
preparação de dado real, e o risco de comprimento insuficiente deste
domínio específico já havia sido nomeado honestamente a priori (mesmo
que o ponto exato de falha mecânica na cadeia `tau`->`d`->posto não
tivesse sido previsto com precisão cirúrgica — apenas que "algum" gate de
comprimento falharia).

## Arquivos locais

- `covid_italy_pre_primary.npy`, `covid_italy_post_primary.npy`,
  `covid_italy_pre_robust.npy`, `covid_italy_post_robust.npy` — pequenos
  (dezenas de amostras cada), commitáveis sem restrição de tamanho.
- `covid_italy_segments_meta.json` — metadados completos + valores
  brutos de incidência diária usados.
