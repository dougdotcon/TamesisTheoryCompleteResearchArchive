# Proveniência — USGS NWIS, Cape Fear River em Lock 1 (02105769), furacão Florence

**Candidato:** `evt-hill`, linha `DISC-TRI-RG-001`.

## Fonte

- **Estação:** USGS `02105769`, "CAPE FEAR R AT LOCK 1 NR KELLY, NC"
  (lat 34,40444, lon −78,29361, `NAD83`) — confirmado via
  `https://waterservices.usgs.gov/nwis/site/?sites=02105769&format=rdb`.
- **PRE — altura de régua diária MÁXIMA** (`parameterCd=00065`,
  `statCd=00001`): `https://waterservices.usgs.gov/nwis/dv/?sites=02105769&parameterCd=00065&statCd=00001&startDT=2000-01-01&endDT=2018-09-13&format=json`
  — arquivo local `data/capefear_pre_dailymax.json`, sha256
  `081bb7e5114fd2f055ac710a4c8a17abd17bd03bb253b4e3de1c6f1f2d167f1f`,
  **`n=6.546`** dias (`2000-10-01` a `2018-09-13` — o período de registro
  da estação começa em outubro/2000, não em janeiro/2000; nenhum gap
  notado na inspeção).
- **POST — altura de régua instantânea** (`parameterCd=00065`, serviço
  `iv`, sem `statCd` — leituras de 15 minutos):
  `https://waterservices.usgs.gov/nwis/iv/?sites=02105769&parameterCd=00065&startDT=2018-09-14&endDT=2018-12-31&format=json`
  — arquivo local `data/capefear_post_instant_wide.json`, sha256
  `a5a9bd18c91b61dcefaf1141ba7df102f5c7276432de3212f97a0ceac75871ec`,
  **`n=10.354`** leituras de 15 min (`2018-09-14` a `2018-12-31`, janela
  larga baixada de uma vez; os scripts de análise cortam o sub-intervalo
  POST exato de cada variante a partir deste arquivo, sem novo download).
  **Todos** os qualificadores USGS nas 10.354 leituras são `'A'`
  (Approved) — nenhuma leitura marcada como estimada/equipamento com
  defeito/gelo, incluindo durante o pico da cheia (19-24/09/2018).
- **Data de acesso:** 2026-08-19 (esta sessão).

## Transição (Gap (d))

**Data:** 2018-09-14 — landfall do furacão Florence, documentado pelo
NHC (próximo a Wrightsville Beach, NC, ~07h15 EDT, como furacão
Categoria 1 após enfraquecer de intensidade Categoria 4 em mar aberto
dias antes). Nota: `METHODOLOGY_NOTE.md` descreve o evento como
"landfall categoria 4" em sua prosa, mas a DATA que a nota trava,
14/09/2018, é a única coisa que este pipeline consome — nenhuma mudança
de data foi feita, o detalhe de categoria no texto da nota não afeta o
parâmetro usado aqui.

## Segmentos (Gap (d))

- **PRE:** altura de régua diária MÁXIMA de `2000-10-01` até
  `2018-09-13` (inclusive) — **`n=6.546`** dias.
- **POST — regra de recessão (necessária, não especificada
  quantitativamente por `METHODOLOGY_NOTE.md`, decisão explícita desta
  sessão):** `METHODOLOGY_NOTE.md` diz "recessão de volta à linha de
  base ou o próximo evento documentado, o que vier primeiro" sem fixar
  um limiar numérico. Regra mecânica, declarada ANTES de qualquer
  inspeção visual do padrão de recessão real (calculada a partir de um
  período de referência de agosto/2018, ANTES de qualquer influência da
  tempestade, não ajustada a posteriori): `baseline` = média da altura
  de régua diária MÁXIMA de `2018-08-01` a `2018-08-31` = **18,413 ft**
  (`n=31` dias). POST termina no primeiro dia em que uma sequência de
  `N` dias consecutivos fica com altura diária máxima `<= baseline *
  (1+tolerancia)`.
  - **Primária:** `tolerancia=10%`, `N=3` dias consecutivos — atingida
    em `2018-10-02` → janela POST `2018-09-14` a `2018-10-02`,
    **`n=1.695`** leituras de 15 min.
  - **Robustez:** `tolerancia=5%`, `N=3` dias consecutivos — atingida em
    `2018-10-10` → janela POST `2018-09-14` a `2018-10-10`,
    **`n=2.462`** leituras de 15 min.
  - Nenhum "próximo evento documentado" mais restritivo foi identificado
    nesta janela (nenhum outro furacão/cheia maior atinge esta bacia
    específica entre landfall e outubro/2018) — a regra de recessão é o
    limite operante em ambas as variantes.

## Ressalva de frequência de amostragem (declarada, não corrigida)

PRE usa altura MÁXIMA DIÁRIA (uma leitura agregada por dia); POST usa
leituras INSTANTÂNEAS brutas de 15 minutos. Este é um desencontro real
de densidade de amostragem entre os dois segmentos — leituras
instantâneas capturam muito mais valores sub-pico que uma máxima diária,
o que poderia, em princípio, inflar ou alterar a cauda aparente de POST
independente de qualquer mudança hidrológica genuína. **Motivo desta
escolha, não uma omissão:** o período de registro em ALTA FREQUÊNCIA
(15 min) desta estação não se estende de volta o suficiente para cobrir
os quase 18 anos de PRE necessários para uma amostra robusta — a máxima
diária foi a estatística de maior frequência disponível de forma
consistente por um PRE longo, e foi escolhida (em vez da MÉDIA diária,
que sub-representaria ainda mais os extremos) especificamente para
minimizar, não eliminar, este desencontro. Reportado explicitamente como
limitação de interpretação em `RESULTS_SUMMARY.md`, não escondido.
