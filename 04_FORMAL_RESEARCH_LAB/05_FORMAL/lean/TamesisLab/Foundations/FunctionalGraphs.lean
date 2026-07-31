import TamesisLab.Foundations.FunctionalGraphs.Relations
import TamesisLab.Foundations.FunctionalGraphs.PeriodicOrbits
import TamesisLab.Foundations.FunctionalGraphs.ComponentCycle
import TamesisLab.Foundations.FunctionalGraphs.Counterexamples
import TamesisLab.Foundations.FunctionalGraphs.Audit

/-!
# FOUND-FUNCTIONAL-GRAPH-001 — agregador

Decomposição de grafos funcionais finitos: `X` finito, `f : X → X`.

```text
Relations.lean        IterReachable, MutuallyReachable, EventuallyMeets
                      sem finitude
PeriodicOrbits.lean   igualdade de orbitas periodicas
                      sem finitude
ComponentCycle.lean   existencia limitada e teorema principal
                      unico arquivo com [Fintype X]
Counterexamples.lean  FFG-CE-001..006
```

O objeto único de cada componente é a **órbita periódica**
`Function.periodicOrbit`, e não um ponto arbitrariamente escolhido.

Resultados **padrão** de dinâmica finita. Nenhuma novidade matemática.
Nenhuma ponte com `SimpleGraph`, árvores, distância mínima ou
representante canônico. Nenhuma alegação física, TRI, TDTR ou TOE.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
mathematical_novelty: NONE
-/
