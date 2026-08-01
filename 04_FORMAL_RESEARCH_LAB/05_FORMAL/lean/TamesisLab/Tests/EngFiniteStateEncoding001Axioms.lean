import TamesisLab.Engineering.FiniteStateEncoding

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — auditoria de axiomas

Somente `#print axioms`. Nenhum experimento destinado a falhar vive
neste arquivo: seu contrato é terminar com código de saída zero.

Resultado esperado, e verificado:

```text
encode_injective    nenhum axioma
encodedStep         nenhum axioma
buildTransitionTable e cadeia posterior
                    propext, Classical.choice, Quot.sound
```

A pegada entra na **primeira** declaração que consome a API de arrays —
`buildTransitionTable`, pelo campo `closed` — e propaga pelo tipo, não
pela prova. Ela vive em proposições apagadas na execução; nenhuma
escolha clássica produz `encode`, `decode`, o `Array` ou o resultado.
-/

namespace TamesisLab.Tests.EngFiniteStateEncoding001Axioms

open TamesisLab.Engineering.FiniteStateEncoding

#print axioms CertifiedFiniteEncoding.encode_injective
#print axioms CertifiedFiniteEncoding.encodedStep
#print axioms buildTransitionTable
#print axioms buildTransitionTable_size
#print axioms CertifiedFiniteEncoding.tableIndex
#print axioms CertifiedFiniteEncoding.tableIndex_val
#print axioms CertifiedFiniteEncoding.tableIndex_semiconj
#print axioms CertifiedFiniteEncoding.table_step_commutes
#print axioms CertifiedFiniteEncoding.table_iterate_commutes
#print axioms CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
#print axioms analyzeEncodedSystem
#print axioms analyzeEncodedSystem_sound
#print axioms analyzeEncodedSystem_complete
#print axioms analyzeEncodedSystem_ne_error

end TamesisLab.Tests.EngFiniteStateEncoding001Axioms
