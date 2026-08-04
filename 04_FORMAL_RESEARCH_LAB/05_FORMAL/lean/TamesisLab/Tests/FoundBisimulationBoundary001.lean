import TamesisLab.Foundations.BisimulationBoundary

set_option autoImplicit false

/-!
# FOUND-BISIMULATION-BOUNDARY-001 — testes formais

Oito casos. Nenhuma declaração destinada a falhar.

O par decisivo é `BIS-TEST-004` com `BIS-TEST-006`: o contraexemplo
**é** uma bissimulação, e bissimulação **não** reflete ciclos.

Não há testes executáveis: a frente é inteiramente proposicional e não
introduz função computável alguma.
-/

namespace TamesisLab.Tests.FoundBisimulationBoundary001

open TamesisLab.Foundations.BisimulationBoundary
open TamesisLab.Foundations.FiniteStateAbstraction
open TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

/-! ## BIS-TEST-001 — o zig é a semiconjugação, por `Iff.rfl` -/

example {C A : Type} (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Simulates abstract stepC stepA ↔ Function.Semiconj abstract stepC stepA :=
  Iff.rfl

/-- A existencial do zag continua no lugar: `STOP-BIS-002` não disparada. -/
example {C A : Type} (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Reflects abstract stepC stepA
      ↔ ∀ c : C, ∃ c' : C, stepC c = c' ∧ abstract c' = stepA (abstract c) :=
  Iff.rfl

/-! ## BIS-TEST-002 — o zag equivale ao zig, instanciado -/

example : Reflects forgetBool concreteStep abstractStep :=
  (reflects_iff_simulates forgetBool concreteStep abstractStep).mpr boolToUnit_semiconj

/-! ## BIS-TEST-003 — o colapso, instanciado -/

example : Bisimulation forgetBool concreteStep abstractStep ↔
    Function.Semiconj forgetBool concreteStep abstractStep :=
  bisimulation_iff_semiconj forgetBool concreteStep abstractStep

/-! ## BIS-TEST-004 — `BOOL_TO_UNIT` é uma bissimulação -/

example : Bisimulation forgetBool concreteStep abstractStep :=
  boolToUnit_bisimulation

/-! ## BIS-TEST-005 — e a abstração é sobrejetiva -/

example : Function.Surjective forgetBool :=
  forgetBool_surjective

/-! ## BIS-TEST-006 — bissimulação NÃO reflete ciclos -/

example : ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
      Bisimulation abstract stepC stepA →
      ∀ start : C, abstract (stepC start) = abstract start → stepC start = start) :=
  bisimulation_does_not_reflect_cycles

/-! ## BIS-TEST-007 — nem bissimulação sobrejetiva -/

example : ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
      Function.Surjective abstract →
      Bisimulation abstract stepC stepA →
      ∀ start : C, abstract (stepC start) = abstract start → stepC start = start) :=
  surjective_bisimulation_does_not_reflect_cycles

/-- A fronteira permanece exatamente onde estava: ser bissimulação não
faz `OrbitSeparating` valer. -/
example : Bisimulation forgetBool concreteStep abstractStep ∧
    ¬ OrbitSeparating forgetBool concreteStep false :=
  ⟨boolToUnit_bisimulation, boolToUnit_not_orbitSeparating⟩

/-! ## BIS-TEST-008 — a cadeia central sem typeclass alguma -/

example {C A : Type*} (abstract : C → A) (stepC : C → C) (stepA : A → A)
    (h : Function.Semiconj abstract stepC stepA) :
    Bisimulation abstract stepC stepA :=
  (bisimulation_iff_semiconj abstract stepC stepA).mpr h

example {C A : Type*} (abstract : C → A) (stepC : C → C) (stepA : A → A)
    (h : Bisimulation abstract stepC stepA) :
    Reflects abstract stepC stepA :=
  h.2

end TamesisLab.Tests.FoundBisimulationBoundary001
