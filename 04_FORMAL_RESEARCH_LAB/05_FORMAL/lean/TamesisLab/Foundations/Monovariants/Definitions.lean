import Mathlib.Logic.Function.Iterate

set_option autoImplicit false

/-!
# FOUND-MONOVARIANT-DESCENT-001 — descida

A segunda metade do par clássico. Um invariante prova que algo **não
muda**; um monovariante prova que algo **decresce**.

A medida tem valores em `Nat`, e só em `Nat`. A boa fundação vem de
graça, nenhuma typeclass é exigida, e o resultado é o monovariante
clássico. Ordens gerais e ordinais ficam fora do recorte.

Atenção ao que **não** vale: boa fundação do contradomínio não substitui
decrescimento estrito. `Instance.lean` registra o contraexemplo.
-/

namespace TamesisLab.Foundations.Monovariants

variable {C : Type*}

/-- Uma medida que **decresce estritamente** a cada passo. -/
def Monovariant (measure : C → Nat) (stepC : C → C) : Prop :=
  ∀ c : C, measure (stepC c) < measure c

/-- A medida decresce ao longo de qualquer número positivo de passos. -/
theorem Monovariant.iterate_lt {measure : C → Nat} {stepC : C → C}
    (h : Monovariant measure stepC) :
    ∀ k : Nat, 0 < k → ∀ c : C, measure ((stepC^[k]) c) < measure c := by
  intro k
  induction k with
  | zero => intro hk; exact absurd hk (Nat.lt_irrefl 0)
  | succ m ih =>
    intro _ c
    rcases Nat.eq_zero_or_pos m with hm | hm
    · subst hm
      simpa using h c
    · have hstep : measure ((stepC^[m]) (stepC c)) < measure (stepC c) := ih hm (stepC c)
      have hlt : measure (stepC c) < measure c := h c
      rw [Function.iterate_succ_apply]
      omega

/-- **Não há ponto periódico algum.**

Um monovariante exclui recorrência concreta em qualquer número positivo
de passos. Nenhuma finitude é usada. -/
theorem Monovariant.no_periodic_point {measure : C → Nat} {stepC : C → C}
    (h : Monovariant measure stepC) {k : Nat} (hk : 0 < k) (c : C) :
    (stepC^[k]) c ≠ c := by
  intro heq
  have hlt := h.iterate_lt k hk c
  rw [heq] at hlt
  exact absurd hlt (Nat.lt_irrefl _)

/-- Nenhum estado se alcança de volta. -/
theorem Monovariant.not_reachable_self {measure : C → Nat} {stepC : C → C}
    (h : Monovariant measure stepC) (c : C) :
    ¬ ∃ k : Nat, 0 < k ∧ (stepC^[k]) c = c := by
  rintro ⟨k, hk, heq⟩
  exact h.no_periodic_point hk c heq

end TamesisLab.Foundations.Monovariants
