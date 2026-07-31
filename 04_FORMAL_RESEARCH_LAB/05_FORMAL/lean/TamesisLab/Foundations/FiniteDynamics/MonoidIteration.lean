import TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity
import Mathlib.Algebra.Group.Action.Defs

set_option autoImplicit false

/-!
# FOUND-SEMIGROUP-002 — Iteração de um elemento (Camada B)

Corolário **derivado** da Camada C. A casa dos pombos **não** é reaplicada:
o resultado funcional é transportado para a linguagem da ação por
`smul_iterate_apply`.

Hipóteses deliberadamente ausentes: `Fintype M`, `DecidableEq X`,
`Group M`. A finitude usada é a de `X`, e só ela.
-/

namespace TamesisLab.Foundations.FiniteDynamics

/-- FSG2-ACT-001 — a iteração de um elemento de monoide sobre um tipo
finito é eventualmente periódica, com os mesmos limitantes.

Derivado de `exists_bounded_iterate_collision` aplicado a `fun y => a • y`,
via `smul_iterate_apply : (a • ·)^[n] x = a ^ n • x`. -/
theorem monoid_element_eventually_periodic {M X : Type*} [Monoid M]
    [Fintype X] [MulAction M X] (a : M) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧
      0 < lam ∧
      mu + lam ≤ Fintype.card X ∧
      a ^ (mu + lam) • x = a ^ mu • x := by
  obtain ⟨mu, lam, hmu, hlam, hsum, hcol⟩ :=
    exists_bounded_iterate_collision (fun y : X => a • y) x
  refine ⟨mu, lam, hmu, hlam, hsum, ?_⟩
  rw [← smul_iterate_apply a (mu + lam) x, ← smul_iterate_apply a mu x]
  exact hcol

/-- FSG2-ACT-002 — versão com propagação, composição curta da API já
provada. -/
theorem monoid_element_eventual_period_propagates {M X : Type*} [Monoid M]
    [Fintype X] [MulAction M X] (a : M) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧
      0 < lam ∧
      mu + lam ≤ Fintype.card X ∧
      ∀ k : ℕ, a ^ (mu + k + lam) • x = a ^ (mu + k) • x := by
  obtain ⟨mu, lam, hmu, hlam, hsum, hcol⟩ :=
    exists_bounded_iterate_collision (fun y : X => a • y) x
  refine ⟨mu, lam, hmu, hlam, hsum, fun k => ?_⟩
  rw [← smul_iterate_apply a (mu + k + lam) x, ← smul_iterate_apply a (mu + k) x]
  exact collision_propagates (fun y : X => a • y) x hcol k

end TamesisLab.Foundations.FiniteDynamics
