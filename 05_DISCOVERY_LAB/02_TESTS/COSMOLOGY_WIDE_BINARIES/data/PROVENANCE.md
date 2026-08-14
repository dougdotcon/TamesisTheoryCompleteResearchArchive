# Proveniência de dados — DISC-COSMOLOGY-MOND-SPARC-003

Catálogo de binárias largas do Gaia eDR3: El-Badry, K., Rix, H.-W. &
Heintz, T. M. (2021), "A million binaries from Gaia eDR3: sample
selection and validation of Gaia parallax uncertainties", MNRAS 506,
2269–2295. DOI: 10.1093/mnras/stab323. arXiv:2101.05282. Catálogo
VizieR `J/MNRAS/506/2269`.

Mesmo catálogo usado por Chae, K.-H. (2023), ApJ 952, 128, para testar
quebra de gravidade padrão em binárias largas de baixa aceleração.

## ReadMe oficial

- **URL exata:** `https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/ReadMe`
- **Baixado em:** 2026-08-14 (nesta sessão, via `curl`, HTTP 200)
- **Tamanho:** 84965 bytes (confirmado por `Content-Length` do HEAD e por
  `wc -c` do arquivo salvo)
- **sha256:** `b04eb71613f35a5fe46367bb2b930eee03036018ae8ea36f73b3f72d5cca83c3`
- **Cópia local:** `data/ReadMe`
- **Última modificação no servidor:** `Fri, 07 Aug 2026 09:42:38 GMT`
  (Etag `14be5-65871d33344a5`)

## Catálogo completo (catalog.dat.gz)

- **URL exata:** `https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/catalog.dat.gz`
- **Content-Length declarado pelo servidor (HEAD, 2026-08-14 17:54:47 GMT):**
  1937351290 bytes
- **Bytes efetivamente baixados:** 1937351290 (idêntico ao
  Content-Length declarado — download 100% completo, nada truncado)
- **Download completo?** SIM
- **sha256 do arquivo bruto (.gz) salvo em disco:**
  `0be0f09484ad7279e00ec5a97655c94dfb7377cdadd795a91978941112910f6f`
  (calculado duas vezes, de forma independente — uma vez via
  `sha256sum` direto no shell, outra vez dentro de
  `analysis/parse_catalog.py`; os dois valores coincidem)
- **Integridade do gzip:** `gzip -t catalog.dat.gz` → OK (sem erro de
  CRC/truncamento)
- **Método de download:** `curl -C - --retry 20 --retry-delay 5
  --retry-all-errors -o catalog.dat.gz <url>` (suporte a resume
  habilitado). **Nota de transparência:** a primeira tentativa de
  download nesta sessão foi interrompida por volta de 715243520 bytes
  (36,9%) porque o processo `curl` em background morreu silenciosamente
  entre chamadas de ferramenta (nohup/disown manual não sobreviveu à
  fronteira entre invocações da ferramenta de shell). O download foi
  **retomado com `-C -` a partir do byte 715243520** (não recomeçado do
  zero) usando o mecanismo de background nativo da ferramenta, e
  completou sem mais interrupções. O arquivo final foi verificado
  íntegro por `gzip -t` + sha256 duplo + contagem de linhas exata (ver
  abaixo) — a interrupção intermediária não deixou nenhum resíduo
  corrompido no arquivo final.
- **Data/hora do download:** iniciado 2026-08-14 17:54:15 UTC
  (1ª tentativa), retomado ~18:05 UTC, concluído 2026-08-14 18:23:44 UTC
- **Taxa observada:** ~0.8–1.9 MB/s através do proxy do ambiente,
  variável (medida por range-request de teste inicial: 50 MiB em
  66,86s = ~784 kB/s; taxa da fase final de download chegou a
  ~1,9 MB/s)
- **Cópia local:** `data/catalog.dat.gz` (mantido intacto — NÃO apagado
  após o parse, para permitir reverificação do checksum a qualquer
  momento)
- **Etag no servidor:** `7379a27a-657e854ac02bd`
- **Last-Modified no servidor:** `Fri, 31 Jul 2026 13:40:24 GMT`
- **Content-Type:** `application/x-gzip`

Nenhum dado foi fabricado, truncado silenciosamente ou reamostrado. Se
o tamanho final divergir do `Content-Length` declarado, isso está
reportado explicitamente no campo "Download completo?" acima e em
`data/parse_manifest.json` — não foi mascarado.

