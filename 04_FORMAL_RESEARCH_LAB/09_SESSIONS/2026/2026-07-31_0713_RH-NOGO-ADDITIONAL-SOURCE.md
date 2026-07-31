---
session_id: 2026-07-31_0713_RH-NOGO-ADDITIONAL-SOURCE
started_at: 2026-07-31T06:55:00-03:00
ended_at: 2026-07-31T07:13:16-03:00
agent: claude-opus-5
git_commit_before: 16427b420aa6e5e89c39d169172ff1c2c3add142
git_commit_after: null
active_work_item: RH-NOGO-001
authorized_action: RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED
result_status: RH_NOGO_LOCAL_TO_GLOBAL_BRIDGE_SUFFICIENT
files_created:
  - "08_REVIEWS/SOURCES/RH_NOGO/W_POWER_CLASS.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/W_ELLIPTIC_CLASS.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/GLOBAL_WEYL_THEOREM_CANDIDATES.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/GLOBAL_WEYL_CONSTANT.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/CLASS_W_V2_DECISION.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/SELF_ADJOINT_REALIZATION_DECISION.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/ORDER_PARITY_AUDIT.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/ADDITIONAL_SOURCE_AUDIT.md"
  - "08_REVIEWS/SOURCES/RH_NOGO/pdf/ivrii_2016_100years_weyl.pdf"
  - "08_REVIEWS/SOURCES/RH_NOGO/pdf/coriasco_doll_2020_weyl_ae.pdf"
  - "rh-nogo-additional-source-result.json"
  - "09_SESSIONS/2026/2026-07-31_0713_RH-NOGO-ADDITIONAL-SOURCE.md"
files_modified:
  - "08_REVIEWS/SOURCES/RH_NOGO/SOURCE_MANIFEST.yaml"
  - "03_MILLENNIUM/01_RIEMANN/STATUS.yaml"
  - "03_MILLENNIUM/01_RIEMANN/GAP_REGISTER.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
tests_executed:
  - "pytest: 2 passed"
  - "labctl validate: PASS, errors []"
claims_changed: []
gaps_closed:
  - "GAP-RH-010 (auto-adjunção) — CLOSED_BY_REFORMULATION"
  - "GAP-RH-011 (paridade da ordem) — CLOSED_BY_REFORMULATION"
gaps_opened:
  - "GAP-RH-013 (atribuição bibliográfica) — RESOLVED_BY_CITATION_RULE"
  - "GAP-RH-014 (positividade de C_P)"
gaps_updated:
  - "GAP-RH-012 → PARTIALLY_SUPPORTED"
next_single_action: "Especificar a ponte formal entre W-ELLIPTIC, W-POWER e ASYM-NOGO-001 sem iniciar a prova completa do no-go espectral."
---

## Objetivo autorizado

Obter uma fonte que enuncie diretamente a lei global de Weyl para uma
classe precisa, ou demonstrar documentalmente quais resultados adicionais
transformam a assíntota local de Hörmander em lei global. Sem iniciar
prova, sem aplicar `ASYM-NOGO-001`, sem formalizar EDP em Lean.

## Fontes

Obtidas por **acesso público** (arXiv): Ivrii 2016, *100 years of Weyl's
law* (90 pp.); Coriasco–Doll 2020, *Weyl Law on Asymptotically Euclidean
Manifolds* (26 pp.). Ambas com `sha256` no manifesto.

`RETRIEVAL_FAILED`: Safarov–Vassiliev, Shubin e a monografia de Ivrii — são
monografias comerciais e **nenhuma tentativa foi feita de obter cópias por
meios que violem direitos de acesso**. As provas da lei global permanecem
em textos não lidos; o que este laboratório possui são **enunciados** em
fontes revisadas por pares.

## Achado 1 — a lei global existe, com hipóteses precisas

Coriasco–Doll, Introdução, p. 1:

> "Hörmander [15] proved, for a positive elliptic self-adjoint classical
> pseudodifferential operator of order `m > 0` on a compact manifold, the
> Weyl law `N(λ) = γ·λ^{d/m} + O(λ^{(d−1)/m})`, `λ → +∞`."

com `N(λ) = #{j : λ_j < λ}` (eq. 1). **Essa é a formulação de
`W-ELLIPTIC` v2** — copiada da fonte, não construída aqui.

Ivrii, Example 3.1.1, dá a versão com constante explícita:
`(3.1.1) N(0,λ) = κ₀λ^{d/m} + O(λ^{(d−1)/m})` e
`(3.1.3) κ₀ = (2π)^{−d}∬ n(x,ξ)dxdξ`, onde `n(x,ξ)` é o número de
autovalores do símbolo principal `A⁰(x,ξ)` em `(0,1)` — **a forma correta
para sistemas**, não um volume escalar.

## Achado 2 — a atribuição corrente é imprecisa

A referência `[15]` de Coriasco–Doll é, literalmente, *L. Hörmander, The
spectral function of an elliptic operator, Acta Math. 121 (1968), 193–218*
— exatamente o artigo que a auditoria anterior mostrou **não conter**
`N(λ)`.

