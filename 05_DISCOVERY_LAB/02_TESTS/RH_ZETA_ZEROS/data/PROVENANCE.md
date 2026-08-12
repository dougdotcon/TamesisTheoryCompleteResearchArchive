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
