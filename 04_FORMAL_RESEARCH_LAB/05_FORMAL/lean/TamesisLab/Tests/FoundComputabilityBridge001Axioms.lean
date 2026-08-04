import TamesisLab.Tests.FoundComputabilityBridge001

/-!
# Pegada de FOUND-COMPUTABILITY-BRIDGE-001

Cobertura **integral**: as 19 públicas, as 2 `TEST_ONLY` e os 7 testes.
O auxiliar privado não é alcançável daqui, e é medido no probe.

As quatro equivalências e as duas codificações são **livres de axioma**.
O que traz pegada é sempre a travessia para `Primcodable`/`Primrec`.
-/

namespace TamesisLab.Tests.FoundComputabilityBridge001Axioms

open TamesisLab.Foundations.ComputabilityBridge

#print axioms encodingEquiv
#print axioms encodingPrimcodable
#print axioms finite_of_encoding
#print axioms isEmpty_of_encoding_zero
#print axioms cycleWitnessEquiv
#print axioms instPrimcodableCycleWitness
#print axioms runtimeCycleErrorEquiv
#print axioms instPrimcodableRuntimeCycleError
#print axioms exceptEquiv
#print axioms instPrimcodableExcept
#print axioms rawTableEquiv
#print axioms instPrimcodableRawTransitionTable
#print axioms UniformPrimrecStatement
#print axioms primrec_of_encoding
#print axioms primrec_analyzeEncodedSystem
#print axioms computable_analyzeEncodedSystem
#print axioms computablePred_of_encoding
#print axioms analyzeTransitionTable_bound
#print axioms analyzeEncodedSystem_bound
#print axioms boolEncoding
#print axioms emptyEncoding

#print axioms TamesisLab.Tests.FoundComputabilityBridge001.boolEncoding_nonempty
#print axioms TamesisLab.Tests.FoundComputabilityBridge001.boolEncoding_analysis_concrete
#print axioms TamesisLab.Tests.FoundComputabilityBridge001.boolEncoding_bound_applies
#print axioms TamesisLab.Tests.FoundComputabilityBridge001.boolEncoding_primrec
#print axioms TamesisLab.Tests.FoundComputabilityBridge001.boolEncoding_primrec_canonical
#print axioms TamesisLab.Tests.FoundComputabilityBridge001.boolEncoding_computable
#print axioms TamesisLab.Tests.FoundComputabilityBridge001.emptyEncoding_isEmpty

end TamesisLab.Tests.FoundComputabilityBridge001Axioms
