# FOUND-FUNCTIONAL-GRAPH-001 — Hipóteses

## Assumidas

1. `X` é um tipo finito (`Fintype X`). A finitude é **essencial**: dela vem
   a existência do ponto periódico, via `exists_eventual_period`.
2. `f : X → X` é total e determinística. Cada estado tem **exatamente uma**
   transição seguinte — é isso que faz o grafo ser funcional.
3. Os resultados de `FOUND-SEMIGROUP-002` estão verificados e podem ser
   consumidos sem reprova.

## Deliberadamente **não** assumidas

```text
DecidableEq X    refutada como necessaria no nucleo (FFG-GAP-008)
Nonempty X       o teorema recebe x : X, que ja habita o tipo
Monoid           a frente eh puramente funcional; nenhum monoide entra
SimpleGraph      diferida (FFG-GAP-012)
Setoid           nenhuma instancia global sera criada
injetividade     f nao precisa ser injetiva — FFG-CE-004 depende disso
sobrejetividade  nao usada
```

## Negativas — cada uma com contraexemplo planejado

| Negativa | Contraexemplo |
|---|---|
| um grafo funcional pode ter mais de um ciclo | `FFG-CE-001` |
| nem todo estado é periódico | `FFG-CE-002` |
| um ciclo não precisa ser ponto fixo | `FFG-CE-003` |
| mesmo componente **não** implica alcançabilidade mútua | `FFG-CE-004` |
| um componente pode ter vários pontos periódicos | `FFG-CE-005` |
| mesmo período **não** implica mesmo componente | `FFG-CE-006` |
| `IterReachable` não é simétrica | `FFG-CE-002` |

**Nenhuma negativa é afirmada sem exemplo planejado.** Esta foi a pendência
que ficou aberta em `FOUND-SEMIGROUP-002` (`FSG2-GAP-007`) e que aqui se
procurou não repetir.

## Fronteira de validade

Os teoremas de `IterReachable`, `EventuallyMeets` e `componentSet` valem
para **qualquer** `X`, finito ou não. A finitude entra apenas em
`FFG-REC-001/002` e, por consequência, em `FFG-MAIN-001/002`.

Isso importa: mostra que o teorema principal **não é tautológico**. Para
`X` infinito — por exemplo `f : ℕ → ℕ`, `f n = n + 1` — as definições
continuam válidas e o teorema principal é **falso**, pois não há ponto
periódico algum.

## Não assumido como premissa

```text
TRI; TDTR; Tamesis; Omega; teoria de tudo; resultados Clay;
claims fisicas; documentos legados nao auditados.
```

As skills orientam o método; **não** constituem fonte matemática.
