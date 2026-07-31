import TamesisLab.Foundations.CycleDetection

set_option autoImplicit false

/-!
# Auditoria de computabilidade de FOUND-CYCLE-DETECTION-001

Registro vinculante, para evitar uma leitura errada da saída abaixo:

```text
A presenca de Classical.choice em #print axioms NAO significa que a
funcao esteja marcada como nao computavel.

A definicao foi avaliada por #eval e nao usa escolha classica para
CONSTRUIR o certificado.
```

A pegada de `detectCycleWitness?` vem de `Fintype.card` e `Finset.univ`,
cuja infraestrutura de `Finset` usa escolha dentro de **provas**, que são
apagadas na compilação. `cycleCandidates`, que não menciona `Fintype`, não
depende de axioma algum.

Permitidos: `propext`, `Classical.choice`, `Quot.sound`.
Proibidos: `sorryAx` e axiomas locais.
-/

namespace TamesisLab.Tests.FoundCycleDetection001Axioms

open TamesisLab.Foundations.CycleDetection

#print axioms cycleCandidates
#print axioms mem_cycleCandidates_iff
#print axioms detectCycleWitness?
#print axioms detectCycleWitness?_sound
#print axioms detectCycleWitness?_complete
#print axioms CycleWitness.isPeriodicPt
#print axioms CycleWitness.mem_periodicPts
#print axioms CycleWitness.propagates

/-! A instância decidível resolve por `#synth`. -/

section
variable {X : Type} [Fintype X] [DecidableEq X] (f : X → X) (x : X)
  (w : CycleWitness)

#synth Decidable (CycleWitness.Valid f x w)

end

end TamesisLab.Tests.FoundCycleDetection001Axioms
