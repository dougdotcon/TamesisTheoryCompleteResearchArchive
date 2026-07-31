---
session_id: 2026-07-31_0649_RH-NOGO-PRIMARY-SOURCE-AUDIT
started_at: 2026-07-31T06:20:00-03:00
ended_at: 2026-07-31T06:49:05-03:00
agent: claude-opus-5
git_commit_before: e1183da0f765189635d4d227ca4ffce313a77d18
git_commit_after: null
active_work_item: RH-NOGO-001
authorized_action: RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED
result_status: RH_NOGO_PRIMARY_SOURCES_PARTIALLY_SUFFICIENT
files_created:
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/SOURCE_MANIFEST.yaml"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/VON_MANGOLDT_1905_AUDIT.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/HORMANDER_1968_AUDIT.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/RIEMANN_1859_AUDIT.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/BOMBIERI_CLAY_AUDIT.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/CLASS_W_SOURCE_MAPPING.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/SOURCE_BRIDGE_REQUIREMENTS.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/UNRESOLVED_SOURCE_QUESTIONS.md"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/pdf/ (4 PDFs originais, não modificados)"
  - "04_FORMAL_RESEARCH_LAB/08_REVIEWS/SOURCES/RH_NOGO/text/ (4 extrações derivadas)"
  - "04_FORMAL_RESEARCH_LAB/primary-source-audit-result.json"
  - "04_FORMAL_RESEARCH_LAB/09_SESSIONS/2026/2026-07-31_0649_RH-NOGO-PRIMARY-SOURCE-AUDIT.md"
files_modified:
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/STATUS.yaml"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/GAP_REGISTER.yaml"
  - "04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/01_RIEMANN/BIBLIOGRAPHY_AUDIT.md"
  - "04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "04_FORMAL_RESEARCH_LAB/10_TOOLS/labctl.py"
  - "04_FORMAL_RESEARCH_LAB/LAB_STATE.md"
  - "04_FORMAL_RESEARCH_LAB/CHANGELOG.md"
commands_executed:
  - "git rev-parse HEAD / git status --short"
  - "python3 10_TOOLS/labctl.py status / validate"
  - "sudo apt-get install -y poppler-utils"
  - "curl (GDZ, claymath.org, archive.ymsc.tsinghua.edu.cn) + sha256sum"
  - "pdfinfo / pdftotext -layout / pdftoppm -r 170 -png"
  - "python3 -m pytest"
tests_executed:
  - "pytest: 2 passed"
  - "labctl validate: PASS, errors []"
claims_changed: []
gaps_opened:
  - "GAP-RH-009 (fibrados/sistemas)"
  - "GAP-RH-010 (formulação da auto-adjunção)"
  - "GAP-RH-011 (paridade de m)"
  - "GAP-RH-012 (discretude do espectro)"
gaps_closed: []
gaps_updated:
  - "GAP-RH-002 → AUDITED_INSUFFICIENT"
next_single_action: "Obter a fonte primária ou monografia necessária para fechar as hipóteses ainda não sustentadas da Classe W, em especial a lei de Weyl global (W8) e a discretude do espectro (W7)."
---

## Objetivo autorizado

Obter e ler integralmente as fontes primárias dos dois pilares que faltam,
sem iniciar prova, sem escrever a ponte formal, sem construir operador e sem
alterar `RH-NOGO-001` de `SCOPED`.

## Fontes obtidas

Quatro documentos, com proveniência, tamanho e `sha256` em
`SOURCE_MANIFEST.yaml`. Os PDFs não foram modificados; as extrações em
`text/` estão marcadas como derivadas. Nenhuma OCR foi usada.

| Fonte | Origem | Texto legível | Leitura |
|---|---|---|---|
| von Mangoldt 1905 | GDZ Göttingen, `LOG_0007` | **não** (scan de imagem) | pp. 1, 2, 18, 19 lidas como imagens |
| Hörmander 1968 | arquivo Tsinghua (DOI 10.1007/BF02391913) | sim | Seções 1 e 5 |
| Riemann 1859 | claymath.org (tradução Wilkins) | sim | **integral** |
| Bombieri/Clay | claymath.org | sim | Seção I |

EuDML devolveu HTTP 403 a acesso automatizado; o texto de von Mangoldt foi
obtido pelo GDZ. O **original alemão de Riemann não foi obtido** — só a
tradução Wilkins de 1998.

## Achado 1 — o pilar dos zeros está sustentado

von Mangoldt 1905, página 19, resultado final para `T > 28,558`:

```
N = (T/2π) l(T/2π) − T/2π + 7/8 + η(0,43200 lT + 1,91662 llT + 12,20373)
                                                          (−1 < η < 1)
```

Página 2 fixa literalmente as convenções que o gate exigia determinar:
`N` conta zeros de `ξ(t)` cujas **partes reais** estão entre 0 e `T`,
„jede so oft gezählt, als ihre **Ordnungszahl** angibt“ — com
multiplicidade — e `T` é escolhido de modo que a vertical por `T` não passe
por zero algum. O método é o princípio do argumento sobre um contorno com
`a > 1/2` arbitrário: **incondicional**, sem hipótese sobre a localização
dos zeros.

Verificação de consistência interna: a página 1 enuncia a mesma cota sem o
termo `7/8`, com constante `13,07873`; e `12,20373 + 7/8 = 13,07873`
exatamente. As duas leituras se confirmam mutuamente.

