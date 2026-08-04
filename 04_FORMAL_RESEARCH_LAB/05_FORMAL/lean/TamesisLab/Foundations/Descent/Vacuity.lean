import TamesisLab.Foundations.Monovariants

set_option autoImplicit false

/-!
# LAB-CORR-MONOVARIANT-VACUITY-001 — a vacuidade, como teorema

`FOUND-MONOVARIANT-DESCENT-001` publicou

```lean
def Monovariant (measure : C → Nat) (stepC : C → C) : Prop :=
  ∀ c : C, measure (stepC c) < measure c
```

e essa definição é **vácua**: ela só pode valer quando `C` é vazio.

O argumento cabe numa linha. Se `C` é habitado, a imagem de `measure` em
`Nat` é um conjunto não vazio de naturais, logo tem mínimo. A hipótese
exige, no estado que realiza esse mínimo, um valor estritamente menor —
e esse valor também está na imagem.

Este módulo **não modifica** a frente encerrada. Ele consome a definição
publicada e prova o que ela implica. A vacuidade passa a ser fato
verificável no repositório, e não errata em prosa.
-/

namespace TamesisLab.Foundations.Descent

open TamesisLab.Foundations.Monovariants

variable {C : Type*}

/-- **A definição publicada implica que o tipo é vazio.**

Sem depender de axioma nenhum. -/
theorem monovariant_forces_empty {measure : C → Nat} {stepC : C → C}
    (h : Monovariant measure stepC) : IsEmpty C := by
  constructor
  intro c
  have key : ∀ n : Nat, ∀ x : C, measure x ≠ n := by
    intro n
    induction n using Nat.strong_induction_on with
    | _ n ih =>
      intro x hx
      exact ih (measure (stepC x)) (hx ▸ h x) (stepC x) rfl
  exact key (measure c) c rfl

/-- Nenhum tipo habitado admite a hipótese publicada. -/
theorem no_monovariant_on_inhabited {measure : C → Nat} {stepC : C → C}
    (c : C) (h : Monovariant measure stepC) : False :=
  (monovariant_forces_empty h).false c

end TamesisLab.Foundations.Descent
