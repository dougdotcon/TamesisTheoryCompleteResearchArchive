import TamesisLab.Foundations.FiniteStateAbstraction.Observation

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — separação da órbita e reflexão

A hipótese que converte recorrência observacional em recorrência
concreta, e o teorema que a consome.

```text
soundness observacional
→ OrbitSeparating
→ igualdade concreta em C
```

`OrbitSeparating` **não** é tautológica: ela quantifica sobre todos os
pares de índices da órbita, enquanto a conclusão da reflexão compara um
único par. `Counterexample.lean` prova que ela falha exatamente onde a
semiconjugação sozinha não basta — logo não decorre dela.

Ela também não exige injetividade global, nem finitude de `C`, nem
igualdade decidível.
-/

namespace TamesisLab.Foundations.FiniteStateAbstraction

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.CycleDetection

variable {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}

/-- A abstração **separa** os estados da órbita alcançada a partir de
`start`.

Obrigação do consumidor, verificável por órbita. Exige injetividade
apenas onde os índices do certificado vivem — não globalmente.

Equivalente a `Set.InjOn abstract (Set.range fun k => stepC^[k] start)`.
A equivalência foi provada em probe e deliberadamente **não** exposta:
nenhum resultado desta frente a consome, e publicá-la obrigaria o núcleo
a carregar `Set`, `Set.range` e `Set.InjOn` para servir a ninguém. -/
def OrbitSeparating (abstract : C → A) (stepC : C → C) (start : C) : Prop :=
  ∀ i j : Nat,
    abstract ((stepC^[i]) start) = abstract ((stepC^[j]) start) →
      (stepC^[i]) start = (stepC^[j]) start

/-- **Soundness concreta, sob hipótese explícita.**

A única declaração pública da frente que conclui uma igualdade em `C`, e
ela paga por isso com `hSeparating`, visível na assinatura.

A hipótese não vive dentro de `CertifiedFiniteAbstraction`, não é
instância e não é derivada. Quem quiser a conclusão concreta tem de
exibir a separação — esse é o conteúdo científico do teorema. -/
theorem analyzeAbstractSystem_reflected_sound
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C} {witness : CycleWitness}
    (hSeparating : OrbitSeparating abstraction.abstract stepC start)
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    (stepC^[witness.baseIndex + witness.period]) start = (stepC^[witness.baseIndex]) start :=
  hSeparating (witness.baseIndex + witness.period) witness.baseIndex
    (analyzeAbstractSystem_observational_sound h)

end TamesisLab.Foundations.FiniteStateAbstraction
