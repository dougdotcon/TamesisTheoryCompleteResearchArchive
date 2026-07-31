---
document_id: FSG2-PUBLIC-API
work_item_id: FOUND-SEMIGROUP-002
public_declarations: 17
internal_helpers: 1
---

# FOUND-SEMIGROUP-002 — Superfície pública

Categorias: `PUBLIC_CORE`, `PUBLIC_COROLLARY`, `INTERNAL_HELPER`,
`COUNTEREXAMPLE_ONLY`, `INSTANCE_SUPPORT`, `TEST_ONLY`.

## API pública

```yaml
- declaration: Reachable
  module: Reachability
  category: PUBLIC_CORE
  mathematical_role: "definicao: existe m no monoide com m . x = y"
  dependencies: [MulAction]
  axioms: none
  recommended_for_reuse: true

- declaration: reachable_refl
  module: Reachability
  category: PUBLIC_CORE
  mathematical_role: reflexividade
  dependencies: [one_smul]
  axioms: none
  recommended_for_reuse: true

- declaration: reachable_trans
  module: Reachability
  category: PUBLIC_CORE
  mathematical_role: transitividade
  dependencies: [mul_smul]
  axioms: none
  recommended_for_reuse: true

- declaration: reachable_isRefl
  module: Reachability
  category: PUBLIC_COROLLARY
  mathematical_role: "reflexividade empacotada em Std.Refl, SEM instancia"
  dependencies: [reachable_refl]
  axioms: none
  recommended_for_reuse: true
  note: "Std.Refl e nao IsRefl: IsRefl esta depreciada na revisao fixada"

- declaration: reachable_isTrans
  module: Reachability
  category: PUBLIC_COROLLARY
  mathematical_role: "transitividade empacotada em IsTrans, SEM instancia"
  dependencies: [reachable_trans]
  axioms: none
  recommended_for_reuse: true

- declaration: reachable_iff_mem_orbit
  module: Reachability
  category: PUBLIC_CORE
  mathematical_role: "ponte definicional com MulAction.orbit"
  dependencies: [MulAction.mem_orbit_iff]
  axioms: none
  recommended_for_reuse: true
  note: "Iff.rfl; nenhuma segunda nocao de orbita foi criada"

- declaration: IsInvariant
  module: Invariants
  category: PUBLIC_CORE
  mathematical_role: "invariante sob a acao COMPLETA"
  dependencies: [MulAction]
  axioms: none
  recommended_for_reuse: true

- declaration: IsInvariantUnder
  module: Invariants
  category: PUBLIC_CORE
  mathematical_role: "invariante sob UM elemento"
  dependencies: [MulAction]
  axioms: none
  recommended_for_reuse: true

- declaration: IsInvariant.under
  module: Invariants
  category: PUBLIC_CORE
  mathematical_role: "IsInvariant implica IsInvariantUnder; IMPLICACAO, nao equivalencia"
  dependencies: [IsInvariant, IsInvariantUnder]
  axioms: none
  recommended_for_reuse: true
  note: "a reciproca NAO eh afirmada; ela vale quando a gera M"

- declaration: IsInvariant.of_reachable
  module: Invariants
  category: PUBLIC_CORE
  mathematical_role: "invariante constante ao longo da alcancabilidade"
  dependencies: [Reachable, IsInvariant]
  axioms: none
  recommended_for_reuse: true
  note: "direcao unica: refuta alcancabilidade, nunca a demonstra (CE-005)"

- declaration: IsInvariantUnder.pow
  module: Invariants
  category: PUBLIC_COROLLARY
  mathematical_role: "invariancia sob a propaga-se a a^n"
  dependencies: [pow_succ, mul_smul]
  axioms: none
  recommended_for_reuse: true

- declaration: exists_bounded_iterate_collision
  module: EventualPeriodicity
  category: PUBLIC_CORE
  mathematical_role: "casa dos pombos: colisao com limitantes de cardinalidade"
  dependencies: [Fintype.exists_ne_map_eq_of_card_lt, eventual_period_of_lt]
  axioms: [propext, Classical.choice, Quot.sound]
  recommended_for_reuse: true
  note: "UNICO ponto de uso do pigeonhole em toda a frente"

- declaration: periodic_tail_of_collision
  module: EventualPeriodicity
  category: PUBLIC_CORE
  mathematical_role: "o ponto f^[mu] x eh periodico de periodo lam"
  dependencies: [Function.iterate_add_apply]
  axioms: none
  recommended_for_reuse: true
  note: "argumento eh f^[mu] x, NAO x"

- declaration: collision_propagates
  module: EventualPeriodicity
  category: PUBLIC_CORE
  mathematical_role: "propagacao a todos os indices posteriores"
  dependencies: [Function.iterate_add_apply]
  axioms: [propext, Quot.sound]
  recommended_for_reuse: true

- declaration: exists_eventual_period
  module: EventualPeriodicity
  category: PUBLIC_CORE
  mathematical_role: "TEOREMA PRINCIPAL: composicao dos tres anteriores"
  dependencies:
    - exists_bounded_iterate_collision
    - periodic_tail_of_collision
    - collision_propagates
  axioms: [propext, Classical.choice, Quot.sound]
  recommended_for_reuse: true

- declaration: monoid_element_eventually_periodic
  module: MonoidIteration
  category: PUBLIC_COROLLARY
  mathematical_role: "iteracao de um elemento de monoide sobre tipo finito"
  dependencies: [exists_bounded_iterate_collision, smul_iterate_apply]
  axioms: [propext, Classical.choice, Quot.sound]
  recommended_for_reuse: true

- declaration: monoid_element_eventual_period_propagates
  module: MonoidIteration
  category: PUBLIC_COROLLARY
  mathematical_role: "versao com propagacao"
  dependencies: [exists_bounded_iterate_collision, collision_propagates, smul_iterate_apply]
  axioms: [propext, Classical.choice, Quot.sound]
  recommended_for_reuse: true
```