Tradução de notação registrada: no plano `t` de von Mangoldt, a **parte
real** corresponde à **ordenada** `Im ρ` moderna. Cuidado adicional: a
Fig. 1 da página 2 escreve o zero genérico como `β + iγ` no plano `t`,
invertendo a convenção moderna `ρ = β + iγ` do plano `s`.

## Achado 2 — o pilar espectral NÃO está sustentado como declarado

Este é o resultado central do gate, e é negativo.

Hörmander 1968 prova a assíntota **local** da função espectral na diagonal,
Teorema 5.1, equação (5.3), p. 215:

```
| e(x,x,λ) − (2π)^(−n) ∫_{p(x,ξ)<λ} dξ | ≤ C(1 + |λ|)^((n−1)/m)
```

uniformemente em compactos. **O artigo não define nem enuncia a função de
contagem global** `N_P(Λ) = #{j : λ_j ≤ Λ}`. Busca no texto integral por
"number of eigenvalues", "counting function", `N(λ)`: nenhuma ocorrência.

A passagem para a contagem global exige `N_P(Λ) = ∫_Ω e(x,x,Λ) dx`, que
requer compacidade e uniformidade — corolário padrão da literatura, mas
**não escrito neste artigo**. A constante global `C_P` também não aparece;
só a constante local `(2π)^{−n} vol(B_x)`.

Outros desencontros literais com a Classe W, todos citados na auditoria:

- **Fibrados (W2):** p. 216 — os métodos cobrem sistemas *„for which the
  eigenvalues of `p(x,ξ)` are distinct“*; para multiplicidade, *„we have no
  information beyond“* Agmon–Kannai e Hörmander [8].
- **Auto-adjunção (W5):** p. 193 — *„by a classical theorem of Friedrichs
  it has **at least one** self-adjoint extension“*. O artigo escolhe uma
  extensão; a Classe W exige essencial auto-adjunção.
- **Compacidade (W1):** `Ω` é paracompacta; compacidade é usada como
  conveniência de prova, não como hipótese.
- **Discretude (W7):** não provada nem enunciada.
- **Ordem (W3):** símbolo principal é polinômio homogêneo **real** de grau
  `m`; com elipticidade e positividade isso força `m` **par** para `d ≥ 2`.
  `OPERATOR_CLASS.md` admite `m ≥ 1` qualquer — a classe declarada é vazia
  para `m` ímpar. Defeito de formulação descoberto pela auditoria.

Resultado: **2 de 8** hipóteses diretamente sustentadas (W4, W6); as duas
decisivas (W7, W8) não.

## Achado 3 — Riemann esboçou, não provou

A tradução Wilkins, lida integralmente, traz a passagem em que Riemann dá a
expressão `(T/2π)log(T/2π) − T/2π`, esboça o argumento por contorno, conjectura
que todas as raízes são reais e então escreve:

> „Certainly one would wish for a stricter proof here; I have meanwhile
> temporarily put aside the search for this after some fleeting futile
> attempts…“

A fórmula rigorosa, com `7/8` e erro efetivo, é de von Mangoldt. Bombieri
confirma independentemente: Riemann *„states, sketching a proof“*.

## Decisão

**B — `PRIMARY_SOURCES_PARTIALLY_SUFFICIENT`.**

A fórmula dos zeros está sustentada; a Classe W exige fonte adicional. Não
forcei a opção A: a cadeia da ponte está quebrada na etapa E
(`SOURCE_BRIDGE_REQUIREMENTS.md`), e escrever a especificação da ponte
agora significaria assumir sem fonte exatamente a hipótese B do lema já
formalizado.

Conforme a seção 10 do protocolo, registro sem ampliar interpretação:
Hörmander 1968 sustenta uma lei espectral **mais geral e mais forte em
outro sentido** (cobre pseudodiferenciais, variedades paracompactas, resto
ótimo), mas é necessária referência adicional para obter
`N_P(Λ) ~ C_P Λ^{d/m}` para a Classe W declarada.

## O que não foi feito

- Nenhum teorema Lean escrito; nenhuma formalização executada.
- `ASYM-NOGO-001` **não** foi aplicado.
- Nenhum operador construído ou excluído.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- Nenhuma claim criada ou promovida.
- A Classe W **não** foi reformulada: as divergências foram registradas
  como gaps, não corrigidas — a escolha entre estreitar a classe e buscar
  fonte pertence ao próximo gate.
- As monografias candidatas de Q1 (Hörmander vols. III/IV, Shubin, Agmon,
  Safarov–Vassiliev, Ivrii) foram **listadas como hipótese bibliográfica**,
  não obtidas e não citadas como contendo o enunciado necessário.
- Nenhum arquivo fora de `04_FORMAL_RESEARCH_LAB/` modificado.

## Próxima ação única

Obter a fonte primária ou monografia necessária para fechar as hipóteses
ainda não sustentadas da Classe W, em especial a lei de Weyl global (W8) e
a discretude do espectro (W7).

## Handoff

O laboratório agora sabe exatamente onde a construção falha, e sabe por
citação de página. O pilar aritmético é sólido e efetivo. O pilar espectral
foi descoberto ser **mais fraco do que o enunciado supunha**: o artigo
canônico da lei de Weyl não contém a lei de contagem global que a Classe W
declara. Essa é a lacuna que o próximo gate deve fechar — ou, alternativa
igualmente legítima, estreitar a Classe W até o que a fonte de fato
sustenta.
