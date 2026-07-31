import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Logic.Function.Iterate
import Mathlib.Dynamics.PeriodicPts.Defs

set_option autoImplicit false

/-!
# FOUND-SEMIGROUP-002 — Periodicidade eventual (Camada C)

**Camada C: nenhum monoide.** Todo este arquivo fala apenas de uma função
`f : X → X` sobre um tipo finito. A periodicidade eventual depende somente
da finitude de `X` e da iteração de `f`; exigir um monoide aqui seria
hipótese ociosa.

A casa dos pombos é usada **uma única vez**, em
`exists_bounded_iterate_collision`. Todo o resto é composição.

## Por que não `Function.minimalPeriod`

`minimalPeriod f x` devolve `0` quando `x` **não** é periódico, e
`IsPeriodicPt f n x` significa `f^[n] x = x` — retorno ao ponto
**inicial**. Numa trajetória com cauda (ver `CE-003`) o ponto inicial não é
periódico. O ponto periódico é `f^[μ] x`, **não** `x`; é isso que
`periodic_tail_of_collision` enuncia.
-/

namespace TamesisLab.Foundations.FiniteDynamics

/-- Auxiliar: normaliza um par de índices já ordenado num par `(μ, λ)`. -/
private theorem eventual_period_of_lt {X : Type*} [Fintype X]
    (f : X → X) (x : X) {i j : ℕ}
    (hlt : i < j) (hj : j ≤ Fintype.card X)
    (h : f^[i] x = f^[j] x) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        f^[mu + lam] x = f^[mu] x := by
  refine ⟨i, j - i, by omega, by omega, by omega, ?_⟩
  have hij : i + (j - i) = j := by omega
  rw [hij, h]

/-- FSG2-PER-001 — **casa dos pombos**: a trajetória colide dentro dos
primeiros `Fintype.card X + 1` índices, e a colisão fornece
`μ < card X`, `0 < λ` e `μ + λ ≤ card X`.

`DecidableEq X` **não** é necessária: o lema de pigeonhole usado
(`Fintype.exists_ne_map_eq_of_card_lt`) não a exige. -/
theorem exists_bounded_iterate_collision {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
        f^[mu + lam] x = f^[mu] x := by
  obtain ⟨i, j, hne, hEq⟩ :=
    Fintype.exists_ne_map_eq_of_card_lt
      (fun k : Fin (Fintype.card X + 1) => f^[(k : ℕ)] x)
      (by simp)
  rcases lt_or_gt_of_ne hne with h | h
  · exact eventual_period_of_lt f x h (Nat.lt_succ_iff.mp j.isLt) hEq
  · exact eventual_period_of_lt f x h (Nat.lt_succ_iff.mp i.isLt) hEq.symm

/-- FSG2-PER-004 — o ponto **da cauda** `f^[μ] x` é periódico no sentido da
Mathlib, com período `λ`.

Note o argumento: `f^[μ] x`, e **não** `x`. Em `CE-003` o ponto inicial não
é periódico. -/
theorem periodic_tail_of_collision {X : Type*} (f : X → X) (x : X) {mu lam : ℕ}
    (h : f^[mu + lam] x = f^[mu] x) :
    Function.IsPeriodicPt f lam (f^[mu] x) := by
  show f^[lam] (f^[mu] x) = f^[mu] x
  rw [← Function.iterate_add_apply f lam mu x, Nat.add_comm lam mu]
  exact h

/-- FSG2-PER-003 — a colisão **propaga-se** a todos os índices posteriores.

Derivado da colisão, sem reprovar a casa dos pombos. -/
theorem collision_propagates {X : Type*} (f : X → X) (x : X) {mu lam : ℕ}
    (h : f^[mu + lam] x = f^[mu] x) (k : ℕ) :
    f^[mu + k + lam] x = f^[mu + k] x := by
  have h₁ : mu + k + lam = k + (mu + lam) := by omega
  have h₂ : mu + k = k + mu := by omega
  rw [h₁, h₂, Function.iterate_add_apply f k (mu + lam) x,
    Function.iterate_add_apply f k mu x, h]

/-- FSG2-PER-002 — **teorema principal**.

Toda trajetória de uma função sobre um tipo finito é eventualmente
periódica, com limitantes em `Fintype.card X`, ponto periódico explícito na
cauda e propagação a todos os índices posteriores.

A prova é **composição** de `exists_bounded_iterate_collision`,
`periodic_tail_of_collision` e `collision_propagates`. A casa dos pombos
não é repetida.

Não se afirma unicidade de `μ`, minimalidade de `λ`, nem decomposição
canônica em cauda e ciclo. -/
theorem exists_eventual_period {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ mu lam : ℕ,
      mu < Fintype.card X ∧
      0 < lam ∧
      mu + lam ≤ Fintype.card X ∧
      Function.IsPeriodicPt f lam (f^[mu] x) ∧
      ∀ k : ℕ, f^[mu + k + lam] x = f^[mu + k] x := by
  obtain ⟨mu, lam, hmu, hlam, hsum, hcol⟩ :=
    exists_bounded_iterate_collision f x
  exact ⟨mu, lam, hmu, hlam, hsum,
    periodic_tail_of_collision f x hcol,
    collision_propagates f x hcol⟩

end TamesisLab.Foundations.FiniteDynamics