## Estrutura de colunas

- **217 colunas** por linha de `catalog.dat`, separadas por `|` (pipe),
  cada uma com largura fixa conforme o bloco "Byte-by-byte Description
  of file: catalog.dat" do ReadMe oficial (bytes 115–667 do arquivo
  `ReadMe`). Largura total por linha = 2844 bytes = `Lrecl` declarado
  no "File Summary" do ReadMe, confirmado empiricamente (amostra real
  de 19611 linhas descomprimidas, todas com exatamente 2844 caracteres
  + quebra de linha, 217 campos ao fazer split por `|`, 0 linhas fora
  do padrão).
- Dicionário completo de colunas (nome, bytes, formato Fortran, unidade,
  nome CDS interno `snake_case`, descrição, convenção de nulo por
  coluna) documentado em `data/COLUMN_DICTIONARY.md`, extraído
  **programaticamente** do ReadMe real (não digitado à mão) — script de
  extração embutido em `analysis/parse_catalog.py::parse_readme_columns`.
- Colunas terminadas em `1`/`2` referem-se ao componente primário
  (Gmag mais brilhante) e secundário do par, respectivamente. Colunas
  sem sufixo (`theta`, `sepAU`, `BinType`, `Sigma18`, `R`) descrevem o
  par como um todo.
- Convenção de nulo: 78 das 217 colunas são documentadas no ReadMe como
  opcionais (prefixo `?`). Dentro dessas, a maioria (astrometria eDR3
  auxiliar: pseudocolor, scan-direction-strength) usa a sentinela
  numérica literal `1.0E20`; as colunas de cross-match com Gaia DR2
  (`dr2plx*`, `dr2pmRA*`, `dr2pmDE*` e erros) usam campo vazio. Ambas
  as convenções foram confirmadas por inspeção de linhas reais (não
  assumidas do texto do ReadMe sozinho).

## Contagem de linhas / sistemas binários

- **Esperado (abstract do paper, El-Badry+2021):** 1817594 pares
- **Esperado (File Summary do ReadMe, `Records` de catalog.dat):** 1817594
- **Contagem real obtida no parse:** 1817594
- **Diferença:** 0 (contagem exata)
- **Verificação cruzada independente:** a distribuição de `BinType`
  obtida do parquet real bate exatamente, linha a linha, com as
  contagens documentadas na Nota (1) do ReadMe:
  MSMS=1412903, MS??=378877, WDMS=22563, WDWD=1565, ????=1040, WD??=646
  (soma = 1817594) — forte evidência independente de que o parse não
  introduziu nem descartou nenhuma linha.

## Parsing / formato tabular

- **Script:** `analysis/parse_catalog.py`
- **Método:** streaming — `gzip.open(...,'rt')` alimenta
  `pandas.read_csv(sep="|", chunksize=200000)` diretamente; o `.dat`
  descomprimido completo (~5,2 GB estimado: 2844 bytes × 1817594
  linhas) **nunca é materializado inteiro em disco**, só o `.gz` bruto
  (proveniência) e o `.parquet` final (tabular) — economia de espaço
  em disco (~17 GB disponíveis no ambiente).
- **Tipos:** colunas de formato Fortran `I*` → inteiro (`Int64`
  anulável do pandas); `F*`/`E*` → `float64`; `A*` (5 colunas:
  `BinType`, `APF1`, `APF2`, `Dup1`, `Dup2`) → string. Nenhuma conversão
  semântica além de string→número foi aplicada — a sentinela `1.0E20`
  foi preservada literal (NÃO convertida para NaN nesta etapa; ver
  `COLUMN_DICTIONARY.md`), e campos vazios tornam-se `NaN`/`<NA>`
  naturalmente na conversão numérica (isso não é fabricação, é a
  representação padrão do pandas para "nada estava lá").
- **Saída:** `data/catalog.parquet` (compressão `zstd`), tamanho no
  disco: 2322928442 bytes (~2,16 GiB), 10 row-groups, 1817594 linhas ×
  217 colunas confirmado via `pyarrow.parquet.ParquetFile(...).metadata`.
- **Tempo total do parse (download já concluído → parquet pronto):**
  ~482 s (~8 min) numa máquina de 4 vCPU / 15 GiB RAM.
- **Arquivo de definição de colunas (JSON, gerado do ReadMe real):**
  `data/column_definitions.json`
- **Manifesto do parse (contagens, sha256, tempos):**
  `data/parse_manifest.json`

