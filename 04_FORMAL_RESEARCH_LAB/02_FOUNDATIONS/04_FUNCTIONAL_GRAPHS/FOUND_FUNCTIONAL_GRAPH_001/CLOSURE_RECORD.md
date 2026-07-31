---
document_id: FFG-CLOSURE-RECORD
work_item_id: FOUND-FUNCTIONAL-GRAPH-001
closed_at: 2026-07-31
reviewed_commit: 3f6d7e785ba8bd90a35f33f7dc889f1234a7b650
decision: A_RESULT_REVIEW_APPROVED
extension_status: NOT_AUTHORIZED
---

# FOUND-FUNCTIONAL-GRAPH-001 — Registro de encerramento

## Estado final

```yaml
active_work_item: FOUND-FUNCTIONAL-GRAPH-001
work_status: VERIFIED
specification_status: APPROVED
formalization_status: VERIFIED
result_review: APPROVED
extension_status: NOT_AUTHORIZED
current_blocker: null
authorized_action: PORTFOLIO_REVIEW_REQUIRED
```

`PORTFOLIO_REVIEW_REQUIRED` é **trava de governança**, não ação
autorizada. Nenhum gate pode agir sob ela.

## O que fica como fundação reutilizável

```text
05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/
  Relations.lean         sem finitude
  PeriodicOrbits.lean    sem finitude
  ComponentCycle.lean    [Fintype X]
  Counterexamples.lean   CE-001..006
  Audit.lean             #check

Tests/FoundFunctionalGraph001.lean
Tests/FoundFunctionalGraph001Counterexamples.lean
Tests/FoundFunctionalGraph001InstanceAudit.lean
```

**16 declarações públicas**, 1 auxiliar `private`, 5 instâncias — todas em
contraexemplos, **zero no núcleo**.

## Força exata do resultado — vinculante

```text
Para cada estado inicial x, existe uma entrada limitada em uma orbita
periodica.

Todos os pontos periodicos do componente de x, definido por
EventuallyMeets, pertencem a MESMA orbita periodica.
```

**Não** registrado como provado:

```text
cada componente foi construido como conjunto ou quociente;
existe um representante canonico;
existe um menor mu;
a bacia foi enumerada;
o grafo subjacente foi construido;
o componente eh conexo em SimpleGraph;
ha decomposicao explicita em arvores;
todo ciclo da funcao eh unico globalmente.
```

## A ressalva que precisa sobreviver

```text
O resultado inverso EXIGE que ambos os pontos sejam periodicos.

Dois pontos NAO periodicos tem, ambos, periodicOrbit = Cycle.nil. As
orbitas vazias sao iguais sem que as trajetorias se encontrem.
```

As hipóteses `p ∈ periodicPts f` e `q ∈ periodicPts f` permanecem
**visíveis** na assinatura e documentadas em `PUBLIC_API.md`,
`RESULT_REVIEW.md` e `RESULT_BOUNDARY.md`.

## Limite computacional

```text
periodicOrbit eh noncomputavel. O resultado nao fornece algoritmo
executavel de enumeracao de componentes, calculo de mu ou deteccao de
ciclo.
```

## Propriedades verificadas na revisão

```text
Fintype X apenas na camada de existencia;
DecidableEq X ausente de todos os teoremas;
Nonempty, Inhabited, Finite ausentes;
zero instancias no nucleo; zero conflitos; umbrella nao ambiguo;
zero Setoid, zero SimpleGraph, zero Quotient;
pigeonhole nao reaplicado;
decide nunca usado sobre igualdade de periodicOrbit;
zero native_decide;
∃! ausente de todos os enunciados.
```

## Gaps que permanecem abertos

```text
FFG-GAP-006  distancia minima      OPEN_DEFERRED
FFG-GAP-007  arvores de entrada    OPEN_DEFERRED
FFG-GAP-012  ponte SimpleGraph     OPEN_DEFERRED
FFG-GAP-014  bibliografia          OPEN_BIBLIOGRAPHIC
```

Encerrar a frente **não fecha** nenhum deles.

## O que não está autorizado

```text
FOUND_FUNCTIONAL_GRAPH_001_GRAPH_BRIDGE_AUTHORIZED
FOUND_FUNCTIONAL_GRAPH_001_TREE_DECOMPOSITION_AUTHORIZED
FOUND_FUNCTIONAL_GRAPH_001_DISTANCE_AUTHORIZED
FOUND_FUNCTIONAL_GRAPH_002
```

Nenhuma foi adicionada ao allowlist.

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Situação do laboratório

```text
FOUND-FUNCTIONAL-GRAPH-001   VERIFIED / APPROVED    encerrado
FOUND-SEMIGROUP-002          VERIFIED / APPROVED    encerrado
RH-NOGO-001                  FROZEN_PARTIAL_RESULT  congelado
```

Nenhuma frente ativa. O próximo passo legítimo é um gate explícito de
revisão de portfólio.
