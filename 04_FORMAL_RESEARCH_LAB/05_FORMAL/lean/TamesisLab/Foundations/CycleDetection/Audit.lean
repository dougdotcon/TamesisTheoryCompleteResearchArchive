import TamesisLab.Foundations.CycleDetection.Correctness
import TamesisLab.Foundations.CycleDetection.Periodicity

set_option autoImplicit false

/-!
# FOUND-CYCLE-DETECTION-001 — Auditoria de assinaturas

Somente `#check`. Nenhuma definição, nenhum teorema.

O que esta auditoria torna visível:

```text
cycleCandidates e mem_cycleCandidates_iff   sem X, sem Fintype, sem DecidableEq
CycleWitness.Valid                          com Fintype, SEM DecidableEq
detectCycleWitness? e seus dois teoremas    com Fintype e DecidableEq
isPeriodicPt, mem_periodicPts, propagates   SEM DecidableEq
```
-/

namespace TamesisLab.Foundations.CycleDetection

-- camada 0: sem hipóteses sobre o tipo de estados
#check @CycleWitness
#check @CycleWitness.baseIndex
#check @CycleWitness.period
#check @cycleCandidates
#check @cycleCandidates_zero
#check @cycleCandidates_one
#check @mem_cycleCandidates_iff

-- camada 1: Fintype pela cota, sem DecidableEq
#check @CycleWitness.Valid

-- instância decidível explícita
#check @CycleWitness.decidableValid

-- camada 2: execução, com DecidableEq
#check @detectCycleWitness?
#check @detectCycleWitness?_sound
#check @detectCycleWitness?_complete

-- camada 3: pontes proposicionais, sem DecidableEq
#check @CycleWitness.isPeriodicPt
#check @CycleWitness.mem_periodicPts
#check @CycleWitness.propagates

-- resultados reutilizados, não reimplementados
#check @TamesisLab.Foundations.FiniteDynamics.exists_bounded_iterate_collision
#check @TamesisLab.Foundations.FiniteDynamics.periodic_tail_of_collision
#check @TamesisLab.Foundations.FiniteDynamics.collision_propagates

end TamesisLab.Foundations.CycleDetection
