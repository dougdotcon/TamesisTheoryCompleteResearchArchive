# Proveniência dos dados reais — VitalDB (indução de anestesia, EEG)

Dados baixados diretamente por fetch verificável (`requests`/HTTPS, sem
login/token), nesta sessão, em 2026-08-18, via `data/prepare_vitaldb.py`
(re-executável, baixa e reprocessa do zero). Nenhum dado embutido/
fabricado. **O caso citado por uma sessão anterior não commitada
(Fase 0.6, caso `1`, "1.477.269 amostras") foi re-verificado NESTA
sessão e confirmado NÃO utilizável** para o desenho PRE/POST desta
metodologia — ver seção "Por que não o caso 1" abaixo.

## Fonte

- **API:** VitalDB (Seoul National University Hospital), `https://api.vitaldb.net`
  (Lee et al. 2022, *JMIR Medical Informatics* 10:e32662).
- **Endpoints usados:**
  - `https://api.vitaldb.net/cases` (metadados de todos os casos, CSV gzip)
  - `https://api.vitaldb.net/trks` (catálogo de faixas de todos os casos, CSV gzip)
  - `https://api.vitaldb.net/{track_id}` (dado bruto de uma faixa, CSV gzip)
- **Data de acesso:** 2026-08-18.

## Seleção de caso/faixa (re-verificada nesta sessão, não herdada às cegas)

Critério, aplicado em `prepare_vitaldb.py::select_case()`: dentre todos os
casos que possuem uma faixa `BIS/EEG1_WAV` ou `BIS/EEG2_WAV` (EEG bruto,
~128Hz) **E** cujo `anestart` cai DENTRO do intervalo de tempo
efetivamente gravado da faixa (`casestart <= anestart <= caseend`) **E**
que têm pelo menos 600s de faixa disponível em AMBOS os lados de
`anestart`, escolher o candidato com o maior `min(duração_PRE,
duração_POST)` (melhor equilíbrio entre os dois segmentos).

**Resultado da varredura:** 45 casos candidatos elegíveis (de 6.388 casos
totais no catálogo). **Caso selecionado: `408`** —
`pre_dur=1.984,0s` (~33,1 min), `post_dur=9.511,0s` (~158,5 min),
faixa `BIS/EEG1_WAV`.

### Por que não o caso 1

O caso `1`, citado por uma sessão anterior da Fase 0.6 (não commitado,
"1.477.269 amostras reais") **NÃO é utilizável** sob a definição PRE/POST
de `METHODOLOGY_NOTE.md` Gap (c): `anestart=-552s`, ou seja, a indução de
anestesia começou 552s ANTES do início da própria gravação da faixa
(`casestart=0`). Não existe amostra de EEG anterior a `anestart` nesse
caso — não há segmento PRE possível. Isso foi confirmado por re-download
e re-verificação NESTA sessão (não assumido do relato da sessão
anterior), e é exatamente o motivo pelo qual `prepare_vitaldb.py` re-
verifica `casestart <= anestart <= caseend` para TODOS os casos antes de
escolher, em vez de reusar a escolha da Fase 0.6 sem checagem.

## Caso e faixa selecionados

| Campo | Valor |
|---|---|
| `caseid` | `408` |
| `track_id` (`BIS/EEG1_WAV`) | `060396a4522784ed0e040be14273b2d6ab321c32` |
| `casestart` / `caseend` (s, relativo ao início do registro) | `0` / `11495` |
| `anestart` / `aneend` (s) | `1984` / `11884` |
| Frequência de amostragem | `128,0000 Hz` (confirmada por reconstrução da grade + checagem contra o último timestamp explícito do CSV) |
| Departamento / tipo de cirurgia | Thoracic surgery / Major resection |
| Tipo de anestesia | Geral |
| Idade / sexo do paciente | 53 / F |

## Reconstrução da série temporal a partir do CSV bruto da API

