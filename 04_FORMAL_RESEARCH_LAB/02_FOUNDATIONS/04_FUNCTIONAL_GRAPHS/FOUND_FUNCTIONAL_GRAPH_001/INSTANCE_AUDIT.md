---
document_id: FFG-INSTANCE-AUDIT
total_instances: 5
instances_in_core: 0
conflicts_found: 0
audit_test: "05_FORMAL/lean/TamesisLab/Tests/FoundFunctionalGraph001InstanceAudit.lean"
---

# FOUND-FUNCTIONAL-GRAPH-001 — Auditoria de instâncias

## Achado principal

```text
Relations.lean        0 instancias
PeriodicOrbits.lean   0 instancias
ComponentCycle.lean   0 instancias
Audit.lean            0 instancias
Counterexamples.lean  5 instancias
```

**O núcleo matemático não declara instância alguma.**

## As cinco instâncias

```yaml
- instance: "instance : Fintype St"
  type: Fintype CE001.St
  module: Counterexamples
  namespace: "...FunctionalGraphs.Counterexamples.CE001"
  scope: local ao modelo
  purpose: "decidir negativas sobre dois pontos fixos"
  exported_by_umbrella: true
  possible_conflict: false
  acceptable: true

- instance: "instance : Fintype St"
  type: Fintype CE002.St
  namespace: "...Counterexamples.CE002"
  purpose: "instanciar o teorema principal no modelo com cauda"
  possible_conflict: false
  acceptable: true

- instance: "instance : Fintype St"
  type: Fintype CE003.St
  namespace: "...Counterexamples.CE003"
  purpose: "modelo de 2-ciclo"
  possible_conflict: false
  acceptable: true

- instance: "instance : Fintype St"
  type: Fintype CE004.St
  namespace: "...Counterexamples.CE004"
  purpose: "modelo decisivo a -> c <- b"
  possible_conflict: false
  acceptable: true

- instance: "instance : Fintype St"
  type: Fintype CE006.St
  namespace: "...Counterexamples.CE006"
  purpose: "dois 2-ciclos disjuntos"
  possible_conflict: false
  acceptable: true
```

`CE005` **não declara instância**: reutiliza o modelo de `CE003`.

Cada `St` é um tipo indutivo próprio do seu namespace; **nenhum par
`(classe, tipo)` recebe duas instâncias**. Não há reutilização cruzada
como a de `CE004`/`CE001.Tr` em `FOUND-SEMIGROUP-002`.

## Exigências do gate

| Exigência | Estado |
|---|---|
| zero instâncias no núcleo | **sim** |
| todas em namespaces de contraexemplo | **sim**, cinco namespaces |
| nenhuma instância global de `Setoid` | **sim** — `Setoid` aparece 1 vez, em docstring |
| nenhuma instância de `SimpleGraph` | **sim** — 0 imports |
| nenhuma instância concorrente | **sim** — verificado par a par |
| umbrella não produz ambiguidade | **sim** — teste exit 0 |

## Teste de auditoria criado

`TamesisLab/Tests/FoundFunctionalGraph001InstanceAudit.lean`, exit **0**.
**Não altera módulo matemático algum.** Verifica:

1. as cinco instâncias por `#synth`;
2. que cada `f` age sobre o seu tipo, por `rfl`;
3. cardinalidades distintas (2, 3, 4) sem interferência;
4. que, com o agregador importado, `IterReachable`, `EventuallyMeets`,
   `exists_cyclePoint_reachable_with_bound` e
   `exists_component_cycle_with_entry_bound` continuam se aplicando a
   `Bool` — a verificação decisiva de que **a poluição não existe**;
5. que os três wrappers relacionais typecheck sem instância;
6. que `eventuallyMeets_of_periodicOrbit_eq` exige as duas hipóteses de
   periodicidade, e que um ponto não periódico tem órbita `Cycle.nil`;
7. as 16 assinaturas públicas.

## Conflitos

```text
0
```

**Nenhuma instância foi criada nem corrigida nesta revisão.**
