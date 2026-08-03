---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-PUBLIC-API
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
public_executable_core: 2
public_specification_core: 5
public_total: 7
typeclasses_required: 0
---

# API pública — final

Congelada pela revisão. Divergir exige gate próprio.

## `PUBLIC_EXECUTABLE_CORE` — 2

```lean
structure CertifiedFiniteAbstraction (C A : Type*) (stepC : C → C) (stepA : A → A)

def analyzeAbstractSystem
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C) :
    Except RuntimeCycleError CycleWitness
```

## `PUBLIC_SPECIFICATION_CORE` — 5

```lean
theorem CertifiedFiniteAbstraction.iterate_commutes
theorem analyzeAbstractSystem_observational_sound
def     OrbitSeparating
theorem analyzeAbstractSystem_reflected_sound
theorem analyzeAbstractSystem_complete
```

## Contagem derivada

```text
PUBLIC_EXECUTABLE_CORE     2
PUBLIC_SPECIFICATION_CORE  5
PUBLIC_TOTAL               7
```

Derivada das duas listas. Será conferida por script contra as
declarações reais no gate de formalização; se divergir, **a contagem é
corrigida, não o código**.

## `DEFERRED_OPTIONAL`

```text
orbitSeparating_iff_injOn
orbitSeparating_of_injective
exclusao universal de erros no nivel abstrato
```

Todas compilam. Nenhuma é publicada: nenhum resultado central as
consome.

`orbitSeparating_of_injective` é reconstruído no arquivo de testes, onde
é efetivamente usado para instanciar a reflexão.

## `TEST_ONLY`

```text
concreteStep, abstractStep, forgetBool
boolToUnitAbstraction, unitEncoding
boolToUnit_semiconj
boolToUnit_abstract_recurrence
boolToUnit_no_concrete_recurrence
boolToUnit_not_orbitSeparating
naive_cycle_reflection_is_false
idEnc4, tailStep, idAbstraction
```

## Contrato de hipóteses

```text
typeclasses exigidas do consumidor    0
finitude de C                         nao exigida
finitude de A                         via CertifiedFiniteEncoding A n, apenas
DecidableEq                           nao exigida em lugar nenhum
```

## O que o consumidor precisa fornecer

```text
stepC : C → C
stepA : A → A
abstract : C → A          com prova de Semiconj
encoding : CertifiedFiniteEncoding A n
start : C
```

E, **somente** se quiser a conclusão concreta:

```text
OrbitSeparating abstract stepC start
```