## Coluna de massa estelar: NÃO existe no catálogo

Confirmado de duas formas independentes: (1) inspeção completa das 217
colunas do bloco byte-by-byte do ReadMe oficial (nenhuma delas contém
"mass", "Mass" ou similar no nome ou explicação — busca `grep -i mass`
no ReadMe completo só encontra ocorrências no texto do abstract e na
seção "See also", nunca no bloco de definição de colunas de
`catalog.dat`); (2) busca programática pelo substring `"mass"` (case
insensitive) diretamente no `schema.names` do `catalog.parquet` já
parseado — **zero colunas encontradas**. O catálogo fornece
apenas astrometria (posição, paralaxe, movimento próprio) e fotometria
Gaia (`Gmag`, `BPmag`, `RPmag` + fluxos e erros) por componente, mais
metadados de qualidade astrométrica/fotométrica e a classificação
`BinType` (MS/WD). O abstract do próprio paper cita "massas... de WDs"
como uma das aplicações de acompanhamento possibilitadas pelo catálogo
público — não como algo já incluído nele.

**Implicação para o teste:** massa estelar de cada componente
precisará ser **derivada**, não lida diretamente. A via padrão na
literatura (inclusive citada no ReadMe em "See also",
e.g. `J/ApJ/870/9`, `J/AJ/161/63`) é magnitude absoluta em G (via
`Gmag` + paralaxe `Plx`, com correção de extinção se aplicável) →
relação massa-luminosidade (isócronas ou relações empíricas MS,
diferentes para MS vs. WD via `BinType`). A escolha exata da relação
M/L (e se replicar bit-a-bit a de Chae 2023) é matéria da verificação
de metodologia paralela mencionada em
`phase0/PHASE0_SEARCH.md` — **não decidida nem aplicada aqui**.

## Checagem de sanidade sobre o parquet real (amostra de colunas-chave)

Executada após o parse completo, carregando `catalog.parquet` real
(não amostra sintética):

- `Source1`/`Source2` (source_id Gaia EDR3): inteiros de ~19 dígitos
  não sequenciais (ex. `4282339100022417152`, `4089436931798712576`)
  — consistentes com IDs reais do Gaia (ao contrário do padrão
  sequencial/artificial encontrado no dataset fabricado descrito em
  `phase0/PHASE0_SEARCH.md`).
- `sepAU` (separação projetada): min=5.11 AU, mediana=3255 AU,
  max=206265 AU (=1 pc, exatamente o limite superior declarado no
  abstract do paper — "separações... de poucos AU até 1pc").
- `R` (chance-align ratio): min≈1.07e-185, mediana=7.6e-4,
  max≈6.7e10 — distribuição extremamente assimétrica como esperado de
  uma razão de densidades KDE (não normalizada a [0,1]; o corte
  recomendado pelos autores é `R<0.1`, a ser decidido no
  pré-registro).
- `dr2plx1` (paralaxe DR2 do primário): 17514/1817594 linhas nulas
  (0,96%) — consistente com "a maioria das fontes eDR3 tem
  contraparte DR2, mas nem todas".
- `pscol1` (pseudocolor): 1439007/1817594 linhas (79,2%) com o valor
  sentinela literal `1.0E20` — a maioria das fontes usa modelo
  astrométrico de 5 parâmetros (sem pseudocolor), consistente com a
  documentação do Gaia EDR3.
- `BinType`: distribuição bate exatamente com o ReadMe (ver acima).

## O que NÃO foi feito nesta etapa (por desenho)

- Nenhum corte de qualidade (`R<0.1`, RUWE, faixa de `sepAU`, remoção
  de triplas, etc.) foi aplicado.
- Nenhuma estatística de teste, split discovery/holdout, ou cálculo de
  velocidade normalizada/aceleração foi realizado.
- Nenhuma conversão de sentinela `1e+20` para `NaN` foi realizada (dado
  bruto preservado tal como está no arquivo original).
- `shift.dat` (catálogo de alinhamentos casuais "deslocados", usado
  pelos autores para calibrar `R`) **não foi baixado** nesta etapa —
  não foi pedido e não é necessário para o teste `SPARC-003` em si
  (apenas para quem quisesse re-derivar `R` do zero, o que não é o
  caso: `R` já vem pronto no catálogo principal).

Essas decisões ficam para o pré-registro formal do teste
`DISC-COSMOLOGY-MOND-SPARC-003`, após a verificação paralela da
metodologia exata de Chae (2023).

