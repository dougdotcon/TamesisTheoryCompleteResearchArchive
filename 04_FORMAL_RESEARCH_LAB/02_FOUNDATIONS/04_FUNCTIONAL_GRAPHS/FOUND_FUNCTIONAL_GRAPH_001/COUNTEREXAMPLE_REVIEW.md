---
document_id: FFG-COUNTEREXAMPLE-REVIEW
counterexamples: 6
distinct_targets: true
---

# FOUND-FUNCTIONAL-GRAPH-001 — Revisão dos contraexemplos

## CE-001 — dois ciclos globais `CONFIRMADO`

```text
a → a,  b → b
```

`a_periodic`, `b_periodic`, `not_meets`. Dois pontos fixos, ambos
periódicos, que **não** se encontram eventualmente. Refuta a existência de
um ciclo global único.

## CE-002 — cauda antes do ciclo `CONFIRMADO`

```text
a → b → c → c
```

`a_not_periodic` (forma **forte**: para período positivo algum),
`c_periodic`, `reach_a_c`, `meets_a_c`. O teorema principal foi
instanciado neste modelo no teste isolado.

## CE-003 — ciclo de comprimento dois `CONFIRMADO`

```text
a ↔ b
```

`a_periodic`, `b_periodic`, `a_ne_b`, `not_fixed`, `orbit_eq`. Nenhum dos
estados é fixo; ambos periódicos; **mesma** `periodicOrbit`, provada por
`periodicOrbit_apply_iterate_eq` e **não** por `decide`.

## CE-004 — mesmo componente sem alcance mútuo `CONFIRMADO`

```text
a → c ← b,  c → c
```

```text
meets_a_b              EventuallyMeets f a b      ⟨1, 1, rfl⟩
not_reach_a_b          ¬ IterReachable f a b
not_reach_b_a          ¬ IterReachable f b a
not_mutually_reachable ¬ MutuallyReachable f a b
```

**Contraexemplo decisivo** para a noção de componente. É ele que sustenta
a rejeição de `MutuallyReachable`.

## CE-005 — vários pontos cíclicos, uma órbita `CONFIRMADO`

Reutiliza o modelo de `CE-003`. Dois pontos periódicos **distintos** com
uma **única** `periodicOrbit`. Refuta "um único ponto periódico por
componente".

## CE-006 — mesmo período, componentes distintos `CONFIRMADO`

```text
a0 ↔ a1,  b0 ↔ b1
```

`a0_minimalPeriod = 2`, `b0_minimalPeriod = 2`,
`¬ EventuallyMeets f a0 b0`. Refuta "igualdade de período implica mesmo
componente".

## Alvos distintos

| ID | Alvo |
|---|---|
| `CE-001` | dois ciclos globais distintos |
| `CE-002` | cauda antes do ciclo |
| `CE-003` | ciclo de comprimento maior que um |
| `CE-004` | `EventuallyMeets` sem `MutuallyReachable` |
| `CE-005` | vários pontos cíclicos na mesma `periodicOrbit` |
| `CE-006` | mesmo comprimento de período em componentes diferentes |

Seis alvos, seis afirmações refutadas **distintas**.

## Independência — registro obrigatório

```text
NAO foi provado que todas essas falhas ocorrem numa UNICA funcao.
NAO foi provado que toda funcao finita exibe essas falhas.
```

`CE-003` e `CE-005` usam o mesmo sistema com perguntas diferentes, e isso
está declarado.

## Lacuna registrada, não fechada

Nenhum dos seis modelos exibe **dois pontos não periódicos com órbitas
(vazias) iguais que não se encontram** — em `CE-002` e `CE-004` os pontos
transitórios **se encontram**. Construí-lo exigiria um sétimo modelo, isto
é, matemática nova, proibida neste gate.

A observação estrutural está registrada em `RESULT_REVIEW.md` e
`RESULT_BOUNDARY.md`; **não** é apresentada como fato formalizado.

## Método

`decide` usado apenas sobre tabelas finitas e desigualdade de estados.
**Nunca** sobre igualdade de `periodicOrbit`, que é noncomputável. Zero
`native_decide`.
