---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-PROBE-RESULT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
probe_exit: 0
probe_removed: true
---

# Resultado do probe descartável

## Execução

```text
arquivo   /tmp/FiniteStateAbstractionProbe.lean
comando   lake env lean /tmp/FiniteStateAbstractionProbe.lean
exit      0
removido  SIM
```

Nenhuma declaração do probe foi destinada a falhar. Experimentos
negativos aparecem como **teoremas de negação que compilam**, nunca
como arquivos deliberadamente inválidos.

## Declarações compiladas

```text
CertifiedFiniteAbstraction
CertifiedFiniteAbstraction.iterate_commutes
analyzeAbstractSystem
analyzeAbstractSystem_observational_sound
OrbitSeparating
orbitSeparating_iff_injOn
orbitSeparating_of_injective
analyzeAbstractSystem_reflected_sound
analyzeAbstractSystem_complete
concreteStep, abstractStep, forgetBool
boolToUnit_semiconj
boolToUnitAbstraction
unitEncoding
boolToUnit_abstract_recurrence
boolToUnit_no_concrete_recurrence
boolToUnit_not_orbitSeparating
idEnc4, tailStep, idAbstraction
```

## Pegada axiomática medida

```text
CertifiedFiniteAbstraction.iterate_commutes        [propext]
analyzeAbstractSystem                              [propext, Classical.choice, Quot.sound]
analyzeAbstractSystem_observational_sound          [propext, Classical.choice, Quot.sound]
OrbitSeparating                                    NENHUM
orbitSeparating_iff_injOn                          NENHUM
orbitSeparating_of_injective                       NENHUM
analyzeAbstractSystem_reflected_sound              [propext, Classical.choice, Quot.sound]
analyzeAbstractSystem_complete                     [propext, Classical.choice, Quot.sound]
boolToUnit_semiconj                                NENHUM
boolToUnit_not_orbitSeparating                     NENHUM
unitEncoding                                       NENHUM
```

A camada nova é majoritariamente livre de axiomas. Os três
infraestruturais entram **apenas** onde a cadeia anterior entra, por
`analyzeEncodedSystem`, e vivem em proposições apagadas na execução.

Nenhuma escolha clássica produz `abstract`, `encode`, `decode`, `Array`
ou `CycleWitness` executável.

## Verificações executáveis

```text
analyzeAbstractSystem boolToUnitAbstraction unitEncoding false = .ok ⟨0,1⟩   decide
analyzeAbstractSystem boolToUnitAbstraction unitEncoding true  = .ok ⟨0,1⟩   decide
analyzeAbstractSystem idAbstraction idEnc4 ⟨0,_⟩ = .ok ⟨2,2⟩                 decide
```

Por `decide` e `rfl`. `native_decide` **não** é usado: ele acrescentaria
um axioma de redução.

## Orientação confirmada

```lean
example {C A : Type} (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Function.Semiconj abstract stepC stepA
      ↔ ∀ c, abstract (stepC c) = stepA (abstract c) :=
  Iff.rfl
```

`Iff.rfl` — a definição desdobra exatamente na orientação congelada.

## Hipóteses negativas confirmadas por compilação

```text
Fintype C        ausente
Finite C         ausente
DecidableEq C    ausente
Nonempty C       ausente
Inhabited C      ausente
Fintype A        ausente
DecidableEq A    ausente
```

Um exemplo genérico com `C A : Type*` e nenhuma instância elabora a
cadeia inteira.

## Tokens proibidos

```text
sorry           0
admit           0
axioma local    0
unsafe          0
noncomputable   0
Classical.choose 0
Classical.decEq  0
native_decide    0
```