**Total público: 17 declarações** — exatamente a lista mínima esperada
pelo gate, nem mais nem menos.

## Auxiliares internos

```yaml
- declaration: eventual_period_of_lt
  module: EventualPeriodicity
  category: INTERNAL_HELPER
  visibility: private
  mathematical_role: >
    normaliza um par de indices ja ordenado (i < j <= card X) no par
    (mu, lam) = (i, j - i), com os tres limitantes por omega.
  used_by: exists_bounded_iterate_collision
  used_twice: true
  note: >
    Existe precisamente para que os ramos i < j e j < i nao dupliquem
    argumento. Eh `private`: NAO faz parte da superficie publica.
  recommended_for_reuse: false
```

**Um único auxiliar, e ele é `private`.** Não há auxiliar público
acidental.

## Contraexemplos

```yaml
category: COUNTEREXAMPLE_ONLY
namespace: TamesisLab.Foundations.FiniteDynamics.Counterexamples
declarations:
  CE001: [St, Tr, act, comp, comp_assoc, idT_comp, comp_idT, act_comp,
          act_one, reachable_zero_one, not_reachable_one_zero,
          reachable_not_symmetric]
  CE002: [St, Tr, act, comp, comp_assoc, idT_comp, comp_idT, act_comp,
          act_a, not_reachable_a_b, not_transitive]
  CE003: [St, f, not_fixed, iterate_one, iterate_two, eventually_fixed,
          iterate_ge_two, s0_not_periodic, periodic_point_is_tail]
  CE004: [St, act, act_comp, not_faithful]
  CE005: [I, I_isInvariant, invariant_does_not_separate_orbits]
recommended_for_reuse: false
note: >
  Existem para refutar generalizacoes. Reutiliza-los como "modelos" seria
  o erro que eles proprios impedem.
```

## Testes

```yaml
category: TEST_ONLY
files:
  - Tests/FoundSemigroup002.lean
  - Tests/FoundSemigroup002Counterexamples.lean
  - Tests/FoundSemigroup002InstanceAudit.lean
recommended_for_reuse: false
```

## Separação verificada

```text
nucleo matematico            4 modulos, 0 instancias, 1 auxiliar private
contraexemplos               1 modulo, 11 instancias, 5 namespaces
auditoria                    1 modulo, so #check
testes                       3 arquivos, fora do namespace da frente
```

A superfície pública está **separada** dos auxiliares e dos
contraexemplos: os primeiros são `private`, os segundos vivem sob
`Counterexamples.CExxx`.