O CSV retornado por `/{track_id}` tem colunas `Time,valor`; `Time` só vem
preenchido na primeira amostra, na segunda amostra (que revela o
intervalo fixo de amostragem, `1/128s`), e num timestamp final de
resincronização — todas as linhas intermediárias deixam `Time` em
branco (amostragem uniforme implícita). Linhas com `valor` em branco são
amostras PERDIDAS (artefato de sinal/desconexão do sensor) — **excluídas,
nunca interpoladas ou fabricadas**.

- `n_valid_samples = 1.470.928` (de 1.471.261 linhas de dado totais)
- `n_missing_samples_dropped = 333` (`frac_missing = 0,000226`, 0,023%)
- Checagem de reconstrução da grade de amostragem: `OK` (o timestamp
  final explícito do CSV, `11492,96s`, bate com a reconstrução via
  `dt=1/128s` dentro de tolerância de 0,5s)
- Intervalo de tempo efetivamente coberto pelas amostras válidas:
  `[0,93, 11492,96]` s

## Definição PRE/POST (Gap (c), regra específica de VitalDB)

- **PRE** = EEG antes de `anestart` (1.984s) → **n=253.825 amostras
  válidas** (1.983,0s ≈ 33,05 min).
- **POST** = EEG após `anestart`, até `min(aneend, fim da faixa
  gravada)`. Aqui `aneend=11.884s` é POSTERIOR ao fim da faixa
  efetivamente gravada (`11.492,96s`) — ou seja, o registro de EEG
  termina antes do fim documentado da anestesia. **POST é então limitado
  pela disponibilidade real do dado (fim da faixa), não por
  `aneend`** — reportado honestamente como tal
  (`post_end_capped_by_track_availability=true`), consistente com a
  convenção já usada em `grafo-de-visibilidade` para o domínio de
  hidrologia (fronteira aberta = fim do registro disponível, quando esse
  é o fator limitante em vez do evento documentado). **n=1.217.103
  amostras válidas** (9.508,6s ≈ 158,5 min).
- Não foi identificada uma intervenção farmacológica documentada,
  isolada e datada, anterior a `aneend`/fim da faixa para usar como
  fronteira alternativa (o caso tem faixas contínuas de infusão de
  propofol/remifentanil — `Orchestra/PPF20_*`, `Orchestra/RFTN20_*` —
  mas não um evento discreto único "próxima intervenção", diferente do
  timestamp único e externo `anestart`/`aneend`); a fronteira usada é a
  mais conservadora e diretamente documentada disponível.

## Variantes de robustez (Gap (c), reaproveitada sem modificação)

- **PRE robustez:** os 50% mais recentes (por contagem) do PRE primário
  → `n=126.913`.
- **POST robustez:** os 50% mais próximos da transição do POST primário
  → `n=608.551`.

## Subamostragem (Gap (d))

`MAX_N_PER_SEGMENT=20.000`, decimação por *stride* uniforme, aplicada
DENTRO de `pe_common.run_pe_analysis` (não manualmente aqui) —
identicamente às 2 variantes deste domínio e ao domínio EDB. Ver
`vitaldb_segments_meta.json` para os `n` brutos de cada segmento antes
da subamostragem; os `stride`/`n_used` efetivamente aplicados por
`run_pe_analysis` ficam registrados em `config.pre_subsample_info` /
`config.post_subsample_info` de cada `result_vitaldb_*.json`.

## Arquivos locais

- `vitaldb_pre_primary.npy`, `vitaldb_post_primary.npy`,
  `vitaldb_pre_robust.npy`, `vitaldb_post_robust.npy` — segmentos
  derivados (já filtrados por tempo/evento, ANTES da subamostragem
  Gap (d), que é aplicada automaticamente dentro do pipeline em tempo de
  execução) — commitados neste diretório.
- `vitaldb_segments_meta.json` — metadados completos da preparação.
- **Os downloads brutos multi-MB (`cases.csv` ~2,4MB, `trks.csv`
  ~9,3MB, o CSV completo da faixa `BIS/EEG1_WAV` do caso 408 ~9,4MB) NÃO
  foram commitados** — reproduzíveis integralmente reexecutando
  `python3 prepare_vitaldb.py` (instrução explícita da sessão
  orquestradora para este passo: documentar via URL/proveniência em vez
  de commitar arquivos brutos grandes).
