# FOUND-FUNCTIONAL-GRAPH-001 — DAG da prova futura

```text
FOUND-SEMIGROUP-002.exists_eventual_period          [VERIFIED]
                    |
                    | Function.mk_mem_periodicPts
                    v
        FFG-REC-002  ponto periodico alcancavel, com mu < card X
                    |
                    +----------------------------+
                    |                            |
                    v                            v
        FFG-REC-001  versao sem limite      FFG-MAIN-002
                    |
                    v
              FFG-MAIN-001
                    ^
                    |
        +-----------+-----------+
        |                       |
  FFG-CYCLE-001           FFG-MEET-002/003/004
  (periodicOrbit)         (equivalencia)
        |                       |
        |                  FFG-MEET-001
        v
  Function.periodicOrbit_apply_iterate_eq   [Mathlib]


IterReachable                    EventuallyMeets
  FFG-REACH-001 refl               FFG-MEET-001 refl
  FFG-REACH-002 trans              FFG-MEET-002 symm
        |                          FFG-MEET-003 trans
        +--- FFG-MEET-004 --------->      |
                                          v
                                    componentSet
                                    FFG-COMP-001/002
```

## Regras estruturais

```text
O pigeonhole eh consumido UMA vez, em FOUND-SEMIGROUP-002, e NAO eh
reaplicado aqui.

FFG-MAIN-001 eh COMPOSICAO: FFG-REC-001 + FFG-MEET-002/003/004 +
FFG-CYCLE-001. Nenhuma inducao nova.

FFG-CYCLE-001 usa exclusivamente periodicOrbit_apply_iterate_eq. Nenhuma
aritmetica modular.

O unico teorema com conteudo proprio real eh FFG-MEET-003
(transitividade), que exige alinhar iteradas em dois casos.
```

## Dependências externas

```yaml
MATHEMATICAL:
  - exists_eventual_period            FOUND-SEMIGROUP-002, VERIFIED
  - Function.iterate_add_apply        Mathlib, localizado
  - princípio da casa dos pombos      já consumido, não reaplicado

LEAN_API:
  - Function.periodicPts              API_FOUND
  - Function.mk_mem_periodicPts       API_FOUND
  - Function.periodicOrbit            API_FOUND
  - Function.periodicOrbit_apply_iterate_eq  API_FOUND
  - Function.mem_periodicOrbit_iff    API_FOUND
  - Function.self_mem_periodicOrbit   API_FOUND

GOVERNANCE:
  - FOUND-SEMIGROUP-002 VERIFIED      pre-condicao do labctl
  - extension_status NOT_AUTHORIZED   preservado

DEFERRED:
  - SimpleGraph.ConnectedComponent    FFG-GAP-012
  - distancia minima, arvores          FFG-GAP-006/007
```

```yaml
blocking_dependencies: 0
```
