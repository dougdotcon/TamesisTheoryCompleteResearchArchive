import TamesisLab.Foundations.FiniteStateAbstraction

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — testes formais

Seis casos. Nenhuma declaração destinada a falhar: o contrato deste
arquivo é terminar com código de saída zero.

O caso decisivo é `ABS-TEST-006`: a cadeia central elabora com
`C A : Type*` e **nenhuma** typeclass.
-/

namespace TamesisLab.Tests.FoundFiniteStateAbstraction001

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.FiniteStateAbstraction
open TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

/-! ## ABS-TEST-001 — orientação da semiconjugação, por `Iff.rfl` -/

example {C A : Type} (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Function.Semiconj abstract stepC stepA ↔ ∀ c, abstract (stepC c) = stepA (abstract c) :=
  Iff.rfl

/-! ## Instância positiva: identidade sobre `Fin 4` -/

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

/-- A abstração identidade: não perde informação nenhuma. -/
def idAbstraction : CertifiedFiniteAbstraction (Fin 4) (Fin 4) tailStep tailStep where
  abstract := id
  commutes := fun _ => rfl

/-- Toda abstração injetiva separa qualquer órbita.

Reconstruído aqui, e não exposto na API: ele é `DEFERRED_OPTIONAL`, e
este é o único lugar que o consome. -/
theorem orbitSeparating_of_injective {C A : Type*} {abstract : C → A}
    (hinj : Function.Injective abstract) (stepC : C → C) (start : C) :
    OrbitSeparating abstract stepC start :=
  fun _ _ h => hinj h

/-! ## ABS-TEST-002 — `iterate_commutes` instanciado -/

example (k : Nat) : idAbstraction.abstract ((tailStep^[k]) ⟨0, by decide⟩)
    = (tailStep^[k]) (idAbstraction.abstract ⟨0, by decide⟩) :=
  idAbstraction.iterate_commutes k ⟨0, by decide⟩

/-! ## ABS-TEST-003 — soundness observacional instanciada -/

example : idAbstraction.abstract ((tailStep^[2 + 2]) ⟨0, by decide⟩)
    = idAbstraction.abstract ((tailStep^[2]) ⟨0, by decide⟩) :=
  analyzeAbstractSystem_observational_sound
    (show analyzeAbstractSystem idAbstraction idEnc4 ⟨0, by decide⟩ = .ok ⟨2, 2⟩ by decide)

/-! ## ABS-TEST-004 — `OrbitSeparating` satisfeita por abstração injetiva -/

example : OrbitSeparating (id : Fin 4 → Fin 4) tailStep ⟨0, by decide⟩ :=
  orbitSeparating_of_injective Function.injective_id tailStep ⟨0, by decide⟩

/-! ## ABS-TEST-005 — reflexão concreta sob `OrbitSeparating` -/

example : tailStep^[2 + 2] ⟨0, by decide⟩ = tailStep^[2] ⟨0, by decide⟩ :=
  analyzeAbstractSystem_reflected_sound
    (orbitSeparating_of_injective Function.injective_id tailStep ⟨0, by decide⟩)
    (show analyzeAbstractSystem idAbstraction idEnc4 ⟨0, by decide⟩ = .ok ⟨2, 2⟩ by decide)

/-! ## ABS-TEST-006 — a cadeia central sem typeclass alguma

`C` e `A` são `Type*` sem instância. Nem `Fintype`, nem `Finite`, nem
`DecidableEq`, nem `Nonempty`, nem `Inhabited`. -/

example {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C) :
    ∃ witness, analyzeAbstractSystem abstraction encoding start = .ok witness :=
  analyzeAbstractSystem_complete abstraction encoding start

example {C A : Type*} {stepC : C → C} {stepA : A → A}
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA) (k : Nat) (start : C) :
    abstraction.abstract ((stepC^[k]) start) = (stepA^[k]) (abstraction.abstract start) :=
  abstraction.iterate_commutes k start

example {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}
    {abstraction : CertifiedFiniteAbstraction C A stepC stepA}
    {encoding : CertifiedFiniteEncoding A n} {start : C} {witness : CycleWitness}
    (hSep : OrbitSeparating abstraction.abstract stepC start)
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    (stepC^[witness.baseIndex + witness.period]) start = (stepC^[witness.baseIndex]) start :=
  analyzeAbstractSystem_reflected_sound hSep h

end TamesisLab.Tests.FoundFiniteStateAbstraction001