A atribuição é matematicamente defensável (a lei global segue por
integração da local sobre variedade compacta) e bibliograficamente
imprecisa (o passo não está escrito no artigo). Registrei a regra de
citação: **Hörmander pelo local; a lei global por Coriasco–Doll/Ivrii ou
pela ponte explícita.** Não reclassifiquei Hörmander 1968.

## Achado 3 — a ponte fecha, e Ivrii escreve a identidade que faltava

Ivrii, eq. (3.1.11): `N⁻(λ) = ∫ e(x,x,λ) dx`. Era exatamente a etapa
ausente. Com ela, as sete etapas ficam:

| Etapa | Estado | Fonte |
|---|---|---|
| A projetor `E_Λ` | `DIRECTLY_PROVED` | Hörmander p. 193 |
| B kernel `e(x,y,Λ)` | `DIRECTLY_PROVED` | Hörmander p. 193 |
| C `N = Tr E_Λ` | `CITED_STANDARD_RESULT` | Coriasco–Doll §3 |
| D `Tr E_Λ = ∫ e(x,x,Λ)` | `CITED_STANDARD_RESULT` | Ivrii (3.1.11) |
| E assíntota local uniforme | `DIRECTLY_PROVED` | Hörmander (5.3) |
| F integração do termo principal | `ELEMENTARY_COROLLARY` | homogeneidade |
| G integração uniforme do erro | `ELEMENTARY_COROLLARY` | compacidade |

Observação decisiva: a estimativa (5.3) é uniforme *em subconjuntos
compactos*; se `M` é compacta, isso **é** uniformidade global. A etapa G
sai de graça — mas só sob compacidade.

Dos cinco pontos que o gate proibiu chamar de triviais, quatro têm estado
declarado e um permanece **`UNRESOLVED`**: o tratamento de fibrados e
sistemas na etapa D, já que (3.1.11) é escalar.

## Achado 4 — o requisito é menor do que parecia

Ivrii, Example 3.1.1(iv): *"without any non-degeneracy assumption we arrive
to one-term asymptotics with the remainder estimate `O(λ^{(d−1+δ)/m})`"*.

Para `W-POWER` basta a assintótica de **um termo**. Logo as condições de
micro-hiperbolicidade e não periodicidade — exigidas para o resto agudo e
o segundo termo — **não são necessárias** para a inclusão.

## Decisões

- **Classe:** `REFORMULATE_AS_CLASSICAL_PSEUDODIFFERENTIAL`. As outras
  quatro opções foram avaliadas e rejeitadas com motivo escrito.
- **Ordem:** `PSEUDODIFFERENTIAL_POSITIVE_ORDER`. `m > 0` real elimina o
  defeito de paridade sem hipótese nova; o caso diferencial de ordem par
  fica contido.
- **Auto-adjunção:** `positive_self_adjoint_operator`. A hipótese mínima é
  uma **realização** auto-adjunta positiva, não essencial auto-adjunção —
  literalmente o que Coriasco–Doll assumem e o que Hörmander constrói
  (extensão de Friedrichs escolhida). O no-go, quando enunciado, deve
  quantificar sobre realizações, o que é mais forte e melhor sustentado.

`GAP-RH-010` e `GAP-RH-011` fechados **por reformulação**, não por prova:
a Classe W v1 não foi corrigida, foi substituída. `OPERATOR_CLASS.md` não
foi editado e permanece como registro histórico do que a auditoria refutou.

## O que não será afirmado

```text
A existência de uma lei global de Weyl para W-ELLIPTIC não
exclui Hilbert–Pólya em geral.

O resultado não cobre operadores fora da classe.

O resultado não cobre espectros de absorção, ressonâncias,
geometrias não compactas ou não comutativas.

A lei global não foi demonstrada apenas porque a assíntota
local se parece com sua densidade.

Nenhuma afirmação foi feita sobre a verdade ou falsidade da
Hipótese de Riemann.
```

## O que não foi feito

- Nenhum teorema Lean criado; `ASYM-NOGO-001` **não** aplicado.
- A inclusão `W-ELLIPTIC ⊆ W-POWER` foi **especificada**, não formalizada
  nem provada.
- Nenhum operador construído ou excluído.
- Nenhuma claim criada ou promovida.
- Nenhuma monografia citada como fonte de enunciado.
- Nenhum arquivo fora de `04_FORMAL_RESEARCH_LAB/` modificado.

## Handoff

A interface está limpa: `operador geométrico ⟹ lei de potência ⟹ lema
assintótico`. O núcleo formal (`ASYM-NOGO-001`) está isolado de qualquer
lacuna de EDP pela classe abstrata `W-POWER`, de modo que futuros
estreitamentos de `W-ELLIPTIC` não o invalidam. Restam quatro pendências
documentadas — fibrados, discretude, positividade de `C_P` e bordo — todas
localizadas e nenhuma bloqueante para a especificação da ponte.
