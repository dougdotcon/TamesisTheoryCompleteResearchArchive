# FOUND-FUNCTIONAL-GRAPH-001 — Resultado-alvo

## Alvo escolhido

```text
CORE_UNIQUE_CYCLE_WITH_ENTRY_BOUND
```

## Enunciado

> Toda trajetória de uma função sobre um tipo finito alcança um ponto
> periódico. Todos os pontos periódicos no mesmo componente funcional
> determinam a mesma órbita periódica.

Assinatura principal (`FFG-MAIN-001`):

```lean
theorem functional_component_has_unique_cycle {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ p : X,
      IterReachable f x p ∧
      p ∈ Function.periodicPts f ∧
      ∀ q : X,
        q ∈ Function.periodicPts f →
        EventuallyMeets f x q →
        Function.periodicOrbit f q = Function.periodicOrbit f p
```

Versão com limite de entrada (`FFG-MAIN-002`) troca `p` por `f^[mu] x`,
com `mu < Fintype.card X`.

---

## O significado exato de "um ciclo por componente" — vinculante

```text
SIGNIFICA:

todos os pontos periodicos do componente produzem a MESMA
Function.periodicOrbit.
```

```text
NAO SIGNIFICA:

existe exatamente um ponto periodico por componente.
```

Falso para ciclos de comprimento maior que um — `FFG-CE-005` exibe dois
pontos periódicos distintos com a mesma órbita.

```text
NAO SIGNIFICA:

existe um representante periodico canonicamente escolhido.
```

O `p` do teorema é **um** representante, produzido pela existência. Não é
único e não é canônico.

```text
NAO SIGNIFICA:

todo componente termina em ponto fixo.
```

Falso — `FFG-CE-003` exibe um ciclo de comprimento 2.

**O objeto único é `Function.periodicOrbit f p`, não o representante.**

---

## O que o alvo **não** inclui

```yaml
weak_graph_component_bridge: DEFERRED
unique_directed_cycle_in_simple_graph_component: NOT_AUTHORIZED
incoming_tree_decomposition: NOT_AUTHORIZED
canonical_tail_cycle_decomposition: NOT_AUTHORIZED
minimal_entry_time: NOT_AUTHORIZED
```

Não serão formalizados neste ciclo:

```text
SimpleGraph e ConnectedComponent;
quociente por componentes;
arvores enraizadas;
distancia minima ao ciclo;
unicidade de mu;
minimalidade do periodo;
contagem de componentes.
```

## Por que o limite de período não aparece na conclusão

`exists_eventual_period` fornece também `0 < lam` e `mu + lam ≤ card X`,
mas expor `lam` apenas para carregar o limite seria dado de saída ocioso —
mesma política que removeu `0 < c` em `COUNTING-LAW-BRIDGE`. Se um gate
futuro precisar, o limite volta com justificativa.

## Critério de sucesso da formalização futura

```text
os onze teoremas CORE compilam;
zero sorry / admit / axiom / unsafe;
#print axioms limitado a propext, Classical.choice, Quot.sound;
os seis contraexemplos verificados;
nenhuma instancia global de Setoid ou de equivalencia;
SimpleGraph ausente do nucleo;
o pigeonhole NAO eh reaplicado;
nenhuma claim cientifica promovida.
```

## O que este resultado **não** é

```text
nao eh descoberta matematica;
nao eh nova teoria de dinamica;
nao eh teoria do tempo;
nao eh resultado fisico;
nao valida TRI nem TDTR;
nao toca problema Clay.
```

Decomposição de grafo funcional em ciclos e trajetórias de entrada é a
"forma rho" da iteração finita — material padrão. Ver
`NOVELTY_BOUNDARY.md`.
