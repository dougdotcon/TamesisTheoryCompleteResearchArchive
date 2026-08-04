import TamesisLab.Foundations.BisimulationBoundary.CycleReflection

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — auditoria de assinaturas

Somente `#check`. Nenhuma definição, nenhum teorema.

O que esta auditoria torna visível:

```text
Reflects        conserva a existencial do zag
Simulates       nenhuma typeclass
Bisimulation    conjuncao, nao coinducao
as tres equivalencias
as duas negacoes
```
-/

namespace TamesisLab.Foundations.BisimulationBoundary

#check @Simulates
#check @Reflects
#check @Bisimulation

#check @simulates_iff_semiconj
#check @reflects_iff_simulates
#check @bisimulation_iff_semiconj

#check @bisimulation_does_not_reflect_cycles
#check @surjective_bisimulation_does_not_reflect_cycles

#check @boolToUnit_bisimulation
#check @forgetBool_surjective

end TamesisLab.Foundations.BisimulationBoundary
