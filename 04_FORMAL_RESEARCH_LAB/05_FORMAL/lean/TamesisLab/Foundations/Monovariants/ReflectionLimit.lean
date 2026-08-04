import TamesisLab.Foundations.Monovariants.Definitions
import TamesisLab.Foundations.Monovariants.WitnessBounds
import TamesisLab.Foundations.FiniteStateAbstraction.OrbitSeparation

set_option autoImplicit false

/-!
# FOUND-MONOVARIANT-DESCENT-001 — o limite da reflexão

O resultado central, e ele é **mais forte** que o da frente de
invariantes.

```text
invariante     OrbitSeparating vale EXATAMENTE nos pontos fixos
monovariante   OrbitSeparating NAO VALE EM LUGAR NENHUM
```

A razão cabe em duas linhas. Um monovariante exclui recorrência concreta
em qualquer número positivo de passos. A análise abstrata **sempre**
devolve um certificado, e o período dele é **positivo**. Logo a reflexão
produziria uma recorrência que o monovariante proíbe.

Consequência: **todo ciclo abstrato de um sistema monovariante é
espúrio**, sem exceção.
-/

namespace TamesisLab.Foundations.Monovariants

open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.FiniteStateAbstraction
open TamesisLab.Engineering.FiniteStateEncoding

variable {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}

/-- **Um monovariante impede a reflexão, sempre.**

Nenhuma hipótese que o consumidor precise inventar: `0 < period` vem de
`WitnessBounds.lean`. -/
theorem monovariant_not_orbitSeparating {measure : C → Nat}
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C} {witness : CycleWitness}
    (hmono : Monovariant measure stepC)
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    ¬ OrbitSeparating abstraction.abstract stepC start := by
  intro hsep
  have hrec := analyzeAbstractSystem_reflected_sound hsep h
  have hp := analyzeAbstractSystem_period_pos h
  have hsum : witness.baseIndex + witness.period = witness.period + witness.baseIndex := by
    omega
  rw [hsum, Function.iterate_add_apply] at hrec
  exact hmono.no_periodic_point hp ((stepC^[witness.baseIndex]) start) hrec

end TamesisLab.Foundations.Monovariants
