# Proveniência dos dados — DISC-SCHUMANN-RESONANCE-001

## Fonte

- **Dataset:** "Four-year measurements from Sierra Nevada ELF station. Year
  2014" (Salinas, Rodríguez-Camacho, Portí, Carrión, Fornieles-Callejón,
  Toledo-Redondo, publicado 2022-03-12, CC-BY-4.0)
- **Página do registro (verificada por fetch direto):**
  https://zenodo.org/records/6348691
- **DOI:** `10.5281/zenodo.6348691` (DOI conceito da série de 4 anos:
  `10.5281/zenodo.6348690`)
- **Arquivo único do registro:** `2014.zip`
- **URL de conteúdo do arquivo (API Zenodo, usada para todos os downloads
  por Range request desta sessão):**
  `https://zenodo.org/api/records/6348691/files/2014.zip/content`
- **Tamanho total do arquivo no servidor (confirmado por `HEAD`/cabeçalho
  `Content-Length` desta sessão):** 26.697.876.825 bytes (≈ 26,70 GB)
- **MD5 do zip completo, conforme metadado da API Zenodo (`GET
  /api/records/6348691`, campo `files[0].checksum`):**
  `md5:916efee568bbbb385bb508541bdff547` — **não foi re-verificado
  byte-a-byte nesta sessão** porque o arquivo completo nunca foi baixado
  (ver "Estratégia de download" abaixo); é citado aqui apenas como o
  checksum publicado pela fonte para o objeto completo.
- **Data de acesso:** 2026-08-27.
- **Licença:** CC-BY-4.0.
- **Outros anos do mesmo dataset, localizados via busca na API Zenodo
  (`GET /api/records?q="Sierra Nevada ELF station"`), NÃO usados nesta
  análise** (citados apenas para registrar que não havia arquivo anual
  menor disponível — todos são do mesmo porte):
  - 2013+2017: `https://zenodo.org/records/6348930` (`2013_2017.zip`,
    26.496.304.719 bytes)
  - 2015: `https://zenodo.org/records/6348773` (`2015.zip`,
    27.603.494.869 bytes)
  - 2016: `https://zenodo.org/records/6348838` (`2016.zip`,
    26.580.844.825 bytes)

## Estratégia de download (subconjunto real, sem baixar os 26,7 GB completos)

Este container tem uma cota de disco pequena e fixa por sessão; baixar o
`2014.zip` inteiro (26,7 GB) não é viável nem necessário. A estratégia
usada, verificada e documentada nesta sessão:

1. **Confirmação de suporte a HTTP Range requests:** `curl` com cabeçalho
   `Range: bytes=0-1023` contra a URL de conteúdo acima retornou
   `HTTP/1.1 206 Partial Content` com `Accept-Ranges: bytes` e
   `Content-Range: bytes 0-1023/26697876825`. Confirmado por fetch direto
   nesta sessão antes de qualquer decisão de estratégia.
2. **Leitura do diretório central do ZIP sem baixar o arquivo inteiro:**
   como o diretório central de um arquivo ZIP fica no final do arquivo, foi
   feita UMA requisição HTTP (Range) pelos últimos 12 MB do arquivo
   (bytes `26685293913-26697876824`), suficiente para conter o End-Of-
   Central-Directory, o localizador/registro Zip64 EOCD (necessário porque
   o arquivo excede 4 GB) e o diretório central completo (33.815 entradas
   para o ano inteiro de 2014). Um objeto Python seekable
   (`analysis/range_zip.py::RangeHTTPFile`) expõe esse cache em memória ao
   módulo padrão `zipfile`, que então lista os nomes de todas as entradas
   sem nenhuma requisição adicional.
3. **Extração seletiva de arquivos individuais:** para cada arquivo horário
   necessário (binário + `_info.txt` companheiro), o offset e o tamanho
   comprimido já são conhecidos a partir do diretório central (sem
   requisição extra); uma única requisição Range cobrindo o cabeçalho
   local + dados comprimidos daquela entrada é feita, e o `zipfile` decodifica
   a partir do cache em memória — sem baixar nenhum outro byte do arquivo.
   `zipfile` valida automaticamente o CRC32 de cada entrada extraída contra
   o valor gravado no diretório central (`BadZipFile` seria levantado em
   caso de divergência); **nenhuma divergência de CRC32 ocorreu em nenhum
   dos arquivos extraídos** — este é o checksum por-arquivo disponível
   (Zenodo só publica MD5 do zip inteiro, não por arquivo interno).
