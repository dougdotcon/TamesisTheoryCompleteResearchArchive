import TamesisLab

set_option autoImplicit false

/-!
# Auditoria de instâncias de FOUND-CYCLE-DETECTION-001

Importa a raiz `TamesisLab`, de modo que **todas** as instâncias do
laboratório ficam em escopo, e confirma que a síntese continua sem
ambiguidade.

Nenhum módulo matemático é alterado. Nenhum teorema novo.
-/

namespace TamesisLab.Tests.FoundCycleDetection001InstanceAudit

open TamesisLab.Foundations.CycleDetection

/-! ## A instância é encontrada, e é a declarada -/

section
variable {X : Type} [Fintype X] [DecidableEq X] (f : X → X) (x : X)
  (w : CycleWitness)

#synth Decidable (CycleWitness.Valid f x w)

end

#synth DecidableEq CycleWitness
#synth Repr CycleWitness
#synth BEq CycleWitness

/-! ## Com o laboratório inteiro em escopo, o detector continua se
aplicando -/

#synth Decidable (CycleWitness.Valid (fun b : Bool => !b) true ⟨0, 2⟩)
#synth Decidable (CycleWitness.Valid (id : Fin 3 → Fin 3) 0 ⟨0, 1⟩)

example : Option CycleWitness := detectCycleWitness? (fun b : Bool => !b) true
example : Option CycleWitness := detectCycleWitness? (id : Fin 1 → Fin 1) 0
example : Option CycleWitness := detectCycleWitness? (id : Fin 3 → Fin 3) 0
example : Option CycleWitness := detectCycleWitness? (id : Fin 4 → Fin 4) 0

#eval detectCycleWitness? (fun b : Bool => !b) true
#eval detectCycleWitness? (id : Fin 3 → Fin 3) 2

/-! ## Nenhuma instância global de `DecidableEq X` foi criada

O detector recebe `DecidableEq X` como hipótese; ele não a fabrica. O
exemplo abaixo só typecheck porque a hipótese é fornecida no contexto. -/

example {X : Type} [Fintype X] [DecidableEq X] (f : X → X) (x : X) :
    Option CycleWitness :=
  detectCycleWitness? f x

/-! ## A instância não interfere nas camadas proposicionais -/

example {X : Type} [Fintype X] {f : X → X} {x : X} {w : CycleWitness}
    (h : CycleWitness.Valid f x w) :
    f^[w.baseIndex] x ∈ Function.periodicPts f :=
  CycleWitness.mem_periodicPts h

/-! ## Coexistência com as instâncias das frentes anteriores -/

open TamesisLab.Foundations.FunctionalGraphs in
example {X : Type} [Fintype X] (f : X → X) (x y : X) : Prop :=
  EventuallyMeets f x y

end TamesisLab.Tests.FoundCycleDetection001InstanceAudit
