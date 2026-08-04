import TamesisLab.Foundations.Monovariants

set_option autoImplicit false

/-!
# LAB-CORR-MONOVARIANT-VACUITY-001 — a forma corrigida

O argumento clássico de monovariante **nunca** exigiu decrescimento em
todo estado. Exigiu decrescimento **enquanto o sistema não parou**.

```text
vacuo      medida decresce em TODO estado
corrigido  medida decresce ENQUANTO P vale
```

A conclusão certa também não é "não há ciclo": é **o sistema sai da
região `P` em um número finito de passos**. Terminação, não ausência de
recorrência.
-/

namespace TamesisLab.Foundations.Descent

variable {C : Type*}

/-- A medida decresce **enquanto** `P` vale. -/
def DescendsOn (measure : C → Nat) (stepC : C → C) (P : C → Prop) : Prop :=
  ∀ c : C, P c → measure (stepC c) < measure c

/-- **O teorema de terminação.**

A partir de qualquer estado, o sistema sai da região `P` em um número
finito de passos. Não é vácuo, e é o conteúdo real do argumento. -/
theorem DescendsOn.exits {measure : C → Nat} {stepC : C → C} {P : C → Prop}
    (h : DescendsOn measure stepC P) :
    ∀ c : C, ∃ k : Nat, ¬ P ((stepC^[k]) c) := by
  have key : ∀ n : Nat, ∀ c : C, measure c = n → ∃ k : Nat, ¬ P ((stepC^[k]) c) := by
    intro n
    induction n using Nat.strong_induction_on with
    | _ n ih =>
      intro c hc
      by_cases hp : P c
      · obtain ⟨k, hk⟩ := ih (measure (stepC c)) (hc ▸ h c hp) (stepC c) rfl
        exact ⟨k + 1, by rwa [Function.iterate_succ_apply]⟩
      · exact ⟨0, by simpa using hp⟩
  intro c
  exact key (measure c) c rfl

end TamesisLab.Foundations.Descent
