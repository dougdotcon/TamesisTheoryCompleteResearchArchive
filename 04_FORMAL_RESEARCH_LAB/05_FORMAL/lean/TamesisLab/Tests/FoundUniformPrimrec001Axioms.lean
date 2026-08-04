import TamesisLab.Tests.FoundUniformPrimrec001

/-!
# Pegada de FOUND-UNIFORM-PRIMREC-001

Cobertura integral das 31 publicas, da TEST_ONLY e dos 3 testes.
O auxiliar privado nao e alcancavel daqui; e medido no probe.
-/

namespace TamesisLab.Tests.FoundUniformPrimrec001Axioms

open TamesisLab.Foundations.UniformPrimrec

#print axioms primrec_next_toList
#print axioms primrec_size
#print axioms primrec_witness_pair
#print axioms primrec_baseIndex
#print axioms primrec_period
#print axioms primrec_mk
#print axioms primrec_step?
#print axioms iterate_bind_none
#print axioms run?_eq_iterate
#print axioms primrec_run?_gen
#print axioms validBool
#print axioms foldr_lt_eq_true
#print axioms validBool_iff
#print axioms primrec_validBool
#print axioms flatMap_eq_foldr
#print axioms primrec_cycleCandidates
#print axioms RawValid
#print axioms rawValidBool
#print axioms rawValidBool_iff
#print axioms primrec_rawValidBool
#print axioms valid_iff_rawValid
#print axioms detectCycle?_eq_raw
#print axioms analyzeRaw
#print axioms analyzeRaw_eq
#print axioms primrec_ok
#print axioms primrec_error
#print axioms primrec_initialStateOutOfBounds
#print axioms primrec_find
#print axioms primrec_analyzeRaw
#print axioms primrec_analyzeTransitionTable
#print axioms uniformPrimrecStatement_holds
#print axioms twoCycle

#print axioms TamesisLab.Tests.FoundUniformPrimrec001.twoCycle_valid
#print axioms TamesisLab.Tests.FoundUniformPrimrec001.twoCycle_analysis
#print axioms TamesisLab.Tests.FoundUniformPrimrec001.twoCycle_analyzeRaw

end TamesisLab.Tests.FoundUniformPrimrec001Axioms
