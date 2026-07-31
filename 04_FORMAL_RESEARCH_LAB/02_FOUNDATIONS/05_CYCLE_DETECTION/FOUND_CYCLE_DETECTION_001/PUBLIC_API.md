---
document_id: FCD-PUBLIC-API
declarations: 13
---

# API pública

Treze declarações, classificadas.

## `PUBLIC_EXECUTABLE_CORE`

```yaml
- declaration: CycleWitness
  module: Witness.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  mathematical_role: "certificado; par de naturais, independente do tipo de estados"
  dependencies: []
  axioms: nenhum
  recommended_for_reuse: true

- declaration: cycleCandidates
  module: Candidates.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: []
  computable: true
  mathematical_role: "dominio finito de busca; nao menciona X"
  dependencies: [List.range, List.flatMap, List.map]
  axioms: "does not depend on any axioms"
  recommended_for_reuse: true

- declaration: detectCycleWitness?
  module: Detector.lean
  category: PUBLIC_EXECUTABLE_CORE
  hypotheses: ["Fintype X", "DecidableEq X"]
  computable: true
  mathematical_role: "busca limitada por certificado; devolve Option"
  dependencies: [cycleCandidates, CycleWitness.Valid, CycleWitness.decidableValid, List.find?]
  axioms: "[propext, Classical.choice, Quot.sound] por Fintype.card"
  recommended_for_reuse: true
```

## `PUBLIC_SPECIFICATION_CORE`

```yaml
- declaration: CycleWitness.Valid
  module: Witness.lean
  category: PUBLIC_SPECIFICATION_CORE
  hypotheses: ["Fintype X"]
  computable: "proposicional, decidivel com DecidableEq X"
  mathematical_role: "contrato do certificado; coincide com exists_bounded_iterate_collision"
  dependencies: [Fintype.card, Nat.iterate]
  axioms: herdados
  recommended_for_reuse: true

- declaration: mem_cycleCandidates_iff
  module: Candidates.lean
  category: PUBLIC_SPECIFICATION_CORE
  hypotheses: []
  computable: n/a
  mathematical_role: "correcao e completude da enumeracao"
  dependencies: [List.mem_flatMap, List.mem_map, List.mem_range]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: detectCycleWitness?_sound
  module: Correctness.lean
  category: PUBLIC_SPECIFICATION_CORE
  hypotheses: ["Fintype X", "DecidableEq X"]
  computable: n/a
  mathematical_role: "o certificado devolvido satisfaz o contrato"
  dependencies: [List.find?_some, of_decide_eq_true]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: detectCycleWitness?_complete
  module: Correctness.lean
  category: PUBLIC_SPECIFICATION_CORE
  hypotheses: ["Fintype X", "DecidableEq X"]
  computable: n/a
  mathematical_role: "algum certificado eh sempre devolvido"
  dependencies: [exists_bounded_iterate_collision, mem_cycleCandidates_iff, List.find?_isSome, Option.isSome_iff_exists]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true
```

## `PUBLIC_COROLLARY`

```yaml
- declaration: CycleWitness.isPeriodicPt
  module: Periodicity.lean
  category: PUBLIC_COROLLARY
  hypotheses: ["Fintype X"]
  computable: n/a
  mathematical_role: "o ponto-base eh periodico com o periodo testemunhado"
  dependencies: [periodic_tail_of_collision]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: CycleWitness.mem_periodicPts
  module: Periodicity.lean
  category: PUBLIC_COROLLARY
  hypotheses: ["Fintype X"]
  computable: n/a
  mathematical_role: "ponte com a interface proposicional da Mathlib"
  dependencies: [CycleWitness.isPeriodicPt, Function.mk_mem_periodicPts]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: CycleWitness.propagates
  module: Periodicity.lean
  category: PUBLIC_COROLLARY
  hypotheses: ["Fintype X"]
  computable: n/a
  mathematical_role: "a repeticao vale para toda a cauda posterior"
  dependencies: [collision_propagates]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: cycleCandidates_zero
  module: Candidates.lean
  category: PUBLIC_COROLLARY
  hypotheses: []
  computable: n/a
  mathematical_role: "caso de fronteira inferior; @[simp]"
  dependencies: []
  axioms: nenhum
  recommended_for_reuse: "marginal — sem uso interno atual"

- declaration: cycleCandidates_one
  module: Candidates.lean
  category: PUBLIC_COROLLARY
  hypotheses: []
  computable: n/a
  mathematical_role: "menor caso nao trivial; @[simp]"
  dependencies: []
  axioms: nenhum
  recommended_for_reuse: "marginal — sem uso interno atual"
```

Os dois corolários de fronteira **não** são usados por prova alguma do
núcleo. Foram mantidos como `PUBLIC_COROLLARY` por serem lemas de
normalização `@[simp]` e âncoras de regressão baratas, ambos provados por
`rfl`. A alternativa — rebaixá-los a `TEST_ONLY` — foi considerada e
recusada: como `@[simp]`, eles pertencem ao ambiente de simplificação e
não a um arquivo de teste.

## `INSTANCE_SUPPORT`

```yaml
- declaration: CycleWitness.decidableValid
  module: Witness.lean
  category: INSTANCE_SUPPORT
  hypotheses: ["Fintype X", "DecidableEq X"]
  computable: true
  mathematical_role: "torna Valid decidivel; sem ela o detector nao elabora"
  dependencies: [instDecidableAnd, Nat.decLt, DecidableEq X]
  axioms: herdados
  recommended_for_reuse: "sim, implicitamente — eh encontrada por sintese"
```

## `INTERNAL_HELPER` e `TEST_ONLY`

```text
INTERNAL_HELPER   nenhum
TEST_ONLY         os modelos f1, fId, fNot, f3 e f4, definidos dentro do
                  arquivo de execucao e nao exportados pelo umbrella
```

## Ausências confirmadas

```text
detectCycleWitness (total)          NAO existe
Option.getD ou fallback             NAO existe
Floyd, Brent, tabela visitada       NAO existem
qualquer teorema de minimalidade    NAO existe
Function.periodicOrbit              NAO aparece no nucleo
```
