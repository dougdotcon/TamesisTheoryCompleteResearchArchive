# Proveniência — NOAA GHCN-Daily, PDX (USW00024229), onda de calor de 2021

**Candidato:** `evt-hill`, linha `DISC-TRI-RG-001`.

## Fonte

- **API:** `https://www.ncei.noaa.gov/access/services/data/v1`
- **Query completa usada:** `?dataset=daily-summaries&stations=USW00024229&dataTypes=TMAX&format=json&startDate=2000-01-01&endDate=2021-08-15&units=metric`
- **Data de acesso:** 2026-08-19 (esta sessão)
- **Arquivo local:** `data/pdx_tmax_raw.json`
- **sha256:** `6ade835939bbb04507bb33c045fb695d4ac8eb36806b9ea1f8bc5f6b5f189f10`
- **Contagem de registros:** 7.898 dias (`2000-01-01` a `2021-08-15`, sem
  gaps notados na inspeção — GHCN-Daily marca ausência simplesmente
  omitindo o campo `TMAX` daquele dia, nenhum registro com `TMAX`
  ausente foi encontrado neste intervalo).
- **Unidade:** graus Celsius (`units=metric` na query).

## Transição (Gap (d))

**Data:** 2021-06-25 — aviso de calor excessivo (Excessive Heat Warning)
do NWS Portland para a região metropolitana, emitido nesse dia para o
fim de semana 26-28/06/2021. Verificado por busca web (não apenas
reaproveitado de `METHODOLOGY_NOTE.md` sem checagem): reportagem do
Washington Post ("Historic heat wave in Pacific Northwest begins",
2021-06-25) e cobertura local (KGW) confirmam o aviso emitido em
25/06/2021 para o pico do fim de semana. O pico observado no próprio
dado baixado (`TMAX=46,7°C` em 2021-06-28) bate exatamente com o
recorde histórico já documentado para PDX, confirmando a identificação
correta do evento — nenhuma mudança da data já fixada em
`METHODOLOGY_NOTE.md`.

## Segmentos (Gap (d), regra domain-agnostic já travada, sem modificação)

- **PRE:** `TMAX` diário de `2000-01-01` até `2021-06-24` (inclusive) —
  **`n=7.846`** dias. "Vários anos" de histórico, conforme instrução da
  sessão orquestradora, usado para maximizar o tamanho da amostra PRE.
- **POST:** `TMAX` diário de `2021-06-25` até `2021-07-31` (o limite
  mais generoso dos dois definidos pelo Gap (d) — "próximo evento de
  calor documentado OU final de julho/2021, o que vier primeiro"; nenhum
  outro evento de calor tão extremo quanto o próprio domo de calor de
  junho/2021 está documentado antes de 31/07/2021 nesta região, então o
  limite de fim de julho é o que se aplica) — **`n=37`** dias.

## Achado honesto sobre o piso de amostra (Gap (e))

`MIN_N_PER_SEGMENT=200` (`METHODOLOGY_NOTE.md` Gap (e)) **NÃO é
atingido pelo segmento POST** (`n=37 << 200`) — uma consequência
estrutural inevitável de combinar (a) a resolução de 1 observação/dia do
GHCN-Daily com (b) a janela de "várias semanas, não dias" que o próprio
Gap (d) especifica para evitar o risco de circularidade já nomeado na
Fase 0.6 (medir `xi` só sobre os dias de pico). Mesmo usando o limite
MAIS GENEROSO permitido pelo Gap (d) (fim de julho, não um evento
anterior mais restritivo), o máximo fisicamente alcançável é 37 dias —
não há como atingir `n=200` sem violar a janela já travada em Gap (d)
(estenderia POST para muito além de "até o próximo evento ou fim de
julho"). **Isto não foi contornado**: `run_evt_hill_analysis` retorna
`status=insufficient_samples` honestamente (ver
`analysis/result_pdx.json`), e este domínio é reportado como
estruturalmente não testável com a combinação exata de resolução
temporal do dado e definição de janela já fixadas, não como um
resultado nulo/negativo por ausência de sinal.
