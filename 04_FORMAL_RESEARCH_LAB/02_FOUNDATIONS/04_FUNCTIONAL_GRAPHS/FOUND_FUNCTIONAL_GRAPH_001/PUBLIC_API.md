---
document_id: FFG-PUBLIC-API
public_declarations: 16
internal_helpers: 1
---

# FOUND-FUNCTIONAL-GRAPH-001 — Superfície pública

Categorias: `PUBLIC_CORE`, `PUBLIC_COROLLARY`, `RELATION_WRAPPER`,
`INTERNAL_HELPER`, `COUNTEREXAMPLE_ONLY`, `INSTANCE_SUPPORT`, `TEST_ONLY`.

```yaml
- declaration: IterReachable
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  mathematical_role: "alcance dirigido: exists n, f^[n] x = y"
  dependencies: [Function.iterate]
  axioms: none
  recommended_for_reuse: true

- declaration: MutuallyReachable
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  mathematical_role: "alcance nas duas direcoes; identifica o CICLO, nao o componente"
  dependencies: [IterReachable]
  axioms: none
  recommended_for_reuse: true
  note: "nao aparece em nenhum enunciado do nucleo; existe para ser refutada em CE-004"

- declaration: EventuallyMeets
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  mathematical_role: "RELACAO DE COMPONENTE FUNCIONAL"
  dependencies: [Function.iterate]
  axioms: none
  recommended_for_reuse: true

- declaration: iterReachable_refl
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  mathematical_role: reflexividade
  dependencies: []
  axioms: none
  recommended_for_reuse: true

- declaration: iterReachable_trans
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  mathematical_role: "transitividade, testemunha b + a"
  dependencies: [Function.iterate_add_apply]
  axioms: "nenhum — does not depend on any axioms"
  recommended_for_reuse: true

- declaration: IterReachable.eventuallyMeets
  module: Relations
  category: PUBLIC_COROLLARY
  hypotheses: nenhuma
  mathematical_role: "alcance implica encontro, testemunhas (n, 0)"
  dependencies: [IterReachable, EventuallyMeets]
  axioms: none
  recommended_for_reuse: true

- declaration: eventuallyMeets_refl
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  axioms: none
  recommended_for_reuse: true

- declaration: eventuallyMeets_symm
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  axioms: none
  recommended_for_reuse: true

- declaration: eventuallyMeets_trans
  module: Relations
  category: PUBLIC_CORE
  hypotheses: nenhuma
  mathematical_role: "unico teorema com conteudo proprio real; dois casos"
  dependencies: [Function.iterate_add_apply, Nat.le_total]
  axioms: "[propext, Quot.sound]"
  recommended_for_reuse: true

- declaration: eventuallyMeets_isRefl
  module: Relations
  category: RELATION_WRAPPER
  mathematical_role: "Std.Refl (EventuallyMeets f) — theorem, NAO instance"
  axioms: none
  recommended_for_reuse: parcial

- declaration: eventuallyMeets_isSymm
  module: Relations
  category: RELATION_WRAPPER
  mathematical_role: "Std.Symm (EventuallyMeets f)"
  axioms: none
  recommended_for_reuse: parcial

- declaration: eventuallyMeets_isTrans
  module: Relations
  category: RELATION_WRAPPER
  mathematical_role: "IsTrans X (EventuallyMeets f)"
  axioms: "[propext, Quot.sound]"
  recommended_for_reuse: parcial

- declaration: periodicOrbit_eq_of_eventuallyMeets
  module: PeriodicOrbits
  category: PUBLIC_CORE
  hypotheses: "duas de periodicidade; NENHUMA de finitude"
  mathematical_role: "periodicos que se encontram tem a mesma orbita"
  dependencies: [Function.periodicOrbit_apply_iterate_eq]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: eventuallyMeets_of_periodicOrbit_eq
  module: PeriodicOrbits
  category: PUBLIC_COROLLARY
  hypotheses: "duas de periodicidade — INDISPENSAVEIS"
  mathematical_role: "reciproca, valida SO para pontos periodicos"
  dependencies: [Function.self_mem_periodicOrbit, Function.mem_periodicOrbit_iff]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true
  warning: >
    Dois pontos NAO periodicos tem ambos periodicOrbit = Cycle.nil. A
    igualdade das orbitas vazias NAO implica encontro. As hipoteses hp e hq
    nao podem ser removidas nem enfraquecidas.

- declaration: exists_cyclePoint_reachable_with_bound
  module: ComponentCycle
  category: PUBLIC_CORE
  hypotheses: "[Fintype X]"
  mathematical_role: "adaptador de exists_eventual_period"
  dependencies: [FiniteDynamics.exists_eventual_period, Function.mk_mem_periodicPts]
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true

- declaration: exists_component_cycle_with_entry_bound
  module: ComponentCycle
  category: PUBLIC_CORE
  hypotheses: "[Fintype X]"
  mathematical_role: "TEOREMA PRINCIPAL, por composicao"
  dependencies:
    - exists_cyclePoint_reachable_with_bound
    - IterReachable.eventuallyMeets
    - eventuallyMeets_symm
    - eventuallyMeets_trans
    - periodicOrbit_eq_of_eventuallyMeets
  axioms: "[propext, Classical.choice, Quot.sound]"
  recommended_for_reuse: true
```

**Dezesseis declarações públicas** — exatamente a lista mínima esperada.

## Auxiliar interno

```yaml
- declaration: minimalPeriod_eq_two
  module: Counterexamples
  category: INTERNAL_HELPER
  visibility: private
  scope: "namespace CE006"
  mathematical_role: "periodo minimo de um 2-ciclo eh 2"
  used_by: [CE006.a0_minimalPeriod, CE006.b0_minimalPeriod]
  recommended_for_reuse: false
```

**Confirmado `private`.** É o único auxiliar, e não vaza para a API.

## Contraexemplos e testes

```yaml
COUNTEREXAMPLE_ONLY:
  namespace: TamesisLab.Foundations.FunctionalGraphs.Counterexamples
  namespaces: [CE001, CE002, CE003, CE004, CE005, CE006]
  recommended_for_reuse: false

INSTANCE_SUPPORT:
  count: 5
  detail: "Fintype de CE001, CE002, CE003, CE004, CE006"

TEST_ONLY:
  - Tests/FoundFunctionalGraph001.lean
  - Tests/FoundFunctionalGraph001Counterexamples.lean
  - Tests/FoundFunctionalGraph001InstanceAudit.lean
```

## Separação verificada

```text
nucleo matematico   3 modulos, 0 instancias, 0 auxiliares publicos
contraexemplos      1 modulo, 5 instancias, 6 namespaces, 1 auxiliar private
auditoria           1 modulo, so #check
testes              3 arquivos, fora do namespace da frente
```
