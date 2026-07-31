---
session_id: 2026-07-31_1850_FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION-REVIEW
started_at: 2026-07-31T18:10:00-03:00
ended_at: 2026-07-31T18:50:00-03:00
agent: claude-opus-5
git_commit_before: 90fb4e26da33cebed2ba414ee5aeb663647de149
git_commit_after: null
active_work_item: FOUND-FUNCTIONAL-GRAPH-001
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_AUTHORIZED
result_status: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED
files_created:
  - ".../FOUND_FUNCTIONAL_GRAPH_001/SPECIFICATION_REVIEW.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/FINAL_DEFINITIONS.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/FINAL_SIGNATURES.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/API_NAMING_DECISION.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/REVIEW_DECISION.md"
  - "found-functional-graph-001-specification-review-result.json"
  - "09_SESSIONS/2026/2026-07-31_1850_FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION-REVIEW.md"
files_modified:
  - ".../FOUND_FUNCTIONAL_GRAPH_001/DEFINITIONS.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/KNOWN_RESULTS_MATRIX.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/NOVELTY_BOUNDARY.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/THEOREM_CANDIDATES.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/COUNTEREXAMPLE_PLAN.md"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/GAP_REGISTER.yaml"
  - ".../FOUND_FUNCTIONAL_GRAPH_001/STATUS.yaml"
  - "01_PORTFOLIO/RESEARCH_QUEUE.yaml"
  - "10_TOOLS/labctl.py"
  - "LAB_STATE.md"
  - "CHANGELOG.md"
repository_lean_files_created: 0
lean_proofs_created: 0
lake_build_executed: false
claims_promoted: 0
decision: A_FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED
next_single_action: "Formalizar o núcleo aprovado de alcance por iteração, encontro eventual, existência limitada de ponto cíclico e unicidade da órbita periódica do componente funcional."
---

## Preflight

`HEAD = 90fb4e26…`, árvore limpa. `canonical_commit` atualizado de
`df6adb9` para `90fb4e2` **antes** da revisão; `cat-file` exit 0,
`merge-base --is-ancestor` exit 0.

## As duas correções que você pediu

### `MutuallyReachable`

A redação anterior — *"identifica o ciclo, não o componente"* — era
imprecisa como afirmação sobre todo o domínio. Corrigida para a formulação
por classes, com o argumento de isolamento escrito:

```text
Se x ≠ y, x alcanca y e y alcanca x, entao f^[n2 + n1] x = x com
n2 + n1 > 0, logo x eh periodico. Contrapositivo: transitorio ⟹ classe
unitaria.
```

Acrescentei um refinamento que o enunciado do gate não continha: **"classe
não trivial" só vale para ciclos de comprimento maior que um**. Um ponto
fixo é periódico e sua classe também é unitária. Logo "classe unitária"
**não** distingue transitório de ponto fixo — o que distingue é a
pertinência a `Function.periodicPts f`. Sem esse reparo, a formulação
corrigida ainda estaria sutilmente errada.

### `IsRecurrent`

Retirado. Você tem razão: "recorrência" carrega, em dinâmica, significados
que este núcleo não prova — Poincaré, retorno a vizinhança, cadeias de
Markov.

Adotei a **Estratégia A com a cláusula condicional resolvida
negativamente**: os teoremas públicos usam `x ∈ Function.periodicPts f`
diretamente, e `IsCyclePoint`/`IsTransientPoint` **não** são criados,
porque a lista `CORE` congelada não os usa — mesmo princípio que já adia
`componentSet`.

Registro que, nessa resolução, a Estratégia A **coincide** com a B. Prefiro
dizer isso a fingir que escolhi uma terceira via.

## A correção que a auditoria revelou

Você pediu para auditar a orientação real de `iterate_add_apply`. O probe
devolveu:

```lean
Function.iterate_add_apply (f : α → α) (m n : ℕ) (x : α) :
  f^[m + n] x = f^[m] (f^[n] x)
```

A contagem **externa** é `m` e fica à **esquerda** da soma. Consequência
sobre as testemunhas da transitividade:

| Caso | Especificação | **Forma natural** |
|---|---|---|
| `ny ≤ my` | `x: mx + d` | **`x: d + mx`** |
| `my ≤ ny` | `z: nz + d` | **`z: d + nz`** |

Mesmo valor, forma sintática diferente — `mx + d` exigiria `Nat.add_comm`
para casar com `rw`. Congelei as formas naturais em `FINAL_SIGNATURES.md`,
com o mapa completo `mx/ny/my/nz`. Vale também para `iterReachable_trans`,
cuja testemunha natural é `b + a`.

Virou `FFG-GAP-015`.

## Uma simplificação do teorema principal

`FFG-MAIN-001` e `FFG-MAIN-002` **colapsaram num só**:

```text
antes:  functional_component_has_unique_cycle   (∃ p : X, ...)
      + functional_component_..._with_bound     (∃ mu : ℕ, ...)

agora:  exists_component_cycle_with_entry_bound (∃ mu : ℕ, ...)
```

O `p` existencial era **sempre** `f^[mu] x`, logo redundante. A forma com
`∃ mu` elimina a duplicação e põe o limite de entrada no enunciado
principal. `FFG-REC-001` (versão sem limite) também caiu, pela mesma razão.

A orientação da conclusão continua obedecendo à regra congelada: o primeiro
argumento de `EventuallyMeets` na aplicação de `FFG-CYCLE-001` é
`f^[mu] x`, e é ele que fica à esquerda.

## Probe descartável

`/tmp/FFGSpecificationReviewProbe.lean`, apenas `import` e `#check`, exit
**0**, **removido**. Zero ocorrências de `theorem`, `example`, `axiom`,
`sorry`, `admit`. **Nenhum arquivo `.lean` criado no repositório. Nenhum
`lake build`.**

Confirmou os três pontos centrais: `periodicPts` exige período positivo
(`IsPeriodicPt f 0 x` é sempre verdadeiro); `periodicOrbit : Cycle X` sem
`DecidableEq` e noncomputável; `periodicOrbit_apply_iterate_eq` com
`f^[n] x` à esquerda, o que faz a rota usar `.symm` no primeiro passo.

## Núcleo congelado

Três definições e **nove** teoremas. Dois corolários opcionais, ambos
condicionados a prova curta e nenhum sendo dependência do principal.

Hipóteses: **nenhuma finitude** nas relações e na igualdade de órbitas;
`[Fintype X]` apenas na existência e no principal. `DecidableEq X`
**ausente**.

## O que fica bloqueado

```text
componentSet   DEFERRED_API_ALIAS — sem uso na API publica
Setoid, SimpleGraph, arvores, distancia minima, representante canonico,
classificacao completa.
```

A ponte com `SimpleGraph` fica registrada como **conjectura futura**, não
como claim.

## O que não foi feito

```text
0 arquivos Lean no repositorio
0 provas
0 lake build
0 experimentos Python
0 claims promovidas (ledger em 18)
0 arquivos de legado
0 arquivos de RH-NOGO-001
0 arquivos matematicos de FOUND-SEMIGROUP-002
```

## Nota sobre os documentos anteriores

Não apaguei o histórico. `DEFINITIONS.md` e `THEOREM_CANDIDATES.md` foram
marcados como **históricos**, com as decisões superadas preservadas e a
correção anexada. Os documentos vigentes são `FINAL_DEFINITIONS.md` e
`FINAL_SIGNATURES.md`.
