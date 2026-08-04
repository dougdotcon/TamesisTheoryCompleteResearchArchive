import TamesisLab.Tests.FoundMonovariantDescent001

/-!
# Pegada de FOUND-MONOVARIANT-DESCENT-001

`Classical.choice` entra apenas no que atravessa `analyzeEncodedSystem`.
A parte puramente de descida não o carrega.
-/

namespace TamesisLab.Tests.FoundMonovariantDescent001Axioms

open TamesisLab.Foundations.Monovariants

#print axioms Monovariant.iterate_lt
#print axioms Monovariant.no_periodic_point
#print axioms Monovariant.not_reachable_self
#print axioms analyzeTransitionTable_period_pos
#print axioms analyzeAbstractSystem_period_pos
#print axioms monovariant_not_orbitSeparating
#print axioms TamesisLab.Tests.FoundMonovariantDescent001.strictDown_not_monovariant

end TamesisLab.Tests.FoundMonovariantDescent001Axioms
