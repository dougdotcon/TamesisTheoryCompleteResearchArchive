import TamesisLab.Engineering.FiniteStateEncoding

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — auditoria de assinaturas

Somente `#check`. Nenhuma definição, nenhum teorema.

O que esta auditoria torna visível:

```text
CertifiedFiniteEncoding    quatro campos, nenhuma typeclass
encodedStep                Fin n -> Fin n, sem hipotese
buildTransitionTable       devolve ValidatedTransitionTable direto
tableIndex                 unico transporte publico
analyzeEncodedSystem       assinatura sem typeclass alguma
```

O auxiliar de leitura é privado e, por isso, **não** aparece aqui.
-/

namespace TamesisLab.Engineering.FiniteStateEncoding

#check @CertifiedFiniteEncoding
#check @CertifiedFiniteEncoding.encode
#check @CertifiedFiniteEncoding.decode
#check @CertifiedFiniteEncoding.decode_encode
#check @CertifiedFiniteEncoding.encode_decode
#check @CertifiedFiniteEncoding.encode_injective
#check @CertifiedFiniteEncoding.encodedStep

#check @buildTransitionTable
#check @buildTransitionTable_size

#check @CertifiedFiniteEncoding.tableIndex
#check @CertifiedFiniteEncoding.tableIndex_val

#check @CertifiedFiniteEncoding.tableIndex_semiconj
#check @CertifiedFiniteEncoding.table_step_commutes
#check @CertifiedFiniteEncoding.table_iterate_commutes
#check @CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate

#check @analyzeEncodedSystem
#check @analyzeEncodedSystem_sound
#check @analyzeEncodedSystem_complete
#check @analyzeEncodedSystem_ne_error

end TamesisLab.Engineering.FiniteStateEncoding
