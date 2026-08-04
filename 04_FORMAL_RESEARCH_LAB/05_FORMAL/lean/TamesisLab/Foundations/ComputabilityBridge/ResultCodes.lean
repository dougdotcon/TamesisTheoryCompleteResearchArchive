import TamesisLab.Foundations.ComputabilityBridge.Encoding

set_option autoImplicit false

/-!
# FOUND-COMPUTABILITY-BRIDGE-001 — codificar o resultado

Sem estas quatro instâncias o enunciado central **não é escrevível**:
`Primrec f` exige `Primcodable` no contradomínio, e o contradomínio da
análise é `Except RuntimeCycleError CycleWitness`.

```text
CycleWitness           ~ Nat x Nat
RuntimeCycleError      ~ Bool + (Nat x Nat)
Except e a             ~ e + a
RawTransitionTable     ~ List Nat
```

Nenhum construtor é descartado. `RuntimeCycleError` tem três
construtores, e os dois sem argumento viram `false` e `true` porque o
Mathlib não oferece `Primcodable Unit` que tornasse a soma tripla mais
natural.

`RawTransitionTable` entra aqui **apenas** para que o nível uniforme
seja enunciável em `Classification.lean`. Nada é provado sobre ele.
-/

namespace TamesisLab.Foundations.ComputabilityBridge

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

/-- O certificado é um par de naturais, e nada mais. -/
def cycleWitnessEquiv : CycleWitness ≃ (Nat × Nat) where
  toFun := fun w => (w.baseIndex, w.period)
  invFun := fun p => ⟨p.1, p.2⟩
  left_inv := fun _ => rfl
  right_inv := fun _ => rfl

instance instPrimcodableCycleWitness : Primcodable CycleWitness :=
  Primcodable.ofEquiv _ cycleWitnessEquiv

/-- Os três construtores de erro, sem perda. -/
def runtimeCycleErrorEquiv : RuntimeCycleError ≃ (Bool ⊕ (Nat × Nat)) where
  toFun := fun err =>
    match err with
    | .transitionDestinationOutOfBounds => .inl false
    | .internalDetectorFailure => .inl true
    | .initialStateOutOfBounds a b => .inr (a, b)
  invFun := fun x =>
    match x with
    | .inl false => .transitionDestinationOutOfBounds
    | .inl true => .internalDetectorFailure
    | .inr p => .initialStateOutOfBounds p.1 p.2
  left_inv := by intro err; cases err <;> rfl
  right_inv := by rintro (b | p) <;> [cases b; skip] <;> rfl

instance instPrimcodableRuntimeCycleError : Primcodable RuntimeCycleError :=
  Primcodable.ofEquiv _ runtimeCycleErrorEquiv

/-- `Except` é a soma, e o Mathlib já sabe codificar somas. -/
def exceptEquiv (ε α : Type*) : Except ε α ≃ (ε ⊕ α) where
  toFun := fun x => match x with | .error e => .inl e | .ok a => .inr a
  invFun := fun x => match x with | .inl e => .error e | .inr a => .ok a
  left_inv := by intro x; cases x <;> rfl
  right_inv := by intro x; cases x <;> rfl

instance instPrimcodableExcept {ε α : Type*} [Primcodable ε] [Primcodable α] :
    Primcodable (Except ε α) :=
  Primcodable.ofEquiv _ (exceptEquiv ε α)

/-- A tabela bruta é uma lista de naturais.

Existe para tornar o **nível uniforme** enunciável. Nada é provado sobre
ele nesta frente — ver `CB-GAP-001`. -/
def rawTableEquiv : RawTransitionTable ≃ List Nat where
  toFun := fun t => t.next.toList
  invFun := fun l => ⟨l.toArray⟩
  left_inv := by intro t; cases t; simp
  right_inv := by intro l; simp

instance instPrimcodableRawTransitionTable : Primcodable RawTransitionTable :=
  Primcodable.ofEquiv _ rawTableEquiv

end TamesisLab.Foundations.ComputabilityBridge
