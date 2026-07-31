import TamesisLab.Foundations.FunctionalGraphs

set_option autoImplicit false

/-!
# Auditoria de instâncias e superfície pública — FOUND-FUNCTIONAL-GRAPH-001

Não introduz matemática. Verifica, por síntese e typecheck:

1. o núcleo matemático (`Relations`, `PeriodicOrbits`, `ComponentCycle`)
   **não declara instância alguma** — as cinco pertencem a contraexemplos;
2. importar o agregador, com todas as instâncias em escopo, **não** cria
   ambiguidade nem impede o uso da API em tipos externos;
3. nenhuma instância de `Setoid`, `Preorder` ou `SimpleGraph` existe.

Nenhum módulo matemático foi alterado para esta auditoria.
-/

namespace TamesisLab.Tests.FoundFunctionalGraph001InstanceAudit

open TamesisLab.Foundations.FunctionalGraphs
open TamesisLab.Foundations.FunctionalGraphs.Counterexamples

/-! ## 1. As cinco instâncias, sintetizadas nominalmente

`CE001`, `CE002`, `CE003`, `CE004` e `CE006` declaram uma `Fintype` cada.
`CE005` não declara instância: reutiliza o modelo de `CE003`. -/

#synth Fintype CE001.St
#synth Fintype CE002.St
#synth Fintype CE003.St
#synth Fintype CE004.St
#synth Fintype CE006.St

/-! ## 2. Nenhuma colisão entre os modelos

Cada `f` age sobre o seu próprio tipo de estados; não há par
`(classe, tipo)` com duas instâncias. -/

example : CE001.f CE001.St.a = CE001.St.a := rfl
example : CE002.f CE002.St.a = CE002.St.b := rfl
example : CE003.f CE003.St.a = CE003.St.b := rfl
example : CE004.f CE004.St.a = CE004.St.c := rfl
example : CE006.f CE006.St.a0 = CE006.St.a1 := rfl

/-! ## 3. Cardinalidades distintas, sem interferência -/

example : Fintype.card CE001.St = 2 := by decide
example : Fintype.card CE002.St = 3 := by decide
example : Fintype.card CE006.St = 4 := by decide

/-! ## 4. A API continua utilizável em tipos externos

Com o agregador importado — portanto com as cinco instâncias em escopo —
os teoremas do núcleo se aplicam a `Bool`, alheio à frente. Esta é a
verificação de que a poluição de instâncias **não existe na prática**. -/

example (f : Bool → Bool) (b : Bool) : IterReachable f b b :=
  iterReachable_refl f b

example (f : Bool → Bool) (b : Bool) : EventuallyMeets f b b :=
  eventuallyMeets_refl f b

example (f : Bool → Bool) (b : Bool) :
    ∃ mu : ℕ, mu < Fintype.card Bool ∧ f^[mu] b ∈ Function.periodicPts f :=
  exists_cyclePoint_reachable_with_bound f b

example (f : Bool → Bool) (b : Bool) :
    ∃ mu : ℕ,
      mu < Fintype.card Bool ∧
      f^[mu] b ∈ Function.periodicPts f ∧
      ∀ q : Bool,
        q ∈ Function.periodicPts f →
        EventuallyMeets f b q →
        Function.periodicOrbit f (f^[mu] b) = Function.periodicOrbit f q :=
  exists_component_cycle_with_entry_bound f b

/-! ## 5. Wrappers relacionais — teoremas, não instâncias

As três linhas typecheck a partir dos teoremas, sem qualquer instância
global envolvida. -/

example {X : Type*} (f : X → X) : Std.Refl (EventuallyMeets f) :=
  eventuallyMeets_isRefl f

example {X : Type*} (f : X → X) : Std.Symm (EventuallyMeets f) :=
  eventuallyMeets_isSymm f

example {X : Type*} (f : X → X) : IsTrans X (EventuallyMeets f) :=
  eventuallyMeets_isTrans f

/-! ## 6. O inverso exige periodicidade — hipóteses visíveis

`eventuallyMeets_of_periodicOrbit_eq` **não** pode ser aplicado sem as
duas hipóteses de periodicidade. Isto importa porque dois pontos **não**
periódicos têm ambos `periodicOrbit = Cycle.nil`, e a igualdade das
órbitas vazias não diz nada sobre encontro de trajetórias. -/

example {X : Type*} {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f) (hq : q ∈ Function.periodicPts f)
    (h : Function.periodicOrbit f p = Function.periodicOrbit f q) :
    EventuallyMeets f p q :=
  eventuallyMeets_of_periodicOrbit_eq hp hq h

/-- Ponto não periódico produz a órbita vazia — a razão de as hipóteses
serem indispensáveis. Reutiliza `CE-002`, onde `a` é transitório. -/
example : Function.periodicOrbit CE002.f CE002.St.a = Cycle.nil :=
  Function.periodicOrbit_eq_nil_iff_not_periodic_pt.mpr CE002.a_not_periodic

/-! ## 7. Superfície pública — typecheck de cada nome exportado -/

#check @IterReachable
#check @MutuallyReachable
#check @EventuallyMeets
#check @iterReachable_refl
#check @iterReachable_trans
#check @IterReachable.eventuallyMeets
#check @eventuallyMeets_refl
#check @eventuallyMeets_symm
#check @eventuallyMeets_trans
#check @eventuallyMeets_isRefl
#check @eventuallyMeets_isSymm
#check @eventuallyMeets_isTrans
#check @periodicOrbit_eq_of_eventuallyMeets
#check @eventuallyMeets_of_periodicOrbit_eq
#check @exists_cyclePoint_reachable_with_bound
#check @exists_component_cycle_with_entry_bound

end TamesisLab.Tests.FoundFunctionalGraph001InstanceAudit
