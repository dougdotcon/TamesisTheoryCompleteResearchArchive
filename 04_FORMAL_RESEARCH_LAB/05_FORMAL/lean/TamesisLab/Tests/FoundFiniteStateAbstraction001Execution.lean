import TamesisLab.Foundations.FiniteStateAbstraction

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — testes executáveis

Cinco casos, por `decide` e `rfl`. A avaliação nativa **não** é usada:
ela acrescentaria um axioma de redução à pegada.

O par decisivo é `ABS-TEST-009` contra `ABS-TEST-010`: a mesma trajetória
repete no abstrato e **não** repete no concreto.
-/

namespace TamesisLab.Tests.FoundFiniteStateAbstraction001Execution

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.FiniteStateAbstraction
open TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

/-! ## ABS-TEST-007 — `BOOL_TO_UNIT` devolve certificado -/

example : analyzeAbstractSystem boolToUnitAbstraction unitEncoding false = .ok ⟨0, 1⟩ := by decide

example : analyzeAbstractSystem boolToUnitAbstraction unitEncoding true = .ok ⟨0, 1⟩ := by decide

/-! ## ABS-TEST-008 — abstração identidade sobre `Fin 4` -/

/-- Codificação identidade sobre `Fin 4`. -/
def idEnc4 : CertifiedFiniteEncoding (Fin 4) 4 where
  encode := id
  decode := id
  decode_encode := by decide
  encode_decode := by decide

/-- `0 → 1 → 2 → 3 → 2`. -/
def tailStep : Fin 4 → Fin 4
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩
  | ⟨2, _⟩ => ⟨3, by decide⟩
  | _ => ⟨2, by decide⟩

/-- A abstração identidade. -/
def idAbstraction : CertifiedFiniteAbstraction (Fin 4) (Fin 4) tailStep tailStep where
  abstract := id
  commutes := fun _ => rfl

example : analyzeAbstractSystem idAbstraction idEnc4 ⟨0, by decide⟩ = .ok ⟨2, 2⟩ := by decide

/-! ## ABS-TEST-009 — a recorrência abstrata vale -/

example : forgetBool (concreteStep false) = forgetBool false := rfl

example : forgetBool ((concreteStep^[0 + 1]) false) = forgetBool ((concreteStep^[0]) false) :=
  analyzeAbstractSystem_observational_sound
    (show analyzeAbstractSystem boolToUnitAbstraction unitEncoding false = .ok ⟨0, 1⟩ by decide)

/-! ## ABS-TEST-010 — a recorrência concreta não vale -/

example : concreteStep false ≠ false := by decide

example : concreteStep true ≠ true := by decide

/-! ## ABS-TEST-011 — `OrbitSeparating` falha no contraexemplo -/

example : ¬ OrbitSeparating forgetBool concreteStep false :=
  boolToUnit_not_orbitSeparating

example : ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
      Function.Semiconj abstract stepC stepA →
      ∀ start : C, abstract (stepC start) = abstract start → stepC start = start) :=
  naive_cycle_reflection_is_false

end TamesisLab.Tests.FoundFiniteStateAbstraction001Execution