4. **Nenhum dado fabricado, embutido, ou de sessão anterior foi usado em
   nenhum momento** — todo byte analisado veio de uma requisição HTTP real
   contra a URL acima, nesta sessão, com verificação TLS padrão (nenhum
   `verify=False`, nenhuma desabilitação de certificado).

Código completo e comentado da estratégia: `analysis/range_zip.py`
(objeto de arquivo seekable sobre Range requests, com cache) e
`analysis/download_segments.py` (seleção dos arquivos horários específicos
e persistência local).

## Formato interno do arquivo ZIP (confirmado por inspeção direta do
diretório central)

- Estrutura: `2014/<AAMM>/smplGRTU1_sensor_<S>_<AAMMDDHHMM>` (dado binário)
  e `2014/<AAMM>/smplGRTU1_sensor_<S>_<AAMMDDHHMM>_info.txt` (metadado
  companheiro), onde `S` é `0` (orientação NS) ou `1` (orientação EW) —
  confirmado pelo texto da descrição do próprio registro Zenodo: *"a
  specific part to denote the sensor used (0 for the NS orientation and 1
  for the EW orientation)"*.
- Cada mês contém 24 arquivos de dado + 24 `_info.txt` por sensor, quando
  completo (verificado para os 3 dias/mês escolhidos: exatamente 24
  arquivos por canal em cada um, ver Seção "Subconjunto escolhido" abaixo).
- O minuto inicial de cada arquivo horário não é fixo (varia por mês,
  conforme a própria descrição do registro), por isso os nomes exatos
  foram obtidos via correspondência de padrão (regex) contra a listagem
  real do diretório central — nunca assumidos ou inventados.

## Taxa de amostragem real e formato binário (lidos do próprio dado, não
assumidos da literatura)

Conteúdo de exemplo de um `_info.txt` real (arquivo
`2014/1401/smplGRTU1_sensor_0_1401150054_info.txt`, extraído nesta sessão):

```
file name: smpl_sensor_0_1401150054
sampling period (usec): 3906.000000
sampling gain: 0
sampling polarity: 0
1st sample timestamp: 15-01-2014 00:54:05.521 UTC
number of samples: 921600
```

- **Taxa de amostragem confirmada:** período de amostragem = 3906,0 µs
  exatos em TODOS os arquivos `_info.txt` inspecionados (144 arquivos, um
  por hora/canal/segmento) ⇒ `fs = 1e6 / 3906 = 256,0163850486431 Hz` —
  **não** os 256 Hz nominais citados na literatura secundária, embora
  muito próximo (diferença ≈ 0,0164 Hz, ≈ 64 ppm). Esta é a taxa usada em
  `nperseg` do método de Welch (Seção 4 do pré-registro), não um valor
  assumido.
- **Formato binário (16 bits, sinalizado):** `file_size` de cada arquivo de
  dado é exatamente `2 × number_of_samples` bytes (ex.: 1.843.200 bytes =
  2 × 921.600 amostras), confirmando amostras de 16 bits. A conversão para
  volts e o range de saturação (±10 V, 16 bits — 1 bit de sinal + 15 bits
  de amplitude, fator `10/2^15` V/LSB) vêm do texto do artigo de origem
  (Salinas et al. 2022, *Computers & Geosciences*, resumo/trecho indexado
  recuperado por busca nesta sessão — o texto completo do artigo está
  bloqueado por paywall/403 tanto no ScienceDirect quanto no mirror
  `digibug.ugr.es` tentados diretamente nesta sessão).
