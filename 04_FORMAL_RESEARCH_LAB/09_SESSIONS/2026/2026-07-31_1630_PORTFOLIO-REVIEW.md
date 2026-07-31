---
session_id: 2026-07-31_1630_PORTFOLIO-REVIEW
started_at: 2026-07-31T16:00:00-03:00
ended_at: 2026-07-31T16:30:00-03:00
agent: claude-opus-5
git_commit_before: 3f72ad0cf19e523f5b714d2d078cd71f3e44c46f
git_commit_after: null
active_work_item: FOUND-FUNCTIONAL-GRAPH-001
authorized_action: PORTFOLIO_REVIEW_AUTHORIZED
result_status: PORTFOLIO_REVIEW_APPROVED_FUNCTIONAL_GRAPH_SELECTED
files_created:
  - "01_PORTFOLIO/PORTFOLIO_REVIEW_2026_07_31.md"
  - "01_PORTFOLIO/NEXT_WORK_ITEM_DECISION.md"
  - "portfolio-review-result.json"
  - "09_SESSIONS/2026/2026-07-31_1630_PORTFOLIO-REVIEW.md"
files_modified:
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "01_PORTFOLIO/GLOBAL_DEPENDENCY_GRAPH.md"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/STATUS.yaml"
  - "02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/CLOSURE_RECORD.md"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
lean_files_created: 0
lean_proofs_created: 0
lake_build_executed: false
claims_promoted: 0
decision: A_PORTFOLIO_REVIEW_APPROVED_FUNCTIONAL_GRAPH_SELECTED
next_single_action: "Preparar a especificação formal da decomposição de grafos funcionais finitos, sem executar provas."
---

## Preflight

`HEAD = 3f72ad0…`, árvore limpa, histórico conforme esperado.
`canonical_commit` atualizado de `b4ce2551` para `3f72ad0` **antes** da
revisão; `cat-file` exit 0, `merge-base --is-ancestor` exit 0.

## A transição da trava

`NO_ACTION_AUTHORIZED` estava em **oito** lugares. Separei-os em dois
grupos, e a distinção importa:

**Renomeados** — governança viva, onde o nome tem efeito:

```text
10_TOOLS/labctl.py                       allowlist literal
LAB_STATE.md                             authorized_action + proibicoes + corpo
01_PORTFOLIO/RESEARCH_QUEUE.yaml         authorized_next_gate
FOUND_SEMIGROUP_002/STATUS.yaml          next_gate
FOUND_SEMIGROUP_002/CLOSURE_RECORD.md    normativo
```

**Preservados** — registros históricos:

```text
found-semigroup-002-result-review.json
09_SESSIONS/2026/*
CHANGELOG.md
```

Esses documentam **o que aquele gate decidiu, com o nome que a trava tinha
então**. Reescrevê-los falsificaria o histórico — o mesmo princípio que nos
levou a não fazer squash de `9510be2` com `3f72ad0`. Uma busca futura por
`NO_ACTION_AUTHORIZED` ainda encontrará essas três ocorrências, e isso é
correto.

A renomeação foi feita **atomicamente**, num único script, antes de
qualquer chamada a `labctl validate` — se allowlist e `LAB_STATE`
divergissem por um instante, a validação falharia.

## Auditoria da fila

Reavaliei os seis itens `SCOPED`. Nenhum satisfaz simultaneamente
infraestrutura Mathlib pronta, acesso alto a contraexemplos e PoC em 30
dias — os três critérios que fizeram `FOUND-SEMIGROUP-002` funcionar.

O caso menos óbvio foi `PVSNP-PHYS-001`: é o único com custo de
formalização apenas médio e acesso alto a contraexemplos. Descartei por
duas razões, e vale dizê-las: definir `P_phys`/`NP_phys` exige escolher um
modelo de computação física, e **essa escolha é ela própria a parte
contenciosa** — não é trabalho de formalização, é trabalho de posição. E
abrir frente vizinha a uma conjectura Clay logo depois de congelar outra
seria repetir o erro que a revisão de `RH-NOGO-001` diagnosticou.

`TOE-INTERFACE-001` está **bloqueado**, não apenas caro: depende
formalmente de `RH-NOGO-001`, que está congelado.

## Alvo selecionado

`FOUND-FUNCTIONAL-GRAPH-001` — decomposição de grafos funcionais finitos.
Busca por duplicata em todos os `.yaml` e `.md`: **zero ocorrências**.

O que muda em relação a `FOUND-SEMIGROUP-002` é a **escala da pergunta**:
lá se perguntava sobre uma trajetória; aqui, sobre a estrutura global do
grafo de `f`. O resultado estrutural candidato — cada componente contém um
ciclo, alcançado em tempo finito — é **consequência direta** de
`exists_eventual_period`, já verificado.

## Uma distinção que precisa ficar registrada

`FOUND-FUNCTIONAL-GRAPH-001` **não é extensão** de `FOUND-SEMIGROUP-002`.
O `extension_status` daquela frente permanece `NOT_AUTHORIZED`, e continua
assim. A relação é de **reutilização de API verificada** — é um work item
próprio, com identificador, gaps e ciclo completo de gates próprios.

A `REUSE_MATRIX.md` da frente anterior já apontava que seis domínios
estavam em `REQUIRES_ADAPTER` porque faltava estrutura sobre o grafo da
função. Esta frente é exatamente esse adaptador, formalizado como
matemática padrão em vez de integração ad hoc.

## O resultado forte não foi autorizado

> Cada componente conexa possui **exatamente um** ciclo, com árvores
> entrando nele.

É verdadeiro para grafos funcionais, mas depende de qual noção de
"componente" se adote — componente fracamente conexa, classe de
alcançabilidade mútua, ou bacia de um ciclo. As três dão enunciados
diferentes, e **uma delas torna a afirmação trivial por definição**.
Registrei em `FFG-GAP-002` e `FFG-GAP-004`, com
`strong_result_status: NOT_AUTHORIZED_BEFORE_SPECIFICATION`.

## Uma previsão que pode se inverter

Em `FOUND-SEMIGROUP-002`, `DecidableEq X` provou-se hipótese ociosa. Aqui
provavelmente **não** será: definir "o menor `μ`" ou decidir pertencimento
a um ciclo tende a exigi-la. Registrei em `FFG-GAP-008` para que a
especificação **verifique** em vez de presumir — em qualquer direção.

## Alteração de governança necessária

O `labctl` exige que `active_work_item` pertença a um conjunto literal.
Sem acrescentar `FOUND-FUNCTIONAL-GRAPH-001` a esse conjunto, o estado
final que o próprio gate mandou produzir reprovaria na validação.
Acrescentei o literal, com a pré-condição `FOUND-SEMIGROUP-002 VERIFIED` —
mesmo padrão usado nas três transições anteriores.

## O que não foi feito

```text
0 arquivos Lean
0 provas
0 lake build
0 claims promovidas
0 arquivos de legado
0 arquivos de RH-NOGO-001
0 arquivos matematicos de FOUND-SEMIGROUP-002
0 pastas de especificacao da nova frente
```

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

A decomposição "rho shape" de iteração finita é material padrão. O valor é
formal e de reutilização.
