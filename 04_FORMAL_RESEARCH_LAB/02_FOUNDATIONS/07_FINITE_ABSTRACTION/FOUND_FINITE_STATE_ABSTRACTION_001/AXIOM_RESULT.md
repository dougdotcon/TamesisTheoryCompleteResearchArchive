---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-AXIOM-RESULT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
sorryAx: 0
local_axioms: 0
classical_choice_producing_data: 0
---

# Pegada — medida no build permanente

Saída de `#print axioms` em
`TamesisLab/Tests/FoundFiniteStateAbstraction001Axioms.lean`, colhida
durante `lake build`.

## Núcleo

```text
CertifiedFiniteAbstraction.iterate_commutes
    propext

analyzeAbstractSystem
    propext, Classical.choice, Quot.sound

analyzeAbstractSystem_complete
    propext, Classical.choice, Quot.sound

analyzeAbstractSystem_observational_sound
    propext, Classical.choice, Quot.sound

OrbitSeparating
    does not depend on any axioms

analyzeAbstractSystem_reflected_sound
    propext, Classical.choice, Quot.sound
```

## Contraexemplo — dez de dez sem pegada

```text
Counterexample.concreteStep                      nenhuma
Counterexample.abstractStep                      nenhuma
Counterexample.forgetBool                        nenhuma
Counterexample.boolToUnit_semiconj               nenhuma
Counterexample.boolToUnitAbstraction             nenhuma
Counterexample.unitEncoding                      nenhuma
Counterexample.boolToUnit_abstract_recurrence    nenhuma
Counterexample.boolToUnit_no_concrete_recurrence nenhuma
Counterexample.boolToUnit_not_orbitSeparating    nenhuma
Counterexample.naive_cycle_reflection_is_false   nenhuma
```

O contraexemplo inteiro — inclusive a refutação da reflexão ingênua — é
**livre de qualquer pegada axiomática**.

## Leitura

A camada genuinamente nova da frente é `OrbitSeparating` mais o
contraexemplo: **onze declarações, zero pegada**.

Os três infraestruturais entram exatamente onde `analyzeEncodedSystem`
entra, pelo tipo, e vivem em proposições apagadas na execução. A frente
não os introduz e não reabre a decisão de conviver com eles — política
já registrada no laboratório.

## Verificações negativas

```text
sorryAx                                0
axiomas declarados localmente          0
escolha classica produzindo dado       0
```

Prova operacional da última linha: `analyzeAbstractSystem` avalia por
`decide` em quatro testes concretos. Uma definição bloqueada por escolha
clássica não reduziria.
