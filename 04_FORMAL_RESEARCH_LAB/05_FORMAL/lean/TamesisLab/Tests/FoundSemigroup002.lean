import TamesisLab.Foundations.FiniteDynamics

set_option autoImplicit false

/-!
# Teste isolado — FOUND-SEMIGROUP-002 (núcleo)

Confirma assinaturas e hipóteses efetivamente exigidas. Nenhuma prova nova.
-/

namespace TamesisLab.Tests.FoundSemigroup002

open TamesisLab.Foundations.FiniteDynamics

/-! ## Camada A — alcançabilidade -/

example {M X : Type*} [Monoid M] [MulAction M X] (x : X) :
    Reachable (M := M) x x :=
  reachable_refl x

example {M X : Type*} [Monoid M] [MulAction M X] {x y z : X}
    (h₁ : Reachable (M := M) x y) (h₂ : Reachable (M := M) y z) :
    Reachable (M := M) x z :=
  reachable_trans h₁ h₂

/-- A ponte com `MulAction.orbit` é definicional. -/
example {M X : Type*} [Monoid M] [MulAction M X] {x y : X} :
    Reachable (M := M) x y ↔ y ∈ MulAction.orbit M x :=
  Iff.rfl

/-- Reflexividade e transitividade empacotadas, **sem** instância global. -/
example {M X : Type*} [Monoid M] [MulAction M X] :
    Std.Refl (fun a b : X => Reachable (M := M) a b) :=
  reachable_isRefl

example {M X : Type*} [Monoid M] [MulAction M X] :
    IsTrans X (fun a b : X => Reachable (M := M) a b) :=
  reachable_isTrans

/-! ## Camada A — invariantes -/

/-- Invariância total implica invariância sob cada elemento. **Implicação,
não equivalência**: a recíproca não é enunciada. -/
example {M X A : Type*} [Monoid M] [MulAction M X] {I : X → A}
    (hI : IsInvariant (M := M) I) (a : M) :
    IsInvariantUnder (M := M) a I :=
  hI.under a

example {M X A : Type*} [Monoid M] [MulAction M X] {I : X → A}
    (hI : IsInvariant (M := M) I) {x y : X} (h : Reachable (M := M) x y) :
    I y = I x :=
  hI.of_reachable h

example {M X A : Type*} [Monoid M] [MulAction M X] {a : M} {I : X → A}
    (hI : IsInvariantUnder (M := M) a I) (n : ℕ) (x : X) :
    I (a ^ n • x) = I x :=
  hI.pow n x

/-! ## Camada C — colisão, cauda, propagação -/

/-- A colisão limitada exige **apenas** `Fintype X`. -/
example {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        f^[mu + lam] x = f^[mu] x :=
  exists_bounded_iterate_collision f x

/-- O ponto periódico é `f^[mu] x`, **não** `x`. -/
example {X : Type*} (f : X → X) (x : X) {mu lam : ℕ}
    (h : f^[mu + lam] x = f^[mu] x) :
    Function.IsPeriodicPt f lam (f^[mu] x) :=
  periodic_tail_of_collision f x h

example {X : Type*} (f : X → X) (x : X) {mu lam : ℕ}
    (h : f^[mu + lam] x = f^[mu] x) (k : ℕ) :
    f^[mu + k + lam] x = f^[mu + k] x :=
  collision_propagates f x h k

/-! ## Camada C — teorema principal -/

example {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧
      0 < lam ∧
      mu + lam ≤ Fintype.card X ∧
      Function.IsPeriodicPt f lam (f^[mu] x) ∧
      ∀ k : ℕ, f^[mu + k + lam] x = f^[mu + k] x :=
  exists_eventual_period f x

/-- Hipóteses efetivamente usadas: **somente** `Fintype X`.
`DecidableEq X` **não** é fornecida aqui, e o teorema ainda se aplica. -/
example (f : Bool → Bool) (b : Bool) :
    ∃ mu lam : ℕ, 0 < lam ∧ f^[mu + lam] b = f^[mu] b := by
  obtain ⟨mu, lam, _, hlam, _, hcol⟩ := exists_bounded_iterate_collision f b
  exact ⟨mu, lam, hlam, hcol⟩

/-- E o teorema principal também se aplica, dando o ponto periódico da
cauda sem nenhuma hipótese além de `Fintype`. -/
example (f : Bool → Bool) (b : Bool) :
    ∃ mu lam : ℕ, 0 < lam ∧ Function.IsPeriodicPt f lam (f^[mu] b) := by
  obtain ⟨mu, lam, _, hlam, _, hper, _⟩ := exists_eventual_period f b
  exact ⟨mu, lam, hlam, hper⟩

/-! ## Camada B — corolário para ações -/

/-- Sem `Fintype M`, sem `DecidableEq X`, sem `Group M`. -/
example {M X : Type*} [Monoid M] [Fintype X] [MulAction M X] (a : M) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        a ^ (mu + lam) • x = a ^ mu • x :=
  monoid_element_eventually_periodic a x

example {M X : Type*} [Monoid M] [Fintype X] [MulAction M X] (a : M) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        ∀ k : ℕ, a ^ (mu + k + lam) • x = a ^ (mu + k) • x :=
  monoid_element_eventual_period_propagates a x

/-! ## Assinaturas — inspeção explícita -/

#check @exists_eventual_period
#check @monoid_element_eventually_periodic

end TamesisLab.Tests.FoundSemigroup002
