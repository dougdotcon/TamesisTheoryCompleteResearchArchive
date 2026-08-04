import Mathlib.Logic.Function.Iterate

set_option autoImplicit false

/-!
# FOUND-INVARIANT-UNREACHABILITY-001 — definições

A frente inteira repousa numa igualdade de definições.

```text
Invariant abstract stepC    forall c, abstract (stepC c) = abstract c
Semiconj abstract stepC id  forall c, abstract (stepC c) = id (abstract c)
```

São a mesma proposição. `Invariant.semiconj` é o próprio termo, sem
`Iff`, sem transporte, sem conversão — e é por isso que toda a
maquinaria de iteradas já provada fica disponível de graça.

Este módulo **não** importa nada do laboratório. Nenhuma typeclass é
exigida, nenhuma finitude é mencionada, e o tipo concreto pode ser
infinito.
-/

namespace TamesisLab.Foundations.Invariants

variable {C A : Type*}

/-- Uma função **invariante** ao longo do passo: observar antes e depois
do passo dá o mesmo valor.

É a forma geral de paridade, coloração e qualquer quantidade conservada.
Nada é exigido de `C`, de `A` ou de `stepC` além de serem o que são. -/
def Invariant (abstract : C → A) (stepC : C → C) : Prop :=
  ∀ c : C, abstract (stepC c) = abstract c

/-- **A ponte, e ela não custa nada.**

Um invariante é uma semiconjugação para o sistema parado. O corpo desta
prova é a hipótese, literalmente: as duas proposições são a mesma. -/
theorem Invariant.semiconj {abstract : C → A} {stepC : C → C}
    (h : Invariant abstract stepC) : Function.Semiconj abstract stepC id :=
  h

/-- Constância ao longo de toda a órbita.

Consequência direta de `Function.Semiconj.iterate_right`, que já estava
provada. A indução **não** é refeita aqui. -/
theorem Invariant.iterate {abstract : C → A} {stepC : C → C}
    (h : Invariant abstract stepC) (k : Nat) (c : C) :
    abstract ((stepC^[k]) c) = abstract c := by
  have hs := h.semiconj.iterate_right k c
  simpa using hs

/-- `y` é alcançável a partir de `x` em um número finito de passos.

Proposicional. Não é decidível, não é enumerada, e nenhuma finitude é
assumida. -/
def Reachable (stepC : C → C) (x y : C) : Prop := ∃ k : Nat, (stepC^[k]) x = y

end TamesisLab.Foundations.Invariants
