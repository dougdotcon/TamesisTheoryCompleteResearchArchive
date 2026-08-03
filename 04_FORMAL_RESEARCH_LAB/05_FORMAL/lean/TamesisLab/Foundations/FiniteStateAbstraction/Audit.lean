import TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — auditoria de assinaturas

Somente `#check`. Nenhuma definição, nenhum teorema.

O que esta auditoria torna visível:

```text
CertifiedFiniteAbstraction   dois campos, nenhuma typeclass
analyzeAbstractSystem        encoding como argumento SEPARADO
iterate_commutes             sem finitude, sem encoding
observational_sound          conclui sob abstract, em A
OrbitSeparating              Prop, sem typeclass
reflected_sound              OrbitSeparating explicita, conclui em C
complete                     existencial, sem OrbitSeparating
```

A diferença entre a quarta e a sexta linha é o resultado da frente.
-/

namespace TamesisLab.Foundations.FiniteStateAbstraction

#check @CertifiedFiniteAbstraction
#check @CertifiedFiniteAbstraction.abstract
#check @CertifiedFiniteAbstraction.commutes
#check @CertifiedFiniteAbstraction.iterate_commutes

#check @analyzeAbstractSystem
#check @analyzeAbstractSystem_complete
#check @analyzeAbstractSystem_observational_sound

#check @OrbitSeparating
#check @analyzeAbstractSystem_reflected_sound

#check @Counterexample.boolToUnit_semiconj
#check @Counterexample.boolToUnit_not_orbitSeparating
#check @Counterexample.naive_cycle_reflection_is_false

end TamesisLab.Foundations.FiniteStateAbstraction
