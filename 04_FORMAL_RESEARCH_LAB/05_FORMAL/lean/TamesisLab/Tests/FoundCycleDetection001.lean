import TamesisLab.Foundations.CycleDetection

set_option autoImplicit false

/-!
# Teste da API formal de FOUND-CYCLE-DETECTION-001

Verifica as assinaturas públicas e a aplicação genérica da API a quatro
tipos finitos concretos. Nenhum teorema novo.
-/

namespace TamesisLab.Tests.FoundCycleDetection001

open TamesisLab.Foundations.CycleDetection

#check @CycleWitness
#check @CycleWitness.Valid
#check @CycleWitness.decidableValid
#check @cycleCandidates
#check @mem_cycleCandidates_iff
#check @detectCycleWitness?
#check @detectCycleWitness?_sound
#check @detectCycleWitness?_complete
#check @CycleWitness.isPeriodicPt
#check @CycleWitness.mem_periodicPts
#check @CycleWitness.propagates

/-! ## A enumeração não vê o tipo de estados -/

example (n : ℕ) : List CycleWitness := cycleCandidates n

example {w : CycleWitness} {n : ℕ} (h : w ∈ cycleCandidates n) :
    w.baseIndex < n :=
  (mem_cycleCandidates_iff.mp h).1

/-! ## `Valid` exige `Fintype`, não `DecidableEq` -/

example {X : Type} [Fintype X] (f : X → X) (x : X) (w : CycleWitness) : Prop :=
  CycleWitness.Valid f x w

/-! ## As pontes proposicionais não exigem `DecidableEq` -/

example {X : Type} [Fintype X] {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) :
    f^[w.baseIndex] x ∈ Function.periodicPts f :=
  CycleWitness.mem_periodicPts h

example {X : Type} [Fintype X] {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) (k : ℕ) :
    f^[w.baseIndex + k + w.period] x = f^[w.baseIndex + k] x :=
  CycleWitness.propagates h k

/-! ## Aplicação genérica a tipos concretos -/

example (f : Bool → Bool) (x : Bool) : Option CycleWitness :=
  detectCycleWitness? f x

example (f : Fin 1 → Fin 1) (x : Fin 1) : Option CycleWitness :=
  detectCycleWitness? f x

example (f : Fin 3 → Fin 3) (x : Fin 3) : Option CycleWitness :=
  detectCycleWitness? f x

example (f : Fin 4 → Fin 4) (x : Fin 4) :
    ∃ w : CycleWitness, detectCycleWitness? f x = some w :=
  detectCycleWitness?_complete f x

example (f : Bool → Bool) (x : Bool) {w : CycleWitness}
    (h : detectCycleWitness? f x = some w) :
    f^[w.baseIndex] x ∈ Function.periodicPts f :=
  CycleWitness.mem_periodicPts (detectCycleWitness?_sound h)

/-! ## A instância decidível resolve -/

example {X : Type} [Fintype X] [DecidableEq X] (f : X → X) (x : X)
    (w : CycleWitness) : Decidable (CycleWitness.Valid f x w) :=
  inferInstance

end TamesisLab.Tests.FoundCycleDetection001
