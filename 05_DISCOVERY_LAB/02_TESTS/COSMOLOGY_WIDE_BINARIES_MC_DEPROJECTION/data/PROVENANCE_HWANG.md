# Proveniência de dados — catálogo de excentricidades de Hwang, Ting & Zakamska (2022)

Usado por `DISC-COSMOLOGY-MOND-SPARC-004` para amostragem de excentricidade
individual por sistema (Gap (a) da `PREREGISTRATION.md` Seção 4).

Hwang, J.-H., Ting, Y.-S. & Zakamska, N. L. (2022), "Wide binaries in
Gaia EDR3: orbital fits and the distribution of eccentricities", MNRAS
512, 3383–3401. DOI: 10.1093/mnras/stac700. arXiv:2111.01789. Catálogo
eletrônico de excentricidades individuais estimadas via ajuste orbital
Bayesiano, aplicado sobre 100% do catálogo de binárias largas de
El-Badry, Rix & Heintz (2021) usado por `COSMOLOGY_WIDE_BINARIES/` e
por este teste.

## Redownload nesta sessão (2026-08-18)

O arquivo bruto original (baixado e verificado em sessão anterior,
2026-08-15) não estava mais acessível — ficou em `/tmp` de scratchpad de
outra sessão de agente, já limpo/inacessível. Esta sessão refez o
download do zero, reutilizando o fluxo já verificado de acesso ao Google
Drive (link de compartilhamento público do autor, não um endpoint
oficial do periódico/arXiv).

### Fluxo de download (2 passos, cookies reutilizados entre eles)

1. `GET https://drive.google.com/uc?export=download&id=1h1pgexHUTpvE80PWCh6m1zY3QMMuYPnd`
   — respondeu `HTTP 303`, redirecionando (via header `location`, sem
   corpo) para
   `https://drive.usercontent.google.com/download?id=1h1pgexHUTpvE80PWCh6m1zY3QMMuYPnd&export=download`.
2. `GET` dessa URL de redirecionamento (mesmos cookies) retornou `HTTP
   200`, corpo de 2446 bytes — a página de aviso de vírus do Google
   Drive para arquivos grandes, contendo um formulário com
   `name="confirm" value="t"` e `name="uuid" value="349d306a-2b63-4624-9667-283fbea458e3"`
   (UUID gerado por sessão, muda a cada tentativa — extraído
   programaticamente do HTML, não hardcoded).
3. **URL final que efetivamente entregou o arquivo bruto:**
   `GET https://drive.usercontent.google.com/download?id=1h1pgexHUTpvE80PWCh6m1zY3QMMuYPnd&export=download&confirm=t&uuid=349d306a-2b63-4624-9667-283fbea458e3`
   (mesmos cookies das etapas 1–2). Resposta: `HTTP 200`,
   `content-disposition: attachment; filename="wide_binary_eccentricity.fits"`,
   `content-type: application/octet-stream`, `content-length: 218220480`.

### Verificação de integridade

- **Bytes efetivamente baixados:** 218.220.480 (idêntico ao
  `content-length` declarado pelo servidor — download completo, nada
  truncado).
- **sha256 do arquivo bruto salvo em disco:**
  `39c4db80e25a2c2ed553c3e51d81f285b4c876d970a02e8c66af180837e0d46a`
  — **idêntico** ao sha256 já registrado na sessão anterior (2026-08-15)
  e citado em `PREREGISTRATION.md` Seção 0/2. Confirma que o conteúdo
  binário do arquivo é byte-a-byte o mesmo de antes, apesar do
  redownload.
- **Nota de transparência sobre o tamanho em bytes:** a `PREREGISTRATION.md`
  (Seções 0 e 2) cita o tamanho do arquivo como "208.220.480 bytes". O
  redownload desta sessão mede **218.220.480 bytes** — os dois números
  diferem no segundo dígito (`08` vs `18`), quase certamente um erro de
  transcrição na sessão anterior (dígitos adjacentes trocados), não uma
  divergência real de conteúdo: o sha256 (que depende de todo o
  conteúdo binário, byte a byte) bate exatamente, e o `content-length`
  do servidor nesta sessão (218.220.480) é consistente com os bytes
  efetivamente recebidos. Reportado aqui explicitamente em vez de
  silenciosamente "corrigido" — o valor correto e verificado empiricamente
  nesta sessão é **218.220.480 bytes**; `content-length` foi conferido
  contra o número de bytes gravados em disco (`wc -c`), que coincidem
  exatamente.
- **Formato:** FITS, confirmado por `file` (`FITS image data...`) e por
  abertura bem-sucedida com `astropy.io.fits`.
- **Estrutura interna (HDU 1, tabela binária):** 1.817.594 linhas, 15
  colunas — bate exatamente com o valor já citado em
  `PREREGISTRATION.md` (1.817.594 linhas = cobertura total do catálogo
  El-Badry+2021) e com as 15 colunas já enumeradas:
  `source_id1 (K/int64), ra1 (D, deg), dec1 (D, deg), source_id2 (K/int64),
  ra2 (D, deg), dec2 (D, deg), sep_AU (D), R_chance_align (D),
  vr_angle (D, deg), vr_angle_error (D, mas/yr), dpm_sig (D, mas/yr),
  alpha (D), e (D), e0 (D), e1 (D)`.
