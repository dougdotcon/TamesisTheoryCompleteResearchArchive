import TamesisLab.Engineering.FiniteStateEncoding.Encoding
import TamesisLab.Engineering.FiniteStateEncoding.TableConstruction
import TamesisLab.Engineering.FiniteStateEncoding.Commutation
import TamesisLab.Engineering.FiniteStateEncoding.DynamicAnalysis

/-!
# ENG-FINITE-STATE-ENCODING-001 — agregador

Ponte entre um sistema determinístico **tipado** e o adaptador de runtime
já verificado.

```text
Encoding.lean           CertifiedFiniteEncoding, encode_injective, encodedStep
TableConstruction.lean  buildTransitionTable, tamanho, tableIndex, tableIndex_val
Commutation.lean        semiconjugacao, passo, iteradas, correspondencia com run?
DynamicAnalysis.lean    analyzeEncodedSystem, soundness e completeness tipadas
```

O consumidor fornece a codificação, `stepS : S → S` e `start : S`.
Nenhuma typeclass é exigida dele.

A frente anterior provava algo sobre **a tabela**. Esta prova algo sobre
**a relação entre a tabela e o sistema**: a soundness termina numa
igualdade em `S`.

Ela cobre apenas sistemas formais tipados acompanhados de codificação
certificada. Não prova que um programa, serviço, workflow, agente ou
processo físico foi corretamente modelado.

scientific_value: FORMAL_SOFTWARE_BRIDGE
mathematical_novelty: NONE
algorithmic_novelty: NONE
-/
