import TamesisLab.Foundations.CycleDetection.Witness
import TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity

set_option autoImplicit false

/-!
# FOUND-CYCLE-DETECTION-001 — Pontes proposicionais

O que o certificado significa, uma vez obtido.

**Nenhum dos três teoremas exige `DecidableEq X`.** Eles consomem apenas a
igualdade `f^[baseIndex + period] x = f^[baseIndex] x` que já vem dentro
de `CycleWitness.Valid`, e são aplicações diretas de teoremas já
verificados em `FOUND-SEMIGROUP-002`. Nenhuma aritmética de iteradas é
reprovada, e `Function.iterate_add_apply` não aparece.

O objeto de órbita da Mathlib — o ciclo quociente por rotação — **não**
aparece aqui: ele não é computável, e a ponte com o componente funcional
foi deliberadamente omitida desta primeira formalização. Ver
`RESULT_BOUNDARY.md`.
-/

namespace TamesisLab.Foundations.CycleDetection

open TamesisLab.Foundations.FiniteDynamics

/-- O ponto-base do certificado é periódico, com o período testemunhado.

Aplicação direta de `periodic_tail_of_collision`. -/
theorem CycleWitness.isPeriodicPt {X : Type*} [Fintype X] {f : X → X} {x : X}
    {w : CycleWitness} (h : CycleWitness.Valid f x w) :
    Function.IsPeriodicPt f w.period (f^[w.baseIndex] x) :=
  periodic_tail_of_collision f x h.2.2.2

/-- O ponto-base pertence ao conjunto dos pontos periódicos.

Consome exatamente o `0 < period` do contrato. `Function.minimalPeriod`
não é usada. -/
theorem CycleWitness.mem_periodicPts {X : Type*} [Fintype X] {f : X → X}
    {x : X} {w : CycleWitness} (h : CycleWitness.Valid f x w) :
    f^[w.baseIndex] x ∈ Function.periodicPts f :=
  Function.mk_mem_periodicPts h.2.1 (CycleWitness.isPeriodicPt h)

/-- A repetição propaga-se a toda a cauda posterior.

Aplicação direta de `collision_propagates`, cuja assinatura tem exatamente
esta forma: hipótese primeiro, `k` depois. -/
theorem CycleWitness.propagates {X : Type*} [Fintype X] {f : X → X} {x : X}
    {w : CycleWitness} (h : CycleWitness.Valid f x w) (k : ℕ) :
    f^[w.baseIndex + k + w.period] x = f^[w.baseIndex + k] x :=
  collision_propagates f x h.2.2.2 k

end TamesisLab.Foundations.CycleDetection
