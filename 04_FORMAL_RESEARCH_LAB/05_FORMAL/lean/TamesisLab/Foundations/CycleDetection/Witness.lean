import Mathlib.Data.Fintype.Card
import Mathlib.Logic.Function.Iterate

set_option autoImplicit false

/-!
# FOUND-CYCLE-DETECTION-001 — Certificado

O dado devolvido pelo detector é um par de naturais. Nada mais.

```text
baseIndex é o índice-base de uma colisão certificada.
Não é afirmado como o menor índice de entrada no ciclo.

period é um período positivo testemunhado.
Não é afirmado como Function.minimalPeriod.
```

A estrutura **não** é parametrizada pelo tipo de estados: `entryPoint` é
derivável por `f^[w.baseIndex] x` e foi deliberadamente rejeitado, junto
com listas do ciclo, marcas de minimalidade e provas embutidas.

O contrato `CycleWitness.Valid` foi escrito para coincidir **termo a
termo** com a conclusão de
`FiniteDynamics.exists_bounded_iterate_collision`: mesmas quatro
cláusulas, mesma ordem, mesmas cotas. É isso que torna a completude um
transporte, e não uma prova nova.
-/

namespace TamesisLab.Foundations.CycleDetection

/-- Certificado de repetição de uma trajetória determinística finita.

`baseIndex` é o índice-base da igualdade
`f^[baseIndex + period] x = f^[baseIndex] x`, e `period` é um período
positivo testemunhado. Nenhum dos dois é afirmado mínimo. -/
structure CycleWitness where
  /-- Índice-base da colisão certificada. Não afirmado mínimo. -/
  baseIndex : ℕ
  /-- Período positivo testemunhado. Não é `Function.minimalPeriod`. -/
  period : ℕ
deriving DecidableEq, Repr, BEq

/-- Contrato do certificado.

As quatro cláusulas estão na mesma ordem da conclusão de
`FiniteDynamics.exists_bounded_iterate_collision`. Note a ausência de
`DecidableEq X`: afirmar a igualdade de dois estados não exige poder
decidi-la. -/
def CycleWitness.Valid {X : Type*} [Fintype X] (f : X → X) (x : X)
    (w : CycleWitness) : Prop :=
  w.baseIndex < Fintype.card X ∧
  0 < w.period ∧
  w.baseIndex + w.period ≤ Fintype.card X ∧
  f^[w.baseIndex + w.period] x = f^[w.baseIndex] x

/-- Instância decidível **explícita**.

A auditoria da especificação mostrou que a resolução de instâncias não
desdobra `CycleWitness.Valid`, por ele ser um `def`. Sem esta declaração,
`decide (CycleWitness.Valid f x w)` não elabora e o detector não compila.

Depende apenas de `[Fintype X]` e `[DecidableEq X]`. -/
instance CycleWitness.decidableValid {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) (w : CycleWitness) :
    Decidable (CycleWitness.Valid f x w) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

end TamesisLab.Foundations.CycleDetection
