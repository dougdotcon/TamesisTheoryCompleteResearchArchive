import TamesisLab.Foundations.BisimulationBoundary

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — auditoria da pegada

Somente `#print axioms`. Nenhum experimento destinado a falhar vive
neste arquivo.

Resultado esperado, e verificado: **nenhuma** declaração da frente
depende de axioma.

Diferente da frente anterior, nada aqui atravessa `analyzeEncodedSystem`
— não há `Array`, não há tabela, não há execução. Por isso `propext`,
`Classical.choice` e `Quot.sound` não entram em lugar nenhum.
-/

namespace TamesisLab.Tests.FoundBisimulationBoundary001Axioms

open TamesisLab.Foundations.BisimulationBoundary

#print axioms Simulates
#print axioms Reflects
#print axioms Bisimulation

#print axioms simulates_iff_semiconj
#print axioms reflects_iff_simulates
#print axioms bisimulation_iff_semiconj

#print axioms boolToUnit_bisimulation
#print axioms forgetBool_surjective
#print axioms bisimulation_does_not_reflect_cycles
#print axioms surjective_bisimulation_does_not_reflect_cycles

end TamesisLab.Tests.FoundBisimulationBoundary001Axioms
