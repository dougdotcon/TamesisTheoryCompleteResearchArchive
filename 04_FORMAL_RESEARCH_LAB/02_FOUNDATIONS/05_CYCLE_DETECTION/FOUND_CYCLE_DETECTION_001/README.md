---
document_id: FCD-README
work_item_id: FOUND-CYCLE-DETECTION-001
specification_status: READY_FOR_REVIEW
primary_algorithm: BOUNDED_CERTIFICATE_SEARCH
lean_files_created: 0
---

# FOUND-CYCLE-DETECTION-001 — especificação

*Executable Cycle Detection for Finite Deterministic Systems.*

> **Especificação apenas.** Nenhum módulo Lean permanente foi criado.
> Nenhum algoritmo foi implementado. Nenhum `lake build` foi executado.

## O que esta frente entrega

Um detector **executável dentro do Lean** que, dados um tipo finito `X`,
uma função `f : X → X` e um estado inicial `x₀`, devolve um certificado

```text
μ : indice-base de uma colisao certificada
λ : periodo positivo testemunhado
```

satisfazendo

```text
μ < card X
0 < λ
μ + λ ≤ card X
f^[μ + λ] x₀ = f^[μ] x₀
```

## O que ela **não** entrega

```text
mu minimo
lambda minimo
complexidade assintotica otima
memoria constante
equivalencia operacional com Floyd
enumeracao da bacia
enumeracao dos componentes
lista ordenada do ciclo
representante canonico do ciclo
```

## Algoritmo

```yaml
primary_algorithm: BOUNDED_CERTIFICATE_SEARCH
future_optimization: FLOYD
reference_alternative: VISITED_TABLE
deferred_algorithm: BRENT
```

A primeira versão **não** é Floyd. Ver `ALGORITHM_SELECTION.md`.

## Ordem de leitura

```text
TARGET_RESULT.md          o que se quer
ALGORITHM_SELECTION.md    por que busca certificada, nao Floyd
DATA_MODEL.md             CycleWitness e Valid
CANDIDATE_ENUMERATION.md  cycleCandidates
EXECUTABLE_CONTRACT.md    predicado executavel e detector parcial
CORRECTNESS_PLAN.md       soundness
COMPLETENESS_PLAN.md      completeness por reutilizacao da colisao
TERMINATION_PLAN.md       terminacao estrutural
COMPUTABILITY_BOUNDARY.md o que nao pode ser computavel
LEAN_API_AUDIT.md         APIs auditadas no checkout fixado
EXTRACTION_FEASIBILITY.md #eval, lean --run, alvo executavel
TEST_PLAN.md              sete casos de regressao
ALGORITHM_COMPARISON.md   Floyd, tabela visitada, Brent
THEOREM_CANDIDATES.md     CORE, OPTIONAL_CORE, DEFERRED
THEOREM_DEPENDENCY_MAP.md o DAG
GAP_REGISTER.yaml         dezenove lacunas
STOP_CONDITIONS.md        dezesseis condicoes de parada
NOVELTY_BOUNDARY.md       novidade zero
SPECIFICATION_DECISION.md a decisao
```

## Limites

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```
