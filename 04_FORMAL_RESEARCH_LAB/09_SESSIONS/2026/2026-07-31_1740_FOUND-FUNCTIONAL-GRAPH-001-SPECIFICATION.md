---
session_id: 2026-07-31_1740_FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION
started_at: 2026-07-31T17:00:00-03:00
ended_at: 2026-07-31T17:40:00-03:00
agent: claude-opus-5
git_commit_before: df6adb93a3bf8c5570954c5a94b0701896be4877
git_commit_after: null
active_work_item: FOUND-FUNCTIONAL-GRAPH-001
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED
result_status: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_READY
files_created:
  - "02_FOUNDATIONS/04_FUNCTIONAL_GRAPHS/FOUND_FUNCTIONAL_GRAPH_001/ (16 artefatos)"
  - "found-functional-graph-001-specification-result.json"
  - "09_SESSIONS/2026/2026-07-31_1740_FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION.md"
files_modified:
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
lean_files_created: 0
lean_proofs_created: 0
lake_build_executed: false
claims_promoted: 0
decision: A_FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_READY
next_single_action: "Revisar as definições de componente funcional, a unicidade por periodicOrbit e a viabilidade das assinaturas antes de autorizar formalização Lean."
---

## Preflight

`HEAD = df6adb93…`, árvore limpa. `canonical_commit` atualizado de
`3f72ad0` para `df6adb9` **antes** da especificação; `cat-file` exit 0,
`merge-base --is-ancestor` exit 0.

## A decisão central

Você a fixou no enunciado do gate, e a especificação a travou com
contraexemplo:

```text
COMPONENTE FUNCIONAL := classe de EventuallyMeets
                        ∃ m n, f^[m] x = f^[n] y
```

O contraexemplo decisivo `FFG-CE-004`:

```text
a → c
b → c
c → c
```

`MutuallyReachable` separaria isso em **três** classes — `{a}`, `{b}`,
`{c}` — quando geometricamente há **uma** estrutura: um ponto fixo com dois
ramos entrando.

## O risco que precisei checar

Uma definição de componente por "encontro eventual" corre o risco de tornar
o teorema principal **verdadeiro por definição**. Ele não fica, e escrevi
o argumento:

```text
EventuallyMeets diz que as trajetorias SE ENCONTRAM.
Nao diz que o encontro ocorre num ponto PERIODICO, nem que exista
ponto periodico algum.
```

A existência vem da **finitude**. Teste de sanidade registrado: as
definições valem para `X` infinito, e ali o teorema principal é **falso** —
`f : ℕ → ℕ`, `f n = n + 1` não tem ponto periódico. É `Fintype X` que faz o
trabalho. Virou `STOP-009`.

## Nomenclatura: um nome só

O gate ofereceu `SameFunctionalComponent` como alternativa semântica e
proibiu duas definições com a mesma semântica. Escolhi **`EventuallyMeets`**
e rejeitei o alias **inclusive na forma `abbrev`** — dois nomes públicos
para o mesmo predicado duplicam a superfície de API sem ganho. "Mesmo
componente funcional" é a *leitura*, registrada nos documentos.

## Três achados da auditoria da Mathlib

**1. `periodicOrbit` não exige `DecidableEq`.** O bloco de variáveis de
`Dynamics/PeriodicPts/Defs.lean:57` é `{α : Type*} {f : α → α} …`, sem
`DecidableEq`. Isso **refuta a previsão** que o gate de portfólio registrou
em `FFG-GAP-008` — a de que `DecidableEq X` provavelmente seria necessária
aqui, ao contrário de `FOUND-SEMIGROUP-002`. Registrei a refutação em vez
de silenciá-la: era uma previsão explícita, e ela errou.

**2. `periodicOrbit` é noncomputável** (`noncomputable section`, linhas
240–490). Consequência prática que muda o plano de contraexemplos:
`decide` **não** se aplica a igualdade de órbitas. Não bloqueia o núcleo —
nenhum teorema `CORE` decide igualdade de ciclos —, mas `FFG-CE-005` terá
de usar `periodicOrbit_apply_iterate_eq`. Virou `FFG-GAP-011`.

**3. `periodicOrbit_apply_iterate_eq` resolve `FFG-CYCLE-001` em três
passos**, sem aritmética modular:

```text
periodicOrbit f p = periodicOrbit f (f^[m] p)    (lema, .symm)
                  = periodicOrbit f (f^[n] q)    (hipotese)
                  = periodicOrbit f q            (lema)
```

Exatamente o que o gate pediu ao dizer "não usar aritmética modular se a
API de órbitas evitar isso".

## Zero `NOT_FOUND`

Diferença importante em relação a `FOUND-SEMIGROUP-002`, onde o alvo
simplesmente não existia na Mathlib: aqui **toda a maquinaria de ciclos já
existe**. O conteúdo matemático próprio desta frente é ainda **menor** que
o da anterior — o valor é de API e integração. Está registrado assim em
`KNOWN_RESULTS_MATRIX.md`.

## Uma assinatura que rejeitei

O gate ofereceu `∃ μ p : ℕ × X` para `exists_recurrent_reachable`, com a
ressalva de que era ilustrativa. Descartei: o par é artificial, obriga a
escrever `p.2` na conclusão e não acrescenta informação — `p` é determinado
por `f^[μ] x`. Adotei a alternativa limpa, que o próprio gate recomendou:

```lean
∃ mu : ℕ, mu < Fintype.card X ∧ f^[mu] x ∈ Function.periodicPts f
```

## O único ponto de atrito real

`FFG-MEET-003`, transitividade de `EventuallyMeets`. Os outros dois são
testemunhas diretas; este exige alinhar duas iteradas da trajetória
intermediária, com os dois casos `n₁ ≤ m₂` e `m₂ ≤ n₁` explícitos.
Escrevi as testemunhas de ambos em `THEOREM_CANDIDATES.md`, para que a
execução não as improvise.

## O que fica adiado

```text
ponte com SimpleGraph        FFG-GAP-012   a reciproca exige inducao sobre Walk
arvores de entrada           FFG-GAP-007
distancia minima ao ciclo    FFG-GAP-006   depende de minimalidade de mu
unicidade de mu              herdado de FSG2-GAP-004b
contagem de componentes      fora de escopo
```

Consequência vinculante enquanto a ponte não existir: "componente" nesta
frente significa **classe de `EventuallyMeets`**, e nenhum texto pode
afirmar que coincide com componente conexa de grafo.

## Homonímia registrada

Três relações com nomes parecidos convivem no laboratório:

```text
IterReachable            esta frente        iteracao de f
Reachable                FOUND-SEMIGROUP-002 acao de monoide
SimpleGraph.Reachable    Mathlib            grafo NAO dirigido
```

O nome `IterReachable` foi escolhido para não colidir, e `SimpleGraph` não
será importada no núcleo.

## O que não foi feito

```text
0 arquivos Lean
0 provas
0 lake build
0 experimentos Python
0 claims promovidas (ledger permanece em 18)
0 arquivos de legado
0 arquivos de RH-NOGO-001
0 arquivos matematicos de FOUND-SEMIGROUP-002
```

E, deliberadamente: **a formalização não foi autorizada**. A próxima etapa
é a revisão da especificação, porque a decisão de componente é a única
difícil de reverter depois de congelada em Lean.
