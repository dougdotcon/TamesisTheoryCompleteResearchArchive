import TamesisLab.Foundations.FiniteDynamics

set_option autoImplicit false

/-!
# Teste isolado — FOUND-SEMIGROUP-002 (contraexemplos)

Confirma os cinco contraexemplos e o que cada um refuta.

Nenhum deles usa `native_decide`. Todos os `decide` verificam termos
finitos pequenos e transparentes.
-/

namespace TamesisLab.Tests.FoundSemigroup002Counterexamples

open TamesisLab.Foundations.FiniteDynamics
open TamesisLab.Foundations.FiniteDynamics.Counterexamples

/-! ## CE-001 — alcançabilidade não é simétrica

Ação **genuína de monoide**, não apenas uma função. -/

example : Monoid CE001.Tr := inferInstance
example : MulAction CE001.Tr CE001.St := inferInstance

example : Reachable (M := CE001.Tr) CE001.St.zero CE001.St.one :=
  CE001.reachable_zero_one

example : ¬ Reachable (M := CE001.Tr) CE001.St.one CE001.St.zero :=
  CE001.not_reachable_one_zero

example :
    Reachable (M := CE001.Tr) CE001.St.zero CE001.St.one ∧
      ¬ Reachable (M := CE001.Tr) CE001.St.one CE001.St.zero :=
  CE001.reachable_not_symmetric

/-! ## CE-002 — ação finita não precisa ser transitiva -/

example : ∃ x y : CE002.St, ¬ Reachable (M := CE002.Tr) x y :=
  CE002.not_transitive

/-! ## CE-003 — cauda antes do ciclo -/

example : CE003.f CE003.St.s0 ≠ CE003.St.s0 := CE003.not_fixed

example : CE003.f^[1] CE003.St.s0 = CE003.St.s1 := CE003.iterate_one

example : CE003.f^[2] CE003.St.s0 = CE003.St.s2 := CE003.iterate_two

example : CE003.f^[2 + 1] CE003.St.s0 = CE003.f^[2] CE003.St.s0 :=
  CE003.eventually_fixed

/-- O estado inicial não é periódico para período positivo algum, embora a
trajetória seja eventualmente periódica. -/
example : ¬ ∃ n : ℕ, 0 < n ∧ CE003.f^[n] CE003.St.s0 = CE003.St.s0 :=
  CE003.s0_not_periodic

/-- O ponto periódico é o da cauda, `f^[2] s0`. -/
example : Function.IsPeriodicPt CE003.f 1 (CE003.f^[2] CE003.St.s0) :=
  CE003.periodic_point_is_tail

/-- O teorema principal se aplica ao modelo com cauda. -/
example :
    ∃ mu lam : ℕ,
      mu < Fintype.card CE003.St ∧
      0 < lam ∧
      mu + lam ≤ Fintype.card CE003.St ∧
      Function.IsPeriodicPt CE003.f lam (CE003.f^[mu] CE003.St.s0) ∧
      ∀ k : ℕ,
        CE003.f^[mu + k + lam] CE003.St.s0 = CE003.f^[mu + k] CE003.St.s0 :=
  exists_eventual_period CE003.f CE003.St.s0

/-! ## CE-004 — ação finita não precisa ser fiel -/

example : ∃ a b : CE001.Tr, a ≠ b ∧ ∀ s : CE004.St, a • s = b • s :=
  CE004.not_faithful

/-! ## CE-005 — invariante não separa órbitas -/

example :
    IsInvariant (M := CE002.Tr) CE005.I ∧
      CE005.I CE002.St.a = CE005.I CE002.St.b ∧
      ¬ Reachable (M := CE002.Tr) CE002.St.a CE002.St.b :=
  CE005.invariant_does_not_separate_orbits

/-! ## Fronteira com o modelo C3

Quatro propriedades verificadas em `FOUND-SEMIGROUP-001` para o modelo `C3`
— fidelidade, transitividade, simetria da alcançabilidade e ausência de
cauda — **não** são consequências gerais de uma ação finita de monoide.
Cada uma tem aqui um contraexemplo. Isto **não** afirma que as quatro
falhem simultaneamente em toda ação. -/

example : ¬ Reachable (M := CE002.Tr) CE002.St.a CE002.St.b :=
  CE002.not_reachable_a_b

end TamesisLab.Tests.FoundSemigroup002Counterexamples
