import TamesisLab.Foundations.FiniteStateAbstraction.OrbitSeparation

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — `BOOL_TO_UNIT`

O contraexemplo que mede a força exata do resultado observacional.

```text
C = Bool     stepC = Bool.not
A = Unit     stepA = id
abstract     constante
```

```text
a semiconjugacao          VALE
a recorrencia abstrata    VALE, periodo 1
a recorrencia concreta    NAO vale
OrbitSeparating           FALHA
```

Ele **não** denuncia defeito da semiconjugação. Ele exibe exatamente a
perda de informação que uma abstração existe para produzir.

Todo resultado negativo aqui é uma **negação provada**, nunca um arquivo
destinado a falhar: o contrato deste módulo é compilar.
-/

namespace TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Foundations.FiniteStateAbstraction

/-- O passo concreto: alterna entre `false` e `true`. Nunca repete. -/
def concreteStep : Bool → Bool := Bool.not

/-- O passo abstrato: um único estado, que repete em um passo. -/
def abstractStep : Unit → Unit := id

/-- A abstração que esquece tudo. -/
def forgetBool : Bool → Unit := fun _ => ()

/-- A semiconjugação **vale**: esquecer depois de alternar é o mesmo que
não fazer nada depois de esquecer. -/
theorem boolToUnit_semiconj : Function.Semiconj forgetBool concreteStep abstractStep := by
  intro b
  cases b <;> rfl

/-- A abstração certificada correspondente. -/
def boolToUnitAbstraction : CertifiedFiniteAbstraction Bool Unit concreteStep abstractStep where
  abstract := forgetBool
  commutes := boolToUnit_semiconj

/-- `Unit` codificado em `Fin 1`, explicitamente. -/
def unitEncoding : CertifiedFiniteEncoding Unit 1 where
  encode := fun _ => ⟨0, by decide⟩
  decode := fun _ => ()
  decode_encode := fun _ => rfl
  encode_decode := by decide

/-- A recorrência **observacional** vale, com período abstrato `1`. -/
theorem boolToUnit_abstract_recurrence : forgetBool (concreteStep false) = forgetBool false := rfl

/-- A recorrência **concreta** não vale. -/
theorem boolToUnit_no_concrete_recurrence : concreteStep false ≠ false := by decide

/-- `OrbitSeparating` **falha**, nos índices `0` e `1`.

Este é o teorema que torna a condição não tautológica: a semiconjugação
vale aqui, e a separação não. Se a separação decorresse da
semiconjugação, valeria também. -/
theorem boolToUnit_not_orbitSeparating : ¬ OrbitSeparating forgetBool concreteStep false :=
  fun hsep => boolToUnit_no_concrete_recurrence (hsep 1 0 rfl)

/-- A reflexão ingênua é **falsa**, em geral.

Semiconjugação mais ciclo abstrato não produz ciclo concreto. -/
theorem naive_cycle_reflection_is_false :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Function.Semiconj abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start) :=
  fun h => boolToUnit_no_concrete_recurrence
    (h Bool Unit concreteStep abstractStep forgetBool boolToUnit_semiconj false rfl)

end TamesisLab.Foundations.FiniteStateAbstraction.Counterexample
