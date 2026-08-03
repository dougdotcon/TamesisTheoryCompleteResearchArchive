import TamesisLab.Foundations.FiniteStateAbstraction.AbstractAnalysis

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — soundness observacional

O resultado central da frente.

```text
analyzeEncodedSystem_sound no sistema A
→ igualdade entre iteradas de stepA
→ iterate_commutes para os dois indices
→ igualdade entre observacoes de estados concretos
```

A conclusão vive em `A`, **depois** de aplicar `abstract`. Ela afirma
que os dois estados concretos têm a mesma observação — e não que sejam
iguais.

Essa distinção é a frente inteira. A igualdade concreta exige uma
hipótese adicional, e mora em `OrbitSeparation.lean`.
-/

namespace TamesisLab.Foundations.FiniteStateAbstraction

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.CycleDetection

variable {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}

/-- **Soundness observacional.**

Um certificado devolvido pela análise do sistema abstrato produz
recorrência **observacional** no sistema concreto.

A hipótese é única: a execução devolveu `.ok`. Não há hipótese de
separação, nem typeclass, nem finitude de `C` — e é essa gratuidade que
torna o resultado o centro da frente.

Nada é afirmado sobre minimalidade de `baseIndex`, sobre `period` ser
mínimo, sobre unicidade do certificado ou sobre invariância sob
recodificação. -/
theorem analyzeAbstractSystem_observational_sound
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C} {witness : CycleWitness}
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    abstraction.abstract ((stepC^[witness.baseIndex + witness.period]) start)
      = abstraction.abstract ((stepC^[witness.baseIndex]) start) := by
  rw [abstraction.iterate_commutes, abstraction.iterate_commutes]
  exact analyzeEncodedSystem_sound h

end TamesisLab.Foundations.FiniteStateAbstraction
