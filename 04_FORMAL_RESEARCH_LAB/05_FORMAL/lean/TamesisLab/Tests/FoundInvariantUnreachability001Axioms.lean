import TamesisLab.Tests.FoundInvariantUnreachability001

/-!
# Pegada de FOUND-INVARIANT-UNREACHABILITY-001

A frente não atravessa `analyzeEncodedSystem`: não há `Array`, não há
tabela, não há execução. Por isso `Classical.choice` **não** aparece em
nenhuma das dez declarações.
-/

namespace TamesisLab.Tests.FoundInvariantUnreachability001Axioms

open TamesisLab.Foundations.Invariants

#print axioms Invariant.semiconj
#print axioms Invariant.iterate
#print axioms unreachable_of_invariant_ne
#print axioms Invariant.pair
#print axioms invariantAbstraction
#print axioms invariant_orbitSeparating_iff_fixedPoint
#print axioms diagStep_invariant
#print axioms TamesisLab.Tests.FoundInvariantUnreachability001.diag_unreachable
#print axioms TamesisLab.Tests.FoundInvariantUnreachability001.constant_invariant_proves_nothing

end TamesisLab.Tests.FoundInvariantUnreachability001Axioms
