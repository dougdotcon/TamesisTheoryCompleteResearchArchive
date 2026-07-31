---
document_id: FFG-REVIEW-DECISION
status: FROZEN
decision: A_FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED
---

# FOUND-FUNCTIONAL-GRAPH-001 — Decisão da revisão

```text
A. FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED
```

## Teoremas autorizáveis na formalização

### `CORE` — definições

```text
IterReachable
MutuallyReachable
EventuallyMeets
```

### `CORE` — teoremas

```text
iterReachable_refl
iterReachable_trans
IterReachable.eventuallyMeets

eventuallyMeets_refl
eventuallyMeets_symm
eventuallyMeets_trans

periodicOrbit_eq_of_eventuallyMeets
exists_cyclePoint_reachable_with_bound
exists_component_cycle_with_entry_bound
```

Nove teoremas, três definições.

### `OPTIONAL_COROLLARY`

```text
eventuallyMeets_of_periodicOrbit_eq
mutuallyReachable_of_periodicOrbit_eq
```

Autorizáveis **somente** se a prova for composição curta. Nenhum dos dois é
dependência do teorema principal.

### `COUNTEREXAMPLE`

```text
FFG-CE-001 a FFG-CE-006
```

### `DEFERRED`

```text
componentSet            nao usado pela API publica
Setoid                  nenhuma instancia
SimpleGraph             ponte diferida
componentes quociente
arvores de entrada
distancia minima
tempo minimo de entrada
representante canonico
classificacao completa
```

## DAG congelado

```text
FOUND-SEMIGROUP-002.exists_eventual_period
                    ↓
exists_cyclePoint_reachable_with_bound
                    ↓
IterReachable / EventuallyMeets
                    ↓
periodicOrbit_eq_of_eventuallyMeets
                    ↓
exists_component_cycle_with_entry_bound
```

O teorema principal é **composição**. A casa dos pombos permanece
exclusivamente na fundação anterior.

## Hipóteses congeladas

```text
relacoes                          nenhuma hipotese de finitude
igualdade de periodicOrbit        nenhuma hipotese de finitude
adaptador de existencia           [Fintype X]
teorema principal                 [Fintype X]
```

Proibidas sem necessidade verificada: `DecidableEq X`, `Finite X`,
`Nonempty X`, `Inhabited X`.

## O que a formalização **não** pode fazer

```text
usar ∃! p : X no teorema principal;
publicar IsRecurrent;
publicar SameFunctionalComponent;
publicar componentSet sem uso;
criar Setoid ou instancia de equivalencia;
importar SimpleGraph no nucleo;
formalizar arvores, distancia minima ou decomposicao canonica;
usar decide sobre igualdade de periodicOrbit;
reaplicar o principio da casa dos pombos;
afirmar novidade matematica.
```

## Estado autorizado

```yaml
work_status: READY
specification_status: APPROVED
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_AUTHORIZED
```

Não autorizados, e nenhum foi acrescentado ao allowlist:

```text
FOUND_FUNCTIONAL_GRAPH_001_GRAPH_BRIDGE_AUTHORIZED
FOUND_FUNCTIONAL_GRAPH_001_TREE_DECOMPOSITION_AUTHORIZED
FOUND_FUNCTIONAL_GRAPH_001_DISTANCE_AUTHORIZED
FOUND_FUNCTIONAL_GRAPH_002
```

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

Ledger de claims permanece com **18** entradas. Nenhuma claim criada.
