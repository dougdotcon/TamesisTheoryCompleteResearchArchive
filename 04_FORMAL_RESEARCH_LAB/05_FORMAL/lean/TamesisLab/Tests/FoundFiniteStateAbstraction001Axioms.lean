import TamesisLab.Foundations.FiniteStateAbstraction

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — auditoria da pegada

Somente `#print axioms`. Nenhum experimento destinado a falhar vive
neste arquivo: seu contrato é terminar com código de saída zero.

Resultado esperado, e verificado:

```text
iterate_commutes              propext
OrbitSeparating               nenhum
contraexemplo inteiro         nenhum
analyzeAbstractSystem e cadeia
                              propext, Classical.choice, Quot.sound
```

A pegada de três entra **exatamente** onde `analyzeEncodedSystem` entra,
pelo tipo, e vive em proposições apagadas na execução. Nenhuma escolha
clássica produz `abstract`, `encode`, `decode`, o `Array` ou o
certificado executável.

A camada verdadeiramente nova — `OrbitSeparating` e todo o
contraexemplo — é livre de qualquer pegada.
-/

namespace TamesisLab.Tests.FoundFiniteStateAbstraction001Axioms

open TamesisLab.Foundations.FiniteStateAbstraction

#print axioms CertifiedFiniteAbstraction.iterate_commutes
#print axioms analyzeAbstractSystem
#print axioms analyzeAbstractSystem_complete
#print axioms analyzeAbstractSystem_observational_sound
#print axioms OrbitSeparating
#print axioms analyzeAbstractSystem_reflected_sound

#print axioms Counterexample.concreteStep
#print axioms Counterexample.abstractStep
#print axioms Counterexample.forgetBool
#print axioms Counterexample.boolToUnit_semiconj
#print axioms Counterexample.boolToUnitAbstraction
#print axioms Counterexample.unitEncoding
#print axioms Counterexample.boolToUnit_abstract_recurrence
#print axioms Counterexample.boolToUnit_no_concrete_recurrence
#print axioms Counterexample.boolToUnit_not_orbitSeparating
#print axioms Counterexample.naive_cycle_reflection_is_false

end TamesisLab.Tests.FoundFiniteStateAbstraction001Axioms