---

## Adição — relação massa-luminosidade (Pecaut & Mamajek 2013)

- **URL exata:** `https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt`
- **Baixado em:** 2026-08-14, HTTP 200, 55.680 bytes.
- **Referência primária:** Pecaut, M.J. & Mamajek, E.E. (2013), "Intrinsic
  Colors, Temperatures, and Bolometric Corrections of Pre-main-sequence
  Stars", ApJS 208, 9. Tabela mantida e atualizada continuamente por
  Eric Mamajek (versão 2022.04.16 no cabeçalho do arquivo).
- **Cópia local:** `data/EEM_dwarf_UBVIJHK_colors_Teff.txt` (bruto,
  íntegro, não editado).
- **Extração:** colunas `M_G` (magnitude absoluta Gaia G) e `Msun`
  (massa em massas solares) extraídas programaticamente para todas as
  linhas com AMBOS os valores presentes (não `...`/placeholder) —
  72 pontos válidos, de B3V (`M_G=-1,19`, `Msun=5,4`) a L2V
  (`M_G=17,3`, `Msun=0,075`), cobrindo folgadamente a faixa
  `4<M_G<14` exigida pelo corte de qualidade do pré-registro. Tabela
  extraída salva em `data/mamajek_mass_luminosity.tsv`. Script de
  extração: `analysis/generate_split_and_bins.py` (função de
  interpolação) usa esta tabela via `numpy.interp` linear.

## Adição — amostra filtrada por qualidade e split discovery/holdout

Aplicação dos cortes de qualidade e derivação de massa:
`analysis/apply_quality_cuts.py`, executado 2026-08-14. Resultado:
**43.147 sistemas** sobrevivem a todos os cortes (`BinType==MSMS`,
`R<0,01`, `200<sepAU<30000`, distância média `<200pc`, concordância de
distância `3sigma`, erro relativo de PM `<0,01` em ambas componentes,
`4<M_G<14` em ambas componentes) E têm interpolação de massa bem
sucedida (`M_G` de ambas componentes dentro da faixa tabelada de
Mamajek). Massa total (`Mtot_Msun`): min=0,220, max=2,309. Separação
(`sepAU`): min=200,0, max=29981,6 (bate com o corte declarado).
Distância média: min=7,2pc, max=200,0pc. Amostra salva em
`data/quality_filtered_sample.parquet` (14.176.456 bytes).

Split discovery/holdout gerado por `analysis/generate_split_and_bins.py`
(seed=20260814, `numpy.random.default_rng`, 70%/30%): **30.203**
sistemas de descoberta, **12.944** de holdout. Lista completa (por
identificador de par `Source1_Source2`) em
`data/discovery_holdout_split.json` (sha256
`8c4d72fe0aad3f2ff6b4361d79b23a6e11489ad00d439653c2091bbe850caed7`).
**Holdout selado, não tocado por nenhuma análise deste pré-registro.**

Bordas de bin em `log10(g_N)` (5 quantis, calculadas SOMENTE sobre
`Mtot_Msun` e `sepAU` da amostra de descoberta, nunca movimento
próprio/velocidade): `[-11,7012; -9,1728; -8,4667; -7,9752; -7,5548;
-6,5224]`, ~6.040-6.041 sistemas por bin.

## Nota sobre arquivos grandes NÃO commitados no git

`data/catalog.dat.gz` (1,94 GB) e `data/catalog.parquet` (2,16 GB) são
grandes demais para versionar em git de forma prática. Eles NÃO estão
commitados no repositório — a proveniência acima (URL exata, sha256,
Content-Length, contagem de linhas) é suficiente para qualquer agente
futuro re-baixar e re-derivar `catalog.parquet` de forma
byte-idêntica a partir de `catalog.dat.gz`, e `catalog.dat.gz` a partir
da URL original, sem depender de os arquivos brutos estarem no
repositório. `data/quality_filtered_sample.parquet` (14 MB, a amostra
já filtrada que a análise pré-registrada de fato usa) e
`data/discovery_holdout_split.json` (1,8 MB) SÃO commitados, por serem
pequenos o bastante e por serem o input direto da análise (reprodutível
de forma determinística a partir do catálogo bruto + os dois scripts
`apply_quality_cuts.py`/`generate_split_and_bins.py`, mas commitados de
qualquer forma para não exigir re-baixar 1,94 GB só para conferir a
análise).