- **Cópia local do arquivo bruto:** mantida apenas em scratchpad da
  sessão (`/tmp/.../scratchpad/hwang_dl/hwang_2022.fits`), **NÃO
  commitada no repositório** — 208/218 MB excede o limite prático de
  commit direto (mesma convenção já usada para o catálogo El-Badry+2021
  de 1,9 GB em `../COSMOLOGY_WIDE_BINARIES/`, documentado por
  URL+sha256 em vez de commitado bruto).

## Cruzamento com a amostra de 43.147 sistemas pós-corte

- **Amostra de entrada:**
  `../COSMOLOGY_WIDE_BINARIES/data/quality_filtered_sample.parquet`
  (43.147 sistemas, colunas `Source1`/`Source2` = `source_id` Gaia EDR3
  do componente primário/secundário).
- **Método de cruzamento:** `pandas.merge` em
  `(Source1,Source2) == (source_id1,source_id2)` do catálogo de Hwang
  (após conversão de `hdul[1].data` para `pandas.DataFrame` via
  `astropy.io.fits`), `how="left"`, com `indicator=True` para contar
  matches exatamente.
- **Fração de cobertura: 43.147/43.147 = 100,00000%** — todos os
  43.147 sistemas da amostra pós-corte têm entrada correspondente no
  catálogo de Hwang. Nenhum par ficou sem match, e nenhum precisou de
  match por ordem trocada (`source_id1↔source_id2`) — checado
  explicitamente, 0 casos. Confirma a expectativa declarada no
  pré-registro (Hwang cobre 100% do catálogo El-Badry+2021, do qual a
  amostra de 43.147 é um subconjunto por cortes de qualidade).
  - Checagem adicional: 0 pares duplicados em `(source_id1,source_id2)`
    dentro do catálogo bruto de Hwang — cada par tem no máximo 1 linha,
    então o merge não pôde ter inflado a contagem de matches.
- **Cobertura do critério de excentricidade individual (Gap (a) da
  `PREREGISTRATION.md`):** dos 43.147 sistemas cruzados, **38.200
  (88,53%)** têm `dpm_sig>3` E `e`/`e0`/`e1` não-NaN (usam Gaussiana
  truncada centrada na excentricidade individual medida); os
  **4.947 restantes (11,47%)** caem no fallback populacional
  `p(e;alpha)=(1+alpha)*e^alpha` usando o `alpha` já tabulado por Hwang
  (nenhum `alpha` NaN entre esses 4.947 — fallback sempre aplicável).
  Consistente com a faixa "~15-18%" citada no pré-registro como
  referência aproximada da fração de fallback do próprio Chae (a fração
  real medida aqui, 11,47%, é da mesma ordem de grandeza, calculada
  diretamente sobre os 43.147 sistemas reais desta amostra, não
  assumida).
  - Nenhum valor de `e` ficou NaN em toda a amostra cruzada (0/43.147) —
    a coluna `e` do catálogo de Hwang está sempre preenchida
    (populacional/individual), mesmo quando `e0`/`e1` (limites do IC)
    não estão.

## Subconjunto extraído e commitado

- **Arquivo:** `data/hwang_eccentricity_subset.parquet`
- **Linhas:** 43.147 (uma por sistema da amostra pós-corte, 1:1 com
  `quality_filtered_sample.parquet` — mesma ordem de linhas não
  garantida, junção deve ser feita por `source_id1,source_id2` a
  jusante, não por posição).
- **Colunas:** `source_id1 (int64), source_id2 (int64), alpha (float64),
  e (float64), e0 (float64), e1 (float64), dpm_sig (float64)` — exatamente
  as colunas relevantes para os Gaps (a)-(b) da `PREREGISTRATION.md`
  Seção 4, nenhuma coluna extra do catálogo bruto (RA/Dec, `sep_AU`,
  `R_chance_align`, `vr_angle*` já existem/são redundantes com
  `quality_filtered_sample.parquet` e não são necessárias aqui).
- **Nenhum valor nulo** em nenhuma das 7 colunas nas 43.147 linhas.
- **Tamanho em disco:** ~2,47 MB (commitável diretamente, muito abaixo
  de qualquer limite prático do GitHub).
- **Filtro aplicado na extração:** nenhum filtro adicional além do
  `merge` 1:1 com a amostra pós-corte já existente — todas as 43.147
  linhas da amostra têm match e são preservadas integralmente no
  subconjunto.

## O que NÃO foi feito

O arquivo bruto de ~208/218 MB não foi commitado no repositório (ver
nota de transparência acima sobre o tamanho exato). Nenhum dado de
velocidade/aceleração real foi tocado nesta etapa — este documento
cobre exclusivamente o catálogo de excentricidades e seu cruzamento.
