# Proveniência de dados — RH-REAL (DISC-RH-REAL-001)

## Fonte: tabelas de Andrew Odlyzko (zeros reais da função zeta de Riemann)

- **URL base (verificada por fetch direto em 2026-08-12):**
  `https://www-users.cse.umn.edu/~odlyzko/zeta_tables/index.html`
  (a URL antiga, `dtc.umn.edu`, redireciona 301 para este domínio —
  confirmado nesta sessão, não assumido).
- **Autoria:** Andrew M. Odlyzko, cálculo numérico de zeros não-triviais
  de ζ(s) sobre a linha crítica (parte imaginária γ tal que ζ(1/2+iγ)=0),
  método de Riemann-Siegel + Odlyzko-Schönhage.

### Arquivos baixados

| Arquivo local | Fonte | Conteúdo | sha256 | Linhas |
|---|---|---|---|---|
| `zeros1.txt` | `zeta_tables/zeros1` | Primeiros 100.000 zeros, texto plano, um por linha | `3436c916a7878261ac183fd7b9448c9a4736b8bbccf1356874a6ce1788541632` | 100.000 |
| `zeros2.txt` | `zeta_tables/zeros2` | Primeiros 100 zeros com >1000 dígitos decimais de precisão | `0439d90a4c025d1ab3ed25f2241f27afeb6d01e651d95672267783b859ee170f` | 100 |
| `zeros3.txt` | `zeta_tables/zeros3` | Zeros #10¹²+1 até #10¹²+10⁴, como offsets de γ=267653395647 (regime de altura muito maior, para checagem cruzada fora do regime de baixa altura) | `75a1f1a978d5e3eddd16518f661d41a95a40b33782389ba02ec4ed0ce0764807` | 10.009 (3 linhas de cabeçalho + 10.000 valores + 6 linhas finais) |

- **Data de acesso:** 2026-08-12.
- **Verificação de conteúdo:** primeiro valor de `zeros1.txt` é
  `14.134725142`, batendo com o valor didático conhecido do primeiro zero
  não-trivial de ζ(s) — confirma que o conteúdo é real, não um stub ou
  placeholder.

### Fontes verificadas mas NÃO baixadas nesta sessão

- **LMFDB** (`https://www.lmfdb.org/zeros/zeta/`): fonte real e
  autoritativa (103.800.788.359 zeros catalogados, cômputo de David
  Platt via método de Turing, precisão ±2⁻¹⁰²), mas o acesso programático
  (curl/requests) foi bloqueado por captcha/verificação humana JS nesta
  sessão — confirmado por tentativa direta, não assumido. Tratada como
  referência de citação/proveniência para precisão, não como fonte de
  download nesta trilha, a menos que um humano salve resultados de
  consulta manualmente no futuro.
- **`mpmath.zetazero(n)`**: computa o n-ésimo zero diretamente, sem
  precisar de arquivo — disponível como ferramenta de verificação
  independente/extensão para além do alcance das tabelas estáticas
  (documentação: https://mpmath.readthedocs.io/en/latest/functions/zeta.html).

## Limitação de escopo desta trilha (Fase 0)

Estes dados cobrem: (a) todos os primeiros 100.000 zeros continuamente, e
(b) uma amostra de 10.000 zeros na vizinhança do zero #10¹². Não cobrem
alturas intermediárias nem o regime de altura muito maior (`zeros4`/`zeros5`,
zeros próximos de #10²¹/#10²²) — esses últimos existem na mesma fonte e
podem ser baixados em uma fase futura se um teste específico exigir.

---

## Adição — Gate de Replicação, terceiro dataset (`zeros4.txt`)

**Agente:** terceiro agente, independente, executando o Gate de Replicação
para `DISC-RH-ZERO-GAP-RUNS-001` (`03_REPLICATION_GATE/PROTOCOL.md`,
cláusula de fallback da Seção 3 — nenhum holdout selado foi declarado no
pré-registro deste teste, então o Gate exige em vez disso uma checagem de
robustez formal contra pelo menos uma fonte de dado adicional). Este
arquivo NUNCA havia sido baixado, inspecionado, ou tocado nesta sessão
antes desta adição — download feito diretamente pelo agente do Gate,
primeira vez que seu conteúdo real foi visto por qualquer agente.

- **URL exata:** `https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros4`
  (mesmo domínio já verificado como real em `data/PROVENANCE.md` acima —
  fetch direto via `curl`, HTTP 200, 160.319 bytes).
- **Data de acesso:** 2026-08-12.
- **Arquivo local:** `data/zeros4.txt`.
- **sha256:** `10d9f7dab2bbfff6b8befbe6f765969b0b3f38f6110ed1df423931addd52da8f`.
- **Linhas totais:** 10.009 (9 linhas de cabeçalho em prosa + 10.000 linhas
  de dado numérico, linhas 10–10.009 — confirmado por parsing programático,
  não assumido por analogia com `zeros3.txt`, embora a contagem tenha
  acabado batendo com a mesma estrutura de 9 linhas de cabeçalho).
- **Conteúdo/formato:** valores de `gamma - BASE`, onde `BASE =
  144176897509546973000` (21 dígitos, declarado no próprio cabeçalho do
  arquivo: "Values of gamma - 144176897509546973000, where gamma runs over
  the heights of the zeros of the Riemann zeta numbered 10^21 + 1 through
  10^21 + 10^4"). Precisão declarada no cabeçalho: "Values are not
  guaranteed, and are probably accurate to within 10^(-6)" — precisão
  nominal menor que `zeros1.txt` (~9 dígitos decimais) e `zeros3.txt`
  (10⁻⁸), mas ainda ~9-10 ordens de magnitude mais fina que a escala de
  comparação (c ∈ {0,10; 0,20; 0,30}) usada pela estatística de teste
  travada.
- **Verificação de conteúdo:** `BASE + primeiro_offset` =
  144176897509546973000 + 538.49806962 = 144176897509546973538,498...,
  batendo com o valor declarado no próprio cabeçalho para o zero
  #10²¹+1 ("1/2 + i * 144,176,897,509,546,973,538.49806962...") —
  confirma que o conteúdo é real, não um stub ou placeholder, e que a
  base foi lida corretamente.
- **Regime de altura:** γ ≈ 1,44×10²⁰ — ~9 ordens de magnitude acima do
  dataset secundário (`zeros3.txt`, γ≈2,68×10¹¹) e ~15 ordens de magnitude
  acima do primário (`zeros1.txt`, γ até ~75.000).
- **Nota de precisão numérica (relevante para o parsing, não para a
  proveniência em si):** `BASE` tem 21 dígitos significativos e não é
  representável exatamente em `float64` (que carrega ~15-17 dígitos
  significativos) — qualquer script de análise que forme `gamma_n =
  BASE + offset_n` como `float64` e em seguida SUBTRAIA dois desses valores
  para obter o gap sofre cancelamento catastrófico (erro absoluto de
  arredondamento de `BASE` em `float64` ~3×10⁴, muito maior que o gap
  normalizado típico ~0,05–2). Gaps devem ser computados diretamente a
  partir da diferença dos offsets brutos (que não sofrem esse problema,
  por serem O(1)–O(2000)), nunca por subtração de dois `gamma_n` já
  somados em ponto flutuante.
- **Fontes ainda não baixadas nesta sessão:** `zeros5.txt` (regime
  #10²²), não baixado — fora do escopo desta checagem de robustez, que só
  exigia uma fonte adicional.
