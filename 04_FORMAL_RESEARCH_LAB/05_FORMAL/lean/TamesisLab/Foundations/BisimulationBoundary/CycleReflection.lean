import TamesisLab.Foundations.BisimulationBoundary.CounterexampleInstance

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — bissimulação não reflete ciclos

As duas negações públicas, consequência do colapso aplicado ao
contraexemplo.

```text
BOOL_TO_UNIT e uma bissimulacao,  e forgetBool e SOBREJETIVA,
e o ciclo continua espurio.
```

O quadro completo:

```text
semiconjugacao             NAO reflete
bissimulacao funcional     NAO reflete   (e a mesma coisa)
bissimulacao sobrejetiva   NAO reflete
OrbitSeparating            REFLETE
```

Reforçar a relação de simulação não atravessa a fronteira entre observar
e refletir. O que atravessa é **separação de estados**.

Ambos os resultados são negações **provadas**. Nenhum arquivo destinado
a falhar.
-/

namespace TamesisLab.Foundations.BisimulationBoundary

open TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

/-- **Bissimulação não reflete ciclos.** -/
theorem bisimulation_does_not_reflect_cycles :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Bisimulation abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start) :=
  fun h => boolToUnit_no_concrete_recurrence
    (h Bool Unit concreteStep abstractStep forgetBool boolToUnit_bisimulation false rfl)

/-- **Nem mesmo bissimulação sobrejetiva reflete ciclos.** -/
theorem surjective_bisimulation_does_not_reflect_cycles :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Function.Surjective abstract →
        Bisimulation abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start) :=
  fun h => boolToUnit_no_concrete_recurrence
    (h Bool Unit concreteStep abstractStep forgetBool forgetBool_surjective
      boolToUnit_bisimulation false rfl)

end TamesisLab.Foundations.BisimulationBoundary
