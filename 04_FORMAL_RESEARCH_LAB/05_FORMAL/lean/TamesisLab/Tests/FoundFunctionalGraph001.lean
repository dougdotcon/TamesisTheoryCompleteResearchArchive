import TamesisLab.Foundations.FunctionalGraphs

set_option autoImplicit false

/-!
# Teste isolado — FOUND-FUNCTIONAL-GRAPH-001 (núcleo)

Confirma assinaturas e, sobretudo, **quais hipóteses cada teorema
efetivamente exige**. Nenhuma prova nova.
-/

namespace TamesisLab.Tests.FoundFunctionalGraph001

open TamesisLab.Foundations.FunctionalGraphs

/-! ## Relações — nenhuma finitude -/

example {X : Type*} (f : X → X) (x : X) : IterReachable f x x :=
  iterReachable_refl f x

example {X : Type*} {f : X → X} {x y z : X}
    (h₁ : IterReachable f x y) (h₂ : IterReachable f y z) :
    IterReachable f x z :=
  iterReachable_trans h₁ h₂

example {X : Type*} {f : X → X} {x y : X} (h : IterReachable f x y) :
    EventuallyMeets f x y :=
  h.eventuallyMeets

example {X : Type*} (f : X → X) (x : X) : EventuallyMeets f x x :=
  eventuallyMeets_refl f x

example {X : Type*} {f : X → X} {x y : X} (h : EventuallyMeets f x y) :
    EventuallyMeets f y x :=
  eventuallyMeets_symm h

/-- Transitividade **sem** `Fintype X` e **sem** `DecidableEq X`. -/
example {X : Type*} {f : X → X} {x y z : X}
    (h₁ : EventuallyMeets f x y) (h₂ : EventuallyMeets f y z) :
    EventuallyMeets f x z :=
  eventuallyMeets_trans h₁ h₂

/-- `MutuallyReachable` é conjunção das duas direções. -/
example {X : Type*} {f : X → X} {x y : X}
    (h₁ : IterReachable f x y) (h₂ : IterReachable f y x) :
    MutuallyReachable f x y :=
  ⟨h₁, h₂⟩

/-! ## Empacotamento relacional — sem instâncias -/

example {X : Type*} (f : X → X) : Std.Refl (EventuallyMeets f) :=
  eventuallyMeets_isRefl f

example {X : Type*} (f : X → X) : Std.Symm (EventuallyMeets f) :=
  eventuallyMeets_isSymm f

example {X : Type*} (f : X → X) : IsTrans X (EventuallyMeets f) :=
  eventuallyMeets_isTrans f

/-! ## Igualdade de órbitas — nenhuma finitude -/

example {X : Type*} {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f) (hq : q ∈ Function.periodicPts f)
    (h : EventuallyMeets f p q) :
    Function.periodicOrbit f p = Function.periodicOrbit f q :=
  periodicOrbit_eq_of_eventuallyMeets hp hq h

/-- Recíproca opcional, também sem finitude. -/
example {X : Type*} {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f) (hq : q ∈ Function.periodicPts f)
    (h : Function.periodicOrbit f p = Function.periodicOrbit f q) :
    EventuallyMeets f p q :=
  eventuallyMeets_of_periodicOrbit_eq hp hq h

/-! ## Existência e teorema principal — `[Fintype X]` apenas -/

example {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ mu : ℕ, mu < Fintype.card X ∧ f^[mu] x ∈ Function.periodicPts f :=
  exists_cyclePoint_reachable_with_bound f x

example {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ mu : ℕ,
      mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f ∧
      ∀ q : X,
        q ∈ Function.periodicPts f →
        EventuallyMeets f x q →
        Function.periodicOrbit f (f^[mu] x) = Function.periodicOrbit f q :=
  exists_component_cycle_with_entry_bound f x

/-- Aplicável a um tipo externo à frente, sem fornecer `DecidableEq`. -/
example (f : Bool → Bool) (b : Bool) :
    ∃ mu : ℕ, mu < Fintype.card Bool ∧ f^[mu] b ∈ Function.periodicPts f :=
  exists_cyclePoint_reachable_with_bound f b

/-! ## Assinaturas — inspeção explícita

A saída destes `#check` deve mostrar que `eventuallyMeets_trans` e
`periodicOrbit_eq_of_eventuallyMeets` **não** exigem `Fintype X` nem
`DecidableEq X`, e que `exists_component_cycle_with_entry_bound` exige
**apenas** `[Fintype X]`. -/

#check @eventuallyMeets_trans
#check @periodicOrbit_eq_of_eventuallyMeets
#check @exists_cyclePoint_reachable_with_bound
#check @exists_component_cycle_with_entry_bound

end TamesisLab.Tests.FoundFunctionalGraph001
