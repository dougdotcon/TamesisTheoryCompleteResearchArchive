---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-PUBLIC-API-SPECIFICATION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
public_executable_core: 2
public_specification_core: 5
public_total: 7
---

# API pública candidata

## `PUBLIC_EXECUTABLE_CORE`

```text
CertifiedFiniteAbstraction
analyzeAbstractSystem
```

## `PUBLIC_SPECIFICATION_CORE`

```text
CertifiedFiniteAbstraction.iterate_commutes
analyzeAbstractSystem_observational_sound
OrbitSeparating
analyzeAbstractSystem_reflected_sound
analyzeAbstractSystem_complete
```

## Contagem derivada da lista

```text
PUBLIC_EXECUTABLE_CORE     2
PUBLIC_SPECIFICATION_CORE  5
PUBLIC_TOTAL               7
```

A contagem é **derivada** das duas listas acima, e conferida por script
contra as declarações reais no gate de formalização. Ela não é fonte
primária.

## `DEFERRED_OPTIONAL`

```text
OrbitSeparating ↔ Set.InjOn sobre a orbita
global_injective_implies_orbitSeparating
exclusao universal de erros no nivel abstrato
```

`orbitSeparating_of_injective` compila sem axiomas e ainda assim fica
fora da v1: nenhum resultado central o consome. Ele é reconstruído no
teste de instanciação, onde é efetivamente usado.

## `TEST_ONLY`

```text
BOOL_TO_UNIT             concreteStep, abstractStep, forgetBool
boolToUnitAbstraction
unitEncoding
boolToUnit_not_orbitSeparating
```

## Hipóteses do contrato público

```text
sobre C   nenhuma typeclass
sobre A   nenhuma typeclass
sobre n   nenhuma restricao
```

A finitude executável de `A` é fornecida exclusivamente por
`CertifiedFiniteEncoding A n`.

## Regra de superfície

Nenhuma declaração entra em `PUBLIC_*` por ser fácil de provar. O
critério é ser consumida pela cadeia central ou ser o contrato que o
consumidor precisa exibir.
