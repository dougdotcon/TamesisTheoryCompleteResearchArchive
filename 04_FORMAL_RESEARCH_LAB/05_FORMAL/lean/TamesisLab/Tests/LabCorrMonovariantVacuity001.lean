import TamesisLab.Foundations.Descent
import TamesisLab.Foundations.Monovariants

set_option autoImplicit false

/-!
# Testes de LAB-CORR-MONOVARIANT-VACUITY-001

A **instância positiva** que a frente encerrada nunca exibiu, e que é
exatamente o que o gate corretivo passa a exigir de toda frente.
-/

namespace TamesisLab.Tests.LabCorrMonovariantVacuity001

open TamesisLab.Foundations.Descent
open TamesisLab.Foundations.Monovariants

/-- **A instância positiva.** Subtração truncada decresce **enquanto** o
estado é positivo. Este é o mesmo `strictDown` que a frente encerrada
registrou como falha — e ele funciona, na forma corrigida. -/
theorem strictDown_descendsOn :
    DescendsOn (fun k : Nat => k) strictDown (fun k : Nat => 0 < k) := by
  intro k hk
  simp only [strictDown]
  omega

/-- E o sistema termina de verdade: chega-se a zero a partir de qualquer
estado. -/
theorem strictDown_reaches_zero (k : Nat) :
    ∃ m : Nat, ¬ (0 < (strictDown^[m]) k) :=
  strictDown_descendsOn.exits k

end TamesisLab.Tests.LabCorrMonovariantVacuity001