- **Ordem de bytes (little-endian): determinada empiricamente nesta
  sessão**, não documentada no registro Zenodo (`related_identifiers` do
  registro está vazio — não há link para repositório de código
  companheiro) nem localizável no texto acessível do artigo. Teste direto
  em um arquivo real (`2014/1401/smplGRTU1_sensor_0_1401150054`):
  - Interpretado como `int16` **little-endian**: média ≈ −0,287 V,
    desvio-padrão ≈ 0,234 V, faixa ≈ [−7,37, +7,33] V — estatísticas
    consistentes com um sinal analógico real de baixa amplitude, bem
    dentro do trilho ±10 V, sem saturação.
  - Interpretado como `int16` **big-endian**: média ≈ 0,022 V,
    desvio-padrão ≈ 5,769 V (≈ 10/√3 = 5,77, o desvio-padrão teórico de
    ruído uniforme em ±10 V) e valor mínimo/máximo batendo exatamente nos
    limites de saturação ±10 V — a assinatura estatística clássica de
    bytes trocados de um sinal originalmente suave, produzindo ruído
    quase uniforme, não um sinal físico real.
  - **Little-endian foi adotado** como a interpretação correta, consistente
    com a convenção padrão de sistemas de aquisição baseados em PC/x86 (o
    artigo cita processamento em Python/NumPy, cujo `dtype` nativo em
    hardware x86 padrão é little-endian).
- **Nenhum repositório de código companheiro foi encontrado** referenciado
  pelo próprio registro Zenodo (campo `related_identifiers` vazio) nem por
  busca direcionada (`WebSearch`) por "Schumann resonance data processing
  programs" + GitHub — os únicos resultados encontrados foram as páginas
  do próprio artigo/registro (ScienceDirect, ResearchGate, ADS, ACM DL),
  sem link de repositório de código associado.

## Subconjunto escolhido (Seção 6 do pré-registro: N=3, estações distintas)

Três dias completos de 24h dentro do ano 2014 (o único ano baixado),
espalhados por três estações distintas, cada um com exatamente 24 arquivos
horários por canal (NS e EW) — confirmado por correspondência de padrão
contra a listagem completa do diretório central antes de qualquer
download real:

| Segmento | Rótulo | Estação | Pasta no ZIP | Arquivos NS | Arquivos EW |
|---|---|---|---|---|---|
| 1 | `2014-01-15` | Verão austral / inverno boreal | `2014/1401/` | 24/24 | 24/24 |
| 2 | `2014-04-15` | Primavera boreal | `2014/1404/` | 24/24 | 24/24 |
| 3 | `2014-07-15` | Verão boreal | `2014/1407/` | 24/24 | 24/24 |

Total: 3 segmentos × 2 canais × 24 horas = 144 arquivos de dado binário
(~1,8 MB cada, descomprimido) + 144 `_info.txt` companheiros = 288 arquivos
extraídos, ≈ 264 MB descomprimidos em disco — muito abaixo da cota da
sessão, e uma fração ínfima (~0,001) do arquivo completo de 26,7 GB.

Estatísticas reais de download desta sessão (de
`analysis/download_segments.py`, ver `data/manifest.json`):

- **Requisições HTTP totais:** ver `download_stats.http_requests` em
  `data/manifest.json`.
- **Bytes efetivamente transferidos pela rede:** ver
  `download_stats.bytes_fetched_over_http` em `data/manifest.json`
  (tipicamente comprimido, ~85% do tamanho descomprimido, já que os dados
  são armazenados com `compress_type=8`/DEFLATE no zip).

Arquivos brutos extraídos ficam em `data/raw/<segmento>/<NS|EW>/`, um por
hora, junto com seu `_info.txt`. Metadado completo por arquivo (offsets,
CRC32, sha256 do conteúdo extraído, conteúdo integral do `_info.txt`) está
em `data/manifest.json`.

## Nota sobre versionamento (adicionada na integração, `DISC-DEC-104`)

`data/raw/` (254 MB, 288 arquivos) está listado em `.gitignore` na raiz
do repositório, seguindo o mesmo padrão já usado por
`COSMOLOGY_WIDE_BINARIES` e `TRI_RG/dmd_koopman` — dado bruto grande
intencionalmente excluído do git. Reprodução byte-idêntica é possível a
qualquer momento via `analysis/range_zip.py` + `analysis/
download_segments.py` contra a URL desta seção, e cada arquivo extraído
tem seu CRC32/SHA256 registrado em `data/manifest.json`.

## Nenhum desvio de proveniência

Nenhum dado fabricado, embutido, cacheado de execução anterior, ou de
fallback substituiu qualquer download real. Toda extração falhou de forma
visível (exceção Python) se o CRC32 não batesse — nenhuma ocorreu. TLS
padrão em todas as requisições (`verify=/root/.ccr/ca-bundle.crt`, nunca
desabilitado).
